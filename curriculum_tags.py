"""Detect curriculum categories from dataset examples."""

from __future__ import annotations

import re

RULES: list[tuple[str, re.Pattern[str]]] = [
    ("tanstack-query", re.compile(r"@tanstack/react-query|useQuery|useMutation|QueryClient", re.I)),
    ("zustand", re.compile(r"\bzustand\b|from\s+['\"]zustand", re.I)),
    ("redux", re.compile(r"@reduxjs/toolkit|createSlice|configureStore|RTK", re.I)),
    ("xstate", re.compile(r"\bxstate\b|useMachine|createMachine|setup\s*\(", re.I)),
    ("graphql", re.compile(r"\bgraphql\b|urql|apollo|gql`|useQuery.*Document", re.I)),
    ("react-hook-form", re.compile(r"react-hook-form|useForm|zodResolver", re.I)),
    ("zod", re.compile(r"\bzod\b|z\.object", re.I)),
    ("gsap", re.compile(r"\bgsap\b|useGSAP|ScrollTrigger", re.I)),
    ("framer-motion", re.compile(r"framer-motion|motion\.|AnimatePresence", re.I)),
    ("testing-library", re.compile(r"@testing-library/react|renderHook|userEvent", re.I)),
    ("vitest", re.compile(r"\bvitest\b|describe\(|it\(|expect\(", re.I)),
    ("msw", re.compile(r"\bmsw\b|http\.get|setupServer", re.I)),
    ("storybook", re.compile(r"\bstorybook\b|Meta<|StoryObj|@storybook", re.I)),
    ("react-router", re.compile(r"react-router|useNavigate|createBrowserRouter|RouterProvider", re.I)),
    ("shadcn", re.compile(r"\bcn\s*\(|class-variance-authority|cva\(|@radix-ui", re.I)),
    ("useActionState", re.compile(r"useActionState", re.I)),
    ("useFormStatus", re.compile(r"useFormStatus", re.I)),
    ("use-optimistic", re.compile(r"useOptimistic", re.I)),
    ("use-server", re.compile(r"['\"]use server['\"]", re.I)),
    ("css-modules", re.compile(r"\.module\.css", re.I)),
    ("scss", re.compile(r"\.module\.scss|\.scss['\"]|@use\s+|@mixin\s+|@include\s+", re.I)),
    ("tailwind", re.compile(r"className=.*\b(flex|grid|rounded|bg-|text-|p-|gap-|sm:|md:|dark:)", re.I)),
    ("when-to-use", re.compile(r"when\s+to\s+use|vs\.?\s|which\s+(should|to)|prefer\s+\w+\s+over", re.I)),
    ("compound-pattern", re.compile(r"compound|\.Header|\.Body|\.Footer|subcomponent", re.I)),
    ("use-reducer", re.compile(r"useReducer", re.I)),
]


def detect_categories(user: str, code: str) -> set[str]:
    blob = f"{user}\n{code}"
    tags: set[str] = set()
    for name, pattern in RULES:
        if pattern.search(blob):
            tags.add(name)
    return tags


def coverage_counts(items: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        user = item["conversations"][1]["content"]
        code = item["conversations"][2]["content"]
        for tag in detect_categories(user, code):
            counts[tag] = counts.get(tag, 0) + 1
    return counts
