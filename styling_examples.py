"""Tailwind CSS and CSS Modules training examples."""

from dataset_common import ex

STYLING_EXAMPLES: list[dict] = [
    # ════════════════════════════════════════════════════════════════════════
    # TAILWIND CSS
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Build an accessible primary button component with Tailwind CSS variants (default, destructive, outline).",
        '''\
'use client';

import { type ButtonHTMLAttributes } from 'react';

type Variant = 'default' | 'destructive' | 'outline';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

const variantClasses: Record<Variant, string> = {
  default:
    'bg-blue-600 text-white hover:bg-blue-700 focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2',
  destructive:
    'bg-red-600 text-white hover:bg-red-700 focus-visible:ring-2 focus-visible:ring-red-500 focus-visible:ring-offset-2',
  outline:
    'border border-gray-300 bg-white text-gray-900 hover:bg-gray-50 focus-visible:ring-2 focus-visible:ring-gray-400 focus-visible:ring-offset-2',
};

export function Button({ variant = 'default', className = '', children, ...props }: ButtonProps) {
  return (
    <button
      type="button"
      className={`inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors disabled:pointer-events-none disabled:opacity-50 ${variantClasses[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}''',
    ),

    ex(
        "Create a responsive product card grid with Tailwind CSS (mobile 1 col, tablet 2, desktop 3).",
        '''\
interface Product {
  id: string;
  name: string;
  price: number;
  imageUrl: string;
}

interface ProductGridProps {
  products: Product[];
}

export function ProductGrid({ products }: ProductGridProps) {
  return (
    <ul className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {products.map((product) => (
        <li key={product.id}>
          <article className="flex h-full flex-col overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
            <img
              src={product.imageUrl}
              alt=""
              className="aspect-video w-full object-cover"
            />
            <div className="flex flex-1 flex-col p-4">
              <h2 className="text-lg font-semibold text-gray-900">{product.name}</h2>
              <p className="mt-auto pt-2 text-sm font-medium text-blue-600">
                ${product.price.toFixed(2)}
              </p>
            </div>
          </article>
        </li>
      ))}
    </ul>
  );
}''',
    ),

    ex(
        "Build an accessible modal dialog with Tailwind CSS: overlay, focus trap, and ESC to close.",
        '''\
'use client';

import { useEffect, useRef, useCallback, type ReactNode } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    },
    [onClose],
  );

  useEffect(() => {
    if (!isOpen) return;
    document.addEventListener('keydown', handleKeyDown);
    document.body.classList.add('overflow-hidden');
    dialogRef.current?.focus();
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.classList.remove('overflow-hidden');
    };
  }, [isOpen, handleKeyDown]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" role="presentation">
      <div
        className="absolute inset-0 bg-black/50"
        aria-hidden="true"
        onClick={onClose}
      />
      <dialog
        ref={dialogRef}
        open
        aria-labelledby="modal-title"
        className="relative z-10 w-full max-w-md rounded-lg bg-white p-6 shadow-xl focus:outline-none"
      >
        <div className="mb-4 flex items-center justify-between">
          <h2 id="modal-title" className="text-lg font-semibold text-gray-900">
            {title}
          </h2>
          <button
            type="button"
            onClick={onClose}
            className="rounded-md p-1 text-gray-500 hover:bg-gray-100 hover:text-gray-700 focus-visible:ring-2 focus-visible:ring-blue-500"
            aria-label="Close dialog"
          >
            ✕
          </button>
        </div>
        {children}
      </dialog>
    </div>
  );
}''',
    ),

    ex(
        "Create a sticky top navigation bar with Tailwind CSS and a mobile hamburger menu.",
        '''\
'use client';

import { useState } from 'react';

const links = [
  { href: '/', label: 'Home' },
  { href: '/about', label: 'About' },
  { href: '/contact', label: 'Contact' },
] as const;

export function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 border-b border-gray-200 bg-white/90 backdrop-blur">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3" aria-label="Main">
        <a href="/" className="text-lg font-bold text-gray-900">
          Acme
        </a>

        <ul className="hidden gap-6 md:flex">
          {links.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className="text-sm font-medium text-gray-600 hover:text-gray-900 focus-visible:underline"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        <button
          type="button"
          className="rounded-md p-2 text-gray-700 hover:bg-gray-100 md:hidden"
          aria-expanded={open}
          aria-controls="mobile-menu"
          onClick={() => setOpen((v) => !v)}
        >
          <span className="sr-only">Toggle menu</span>
          {open ? '✕' : '☰'}
        </button>
      </nav>

      {open && (
        <ul id="mobile-menu" className="border-t border-gray-200 px-4 py-2 md:hidden">
          {links.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className="block rounded-md px-2 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                onClick={() => setOpen(false)}
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>
      )}
    </header>
  );
}''',
    ),

    ex(
        "Style a login form with Tailwind CSS including focus rings and error states.",
        '''\
'use client';

import { useActionState } from 'react';

type LoginState = { error: string | null };

async function loginAction(_prev: LoginState, formData: FormData): Promise<LoginState> {
  const email = formData.get('email') as string;
  if (!email.includes('@')) return { error: 'Enter a valid email.' };
  return { error: null };
}

export default function LoginForm() {
  const [state, dispatch, isPending] = useActionState(loginAction, { error: null });

  return (
    <form action={dispatch} className="mx-auto w-full max-w-sm space-y-4 rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <h1 className="text-xl font-semibold text-gray-900">Sign in</h1>

      {state.error && (
        <p role="alert" className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">
          {state.error}
        </p>
      )}

      <div>
        <label htmlFor="email" className="mb-1 block text-sm font-medium text-gray-700">
          Email
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          disabled={isPending}
          className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 disabled:bg-gray-50"
        />
      </div>

      <button
        type="submit"
        disabled={isPending}
        className="w-full rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
      >
        {isPending ? 'Signing in…' : 'Sign in'}
      </button>
    </form>
  );
}''',
    ),

    ex(
        "Build a dark-mode toggle using Tailwind CSS dark: variants and localStorage.",
        '''\
'use client';

import { useEffect, useState } from 'react';

export function ThemeToggle() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const isDark = stored === 'dark' || (!stored && prefersDark);
    setDark(isDark);
    document.documentElement.classList.toggle('dark', isDark);
  }, []);

  const toggle = () => {
    const next = !dark;
    setDark(next);
    document.documentElement.classList.toggle('dark', next);
    localStorage.setItem('theme', next ? 'dark' : 'light');
  };

  return (
    <button
      type="button"
      onClick={toggle}
      aria-pressed={dark}
      className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-800 shadow-sm hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 dark:hover:bg-gray-700"
    >
      {dark ? 'Light mode' : 'Dark mode'}
    </button>
  );
}''',
    ),

    ex(
        "Create a data table with Tailwind CSS striped rows and hover states.",
        '''\
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'member';
}

interface UserTableProps {
  users: User[];
}

export function UserTable({ users }: UserTableProps) {
  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200 shadow-sm">
      <table className="min-w-full divide-y divide-gray-200 text-sm">
        <thead className="bg-gray-50">
          <tr>
            <th scope="col" className="px-4 py-3 text-left font-semibold text-gray-900">Name</th>
            <th scope="col" className="px-4 py-3 text-left font-semibold text-gray-900">Email</th>
            <th scope="col" className="px-4 py-3 text-left font-semibold text-gray-900">Role</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100 bg-white">
          {users.map((user, i) => (
            <tr
              key={user.id}
              className={i % 2 === 1 ? 'bg-gray-50/80 hover:bg-gray-100' : 'hover:bg-gray-50'}
            >
              <td className="px-4 py-3 font-medium text-gray-900">{user.name}</td>
              <td className="px-4 py-3 text-gray-600">{user.email}</td>
              <td className="px-4 py-3">
                <span className="inline-flex rounded-full bg-blue-100 px-2 py-0.5 text-xs font-medium text-blue-800">
                  {user.role}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}''',
    ),

    ex(
        "Use Tailwind CSS with clsx to compose conditional class names for alert variants.",
        '''\
import { type ReactNode } from 'react';

type AlertVariant = 'info' | 'success' | 'warning' | 'error';

interface AlertProps {
  variant: AlertVariant;
  title: string;
  children?: ReactNode;
}

function cn(...classes: Array<string | false | undefined>) {
  return classes.filter(Boolean).join(' ');
}

const variantStyles: Record<AlertVariant, string> = {
  info: 'border-blue-200 bg-blue-50 text-blue-900',
  success: 'border-green-200 bg-green-50 text-green-900',
  warning: 'border-amber-200 bg-amber-50 text-amber-900',
  error: 'border-red-200 bg-red-50 text-red-900',
};

export function Alert({ variant, title, children }: AlertProps) {
  return (
    <div
      role="alert"
      className={cn('rounded-lg border px-4 py-3', variantStyles[variant])}
    >
      <p className="font-semibold">{title}</p>
      {children && <div className="mt-1 text-sm opacity-90">{children}</div>}
    </div>
  );
}''',
    ),

    # ════════════════════════════════════════════════════════════════════════
    # CSS MODULES
    # ════════════════════════════════════════════════════════════════════════

    ex(
        "Create a ProductCard component with CSS Modules (ProductCard.module.css) and TypeScript props.",
        '''\
// ProductCard.tsx
import styles from './ProductCard.module.css';

interface ProductCardProps {
  name: string;
  price: number;
  imageUrl: string;
  onAddToCart: () => void;
}

export function ProductCard({ name, price, imageUrl, onAddToCart }: ProductCardProps) {
  return (
    <article className={styles.card}>
      <img src={imageUrl} alt="" className={styles.image} />
      <div className={styles.body}>
        <h2 className={styles.title}>{name}</h2>
        <p className={styles.price}>${price.toFixed(2)}</p>
        <button type="button" className={styles.button} onClick={onAddToCart}>
          Add to cart
        </button>
      </div>
    </article>
  );
}

/* ProductCard.module.css */
.card {
  display: flex;
  flex-direction: column;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 1px 2px rgb(0 0 0 / 0.05);
}

.image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}

.body {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
}

.title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
}

.price {
  font-size: 0.875rem;
  font-weight: 500;
  color: #2563eb;
}

.button {
  margin-top: auto;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  background: #2563eb;
  color: #fff;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
}

.button:hover {
  background: #1d4ed8;
}

.button:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}''',
    ),

    ex(
        "Build a responsive navbar with CSS Modules and a mobile menu toggle.",
        '''\
// Navbar.tsx
'use client';

import { useState } from 'react';
import styles from './Navbar.module.css';

const links = [
  { href: '/', label: 'Home' },
  { href: '/products', label: 'Products' },
  { href: '/contact', label: 'Contact' },
] as const;

export function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className={styles.header}>
      <nav className={styles.nav} aria-label="Main">
        <a href="/" className={styles.logo}>Shop</a>

        <ul className={styles.desktopLinks}>
          {links.map((l) => (
            <li key={l.href}>
              <a href={l.href} className={styles.link}>{l.label}</a>
            </li>
          ))}
        </ul>

        <button
          type="button"
          className={styles.menuButton}
          aria-expanded={open}
          aria-controls="mobile-nav"
          onClick={() => setOpen((v) => !v)}
        >
          <span className={styles.srOnly}>Menu</span>
          <span aria-hidden="true">{open ? '✕' : '☰'}</span>
        </button>
      </nav>

      {open && (
        <ul id="mobile-nav" className={styles.mobileLinks}>
          {links.map((l) => (
            <li key={l.href}>
              <a href={l.href} className={styles.mobileLink} onClick={() => setOpen(false)}>
                {l.label}
              </a>
            </li>
          ))}
        </ul>
      )}
    </header>
  );
}

/* Navbar.module.css */
.header {
  position: sticky;
  top: 0;
  z-index: 40;
  border-bottom: 1px solid #e5e7eb;
  background: rgb(255 255 255 / 0.9);
  backdrop-filter: blur(8px);
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 72rem;
  margin: 0 auto;
  padding: 0.75rem 1rem;
}

.logo {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827;
  text-decoration: none;
}

.desktopLinks {
  display: none;
  gap: 1.5rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

@media (min-width: 768px) {
  .desktopLinks { display: flex; }
  .menuButton { display: none; }
}

.link {
  font-size: 0.875rem;
  font-weight: 500;
  color: #4b5563;
  text-decoration: none;
}

.link:hover { color: #111827; }

.menuButton {
  padding: 0.5rem;
  border: none;
  background: transparent;
  border-radius: 0.375rem;
  cursor: pointer;
}

.menuButton:hover { background: #f3f4f6; }

.mobileLinks {
  list-style: none;
  margin: 0;
  padding: 0.5rem 1rem 1rem;
  border-top: 1px solid #e5e7eb;
}

@media (min-width: 768px) {
  .mobileLinks { display: none; }
}

.mobileLink {
  display: block;
  padding: 0.5rem;
  border-radius: 0.375rem;
  color: #374151;
  text-decoration: none;
}

.mobileLink:hover { background: #f9fafb; }

.srOnly {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}''',
    ),

    ex(
        "Create a modal dialog with CSS Modules including overlay and dialog styles.",
        '''\
// Modal.tsx
'use client';

import { useEffect, useRef, type ReactNode } from 'react';
import styles from './Modal.module.css';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const ref = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    if (!isOpen) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', onKey);
    ref.current?.focus();
    return () => document.removeEventListener('keydown', onKey);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className={styles.backdrop} role="presentation" onClick={onClose}>
      <dialog
        ref={ref}
        open
        className={styles.dialog}
        aria-labelledby="modal-title"
        onClick={(e) => e.stopPropagation()}
      >
        <header className={styles.header}>
          <h2 id="modal-title" className={styles.title}>{title}</h2>
          <button type="button" className={styles.close} onClick={onClose} aria-label="Close">
            ✕
          </button>
        </header>
        <div className={styles.body}>{children}</div>
      </dialog>
    </div>
  );
}

/* Modal.module.css */
.backdrop {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: rgb(0 0 0 / 0.5);
}

.dialog {
  width: 100%;
  max-width: 28rem;
  margin: 0;
  padding: 0;
  border: none;
  border-radius: 0.5rem;
  background: #fff;
  box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.25);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #e5e7eb;
}

.title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.close {
  border: none;
  background: transparent;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  cursor: pointer;
  color: #6b7280;
}

.close:hover { background: #f3f4f6; color: #111827; }

.body { padding: 1.25rem; }''',
    ),

    ex(
        "Style a contact form with CSS Modules including error and focus states.",
        '''\
// ContactForm.tsx
'use client';

import { useActionState } from 'react';
import styles from './ContactForm.module.css';

type State = { error: string | null; success: boolean };

async function submitAction(_prev: State, formData: FormData): Promise<State> {
  const message = formData.get('message') as string;
  if (!message.trim()) return { error: 'Message is required.', success: false };
  return { error: null, success: true };
}

export default function ContactForm() {
  const [state, dispatch, isPending] = useActionState(submitAction, { error: null, success: false });

  return (
    <form action={dispatch} className={styles.form} aria-label="Contact">
      {state.error && <p role="alert" className={styles.error}>{state.error}</p>}
      {state.success && <p role="status" className={styles.success}>Message sent!</p>}

      <label htmlFor="message" className={styles.label}>Message</label>
      <textarea
        id="message"
        name="message"
        rows={5}
        required
        disabled={isPending}
        className={styles.textarea}
      />

      <button type="submit" className={styles.submit} disabled={isPending}>
        {isPending ? 'Sending…' : 'Send'}
      </button>
    </form>
  );
}

/* ContactForm.module.css */
.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 24rem;
  padding: 1.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  background: #fff;
}

.label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.textarea {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  resize: vertical;
}

.textarea:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 0;
  border-color: #3b82f6;
}

.textarea:disabled { background: #f9fafb; opacity: 0.7; }

.submit {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  background: #2563eb;
  color: #fff;
  font-weight: 500;
  cursor: pointer;
}

.submit:hover:not(:disabled) { background: #1d4ed8; }

.submit:disabled { opacity: 0.5; cursor: not-allowed; }

.error {
  margin: 0;
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  background: #fef2f2;
  color: #b91c1c;
  font-size: 0.875rem;
}

.success {
  margin: 0;
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  background: #f0fdf4;
  color: #15803d;
  font-size: 0.875rem;
}''',
    ),

    ex(
        "Build a CSS Modules button with primary and secondary variants using composition.",
        '''\
// Button.tsx
import { type ReactNode } from 'react';
import styles from './Button.module.css';

type Variant = 'primary' | 'secondary';

interface ButtonProps {
  variant?: Variant;
  children: ReactNode;
  type?: 'button' | 'submit';
  disabled?: boolean;
  onClick?: () => void;
}

export function Button({
  variant = 'primary',
  children,
  type = 'button',
  disabled,
  onClick,
}: ButtonProps) {
  const className = [styles.base, styles[variant]].join(' ');
  return (
    <button type={type} className={className} disabled={disabled} onClick={onClick}>
      {children}
    </button>
  );
}

/* Button.module.css */
.base {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}

.base:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.base:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.primary {
  border: none;
  background: #2563eb;
  color: #fff;
}

.primary:hover:not(:disabled) {
  background: #1d4ed8;
}

.secondary {
  border: 1px solid #d1d5db;
  background: #fff;
  color: #111827;
}

.secondary:hover:not(:disabled) {
  background: #f9fafb;
}''',
    ),

    ex(
        "Create a Server Component page layout with CSS Modules for header, main, and footer.",
        '''\
// PageLayout.tsx
import { type ReactNode } from 'react';
import styles from './PageLayout.module.css';

interface PageLayoutProps {
  children: ReactNode;
}

export function PageLayout({ children }: PageLayoutProps) {
  return (
    <div className={styles.wrapper}>
      <header className={styles.header}>
        <a href="/" className={styles.brand}>My App</a>
      </header>
      <main id="main-content" className={styles.main}>
        {children}
      </main>
      <footer className={styles.footer}>
        <p className={styles.copyright}>© {new Date().getFullYear()} My App</p>
      </footer>
    </div>
  );
}

/* PageLayout.module.css */
.wrapper {
  display: flex;
  min-height: 100dvh;
  flex-direction: column;
}

.header {
  border-bottom: 1px solid #e5e7eb;
  padding: 1rem 1.5rem;
}

.brand {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  text-decoration: none;
}

.main {
  flex: 1;
  width: 100%;
  max-width: 72rem;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.footer {
  border-top: 1px solid #e5e7eb;
  padding: 1rem 1.5rem;
  background: #f9fafb;
}

.copyright {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}''',
    ),

    ex(
        "Use CSS Modules with a loading skeleton animation for async content.",
        '''\
// SkeletonCard.tsx
import styles from './SkeletonCard.module.css';

interface SkeletonCardProps {
  lines?: number;
}

export function SkeletonCard({ lines = 3 }: SkeletonCardProps) {
  return (
    <article className={styles.card} aria-busy="true" aria-label="Loading content">
      <div className={styles.thumbnail} />
      <div className={styles.content}>
        {Array.from({ length: lines }, (_, i) => (
          <div
            key={i}
            className={styles.line}
            style={{ width: i === lines - 1 ? '60%' : '100%' }}
          />
        ))}
      </div>
    </article>
  );
}

/* SkeletonCard.module.css */
.card {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  overflow: hidden;
  background: #fff;
}

.thumbnail {
  height: 10rem;
  background: linear-gradient(90deg, #f3f4f6 25%, #e5e7eb 50%, #f3f4f6 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
}

.line {
  height: 0.875rem;
  border-radius: 0.25rem;
  background: linear-gradient(90deg, #f3f4f6 25%, #e5e7eb 50%, #f3f4f6 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}''',
    ),

    ex(
        "When should I use Tailwind CSS vs CSS Modules in a React 19 project? Show a brief comparison with one example of each for the same Alert component.",
        '''\
/*
  Choose Tailwind when:
  - You want rapid UI iteration with utility classes
  - Design tokens live in tailwind.config (spacing, colors)
  - Team prefers colocated markup + styling in JSX

  Choose CSS Modules when:
  - You want scoped CSS files separate from JSX
  - Designers hand off .css files or you need complex selectors/animations
  - Strict "no utility classes in markup" policy

  Do not mix both in one component unless migrating.
*/

// ── Tailwind version ──
import { type ReactNode } from 'react';

interface AlertProps {
  title: string;
  children?: ReactNode;
}

export function AlertTailwind({ title, children }: AlertProps) {
  return (
    <div
      role="alert"
      className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-amber-900"
    >
      <p className="font-semibold">{title}</p>
      {children && <p className="mt-1 text-sm">{children}</p>}
    </div>
  );
}

// ── CSS Modules version ──
import styles from './Alert.module.css';

export function AlertModules({ title, children }: AlertProps) {
  return (
    <div role="alert" className={styles.alert}>
      <p className={styles.title}>{title}</p>
      {children && <p className={styles.body}>{children}</p>}
    </div>
  );
}

/* Alert.module.css */
.alert {
  border: 1px solid #fde68a;
  border-radius: 0.5rem;
  background: #fffbeb;
  padding: 0.75rem 1rem;
  color: #78350f;
}

.title { margin: 0; font-weight: 600; }

.body { margin: 0.25rem 0 0; font-size: 0.875rem; }''',
    ),
]
