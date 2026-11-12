# Round 2: does a Tev that revises on critic A's findings make films Angelina prefers? A first look

**Status: frozen on 11 November 2026** with the tagged commit `round2-frozen`, before the first round-2 film was made. Nothing in
sections 1–6 changes after that. Any later change is logged in section 7 with its date and reason. **Results, 12 November 2026:**
section 8.

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
- **12 November, what became of that session (04:15–06:59 UTC):** all nine films were made and exported, and all nine videos were
  lost: Tev empties its export folder each time it opens, so each film's launch deleted the film before it, and the script opened Tev
  again before taking the last one ($22.41). Their records (every model answer, critic scores and notes) are kept. Then, at
  Angelina's word, film by film:
  - Olsens_Oversized on 2.3.10 and Madame_T on 2.3.10 made again on her phone (runs `…-again`, 11:07 and 11:34 UTC), each copied
    off the phone before Tev opened again.
  - Trousers_Five_Looks, both films, **rebuilt on the Mac from their own records** (runs `…-rebuilt`): their recorded answers
    replayed by Tev's own replay tool (tev-apply) on the case's media as Tev seeds it, with the phone's own numbering of the clips,
    and exported by Tev's own exporter on a simulator. The rebuilt first cut matches the phone's own description of it shot for shot
    and title for title. What differs: the iPhone's HDR clips were converted to standard range on the Mac before the edit, and the
    export ran on a simulator. Both films of the pair are made the same way.
  - Madame_T on the new version: made twice on her phone (14:25 and 14:53 UTC, $2.94 and $2.49) and exported neither time, an
    email's banner over the Chat/Editor switch taking the test's tap. The second time its project was saved before the export
    (run `…-again`: the whole edit and the speaker's cut-out); it is to be exported from that saved project, with no model call.
- **12 November, ~15:35 UTC, at Angelina's word ("Yes, on the simulator"):** Stella_Boots_Lookbook's two films are made on an
  iOS 27.0 simulator on this Mac, not on her phone: the same test (CaseFilmUITests, iOS `a551616b`), Worker and versions, one session
  per film, the new version first (runs `2026-11-12-r2-<version>-sim`). What differs from a phone: the simulator has no body pose, so
  the films' crops "focused on the feet" aim at the middle of the frame (this case's simulator film of 10 November did so), and a
  session token for the same account stands in for App Attest. Both films of the pair are made the same way. They were made
  16:25–16:52 and 16:52–17:10 UTC (runs `2026-11-12-r2-2.3.10-a-sim` and `2026-11-12-r2-2.3.10-sim`): 16.1 s and 19.7 s, at
  1080p/30.
- **12 November, 17:05–17:07 UTC, Madame_T's new-version film exported from its saved project on her phone** (run
  `2026-11-12-r2-2.3.10-a-again`, no model call): the case's media seeded as a case film seeds it, the saved edit put in place of
  the seeded one with its ids mapped (a video by its content hash, a picture by its import order and size, the phone's own cut-out
  of the speaker copied in), then exported by Tev's own exporter (the workspace's `scorer-audit/round2/reexport.py`, with a local
  UI test, `ExportSavedProjectUITests`). Rehearsed twice on a simulator first, the two films the same. On the phone the export
  took 17 s, and the film (46.7 s, 1080p/30) was copied whole to the Mac, frame for frame the rehearsals' film (PSNR 40.8 dB; the
  encoders differ).
- **12 November, pair 2 is not blind:** until that export, Angelina's page showed one of pair 2's films as "not made", and she
  knew the missing one was the new version. Her choice is kept and reported apart from the blind pairs (§8). From 17:11 UTC the
  page showed a pair only when both its films existed.
- **12 November, Autumn_Wardrobe has no films:** its two films were among the nine lost that morning, and they were not made
  again (a talking head needs her phone's cut-out of the speaker). Its pair is missing.
- **12 November, found after the films:** no round-2 film took its captions from the environment's transcription model (there
  is no transcription call in any film's turn): the app treated the test account as unpaid, so the captions came from Apple's
  on-device recognizer, for both versions alike. The caption faults Angelina saw (wrong words, phrases rewritten as they built)
  are in both versions' films.

## 8. Results

Angelina's choices were saved on 12 November 2026 at 21:01 UTC, and the versions were revealed to her after that. Four pairs have
films; pair 3 (Autumn_Wardrobe) has none.

| Pair | Case | Made | A's film she saw (2.3.10-a) | B's film she saw (2.3.10) | She preferred |
|---|---|---|---|---|---|
| 1 | Olsens_Oversized | her phone | the revision (0.78 against 0.76) | the revision (0.76 against 0.72) | **B** |
| 2 | Madame_T (not blind) | her phone | the revision (0.80 against 0.74) | the revision (0.87 against 0.76) | **B** |
| 4 | Trousers_Five_Looks | rebuilt on the Mac from the phone's records | the first cut (0.80; its revision 0.76) | the revision (0.88 against 0.82) | **B** |
| 5 | Stella_Boots_Lookbook | a simulator | the first cut (0.72; its revision never judged) | the first cut (0.68; its revision never judged) | **A** |

- **The measure (§4):** A preferred in 1 pair, B in 3, "same" in none; two-sided sign test p = 0.625. The blind pairs alone (1, 4
  and 5): A 1, B 2, p = 1.0. With four pairs no result is a clear one: this is a first look.
- **What the critics changed in the films she saw:** in pairs 1 and 2, both films are their critic's revision. In pair 4, B's
  film is its revision and A's is its first cut (A's revision scored lower, and Tev took it back). In pair 5, neither: in both
  films the revision ended in questions to the owner rather than a last look, so Tev took it back and the first cut stands. Both
  versions use the same Designer, so pair 5 compares two first cuts that differ by chance, not by critic.
- **Critic A's failed requirement lines**, the note its revision gets first: 9 in Olsens_Oversized, 4 in Madame_T, 6 in
  Trousers_Five_Looks and 7 in Stella_Boots_Lookbook; the note reached the revision in all four. The critics' own changes: A 6, 6,
  4 and 5; B 6, 6, 2 and 4.
- **Her choice and the critics' scores:** the film she preferred has the higher kept score in 3 of the 4 pairs (not in pair 1).
  Each critic scored only its own version's film, so this does not compare the two critics' scales.
- **Time and cost:** the turns took A 799, 812, 600 and 1,185 s, and B 579, 908, 901 and 518 s. The films cost A $3.07, $2.49,
  $2.47 and $2.91 ($10.94), and B $2.15, $2.64, $2.54 and $2.05 ($9.38), on her environment's keys; a case's footage descriptions
  are paid by whichever of its films was made first. Round 2 cost $40.66 in all: $20.32 for these eight films, $17.40 for the
  seven other films lost on the morning of 12 November, and $2.94 for a Madame_T new-version film that was never exported (§7).
- **Her reasons**, in her words with spelling and grammar corrected (a Russian word translated); "Film 1" and "Film 2" are the
  page's order. Her words as written stay in the private workspace.
  - Pair 1, Olsens_Oversized (Film 1 was B): "I love the images selected in Film 1 more than in Film 2. Film 2 also missed a zoom
    where I had expected one, at 21–24 s. Maybe the words cover my talking face more in Film 2, but I'm not 100% sure."
  - Pair 2, Madame_T (Film 2 was B): "I love the second one more. In the first, my head sometimes covers the heads and figures of
    the people in the images, and it feels a bit too big. Also, I noticed several times that Tev clips the last word too much:
    instead of 'versatility', it only said 'versatil'. I love that both versions used videos of influencers wearing the Madame T."
  - Pair 4, Trousers_Five_Looks (Film 2 was B): "They're not great, but the second is a bit better. In a lookbook-style video, if
    the item isn't shown separately at the beginning, then all the titles are equal – they're all peers – so the font etc. should
    be the same. '1 trousers - 5 looks' could have been placed either on a frame showing the item on its own (which was missing),
    or shown all the way through, or set apart from 'with the long coat'. 'With the long coat' should have been the same size etc.
    as the other 'with the …' titles. If we keep 'with this and that', I'd have removed '1 trousers - 5 looks'. But the second
    film did better, because the text almost never covered my face and body and was placed in the free space (except for the
    first 2 seconds). Also, I feel both picked not the best parts of the videos – I'm talking, I'm moving, adjusting my clothes,
    etc. I'm sure there are better shots."
  - Pair 5, Stella_Boots_Lookbook (Film 2 was A): "The first is way too long and uses the same dress outfit twice; at 0:11 I'm
    clearly adjusting my top – why select this moment out of all the beautiful and confident ones? In the second, the text could
    have been placed in the free space, not on my head and clothes. However, the second video was edited smartly enough to crop
    out the sockets and not repeat outfits."
- **Reading:** round 2 gives no support to its hypothesis. In the three pairs where a critic shaped at least one of the films she
  saw, she preferred B's film each time (one of these pairs is not blind); the one pair she gave to A has no critic's work in
  either film. Round 1's critic A flagged more of her bad decisions than critic B (§1), but in these films, revising on its
  findings did not make films she preferred. Her reasons name things that neither critic's revision fixed: text over her face
  and body (pairs 1, 4 and 5), the speaker's cut-out too big and over the people in the pictures (pair 2, A), a last word cut
  short (pair 2, A), the moments chosen (pairs 4 and 5), an outfit repeated (pair 5, B), and titles of unequal sizes (pair 4, A).
