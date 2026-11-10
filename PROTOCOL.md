# Protocol: do Tev's AI critics flag what one editor flags? A pilot

**Status: draft, 10 November 2026.** This file is frozen with a tagged commit, `protocol-frozen`, before a critic first
looks at a study film (planned for 11 November 2026). Nothing in sections 1–10 changes after that. Any later change is
logged in section 11 with its date and reason.

**To settle before freezing (Angelina):** the predictions (section 8). Filled in by code at freezing (marked FILL): the
commits and the seed.

## 1. Questions

Tev is an AI video editor that turns a person's footage and photos into a short film. An LLM critic decides whether a
film is good enough to release, or asks for one revision. One editor, Angelina, is the answer key: she labelled single
editing decisions in 27 of Tev's films.

1. **Agreement:** of the decisions she would change, how many does each critic flag, and how many of those she would
   keep does it flag by mistake?
2. **Compared:** Tev's newest critic is told only the person's words and shown only the film. Does it flag more or fewer
   of the same decisions than the critic that reads her written requirements?
3. **Stable:** looking at the same film twice, does a critic flag the same decisions?

## 2. Why it matters, and what a pilot can say

This pilot illustrates the scalable-oversight question; it cannot answer it. The question is whether an AI judge can
oversee an AI's work where "right" is a matter of taste rather than a test that passes. Most oversight studies use tasks
with checkable answers, such as code or maths. Here the answer key is one editor's eye, on four cases of one genre. The
critics matter in practice: they decide which films Tev releases. A single score per film also hides why: Tev's earlier
rule-based scorer gave 0.967 to the film this editor rated lowest of three on 10 November.

## 3. The critics, frozen

- **Model:** Claude Opus 5.5 at effort xhigh, for both.
- **What a critic returns:** a score from 0 to 1, where 0.85 or more releases the film; a list of changes, each with its
  seconds (from, to), what to change and why; critic A also gives a verdict on each requirement line.
- **The two critics, Angelina's choice on 10 November:**
  - **A, reads the requirements:** Tev policy 2.3.7, critic prompt `critique-v8` (sha256 `e475b2986c25…`) with her
    requirements `requirements-v2` (sha256 `2ec3fe4f6f17…`, 113 lines, 53 to 59 shown for a film's recipe).
  - **B, a viewer only:** Tev policy 2.3.10, critic prompt `critique-v11` (bundle file sha256 `09f60874a994…`) under
    `viewerOnly`. It is told only the person's words and shown only the film; it describes the pictures before it reads a
    word, and it gives no requirement verdicts.
  - The prompts differ in more than the requirements, so the comparison is between two critics Tev has built, not of
    the requirements alone.
- **Runner:** Tev's backend `evals/experiments/judges/critic.ts` (backend commit `05cac57`, or FILL at freezing). It makes
  each look exactly as the Worker's `critique2` route makes it under the policy, with the bundles read from the files the
  Worker's store holds. Only the primary model's answers count: no fallback, one retry of the primary.

**What a critic gets, on the Mac:**
- the film as Angelina rated it (its exported mp4);
- 24 frames at even steps, 540 × 960, with their times; the captions and titles are burned in as rendered;
- facts measured from the film: its length, shape and frame rate, its cuts, its loudness every half second, and its
  titles with their times and places, from its project;
- the person's first message;
- for critic A only, the requirement lines, as their ids and text.

It gets no Tev reply, no designer intent and no transcript, so it knows what is said only through captions in its
frames. On the phone it would see other frames (the start, middle and end of each shot). These differences could move
results either way, so results speak for this setup only, not for Tev's release gate.

## 4. Films, decisions and labels

**Films:** the 27 films Angelina rated, from four fashion cases (A–D): 21 rated on 3 November, 3 on 4 November, 3 on
10 November. They were made by Tev's earlier pipeline, versions v64 to v94, between 25 October and 4 November 2026. A
fifth case's six films, rated by their owner rather than Angelina, are not in the study.

| Kind of decision | In the 27 films | Labelled |
|---|---|---|
| Zoom | 46 | all: 14 good, 32 bad |
| Title or count card | 71 | all: 11 good, 60 bad |
| Picture or screen recording shown with the talk | 548 | not in this round: whether a picture's place matters depends on the moment, so one good or bad label per picture misses it |

**Labels:** each label is one of:
- **bad:** "I would change this decision in my own edit", even a little;
- **good:** "I would keep it";
- **unsure:** "I can't tell"; left out of every share.

Each label has a few words on why. The labels are `labels.csv`, built by Tev's `make_label_list.py`, committed before any
study look (section 11). Angelina labelled before seeing any critic's answer on these films.

**Reliability:** 30 decisions, 15 per kind, drawn with seed FILL, are labelled again by Angelina without her first labels,
at least three days after the first. Her agreement with herself is the human ceiling beside the critics.

**Contamination:** where a critic has, in effect, been told the answer, those films are left out of its primary results
and reported separately.
- **Critic A:** its requirement G-ZOOMS-1, in the text it sees, names six of the 27 films and gives Angelina's verdict on
  their zooms. Those six films hold 28 of the 46 zooms, and they are left out of A's zoom results. Requirement
  G-PICTURES-6 describes one film's count slip (03-camellia of the 10 November round) without naming it, so that film's
  titles are left out of A's results.
- **Critic B:** while it was built, the team checked it against Angelina's film ratings of six of the 27 films:
  01-anemone, 02-begonia, 19-papaya, 05-coconut, 20-peach and 04-cherry (workspace plans/2026-11-10-critique-check/).
  Those six films are left out of B's results.
- **Compared** counts only decisions in films left out of neither.

## 5. Looks

Each critic looks at each of the 27 films twice, the second look a separate call with the same request: 108 looks in
all. Two films outside the study, from Angelina's own later cases (Unboxing_Peggy_Clutch or Stella_Boots_Lookbook), are
looked at first, once by each critic, as a dry run and a pilot: the price of a look, and the runner's logs.

## 6. Procedure

1. **Labels (10 November):** done and committed.
2. **Pilot (11 November):** two films outside the study, both critics.
3. **Freeze:** predictions written, this file tagged `protocol-frozen`.
4. **Looks:** critic A and critic B, two looks each at every study film.
5. **Reliability:** Angelina labels the 30 drawn decisions again, on or after 13 November.
6. **Analysis:** the measures below, in code.

## 7. Measures

**Flagged:** decided in code, never by hand.
- **A change flags a decision** when both are true:
  - its seconds overlap the decision's time, widened by 0.5 s on each side;
  - its words name the decision's kind: "zoom" for a zoom; "title", "text", "card" or "heading" for a title or card.
- **One decision per change:** each change goes to at most one decision, the overlapping decision of that kind nearest
  in time.
- **Requirement verdicts (critic A):** a failed verdict flags a decision only when what it saw names a time inside that
  window.
- **Unsure:** two or more decisions tie for a change. They count as not flagged in the primary result and as flagged in a
  sensitivity check.
- **A decision is flagged by a critic** when its first look flags it. The second look is for Stable.

**Primary results, one per question:**
- **Q1, Agreement:** for each critic, the share of decisions labelled bad that it flagged, pooled over zooms and titles;
  the share of decisions labelled good that it flagged is given beside it.
- **Q2, Compared:** critic B's share of bad decisions flagged minus critic A's, on the same decisions, pooled.
- **Q3, Stable:** for each critic, the share of decisions whose flag is the same in its two looks.

Each primary result has a 95% interval from 10,000 bootstrap resamples of films (seed FILL), with exact (Clopper–Pearson)
intervals beside it for reference.

**Exploratory, everything else:**
- **By kind and by film.**
- **Seen:** whether any of a critic's frames falls inside the decision's time; the shares flagged for seen and unseen
  decisions.
- **Film scores:** each critic's score against Angelina's 1–5 rating of the film (rank correlation), and its release
  decision against her rating; the score and release difference between the two looks.
- **Chance:** the share flagged if a critic's flags fell at random, at its own flag rate.
- **Human ceiling:** Angelina's agreement with herself.
- **Changes per look,** and how many of them name a zoom or a title at all.

**A prediction is right** when the observed share falls on the side of its number that it says.

## 8. Predictions (Angelina's, written before the freeze)

TO WRITE. One line each, with a number, for example: "critic A flags fewer than half of the zooms I labelled bad".

1. Q1, Agreement, critic A:
2. Q1, Agreement, critic B:
3. Q2, Compared:
4. Q3, Stable:
5. Film scores: does either critic order the films as I rated them?

## 9. Reporting

- **Numbers:** counts and intervals, also given by kind and by film. Decisions within one film are not independent.
- **One chart:** for each kind, the share of bad decisions each critic flagged and the share of good ones it flagged by
  mistake, with intervals.
- **Everything run is reported:** failed looks, the films left out and why, and every change to this file.

## 10. Budget and what is public

- **Budget:** $40 for every model call of the study, from 9 to 17 November, paid from Angelina's own Anthropic account and
  counted by Tev's budget window `JUDGE`; the runner refuses a call the window cannot pay for. The dry run estimates
  $0.23 a look for critic A and $0.21 for B: about $24 for the 108 looks and $1 for the pilot. If the pilot shows a look
  costs more than $0.35, the second looks are dropped and Stable is reported on what remains.
- **Public (this repository):** this protocol, the analysis code, the anonymised results tables (decision id, kind, time,
  label, each critic's flag and score; cases as A–D), the chart and the write-up.
- **Private, in Tev:** the films, the footage and the pictures, the prompts and the requirements text, Tev's code, and the
  critics' raw answers.

## 11. Record and changes after freezing

| Date | What | Why |
|---|---|---|
| 10 Nov, before freezing | Pictures left out of this round | Angelina: a picture's place matters only at some moments, so one good or bad label per picture misses it |
| 10 Nov, before freezing | Five unsure labels (two zooms, three titles) changed to bad, notes kept | Angelina: they leaned negative; bad now means "I would change it, even a little" |
| 10 Nov, 20:40 UTC | Labels complete: 46 zooms (14 good, 32 bad), 71 titles (11 good, 60 bad); workspace commit `47bd4a4`, `labels.csv` sha256 `befb7de3c8d7e3ea…` | The answer key, before any study look |
| 10 Nov, about 20:35 UTC | Angelina saw both critics' film-level scores on six study films (no notes), after labelling them | Shown by the session building the critics; those six films are already left out of B's results |
| 10 Nov, before freezing | Planted flaws dropped | Tev's export test is not on its main branch, and zooms added with ffmpeg also enlarge the titles, captions and speaker that a real Tev zoom leaves alone, so the flaw would not be Tev's. Kept for later, with an export test |

## 12. Who did what

Angelina Mkrtchyan designed the study and owns it. She labelled the decisions, writes the predictions, and writes the
analysis and the first draft of the write-up. Claude (Anthropic) helped with the design, the code and the editing. The
critics are Claude models too, so the same model family helped design the rules that score them.
