#!/usr/bin/env python3
"""
React Dataset Augmentation (train split only).

Loads train_seeds.jsonl (from split_dataset.py), applies prompt paraphrases (~3×),
and writes train.jsonl. Eval seeds are never paraphrased.

Run after split_dataset.py:
    python augment_dataset.py
"""

import json
import re
import shutil
from pathlib import Path

from dataset_common import ex

TRAIN_SEEDS_FILE = Path("train_seeds.jsonl")
TRAIN_FILE = Path("train.jsonl")
LEGACY_FULL_FILE = Path("react_golden_dataset_full.jsonl")


def _swap(p: str, old: str, new: str) -> str:
    return re.sub(rf"\b{old}\b", new, p, count=1, flags=re.I) if re.search(rf"\b{old}\b", p, re.I) else p


def paraphrase(prompt: str) -> list[str]:
    s = prompt
    base = s[0].lower() + s[1:].rstrip(".?!")
    variants: list[str] = [
        s,
        _swap(s, "Create", "Build"),
        f"How do I {base}?",
        f"Using React 19 and TypeScript, {base}.",
    ]
    seen: set[str] = set()
    out: list[str] = []
    for v in variants:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def augment(examples: list[dict]) -> list[dict]:
    """Expand each example with prompt paraphrases; code answer stays identical."""
    out: list[dict] = []
    seen: set[str] = set()

    for item in examples:
        conv = item["conversations"]
        user_msg = conv[1]["content"]
        assistant_msg = conv[2]["content"]

        for variant_prompt in paraphrase(user_msg):
            key = variant_prompt + assistant_msg[:100]
            if key in seen:
                continue
            seen.add(key)
            out.append(ex(variant_prompt, assistant_msg))

    return out


def main() -> None:
    if not TRAIN_SEEDS_FILE.exists():
        print(f"ERROR: {TRAIN_SEEDS_FILE} not found. Run: python split_dataset.py")
        return

    seeds: list[dict] = []
    with TRAIN_SEEDS_FILE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                seeds.append(json.loads(line))

    print(f"Loaded {len(seeds)} train seeds (eval split excluded).")

    augmented = augment(seeds)
    multiplier = len(augmented) // max(len(seeds), 1)
    print(f"After augmentation (~×{multiplier}): {len(augmented)} training examples")

    with TRAIN_FILE.open("w", encoding="utf-8") as f:
        for item in augmented:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    shutil.copyfile(TRAIN_FILE, LEGACY_FULL_FILE)

    print(f"\nWrote {len(augmented)} examples → {TRAIN_FILE}")
    print(f"Copied to {LEGACY_FULL_FILE}")


if __name__ == "__main__":
    main()
