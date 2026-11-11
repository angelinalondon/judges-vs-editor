#!/usr/bin/env python3
"""The study's choices of films and decisions, made once before freezing and written to draws.json (PROTOCOL.md sections 4,
5 and 7).

    python3 draw.py <labels.csv> [draws.json]

- stable: the films whose second look counts for Stable. They are the films whose zoom and title decisions count for both
  critics: no film left out of either critic's results, for either kind (section 4). This is a rule, not a draw.
- reliability: 30 decisions Angelina labels a second time without her first labels, 15 zooms and 15 titles, drawn at random
  among all zoom and title decisions with seed 20261111.

Written with Claude, 11 November 2026, for "Does Tev's AI critic flag what an editor flags?".
"""
import csv
import json
import random
import sys
from collections import Counter

SEED = 20261111

# Section 4, contamination: (round, film) left out of a critic's results, and for which kinds.
LEFT_OUT = {
    "A": {
        ("2026-11-04", "01-aspen"): {"zoom"}, ("2026-11-04", "02-birch"): {"zoom"}, ("2026-11-04", "03-cedar"): {"zoom"},
        ("2026-11-03", "09-guava"): {"zoom"}, ("2026-11-03", "11-lemon"): {"zoom"}, ("2026-11-03", "14-mango"): {"zoom"},
        ("2026-11-04b", "03-camellia"): {"title"},
    },
    "B": {
        film: {"zoom", "title"}
        for film in [("2026-11-04b", "01-anemone"), ("2026-11-04b", "02-begonia"), ("2026-11-03", "19-papaya"),
                     ("2026-11-03", "05-coconut"), ("2026-11-03", "20-peach"), ("2026-11-03", "04-cherry")]
    },
}


def main():
    rows = [r for r in csv.DictReader(open(sys.argv[1])) if r["kind"] in ("zoom", "title")]
    out = sys.argv[2] if len(sys.argv) > 2 else "draws.json"
    films = sorted({(r["round"], r["film"]) for r in rows})
    left_out = set(LEFT_OUT["A"]) | set(LEFT_OUT["B"])
    stable = [f for f in films if f not in left_out]
    in_stable = [r for r in rows if (r["round"], r["film"]) in set(stable)]

    rng = random.Random(SEED)
    reliability = []
    for kind in ("zoom", "title"):
        keys = sorted(r["key"] for r in rows if r["kind"] == kind)
        reliability += sorted(rng.sample(keys, 15))

    draws = {
        "seed": SEED,
        "stable": {"films": [f"{rnd}/{film}" for rnd, film in stable],
                   "decisions": dict(Counter(r["kind"] for r in in_stable))},
        "reliability": reliability,
    }
    with open(out, "w") as f:
        json.dump(draws, f, indent=1)
        f.write("\n")
    print(f"stable: {len(stable)} films, {draws['stable']['decisions']}; reliability: {len(reliability)} decisions -> {out}")


if __name__ == "__main__":
    main()
