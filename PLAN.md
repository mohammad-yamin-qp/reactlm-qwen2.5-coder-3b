# Custom React Developer LLM — Build Plan

---

## Step 1: Select the Base Model

For a coding-specific model under 4B parameters, use state-of-the-art open-weights models.

**Top Recommendation: Qwen2.5-Coder-3B**
- Heavily optimized for code generation
- Fits on standard consumer hardware
- Outperforms comparably-sized general models on code benchmarks

**Alternative: Llama 3.2 (3B)**
- Meta's lightweight model, fast inference, strong reasoning

---

## Step 2: Build the "React Golden Dataset"

The model learns from **Instruction → Response** pairs, not documentation.

Target **~900–1,100 unique seeds** (senior React + ecosystem curriculum), **~3× paraphrase**
for **~2,500–3,200** `train.jsonl` rows. Quality over arbitrary row caps — run
`python check_step2_ready.py` to confirm Step 2 is complete.

> **Quality beats quantity.** Unique, linted scenarios outperform thousands of
> near-duplicate prompt variants with identical answers. Validate seeds before augmenting.

> **React-first, not Next.js.** Training data uses React 19 patterns (`'use server'`,
> Server Components, Server Actions) without `next/*` imports or Next.js-specific APIs.
> Re-run `python neutralize_nextjs.py` after editing dataset sources if needed.

### What your data must cover

| Focus Area | Examples to Include |
|---|---|
| React 19 features | `useActionState`, `useFormStatus`, `use()` API, Server Actions |
| Server vs. Client Components | When to add `'use client'` vs. keeping a Server Component |
| Performance | `useMemo`, `useCallback`, `React.memo`, `Suspense`, `lazy()` |
| Accessibility | ARIA roles, semantic HTML, keyboard navigation |
| TypeScript | Fully typed props, generics, no `any` |
| **Tailwind CSS** | Utility classes, responsive (`sm:`/`md:`), `dark:`, forms, modals, tables |
| **CSS Modules** | `*.module.css` imports, `styles.className`, composition, co-located CSS |
| **SCSS modules** | `*.module.scss`, variables, mixins, nesting, `@use`, co-located Sass |
| **React patterns** | Compound components, provider + hooks, controlled/uncontrolled, composition |
| **Ecosystem** | TanStack Query, Zustand, Redux Toolkit, XState, GraphQL (urql/Apollo), RHF + Zod |
| **Animation** | GSAP, Framer Motion |
| **Testing / docs** | Vitest, React Testing Library, MSW, Storybook |
| **Routing / UI** | React Router v6+, shadcn/ui + Radix |
| **Senior judgment** | “When to use what” comparison seeds (Query vs fetch, Zustand vs Redux, etc.) |

**Deferred (v1):** TanStack Start, full MUI/Ant Design API — use Context7 MCP at inference for version-specific docs.

### Styling rules (training + inference)

- User asks for **Tailwind** → assistant uses Tailwind utility `className`s (no CSS Modules in that component).
- User asks for **CSS Modules** → assistant imports `*.module.css` and uses `styles.*` (include the `.module.css` file in the answer).
- User asks for **SCSS / Sass** → assistant imports `*.module.scss`, uses `styles.*`, and includes the `.scss` source (variables, nesting, mixins as appropriate).
- User does not specify → default to **Tailwind** for new UI (per system prompt).
- Do **not** mix Tailwind, CSS Modules, and SCSS in one component unless the prompt is a comparison/migration example.

Examples: `generate_dataset.py`, `seeds/` (curriculum modules), `styling_examples.py`; shared prompt in `dataset_common.py`.

### Dataset pipeline (quality-first)

```bash
python build_dataset.py         # full pipeline + check_step2_ready.py
# — or step by step —
python generate_dataset.py
python scripts/generate_curriculum.py   # seeds/generated_curriculum.py
python split_dataset.py
python validate_dataset.py all_seeds.jsonl --strict-seeds
python augment_dataset.py               # ~3× paraphrase → train.jsonl
python check_step2_ready.py
```

**Alternate fine-tune set:** use `train_seeds.jsonl` (unique seeds only, no paraphrase) for maximum uniqueness on small models.

| File | Purpose |
|------|---------|
| `all_seeds.jsonl` | All unique seeds (deduplicated) |
| `train_seeds.jsonl` | ~90% — paraphrase allowed |
| `eval.jsonl` | ~10% — **never** paraphrased; use for Step 5 eval |
| `train.jsonl` | Fine-tuning set |

### JSONL structure

Each line is one training example:

```json
{
  "conversations": [
    { "role": "system", "content": "<see dataset_common.py SYSTEM_PROMPT>" },
    { "role": "user", "content": "Create a React Server Component that fetches a list of users and passes them to a Client Component with a search bar." },
    { "role": "assistant", "content": "<your flawless TypeScript/React code here>" }
  ]
}
```

---

## Step 3: Chat Template

**Do not hand-format ChatML tokens yourself.**

Qwen2.5-Coder uses `<|im_start|>` / `<|im_end|>` tokens internally. Unsloth's
`get_chat_template("qwen-2.5")` applies the correct template automatically when
you call `apply_chat_template()` on your dataset. Manual formatting will cause
token misalignment.

---

## Step 4: Fine-Tune with QLoRA + Unsloth

No supercomputer required. Use Google Colab (free T4) or a rented GPU (RunPod A40, ~$0.30/hr).

### Why Unsloth

- Up to 2× faster training than standard HuggingFace
- ~70% less VRAM via 4-bit quantization (QLoRA)
- Built-in GGUF export

### How QLoRA works

The base 3B weights are frozen at 4-bit precision. Unsloth trains only a small
set of adapter weights (LoRA layers). Final adapter is merged back into the base
model before export. Training time: **2–5 hours** on a single GPU.

### Key training config (starting point)

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen2.5-Coder-3B-Instruct",
    max_seq_length=4096,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,               # LoRA rank
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
)
```

---

## Step 5: Evaluate Before Exporting

Hold out **5–10% of your dataset** (never seen during training) as an eval set.

Before exporting, run inference on 20–30 eval prompts manually and check:
- Does it default to `'use client'` unnecessarily?
- Does it still use class components or `componentDidMount`?
- Is TypeScript correct and non-trivially typed?

Only proceed to export once the eval results meet your quality bar.

---

## Step 6: Quantize and Export (GGUF)

Unsloth exports GGUF directly:

```python
model.save_pretrained_gguf("react-expert", tokenizer, quantization_method="q4_k_m")
```

- Output: `react-expert.Q4_K_M.gguf`
- File size: ~**1.9 GB** for a 3B model at Q4_K_M
- Ready to load in Ollama

---

## Step 7: Deploy with Ollama + Modelfile

Simply placing the GGUF in Ollama is not enough — without a `Modelfile`, every
session starts without the React system prompt and the model reverts to generic behavior.

Create a `Modelfile` alongside your GGUF:

```dockerfile
FROM ./react-expert.Q4_K_M.gguf

SYSTEM """
You are an expert React 19 frontend developer. Always write clean, accessible,
and highly performant functional components using TypeScript. Default to Server
Components unless interactivity requires 'use client'. Never use class components.
Use Tailwind CSS when the user asks for Tailwind or for unspecified UI styling.
Use CSS Modules (import from *.module.css) when the user asks for CSS Modules or
scoped/modular CSS. Do not mix Tailwind and CSS Modules in one component unless asked.
"""

PARAMETER temperature 0.2
PARAMETER num_ctx 4096
```

Then register and run:

```bash
ollama create react-expert -f Modelfile
ollama run react-expert
```

---

## Step 8: IDE Integration (Optional but Recommended)

Use **Continue.dev** (VS Code / JetBrains plugin) to wire your local Ollama model
into your editor for inline completions and chat — no API calls, fully offline.

Config in `~/.continue/config.json`:

```json
{
  "models": [{
    "title": "React Expert (Local)",
    "provider": "ollama",
    "model": "react-expert"
  }]
}
```

---

## Summary

| Step | Action | Tool |
|---|---|---|
| 1 | Pick base model | Qwen2.5-Coder-3B |
| 2 | Build + validate senior dataset | `build_dataset.py` → `check_step2_ready.py` |
| 3 | Apply chat template | Unsloth `get_chat_template()` |
| 4 | Fine-tune | Unsloth + QLoRA on Colab/RunPod |
| 5 | Evaluate | Held-out eval set, manual review |
| 6 | Export | GGUF Q4_K_M (~1.9 GB) |
| 7 | Deploy | Ollama + Modelfile with system prompt |
| 8 | Integrate | Continue.dev in VS Code |
