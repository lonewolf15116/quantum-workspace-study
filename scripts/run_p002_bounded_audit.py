#!/usr/bin/env python3
"""Execute the two bounded P002 failure-mode diagnostics in sequence.

This is a local foreground runner, not a new experiment or a checkpoint
selector. Existing outputs are never overwritten. Final-step training MAE
is the entangled-overfit primary endpoint.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_checked(cmd):
    print("RUN", " ".join(map(str, cmd)), flush=True)
    subprocess.run([str(x) for x in cmd], check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="p002_dataset")
    parser.add_argument("--prefix", default="p002_bounded_audit_s202")
    parser.add_argument("--device", choices=["cuda", "cpu"], default="cuda")
    parser.add_argument("--seed", type=int, default=202)
    parser.add_argument("--steps", type=int, default=1500)
    parser.add_argument("--layers", type=int, choices=[12, 24, 40], default=12)
    args = parser.parse_args()
    if args.steps < 1:
        parser.error("--steps must be positive")
    base = Path(args.prefix)
    entangled = Path(str(base) + "_entangled")
    labels = Path(str(base) + "_labels.json")
    summary = Path(str(base) + "_summary.json")
    for path in (entangled, labels, summary):
        if path.exists():
            raise SystemExit(f"Refusing to overwrite existing audit evidence: {path}")
    root = Path(__file__).resolve().parent
    run_checked([
        sys.executable, root / "check_p002_entangled_overfit.py",
        "--device", args.device, "--data", args.data,
        "--out", entangled, "--seed", args.seed,
        "--layers", args.layers, "--steps", args.steps,
    ])
    run_checked([
        sys.executable, root / "audit_p002_labels.py",
        "--data", args.data, "--out", labels,
    ])
    checkpoints = [
        json.loads(s) for s in (entangled / "checkpoints.jsonl").read_text().splitlines()
    ]
    assert checkpoints[-1]["step"] == args.steps
    last = checkpoints[-1]
    all_labels = json.loads(labels.read_text())
    for panel in ("training", "within", "heldout"):
        assert all_labels[panel]["all"]["labels"] > 0
    final = {
        "protocol": "P002-BOUNDED-AUDIT-001",
        "status": "completed",
        "source_outputs": {"entangled": str(entangled), "labels": str(labels)},
        "primary_step": args.steps,
        "train_mae": last["train"]["mae"],
        "train_zero_mae": last["train"]["zero_mae"],
        "within_mae": last["within"]["mae"],
        "within_zero_mae": last["within"]["zero_mae"],
        "train_by_observable": last["train_by_observable"],
        "within_by_observable": last["within_by_observable"],
        "label_distribution": {
            panel: all_labels[panel]["all"]
            for panel in ("training", "within", "heldout")
        },
        "interpretation": (
            "Exploratory only. Near-zero training error on a tiny fixed entangled "
            "subset shows local fitting, not held-out-template generalisation. "
            "Training loss is MSE; MAE and literal-zero are diagnostics and "
            "must not be confused with an optimised constant MSE predictor."
        ),
    }
    summary.write_text(json.dumps(final, indent=2, sort_keys=True) + "\n")
    print("\nAUDIT SUMMARY\n" + json.dumps(final, indent=2), flush=True)
    print("Saved:", summary)


if __name__ == "__main__":
    main()
