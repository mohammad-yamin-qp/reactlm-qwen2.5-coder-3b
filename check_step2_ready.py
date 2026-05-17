#!/usr/bin/env python3
"""Verify Step 2 dataset meets senior React expert curriculum gates."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from curriculum_tags import coverage_counts
from dataset_ui import is_styling_exception, is_ui_example

ROOT = Path(__file__).parent

MINIMUMS: dict[str, int] = {
    "tanstack-query": 60,
    "zustand": 25,
    "redux": 25,
    "xstate": 25,
    "react-hook-form": 25,
    "zod": 25,
    "gsap": 20,
    "framer-motion": 10,
    "testing-library": 20,
    "vitest": 20,
    "storybook": 25,
    "react-router": 20,
    "shadcn": 15,
    "when-to-use": 30,
    "useActionState": 20,
    "css-modules": 5,
    "scss": 12,
    "compound-pattern": 5,
}

TAILWIND_CODE = re.compile(
    r"className=.*\b(inline-flex|flex|grid|rounded|bg-|text-|p-|px-|py-|gap-|sm:|md:|lg:|dark:)"
)


def load_jsonl(path: Path) -> list[dict]:
    items: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))
    return items


def count_lines(path: Path) -> int:
    return sum(1 for _ in path.open() if _.strip())


def ui_tailwind_ratio(items: list[dict]) -> float:
    ui_total = 0
    ui_tailwind = 0
    for item in items:
        user = item["conversations"][1]["content"]
        code = item["conversations"][2]["content"]
        if not is_ui_example(user) or is_styling_exception(user, code):
            continue
        ui_total += 1
        if TAILWIND_CODE.search(code) or (
            "className=" in code
            and re.search(r"\b(flex|grid|rounded|bg-|text-|p-|px-|py-|gap-|sm:|md:)", code)
        ):
            ui_tailwind += 1
    return ui_tailwind / ui_total if ui_total else 1.0


def main() -> None:
    failures: list[str] = []

    all_seeds = ROOT / "all_seeds.jsonl"
    train = ROOT / "train.jsonl"
    eval_f = ROOT / "eval.jsonl"

    for p in (all_seeds, train, eval_f):
        if not p.exists():
            failures.append(f"Missing {p.name} — run: python build_dataset.py")

    if failures:
        for f in failures:
            print(f"FAIL: {f}")
        sys.exit(1)

    n_all = count_lines(all_seeds)
    n_train = count_lines(train)
    n_eval = count_lines(eval_f)

    if n_all < 900:
        failures.append(f"all_seeds.jsonl has {n_all} seeds (need >= 900)")
    # allow 900+ after expansion
    if n_eval < 90:
        failures.append(f"eval.jsonl has {n_eval} seeds (need >= 90)")
    if n_train < 2400:
        failures.append(f"train.jsonl has {n_train} rows (need >= 2400)")

    items = load_jsonl(all_seeds)
    counts = coverage_counts(items)

    gql = sum(
        1
        for item in items
        if re.search(r"urql|@apollo/client|\bgraphql\b", item["conversations"][2]["content"], re.I)
    )
    if gql < 35:
        failures.append(f"graphql/urql/apollo coverage {gql} < 35")

    for tag, minimum in MINIMUMS.items():
        got = counts.get(tag, 0)
        if got < minimum:
            failures.append(f"curriculum '{tag}': {got} < {minimum}")

    next_hits = 0
    for item in items:
        user = item["conversations"][1]["content"]
        code = item["conversations"][2]["content"]
        if re.search(r"(from\s+['\"]next/|['\"]next/)", user + code, re.I):
            if "do not use next" not in (user + code).lower():
                next_hits += 1
    if next_hits:
        failures.append(f"found {next_hits} examples with next/ references")

    ratio = ui_tailwind_ratio(items)
    if ratio < 0.80:
        failures.append(f"UI Tailwind ratio {ratio:.1%} < 80%")

    for path, extra in [(all_seeds, ["--strict-seeds"]), (train, []), (eval_f, [])]:
        cmd = ["python", "validate_dataset.py", str(path), *extra]
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            failures.append(f"validate_dataset failed for {path.name}:\n{r.stdout}\n{r.stderr}")

    if failures:
        print("Step 2 NOT ready:\n")
        for f in failures:
            print(f"  • {f}")
        sys.exit(1)

    print("Step 2 READY — dataset passes all gates.")
    print(f"  all_seeds: {n_all}  train: {n_train}  eval: {n_eval}")
    print(f"  UI Tailwind ratio: {ratio:.1%}")
    print("  Top curriculum tags:")
    for tag, n in sorted(counts.items(), key=lambda x: -x[1])[:12]:
        print(f"    {tag}: {n}")
    print("\nYou can proceed to Step 3 (chat template + fine-tune).")


if __name__ == "__main__":
    main()
