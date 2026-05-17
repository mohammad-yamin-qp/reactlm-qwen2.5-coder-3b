"""SCSS / SCSS Modules training examples."""

from dataset_common import ex

SCSS_EXAMPLES: list[dict] = [
    ex(
        "Build a primary button component using SCSS modules with hover and focus states.",
        '''\
import styles from './Button.module.scss';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
}

export function Button({ variant = 'primary', className = '', children, ...props }: ButtonProps) {
  return (
    <button
      type="button"
      className={`${styles.button} ${styles[variant]} ${className}`.trim()}
      {...props}
    >
      {children}
    </button>
  );
}

/* Button.module.scss */
@use './tokens' as *;

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: $radius-md;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: background-color 150ms ease;

  &:focus-visible {
    outline: 2px solid $color-focus;
    outline-offset: 2px;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.primary {
  background: $color-primary;
  color: #fff;

  &:hover:not(:disabled) {
    filter: brightness(0.92);
  }
}

.secondary {
  background: transparent;
  color: $color-primary;
  border: 1px solid $color-border;

  &:hover:not(:disabled) {
    background: $color-surface-muted;
  }
}

/* tokens.scss */
$color-primary: #2563eb;
$color-focus: #3b82f6;
$color-border: #d1d5db;
$color-surface-muted: #f3f4f6;
$radius-md: 0.375rem;''',
    ),
    ex(
        "Create a responsive card grid with SCSS modules, variables, and a mobile-first breakpoint mixin.",
        '''\
import styles from './ProductGrid.module.scss';

interface Product {
  id: string;
  name: string;
  price: number;
}

export function ProductGrid({ products }: { products: Product[] }) {
  return (
    <ul className={styles.grid}>
      {products.map((p) => (
        <li key={p.id} className={styles.card}>
          <h3 className={styles.title}>{p.name}</h3>
          <p className={styles.price}>${p.price.toFixed(2)}</p>
        </li>
      ))}
    </ul>
  );
}

/* ProductGrid.module.scss */
$breakpoint-md: 768px;

@mixin from-md {
  @media (min-width: $breakpoint-md) {
    @content;
  }
}

.grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
  list-style: none;
  margin: 0;
  padding: 0;

  @include from-md {
    grid-template-columns: repeat(3, 1fr);
  }
}

.card {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
  background: #fff;
}

.title {
  margin: 0 0 0.25rem;
  font-size: 1rem;
  font-weight: 600;
}

.price {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
}''',
    ),
    ex(
        "Implement an accessible modal with SCSS modules, nesting, and backdrop styles.",
        '''\
'use client';

import styles from './Modal.module.scss';

interface ModalProps {
  open: boolean;
  title: string;
  onClose: () => void;
  children: React.ReactNode;
}

export function Modal({ open, title, onClose, children }: ModalProps) {
  if (!open) return null;

  return (
    <div className={styles.overlay} role="presentation" onClick={onClose}>
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className={styles.modal}
        onClick={(e) => e.stopPropagation()}
      >
        <header className={styles.header}>
          <h2 id="modal-title" className={styles.title}>{title}</h2>
          <button type="button" className={styles.close} onClick={onClose} aria-label="Close">
            ×
          </button>
        </header>
        <div className={styles.body}>{children}</div>
      </div>
    </div>
  );
}

/* Modal.module.scss */
.overlay {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgb(0 0 0 / 45%);
  z-index: 50;
}

.modal {
  width: min(100% - 2rem, 32rem);
  background: #fff;
  border-radius: 0.75rem;
  box-shadow: 0 25px 50px -12px rgb(0 0 0 / 25%);
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
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  color: #6b7280;
}

.body {
  padding: 1.25rem;
}''',
    ),
    ex(
        "Build a login form with SCSS modules, nested field styles, and error state modifiers.",
        '''\
'use client';

import styles from './LoginForm.module.scss';

export function LoginForm() {
  return (
    <form className={styles.form} noValidate>
      <div className={styles.field}>
        <label htmlFor="email" className={styles.label}>Email</label>
        <input id="email" name="email" type="email" className={styles.input} required />
      </div>
      <div className={styles.field}>
        <label htmlFor="password" className={styles.label}>Password</label>
        <input id="password" name="password" type="password" className={styles.input} required />
      </div>
      <button type="submit" className={styles.submit}>Sign in</button>
    </form>
  );
}

/* LoginForm.module.scss */
.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 24rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.input {
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.5rem 0.75rem;
  font-size: 1rem;

  &:focus {
    outline: 2px solid #3b82f6;
    border-color: #3b82f6;
  }

  &.error {
    border-color: #dc2626;
  }
}

.submit {
  margin-top: 0.5rem;
  padding: 0.625rem 1rem;
  border: none;
  border-radius: 0.375rem;
  background: #2563eb;
  color: #fff;
  font-weight: 600;
  cursor: pointer;

  &:hover {
    background: #1d4ed8;
  }
}''',
    ),
    ex(
        "Create a dark theme toggle using SCSS variables and a global :root class on the document.",
        '''\
'use client';

import { useEffect, useState } from 'react';
import styles from './ThemeToggle.module.scss';

export function ThemeToggle() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle('theme-dark', dark);
  }, [dark]);

  return (
    <button
      type="button"
      className={`${styles.toggle} ${dark ? styles.isDark : ''}`}
      onClick={() => setDark((d) => !d)}
      aria-pressed={dark}
    >
      {dark ? 'Light mode' : 'Dark mode'}
    </button>
  );
}

/* ThemeToggle.module.scss */
.toggle {
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
}

.isDark {
  background: #1f2937;
  color: #f9fafb;
}

/* globals.scss — import once in app entry */
:root {
  --surface: #ffffff;
  --text: #111827;
  --border: #e5e7eb;
}

:root.theme-dark {
  --surface: #111827;
  --text: #f9fafb;
  --border: #374151;
}''',
    ),
    ex(
        "When should I use Tailwind vs SCSS modules vs plain CSS modules in React?",
        '''\
/*
  Tailwind: utility-first, fastest iteration in JSX, great with shadcn.
  SCSS modules: scoped styles + variables, mixins, nesting — ideal for design systems with Sass.
  CSS modules (.module.css): same scoping as SCSS modules without Sass features.

  Pick one approach per component. Do not mix Tailwind utilities with SCSS module classes on the same element.
*/

// SCSS modules example — use when team already uses Sass
import styles from './Badge.module.scss';

export function BadgeScss({ children }: { children: React.ReactNode }) {
  return <span className={styles.badge}>{children}</span>;
}

/* Badge.module.scss */
$badge-bg: #dbeafe;
$badge-text: #1e40af;

.badge {
  display: inline-block;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  background: $badge-bg;
  color: $badge-text;
}''',
    ),
]
