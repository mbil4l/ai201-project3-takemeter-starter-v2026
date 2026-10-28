# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter reads comments from [formula1@lemmy.world](https://lemmy.world/c/formula1),
the Formula 1 community on Lemmy, and sorts each one by how much of a *take*
it is: `analysis` (a claim carried by a checkable detail — a lap, gap, points
total, rule or quote), `hot_take` (a confident claim with nothing checkable
behind it), or `reaction` (no arguable claim at all — live narration,
feelings, jokes). It's a DistilBERT model fine-tuned on 236 public comments
from race-weekend live threads, post-race threads and news threads. The use
it's built for: take a 300-comment race thread and pull the handful of posts
that actually argue from evidence out of the noise.



---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

Three labels: a take that is backed, a take that isn't, and a post that isn't
a take at all. All examples are real comments from formula1@lemmy.world, quoted
whole.

### `analysis`

**Definition:** An argument or explanation about F1 where a specific, checkable
detail — a lap, gap, position, points total, tyre call, rule or quote —
carries the point.

**Example 1:** *(2025 Spanish GP, post-race thread)*
> The real punishment is that he is now on 11 penalty points for the next two
> races, even a reasonably minor infraction could result in a race ban.
>
> If he did get a race ban what would be interesting is how RB would fill that
> seat, would Liam get recalled for a race as he has recent experience of car?
> Isack can a crack at it? Who would replace either of them in the Racing Bull?

**Example 2:** *(2024 Monaco GP, race thread)*
> No need to pit. They have already changed to a second compound at the red
> flag. They are going to the end

### `hot_take`

**Definition:** A confident general claim about drivers, teams, races, the FIA
or the sport, with no checkable support offered.

**Example 1:** *(2023 Japanese GP, race thread)*
> RBR sending Perez out again is some passive-aggressiveness at this point.

**Example 2:** *(news thread: Hamilton and Leclerc disqualified from USGP)*
> The FIA can't check every car on the grid for every single rule in the
> regulations. It's not practical, and is a waste of time and money.

### `reaction`

**Definition:** A response to a moment — something on track, a headline,
another comment — through feeling, narration or a joke, with no general claim
to argue with.

**Example 1:** *(2025 Hungarian GP, race thread)*
> They just showed the replay of it. Yikes that looked painful.

**Example 2:** *(2023 Hungarian GP, race thread)*
> Guys I think we should pitch in and hire a therapist for Charles

### The hardest boundary

**Which two labels:** `analysis` and `hot_take`.

The post that forced the rule, from the 2023 Dutch GP race thread:

> Alonso is 3rd, stroll 19th (and by a mile)
>
> Just get stroll out of there, honestly

The positions are real and checkable, and they're obviously why the poster
wants Stroll gone — but the post never says how one race's positions get to
"drop him".

**The decision rule I used every time:** Does the claim reach further than the
detail can carry? A checkable detail makes a post `analysis` only when the
claim stays inside what that detail shows — either the post spells out the
link (*because*, *so*, *and yet*) or the claim follows straight from it. When
the verdict reaches past the detail — one race's positions as the case for
dropping a driver, one season's win count as proof a career is over — it's a
`hot_take` with a number in it, however true the number is. A detail only
counts if it's specific enough to be wrong: a position, lap, gap, points total,
tyre call, rule or quote. "Typical VCARB strategy" is not a detail.

So the Stroll post is `hot_take`: 19th in one race can't carry "get him out".
These two are `analysis`, one with the link spelled out and one where the claim
never leaves the number:

> He was clearly faster than Lec in the first and second stints, and yet
> Ferrari just let him keep station while both their drivers fell back from
> Ver.

> Ferrari just 8 points behind of Red Bull. [P2](https://youtu.be/GLC8c3V0JzE)
> very much in play for them.

The first version of this rule only asked whether the detail was joined by a
connecting word. It split posts that make the same move, so it was tightened
during labelling to the version above, and every `analysis` and `hot_take` row
was re-checked against it (three labels changed). Details in
[notes.md](notes.md).

**The other two boundaries**

- **`hot_take` vs `reaction`:** could someone reply "no, you're wrong" to a
  general claim about the sport? Then it's `hot_take`, however heated and
  however live. If it's about this moment, the writer's feelings, or the joke,
  it's `reaction`. For sarcasm, restate it as a sincere sentence — if the point
  survives as a claim about the sport, it's `hot_take`.
- **`reaction` vs `analysis`:** recency doesn't outrank evidence. A race-thread
  post that explains with a rule or a number is `analysis`.
- **Mixed posts:** label by what most of the words are doing — a tie-break,
  used only after the rules above.

**A label that didn't survive:** the first draft had a fourth label, `banter`,
for posts where the joke is the point. In live threads the jokes *are* the
reactions ("hire a therapist for Charles" is both), and no rule kept them
apart. What jokes and reactions share is that neither makes an arguable claim,
so they merged into `reaction`. The working is in [notes.md](notes.md).



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Public comments from
[formula1@lemmy.world](https://lemmy.world/c/formula1), pulled through Lemmy's
public API by [collect.py](collect.py) — no account needed. The pool was 4,483
comments from 90 threads: 30 live session threads (`[RACE]`, `[QUALIFYING]`,
`[SPRINT]`), 30 post-race threads, and 30 news threads, June 2023 to May
2026. The 236 in `labels.csv` were read and picked from that pool. Every row
links back to its comment in [data/sources.csv](data/sources.csv) (same row
order).

| Thread kind | Rows |
|---|---|
| live — written during the session | 103 |
| post — post-race threads and "X wins" posts | 75 |
| news — articles, quotes, announcements | 58 |

Posts are kept whole, including quoted text from the comment they reply to.
Left out: deleted comments, bot accounts, link-only and image-only replies (at
collection); pure questions, which aren't a take or a reaction; tangents that
aren't about F1 (German energy policy, users trading insults); and eight short
replies that can't be understood without the comment they answer.

**How I labelled them:** All 236 rows were pre-labelled with an AI tool working
from the definitions and decision rules in the Label Taxonomy above. Every row
is marked `pre-labelled` in the `note` column, and the ones that were hard
calls carry the reason in the note as well. 20 rows are set aside, text only,
in `cold_round.csv` for an unaided round; [cold_merge.py](cold_merge.py)
writes those labels back into `labels.csv`, marks them `cold`, and reports the
agreement with the pre-labels.

Thread kind and label line up the way you'd expect but not perfectly — 54 of
the 89 `reaction` posts come from live threads, but so do 23 of the 65
`analysis` posts (rule explanations and strategy arguments written mid-race).

| | live | post | news |
|---|---|---|---|
| `analysis` | 23 | 23 | 19 |
| `hot_take` | 26 | 27 | 29 |
| `reaction` | 54 | 25 | 10 |

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `analysis` | 65 | 27.5% |
| `hot_take` | 82 | 34.7% |
| `reaction` | 89 | 37.7% |
| **Total** | 236 | 100% |

`reaction` was the easiest to collect and went over 40% (criterion 3) before
the eight context-dependent replies were trimmed. `analysis` was the hardest —
long news and post-race comments were read first to find enough of it.

**Three hard cases**

**1.**
> *The post:* "226 point lead on his teammate, and 2nd place. Max had been
> unbelievable this season." *(2023 Mexico City GP, race thread)*
>
> *Could have been:* `analysis` or `hot_take`.
>
> *I chose, because:* `analysis`. Structurally it's the Stroll post — a stat
> set beside a verdict, no connecting word. But a 226-point lead over a
> teammate in the same car carries "unbelievable this season" all on its own;
> the claim never reaches past the number. This post is why the decision rule
> changed from "is there a connecting word?" to "does the claim reach further
> than the detail?" — the old version called it `hot_take`.

**2.**
> *The post:* "I am fairly sure this is the worst race I have ever seen. Might
> as well have called it 80 formation laps. Jesus." *(2024 Monaco GP, race
> thread)*
>
> *Could have been:* `reaction` or `hot_take`.
>
> *I chose, because:* `hot_take`. It reads like a live reaction, but "worst race
> I have ever seen" ranks this race against every other race, which is a
> general claim someone could argue with. The rule I applied: a verdict on just
> this race ("Man that was boring") is `reaction`; a ranking against other
> races ("best race in years", "best since 2021") is `hot_take`.

**3.**
> *The post:* "Oh my god that was dangerous from Ocon, Gasly is absolutely right
> to be pissed. / Ocon literally did what he did to Perez back at Force India -
> overtake stupidly and leave no room for his teammate." *(2024 Monaco GP, race
> thread)*
>
> *Could have been:* `reaction` or `analysis`.
>
> *I chose, because:* `analysis`. The first line is pure reaction. The second
> argues "this is a pattern" from a named, checkable precedent (Ocon and Perez
> at Force India), and the claim stays within what two incidents can show.
> Recency doesn't outrank evidence — being written thirty seconds after the
> crash doesn't make it a reaction.

More hard cases are flagged in the `note` column of `labels.csv` and listed in
[notes.md](notes.md).

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`, fine-tuned for three-way
classification by `takemeter.ipynb` (sections 1–5).

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, 128 tokens per post,
seed 42.

**Device:** `cpu` — PyTorch `2.14.1+cpu`, recorded in `results.json`. The
laptop has an NVIDIA GPU, but the PyTorch wheel `pip install -r
requirements.txt` installs on Windows is CPU-only, so training didn't use it.
The full run (sections 1–5) took about a minute.

**Anything I changed from the defaults, and why:** Nothing. Every setting is
the notebook default. 128 tokens is enough for this data: the median post is
38 tokens, and only 4 of the 236 run past 128 and get truncated (2 `analysis`,
1 `hot_take`, 1 `reaction`).

**Split sizes:** 236 rows → train 164 · val 36 · test 36, stratified.

| Label | Train | Val | Test |
|---|---|---|---|
| `analysis` | 45 | 10 | 10 |
| `hot_take` | 57 | 13 | 12 |
| `reaction` | 62 | 13 | 14 |

Every label has at least 8 posts in the test split, so the notebook raised no
thin-label note. `analysis` is still the smallest at 10, and with 36 test posts
each post is worth about 2.8 points of accuracy. That's the main thing to
expect between seeds in unit 6.

`results.json` and `test_split.csv` are committed. The numbers haven't been
read against the criteria yet — that's unit 6.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Pre-labelling disclosure:** All 236 rows in `labels.csv` were pre-labelled
with an AI tool from the definitions and decision rules in the Label Taxonomy,
and are marked `pre-labelled` in the `note` column. The 20 rows in
`cold_round.csv` are for the unaided round and get marked `cold` when merged.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

Both columns are scored on the same 36 held-out posts in `test_split.csv`
(seed 42's test split, committed in unit 5). Baseline: `facebook/bart-large-mnli`
zero-shot, run locally with `python baseline.py --trained results.json`,
prompted with the three definitions in `label_definitions.txt`. Output in
`baseline_results.json`.

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.306 | 0.500 | +0.194 |
| Macro F1 | 0.196 | 0.464 | +0.268 |
| F1 — `analysis` | 0.476 | 0.444 | -0.032 |
| F1 — `hot_take` | 0.000 | 0.300 | +0.300 |
| F1 — `reaction` | 0.111 | 0.647 | +0.536 |

**The same baseline with bare label names** (no `label_definitions.txt`;
`python baseline.py --definitions no_definitions.txt --out
baseline_results_bare_names.json --trained results.json`). Run on purpose, to
measure what the definitions were worth:

| Measure | Baseline (bare names) | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.500 | 0.500 | +0.000 |
| Macro F1 | 0.437 | 0.464 | +0.027 |
| F1 — `analysis` | 0.182 | 0.444 | +0.263 |
| F1 — `hot_take` | 0.485 | 0.300 | -0.185 |
| F1 — `reaction` | 0.643 | 0.647 | +0.004 |

**What my definitions were worth to the baseline: −0.194 accuracy.** The
definitions made the zero-shot model *worse*. Its predictions show why:

| Baseline prompt | Predicted `analysis` | Predicted `hot_take` | Predicted `reaction` |
|---|---|---|---|
| With definitions | 32 | 0 | 4 |
| Bare names | 1 | 21 | 14 |

With definitions it called 32 of 36 posts `analysis` and never once said
`hot_take`. All three definitions are about F1, but only `analysis` starts by
saying so ("an argument or explanation about F1…"), and every post in the set is
about F1 — so that hypothesis is "entailed" by nearly everything. The other two
definitions do their work with negations ("with *no* checkable support
offered", "with *no* general claim to argue with"), and an entailment model
reads the topic words and largely ignores the "no". The definitions were
written for a person; as a prompt they reward the one label whose wording
matches the topic.

Runtime: each baseline run took about 27 seconds for 36 posts on the laptop CPU
(model load included, two runs side by side). The trained DistilBERT scores the
same 36 posts in well under a second. It's slower but nowhere near "a few
seconds per post" on this machine.

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

*Written and committed before `baseline.py` was run (see the commit history).*

The trained model will beat the baseline clearly on `reaction` — short
live-thread lines and jokes are a register a model only learns from examples,
and "a response to a moment … with no general claim" is a negative definition
an entailment model has little to grip — while the baseline will come closest
on `analysis`, because "a specific, checkable detail (a lap, gap, position,
points total…)" is something a general model can spot from the definition
alone.

One honest caveat: the unit 5 notebook printed the trained model's seed-42
accuracy (0.500) when it wrote `results.json`, so the trained column was not a
complete unknown. The prediction above is about where the *baseline* would land
against it, label by label, which nothing had shown me yet.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

**How the prediction did:** right on `reaction` (+0.536, the biggest gap in
the table). On `analysis` it was right in the letter but for the wrong reason.
The baseline did come closest there, and even edged ahead (0.476 vs 0.444), but
not by spotting checkable details: it called almost *everything* `analysis`, so
its recall was 1.00 and its precision 0.31. That is a label it guessed, not one
it found.

**What the gap means:**

- Against the baseline as the brief defines it (definitions as the prompt),
  fine-tuning bought +0.194 accuracy and +0.268 macro F1, nearly all of it on
  `reaction` and `hot_take`, the two labels the zero-shot prompt couldn't tell
  apart from `analysis`.
- **Against the bare-names baseline, fine-tuning added nothing on accuracy:**
  both are 0.500 on the same 36 posts. The trained model is better on
  `analysis` (+0.263) and worse on `hot_take` (−0.185), so the two models are
  making *different* mistakes at the same rate rather than one being better.
- Taken together: 164 training posts taught DistilBERT about as much as the
  bare words "analysis / hot_take / reaction" give a general model for free.
  This is seed 42 only. The three-seed run below says whether 0.500 is typical.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

**Run conditions:** notebook sections 1–7 run top to bottom, section 6 with
`RUN_LABEL = "before"` → `results_three_seeds_before.json`. Device **`cpu`**
(PyTorch `2.14.1+cpu`, no CUDA build on Windows). Every setting is the unit 5
default: 3 epochs, learning rate 2e-5, batch 16, 128 tokens. Each seed: 164
train / 36 val / 36 test, stratified. About 47 seconds of training per seed.
Seed 42 reproduced unit 5's `results.json` exactly, so CPU training is
deterministic here.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 on every seed | 0.500 | 0.500 | 0.583 | **MISSED** |
| 2. No label left behind | F1 ≥ 0.40 `analysis`; ≥ 0.50 `hot_take` and `reaction`; every seed | A 0.444 · H **0.300** · R 0.647 | A **0.000** · H **0.444** · R 0.636 | A 0.588 · H 0.500 · R 0.645 | **MISSED** |
| 3. Balance | every label 25–40% of `labels.csv` | 27.5 / 34.7 / 37.7% | 27.5 / 34.7 / 37.7% | 27.5 / 34.7 / 37.7% | **MET** |
| 4. Agreement with staff set | ≥ 23 / 30 | one measurement, not per seed: **pending the staff key** (see Agreement Report) | — | — | **PENDING** |
| 5. Confidence means something | most-sure third − least-sure third ≥ 0.20 on every seed | 0.417 (0.667 − 0.250) | 0.500 (0.917 − 0.417) | 0.333 (0.667 − 0.333) | **MET** |

A = `analysis`, H = `hot_take`, R = `reaction`. Bold cells are the ones under
target. Criterion 3 counts the file, so it can't move between seeds.

**The spread table, as section 6 printed it:**

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.500 | 0.500 | 0.583 | 0.083 |
| Macro F1 | 0.464 | 0.360 | 0.578 | 0.218 |
| F1 — `analysis` | 0.444 | 0.000 | 0.588 | 0.588 |
| F1 — `hot_take` | 0.300 | 0.444 | 0.500 | 0.200 |
| F1 — `reaction` | 0.647 | 0.636 | 0.645 | 0.011 |

**Reading the spread.** Accuracy moved 8.3 points, under the 10-point line for
an unstable measure, but that's one test post in either direction of three
(each post is 2.8 points). The real instability is per label: `analysis` F1
runs from 0.000 to 0.588. On seed 7 the model **never predicted `analysis` at
all**. It sent 30 of 36 test posts to `reaction`. `reaction` is the only
stable number (0.636–0.647), and it's stable because the model guesses it by
default, not because it found it. Its precision is 0.47–0.59 on every seed.

### Confusion matrix

Seed 42, as notebook section 7 prints it (rows = true label, columns = the
model's guess):

| true \ predicted | analysis | hot_take | reaction |
|---|---|---|---|
| **analysis** | 4 | 4 | 2 |
| **hot_take** | 2 | 3 | 7 |
| **reaction** | 2 | 1 | 11 |

Section 7 only prints the first seed, so here are all three seeds' test splits
summed (108 predictions), from `results_three_seeds_before.json`:

| true \ predicted | analysis | hot_take | reaction |
|---|---|---|---|
| **analysis** | 9 | 9 | 12 |
| **hot_take** | 3 | 13 | 20 |
| **reaction** | 3 | 4 | 35 |

Column totals: the model guessed `reaction` 67 times out of 108 (62%) when
39% of the posts were `reaction`, and guessed `analysis` only 15 times for 30
real ones.

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

7 real `hot_take` posts were called `reaction` on seed 42 (20 across all three
seeds) and only 1 went the other way (4 across three), so the model hasn't
learned my `hot_take`/`reaction` line, "is there a general claim someone could
argue with?", and resolves every doubt toward `reaction`. The same lean shows
on `analysis` (12 to `reaction`, 3 back). So this is mostly a model that
falls back on the most common label, not one boundary on its own. Milestone 4
works out which.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** **pending.** `data/staff_labels.csv` hasn't arrived from
my TF, and it isn't in the starter. The `data/` folder ships `staff_posts.csv`
(ids and text only) and `staff_taxonomy.md`, but no labels. `python
agreement.py` stops at "No file at data/staff_labels.csv". I won't guess the key.

**What is done:** all 30 posts are labelled under `data/staff_taxonomy.md`,
saved as [`my_staff_labels.csv`](my_staff_labels.csv) (text copied
programmatically from `staff_posts.csv`, so every row will match), and
committed in `16504af` *before* any key existed on this machine. The `note`
column gives my reasoning on every call that wasn't obvious, written at
labelling time.

| | `analysis` | `hot_take` | `reaction` |
|---|---|---|---|
| My labels | 10 (sp_001–010) | 10 (sp_011–020) | 10 (sp_021–030) |

My labels fall in three clean blocks in file order. I labelled each post on its
own against the rules, but the pattern is worth flagging: the staff note says
several of these were picked *because* they're ambiguous. Any place the staff
key breaks those blocks is a post where the authors read a rule differently
from me, and those are the ones to argue.

**The calls I expect to be argued, with my reasoning from the staff rules**
(written before the key, so it can't bend to fit it):

| Post | My label | The other defensible label | Why I chose mine |
|---|---|---|---|
| sp_014 "Times are down about 3% since the shoe rules changed, so obviously the shoes are the whole story…" | `hot_take` | `analysis` | It's rule 1's own `hot_take` example with "so obviously" added. The "so" makes the 3% *look* like the reason, but 3% can't carry "the whole story" (nothing rules out other causes) or "the sport has a problem". Rule 1's `analysis` version earns its label by lining up the dates and hedging ("most likely single cause"). This one does neither. |
| sp_010 "Three of us ran the same session… within 10 seconds…" | `analysis` | `hot_take` | n = 3 and nothing is controlled, so the argument is weak. But rule 1 asks whether the fact is load-bearing, not whether the argument is good, and the claim is scoped to what the 10-second spread shows ("smaller than the noise between three people"). |
| sp_002, sp_005, sp_007 (personal tracking: sleep, shoes vs mileage, heat) | `analysis` | `reaction` | All three are "about the writer's own experience", which is the `reaction` definition's wording. But none is immediate (eleven weeks, two years, a fortnight), and each uses its own numbers as the reason for a general claim. Rule 3: recency doesn't decide it, a load-bearing fact does. |
| sp_016 "gel before 90 minutes", sp_017 "peaked in about 2015", sp_018 "slower than 8 minute miles" | `hot_take` | `analysis` | Each number is *part of the claim*, not support for it. A threshold isn't evidence. |
| sp_020 "Every injury thread on this forum is the same injury…" | `hot_take` | `reaction` | Exasperated, but rule 2 says heated posts can still be `hot_take` if they assert something general, and this asserts something about every thread. |
| sp_021 "Four minutes off. FOUR.", sp_027 "leaning at about 20 degrees" | `reaction` | `analysis` | The numbers *are* the news (or hyperbole). Nothing is argued from them. |
| sp_029 "the shoes I set every PB in… bought by accident in the wrong size" | `reaction` | `hot_take` / `analysis` | It invites "shoes don't matter", but never says it. It's a realisation about the writer's own year, which is rule 2's `reaction` side. |

**The post I'd bring to the breakout:** sp_014. Making the strongest case for
each label from the staff definitions alone (the "working on your own" prompt):

- *For `analysis`:* it contains a specific, checkable stat and the writer
  explicitly makes it the reason ("…changed, **so** …"). Rule 1's `hot_take`
  example is marked as such because the 3% is "offered as a flourish, not as
  the reason", and here it *is* offered as the reason.
- *For `hot_take`:* rule 1 asks whether the fact *carries* the argument, not
  whether a connecting word is present. "Obviously … the whole story" is a
  conclusion the 3% cannot reach on its own; the `analysis` version in the
  taxonomy only gets there by adding the matching date and hedging.

My call stays `hot_take`. A connecting word is what my *own* first rule asked
for in unit 5, and I threw that rule out because it split posts that make the
same move (see the Label Taxonomy). Rule 1 here is my revised rule in other
words.

**To finish this section when the key arrives:** save it as
`data/staff_labels.csv` (columns `id,label`), run `python agreement.py`, commit
`agreement_results.json`, then fill one block below per disagreement and the
criterion 4 verdict.

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

*None listed yet: there is nothing to disagree with until the staff key
arrives.* One block per disagreement goes here, in this shape:

> *The post:* (sp_0xx, quoted)
>
> *Staff said / I said:*
>
> *My call, and why:* (argued from rules 1–4 in `data/staff_taxonomy.md`;
> the table above already holds my reasoning for the likeliest ones)
>
> *Which pile:* (a) applied loosely · (b) rule doesn't say · (c) ambiguous,
> my reading defensible

**What the pattern in my disagreements tells me:** *pending the key.* What to
look for when it arrives: rule 1 here (does the fact carry the argument?) is
the same move as my own `analysis`/`hot_take` rule, and rule 2 (claim vs. the
writer) is my `hot_take`/`reaction` rule. Disagreements that sit in pile (a) on
rule 2 would be direct evidence that I also applied my own `hot_take`/`reaction`
line loosely across the 236, the pair the confusion matrix mixes up most.



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
