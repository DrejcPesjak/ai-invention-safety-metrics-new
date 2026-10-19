# gen_art_experiment_2 — test_idea

> Phase: `invention_loop` · round 3 · `gen_art`
> Run: `iter1_33370088803c` — Catching Edited Safety Models by Reading Weights in Sliding Windows
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_2` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-13 20:25:17 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact exe... [truncated, 58013 chars total]
```

### [2] HUMAN-USER prompt · 2026-08-13 20:25:17 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [3] SKILL-INPUT — aii-python · 2026-08-13 20:25:23 UTC

The agent loaded the **aii-python** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-python
description: Python coding standards for experiment and evaluation scripts. Covers environment setup, logging, error handling, and code structure.
---

## Environment Setup

- Python 3.12+
- **NEVER use `pip` or `.venv/bin/pip`** — they are not installed. Use `uv` for ALL package operations:
  ```bash
  uv venv .venv --python=3.12
  source .venv/bin/activate  # or: .venv/bin/python script.py
  uv pip install pandas loguru  # NOT: pip install
  ```
- Create `.toml` file with dependencies, create uv `.venv` and activate it
- NO inline dependencies (no `# /// script` headers)

## Logging

Use `loguru` for all logging. Add a file sink alongside stdout.

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")
```

Rules:
- Log every major step (data loading, processing start/end, results)
- If applicable, log every LLM API call input and output
- Truncate long outputs in logs (add truncation logic for potentially large strings)
- Use `logger.error()` in except blocks (traceback auto-captured)

## Error Handling

- Wrap major operations in try/except blocks
- Use `@logger.catch(reraise=True)` decorator on main functions — without `reraise=True`, the script exits 0 even on uncaught exceptions, hiding failures from downstream consumers
- Use explicit exception types, not bare `except:`
- Never silently swallow exceptions — always log them

```python
@logger.catch(reraise=True)
def main():
    try:
        data = load_data(path)
    except FileNotFoundError:
        logger.error("Data file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file")
        raise
```

## Code Structure

- Use `pathlib.Path` for file operations: `Path("data/input.json").read_text()` not `open(...).read()`
- Use type hints for function signatures
- Use keyword arguments for functions with more than 4 parameters
- No hardcoded paths — derive from script location or accept as arguments

## Script Pattern

Standard pattern for experiment/evaluation scripts:

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

from loguru import logger
from pathlib import Path
import json
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    # Load data
    data_path = Path("full_data_out.json")
    logger.info(f"Loading data from {data_path}")
    data = json.loads(data_path.read_text())
    logger.info(f"Loaded {len(data['examples'])} examples")

    # Process
    results = []
    for i, example in enumerate(data["examples"]):
        try:
            result = process(example)
            results.append(result)
        except Exception:
            logger.error(f"Failed on example {i}")
            continue

    # Save output
    output = {"examples": results}
    Path("method_out.json").write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(results)} results")

if __name__ == "__main__":
    main()
```
````

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-08-13 20:25:27 UTC

The agent loaded the **aii-long-running-tasks** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-long-running-tasks
description: Gradual scaling pattern for long-running autonomous tasks. Use when running experiments, evaluations, or any code that processes data at increasing scale with runtime checks.
---

## Core Principles

1. **Time budget first**: Read your time/runtime constraints before running anything. Set every Bash timeout to fit within the budget.
2. **Start small, scale up**: Run on minimal input first, fix errors, then increase scale.
3. **Extrapolate before scaling**: Use recorded runtimes to predict whether the next step fits in the budget. Don't guess — calculate.
4. **Background execution**: For anything that takes >1 min, run in background (`run_in_background=true`) and do useful work while waiting.
5. **Stop early if needed**: Quality results on less data beats a timeout or crash. It's always acceptable to stop at a smaller scale.

---

## Gradual Scaling Sequence

Run code at increasing data sizes, checking runtime at each step.

Substitute your actual file names:
- `{mini_file}` — mini JSON (3 examples) from dependency workspace
- `{full_file}` — full dataset from dependency workspace
- `{script}` — your processing script (e.g., `./method.py`, `./eval.py`)
- `{schema}` — JSON schema to validate output against

**STEP 1 — MINI DATA:** Run `{script}` on `{mini_file}`. Do NOT truncate logs. Fix all errors. Validate output against `{schema}`. Verify you are NOT using mock scripts, mock data, or mock APIs.

**STEP 2 — 10 EXAMPLES:** Modify `{script}` to load only the first 10 examples from `{full_file}`. Run and fix errors. Validate schema. Record the runtime.

**STEP 3 — 50 EXAMPLES:** Load first 50 examples from `{full_file}`. Run and fix errors. Record runtime. **EXTRAPOLATE**: Using runtimes from steps 2-3, estimate time per example. Calculate how many examples fit in your remaining time budget. If 50 already used most of the budget, stop here.

**STEP 4 — 100 EXAMPLES (if budget allows):** Load first 100 examples. Run and fix errors. Record runtime. Re-extrapolate with the new data point.

**STEP 5 — 200 EXAMPLES (if budget allows):** Load first 200 examples from `{full_file}`. Run and fix errors. Record runtime.

**STEP 6 — MAXIMIZE:** Using all recorded runtimes, extrapolate time-per-example (it may not be perfectly linear — account for overhead). Calculate the maximum number of examples that fits within your remaining time budget with a 10% safety margin. Load that many (or all if they fit). Run and validate.

## Final Testing Phase

After completing the scaling sequence, redo the entire sequence **one more time** up to your final example count:

mini → 10 → 50 → 100 → 200 → max

At each scale: look for issues, fix problems, validate output, ensure it completes within time limits.

---

## Background Execution

For any step that takes >1 min, run as a **background task**:

1. Launch with Bash `run_in_background=true`
2. While it runs, use the time productively:
   - Sanity-check previous outputs
   - Verify file integrity (correct field names, non-empty values)
   - Review code for edge cases at larger scale
   - Prepare the next step
3. Check back on the background task to get results
4. If it failed, fix errors and re-run

---

## Resource Limits

Set hard RAM and CPU time limits so code fails fast instead of crashing the system. Read limits from `<hardware>` and leave headroom for the OS (e.g., if 16GB total, cap at 14GB).

Python example using stdlib `resource` module:
```python
import resource
resource.setrlimit(resource.RLIMIT_AS, (14 * 1024**3, 14 * 1024**3))  # 14GB RAM
resource.setrlimit(resource.RLIMIT_CPU, (3600, 3600))  # 1 hour CPU time
```
Exceeding RAM raises `MemoryError`. Exceeding CPU time sends `SIGKILL`.

## Monitoring

At each step, record runtime AND check resource usage (`free -h` for RAM, `top -bn1 | head -5` for CPU). If memory usage is climbing toward the limit or CPU is pegged, stop and investigate before scaling further.
````

### [5] SKILL-INPUT — aii-json · 2026-08-13 20:25:27 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: JSON validation and formatting toolkit. Validate JSON files against schemas for experiment pipelines, and generate full/mini/preview versions of JSON datasets. Use for validating pipeline outputs, checking schema compliance, or creating size-optimized JSON variants.
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Hypothesis Selection & Evaluation:**
- `sel_hypo_out.json` - Hypothesis Selection output (all hypotheses with selected flags)
- `feasibility_eval_all.json` - All hypotheses with feasibility scores
- `feasibility_eval_top.json` - Top 5 most feasible hypotheses
- `novelty_research_one.json` - Single hypothesis novelty research arguments with citations
- `novelty_eval_all.json` - All hypotheses with novelty scores
- `novelty_eval_top.json` - Single best selected hypothesis

**Experiment Pipeline:**
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [6] SKILL-INPUT — aii-file-size-limit · 2026-08-13 20:25:27 UTC

The agent loaded the **aii-file-size-limit** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

```
---
name: aii-file-size-limit
description: File size check procedure for splitting oversized output files. Use after generating JSON output files to check and split files exceeding the provided size limit.
---

## File Size Check

After generating output files, run `ls -lh` to check sizes. If ANY file exceeds the provided file size limit:

1. Create directory with same base name (e.g., `data_out/` for `full_data_out.json`)
2. Split into parts under the limit named: `full_data_out_1.json`, `full_data_out_2.json`, etc.
3. Place parts in directory (e.g., `data_out/full_data_out_1.json`, `data_out/full_data_out_2.json`)
4. Delete the original oversized file
5. Update the script to read from split files: `for f in sorted(glob.glob('data_out/full_data_out_*.json')): data.extend(json.load(open(f)))`
6. For each split part, generate its own mini/preview versions with the json skill's format script
```

### [7] SKILL-INPUT — aii-use-hardware · 2026-08-13 20:25:27 UTC

The agent loaded the **aii-use-hardware** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-use-hardware
description: Detect hardware and use it responsibly. Covers CPU/RAM/GPU detection, memory-safe data processing, and resource-aware computation.
---

**Step 1** — Run `bash scripts/get_hardware.sh` (relative to this skill's directory).

Read the `=== CGROUP ===` section carefully. If `Type: cgroup v1` or `cgroup v2`:
- You are in a **container with hard resource limits**. Exceeding them = OOM kill, no recovery.
- **Never** use `psutil.virtual_memory().total`, `free -h`, `/proc/meminfo`, `os.cpu_count()`, or `nproc` for resource limits — these report **host** values, not your container's allocation.
- **Always** read limits from the cgroup paths shown in the output, or use the Python helpers below.
- For **runtime memory monitoring**, read current usage from cgroup too:
  - v2: `/sys/fs/cgroup/memory.current`
  - v1: `/sys/fs/cgroup/memory/memory.usage_in_bytes`

**Step 2** — Use Step 1 results to pick package variants **before** installing.

Defaults often target the most powerful environment — PyPI's `torch` ships with CUDA libs even on CPU-only hosts. Wrong variant = wasted disk, slow setup, possible import-time failures.

If `=== GPU ===` shows `No GPU`, install torch's CPU build (skips ~4.5GB of CUDA libs):
```bash
uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```
Same idea for any library whose wheel selection depends on detected hardware (GPU/CPU-only builds, architecture-specific wheels).

After install, sanity-check imports right away (`python -c "import torch"`). Disk-pressure or interrupted installs leave half-built wheels (e.g. `libtorch_global_deps.so` missing) — catch these before the experiment runs.

**Step 3** — Set Python constants from the Step 1 results:
```python
import os, math, torch, psutil
from pathlib import Path

def _detect_cpus() -> int:
    """Detect actual CPU allocation (containers/pods/bare metal)."""
    try:  # cgroups v2 quota
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError): pass
    try:  # cgroups v1 quota
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError): pass
    try:  # CPU affinity (cpuset — used by RunPod, Docker --cpuset-cpus)
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError): pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float | None:
    """Read RAM limit from cgroup (containers/pods)."""
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError): pass
    return None

NUM_CPUS = _detect_cpus()
HAS_GPU = torch.cuda.is_available()
VRAM_GB = torch.cuda.get_device_properties(0).total_mem / 1e9 if HAS_GPU else 0
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9
AVAILABLE_RAM_GB = min(psutil.virtual_memory().available / 1e9, TOTAL_RAM_GB)
```

## Step 4 — Set Memory Limits

OOM kills the entire container. **Every script MUST set RAM and VRAM limits at startup.**

Decide the budget based on what the script actually needs. Estimate data size × 2-5x for in-memory overhead, then add ~50% breathing room for temporaries. You may use up to 90% of available RAM/VRAM, but **scale gradually** — start small (e.g. 30-50%), verify it works, then increase toward the limit. Never exceed 90% to keep a buffer for the OS, system processes, and the agent runtime itself. Going over crashes the container/machine with no recovery.

```python
import resource, psutil

_avail = psutil.virtual_memory().available
RAM_BUDGET = ???  # YOU decide: estimate what this script needs (in bytes)
assert RAM_BUDGET < _avail, f"Budget {RAM_BUDGET/1e9:.1f}GB > available {_avail/1e9:.1f}GB"
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))  # 3x: virtual > RSS; raises MemoryError on exceed

if HAS_GPU:
    _free, _total = torch.cuda.mem_get_info(0)
    VRAM_BUDGET = ???  # YOU decide: estimate GPU memory needs
    torch.cuda.set_per_process_memory_fraction(min(VRAM_BUDGET / _total, 0.95))  # raises OutOfMemoryError on exceed
```

## Memory-Safe Data Processing

- **One at a time**: load one large object → process → `del obj; gc.collect()` → next
- **Load only what you need**: select specific tables/columns/rows, not entire databases
- **Test small first**: run on a sample before scaling to full data to estimate memory/time
- **Free intermediates in loops**: don't accumulate large results — aggregate incrementally
- **Size before loading**: check file/dataset size before loading; if it's >30% of `RAM_BUDGET`, chunk it

## Common Mistakes (from real crashes)

- **Skipping this skill entirely** — loading data with no RAM detection, no limits, no budget. Container OOM-killed, all agents lost.
- **Using `psutil.virtual_memory().total` instead of `_container_ram_gb()`** — reports host RAM (e.g. 66 GB) when container limit is 28 GB. You MUST use the cgroup-aware functions above.
- **Loading all tables from a multi-table database at once** — one agent loaded 14 RelBench tables simultaneously, spiked past container limit.
- **Setting no memory limits** — without `resource.setrlimit` (RAM) and `set_per_process_memory_fraction` (VRAM), a runaway script OOM-kills the container instead of raising a catchable error.
- **Using `os.cpu_count()` directly** — returns host CPUs (e.g. 192) instead of container limit (e.g. 4) on RunPod/Docker. Always use `_detect_cpus()` above which checks cgroup quota → CPU affinity → `os.cpu_count()` in order.

## Hardware Use

- Keep these results in mind for ALL subsequent tasks — don't assume more than detected
- GPU if available and parallelizable, multiprocessing if multiple CPUs
- Push available resources to their full potential — don't leave hardware idle
````

### [8] SYSTEM-USER prompt · 2026-08-13 21:51:56 UTC

```
continue where you left off — reuse any partial work already written to disk. Do NOT start over.
```

### [9] SYSTEM-USER prompt · 2026-08-13 22:02:54 UTC

```
continue where you left off — reuse any partial work already written to disk. Do NOT start over.
```

### [10] SKILL-INPUT — aii-data-fig-gen · 2026-08-13 22:03:10 UTC

The agent loaded the **aii-data-fig-gen** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-data-fig-gen
description: Render publication-quality DATA FIGURES (figure_type='data') — bar, line, scatter, heatmap/confusion matrix, box, violin, beeswarm, histogram, ECDF, scaling law, stacked area, forest/CI, Pareto frontier, ROC/PR, volcano, bump/rank, joint scatter with marginals, dendrogram, clustermap, network graph, and multi-panel composites — deterministically from a JSON spec, as vector PDF plus a PNG. Use for any figure that plots numbers. For CONCEPT FIGURES (figure_type='concept') — conceptual artwork, architecture and flow diagrams, anything with no underlying data — use aii-concept-fig-gen instead.
---

# Data figures — charts rendered from their numbers

Deterministic figures from a JSON spec: the numbers go in, matplotlib draws
them, and the picture cannot disagree with the data. Nothing is generated by
a model, so a bar is the height of its value and every axis is computed.
Re-running a spec gives a byte-identical PNG; the PDF differs only in its
embedded creation timestamp.

## Data figure or concept figure?

| The figure is… | Use |
|---|---|
| A chart of numbers you have | **this skill** (data figure) |
| A confusion matrix, ablation grid, correlation | **this skill** (data figure) |
| A scaling law, training curve, Pareto trade-off | **this skill** (data figure) |
| Conceptual artwork, a metaphor, a cover image | `aii-concept-fig-gen` (concept figure) |
| An architecture or flow diagram | `aii-concept-fig-gen` (concept figure — see *Limits*) |

The test is whether the figure has underlying numbers. If it does, an image
model will approximate them — bars that do not match their labels, axis
ticks that do not divide evenly, invented data points. That failure is
invisible to a reviewer of the prompt and obvious to a reviewer of the
paper.

## Use a generator when one fits — hand-write only when none does

The generators are a menu, not a fence. Every type below is a shortcut that
already has the house style, the data-integrity guards and the layout fixes
baked in, so reaching for one is almost always less work than plotting by
hand and the result is consistent with every other figure in the paper.

**Check `--list-types` first.** If a type matches what you need, use it.
Two-thirds of research figures are a bar, a line, a scatter or a heatmap,
and those are solved.

**If nothing fits, write matplotlib yourself** — that is expected and
supported, not a failure. Novel or one-off figures exist. When you do:

```python
import sys; sys.path.insert(0, "<skill>/scripts")
import matplotlib.pyplot as plt
from chart_geometry import assert_text_is_legible, fit_point_labels
from chart_style import (
    apply_house_style, PALETTE, literal, place_legend, place_point_label,
    fit_legends, clear_legends_of_data, fit_tick_labels, fit_titles,
    rasterize_dense_clouds, assert_legends_clear_of_data,
    assert_series_are_distinguishable, assert_axis_names_are_unique,
)

apply_house_style()                 # fonts, palette, grid, Type-42 PDF fonts
fig, ax = plt.subplots(figsize=(7, 3.94), layout="constrained")
...
place_legend(ax, loc="best")        # a legend fit_legends can reflow
place_point_label(ax, literal("Ours"), (1, 2))   # a name, nudged off the data
fit_legends(fig)                    # reflow a legend wider than its axes
clear_legends_of_data(fig)          # move it below the axes if it sits on data
fit_tick_labels(fig)                # wrap/tilt tick labels that would collide
fit_titles(fig)                     # wrap any title wider than its axes
clear_legends_of_data(fig)          # AGAIN — the two above reshaped the axes
fit_point_labels(fig)               # move point names off markers and curves
rasterize_dense_clouds(fig)         # >25k points as a bitmap, text stays vector
assert_text_is_legible(fig)         # raises if any text collides or is cut off
assert_legends_clear_of_data(fig)   # raises if a legend still hides its data
assert_series_are_distinguishable(fig)  # raises on two identical legend keys
assert_axis_names_are_unique(fig)   # raises if one name labels two positions
fig.savefig("figX_v0.pdf")          # vector, so LaTeX renders text at page res
```

Call the fitters in that order — the legend decides how much room the axes
has, whether it then has to move out of the data is only knowable once it is
placed, tick labels change the axes height, the title is measured against the
axes it ends up on, and a point's name can only be placed once nothing above
it will move the point again. `clear_legends_of_data` appears TWICE on
purpose: it decides by measuring, and the two passes between its calls shrink
the axes under a legend that is already placed and a fixed size. A wrapped
title took a lone chart from 179 px of axes height to 141, and a legend that
covered nothing before covered half a curve after — with the mover's turn
already past, so the figure was refused rather than fixed. The first call
still has to happen first, because the room the legend needs is an input to
the passes below it. Two further gates are warning-based and so are
not in the snippet: `assert_layout_applied` and `assert_all_glyphs_rendered`
read what matplotlib warned about during the draw, so they need the figure
built inside `warnings.catch_warnings(record=True)` — worth doing, since a
missing glyph is only ever a warning and ships as a hollow box.
`place_legend` and `place_point_label` are how
the fitters find what to fix: a legend built with a bare `ax.legend` cannot
be reflowed, and a name written with a bare `ax.annotate` will not be moved
off the marker it landed on.

That keeps a hand-written figure looking like the rest of the paper and
still gets you colourblind-safe colours, submission-compliant fonts, no
clipped labels and no overprinted ones. What you lose is the data-integrity
checking — so verify the numbers yourself.

**If you hand-write the same figure type twice, add a renderer instead.**
`chart_renderers*.py` — one function, `(ax, spec) -> None`, registered in
its family's dict. That is how this catalogue got here.

## Use it

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-data-fig-gen"
G="$SKILL_DIR/scripts/chart_gen.py"

python "$G" --list-types            # the catalogue
python "$G" --example bar           # a complete spec to copy and edit
python "$G" --spec fig1.json --out figures/fig1
```

`python` here is the pipeline image's interpreter, which has matplotlib and
scipy installed system-wide. Outside the image use the project venv —
`.venv/bin/python` — since a bare `python3` will not have them.

Writes `figures/fig1.pdf` **and** `figures/fig1.png`. The PDF is the
deliverable — LaTeX renders vector text at page resolution, so it stays
sharp and selectable at any zoom. The PNG exists so you can read the figure
back and look at it.

`--format pdf`, `--format png`, `--format pdf,png,svg` narrows the output.
SVG keeps its labels as TEXT rather than paths, so it stays editable and
searchable. EPS is refused: the PostScript backend cannot draw transparency
and flattens it silently, which the house style uses on nine of every ten
figures — the file would not match the PNG you checked.
`--spec -` reads the spec from stdin.

Runs on `matplotlib` + `numpy`, both already `aii_pipeline` dependencies —
nothing to install.

## The catalogue

`--example <type>` prints a complete spec for any of these. The "instead of"
column is the useful one: most figures have two plausible types and the
choice between them is what decides whether a reviewer reads the point.

### Comparing categories

| type | draws | choose it over |
|---|---|---|
| `bar` | Vertical bars, grouped or stacked, optional error bars. | The default. `barh` if names are long. |
| `barh` | Horizontal bars — labels on the y-axis with room to run. | `bar`, whenever names exceed ~40 chars, or for a ranking. |
| `lollipop` | A stem and a dot per category. | `barh`, past ~20 categories, where bars become a picket fence. |
| `dumbbell` | Two markers per row joined by a line. | Paired bars, when the GAP between them is the story. |
| `slope` | One line per item from a before value to an after value. | Paired bars, when which items changed RANK is the story. |
| `bump` | Rank against time, one line per item; the crossings are the finding. | `slope`, which shows a reordering for exactly TWO time points and cannot show the path between more. |
| `volcano` | Effect size against significance, with both thresholds drawn. | A `bar` of effects, which cannot show what survived correction, or a table of p-values, which cannot show what was big enough to matter. |
| `diverging` | Signed bars either side of zero, sorted. | `bar`, for deltas — direction reads instantly. |
| `waterfall` | Steps from a starting total to a final total. | `bar`, for an ablation — it shows contributions compounding. |
| `bar_sig` | Grouped bars with significance brackets and stars. | `bar`, when the comparison being claimed is pairwise. |
| `forest` | Point estimates with confidence intervals and a null line. | `bar`, when whether an interval crosses zero is the question. |
| `radar` | A closed polygon per method over 3+ metrics. | Several bar charts, for a multi-metric profile at a glance. |
| `parallel` | One polyline per configuration across independently scaled axes. | A table, for a hyperparameter sweep — trends across axes show up. |
| `funnel` | Stage attrition with retention vs. previous and vs. intake. | `barh`, when the stages are sequential and losses compound. |
| `stacked_pct` | Composition as percentages; every bar full height. | Stacked `bar`, when categories have very different totals. |
| `treemap` | Nested rectangles with AREA proportional to value. | `bar`, only when there are too many parts for one axis — length beats area for precise reading. |
| `upset` | Set intersections as sorted bars over a membership matrix. | A Venn diagram, past 3 sets — circles cannot stay area-true and stop reading as sets. |

### Trends and relationships

| type | draws | choose it over |
|---|---|---|
| `line` | Multi-series lines with optional uncertainty bands. | The default for anything against time or steps. |
| `fan` | A median with nested quantile bands around it. | `line` with a band, when the spread is skewed or bounded — a symmetric ± band on an accuracy near its ceiling implies scores above 100%. |
| `step` | A piecewise-constant series — value holds, then jumps. | `line`, for schedules — a slope implies values that never occurred. |
| `scatter` | Points with an optional least-squares fit and R². | `line`, when x is not ordered and the relationship is the point. |
| `joint` | Scatter with the marginal distribution of each variable beside it. | `scatter`, when "and how is each one distributed?" is the obvious next question — which for a headline correlation it always is. |
| `splom` | Every pair of variables as its own scatter, distributions down the diagonal. | `corr`, when the SHAPE of each relationship is the claim — one number cannot tell a straight line from two clusters or an outlier. |
| `bubble` | Scatter with a third variable as marker AREA, plus a size key. | `scatter`, when a third quantity matters but not enough for its own axis. |
| `scaling` | Log-log points with a fitted power law and its exponent. | `line`, for scaling laws — the exponent is computed and annotated. |
| `speedup` | Measured speedup against worker count, with the ideal line. | `line`, for parallel results — the ideal reference is what the claim is measured against. |
| `pareto` | Scatter with the non-dominated frontier drawn through it. | `scatter`, for trade-offs where the frontier is the finding. |
| `area` | Stacked areas — a total and how it divides. | `line`, when the total matters as much as the parts. |
| `residual` | Residuals against fitted values, with the zero line. | Predicted-vs-actual, where heteroscedasticity hides on the diagonal. |
| `bland_altman` | Difference between two methods against their mean, with limits of agreement. | A scatter of A against B, where the diagonal reads as agreement and r = 0.99 hides a 10% offset. |
| `acf` | Autocorrelation per lag as stems, with the significance band. | `line`, which shows the level and hides whether each point predicts the next. |
| `sankey` | Flows between stages at proportional widths. | `area`, when what matters is what became what. |
| `timeline` | Gantt-style spans, one row per task. | A table of timestamps, when overlap and duration are the point. |

### Model evaluation

Give these raw `labels` and `scores` rather than a precomputed curve wherever
you can: the renderer sweeps the threshold itself, so the AUC or AP in the
legend is integrated from the points actually drawn and cannot drift from
the curve beside it.

When only the curve survives — it came from a paper, or from a logged
artefact — pass it directly instead: `fpr`/`tpr` for `roc`, `recall`/
`precision` for `pr`, `probabilities`/`labels` for `calibration`. The
summary statistic is still integrated from the plotted points, so a PR curve
that stops short reports `AP = 0.375 up to recall 0.60` rather than quietly
extrapolating the rest. One evaluation set per figure: `pr`'s baseline and
`calibration`'s bins both move with class balance, so curves from different
test sets cannot share axes honestly.

| type | draws | choose it over |
|---|---|---|
| `roc` | ROC curves with AUC in the legend, plus the chance diagonal. | `pr`, when the classes are roughly balanced. |
| `pr` | Precision-recall curves with average precision and the prevalence baseline. | `roc`, when positives are rare — ROC flatters a rare-class model. |
| `calibration` | Reliability diagram with the ideal diagonal, ECE, and per-bin counts. | `roc`/`pr`, when whether to TRUST a probability is the question. |
| `learning_curve` | Score against training-set size, train and validation with ±std bands. | `line`, to show whether more data or a better model is the bottleneck. |
| `qq` | Sample quantiles against theoretical normal quantiles, with a reference line. | `hist`, for judging normality — the eye reads a straight line far better than a bell. |
| `cd_diagram` | Mean ranks over many datasets, joining methods a test cannot separate. | `bar_sig`, which compares pairwise on ONE dataset — this is the many-datasets headline figure. |

### Distributions

| type | draws | choose it over |
|---|---|---|
| `box` | Median, quartiles, whiskers, outliers per group. | The compact default for a few groups. |
| `violin` | Full mirrored density per group. | `box`, when a distribution may be multi-modal — a box hides that. |
| `strip` | Every raw observation, jittered, with the mean marked. | `box`, when n is small enough that each point should be visible. |
| `beeswarm` | Every observation, packed sideways so none hides another. | `strip`, whose random jitter still overlaps at any real n — the eye reads the clumps as density and they are partly collision. |
| `ridgeline` | Stacked density curves, one row per group. | `violin`, past ~6 groups, where a violin grid gets too wide. |
| `raincloud` | Half violin, box and jittered points together, with n. | `violin`, when the reader must see the observations — twelve seeds look as smooth as twelve thousand. |
| `hist` | Binned counts or density. | `ecdf`, only when the shape of ONE distribution is the point. |
| `ecdf` | Empirical cumulative distribution, stepped. | `hist`, for comparing distributions — no bin width to argue about. |
| `survival` | Kaplan-Meier curves with censoring ticks and confidence bands. | `ecdf`, when some subjects have not finished — an ECDF must drop or invent those. |
| `hexbin` | Hexagonal density bins with a colourbar. | `scatter`, past ~2000 points where it becomes a solid blob. |
| `hist2d` | A joint distribution as a rectangular binned grid. | `hexbin`, when the axes are naturally rectangular. |

### Matrices and fields

| type | draws | choose it over |
|---|---|---|
| `heatmap` | Annotated matrix with a colourbar. | A table, when the pattern matters more than the digits. |
| `seqheat` | A per-token quantity drawn on the tokens themselves. | `heatmap`, for anything measured per token — it puts indices on an axis and leaves the reader rebuilding the sentence from a legend. |
| `corr` | Correlation matrix, diverging map centred at zero. | `heatmap`, for correlations — sign reads from colour direction. |
| `contour` | Filled contours of a 2-D field, levels labelled. | `heatmap`, for a smooth field like a loss surface. |
| `clustermap` | Heatmap with rows and columns reordered into their clusters, trees drawn beside. | `heatmap`, whenever the row order is arbitrary — block structure that is obvious once reordered is invisible in the order the log happened to emit. |
| `catmap` | A grid whose cells hold a CATEGORY, with a discrete legend and no scale. | `heatmap`, for any nominal cell — expert IDs, pass/fail/timeout, which variant won. A ramp asserts that expert 4 is more than expert 1 and that 2 lies between them, and a reader takes the ordering as real. |
| `quiver` | A field of arrows: where each sample is, and where it went. | A `scatter` of the before and after positions, which carries the same numbers and leaves the reader pairing points up by eye. |

### Structure

| type | draws | choose it over |
|---|---|---|
| `dendrogram` | Hierarchical clustering as a tree, branch heights the real merge distances. | `corr`, which shows every pairwise relationship and no grouping. |
| `tree` | A rooted tree from a parent/child structure you already have. | `dendrogram`, which computes its own linkage from a matrix and cannot be given a tree — and `network`, whose force layout loses depth. |
| `network` | A graph as nodes and links, node area and edge width from the data. | A concept figure, for anything with REAL edges — an image model draws a plausible graph, not yours. Use `sankey` for flows between ordered stages and `heatmap` for a dense graph. |

### Composites

| type | draws | choose it over |
|---|---|---|
| `panel` | Any of the above in a lettered grid, `(a)`–`(p)`. | Several separate figures, when they are read together. |

## Spec shape

```json
{
  "type": "bar",
  "title": "Accuracy by benchmark",
  "xlabel": "Benchmark",
  "ylabel": "Accuracy (%)",
  "aspect": "16:9",
  "categories": ["ARC", "GSM8K", "HumanEval"],
  "series": [
    {"label": "Baseline", "values": [41.2, 55.8, 33.1], "errors": [1.8, 2.4, 2.9]},
    {"label": "Ours",     "values": [48.9, 67.3, 45.6], "errors": [1.5, 2.0, 2.6]}
  ]
}
```

Keys every type takes: `title`, `aspect` (`"W:H"`), `width_in` (default 7.0
— a full text-width figure), `font_pt`, `font_family`.

Keys that depend on what the type actually draws. Passing one to a type that
never reads it is REFUSED by name — *"nothing read this key"* — rather than
dropped quietly, so a figure never comes back missing what the spec asked
for. "Applies to" below is therefore the set that is accepted, not a hint:

| key | applies to |
|---|---|
| `xlabel`, `ylabel` | every type with axes, which is all of them but `panel` — a panel has none of its own, so put the labels on the sub-specs and a label at panel level is refused. `radar`, `treemap`, `sankey`, `parallel` and `upset` do read the key, but draw their own geometry with the axis turned off, so the label is accepted and never painted. |
| `xlim`, `ylim` | every type — the shared layer applies them whatever the geometry, so these two are never refused as unread. Limits that would crop data are refused rather than applied. |
| `legend_loc` | only the types that actually draw a legend, i.e. two or more named series. A one-series chart gets none, because a one-entry legend restates the y-label — and asking to place a legend that is not drawn is refused. Takes matplotlib's in-axes placements (`best`, `upper right`, `lower left`, …) and NOT `outside …`: that is what the layout pass itself uses when it moves a legend off the data, and matplotlib accepts it only on a figure legend. You do not need to ask for it — the move happens on its own. |
| `cmap` | only the eight types that encode a value as colour — `heatmap`, `clustermap`, `corr`, `hist2d`, `hexbin`, `contour`, `quiver`, `seqheat`. Anywhere else it is refused: a bar chart given a colour map is a spec expecting colour to carry a meaning that chart never encodes. The default is already perceptually uniform (`cividis`, or `RdBu_r` where the scale has a meaningful zero), so reach for this only with a reason. Rainbow and cyclic maps are refused: `jet` puts a bright band in the middle of a run that is monotonic in the data, and a reader takes the band for a boundary in the result. |

`font_family` REPLACES the font, it does not add a fallback. matplotlib uses
the first family it can find and only that one, so the font you name has to
cover everything on the figure — the script AND the Latin labels, digits and
axis numbers around it. Needed only for a script the default cannot draw —
CJK, Devanagari, Thai — and picking a script-only face (e.g. "Noto Sans Thai",
which has no Latin) trades one set of hollow boxes for another. Measured: with
that font the missing-glyph gate refuses again, naming `l`, `p` and the
digits. See *Legibility*.

Per-type keys are documented by `--example <type>`; start from the example
rather than the schema.

### Multi-panel

```json
{"type": "panel", "title": "Overview", "ncols": 2, "panels": [
  {"type": "bar", "categories": ["A", "B"], "series": [{"values": [3, 5]}]},
  {"type": "line", "series": [{"values": [1, 2, 4, 8]}]}
]}
```

Any chart type nests inside `panels`. Sub-panels are lettered `(a)`, `(b)`…
automatically — do not put the letter in the panel's own `title`, which is
how panel labels end up collided with their titles.

`ncols` and `aspect` both default from the panel count: the grid is squared
(capped at three columns, which is the most that fits at the 7-inch text
width) and the canvas is sized so each cell is about 4:3. Pinning `ncols: 4`
is allowed but leaves each cell 1.75 inches wide, which is narrower than a
labelled chart needs — it will be refused rather than drawn on top of
itself.

## How long text may be

Hard caps, checked before anything is drawn, so an over-long string is a
message rather than a figure with its labels cut off. Each was set by
growing that slot until the figure broke, then backing off:

| key | max | what happened past it |
|---|---|---|
| `title` | 120 | Never refused, never collided — it just ate the canvas. At 600 characters the chart was 38% of its own figure. |
| `xlabel`, `ylabel`, `cbar_label` | 80 | Silently CLIPPED. An x-label ran off both edges from ~90 characters, a y-label from ~50, cut mid-word, at exit 0. |
| `series[].label` | 60 | Legend entries collided at 80 and collapsed the layout at 100. |
| `categories[]`, any other text | 80 | Under a *vertical* bar the limit is 40, with a pointer to `barh` — see *Legibility*. |

A title is a heading; an axis label is a quantity and its unit. Detail
belongs in the caption, which has the full column width and as many lines as
it needs.

These are coarse budgets that cannot know the figure's real width — a
3.5-inch column fits about half as much — so the drawn result is measured
too, and anything that still does not fit is refused with the same kind of
message.

## It refuses rather than lying

The generator exits non-zero, writing nothing, when the figure would not
match its data or a reader would not be able to read it. These were live
defects, each of which exited 0 and produced a confident, plausible, wrong
picture:

- **Length mismatches.** Five categories against three values used to render
  three bars and silently drop two categories. Ragged series were zero-filled,
  inventing measurements nobody made.
- **NaN / Infinity / null / strings in values.** matplotlib draws NaN as
  *nothing*, so the gap reads as a measured zero.
- **Right-to-left text.** matplotlib does no bidi reordering and no Arabic
  joining, so Hebrew and Arabic draw left to right in isolated forms —
  reversed and unjoined. Every glyph exists, so the missing-glyph gate above
  sees nothing; the reader who can read the script is the first to know.
- **Glyphs the font cannot draw.** A missing glyph renders as a hollow box
  and matplotlib only warns. It is machine-dependent too: CJK looks right on
  a laptop with a CJK font and ships as boxes from the pipeline image.
- **Labels printed over each other.** Measured on the drawn figure, on the
  ORIENTED box of each label so a tilted tick is judged on its ink rather
  than on the much larger box around it. A 7x7 correlation matrix forced to
  `21:9` rendered its cells as `0.290.360.581.00`.
- **Labels running off the canvas.** A 300-character x-label was drawn with
  30% of itself visible, cut mid-word at both ends, with no warning.
- **A legend sitting on the data it explains.** The legend is opaque by
  design, so whatever is under it is gone rather than faint. A lone chart's
  legend is measured after layout and moved below the axes; a panel cell has
  nowhere to move it and is refused. A `timeline` in a two-column grid drew
  its legend over eight of its nine bars, and the `bar` cell beside it had
  its bar TOPS masked — GSM8K reading as ~40 where the spec said 55.8.
- **Keys nothing reads.** `x_label`/`y_label` instead of `xlabel`/`ylabel` is
  a natural guess; it used to be accepted in silence and the figure came back
  with no axis labels at all — failing the first item on your own checklist,
  visibly only if you look closely. Every key is now checked against what the
  render actually looked up, at every level, so a typo inside a series or a
  panel is caught too, and the message suggests the real spelling.
- **A series drawn without a name while its neighbours have one.** The
  legend names only the series that carry a `label`, so the rest are drawn
  and left unidentified — three series with two labelled shows blue, amber
  and green bars and names two colours. Nothing about the picture looks
  wrong, which is what makes it worth refusing. Naming none of them is fine:
  that is a chart with one meaning, and the y-label carries it.
- **A stated limit that crops the data.** `xlim`/`ylim` outside the values,
  `vmin`/`vmax` outside the matrix, or an explicit `levels` list narrower than
  `z`. Each one hides part of the finding while the axis or colourbar states a
  range the data does not have: `vmax: 0.3` on a matrix running 0.10..0.95
  painted 0.30 and 0.95 the identical yellow under a bar labelled
  0.100..0.300, and `levels: [2.6..3.2]` over a field of 2.3..4.6 left 70% of
  the plot area as bare page — the basin holding the optimum included, drawn
  exactly like no-data. Cropping is a legitimate wish; it just has to be a
  stated one, so widen the limit or drop it and let the axis fit.
- **Non-positive values on a log axis.** matplotlib MASKS them rather than
  complaining, so the figure comes back with fewer points than the data. Five
  points drawn trending up carried a fit annotation reading `y = -1.75x +
  53.2`, because the slope was still computed over the two at `x = 0` that the
  reader cannot see. Applies wherever `logx`/`logy` does — `line`, `scaling`,
  `scatter`, `pareto`.
- **A negative band in a stacked chart.** Bands and segments are drawn end to
  end, so a negative one folds back over the one beneath it and every height
  stops matching its value: 10 / -8 / 5 drew as three bands of 10 / 8 / 5,
  with a top edge of 10 where the total is 7. Use `line` with one line per
  part for signed quantities. Same for stacked `bar` and `stacked_pct`.
- **Tied scores in a `bump` chart.** It has one row per rank, so a tie can
  only be broken by the order the series happen to appear in — two models
  level at 80.0 drew as a permanent one-rank gap, and moving them past each
  other in the spec, numbers unchanged, showed a crossing that is not in the
  data. Crossings are what this chart type is read for. Use `line`, or
  `slope` for two periods, which draw the scores themselves.
- **Two series a reader cannot tell apart.** The palette holds eight colours
  and wraps; the dash pattern is a second channel and multiplies that to 32
  for line charts, but a solid shape has no dash. A twelve-series `bar`
  shipped four PAIRS of identical swatches and a fifty-series `line` wrapped
  both channels at series 32. Measured on the drawn legend, so it holds for
  bars, lines and markers alike — and `bubble`'s size key, whose entries
  share a colour on purpose, is judged on size as well and passes.

Errors name the offending key and index (`series[1].values has 2 entries but
5 were expected`), so a bad spec is one edit from correct. Nothing partial is
ever written — a half-file would pass the downstream existence check.

## Legibility

- **Non-Latin scripts.** The default font covers Latin, Greek and Cyrillic —
  all three verified, not assumed. Hebrew and Arabic are refused even though
  the glyphs are there: matplotlib does no bidi reordering and no Arabic
  joining, so it draws the characters left to right in isolated forms and the
  label comes out reversed and unjoined, with every glyph present and nothing
  else noticing. Transliterate, or write the label in the paper's own script.
  For any other script set
  `font_family` (e.g. `"Noto Sans CJK JP"`) — matplotlib uses the *first*
  resolvable family and does no per-glyph fallback, so the covering font has
  to go first. Without it the figure is refused rather than shipped full of
  boxes.

  **`font_family` only helps where that font is installed, and the pipeline
  image has none.** It ships 23 families, not one of which covers CJK, Indic
  or Thai — so inside the image the escape hatch resolves to nothing and the
  figure is refused either way. The refusal now names the FONT rather than
  the script: a name that does not resolve is caught before anything is
  drawn, with the closest installed families listed, because matplotlib
  otherwise falls back in silence and the glyph gate then blames the text.
  Label it in Latin script, or add the font to
  `Dockerfile.pipeline` (Noto Sans CJK is ~20 MB). On a developer machine
  with the font present it works: verified rendering a Japanese title and
  Japanese category labels with no missing glyph.
- **Dense categories.** Labels wrap when long, tilt at 30° when that isn't
  enough, and stand up at 90° when even that collides — where neighbours
  cannot touch however long they get. Which of the three applies is decided
  by MEASURING the drawn labels against the axes after layout, so a panel
  cell gets the treatment its own width needs rather than the one the whole
  figure's width would suggest. Names past ~40 characters do not fit under a
  vertical bar at all and are refused with a pointer to `barh`, which puts
  the label on the y-axis where the full width is available.
- **Column-width figures.** `width_in: 3.5` works for the ordinary types —
  bar, barh, line, scatter, box, hist, ecdf, heatmap — provided the spec is
  written for that size: about four categories, two or three series, and a
  title under ~45 characters. These of the catalogue's own examples are
  refused at 3.5 inches, because each is written for the full text width —
  the list is pinned by a test that measures it, so it cannot go stale:

  > `bar_sig`, `bland_altman`, `bubble`, `bump`, `catmap`, `cd_diagram`,
  > `clustermap`, `contour`, `corr`, `dendrogram`, `dumbbell`, `fan`,
  > `funnel`, `panel`, `parallel`, `radar`, `sankey`, `seqheat`, `slope`,
  > `speedup`, `survival`, `timeline`, `treemap`, `upset`, `volcano`

  A leaner spec fits for every one of them — measured, including the
  label-dense ones (`corr`, `upset`, `sankey`, `treemap`, `parallel`,
  `radar`, `cd_diagram`), which only refuse above a lower ceiling than the
  ordinary types. Three one-letter categories draw at 3.5 inches; `upset`
  is the tightest, taking two sets before its own "Intersection size" axis
  label runs off the edge. What the list above says is that the SHIPPED
  EXAMPLES do not fit, because each is written for the full text width.
  Every refusal names what is in the way, and `upset` and `cd_diagram`
  quantify it ("the method names need 4.2 inches of margin") rather than
  shipping something unreadable.
- **Many series.** Past eight the palette wraps, so the line style becomes a
  second channel — otherwise series 1 and 9 were the same colour. Past six,
  the legend moves below the axes. Inside, it
  covered the data at twelve series and hid a tick label; outside, layout
  reserves real space for it.
- **Long titles** are measured after layout and wrapped. On a chart whose
  axes is a narrow strip (a `barh` with long names) the title is promoted to
  a figure heading, since an axes title would centre on the strip and run
  off the page.
- **`$` is safe.** A matched pair used to be read as mathtext, so
  "Cost $5 to $9" rendered as "Cost 5to9". All user text is now escaped, so
  dollars print verbatim. The trade: mathtext is unavailable — write
  superscripts in Unicode (`R²`, `10⁻³`), which the fits already do.

## What the house style already handles

Do not re-solve these; they are set globally in `chart_style.py`.

- **Colourblind-safe palette** (seaborn's `colorblind` set). Never override
  it with a red/green pair. The separations are measured, not assumed: the
  closest pair is ΔE*ab 14.0 under protanopia and 10.3 under deuteranopia,
  against a just-noticeable difference of ~1. **Greyscale print separates
  the first three series and no more** — past that the lightnesses cluster,
  and violet against grey is ΔL* 0.3, the same shade in print. If the paper
  will be read in B&W, keep it to three series or give the extras a second
  channel of your own.
- **Sans-serif**, sized for the figure's final print size.
- **No chartjunk** — no 3D, gradients, shadows, coloured plot background;
  faint horizontal grid behind the data only.
- **Constrained layout**, so an axis label can never be clipped off the
  canvas. This was the single most common defect across every library
  surveyed, including in otherwise flawless output. Layout alone does not
  cover TITLES — it reflows axes but cannot wrap a line — so titles wider
  than their axes are measured after layout and wrapped.
- **TrueType (Type 42) fonts, never Type 3.** matplotlib emits Type 3 by
  default and **IEEE and ACM submission systems reject PDFs containing
  it**, so every default matplotlib figure is non-compliant.
- **Legend headroom** — the y-range is widened before an inside legend is
  placed, because `loc="best"` lands on the data when nothing is free. Where
  headroom cannot help — a horizontal chart, whose free space is on the
  x-axis, or a plot area that is full by construction — the placed legend is
  MEASURED against the drawn bars and moved below the axes if it covers any.
- **Very dense point clouds are drawn as a bitmap inside the vector file.**
  A scatter writes every marker as its own path — 360,000 points is a 5.7 MB
  PDF, and six of those do not fit a venue's upload limit. Past ~25,000
  points in one series the cloud alone is rasterized; the axes, ticks,
  labels and legend stay vector, so the text is still selectable and sharp
  at any zoom. Below that threshold the bitmap would be the *larger* of the
  two, so nothing changes.
- **Cell annotations are outlined against their own fill.** A heatmap's
  numbers take near-black or near-white, whichever contrasts better with the
  cell — and over a continuous colour map the better one is not always
  enough: cividis bottoms out at 4.18:1 and RdBu_r at 4.19:1, against the
  4.5:1 the rest of the style holds itself to, in exactly the mid-range cells
  that make up most of a matrix. A hairline in the opposite ink fixes that
  without touching the map, which is the part that cannot change.
- **Sub-decade log axes keep their tick labels.** A log axis spanning less
  than one decade — a loss curve from 2.90 to 2.05, say — contains no power
  of ten. matplotlib ticks only at powers of ten, so it places 10⁰ and 10¹,
  *both outside the view*, and the visible axis carries no label at all.
  Silently. Handled.

## Verify what you generated

Read the PNG back and look at it. The generator prevents the structural
defects above, but it cannot know that your data was wrong. Check:

- every number in the figure matches the number you meant to plot;
- axis labels state units;
- the caption describes what is actually drawn;
- the chart type still says what you meant once you can see it.

Two things that used to be on this list are now refused instead, so a figure
you can read back cannot have them: overlapping category labels, and a
series drawn without a name while its neighbours have one.

If a figure is crowded, widen `aspect` (`"21:9"`) or split it into a
`panel` — do not shrink the font.

## Limits

- **Hand-drawn architecture diagrams** (a pipeline, a block diagram, a
  flowchart with prose in the boxes) are out of scope: they have no
  underlying numbers and a layout engine has nothing to compute from. Those
  go to `aii-concept-fig-gen`. A graph whose edges ARE data — citations,
  message counts, co-occurrence — is a `network` here, because the picture
  has to match the edge list.
- **No LaTeX-native output.** PGFPlots produces the best camera-ready
  result of anything surveyed, because the figure text is typeset by the
  paper's own engine in the paper's own font. What is missing is a second
  backend behind 60 renderers, not the toolchain: `texlive-pictures` is
  already in the pipeline image, pulled in as a dependency of
  `texlive-latex-extra`, and a pgfplots document compiles there at exit 0.
  (This entry used to say the package was absent and would cost +81 MB.
  Measured in the built image, both halves were wrong.)
- **The legibility gate reads TEXT.** It refuses a label printed over another
  label or cut off by the canvas. A label printed over the DATA is only
  handled where a renderer registers it with `place_point_label`, which five
  types do: `pareto`, `network`, `tree`, `volcano` and `bubble`. If you
  hand-write a figure, call `fit_point_labels` too.
  `bubble` registers only the names it draws OUTSIDE their disc — a name
  small enough to sit inside its own bubble is already where it belongs and
  no nudge improves it. That registration became worth doing once the
  clearance test started measuring each marker against ITS OWN radius: with
  a single radius for the axes (the largest drawn) a bubble field running
  4 px to 88 px left no candidate position measuring clean, so every name
  stayed on its first guess.
  One limit remains, and it is the candidate SET rather than the model: the
  nudger tries corners a few pixels out, which cannot clear a very large
  neighbouring disc. On a crowded bubble chart a small bubble's name can
  still touch a big one — give those names in a legend, or space the points.
- Still uncovered: geographic/choropleth (needs a basemap and boundary data,
  neither of which is in the image). Add a renderer to its family's
  `chart_renderers*.py` rather than hand-writing matplotlib at the call site
  — that is what keeps every figure in a paper looking like a set.
````

### [11] SYSTEM-USER prompt · 2026-08-13 23:00:54 UTC

```
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_art/gen_art_experiment_2`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_art/gen_art_experiment_2/`:
... [truncated, 58129 chars total]
```

### [12] SYSTEM-USER prompt · 2026-08-13 23:03:07 UTC

```
<CRITICAL_ERROR>
Some files in your workspace exceed the 100MB size limit for GitHub deployment.

OVERSIZED FILES:
  - results/root_sd.pt (3875.3 MB)

You MUST reduce these files to under 100MB each. Use ONE of these strategies:

=== STRATEGY 1: SPLIT FILES (PREFERRED) ===
Split large files into smaller parts and update code to read them sequentially.

For data files (JSON, JSONL, CSV, Parquet):
1. Split the file into parts under 100MB each:
   - data.jsonl -> data_part_001.jsonl, data_part_002.jsonl, ...
2. Update ALL code that reads this file to handle the split parts
3. Delete the original large file after splitting

=== STRATEGY 2: COMPRESSION (FALLBACK) ===
Only use if splitting is not feasible (e.g., binary files, model weights).

1. Compress the file with gzip
2. Update ALL code to decompress before use
3. Delete the original uncompressed file

=== REQUIRED: UPDATE AND TEST CODE ===
After applying your chosen strategy, you MUST:

1. Find ALL code files that reference the modified files (use grep/search)
2. Update each file to work with the new format (split parts or compressed)
3. Run the updated code to verify it still works correctly
4. Fix any errors that occur until the code runs successfully

Do NOT skip testing - the code must actually execute without errors.

Start by listing the oversized files with `ls -lh`, then apply the appropriate strategy.
</CRITICAL_ERROR>
```

### [13] SYSTEM-USER prompt · 2026-08-13 23:20:07 UTC

```
<CRITICAL_ERROR>
Some files in your workspace exceed the 100MB size limit for GitHub deployment.

OVERSIZED FILES:
  - hf_home/hub/models--Qwen--Qwen3-1.7B/snapshots/70d244cc86ccca08cf5af4e1e306ecf908b1ad5e/model-00001-of-00002.safetensors (3281.8 MB)
  - hf_home/hub/models--Qwen--Qwen3-1.7B/blobs/169ad53ec313c3a34b06c0809216e4fc072cce444a5d4ff2b59690d064130ed5 (3281.8 MB)
  - hf_home/hub/models--Qwen--Qwen3-1.7B/snapshots/70d244cc86ccca08cf5af4e1e306ecf908b1ad5e/model-00002-of-00002.safetensors (593.5 MB)
  - hf_home/hub/models--Qwen--Qwen3-1.7B/blobs/912becff8d60672aa8628ef08c05898d9adf17c2ad4ae3caf99b065622fdeff9 (593.5 MB)

You MUST reduce these files to under 100MB each. Use ONE of these strategies:

=== STRATEGY 1: SPLIT FILES (PREFERRED) ===
Split large files into smaller parts and update code to read them sequentially.

For data files (JSON, JSONL, CSV, Parquet):
1. Split the file into parts under 100MB each:
   - data.jsonl -> data_part_001.jsonl, data_part_002.jsonl, ...
2. Update ALL code that reads this file to handle the split parts
3. Delete the original large file after splitting

=== STRATEGY 2: COMPRESSION (FALLBACK) ===
Only use if splitting is not feasible (e.g., binary files, model weights).

1. Compress the file with gzip
2. Update ALL code to decompress before use
3. Delete the original uncompressed file

=== REQUIRED: UPDATE AND TEST CODE ===
After applying your chosen strategy, you MUST:

1. Find ALL code files that reference the modified files (use grep/search)
2. Update each file to work with the new format (split parts or compressed)
3. Run the updated code to verify it still works correctly
4. Fix any errors that occur until the code runs successfully

Do NOT skip testing - the code must actually execute without errors.

Start by listing the oversized files with `ls -lh`, then apply the appropriate strategy.
</CRITICAL_ERROR>
```
