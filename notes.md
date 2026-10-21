# Working notes

Running notes for unit 5, in the order things were decided. The README is the
write-up; this is where the decisions came from.

---

## Milestone 1 — community

**Community:** [formula1@lemmy.world](https://lemmy.world/c/formula1) — the
Formula 1 community on Lemmy. ~11,000 subscribers, ~28,000 comments since mid
2023.

**Why this one**

- Public. Lemmy has no invite wall and its API serves comments without an
  account.
- A sport, not a single show or release, so there is no spoiler problem beyond
  ordinary race results.
- Real variation in quality. The same thread holds lap-time arguments, one-line
  verdicts on drivers and pure jokes.
- Three different kinds of thread, which pull the writing in different
  directions:
  - **live** — `[RACE]`, `[QUALIFYING]`, `[SPRINT]` discussion threads,
    written while the session is running
  - **post** — `[POST RACE]` threads and "X wins the Y Grand Prix" posts
  - **news** — articles, driver quotes, FIA announcements

**Reading pass:** 45 comments drawn at random from the newest, top and hot
lists, across all three thread kinds and 2023–2026.

### Candidate distinctions — things that are actually in the text

1. **Some posts carry a checkable detail; most don't.** "Lewis asks for a swap
   because he had better tires and they wait 4 laps to even radio Charles."
   "Even the cheapest 3 day tickets are over $800." Against: "Ferrari strategy
   doesn't seem to be very dynamic." Both are about Ferrari strategy; only one
   could be checked.
2. **Live-thread posts narrate the moment; news-thread posts argue about the
   sport.** "Albon in the wall oof. Blessing for Antonelli to catch up." is
   about the last thirty seconds. "F1 doesn't genuinely care about being road
   relevant" is about the last thirty years.
3. **A big share are jokes where the punchline is the whole post.** "Must be
   difficult to find so many people called Jack" (on McLaren's 1.80s pit stop).
   "The year is 2073. Alonso's great-grandson gets his first contract…" Nothing
   in them could be agreed or disagreed with.
4. **Some posts explain how the sport works and argue nothing.** "Teams are not
   allowed to drive their cars on track outside of a few set moments…" —
   factual, checkable, no opinion.

Also noticed, not a distinction: questions ("Is it $5?"), link-only and
image-only replies, and off-topic politics show up in every thread. Link-only
and image-only posts carry no text to classify and get dropped at collection.

---

## Milestone 2 — labels

Second reading pass: 90 comments from the collected pool (`collect.py`),
spread across live, post and news threads.

### First draft: four labels

| Label | Draft definition |
|---|---|
| `analysis` | argues a point with a specific, checkable fact |
| `hot_take` | a confident claim with no support |
| `reaction` | an immediate response to what is happening on track |
| `banter` | the point of the post is the joke |

`banter` came straight from distinction 3. It did not survive the reading.

**Why `banter` wouldn't hold.** In live threads the jokes *are* the reactions.
"Guys I think we should pitch in and hire a therapist for Charles" is posted
seconds after Leclerc's race goes wrong — it is a joke and it is a reaction to
the moment, equally. "Two local heroes on the podium today! 😅 (Brazil borders
France)" is the same. There was no sentence that put these on one side of a
reaction/banter line and kept them there.

What jokes and live reactions *do* share is that neither makes a claim anyone
could argue with. That is the line that held, so they merged into one label:
`reaction` now means "no arguable claim", whatever the tone.

This gives the taxonomy a shape that fits a take-meter: a take that is backed,
a take that isn't, and a post that isn't a take.

### Final labels

- **`analysis`** — an argument or explanation about F1 where a specific,
  checkable detail (a lap, gap, position, points total, tyre call, rule or
  quote) carries the point.
- **`hot_take`** — a confident general claim about drivers, teams, races, the
  FIA or the sport, with no checkable support offered.
- **`reaction`** — a response to a moment (something on track, a headline,
  another comment) through feeling, narration or a joke, with no general claim
  to argue with.

Explainers (distinction 4) fold into `analysis`: "No need to pit. They have
already changed to a second compound at the red flag" uses a rule to make a
point, even with no opinion in it.

**Collection rule that follows from this:** pure questions are left out. They
are neither a take nor a reaction to anything, and there aren't enough of them
to be worth a fourth label.

### The borderline post

> Alonso is 3rd, stroll 19th (and by a mile)
>
> Just get stroll out of there, honestly

*2023 Dutch GP race thread.* Between `analysis` and `hot_take`. The positions
are real and checkable, and they are clearly why the poster wants Stroll gone.
But the post never says *how* one race's positions get to "drop him".

Compare, from the 2023 Austrian GP race thread:

> He was clearly faster than Lec in the first and second stints, and yet
> Ferrari just let him keep station while both their drivers fell back from
> Ver.

Here the detail is connected to the claim: faster, *and yet* held station, so
both lost ground. That's an argument.

**Decision rule (analysis vs hot_take):** does the post show how the detail
gets to the claim? If a checkable detail is joined to the conclusion by
reasoning — *because*, *so*, *and yet*, *which means* — it's `analysis`. If the
detail just sits beside a verdict, it's a `hot_take` with a number in it,
however true the number is. A detail only counts if it is specific enough to be
wrong: a position, lap, gap, points total, tyre call, rule or quote. "Typical
VCARB strategy" is not a detail.

→ The Stroll post is `hot_take`. The Ferrari post is `analysis`.

### Other boundaries

- **`hot_take` vs `reaction`:** could someone reply "no, you're wrong" to a
  general claim about the sport? Then it's `hot_take`, however heated and
  however live. If the post is about this moment, the writer's feelings, or
  the joke, it's `reaction`. Sarcasm: restate it as a sincere sentence. If the
  point survives as a claim about the sport, it's `hot_take`.
- **`reaction` vs `analysis`:** recency doesn't outrank evidence. A live-thread
  post that explains with a rule or a number is `analysis`.
- **Mixed posts:** label by what most of the words are doing. A tie-break, used
  only after the rules above.

### Stress test — eight posts written to sit on the boundaries

Eight made-up posts, each aimed at a boundary, classified with the rules above
and no other help.

| # | Post | Boundary | Call | Clean? |
|---|---|---|---|---|
| 1 | Hamilton is cooked. Zero wins all season. | analysis / hot_take | `hot_take` | Not at first — see below |
| 2 | Norris has lost 4 of his last 5 starts to Piastri off the line, so P1 isn't the advantage it looks like for him. | analysis / hot_take | `analysis` | Yes |
| 3 | LMAO Stroll in the gravel again, someone get this man a sim rig | reaction / (banter) | `reaction` | Yes, once `banter` was gone |
| 4 | Monaco should be dropped. Nobody can overtake there. | analysis / hot_take | `hot_take` | Yes — "nobody can overtake" is a generalisation, not a detail |
| 5 | Can't believe Ferrari pitted him there, I'm actually shaking | reaction / hot_take | `reaction` | Yes |
| 6 | Leclerc pitted on lap 18 for hards — 40 laps on one set at a track where everyone two-stopped last year. He's not making it. | reaction / analysis | `analysis` | Yes, rule "recency doesn't outrank evidence" |
| 7 | Imagine paying $800 for a Vegas ticket to watch a DRS train lol | hot_take / reaction | `hot_take` | No — the hardest of the eight |
| 8 | Ferrari's strategists are the worst on the grid. | hot_take / reaction | `hot_take` | Yes |

**What changed because of it**

- **Post 1** broke the first version of the analysis rule, which only asked
  whether a checkable fact was *present*. "Zero wins all season" is present,
  checkable and true, and the post is still obviously a verdict. That is where
  "does the post show how the detail gets to the claim?" came from. Before the
  stress test, the Stroll post above would have been `analysis`.
- **Post 7** is a joke, has a number, and makes a claim. Restating it gives
  "Vegas is bad value for a boring race" — the point survives, so `hot_take`.
  The $800 sits beside the verdict rather than arguing it. This is the pattern
  to watch for while labelling: sarcastic posts with a stat in them.
- **Post 3** is the clearest case for dropping `banter`: under four labels it
  is both `reaction` and `banter` with nothing to choose between them.

---

## Milestone 4 — collecting and labelling

**Pool:** `python collect.py` → 4,483 comments from 90 threads (30 live, 30
post, 30 news), June 2023 – May 2026.

**Reading order.** Four batches, ~290 posts read in total, aimed at the label
that was running short:

1. Long comments containing a number, a lap, a tyre, a penalty or a rule —
   most likely to be `analysis`.
2. Live-thread comments — mostly `reaction`.
3. News and post-race comments — mostly `hot_take`.
4. Long post-race comments and short number-free news comments, to top up
   `analysis` and `hot_take`.

Skipped while reading: pure questions, off-topic tangents (German energy
policy, users insulting each other), and posts that only make sense next to an
image.

### The rule changed during labelling

The Milestone 2 rule for `analysis` vs `hot_take` asked whether the detail was
*joined* to the claim by a connecting word. Batch 2 broke it:

- "226 point lead on his teammate, and 2nd place. Max had been unbelievable
  this season." — no connecting word, so `hot_take` under the old rule.
- "That would've been driver of the day for me too. From 19th to 8th in the
  first half of the race." — same.

But in both, the detail fully carries the claim. What actually separates them
from the Stroll post is that Stroll's claim ("get him out") reaches far past
one race's positions. New rule: **does the claim reach further than the detail
can carry?** README updated to match.

**Re-check.** Every `analysis` and `hot_take` row with a number or a named
result in it was re-read under the new rule. Three changed:

| Post (start) | Was | Now | Why |
|---|---|---|---|
| "226 point lead on his teammate…" | `hot_take` | `analysis` | the stat carries "unbelievable this season" |
| "Marko was born in 1943 within a country annexed…" | `analysis` | `hot_take` | a birth year can't carry a claim about his views |
| "Max going for the fastest lap at the end shows… dominance in all aspects" | `analysis` | `hot_take` | one fastest-lap attempt can't carry "all aspects" |

### Hard cases

Each is flagged in the `note` column too.

| Post (start) | Between | Chose | Because |
|---|---|---|---|
| "Alonso is 3rd, stroll 19th (and by a mile)…" | analysis / hot_take | `hot_take` | one race's positions can't carry "get him out" |
| "226 point lead on his teammate, and 2nd place…" | analysis / hot_take | `analysis` | the claim stays inside the number |
| "Max going for the fastest lap at the end shows…" | analysis / hot_take | `hot_take` | "all aspects" reaches past one lap |
| "Marko was born in 1943…" | analysis / hot_take | `hot_take` | the fact is background, not support |
| "I am fairly sure this is the worst race I have ever seen…" | reaction / hot_take | `hot_take` | ranks the race against all others |
| "Couldn't agree more. Best race in years. Goosebumps…" | reaction / hot_take | `hot_take` | same rule — a ranking is a claim |
| "Oh my god that was dangerous from Ocon… Force India…" | reaction / analysis | `analysis` | named precedent, claim stays within it |
| "…MV finishing 20s+ seconds ahead of the 2nd is not what I want to tune in every Sunday for…" | reaction / analysis | `reaction` | the number describes the moment; the "claim" is a preference |
| "Race was alright until that safety car made it spicy… 11 penalty points…" | reaction / analysis | `reaction` | a recap; the penalty maths is one line of nine |
| "If only there was an Mercedes-AMG Petronas F1 Team with connections to both countries…" | reaction / hot_take | `hot_take` | sarcasm restates as "Mercedes should push for those races" |

**Pattern worth remembering for unit 6:** seven of the ten hard cases involve
`hot_take`. The three `analysis` vs `reaction` cases are all race-weekend
posts — live comments or post-race recaps — where a number shows up inside a
reaction.

### Final file

- 236 rows: `analysis` 65, `hot_take` 82, `reaction` 89.
- `reaction` was 95 of 236 (40.3%) before trimming eight replies that can't be
  understood without their parent comment ("yeah I love when he got that type
  of mojo", "Okay, see you guys after the summer break", …).
- The README's example posts are in the file with the labels the README gives
  them.
- 20 rows (6 / 7 / 7, none of them hard cases or README examples) copied to
  `cold_round.csv` with the label blank, for the unaided round.
