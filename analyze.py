#!/usr/bin/env python3
"""The study's analysis, as PROTOCOL.md section 7 defines it. Written and committed before any study look was read
(11 November 2026).

    python3 analyze.py --labels <labels.csv> --looks <dir> --ratings <datasets/ratings> [--relabel <csv>] [--out results]

--looks is the runner's output folder: <dir>/2.3.7/ (critic A) and <dir>/2.3.10/ (critic B), one JSON file a look; first
looks have ids original/<round>/<film>, second looks second/<round>/<film>. --ratings holds <round>/ratings.json with
Angelina's 1-5 rating of each film. --relabel (later) is her second labelling of the 30 reliability decisions (key,label).
Writes <out>/decisions.csv, <out>/films.csv, <out>/summary.json and <out>/summary.md. Cases appear only as A-D.

Written with Claude for "Does Tev's AI critic flag what an editor flags?".
"""
import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import beta, spearmanr

from draw import LEFT_OUT, SEED

CRITICS = {"A": "2.3.7", "B": "2.3.10"}
KINDS = ("zoom", "title")
WIDEN = 0.5          # section 7: a decision's time, widened by 0.5 s on each side
RELEASE = 0.85       # section 3: a score of 0.85 or more releases the film
BOOT = 10_000        # section 7: bootstrap resamples of films
CHANCE_DRAWS = 1_000
CASES = {}  # case name -> A-D, by the names' alphabetical order, filled from the labels (so no name is written here)

# Section 7: the words that name a decision's kind ("punch in" and "push in" added before freezing, 11 November).
WORDS = {
    "zoom": re.compile(r"\bzoom|\bpunch[- ]?in\b|\bpush[- ]?in\b", re.I),
    "title": re.compile(r"\btitles?\b|\btexts?\b|\bcards?\b|\bheadings?\b", re.I),
}
# Sensitivity only (added after freezing, before any study look was read; section 11): in the pilot, critic A called a
# title a "label" and quoted its words without the word "title".
EXTRA_TITLE = re.compile(r"\blabels?\b", re.I)
QUOTED = re.compile(r"[\"“”'‘’]([^\"“”'‘’]{3,})[\"“”'‘’]")


# ---- reading ----

class Decision:
    def __init__(self, row):
        self.key, self.kind, self.round, self.film = row["key"], row["kind"], row["round"], row["film"]
        self.start, self.end = float(row["start_s"]), float(row["end_s"])
        self.label, self.case = row["label"], CASES.get(row["case"], "?")

    @property
    def filmkey(self):
        return f"{self.round}/{self.film}"

    def counts_for(self, critic):
        return self.kind not in LEFT_OUT[critic].get((self.round, self.film), set())


def read_looks(folder):
    looks = {}
    for path in sorted(Path(folder).glob("*.json")):
        d = json.loads(path.read_text())
        looks[d["look"]["id"]] = d
    return looks


def duration_of(look):
    m = re.search(r"FILM (\d+(?:\.\d+)?) s", look.get("facts") or "")
    return float(m.group(1)) if m else None


def titles_of(look):
    return [re.sub(r"\s+", " ", t["text"]).strip().lower() for t in look["look"].get("titles", [])]


# ---- what a change or a verdict names ----

def kinds_named(text, titles, extended):
    kinds = {k for k, rx in WORDS.items() if rx.search(text)}
    if extended:
        if EXTRA_TITLE.search(text):
            kinds.add("title")
        for quote in QUOTED.findall(text):
            q = re.sub(r"\s+", " ", quote).strip().lower()
            if any(q == t or (len(q) >= 6 and q in t) for t in titles):
                kinds.add("title")
    return kinds


MSS_RANGE = re.compile(r"(\d+):(\d{1,2}(?:\.\d+)?)\s*[–-]\s*(?:(\d+):)?(\d+(?:\.\d+)?)")
MSS = re.compile(r"(\d+):(\d{1,2}(?:\.\d+)?)")
S_RANGE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:–|-|to)\s*(\d+(?:\.\d+)?)\s*s\b")
S_ONE = re.compile(r"(\d+(?:\.\d+)?)\s*s\b")


def times_named(text):
    """The times a verdict's 'saw' names, as (from, to) in seconds: m:ss(.s) and its ranges, and numbers followed by s."""
    found, rest = [], text
    for m in MSS_RANGE.finditer(rest):
        mins = int(m.group(1))
        lo = mins * 60 + float(m.group(2))
        hi = (int(m.group(3)) * 60 if m.group(3) else mins * 60) + float(m.group(4))
        found.append((lo, max(lo, hi)))
    rest = MSS_RANGE.sub(" ", rest)
    for m in MSS.finditer(rest):
        found.append((int(m.group(1)) * 60 + float(m.group(2)),) * 2)
    rest = MSS.sub(" ", rest)
    for m in S_RANGE.finditer(rest):
        lo, hi = float(m.group(1)), float(m.group(2))
        found.append((lo, max(lo, hi)))
    rest = S_RANGE.sub(" ", rest)
    for m in S_ONE.finditer(rest):
        found.append((float(m.group(1)),) * 2)
    return found


def nearest(lo, hi, kinds, decisions):
    """Section 7: the overlapping decisions of a named kind nearest in time; several at the same distance = a tie."""
    cands = [d for d in decisions if d.kind in kinds and lo <= d.end + WIDEN and hi >= d.start - WIDEN]
    if not cands:
        return []
    mid = (lo + hi) / 2
    dist = {d.key: abs(mid - (d.start + d.end) / 2) for d in cands}
    best = min(dist.values())
    return [d for d in cands if abs(dist[d.key] - best) < 1e-9]


def flags_of(look, decisions, extended=False, shift=None):
    """{decision key: 'flag' | 'tie'} for one look at one film. shift(lo, hi) moves a change or a time (for chance)."""
    out = {}
    titles = titles_of(look)
    outcome = look.get("outcome") or {}

    def mark(hits):
        if len(hits) == 1:
            out[hits[0].key] = "flag"
        else:
            for d in hits:
                out.setdefault(d.key, "tie")

    for ch in outcome.get("changes") or []:
        lo, hi = float(ch["from"]), float(ch["to"])
        if shift:
            lo, hi = shift(lo, hi)
        kinds = kinds_named(f"{ch.get('change', '')} {ch.get('why', '')}", titles, extended)
        if kinds:
            mark(nearest(lo, hi, kinds, decisions))
    # Critic A's requirement verdicts: a failed verdict flags a decision only when what it saw names a time inside that
    # window; and, as for a change, its words must name the decision's kind (section 11, 11 November).
    for v in outcome.get("verdicts") or []:
        if v.get("verdict") != "fail":
            continue
        kinds = kinds_named(v.get("saw", ""), titles, extended)
        if not kinds:
            continue
        for lo, hi in times_named(v.get("saw", "")):
            if shift:
                lo, hi = shift(lo, hi)
            mark(nearest(lo, hi, kinds, decisions))
    return out


def seen(look, d):
    return any(d.start <= t <= d.end for t in look.get("frames") or [])


# ---- numbers ----

def cp(k, n):
    """Exact (Clopper-Pearson) 95% interval."""
    if n == 0:
        return [None, None]
    lo = 0.0 if k == 0 else float(beta.ppf(0.025, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(0.975, k + 1, n - k))
    return [round(lo, 3), round(hi, 3)]


def boot(per_film, stat):
    """95% percentile interval from resampling films (section 7). per_film: list of tuples of counts, one per film."""
    if not per_film:
        return [None, None]
    arr = np.array(per_film, dtype=float)
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, len(arr), size=(BOOT, len(arr)))
    sums = arr[idx].sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        values = stat(sums.T)
    values = values[~np.isnan(values)]
    if values.size == 0:
        return [None, None]
    return [round(float(np.percentile(values, 2.5)), 3), round(float(np.percentile(values, 97.5)), 3)]


def share(rows, flag_of):
    k = sum(1 for r in rows if flag_of(r))
    return k, len(rows)


def share_result(rows, flag_of):
    k, n = share(rows, flag_of)
    by_film = defaultdict(lambda: [0, 0])
    for r in rows:
        by_film[r["film"]][0] += 1 if flag_of(r) else 0
        by_film[r["film"]][1] += 1
    return {"k": k, "n": n, "share": round(k / n, 3) if n else None, "cp": cp(k, n),
            "boot": boot(list(by_film.values()), lambda s: s[0] / s[1])}


def diff_result(rows, minus, plus):
    """plus's share minus minus's share, on the same decisions, resampled by film. minus, plus: (name, flag function)."""
    by_film = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        by_film[r["film"]][0] += 1 if minus[1](r) else 0
        by_film[r["film"]][1] += 1 if plus[1](r) else 0
        by_film[r["film"]][2] += 1
    km, kp, n = (sum(v[i] for v in by_film.values()) for i in range(3))
    return {"of": f"{plus[0]} minus {minus[0]}", minus[0]: km, plus[0]: kp, "n": n,
            "diff": round((kp - km) / n, 3) if n else None,
            "boot": boot(list(by_film.values()), lambda s: (s[1] - s[0]) / s[2])}


# ---- the run ----

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", required=True)
    ap.add_argument("--looks", required=True)
    ap.add_argument("--ratings", required=True)
    ap.add_argument("--relabel")
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    draws = json.loads((Path(__file__).parent / "draws.json").read_text())
    stable_films = set(draws["stable"]["films"])

    labelled = list(csv.DictReader(open(args.labels)))
    CASES.update({name: "ABCD"[i] for i, name in enumerate(sorted({r["case"] for r in labelled if r.get("case")}))})
    decisions = [Decision(r) for r in labelled if r["kind"] in KINDS]
    by_film = defaultdict(list)
    for d in decisions:
        by_film[d.filmkey].append(d)
    ratings = {}
    for path in sorted(Path(args.ratings).glob("*/ratings.json")):
        r = json.loads(path.read_text())
        for f in r["films"]:
            ratings[f"{r['round']}/{f['name']}"] = f.get("score")
    films = sorted({f"{r['round']}/{r['film']}" for r in labelled if r.get("round")})  # the 27 study films

    looks = {c: read_looks(Path(args.looks) / p) for c, p in CRITICS.items()}
    failed = {c: sorted(i for i, l in looks[c].items() if l.get("error") or not l.get("outcome")) for c in CRITICS}

    def look(c, which, filmkey):
        lk = looks[c].get(f"{which}/{filmkey}")
        return None if lk is None or lk.get("error") or not lk.get("outcome") else lk

    # one row per decision
    rows = []
    for d in decisions:
        row = {"key": d.key, "film": d.filmkey, "case": d.case, "kind": d.kind, "start": d.start, "end": d.end, "label": d.label}
        for c in CRITICS:
            row[f"{c}_counts"] = d.counts_for(c)
            for which in ("original", "second"):
                lk = look(c, which, d.filmkey)
                tag = which[0]
                if lk is None:
                    row[f"{c}_{tag}"] = row[f"{c}_{tag}_tie"] = row[f"{c}_{tag}_ext"] = row[f"{c}_{tag}_seen"] = None
                    continue
                prim, ext = flags_of(lk, by_film[d.filmkey]), flags_of(lk, by_film[d.filmkey], extended=True)
                row[f"{c}_{tag}"] = prim.get(d.key) == "flag"
                row[f"{c}_{tag}_tie"] = d.key in prim
                row[f"{c}_{tag}_ext"] = ext.get(d.key) == "flag"
                row[f"{c}_{tag}_seen"] = seen(lk, d)
        rows.append(row)

    def has(c, tag="o"):
        return lambda r: r[f"{c}_{tag}"] is not None

    def flag(c, tag="o", variant=""):
        return lambda r: bool(r[f"{c}_{tag}{variant}"])

    summary = {"looks": {c: {"first": sum(1 for i in looks[c] if i.startswith("original/")),
                             "second": sum(1 for i in looks[c] if i.startswith("second/")),
                             "failed": failed[c]} for c in CRITICS},
               "costUSD": round(sum(l.get("costUSD") or 0 for c in CRITICS for l in looks[c].values()), 2)}

    # Q1, Agreement: each critic on the decisions that count for it, first looks
    q1 = {}
    for c in CRITICS:
        mine = [r for r in rows if r[f"{c}_counts"] and has(c)(r)]
        q1[c] = {}
        for label in ("bad", "good"):
            pool = [r for r in mine if r["label"] == label]
            q1[c][label] = share_result(pool, flag(c))
            q1[c][label + "_ties_flagged"] = share_result(pool, flag(c, variant="_tie"))
            q1[c][label + "_extended_words"] = share_result(pool, flag(c, variant="_ext"))
            for kind in KINDS:
                q1[c][f"{label}_{kind}"] = share_result([r for r in pool if r["kind"] == kind], flag(c))
                q1[c][f"{label}_{kind}_extended_words"] = share_result([r for r in pool if r["kind"] == kind], flag(c, variant="_ext"))
    summary["Q1_agreement"] = q1

    # Q2, Compared: B - A on the same bad decisions, counting for both
    both = [r for r in rows if r["A_counts"] and r["B_counts"] and has("A")(r) and has("B")(r)]
    bad_both = [r for r in both if r["label"] == "bad"]
    def AB(variant=""):
        return ("A", flag("A", variant=variant)), ("B", flag("B", variant=variant))

    summary["Q2_compared"] = {
        "bad": diff_result(bad_both, *AB()),
        "bad_ties_flagged": diff_result(bad_both, *AB("_tie")),
        "bad_extended_words": diff_result(bad_both, *AB("_ext")),
        "good": diff_result([r for r in both if r["label"] == "good"], *AB()),
        **{f"bad_{k}": diff_result([r for r in bad_both if r["kind"] == k], *AB()) for k in KINDS},
    }

    # Q3, Stable: the 13 films of draws.json, decisions whose flag is the same in both looks
    q3 = {}
    for c in CRITICS:
        pool = [r for r in rows if r["film"] in stable_films and r[f"{c}_counts"] and has(c)(r) and has(c, "s")(r)]
        q3[c] = share_result(pool, lambda r, c=c: r[f"{c}_o"] == r[f"{c}_s"])
        q3[c]["flagged_first"] = sum(1 for r in pool if r[f"{c}_o"])
        q3[c]["flagged_second"] = sum(1 for r in pool if r[f"{c}_s"])
    summary["Q3_stable"] = q3

    # The prediction (section 8)
    good_zooms = [r for r in both if r["label"] == "good" and r["kind"] == "zoom"]
    summary["prediction"] = {
        "misses_B_minus_A_on_bad": summary["Q2_compared"]["bad"],
        "good_zooms_A_minus_B": diff_result(good_zooms, ("B", flag("B")), ("A", flag("A"))),
    }

    # Exploratory: seen, chance, film scores, changes per look
    expl = {"seen": {}, "chance": {}, "changes_per_look": {}, "film_scores": {}}
    for c in CRITICS:
        mine = [r for r in rows if r[f"{c}_counts"] and has(c)(r) and r["label"] == "bad"]
        expl["seen"][c] = {"seen": share_result([r for r in mine if r[f"{c}_o_seen"]], flag(c)),
                           "unseen": share_result([r for r in mine if not r[f"{c}_o_seen"]], flag(c))}
        # chance: the same changes and verdict times at random places in the film, CHANCE_DRAWS times
        rng = np.random.default_rng(SEED)
        totals = {"bad": [], "good": []}
        counted = {fk: [d for d in ds if d.counts_for(c)] for fk, ds in by_film.items()}
        for _ in range(CHANCE_DRAWS):
            k = {"bad": 0, "good": 0}
            n = {"bad": 0, "good": 0}
            for fk, ds in counted.items():
                lk = look(c, "original", fk)
                dur = duration_of(lk) if lk else None
                if not lk or not dur or not ds:
                    continue

                def shift(lo, hi, dur=dur):
                    length = max(0.0, hi - lo)
                    start = rng.uniform(0, max(0.0, dur - length))
                    return start, start + length

                f = flags_of(lk, by_film[fk], shift=shift)
                for d in ds:
                    n[d.label] += 1
                    k[d.label] += 1 if f.get(d.key) == "flag" else 0
            for label in totals:
                totals[label].append(k[label] / n[label] if n[label] else np.nan)
        expl["chance"][c] = {label: round(float(np.nanmean(v)), 3) for label, v in totals.items()}
        changes = [l["outcome"].get("changes") or [] for i, l in looks[c].items() if i.startswith("original/") and l.get("outcome")]
        named = [sum(1 for ch in cs if kinds_named(f"{ch.get('change', '')} {ch.get('why', '')}", [], False)) for cs in changes]
        expl["changes_per_look"][c] = {"looks": len(changes), "mean_changes": round(float(np.mean([len(x) for x in changes])), 2) if changes else None,
                                       "mean_naming_zoom_or_title": round(float(np.mean(named)), 2) if named else None}
        # film scores against her rating, on the films not left out for this critic
        left = set(f"{r}/{f}" for r, f in LEFT_OUT[c])
        pairs = [(look(c, "original", fk)["outcome"]["score"], ratings[fk]) for fk in films
                 if fk not in left and ratings.get(fk) is not None and look(c, "original", fk)]
        if len(pairs) >= 3:
            rho, p = spearmanr([a for a, _ in pairs], [b for _, b in pairs])
            released = [b for a, b in pairs if a >= RELEASE]
            held = [b for a, b in pairs if a < RELEASE]
            expl["film_scores"][c] = {"films": len(pairs), "spearman": round(float(rho), 3), "p": round(float(p), 4),
                                      "released": len(released), "mean_rating_released": round(float(np.mean(released)), 2) if released else None,
                                      "mean_rating_held": round(float(np.mean(held)), 2) if held else None}
        twice = [(look(c, "original", fk)["outcome"]["score"], look(c, "second", fk)["outcome"]["score"])
                 for fk in sorted(stable_films) if look(c, "original", fk) and look(c, "second", fk)]
        if twice:
            expl["film_scores"][c] = {**expl["film_scores"].get(c, {}),
                                      "stable_films_mean_abs_score_change": round(float(np.mean([abs(a - b) for a, b in twice])), 3),
                                      "stable_films_release_changed": sum(1 for a, b in twice if (a >= RELEASE) != (b >= RELEASE))}
    summary["exploratory"] = expl

    if args.relabel:
        second = {r["key"]: r["label"] for r in csv.DictReader(open(args.relabel))}
        first = {d.key: d.label for d in decisions}
        keys = [k for k in draws["reliability"] if k in second]
        summary["human_ceiling"] = {"k": sum(1 for k in keys if second[k] == first[k]), "n": len(keys),
                                    "cp": cp(sum(1 for k in keys if second[k] == first[k]), len(keys))}

    # tables
    with open(out / "decisions.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(out / "films.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["film", "case", "rating"] + [f"{c}_{x}" for c in CRITICS for x in ("score1", "release1", "score2")])
        for fk in films:
            case = next((d.case for d in by_film.get(fk, [])), "?")
            line = [fk, case, ratings.get(fk)]
            for c in CRITICS:
                a, b = look(c, "original", fk), look(c, "second", fk)
                line += [a["outcome"]["score"] if a else None, (a["outcome"]["score"] >= RELEASE) if a else None, b["outcome"]["score"] if b else None]
            w.writerow(line)
    (out / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    (out / "summary.md").write_text(render(summary))
    print(render(summary))


def fmt(res):
    if not res or res.get("n", 0) == 0:
        return "no decisions"
    if "diff" in res:
        counts = ", ".join(f"{k} {v}" for k, v in res.items() if k in CRITICS)
        return f"{res['of']} {res['diff']:+.3f} ({counts} of {res['n']}; bootstrap {res['boot'][0]} to {res['boot'][1]})"
    return f"{res['share']:.3f} ({res['k']}/{res['n']}; bootstrap {res['boot'][0]} to {res['boot'][1]}; exact {res['cp'][0]} to {res['cp'][1]})"


def render(s):
    lines = ["# Results", "", f"Looks: {json.dumps(s['looks'])}; cost ${s['costUSD']}", "", "## Q1, Agreement (first looks)"]
    for c, r in s["Q1_agreement"].items():
        lines += [f"- Critic {c}: bad flagged {fmt(r['bad'])}; good flagged {fmt(r['good'])}",
                  f"  - zooms: bad {fmt(r['bad_zoom'])}; good {fmt(r['good_zoom'])}",
                  f"  - titles: bad {fmt(r['bad_title'])}; good {fmt(r['good_title'])}",
                  f"  - ties counted as flagged: bad {fmt(r['bad_ties_flagged'])}",
                  f"  - extended words (sensitivity): bad {fmt(r['bad_extended_words'])}"]
    q2 = s["Q2_compared"]
    lines += ["", "## Q2, Compared (bad decisions counting for both critics)", f"- {fmt(q2['bad'])}",
              f"- zooms: {fmt(q2['bad_zoom'])}; titles: {fmt(q2['bad_title'])}",
              f"- ties counted as flagged: {fmt(q2['bad_ties_flagged'])}; extended words: {fmt(q2['bad_extended_words'])}",
              f"- good decisions: {fmt(q2['good'])}", "", "## Q3, Stable (13 films)"]
    for c, r in s["Q3_stable"].items():
        lines.append(f"- Critic {c}: same flag in both looks {fmt(r)}; flagged {r['flagged_first']} then {r['flagged_second']}")
    p = s["prediction"]
    lines += ["", "## The prediction", f"- Misses, on bad decisions: {fmt(p['misses_B_minus_A_on_bad'])} (right if above 0)",
              f"- Good zooms: {fmt(p['good_zooms_A_minus_B'])} (right if above 0)", "", "## Exploratory",
              "```", json.dumps(s["exploratory"], indent=1), "```"]
    if "human_ceiling" in s:
        lines += ["", f"Human ceiling: {s['human_ceiling']}"]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
