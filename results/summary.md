# Results

Looks: {"A": {"first": 27, "second": 13, "failed": []}, "B": {"first": 27, "second": 13, "failed": []}}; cost $35.1

## Q1, Agreement (first looks)
- Critic A: bad flagged 0.735 (50/68; bootstrap 0.652 to 0.837; exact 0.614 to 0.835); good flagged 0.294 (5/17; bootstrap 0.071 to 0.45; exact 0.103 to 0.56)
  - zooms: bad 0.455 (5/11; bootstrap 0.182 to 0.778; exact 0.167 to 0.766); good 0.286 (2/7; bootstrap 0.0 to 0.5; exact 0.037 to 0.71)
  - titles: bad 0.789 (45/57; bootstrap 0.714 to 0.878; exact 0.661 to 0.886); good 0.300 (3/10; bootstrap 0.0 to 0.5; exact 0.067 to 0.652)
  - ties counted as flagged: bad 0.735 (50/68; bootstrap 0.652 to 0.837; exact 0.614 to 0.835)
  - extended words (sensitivity): bad 0.750 (51/68; bootstrap 0.662 to 0.86; exact 0.63 to 0.847)
- Critic B: bad flagged 0.506 (41/81; bootstrap 0.38 to 0.629; exact 0.393 to 0.619); good flagged 0.316 (6/19; bootstrap 0.143 to 0.55; exact 0.126 to 0.566)
  - zooms: bad 0.379 (11/29; bootstrap 0.175 to 0.696; exact 0.207 to 0.577); good 0.333 (4/12; bootstrap 0.091 to 0.636; exact 0.099 to 0.651)
  - titles: bad 0.577 (30/52; bootstrap 0.464 to 0.702; exact 0.432 to 0.713); good 0.286 (2/7; bootstrap 0.0 to 0.333; exact 0.037 to 0.71)
  - ties counted as flagged: bad 0.506 (41/81; bootstrap 0.38 to 0.629; exact 0.393 to 0.619)
  - extended words (sensitivity): bad 0.519 (42/81; bootstrap 0.388 to 0.651; exact 0.405 to 0.631)

## Q2, Compared (bad decisions counting for both critics)
- B minus A -0.140 (A 42, B 34 of 57; bootstrap -0.26 to -0.032)
- zooms: B minus A +0.250 (A 3, B 5 of 8; bootstrap 0.0 to 0.6); titles: B minus A -0.204 (A 39, B 29 of 49; bootstrap -0.309 to -0.1)
- ties counted as flagged: B minus A -0.140 (A 42, B 34 of 57; bootstrap -0.26 to -0.032); extended words: B minus A -0.140 (A 43, B 35 of 57; bootstrap -0.267 to -0.018)
- good decisions: B minus A +0.182 (A 2, B 4 of 11; bootstrap 0.0 to 0.364)

## Q3, Stable (13 films)
- Critic A: same flag in both looks 0.894 (42/47; bootstrap 0.852 to 0.952; exact 0.769 to 0.965); flagged 32 then 31
- Critic B: same flag in both looks 0.723 (34/47; bootstrap 0.521 to 0.878; exact 0.574 to 0.844); flagged 28 then 25

## The prediction
- Misses, on bad decisions: B minus A -0.140 (A 42, B 34 of 57; bootstrap -0.26 to -0.032) (right if above 0)
- Good zooms: A minus B -0.200 (B 2, A 1 of 5; bootstrap -0.5 to 0.0) (right if above 0)

## Exploratory
```
{
 "seen": {
  "A": {
   "seen": {
    "k": 49,
    "n": 66,
    "share": 0.742,
    "cp": [
     0.62,
     0.842
    ],
    "boot": [
     0.659,
     0.843
    ]
   },
   "unseen": {
    "k": 1,
    "n": 2,
    "share": 0.5,
    "cp": [
     0.013,
     0.987
    ],
    "boot": [
     0.5,
     0.5
    ]
   }
  },
  "B": {
   "seen": {
    "k": 41,
    "n": 78,
    "share": 0.526,
    "cp": [
     0.409,
     0.64
    ],
    "boot": [
     0.403,
     0.643
    ]
   },
   "unseen": {
    "k": 0,
    "n": 3,
    "share": 0.0,
    "cp": [
     0.0,
     0.708
    ],
    "boot": [
     0.0,
     0.0
    ]
   }
  }
 },
 "chance": {
  "A": {
   "bad": 0.533,
   "good": 0.417
  },
  "B": {
   "bad": 0.267,
   "good": 0.2
  }
 },
 "changes_per_look": {
  "A": {
   "looks": 27,
   "mean_changes": 5.33,
   "mean_naming_zoom_or_title": 3.15
  },
  "B": {
   "looks": 27,
   "mean_changes": 4.59,
   "mean_naming_zoom_or_title": 3.33
  }
 },
 "film_scores": {
  "A": {
   "films": 19,
   "spearman": 0.817,
   "p": 0.0,
   "released": 0,
   "mean_rating_released": null,
   "mean_rating_held": 2.17,
   "stable_films_mean_abs_score_change": 0.028,
   "stable_films_release_changed": 0
  },
  "B": {
   "films": 20,
   "spearman": 0.847,
   "p": 0.0,
   "released": 0,
   "mean_rating_released": null,
   "mean_rating_held": 2.33,
   "stable_films_mean_abs_score_change": 0.032,
   "stable_films_release_changed": 0
  }
 }
}
```
