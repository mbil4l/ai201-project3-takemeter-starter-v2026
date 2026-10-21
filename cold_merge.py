#!/usr/bin/env python3
"""
Fold the unaided round into labels.csv.

cold_round.csv holds 20 posts from labels.csv with the label column blank.
Label them from the README definitions alone — no tools, and without looking
at labels.csv first. Then:

    python cold_merge.py

For each of the 20 it replaces the label in labels.csv with yours, sets the
note to `cold`, and prints how often you agreed with the pre-label that was
there. Re-run the notebook from section 2 afterwards, since the data changed.
"""

import sys

import pandas as pd

LABELS = {"analysis", "hot_take", "reaction"}

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError, ValueError):
        pass


def main():
    cold = pd.read_csv("cold_round.csv", keep_default_na=False)
    cold["label"] = cold["label"].astype(str).str.strip()

    bad = cold[~cold["label"].isin(LABELS)]
    if len(bad):
        print(f"{len(bad)} rows in cold_round.csv have no label or one not in {sorted(LABELS)}.")
        print("Finish those first.")
        return 1

    df = pd.read_csv("labels.csv", keep_default_na=False)
    agreed, disagreements = 0, []

    for _, row in cold.iterrows():
        match = df.index[df["text"] == row["text"]]
        if len(match) != 1:
            print(f"[skip] no single match in labels.csv for: {row['text'][:60]!r}")
            continue
        i = match[0]
        if df.at[i, "note"] == "cold":
            print(f"[skip] already merged: {row['text'][:60]!r}")
            continue
        before = df.at[i, "label"]
        if before == row["label"]:
            agreed += 1
        else:
            disagreements.append((row["text"], before, row["label"]))
        df.at[i, "label"] = row["label"]
        df.at[i, "note"] = "cold"

    df.to_csv("labels.csv", index=False)

    total = agreed + len(disagreements)
    print(f"Merged {total} cold labels into labels.csv.")
    if total:
        print(f"You agreed with the pre-label on {agreed} of {total} ({agreed / total:.0%}).")
    for text, before, after in disagreements:
        print(f"\n  pre-label {before} → you said {after}")
        print(f"  {text[:200]!r}")
    print("\nRe-run the notebook from section 2 — the labels changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
