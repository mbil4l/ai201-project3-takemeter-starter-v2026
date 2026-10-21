# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy is at least 0.60

Accuracy on the held-out test split is **at least 0.60 on every one of the
three seeds** (42, 7, 2024).

**Why this target:** With three labels planned at roughly 60 / 70 / 70, always
guessing the biggest label scores about 0.35, and a coin flip about 0.33. A
test split of ~30 posts means 0.60 is 18 right, and one post is worth 3.3
points, so a target of 0.70 would rest on two or three lucky posts. 0.60 is the
lowest score at which I'd trust it as a first-pass sort of a race thread —
right more often than not, by a clear margin over guessing.

---

## 2. No label is left behind: F1 ≥ 0.50, and ≥ 0.40 for `analysis`

On every one of the three seeds, `hot_take` and `reaction` each have an F1 of
**at least 0.50** on the test split, and `analysis` has an F1 of **at least
0.40**.

**Why this target:** A take-meter that never finds `analysis` has missed the
only label that marks a substantial post, so a high overall accuracy built on
the other two would be hiding a failure. `analysis` gets the looser floor
because it is the label this community writes least — I expect about 55–60
examples, so only ~9 in the test split, where one post moves F1 by 0.05–0.10
and seeds will swing it. `hot_take` and `reaction` should have ~70 each and a
steadier score, so they're held higher.

---

## 3. Balance: every label is between 25% and 40% of `labels.csv`

In the final `labels.csv`, **no label is more than 40% of the rows and none is
under 25%.** Checked by counting the file.

**Why this target:** The brief's cap is 70%, which for three labels still
allows one label to drown the other two. Reading the community, `reaction`
dominates live race threads and `analysis` is rare everywhere, so the file will
drift lopsided unless I collect against it. 25% of 200 is 50 rows, which is
roughly the fewest that leaves ~8 posts per label in the test split — the point
below which the notebook itself warns a label's F1 is too small to measure. 40%
keeps a "guess the biggest label" model at or under 0.40 accuracy, well under
criterion 1.

---

## 4. Consistency: at least 23 of 30 agree with the staff set (77%)

On the unit 6 agreement check — the 30 staff posts labelled under
`data/staff_taxonomy.md` — my labels match the staff labels on **at least 23 of
30**.

**Why this target:** The staff note says a rate in the 70s is normal because
several posts were picked for being ambiguous, so 23/30 is the upper-middle of
"normal", not a free pass. I'm holding myself above the bottom of that range
because my own hardest boundary is the same one as staff rule 1 — whether a
fact actually carries the argument — and I've already had to write a rule for
it. If I can't apply *their* version of that rule consistently on 30 posts, I
have no grounds to believe I applied mine consistently across 200.

---

## 5. Confidence means something: the confident third beats the unsure third by 0.20

On every one of the three seeds, accuracy on the model's **most-confident third
of test predictions is at least 0.20 higher** than on its least-confident third
(`accuracy_most_confident_third` − `accuracy_least_confident_third` in
`results.json`).

**Why this target:** The useful version of this classifier flags its unsure
posts for a person to read. That only works if "unsure" actually means more
mistakes. With ~30 test posts each third is ~10 posts, so the score moves in
steps of 0.10 — a 0.10 gap is a single post and could be noise. 0.20 is two
more right answers out of ten in the confident group, the smallest gap I'd act
on.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
