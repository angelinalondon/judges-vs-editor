# Round 3: do the critics flag what Angelina flags in other creators' own edits? A first look

**Status: frozen on 13 November 2026** with the tagged commit `round3-frozen`, before any critic looked at a round-3 video.
Nothing in sections 1–8 changes after that. Any later change is logged in section 9 with its date and reason.

## 1. The question, and how it connects to rounds 1 and 2

This is a **new question**. Round 1 (`PROTOCOL.md`) found that critic A, which reads Angelina's written requirements, flagged
more of the decisions she called bad than critic B, a viewer told only the person's words: 74% against 51% in first looks, and
42 against 34 of the 57 bad decisions that counted for both. Every film in round 1 was Tev's edit of Angelina's own footage, her
requirements were written from those films, and only 17 to 19 of the decisions she labelled were good, so how often a critic
flags good work was the least certain number. Round 2 (`ROUND2.md`) found no sign that revising on critic A's findings makes
films she prefers.

Round 3 asks: **in videos that other creators edited and posted themselves, does critic A still flag more of the decisions
Angelina calls bad than critic B, and how often does each critic flag decisions she calls good?** These are human edits, made
from footage her requirements were not written from.

## 2. The critics

Unchanged from round 1 (`PROTOCOL.md` §3): **critic A** is policy 2.3.7's Critique (critique-v8, sha256 `e475b2986c25…`, reading
requirements-v2, sha256 `2ec3fe4f6f17…`); **critic B** is policy 2.3.10's (critique-v11, sha256 `09f60874a994…`, a viewer only).
Same models and settings, and the round-1 runner (the backend's `evals/experiments/judges/`, at `393c4e8`).

## 3. The videos

- **Six finished videos by five other creators, Angelina's friends,** who agreed to share them with her (13 November 2026). Raw
  footage from other people is not available. Five are a talking head over pictures, the kind Tev's "material" recipe makes,
  and one is a talking head with pictures set into the frame; they run 18 to 48 s. One creator made two of them.
- **Angelina's own lookbook (13 s, seven looks, Monday to Sunday), reported apart.** She added it as a negative example she is
  unsure of: the camera moves within its shots. Both critics look at it as at the others, but it stays out of the primary results,
  because its footage is hers. Reported for it: each critic's score and release, whether it names the camera's movement, and how
  it flags the titles and zooms she marks.
- **The creators agreed** (13 November, through Angelina) to their videos being shown to the critics: a look sends 24 frames of a
  video and its words to Anthropic's API.
- Her labels (§4) found no title she would keep in the friends' videos, so the hope of many good decisions, which round 1 lacked
  (17 to 19), was not met.
- The videos, their creators' names and their words stay private: never in this repository, never on Tev evals. Here the
  creators are "creator A" to "creator E".

## 4. Decisions and labels

- There is no Tev project to list the decisions, so **Angelina marks them:** every zoom (a push-in or punch-in, or a cut to a
  closer framing of the same shot) and every title or card, each with its start and end time, and for a title its words.
- She labels each one as in round 1 (`PROTOCOL.md` §4): **bad** ("I would change this decision in my own edit", even a little),
  **good** ("I would keep it") or **unsure**, with a few words why.
- Her marks and labels are frozen **before any critic looks at any video**: her labels file (private, in the workspace's
  `scorer-audit/round3/`) has sha256 `3042e83b0d718734…`, and its anonymised copy is `results/round3-labels.csv` here (video,
  kind, times, label, and whether the label is hers or copied; no words or notes).
- **How the marks were made (13 November):** Claude read every title's words and on-screen times from the videos' frames (Apple's
  on-device text recognition, four frames a second, uncertain moments checked by eye), and Angelina's own notes were attached to
  their titles. The six friends' videos hold **20 titles and no zoom** (one video has no title, only word-by-word captions); her
  lookbook holds 7. Her notes about the word-by-word captions are kept as "caption" marks, outside the titles.
- **Labels copied across a style, at her word:** within a video, titles of one style share one label. Angelina labelled one title
  of each style, and its label and note were copied to the others of that style: 12 of the friends' 20 titles are copies (one of
  them from the same creator's other video, the same opening title), and 8 carry her own label (one from a note she wrote about
  two labels at once). Each copy is marked in her labels file and in `results/round3-labels.csv`. **All 20 of the friends' titles
  are labelled bad** (a soft shadow she would add, numbering, the outline of thin letters, a white box over the pictures); her
  lookbook's 7 are good.

## 5. Looks

Each critic looks at each of the seven videos twice (14 looks each, 28 in all), with the round-1 runner and the round-1 inputs:
- 24 frames at even steps and the facts measured from the video (length, shape, cuts, loudness), as in round 1;
- the titles' words and times, from Angelina's marks (in round 1, from Tev's project);
- **a first message for each video,** as its creator might have written it to Tev (in round 1, the case's real first message):
  Angelina wrote two, and approved as they stand Claude's drafts of the other five;
- for critic A, her requirements, as in round 1;
- **no recipe:** these videos were not made from one (in round 1, critic A read the case's recipe);
- as in round 1, no raw takes, no Designer's intent and no code checks: round 1's critics never saw them either.

The runner reads a downloaded video as it reads a Tev export (a look names the video file, its titles and the person's words); its
one change spends under round 3's own window (backend `393c4e8`). Before the freeze, a dry run built all 28 requests and sent none:
24 frames each, and critic A's with her 34 requirement lines. The looks file has sha256 `a924f68646c04a51…`.

## 6. Measures

Exactly `PROTOCOL.md` §7: when a change or a failed verdict flags a decision, and the three primary results: **Q1, Agreement**
(the share of bad decisions each critic flags, with the share of good ones beside it), **Q2, Compared** (B minus A on the same
bad decisions) and **Q3, Stable**, on the six friends' videos, each with a bootstrap interval over videos (seed 20261113)
and exact intervals beside it.
Reported beside round 1's numbers.

What the labels allow, and two additions (13 November, before any look):
- **No good title among the friends' videos:** round 3 measures how many of her bad titles each critic catches, not how often it
  flags a title she would keep. Her lookbook's 7 good titles are reported apart (§3).
- **With her own labels only:** the results are also given on the titles she labelled herself (the copies left out).
- **Per video:** most bad labels repeat one complaint per video (no soft shadow, for example), and by `PROTOCOL.md` §7 one change
  flags one title, so a critic that asks once to add a shadow to every title catches one of them. Beside the per-title results,
  each critic is reported per video: whether any of its changes or failed verdicts names the problem she gave for that video's
  titles.

## 7. Prediction

None: Angelina wrote no prediction before the freeze.

## 8. What it cannot show

- 20 titles in the friends' videos, from five creators, all of them bad, with most labels copied across a style: every
  interval will be wide. This is a first look.
- Four of the six videos are 464×848 (shared through a messenger): a small title may be hard to read in 24 frames, for a critic
  and for anyone.
- One rater, who is also the person whose requirements critic A reads. Her requirements describe her own taste and Tev's
  recipes; another creator's style may break them on purpose.
- A first message written for the study stands in for the creator's real one.
- The critics are told, as for any film in Tev, that Tev made the film.
- The decisions are hers to find: a zoom or title she does not mark cannot be judged.

## 9. Budget, timeline and record

- **Budget:** window `JUDGE3`, $15 (backend `evals/compare/budgets.json`, `393c4e8`; Angelina: "Go for it"). No films are made.
  The 28 looks cost about $12 at round 1's price ($35.10 for 80 looks); the dry run's estimate was $5.90.
- **Timeline:** the marks, labels, first messages and freeze on 13 November; looks and analysis next; results by 16–17 November.
- **Changes after the freeze:**
  - 13 November, while the looks ran and before any was read: the analysis code, `analyze3.py` (private, in the workspace's
    `scorer-audit/round3/`, sha256 `23d10049946f08c8…`), which imports round 1's `analyze.py` for §6's rules and sets the seed to 20261113. It
    states §6's per-video measure in words: a change or a failed verdict names her problem when it names a title (round 1's words,
    extended) and uses the words of the problem she gave for that video's titles: legibility (shadow, outline, contrast, legible,
    readable, hard to read or see, visible, scrim), numbering, a white box over the pictures, or the font and its spacing.
