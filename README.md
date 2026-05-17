# react-lm

Build a **React Golden Dataset** for fine-tuning a small coding LLM (e.g. [Qwen2.5-Coder-3B](https://huggingface.co/Qwen/Qwen2.5-Coder-3B)) into a React 19 expert. This repo is a **dataset factory**: Python modules hold instruction → code pairs; scripts merge, validate, split, and augment them into JSONL ready for QLoRA training.

For the full path from base model → Colab fine-tune → GGUF → Ollama, see **[PLAN.md](PLAN.md)**.

## What you get

| Output | Use |
|--------|-----|
| `train.jsonl` | Fine-tuning (~3× paraphrased prompts, same answers) |
| `train_seeds.jsonl` | Unique train split only (no paraphrase; good for small models) |
| `eval.jsonl` | Held-out eval (~10%, never paraphrased) |
| `all_seeds.jsonl` | All unique seeds after dedupe |
| `Modelfile` | Ollama system prompt after you export a GGUF |

Each line is a chat example:

```json
{
  "conversations": [
    { "role": "system", "content": "..." },
    { "role": "user", "content": "Create a login form with useActionState..." },
    { "role": "assistant", "content": "<TypeScript / React code>" }
  ]
}
```

The shared system prompt lives in `dataset_common.py`.

## Requirements

- **Python 3.10+** (stdlib only; no `pip install` needed for the pipeline)

## Quick start

Regenerate the full dataset and run quality gates:

```bash
python build_dataset.py
```

Verify Step 2 is complete:

```bash
python check_step2_ready.py
```

### Pipeline (step by step)

```bash
python generate_dataset.py              # → react_golden_dataset.jsonl
python scripts/generate_curriculum.py   # → seeds/generated_curriculum.py
python split_dataset.py                 # → all_seeds.jsonl, train_seeds.jsonl, eval.jsonl
python validate_dataset.py all_seeds.jsonl --strict-seeds
python augment_dataset.py               # → train.jsonl
python check_step2_ready.py
```

## Curriculum

Training data targets **senior React 19** practice: Server Components, Server Actions, `useActionState`, TypeScript without `any`, accessibility, performance, and ecosystem tools (TanStack Query, Zustand, Redux Toolkit, RHF + Zod, Vitest, Storybook, React Router, shadcn/Radix, etc.).

**React-first, not Next.js.** Seeds avoid `next/*` imports and Next-specific APIs. After editing sources, you can run `python neutralize_nextjs.py` to strip legacy Next wording from seed files.

### Styling rules

| User asks for | Assistant should use |
|---------------|----------------------|
| Tailwind (or unspecified UI) | Tailwind utility `className`s |
| CSS Modules | `*.module.css` + `styles.*` |
| SCSS / Sass | `*.module.scss` + included `.scss` source |

Do not mix Tailwind, CSS Modules, and SCSS in one answer unless the prompt is a comparison or migration example.

## Project layout

```
react-lm/
├── PLAN.md                    # End-to-end fine-tune & deploy guide
├── Modelfile                  # Ollama config (after GGUF export)
├── dataset_common.py          # SYSTEM_PROMPT + ex(user, assistant)
├── curriculum_tags.py         # Tag detection & coverage counts
├── dataset_ui.py              # UI vs non-UI example helpers
│
├── generate_dataset.py        # Core hand-written React examples
├── styling_examples.py        # Tailwind + CSS Modules
├── styling_scss_examples.py   # SCSS modules
├── quality_examples.py        # Fix / refactor / “when to use” seeds
│
├── seeds/
│   ├── __init__.py            # Aggregates ALL_CURRICULUM_SEEDS
│   ├── extra_seeds.py         # Large migrated seed library
│   ├── folder_structure_examples.py
│   └── generated_curriculum.py  # Generated (run scripts/generate_curriculum.py)
│
├── scripts/
│   └── generate_curriculum.py # Programmatic bulk seeds
│
├── build_dataset.py           # Full pipeline orchestrator
├── split_dataset.py           # Merge, dedupe, train/eval split
├── augment_dataset.py         # Prompt paraphrases → train.jsonl
├── validate_dataset.py        # Lint-style dataset checks
├── check_step2_ready.py         # Step 2 readiness gates
└── neutralize_nextjs.py       # Strip Next.js from seed sources
```

## Adding seeds

1. Add examples with `ex(user_prompt, assistant_code)` from `dataset_common.py`.
2. Place them in the right module (`generate_dataset.py`, `seeds/extra_seeds.py`, `quality_examples.py`, etc.) or extend `scripts/generate_curriculum.py` for templated bulk seeds.
3. Re-run `python build_dataset.py`.
4. Fix anything reported by `validate_dataset.py` or `check_step2_ready.py`.

`seeds/__init__.py` merges curriculum modules for `split_dataset.py`. Duplicates are dropped by hashing the assistant (code) body.

## Validation

`validate_dataset.py` checks examples for:

- Matching styling (Tailwind / CSS Modules / SCSS) to the user prompt
- No class components, legacy lifecycles, or trivial `any`
- Library imports that match the prompt (e.g. Zustand → `from 'zustand'`)
- No stray `next/` usage
- Optional `--report-coverage` for curriculum tags

`check_step2_ready.py` enforces minimum seed counts, per-topic coverage (TanStack Query, folder-structure, etc.), eval size, UI Tailwind ratio, and runs strict validation on seed files.

## Fine-tuning & deployment

This repo stops at **dataset prep**. Next steps (Unsloth QLoRA, eval on `eval.jsonl`, GGUF export, Ollama) are documented in **[PLAN.md](PLAN.md)**.

After export, register the model with the included Modelfile:

```bash
ollama create react-expert -f Modelfile
ollama run react-expert
```

Place your `react-expert.Q4_K_M.gguf` next to the Modelfile or adjust the `FROM` path inside it.

## License

Add a license file if you plan to publish or share the dataset.
