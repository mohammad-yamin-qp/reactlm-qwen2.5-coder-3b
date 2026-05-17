#!/usr/bin/env python3
"""
Validate react golden dataset JSONL before augmentation or training.

Usage:
    python validate_dataset.py                         # react_golden_dataset.jsonl
    python validate_dataset.py train_seeds.jsonl --strict-seeds
    python validate_dataset.py all_seeds.jsonl --strict-seeds --strict-ui
    python validate_dataset.py all_seeds.jsonl --report-coverage
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from curriculum_tags import coverage_counts
from dataset_common import SYSTEM_PROMPT
from dataset_ui import is_styling_exception, is_ui_example

TAILWIND_USER = re.compile(r"\btailwind\b", re.I)
SCSS_USER = re.compile(r"\bscss\b|\bsass\b|\.module\.scss\b|\bscss\s+modules?\b", re.I)
MODULES_USER = re.compile(
    r"\bcss\s+modules?\b|\bmodular\s+css\b|(?<!\.module\.)scoped\s+css\b", re.I
)
SCSS_CODE = re.compile(
    r"import\s+\w+\s+from\s+['\"][^'\"]+\.module\.scss['\"]|/\*[^*]*\.module\.scss"
)
TAILWIND_CODE = re.compile(
    r"(className=|cva\(|className:\s*[\"']).*\b(inline-flex|flex|grid|rounded|bg-|text-|p-|px-|py-|gap-|sm:|md:|lg:|dark:)"
)
MODULES_CODE = re.compile(r"import\s+\w+\s+from\s+['\"][^'\"]+\.module\.css['\"]")
MODULES_USAGE = re.compile(r"styles\.\w+")
INLINE_STYLE = re.compile(r"style=\{\{")
CLASS_COMPONENT = re.compile(r"class\s+\w+\s+extends\s+(React\.)?Component")
LEGACY_LIFECYCLE = re.compile(
    r"componentDidMount|componentWillUnmount|getDerivedStateFromProps"
)
ANY_TYPE = re.compile(r":\s*any\b|as\s+any\b")
USE_CLIENT = re.compile(r"['\"]use client['\"]")
STRONG_CLIENT_HOOKS = re.compile(
    r"\b(useState|useEffect|useReducer|useActionState|useOptimistic|useTransition|useFormStatus)\b"
)
NEXT_PATTERN = re.compile(r"(from\s+['\"]next/|['\"]next/|import\s+[^;\n]*\bnext/)", re.I)
BROKEN_IMAGE = re.compile(r"<Image\b")
IMAGE_IMPORT = re.compile(r"import\s+.*\bImage\b.*from")

LIBRARY_RULES: list[tuple[re.Pattern[str], re.Pattern[str]]] = [
    (re.compile(r"\busing\s+Zustand\b|\bZustand\s+store\b", re.I), re.compile(r"from\s+['\"]zustand['\"]|from\s+['\"]zustand/")),
    (re.compile(r"\bTanStack\s+Query\b", re.I), re.compile(r"@tanstack/react-query")),
    (re.compile(r"\bReact\s+Hook\s+Form\b", re.I), re.compile(r"react-hook-form")),
    (re.compile(r"\bXState\b", re.I), re.compile(r"\bxstate\b|@xstate/react")),
    (re.compile(r"\burql\b", re.I), re.compile(r"from\s+['\"]urql['\"]")),
    (re.compile(r"\bApollo\s+Client\b", re.I), re.compile(r"@apollo/client")),
    (re.compile(r"\bRedux\s+Toolkit\b", re.I), re.compile(r"@reduxjs/toolkit")),
    (re.compile(r"\bGSAP\b", re.I), re.compile(r"\bgsap\b|@gsap/react")),
    (re.compile(r"\bFramer\s+Motion\b", re.I), re.compile(r"framer-motion")),
    (re.compile(r"\bStorybook\b", re.I), re.compile(r"@storybook|storybook")),
    (re.compile(r"\bReact\s+Router\b", re.I), re.compile(r"react-router")),
    (re.compile(r"\bshadcn\b", re.I), re.compile(r"class-variance-authority|@radix-ui|cn\s*\(")),
]


def _user_prompt(item: dict) -> str:
    return item["conversations"][1]["content"]


def _assistant_code(item: dict) -> str:
    return item["conversations"][2]["content"]


def _wants_tailwind(user: str) -> bool:
    return bool(TAILWIND_USER.search(user))


def _wants_scss(user: str) -> bool:
    return bool(SCSS_USER.search(user))


def _wants_modules(user: str) -> bool:
    if _wants_scss(user):
        return False
    return bool(MODULES_USER.search(user))


def _is_comparison_example(user: str) -> bool:
    lower = user.lower()
    return "vs css modules" in lower or "vs scss" in lower or "tailwind vs" in lower


def _has_tailwind_utilities(code: str) -> bool:
    if re.search(r"cva\s*\(|['\"]inline-flex|['\"]rounded-md|['\"]bg-|['\"]text-", code):
        return True
    for m in re.finditer(r'className=(?:\{`([^`]+)`\}|"([^"]+)"|\{([^}]+)\})', code):
        chunk = next(g for g in m.groups() if g)
        if "styles." in chunk:
            continue
        if re.search(r"\b(sm:|md:|lg:|bg-|text-|flex|grid|rounded|inline-flex|gap-|px-|py-)", chunk):
            return True
    return False


def _allows_next_mention(user: str, code: str) -> bool:
    blob = (user + code).lower()
    return "do not use next" in blob or "don't use next" in blob or "without next" in blob


def validate_item(
    item: dict,
    index: int,
    *,
    strict_ui: bool = False,
) -> list[str]:
    errors: list[str] = []
    conv = item.get("conversations")
    if not isinstance(conv, list) or len(conv) != 3:
        return [f"line {index}: expected 3 conversations"]
    roles = [c.get("role") for c in conv]
    if roles != ["system", "user", "assistant"]:
        errors.append(f"line {index}: roles must be system, user, assistant (got {roles})")
    if conv[0].get("content") != SYSTEM_PROMPT:
        errors.append(f"line {index}: system prompt does not match dataset_common.SYSTEM_PROMPT")
    user = conv[1].get("content", "")
    code = conv[2].get("content", "")
    if not user.strip():
        errors.append(f"line {index}: empty user prompt")
    if not code.strip():
        errors.append(f"line {index}: empty assistant content")

    if NEXT_PATTERN.search(user) or NEXT_PATTERN.search(code):
        if not _allows_next_mention(user, code):
            errors.append(f"line {index}: contains next/ API reference")

    if BROKEN_IMAGE.search(code) and not IMAGE_IMPORT.search(code):
        errors.append(f"line {index}: uses <Image> without Image import (Next.js leftover)")

    code_active = re.sub(r"//.*?$", "", code, flags=re.M)
    code_active = re.sub(r"/\*.*?\*/", "", code_active, flags=re.S)
    if CLASS_COMPONENT.search(code_active) and "ErrorBoundary" not in code_active:
        errors.append(f"line {index}: class component in assistant (forbidden)")
    if LEGACY_LIFECYCLE.search(code) and "BEFORE" not in code and "// class" not in code.lower():
        errors.append(f"line {index}: legacy lifecycle in assistant")
    if ANY_TYPE.search(code):
        errors.append(f"line {index}: uses 'any' type")

    has_tailwind = _has_tailwind_utilities(code)
    has_modules = bool(MODULES_CODE.search(code) and MODULES_USAGE.search(code))
    has_scss = bool(SCSS_CODE.search(code) and MODULES_USAGE.search(code))

    if (
        _wants_tailwind(user)
        and not _is_comparison_example(user)
        and not re.search(r"when\s+(to|should)\s+i\s+use", user, re.I)
    ):
        has_tw = has_tailwind or bool(
            re.search(r"cva\s*\(|['\"]inline-flex|['\"]rounded-md|['\"]bg-", code)
        )
        if not has_tw:
            errors.append(f"line {index}: user asks for Tailwind but assistant lacks Tailwind classes")
        if has_modules and "CSS Modules version" not in code:
            errors.append(f"line {index}: mixes CSS Modules with Tailwind-only prompt")

    if _wants_modules(user) and not _is_comparison_example(user):
        if not has_modules:
            errors.append(f"line {index}: user asks for CSS Modules but assistant lacks .module.css import")
        if has_tailwind and "Tailwind version" not in code:
            errors.append(f"line {index}: mixes Tailwind with CSS Modules-only prompt")

    if _wants_scss(user) and not _is_comparison_example(user):
        if not has_scss:
            errors.append(f"line {index}: user asks for SCSS but assistant lacks .module.scss import and styles")
        if ".module.css" in code and ".module.scss" not in code:
            errors.append(f"line {index}: user asks for SCSS but assistant uses .module.css instead")
        if has_tailwind and not has_scss and "Tailwind version" not in code:
            errors.append(f"line {index}: mixes Tailwind with SCSS-only prompt")

    if strict_ui and is_ui_example(user) and not is_styling_exception(user, code):
        if not _wants_modules(user) and not _wants_scss(user) and not has_tailwind and not has_modules:
            errors.append(f"line {index}: UI example should use Tailwind utilities by default")

    is_guidance_only = code.strip().startswith("//") or "architectureNotes" in code or "guidance =" in code
    if not is_guidance_only and not re.search(
        r"when\s+(to|should)\s+i\s+use|when\s+should\s+you\s+use|architect a production",
        user,
        re.I,
    ):
        for user_pat, code_pat in LIBRARY_RULES:
            if user_pat.search(user) and not code_pat.search(code):
                errors.append(f"line {index}: prompt references library but assistant code missing import")

    if (
        not is_guidance_only
        and STRONG_CLIENT_HOOKS.search(code_active)
        and not USE_CLIENT.search(code)
    ):
        teaching = re.search(
            r"server component|without.*['\"]use client['\"]|fix.*use client|refactor.*server|when\s+should\s+i\s+use",
            user,
            re.I,
        )
        if not teaching and "BEFORE" not in code:
            errors.append(f"line {index}: client hooks but missing 'use client'")

    return errors


def _assistant_hash(code: str) -> str:
    normalized = "\n".join(line.rstrip() for line in code.splitlines())
    return hashlib.sha256(normalized.encode()).hexdigest()


def validate_file(
    path: Path,
    *,
    strict_seeds: bool = False,
    strict_ui: bool = False,
) -> tuple[int, list[str]]:
    all_errors: list[str] = []
    count = 0
    seen_hashes: dict[str, int] = {}
    with path.open(encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            count += 1
            try:
                item = json.loads(line)
            except json.JSONDecodeError as e:
                all_errors.append(f"line {i}: invalid JSON — {e}")
                continue
            all_errors.extend(validate_item(item, i, strict_ui=strict_ui))
            if strict_seeds:
                h = _assistant_hash(_assistant_code(item))
                if h in seen_hashes:
                    all_errors.append(
                        f"line {i}: duplicate assistant body (same as line {seen_hashes[h]})"
                    )
                else:
                    seen_hashes[h] = i
    return count, all_errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="react_golden_dataset.jsonl")
    parser.add_argument("--strict-seeds", action="store_true")
    parser.add_argument("--strict-ui", action="store_true")
    parser.add_argument("--report-coverage", action="store_true")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"ERROR: {path} not found")
        sys.exit(1)

    if args.report_coverage:
        items = []
        with path.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    items.append(json.loads(line))
        counts = coverage_counts(items)
        print(f"Coverage report ({len(items)} examples):\n")
        for tag, n in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"  {tag}: {n}")
        return

    count, errors = validate_file(path, strict_seeds=args.strict_seeds, strict_ui=args.strict_ui)
    if errors:
        print(f"FAILED — {len(errors)} issue(s) in {count} examples ({path}):\n")
        for err in errors[:50]:
            print(f"  • {err}")
        if len(errors) > 50:
            print(f"  … and {len(errors) - 50} more")
        sys.exit(1)
    suffix = ""
    if args.strict_seeds:
        suffix += " (strict seeds)"
    if args.strict_ui:
        suffix += " (strict ui)"
    print(f"OK — {count} examples passed validation{suffix} ({path})")


if __name__ == "__main__":
    main()
