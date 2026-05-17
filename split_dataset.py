#!/usr/bin/env python3
"""
Merge all unique seeds, deduplicate, and split into train / eval before augmentation.

Reads:
  - react_golden_dataset.jsonl (from generate_dataset.py)
  - ALL_CURRICULUM_SEEDS from seeds package

Writes:
  - all_seeds.jsonl     (deduplicated unique seeds)
  - train_seeds.jsonl   (~90%, paraphrase allowed)
  - eval.jsonl          (~10%, never paraphrased)
"""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

from seeds import ALL_CURRICULUM_SEEDS

BASE_FILE = Path("react_golden_dataset.jsonl")
ALL_SEEDS_FILE = Path("all_seeds.jsonl")
TRAIN_SEEDS_FILE = Path("train_seeds.jsonl")
EVAL_FILE = Path("eval.jsonl")

EVAL_RATIO = 0.10
RANDOM_SEED = 42


def _assistant_hash(item: dict) -> str:
    code = item["conversations"][2]["content"]
    normalized = "\n".join(line.rstrip() for line in code.splitlines())
    return hashlib.sha256(normalized.encode()).hexdigest()


def _load_jsonl(path: Path) -> list[dict]:
    items: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def _write_jsonl(path: Path, items: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def dedupe_seeds(items: list[dict]) -> tuple[list[dict], int]:
    seen: set[str] = set()
    unique: list[dict] = []
    dropped = 0
    for item in items:
        h = _assistant_hash(item)
        if h in seen:
            dropped += 1
            continue
        seen.add(h)
        unique.append(item)
    return unique, dropped


def main() -> None:
    if not BASE_FILE.exists():
        print(f"ERROR: {BASE_FILE} not found. Run: python generate_dataset.py")
        return

    base = _load_jsonl(BASE_FILE)
    combined = base + ALL_CURRICULUM_SEEDS
    print(
        f"Loaded seeds: {len(base)} base + {len(ALL_CURRICULUM_SEEDS)} curriculum "
        f"= {len(combined)}"
    )

    unique, dropped = dedupe_seeds(combined)
    if dropped:
        print(f"Deduplicated: removed {dropped} duplicate assistant bodies")

    rng = random.Random(RANDOM_SEED)
    shuffled = unique.copy()
    rng.shuffle(shuffled)

    eval_count = max(1, round(len(shuffled) * EVAL_RATIO))
    eval_items = shuffled[:eval_count]
    train_items = shuffled[eval_count:]

    _write_jsonl(ALL_SEEDS_FILE, unique)
    _write_jsonl(TRAIN_SEEDS_FILE, train_items)
    _write_jsonl(EVAL_FILE, eval_items)

    print(f"\nWrote {len(unique)} unique seeds → {ALL_SEEDS_FILE}")
    print(f"  train_seeds: {len(train_items)} ({100 - int(EVAL_RATIO * 100)}%)")
    print(f"  eval:        {len(eval_items)} ({int(EVAL_RATIO * 100)}%)")


if __name__ == "__main__":
    main()
