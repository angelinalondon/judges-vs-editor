# Does an AI critic flag what an editor flags?

A small study of the AI critics in Tev ([tevapp.ai](https://tevapp.ai)), an AI video editor that turns a person's footage and
photos into a short film. Tev's critic, a Claude model, watches a film and decides whether it is good enough to release or asks
for one revision. Here two of Tev's critics are compared with one video editor's own judgments, Angelina Mkrtchyan's:

- **Critic A** reads her written requirements for a film and judges it against each line.
- **Critic B** is told only the person's words and shown only the film.

Most studies of AI judges use tasks with answers that can be checked, such as code or maths. Here "right" is a matter of taste,
and the answer key is one editor's eye.

**Status, 14 November 2026:** three rounds, each frozen with a tagged commit before any critic output was read. The results
are below; the write-up is to come.

## The three rounds

| Round | Question | What was judged | Frozen |
|---|---|---|---|
| 1 ([PROTOCOL.md](PROTOCOL.md)) | Of the editing decisions she would change, how many does each critic flag? | 117 decisions she labelled (46 zooms, 71 titles) in 27 of Tev's films; 80 critic looks | `protocol-frozen`, 11 Nov |
| 2 ([ROUND2.md](ROUND2.md)) | Does a Tev that revises its films on critic A's findings make films she prefers? | her blind choice between two versions' films of the same case | `round2-frozen`, 11 Nov |
| 3 ([ROUND3.md](ROUND3.md)) | Does critic A's lead hold on videos other creators edited themselves? | six finished videos by five creators (20 titles), and her own lookbook apart; 28 looks | `round3-frozen`, 13 Nov |

![How many of Angelina's "bad" editing decisions each critic flagged, rounds 1 and 3](figures/critics-flagged.svg)

## Results

**Round 1, Tev's films** ([results/summary.md](results/summary.md)):

| | Critic A (reads her requirements) | Critic B (viewer only) |
|---|---|---|
| Her "bad" decisions it flagged, first look | 74% (50 of 68; exact 95% interval 61–84%) | 51% (41 of 81; 39–62%) |
| Her "good" decisions it flagged by mistake | 29% (5 of 17) | 32% (6 of 19) |
| Same flag in both looks (13 films) | 89% (42 of 47) | 72% (34 of 47) |

- On the 57 bad decisions that counted for both critics, A flagged 42 and B 34: B minus A is −0.14 (bootstrap 95% interval
  −0.26 to −0.03, resampling films). The difference is in titles (A 39, B 29 of 49); on zooms B flagged 5 and A 3 of 8.
- Angelina's prediction, written before the freeze, was that critic A would do slightly worse: miss more of her bad decisions
  and flag more of her good zooms. Neither half was borne out.
- Each critic's own count leaves out the films it had in effect been told about (`PROTOCOL.md` §4), so the two denominators
  differ.

**Round 2, blind choice between films** ([ROUND2.md](ROUND2.md) §8): she preferred today's Tev (critic B) in 3 of 4 pairs, and
the version revised on critic A's findings in 1 (two-sided sign test p = 0.625, a first look). The one pair she gave to critic
A's version had no critic's work in either film: both revisions ended in questions and were taken back.

**Round 3, other creators' videos** ([ROUND3.md](ROUND3.md) §10): every one of the 20 titles was labelled bad, so this round
measures misses only. Critic A flagged 11 (55%; exact 32–77%) and critic B 6 (30%; 12–54%): B minus A is −0.25 (bootstrap −0.44
to −0.05). The critics agreed with her more on which titles to change than on why. On her own lookbook, reported apart, neither
critic flagged any of its 7 titles, which she called good.

**What this cannot show:** one rater, who also wrote the requirements critic A reads; small samples; and each round is a first
look, not a test. Each round's file lists its own limits.

## What is in this repository

- `PROTOCOL.md`, `ROUND2.md`, `ROUND3.md`: each round's protocol as frozen, with a dated record of every change after the freeze
  and the round's results.
- `analyze.py` and its checks `test_analyze.py`: round 1's analysis, committed before any look was read. `draw.py` and
  `draws.json`: the random draws it uses (seed 20261111).
- `results/`: round 1's anonymised tables (`decisions.csv`, one row per decision with its kind, time, her label and each
  critic's flags; `films.csv`, her 1–5 rating and each critic's scores; `summary.json` and `summary.md`), and round 3's labels
  (`round3-labels.csv`).
- `figures/critics-flagged.svg`: the chart above.

## What stays private

The films, the footage and the pictures (hers and those of the friends who lent their videos to round 3), the people's own
words to Tev, Tev's prompts and requirements, Tev's code, and the critics' raw answers. Round 1's films appear only under code
names and its cases as letters A–D; rounds 2 and 3 name their cases by working title, and round 3's creators only as A–E.

## Licence

The code (`analyze.py`, `draw.py` and `test_analyze.py`) is under the [MIT License](LICENSE). Everything else here (the text,
the chart and the data) is under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). To cite it: Angelina Mkrtchyan,
*Does an AI critic flag what an editor flags?* (2026), https://github.com/angelinalondon/judges-vs-editor.

## How it was made

Claude helped with the design, the code and the editing; the labels, the judgments and the first drafts are Angelina's. The
critics are Claude models too (Claude Opus 5.5, as Tev runs them). Every look was made on her Mac by Tev's own critic code,
counted against a fixed budget for the study.

Angelina Mkrtchyan, with Claude's help on the design, the code and the editing.
