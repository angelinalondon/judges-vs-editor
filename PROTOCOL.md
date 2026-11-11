# Protocol: do Tev's AI critics flag what one editor flags? A pilot

**Status: frozen on 11 November 2026** with the tagged commit `protocol-frozen`, before a critic first looked at a study
film. Nothing in sections 1–10 changes after that. Any later change is logged in section 11 with its date and reason.

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
- **Runner:** Tev's backend `evals/experiments/judges/critic.ts` (backend commit `3ac887a`, run from a clean checkout of
  that commit; the looks file from the workspace's `scorer-audit/make_looks.py`, workspace commit `7d72795`). It makes
  each look exactly as the Worker's `critique2` route makes it under the policy, with the bundles read from the files the
  Worker's store holds. Only the primary model's answers count: no fallback, one retry of the primary.

**What a critic gets, on the Mac:**
- the film as Angelina rated it (its exported mp4);
- 24 frames at even steps, 540 × 960, with their times; the captions and titles are burned in as rendered;
- facts measured from the film: its length, shape and frame rate, its cuts, its loudness every half second, and its
  titles with their times and places, from its project;
- the person's first message (a look without it is refused, never sent);
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

**Reliability:** 30 decisions, 15 per kind, drawn at random with seed 20261111 (`draw.py`, listed in `draws.json`), are
labelled again by Angelina without her first labels, at least three days after the first. Her agreement with herself is
the human ceiling beside the critics.

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

Each critic looks once at each of the 27 films: 54 looks. For Stable, each critic looks a second time, a separate call
with the same request, at the 13 films whose zoom and title decisions count for both critics (section 4; `draws.json`):
26 more looks, 80 in all.

**Pilot, 11 November:** each critic looked once at two films outside the study, from Angelina's own later cases
(Unboxing_Peggy_Clutch 2026-11-08-2.3.2a and Stella_Boots_Lookbook 2026-11-08-2.3.1a). All four looks were answered. A
look cost $0.57 for critic A and $0.30 for B (section 10).

## 6. Procedure

1. **Labels (10 November):** done and committed.
2. **Pilot (11 November):** done; two films outside the study, both critics.
3. **Freeze:** predictions written, this file tagged `protocol-frozen`.
4. **Looks:** critic A and critic B, one look each at every study film, and a second look each at the 13 films of Stable.
5. **Reliability:** Angelina labels the 30 drawn decisions again, on or after 13 November.
6. **Analysis:** the measures below, in code.

## 7. Measures

**Flagged:** decided in code, never by hand.
- **A change flags a decision** when both are true:
  - its seconds overlap the decision's time, widened by 0.5 s on each side;
  - its words name the decision's kind: "zoom", "punch in" or "push in" for a zoom; "title", "text", "card" or "heading" for
    a title or card. Words match in any case, and "punch-in" or "push-in" with a hyphen count too.
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
- **Q3, Stable:** for each critic, the share of decisions whose flag is the same in its two looks, at the 13 films whose
  decisions count for both critics (47 decisions: 13 zooms, 34 titles).

Each primary result has a 95% interval from 10,000 bootstrap resamples of films (seed 20261111), with exact
(Clopper–Pearson) intervals beside it for reference.

**Exploratory, everything else:**
- **By kind and by film.**
- **Seen:** whether any of a critic's frames falls inside the decision's time; the shares flagged for seen and unseen
  decisions.
- **Film scores:** each critic's score against Angelina's 1–5 rating of the film (rank correlation), and its release
  decision against her rating; the score and release difference between the two looks.
- **Chance:** the share flagged if a critic's flags fell at random, at its own flag rate.
- **Human ceiling:** Angelina's agreement with herself.
- **Changes per look,** and how many of them name a zoom or a title at all.

**The prediction (section 8) is right** on each half when the observed difference has the sign it says; its interval
shows how sure that is.

## 8. Prediction (Angelina's, written before the freeze)

Angelina wrote one hypothesis rather than a number for each question (11 November 2026, her words): critic A will do
slightly worse than critic B. It will miss more of the failures, and it will flag more of the good zooms.

It is checked as two directions, with no threshold:
1. **Misses (Q2, Compared):** critic B flags a larger share than critic A of the decisions labelled bad that count for
   both critics (57: 49 titles, 8 zooms).
2. **Good zooms:** critic A flags a larger share than critic B of the zooms labelled good that count for both critics.
   There are only 5, so this half is read loosely.

"Slightly" is reported, not tested.

## 9. Reporting

- **Numbers:** counts and intervals, also given by kind and by film. Decisions within one film are not independent.
- **One chart:** for each kind, the share of bad decisions each critic flagged and the share of good ones it flagged by
  mistake, with intervals.
- **Everything run is reported:** failed looks, the films left out and why, and every change to this file.

## 10. Budget and what is public

- **Budget:** $40 for every model call of the study, from 9 to 17 November, counted by Tev's budget window `JUDGE`; the
  runner refuses a call the window cannot pay for. The calls are paid from Dmitry's Anthropic account, with a key made for
  the study.
- **Prices:** the pilot measured a look at $0.57 for critic A and $0.30 for B. The dry run had estimated $0.23 and $0.21;
  most of a look's price is the critic's own output, about 22,000 tokens for A and 10,000 for B. The 108 looks first
  planned would have cost about $47, so second looks are made only at the 13 films of Stable. The pilot cost $1.74, the 80
  looks cost about $35, and about $3 is left for looks that fail and are made again.
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
| 10 Nov, before freezing | Critic B is critique-v11, viewer only; a second version of one critic shown frames at the decisions' moments (the earlier "round 2") moved to later work | Angelina's choice of v11 for B |
| 11 Nov, before freezing | "punch in" and "push in" added to the words that name a zoom (section 7) | The pilot: critic B asked for a zoom once as "Zoom in" and once as "Punch in"; Angelina agreed |
| 11 Nov, before freezing | Pilot: four looks answered, $1.74; a look costs $0.57 for critic A and $0.30 for B | Section 5 |
| 11 Nov, before freezing | Second looks only at the 13 films whose decisions count for both critics: 80 looks, not 108 | The pilot's prices. Angelina chose Stable on about 12 films over a second version of critic B shown frames at the decisions; 13 is every film that counts for both critics, so no film is drawn |
| 11 Nov, before freezing | The runner refuses a look without the person's words, and takes any Anthropic key (`sk-ant-…`) | Stella_Boots_Lookbook has no `turn-request.json`, and the dry run sent it with no words; the study's key is not `sk-ant-api…`. Neither changes a study film's request. Angelina agreed |
| 11 Nov, before freezing | Paid from Dmitry's Anthropic account, not Angelina's | Angelina's choice |
| 11 Nov, before freezing | Seed 20261111 for the reliability draw and the bootstrap; `draw.py` writes `draws.json` | |

## 12. Who did what

Angelina Mkrtchyan designed the study and owns it. She labelled the decisions, writes the predictions, and writes the
analysis and the first draft of the write-up. Claude (Anthropic) helped with the design, the code and the editing. The
critics are Claude models too, so the same model family helped design the rules that score them.
