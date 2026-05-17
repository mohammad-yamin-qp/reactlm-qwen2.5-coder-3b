"""Migrated seeds from augment_dataset."""

from dataset_common import ex

EXTRA_SEEDS: list[dict] = [

    ex(
        "Create a useLocalStorage hook in TypeScript that syncs state to localStorage.",
        '''\
'use client';

import { useState, useCallback, useEffect } from 'react';

function readStorage<T>(key: string, fallback: T): T {
  try {
    const item = window.localStorage.getItem(key);
    return item !== null ? (JSON.parse(item) as T) : fallback;
  } catch {
    return fallback;
  }
}

export function useLocalStorage<T>(key: string, initialValue: T): [T, (v: T | ((prev: T) => T)) => void] {
  const [value, setValue] = useState<T>(() => readStorage(key, initialValue));

  useEffect(() => {
    function onStorage(e: StorageEvent) {
      if (e.key === key && e.newValue !== null) {
        setValue(JSON.parse(e.newValue) as T);
      }
    }
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, [key]);

  const set = useCallback(
    (action: T | ((prev: T) => T)) => {
      setValue((prev) => {
        const next = typeof action === 'function' ? (action as (p: T) => T)(prev) : action;
        try { window.localStorage.setItem(key, JSON.stringify(next)); } catch {}
        return next;
      });
    },
    [key],
  );

  return [value, set];
}''',
    ),

    ex(
        "Build a useMediaQuery hook that returns true when a CSS media query matches.",
        '''\
'use client';

import { useState, useEffect } from 'react';

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mql = window.matchMedia(query);
    setMatches(mql.matches);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mql.addEventListener('change', handler);
    return () => mql.removeEventListener('change', handler);
  }, [query]);

  return matches;
}

// Usage:
// const isMobile = useMediaQuery('(max-width: 768px)');
// const prefersReducedMotion = useMediaQuery('(prefers-reduced-motion: reduce)');
// const isDarkMode = useMediaQuery('(prefers-color-scheme: dark)');''',
    ),

    ex(
        "Create a useOnClickOutside hook that calls a handler when the user clicks outside a ref element.",
        '''\
'use client';

import { useEffect, type RefObject } from 'react';

export function useOnClickOutside<T extends HTMLElement>(
  ref: RefObject<T>,
  handler: (event: MouseEvent | TouchEvent) => void,
): void {
  useEffect(() => {
    function listener(e: MouseEvent | TouchEvent) {
      if (!ref.current || ref.current.contains(e.target as Node)) return;
      handler(e);
    }
    document.addEventListener('mousedown', listener);
    document.addEventListener('touchstart', listener);
    return () => {
      document.removeEventListener('mousedown', listener);
      document.removeEventListener('touchstart', listener);
    };
  }, [ref, handler]);
}''',
    ),

    ex(
        "Write a useToggle hook with TypeScript that returns a boolean and a stable toggle function.",
        '''\
'use client';

import { useState, useCallback } from 'react';

export function useToggle(initial = false): [boolean, () => void, (v: boolean) => void] {
  const [value, setValue] = useState(initial);
  const toggle = useCallback(() => setValue((v) => !v), []);
  const set = useCallback((v: boolean) => setValue(v), []);
  return [value, toggle, set];
}

// Usage:
// const [isOpen, toggleOpen, setOpen] = useToggle(false);
// <button onClick={toggleOpen}>Toggle</button>
// <button onClick={() => setOpen(false)}>Close</button>''',
    ),

    ex(
        "Build a useDebounce hook that returns a debounced version of a value.",
        '''\
'use client';

import { useState, useEffect } from 'react';

export function useDebounce<T>(value: T, delayMs: number): T {
  const [debounced, setDebounced] = useState<T>(value);

  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delayMs);
    return () => clearTimeout(id);
  }, [value, delayMs]);

  return debounced;
}

// Usage in a search component:
// const [search, setSearch] = useState('');
// const debouncedSearch = useDebounce(search, 300);
// useEffect(() => { fetchResults(debouncedSearch); }, [debouncedSearch]);''',
    ),

    ex(
        "Create a useAsyncFn hook that wraps an async function and tracks its loading, error, and value states.",
        '''\
'use client';

import { useState, useCallback } from 'react';

type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; value: T }
  | { status: 'error'; error: Error };

type AsyncFn<T, Args extends unknown[]> = (...args: Args) => Promise<T>;

export function useAsyncFn<T, Args extends unknown[]>(
  fn: AsyncFn<T, Args>,
): [AsyncState<T>, (...args: Args) => Promise<void>] {
  const [state, setState] = useState<AsyncState<T>>({ status: 'idle' });

  const execute = useCallback(
    async (...args: Args) => {
      setState({ status: 'loading' });
      try {
        const value = await fn(...args);
        setState({ status: 'success', value });
      } catch (err) {
        setState({ status: 'error', error: err instanceof Error ? err : new Error(String(err)) });
      }
    },
    [fn],
  );

  return [state, execute];
}''',
    ),

    ex(
        "Write a usePrevious hook that returns the previous value of a variable across renders.",
        '''\
'use client';

import { useRef, useEffect } from 'react';

export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

// Usage: animate transitions between values
// const prevCount = usePrevious(count);
// const direction = count > (prevCount ?? count) ? 'up' : 'down';''',
    ),

    ex(
        "Create a useIntersectionObserver hook for detecting when an element enters the viewport.",
        '''\
'use client';

import { useState, useEffect, useRef, type RefObject } from 'react';

interface UseIntersectionObserverOptions extends IntersectionObserverInit {
  freezeOnceVisible?: boolean;
}

export function useIntersectionObserver(
  options: UseIntersectionObserverOptions = {},
): [RefObject<HTMLDivElement>, boolean] {
  const { freezeOnceVisible = false, ...observerOptions } = options;
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (freezeOnceVisible && isVisible) return;

    const observer = new IntersectionObserver(([entry]) => {
      setIsVisible(entry.isIntersecting);
    }, observerOptions);

    observer.observe(el);
    return () => observer.disconnect();
  }, [freezeOnceVisible, isVisible, JSON.stringify(observerOptions)]);

  return [ref, isVisible];
}''',
    ),

    ex(
        "Build a useClipboard hook that copies text and resets the copied state after a timeout.",
        '''\
'use client';

import { useState, useCallback } from 'react';

interface UseClipboardResult {
  copy: (text: string) => Promise<void>;
  copied: boolean;
  error: Error | null;
}

export function useClipboard(resetMs = 2000): UseClipboardResult {
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const copy = useCallback(async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setError(null);
      setTimeout(() => setCopied(false), resetMs);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Copy failed'));
    }
  }, [resetMs]);

  return { copy, copied, error };
}

// Usage:
// const { copy, copied } = useClipboard();
// <button onClick={() => copy(apiKey)}>{copied ? 'Copied!' : 'Copy'}</button>''',
    ),

    ex(
        "Create a useKeyboard hook that fires a callback when a specific key combination is pressed.",
        '''\
'use client';

import { useEffect, useCallback } from 'react';

interface KeyCombo {
  key: string;
  ctrl?: boolean;
  meta?: boolean;
  shift?: boolean;
  alt?: boolean;
}

export function useKeyboard(combo: KeyCombo, handler: (e: KeyboardEvent) => void): void {
  const stableHandler = useCallback(handler, [handler]);

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      const match =
        e.key.toLowerCase() === combo.key.toLowerCase() &&
        !!combo.ctrl === e.ctrlKey &&
        !!combo.meta === e.metaKey &&
        !!combo.shift === e.shiftKey &&
        !!combo.alt === e.altKey;
      if (match) stableHandler(e);
    }
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [combo.key, combo.ctrl, combo.meta, combo.shift, combo.alt, stableHandler]);
}

// Usage:
// useKeyboard({ key: 'k', meta: true }, (e) => { e.preventDefault(); openCommandPalette(); });''',
    ),

    ex(
        "Write a useInterval hook that runs a callback on a fixed interval and cleans up on unmount.",
        '''\
'use client';

import { useEffect, useRef } from 'react';

export function useInterval(callback: () => void, delayMs: number | null): void {
  const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (delayMs === null) return;
    const id = setInterval(() => savedCallback.current(), delayMs);
    return () => clearInterval(id);
  }, [delayMs]);
}

// Usage:
// const [count, setCount] = useState(0);
// useInterval(() => setCount((c) => c + 1), 1000); // pause by passing null''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section B: Form patterns
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Create a file upload input with drag-and-drop support and file type validation in TypeScript.",
        '''\
'use client';

import { useState, useRef, useCallback, type DragEvent } from 'react';

interface FileUploadProps {
  accept: string[];
  maxSizeMb?: number;
  onFiles: (files: File[]) => void;
}

export function FileUpload({ accept, maxSizeMb = 5, onFiles }: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const validate = useCallback((files: FileList | null): File[] | null => {
    if (!files || files.length === 0) return null;
    const arr = Array.from(files);
    const invalid = arr.filter((f) => !accept.some((a) => f.type === a || f.name.endsWith(a)));
    if (invalid.length > 0) {
      setError(`Invalid file type. Allowed: ${accept.join(', ')}`);
      return null;
    }
    const tooBig = arr.filter((f) => f.size > maxSizeMb * 1024 * 1024);
    if (tooBig.length > 0) {
      setError(`File too large. Max size: ${maxSizeMb}MB`);
      return null;
    }
    setError(null);
    return arr;
  }, [accept, maxSizeMb]);

  function handleDrop(e: DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setIsDragging(false);
    const valid = validate(e.dataTransfer.files);
    if (valid) onFiles(valid);
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const valid = validate(e.target.files);
    if (valid) onFiles(valid);
  }

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') inputRef.current?.click(); }}
      aria-label={`Upload files. Accepted: ${accept.join(', ')}. Max ${maxSizeMb}MB.`}
      style={{ border: `2px dashed ${isDragging ? '#0070f3' : '#ccc'}`, padding: '2rem', cursor: 'pointer' }}
    >
      <input
        ref={inputRef}
        type="file"
        accept={accept.join(',')}
        multiple
        onChange={handleChange}
        style={{ display: 'none' }}
        aria-hidden="true"
      />
      <p>{isDragging ? 'Drop files here' : 'Drag & drop or click to select files'}</p>
      {error && <p role="alert" style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}''',
    ),

    ex(
        "Build a tag input component that lets users add and remove text tags with keyboard support.",
        '''\
'use client';

import { useState, useId, type KeyboardEvent } from 'react';

interface TagInputProps {
  label: string;
  value: string[];
  onChange: (tags: string[]) => void;
  placeholder?: string;
  maxTags?: number;
}

export function TagInput({ label, value: tags, onChange, placeholder = 'Add tag…', maxTags }: TagInputProps) {
  const [input, setInput] = useState('');
  const inputId = useId();

  function addTag(raw: string) {
    const tag = raw.trim().toLowerCase();
    if (!tag || tags.includes(tag)) return;
    if (maxTags && tags.length >= maxTags) return;
    onChange([...tags, tag]);
    setInput('');
  }

  function removeTag(index: number) {
    onChange(tags.filter((_, i) => i !== index));
  }

  function handleKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter' || e.key === ',') { e.preventDefault(); addTag(input); }
    if (e.key === 'Backspace' && input === '' && tags.length > 0) removeTag(tags.length - 1);
  }

  return (
    <div>
      <label htmlFor={inputId}>{label}</label>
      <div role="group" aria-label={`${label} tags`} style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
        {tags.map((tag, i) => (
          <span key={tag} style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
            {tag}
            <button
              type="button"
              onClick={() => removeTag(i)}
              aria-label={`Remove tag: ${tag}`}
            >
              ×
            </button>
          </span>
        ))}
        <input
          id={inputId}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={() => addTag(input)}
          placeholder={maxTags && tags.length >= maxTags ? `Max ${maxTags} tags` : placeholder}
          disabled={!!(maxTags && tags.length >= maxTags)}
          aria-label={`Add ${label} tag. Press Enter or comma to add.`}
        />
      </div>
    </div>
  );
}''',
    ),

    ex(
        "Create a character-count textarea that warns when approaching the limit and prevents overflow.",
        '''\
'use client';

import { useState, useId } from 'react';

interface CharCountTextareaProps {
  label: string;
  name: string;
  maxLength: number;
  warnAt?: number;
  rows?: number;
  required?: boolean;
}

export function CharCountTextarea({
  label,
  name,
  maxLength,
  warnAt = Math.floor(maxLength * 0.8),
  rows = 4,
  required,
}: CharCountTextareaProps) {
  const [value, setValue] = useState('');
  const id = useId();
  const countId = useId();
  const remaining = maxLength - value.length;
  const isWarning = remaining <= maxLength - warnAt;
  const isAtLimit = remaining === 0;

  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <textarea
        id={id}
        name={name}
        value={value}
        onChange={(e) => setValue(e.target.value.slice(0, maxLength))}
        rows={rows}
        required={required}
        aria-required={required}
        aria-describedby={countId}
        aria-invalid={isAtLimit}
        maxLength={maxLength}
      />
      <span
        id={countId}
        aria-live="polite"
        aria-atomic="true"
        style={{ color: isAtLimit ? 'red' : isWarning ? 'orange' : 'inherit' }}
      >
        {isAtLimit
          ? 'Character limit reached'
          : `${remaining} character${remaining !== 1 ? 's' : ''} remaining`}
      </span>
    </div>
  );
}''',
    ),

    ex(
        "Write a rating input component (1–5 stars) that is keyboard-accessible and screen-reader-friendly.",
        '''\
'use client';

import { useState, useId } from 'react';

interface RatingInputProps {
  name: string;
  label: string;
  value?: number;
  onChange?: (rating: number) => void;
}

export function RatingInput({ name, label, value = 0, onChange }: RatingInputProps) {
  const [hover, setHover] = useState(0);
  const groupId = useId();
  const display = hover || value;

  return (
    <fieldset aria-labelledby={groupId} style={{ border: 'none', padding: 0 }}>
      <legend id={groupId}>{label}</legend>
      <div role="group" aria-label={`${label}: ${value} out of 5 stars`}>
        {[1, 2, 3, 4, 5].map((star) => (
          <label key={star} style={{ cursor: 'pointer', fontSize: '1.5rem' }}>
            <input
              type="radio"
              name={name}
              value={star}
              checked={value === star}
              onChange={() => onChange?.(star)}
              onFocus={() => setHover(star)}
              onBlur={() => setHover(0)}
              style={{ position: 'absolute', opacity: 0, width: 0 }}
              aria-label={`${star} star${star !== 1 ? 's' : ''}`}
            />
            <span
              aria-hidden="true"
              onMouseEnter={() => setHover(star)}
              onMouseLeave={() => setHover(0)}
              onClick={() => onChange?.(star)}
              style={{ color: star <= display ? '#f59e0b' : '#d1d5db' }}
            >
              ★
            </span>
          </label>
        ))}
      </div>
    </fieldset>
  );
}''',
    ),

    ex(
        "Create a toggle switch component with proper ARIA role and keyboard interaction.",
        '''\
'use client';

import { useId } from 'react';

interface ToggleSwitchProps {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  disabled?: boolean;
  description?: string;
}

export function ToggleSwitch({ label, checked, onChange, disabled, description }: ToggleSwitchProps) {
  const switchId = useId();
  const descId = useId();

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <button
        role="switch"
        id={switchId}
        aria-checked={checked}
        aria-disabled={disabled}
        aria-describedby={description ? descId : undefined}
        onClick={() => !disabled && onChange(!checked)}
        onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); !disabled && onChange(!checked); } }}
        disabled={disabled}
        style={{
          width: 44,
          height: 24,
          borderRadius: 12,
          background: checked ? '#0070f3' : '#d1d5db',
          border: 'none',
          cursor: disabled ? 'not-allowed' : 'pointer',
          position: 'relative',
          transition: 'background 0.2s',
        }}
      >
        <span
          aria-hidden="true"
          style={{
            position: 'absolute',
            top: 2,
            left: checked ? 22 : 2,
            width: 20,
            height: 20,
            borderRadius: '50%',
            background: '#fff',
            transition: 'left 0.2s',
          }}
        />
      </button>
      <label htmlFor={switchId} style={{ cursor: disabled ? 'not-allowed' : 'pointer' }}>
        {label}
      </label>
      {description && <span id={descId} style={{ fontSize: '0.875rem', color: '#6b7280' }}>{description}</span>}
    </div>
  );
}''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section C: Layout and navigation
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Build a Breadcrumb component that generates structured navigation from a path array.",
        '''\

interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
}

export function Breadcrumb({ items }: BreadcrumbProps) {
  return (
    <nav aria-label="Breadcrumb">
      <ol style={{ display: 'flex', listStyle: 'none', gap: 4, padding: 0, flexWrap: 'wrap' }}>
        {items.map((item, index) => {
          const isLast = index === items.length - 1;
          return (
            <li key={index} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              {!isLast && item.href ? (
                <>
                  <a href={item.href}>{item.label}</a>
                  <span aria-hidden="true">/</span>
                </>
              ) : (
                <span aria-current={isLast ? 'page' : undefined}>{item.label}</span>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

// Usage:
// <Breadcrumb items={[
//   { label: 'Home', href: '/' },
//   { label: 'Products', href: '/products' },
//   { label: 'Shoes' },   ← current page, no href
// ]} />''',
    ),

    ex(
        "Create a scroll-to-top button that appears after scrolling 300px and smoothly scrolls back to the top.",
        '''\
'use client';

import { useState, useEffect } from 'react';

export function ScrollToTop() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    function onScroll() {
      setVisible(window.scrollY > 300);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  if (!visible) return null;

  return (
    <button
      type="button"
      onClick={scrollToTop}
      aria-label="Scroll to top of page"
      style={{
        position: 'fixed',
        bottom: '2rem',
        right: '2rem',
        width: 44,
        height: 44,
        borderRadius: '50%',
        background: '#0070f3',
        color: '#fff',
        border: 'none',
        cursor: 'pointer',
        fontSize: '1.25rem',
      }}
    >
      ↑
    </button>
  );
}''',
    ),

    ex(
        "Build a command palette (Cmd+K) component with fuzzy search over a list of actions.",
        '''\
'use client';

import { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { createPortal } from 'react-dom';

interface Command {
  id: string;
  label: string;
  description?: string;
  onSelect: () => void;
}

interface CommandPaletteProps {
  commands: Command[];
}

function fuzzy(query: string, target: string): boolean {
  const q = query.toLowerCase();
  const t = target.toLowerCase();
  let qi = 0;
  for (let i = 0; i < t.length && qi < q.length; i++) {
    if (t[i] === q[qi]) qi++;
  }
  return qi === q.length;
}

export function CommandPalette({ commands }: CommandPaletteProps) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [activeIdx, setActiveIdx] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setOpen((o) => !o);
        setQuery('');
        setActiveIdx(0);
      }
      if (e.key === 'Escape') setOpen(false);
    }
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  useEffect(() => { if (open) setTimeout(() => inputRef.current?.focus(), 0); }, [open]);

  const filtered = useMemo(
    () => commands.filter((c) => !query || fuzzy(query, c.label)),
    [commands, query],
  );

  function handleKey(e: React.KeyboardEvent) {
    if (e.key === 'ArrowDown') { e.preventDefault(); setActiveIdx((i) => Math.min(i + 1, filtered.length - 1)); }
    if (e.key === 'ArrowUp')   { e.preventDefault(); setActiveIdx((i) => Math.max(i - 1, 0)); }
    if (e.key === 'Enter' && filtered[activeIdx]) { filtered[activeIdx].onSelect(); setOpen(false); }
  }

  if (!open) return null;

  return createPortal(
    <div
      role="presentation"
      style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)', zIndex: 9999 }}
      onClick={(e) => { if (e.target === e.currentTarget) setOpen(false); }}
    >
      <div
        role="dialog"
        aria-label="Command palette"
        aria-modal="true"
        style={{ background: '#fff', borderRadius: 8, maxWidth: 560, margin: '10vh auto', overflow: 'hidden' }}
      >
        <input
          ref={inputRef}
          role="combobox"
          aria-expanded={filtered.length > 0}
          aria-controls="cmd-list"
          aria-autocomplete="list"
          value={query}
          onChange={(e) => { setQuery(e.target.value); setActiveIdx(0); }}
          onKeyDown={handleKey}
          placeholder="Search commands…"
          style={{ width: '100%', padding: '1rem', border: 'none', borderBottom: '1px solid #e5e7eb', fontSize: '1rem' }}
        />
        <ul id="cmd-list" role="listbox" aria-label="Commands" style={{ margin: 0, padding: '0.5rem', listStyle: 'none', maxHeight: 360, overflowY: 'auto' }}>
          {filtered.map((cmd, i) => (
            <li
              key={cmd.id}
              role="option"
              aria-selected={i === activeIdx}
              onMouseEnter={() => setActiveIdx(i)}
              onClick={() => { cmd.onSelect(); setOpen(false); }}
              style={{ padding: '0.75rem', borderRadius: 6, background: i === activeIdx ? '#eff6ff' : undefined, cursor: 'pointer' }}
            >
              <span style={{ fontWeight: 500 }}>{cmd.label}</span>
              {cmd.description && <span style={{ marginLeft: 8, color: '#6b7280', fontSize: '0.875rem' }}>{cmd.description}</span>}
            </li>
          ))}
          {filtered.length === 0 && <li style={{ padding: '0.75rem', color: '#6b7280' }}>No commands found.</li>}
        </ul>
      </div>
    </div>,
    document.body,
  );
}''',
    ),

    ex(
        "Create a Pagination component with first/prev/next/last controls and accessible page labels.",
        '''\
interface PaginationProps {
  page: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  siblingCount?: number;
}

function range(start: number, end: number): number[] {
  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
}

export function Pagination({ page, totalPages, onPageChange, siblingCount = 1 }: PaginationProps) {
  if (totalPages <= 1) return null;

  const sibs = Math.min(siblingCount, totalPages);
  const leftSib  = Math.max(page - sibs, 2);
  const rightSib = Math.min(page + sibs, totalPages - 1);
  const showLeftDots  = leftSib > 2;
  const showRightDots = rightSib < totalPages - 1;

  const pages: (number | '…')[] = [
    1,
    ...(showLeftDots ? ['…' as const] : []),
    ...range(leftSib, rightSib),
    ...(showRightDots ? ['…' as const] : []),
    totalPages,
  ];

  return (
    <nav aria-label="Pagination">
      <ul style={{ display: 'flex', listStyle: 'none', gap: 4, padding: 0 }}>
        <li>
          <button onClick={() => onPageChange(1)} disabled={page === 1} aria-label="First page">«</button>
        </li>
        <li>
          <button onClick={() => onPageChange(page - 1)} disabled={page === 1} aria-label="Previous page">‹</button>
        </li>
        {pages.map((p, i) =>
          p === '…' ? (
            <li key={`dots-${i}`} aria-hidden="true"><span>…</span></li>
          ) : (
            <li key={p}>
              <button
                onClick={() => onPageChange(p)}
                aria-current={page === p ? 'page' : undefined}
                aria-label={`Page ${p}`}
                style={{ fontWeight: page === p ? 700 : undefined }}
              >
                {p}
              </button>
            </li>
          )
        )}
        <li>
          <button onClick={() => onPageChange(page + 1)} disabled={page === totalPages} aria-label="Next page">›</button>
        </li>
        <li>
          <button onClick={() => onPageChange(totalPages)} disabled={page === totalPages} aria-label="Last page">»</button>
        </li>
      </ul>
    </nav>
  );
}''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section D: Loading / error / empty states
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Create a skeleton screen loader component that matches a card layout.",
        '''\
interface SkeletonProps {
  width?: string | number;
  height?: string | number;
  borderRadius?: string | number;
  className?: string;
}

function Skeleton({ width = '100%', height = 16, borderRadius = 4 }: SkeletonProps) {
  return (
    <div
      aria-hidden="true"
      style={{
        width,
        height,
        borderRadius,
        background: 'linear-gradient(90deg, #e5e7eb 25%, #f3f4f6 50%, #e5e7eb 75%)',
        backgroundSize: '200% 100%',
        animation: 'shimmer 1.5s infinite',
      }}
    />
  );
}

export function CardSkeleton() {
  return (
    <div
      role="status"
      aria-label="Loading card content"
      style={{ padding: '1rem', border: '1px solid #e5e7eb', borderRadius: 8 }}
    >
      <Skeleton width={64} height={64} borderRadius="50%" />
      <div style={{ marginTop: 12, display: 'flex', flexDirection: 'column', gap: 8 }}>
        <Skeleton width="60%" height={18} />
        <Skeleton width="90%" height={14} />
        <Skeleton width="75%" height={14} />
      </div>
      <span className="sr-only">Loading…</span>
    </div>
  );
}

// In globals.css:
// @keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }''',
    ),

    ex(
        "Build an empty state component with an optional call-to-action button.",
        '''\
import type { ReactNode } from 'react';

interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export function EmptyState({ icon, title, description, action }: EmptyStateProps) {
  return (
    <div
      role="status"
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '3rem 1rem',
        textAlign: 'center',
        color: '#6b7280',
      }}
    >
      {icon && <div aria-hidden="true" style={{ fontSize: '3rem', marginBottom: '1rem' }}>{icon}</div>}
      <h2 style={{ fontSize: '1.125rem', fontWeight: 600, color: '#111827', margin: 0 }}>{title}</h2>
      {description && <p style={{ marginTop: '0.5rem', maxWidth: 360 }}>{description}</p>}
      {action && (
        <button
          type="button"
          onClick={action.onClick}
          style={{ marginTop: '1.5rem' }}
        >
          {action.label}
        </button>
      )}
    </div>
  );
}

// Usage:
// <EmptyState
//   icon="📋"
//   title="No tasks yet"
//   description="Create your first task to get started."
//   action={{ label: 'New task', onClick: openCreateDialog }}
// />''',
    ),

    ex(
        "Create a network-offline banner that appears automatically when the user loses internet connection.",
        '''\
'use client';

import { useState, useEffect } from 'react';

export function OfflineBanner() {
  const [offline, setOffline] = useState(false);

  useEffect(() => {
    setOffline(!navigator.onLine);
    function onOnline()  { setOffline(false); }
    function onOffline() { setOffline(true); }
    window.addEventListener('online',  onOnline);
    window.addEventListener('offline', onOffline);
    return () => {
      window.removeEventListener('online',  onOnline);
      window.removeEventListener('offline', onOffline);
    };
  }, []);

  if (!offline) return null;

  return (
    <div
      role="status"
      aria-live="assertive"
      aria-atomic="true"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        background: '#fef3c7',
        color: '#92400e',
        textAlign: 'center',
        padding: '0.5rem 1rem',
        zIndex: 9999,
        fontWeight: 500,
      }}
    >
      You are offline. Some features may not be available.
    </div>
  );
}''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section E: Advanced TypeScript
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Create a type-safe event emitter in TypeScript with generic event maps.",
        '''\
type EventMap = Record<string, unknown[]>;

class TypedEventEmitter<Events extends EventMap> {
  private listeners = new Map<keyof Events, Set<(...args: unknown[]) => void>>();

  on<K extends keyof Events>(event: K, listener: (...args: Events[K]) => void): () => void {
    const set = this.listeners.get(event) ?? new Set();
    set.add(listener as (...args: unknown[]) => void);
    this.listeners.set(event, set);
    return () => this.off(event, listener);
  }

  off<K extends keyof Events>(event: K, listener: (...args: Events[K]) => void): void {
    this.listeners.get(event)?.delete(listener as (...args: unknown[]) => void);
  }

  emit<K extends keyof Events>(event: K, ...args: Events[K]): void {
    this.listeners.get(event)?.forEach((l) => l(...args));
  }
}

// Usage in a React context:
interface AppEvents extends EventMap {
  'cart:add':    [productId: string, quantity: number];
  'cart:remove': [productId: string];
  'user:logout': [];
  'toast:show':  [message: string, type: 'success' | 'error'];
}

export const appBus = new TypedEventEmitter<AppEvents>();

// appBus.on('cart:add', (productId, quantity) => { ... }); // fully typed
// appBus.emit('toast:show', 'Saved!', 'success');''',
    ),

    ex(
        "Write a DeepReadonly utility type and a deepFreeze function in TypeScript.",
        '''\
type DeepReadonly<T> =
  T extends (infer U)[]
    ? ReadonlyArray<DeepReadonly<U>>
    : T extends object
    ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
    : T;

type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

function deepFreeze<T extends object>(obj: T): DeepReadonly<T> {
  Object.getOwnPropertyNames(obj).forEach((name) => {
    const value = (obj as Record<string, unknown>)[name];
    if (typeof value === 'object' && value !== null) {
      deepFreeze(value as object);
    }
  });
  return Object.freeze(obj) as DeepReadonly<T>;
}

// Usage — config objects that must never mutate:
interface Config {
  api: { baseUrl: string; timeout: number };
  features: { darkMode: boolean; analytics: boolean };
}

const CONFIG: DeepReadonly<Config> = deepFreeze({
  api: { baseUrl: 'https://api.example.com', timeout: 5000 },
  features: { darkMode: true, analytics: false },
});

// CONFIG.api.baseUrl = '...'; // TypeScript error — readonly''',
    ),

    ex(
        "Implement a type-safe builder pattern for constructing complex query objects in TypeScript.",
        '''\
interface QueryOptions {
  filters: Record<string, string | number | boolean>;
  sort: { field: string; direction: 'asc' | 'desc' };
  pagination: { page: number; pageSize: number };
  include: string[];
}

class QueryBuilder {
  private opts: Partial<QueryOptions> = {};

  where(field: string, value: string | number | boolean): this {
    this.opts.filters = { ...this.opts.filters, [field]: value };
    return this;
  }

  orderBy(field: string, direction: 'asc' | 'desc' = 'asc'): this {
    this.opts.sort = { field, direction };
    return this;
  }

  paginate(page: number, pageSize: number): this {
    this.opts.pagination = { page, pageSize };
    return this;
  }

  with(...relations: string[]): this {
    this.opts.include = [...(this.opts.include ?? []), ...relations];
    return this;
  }

  build(): QueryOptions {
    return {
      filters:    this.opts.filters ?? {},
      sort:       this.opts.sort ?? { field: 'createdAt', direction: 'desc' },
      pagination: this.opts.pagination ?? { page: 1, pageSize: 20 },
      include:    this.opts.include ?? [],
    };
  }
}

// Usage:
// const query = new QueryBuilder()
//   .where('status', 'active')
//   .where('role', 'admin')
//   .orderBy('name')
//   .paginate(1, 10)
//   .with('profile', 'roles')
//   .build();''',
    ),

    ex(
        "Create conditional prop types in TypeScript: a component that requires an href when used as a link, but not otherwise.",
        '''\
import type { ComponentPropsWithoutRef } from 'react';

// When variant is 'link', href is required. For all other variants, href must be absent.
type ButtonVariant = 'primary' | 'secondary' | 'danger';

type ButtonProps =
  | (ComponentPropsWithoutRef<'button'> & {
      variant?: ButtonVariant;
      href?: never;
    })
  | (ComponentPropsWithoutRef<'a'> & {
      variant?: ButtonVariant;
      href: string;
      external?: boolean;
    });

export function Button(props: ButtonProps) {
  if ('href' in props && props.href !== undefined) {
    const { href, external, variant = 'primary', children, ...rest } = props;
    return (
      <a
        href={href}
        className={`btn btn-${variant}`}
        {...(external ? { target: '_blank', rel: 'noopener noreferrer' } : {})}
        {...rest}
      >
        {children}
        {external && <span aria-label=" (opens in new tab)"> ↗</span>}
      </a>
    );
  }

  const { variant = 'primary', children, type = 'button', ...rest } = props;
  return (
    <button type={type} className={`btn btn-${variant}`} {...rest}>
      {children}
    </button>
  );
}

// TypeScript enforces:
// <Button href="/about">Link</Button>       ✓
// <Button onClick={...}>Click me</Button>   ✓
// <Button>No href, no onClick</Button>      ✓
// <Button href="">Empty href</Button>       ✓ (valid anchor)''',
    ),

    ex(
        "Write a generic useReducer with middleware support (logging, analytics) in TypeScript.",
        '''\
'use client';

import { useReducer, useCallback } from 'react';

type Reducer<S, A> = (state: S, action: A) => S;
type Middleware<S, A> = (state: S, action: A, next: (action: A) => void) => void;

function applyMiddleware<S, A>(
  reducer: Reducer<S, A>,
  middlewares: Middleware<S, A>[],
): Reducer<S, A> {
  return (state: S, action: A) => {
    let dispatched = false;
    let nextState = state;

    const chain = middlewares.reduceRight(
      (next: (a: A) => void, mw: Middleware<S, A>) =>
        (a: A) => mw(state, a, next),
      (a: A) => {
        nextState = reducer(state, a);
        dispatched = true;
      },
    );

    chain(action);
    return dispatched ? nextState : reducer(state, action);
  };
}

// Cart example
interface CartState { items: string[]; total: number }
type CartAction = { type: 'ADD'; item: string } | { type: 'CLEAR' }

const cartReducer: Reducer<CartState, CartAction> = (state, action) => {
  if (action.type === 'ADD')  return { ...state, items: [...state.items, action.item] };
  if (action.type === 'CLEAR') return { items: [], total: 0 };
  return state;
};

const logger: Middleware<CartState, CartAction> = (state, action, next) => {
  console.log('[cart]', action.type, state);
  next(action);
};

export function useCartReducer() {
  const enhancedReducer = applyMiddleware(cartReducer, [logger]);
  return useReducer(enhancedReducer, { items: [], total: 0 });
}''',
    ),

    ex(
        "Create branded/nominal types in TypeScript to prevent mixing up IDs of different entity types.",
        '''\
// Nominal typing with a brand — prevents passing a UserId where ProductId is expected
type Brand<T, B extends string> = T & { readonly __brand: B };

export type UserId    = Brand<string, 'UserId'>;
export type ProductId = Brand<string, 'ProductId'>;
export type OrderId   = Brand<string, 'OrderId'>;

// Constructor functions that assert the brand
export const UserId    = (id: string) => id as UserId;
export const ProductId = (id: string) => id as ProductId;
export const OrderId   = (id: string) => id as OrderId;

// Functions that now reject wrong ID types at compile time
async function getUser(id: UserId): Promise<{ id: UserId; name: string }> {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
}

async function getProduct(id: ProductId): Promise<{ id: ProductId; name: string }> {
  const res = await fetch(`/api/products/${id}`);
  return res.json();
}

// Safe:
const uid = UserId('user-123');
getUser(uid);   // ✓

// TypeScript compile error — cannot pass ProductId where UserId is expected:
// const pid = ProductId('prod-456');
// getUser(pid);  // ✗ Type 'ProductId' is not assignable to parameter of type 'UserId'.''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section F: React 19 advanced patterns
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Show how to use React 19 Server Actions with useTransition for non-form mutations.",
        '''\
// actions/archive.ts
'use server';


export async function archivePost(postId: string): Promise<{ success: boolean; message: string }> {
  const res = await fetch(`${process.env.API_URL}/posts/${postId}/archive`, { method: 'POST' });
  if (!res.ok) return { success: false, message: 'Failed to archive post.' };
  // // // // revalidatePath('/posts');
  return { success: true, message: 'Post archived.' };
}

// components/ArchiveButton.tsx
'use client';

import { useTransition, useState } from 'react';
import { archivePost } from '@/actions/archive';

interface ArchiveButtonProps {
  postId: string;
  onSuccess?: () => void;
}

export function ArchiveButton({ postId, onSuccess }: ArchiveButtonProps) {
  const [isPending, startTransition] = useTransition();
  const [message, setMessage] = useState<string | null>(null);

  function handleClick() {
    startTransition(async () => {
      const result = await archivePost(postId);
      setMessage(result.message);
      if (result.success) onSuccess?.();
    });
  }

  return (
    <>
      <button
        type="button"
        onClick={handleClick}
        disabled={isPending}
        aria-busy={isPending}
      >
        {isPending ? 'Archiving…' : 'Archive post'}
      </button>
      {message && <p role="status" aria-live="polite">{message}</p>}
    </>
  );
}''',
    ),

    ex(
        "Implement a React Server Action that handles file upload and returns a signed URL.",
        '''\
// actions/upload.ts
'use server';

export type UploadResult =
  | { success: true; url: string; fileName: string }
  | { success: false; error: string };

export async function uploadFile(formData: FormData): Promise<UploadResult> {
  const file = formData.get('file') as File | null;
  if (!file) return { success: false, error: 'No file provided.' };

  const MAX = 5 * 1024 * 1024; // 5MB
  if (file.size > MAX) return { success: false, error: 'File must be under 5MB.' };

  const ALLOWED = ['image/jpeg', 'image/png', 'image/webp'];
  if (!ALLOWED.includes(file.type)) return { success: false, error: 'Only JPEG, PNG, and WebP allowed.' };

  const bytes = await file.arrayBuffer();
  const body  = Buffer.from(bytes);

  const res = await fetch(`${process.env.STORAGE_URL}/upload`, {
    method: 'POST',
    headers: { 'Content-Type': file.type, 'X-File-Name': file.name },
    body,
  });

  if (!res.ok) return { success: false, error: 'Upload failed. Please try again.' };

  const { url } = (await res.json()) as { url: string };
  return { success: true, url, fileName: file.name };
}

// components/AvatarUploadForm.tsx
'use client';

import { useActionState } from 'react';
import { uploadFile, type UploadResult } from '@/actions/upload';

const INITIAL: UploadResult | null = null;

export function AvatarUploadForm() {
  const [result, dispatch, isPending] = useActionState<UploadResult | null, FormData>(
    async (_prev, formData) => uploadFile(formData),
    INITIAL,
  );

  return (
    <form action={dispatch} encType="multipart/form-data" aria-label="Upload avatar">
      <label htmlFor="avatar-file">Profile photo (JPEG, PNG, WebP, max 5MB)</label>
      <input id="avatar-file" name="file" type="file" accept="image/jpeg,image/png,image/webp" required />
      {result?.success === false && <p role="alert">{result.error}</p>}
      {result?.success === true  && (
        <p role="status">
          Uploaded! <img src={result.url} alt="New avatar preview" width={80} height={80} />
        </p>
      )}
      <button type="submit" disabled={isPending} aria-busy={isPending}>
        {isPending ? 'Uploading…' : 'Upload photo'}
      </button>
    </form>
  );
}''',
    ),

    ex(
        "Demonstrate progressive enhancement with a Server Action form that works without JavaScript.",
        '''\
// subscribe/actions.ts
'use server';


export async function subscribeAction(formData: FormData): Promise<never> {
  const email = (formData.get('email') as string | null)?.trim() ?? '';
  if (!email || !email.includes('@')) // // // // redirect('/subscribe?error=invalid-email');

  await fetch(`${process.env.API_URL}/newsletter`, {
    method: 'POST',
    body: JSON.stringify({ email }),
    headers: { 'Content-Type': 'application/json' },
  });

  // // // // redirect('/subscribe?success=true');
}

// subscribe/page.tsx — Server Component that works without JS
interface SubscribePageProps {
  searchParams: { error?: string; success?: string };
}

export default function SubscribePage({ searchParams }: SubscribePageProps) {
  const success = searchParams.success === 'true';
  const error   = searchParams.error;

  return (
    <main>
      <h1>Newsletter</h1>

      {success && <p role="status">Subscribed! Check your email.</p>}

      {error === 'invalid-email' && (
        <p role="alert">Please enter a valid email address.</p>
      )}

      {/* Works with JS (Server Action dispatch) AND without JS (regular POST) */}
      <form action={subscribeAction}>
        <label htmlFor="sub-email">Email address</label>
        <input
          id="sub-email"
          name="email"
          type="email"
          required
          autoComplete="email"
          aria-describedby={error ? 'sub-error' : undefined}
        />
        <button type="submit">Subscribe</button>
      </form>
    </main>
  );
}''',
    ),

    ex(
        "Create a Server Component page that generates dynamic Open Graph metadata from fetched data.",
        '''\
// blog/[slug]/page.tsx

interface Post {
  slug: string;
  title: string;
  excerpt: string;
  author: string;
  publishedAt: string;
  coverImage: string;
}

async function getPost(slug: string): Promise<Post | null> {
  const res = await fetch(`${process.env.API_URL}/posts/${slug}`);
  return res.ok ? (res.json() as Promise<Post>) : null;
}

interface Params { params: { slug: string } }

export async function generateMetadata({ params }: Params): Promise<{ title: string; description?: string }> {
  const post = await getPost(params.slug);
  if (!post) return { title: 'Post not found' };

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title:       post.title,
      description: post.excerpt,
      type:        'article',
      publishedTime: post.publishedAt,
      authors:     [post.author],
      images: [{ url: post.coverImage, width: 1200, height: 630, alt: post.title }],
    },
    twitter: {
      card:        'summary_large_image',
      title:       post.title,
      description: post.excerpt,
      images:      [post.coverImage],
    },
  };
}

export default async function BlogPostPage({ params }: Params) {
  const post = await getPost(params.slug);
  if (!post) return <main><p>Post not found.</p></main>;

  return (
    <main>
      <article>
        <header>
          <h1>{post.title}</h1>
          <p>By {post.author} · <time dateTime={post.publishedAt}>{new Date(post.publishedAt).toLocaleDateString()}</time></p>
        </header>
        <img src={post.coverImage} alt={post.title} width={1200} height={630} priority />
        <p>{post.excerpt}</p>
      </article>
    </main>
  );
}''',
    ),

    ex(
        "Use useOptimistic to optimistically add a new todo before the server responds, then reconcile.",
        '''\
'use client';

import { useOptimistic, useActionState, useRef } from 'react';
import { createTodo } from '@/actions/todos';

interface Todo {
  id: string;
  title: string;
  done: boolean;
  pending?: boolean;
}

interface OptimisticTodoListProps {
  initialTodos: Todo[];
}

export function OptimisticTodoList({ initialTodos }: OptimisticTodoListProps) {
  const formRef = useRef<HTMLFormElement>(null);
  const [optimisticTodos, addOptimistic] = useOptimistic<Todo[], Todo>(
    initialTodos,
    (state, newTodo) => [...state, newTodo],
  );

  const [, dispatch, isPending] = useActionState(
    async (_prev: null, formData: FormData) => {
      const title = formData.get('title') as string;
      if (!title.trim()) return null;

      addOptimistic({ id: `temp-${Date.now()}`, title, done: false, pending: true });
      formRef.current?.reset();
      await createTodo(title);
      return null;
    },
    null,
  );

  return (
    <section>
      <form ref={formRef} action={dispatch} aria-label="Add todo">
        <label htmlFor="todo-input">New todo</label>
        <input id="todo-input" name="title" required disabled={isPending} placeholder="What needs doing?" />
        <button type="submit" disabled={isPending} aria-busy={isPending}>
          {isPending ? 'Adding…' : 'Add'}
        </button>
      </form>

      <ul aria-label="Todos" aria-live="polite">
        {optimisticTodos.map((todo) => (
          <li key={todo.id} style={{ opacity: todo.pending ? 0.5 : 1 }}>
            <span>{todo.title}</span>
            {todo.pending && <span aria-label="Saving…"> ⟳</span>}
          </li>
        ))}
      </ul>
    </section>
  );
}''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section G: Performance patterns
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Implement a virtualised list in React that only renders visible items to handle 10,000+ rows.",
        '''\
'use client';

import { useState, useRef, useMemo, useCallback } from 'react';

interface VirtualListProps<T> {
  items: T[];
  itemHeight: number;
  containerHeight: number;
  renderItem: (item: T, index: number) => React.ReactNode;
  overscan?: number;
}

export function VirtualList<T>({
  items,
  itemHeight,
  containerHeight,
  renderItem,
  overscan = 3,
}: VirtualListProps<T>) {
  const [scrollTop, setScrollTop] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);

  const { startIndex, endIndex, offsetY } = useMemo(() => {
    const visible  = Math.ceil(containerHeight / itemHeight);
    const start    = Math.max(0, Math.floor(scrollTop / itemHeight) - overscan);
    const end      = Math.min(items.length - 1, start + visible + overscan * 2);
    return { startIndex: start, endIndex: end, offsetY: start * itemHeight };
  }, [scrollTop, containerHeight, itemHeight, items.length, overscan]);

  const handleScroll = useCallback((e: React.UIEvent<HTMLDivElement>) => {
    setScrollTop(e.currentTarget.scrollTop);
  }, []);

  const totalHeight = items.length * itemHeight;
  const visible     = items.slice(startIndex, endIndex + 1);

  return (
    <div
      ref={containerRef}
      onScroll={handleScroll}
      style={{ height: containerHeight, overflowY: 'auto', position: 'relative' }}
      role="list"
      aria-label={`List of ${items.length} items`}
    >
      <div style={{ height: totalHeight, position: 'relative' }}>
        <div style={{ position: 'absolute', top: offsetY, width: '100%' }}>
          {visible.map((item, i) => (
            <div key={startIndex + i} role="listitem" style={{ height: itemHeight }}>
              {renderItem(item, startIndex + i)}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}''',
    ),

    ex(
        "Show how React.startTransition prevents urgent state updates from being blocked by a slow render.",
        '''\
'use client';

import { useState, startTransition, useDeferredValue, useMemo } from 'react';

interface Item {
  id: number;
  name: string;
}

function generateItems(count: number): Item[] {
  return Array.from({ length: count }, (_, i) => ({ id: i, name: `Item ${i + 1}` }));
}

const ALL_ITEMS = generateItems(5000);

// Simulate expensive filtering
function filterItems(items: Item[], query: string): Item[] {
  return items.filter((item) => item.name.toLowerCase().includes(query.toLowerCase()));
}

export function TransitionSearchDemo() {
  const [query, setQuery] = useState('');
  // deferredQuery updates are low-priority — the input stays responsive
  const deferredQuery = useDeferredValue(query);

  const filtered = useMemo(
    () => filterItems(ALL_ITEMS, deferredQuery),
    [deferredQuery],
  );

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    // Input update is urgent — happens immediately
    const value = e.target.value;
    setQuery(value);
    // List re-render is deferred — won't block typing
    startTransition(() => {
      // heavy list rendering deferred automatically via deferredQuery
    });
  }

  const isStale = query !== deferredQuery;

  return (
    <div>
      <label htmlFor="ts-search">Search 5,000 items</label>
      <input
        id="ts-search"
        type="search"
        value={query}
        onChange={handleChange}
        placeholder="Type to filter…"
      />
      <p aria-live="polite">{filtered.length} results {isStale && '(updating…)'}</p>
      <ul style={{ opacity: isStale ? 0.6 : 1 }} aria-label="Results">
        {filtered.slice(0, 50).map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
        {filtered.length > 50 && <li>…and {filtered.length - 50} more</li>}
      </ul>
    </div>
  );
}''',
    ),

    ex(
        "Memoize an expensive recursive tree component so only changed branches re-render.",
        '''\
'use client';

import { memo, useState, useCallback } from 'react';

interface TreeNode {
  id: string;
  label: string;
  children?: TreeNode[];
}

interface TreeItemProps {
  node: TreeNode;
  depth: number;
  onSelect: (id: string) => void;
  selectedId: string | null;
}

// memo + custom comparator — only re-renders if this node's data or selection changes
const TreeItem = memo(
  function TreeItem({ node, depth, onSelect, selectedId }: TreeItemProps) {
    const [expanded, setExpanded] = useState(false);
    const hasChildren = (node.children?.length ?? 0) > 0;

    return (
      <li style={{ paddingLeft: depth * 16 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          {hasChildren && (
            <button
              type="button"
              aria-expanded={expanded}
              aria-label={`${expanded ? 'Collapse' : 'Expand'} ${node.label}`}
              onClick={() => setExpanded((e) => !e)}
            >
              {expanded ? '▼' : '▶'}
            </button>
          )}
          <button
            type="button"
            aria-pressed={selectedId === node.id}
            onClick={() => onSelect(node.id)}
            style={{ fontWeight: selectedId === node.id ? 700 : undefined }}
          >
            {node.label}
          </button>
        </div>
        {hasChildren && expanded && (
          <ul role="group" aria-label={`${node.label} children`}>
            {node.children!.map((child) => (
              <TreeItem
                key={child.id}
                node={child}
                depth={depth + 1}
                onSelect={onSelect}
                selectedId={selectedId}
              />
            ))}
          </ul>
        )}
      </li>
    );
  },
  (prev, next) =>
    prev.node === next.node &&
    prev.selectedId === next.selectedId &&
    prev.onSelect === next.onSelect,
);

interface TreeProps {
  nodes: TreeNode[];
}

export function Tree({ nodes }: TreeProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const handleSelect = useCallback((id: string) => setSelectedId(id), []);

  return (
    <ul role="tree" aria-label="File tree">
      {nodes.map((node) => (
        <TreeItem key={node.id} node={node} depth={0} onSelect={handleSelect} selectedId={selectedId} />
      ))}
    </ul>
  );
}''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section H: Accessibility advanced
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Create an accessible accordion component where only one panel is open at a time.",
        '''\
'use client';

import { useState, useId, type ReactNode } from 'react';

interface AccordionItem {
  id: string;
  title: string;
  content: ReactNode;
}

interface AccordionProps {
  items: AccordionItem[];
  defaultOpen?: string;
}

export function Accordion({ items, defaultOpen }: AccordionProps) {
  const [openId, setOpenId] = useState<string | null>(defaultOpen ?? null);
  const prefix = useId();

  function toggle(id: string) {
    setOpenId((current) => (current === id ? null : id));
  }

  return (
    <div>
      {items.map((item) => {
        const isOpen       = openId === item.id;
        const headingId    = `${prefix}-heading-${item.id}`;
        const panelId      = `${prefix}-panel-${item.id}`;

        return (
          <div key={item.id}>
            <h3 style={{ margin: 0 }}>
              <button
                type="button"
                id={headingId}
                aria-expanded={isOpen}
                aria-controls={panelId}
                onClick={() => toggle(item.id)}
                style={{
                  width: '100%',
                  textAlign: 'left',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '1rem',
                  background: 'none',
                  border: 'none',
                  borderBottom: '1px solid #e5e7eb',
                  cursor: 'pointer',
                  fontWeight: 600,
                }}
              >
                {item.title}
                <span aria-hidden="true">{isOpen ? '−' : '+'}</span>
              </button>
            </h3>
            <div
              id={panelId}
              role="region"
              aria-labelledby={headingId}
              hidden={!isOpen}
              style={{ padding: isOpen ? '1rem' : undefined }}
            >
              {item.content}
            </div>
          </div>
        );
      })}
    </div>
  );
}''',
    ),

    ex(
        "Build an accessible tooltip component triggered by hover and focus, using ARIA description.",
        '''\
'use client';

import { useState, useRef, useId, type ReactNode } from 'react';
import { createPortal } from 'react-dom';

interface TooltipProps {
  content: string;
  children: ReactNode;
}

export function Tooltip({ content, children }: TooltipProps) {
  const [visible, setVisible] = useState(false);
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const triggerRef = useRef<HTMLSpanElement>(null);
  const tooltipId  = useId();

  function show() {
    const rect = triggerRef.current?.getBoundingClientRect();
    if (rect) {
      setPosition({ top: rect.bottom + 8 + window.scrollY, left: rect.left + rect.width / 2 + window.scrollX });
    }
    setVisible(true);
  }

  function hide() { setVisible(false); }

  return (
    <>
      <span
        ref={triggerRef}
        onMouseEnter={show}
        onMouseLeave={hide}
        onFocus={show}
        onBlur={hide}
        aria-describedby={visible ? tooltipId : undefined}
        tabIndex={0}
        style={{ display: 'inline-block' }}
      >
        {children}
      </span>
      {visible && createPortal(
        <div
          id={tooltipId}
          role="tooltip"
          style={{
            position: 'absolute',
            top: position.top,
            left: position.left,
            transform: 'translateX(-50%)',
            background: '#111827',
            color: '#fff',
            padding: '0.375rem 0.75rem',
            borderRadius: 4,
            fontSize: '0.875rem',
            pointerEvents: 'none',
            zIndex: 9999,
            maxWidth: 240,
            textAlign: 'center',
          }}
        >
          {content}
        </div>,
        document.body,
      )}
    </>
  );
}''',
    ),

    ex(
        "Build a focus trap hook for modal dialogs that cycles through focusable elements with Tab.",
        '''\
'use client';

import { useEffect, type RefObject } from 'react';

const FOCUSABLE_SELECTORS = [
  'a[href]',
  'button:not([disabled])',
  'input:not([disabled])',
  'select:not([disabled])',
  'textarea:not([disabled])',
  '[tabindex]:not([tabindex="-1"])',
].join(',');

export function useFocusTrap(containerRef: RefObject<HTMLElement>, active: boolean): void {
  useEffect(() => {
    if (!active) return;

    const container = containerRef.current;
    if (!container) return;

    const focusable = () =>
      Array.from(container.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTORS)).filter(
        (el) => !el.closest('[hidden]'),
      );

    function onKeyDown(e: KeyboardEvent) {
      if (e.key !== 'Tab') return;
      const elements = focusable();
      if (elements.length === 0) { e.preventDefault(); return; }
      const first = elements[0];
      const last  = elements[elements.length - 1];

      if (e.shiftKey) {
        if (document.activeElement === first) { e.preventDefault(); last.focus(); }
      } else {
        if (document.activeElement === last)  { e.preventDefault(); first.focus(); }
      }
    }

    // Move focus inside on activate
    const first = focusable()[0];
    first?.focus();

    container.addEventListener('keydown', onKeyDown);
    return () => container.removeEventListener('keydown', onKeyDown);
  }, [active, containerRef]);
}''',
    ),

    ex(
        "Add ARIA live region announcements for route changes in a React app.",
        '''\
'use client';

import { useEffect, useRef, useState } from 'react';

interface RouteAnnouncerProps {
  pathname: string;
}

export function RouteAnnouncer({ pathname }: RouteAnnouncerProps) {
  const [message, setMessage] = useState('');
  const prevPath    = useRef<string | null>(null);

  useEffect(() => {
    if (prevPath.current === null) { prevPath.current = pathname; return; }
    if (prevPath.current === pathname) return;

    const title = document.title || pathname;
    setMessage(`Navigated to ${title}`);
    prevPath.current = pathname;

    const timer = setTimeout(() => setMessage(''), 1000);
    return () => clearTimeout(timer);
  }, [pathname]);

  return (
    // Positioned off-screen; always present in DOM so screen readers register it early
    <div
      aria-live="assertive"
      aria-atomic="true"
      style={{
        position: 'absolute',
        width: 1,
        height: 1,
        padding: 0,
        overflow: 'hidden',
        clip: 'rect(0,0,0,0)',
        whiteSpace: 'nowrap',
        border: 0,
      }}
    >
      {message}
    </div>
  );
}

// Place in root layout.tsx:
// <body>
//   <RouteAnnouncer />
//   {children}
// </body>''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section I: Full real-world components
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Build a notification center: Server Component loads notifications, Client handles mark-as-read via Server Action.",
        '''\
// notifications/page.tsx — Server Component
import { Suspense } from 'react';
import { NotificationList } from './NotificationList';

interface Notification {
  id: string;
  title: string;
  body: string;
  read: boolean;
  createdAt: string;
  type: 'info' | 'warning' | 'success';
}

async function getNotifications(): Promise<Notification[]> {
  const res = await fetch(`${process.env.API_URL}/notifications`, { cache: 'no-store' });
  return res.json() as Promise<Notification[]>;
}

export default async function NotificationsPage() {
  const notifications = await getNotifications();
  const unread = notifications.filter((n) => !n.read).length;
  return (
    <main>
      <h1>Notifications {unread > 0 && <span aria-label={`${unread} unread`}>({unread})</span>}</h1>
      <Suspense fallback={<p>Loading…</p>}>
        <NotificationList notifications={notifications} />
      </Suspense>
    </main>
  );
}

// notifications/actions.ts
'use server';


export async function markAsRead(id: string): Promise<void> {
  await fetch(`${process.env.API_URL}/notifications/${id}/read`, { method: 'POST' });
  // // // // revalidateTag('notifications');
}

export async function markAllAsRead(): Promise<void> {
  await fetch(`${process.env.API_URL}/notifications/read-all`, { method: 'POST' });
  // // // // revalidateTag('notifications');
}

// notifications/NotificationList.tsx
'use client';

import { useTransition } from 'react';
import { markAsRead, markAllAsRead } from './actions';

interface Notification {
  id: string;
  title: string;
  body: string;
  read: boolean;
  createdAt: string;
  type: 'info' | 'warning' | 'success';
}

const TYPE_ICON: Record<Notification['type'], string> = { info: 'ℹ️', warning: '⚠️', success: '✅' };

export function NotificationList({ notifications }: { notifications: Notification[] }) {
  const [isPending, startTransition] = useTransition();

  function handleMarkRead(id: string) {
    startTransition(() => { markAsRead(id); });
  }
  function handleMarkAll() {
    startTransition(() => { markAllAsRead(); });
  }

  return (
    <div>
      <button type="button" onClick={handleMarkAll} disabled={isPending || notifications.every((n) => n.read)}>
        Mark all as read
      </button>
      <ul aria-label="Notifications" aria-live="polite">
        {notifications.map((n) => (
          <li key={n.id} style={{ opacity: n.read ? 0.6 : 1 }}>
            <span aria-hidden="true">{TYPE_ICON[n.type]}</span>
            <div>
              <strong>{n.title}</strong>
              <p>{n.body}</p>
              <time dateTime={n.createdAt}>{new Date(n.createdAt).toLocaleString()}</time>
            </div>
            {!n.read && (
              <button type="button" onClick={() => handleMarkRead(n.id)} disabled={isPending}
                aria-label={`Mark "${n.title}" as read`}>
                Mark read
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}''',
    ),

    ex(
        "Create a full settings page: Server Component for layout, Client Components for each settings section, Server Actions for saving.",
        '''\
// settings/page.tsx — Server Component layout
import { ProfileSettings } from './ProfileSettings';
import { NotificationSettings } from './NotificationSettings';

interface Settings {
  name: string;
  email: string;
  bio: string;
  emailNotifications: boolean;
  pushNotifications: boolean;
  marketingEmails: boolean;
}

async function getSettings(): Promise<Settings> {
  const res = await fetch(`${process.env.API_URL}/settings`);
  return res.json() as Promise<Settings>;
}

export default async function SettingsPage() {
  const settings = await getSettings();
  return (
    <main>
      <h1>Settings</h1>
      <section aria-label="Profile settings">
        <h2>Profile</h2>
        <ProfileSettings initial={{ name: settings.name, email: settings.email, bio: settings.bio }} />
      </section>
      <section aria-label="Notification settings">
        <h2>Notifications</h2>
        <NotificationSettings initial={{
          emailNotifications: settings.emailNotifications,
          pushNotifications:  settings.pushNotifications,
          marketingEmails:    settings.marketingEmails,
        }} />
      </section>
    </main>
  );
}

// settings/actions.ts
'use server';


export async function saveProfile(data: { name: string; email: string; bio: string }): Promise<{ error: string | null }> {
  const res = await fetch(`${process.env.API_URL}/settings/profile`, {
    method: 'PUT',
    body: JSON.stringify(data),
    headers: { 'Content-Type': 'application/json' },
  });
  if (!res.ok) return { error: 'Failed to save profile.' };
  // // // // revalidateTag('settings');
  return { error: null };
}

export async function saveNotifications(data: Record<string, boolean>): Promise<{ error: string | null }> {
  const res = await fetch(`${process.env.API_URL}/settings/notifications`, {
    method: 'PUT',
    body: JSON.stringify(data),
    headers: { 'Content-Type': 'application/json' },
  });
  if (!res.ok) return { error: 'Failed to save notification preferences.' };
  // // // // revalidateTag('settings');
  return { error: null };
}

// settings/ProfileSettings.tsx
'use client';

import { useActionState } from 'react';
import { saveProfile } from './actions';

interface ProfileData { name: string; email: string; bio: string }
type SaveState = { error: string | null; success: boolean };

export function ProfileSettings({ initial }: { initial: ProfileData }) {
  async function action(_prev: SaveState, formData: FormData): Promise<SaveState> {
    const result = await saveProfile({
      name:  formData.get('name')  as string,
      email: formData.get('email') as string,
      bio:   formData.get('bio')   as string,
    });
    return { error: result.error, success: !result.error };
  }

  const [state, dispatch, isPending] = useActionState(action, { error: null, success: false });

  return (
    <form action={dispatch}>
      {state.success && <p role="status">Profile saved.</p>}
      {state.error   && <p role="alert">{state.error}</p>}
      <label htmlFor="prof-name">Name</label>
      <input id="prof-name" name="name" defaultValue={initial.name} required disabled={isPending} />
      <label htmlFor="prof-email">Email</label>
      <input id="prof-email" name="email" type="email" defaultValue={initial.email} required disabled={isPending} />
      <label htmlFor="prof-bio">Bio</label>
      <textarea id="prof-bio" name="bio" defaultValue={initial.bio} rows={3} disabled={isPending} />
      <button type="submit" disabled={isPending} aria-busy={isPending}>
        {isPending ? 'Saving…' : 'Save profile'}
      </button>
    </form>
  );
}''',
    ),

    ex(
        "Create a multi-step onboarding flow using Server Actions with persistent state in a cookie.",
        '''\
// onboarding/actions.ts
'use server';


interface OnboardingData {
  step: number;
  name?: string;
  role?: string;
  team?: string;
}

// Stand-in store — replace with your framework session/cookie or database persistence.
let onboardingStore: OnboardingData = { step: 1 };

function getOnboarding(): OnboardingData {
  return onboardingStore;
}

function saveOnboarding(data: OnboardingData): void {
  onboardingStore = data;
}

export async function submitStep1(formData: FormData): Promise<void> {
  const name = (formData.get('name') as string).trim();
  if (!name) return;
  const data = getOnboarding();
  saveOnboarding({ ...data, step: 2, name });
  // // // // redirect('/onboarding/step-2');
}

export async function submitStep2(formData: FormData): Promise<void> {
  const role = formData.get('role') as string;
  const data = getOnboarding();
  saveOnboarding({ ...data, step: 3, role });
  // // // // redirect('/onboarding/step-3');
}

export async function completeOnboarding(formData: FormData): Promise<void> {
  const team = formData.get('team') as string;
  const data = getOnboarding();
  await fetch(`${process.env.API_URL}/users/onboard`, {
    method: 'POST',
    body: JSON.stringify({ ...data, team }),
    headers: { 'Content-Type': 'application/json' },
  });
  onboardingStore = { step: 1 };
  // // // redirect('/dashboard');
}

// onboarding/step-1/page.tsx
export default function Step1Page() {
  return (
    <main>
      <h1>Welcome! What is your name?</h1>
      <form action={submitStep1}>
        <label htmlFor="ob-name">Full name</label>
        <input id="ob-name" name="name" type="text" autoComplete="name" required autoFocus />
        <button type="submit">Continue</button>
      </form>
    </main>
  );
}''',
    ),


    # ─────────────────────────────────────────────────────────────────────────
    # Section J: More custom hooks
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Build a useScrollPosition hook that tracks the current X and Y scroll position.",
        '''\
'use client';

import { useState, useEffect } from 'react';

interface ScrollPosition { x: number; y: number }

export function useScrollPosition(): ScrollPosition {
  const [position, setPosition] = useState<ScrollPosition>({ x: 0, y: 0 });

  useEffect(() => {
    function onScroll() {
      setPosition({ x: window.scrollX, y: window.scrollY });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    setPosition({ x: window.scrollX, y: window.scrollY });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return position;
}''',
    ),

    ex(
        "Create a useWindowSize hook that returns the current viewport width and height.",
        '''\
'use client';

import { useState, useEffect } from 'react';

interface WindowSize { width: number; height: number }

export function useWindowSize(): WindowSize {
  const [size, setSize] = useState<WindowSize>({ width: 0, height: 0 });

  useEffect(() => {
    function update() {
      setSize({ width: window.innerWidth, height: window.innerHeight });
    }
    window.addEventListener('resize', update);
    update();
    return () => window.removeEventListener('resize', update);
  }, []);

  return size;
}''',
    ),

    ex(
        "Write a useCounter hook with increment, decrement, reset, and a configurable min/max.",
        '''\
'use client';

import { useState, useCallback } from 'react';

interface UseCounterOptions {
  initial?: number;
  min?: number;
  max?: number;
  step?: number;
}

interface UseCounterResult {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
  set: (n: number) => void;
}

export function useCounter({ initial = 0, min = -Infinity, max = Infinity, step = 1 }: UseCounterOptions = {}): UseCounterResult {
  const [count, setCount] = useState(initial);
  const clamp = (n: number) => Math.min(max, Math.max(min, n));
  const increment = useCallback(() => setCount((c) => clamp(c + step)), [max, min, step]);
  const decrement = useCallback(() => setCount((c) => clamp(c - step)), [max, min, step]);
  const reset     = useCallback(() => setCount(initial), [initial]);
  const set       = useCallback((n: number) => setCount(clamp(n)), [max, min]);
  return { count, increment, decrement, reset, set };
}''',
    ),

    ex(
        "Create a useThrottle hook that limits how often a value updates.",
        '''\
'use client';

import { useState, useEffect, useRef } from 'react';

export function useThrottle<T>(value: T, limitMs: number): T {
  const [throttled, setThrottled] = useState<T>(value);
  const lastRun   = useRef<number>(0);
  const timerRef  = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    const now = Date.now();
    const remaining = limitMs - (now - lastRun.current);

    if (timerRef.current) clearTimeout(timerRef.current);

    if (remaining <= 0) {
      lastRun.current = now;
      setThrottled(value);
    } else {
      timerRef.current = setTimeout(() => {
        lastRun.current = Date.now();
        setThrottled(value);
      }, remaining);
    }

    return () => { if (timerRef.current) clearTimeout(timerRef.current); };
  }, [value, limitMs]);

  return throttled;
}''',
    ),

    ex(
        "Build a useQueue hook for managing a FIFO queue of items in state.",
        '''\
'use client';

import { useState, useCallback } from 'react';

interface UseQueueResult<T> {
  queue: T[];
  enqueue: (item: T) => void;
  dequeue: () => T | undefined;
  peek: () => T | undefined;
  clear: () => void;
  size: number;
  isEmpty: boolean;
}

export function useQueue<T>(initial: T[] = []): UseQueueResult<T> {
  const [queue, setQueue] = useState<T[]>(initial);

  const enqueue = useCallback((item: T) => setQueue((q) => [...q, item]), []);
  const dequeue = useCallback((): T | undefined => {
    let removed: T | undefined;
    setQueue((q) => { removed = q[0]; return q.slice(1); });
    return removed;
  }, []);
  const peek  = useCallback(() => queue[0], [queue]);
  const clear = useCallback(() => setQueue([]), []);

  return { queue, enqueue, dequeue, peek, clear, size: queue.length, isEmpty: queue.length === 0 };
}''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section K: E-commerce patterns
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Create a product grid Server Component with category filter from URL searchParams.",
        '''\
// shop/page.tsx

interface Product {
  id: string;
  name: string;
  price: number;
  imageUrl: string;
  category: string;
}

async function getProducts(category: string): Promise<Product[]> {
  const url = new URL(`${process.env.API_URL}/products`);
  if (category) url.searchParams.set('category', category);
  const res = await fetch(url.toString());
  return res.json() as Promise<Product[]>;
}

async function getCategories(): Promise<string[]> {
  const res = await fetch(`${process.env.API_URL}/categories`);
  return res.json() as Promise<string[]>;
}

interface ShopPageProps {
  searchParams: { category?: string };
}

export default async function ShopPage({ searchParams }: ShopPageProps) {
  const category = searchParams.category ?? '';
  const [products, categories] = await Promise.all([getProducts(category), getCategories()]);

  return (
    <main>
      <h1>Shop</h1>
      <nav aria-label="Category filter">
        <a href="/shop" aria-current={!category ? 'page' : undefined}>All</a>
        {categories.map((cat) => (
          <a key={cat} href={`/shop?category=${encodeURIComponent(cat)}`}
            aria-current={category === cat ? 'page' : undefined}>{cat}</a>
        ))}
      </nav>
      <p aria-live="polite">{products.length} products</p>
      <ul role="list" aria-label="Products">
        {products.map((p) => (
          <li key={p.id}>
            <article>
              <img src={p.imageUrl} alt={p.name} width={300} height={300} loading="lazy" />
              <h2><a href={`/shop/${p.id}`}>{p.name}</a></h2>
              <p>${p.price.toFixed(2)}</p>
            </article>
          </li>
        ))}
      </ul>
    </main>
  );
}''',
    ),

    ex(
        "Build a wishlist toggle button that uses optimistic UI and a Server Action.",
        '''\
'use client';

import { useOptimistic, useTransition } from 'react';
import { toggleWishlist } from '@/actions/wishlist';

interface WishlistButtonProps {
  productId: string;
  initialInWishlist: boolean;
}

export function WishlistButton({ productId, initialInWishlist }: WishlistButtonProps) {
  const [isPending, startTransition] = useTransition();
  const [inWishlist, setOptimistic] = useOptimistic(
    initialInWishlist,
    (_current, next: boolean) => next,
  );

  function handleClick() {
    const next = !inWishlist;
    startTransition(async () => {
      setOptimistic(next);
      await toggleWishlist(productId, next);
    });
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      disabled={isPending}
      aria-pressed={inWishlist}
      aria-label={inWishlist ? 'Remove from wishlist' : 'Add to wishlist'}
    >
      {inWishlist ? '♥ Saved' : '♡ Save'}
    </button>
  );
}

// actions/wishlist.ts
'use server';


export async function toggleWishlist(productId: string, add: boolean): Promise<void> {
  await fetch(`${process.env.API_URL}/wishlist/${productId}`, {
    method: add ? 'PUT' : 'DELETE',
  });
  // // // // revalidatePath('/wishlist');
}''',
    ),

    ex(
        "Create an order history page as a Server Component with status badges and date formatting.",
        '''\
// orders/page.tsx
type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';

interface Order {
  id: string;
  createdAt: string;
  total: number;
  status: OrderStatus;
  itemCount: number;
}

const STATUS_LABEL: Record<OrderStatus, string> = {
  pending:    'Pending',
  processing: 'Processing',
  shipped:    'Shipped',
  delivered:  'Delivered',
  cancelled:  'Cancelled',
};

const STATUS_COLOR: Record<OrderStatus, string> = {
  pending:    '#92400e',
  processing: '#1d4ed8',
  shipped:    '#7c3aed',
  delivered:  '#166534',
  cancelled:  '#991b1b',
};

async function getOrders(): Promise<Order[]> {
  const res = await fetch(`${process.env.API_URL}/orders`);
  return res.json() as Promise<Order[]>;
}

export default async function OrdersPage() {
  const orders = await getOrders();

  return (
    <main>
      <h1>Order history</h1>
      {orders.length === 0 ? (
        <p>No orders yet.</p>
      ) : (
        <table>
          <caption>Your orders</caption>
          <thead>
            <tr>
              <th scope="col">Order</th>
              <th scope="col">Date</th>
              <th scope="col">Items</th>
              <th scope="col">Total</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td>#{order.id.slice(-6).toUpperCase()}</td>
                <td><time dateTime={order.createdAt}>{new Date(order.createdAt).toLocaleDateString()}</time></td>
                <td>{order.itemCount} item{order.itemCount !== 1 ? 's' : ''}</td>
                <td>${order.total.toFixed(2)}</td>
                <td>
                  <span
                    style={{ color: STATUS_COLOR[order.status], fontWeight: 600 }}
                    aria-label={`Status: ${STATUS_LABEL[order.status]}`}
                  >
                    {STATUS_LABEL[order.status]}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}''',
    ),

    ex(
        "Build a coupon code form using useActionState that validates and applies a discount.",
        '''\
'use client';

import { useActionState } from 'react';

interface CouponState {
  error: string | null;
  discount: number | null;
  code: string | null;
}

async function applyCoupon(_prev: CouponState, formData: FormData): Promise<CouponState> {
  const code = (formData.get('code') as string).trim().toUpperCase();
  if (!code) return { error: 'Enter a coupon code.', discount: null, code: null };

  const res = await fetch('/api/coupons/validate', {
    method: 'POST',
    body: JSON.stringify({ code }),
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) return { error: 'Invalid or expired coupon code.', discount: null, code: null };

  const { discount } = (await res.json()) as { discount: number };
  return { error: null, discount, code };
}

interface CouponFormProps {
  onApplied: (discount: number, code: string) => void;
}

export function CouponForm({ onApplied }: CouponFormProps) {
  const [state, dispatch, isPending] = useActionState(applyCoupon, { error: null, discount: null, code: null });

  if (state.discount !== null && state.code !== null) {
    onApplied(state.discount, state.code);
    return (
      <p role="status" aria-live="polite">
        Coupon <strong>{state.code}</strong> applied — {state.discount}% off!
      </p>
    );
  }

  return (
    <form action={dispatch} aria-label="Apply coupon">
      <label htmlFor="coupon-code">Coupon code</label>
      <input
        id="coupon-code"
        name="code"
        type="text"
        placeholder="SAVE20"
        disabled={isPending}
        style={{ textTransform: 'uppercase' }}
        aria-describedby={state.error ? 'coupon-err' : undefined}
      />
      {state.error && <span id="coupon-err" role="alert">{state.error}</span>}
      <button type="submit" disabled={isPending} aria-busy={isPending}>
        {isPending ? 'Checking…' : 'Apply'}
      </button>
    </form>
  );
}''',
    ),

    ex(
        "Create a product image gallery Client Component with thumbnail navigation and keyboard support.",
        '''\
'use client';

import { useState, type KeyboardEvent } from 'react';

interface ProductGalleryProps {
  images: Array<{ src: string; alt: string }>;
  productName: string;
}

export function ProductGallery({ images, productName }: ProductGalleryProps) {
  const [activeIdx, setActiveIdx] = useState(0);

  function handleKeyDown(e: KeyboardEvent<HTMLDivElement>) {
    if (e.key === 'ArrowRight') setActiveIdx((i) => (i + 1) % images.length);
    if (e.key === 'ArrowLeft')  setActiveIdx((i) => (i - 1 + images.length) % images.length);
  }

  return (
    <div aria-label={`${productName} image gallery`}>
      <div
        tabIndex={0}
        onKeyDown={handleKeyDown}
        role="img"
        aria-label={images[activeIdx].alt}
        aria-roledescription="image carousel"
      >
        <img
          src={images[activeIdx].src}
          alt={images[activeIdx].alt}
          width={600}
          height={600}
          style={{ width: '100%', objectFit: 'cover' }}
        />
      </div>

      <div role="tablist" aria-label="Select image" style={{ display: 'flex', gap: 8, marginTop: 8 }}>
        {images.map((img, i) => (
          <button
            key={i}
            role="tab"
            aria-selected={i === activeIdx}
            aria-label={`Image ${i + 1}: ${img.alt}`}
            onClick={() => setActiveIdx(i)}
            style={{ padding: 0, border: i === activeIdx ? '2px solid #0070f3' : '2px solid transparent' }}
          >
            <img src={img.src} alt="" aria-hidden="true" width={80} height={80} style={{ objectFit: 'cover' }} />
          </button>
        ))}
      </div>
      <p aria-live="polite" className="sr-only">
        Image {activeIdx + 1} of {images.length}
      </p>
    </div>
  );
}''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section L: SaaS / Dashboard patterns
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Create a team member invite form with useActionState that validates email and assigns a role.",
        '''\
'use client';

import { useActionState } from 'react';

type Role = 'viewer' | 'editor' | 'admin';
type InviteState = { error: string | null; success: boolean };

async function inviteAction(_prev: InviteState, formData: FormData): Promise<InviteState> {
  const email = (formData.get('email') as string).trim();
  const role  = formData.get('role') as Role;
  const EMAIL_RE = /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/;
  if (!EMAIL_RE.test(email)) return { error: 'Enter a valid email address.', success: false };
  const res = await fetch('/api/team/invite', {
    method: 'POST',
    body: JSON.stringify({ email, role }),
    headers: { 'Content-Type': 'application/json' },
  });
  if (!res.ok) return { error: res.status === 409 ? 'This person is already on the team.' : 'Invite failed.', success: false };
  return { error: null, success: true };
}

export function InviteTeamMemberForm() {
  const [state, dispatch, isPending] = useActionState(inviteAction, { error: null, success: false });

  return (
    <form action={dispatch} aria-label="Invite team member">
      {state.success && <p role="status">Invite sent!</p>}
      {state.error   && <p role="alert">{state.error}</p>}

      <label htmlFor="invite-email">Email address</label>
      <input id="invite-email" name="email" type="email" required disabled={isPending} autoComplete="email" />

      <fieldset disabled={isPending}>
        <legend>Role</legend>
        {(['viewer', 'editor', 'admin'] as Role[]).map((r) => (
          <label key={r}>
            <input type="radio" name="role" value={r} defaultChecked={r === 'viewer'} required />
            {r.charAt(0).toUpperCase() + r.slice(1)}
          </label>
        ))}
      </fieldset>

      <button type="submit" disabled={isPending} aria-busy={isPending}>
        {isPending ? 'Sending invite…' : 'Send invite'}
      </button>
    </form>
  );
}''',
    ),

    ex(
        "Create a dashboard stats overview Server Component with percentage-change indicators.",
        '''\
// dashboard/StatsOverview.tsx
interface Stat {
  label: string;
  value: string;
  change: number;
  unit?: string;
}

async function getStats(): Promise<Stat[]> {
  const res = await fetch(`${process.env.API_URL}/stats/overview`);
  return res.json() as Promise<Stat[]>;
}

function ChangeIndicator({ change }: { change: number }) {
  const positive = change >= 0;
  return (
    <span
      aria-label={`${positive ? 'Increased' : 'Decreased'} by ${Math.abs(change).toFixed(1)}% from last period`}
      style={{ color: positive ? '#16a34a' : '#dc2626', fontWeight: 500, fontSize: '0.875rem' }}
    >
      {positive ? '↑' : '↓'} {Math.abs(change).toFixed(1)}%
    </span>
  );
}

export async function StatsOverview() {
  const stats = await getStats();
  return (
    <section aria-label="Key metrics">
      <dl style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
        {stats.map((stat) => (
          <div key={stat.label} style={{ padding: '1.25rem', border: '1px solid #e5e7eb', borderRadius: 8 }}>
            <dt style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.25rem' }}>{stat.label}</dt>
            <dd style={{ display: 'flex', alignItems: 'baseline', gap: '0.5rem', margin: 0 }}>
              <span style={{ fontSize: '1.5rem', fontWeight: 700 }}>
                {stat.unit}{stat.value}
              </span>
              <ChangeIndicator change={stat.change} />
            </dd>
          </div>
        ))}
      </dl>
    </section>
  );
}''',
    ),

    ex(
        "Build an API key management page: Server Component lists keys, Server Action generates and revokes.",
        '''\
// settings/api-keys/page.tsx
import { Suspense } from 'react';
import { RevokeKeyButton } from './RevokeKeyButton';
import { generateApiKey } from './actions';

interface ApiKey {
  id: string;
  name: string;
  prefix: string;
  createdAt: string;
  lastUsedAt: string | null;
}

async function getApiKeys(): Promise<ApiKey[]> {
  const res = await fetch(`${process.env.API_URL}/api-keys`);
  return res.json() as Promise<ApiKey[]>;
}

export default async function ApiKeysPage() {
  const keys = await getApiKeys();

  return (
    <main>
      <h1>API Keys</h1>

      <form action={generateApiKey} aria-label="Generate new API key">
        <label htmlFor="key-name">Key name</label>
        <input id="key-name" name="name" type="text" placeholder="e.g. Production server" required />
        <button type="submit">Generate key</button>
      </form>

      <table aria-label="API keys">
        <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Key prefix</th>
            <th scope="col">Created</th>
            <th scope="col">Last used</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          {keys.map((key) => (
            <tr key={key.id}>
              <td>{key.name}</td>
              <td><code>{key.prefix}…</code></td>
              <td><time dateTime={key.createdAt}>{new Date(key.createdAt).toLocaleDateString()}</time></td>
              <td>{key.lastUsedAt ? new Date(key.lastUsedAt).toLocaleDateString() : 'Never'}</td>
              <td><RevokeKeyButton keyId={key.id} keyName={key.name} /></td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}

// actions.ts
'use server';

export async function generateApiKey(formData: FormData): Promise<void> {
  const name = formData.get('name') as string;
  await fetch(`${process.env.API_URL}/api-keys`, {
    method: 'POST',
    body: JSON.stringify({ name }),
    headers: { 'Content-Type': 'application/json' },
  });
  // // // // revalidateTag('api-keys');
}

export async function revokeApiKey(keyId: string): Promise<void> {
  await fetch(`${process.env.API_URL}/api-keys/${keyId}`, { method: 'DELETE' });
  // // // // revalidateTag('api-keys');
}''',
    ),

    ex(
        "Create a usage meter component that shows a plan limit with a progress bar and upgrade CTA.",
        '''\
// components/UsageMeter.tsx — Server Component
interface Usage {
  label: string;
  used: number;
  limit: number;
  unit: string;
}

interface UsageMeterProps {
  usage: Usage;
  onUpgrade?: () => void;
}

export function UsageMeter({ usage, onUpgrade }: UsageMeterProps) {
  const pct     = Math.min(100, (usage.used / usage.limit) * 100);
  const isWarn  = pct >= 80;
  const isCrit  = pct >= 95;
  const color   = isCrit ? '#dc2626' : isWarn ? '#d97706' : '#0070f3';

  return (
    <div aria-label={`${usage.label} usage`}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
        <span>{usage.label}</span>
        <span aria-label={`${usage.used} of ${usage.limit} ${usage.unit} used`}>
          {usage.used.toLocaleString()} / {usage.limit.toLocaleString()} {usage.unit}
        </span>
      </div>
      <div
        role="progressbar"
        aria-valuenow={usage.used}
        aria-valuemin={0}
        aria-valuemax={usage.limit}
        aria-valuetext={`${Math.round(pct)}% of ${usage.limit} ${usage.unit} used`}
        style={{ height: 8, background: '#e5e7eb', borderRadius: 4, overflow: 'hidden' }}
      >
        <div style={{ width: `${pct}%`, height: '100%', background: color, transition: 'width 0.3s' }} />
      </div>
      {isCrit && onUpgrade && (
        <p role="alert" style={{ marginTop: 8, fontSize: '0.875rem', color }}>
          You are at {Math.round(pct)}% of your limit.{' '}
          <button type="button" onClick={onUpgrade} style={{ color, textDecoration: 'underline', background: 'none', border: 'none', cursor: 'pointer' }}>
            Upgrade your plan
          </button>
        </p>
      )}
    </div>
  );
}''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section M: More TypeScript patterns
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Create a type-safe route params utility using TypeScript template literal types for React.",
        '''\
// Encode route patterns as template literal types to catch param mismatches at build time.

type ExtractParams<T extends string> =
  T extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? Param | ExtractParams<Rest>
    : T extends `${infer _Start}:${infer Param}`
    ? Param
    : never;

type RouteParams<T extends string> = Record<ExtractParams<T>, string>;

function buildPath<T extends string>(pattern: T, params: RouteParams<T>): string {
  let path: string = pattern;
  for (const [key, value] of Object.entries(params)) {
    path = path.replace(`:${key}`, encodeURIComponent(value as string));
  }
  return path;
}

// Defined routes — TypeScript knows which params each route needs
const ROUTES = {
  userProfile: '/users/:userId',
  postDetail:  '/posts/:postId',
  postComment: '/posts/:postId/comments/:commentId',
} as const;

// Usage — TypeScript error if wrong params are passed:
const userUrl = buildPath(ROUTES.userProfile, { userId: '123' });           // '/users/123'
const postUrl = buildPath(ROUTES.postDetail,  { postId: 'abc' });           // '/posts/abc'
// buildPath(ROUTES.userProfile, { postId: '123' }); // ✗ TypeScript error

export { buildPath, ROUTES };''',
    ),

    ex(
        "Implement a type-safe React context factory function that removes boilerplate.",
        '''\
import { createContext, useContext, type ReactNode, type Context } from 'react';

interface ContextFactory<T> {
  Provider: React.FC<{ value: T; children: ReactNode }>;
  useContext: () => T;
  Context: Context<T | null>;
}

export function createSafeContext<T>(displayName: string): ContextFactory<T> {
  const Ctx = createContext<T | null>(null);
  Ctx.displayName = displayName;

  function SafeProvider({ value, children }: { value: T; children: ReactNode }) {
    return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
  }
  SafeProvider.displayName = `${displayName}Provider`;

  function useSafeContext(): T {
    const value = useContext(Ctx);
    if (value === null) {
      throw new Error(`${displayName} context used outside of <${displayName}Provider>`);
    }
    return value;
  }

  return { Provider: SafeProvider, useContext: useSafeContext, Context: Ctx };
}

// Usage — zero boilerplate:
interface AuthContextValue { userId: string; role: 'admin' | 'user'; logout: () => void }
const AuthContext = createSafeContext<AuthContextValue>('Auth');

export const AuthProvider = AuthContext.Provider;
export const useAuth = AuthContext.useContext;
// useAuth() throws a clear error if used outside <AuthProvider>''',
    ),

    ex(
        "Write TypeScript type guards for discriminated union API responses.",
        '''\
// Model a consistent API response envelope with type guards

interface ApiSuccess<T> {
  status: 'success';
  data: T;
}

interface ApiError {
  status: 'error';
  code: string;
  message: string;
}

interface ApiLoading {
  status: 'loading';
}

type ApiResponse<T> = ApiSuccess<T> | ApiError | ApiLoading;

// Type guards — narrow the union safely
function isSuccess<T>(r: ApiResponse<T>): r is ApiSuccess<T> {
  return r.status === 'success';
}
function isError<T>(r: ApiResponse<T>): r is ApiError {
  return r.status === 'error';
}
function isLoading<T>(r: ApiResponse<T>): r is ApiLoading {
  return r.status === 'loading';
}

// Usage in a component:
interface User { id: string; name: string }

interface ApiDisplayProps {
  response: ApiResponse<User[]>;
}

export function ApiDisplay({ response }: ApiDisplayProps) {
  if (isLoading(response))  return <p aria-busy="true">Loading…</p>;
  if (isError(response))    return <p role="alert">{response.message} ({response.code})</p>;

  // TypeScript knows response.data is User[] here
  return (
    <ul aria-label="Users">
      {response.data.map((u) => <li key={u.id}>{u.name}</li>)}
    </ul>
  );
}''',
    ),

    ex(
        "Create a type-safe form state management pattern using TypeScript satisfies and const assertions.",
        '''\
// Define form schemas with const assertions — full type inference, no runtime library needed

const CONTACT_FORM = {
  name:    { type: 'text',  required: true,  label: 'Full name',     minLength: 2 },
  email:   { type: 'email', required: true,  label: 'Email address', pattern: /^[^@\\s]+@[^@\\s]+/ },
  message: { type: 'textarea', required: true, label: 'Message',     maxLength: 1000 },
} as const satisfies Record<string, {
  type: 'text' | 'email' | 'textarea';
  required: boolean;
  label: string;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
}>;

type ContactFormKey = keyof typeof CONTACT_FORM;
type ContactFormData = Record<ContactFormKey, string>;

function validateForm(data: ContactFormData): Partial<Record<ContactFormKey, string>> {
  const errors: Partial<Record<ContactFormKey, string>> = {};
  for (const [key, schema] of Object.entries(CONTACT_FORM) as [ContactFormKey, typeof CONTACT_FORM[ContactFormKey]][]) {
    const value = data[key];
    if (schema.required && !value.trim()) {
      errors[key] = `${schema.label} is required.`;
    } else if ('minLength' in schema && schema.minLength && value.length < schema.minLength) {
      errors[key] = `${schema.label} must be at least ${schema.minLength} characters.`;
    } else if ('pattern' in schema && schema.pattern && !schema.pattern.test(value)) {
      errors[key] = `${schema.label} is invalid.`;
    }
  }
  return errors;
}

export { CONTACT_FORM, validateForm };
export type { ContactFormData, ContactFormKey };''',
    ),

    ex(
        "Use TypeScript mapped types to create a Partial version of a component's required props.",
        '''\
import type { ComponentType, ReactNode } from 'react';

// Utility: make a subset of props optional and provide defaults
type WithDefaults<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

interface ButtonProps {
  label: string;
  variant: 'primary' | 'secondary' | 'danger';
  size: 'sm' | 'md' | 'lg';
  disabled: boolean;
  onClick: () => void;
  icon?: ReactNode;
}

// Consumer doesn't need to pass variant/size/disabled — they have defaults
type ButtonPublicProps = WithDefaults<ButtonProps, 'variant' | 'size' | 'disabled'>;

function Button({
  label,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  icon,
}: ButtonPublicProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant} btn-${size}`}
      aria-disabled={disabled}
    >
      {icon && <span aria-hidden="true">{icon}</span>}
      {label}
    </button>
  );
}

// Higher-order utility: wrap any component to inject fixed prop defaults
function withDefaults<T extends object, K extends keyof T>(
  Component: ComponentType<T>,
  defaults: Required<Pick<T, K>>,
): ComponentType<WithDefaults<T, K>> {
  return function WrappedComponent(props: WithDefaults<T, K>) {
    return <Component {...defaults} {...(props as T)} />;
  };
}

export const PrimaryButton = withDefaults(Button, { variant: 'primary', size: 'md', disabled: false });
export type { ButtonPublicProps, WithDefaults };''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section N: More Server Component patterns
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Build a React Server Component that shows different content based on the user's authentication status.",
        '''\
// home/page.tsx

interface UserSession {
  userId: string;
  name: string;
  plan: 'free' | 'pro';
}

async function getSession(sessionToken: string | null): Promise<UserSession | null> {
  if (!sessionToken) return null;
  const res = await fetch(`${process.env.API_URL}/session`, {
    headers: { Authorization: `Bearer ${sessionToken}` },
    cache: 'no-store',
  });
  return res.ok ? (res.json() as Promise<UserSession>) : null;
}

interface HomePageProps {
  sessionToken: string | null;
}

export default async function HomePage({ sessionToken }: HomePageProps) {
  const session = await getSession(sessionToken);

  return (
    <main>
      <h1>Welcome{session ? `, ${session.name}` : ' to the App'}</h1>

      {session ? (
        <section aria-label="Dashboard overview">
          <p>You are on the <strong>{session.plan}</strong> plan.</p>
          {session.plan === 'free' && (
            <a href="/upgrade">Upgrade to Pro →</a>
          )}
          <a href="/dashboard">Go to dashboard</a>
        </section>
      ) : (
        <section aria-label="Get started">
          <p>Sign in to access your dashboard.</p>
          <a href="/login">Sign in</a>
          <a href="/register">Create account</a>
        </section>
      )}
    </main>
  );
}''',
    ),

    ex(
        "Create a layout Server Component that fetches navigation items and highlights the active route.",
        '''\
// layout.tsx
import type { ReactNode } from 'react';

interface NavItem {
  label: string;
  href: string;
  icon: string;
}

async function getNavItems(): Promise<NavItem[]> {
  const res = await fetch(`${process.env.API_URL}/nav`);
  return res.json() as Promise<NavItem[]>;
}

interface RootLayoutProps {
  children: ReactNode;
  activePath: string;
}

export default async function RootLayout({ children, activePath }: RootLayoutProps) {
  const navItems = await getNavItems();
  const pathname = activePath;

  return (
    <html lang="en">
      <body>
        <a href="#main" className="sr-only focus:not-sr-only">Skip to main content</a>
        <nav aria-label="Primary">
          <ul>
            {navItems.map((item) => {
              const isActive = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href));
              return (
                <li key={item.href}>
                  <a
                    href={item.href}
                    aria-current={isActive ? 'page' : undefined}
                    style={{ fontWeight: isActive ? 700 : undefined }}
                  >
                    <span aria-hidden="true">{item.icon}</span>
                    {item.label}
                  </a>
                </li>
              );
            })}
          </ul>
        </nav>
        <main id="main">{children}</main>
      </body>
    </html>
  );
}''',
    ),

    ex(
        "Create a React Server Component for an article page that streams the content and sidebar independently.",
        '''\
// articles/[slug]/page.tsx
import { Suspense } from 'react';

interface Article {
  title: string;
  content: string;
  author: string;
  publishedAt: string;
  tags: string[];
}
interface RelatedArticle { id: string; title: string; slug: string }

async function getArticle(slug: string): Promise<Article> {
  const res = await fetch(`${process.env.API_URL}/articles/${slug}`);
  if (!res.ok) throw new Error('Article not found');
  return res.json() as Promise<Article>;
}

async function getRelated(slug: string): Promise<RelatedArticle[]> {
  const res = await fetch(`${process.env.API_URL}/articles/${slug}/related`);
  return res.json() as Promise<RelatedArticle[]>;
}

async function ArticleContent({ slug }: { slug: string }) {
  const article = await getArticle(slug);
  return (
    <article>
      <h1>{article.title}</h1>
      <p>By {article.author} · <time dateTime={article.publishedAt}>{new Date(article.publishedAt).toLocaleDateString()}</time></p>
      <ul aria-label="Tags">
        {article.tags.map((t) => <li key={t}>{t}</li>)}
      </ul>
      <div dangerouslySetInnerHTML={{ __html: article.content }} />
    </article>
  );
}

async function RelatedArticles({ slug }: { slug: string }) {
  const related = await getRelated(slug);
  if (related.length === 0) return null;
  return (
    <aside aria-label="Related articles">
      <h2>Related</h2>
      <ul>
        {related.map((r) => <li key={r.id}><a href={`/articles/${r.slug}`}>{r.title}</a></li>)}
      </ul>
    </aside>
  );
}

export default function ArticlePage({ params }: { params: { slug: string } }) {
  return (
    <main style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: '2rem' }}>
      <Suspense fallback={<p aria-busy="true">Loading article…</p>}>
        <ArticleContent slug={params.slug} />
      </Suspense>
      <Suspense fallback={<p aria-busy="true">Loading related…</p>}>
        <RelatedArticles slug={params.slug} />
      </Suspense>
    </main>
  );
}''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section O: More performance patterns
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Explain the difference between useMemo and useCallback with concrete examples showing when to use each.",
        '''\
'use client';

import { useState, useMemo, useCallback, memo } from 'react';

interface Item { id: number; name: string; price: number }

interface ListProps {
  items: Item[];
  onItemClick: (id: number) => void;
}

// memo — prevents re-render when parent re-renders with same props
const ItemList = memo(function ItemList({ items, onItemClick }: ListProps) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>
          {item.name} — ${item.price}
          <button type="button" onClick={() => onItemClick(item.id)}>Select</button>
        </li>
      ))}
    </ul>
  );
});

const ALL_ITEMS: Item[] = Array.from({ length: 1000 }, (_, i) => ({
  id: i, name: `Item ${i}`, price: Math.round(Math.random() * 100),
}));

export function Demo() {
  const [query, setQuery] = useState('');
  const [selectedId, setSelectedId] = useState<number | null>(null);

  // useMemo — caches a COMPUTED VALUE (the filtered array)
  // Re-runs only when ALL_ITEMS or query changes — not on every render
  const filtered = useMemo(
    () => ALL_ITEMS.filter((i) => i.name.toLowerCase().includes(query.toLowerCase())),
    [query],   // ALL_ITEMS is stable (module-level const), safe to omit
  );

  // useCallback — caches a FUNCTION REFERENCE
  // Re-creates only when setSelectedId changes (it never does)
  // Stable reference means ItemList (memo) won't re-render when the parent re-renders
  const handleClick = useCallback((id: number) => {
    setSelectedId(id);
  }, []); // setSelectedId is stable — no deps needed

  return (
    <div>
      <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Filter…" />
      <p>{filtered.length} items</p>
      {selectedId !== null && <p>Selected: {selectedId}</p>}
      {/* ItemList only re-renders when filtered or handleClick changes */}
      <ItemList items={filtered} onItemClick={handleClick} />
    </div>
  );
}

// RULE:
// useMemo    → cache an expensive COMPUTED VALUE (array transforms, heavy math)
// useCallback → cache a FUNCTION so it stays reference-equal across renders
//               (pass stable callbacks to memo'd children to prevent their re-render)''',
    ),

    ex(
        "Optimise a search-as-you-type feature using useDeferredValue so the input stays responsive.",
        '''\
'use client';

import { useState, useDeferredValue, useMemo } from 'react';

interface Result { id: number; title: string; body: string }

const DATASET: Result[] = Array.from({ length: 2000 }, (_, i) => ({
  id: i,
  title: `Result ${i + 1}`,
  body: `Some content for result number ${i + 1}. Lorem ipsum dolor sit amet.`,
}));

function SearchResults({ query }: { query: string }) {
  // useMemo is still needed — it prevents recomputing on unrelated renders
  const results = useMemo(() => {
    if (!query) return [];
    const q = query.toLowerCase();
    return DATASET.filter((r) => r.title.toLowerCase().includes(q) || r.body.toLowerCase().includes(q));
  }, [query]);

  return (
    <ul aria-live="polite" aria-label="Search results">
      {results.slice(0, 20).map((r) => (
        <li key={r.id}>
          <strong>{r.title}</strong>
          <p>{r.body}</p>
        </li>
      ))}
      {results.length > 20 && <li>…and {results.length - 20} more results</li>}
    </ul>
  );
}

export function DeferredSearch() {
  const [input, setInput] = useState('');
  // deferredInput lags behind input — React prioritises updating the input first
  const deferredInput = useDeferredValue(input);
  const isStale = input !== deferredInput;

  return (
    <div>
      <label htmlFor="def-search">Search</label>
      <input
        id="def-search"
        type="search"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        // Input updates immediately — never blocked by the expensive render
      />
      {isStale && <span aria-live="polite" aria-busy="true"> Updating…</span>}
      <div style={{ opacity: isStale ? 0.7 : 1 }}>
        <SearchResults query={deferredInput} />
      </div>
    </div>
  );
}''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section P: More accessibility patterns
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Create an accessible disclosure widget (show/hide content) with proper ARIA expanded state.",
        '''\
'use client';

import { useState, useId, type ReactNode } from 'react';

interface DisclosureProps {
  summary: string;
  children: ReactNode;
  defaultOpen?: boolean;
}

export function Disclosure({ summary, children, defaultOpen = false }: DisclosureProps) {
  const [open, setOpen] = useState(defaultOpen);
  const contentId = useId();

  return (
    <div>
      <button
        type="button"
        aria-expanded={open}
        aria-controls={contentId}
        onClick={() => setOpen((o) => !o)}
        style={{ display: 'flex', alignItems: 'center', gap: 8, background: 'none', border: 'none', cursor: 'pointer', fontWeight: 600 }}
      >
        <span aria-hidden="true" style={{ transition: 'transform 0.2s', transform: open ? 'rotate(90deg)' : 'none' }}>▶</span>
        {summary}
      </button>
      <div
        id={contentId}
        hidden={!open}
        style={{ paddingLeft: '1.5rem' }}
      >
        {children}
      </div>
    </div>
  );
}''',
    ),

    ex(
        "Build a menu button component that opens a dropdown list following the ARIA menu pattern.",
        '''\
'use client';

import { useState, useRef, useId, useCallback, type KeyboardEvent } from 'react';

interface MenuItem {
  id: string;
  label: string;
  onSelect: () => void;
  disabled?: boolean;
}

interface MenuButtonProps {
  label: string;
  items: MenuItem[];
}

export function MenuButton({ label, items }: MenuButtonProps) {
  const [open, setOpen] = useState(false);
  const [activeIdx, setActiveIdx] = useState(-1);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const menuId    = useId();

  const close = useCallback(() => { setOpen(false); setActiveIdx(-1); buttonRef.current?.focus(); }, []);

  function handleButtonKeyDown(e: KeyboardEvent<HTMLButtonElement>) {
    if (e.key === 'ArrowDown' || e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      setOpen(true);
      setActiveIdx(0);
    }
  }

  function handleMenuKeyDown(e: KeyboardEvent<HTMLUListElement>) {
    const enabled = items.map((_, i) => i).filter((i) => !items[i].disabled);
    const pos     = enabled.indexOf(activeIdx);

    if (e.key === 'ArrowDown') { e.preventDefault(); setActiveIdx(enabled[(pos + 1) % enabled.length] ?? 0); }
    if (e.key === 'ArrowUp')   { e.preventDefault(); setActiveIdx(enabled[(pos - 1 + enabled.length) % enabled.length] ?? 0); }
    if (e.key === 'Escape')    close();
    if (e.key === 'Tab')       close();
    if ((e.key === 'Enter' || e.key === ' ') && activeIdx >= 0 && !items[activeIdx].disabled) {
      e.preventDefault();
      items[activeIdx].onSelect();
      close();
    }
  }

  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <button
        ref={buttonRef}
        type="button"
        aria-haspopup="menu"
        aria-expanded={open}
        aria-controls={menuId}
        onClick={() => setOpen((o) => !o)}
        onKeyDown={handleButtonKeyDown}
      >
        {label} ▾
      </button>
      {open && (
        <ul
          id={menuId}
          role="menu"
          aria-label={label}
          tabIndex={-1}
          onKeyDown={handleMenuKeyDown}
          onBlur={(e) => { if (!e.currentTarget.contains(e.relatedTarget)) close(); }}
          style={{ position: 'absolute', top: '100%', left: 0, background: '#fff', border: '1px solid #e5e7eb', borderRadius: 6, listStyle: 'none', padding: '0.25rem', minWidth: 160, zIndex: 50 }}
        >
          {items.map((item, i) => (
            <li key={item.id} role="none">
              <button
                type="button"
                role="menuitem"
                disabled={item.disabled}
                aria-disabled={item.disabled}
                id={`${menuId}-item-${item.id}`}
                tabIndex={i === activeIdx ? 0 : -1}
                onMouseEnter={() => setActiveIdx(i)}
                onClick={() => { item.onSelect(); close(); }}
                style={{ width: '100%', textAlign: 'left', padding: '0.5rem 0.75rem', background: i === activeIdx ? '#eff6ff' : 'none', border: 'none', cursor: item.disabled ? 'not-allowed' : 'pointer', opacity: item.disabled ? 0.5 : 1 }}
              >
                {item.label}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section Q: More Server Actions
    # ─────────────────────────────────────────════════════════════════════════

    ex(
        "Implement a bulk delete Server Action that takes a list of IDs and deletes them in parallel.",
        '''\
// actions/bulk.ts
'use server';


interface BulkDeleteResult {
  deleted: string[];
  failed: string[];
}

export async function bulkDeleteItems(ids: string[], resource: string): Promise<BulkDeleteResult> {
  const results = await Promise.allSettled(
    ids.map((id) =>
      fetch(`${process.env.API_URL}/${resource}/${id}`, { method: 'DELETE' })
        .then((r) => r.ok ? id : Promise.reject(id))
    ),
  );

  const deleted = results.filter((r): r is PromiseFulfilledResult<string> => r.status === 'fulfilled').map((r) => r.value);
  const failed  = results.filter((r): r is PromiseRejectedResult => r.status === 'rejected').map((r) => r.reason as string);

  // // // // revalidatePath(`/${resource}`);
  return { deleted, failed };
}

// components/BulkDeleteToolbar.tsx
'use client';

import { useState, useTransition } from 'react';
import { bulkDeleteItems } from '@/actions/bulk';

interface BulkDeleteToolbarProps {
  selectedIds: string[];
  resource: string;
  onComplete: () => void;
}

export function BulkDeleteToolbar({ selectedIds, resource, onComplete }: BulkDeleteToolbarProps) {
  const [isPending, startTransition] = useTransition();
  const [result, setResult] = useState<{ deleted: string[]; failed: string[] } | null>(null);

  if (selectedIds.length === 0) return null;

  function handleDelete() {
    if (!confirm(`Delete ${selectedIds.length} items? This cannot be undone.`)) return;
    startTransition(async () => {
      const r = await bulkDeleteItems(selectedIds, resource);
      setResult(r);
      onComplete();
    });
  }

  return (
    <div role="toolbar" aria-label="Selection actions">
      <span aria-live="polite">{selectedIds.length} selected</span>
      {result && (
        <p role="status">
          Deleted {result.deleted.length}
          {result.failed.length > 0 && `, ${result.failed.length} failed`}
        </p>
      )}
      <button type="button" onClick={handleDelete} disabled={isPending} aria-busy={isPending}>
        {isPending ? 'Deleting…' : 'Delete selected'}
      </button>
    </div>
  );
}''',
    ),

    ex(
        "Create a Server Action that redirects to a Stripe checkout session URL.",
        '''\
// actions/billing.ts
'use server';


interface CheckoutSessionResponse {
  url: string;
}

export async function startCheckout(sessionToken: string, priceId: string): Promise<void> {
  if (!sessionToken) throw new Error('Not authenticated');

  const res = await fetch(`${process.env.API_URL}/billing/checkout`, {
    method: 'POST',
    body: JSON.stringify({ priceId, successUrl: `${process.env.APP_URL}/billing/success`, cancelUrl: `${process.env.APP_URL}/pricing` }),
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${sessionToken}`,
    },
  });

  if (!res.ok) // // // // redirect('/pricing?error=checkout-failed');

  const { url } = (await res.json()) as CheckoutSessionResponse;
  // // // // redirect(url);
}

// components/UpgradeButton.tsx
'use client';

import { useTransition } from 'react';
import { startCheckout } from '@/actions/billing';

interface UpgradeButtonProps {
  priceId: string;
  label: string;
}

export function UpgradeButton({ priceId, label }: UpgradeButtonProps) {
  const [isPending, startTransition] = useTransition();

  return (
    <button
      type="button"
      onClick={() => startTransition(() => { startCheckout(priceId); })}
      disabled={isPending}
      aria-busy={isPending}
    >
      {isPending ? 'Redirecting to checkout…' : label}
    </button>
  );
}''',
    ),

    ex(
        "Write a Server Action for submitting a multi-part form that saves data and redirects on success.",
        '''\
// actions/profile.ts
'use server';


type ProfileResult = { error: string } | never;

export async function updateProfileAction(formData: FormData): Promise<ProfileResult> {
  const name     = (formData.get('name') as string | null)?.trim() ?? '';
  const bio      = (formData.get('bio') as string | null)?.trim() ?? '';
  const website  = (formData.get('website') as string | null)?.trim() ?? '';

  if (!name) return { error: 'Name is required.' };
  if (name.length > 100) return { error: 'Name must be 100 characters or less.' };

  if (website && !URL.canParse(website)) return { error: 'Invalid website URL.' };

  const res = await fetch(`${process.env.API_URL}/profile`, {
    method: 'PUT',
    body: JSON.stringify({ name, bio, website }),
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) return { error: 'Failed to update profile. Please try again.' };

  // // // // revalidatePath('/profile');
  // // // // redirect('/profile?updated=1');
}

// profile/edit/page.tsx — Server Component; action redirects on success
interface EditPageProps {
  searchParams: { error?: string };
}

export default function EditProfilePage({ searchParams }: EditPageProps) {
  return (
    <main>
      <h1>Edit profile</h1>
      {searchParams.error && <p role="alert">{searchParams.error}</p>}
      <form action={updateProfileAction}>
        <label htmlFor="ep-name">Display name</label>
        <input id="ep-name" name="name" type="text" required maxLength={100} />
        <label htmlFor="ep-bio">Bio</label>
        <textarea id="ep-bio" name="bio" rows={4} maxLength={500} />
        <label htmlFor="ep-web">Website</label>
        <input id="ep-web" name="website" type="url" placeholder="https://" />
        <button type="submit">Save profile</button>
      </form>
    </main>
  );
}''',
    ),


    # ─────────────────────────────────────────────────────────────────────────
    # Section R: Anti-patterns → correct patterns
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Refactor this component that fetches data inside useEffect into a proper Server Component.",
        '''\
// ✗ BEFORE — Client Component fetching in useEffect (anti-pattern in React Server Components architecture)
// 'use client';
// import { useState, useEffect } from 'react';
// export function UserList() {
//   const [users, setUsers] = useState([]);
//   useEffect(() => { fetch('/api/users').then(r => r.json()).then(setUsers); }, []);
//   return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
// }

// ✓ AFTER — Server Component: no client JS, no loading flash, no waterfall
interface User { id: string; name: string; email: string }

async function getUsers(): Promise<User[]> {
  const res = await fetch(`${process.env.API_URL}/users`);
  if (!res.ok) throw new Error('Failed to load users');
  return res.json() as Promise<User[]>;
}

export default async function UserList() {
  const users = await getUsers();
  return (
    <ul aria-label="Users">
      {users.map((u) => (
        <li key={u.id}>
          <strong>{u.name}</strong> — {u.email}
        </li>
      ))}
    </ul>
  );
}

// WHY: Server Components run on the server — they can fetch data directly,
// have access to env vars, and send zero JS to the browser for the data-fetching logic.
// useEffect fetching is still valid in pure client apps (Vite, CRA),
// but in React Server Components architecture, prefer async Server Components.''',
    ),

    ex(
        "Fix a React component that has a stale closure bug inside useEffect.",
        '''\
'use client';

import { useState, useEffect, useRef, useCallback } from 'react';

// ✗ BUGGY — stale closure: count is captured as 0 forever
// useEffect(() => {
//   const id = setInterval(() => {
//     console.log(count); // always 0 — stale closure
//     setCount(count + 1); // will only ever set to 1
//   }, 1000);
//   return () => clearInterval(id);
// }, []); // empty deps = runs once = captures initial count

// ✓ FIX 1 — use functional update form (no closure needed)
export function CounterFix1() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setCount((c) => c + 1); // reads latest value via functional update
    }, 1000);
    return () => clearInterval(id);
  }, []); // safe — no closure on count

  return <p>Count: {count}</p>;
}

// ✓ FIX 2 — use a ref to always access latest value
export function CounterFix2() {
  const [count, setCount] = useState(0);
  const countRef = useRef(count);
  countRef.current = count; // always up to date

  useEffect(() => {
    const id = setInterval(() => {
      console.log(countRef.current); // reads latest via ref
      setCount((c) => c + 1);
    }, 1000);
    return () => clearInterval(id);
  }, []);

  return <p>Count: {count}</p>;
}''',
    ),

    ex(
        "Show the correct way to handle async operations in useEffect to avoid race conditions.",
        '''\
'use client';

import { useState, useEffect } from 'react';

interface User { id: string; name: string; email: string }

// ✗ BUGGY — race condition: if userId changes rapidly,
//   slower responses can overwrite newer results
// useEffect(() => {
//   fetch(`/api/users/${userId}`).then(r => r.json()).then(setUser);
// }, [userId]);

// ✓ FIX 1 — cleanup flag (simple, no AbortController)
export function UserProfile1({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetch(`/api/users/${userId}`)
      .then((r) => r.json() as Promise<User>)
      .then((data) => { if (!cancelled) setUser(data); });
    return () => { cancelled = true; };
  }, [userId]);

  return user ? <p>{user.name}</p> : <p aria-busy="true">Loading…</p>;
}

// ✓ FIX 2 — AbortController (preferred: cancels the in-flight request)
export function UserProfile2({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    setUser(null);
    setError(null);

    fetch(`/api/users/${userId}`, { signal: controller.signal })
      .then((r) => r.json() as Promise<User>)
      .then(setUser)
      .catch((err: unknown) => {
        if (err instanceof Error && err.name === 'AbortError') return;
        setError('Failed to load user.');
      });

    return () => controller.abort();
  }, [userId]);

  if (error) return <p role="alert">{error}</p>;
  return user ? <p>{user.name}</p> : <p aria-busy="true">Loading…</p>;
}''',
    ),

    ex(
        "Demonstrate why you should not create components inside other components and the correct alternative.",
        '''\
'use client';

import { useState } from 'react';

interface Item { id: number; label: string }

// ✗ BAD — component defined inside render; recreated every render, causes remount
// export function ItemList() {
//   const [selected, setSelected] = useState<number | null>(null);
//
//   function ItemRow({ item }: { item: Item }) { // ← recreated every render!
//     return <li onClick={() => setSelected(item.id)}>{item.label}</li>;
//   }
//   ...
// }

// ✓ GOOD — ItemRow defined outside; stable reference, no remount
interface ItemRowProps {
  item: Item;
  selected: boolean;
  onSelect: (id: number) => void;
}

function ItemRow({ item, selected, onSelect }: ItemRowProps) {
  return (
    <li>
      <button
        type="button"
        aria-pressed={selected}
        onClick={() => onSelect(item.id)}
        style={{ fontWeight: selected ? 700 : undefined }}
      >
        {item.label}
      </button>
    </li>
  );
}

export function ItemList({ items }: { items: Item[] }) {
  const [selectedId, setSelectedId] = useState<number | null>(null);

  return (
    <ul aria-label="Items">
      {items.map((item) => (
        <ItemRow
          key={item.id}
          item={item}
          selected={selectedId === item.id}
          onSelect={setSelectedId}
        />
      ))}
    </ul>
  );
}''',
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # Section S: More full-stack patterns
    # ─────────────────────────────────────────────────────────────────────────

    ex(
        "Create a real-time-like feed that polls for new items every 30 seconds using useInterval.",
        '''\
'use client';

import { useState, useCallback } from 'react';
import { useInterval } from '@/hooks/useInterval';

interface FeedItem { id: string; content: string; author: string; createdAt: string }

interface LiveFeedProps {
  initialItems: FeedItem[];
}

export function LiveFeed({ initialItems }: LiveFeedProps) {
  const [items, setItems] = useState<FeedItem[]>(initialItems);
  const [newCount, setNewCount] = useState(0);
  const latestId = items[0]?.id ?? null;

  const poll = useCallback(async () => {
    if (!latestId) return;
    const res = await fetch(`/api/feed?after=${latestId}`);
    if (!res.ok) return;
    const fresh = (await res.json()) as FeedItem[];
    if (fresh.length > 0) {
      setItems((prev) => [...fresh, ...prev]);
      setNewCount((c) => c + fresh.length);
    }
  }, [latestId]);

  useInterval(poll, 30_000);

  return (
    <div>
      {newCount > 0 && (
        <button
          type="button"
          onClick={() => setNewCount(0)}
          aria-live="polite"
        >
          {newCount} new post{newCount !== 1 ? 's' : ''} — click to dismiss
        </button>
      )}
      <ol aria-label="Feed" aria-live="polite">
        {items.map((item) => (
          <li key={item.id}>
            <strong>{item.author}</strong>
            <p>{item.content}</p>
            <time dateTime={item.createdAt}>{new Date(item.createdAt).toLocaleTimeString()}</time>
          </li>
        ))}
      </ol>
    </div>
  );
}''',
    ),

    ex(
        "Build a form that auto-saves as a draft every 2 seconds while the user is typing.",
        '''\
'use client';

import { useState, useEffect, useRef } from 'react';

type SaveStatus = 'idle' | 'saving' | 'saved' | 'error';

async function saveDraft(title: string, body: string): Promise<void> {
  await fetch('/api/drafts', {
    method: 'PUT',
    body: JSON.stringify({ title, body }),
    headers: { 'Content-Type': 'application/json' },
  });
}

export function AutoSaveEditor() {
  const [title, setTitle] = useState('');
  const [body,  setBody]  = useState('');
  const [status, setStatus] = useState<SaveStatus>('idle');
  const timerRef  = useRef<ReturnType<typeof setTimeout> | null>(null);
  const dirtyRef  = useRef(false);

  function scheduleAutosave(newTitle: string, newBody: string) {
    dirtyRef.current = true;
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(async () => {
      if (!dirtyRef.current) return;
      setStatus('saving');
      try {
        await saveDraft(newTitle, newBody);
        dirtyRef.current = false;
        setStatus('saved');
      } catch {
        setStatus('error');
      }
    }, 2000);
  }

  useEffect(() => () => { if (timerRef.current) clearTimeout(timerRef.current); }, []);

  return (
    <div>
      <div role="status" aria-live="polite" style={{ fontSize: '0.875rem', color: '#6b7280' }}>
        {status === 'saving' && 'Saving draft…'}
        {status === 'saved'  && 'Draft saved'}
        {status === 'error'  && 'Failed to save draft'}
      </div>

      <label htmlFor="ae-title">Title</label>
      <input
        id="ae-title"
        value={title}
        onChange={(e) => { setTitle(e.target.value); scheduleAutosave(e.target.value, body); }}
        placeholder="Post title"
      />

      <label htmlFor="ae-body">Content</label>
      <textarea
        id="ae-body"
        value={body}
        onChange={(e) => { setBody(e.target.value); scheduleAutosave(title, e.target.value); }}
        rows={10}
        placeholder="Start writing…"
      />
    </div>
  );
}''',
    ),

    ex(
        "Create a drag-and-drop reorderable list without any library, using the HTML5 Drag and Drop API.",
        '''\
'use client';

import { useState, useRef } from 'react';

interface DraggableItem { id: string; label: string }

interface DraggableListProps {
  initialItems: DraggableItem[];
  onChange?: (items: DraggableItem[]) => void;
}

export function DraggableList({ initialItems, onChange }: DraggableListProps) {
  const [items, setItems] = useState(initialItems);
  const dragIdx = useRef<number | null>(null);

  function reorder(from: number, to: number) {
    const next = [...items];
    const [moved] = next.splice(from, 1);
    next.splice(to, 0, moved);
    setItems(next);
    onChange?.(next);
  }

  return (
    <ul aria-label="Reorderable list" style={{ listStyle: 'none', padding: 0 }}>
      {items.map((item, idx) => (
        <li
          key={item.id}
          draggable
          onDragStart={() => { dragIdx.current = idx; }}
          onDragOver={(e) => { e.preventDefault(); }}
          onDrop={() => {
            if (dragIdx.current !== null && dragIdx.current !== idx) {
              reorder(dragIdx.current, idx);
              dragIdx.current = null;
            }
          }}
          onDragEnd={() => { dragIdx.current = null; }}
          aria-label={`${item.label} — drag to reorder`}
          style={{ padding: '0.75rem', border: '1px solid #e5e7eb', borderRadius: 6, marginBottom: 4, cursor: 'grab', background: '#fff' }}
        >
          <span aria-hidden="true">⠿</span> {item.label}
        </li>
      ))}
    </ul>
  );
}''',
    ),

    ex(
        "Create a two-factor authentication form that accepts a 6-digit OTP with auto-advance between inputs.",
        '''\
'use client';

import { useRef, type ClipboardEvent, type KeyboardEvent } from 'react';
import { useActionState } from 'react';

type OtpState = { error: string | null; success: boolean };

async function verifyOtp(_prev: OtpState, formData: FormData): Promise<OtpState> {
  const code = Array.from({ length: 6 }, (_, i) => formData.get(`d${i}`) as string).join('');
  if (code.length !== 6 || !/^\\d{6}$/.test(code)) return { error: 'Enter all 6 digits.', success: false };
  const res = await fetch('/api/auth/otp', {
    method: 'POST',
    body: JSON.stringify({ code }),
    headers: { 'Content-Type': 'application/json' },
  });
  return res.ok ? { error: null, success: true } : { error: 'Incorrect code. Please try again.', success: false };
}

export function OtpForm() {
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);
  const [state, dispatch, isPending] = useActionState(verifyOtp, { error: null, success: false });

  if (state.success) return <p role="status">Verified! Signing you in…</p>;

  function handleInput(index: number, value: string) {
    if (!/^\\d?$/.test(value)) return;
    if (value && index < 5) inputRefs.current[index + 1]?.focus();
  }

  function handleKeyDown(index: number, e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Backspace' && !e.currentTarget.value && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  }

  function handlePaste(e: ClipboardEvent<HTMLInputElement>) {
    const paste = e.clipboardData.getData('text').replace(/\\D/g, '').slice(0, 6);
    paste.split('').forEach((char, i) => {
      const el = inputRefs.current[i];
      if (el) { el.value = char; }
    });
    inputRefs.current[Math.min(paste.length, 5)]?.focus();
    e.preventDefault();
  }

  return (
    <form action={dispatch} aria-label="Two-factor authentication">
      <p id="otp-label">Enter the 6-digit code from your authenticator app</p>
      <div role="group" aria-labelledby="otp-label" style={{ display: 'flex', gap: 8 }}>
        {Array.from({ length: 6 }, (_, i) => (
          <input
            key={i}
            ref={(el) => { inputRefs.current[i] = el; }}
            name={`d${i}`}
            type="text"
            inputMode="numeric"
            maxLength={1}
            pattern="\\d"
            required
            disabled={isPending}
            aria-label={`Digit ${i + 1}`}
            onInput={(e) => handleInput(i, e.currentTarget.value)}
            onKeyDown={(e) => handleKeyDown(i, e)}
            onPaste={handlePaste}
            style={{ width: 44, height: 52, textAlign: 'center', fontSize: '1.5rem', borderRadius: 6, border: '1px solid #d1d5db' }}
          />
        ))}
      </div>
      {state.error && <p role="alert">{state.error}</p>}
      <button type="submit" disabled={isPending} aria-busy={isPending}>
        {isPending ? 'Verifying…' : 'Verify'}
      </button>
    </form>
  );
}''',
    ),

    ex(
        "Build a copy-to-clipboard button component that shows a confirmation tick using useClipboard.",
        '''\
'use client';

import { useClipboard } from '@/hooks/useClipboard';

interface CopyButtonProps {
  text: string;
  label?: string;
}

export function CopyButton({ text, label = 'Copy' }: CopyButtonProps) {
  const { copy, copied, error } = useClipboard(2000);

  return (
    <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8 }}>
      <button
        type="button"
        onClick={() => copy(text)}
        aria-label={copied ? 'Copied!' : `${label} to clipboard`}
        aria-live="polite"
      >
        {copied ? '✓ Copied' : label}
      </button>
      {error && <span role="alert" style={{ fontSize: '0.75rem', color: '#dc2626' }}>Copy failed</span>}
    </div>
  );
}

// Usage in an API key display:
// <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
//   <code>{apiKey}</code>
//   <CopyButton text={apiKey} label="Copy key" />
// </div>''',
    ),

    ex(
        "Create a responsive image component with native img, blur-up loading, and Tailwind CSS.",
        '''\
'use client';

import { useState } from 'react';

interface ResponsiveImageProps {
  src: string;
  alt: string;
  blurDataUrl?: string;
  className?: string;
  priority?: boolean;
}

export function ResponsiveImage({
  src,
  alt,
  blurDataUrl,
  className = '',
  priority = false,
}: ResponsiveImageProps) {
  const [loaded, setLoaded] = useState(false);

  return (
    <div className={`relative aspect-video w-full overflow-hidden rounded-lg bg-gray-200 ${className}`}>
      {blurDataUrl && !loaded && (
        <img
          src={blurDataUrl}
          alt=""
          aria-hidden
          className="absolute inset-0 h-full w-full scale-110 object-cover blur-lg"
        />
      )}
      <img
        src={src}
        alt={alt}
        loading={priority ? 'eager' : 'lazy'}
        decoding="async"
        onLoad={() => setLoaded(true)}
        className={`h-full w-full object-cover transition-opacity duration-300 ${loaded ? 'opacity-100' : 'opacity-0'}`}
      />
    </div>
  );
}''',
    ),

    ex(
        "Build a search results page that highlights the matching query terms in the results.",
        '''\
'use client';

import { useMemo } from 'react';

interface SearchResult {
  id: string;
  title: string;
  excerpt: string;
}

function highlight(text: string, query: string): React.ReactNode {
  if (!query.trim()) return text;
  const parts = text.split(new RegExp(`(${query.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&')})`, 'gi'));
  return parts.map((part, i) =>
    part.toLowerCase() === query.toLowerCase()
      ? <mark key={i} style={{ background: '#fef08a', borderRadius: 2 }}>{part}</mark>
      : part,
  );
}

interface SearchResultsProps {
  results: SearchResult[];
  query: string;
}

export function SearchResults({ results, query }: SearchResultsProps) {
  const highlighted = useMemo(
    () => results.map((r) => ({
      ...r,
      title:   highlight(r.title, query),
      excerpt: highlight(r.excerpt, query),
    })),
    [results, query],
  );

  if (highlighted.length === 0) {
    return <p role="status">No results for <q>{query}</q>.</p>;
  }

  return (
    <>
      <p role="status" aria-live="polite">{highlighted.length} result{highlighted.length !== 1 ? 's' : ''} for <q>{query}</q></p>
      <ol aria-label="Search results">
        {highlighted.map((r) => (
          <li key={r.id}>
            <article>
              <h2>{r.title}</h2>
              <p>{r.excerpt}</p>
            </article>
          </li>
        ))}
      </ol>
    </>
  );
}''',
    ),

    ex(
        "Create a Server Component that generates an RSS feed for a blog.",
        '''\
// feed.xml/route.ts — server route handler

interface Post {
  slug: string;
  title: string;
  excerpt: string;
  publishedAt: string;
  author: string;
}

async function getPosts(): Promise<Post[]> {
  const res = await fetch(`${process.env.API_URL}/posts?limit=20`);
  return res.json() as Promise<Post[]>;
}

function escapeXml(str: string): string {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

export async function GET(): Promise<Response> {
  const posts  = await getPosts();
  const siteUrl = process.env.NEXT_PUBLIC_APP_URL ?? 'https://example.com';

  const items = posts.map((post) => `
    <item>
      <title>${escapeXml(post.title)}</title>
      <link>${siteUrl}/blog/${post.slug}</link>
      <description>${escapeXml(post.excerpt)}</description>
      <author>${escapeXml(post.author)}</author>
      <pubDate>${new Date(post.publishedAt).toUTCString()}</pubDate>
      <guid>${siteUrl}/blog/${post.slug}</guid>
    </item>`).join('');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>My Blog</title>
    <link>${siteUrl}</link>
    <description>Latest posts</description>
    <language>en-us</language>
    <atom:link href="${siteUrl}/feed.xml" rel="self" type="application/rss+xml" />
    ${items}
  </channel>
</rss>`;

  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml', 'Cache-Control': 'public, max-age=3600' },
  });
}''',
    ),

    ex(
        "Create an image upload preview component that shows a thumbnail before uploading.",
        '''\
'use client';

import { useState, useId } from 'react';

interface ImagePreviewUploadProps {
  name: string;
  label: string;
  accept?: string;
  maxSizeMb?: number;
}

export function ImagePreviewUpload({ name, label, accept = 'image/*', maxSizeMb = 5 }: ImagePreviewUploadProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [error,   setError]   = useState<string | null>(null);
  const inputId = useId();

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) { setPreview(null); return; }

    if (file.size > maxSizeMb * 1024 * 1024) {
      setError(`Image must be under ${maxSizeMb}MB.`);
      setPreview(null);
      return;
    }

    setError(null);
    const reader = new FileReader();
    reader.onload = (ev) => setPreview(ev.target?.result as string);
    reader.readAsDataURL(file);
  }

  return (
    <div>
      <label htmlFor={inputId}>{label}</label>
      <input
        id={inputId}
        name={name}
        type="file"
        accept={accept}
        onChange={handleChange}
        aria-describedby={error ? `${inputId}-err` : undefined}
      />
      {error && <span id={`${inputId}-err`} role="alert">{error}</span>}
      {preview && (
        <figure style={{ marginTop: 8 }}>
          <img
            src={preview}
            alt="Upload preview"
            style={{ maxWidth: 200, maxHeight: 200, borderRadius: 8, objectFit: 'cover' }}
          />
          <figcaption>Preview</figcaption>
        </figure>
      )}
    </div>
  );
}''',
    ),

    ex(
        "Build a keyboard shortcut help dialog that lists all shortcuts registered with useKeyboard.",
        '''\
'use client';

import { useState } from 'react';
import { createPortal } from 'react-dom';
import { useKeyboard } from '@/hooks/useKeyboard';

interface Shortcut {
  keys: string;
  description: string;
  category: string;
}

const SHORTCUTS: Shortcut[] = [
  { keys: '⌘K', description: 'Open command palette', category: 'Navigation' },
  { keys: '⌘/', description: 'Show keyboard shortcuts', category: 'Navigation' },
  { keys: '⌘S', description: 'Save changes', category: 'Editing' },
  { keys: '⌘Z', description: 'Undo', category: 'Editing' },
  { keys: '⌘⇧Z', description: 'Redo', category: 'Editing' },
  { keys: 'Esc', description: 'Close dialog / cancel', category: 'Navigation' },
];

const CATEGORIES = Array.from(new Set(SHORTCUTS.map((s) => s.category)));

export function ShortcutHelp() {
  const [open, setOpen] = useState(false);

  useKeyboard({ key: '/', meta: true }, (e) => { e.preventDefault(); setOpen((o) => !o); });
  useKeyboard({ key: 'Escape' },        ()  => setOpen(false));

  if (!open) return null;

  return createPortal(
    <div
      role="presentation"
      style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)', zIndex: 9999 }}
      onClick={(e) => { if (e.target === e.currentTarget) setOpen(false); }}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label="Keyboard shortcuts"
        style={{ background: '#fff', maxWidth: 480, margin: '10vh auto', borderRadius: 12, padding: '1.5rem' }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <h2>Keyboard shortcuts</h2>
          <button type="button" onClick={() => setOpen(false)} aria-label="Close">✕</button>
        </div>
        {CATEGORIES.map((cat) => (
          <section key={cat}>
            <h3 style={{ fontSize: '0.875rem', color: '#6b7280', textTransform: 'uppercase', letterSpacing: 1 }}>{cat}</h3>
            <dl>
              {SHORTCUTS.filter((s) => s.category === cat).map((s) => (
                <div key={s.keys} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.25rem 0' }}>
                  <dt>{s.description}</dt>
                  <dd><kbd style={{ fontFamily: 'monospace', background: '#f3f4f6', padding: '0 6px', borderRadius: 4 }}>{s.keys}</kbd></dd>
                </div>
              ))}
            </dl>
          </section>
        ))}
      </div>
    </div>,
    document.body,
  );
}''',
    ),

    ex(
        "Implement a client-side auth gate that redirects unauthenticated users to login.",
        '''\
'use client';

import { useEffect, type ReactNode } from 'react';

const PUBLIC_PATHS = new Set(['/', '/login', '/register', '/forgot-password']);

interface AuthGateProps {
  children: ReactNode;
  isAuthenticated: boolean;
  pathname: string;
}

export function AuthGate({ children, isAuthenticated, pathname }: AuthGateProps) {
  useEffect(() => {
    if (isAuthenticated || PUBLIC_PATHS.has(pathname)) return;
    const login = `/login?redirect=${encodeURIComponent(pathname)}`;
    window.location.assign(login);
  }, [isAuthenticated, pathname]);

  if (!isAuthenticated && !PUBLIC_PATHS.has(pathname)) {
    return <p role="status" aria-live="polite">Redirecting to sign in…</p>;
  }

  return <>{children}</>;
}

// Parent Server Component passes isAuthenticated from your session API:
// <AuthGate isAuthenticated={!!session} pathname={currentPath}>{children}</AuthGate>''',
    ),

    ex(
        "Create a multi-select component with checkboxes that supports select-all and clear-all.",
        '''\
'use client';

import { useId, useMemo } from 'react';

interface Option { id: string; label: string }

interface MultiSelectProps {
  options: Option[];
  value: string[];
  onChange: (ids: string[]) => void;
  label: string;
}

export function MultiSelect({ options, value, onChange, label }: MultiSelectProps) {
  const groupId = useId();
  const selectedSet = useMemo(() => new Set(value), [value]);

  const allSelected = options.length > 0 && selectedSet.size === options.length;
  const someSelected = selectedSet.size > 0 && !allSelected;

  function toggleAll() {
    onChange(allSelected ? [] : options.map((o) => o.id));
  }

  function toggle(id: string) {
    const next = new Set(selectedSet);
    next.has(id) ? next.delete(id) : next.add(id);
    onChange(Array.from(next));
  }

  return (
    <fieldset aria-labelledby={groupId} style={{ border: '1px solid #e5e7eb', borderRadius: 8, padding: '1rem' }}>
      <legend id={groupId} style={{ fontWeight: 600 }}>{label}</legend>

      <label style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
        <input
          type="checkbox"
          checked={allSelected}
          ref={(el) => { if (el) el.indeterminate = someSelected; }}
          onChange={toggleAll}
          aria-label={allSelected ? 'Deselect all' : 'Select all'}
        />
        <strong>{allSelected ? 'Deselect all' : 'Select all'}</strong>
        <span style={{ marginLeft: 'auto', color: '#6b7280', fontSize: '0.875rem' }}>
          {selectedSet.size} / {options.length}
        </span>
      </label>

      <div role="group" aria-label={label}>
        {options.map((opt) => (
          <label key={opt.id} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '0.25rem 0' }}>
            <input
              type="checkbox"
              checked={selectedSet.has(opt.id)}
              onChange={() => toggle(opt.id)}
              aria-label={opt.label}
            />
            {opt.label}
          </label>
        ))}
      </div>
    </fieldset>
  );
}''',
    ),

    ex(
        "Implement a confirm dialog hook that returns a promise resolved on user confirmation.",
        '''\
'use client';

import { useState, useCallback, useRef, createContext, useContext, type ReactNode } from 'react';
import { createPortal } from 'react-dom';

interface ConfirmOptions {
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  danger?: boolean;
}

type ConfirmFn = (options: ConfirmOptions) => Promise<boolean>;
const ConfirmContext = createContext<ConfirmFn | null>(null);

export function ConfirmProvider({ children }: { children: ReactNode }) {
  const [dialog, setDialog] = useState<(ConfirmOptions & { resolve: (v: boolean) => void }) | null>(null);

  const confirm: ConfirmFn = useCallback(
    (options) => new Promise<boolean>((resolve) => setDialog({ ...options, resolve })),
    [],
  );

  function close(value: boolean) {
    dialog?.resolve(value);
    setDialog(null);
  }

  return (
    <ConfirmContext.Provider value={confirm}>
      {children}
      {dialog && createPortal(
        <div role="presentation" style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)', zIndex: 9999, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div role="alertdialog" aria-modal="true" aria-labelledby="confirm-title" aria-describedby="confirm-msg"
            style={{ background: '#fff', borderRadius: 12, padding: '1.5rem', maxWidth: 400, width: '90%' }}>
            <h2 id="confirm-title">{dialog.title}</h2>
            <p id="confirm-msg">{dialog.message}</p>
            <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: '1rem' }}>
              <button type="button" onClick={() => close(false)}>{dialog.cancelLabel ?? 'Cancel'}</button>
              <button type="button" onClick={() => close(true)}
                style={{ color: dialog.danger ? '#dc2626' : undefined }}>
                {dialog.confirmLabel ?? 'Confirm'}
              </button>
            </div>
          </div>
        </div>,
        document.body,
      )}
    </ConfirmContext.Provider>
  );
}

export function useConfirm(): ConfirmFn {
  const ctx = useContext(ConfirmContext);
  if (!ctx) throw new Error('useConfirm must be used inside <ConfirmProvider>');
  return ctx;
}

// Usage:
// const confirm = useConfirm();
// const ok = await confirm({ title: 'Delete post?', message: 'This cannot be undone.', danger: true });
// if (ok) deletePost(id);''',
    ),

    ex(
        "Build a read-more / truncated text component that expands inline without a layout shift.",
        '''\
'use client';

import { useState, useRef, useLayoutEffect } from 'react';

interface ReadMoreProps {
  text: string;
  maxLines?: number;
  expandLabel?: string;
  collapseLabel?: string;
}

export function ReadMore({
  text,
  maxLines = 3,
  expandLabel   = 'Read more',
  collapseLabel = 'Show less',
}: ReadMoreProps) {
  const [expanded, setExpanded]     = useState(false);
  const [needsButton, setNeedsButton] = useState(false);
  const textRef = useRef<HTMLParagraphElement>(null);

  useLayoutEffect(() => {
    const el = textRef.current;
    if (!el) return;
    const lineHeight = parseFloat(getComputedStyle(el).lineHeight);
    const maxHeight  = lineHeight * maxLines;
    setNeedsButton(el.scrollHeight > maxHeight + 1);
  }, [text, maxLines]);

  return (
    <div>
      <p
        ref={textRef}
        style={{
          overflow: expanded || !needsButton ? 'visible' : 'hidden',
          display: '-webkit-box',
          WebkitLineClamp: expanded || !needsButton ? 'unset' : maxLines,
          WebkitBoxOrient: 'vertical',
          margin: 0,
        }}
      >
        {text}
      </p>
      {needsButton && (
        <button
          type="button"
          onClick={() => setExpanded((e) => !e)}
          aria-expanded={expanded}
          style={{ marginTop: 4, background: 'none', border: 'none', color: '#0070f3', cursor: 'pointer', padding: 0 }}
        >
          {expanded ? collapseLabel : expandLabel}
        </button>
      )}
    </div>
  );
}''',
    ),

    ex(
        "Create a error page component (error.tsx convention) that catches runtime errors and offers a retry button.",
        '''\
// error.tsx — Error boundary for the app directory
'use client';

import { useEffect } from 'react';

interface ErrorPageProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ErrorPage({ error, reset }: ErrorPageProps) {
  useEffect(() => {
    // Log to error tracking service (Sentry, Datadog, etc.)
    console.error('[Runtime error]', error.digest, error.message);
  }, [error]);

  return (
    <main
      role="main"
      aria-labelledby="error-title"
      style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '50vh', padding: '2rem', textAlign: 'center' }}
    >
      <h1 id="error-title" style={{ fontSize: '1.5rem', fontWeight: 700 }}>Something went wrong</h1>
      <p style={{ color: '#6b7280', maxWidth: 400, marginTop: '0.5rem' }}>
        An unexpected error occurred. Our team has been notified.
      </p>
      {error.digest && (
        <p style={{ fontFamily: 'monospace', fontSize: '0.75rem', color: '#9ca3af', marginTop: '0.25rem' }}>
          Error reference: {error.digest}
        </p>
      )}
      <button
        type="button"
        onClick={reset}
        style={{ marginTop: '1.5rem', padding: '0.5rem 1.5rem' }}
      >
        Try again
      </button>
    </main>
  );
}''',
    ),

    ex(
        "Write a not-found.tsx page for React Server Components architecture with a search box and helpful links.",
        '''\
// not-found.tsx

const HELPFUL_LINKS = [
  { href: '/',         label: 'Home' },
  { href: '/blog',     label: 'Blog' },
  { href: '/docs',     label: 'Documentation' },
  { href: '/contact',  label: 'Contact support' },
];

export default function NotFound() {
  return (
    <main
      aria-labelledby="nf-title"
      style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', padding: '2rem', textAlign: 'center' }}
    >
      <p aria-hidden="true" style={{ fontSize: '5rem', fontWeight: 900, color: '#e5e7eb', lineHeight: 1 }}>404</p>
      <h1 id="nf-title" style={{ fontSize: '1.5rem', fontWeight: 700, marginTop: '1rem' }}>Page not found</h1>
      <p style={{ color: '#6b7280', maxWidth: 400 }}>
        The page you are looking for does not exist or has been moved.
      </p>

      <form method="get" action="/search" role="search" style={{ marginTop: '1.5rem', display: 'flex', gap: 8 }}>
        <label htmlFor="nf-search" className="sr-only">Search the site</label>
        <input id="nf-search" name="q" type="search" placeholder="Search…" style={{ padding: '0.5rem 0.75rem', borderRadius: 6, border: '1px solid #d1d5db' }} />
        <button type="submit">Search</button>
      </form>

      <nav aria-label="Helpful links" style={{ marginTop: '2rem' }}>
        <ul style={{ listStyle: 'none', display: 'flex', gap: '1rem', padding: 0, flexWrap: 'wrap', justifyContent: 'center' }}>
          {HELPFUL_LINKS.map((link) => (
            <li key={link.href}>
              <a href={link.href}>{link.label}</a>
            </li>
          ))}
        </ul>
      </nav>
    </main>
  );
}''',
    ),

    ex(
        "Create a generic infinite-scroll hook that can be attached to any list with a load-more function.",
        '''\
'use client';

import { useState, useEffect, useRef, useCallback } from 'react';

interface UseInfiniteScrollOptions<T> {
  fetchPage: (page: number) => Promise<T[]>;
  pageSize?: number;
}

interface UseInfiniteScrollResult<T> {
  items: T[];
  isLoading: boolean;
  hasMore: boolean;
  error: Error | null;
  sentinelRef: React.RefObject<HTMLDivElement>;
}

export function useInfiniteScroll<T>({ fetchPage, pageSize = 20 }: UseInfiniteScrollOptions<T>): UseInfiniteScrollResult<T> {
  const [items,     setItems]     = useState<T[]>([]);
  const [page,      setPage]      = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [hasMore,   setHasMore]   = useState(true);
  const [error,     setError]     = useState<Error | null>(null);
  const sentinelRef = useRef<HTMLDivElement>(null);

  const loadMore = useCallback(async () => {
    if (isLoading || !hasMore) return;
    setIsLoading(true);
    setError(null);
    try {
      const fresh = await fetchPage(page);
      if (fresh.length < pageSize) setHasMore(false);
      setItems((prev) => [...prev, ...fresh]);
      setPage((p) => p + 1);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to load'));
    } finally {
      setIsLoading(false);
    }
  }, [fetchPage, page, isLoading, hasMore, pageSize]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) loadMore(); },
      { rootMargin: '300px' },
    );
    if (sentinelRef.current) observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [loadMore]);

  return { items, isLoading, hasMore, error, sentinelRef };
}''',
    ),

    ex(
        "Demonstrate how to use React.Suspense with the use() hook to stream data from a Server Component.",
        '''\
// products/[id]/page.tsx — Server Component passes a promise to a client component
import { Suspense } from 'react';
import { ProductDetails } from './ProductDetails';
import { RelatedProducts } from './RelatedProducts';

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  images: string[];
}

function fetchProduct(id: string): Promise<Product> {
  return fetch(`${process.env.API_URL}/products/${id}`)
    .then((r) => r.json() as Promise<Product>);
}

function fetchRelated(id: string): Promise<Product[]> {
  return fetch(`${process.env.API_URL}/products/${id}/related`)
    .then((r) => r.json() as Promise<Product[]>);
}

export default function ProductPage({ params }: { params: { id: string } }) {
  // Pass promises (not await) — Suspense handles streaming
  const productPromise = fetchProduct(params.id);
  const relatedPromise = fetchRelated(params.id);

  return (
    <main>
      <Suspense fallback={<div aria-busy="true">Loading product…</div>}>
        <ProductDetails promise={productPromise} />
      </Suspense>
      <Suspense fallback={<div aria-busy="true">Loading related…</div>}>
        <RelatedProducts promise={relatedPromise} />
      </Suspense>
    </main>
  );
}

// ProductDetails.tsx
'use client';

import { use } from 'react';

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  images: string[];
}

export function ProductDetails({ promise }: { promise: Promise<Product> }) {
  const product = use(promise);  // suspends until resolved
  return (
    <article>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p aria-label={`Price: $${product.price.toFixed(2)}`}>${product.price.toFixed(2)}</p>
      <img src={product.images[0]} alt={product.name} width={600} height={600} />
    </article>
  );
}''',
    ),

    ex(
        "Show how to properly type a page component with both params and searchParams in TypeScript.",
        '''\
// shop/[category]/page.tsx

type SortField = 'price' | 'name' | 'rating';
type SortDir   = 'asc' | 'desc';

interface PageParams {
  category: string;
}

interface PageSearchParams {
  sort?:    SortField;
  dir?:     SortDir;
  page?:    string;
  q?:       string;
}

interface PageProps {
  params:       PageParams;
  searchParams: PageSearchParams;
}

const VALID_CATEGORIES = new Set(['electronics', 'clothing', 'books', 'home']);

export async function generateMetadata({ params }: PageProps): Promise<{ title: string; description?: string }> {
  if (!VALID_CATEGORIES.has(params.category)) return { title: 'Not found' };
  return {
    title: `${params.category.charAt(0).toUpperCase()}${params.category.slice(1)} — Shop`,
    description: `Browse ${params.category} products.`,
  };
}

export async function generateStaticParams(): Promise<PageParams[]> {
  return Array.from(VALID_CATEGORIES).map((category) => ({ category }));
}

export default async function CategoryPage({ params, searchParams }: PageProps) {
  if (!VALID_CATEGORIES.has(params.category)) throw new Error('Not found');

  const page  = Math.max(1, Number(searchParams.page ?? 1));
  const sort  = (searchParams.sort  ?? 'name') satisfies SortField;
  const dir   = (searchParams.dir   ?? 'asc')  satisfies SortDir;
  const query = searchParams.q ?? '';

  const res = await fetch(
    `${process.env.API_URL}/products/${params.category}?page=${page}&sort=${sort}&dir=${dir}&q=${encodeURIComponent(query)}`,
  );
  const products = await res.json() as Array<{ id: string; name: string; price: number }>;

  return (
    <main>
      <h1>{params.category}</h1>
      <p>{products.length} products</p>
      <ul>
        {products.map((p) => <li key={p.id}>{p.name} — ${p.price}</li>)}
      </ul>
    </main>
  );
}''',
    ),

]  # END NEW_EXAMPLES