"""Seeds teaching conventional React + TypeScript project folder structure."""

from dataset_common import ex

FOLDER_STRUCTURE_EXAMPLES: list[dict] = [
    ex(
        "What is a conventional React 19 + TypeScript + Vite folder structure for a medium-sized SPA?",
        '''\
Use a shallow `src/` tree early; grow into feature folders as domains appear.

```
my-app/
├── public/
├── src/
│   ├── app/                 # App shell: providers, router root, global layout
│   │   ├── App.tsx
│   │   ├── providers.tsx    # QueryClient, theme, etc.
│   │   └── routes.tsx       # React Router route config (optional)
│   ├── features/            # Business domains (checkout, auth, dashboard)
│   │   └── products/
│   │       ├── components/
│   │       ├── hooks/
│   │       ├── api.ts
│   │       └── types.ts
│   ├── components/          # Shared UI only (Button, Modal, Input)
│   │   └── ui/
│   ├── hooks/               # Shared hooks (useDebounce, useMediaQuery)
│   ├── lib/                 # Pure helpers, fetch wrappers, formatters
│   ├── types/               # Global types / API contracts
│   ├── assets/
│   ├── main.tsx
│   └── vite-env.d.ts
├── index.html
├── vite.config.ts
└── tsconfig.json
```

Principles:
- **Colocate by feature** what changes together (checkout UI + checkout hooks + checkout API).
- Keep **shared** pieces in `components/` and `hooks/` only when used in 2+ features.
- Put **providers** in one place (`app/providers.tsx`) so wiring is obvious.
- Avoid deep nesting until a folder has ~7+ files; then split (`components/`, `hooks/`).''',
    ),
    ex(
        "Feature-based vs type-based folder structure in React — when should I use each?",
        '''\
**Type-based** (`components/`, `hooks/`, `pages/` at the root) works well for:
- Small apps and prototypes
- Few domains, many reusable UI primitives
- Teams that mostly share one component library

**Feature-based** (`features/auth/`, `features/checkout/`) works well for:
- Multiple product domains owned by different people
- Reducing cross-import spaghetti
- Deleting or extracting a whole feature as a unit

**Hybrid (recommended at scale):**

```
src/
  features/checkout/     # owns checkout-specific UI + hooks + API
  features/auth/
  components/ui/         # design-system primitives used everywhere
  hooks/                 # truly generic hooks
  lib/
```

Rule of thumb: start type-based; move a folder into `features/<name>/` when imports from other domains appear inside it, or when one team owns that slice end-to-end.''',
    ),
    ex(
        "Architect a production checkout feature (TanStack Query + XState + React Hook Form) — show folder structure and provider wiring.",
        '''\
```
src/
├── app/
│   └── providers.tsx
├── features/
│   └── checkout/
│       ├── components/
│       │   ├── CheckoutWizard.tsx
│       │   ├── PaymentStep.tsx
│       │   └── OrderSummary.tsx
│       ├── hooks/
│       │   ├── useCheckoutMachine.ts
│       │   └── useCheckoutForm.ts
│       ├── api/
│       │   └── checkoutApi.ts
│       ├── checkoutMachine.ts
│       └── types.ts
└── main.tsx
```

`src/app/providers.tsx` — mount data + form context once:

```tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import type { ReactNode } from 'react';
import { useState } from 'react';

export function AppProviders({ children }: { children: ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}
```

`src/features/checkout/hooks/useCheckoutForm.ts` — RHF + Zod live next to the feature:

```tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({ email: z.string().email(), cardLast4: z.string().length(4) });
export type CheckoutFormValues = z.infer<typeof schema>;

export function useCheckoutForm() {
  return useForm<CheckoutFormValues>({ resolver: zodResolver(schema), mode: 'onBlur' });
}
```

`src/features/checkout/checkoutMachine.ts` — XState machine is a plain module (testable without React).

Keep **routes/pages thin**: they compose `CheckoutWizard` and pass route params; business logic stays under `features/checkout/`.''',
    ),
    ex(
        "Where should shared UI components vs feature-specific components live in a React codebase?",
        '''\
**Shared (`src/components/`)** — move here when:
- Used in 2+ features (Button, Dialog, DataTable shell)
- No business rules (only presentation + a11y)
- Part of your design system / shadcn `ui/` layer

**Feature (`src/features/<feature>/components/`)** — keep here when:
- Named after domain concepts (`OrderSummary`, `SeatPicker`)
- Imports feature hooks, API, or types
- Would break if the feature were removed

Example:

```
src/
  components/ui/button.tsx          # generic
  features/checkout/components/
    PaymentStep.tsx                   # knows about checkout form + machine
```

Anti-pattern: `components/CheckoutPaymentStep.tsx` that imports `features/checkout/hooks` — that couples shared UI to one domain. Either move it into the feature or split a dumb presentational piece into `components/ui/`.''',
    ),
    ex(
        "Show colocated folder structure for a React component using CSS Modules (Button with variants).",
        '''\
Colocate the component, styles, tests, and barrel export:

```
src/components/ui/Button/
├── Button.tsx
├── Button.module.css
├── Button.test.tsx
└── index.ts
```

`Button.tsx`:

```tsx
import styles from './Button.module.css';

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'ghost';
};

export function Button({ variant = 'primary', className, ...props }: ButtonProps) {
  return (
    <button
      type="button"
      className={[styles.root, styles[variant], className].filter(Boolean).join(' ')}
      {...props}
    />
  );
}
```

`Button.module.css`:

```css
.root {
  display: inline-flex;
  align-items: center;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
}
.primary {
  background: #2563eb;
  color: #fff;
}
.ghost {
  background: transparent;
  color: #374151;
}
```

`index.ts`:

```ts
export { Button } from './Button';
```

Import as `import { Button } from '@/components/ui/Button'`. Do not put feature-specific buttons in `components/ui/` — use `features/<name>/components/` instead.''',
    ),
    ex(
        "React Router v6: show a conventional folder layout with route colocation.",
        '''\
Colocate each route's page and its private components:

```
src/
├── app/
│   ├── providers.tsx
│   └── router.tsx
├── routes/
│   ├── products/
│   │   ├── ProductsPage.tsx
│   │   ├── ProductSearch.tsx      # only used by products route
│   │   └── productLoader.ts
│   └── settings/
│       └── SettingsPage.tsx
├── components/ui/                 # shared primitives
└── main.tsx
```

`src/app/router.tsx`:

```tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { ProductsPage } from '@/routes/products/ProductsPage';
import { SettingsPage } from '@/routes/settings/SettingsPage';

const router = createBrowserRouter([
  { path: '/', element: <ProductsPage /> },
  { path: '/settings', element: <SettingsPage /> },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
```

`src/routes/products/ProductsPage.tsx` — fetch or loader at route boundary; client filter in sibling file:

```tsx
import { ProductSearch } from './ProductSearch';

export function ProductsPage() {
  // In a data-router setup, useRouteLoaderData('products') here
  const products = [{ id: '1', name: 'Desk', category: 'Office' }];
  return (
    <main className="mx-auto max-w-4xl p-6">
      <h1 className="text-2xl font-bold">Products</h1>
      <ProductSearch products={products} />
    </main>
  );
}
```

Keep **loaders/actions** beside the route (`productLoader.ts`), not in a global `api/` folder, unless multiple routes share the same client.''',
    ),
    ex(
        "What is the difference between src/lib, src/utils, and src/hooks in a React project?",
        '''\
There is no universal standard — pick names and document them. Common conventions:

| Folder | Put here | Avoid |
|--------|----------|--------|
| `lib/` | App-specific infrastructure: `apiClient`, `queryKeys`, auth token helpers | React hooks |
| `utils/` or `lib/utils/` | Pure functions: `formatCurrency`, `cn()`, date helpers | Side effects, `fetch` |
| `hooks/` | Reusable React hooks: `useDebounce`, `useLocalStorage` | One-off feature hooks |

**Feature hooks** belong in `features/<name>/hooks/`, not root `hooks/`.

Example:

```
src/
  lib/
    apiClient.ts       # fetch wrapper + base URL
    queryKeys.ts
  utils/
    format.ts
  hooks/
    useDebounce.ts
  features/auth/hooks/
    useSession.ts
```

If `lib/` and `utils/` feel redundant, merge into `lib/` with subfolders: `lib/api/`, `lib/format/`. Consistency matters more than the exact label.''',
    ),
    ex(
        "How should I organize tests in a React + Vitest project — colocated vs top-level tests folder?",
        '''\
Both are valid; many teams use **colocated tests** next to source:

```
src/features/checkout/components/
  CheckoutWizard.tsx
  CheckoutWizard.test.tsx
```

Or a `__tests__` sibling folder when a component accumulates many test files:

```
Button/
  Button.tsx
  __tests__/Button.test.tsx
  __tests__/Button.a11y.test.tsx
```

**Top-level `tests/`** is useful for:
- End-to-end specs (Playwright)
- MSW handlers shared across features (`tests/mocks/handlers.ts`)
- Integration tests that span multiple features

Suggested layout:

```
src/                    # unit + component tests colocated
tests/
  e2e/
  mocks/
vitest.config.ts
```

Import test utilities from `@/tests/mocks/server` only in test files, never in production `src/`.''',
    ),
    ex(
        "Show a dashboard feature folder structure using TanStack Query and Zustand for UI filters.",
        '''\
```
src/features/dashboard/
├── components/
│   ├── DashboardPage.tsx
│   ├── MetricsGrid.tsx
│   └── FilterBar.tsx
├── hooks/
│   ├── useMetricsQuery.ts
│   └── useDashboardFilters.ts
├── store/
│   └── filterStore.ts
└── types.ts
```

`store/filterStore.ts` — Zustand for client-only UI state (date range, tab):

```ts
import { create } from 'zustand';

type FilterState = { range: '7d' | '30d'; setRange: (r: '7d' | '30d') => void };

export const useFilterStore = create<FilterState>((set) => ({
  range: '7d',
  setRange: (range) => set({ range }),
}));
```

`hooks/useMetricsQuery.ts` — server state via TanStack Query:

```tsx
import { useQuery } from '@tanstack/react-query';
import { useFilterStore } from '../store/filterStore';

async function fetchMetrics(range: string) {
  const res = await fetch(`/api/metrics?range=${range}`);
  if (!res.ok) throw new Error('Failed to load metrics');
  return res.json() as Promise<{ label: string; value: number }[]>;
}

export function useMetricsQuery() {
  const range = useFilterStore((s) => s.range);
  return useQuery({ queryKey: ['metrics', range], queryFn: () => fetchMetrics(range) });
}
```

**Split rule:** Query = server data; Zustand = UI filters that should not be refetched. Do not put API responses in Zustand unless you have a documented cache-sync strategy.''',
    ),
    ex(
        "Design-system / Storybook folder structure with compound components in React.",
        '''\
```
src/
├── components/ui/              # primitives (Button, Input) — Storybook stories here
│   ├── Button/
│   └── Dialog/
├── features/design-system/     # optional: docs-only stories for compositions
│   └── stories/
└── .storybook/
    ├── main.ts
    └── preview.tsx
```

Compound card example — one folder, subcomponents as static properties:

```
src/components/ui/Card/
├── Card.tsx
├── Card.module.css
├── Card.stories.tsx
└── index.ts
```

`Card.tsx`:

```tsx
import type { ReactNode } from 'react';
import styles from './Card.module.css';

function CardRoot({ children }: { children: ReactNode }) {
  return <article className={styles.card}>{children}</article>;
}
function CardHeader({ children }: { children: ReactNode }) {
  return <header className={styles.header}>{children}</header>;
}
function CardBody({ children }: { children: ReactNode }) {
  return <div className={styles.body}>{children}</div>;
}

export const Card = Object.assign(CardRoot, { Header: CardHeader, Body: CardBody });
```


Storybook files sit next to the component (`Card.stories.tsx`) so stories move with refactors. Feature-specific composites (e.g. `CheckoutSummaryCard`) belong under `features/checkout/components/`, not `components/ui/`.''',
    ),
    ex(
        "Small React app: minimal src/ layout before introducing features/ folder.",
        '''\
For apps under ~15 components, keep it flat:

```
src/
├── components/       # all UI for now
├── hooks/
├── pages/            # route-level screens (or routes/ with React Router)
├── lib/
├── App.tsx
└── main.tsx
```

When `components/` mixes unrelated domains (auth forms + billing tables + chat widgets), create the first feature folder:

```
src/features/billing/components/InvoiceTable.tsx
```

Move files in a single PR per feature to keep git history readable. Do not create empty `features/*` scaffolding upfront — wait until a second domain appears.''',
    ),
    ex(
        "How do I structure environment config and API base URLs in a Vite + React TypeScript app?",
        '''\
Keep env access in one module; never scatter `import.meta.env` across components.

```
src/
├── lib/
│   └── config.ts
├── vite-env.d.ts
└── main.tsx
```

`vite-env.d.ts`:

```ts
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_ENABLE_ANALYTICS: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

`src/lib/config.ts`:

```ts
function requireEnv(key: keyof ImportMetaEnv): string {
  const value = import.meta.env[key];
  if (!value) throw new Error(`Missing env: ${key}`);
  return value;
}

export const config = {
  apiUrl: requireEnv('VITE_API_URL'),
  analytics: import.meta.env.VITE_ENABLE_ANALYTICS === 'true',
} as const;
```

`src/lib/apiClient.ts` imports `config.apiUrl` only. Feature folders import `apiClient`, not `import.meta.env` directly.''',
    ),
]
