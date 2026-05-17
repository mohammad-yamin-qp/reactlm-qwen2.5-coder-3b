#!/usr/bin/env python3
"""Run the full quality-first dataset pipeline."""

from __future__ import annotations

import subprocess
import sys


def run(cmd: list[str]) -> None:
    print(f"\n→ {' '.join(cmd)}\n")
    subprocess.run(cmd, check=True)


def main() -> None:
    steps = [
        ["python", "generate_dataset.py"],
        ["python", "scripts/generate_curriculum.py"],
        ["python", "split_dataset.py"],
        ["python", "validate_dataset.py", "all_seeds.jsonl", "--strict-seeds"],
        ["python", "validate_dataset.py", "train_seeds.jsonl", "--strict-seeds"],
        ["python", "validate_dataset.py", "eval.jsonl", "--strict-seeds"],
        ["python", "augment_dataset.py"],
        ["python", "validate_dataset.py", "train.jsonl"],
        ["python", "validate_dataset.py", "eval.jsonl"],
        ["python", "check_step2_ready.py"],
    ]
    for cmd in steps:
        try:
            run(cmd)
        except subprocess.CalledProcessError:
            print(f"\nPipeline failed at: {' '.join(cmd)}", file=sys.stderr)
            sys.exit(1)
    print("\n✓ Dataset pipeline complete.")
    print("  train.jsonl              — use for fine-tuning")
    print("  eval.jsonl               — held-out eval (never paraphrased)")
    print("  react_golden_dataset_full.jsonl — alias of train.jsonl")
    print("\nRun: python check_step2_ready.py")


if __name__ == "__main__":
    main()
