#!/usr/bin/env python3
"""
Per-post predictions for the three-seed run. ← unit 6, Milestone 4

The notebook's section 6 keeps only the summary numbers for each seed. To
diagnose a miss you need the posts themselves: which real `hot_take` posts were
called `reaction`, how sure the model was, and what kind of thread they came
from. This re-runs exactly what section 6 does — the same split function, the
same settings, the same seeds — and writes one row per held-out post.

CPU training is deterministic here (seed 42 reproduces unit 5's results.json
to the last digit), so these predictions are the ones behind the numbers in
results_three_seeds_<label>.json. The script checks that and says so.

    python error_analysis.py                     # unit 5 settings → errors_before.csv
    python error_analysis.py --epochs 10 --label after

It doesn't change anything in the system. It only reads labels.csv.
"""

import argparse
import json
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError, ValueError):
        pass

LABELS = ["analysis", "hot_take", "reaction"]
SEEDS = [42, 7, 2024]
BASE_MODEL = "distilbert-base-uncased"


def split_dataset(df, seed, test_size=0.15, val_size=0.15):
    """Identical to the notebook's section 3."""
    from sklearn.model_selection import train_test_split

    def _stratify_on(frame):
        counts = frame["label"].value_counts()
        return frame["label"] if counts.min() >= 2 else None

    rest, test = train_test_split(
        df, test_size=test_size, random_state=seed, stratify=_stratify_on(df)
    )
    val_share = val_size / (1 - test_size)
    train, val = train_test_split(
        rest, test_size=val_share, random_state=seed, stratify=_stratify_on(rest)
    )
    return train, val, test


def train_and_predict(train, val, test, seed, epochs, lr, batch, max_length):
    """The notebook's section 4 training, then per-post predictions on test."""
    import numpy as np
    from datasets import Dataset
    from transformers import (
        AutoTokenizer, AutoModelForSequenceClassification,
        TrainingArguments, Trainer, set_seed,
    )

    set_seed(seed)
    lookup = {label: i for i, label in enumerate(LABELS)}
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL, num_labels=len(LABELS),
        id2label=dict(enumerate(LABELS)), label2id=lookup,
    )

    def to_ds(frame):
        out = frame[["text"]].copy()
        out["labels"] = frame["label"].map(lookup)
        ds = Dataset.from_pandas(out.reset_index(drop=True))
        return ds.map(lambda b: tokenizer(b["text"], truncation=True,
                                          padding="max_length", max_length=max_length),
                      batched=True)

    args = TrainingArguments(
        output_dir="./takemeter_out", num_train_epochs=epochs, learning_rate=lr,
        per_device_train_batch_size=batch, per_device_eval_batch_size=batch,
        eval_strategy="epoch", save_strategy="no", logging_steps=10, seed=seed,
        report_to="none", disable_tqdm=True,
    )
    trainer = Trainer(model=model, args=args, train_dataset=to_ds(train),
                      eval_dataset=to_ds(val))
    trainer.train()

    logits = trainer.predict(to_ds(test)).predictions
    exp = np.exp(logits - logits.max(axis=-1, keepdims=True))
    probs = exp / exp.sum(axis=-1, keepdims=True)
    log = [e for e in trainer.state.log_history if "loss" in e or "eval_loss" in e]
    return probs, log


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--lr", type=float, default=2e-5)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--label", default="before")
    args = parser.parse_args()

    import pandas as pd

    df = pd.read_csv("labels.csv")
    sources = pd.read_csv("data/sources.csv")      # same row order as labels.csv
    df["kind"] = sources["kind"].values
    df["thread"] = sources["thread"].values

    rows, curves = [], {}
    for seed in SEEDS:
        train, val, test = split_dataset(df, seed)
        probs, log = train_and_predict(train, val, test, seed, args.epochs, args.lr,
                                       args.batch, args.max_length)
        curves[seed] = log
        correct = 0
        for (_, post), p in zip(test.iterrows(), probs):
            guess = LABELS[int(p.argmax())]
            correct += guess == post["label"]
            rows.append({
                "seed": seed, "gold": post["label"], "predicted": guess,
                "confidence": round(float(p.max()), 3),
                **{f"p_{label}": round(float(p[i]), 3) for i, label in enumerate(LABELS)},
                "kind": post["kind"], "words": len(str(post["text"]).split()),
                "text": post["text"], "note": post.get("note", ""),
            })
        print(f"seed {seed}: accuracy {correct / len(test):.3f}")

    out = Path(f"errors_{args.label}.csv")
    pd.DataFrame(rows).to_csv(out, index=False)
    Path(f"errors_{args.label}_curves.json").write_text(json.dumps(
        {"settings": vars(args), "curves": curves}, indent=2), encoding="utf-8")

    reference = Path(f"results_three_seeds_{args.label}.json")
    if reference.exists():
        expected = {r["seed"]: r["accuracy"] for r in json.loads(reference.read_text())}
        got = pd.DataFrame(rows).assign(ok=lambda d: d.gold == d.predicted) \
                                .groupby("seed")["ok"].mean().to_dict()
        same = all(abs(expected[s] - got[s]) < 1e-9 for s in SEEDS)
        print(f"\nMatches {reference}: {'yes' if same else 'NO — numbers differ'}")
    print(f"Wrote {out} and {out.stem}_curves.json")


if __name__ == "__main__":
    main()
