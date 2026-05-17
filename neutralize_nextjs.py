#!/usr/bin/env python3
"""Remove Next.js-specific prompts and imports from dataset source files."""

from pathlib import Path

_ROOT = Path(__file__).parent
FILES: list[Path] = [
    _ROOT / "generate_dataset.py",
    _ROOT / "augment_dataset.py",
    _ROOT / "quality_examples.py",
]
FILES.extend(sorted(_ROOT.glob("seeds/**/*.py")))

# Most specific first
PROMPT_REPLACEMENTS = [
    ("Next.js Server Component", "React Server Component"),
    ("Next.js Server Action", "React Server Action"),
    ("Next.js App Router", "React Server Components architecture"),
    ("Next.js Route Handler (Server-side)", "server route handler"),
    ("Next.js dashboard Server Component", "dashboard Server Component"),
    ("Next.js product page", "product page"),
    ("Next.js layout Server Component", "layout Server Component"),
    ("Next.js middleware file that protects authenticated routes", "auth gate pattern that protects authenticated routes"),
    ("Next.js error.tsx page", "error page component (error.tsx convention)"),
    ("not-found.tsx page for Next.js App Router", "not-found page component"),
    ("Next.js page component", "page component"),
    ("on a Next.js page", "on a page using Server Components"),
    ("in a Next.js app", "in a React app"),
    ("for Next.js", "for React"),
    ("using next/image", "with native img and lazy loading"),
    ("next/image", "native img"),
    ("Next.js ", ""),
]

IMPORT_LINES = [
    "import { revalidatePath } from 'next/cache';\n",
    "import { revalidateTag } from 'next/cache';\n",
    "import { redirect } from 'next/navigation';\n",
    "import { cookies } from 'next/headers';\n",
    "import { headers } from 'next/headers';\n",
    "import Link from 'next/link';\n",
    "import Image from 'next/image';\n",
    "import { usePathname } from 'next/navigation';\n",
    "import { notFound } from 'next/navigation';\n",
    "import type { Metadata } from 'next';\n",
    "import { NextResponse, type NextRequest } from 'next/server';\n",
    "import { NextResponse } from 'next/server';\n",
]

CALL_REPLACEMENTS = [
    ("revalidatePath(", "// revalidatePath("),
    ("revalidateTag(", "// revalidateTag("),
    ("redirect(", "// redirect("),
    ("notFound()", "throw new Error('Not found')"),
    ("Promise<NextResponse>", "Promise<Response>"),
    ("NextResponse.redirect", "// redirect"),
    ("NextResponse.next", "Response"),
    ("new NextResponse(", "new Response("),
    ("export function middleware(request: NextRequest): NextResponse", "export function authMiddleware(request: Request): Response"),
    ("export function middleware(request: NextRequest)", "export function authMiddleware(request: Request)"),
    ("<Link ", "<a "),
    ("</Link>", "</a>"),
    ("<Image ", "<img "),
    ("const pathname = usePathname()", "const pathname = typeof window !== 'undefined' ? window.location.pathname : '/'"),
]

PATH_COMMENTS = [
    ("// app/", "// "),
]

import re

FETCH_NEXT_RE = re.compile(r",\s*\{\s*next:\s*\{[^}]+\}\s*\}")


def neutralize(text: str) -> str:
    for old, new in PROMPT_REPLACEMENTS:
        text = text.replace(old, new)
    for line in IMPORT_LINES:
        text = text.replace(line, "")
    for old, new in CALL_REPLACEMENTS:
        text = text.replace(old, new)
    for old, new in PATH_COMMENTS:
        text = text.replace(old, new)
    text = FETCH_NEXT_RE.sub("", text)
    text = text.replace("@/app/actions/", "@/actions/")
    text = text.replace("<Link", "<a")
    text = text.replace(": Promise<Metadata>", ": Promise<{ title: string; description?: string }>")
    return text


def main() -> None:
    for path in FILES:
        original = path.read_text(encoding="utf-8")
        updated = neutralize(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"Updated {path}")
        else:
            print(f"No changes in {path}")


if __name__ == "__main__":
    main()
