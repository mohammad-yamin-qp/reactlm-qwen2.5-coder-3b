"""
Additional unique seeds: fix / refactor / choose patterns and under-covered APIs.
"""

from dataset_common import ex

QUALITY_EXAMPLES: list[dict] = [
    # ── Fix: unnecessary 'use client' ────────────────────────────────────────
    ex(
        "This component fetches users on the server but has 'use client' — fix it.",
        '''\
// Fetch on the server; no client hooks needed.
interface User {
  id: string;
  name: string;
}

async function getUsers(): Promise<User[]> {
  const res = await fetch(`${process.env.API_URL}/users`);
  if (!res.ok) throw new Error('Failed to load users');
  return res.json() as Promise<User[]>;
}

export default async function UserList() {
  const users = await getUsers();
  return (
    <ul className="divide-y divide-gray-200 rounded-lg border border-gray-200">
      {users.map((u) => (
        <li key={u.id} className="px-4 py-3 text-sm text-gray-900">
          {u.name}
        </li>
      ))}
    </ul>
  );
}''',
    ),
    ex(
        "Fix this Client Component that derives filtered items in useEffect instead of during render.",
        '''\
'use client';

import { useMemo, useState } from 'react';

interface ItemListProps {
  items: string[];
}

export function ItemList({ items }: ItemListProps) {
  const [query, setQuery] = useState('');

  const filtered = useMemo(
    () => items.filter((item) => item.toLowerCase().includes(query.toLowerCase())),
    [items, query],
  );

  return (
    <div className="space-y-3">
      <label htmlFor="search" className="sr-only">
        Filter items
      </label>
      <input
        id="search"
        type="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search…"
        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
      />
      <ul className="list-disc pl-5 text-sm text-gray-800">
        {filtered.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}''',
    ),
    # ── Choose: Server vs Client split ───────────────────────────────────────
    ex(
        "Split a product page into a Server Component that fetches data and a Client Component search filter with Tailwind CSS.",
        '''\
// products/page.tsx — Server Component
import { ProductSearch } from './ProductSearch';

interface Product {
  id: string;
  name: string;
  category: string;
}

async function getProducts(): Promise<Product[]> {
  const res = await fetch(`${process.env.API_URL}/products`);
  return res.json() as Promise<Product[]>;
}

export default async function ProductsPage() {
  const products = await getProducts();
  return (
    <main className="mx-auto max-w-4xl p-6">
      <h1 className="mb-4 text-2xl font-bold text-gray-900">Products</h1>
      <ProductSearch products={products} />
    </main>
  );
}

// products/ProductSearch.tsx
'use client';

import { useMemo, useState } from 'react';

interface Product {
  id: string;
  name: string;
  category: string;
}

interface ProductSearchProps {
  products: Product[];
}

export function ProductSearch({ products }: ProductSearchProps) {
  const [q, setQ] = useState('');

  const visible = useMemo(
    () => products.filter((p) => p.name.toLowerCase().includes(q.toLowerCase())),
    [products, q],
  );

  return (
    <div className="space-y-4">
      <input
        type="search"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Search products…"
        aria-label="Search products"
        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
      />
      <ul className="grid gap-3 sm:grid-cols-2">
        {visible.map((p) => (
          <li key={p.id} className="rounded-lg border border-gray-200 p-4">
            <p className="font-medium text-gray-900">{p.name}</p>
            <p className="text-xs text-gray-500">{p.category}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}''',
    ),
    # ── React 19: useOptimistic ──────────────────────────────────────────────
    ex(
        "Build a todo list with useOptimistic and a Server Action in React 19.",
        '''\
'use client';

import { useOptimistic, useTransition } from 'react';

interface Todo {
  id: string;
  text: string;
  done: boolean;
}

interface TodoListProps {
  initialTodos: Todo[];
  addTodo: (text: string) => Promise<Todo>;
  toggleTodo: (id: string) => Promise<void>;
}

type TodoAction =
  | { type: 'add'; text: string }
  | { type: 'toggle'; id: string };

function applyTodoAction(todos: Todo[], action: TodoAction): Todo[] {
  if (action.type === 'add') {
    return [...todos, { id: `temp-${Date.now()}`, text: action.text, done: false }];
  }
  return todos.map((t) => (t.id === action.id ? { ...t, done: !t.done } : t));
}

export function TodoList({ initialTodos, addTodo, toggleTodo }: TodoListProps) {
  const [optimisticTodos, addOptimistic] = useOptimistic(initialTodos, applyTodoAction);
  const [isPending, startTransition] = useTransition();

  const handleAdd = (formData: FormData) => {
    const text = (formData.get('text') as string).trim();
    if (!text) return;
    startTransition(async () => {
      addOptimistic({ type: 'add', text });
      await addTodo(text);
    });
  };

  const handleToggle = (id: string) => {
    startTransition(async () => {
      addOptimistic({ type: 'toggle', id });
      await toggleTodo(id);
    });
  };

  return (
    <div className="mx-auto max-w-md space-y-4">
      <form action={handleAdd} className="flex gap-2">
        <input
          name="text"
          required
          disabled={isPending}
          className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm"
          placeholder="New todo…"
        />
        <button
          type="submit"
          disabled={isPending}
          className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          Add
        </button>
      </form>
      <ul className="space-y-2">
        {optimisticTodos.map((todo) => (
          <li key={todo.id} className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={todo.done}
              onChange={() => handleToggle(todo.id)}
              disabled={isPending}
              aria-label={`Mark "${todo.text}" as done`}
            />
            <span className={todo.done ? 'text-gray-400 line-through' : 'text-gray-900'}>
              {todo.text}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}''',
    ),
    ex(
        "Use useTransition to keep the UI responsive while updating a large filtered list.",
        '''\
'use client';

import { useMemo, useState, useTransition } from 'react';

interface Record {
  id: string;
  label: string;
}

interface FilteredListProps {
  records: Record[];
}

function filterRecords(records: Record[], query: string): Record[] {
  const q = query.toLowerCase();
  return records.filter((r) => r.label.toLowerCase().includes(q));
}

export function FilteredList({ records }: FilteredListProps) {
  const [query, setQuery] = useState('');
  const [displayQuery, setDisplayQuery] = useState('');
  const [isPending, startTransition] = useTransition();

  const filtered = useMemo(
    () => filterRecords(records, displayQuery),
    [records, displayQuery],
  );

  const onChange = (value: string) => {
    setQuery(value);
    startTransition(() => setDisplayQuery(value));
  };

  return (
    <div className="space-y-2">
      <input
        type="search"
        value={query}
        onChange={(e) => onChange(e.target.value)}
        aria-busy={isPending}
        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
        placeholder="Filter…"
      />
      <p className="text-xs text-gray-500" aria-live="polite">
        {isPending ? 'Updating…' : `${filtered.length} results`}
      </p>
      <ul className="max-h-64 overflow-y-auto rounded-md border border-gray-200">
        {filtered.map((r) => (
          <li key={r.id} className="border-b border-gray-100 px-3 py-2 text-sm last:border-0">
            {r.label}
          </li>
        ))}
      </ul>
    </div>
  );
}''',
    ),
    ex(
        "Create an App Router error.tsx boundary with Tailwind CSS and a retry button.",
        '''\
'use client';

interface ErrorPageProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ErrorPage({ error, reset }: ErrorPageProps) {
  return (
    <main className="flex min-h-[50vh] flex-col items-center justify-center p-6 text-center">
      <h1 className="text-2xl font-bold text-gray-900">Something went wrong</h1>
      <p className="mt-2 max-w-md text-sm text-gray-600" role="alert">
        {error.message || 'An unexpected error occurred.'}
      </p>
      {error.digest && (
        <p className="mt-1 font-mono text-xs text-gray-400">ID: {error.digest}</p>
      )}
      <button
        type="button"
        onClick={reset}
        className="mt-6 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
      >
        Try again
      </button>
    </main>
  );
}''',
    ),
    ex(
        "Create a loading.tsx skeleton for a blog post page using Tailwind CSS.",
        '''\
export default function Loading() {
  return (
    <article className="mx-auto max-w-2xl animate-pulse space-y-4 p-6" aria-busy="true" aria-label="Loading article">
      <div className="h-8 w-3/4 rounded bg-gray-200" />
      <div className="h-4 w-1/3 rounded bg-gray-200" />
      <div className="space-y-2 pt-4">
        <div className="h-4 w-full rounded bg-gray-100" />
        <div className="h-4 w-5/6 rounded bg-gray-100" />
      </div>
    </article>
  );
}''',
    ),
    ex(
        "Refactor this legacy fetch-on-mount pattern into a Server Component.",
        '''\
// BEFORE (client fetch on mount — avoid):
// 'use client';
// useEffect(() => { fetch('/api/posts').then(r => r.json()).then(setPosts); }, []);

// AFTER — Server Component:
interface Post {
  id: string;
  title: string;
}

async function getPosts(): Promise<Post[]> {
  const res = await fetch(`${process.env.API_URL}/posts`, {
    next: { tags: ['posts'] },
  });
  if (!res.ok) throw new Error('Failed to load posts');
  return res.json() as Promise<Post[]>;
}

export default async function PostList() {
  const posts = await getPosts();
  return (
    <section aria-labelledby="posts-heading">
      <h2 id="posts-heading" className="mb-4 text-xl font-semibold text-gray-900">
        Latest posts
      </h2>
      <ul className="space-y-3">
        {posts.map((post) => (
          <li key={post.id}>
            <a href={`/posts/${post.id}`} className="text-blue-600 hover:underline">
              {post.title}
            </a>
          </li>
        ))}
      </ul>
    </section>
  );
}''',
    ),
    ex(
        "Build a typed React context for theme (light/dark) with CSS Modules and a provider hook.",
        '''\
// ThemeContext.tsx
'use client';

import { createContext, useContext, useState, useCallback, type ReactNode } from 'react';
import styles from './ThemeProvider.module.css';

type Theme = 'light' | 'dark';

interface ThemeContextValue {
  theme: Theme;
  toggle: () => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

interface ThemeProviderProps {
  children: ReactNode;
  initial?: Theme;
}

export function ThemeProvider({ children, initial = 'light' }: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(initial);
  const toggle = useCallback(
    () => setTheme((t) => (t === 'light' ? 'dark' : 'light')),
    [],
  );

  return (
    <ThemeContext.Provider value={{ theme, toggle }}>
      <div className={theme === 'dark' ? styles.dark : styles.light}>{children}</div>
    </ThemeContext.Provider>
  );
}

export function useTheme(): ThemeContextValue {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider');
  return ctx;
}

/* ThemeProvider.module.css */
.light {
  background: #ffffff;
  color: #111827;
  min-height: 100%;
}

.dark {
  background: #111827;
  color: #f9fafb;
  min-height: 100%;
}''',
    ),
    ex(
        "Fix a form that uses index as key when reordering items — show the corrected list component.",
        '''\
'use client';

import { useState } from 'react';

interface Task {
  id: string;
  label: string;
}

const INITIAL: Task[] = [
  { id: 'a', label: 'Write tests' },
  { id: 'b', label: 'Ship feature' },
  { id: 'c', label: 'Update docs' },
];

export function ReorderableTasks() {
  const [tasks, setTasks] = useState<Task[]>(INITIAL);

  const moveUp = (index: number) => {
    if (index === 0) return;
    setTasks((prev) => {
      const next = [...prev];
      [next[index - 1], next[index]] = [next[index], next[index - 1]];
      return next;
    });
  };

  return (
    <ul className="space-y-2">
      {tasks.map((task, index) => (
        <li key={task.id} className="flex items-center gap-2 rounded-md border border-gray-200 p-2">
          <span className="flex-1 text-sm text-gray-900">{task.label}</span>
          <button
            type="button"
            onClick={() => moveUp(index)}
            disabled={index === 0}
            className="rounded px-2 py-1 text-xs text-blue-600 hover:bg-blue-50 disabled:opacity-40"
          >
            Move up
          </button>
        </li>
      ))}
    </ul>
  );
}''',
    ),
]
