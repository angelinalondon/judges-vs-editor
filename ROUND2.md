# Round 2: does a Tev that revises on critic A's findings make films Angelina prefers? A first look

**Status: frozen on 11 November 2026** with the tagged commit `round2-frozen`, before the first round-2 film was made. Nothing in
sections 1–6 changes after that. Any later change is logged in section 7 with its date and reason.

## 1. The question, and how it connects to round 1

This is a **new question**. Round 1's question, "Do Tev's AI critics flag what one editor flags?" (`PROTOCOL.md`), is unchanged, and
its labels and results stand as they are: critic A (critique-v8, reading Angelina's requirements) flagged more of her bad decisions
than critic B (critique-v11, a viewer only), 42 against 34 of 57, the whole difference in titles and coming from A's verdicts on
her requirement lines.

In Tev those verdicts are kept for the record only: the revision is made from the critic's changes alone. So round 1 cannot say
whether Tev should use critic A. Round 2 asks: **when Tev revises a film on critic A's findings, its failed requirement lines
included, does Angelina prefer the film to the one Tev makes today, with critic B?**

## 2. The two versions (Angelina's environment, `angelina`)

- **B, today's Tev:** version `2.3.10` as it is (`routingPolicy:2.3.10`, sha256 `15fa630c1c16…`): the Designer (designer-v9 on
  Claude Opus 5.5, checking requirements-v2 before it answers), and critic B (critique-v11, a viewer only).
- **A:** version `2.3.10-a`, label v2.3.10-A (`routingPolicy:2.3.10-a`, sha256 `da3b55f1a42c…`): the same, but for the critic,
  which is critic A of round 1 (policy 2.3.7's: critique-v8, sha256 `e475b2986c25…`, with requirements-v2, sha256
  `2ec3fe4f6f17…`), and its failed requirement lines reach the revision. They go as one note, first, over the whole film: the
  failed lines' ids, which the Designer reads with their text in its own requirements, and what the critic saw. The critic's own
  changes follow, as many as Tev's six notes leave (backend `86962e7`, `critique.params.revisesFailedRequirements`). In round 1,
  critic A wrote six changes in 24 of its 40 looks, so in such a film its sixth change gives way to the note.
- **The same for both:** the Worker (`ca2fe653`, backend `86962e7`), the app build (iOS `ba02d694`, Debug: main with the export
  fix of `936efbcb`, the screen kept on during a test of `934aa515`, and the footage-sheet setting of `ba02d694`), the phone
  (Angelina's iPhone 18 Pro Max, iOS 27.2), the account (`suite-angelina`). In both, the critic looks at the
  first cut; at 0.85 or more the film is released, below it Tev makes one revision from its notes, the critic looks again, and
  Tev keeps the higher-scored cut, as it does today.

## 3. Films

- **Five cases, Angelina's choice (11 November):** Olsens_Oversized, Madame_T and Autumn_Wardrobe (talking head), and
  Trousers_Five_Looks and Stella_Boots_Lookbook (lookbook). Marlo_Tote and Opinion are left out at her word; Zegna is Dmitry's case.
- **One film per case and version: 10 films,** all on her phone (the talking heads need its cut-out of the speaker, and the
  simulator has no body pose for a lookbook's zooms).
- **Each film is made as in her rating rounds:** `CaseFilmUITests` with the case's real first message (`request.json`), the case's
  recipe picked (talking head: "material", the speaker small over the pictures; lookbook: "quick", as `datasets/recipes.json` says),
  the phone's footage sheet read, as for any version listed with it, Tev's questions answered with its recommended option, no
  follow-up, and the film review's "Fix these" left unanswered. The script is the workspace's `scorer-audit/round2/film.sh`
  (private: it names the cases).
- **Order:** the cases in the order above; within a case, A goes first in the first, third and fifth cases, B in the second and
  fourth.
- A film that fails to finish (an error, the phone, a provider) is made once more with the same version. A film that fails twice
  is reported as missing, and its case's pair is left out.

## 4. The measure

- **Angelina's blind choice.** For each case she watches its two films on one page, their order shuffled (seed 20261112), with
  no version, score or critic note shown, and picks the one she prefers, or "same", with a few words why. She sees no critic
  output before she has chosen all five.
- **Reported:** how many cases she prefers A in, B in, or neither, with her reasons. With five pairs no result is a clear one:
  even 5 of 5 gives p = 0.0625 (two-sided sign test). It is a first look, not a test.
- **Exploratory, from the films' own records (no extra cost):** each critic's score of the first cut and whether it asked for a
  revision; how many notes reached the revision, and how many of A's failed lines; which cut Tev kept; each film's cost and time;
  whether the film she prefers is the one its critic scored higher (each critic scored only its own version's film, so this is not
  a comparison of the two critics' scales).

## 5. What it cannot show

- One film per version and case: each version makes its own first cut, and the Designer never cuts the same way twice, so the
  two films of a pair differ by chance as well as by the critic.
- Four of the five cases are cases her requirements were written from (Olsens_Oversized, Madame_T, Autumn_Wardrobe and
  Trousers_Five_Looks); only Stella_Boots_Lookbook is not.
- A and B differ in the whole critic (prompt, inputs, requirements) and in what reaches the revision, not in one thing.
- One rater, who is also the person whose requirements critic A reads.

## 6. Budget

About $25 for the 10 films, on her environment's keys (about $2.30 a film, by the 2.3.8 film of 10 November), outside the $40 of
window JUDGE, which counts round 1's calls. No model call is made from the Mac in round 2.

## 7. Changes after the freeze

- **12 November, 04:15 UTC, before any of the other nine films, at Angelina's word ("do in one"):** the nine films after the first
  are made in **one test session** (`CaseFilmUITests.testTheCasesFirstMessagesMakeFilms`, iOS `1e5a40c5`, through the workspace's
  `scorer-audit/round2/session.sh`), each with exactly the steps of the single-film test, in the order of section 3. **Why:** the
  phone asks its owner to approve UI automation (Face ID or the passcode) once per test session. The first film was made in a
  session of its own on 11 November (22:35–22:54 UTC); every later film, each in its own session, stopped after about a minute
  with "Timed out while enabling automation mode" while she slept (22:55–23:19 UTC, two tries each). No film started in them and
  nothing was paid. One session asks once. The test build is the one the first film used plus the session test (built before
  Dmitry's case-film change `53750f3f`, whose settings these films do not use). The nine are made on 12 November (runs
  `2026-11-12-r2-<version>`); a film that fails is made once more in a second session (`…-again`).
