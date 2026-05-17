"""UI example detection for dataset validation."""

from __future__ import annotations

import re

UI_KEYWORDS = re.compile(
    r"\b("
    r"button|form|modal|dialog|card|layout|dashboard|table|nav|menu|sidebar|"
    r"header|footer|login|signup|list|input|select|checkbox|toast|alert|banner|"
    r"hero|pricing|cart|checkout|avatar|badge|tab|dropdown|tooltip|skeleton|"
    r"spinner|pagination|search\s*bar|page|grid|panel|drawer|popover|"
    r"component|ui|stylesheet|tailwind|css\s*modules?"
    r")\b",
    re.I,
)

NON_UI_KEYWORDS = re.compile(
    r"\b("
    r"custom\s+hook|use[A-Z]\w+|hook\s+that|hook\s+to|"
    r"type\s+only|typescript\s+type|generic\s+type|interface\s+only|"
    r"refactor\s+this|fix\s+this|anti-?pattern|without\s+['\"]use client['\"]|"
    r"server\s+action\s+only|when\s+to\s+use|vs\s+|comparison|"
    r"test\s+for|vitest|storybook\s+config|eslint|vite\s+config"
    r")\b",
    re.I,
)

COMPARISON = re.compile(r"\bvs\.?\b|when\s+to\s+use|which\s+(should|to)\b", re.I)


def is_ui_example(user: str) -> bool:
    if NON_UI_KEYWORDS.search(user) and not UI_KEYWORDS.search(user):
        return False
    return bool(UI_KEYWORDS.search(user))


def is_styling_exception(user: str, code: str) -> bool:
    if COMPARISON.search(user):
        return True
    if NON_UI_KEYWORDS.search(user):
        return True
    if re.search(r"fix\s+this|refactor|BEFORE|anti-?pattern", user, re.I):
        return True
    if "hook" in user.lower() and "component" not in user.lower():
        return True
    # Legacy seeds that use inline layout styles (pre-Tailwind retrofit backlog)
    if re.search(r"style=\{\{", code) and not re.search(
        r"className=.*\b(flex|grid|rounded|bg-|text-|p-|gap-)", code
    ):
        return True
    # Unstyled legacy markup (no className, no inline styles) — excluded from Tailwind ratio
    if is_ui_example(user) and "className=" not in code and "style={{" not in code:
        return True
    # Single dynamic inline for progress etc.
    if code.count("style={{") == 1 and re.search(r"width|height|transform|progress", code):
        return True
    return False
