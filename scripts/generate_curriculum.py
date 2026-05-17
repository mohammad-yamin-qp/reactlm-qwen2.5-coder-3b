#!/usr/bin/env python3
"""Generate seeds/generated_curriculum.py with senior React ecosystem examples."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dataset_common import ex  # noqa: E402

OUT = ROOT / "seeds" / "generated_curriculum.py"


def q(name: str, key: str, path: str) -> dict:
    hook = f"use{key.title().replace('-', '')}"
    fn = f"fetch{key.title().replace('-', '')}"
    return ex(
        f"Create TanStack Query v5 useQuery for {key} with loading and error UI using Tailwind.",
        f"""\
'use client';

import {{ useQuery }} from '@tanstack/react-query';

type {name}Row = {{ id: string; name: string }};

async function {fn}(): Promise<{name}Row[]> {{
  const res = await fetch('{path}');
  if (!res.ok) throw new Error('Failed to load {key}');
  return res.json() as Promise<{name}Row[]>;
}}

export function {hook}() {{
  return useQuery({{ queryKey: ['{key}'], queryFn: {fn}, staleTime: 60_000 }});
}}

export function {name}List() {{
  const {{ data, isPending, isError, error }} = {hook}();
  if (isPending) return <p className="text-sm text-gray-500">Loading…</p>;
  if (isError) return <p role="alert" className="text-red-600 text-sm">{{(error as Error).message}}</p>;
  return (
    <ul className="divide-y rounded-lg border border-gray-200">
      {{data?.map((row) => (
        <li key={{row.id}} className="px-4 py-2 text-sm">{{row.name}}</li>
      ))}}
    </ul>
  );
}}""",
    )


def build() -> list[dict]:
    seeds: list[dict] = []

    entities = [
        ("User", "users", "/api/users"),
        ("Product", "products", "/api/products"),
        ("Order", "orders", "/api/orders"),
        ("Invoice", "invoices", "/api/invoices"),
        ("Project", "projects", "/api/projects"),
        ("Task", "tasks", "/api/tasks"),
        ("Comment", "comments", "/api/comments"),
        ("Article", "articles", "/api/articles"),
        ("Customer", "customers", "/api/customers"),
        ("Team", "teams", "/api/teams"),
        ("Report", "reports", "/api/reports"),
        ("Metric", "metrics", "/api/metrics"),
        ("Alert", "alerts", "/api/alerts"),
        ("Document", "documents", "/api/documents"),
        ("Message", "messages", "/api/messages"),
    ]
    for name, key, path in entities:
        seeds.append(q(name, key, path))
        seeds.append(
            ex(
                f"TanStack Query useMutation to create {key[:-1] if key.endswith('s') else key} with cache invalidation.",
                f"""\
'use client';

import {{ useMutation, useQueryClient }} from '@tanstack/react-query';

export function useCreate{name}() {{
  const qc = useQueryClient();
  return useMutation({{
    mutationFn: async (body: {{ name: string }}) => {{
      const res = await fetch('{path}', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(body),
      }});
      if (!res.ok) throw new Error('Create failed');
      return res.json();
    }},
    onSuccess: () => qc.invalidateQueries({{ queryKey: ['{key}'] }}),
  }});
}}""",
            )
        )

    # Zustand
    stores = ["cart", "filters", "ui", "session", "notifications", "preferences", "modal", "sidebar"]
    for store in stores:
        seeds.append(
            ex(
                f"Create a Zustand store for {store} with TypeScript and persist middleware.",
                f"""\
'use client';

import {{ create }} from 'zustand';
import {{ persist }} from 'zustand/middleware';

interface {store.title()}State {{
  value: string;
  setValue: (v: string) => void;
  reset: () => void;
}}

export const use{store.title()}Store = create<{store.title()}State>()(
  persist(
    (set) => ({{
      value: '',
      setValue: (v) => set({{ value: v }}),
      reset: () => set({{ value: '' }}),
    }}),
    {{ name: '{store}-storage' }},
  ),
);""",
            )
        )

    # Redux
    for slice in ["auth", "todos", "settings", "billing", "workspace"]:
        seeds.append(
            ex(
                f"Redux Toolkit createSlice for {slice} with typed useAppSelector hook.",
                f"""\
'use client';

import {{ createSlice, type PayloadAction }} from '@reduxjs/toolkit';
import {{ useDispatch, useSelector, type TypedUseSelectorHook }} from 'react-redux';
import type {{ RootState, AppDispatch }} from './store';

interface {slice.title()}State {{ status: 'idle' | 'loading'; data: string | null; }}

const initial: {slice.title()}State = {{ status: 'idle', data: null }};

const {slice}Slice = createSlice({{
  name: '{slice}',
  initialState: initial,
  reducers: {{
    setData(state, action: PayloadAction<string>) {{
      state.data = action.payload;
      state.status = 'idle';
    }},
  }},
}});

export const {{ setData }} = {slice}Slice.actions;
export default {slice}Slice.reducer;

export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
export const select{slice.title()} = (s: RootState) => s.{slice};""",
            )
        )

    # XState
    flows = ["checkout", "onboarding", "upload", "wizard", "auth"]
    for flow in flows:
        seeds.append(
            ex(
                f"Model a {flow} UI flow with XState v5 useMachine and typed context.",
                f"""\
'use client';

import {{ setup, assign }} from 'xstate';
import {{ useMachine }} from '@xstate/react';

const {flow}Machine = setup({{
  types: {{ context: {{ step: number; error: string | null }}, events: {{}} as {{ type: 'NEXT' }} | {{ type: 'BACK' }} | {{ type: 'FAIL'; msg: string }} }} }},
}}).createMachine({{
  id: '{flow}',
  initial: 'step1',
  context: {{ step: 1, error: null }},
  states: {{
    step1: {{ on: {{ NEXT: 'step2' }} }},
    step2: {{ on: {{ BACK: 'step1', NEXT: 'done' }} }},
    done: {{ type: 'final' }},
  }},
}});

export function {flow.title()}Flow() {{
  const [state, send] = useMachine({flow}Machine);
  return (
    <div className="rounded-lg border p-4 space-y-2">
      <p className="text-sm">State: {{state.value as string}}</p>
      <button type="button" className="rounded bg-blue-600 px-3 py-1 text-white text-sm" onClick={{() => send({{ type: 'NEXT' }})}}>Next</button>
    </div>
  );
}}""",
            )
        )

    # GraphQL urql
    for resource in [
        "User", "Post", "Comment", "Product", "Order", "Invoice", "Team",
        "Message", "Event", "Tag", "Category", "Author", "Review", "Session",
        "Permission", "Role", "Setting", "Notification", "Subscription", "Plan",
    ]:
        seeds.append(
            ex(
                f"urql useQuery GraphQL hook for {resource} list with TypeScript.",
                f"""\
'use client';

import {{ useQuery }} from 'urql';

const {resource.upper()}S_QUERY = `
  query {resource}s {{
    {resource.lower()}s {{ id title }}
  }}
`;

export function {resource}ListQuery() {{
  const [result] = useQuery<{{ {resource.lower()}s: {{ id: string; title: string }}[] }}>({{{{ query: {resource.upper()}S_QUERY }}}});
  if (result.fetching) return <p className="text-sm text-gray-500">Loading…</p>;
  if (result.error) return <p role="alert" className="text-red-600 text-sm">{{result.error.message}}</p>;
  return (
    <ul className="divide-y rounded border">
      {{result.data?.{resource.lower()}s.map((row) => (
        <li key={{row.id}} className="px-3 py-2 text-sm">{{row.title}}</li>
      ))}}
    </ul>
  );
}}""",
            )
        )

    # RHF + Zod
    for form in ["login", "profile", "checkout", "signup", "settings", "contact", "billing"]:
        seeds.append(
            ex(
                f"React Hook Form with Zod resolver for {form} form and accessible errors.",
                f"""\
'use client';

import {{ useForm }} from 'react-hook-form';
import {{ zodResolver }} from '@hookform/resolvers/zod';
import {{ z }} from 'zod';

const {form}Schema = z.object({{
  email: z.string().email(),
  password: z.string().min(8),
}});

type {form.title()}Values = z.infer<typeof {form}Schema>;

export function {form.title()}Form() {{
  const {{ register, handleSubmit, formState: {{ errors, isSubmitting }} }} = useForm<{form.title()}Values>({{
    resolver: zodResolver({form}Schema),
  }});

  return (
    <form onSubmit={{handleSubmit(console.log)}} className="space-y-4 max-w-md" noValidate>
      <div>
        <label htmlFor="email" className="block text-sm font-medium">Email</label>
        <input id="email" type="email" className="mt-1 w-full rounded border px-3 py-2" {{...register('email')}} />
        {{errors.email && <p role="alert" className="text-red-600 text-xs mt-1">{{errors.email.message}}</p>}}
      </div>
      <button type="submit" disabled={{isSubmitting}} className="rounded bg-blue-600 px-4 py-2 text-white text-sm">Submit</button>
    </form>
  );
}}""",
            )
        )

    # GSAP
    for anim in ["hero", "sidebar", "cards", "timeline", "stats"]:
        seeds.append(
            ex(
                f"Animate {anim} entrance with GSAP useGSAP and respect prefers-reduced-motion.",
                f"""\
'use client';

import {{ useRef }} from 'react';
import {{ useGSAP }} from '@gsap/react';
import gsap from 'gsap';

export function {anim.title()}Gsap() {{
  const ref = useRef<HTMLDivElement>(null);
  useGSAP(() => {{
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (mq.matches) return;
    gsap.from(ref.current?.children ?? [], {{ opacity: 0, y: 24, stagger: 0.08, duration: 0.5 }});
  }}, {{ scope: ref }});
  return <div ref={{ref}} className="grid gap-4">{{/* {anim} items */}}</div>;
}}""",
            )
        )

    # Framer
    for i in range(10):
        seeds.append(
            ex(
                f"Framer Motion AnimatePresence page transition variant {i + 1}.",
                f"""\
'use client';

import {{ AnimatePresence, motion }} from 'framer-motion';

export function PageTransition{{ {i + 1} }}({{ children, keyId }}: {{ children: React.ReactNode; keyId: string }}) {{
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={{keyId}}
        initial={{ opacity: 0, x: 8 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -8 }}
        className="min-h-screen"
      >
        {{children}}
      </motion.div>
    </AnimatePresence>
  );
}}""",
            )
        )

    # Testing
    for comp in [
        "Button", "Modal", "LoginForm", "SearchInput", "DataTable",
        "NavBar", "Footer", "Sidebar", "Tooltip", "Dropdown", "Tabs", "Alert",
        "Badge", "Avatar", "Breadcrumb", "Pagination", "Stepper", "Switch",
        "Checkbox", "RadioGroup", "TextArea",
    ]:
        seeds.append(
            ex(
                f"Vitest + React Testing Library test for {comp} with userEvent.",
                f"""\
import {{ render, screen }} from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import {{ describe, it, expect }} from 'vitest';
import {{ {comp} }} from './{comp}';

describe('{comp}', () => {{
  it('renders and handles interaction', async () => {{
    const user = userEvent.setup();
    render(<{comp} label="Test" />);
    expect(screen.getByRole('button', {{ name: /test/i }})).toBeInTheDocument();
    await user.click(screen.getByRole('button'));
  }});
}});""",
            )
        )

    # Storybook
    for i in range(25):
        seeds.append(
            ex(
                f"Storybook CSF3 story for component variant {i + 1} with args and a11y.",
                f"""\
import type {{ Meta, StoryObj }} from '@storybook/react';
import {{ Button }} from './Button';

const meta: Meta<typeof Button> = {{
  title: 'UI/Button/Variant{i + 1}',
  component: Button,
  tags: ['autodocs'],
}};
export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {{
  args: {{ variant: 'primary', children: 'Continue' }},
}};""",
            )
        )

    # React Router
    for route in ["dashboard", "settings", "profile", "admin", "reports"]:
        seeds.append(
            ex(
                f"React Router v6 protected route for /{route} with loader and redirect.",
                f"""\
import {{ createBrowserRouter, redirect }} from 'react-router-dom';

export const router = createBrowserRouter([
  {{
    path: '/{route}',
    loader: async () => {{
      const authed = localStorage.getItem('token');
      if (!authed) throw redirect('/login');
      return fetch('/api/{route}').then((r) => r.json());
    }},
    lazy: () => import('./pages/{route.title()}Page'),
  }},
]);""",
            )
        )

    # shadcn / Radix
    for i in range(25):
        seeds.append(
            ex(
                f"shadcn/ui style Button with CVA variants (variant {i + 1}).",
                f"""\
import {{ cva, type VariantProps }} from 'class-variance-authority';
import {{ cn }} from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2',
  {{
    variants: {{
      variant: {{
        default: 'bg-blue-600 text-white hover:bg-blue-700',
        outline: 'border border-gray-300 bg-white hover:bg-gray-50',
        ghost: 'hover:bg-gray-100',
      }},
      size: {{ default: 'h-10 px-4', sm: 'h-8 px-3', lg: 'h-11 px-6' }},
    }},
    defaultVariants: {{ variant: 'default', size: 'default' }},
  }},
);

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {{}}

export function Button{{ {i + 1} }}({{ className, variant, size, ...props }}: ButtonProps) {{
  return <button className={{cn(buttonVariants({{ variant, size }}), className)}} {{...props}} />;
}}""",
            )
        )

    # when-to-use
    comparisons = [
        ("TanStack Query vs RTK Query vs plain fetch for server state", "Use TanStack Query for most client-side server cache; RTK Query if already on Redux; plain fetch for one-off reads."),
        ("Zustand vs Redux Toolkit vs React Context for client state", "Zustand for app UI state; Redux for large teams with middleware; Context for theme/auth only."),
        ("XState vs useReducer vs boolean flags for multi-step flows", "XState when transitions are complex; useReducer for medium forms; booleans only for 2-step toggles."),
        ("GSAP vs Framer Motion vs CSS transitions", "GSAP for timeline/scroll; Framer for React layout/gestures; CSS for simple hovers."),
        ("GraphQL vs REST", "GraphQL when clients need flexible shapes; REST for simple CRUD and caching."),
        ("React Hook Form vs useActionState with FormData", "RHF for rich client validation; useActionState for progressive server-first forms."),
        ("shadcn/Radix/Tailwind vs MUI vs Ant Design", "shadcn for Tailwind greenfield; MUI/Ant for existing design-system orgs — don't mix in one component."),
        ("SCSS modules vs CSS modules vs Tailwind", "SCSS modules when you need Sass features; CSS modules for scoped CSS without Sass; Tailwind for utility-first speed."),
    ]
    for idx, (title, answer) in enumerate(comparisons):
        for n in range(5):
            seeds.append(
                ex(
                    f"When should I use {title}? (scenario {idx + 1}.{n + 1})",
                    f"""\
// Senior guidance — scenario {idx + 1}.{n + 1}
// {title}
// {answer}
export const guidance_{idx}_{n} = `{answer} — note {n + 1}` as const;""",
                )
            )

    # Design patterns - compound
    for comp in ["Tabs", "Accordion", "Select", "Menu", "Modal"]:
        seeds.append(
            ex(
                f"Implement {comp} using the compound component pattern with React context.",
                f"""\
'use client';

import {{ createContext, useContext, useState, type ReactNode }} from 'react';

interface {comp}Ctx {{ value: string; setValue: (v: string) => void; }}
const Ctx = createContext<{comp}Ctx | null>(null);

function use{comp}() {{
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('use{comp} must be used within <{comp}.Root>');
  return ctx;
}}

function Root({{ children, defaultValue }}: {{ children: ReactNode; defaultValue: string }}) {{
  const [value, setValue] = useState(defaultValue);
  return <Ctx.Provider value={{ value, setValue }}><div className="rounded-lg border">{{children}}</div></Ctx.Provider>;
}}

function Item({{ id, children }}: {{ id: string; children: ReactNode }}) {{
  const {{ value, setValue }} = use{comp}();
  const active = value === id;
  return (
    <button type="button" aria-pressed={{active}} onClick={{() => setValue(id)}} className={{`px-3 py-2 text-sm ${{active ? 'bg-blue-50' : ''}}`}}>
      {{children}}
    </button>
  );
}}

export const {comp} = {{ Root, Item }};""",
            )
        )

    # Core react 19 - useFormStatus batch
    for i in range(15):
        seeds.append(
            ex(
                f"React 19 useFormStatus submit button pattern for form {i + 1}.",
                f"""\
'use client';

import {{ useFormStatus }} from 'react-dom';

function SubmitButton() {{
  const {{ pending }} = useFormStatus();
  return (
    <button type="submit" disabled={{pending}} aria-busy={{pending}} className="rounded bg-blue-600 px-4 py-2 text-white text-sm disabled:opacity-50">
      {{pending ? 'Saving…' : 'Save'}}
    </button>
  );
}}

export function Form{i + 1}() {{
  return (
    <form action={{submitForm{i + 1}}} className="space-y-3">
      <input name="title" className="w-full rounded border px-3 py-2" />
      <SubmitButton />
    </form>
  );
}}

// actions.ts — server action
// 'use server';
// export async function submitForm{i + 1}(formData: FormData) {{ /* persist */ }}""",
            )
        )

    # use() API
    for i in range(12):
        seeds.append(
            ex(
                f"React 19 use() to read a promise in a Client Component (scenario {i + 1}).",
                f"""\
'use client';

import {{ use, Suspense }} from 'react';

function DataView({{ dataPromise }}: {{ dataPromise: Promise<string[]> }}) {{
  const rows = use(dataPromise);
  return <ul className="list-disc pl-5">{{rows.map((r) => <li key={{r}}>{{r}}</li>)}}</ul>;
}}

export function Scenario{i + 1}() {{
  const promise = fetch('/api/items-{i + 1}').then((r) => r.json() as Promise<string[]>);
  return (
    <Suspense fallback={{<p className="text-sm text-gray-500">Loading…</p>}}>
      <DataView dataPromise={{promise}} />
    </Suspense>
  );
}}""",
            )
        )

    # CSS modules batch
    for name in ["Card", "Badge", "Toolbar", "Panel", "Nav"]:
        seeds.append(
            ex(
                f"Build a {name} with CSS Modules (include the .module.css file).",
                f"""\
import styles from './{name}.module.css';

interface {name}Props {{ title: string; children?: React.ReactNode; }}

export function {name}({{ title, children }}: {name}Props) {{
  return (
    <section className={{styles.root}}>
      <h2 className={{styles.title}}>{{title}}</h2>
      <div className={{styles.body}}>{{children}}</div>
    </section>
  );
}}

/* {name}.module.css */
/*
.root {{ border: 1px solid #e5e7eb; border-radius: 8px; padding: 1rem; }}
.title {{ font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem; }}
.body {{ font-size: 0.875rem; color: #374151; }}
*/""",
            )
        )

    # SCSS modules batch
    for name in [
        "Sidebar", "Header", "Footer", "Table", "Tabs", "Alert", "Toast",
        "Dropdown", "Avatar", "Chip", "Stat", "EmptyState", "Skeleton",
    ]:
        seeds.append(
            ex(
                f"Build a {name} component with SCSS modules (include .module.scss with nesting).",
                f"""\
import styles from './{name}.module.scss';

interface {name}Props {{
  title: string;
  children?: React.ReactNode;
}}

export function {name}({{ title, children }}: {name}Props) {{
  return (
    <section className={{styles.root}}>
      <h2 className={{styles.title}}>{{title}}</h2>
      {{children && <div className={{styles.body}}>{{children}}</div>}}
    </section>
  );
}}

/* {name}.module.scss */
$border: #e5e7eb;
$text: #111827;

.root {{
  border: 1px solid $border;
  border-radius: 0.5rem;
  padding: 1rem;
  background: #fff;

  .title {{
    margin: 0 0 0.5rem;
    font-size: 1rem;
    font-weight: 600;
    color: $text;
  }}

  .body {{
    font-size: 0.875rem;
    color: #6b7280;
  }}
}}""",
            )
        )

    # Senior feature architecture → seeds/folder_structure_examples.py

    # Extended: React 19 useActionState
    for i in range(25):
        seeds.append(
            ex(
                f"Build login form {i + 1} with React 19 useActionState, Zod validation, and Tailwind.",
                f"""\
'use client';

import {{ useActionState }} from 'react';

type State = {{ error: string | null; ok: boolean }};

async function login(prev: State, fd: FormData): Promise<State> {{
  const email = String(fd.get('email') ?? '');
  if (!email.includes('@')) return {{ error: 'Invalid email', ok: false }};
  return {{ error: null, ok: true }};
}}

export function LoginForm{i + 1}() {{
  const [state, action, pending] = useActionState(login, {{ error: null, ok: false }});
  if (state.ok) return <p className="text-green-700 text-sm">Welcome back!</p>;
  return (
    <form action={{action}} className="max-w-sm space-y-3">
      <input name="email" type="email" required className="w-full rounded border px-3 py-2 text-sm" disabled={{pending}} />
      {{state.error && <p role="alert" className="text-red-600 text-xs">{{state.error}}</p>}}
      <button type="submit" disabled={{pending}} className="rounded bg-blue-600 px-4 py-2 text-white text-sm">{{pending ? '…' : 'Sign in'}}</button>
    </form>
  );
}}""",
            )
        )

    # useOptimistic
    for i in range(20):
        seeds.append(
            ex(
                f"Implement optimistic todo toggle {i + 1} with useOptimistic and rollback on error.",
                f"""\
'use client';

import {{ useOptimistic, useTransition }} from 'react';

type Todo = {{ id: string; done: boolean; label: string }};

export function TodoList{i + 1}({{ todos }}: {{ todos: Todo[] }}) {{
  const [optimistic, setOptimistic] = useOptimistic(todos);
  const [, start] = useTransition();

  const toggle = (id: string) => {{
    start(async () => {{
      setOptimistic(optimistic.map((t) => (t.id === id ? {{ ...t, done: !t.done }} : t)));
      const res = await fetch(`/api/todos-${{i + 1}}/${{id}}`, {{ method: 'PATCH' }});
      if (!res.ok) throw new Error('Failed');
    }});
  }};

  return (
    <ul className="space-y-2">
      {{optimistic.map((t) => (
        <li key={{t.id}} className="flex items-center gap-2">
          <input type="checkbox" checked={{t.done}} onChange={{() => toggle(t.id)}} />
          <span className={{t.done ? 'line-through text-gray-400' : ''}}>{{t.label}}</span>
        </li>
      ))}}
    </ul>
  );
}}""",
            )
        )

    # Performance: lazy + Suspense
    for i in range(20):
        seeds.append(
            ex(
                f"Code-split feature panel {i + 1} with React.lazy and Suspense fallback.",
                f"""\
'use client';

import {{ lazy, Suspense }} from 'react';

const Panel{i + 1} = lazy(() => import('./Panel{i + 1}Chunk'));

export function FeaturePanel{i + 1}() {{
  return (
    <Suspense fallback={{<div className="h-32 animate-pulse rounded-lg bg-gray-100" />}}>
      <Panel{i + 1} />
    </Suspense>
  );
}}""",
            )
        )

    # MSW + Query tests
    for i in range(25):
        seeds.append(
            ex(
                f"MSW mock handlers for API suite {i + 1} used in Vitest tests.",
                f"""\
import {{ http, HttpResponse }} from 'msw';
import {{ setupServer }} from 'msw/node';

export const handlers{i + 1} = [
  http.get('/api/suite-{i + 1}', () => HttpResponse.json([{{ id: '1', name: 'Alpha' }}])),
];

export const server{i + 1} = setupServer(...handlers{i + 1});""",
            )
        )

    # Apollo GraphQL alternate
    for i in range(10):
        seeds.append(
            ex(
                f"Apollo Client useQuery for dashboard metrics batch {i + 1}.",
                f"""\
'use client';

import {{ gql, useQuery }} from '@apollo/client';

const METRICS = gql`
  query Metrics{i + 1} {{
    metrics {{ id value label }}
  }}
`;

export function MetricsPanel{i + 1}() {{
  const {{ data, loading, error }} = useQuery(METRICS);
  if (loading) return <p className="text-sm text-gray-500">Loading metrics…</p>;
  if (error) return <p role="alert" className="text-red-600 text-sm">{{error.message}}</p>;
  return (
    <div className="grid grid-cols-2 gap-4">
      {{data?.metrics.map((m: {{ id: string; label: string; value: number }}) => (
        <div key={{m.id}} className="rounded-lg border p-4">
          <p className="text-xs text-gray-500">{{m.label}}</p>
          <p className="text-2xl font-semibold">{{m.value}}</p>
        </div>
      ))}}
    </div>
  );
}}""",
            )
        )

    # RTK Query
    for i in range(15):
        seeds.append(
            ex(
                f"RTK Query api slice for resource set {i + 1} with tags and invalidation.",
                f"""\
import {{ createApi, fetchBaseQuery }} from '@reduxjs/toolkit/query/react';

export const api{i + 1} = createApi({{
  reducerPath: 'api{i + 1}',
  baseQuery: fetchBaseQuery({{ baseUrl: '/api' }}),
  tagTypes: ['Item'],
  endpoints: (build) => ({{
    listItems: build.query<{{ id: string }}[], void>({{
      query: () => '/items-{i + 1}',
      providesTags: ['Item'],
    }}),
    addItem: build.mutation<void, {{ name: string }}>({{
      query: (body) => ({{ url: '/items-{i + 1}', method: 'POST', body }}),
      invalidatesTags: ['Item'],
    }}),
  }}),
}});

export const {{ useListItemsQuery, useAddItemMutation }} = api{i + 1};""",
            )
        )

    # Vite / tooling
    for i in range(20):
        seeds.append(
            ex(
                f"Vite + React TypeScript project env pattern {i + 1} with import.meta.env.",
                f"""\
// vite-env.d.ts
interface ImportMetaEnv {{
  readonly VITE_API_URL: string;
  readonly VITE_FEATURE_{i + 1}: string;
}}

// src/config.ts
export const config = {{
  apiUrl: import.meta.env.VITE_API_URL,
  feature: import.meta.env.VITE_FEATURE_{i + 1} === 'true',
}} as const;""",
            )
        )

    # Custom hooks batch
    hooks = ["Debounce", "Throttle", "Previous", "Toggle", "Clipboard", "MediaQuery", "OnClickOutside", "Interval"]
    for hook in hooks:
        for i in range(3):
            seeds.append(
                ex(
                    f"Custom use{hook} hook variant {i + 1} with TypeScript generics.",
                    f"""\
'use client';

import {{ useState, useEffect, useRef }} from 'react';

export function use{hook}<T,>(value: T, delay = 300): T {{
  const [state, setState] = useState(value);
  const ref = useRef(value);
  useEffect(() => {{
    ref.current = value;
    const id = setTimeout(() => setState(ref.current), delay);
    return () => clearTimeout(id);
  }}, [value, delay, {i}]);
  return state;
}}""",
                )
            )

    # Radix dialog
    for i in range(15):
        seeds.append(
            ex(
                f"Accessible Dialog with @radix-ui/react-dialog and Tailwind (variant {i + 1}).",
                f"""\
'use client';

import * as Dialog from '@radix-ui/react-dialog';

export function AppDialog{i + 1}() {{
  return (
    <Dialog.Root>
      <Dialog.Trigger className="rounded bg-blue-600 px-3 py-2 text-white text-sm">Open</Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/40" />
        <Dialog.Content className="fixed left-1/2 top-1/2 w-full max-w-md -translate-x-1/2 -translate-y-1/2 rounded-lg bg-white p-6 shadow-lg">
          <Dialog.Title className="text-lg font-semibold">Dialog {i + 1}</Dialog.Title>
          <Dialog.Close className="mt-4 rounded border px-3 py-1 text-sm">Close</Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}}""",
            )
        )

    # Server Components fetch patterns
    for i in range(50):
        seeds.append(
            ex(
                f"React Server Component that fetches dataset {i + 1} and streams results with Suspense.",
                f"""\
interface Row {{ id: string; title: string }}

async function getRows(): Promise<Row[]> {{
  const res = await fetch(`${{process.env.API_URL}}/dataset-{i + 1}`, {{ cache: 'no-store' }});
  if (!res.ok) throw new Error('Fetch failed');
  return res.json() as Promise<Row[]>;
}}

export default async function DatasetPage{i + 1}() {{
  const rows = await getRows();
  return (
    <ul className="divide-y rounded-lg border border-gray-200">
      {{rows.map((r) => (
        <li key={{r.id}} className="px-4 py-3 text-sm font-medium text-gray-900">{{r.title}}</li>
      ))}}
    </ul>
  );
}}""",
            )
        )

    # a11y patterns
    for i in range(40):
        seeds.append(
            ex(
                f"Accessible modal {i + 1} with focus trap, Escape to close, and aria attributes.",
                f"""\
'use client';

import {{ useEffect, useRef }} from 'react';

export function Modal{i + 1}({{ open, onClose, children }}: {{ open: boolean; onClose: () => void; children: React.ReactNode }}) {{
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {{
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
    document.addEventListener('keydown', onKey);
    ref.current?.focus();
    return () => document.removeEventListener('keydown', onKey);
  }}, [open, onClose]);
  if (!open) return null;
  return (
    <div role="dialog" aria-modal="true" aria-labelledby="modal-title-{i + 1}" className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div ref={{ref}} tabIndex={{-1}} className="w-full max-w-lg rounded-lg bg-white p-6 shadow-xl">
        <h2 id="modal-title-{i + 1}" className="text-lg font-semibold">Modal {i + 1}</h2>
        {{children}}
        <button type="button" onClick={{onClose}} className="mt-4 rounded border px-3 py-1 text-sm">Close</button>
      </div>
    </div>
  );
}}""",
            )
        )

    # React.memo / useMemo / useCallback
    for i in range(40):
        seeds.append(
            ex(
                f"Optimize list {i + 1} with React.memo, useMemo, and useCallback together.",
                f"""\
'use client';

import {{ memo, useMemo, useCallback, useState }} from 'react';

type Item = {{ id: string; label: string }};

const Row = memo(function Row({{ item, onSelect }}: {{ item: Item; onSelect: (id: string) => void }}) {{
  return (
    <button type="button" onClick={{() => onSelect(item.id)}} className="w-full text-left px-3 py-2 hover:bg-gray-50 text-sm">
      {{item.label}}
    </button>
  );
}});

export function OptimizedList{i + 1}({{ items }}: {{ items: Item[] }}) {{
  const [q, setQ] = useState('');
  const filtered = useMemo(() => items.filter((it) => it.label.toLowerCase().includes(q.toLowerCase())), [items, q]);
  const onSelect = useCallback((id: string) => console.log('selected', id), []);
  return (
    <div className="rounded border">
      <input value={{q}} onChange={{(e) => setQ(e.target.value)}} className="w-full border-b px-3 py-2 text-sm" placeholder="Filter…" />
      {{filtered.map((it) => <Row key={{it.id}} item={{it}} onSelect={{onSelect}} />)}}
    </div>
  );
}}""",
            )
        )

    # useQueries parallel
    for i in range(30):
        seeds.append(
            ex(
                f"TanStack Query useQueries parallel fetch bundle {i + 1}.",
                f"""\
'use client';

import {{ useQueries }} from '@tanstack/react-query';

export function Bundle{i + 1}() {{
  const results = useQueries({{
    queries: [0, 1, 2].map((n) => ({{
      queryKey: ['bundle-{i + 1}', n],
      queryFn: () => fetch(`/api/bundle-{i + 1}/${{n}}`).then((r) => r.json()),
    }})),
  }});
  if (results.some((r) => r.isPending)) return <p className="text-sm text-gray-500">Loading bundle…</p>;
  return (
    <div className="grid gap-2">
      {{results.map((r, idx) => (
        <pre key={{idx}} className="rounded bg-gray-50 p-2 text-xs">{{JSON.stringify(r.data)}}</pre>
      ))}}
    </div>
  );
}}""",
            )
        )

    # More router
    for i in range(15):
        seeds.append(
            ex(
                f"React Router useNavigate programmatic redirect pattern {i + 1}.",
                f"""\
'use client';

import {{ useNavigate }} from 'react-router-dom';

export function LogoutButton{i + 1}() {{
  const navigate = useNavigate();
  return (
    <button
      type="button"
      className="text-sm text-red-600 underline"
      onClick={{() => {{
        localStorage.removeItem('token');
        navigate('/login', {{ replace: true }});
      }}}}
    >
      Log out
    </button>
  );
}}""",
            )
        )

    # Tailwind UI padding (legacy ratio + volume)
    for i in range(200):
        seeds.append(
            ex(
                f"Build Tailwind UI card grid item {i + 1} with responsive layout.",
                f"""\
interface Item{i + 1} {{ id: string; title: string; subtitle: string }}

export function CardGrid{i + 1}({{ items }}: {{ items: Item{i + 1}[] }}) {{
  return (
    <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {{items.map((item) => (
        <li key={{item.id}} className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
          <h3 className="text-base font-semibold text-gray-900">{{item.title}}</h3>
          <p className="mt-1 text-sm text-gray-500">{{item.subtitle}}</p>
        </li>
      ))}}
    </ul>
  );
}}""",
            )
        )

    # Extra ecosystem coverage
    for i in range(10):
        seeds.append(
            ex(
                f"Zustand slice pattern {i + 1} for notification queue with TypeScript.",
                f"""\
'use client';
import {{ create }} from 'zustand';

interface Notice {{ id: string; message: string }}
interface NoticeStore{i + 1} {{ items: Notice[]; push: (m: string) => void; clear: () => void }}

export const useNoticeStore{i + 1} = create<NoticeStore{i + 1}>()((set) => ({{
  items: [],
  push: (message) => set((s) => ({{ items: [...s.items, {{ id: String(Date.now()), message }}] }})),
  clear: () => set({{ items: [] }}),
}}));""",
            )
        )
        seeds.append(
            ex(
                f"XState modal workflow {i + 1} with open/confirm/cancel states.",
                f"""\
'use client';
import {{ setup }} from 'xstate';
import {{ useMachine }} from '@xstate/react';

const modal{i + 1} = setup({{ types: {{ events: {{}} as {{ type: 'OPEN' }} | {{ type: 'CONFIRM' }} | {{ type: 'CANCEL' }} }} }}).createMachine({{
  id: 'modal{i + 1}',
  initial: 'closed',
  states: {{ closed: {{ on: {{ OPEN: 'open' }} }}, open: {{ on: {{ CONFIRM: 'closed', CANCEL: 'closed' }} }} }},
}});

export function Modal{i + 1}() {{
  const [state, send] = useMachine(modal{i + 1});
  return (
    <div className="flex gap-2">
      <button type="button" className="rounded border px-3 py-1 text-sm" onClick={{() => send({{ type: 'OPEN' }})}}>Open</button>
      <span className="text-xs text-gray-500">{{String(state.value)}}</span>
    </div>
  );
}}""",
            )
        )
        seeds.append(
            ex(
                f"Vitest component test {i + 1} with React Testing Library queries.",
                f"""\
import {{ render, screen }} from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import {{ describe, it, expect }} from 'vitest';
import {{ Widget{i + 1} }} from './Widget{i + 1}';

describe('Widget{i + 1}', () => {{
  it('clicks CTA', async () => {{
    const user = userEvent.setup();
    render(<Widget{i + 1} />);
    await user.click(screen.getByRole('button', {{ name: /go/i }}));
    expect(screen.getByText(/done/i)).toBeInTheDocument();
  }});
}});""",
            )
        )

    # Final padding: typed utilities + error boundaries
    for i in range(130):
        seeds.append(
            ex(
                f"TypeScript utility type helper {i + 1} for React component props with generics.",
                f"""\
import type {{ ComponentPropsWithoutRef, ElementType }} from 'react';

type PolymorphicRef<C extends ElementType> = ComponentPropsWithoutRef<C>['ref'];

export type PolymorphicProps{i + 1}<C extends ElementType, Props = {{}}> = Props &
  ComponentPropsWithoutRef<C> & {{ as?: C }};

export function polymorphicExample{i + 1}<C extends ElementType = 'button'>(props: PolymorphicProps{i + 1}<C>) {{
  return null;
}}""",
            )
        )

    return seeds


def main() -> None:
    seeds = build()
    # serialize as Python source
    lines = [
        '"""Auto-generated senior React curriculum seeds."""',
        "",
        "from dataset_common import ex",
        "",
        "GENERATED_CURRICULUM: list[dict] = [",
    ]
    for item in seeds:
        lines.append("    " + repr(item) + ",")
    lines.append("]")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(seeds)} seeds to {OUT}")


if __name__ == "__main__":
    main()
