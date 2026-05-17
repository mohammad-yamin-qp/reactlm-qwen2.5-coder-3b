#!/usr/bin/env python3
"""
React Golden Dataset Generator
Run: python generate_dataset.py
Output: react_golden_dataset.jsonl
"""

import json
from pathlib import Path

from dataset_common import ex
from styling_examples import STYLING_EXAMPLES

EXAMPLES: list[dict] = [

    # ════════════════════════════════════════════════════════════════════════
    # REACT 19 — useActionState
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Create a login form using React 19's useActionState with TypeScript, loading state, and error display.",
        '''\
'use client';

import { useActionState } from 'react';

type LoginState = { error: string | null; success: boolean };

async function loginAction(_prev: LoginState, formData: FormData): Promise<LoginState> {
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;
  if (!email || !password) return { error: 'Email and password are required.', success: false };
  const res = await fetch('/api/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
    headers: { 'Content-Type': 'application/json' },
  });
  return res.ok ? { error: null, success: true } : { error: 'Invalid credentials.', success: false };
}

export default function LoginForm() {
  const [state, dispatch, isPending] = useActionState(loginAction, { error: null, success: false });

  if (state.success) return <p role="status">Login successful! Redirecting…</p>;

  return (
    <form action={dispatch} aria-label="Login form" noValidate>
      <div>
        <label htmlFor="email">Email address</label>
        <input id="email" name="email" type="email" autoComplete="email" required disabled={isPending} />
      </div>
      <div>
        <label htmlFor="password">Password</label>
        <input id="password" name="password" type="password" autoComplete="current-password" required disabled={isPending} />
      </div>
      {state.error && <p role="alert" aria-live="assertive">{state.error}</p>}
      <button type="submit" disabled={isPending} aria-busy={isPending}>
        {isPending ? 'Signing in…' : 'Sign in'}
      </button>
    </form>
  );
}''',
    ),

    ex(
        "Build a registration form with useActionState that validates email format and password strength.",
        '''\
'use client';

import { useActionState } from 'react';

type RegisterState = { errors: Record<string, string>; success: boolean };

const EMAIL_RE = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;

async function registerAction(_prev: RegisterState, formData: FormData): Promise<RegisterState> {
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;
  const confirm = formData.get('confirm') as string;
  const errors: Record<string, string> = {};

  if (!EMAIL_RE.test(email)) errors.email = 'Enter a valid email address.';
  if (password.length < 8) errors.password = 'Password must be at least 8 characters.';
  if (password !== confirm) errors.confirm = 'Passwords do not match.';
  if (Object.keys(errors).length > 0) return { errors, success: false };

  const res = await fetch('/api/register', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
    headers: { 'Content-Type': 'application/json' },
  });
  if (!res.ok) return { errors: { form: 'Registration failed. Try again.' }, success: false };
  return { errors: {}, success: true };
}

export default function RegisterForm() {
  const [state, dispatch, isPending] = useActionState(registerAction, { errors: {}, success: false });

  if (state.success) return <p role="status">Account created! Check your email.</p>;

  return (
    <form action={dispatch} noValidate aria-label="Create account">
      {state.errors.form && <p role="alert">{state.errors.form}</p>}

      <div>
        <label htmlFor="reg-email">Email</label>
        <input id="reg-email" name="email" type="email" required disabled={isPending}
          aria-describedby={state.errors.email ? 'email-err' : undefined} />
        {state.errors.email && <span id="email-err" role="alert">{state.errors.email}</span>}
      </div>

      <div>
        <label htmlFor="reg-password">Password</label>
        <input id="reg-password" name="password" type="password" required disabled={isPending}
          aria-describedby={state.errors.password ? 'pw-err' : undefined} />
        {state.errors.password && <span id="pw-err" role="alert">{state.errors.password}</span>}
      </div>

      <div>
        <label htmlFor="reg-confirm">Confirm password</label>
        <input id="reg-confirm" name="confirm" type="password" required disabled={isPending}
          aria-describedby={state.errors.confirm ? 'confirm-err' : undefined} />
        {state.errors.confirm && <span id="confirm-err" role="alert">{state.errors.confirm}</span>}
      </div>

      <button type="submit" disabled={isPending} aria-busy={isPending}>
        {isPending ? 'Creating account…' : 'Create account'}
      </button>
    </form>
  );
}''',
    ),

    ex(
        "Create a contact form with useActionState that sends a message and resets on success.",
        '''\
'use client';

import { useActionState, useRef, useEffect } from 'react';

type ContactState = { error: string | null; success: boolean };

async function sendMessage(_prev: ContactState, formData: FormData): Promise<ContactState> {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;
  const message = formData.get('message') as string;
  if (!name || !email || !message) return { error: 'All fields are required.', success: false };
  const res = await fetch('/api/contact', {
    method: 'POST',
    body: JSON.stringify({ name, email, message }),
    headers: { 'Content-Type': 'application/json' },
  });
  return res.ok ? { error: null, success: true } : { error: 'Failed to send. Please try again.', success: false };
}

export default function ContactForm() {
  const formRef = useRef<HTMLFormElement>(null);
  const [state, dispatch, isPending] = useActionState(sendMessage, { error: null, success: false });

  useEffect(() => {
    if (state.success) formRef.current?.reset();
  }, [state.success]);

  return (
    <form ref={formRef} action={dispatch} aria-label="Contact form">
      {state.success && <p role="status" aria-live="polite">Message sent! We will be in touch soon.</p>}
      {state.error && <p role="alert">{state.error}</p>}

      <label htmlFor="ct-name">Full name</label>
      <input id="ct-name" name="name" type="text" autoComplete="name" required disabled={isPending} />

      <label htmlFor="ct-email">Email</label>
      <input id="ct-email" name="email" type="email" autoComplete="email" required disabled={isPending} />

      <label htmlFor="ct-message">Message</label>
      <textarea id="ct-message" name="message" rows={5} required disabled={isPending} />

      <button type="submit" disabled={isPending} aria-busy={isPending}>
        {isPending ? 'Sending…' : 'Send message'}
      </button>
    </form>
  );
}''',
    ),

    ex(
        "Use useActionState to build a multi-step wizard form (step 1: name/email, step 2: address, step 3: confirmation).",
        '''\
'use client';

import { useActionState } from 'react';

type Step = 1 | 2 | 3;
type WizardState = {
  step: Step;
  data: { name: string; email: string; address: string; city: string };
  error: string | null;
};

const INITIAL: WizardState = { step: 1, data: { name: '', email: '', address: '', city: '' }, error: null };

async function wizardAction(prev: WizardState, formData: FormData): Promise<WizardState> {
  if (prev.step === 1) {
    const name = formData.get('name') as string;
    const email = formData.get('email') as string;
    if (!name || !email) return { ...prev, error: 'Name and email are required.' };
    return { step: 2, data: { ...prev.data, name, email }, error: null };
  }
  if (prev.step === 2) {
    const address = formData.get('address') as string;
    const city = formData.get('city') as string;
    if (!address || !city) return { ...prev, error: 'Address and city are required.' };
    return { step: 3, data: { ...prev.data, address, city }, error: null };
  }
  await fetch('/api/submit', {
    method: 'POST',
    body: JSON.stringify(prev.data),
    headers: { 'Content-Type': 'application/json' },
  });
  return { ...prev, step: 3, error: null };
}

export default function WizardForm() {
  const [state, dispatch, isPending] = useActionState(wizardAction, INITIAL);

  return (
    <div>
      <p aria-live="polite">Step {state.step} of 3</p>
      {state.error && <p role="alert">{state.error}</p>}

      <form action={dispatch}>
        {state.step === 1 && (
          <>
            <label htmlFor="wz-name">Name</label>
            <input id="wz-name" name="name" defaultValue={state.data.name} required />
            <label htmlFor="wz-email">Email</label>
            <input id="wz-email" name="email" type="email" defaultValue={state.data.email} required />
          </>
        )}
        {state.step === 2 && (
          <>
            <label htmlFor="wz-addr">Address</label>
            <input id="wz-addr" name="address" defaultValue={state.data.address} required />
            <label htmlFor="wz-city">City</label>
            <input id="wz-city" name="city" defaultValue={state.data.city} required />
          </>
        )}
        {state.step === 3 && (
          <dl>
            <dt>Name</dt><dd>{state.data.name}</dd>
            <dt>Email</dt><dd>{state.data.email}</dd>
            <dt>Address</dt><dd>{state.data.address}, {state.data.city}</dd>
          </dl>
        )}
        <button type="submit" disabled={isPending} aria-busy={isPending}>
          {state.step < 3 ? 'Next' : 'Confirm & Submit'}
        </button>
      </form>
    </div>
  );
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # REACT 19 — useFormStatus
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Create a reusable SubmitButton component using useFormStatus that shows a spinner when the form is submitting.",
        '''\
'use client';

import { useFormStatus } from 'react-dom';

interface SubmitButtonProps {
  label: string;
  pendingLabel: string;
}

export function SubmitButton({ label, pendingLabel }: SubmitButtonProps) {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending} aria-busy={pending}>
      {pending ? (
        <>
          <span aria-hidden="true" className="spinner" />
          <span>{pendingLabel}</span>
        </>
      ) : (
        label
      )}
    </button>
  );
}''',
    ),

    ex(
        "Use useFormStatus to disable all form inputs while the form action is executing.",
        '''\
'use client';

import { useFormStatus } from 'react-dom';
import { useActionState } from 'react';

function FormFields() {
  const { pending } = useFormStatus();
  return (
    <>
      <label htmlFor="fs-name">Name</label>
      <input id="fs-name" name="name" required disabled={pending} />
      <label htmlFor="fs-email">Email</label>
      <input id="fs-email" name="email" type="email" required disabled={pending} />
      <label htmlFor="fs-msg">Message</label>
      <textarea id="fs-msg" name="message" rows={4} required disabled={pending} />
      <button type="submit" disabled={pending} aria-busy={pending}>
        {pending ? 'Submitting…' : 'Submit'}
      </button>
    </>
  );
}

type State = { ok: boolean; error: string | null };

async function submitAction(_prev: State, formData: FormData): Promise<State> {
  await fetch('/api/contact', { method: 'POST', body: formData });
  return { ok: true, error: null };
}

export default function ContactFormWithStatus() {
  const [state, dispatch] = useActionState(submitAction, { ok: false, error: null });
  return (
    <form action={dispatch} aria-label="Contact">
      {state.ok && <p role="status">Sent successfully!</p>}
      <FormFields />
    </form>
  );
}''',
    ),

    ex(
        "Build a form that shows an animated progress bar at the top using useFormStatus while submitting.",
        '''\
'use client';

import { useFormStatus } from 'react-dom';
import { useActionState } from 'react';

function ProgressBar() {
  const { pending } = useFormStatus();
  if (!pending) return null;
  return (
    <div
      role="progressbar"
      aria-label="Submitting…"
      aria-busy="true"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        height: '3px',
        background: '#0070f3',
        animation: 'progress 1.5s ease-in-out infinite',
        width: '100%',
      }}
    />
  );
}

type State = { success: boolean };

async function saveAction(_prev: State, formData: FormData): Promise<State> {
  const title = formData.get('title') as string;
  await fetch('/api/posts', {
    method: 'POST',
    body: JSON.stringify({ title }),
    headers: { 'Content-Type': 'application/json' },
  });
  return { success: true };
}

export default function PostForm() {
  const [state, dispatch] = useActionState(saveAction, { success: false });
  return (
    <form action={dispatch}>
      <ProgressBar />
      {state.success && <p role="status">Post saved!</p>}
      <label htmlFor="pf-title">Title</label>
      <input id="pf-title" name="title" required />
      <button type="submit">Save post</button>
    </form>
  );
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # REACT 19 — use() API
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Use the React 19 use() hook to read a user profile promise passed from a Server Component, wrapped in Suspense.",
        '''\
// server-component (app/users/[id]/page.tsx)
import { Suspense } from 'react';
import { UserProfile } from './UserProfile';

interface User {
  id: string;
  name: string;
  email: string;
  avatarUrl: string;
}

async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error('User not found');
  return res.json() as Promise<User>;
}

export default function UserPage({ params }: { params: { id: string } }) {
  const userPromise = fetchUser(params.id);
  return (
    <Suspense fallback={<p>Loading profile…</p>}>
      <UserProfile promise={userPromise} />
    </Suspense>
  );
}

// UserProfile.tsx — client component
'use client';

import { use } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  avatarUrl: string;
}

interface UserProfileProps {
  promise: Promise<User>;
}

export function UserProfile({ promise }: UserProfileProps) {
  const user = use(promise);
  return (
    <article>
      <img src={user.avatarUrl} alt={`${user.name} avatar`} width={80} height={80} />
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </article>
  );
}''',
    ),

    ex(
        "Use React 19's use() to conditionally read a theme context only when a dark-mode prop is set.",
        '''\
'use client';

import { use, createContext, type ReactNode } from 'react';

interface Theme {
  background: string;
  foreground: string;
  accent: string;
}

const LIGHT: Theme = { background: '#fff', foreground: '#111', accent: '#0070f3' };
const DARK: Theme = { background: '#111', foreground: '#f5f5f5', accent: '#60a5fa' };

export const ThemeContext = createContext<Theme>(LIGHT);

interface CardProps {
  title: string;
  children: ReactNode;
  useDarkTheme?: boolean;
}

export function Card({ title, children, useDarkTheme = false }: CardProps) {
  const theme = useDarkTheme ? use(ThemeContext) : LIGHT;
  return (
    <div
      style={{
        background: useDarkTheme ? DARK.background : theme.background,
        color: useDarkTheme ? DARK.foreground : theme.foreground,
        padding: '1rem',
        borderRadius: '8px',
      }}
    >
      <h2>{title}</h2>
      {children}
    </div>
  );
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # SERVER ACTIONS
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Write a React Server Action that adds an item to a shopping cart and revalidates the cart page.",
        '''\
// actions/cart.ts
'use server';


interface CartItem {
  productId: string;
  quantity: number;
}

export async function addToCart(sessionId: string, productId: string, quantity: number = 1): Promise<void> {
  if (!sessionId) throw new Error('No session');

  await fetch(`${process.env.API_URL}/cart/${sessionId}/items`, {
    method: 'POST',
    body: JSON.stringify({ productId, quantity } satisfies CartItem),
    headers: { 'Content-Type': 'application/json' },
  });

  // // // // revalidatePath('/cart');
}

// components/AddToCartButton.tsx
'use client';

import { useTransition } from 'react';
import { addToCart } from '@/actions/cart';

interface AddToCartButtonProps {
  productId: string;
}

export function AddToCartButton({ productId }: AddToCartButtonProps) {
  const [isPending, startTransition] = useTransition();

  function handleClick() {
    startTransition(() => {
      addToCart(productId);
    });
  }

  return (
    <button onClick={handleClick} disabled={isPending} aria-busy={isPending}>
      {isPending ? 'Adding…' : 'Add to cart'}
    </button>
  );
}''',
    ),

    ex(
        "Implement a Server Action with optimistic UI using useOptimistic to instantly toggle a post like.",
        '''\
'use client';

import { useOptimistic, useTransition } from 'react';
import { toggleLike } from '@/actions/likes';

interface LikeButtonProps {
  postId: string;
  initialLiked: boolean;
  initialCount: number;
}

export function LikeButton({ postId, initialLiked, initialCount }: LikeButtonProps) {
  const [isPending, startTransition] = useTransition();
  const [optimisticState, setOptimistic] = useOptimistic(
    { liked: initialLiked, count: initialCount },
    (current, action: 'toggle') => {
      if (action === 'toggle') {
        return { liked: !current.liked, count: current.liked ? current.count - 1 : current.count + 1 };
      }
      return current;
    },
  );

  function handleClick() {
    startTransition(async () => {
      setOptimistic('toggle');
      await toggleLike(postId);
    });
  }

  return (
    <button
      onClick={handleClick}
      disabled={isPending}
      aria-pressed={optimisticState.liked}
      aria-label={`${optimisticState.liked ? 'Unlike' : 'Like'} post. ${optimisticState.count} likes.`}
    >
      {optimisticState.liked ? '❤️' : '🤍'} {optimisticState.count}
    </button>
  );
}

// actions/likes.ts
'use server';


export async function toggleLike(postId: string): Promise<void> {
  await fetch(`${process.env.API_URL}/posts/${postId}/like`, { method: 'POST' });
  // // // // revalidatePath('/posts');
}''',
    ),

    ex(
        "Create a Server Action that deletes a post, with a client-side confirmation dialog before executing.",
        '''\
// actions/posts.ts
'use server';


export async function deletePost(postId: string): Promise<void> {
  const res = await fetch(`${process.env.API_URL}/posts/${postId}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete post');
  // // // // revalidatePath('/posts');
  // // // // redirect('/posts');
}

// components/DeletePostButton.tsx
'use client';

import { useTransition } from 'react';
import { deletePost } from '@/actions/posts';

interface DeletePostButtonProps {
  postId: string;
  postTitle: string;
}

export function DeletePostButton({ postId, postTitle }: DeletePostButtonProps) {
  const [isPending, startTransition] = useTransition();

  function handleDelete() {
    if (!confirm(`Delete "${postTitle}"? This cannot be undone.`)) return;
    startTransition(() => {
      deletePost(postId);
    });
  }

  return (
    <button
      onClick={handleDelete}
      disabled={isPending}
      aria-busy={isPending}
    >
      {isPending ? 'Deleting…' : 'Delete post'}
    </button>
  );
}''',
    ),

    ex(
        "Write a React Server Action that creates a new todo item with Zod validation.",
        '''\
// actions/todos.ts
'use server';

import { z } from 'zod';

const CreateTodoSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title too long'),
  priority: z.enum(['low', 'medium', 'high']),
});

type CreateTodoResult = { success: true } | { success: false; errors: Record<string, string> };

export async function createTodo(formData: FormData): Promise<CreateTodoResult> {
  const parsed = CreateTodoSchema.safeParse({
    title: formData.get('title'),
    priority: formData.get('priority'),
  });

  if (!parsed.success) {
    const errors: Record<string, string> = {};
    for (const [field, msgs] of Object.entries(parsed.error.flatten().fieldErrors)) {
      errors[field] = (msgs as string[])[0];
    }
    return { success: false, errors };
  }

  await fetch(`${process.env.API_URL}/todos`, {
    method: 'POST',
    body: JSON.stringify(parsed.data),
    headers: { 'Content-Type': 'application/json' },
  });

  // // // // revalidatePath('/todos');
  return { success: true };
}

// components/CreateTodoForm.tsx
'use client';

import { useActionState } from 'react';
import { createTodo } from '@/actions/todos';

type State = { success: boolean; errors: Record<string, string> };

async function action(prev: State, formData: FormData): Promise<State> {
  const result = await createTodo(formData);
  return result.success ? { success: true, errors: {} } : { success: false, errors: result.errors };
}

export default function CreateTodoForm() {
  const [state, dispatch, isPending] = useActionState(action, { success: false, errors: {} });

  return (
    <form action={dispatch}>
      {state.success && <p role="status">Todo created!</p>}

      <label htmlFor="todo-title">Title</label>
      <input id="todo-title" name="title" required disabled={isPending}
        aria-describedby={state.errors.title ? 'title-err' : undefined} />
      {state.errors.title && <span id="title-err" role="alert">{state.errors.title}</span>}

      <label htmlFor="todo-priority">Priority</label>
      <select id="todo-priority" name="priority" disabled={isPending}>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
      {state.errors.priority && <span role="alert">{state.errors.priority}</span>}

      <button type="submit" disabled={isPending} aria-busy={isPending}>
        {isPending ? 'Creating…' : 'Create todo'}
      </button>
    </form>
  );
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # SERVER COMPONENTS
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Create a React Server Component page that fetches and displays a list of users with search from URL params.",
        '''\
// users/page.tsx
import { Suspense } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
  createdAt: string;
}

async function getUsers(search: string): Promise<User[]> {
  const url = new URL(`${process.env.API_URL}/users`);
  if (search) url.searchParams.set('q', search);
  const res = await fetch(url.toString());
  if (!res.ok) throw new Error('Failed to fetch users');
  return res.json() as Promise<User[]>;
}

function UserRow({ user }: { user: User }) {
  return (
    <tr>
      <td>{user.name}</td>
      <td>{user.email}</td>
      <td>
        <span aria-label={`Role: ${user.role}`}>{user.role}</span>
      </td>
      <td>{new Date(user.createdAt).toLocaleDateString()}</td>
    </tr>
  );
}

async function UsersTable({ search }: { search: string }) {
  const users = await getUsers(search);
  if (users.length === 0) return <p>No users found.</p>;
  return (
    <table>
      <caption>Users{search ? ` matching "${search}"` : ''}</caption>
      <thead>
        <tr>
          <th scope="col">Name</th>
          <th scope="col">Email</th>
          <th scope="col">Role</th>
          <th scope="col">Joined</th>
        </tr>
      </thead>
      <tbody>
        {users.map((u) => <UserRow key={u.id} user={u} />)}
      </tbody>
    </table>
  );
}

interface PageProps {
  searchParams: { q?: string };
}

export default function UsersPage({ searchParams }: PageProps) {
  const search = searchParams.q ?? '';
  return (
    <main>
      <h1>Users</h1>
      <form method="get" role="search">
        <label htmlFor="user-search">Search users</label>
        <input id="user-search" name="q" type="search" defaultValue={search} />
        <button type="submit">Search</button>
      </form>
      <Suspense fallback={<p aria-live="polite">Loading users…</p>} key={search}>
        <UsersTable search={search} />
      </Suspense>
    </main>
  );
}''',
    ),

    ex(
        "Build a Server Component blog post listing page with pagination using searchParams.",
        '''\
// blog/page.tsx

const PAGE_SIZE = 10;

interface Post {
  id: string;
  slug: string;
  title: string;
  excerpt: string;
  author: string;
  publishedAt: string;
}

interface PostsResponse {
  posts: Post[];
  total: number;
}

async function getPosts(page: number): Promise<PostsResponse> {
  const res = await fetch(
    `${process.env.API_URL}/posts?page=${page}&limit=${PAGE_SIZE}`,
  );
  if (!res.ok) throw new Error('Failed to load posts');
  return res.json() as Promise<PostsResponse>;
}

interface PageProps {
  searchParams: { page?: string };
}

export default async function BlogPage({ searchParams }: PageProps) {
  const page = Math.max(1, Number(searchParams.page ?? 1));
  const { posts, total } = await getPosts(page);
  const totalPages = Math.ceil(total / PAGE_SIZE);

  return (
    <main>
      <h1>Blog</h1>
      <ol aria-label="Blog posts" style={{ listStyle: 'none', padding: 0 }}>
        {posts.map((post) => (
          <li key={post.id}>
            <article>
              <h2>
                <a href={`/blog/${post.slug}`}>{post.title}</a>
              </h2>
              <p>{post.excerpt}</p>
              <footer>
                <span>By {post.author}</span>
                <time dateTime={post.publishedAt}>
                  {new Date(post.publishedAt).toLocaleDateString()}
                </time>
              </footer>
            </article>
          </li>
        ))}
      </ol>

      <nav aria-label="Pagination">
        {page > 1 && <a href={`/blog?page=${page - 1}`}>Previous</a>}
        <span aria-current="page">Page {page} of {totalPages}</span>
        {page < totalPages && <a href={`/blog?page=${page + 1}`}>Next</a>}
      </nav>
    </main>
  );
}''',
    ),

    ex(
        "Create a dashboard Server Component that fetches multiple data sources in parallel.",
        '''\
// dashboard/page.tsx
interface Stats {
  totalUsers: number;
  activeUsers: number;
  revenue: number;
  orders: number;
}
interface RecentOrder {
  id: string;
  customer: string;
  amount: number;
  status: 'pending' | 'shipped' | 'delivered';
}

async function fetchStats(): Promise<Stats> {
  const res = await fetch(`${process.env.API_URL}/stats`);
  return res.json() as Promise<Stats>;
}

async function fetchRecentOrders(): Promise<RecentOrder[]> {
  const res = await fetch(`${process.env.API_URL}/orders?limit=5`);
  return res.json() as Promise<RecentOrder[]>;
}

function StatCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div role="region" aria-label={label}>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  );
}

export default async function DashboardPage() {
  const [stats, orders] = await Promise.all([fetchStats(), fetchRecentOrders()]);

  return (
    <main>
      <h1>Dashboard</h1>

      <section aria-label="Key metrics">
        <dl>
          <StatCard label="Total users" value={stats.totalUsers.toLocaleString()} />
          <StatCard label="Active users" value={stats.activeUsers.toLocaleString()} />
          <StatCard label="Revenue" value={`$${stats.revenue.toLocaleString()}`} />
          <StatCard label="Orders" value={stats.orders.toLocaleString()} />
        </dl>
      </section>

      <section aria-label="Recent orders">
        <h2>Recent Orders</h2>
        <table>
          <thead>
            <tr>
              <th scope="col">Order</th>
              <th scope="col">Customer</th>
              <th scope="col">Amount</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td>#{order.id}</td>
                <td>{order.customer}</td>
                <td>${order.amount.toFixed(2)}</td>
                <td>{order.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}''',
    ),

    ex(
        "When should I use a Server Component vs a Client Component? Give examples of both.",
        '''\
// SERVER COMPONENT — no interactivity, fetches data directly, no "use client"
// products/page.tsx
interface Product {
  id: string;
  name: string;
  price: number;
}

async function getProducts(): Promise<Product[]> {
  const res = await fetch(`${process.env.API_URL}/products`);
  return res.json() as Promise<Product[]>;
}

// Server Component: renders on the server, can be async, has zero JS sent to client
export default async function ProductsPage() {
  const products = await getProducts();
  return (
    <ul>
      {products.map((p) => (
        <li key={p.id}>{p.name} — ${p.price}</li>
      ))}
    </ul>
  );
}

// ─────────────────────────────────────────────────────────────────────────────

// CLIENT COMPONENT — needs interactivity (useState, event handlers, browser APIs)
// components/AddToCartButton.tsx
'use client';

import { useState } from 'react';

interface AddToCartButtonProps {
  productId: string;
}

// Client Component: adds interactivity, runs in the browser
export function AddToCartButton({ productId }: AddToCartButtonProps) {
  const [added, setAdded] = useState(false);

  async function handleClick() {
    await fetch('/api/cart', {
      method: 'POST',
      body: JSON.stringify({ productId }),
      headers: { 'Content-Type': 'application/json' },
    });
    setAdded(true);
  }

  return (
    <button onClick={handleClick} disabled={added}>
      {added ? 'Added ✓' : 'Add to cart'}
    </button>
  );
}

// RULE OF THUMB:
// Server Component  → data fetching, layouts, static content, heavy imports (markdown parsers, etc.)
// Client Component  → useState, useEffect, event handlers, browser APIs (localStorage, geolocation)
// Compose them: Server Component renders content + passes data to Client Components for interactivity''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # CLIENT COMPONENTS
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Build an accessible tabs component using TypeScript, keyboard navigation (arrow keys), and proper ARIA roles.",
        '''\
'use client';

import { useState, useRef, type KeyboardEvent } from 'react';

interface Tab {
  id: string;
  label: string;
  content: React.ReactNode;
}

interface TabsProps {
  tabs: Tab[];
  defaultTab?: string;
}

export function Tabs({ tabs, defaultTab }: TabsProps) {
  const [activeId, setActiveId] = useState(defaultTab ?? tabs[0]?.id ?? '');
  const tabRefs = useRef<Map<string, HTMLButtonElement>>(new Map());

  function handleKeyDown(e: KeyboardEvent<HTMLDivElement>) {
    const ids = tabs.map((t) => t.id);
    const currentIdx = ids.indexOf(activeId);

    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
      e.preventDefault();
      const next = ids[(currentIdx + 1) % ids.length];
      setActiveId(next);
      tabRefs.current.get(next)?.focus();
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault();
      const prev = ids[(currentIdx - 1 + ids.length) % ids.length];
      setActiveId(prev);
      tabRefs.current.get(prev)?.focus();
    } else if (e.key === 'Home') {
      e.preventDefault();
      setActiveId(ids[0]);
      tabRefs.current.get(ids[0])?.focus();
    } else if (e.key === 'End') {
      e.preventDefault();
      const last = ids[ids.length - 1];
      setActiveId(last);
      tabRefs.current.get(last)?.focus();
    }
  }

  return (
    <div>
      <div role="tablist" onKeyDown={handleKeyDown} aria-label="Tabs">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            role="tab"
            id={`tab-${tab.id}`}
            aria-selected={activeId === tab.id}
            aria-controls={`panel-${tab.id}`}
            tabIndex={activeId === tab.id ? 0 : -1}
            ref={(el) => { if (el) tabRefs.current.set(tab.id, el); }}
            onClick={() => setActiveId(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      {tabs.map((tab) => (
        <div
          key={tab.id}
          role="tabpanel"
          id={`panel-${tab.id}`}
          aria-labelledby={`tab-${tab.id}`}
          hidden={activeId !== tab.id}
          tabIndex={0}
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
}''',
    ),

    ex(
        "Create an accessible modal dialog component with focus trapping and close on Escape.",
        '''\
'use client';

import { useEffect, useRef, type ReactNode } from 'react';
import { createPortal } from 'react-dom';

const FOCUSABLE = 'a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<Element | null>(null);

  useEffect(() => {
    if (!isOpen) return;
    previousFocusRef.current = document.activeElement;
    const firstFocusable = dialogRef.current?.querySelectorAll<HTMLElement>(FOCUSABLE)?.[0];
    firstFocusable?.focus();

    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') { onClose(); return; }
      if (e.key !== 'Tab') return;
      const focusable = dialogRef.current?.querySelectorAll<HTMLElement>(FOCUSABLE);
      if (!focusable || focusable.length === 0) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }

    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      (previousFocusRef.current as HTMLElement | null)?.focus();
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return createPortal(
    <div role="presentation" style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)' }}
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        style={{ background: '#fff', borderRadius: 8, padding: '1.5rem', maxWidth: 480, margin: '10vh auto' }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 id="modal-title">{title}</h2>
          <button onClick={onClose} aria-label="Close dialog">✕</button>
        </div>
        {children}
      </div>
    </div>,
    document.body,
  );
}''',
    ),

    ex(
        "Build a search input with debounce (300ms) that calls an onSearch callback.",
        '''\
'use client';

import { useState, useEffect, useCallback } from 'react';

interface SearchInputProps {
  onSearch: (query: string) => void;
  placeholder?: string;
  debounceMs?: number;
}

export function SearchInput({ onSearch, placeholder = 'Search…', debounceMs = 300 }: SearchInputProps) {
  const [value, setValue] = useState('');

  useEffect(() => {
    const id = setTimeout(() => onSearch(value.trim()), debounceMs);
    return () => clearTimeout(id);
  }, [value, debounceMs, onSearch]);

  const handleClear = useCallback(() => {
    setValue('');
    onSearch('');
  }, [onSearch]);

  return (
    <div role="search" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <label htmlFor="search-input" className="sr-only">Search</label>
      <input
        id="search-input"
        type="search"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={placeholder}
        aria-label={placeholder}
      />
      {value && (
        <button type="button" onClick={handleClear} aria-label="Clear search">✕</button>
      )}
    </div>
  );
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # PERFORMANCE — useMemo
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Optimize a large product list component with filter and sort using useMemo.",
        '''\
'use client';

import { useState, useMemo } from 'react';

interface Product {
  id: string;
  name: string;
  price: number;
  category: string;
  rating: number;
}

type SortKey = 'name' | 'price' | 'rating';

interface ProductListProps {
  products: Product[];
}

export function ProductList({ products }: ProductListProps) {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [sortKey, setSortKey] = useState<SortKey>('name');

  const categories = useMemo(
    () => ['', ...Array.from(new Set(products.map((p) => p.category))).sort()],
    [products],
  );

  const filtered = useMemo(() => {
    const q = search.toLowerCase();
    return products
      .filter((p) => (!q || p.name.toLowerCase().includes(q)) && (!category || p.category === category))
      .sort((a, b) => {
        if (sortKey === 'price' || sortKey === 'rating') return b[sortKey] - a[sortKey];
        return a.name.localeCompare(b.name);
      });
  }, [products, search, category, sortKey]);

  return (
    <div>
      <div role="toolbar" aria-label="Filter and sort">
        <label htmlFor="pl-search">Search</label>
        <input id="pl-search" type="search" value={search} onChange={(e) => setSearch(e.target.value)} />

        <label htmlFor="pl-category">Category</label>
        <select id="pl-category" value={category} onChange={(e) => setCategory(e.target.value)}>
          {categories.map((c) => <option key={c} value={c}>{c || 'All categories'}</option>)}
        </select>

        <label htmlFor="pl-sort">Sort by</label>
        <select id="pl-sort" value={sortKey} onChange={(e) => setSortKey(e.target.value as SortKey)}>
          <option value="name">Name</option>
          <option value="price">Price</option>
          <option value="rating">Rating</option>
        </select>
      </div>

      <p aria-live="polite">{filtered.length} product{filtered.length !== 1 ? 's' : ''} found</p>

      <ul aria-label="Product results">
        {filtered.map((p) => (
          <li key={p.id}>
            <strong>{p.name}</strong> — ${p.price.toFixed(2)} — ★{p.rating}
          </li>
        ))}
      </ul>
    </div>
  );
}''',
    ),

    ex(
        "Use useMemo to transform a flat list of employees into a department tree for a hierarchy view.",
        '''\
'use client';

import { useMemo } from 'react';

interface Employee {
  id: string;
  name: string;
  department: string;
  role: string;
}

interface DepartmentGroup {
  department: string;
  employees: Employee[];
}

function groupByDepartment(employees: Employee[]): DepartmentGroup[] {
  const map = new Map<string, Employee[]>();
  for (const emp of employees) {
    const list = map.get(emp.department) ?? [];
    list.push(emp);
    map.set(emp.department, list);
  }
  return Array.from(map.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([department, emps]) => ({ department, employees: emps }));
}

interface OrgChartProps {
  employees: Employee[];
}

export function OrgChart({ employees }: OrgChartProps) {
  const tree = useMemo(() => groupByDepartment(employees), [employees]);

  return (
    <div>
      {tree.map(({ department, employees: emps }) => (
        <section key={department} aria-label={`${department} department`}>
          <h2>{department} <span>({emps.length})</span></h2>
          <ul>
            {emps.map((e) => (
              <li key={e.id}>
                <span>{e.name}</span> — <span>{e.role}</span>
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # PERFORMANCE — useCallback
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Build a data table with sortable columns using useCallback to memoize the sort handler.",
        '''\
'use client';

import { useState, useCallback, useMemo } from 'react';

interface Column<T> {
  key: keyof T;
  label: string;
  sortable?: boolean;
}

interface DataTableProps<T extends Record<string, unknown>> {
  data: T[];
  columns: Column<T>[];
  keyField: keyof T;
}

type SortDir = 'asc' | 'desc';

export function DataTable<T extends Record<string, unknown>>({ data, columns, keyField }: DataTableProps<T>) {
  const [sortKey, setSortKey] = useState<keyof T | null>(null);
  const [sortDir, setSortDir] = useState<SortDir>('asc');

  const handleSort = useCallback((key: keyof T) => {
    setSortKey((prev) => {
      if (prev === key) {
        setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'));
        return prev;
      }
      setSortDir('asc');
      return key;
    });
  }, []);

  const sorted = useMemo(() => {
    if (!sortKey) return data;
    return [...data].sort((a, b) => {
      const av = a[sortKey];
      const bv = b[sortKey];
      const cmp = typeof av === 'string' && typeof bv === 'string'
        ? av.localeCompare(bv)
        : Number(av) - Number(bv);
      return sortDir === 'asc' ? cmp : -cmp;
    });
  }, [data, sortKey, sortDir]);

  return (
    <table>
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={String(col.key)} scope="col"
              aria-sort={sortKey === col.key ? (sortDir === 'asc' ? 'ascending' : 'descending') : 'none'}>
              {col.sortable ? (
                <button type="button" onClick={() => handleSort(col.key)}>
                  {col.label} {sortKey === col.key ? (sortDir === 'asc' ? '↑' : '↓') : '↕'}
                </button>
              ) : col.label}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {sorted.map((row) => (
          <tr key={String(row[keyField])}>
            {columns.map((col) => <td key={String(col.key)}>{String(row[col.key])}</td>)}
          </tr>
        ))}
      </tbody>
    </table>
  );
}''',
    ),

    ex(
        "Implement a debounced search with useCallback so the function reference stays stable across renders.",
        '''\
'use client';

import { useState, useCallback, useEffect, useRef } from 'react';

interface SearchResult {
  id: string;
  title: string;
}

async function searchApi(query: string): Promise<SearchResult[]> {
  const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
  return res.json() as Promise<SearchResult[]>;
}

export function LiveSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const debouncedSearch = useCallback((q: string) => {
    if (timerRef.current) clearTimeout(timerRef.current);
    if (!q.trim()) { setResults([]); return; }
    timerRef.current = setTimeout(async () => {
      setIsLoading(true);
      try {
        const data = await searchApi(q);
        setResults(data);
      } finally {
        setIsLoading(false);
      }
    }, 300);
  }, []);

  useEffect(() => {
    debouncedSearch(query);
    return () => { if (timerRef.current) clearTimeout(timerRef.current); };
  }, [query, debouncedSearch]);

  return (
    <div>
      <label htmlFor="live-search">Search</label>
      <input
        id="live-search"
        type="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        aria-controls="live-search-results"
        aria-expanded={results.length > 0}
      />
      {isLoading && <span aria-live="polite">Searching…</span>}
      <ul id="live-search-results" role="listbox" aria-label="Search results">
        {results.map((r) => (
          <li key={r.id} role="option">{r.title}</li>
        ))}
      </ul>
    </div>
  );
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # PERFORMANCE — React.memo
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Create a memoized ProductCard component that prevents re-renders when parent state changes unrelated data.",
        '''\
'use client';

import { memo } from 'react';

interface Product {
  id: string;
  name: string;
  price: number;
  imageUrl: string;
  category: string;
  rating: number;
  reviewCount: number;
}

interface ProductCardProps {
  product: Product;
  onAddToCart: (id: string) => void;
}

export const ProductCard = memo(function ProductCard({ product, onAddToCart }: ProductCardProps) {
  return (
    <article aria-label={product.name}>
      <img src={product.imageUrl} alt={product.name} width={200} height={200} loading="lazy" />
      <div>
        <h3>{product.name}</h3>
        <p>{product.category}</p>
        <p>
          <span aria-label={`Rating: ${product.rating} out of 5`}>
            {'★'.repeat(Math.round(product.rating))}
          </span>
          <span>({product.reviewCount})</span>
        </p>
        <p aria-label={`Price: $${product.price.toFixed(2)}`}>${product.price.toFixed(2)}</p>
        <button
          type="button"
          onClick={() => onAddToCart(product.id)}
          aria-label={`Add ${product.name} to cart`}
        >
          Add to cart
        </button>
      </div>
    </article>
  );
});''',
    ),

    ex(
        "Build a memoized CommentItem that only re-renders when its own data changes, not when siblings update.",
        '''\
'use client';

import { memo } from 'react';

interface Comment {
  id: string;
  author: string;
  avatarUrl: string;
  body: string;
  createdAt: string;
  likeCount: number;
}

interface CommentItemProps {
  comment: Comment;
  onLike: (id: string) => void;
  onDelete: (id: string) => void;
  currentUserId: string;
}

export const CommentItem = memo(
  function CommentItem({ comment, onLike, onDelete, currentUserId }: CommentItemProps) {
    const isOwner = comment.author === currentUserId;
    return (
      <article aria-label={`Comment by ${comment.author}`}>
        <header>
          <img src={comment.avatarUrl} alt="" aria-hidden="true" width={32} height={32} />
          <strong>{comment.author}</strong>
          <time dateTime={comment.createdAt}>
            {new Date(comment.createdAt).toLocaleDateString()}
          </time>
        </header>
        <p>{comment.body}</p>
        <footer>
          <button
            type="button"
            onClick={() => onLike(comment.id)}
            aria-label={`Like comment by ${comment.author}. ${comment.likeCount} likes.`}
          >
            ♥ {comment.likeCount}
          </button>
          {isOwner && (
            <button
              type="button"
              onClick={() => onDelete(comment.id)}
              aria-label="Delete comment"
            >
              Delete
            </button>
          )}
        </footer>
      </article>
    );
  },
  (prev, next) =>
    prev.comment === next.comment &&
    prev.onLike === next.onLike &&
    prev.onDelete === next.onDelete &&
    prev.currentUserId === next.currentUserId,
);''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # PERFORMANCE — Suspense & lazy()
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Lazy load a heavy chart component using React.lazy and Suspense with a skeleton fallback.",
        '''\
'use client';

import { lazy, Suspense } from 'react';

const SalesChart = lazy(() => import('./SalesChart'));

interface ChartData {
  month: string;
  revenue: number;
}

function ChartSkeleton() {
  return (
    <div
      aria-hidden="true"
      style={{ width: '100%', height: 300, background: '#e5e7eb', borderRadius: 8, animation: 'pulse 2s infinite' }}
    />
  );
}

interface SalesChartPanelProps {
  data: ChartData[];
}

export function SalesChartPanel({ data }: SalesChartPanelProps) {
  return (
    <section aria-label="Sales chart">
      <h2>Revenue Overview</h2>
      <Suspense fallback={<ChartSkeleton />}>
        <SalesChart data={data} />
      </Suspense>
    </section>
  );
}''',
    ),

    ex(
        "Create a tabs component where each tab panel is lazy-loaded only when first selected.",
        '''\
'use client';

import { lazy, Suspense, useState } from 'react';

const OverviewPanel = lazy(() => import('./panels/OverviewPanel'));
const AnalyticsPanel = lazy(() => import('./panels/AnalyticsPanel'));
const SettingsPanel = lazy(() => import('./panels/SettingsPanel'));

type TabId = 'overview' | 'analytics' | 'settings';

const TABS: { id: TabId; label: string }[] = [
  { id: 'overview', label: 'Overview' },
  { id: 'analytics', label: 'Analytics' },
  { id: 'settings', label: 'Settings' },
];

function PanelSkeleton() {
  return <div aria-busy="true" aria-label="Loading panel…" style={{ padding: '2rem', textAlign: 'center' }}>Loading…</div>;
}

export function LazyTabs() {
  const [active, setActive] = useState<TabId>('overview');
  const [loaded, setLoaded] = useState<Set<TabId>>(new Set(['overview']));

  function selectTab(id: TabId) {
    setActive(id);
    setLoaded((prev) => new Set([...prev, id]));
  }

  return (
    <div>
      <div role="tablist">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            role="tab"
            id={`tab-${tab.id}`}
            aria-selected={active === tab.id}
            aria-controls={`panel-${tab.id}`}
            onClick={() => selectTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      {loaded.has('overview') && (
        <div role="tabpanel" id="panel-overview" aria-labelledby="tab-overview" hidden={active !== 'overview'}>
          <Suspense fallback={<PanelSkeleton />}><OverviewPanel /></Suspense>
        </div>
      )}
      {loaded.has('analytics') && (
        <div role="tabpanel" id="panel-analytics" aria-labelledby="tab-analytics" hidden={active !== 'analytics'}>
          <Suspense fallback={<PanelSkeleton />}><AnalyticsPanel /></Suspense>
        </div>
      )}
      {loaded.has('settings') && (
        <div role="tabpanel" id="panel-settings" aria-labelledby="tab-settings" hidden={active !== 'settings'}>
          <Suspense fallback={<PanelSkeleton />}><SettingsPanel /></Suspense>
        </div>
      )}
    </div>
  );
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # ACCESSIBILITY
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Add a skip-to-main-content link for keyboard and screen reader users at the top of the layout.",
        '''\
// layout.tsx
import type { ReactNode } from 'react';

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <a
          href="#main-content"
          style={{
            position: 'absolute',
            left: '-9999px',
            top: 'auto',
            width: 1,
            height: 1,
            overflow: 'hidden',
          }}
          onFocus={(e) => {
            const el = e.currentTarget;
            el.style.position = 'static';
            el.style.width = 'auto';
            el.style.height = 'auto';
            el.style.overflow = 'visible';
          }}
          onBlur={(e) => {
            const el = e.currentTarget;
            el.style.position = 'absolute';
            el.style.left = '-9999px';
            el.style.width = '1px';
            el.style.height = '1px';
            el.style.overflow = 'hidden';
          }}
        >
          Skip to main content
        </a>
        <header>
          <nav aria-label="Primary navigation">{/* nav items */}</nav>
        </header>
        <main id="main-content" tabIndex={-1}>
          {children}
        </main>
      </body>
    </html>
  );
}''',
    ),

    ex(
        "Create an ARIA live region notification system (toasts) that announces messages to screen readers.",
        '''\
'use client';

import { useState, useCallback, createContext, useContext, type ReactNode } from 'react';

interface Toast {
  id: number;
  message: string;
  type: 'success' | 'error' | 'info';
}

interface ToastContextValue {
  addToast: (message: string, type?: Toast['type']) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((message: string, type: Toast['type'] = 'info') => {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => setToasts((prev) => prev.filter((t) => t.id !== id)), 5000);
  }, []);

  return (
    <ToastContext.Provider value={{ addToast }}>
      {children}
      {/* aria-live region: always in the DOM so screen readers register it early */}
      <div
        aria-live="polite"
        aria-atomic="true"
        aria-relevant="additions"
        style={{ position: 'fixed', bottom: '1rem', right: '1rem', zIndex: 9999 }}
      >
        {toasts.map((toast) => (
          <div
            key={toast.id}
            role="status"
            style={{
              marginTop: '0.5rem',
              padding: '0.75rem 1rem',
              borderRadius: 6,
              background: toast.type === 'error' ? '#fee2e2' : toast.type === 'success' ? '#dcfce7' : '#e0f2fe',
              color: toast.type === 'error' ? '#991b1b' : toast.type === 'success' ? '#166534' : '#0c4a6e',
            }}
          >
            {toast.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast(): ToastContextValue {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error('useToast must be used inside ToastProvider');
  return ctx;
}''',
    ),

    ex(
        "Build an accessible combobox (autocomplete input) with ARIA patterns for keyboard and screen reader support.",
        '''\
'use client';

import { useState, useRef, useId, useCallback, type KeyboardEvent } from 'react';

interface Option {
  id: string;
  label: string;
}

interface ComboboxProps {
  options: Option[];
  label: string;
  onSelect: (option: Option) => void;
  placeholder?: string;
}

export function Combobox({ options, label, onSelect, placeholder }: ComboboxProps) {
  const [inputValue, setInputValue] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const listId = useId();
  const inputId = useId();

  const filtered = options.filter((o) => o.label.toLowerCase().includes(inputValue.toLowerCase()));

  const select = useCallback((option: Option) => {
    setInputValue(option.label);
    setIsOpen(false);
    setActiveIndex(-1);
    onSelect(option);
  }, [onSelect]);

  function handleKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    if (!isOpen && (e.key === 'ArrowDown' || e.key === 'Enter')) {
      setIsOpen(true);
      setActiveIndex(0);
      return;
    }
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActiveIndex((i) => Math.min(i + 1, filtered.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActiveIndex((i) => Math.max(i - 1, 0));
    } else if (e.key === 'Enter' && activeIndex >= 0) {
      e.preventDefault();
      select(filtered[activeIndex]);
    } else if (e.key === 'Escape') {
      setIsOpen(false);
      setActiveIndex(-1);
    }
  }

  return (
    <div style={{ position: 'relative' }}>
      <label htmlFor={inputId}>{label}</label>
      <input
        id={inputId}
        ref={inputRef}
        role="combobox"
        aria-autocomplete="list"
        aria-expanded={isOpen}
        aria-controls={listId}
        aria-activedescendant={activeIndex >= 0 ? `option-${filtered[activeIndex]?.id}` : undefined}
        value={inputValue}
        placeholder={placeholder}
        onChange={(e) => { setInputValue(e.target.value); setIsOpen(true); setActiveIndex(0); }}
        onKeyDown={handleKeyDown}
        onBlur={() => setTimeout(() => setIsOpen(false), 150)}
        autoComplete="off"
      />
      {isOpen && filtered.length > 0 && (
        <ul
          id={listId}
          role="listbox"
          aria-label={label}
          style={{ position: 'absolute', zIndex: 10, width: '100%', listStyle: 'none', background: '#fff', border: '1px solid #ccc', padding: 0, margin: 0 }}
        >
          {filtered.map((opt, idx) => (
            <li
              key={opt.id}
              id={`option-${opt.id}`}
              role="option"
              aria-selected={idx === activeIndex}
              onMouseDown={() => select(opt)}
              style={{ padding: '0.5rem', background: idx === activeIndex ? '#e0f2fe' : undefined, cursor: 'pointer' }}
            >
              {opt.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}''',
    ),

    ex(
        "Create an accessible progress bar component with proper ARIA attributes.",
        '''\
interface ProgressBarProps {
  value: number;
  max?: number;
  label: string;
  showValue?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

const HEIGHT = { sm: 4, md: 8, lg: 16 };

export function ProgressBar({ value, max = 100, label, showValue = false, size = 'md' }: ProgressBarProps) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  const height = HEIGHT[size];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
        <span id="progress-label">{label}</span>
        {showValue && <span aria-hidden="true">{Math.round(pct)}%</span>}
      </div>
      <div
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
        aria-labelledby="progress-label"
        aria-valuetext={`${label}: ${Math.round(pct)}%`}
        style={{
          width: '100%',
          height,
          background: '#e5e7eb',
          borderRadius: height / 2,
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            width: `${pct}%`,
            height: '100%',
            background: '#0070f3',
            borderRadius: height / 2,
            transition: 'width 0.3s ease',
          }}
        />
      </div>
    </div>
  );
}''',
    ),

    ex(
        "Build an accessible data table with sortable columns, caption, and proper scope attributes.",
        '''\
interface Column<T> {
  key: keyof T;
  label: string;
  sortable?: boolean;
  render?: (value: T[keyof T], row: T) => React.ReactNode;
}

interface AccessibleTableProps<T extends { id: string }> {
  caption: string;
  columns: Column<T>[];
  rows: T[];
  onSort?: (key: keyof T, direction: 'asc' | 'desc') => void;
  sortKey?: keyof T;
  sortDirection?: 'asc' | 'desc';
}

export function AccessibleTable<T extends { id: string }>({
  caption,
  columns,
  rows,
  onSort,
  sortKey,
  sortDirection = 'asc',
}: AccessibleTableProps<T>) {
  function handleSort(key: keyof T) {
    if (!onSort) return;
    const nextDir = sortKey === key && sortDirection === 'asc' ? 'desc' : 'asc';
    onSort(key, nextDir);
  }

  return (
    <table>
      <caption>{caption}</caption>
      <thead>
        <tr>
          {columns.map((col) => (
            <th
              key={String(col.key)}
              scope="col"
              aria-sort={
                col.sortable && sortKey === col.key
                  ? sortDirection === 'asc' ? 'ascending' : 'descending'
                  : col.sortable ? 'none' : undefined
              }
            >
              {col.sortable ? (
                <button
                  type="button"
                  onClick={() => handleSort(col.key)}
                  aria-label={`Sort by ${col.label}${sortKey === col.key ? `, currently ${sortDirection}ending` : ''}`}
                >
                  {col.label}
                  {sortKey === col.key && <span aria-hidden="true">{sortDirection === 'asc' ? ' ↑' : ' ↓'}</span>}
                </button>
              ) : col.label}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.id}>
            {columns.map((col) => (
              <td key={String(col.key)}>
                {col.render ? col.render(row[col.key], row) : String(row[col.key])}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # TYPESCRIPT PATTERNS
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Create a generic List component in TypeScript that accepts any item type and a custom render function.",
        '''\
import type { ReactNode } from 'react';

interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => ReactNode;
  keyExtractor: (item: T, index: number) => string;
  emptyMessage?: string;
  'aria-label'?: string;
}

export function List<T>({
  items,
  renderItem,
  keyExtractor,
  emptyMessage = 'No items found.',
  'aria-label': ariaLabel,
}: ListProps<T>) {
  if (items.length === 0) {
    return <p role="status">{emptyMessage}</p>;
  }

  return (
    <ul aria-label={ariaLabel}>
      {items.map((item, index) => (
        <li key={keyExtractor(item, index)}>
          {renderItem(item, index)}
        </li>
      ))}
    </ul>
  );
}

// Usage example:
// <List
//   items={users}
//   keyExtractor={(u) => u.id}
//   renderItem={(u) => <span>{u.name}</span>}
//   aria-label="User list"
// />''',
    ),

    ex(
        "Build a polymorphic Button component that can render as a <button>, <a>, or any other element while preserving TypeScript types.",
        '''\
import { type ElementType, type ComponentPropsWithoutRef } from 'react';

type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger';
type ButtonSize = 'sm' | 'md' | 'lg';

type PolymorphicButtonProps<E extends ElementType = 'button'> = {
  as?: E;
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  loadingText?: string;
} & Omit<ComponentPropsWithoutRef<E>, 'as'>;

const VARIANT_STYLES: Record<ButtonVariant, string> = {
  primary: 'btn-primary',
  secondary: 'btn-secondary',
  ghost: 'btn-ghost',
  danger: 'btn-danger',
};

const SIZE_STYLES: Record<ButtonSize, string> = {
  sm: 'btn-sm',
  md: 'btn-md',
  lg: 'btn-lg',
};

export function Button<E extends ElementType = 'button'>({
  as,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  loadingText,
  children,
  className,
  disabled,
  ...rest
}: PolymorphicButtonProps<E>) {
  const Tag = as ?? 'button';
  const isDisabled = disabled || isLoading;

  return (
    <Tag
      className={[VARIANT_STYLES[variant], SIZE_STYLES[size], className].filter(Boolean).join(' ')}
      disabled={Tag === 'button' ? isDisabled : undefined}
      aria-disabled={isDisabled || undefined}
      aria-busy={isLoading || undefined}
      {...rest}
    >
      {isLoading ? (loadingText ?? 'Loading…') : children}
    </Tag>
  );
}''',
    ),

    ex(
        "Create a type-safe generic useFetch hook with loading, error, and data states in TypeScript.",
        '''\
'use client';

import { useState, useEffect, useRef } from 'react';

type FetchState<T> =
  | { status: 'idle'; data: null; error: null }
  | { status: 'loading'; data: null; error: null }
  | { status: 'success'; data: T; error: null }
  | { status: 'error'; data: null; error: Error };

interface UseFetchOptions extends RequestInit {
  skip?: boolean;
}

export function useFetch<T>(url: string, options?: UseFetchOptions): FetchState<T> {
  const [state, setState] = useState<FetchState<T>>({ status: 'idle', data: null, error: null });
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    if (options?.skip) return;

    abortRef.current?.abort();
    abortRef.current = new AbortController();
    const { skip: _skip, ...fetchOptions } = options ?? {};

    setState({ status: 'loading', data: null, error: null });

    fetch(url, { ...fetchOptions, signal: abortRef.current.signal })
      .then(async (res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        const data = (await res.json()) as T;
        setState({ status: 'success', data, error: null });
      })
      .catch((err: unknown) => {
        if (err instanceof Error && err.name === 'AbortError') return;
        setState({ status: 'error', data: null, error: err instanceof Error ? err : new Error(String(err)) });
      });

    return () => abortRef.current?.abort();
  }, [url, options?.skip]);

  return state;
}

// Usage:
// const state = useFetch<User[]>('/api/users');
// if (state.status === 'success') console.log(state.data); // typed as User[]''',
    ),

    ex(
        "Create a type-safe Context + Provider with useContext hook in TypeScript, throwing on missing provider.",
        '''\
'use client';

import { createContext, useContext, useState, useCallback, type ReactNode } from 'react';

interface CartItem {
  productId: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartContextValue {
  items: CartItem[];
  total: number;
  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (productId: string) => void;
  clearCart: () => void;
}

const CartContext = createContext<CartContextValue | null>(null);

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([]);

  const addItem = useCallback((newItem: Omit<CartItem, 'quantity'>) => {
    setItems((prev) => {
      const existing = prev.find((i) => i.productId === newItem.productId);
      if (existing) {
        return prev.map((i) =>
          i.productId === newItem.productId ? { ...i, quantity: i.quantity + 1 } : i,
        );
      }
      return [...prev, { ...newItem, quantity: 1 }];
    });
  }, []);

  const removeItem = useCallback((productId: string) => {
    setItems((prev) => prev.filter((i) => i.productId !== productId));
  }, []);

  const clearCart = useCallback(() => setItems([]), []);

  const total = items.reduce((sum, i) => sum + i.price * i.quantity, 0);

  return (
    <CartContext.Provider value={{ items, total, addItem, removeItem, clearCart }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart(): CartContextValue {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error('useCart must be used inside <CartProvider>');
  return ctx;
}''',
    ),

    ex(
        "Create a discriminated union type for a Button component that enforces required href only when used as a link.",
        '''\
import type { ReactNode, ButtonHTMLAttributes, AnchorHTMLAttributes } from 'react';

type ButtonBaseProps = {
  children: ReactNode;
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
};

type ButtonAsButton = ButtonBaseProps &
  Omit<ButtonHTMLAttributes<HTMLButtonElement>, keyof ButtonBaseProps> & {
    as?: 'button';
    href?: never;
    external?: never;
  };

type ButtonAsAnchor = ButtonBaseProps &
  Omit<AnchorHTMLAttributes<HTMLAnchorElement>, keyof ButtonBaseProps> & {
    as: 'a';
    href: string;
    external?: boolean;
  };

type ButtonProps = ButtonAsButton | ButtonAsAnchor;

export function Button(props: ButtonProps) {
  const { children, variant = 'primary', size = 'md', as, ...rest } = props;
  const className = `btn btn-${variant} btn-${size}`;

  if (as === 'a') {
    const { href, external, ...anchorRest } = rest as Omit<ButtonAsAnchor, keyof ButtonBaseProps | 'as'>;
    return (
      <a
        href={href}
        className={className}
        {...(external ? { target: '_blank', rel: 'noopener noreferrer' } : {})}
        {...anchorRest}
      >
        {children}
        {external && <span aria-label=" (opens in new tab)" aria-hidden="false"> ↗</span>}
      </a>
    );
  }

  const { type = 'button', ...buttonRest } = rest as Omit<ButtonAsButton, keyof ButtonBaseProps | 'as'>;
  return (
    <button type={type} className={className} {...buttonRest}>
      {children}
    </button>
  );
}''',
    ),

    ex(
        "Write a generic generic paginated data hook usePagination that works with any async fetch function.",
        '''\
'use client';

import { useState, useEffect, useCallback } from 'react';

interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
}

interface UsePaginationOptions {
  initialPage?: number;
  pageSize?: number;
}

interface UsePaginationResult<T> {
  data: T[];
  total: number;
  page: number;
  totalPages: number;
  isLoading: boolean;
  error: Error | null;
  goToPage: (page: number) => void;
  nextPage: () => void;
  prevPage: () => void;
}

type FetchFn<T> = (page: number, pageSize: number) => Promise<PaginatedResponse<T>>;

export function usePagination<T>(
  fetchFn: FetchFn<T>,
  options: UsePaginationOptions = {},
): UsePaginationResult<T> {
  const { initialPage = 1, pageSize = 20 } = options;
  const [page, setPage] = useState(initialPage);
  const [data, setData] = useState<T[]>([]);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;
    setIsLoading(true);
    setError(null);
    fetchFn(page, pageSize)
      .then((res) => {
        if (!cancelled) { setData(res.data); setTotal(res.total); }
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(err instanceof Error ? err : new Error(String(err)));
      })
      .finally(() => { if (!cancelled) setIsLoading(false); });
    return () => { cancelled = true; };
  }, [fetchFn, page, pageSize]);

  const totalPages = Math.ceil(total / pageSize);
  const goToPage = useCallback((p: number) => setPage(Math.min(Math.max(1, p), totalPages)), [totalPages]);
  const nextPage = useCallback(() => goToPage(page + 1), [goToPage, page]);
  const prevPage = useCallback(() => goToPage(page - 1), [goToPage, page]);

  return { data, total, page, totalPages, isLoading, error, goToPage, nextPage, prevPage };
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # MIXED / FULL COMPONENT PATTERNS
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Build a full comment section: Server Component fetches comments, Client Component handles new comment submission with optimistic UI.",
        '''\
// posts/[id]/CommentSection.tsx — Server Component
import { Suspense } from 'react';
import { CommentList } from './CommentList';
import { AddCommentForm } from './AddCommentForm';

interface Comment {
  id: string;
  author: string;
  body: string;
  createdAt: string;
}

async function getComments(postId: string): Promise<Comment[]> {
  const res = await fetch(`${process.env.API_URL}/posts/${postId}/comments`, { cache: 'no-store' });
  return res.json() as Promise<Comment[]>;
}

export async function CommentSection({ postId }: { postId: string }) {
  const comments = await getComments(postId);
  return (
    <section aria-label="Comments">
      <h2>Comments ({comments.length})</h2>
      <AddCommentForm postId={postId} />
      <Suspense fallback={<p>Loading comments…</p>}>
        <CommentList comments={comments} />
      </Suspense>
    </section>
  );
}

// AddCommentForm.tsx — Client Component with optimistic UI
'use client';

import { useOptimistic, useActionState } from 'react';
import { addComment } from '@/actions/comments';

interface Comment {
  id: string;
  author: string;
  body: string;
  createdAt: string;
}

interface AddCommentFormProps {
  postId: string;
}

type State = { error: string | null };

export function AddCommentForm({ postId }: AddCommentFormProps) {
  const [optimisticComments, addOptimistic] = useOptimistic<Comment[], Comment>(
    [],
    (state, newComment) => [...state, newComment],
  );

  async function action(_prev: State, formData: FormData): Promise<State> {
    const body = formData.get('body') as string;
    if (!body.trim()) return { error: 'Comment cannot be empty.' };
    addOptimistic({ id: `temp-${Date.now()}`, author: 'You', body, createdAt: new Date().toISOString() });
    await addComment(postId, body);
    return { error: null };
  }

  const [state, dispatch, isPending] = useActionState(action, { error: null });

  return (
    <>
      <form action={dispatch} aria-label="Add comment">
        <label htmlFor="comment-body">Your comment</label>
        <textarea id="comment-body" name="body" rows={3} required disabled={isPending} />
        {state.error && <p role="alert">{state.error}</p>}
        <button type="submit" disabled={isPending} aria-busy={isPending}>
          {isPending ? 'Posting…' : 'Post comment'}
        </button>
      </form>
      {optimisticComments.map((c) => (
        <div key={c.id} aria-label="Pending comment" style={{ opacity: 0.6 }}>
          <strong>You</strong>: {c.body}
        </div>
      ))}
    </>
  );
}''',
    ),

    ex(
        "Create a product page: Server Component for the product data, Client Component for quantity selector and add-to-cart, Server Action for cart mutation.",
        '''\
// products/[slug]/page.tsx — Server Component
import { Suspense } from 'react';
import { AddToCartSection } from './AddToCartSection';

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  imageUrl: string;
  stock: number;
  slug: string;
}

async function getProduct(slug: string): Promise<Product> {
  const res = await fetch(`${process.env.API_URL}/products/${slug}`);
  if (!res.ok) throw new Error('Product not found');
  return res.json() as Promise<Product>;
}

export default async function ProductPage({ params }: { params: { slug: string } }) {
  const product = await getProduct(params.slug);
  return (
    <main>
      <article aria-label={product.name}>
        <img src={product.imageUrl} alt={product.name} width={600} height={600} priority />
        <div>
          <h1>{product.name}</h1>
          <p>{product.description}</p>
          <p aria-label={`Price: $${product.price.toFixed(2)}`}>
            <strong>${product.price.toFixed(2)}</strong>
          </p>
          <p aria-live="polite">
            {product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}
          </p>
          <Suspense fallback={null}>
            <AddToCartSection productId={product.id} maxStock={product.stock} />
          </Suspense>
        </div>
      </article>
    </main>
  );
}

// AddToCartSection.tsx — Client Component
'use client';

import { useState, useTransition } from 'react';
import { addToCart } from '@/actions/cart';

interface AddToCartSectionProps {
  productId: string;
  maxStock: number;
}

export function AddToCartSection({ productId, maxStock }: AddToCartSectionProps) {
  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(false);
  const [isPending, startTransition] = useTransition();

  function handleAdd() {
    startTransition(async () => {
      await addToCart(productId, quantity);
      setAdded(true);
      setTimeout(() => setAdded(false), 3000);
    });
  }

  return (
    <div>
      <div role="group" aria-label="Quantity">
        <button
          type="button"
          onClick={() => setQuantity((q) => Math.max(1, q - 1))}
          disabled={quantity <= 1 || isPending}
          aria-label="Decrease quantity"
        >
          −
        </button>
        <span aria-live="polite" aria-atomic="true">{quantity}</span>
        <button
          type="button"
          onClick={() => setQuantity((q) => Math.min(maxStock, q + 1))}
          disabled={quantity >= maxStock || isPending}
          aria-label="Increase quantity"
        >
          +
        </button>
      </div>
      <button
        type="button"
        onClick={handleAdd}
        disabled={isPending || maxStock === 0}
        aria-busy={isPending}
        aria-live="polite"
      >
        {added ? 'Added to cart ✓' : isPending ? 'Adding…' : 'Add to cart'}
      </button>
    </div>
  );
}

// actions/cart.ts
'use server';


export async function addToCart(productId: string, quantity: number): Promise<void> {
  await fetch(`${process.env.API_URL}/cart/items`, {
    method: 'POST',
    body: JSON.stringify({ productId, quantity }),
    headers: { 'Content-Type': 'application/json' },
  });
  // // // // revalidatePath('/cart');
}''',
    ),

    ex(
        "Implement an infinite scroll list using a Server Component for initial data and a Client Component for loading more.",
        '''\
// feed/page.tsx — Server Component loads first page
import { FeedList } from './FeedList';

interface Post {
  id: string;
  title: string;
  excerpt: string;
  author: string;
  imageUrl: string;
}

async function getInitialPosts(): Promise<Post[]> {
  const res = await fetch(`${process.env.API_URL}/posts?page=1&limit=10`);
  return res.json() as Promise<Post[]>;
}

export default async function FeedPage() {
  const initialPosts = await getInitialPosts();
  return (
    <main>
      <h1>Feed</h1>
      <FeedList initialPosts={initialPosts} />
    </main>
  );
}

// FeedList.tsx — Client Component with infinite scroll
'use client';

import { useState, useEffect, useRef, useCallback } from 'react';

interface Post {
  id: string;
  title: string;
  excerpt: string;
  author: string;
  imageUrl: string;
}

interface FeedListProps {
  initialPosts: Post[];
}

export function FeedList({ initialPosts }: FeedListProps) {
  const [posts, setPosts] = useState<Post[]>(initialPosts);
  const [page, setPage] = useState(2);
  const [hasMore, setHasMore] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const sentinelRef = useRef<HTMLDivElement>(null);

  const loadMore = useCallback(async () => {
    if (isLoading || !hasMore) return;
    setIsLoading(true);
    const res = await fetch(`/api/posts?page=${page}&limit=10`);
    const newPosts = (await res.json()) as Post[];
    if (newPosts.length === 0) { setHasMore(false); } else {
      setPosts((prev) => [...prev, ...newPosts]);
      setPage((p) => p + 1);
    }
    setIsLoading(false);
  }, [isLoading, hasMore, page]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => { if (entries[0].isIntersecting) loadMore(); },
      { rootMargin: '200px' },
    );
    if (sentinelRef.current) observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [loadMore]);

  return (
    <>
      <ol aria-label="Feed posts" style={{ listStyle: 'none', padding: 0 }}>
        {posts.map((post) => (
          <li key={post.id}>
            <article>
              <img src={post.imageUrl} alt="" loading="lazy" width={400} height={200} />
              <h2>{post.title}</h2>
              <p>{post.excerpt}</p>
              <span>By {post.author}</span>
            </article>
          </li>
        ))}
      </ol>
      <div ref={sentinelRef} aria-hidden="true" />
      {isLoading && <p role="status" aria-live="polite">Loading more posts…</p>}
      {!hasMore && <p>You have reached the end of the feed.</p>}
    </>
  );
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # ADDITIONAL useActionState PATTERNS
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Build a password change form with useActionState that validates current password and confirms new password.",
        '''\
'use client';

import { useActionState } from 'react';

type PasswordState = { errors: Partial<Record<'current' | 'new' | 'confirm' | 'form', string>>; success: boolean };

async function changePasswordAction(_prev: PasswordState, formData: FormData): Promise<PasswordState> {
  const current = formData.get('current') as string;
  const newPw = formData.get('new') as string;
  const confirm = formData.get('confirm') as string;
  const errors: PasswordState['errors'] = {};

  if (!current) errors.current = 'Current password is required.';
  if (newPw.length < 8) errors.new = 'New password must be at least 8 characters.';
  if (newPw !== confirm) errors.confirm = 'Passwords do not match.';
  if (Object.keys(errors).length > 0) return { errors, success: false };

  const res = await fetch('/api/user/password', {
    method: 'PUT',
    body: JSON.stringify({ currentPassword: current, newPassword: newPw }),
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    const status = res.status;
    return {
      errors: { form: status === 401 ? 'Current password is incorrect.' : 'Failed to update password.' },
      success: false,
    };
  }
  return { errors: {}, success: true };
}

export default function ChangePasswordForm() {
  const [state, dispatch, isPending] = useActionState(changePasswordAction, { errors: {}, success: false });

  if (state.success) return <p role="status">Password updated successfully.</p>;

  return (
    <form action={dispatch} aria-label="Change password">
      {state.errors.form && <p role="alert">{state.errors.form}</p>}

      {(['current', 'new', 'confirm'] as const).map((field) => (
        <div key={field}>
          <label htmlFor={`pw-${field}`}>
            {field === 'current' ? 'Current password' : field === 'new' ? 'New password' : 'Confirm new password'}
          </label>
          <input
            id={`pw-${field}`}
            name={field}
            type="password"
            required
            disabled={isPending}
            aria-describedby={state.errors[field] ? `${field}-err` : undefined}
            aria-invalid={!!state.errors[field]}
            autoComplete={field === 'current' ? 'current-password' : 'new-password'}
          />
          {state.errors[field] && <span id={`${field}-err`} role="alert">{state.errors[field]}</span>}
        </div>
      ))}

      <button type="submit" disabled={isPending} aria-busy={isPending}>
        {isPending ? 'Updating…' : 'Update password'}
      </button>
    </form>
  );
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # SUSPENSE STREAMING
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Use React Suspense to stream multiple independent data sections on a page using Server Components.",
        '''\
// profile/[id]/page.tsx
import { Suspense } from 'react';

// Each async Server Component fetches independently — Suspense streams each section
async function UserHeader({ userId }: { userId: string }) {
  const res = await fetch(`${process.env.API_URL}/users/${userId}`);
  const user = await res.json() as { name: string; bio: string; avatarUrl: string };
  return (
    <header>
      <img src={user.avatarUrl} alt={`${user.name} avatar`} width={80} height={80} />
      <h1>{user.name}</h1>
      <p>{user.bio}</p>
    </header>
  );
}

async function UserPosts({ userId }: { userId: string }) {
  const res = await fetch(`${process.env.API_URL}/users/${userId}/posts`);
  const posts = await res.json() as Array<{ id: string; title: string }>;
  return (
    <section aria-label="Posts">
      <h2>Posts ({posts.length})</h2>
      <ul>
        {posts.map((p) => <li key={p.id}>{p.title}</li>)}
      </ul>
    </section>
  );
}

async function UserActivity({ userId }: { userId: string }) {
  const res = await fetch(`${process.env.API_URL}/users/${userId}/activity`);
  const activity = await res.json() as Array<{ id: string; event: string; date: string }>;
  return (
    <section aria-label="Recent activity">
      <h2>Activity</h2>
      <ul>
        {activity.map((a) => (
          <li key={a.id}>
            {a.event} — <time dateTime={a.date}>{new Date(a.date).toLocaleDateString()}</time>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default function ProfilePage({ params }: { params: { id: string } }) {
  return (
    <main>
      <Suspense fallback={<div aria-busy="true">Loading profile…</div>}>
        <UserHeader userId={params.id} />
      </Suspense>
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
        <Suspense fallback={<div aria-busy="true">Loading posts…</div>}>
          <UserPosts userId={params.id} />
        </Suspense>
        <Suspense fallback={<div aria-busy="true">Loading activity…</div>}>
          <UserActivity userId={params.id} />
        </Suspense>
      </div>
    </main>
  );
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # PERFORMANCE — useCallback with React.memo
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Show how to correctly combine React.memo and useCallback in a parent-child component pair to prevent unnecessary re-renders.",
        '''\
'use client';

import { useState, useCallback, memo } from 'react';

interface Task {
  id: string;
  title: string;
  done: boolean;
}

interface TaskItemProps {
  task: Task;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

// memo prevents re-render unless task, onToggle, or onDelete change reference
const TaskItem = memo(function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  return (
    <li>
      <label>
        <input
          type="checkbox"
          checked={task.done}
          onChange={() => onToggle(task.id)}
          aria-label={`Mark "${task.title}" as ${task.done ? 'incomplete' : 'complete'}`}
        />
        <span style={{ textDecoration: task.done ? 'line-through' : 'none' }}>{task.title}</span>
      </label>
      <button type="button" onClick={() => onDelete(task.id)} aria-label={`Delete task: ${task.title}`}>
        Delete
      </button>
    </li>
  );
});

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([
    { id: '1', title: 'Buy groceries', done: false },
    { id: '2', title: 'Write tests', done: true },
  ]);
  const [filter, setFilter] = useState<'all' | 'active' | 'done'>('all');

  // useCallback ensures stable references so memo on TaskItem is effective
  const handleToggle = useCallback((id: string) => {
    setTasks((prev) => prev.map((t) => t.id === id ? { ...t, done: !t.done } : t));
  }, []);

  const handleDelete = useCallback((id: string) => {
    setTasks((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const visible = tasks.filter((t) => {
    if (filter === 'active') return !t.done;
    if (filter === 'done') return t.done;
    return true;
  });

  return (
    <div>
      <div role="group" aria-label="Filter tasks">
        {(['all', 'active', 'done'] as const).map((f) => (
          <button
            key={f}
            type="button"
            aria-pressed={filter === f}
            onClick={() => setFilter(f)}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>
      <ul aria-label="Tasks">
        {visible.map((task) => (
          <TaskItem key={task.id} task={task} onToggle={handleToggle} onDelete={handleDelete} />
        ))}
      </ul>
      <p aria-live="polite">{tasks.filter((t) => !t.done).length} task(s) remaining</p>
    </div>
  );
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # ADDITIONAL TYPESCRIPT — Generic Table
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Build a fully generic TypeScript DataGrid component that infers column types from the data shape.",
        '''\
import type { ReactNode } from 'react';

type Primitive = string | number | boolean | null | undefined;

interface ColumnDef<T> {
  accessor: keyof T;
  header: string;
  cell?: (value: T[keyof T], row: T) => ReactNode;
  sortable?: boolean;
}

interface DataGridProps<T extends Record<string, Primitive>> {
  caption: string;
  columns: ColumnDef<T>[];
  rows: T[];
  getRowKey: (row: T) => string;
  isLoading?: boolean;
  emptyMessage?: string;
}

export function DataGrid<T extends Record<string, Primitive>>({
  caption,
  columns,
  rows,
  getRowKey,
  isLoading = false,
  emptyMessage = 'No data available.',
}: DataGridProps<T>) {
  if (isLoading) {
    return (
      <div role="status" aria-busy="true" aria-label="Loading data">
        <span className="sr-only">Loading…</span>
      </div>
    );
  }

  if (rows.length === 0) {
    return <p role="status">{emptyMessage}</p>;
  }

  return (
    <div style={{ overflowX: 'auto' }}>
      <table>
        <caption>{caption}</caption>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={String(col.accessor)} scope="col">
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={getRowKey(row)}>
              {columns.map((col) => (
                <td key={String(col.accessor)}>
                  {col.cell
                    ? col.cell(row[col.accessor], row)
                    : String(row[col.accessor] ?? '')}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// Usage:
// <DataGrid
//   caption="Users"
//   columns={[{ accessor: 'name', header: 'Name' }, { accessor: 'email', header: 'Email' }]}
//   rows={users}
//   getRowKey={(u) => u.id}
// />''',
    ),

    ex(
        "Convert a class-based React component to a functional component with hooks.",
        '''\
// BEFORE — class component (do not write like this):
// class Timer extends React.Component {
//   state = { seconds: 0 };
//   interval: ReturnType<typeof setInterval> | null = null;
//   componentDidMount() { this.interval = setInterval(() => this.setState(s => ({ seconds: s.seconds + 1 })), 1000); }
//   componentWillUnmount() { if (this.interval) clearInterval(this.interval); }
//   render() { return <div>Elapsed: {this.state.seconds}s</div>; }
// }

// AFTER — functional component with hooks:
'use client';

import { useState, useEffect } from 'react';

interface TimerProps {
  onTimeUp?: (elapsed: number) => void;
  limit?: number;
}

export function Timer({ onTimeUp, limit }: TimerProps) {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds((s) => {
        const next = s + 1;
        if (limit && next >= limit) {
          clearInterval(interval);
          onTimeUp?.(next);
        }
        return next;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [limit, onTimeUp]);

  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;

  return (
    <time
      aria-label={`Elapsed time: ${minutes} minutes and ${secs} seconds`}
      dateTime={`PT${minutes}M${secs}S`}
    >
      {String(minutes).padStart(2, '0')}:{String(secs).padStart(2, '0')}
    </time>
  );
}''',
    ),

    ex(
        "Explain when NOT to use useEffect and show the correct alternative for each case.",
        '''\
'use client';

// ✗ BAD: useEffect to derive state from props
// useEffect(() => { setFullName(firstName + ' ' + lastName); }, [firstName, lastName]);

// ✓ GOOD: derive state during render — no useEffect needed
import { useMemo } from 'react';

interface NameBadgeProps {
  firstName: string;
  lastName: string;
  items: string[];
  filterText: string;
}

export function NameBadge({ firstName, lastName, items, filterText }: NameBadgeProps) {
  // Derived value — compute during render, no effect needed
  const fullName = `${firstName} ${lastName}`.trim();

  // Derived + expensive — useMemo, still no effect needed
  const filtered = useMemo(
    () => items.filter((item) => item.toLowerCase().includes(filterText.toLowerCase())),
    [items, filterText],
  );

  return (
    <div>
      <p>Welcome, {fullName}</p>
      <ul aria-label="Filtered items">
        {filtered.map((item) => <li key={item}>{item}</li>)}
      </ul>
    </div>
  );
}

// ✗ BAD: useEffect to fetch data on mount in a client component that could be a Server Component
// useEffect(() => { fetch('/api/data').then(...) }, []);

// ✓ GOOD: Server Component fetches data directly
// export default async function DataPage() {
//   const data = await fetch('/api/data').then(r => r.json());
//   return <div>{data.map(...)}</div>;
// }

// ✓ GOOD: When you genuinely need a side effect (syncing to an external system):
import { useEffect, useRef } from 'react';

interface VideoPlayerProps {
  src: string;
  isPlaying: boolean;
}

export function VideoPlayer({ src, isPlaying }: VideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null);

  // ✓ VALID useEffect: syncing React state to a DOM API
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    if (isPlaying) { video.play().catch(() => {}); }
    else { video.pause(); }
  }, [isPlaying]);

  return <video ref={videoRef} src={src} aria-label="Video player" />;
}''',
    ),

    ex(
        "Create a reusable ErrorBoundary component with TypeScript and a fallback UI that allows retry.",
        '''\
'use client';

import { Component, type ErrorInfo, type ReactNode } from 'react';

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: (error: Error, reset: () => void) => ReactNode;
}

interface ErrorBoundaryState {
  error: Error | null;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('[ErrorBoundary]', error, info.componentStack);
  }

  reset = () => this.setState({ error: null });

  render() {
    const { error } = this.state;
    const { children, fallback } = this.props;

    if (error) {
      if (fallback) return fallback(error, this.reset);
      return (
        <div role="alert" aria-live="assertive">
          <h2>Something went wrong</h2>
          <p>{error.message}</p>
          <button type="button" onClick={this.reset}>Try again</button>
        </div>
      );
    }

    return children;
  }
}

// Usage in a Server Component:
// <ErrorBoundary fallback={(err, reset) => (
//   <div role="alert">
//     <p>Failed to load: {err.message}</p>
//     <button onClick={reset}>Retry</button>
//   </div>
// )}>
//   <AsyncComponent />
// </ErrorBoundary>''',
    ),

]

EXAMPLES.extend(STYLING_EXAMPLES)


def main() -> None:
    out = Path("react_golden_dataset.jsonl")
    with out.open("w", encoding="utf-8") as f:
        for item in EXAMPLES:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Wrote {len(EXAMPLES)} examples → {out}")
    print("\nCategory breakdown:")
    print("  useActionState        : ~6 examples")
    print("  useFormStatus         : ~3 examples")
    print("  use() API             : ~2 examples")
    print("  Server Actions        : ~4 examples")
    print("  Server Components     : ~4 examples")
    print("  Client Components     : ~3 examples")
    print("  useMemo               : ~2 examples")
    print("  useCallback           : ~2 examples")
    print("  React.memo            : ~2 examples")
    print("  Suspense / lazy()     : ~3 examples")
    print("  Accessibility         : ~5 examples")
    print("  TypeScript patterns   : ~6 examples")
    print("  Mixed full components : ~5 examples")
    print("  Misc patterns         : ~3 examples")
    print(f"  Tailwind + CSS Modules: {len(STYLING_EXAMPLES)} examples")


if __name__ == "__main__":
    main()
