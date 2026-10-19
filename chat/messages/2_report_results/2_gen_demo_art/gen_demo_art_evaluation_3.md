# gen_demo_art_evaluation_3 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `iter1_33370088803c` — Catching Edited Safety Models by Reading Weights in Sliding Windows
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_evaluation_3` (terminal_claude_agent, claude-opus-5)

### [1] CONFIG · 2026-08-14 07:38:12 UTC

```
model: claude-opus-5 | effort: medium | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins
```

### [2] SYSTEM-USER prompt · 2026-08-14 07:38:18 UTC

````
<conversion_philosophy>
**MINIMAL CHANGES — PRESERVE THE ORIGINAL CODE**

The goal is to make the artifact's code READABLE, UNDERSTANDABLE, and RUNNABLE in a short time
to someone reviewing the research, with the option to easily scale parameters back to original
values for a full run (which can take much longer). Think of this as annotating and reformatting,
not refactoring.

**DO:**
- Split the original script into logical notebook cells (imports, setup, processing, results)
- Add markdown cells BETWEEN code cells explaining what each section does and why
- Add inline comments where the logic is non-obvious
- Add a visualization/summary cell at the end showing key outputs
- Fix hardcoded file paths to use the GitHub data loading pattern

**DO NOT:**
- Rewrite functions or change algorithms
- Rename variables or restructure logic
- Add error handling, type hints, or "improvements" that weren't in the original
- Simplify or "clean up" the original code
- Remove any original comments or logic
- Change the computational approach

The reader should recognize the original script when looking at the notebook — it's the
same code, just split into cells with explanatory markdown between sections.
</conversion_philosophy>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins/`:
GOOD: `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins/file.py`, `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<task>
Convert this artifact's Python script into a demo notebook with MINIMAL changes to the original code.
Split into cells, add markdown explanations between sections, add a visualization cell at the end.
Output: mini_demo_data.json + code_demo.ipynb (notebook that loads data from GitHub URL)
</task>

<artifact_info>
id: art_ckuwEkspyins
type: evaluation
title: Rechecking every number in the draft
summary: |-
  PURE RE-ANALYSIS, $0.00 LLM spend, 0 weights loaded, 0 forward passes, 0 generations, 0 Hub fetches, ~21 s on 4 CPUs. Reads the six archived trees (A1-A4 as declared deps, plus A5 iter-3 evaluation-1 and A6 iter-3 research-1 read directly from disk). Every file resolved by GLOB, never by assumed filename; manifest with size+sha256+role; every emitted number carries provenance = {file, line_or_key, raw_value}.

  ASSERTION TABLE: 110 claim_ids -> 105 MATCH / 5 MISMATCH / 0 UNAVAILABLE. Tolerances declared up front (1e-6 verbatim, 1e-4 float re-derivation, 0.005 reconstructed rates, exact string for repo_ids/evidence spans). GATES: A2/verify.py re-run 17/17 PASS; A1 wstats max|dW05| = 9.91e-06 (gate.json full precision 9.908662263136137e-06, so the quoted '9.9e-06' is a 2-s.f. rounding), Spearman 1.0000, ordering preserved. DETERMINISM: two full runs BYTE_IDENTICAL_APART_FROM_TIMING.

  THE 5 DISAGREEMENTS (the product, each classified): (1) crossing.jsonl holds SEVEN real intensity axes (4 EVADABLE + 3 NEITHER_DIES) plus one 'combined' non-axis row - the per-verdict counts are right, the denominator quoted as 6 is stale. (2) scan.jsonl gives 81 UNRESOLVED non-control rows, not 65 - the 65-vs-81 discrepancy is adjudicated mechanically, 65 is stale. (3) 8 SKIPPED, not 7. (4) quoted_value_forensics carries FIVE unreproduced quoted values (A01, A02, A22, B09, W01), not four. (5) B09's 0.766 is the 26-member renderer=='chatml' value (reproduces to 1e-4); on the 28-member contract subset the draft states it is 0.670 - the number was right, the SUBSET LABEL was not; the other four reproduce under NONE of 32 conventions and must be regenerated.

  W1 RELABEL: decision rule published as a literal dict; relabel fires only on a verbatim toolkit string. Two Heretic checkpoints -> per_component_optimised (APPLIED); mlabonne and BennyDaBall -> unknown, NOT_IN_ARCHIVE, PROVISIONAL (mlabonne's Gaussian-depth string is NOT in the archived card text - no kernel is inferred from W05). Honest count: 2 of 4 misses carry a verbatim non-uniform kernel string, unattributed remainder 2. LEAVE-ONE-RECIPE-CLASS-OUT (primary) is where the failure lives: per_component_optimised AUROC 0.264 / sensitivity 0.000 vs uniform_global 0.956 / 0.900; leave-one-uploader-out shipped beside it, identical columns. Limitation 3 REFUTED from A6: sub-4.2B MPOA / Heretic / OBLITERATUS at 4,022,468,096 params on the panel's own Qwen3-4B family. 6-entry draft_edit_list.

  W2 LADDER: 136 interval rows, Wilson primary + 10k bootstrap, ACHIEVED denominators recovered as the LARGEST n <= nominal (31-40, not 40; root 6/37 = 0.162 [0.077, 0.311]). All four signed evasion costs (-0.004, +0.07, +0.07, +0.1) and int4-minus-root (-0.03 [-0.189, +0.135]) are NOT A RESOLVABLE DIFFERENCE. Power: smallest UPWARD detectable difference at n=40, p=0.20 is 0.29, so the ORDERING survives and the decimals do not.

  W3 E_1 BANDS: the archived [0.25,0.75] band reproduces the arm-2 headline exactly (12 pairs 1.000/1.000/+0.000; 15 pairs E_1 1.000 vs W05 0.833, diff -0.167; 41 pairs -0.186 [-0.373,-0.076]). FULL STACK and [0.4,0.6] are NOT_RECOMPUTABLE_FROM_ARCHIVE - per-matrix singular values were never persisted - so the verdict is withheld as UNDETERMINED_INSUFFICIENT_BANDS (INVARIANT at the primary band only, 3/3 checks hold) rather than answered on one band. Synthetic dependence made visible: excluding the 26 in-house synthetics the interval becomes -0.167 [-0.444, 0.000] and COVERS ZERO.

  W4 COST TABLE: 54 rows sorted cost-ascending with prompts / harmful_prompts / forward passes / wall-clock, correlations carried forward verbatim (recomputed=false). 0 candidates beat B09 positively (the one CI excluding zero is W02 at -0.457, i.e. worse). Practitioner sentence bound to provenance: interior observables ARE predictive (A19 rho +0.763 [+0.592,+0.864] member, +0.800 lineage) but do not beat a 40-prompt greedy refusal rate.

  W5 FIDELITY: counts generated from rows (270 = 20 controls + 250 attempted, 160 completed); boundary at full precision -2.7415117804288127 with the abliterated MAXIMUM/minimum stated correctly (-2.7415 / -4.8204, margin 0.0763); oriented-vs-raw AUROC with a convention string; [min,max] for every class x W01-W05 with the base/abliterated overlaps flagged; W03 corrected to 256 directions; the 4.869-vs--4.82 adjacency flagged with a suggested rewrite. Eligibility filter: 85 eligible of 160 (48 n_layers<8, 38 hidden_size<128, 38 name/tag, 4 oversize), FP 0/85 Wilson [0, 0.0432] PRIMARY vs 0/160 [0, 0.0234] SECONDARY. Threshold brittleness: first false positive at -2.61 (rinna/japanese-gpt-neox-small), shift 0.1315 log10 ~ 1.7 margin-widths. Claim map reproduces 4 SUPPORTED / 2 PLAN-ONLY / 6 UNSUPPORTED, totals 12.

  SHIPPED: eval_out.json (schema exp_eval_sol_out PASSED; 8 tabular datasets), results/arm1_real_corrected.jsonl, disagreements.json, draft_edit_list.json, determinism.json, README.md, pinned pyproject.toml verified by rebuilding the venv from scratch.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
out_demo_files:
- path: eval.py
  description: Evaluation script with metrics computation
</artifact_info>

<github_repo>
Repo URL: https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa
Raw data URL: https://raw.githubusercontent.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/main/round-4/evaluation-1/demo/mini_demo_data.json

URLs won't work yet — files pushed to GitHub AFTER notebook creation.
Use local fallback pattern so notebook works locally (now) and in Colab (after deployment).
</github_repo>

<data_file_sizes>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_file_sizes>

<install_dependencies_pattern>
Follow the aii-colab skill exactly. It has the install cell pattern, pre-installed package list, numpy 2.0 compat shims, and all Colab-specific rules.
</install_dependencies_pattern>

<data_loading_pattern>
`mini_demo_data.json` = curated subset for the demo.
Use this pattern for Colab compatibility (GitHub URL with local fallback):
```python
GITHUB_DATA_URL = "https://raw.githubusercontent.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/main/round-4/evaluation-1/demo/mini_demo_data.json"
import json, os

def load_data():
    try:
        import urllib.request
        with urllib.request.urlopen(GITHUB_DATA_URL) as response:
            return json.loads(response.read().decode())
    except Exception: pass
    if os.path.exists("mini_demo_data.json"):
        with open("mini_demo_data.json") as f: return json.load(f)
    raise FileNotFoundError("Could not load mini_demo_data.json")
```
</data_loading_pattern>

<notebook_structure>
--- Setup ---
Cell 1 (markdown): Title, description, what this artifact does.
Cell 2 (code): Install dependencies — follow the aii-colab skill's install cell pattern exactly. Fill in all packages imported by the artifact's code.
Cell 3 (code): Imports — copy original import block as-is, plus any additional imports needed for the notebook (e.g. matplotlib for visualization).
Cell 4 (code): Data loading helper — use the <data_loading_pattern> above.
Cell 5 (code): `data = load_data()`

--- Config ---
Config cell (code): Define ALL tunable parameters (iterations, epochs, n_samples, hidden_size, etc.) as variables at the top of this cell. Start with the ABSOLUTE MINIMUM values — the smallest that produce any output at all (e.g. 1 iteration, 2 samples, smallest array size). These get gradually increased during testing — see TODOs.

--- Processing ---
Remaining cells: One code cell per logical section of the original script. Add a markdown cell BEFORE each code cell. Copy code as closely as possible, with these changes:
  1. Replace file paths to use the loaded `data` variable.
  2. Use the config variables from the config cell (NOT hardcoded values).
  3. Minimal fixes are allowed if something doesn't work in notebook context (e.g. adjusting paths, removing CLI args, fixing imports), but keep changes to the absolute minimum.

--- Results ---
Visualization cell (code): Print key results in a readable table, plot numeric data with matplotlib if appropriate.
</notebook_structure>

<priority>
WORKING > OPTIMIZED. A small-scale demo that runs correctly is the goal. Once the notebook passes with minimum config values, scale up only if time permits — do NOT spend multiple retries chasing larger parameters. If a working version exists, finish and move on.
</priority>

<max_notebook_total_runtime>600s (10 min)</max_notebook_total_runtime>

<test_environment>
To test-run the notebook in a clean environment (simulating Colab), create a disposable `.nb_env` in your workspace:
```bash
/usr/local/bin/python3.12 -m venv .nb_env
.nb_env/bin/pip install -q pip jupyter ipykernel
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
rm -rf .nb_env
```
The timeout is set to <max_notebook_total_runtime>. The entire notebook must finish within this time.

What happens: the .venv starts empty (just jupyter). When the notebook's install cell runs, `google.colab` is NOT in sys.modules, so ALL packages get installed — non-Colab packages unconditionally, and Colab packages (numpy, pandas, etc.) at Colab's exact versions via the guard block. The result mirrors Colab's environment as closely as possible. If a cell fails, fix the notebook and re-run.
</test_environment>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.


<todos>
TODO 1. Read and STRICTLY follow these skills: aii-colab, aii-long-running-tasks.
TODO 2. Read demo file and relevant preview_* files (preview only). Understand script structure: imports, setup, processing, output. Identify ALL tunable parameters (iterations, epochs, n_samples, hidden_size, batch_size, etc.) — these go in the config cell.
TODO 3. Create `mini_demo_data.json`: curated subset from at most ONE dataset (no more than 100 diverse examples). CRITICAL: do NOT read/grep full output file — may crash. Use `head -c 5000` or stream first entries with Python to pick examples.
TODO 4. Create `code_demo.ipynb` via NotebookEdit following <notebook_structure>. Set ALL config parameters to ABSOLUTE MINIMUM values — the smallest that produce any output (e.g. 1 iteration, 2 samples, smallest array sizes). Test-run using <test_environment>. Fix all errors until it passes.
TODO 5. GRADUALLY SCALE (but don't overdo it): increase config params step by step (e.g. ~2x each round). After each increase: test-run, record runtime, fix errors. STOP SCALING as soon as results look meaningful — a working small-scale demo beats a failed large-scale one. If full original params fit within <max_notebook_total_runtime> (10% margin), use them. Otherwise keep whatever works and comment out the true original values. Do NOT spend more than 2-3 scaling rounds.
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/main/round-4/evaluation-1/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "DemoExpectedFiles": {
      "description": "Expected output files from code demo notebook generation.",
      "properties": {
        "notebook": {
          "default": "",
          "description": "Path to the generated demo notebook. Example: 'code_demo.ipynb'",
          "title": "Notebook",
          "type": "string"
        },
        "mini_data_file": {
          "default": "",
          "description": "Path to the mini demo data JSON (curated subset). Example: 'mini_demo_data.json'",
          "title": "Mini Data File",
          "type": "string"
        }
      },
      "title": "DemoExpectedFiles",
      "type": "object"
    }
  },
  "description": "Dataset/experiment/evaluation \u2192 Jupyter notebook demo.\n\nTitle and summary come from the parent artifact (gen_art step),\nnot from the demo agent. The agent only outputs expected files.",
  "properties": {
    "out_expected_files": {
      "$ref": "#/$defs/DemoExpectedFiles",
      "description": "All output files you created. Must include the demo notebook."
    }
  },
  "required": [],
  "title": "CodeDemo",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-14 07:38:18 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [4] ASSISTANT · 2026-08-14 07:38:28 UTC

```
I'll start by loading the required skills and inspecting the artifact.
```

### [5] TOOL CALL — Skill · 2026-08-14 07:38:28 UTC

```
aii-colab
```

### [6] TOOL RESULT — Skill · 2026-08-14 07:38:28 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [7] TOOL CALL — Bash · 2026-08-14 07:38:28 UTC

```
List artifact workspace:
ls -la /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_evaluation_1/
```

### [8] TOOL RESULT — Bash · 2026-08-14 07:38:28 UTC

```
{"stdout": "total 15001\ndrwxr-xr-x 6 root root 2018058 Aug 14 01:05 .\ndrwxr-xr-x 7 root root 3001407 Aug 13 23:55 ..\n-rw-r--r-- 1 root root 2920151 Aug 14 01:05 .repl_agent.ptylog\n-rw-r--r-- 1 root root    5536 Aug 14 01:05 .terminal_claude_agent_struct_out.json\ndrwxr-xr-x 4 root root 2017521 Aug 14 01:02 .venv\n-rw-r--r-- 1 root root    1851 Aug 14 01:03 README.md\ndrwxr-xr-x 2 root root 1015361 Aug 14 00:59 __pycache__\n-rw-r--r-- 1 root root    3838 Aug 14 00:32 determinism.py\n-rw-r--r-- 1 root root   25952 Aug 14 01:00 eval.py\n-rw-r--r-- 1 root root  664760 Aug 14 01:03 eval_out.json\n-rw-r--r-- 1 root root  781812 Aug 14 01:03 full_eval_out.json\n-rw-r--r-- 1 root root   15158 Aug 14 00:36 lib_arch.py\ndrwxr-xr-x 2 root root 1016657 Aug 14 00:32 logs\n-rw-r--r-- 1 root root  592893 Aug 14 01:03 mini_eval_out.json\n-rw-r--r-- 1 root root  120223 Aug 14 01:03 preview_eval_out.json\n-rw-r--r-- 1 root root     313 Aug 14 01:02 pyproject.toml\ndrwxr-xr-x 2 root root 1001324 Aug 14 00:32 results\n-rw-r--r-- 1 root root   31856 Aug 14 01:02 uv.lock\n-rw-r--r-- 1 root root   29537 Aug 14 00:59 ws_assert.py\n-rw-r--r-- 1 root root   21973 Aug 14 00:33 ws_w1.py\n-rw-r--r-- 1 root root   14904 Aug 14 00:36 ws_w2.py\n-rw-r--r-- 1 root root   13526 Aug 14 00:28 ws_w3.py\n-rw-r--r-- 1 root root   21482 Aug 14 00:59 ws_w4.py\n-rw-r--r-- 1 root root   19654 Aug 14 00:36 ws_w5.py", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Skill · 2026-08-14 07:38:36 UTC

```
aii-long-running-tasks
```

### [10] TOOL RESULT — Skill · 2026-08-14 07:38:36 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [11] TOOL CALL — Bash · 2026-08-14 07:38:36 UTC

```
cd /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_evaluation_1 && head -c 4000 preview_eval_out.json && echo "---KEYS---" && python3 -c "
import json
d=json.load(open('preview_eval_out.json'))
def w(o,p='',d_=0):
    if d_>2: return
    if isinstance(o,dict):
        for k,v in o.items(): print(p+k, type(v).__name__, (len(v) if isinstance(v,(list,dict)) else str(v)[:60])); w(v,p+'  ',d_+1)
    elif isinstance(o,list) and o: w(o[0],p+'[0].',d_+1)
w(d)
" 2>&1 | head -120
```

### [12] TOOL RESULT — Bash · 2026-08-14 07:38:38 UTC

```
{"stdout": "{\n  \"datasets\": [\n    {\n      \"dataset\": \"assertions\",\n      \"examples\": [\n        {\n          \"eval_abs_diff\": 0.0,\n          \"eval_is_match\": 1.0,\n          \"eval_tolerance\": 0.0001,\n          \"input\": \"W1.W05.mlabonne/Qwen3-0.6B-abliterated\",\n          \"metadata_provenance\": \"A1/results/arm1_real.jsonl:W05\",\n          \"metadata_tolerance_class\": \"float_rederive\",\n          \"output\": \"MATCH\",\n          \"predict_draft_quoted_value\": \"-0.964\",\n          \"predict_recomputed_value\": \"-0.964\"\n        },\n        {\n          \"eval_abs_diff\": 0.0,\n          \"eval_is_match\": 1.0,\n          \"eval_tolerance\": 0.0,\n          \"input\": \"W1.repo_id.mlabonne/Qwen3-0.6B-abliterated\",\n          \"metadata_provenance\": \"A1/results/arm1_real.jsonl:variant_id\",\n          \"metadata_tolerance_class\": \"exact_string\",\n          \"output\": \"MATCH\",\n          \"predict_draft_quoted_value\": \"\\\"mlabonne/Qwen3-0.6B-abliterated\\\"\",\n          \"predict_recomputed_value\": \"\\\"mlabonne/Qwen3-0.6B-abliterated\\\"\"\n        },\n        {\n          \"eval_abs_diff\": 0.0,\n          \"eval_is_match\": 1.0,\n          \"eval_tolerance\": 0.0001,\n          \"input\": \"W1.W05.MagicalAlchemist/Qwen3-1.7B-Magic_decensored\",\n          \"metadata_provenance\": \"A1/results/arm1_real.jsonl:W05\",\n          \"metadata_tolerance_class\": \"float_rederive\",\n          \"output\": \"MATCH\",\n          \"predict_draft_quoted_value\": \"-1.01\",\n          \"predict_recomputed_value\": \"-1.01\"\n        }\n      ]\n    },\n    {\n      \"dataset\": \"recipe_relabel\",\n      \"examples\": [\n        {\n          \"eval_W01\": 0.6235601911201958,\n          \"eval_W05\": -0.963652524643444,\n          \"eval_caught_at_fitted_threshold\": 0.0,\n          \"input\": \"mlabonne/Qwen3-0.6B-abliterated\",\n          \"metadata_decision_rule_id\": \"R-2026-08-14-verbatim-kernel-string-v1\",\n          \"metadata_evidence_char_offsets\": null,\n          \"metadata_evidence_span_verbatim\": \"\",\n          \"metadata_evidence_status\": \"NOT_IN_ARCHIVE\",\n          \"metadata_mechanically_different_new\": \"UNDETERMINED\",\n          \"metadata_mechanically_different_old\": false,\n          \"metadata_relabel_status\": \"PROVISIONAL\",\n          \"metadata_uploader\": \"mlabonne\",\n          \"output\": \"global_diff_in_means\",\n          \"predict_kernel_family\": \"unknown\",\n          \"predict_recipe_class_old\": \"global_diff_in_means\"\n        },\n        {\n          \"eval_W01\": 0.747820588659054,\n          \"eval_W05\": -2.1605665885899787,\n          \"eval_caught_at_fitted_threshold\": 0.0,\n          \"input\": \"BennyDaBall/Qwen3-4b-Z-Image-Turbo-AbliteratedV1\",\n          \"metadata_decision_rule_id\": \"R-2026-08-14-verbatim-kernel-string-v1\",\n          \"metadata_evidence_char_offsets\": null,\n          \"metadata_evidence_span_verbatim\": \"\",\n          \"metadata_evidence_status\": \"NOT_IN_ARCHIVE\",\n          \"metadata_mechanically_different_new\": \"UNDETERMINED\",\n          \"metadata_mechanically_different_old\": false,\n          \"metadata_relabel_status\": \"PROVISIONAL\",\n          \"metadata_uploader\": \"BennyDaBall\",\n          \"output\": \"global_diff_in_means\",\n          \"predict_kernel_family\": \"unknown\",\n          \"predict_recipe_class_old\": \"global_diff_in_means\"\n        },\n        {\n          \"eval_W01\": 0.4969141058704426,\n          \"eval_W05\": -0.9904157743710144,\n          \"eval_caught_at_fitted_threshold\": 0.0,\n          \"input\": \"prithivMLmods/VibeThinker-3B-heretic_decensored\",\n          \"metadata_decision_rule_id\": \"R-2026-08-14-verbatim-kernel-string-v1\",\n          \"metadata_evidence_char_offsets\": [\n            42,\n            300\n          ],\n          \"metadata_evidence_span_verbatim\": \"x; color: #cbd5e1; font-weight: 500;\\\">Reasoning-focused language model modified using the Heretic abliteration toolkit</p>\\n  </div>\\n  <div style=\\\"display: flex; gap: 8px; flex-wrap: wrap; padding: 12p...\",\n          \"metadata_evidence_status\": \"IN_ARCHIVE\",\n          \"metadata_mechanically_different_new\": \"TRUE\",\n          \"metadata_mechanically_different_old\": false,\n          \"metadata_relabel_st---KEYS---\ndatasets list 3\n  [0].dataset str assertions\n  [0].examples list 3\nmetadata dict 13\n  archives dict 6\n    A1 str /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop\n    A2 str /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop\n    A3 str /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop\n    A4 str /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop\n    A5 str /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop\n    A6 str /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop\n  assertion_tolerances dict 4\n    float_rederivation float 0.0001\n    rate_from_reconstructed_counts float 0.005\n    repo_ids_and_evidence_spans str exact string match\n    verbatim_copy float 1e-06\n  assertion_verdict_counts dict 3\n    MATCH int 105\n    MISMATCH int 5\n    UNAVAILABLE int 0\n  blocks dict 9\n    archive_headers dict 6\n    assertions list 3\n    cost_table dict 12\n    e1_bands dict 14\n    fidelity dict 8\n    ladder_intervals dict 16\n    manifest list 3\n    provenance dict 8\n    recipe_relabel dict 12\n  bootstrap_B int 10000\n  cross_check_gates dict 2\n    verify_py dict 7\n    wstats_gate dict 14\n  description str Pure re-analysis over the archived iteration-2 and iteration\n  evaluation_name str Recheck every number in the draft\n  resolved_paths dict 11\n    A1:full_method_out.json str full_method_out.json\n    A1:results/arm1_real*.jsonl str results/arm1_real.jsonl\n    A1:results/arm2_all*.jsonl str results/arm2_all.jsonl\n    A1:results/gate.json str results/gate.json\n    A2:full_method_out.json str full_method_out.json\n    A2:results/ladder*.jsonl str results/ladder.jsonl\n    A2:results/root.json str results/root.json\n    A2:results/scan*.jsonl str results/scan.jsonl\n    A2:results/scan_enumeration.json str results/scan_enumeration.json\n    A3:full_method_out.json str full_method_out.json\n    A5:numbers.json str numbers.json\n  scope_constraints dict 7\n    forward_passes int 0\n    generations int 0\n    hand_reconstructed_numbers int 0\n    hub_fetches int 0\n    llm_calls int 0\n    model_weights_loaded bool False\n    openrouter_spend_usd float 0.0\n  seed int 20260814\n  unresolved_globs list 0\n  wall_clock_s float 21.37\nmetrics_agg dict 37\n  assertion_match_rate float 0.9545454545454546\n  e1_bands_not_recomputable float 6.0\n  e1_bands_recomputable float 3.0\n  eligibility_n_eligible float 85.0\n  eligibility_n_excluded float 75.0\n  eligibility_n_raw float 160.0\n  fp_rate_eligible float 0.0\n  fp_rate_raw float 0.0\n  ladder_mdd_upward_at_p020_n40 float 0.2939\n  n_assertions float 110.0\n  n_assertions_match float 105.0\n  n_assertions_mismatch float 5.0\n  n_assertions_unavailable float 0.0\n  n_carry_forward_values float 28.0\n  n_cost_table_rows float 54.0\n  n_forward_passes float 0.0\n  n_generations float 0.0\n  n_hub_fetches float 0.0\n  n_ladder_interval_rows float 136.0\n  n_misses_with_verbatim_non_uniform_kernel float 2.0\n  n_prereg_claims float 12.0\n  n_recipe_rows_provisional float 2.0\n  n_recipe_rows_relabelled float 2.0\n  n_subset_corrected_values float 5.0\n  n_unresolvable_evasion_costs float 4.0\n  n_wilson_vs_bootstrap_disagreements float 120.0\n  new_uploader_auroc_recomputed float 0.3819444444444444\n  openrouter_spend_usd float 0.0\n  paired_diff_W05_minus_E1_15pairs float -0.16666666666666663\n  scan_completed float 160.0\n  scan_total_rows float 270.0\n  scan_unresolved_recomputed float 81.0\n  smallest_shift_to_first_false_positive float 0.13151178042881284\n  verify_py_checks_passed float 17.0\n  verify_py_checks_total float 17.0\n  wilson95_upper_eligible float 0.04323948381405149\n  wstats_max_abs_delta_W05 float 9.91e-06", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [13] TOOL CALL — Bash · 2026-08-14 07:38:44 UTC

```
cd /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_evaluation_1 && sed -n 1,80p eval.py && echo "=====GREP DEF====" && grep -n "^def \|^class \|^TOL\|^[A-Z_]* = " eval.py ws_assert.py | head -80
```

### [14] TOOL RESULT — Bash · 2026-08-14 07:38:46 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Recheck every number in the draft.\n\nPURE RE-ANALYSIS over the archived iteration-2 and iteration-3 trees.\nNo model weights, no forward passes, no generations, no LLM calls ($0.00), no Hub fetches.\n\nOutputs\n-------\neval_out.json                     blocks: recipe_relabel, ladder_intervals, e1_bands,\n                                  cost_table, fidelity, assertions, provenance, manifest\nresults/arm1_real_corrected.jsonl corrected arm-1 rows, OLD and NEW labels side by side\nresults/disagreements.json        every MISMATCH / UNAVAILABLE assertion row\nresults/draft_edit_list.json      the numbered draft edit list\nREADME.md                         spend, seed, determinism result, MATCH/MISMATCH/UNAVAILABLE counts\n\"\"\"\n\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport sys\nimport time\nfrom pathlib import Path\nfrom typing import Any\n\nfrom loguru import logger\n\nHERE = Path(__file__).resolve().parent\nsys.path.insert(0, str(HERE))\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(str(HERE / \"logs/run.log\"), rotation=\"30 MB\", level=\"DEBUG\")\n\nfrom lib_arch import ARCHIVES, BOOT_B, SEED, Resolver, build_manifest  # noqa: E402\nfrom ws_assert import build_assertions, cross_check_gates  # noqa: E402\nfrom ws_w1 import run_w1  # noqa: E402\nfrom ws_w2 import run_w2  # noqa: E402\nfrom ws_w3 import run_w3  # noqa: E402\nfrom ws_w4 import run_w4  # noqa: E402\nfrom ws_w5 import run_w5  # noqa: E402\n\n\ndef _headers(res: Resolver) -> dict[str, Any]:\n    \"\"\"Print (and record) the top-level key set of every *_out.json and header keys of .jsonl.\"\"\"\n    out: dict[str, Any] = {}\n    from lib_arch import walk_archive\n\n    for tag, root in ARCHIVES.items():\n        entry: dict[str, Any] = {}\n        files = walk_archive(root)\n        for p in [f for f in files if f.name.endswith(\"_out.json\") and f.parent == root]:\n            try:\n                d = json.loads(p.read_text())\n            except (json.JSONDecodeError, OSError):\n                continue\n            entry[p.name] = sorted(d.keys()) if isinstance(d, dict) else f\"list[{len(d)}]\"\n            if isinstance(d, dict) and \"datasets\" in d:\n                entry[p.name + \"::datasets\"] = {\n                    ds[\"dataset\"]: len(ds[\"examples\"]) for ds in d[\"datasets\"]\n                }\n            break  # one representative assembled artifact per tree is enough\n        for p in [f for f in files if f.suffix == \".jsonl\"]:\n            try:\n                first = next((ln for ln in p.read_text().splitlines() if ln.strip()), None)\n            except OSError:\n                continue\n            if first is None:\n                continue\n            try:\n                entry[str(p.relative_to(root))] = sorted(json.loads(first).keys())\n            except json.JSONDecodeError:\n                continue\n        out[tag] = entry\n        for k, v in entry.items():\n            logger.info(f\"[{tag}] {k}: {v if not isinstance(v, list) else v[:12]}\")\n    return out\n\n\ndef _flatten_metrics(blocks: dict[str, Any], assertions: list[dict], gates: dict) -> dict[str, float]:\n=====GREP DEF====\neval.py:28:HERE = Path(__file__).resolve().parent\neval.py:44:def _headers(res: Resolver) -> dict[str, Any]:\neval.py:80:def _flatten_metrics(blocks: dict[str, Any], assertions: list[dict], gates: dict) -> dict[str, float]:\neval.py:143:def _datasets(blocks: dict[str, Any], assertions: list[dict]) -> list[dict[str, Any]]:\neval.py:313:def main() -> None:\nws_assert.py:20:TOL = {\nws_assert.py:29:def _get(obj: Any, path: str) -> Any:\nws_assert.py:46:def _row(claim_id: str, quoted: Any, recomputed: Any, tol_key: str, provenance: str) -> dict[str, Any]:\nws_assert.py:64:def build_assertions(blocks: dict[str, Any], numbers: dict[str, Any],\nws_assert.py:382:def cross_check_gates(res: Resolver) -> dict[str, Any]:", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] TOOL CALL — Bash · 2026-08-14 07:38:54 UTC

```
cd /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_evaluation_1 && sed -n 15,64p ws_assert.py && echo "=====W2 WILSON====" && grep -n "def \|wilson\|bootstrap" ws_w2.py | head -40
```

### [16] TOOL RESULT — Bash · 2026-08-14 07:38:54 UTC

```
{"stdout": "from loguru import logger\n\nfrom lib_arch import ARCHIVES, Resolver\n\n# Tolerances declared up front.\nTOL = {\n    \"verbatim\": 1e-6,       # values copied verbatim from an archive\n    \"float_rederive\": 1e-4,  # float re-derivations\n    \"rate_reconstructed\": 0.005,  # rates re-derived from reconstructed counts\n    \"exact_string\": 0.0,     # repo_ids and evidence spans\n    \"quoted_rounding\": 5.001e-4,  # a draft value quoted at 3 dp against its full-precision source\n}\n\n\ndef _get(obj: Any, path: str) -> Any:\n    cur = obj\n    for part in path.split(\".\"):\n        if cur is None:\n            return None\n        if isinstance(cur, list):\n            try:\n                cur = cur[int(part)]\n                continue\n            except (ValueError, IndexError):\n                return None\n        if not isinstance(cur, dict) or part not in cur:\n            return None\n        cur = cur[part]\n    return cur\n\n\ndef _row(claim_id: str, quoted: Any, recomputed: Any, tol_key: str, provenance: str) -> dict[str, Any]:\n    tol = TOL[tol_key]\n    if recomputed is None:\n        return {\"claim_id\": claim_id, \"draft_quoted_value\": quoted, \"recomputed_value\": None,\n                \"abs_diff\": None, \"tolerance\": tol, \"tolerance_class\": tol_key,\n                \"verdict\": \"UNAVAILABLE\", \"provenance\": provenance}\n    if not isinstance(quoted, (int, float)) or not isinstance(recomputed, (int, float)) \\\n            or isinstance(quoted, bool) or isinstance(recomputed, bool):\n        ok = quoted == recomputed\n        return {\"claim_id\": claim_id, \"draft_quoted_value\": quoted, \"recomputed_value\": recomputed,\n                \"abs_diff\": 0.0 if ok else None, \"tolerance\": tol, \"tolerance_class\": tol_key,\n                \"verdict\": \"MATCH\" if ok else \"MISMATCH\", \"provenance\": provenance}\n    d = abs(float(quoted) - float(recomputed))\n    return {\"claim_id\": claim_id, \"draft_quoted_value\": quoted, \"recomputed_value\": recomputed,\n            \"abs_diff\": d, \"tolerance\": tol, \"tolerance_class\": tol_key,\n            \"verdict\": \"MATCH\" if d <= tol else \"MISMATCH\", \"provenance\": provenance}\n\n\ndef build_assertions(blocks: dict[str, Any], numbers: dict[str, Any],\n=====W2 WILSON====\n2:\"\"\"W2 - Wilson + bootstrap intervals on the 34-stage laundering ladder (block: ladder_intervals).\"\"\"\n20:    wilson95,\n32:def _one_sig(x: float) -> str:\n44:def run_w2(res: Resolver) -> dict[str, Any]:\n57:    disagreements_wilson_vs_boot: list[dict[str, Any]] = []\n73:            wlo, whi = wilson95(k, n_ach)\n77:                disagreements_wilson_vs_boot.append(\n79:                     \"wilson\": [wlo, whi], \"bootstrap\": [blo, bhi],\n97:                    \"wilson95_lo\": wlo,\n98:                    \"wilson95_hi\": whi,\n99:                    \"bootstrap95_lo\": blo,\n100:                    \"bootstrap95_hi\": bhi,\n115:    rwlo, rwhi = wilson95(rk, rn)\n122:        \"wilson95\": [rwlo, rwhi],\n123:        \"bootstrap95\": [rblo, rbhi],\n168:            lo, hi = wilson95(k, n)\n180:                    \"wilson95_at_flag_death\": [lo, hi],\n181:                    \"bootstrap95_at_flag_death\": [blo, bhi],\n183:                    \"root_wilson95\": [rwlo, rwhi],\n186:                    \"signed_evasion_cost_bootstrap95\": [dlo, dhi],\n212:        dlo, dhi = r[\"signed_evasion_cost_bootstrap95\"]\n254:            \"bootstrap95\": [dlo, dhi],\n324:        \"bootstrap_B\": BOOT_B,\n326:        \"bootstrap is reported beside it and any endpoint disagreement > 0.02 is listed.\",\n331:        \"wilson_vs_bootstrap_disagreements\": disagreements_wilson_vs_boot,\n332:        \"n_wilson_vs_bootstrap_disagreements\": len(disagreements_wilson_vs_boot),", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [17] TOOL CALL — Bash · 2026-08-14 07:38:54 UTC

```
cd /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_evaluation_1 && python3 -c "
import json
d=json.load(open('full_eval_out.json'))
for ds in d['datasets']: print(ds['dataset'], len(ds['examples']), sorted(ds['examples'][0].keys()))
"
```

### [18] TOOL RESULT — Bash · 2026-08-14 07:38:54 UTC

```
{"stdout": "assertions 110 ['eval_abs_diff', 'eval_is_match', 'eval_tolerance', 'input', 'metadata_provenance', 'metadata_tolerance_class', 'output', 'predict_draft_quoted_value', 'predict_recomputed_value']\nrecipe_relabel 4 ['eval_W01', 'eval_W05', 'eval_caught_at_fitted_threshold', 'input', 'metadata_decision_rule_id', 'metadata_evidence_char_offsets', 'metadata_evidence_span_verbatim', 'metadata_evidence_status', 'metadata_mechanically_different_new', 'metadata_mechanically_different_old', 'metadata_relabel_status', 'metadata_uploader', 'output', 'predict_kernel_family', 'predict_recipe_class_old']\nladder_intervals 136 ['eval_k_refused', 'eval_n_achieved', 'eval_n_nominal', 'eval_rate', 'eval_reconstruction_residual', 'eval_se_binomial', 'input', 'metadata_axis', 'metadata_denominator_source', 'metadata_intensity', 'output', 'predict_bootstrap95', 'predict_wilson95']\ne1_bands 9 ['eval_auroc_E1', 'eval_auroc_W05', 'eval_n_pairs', 'input', 'metadata_band_label', 'metadata_ci', 'metadata_reason', 'output', 'predict_paired_diff_W05_minus_E1']\ncost_table 54 ['eval_forward_passes_required', 'eval_harmful_prompts_required', 'eval_prompts_required', 'eval_rho_lineage', 'eval_wall_clock_median_s', 'input', 'metadata_carried_forward', 'metadata_ci_lineage', 'metadata_ci_member', 'metadata_paired_diff_ci', 'metadata_paired_diff_vs_best_blackbox', 'metadata_parent_model_required', 'output', 'predict_rho_member']\nclaim_map 12 ['eval_is_supported', 'input', 'metadata_artifact_file', 'metadata_line_or_key', 'output', 'predict_corrected_wording']\nthreshold_brittleness 7 ['eval_hits_eligible', 'eval_hits_raw_160', 'eval_threshold', 'input', 'output', 'predict_hits_eligible']\nweights_table_minmax 25 ['eval_max', 'eval_median', 'eval_min', 'eval_n', 'input', 'metadata_provenance', 'output', 'predict_range_as_the_paper_must_report_it']", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Bash · 2026-08-14 07:39:04 UTC

```
cd /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_evaluation_1 && grep -n "def wilson95" -A 20 lib_arch.py && grep -n "def bootstrap" -A 15 lib_arch.py
```

### [20] TOOL RESULT — Bash · 2026-08-14 07:39:04 UTC

```
{"stdout": "206:def wilson95(k: int, n: int) -> tuple[float, float]:\n207-    \"\"\"Wilson score interval (primary for small n and rates near 0).\"\"\"\n208-    if n <= 0:\n209-        return (float(\"nan\"), float(\"nan\"))\n210-    z = 1.959963984540054\n211-    p = k / n\n212-    d = 1.0 + z * z / n\n213-    c = p + z * z / (2 * n)\n214-    hw = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))\n215-    return ((c - hw) / d, (c + hw) / d)\n216-\n217-\n218-def boot_rate_ci(k: int, n: int, rng: np.random.Generator, b: int = BOOT_B) -> tuple[float, float]:\n219-    \"\"\"Item-level nonparametric bootstrap of a binomial rate.\"\"\"\n220-    if n <= 0:\n221-        return (float(\"nan\"), float(\"nan\"))\n222-    items = np.zeros(n)\n223-    items[:k] = 1.0\n224-    draws = rng.integers(0, n, size=(b, n))\n225-    reps = items[draws].mean(axis=1)\n226-    return (float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5)))", "stderr": "", "interrupted": false, "isImage": false, "returnCodeInterpretation": "No matches found", "noOutputExpected": false}
```

### [21] ASSISTANT · 2026-08-14 07:39:16 UTC

```
Now building the mini demo data.
```

### [22] TOOL CALL — Bash · 2026-08-14 07:39:16 UTC

```
python3 - <<'EOF'
import json
src="/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_evaluation_1/full_eval_out.json"
d=json.load(open(src))
ds=[x for x in d["datasets"] if x["dataset"]=="assertions"][0]["examples"]
mm=[e for e in ds if e["output"]!="MATCH"]
mt=[e for e in ds if e["output"]=="MATCH"]
# diverse: stratify MATCH by tolerance class
by={}
for e in mt: by.setdefault(e["metadata_tolerance_class"],[]).append(e)
sel=list(mm)
quota=100-len(sel)
order=sorted(by, key=lambda k:-len(by[k]))
i=0
while len(sel)<100:
    added=False
    for k in order:
        if len(sel)>=100: break
        if i<len(by[k]): sel.append(by[k][i]); added=True
    if not added: break
    i+=1
sel=sel[:100]
sel.sort(key=lambda e: e["input"])
md=d["metadata"]
mini={
 "dataset":"assertions",
 "examples":sel,
 "metadata":{
   "evaluation_name":md["evaluation_name"],
   "description":md["description"],
   "seed":md["seed"],
   "assertion_tolerances":md["assertion_tolerances"],
   "assertion_verdict_counts_full":md["assertion_verdict_counts"],
   "cross_check_gates":md["cross_check_gates"],
   "scope_constraints":md["scope_constraints"],
   "n_assertions_full":int(d["metrics_agg"]["n_assertions"]),
   "assertion_match_rate_full":d["metrics_agg"]["assertion_match_rate"],
 },
}
json.dump(mini,open("mini_demo_data.json","w"),indent=1)
print(len(sel), sum(1 for e in sel if e["output"]!="MATCH"), {k:sum(1 for e in sel if e["metadata_tolerance_class"]==k) for k in set(e["metadata_tolerance_class"] for e in sel)})
import os; print(os.path.getsize("mini_demo_data.json"))
EOF
```

### [23] TOOL RESULT — Bash · 2026-08-14 07:39:16 UTC

```
{"stdout": "100 5 {'quoted_rounding': 2, 'rate_reconstructed': 7, 'exact_string': 10, 'float_rederive': 34, 'verbatim': 47}\n43042", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] TOOL CALL — Bash · 2026-08-14 07:39:22 UTC

```
ls -la /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins/
```

### [25] TOOL RESULT — Bash · 2026-08-14 07:39:22 UTC

```
{"stdout": "total 3176\ndrwxr-xr-x 2 root root 1014875 Aug 14 07:39 .\ndrwxr-xr-x 6 root root 2083452 Aug 14 07:37 ..\n-rw-r--r-- 1 root root  109279 Aug 14 07:39 .repl_agent.ptylog\n-rw-r--r-- 1 root root   43042 Aug 14 07:39 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] TOOL CALL — ToolSearch · 2026-08-14 07:39:22 UTC

```
{'query': 'select:NotebookEdit', 'max_results': 1}
```

### [27] TOOL RESULT — ToolSearch · 2026-08-14 07:39:22 UTC

```
{"matches": ["NotebookEdit"], "query": "select:NotebookEdit", "total_deferred_tools": 22}
```

### [28] TOOL CALL — Bash · 2026-08-14 07:40:30 UTC

```
cat > /tmp/claude-0/-ai-inventor-aii-data-runs-run-UtpduT-D2IS2-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-4-art-ckuwEkspyins/dbd2ef6a-2da1-4fdc-98a4-a2d87c8eb624/scratchpad/mk.py <<'PYEOF'
import json

C = []
def md(s): C.append({"cell_type":"markdown","metadata":{},"source":s})
def co(s): C.append({"cell_type":"code","metadata":{},"execution_count":None,"outputs":[],"source":s})

md("""# Rechecking every number in the draft — demo

This artifact is a **pure re-analysis**: `$0.00` of LLM spend, **0** model weights loaded,
**0** forward passes, **0** generations, **0** Hub fetches. The original `eval.py` reads six
archived experiment trees and re-derives every number the paper draft quotes, emitting an
**assertion table** where each row carries `(draft_quoted_value, recomputed_value, tolerance,
verdict, provenance)`.

Full run: **110 claim_ids -> 105 MATCH / 5 MISMATCH / 0 UNAVAILABLE** (~21 s on 4 CPUs).

This notebook replays the *comparison core* of that evaluation on a curated 100-row subset of the
shipped assertion table (all 5 MISMATCH rows plus 95 MATCH rows stratified across the five
tolerance classes). The verdict logic (`TOL`, `_row`) and the interval helpers (`wilson95`,
`boot_rate_ci`) are copied verbatim from `ws_assert.py` / `lib_arch.py`; we re-run them on the
archived `(quoted, recomputed)` pairs and check that every verdict reproduces.""")

co("""import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# Core packages (pre-installed on Colab, install locally to match Colab env)
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'matplotlib==3.10.0')""")

co("""# Imports as in the original scripts (eval.py / ws_assert.py / lib_arch.py), plus matplotlib
from __future__ import annotations

import json
import math
import os
from typing import Any

import numpy as np
import matplotlib.pyplot as plt""")

co('''GITHUB_DATA_URL = "https://raw.githubusercontent.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/main/round-4/evaluation-1/demo/mini_demo_data.json"

def load_data():
    try:
        import urllib.request
        with urllib.request.urlopen(GITHUB_DATA_URL) as response:
            return json.loads(response.read().decode())
    except Exception: pass
    if os.path.exists("mini_demo_data.json"):
        with open("mini_demo_data.json") as f: return json.load(f)
    raise FileNotFoundError("Could not load mini_demo_data.json")''')

co("""data = load_data()
print(data["metadata"]["evaluation_name"])
print("subset rows:", len(data["examples"]), "| full-run rows:", data["metadata"]["n_assertions_full"])
print("full-run verdicts:", data["metadata"]["assertion_verdict_counts_full"])
print("declared tolerances:", json.dumps(data["metadata"]["assertion_tolerances"], indent=2))""")

md("""## Config

All tunable parameters. `N_ASSERTIONS` is how many rows of the archived assertion table we replay,
`BOOT_B` is the bootstrap replicate count (original: 10,000), `SEED` is the original run's seed.""")

co("""# --- tunable parameters (original values in comments) ---
N_ASSERTIONS = 100      # rows of the assertion table to replay (full run: 110)
BOOT_B       = 10000    # bootstrap replicates for the rate CI (original: 10000)
SEED         = data["metadata"]["seed"]   # 20260814, the original run's seed

rows_in = data["examples"][:N_ASSERTIONS]
print(f"replaying {len(rows_in)} assertion rows | BOOT_B={BOOT_B} | SEED={SEED}")""")

md("""## 1. The verdict logic, verbatim

`TOL` and `_row` are copied unchanged from `ws_assert.py`. Every claim is compared under a
tolerance declared **up front** by its class: `1e-6` for values copied verbatim out of an archive,
`1e-4` for float re-derivations, `0.005` for rates rebuilt from reconstructed counts, exact string
equality for repo_ids and evidence spans, and `5.001e-4` for a draft value quoted at 3 dp against
its full-precision source.""")

co('''# Tolerances declared up front.
TOL = {
    "verbatim": 1e-6,       # values copied verbatim from an archive
    "float_rederive": 1e-4,  # float re-derivations
    "rate_reconstructed": 0.005,  # rates re-derived from reconstructed counts
    "exact_string": 0.0,     # repo_ids and evidence spans
    "quoted_rounding": 5.001e-4,  # a draft value quoted at 3 dp against its full-precision source
}


def _row(claim_id: str, quoted: Any, recomputed: Any, tol_key: str, provenance: str) -> dict[str, Any]:
    tol = TOL[tol_key]
    if recomputed is None:
        return {"claim_id": claim_id, "draft_quoted_value": quoted, "recomputed_value": None,
                "abs_diff": None, "tolerance": tol, "tolerance_class": tol_key,
                "verdict": "UNAVAILABLE", "provenance": provenance}
    if not isinstance(quoted, (int, float)) or not isinstance(recomputed, (int, float)) \\
            or isinstance(quoted, bool) or isinstance(recomputed, bool):
        ok = quoted == recomputed
        return {"claim_id": claim_id, "draft_quoted_value": quoted, "recomputed_value": recomputed,
                "abs_diff": 0.0 if ok else None, "tolerance": tol, "tolerance_class": tol_key,
                "verdict": "MATCH" if ok else "MISMATCH", "provenance": provenance}
    d = abs(float(quoted) - float(recomputed))
    return {"claim_id": claim_id, "draft_quoted_value": quoted, "recomputed_value": recomputed,
            "abs_diff": d, "tolerance": tol, "tolerance_class": tol_key,
            "verdict": "MATCH" if d <= tol else "MISMATCH", "provenance": provenance}''')

md("""## 2. Replay the assertion table

The archived rows store the quoted / recomputed pair as strings (that is how they are shipped in
`eval_out.json`). We coerce back to float where the pair is numeric — a value that cannot be parsed
as a float stays a string and falls through `_row`'s exact-equality branch, which is exactly what
the original does for `repo_id` and evidence-span claims. A `None` recomputed value yields
`UNAVAILABLE`.

Each replayed verdict is then checked against the verdict the original run emitted.""")

co('''def _maybe_float(x):
    """Archived rows ship values as strings; restore numerics, leave genuine strings alone."""
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return x
    try:
        return float(x)
    except (TypeError, ValueError):
        return x


replayed = []
for ex in rows_in:
    q = _maybe_float(ex["predict_draft_quoted_value"])
    r = _maybe_float(ex["predict_recomputed_value"])
    replayed.append(_row(ex["input"], q, r, ex["metadata_tolerance_class"], ex["metadata_provenance"]))

counts = {"MATCH": 0, "MISMATCH": 0, "UNAVAILABLE": 0}
for row in replayed:
    counts[row["verdict"]] += 1

agree = sum(1 for row, ex in zip(replayed, rows_in) if row["verdict"] == ex["output"])
print("replayed verdict counts:", counts)
print(f"verdicts reproducing the archived run: {agree}/{len(replayed)}")
print("match rate on this subset:", round(counts["MATCH"] / len(replayed), 6))''')

md("""## 3. Wilson + bootstrap interval on the match rate

`wilson95` and `boot_rate_ci` are copied verbatim from `lib_arch.py`. Wilson is the **primary**
interval throughout the evaluation (it is the one that behaves for small `n` and for rates near 0
or 1); the item-level nonparametric bootstrap is reported beside it as a cross-check.""")

co('''def wilson95(k: int, n: int) -> tuple[float, float]:
    """Wilson score interval (primary for small n and rates near 0)."""
    if n <= 0:
        return (float("nan"), float("nan"))
    z = 1.959963984540054
    p = k / n
    d = 1.0 + z * z / n
    c = p + z * z / (2 * n)
    hw = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - hw) / d, (c + hw) / d)


def boot_rate_ci(k: int, n: int, rng: np.random.Generator, b: int = BOOT_B) -> tuple[float, float]:
    """Item-level nonparametric bootstrap of a binomial rate."""
    if n <= 0:
        return (float("nan"), float("nan"))
    items = np.zeros(n)
    items[:k] = 1.0
    draws = rng.integers(0, n, size=(b, n))
    reps = items[draws].mean(axis=1)
    return (float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5)))


rng = np.random.default_rng(SEED)
k, n = counts["MATCH"], len(replayed)
wlo, whi = wilson95(k, n)
blo, bhi = boot_rate_ci(k, n, rng)
print(f"match rate {k}/{n} = {k/n:.4f}")
print(f"  wilson95    [{wlo:.4f}, {whi:.4f}]")
print(f"  bootstrap95 [{blo:.4f}, {bhi:.4f}]   (B={BOOT_B})")
print(f"  full-run match rate (110 rows): {data['metadata']['assertion_match_rate_full']:.4f}")''')

md("""## 4. The disagreements — the actual product

The five MISMATCH rows are the point of the whole evaluation: each one is a number in the draft
that does not survive recomputation, classified rather than merely flagged (stale denominators, a
stale count, an undercount of unreproduced quoted values, and one case where the *value* was right
but the **subset label** was not).""")

co('''mismatches = [row for row in replayed if row["verdict"] != "MATCH"]
print(f"{len(mismatches)} disagreement(s) in this subset\\n")
for row in mismatches:
    print(f"claim_id   : {row['claim_id']}")
    print(f"  quoted     : {row['draft_quoted_value']}")
    print(f"  recomputed : {row['recomputed_value']}")
    print(f"  abs_diff   : {row['abs_diff']}   tol={row['tolerance']} ({row['tolerance_class']})")
    print(f"  provenance : {row['provenance']}")
    print(f"  verdict    : {row['verdict']}\\n")''')

md("""## 5. Cross-check gates and scope

Two gates guard the re-analysis itself, both carried in the archived metadata: the arm-2
`verify.py` re-run (17/17 PASS) and the arm-1 weight-statistics gate (`max|dW05|` ~ 1e-5, Spearman
1.0000, ordering preserved). The scope constraints record what the evaluation deliberately did
*not* do.""")

co('''gates = data["metadata"]["cross_check_gates"]
for name, g in gates.items():
    print(f"[{name}]")
    for kk, vv in g.items():
        print(f"   {kk}: {vv}")
    print()
print("scope constraints:")
for kk, vv in data["metadata"]["scope_constraints"].items():
    print(f"   {kk}: {vv}")''')

md("""## 6. Results

Left: replayed verdicts broken out by tolerance class. Right: `abs_diff` against its declared
tolerance on log axes — every point below the diagonal is a MATCH, every point above it is a
disagreement. Exact-string claims (tolerance 0) and non-numeric rows are plotted at the axis floor.""")

co('''# ---- summary table -------------------------------------------------------
classes = sorted(TOL.keys())
print(f"{'tolerance_class':<22}{'tol':>10}{'n':>6}{'MATCH':>8}{'MISMATCH':>10}")
print("-" * 56)
for c in classes:
    sub = [r for r in replayed if r["tolerance_class"] == c]
    if not sub:
        continue
    m = sum(1 for r in sub if r["verdict"] == "MATCH")
    print(f"{c:<22}{TOL[c]:>10.2e}{len(sub):>6}{m:>8}{len(sub)-m:>10}")
print("-" * 56)
print(f"{'TOTAL':<22}{'':>10}{len(replayed):>6}{counts['MATCH']:>8}{counts['MISMATCH']:>10}")

# ---- figure --------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.6))

present = [c for c in classes if any(r["tolerance_class"] == c for r in replayed)]
nmatch = [sum(1 for r in replayed if r["tolerance_class"] == c and r["verdict"] == "MATCH") for c in present]
nmiss = [sum(1 for r in replayed if r["tolerance_class"] == c and r["verdict"] != "MATCH") for c in present]
x = np.arange(len(present))
ax1.bar(x, nmatch, color="#2e7d32", label="MATCH")
ax1.bar(x, nmiss, bottom=nmatch, color="#c62828", label="MISMATCH")
ax1.set_xticks(x); ax1.set_xticklabels(present, rotation=20, ha="right")
ax1.set_ylabel("assertions"); ax1.set_title(f"Replayed verdicts by tolerance class (n={len(replayed)})")
ax1.legend()
for xi, (a, b) in enumerate(zip(nmatch, nmiss)):
    if b: ax1.text(xi, a + b + 0.6, str(b), ha="center", color="#c62828", fontweight="bold")

FLOOR = 1e-8
for verdict, color, mark in (("MATCH", "#2e7d32", "o"), ("MISMATCH", "#c62828", "X")):
    sub = [r for r in replayed if r["verdict"] == verdict]
    if not sub:
        continue
    xs = [max(r["tolerance"], FLOOR) for r in sub]
    ys = [max(r["abs_diff"], FLOOR) if r["abs_diff"] is not None else 1.0 for r in sub]
    ax2.scatter(xs, ys, c=color, marker=mark, s=48 if verdict == "MISMATCH" else 26,
                alpha=0.85, label=verdict, zorder=3 if verdict == "MISMATCH" else 2)
lim = [FLOOR / 2, 10]
ax2.plot(lim, lim, "k--", lw=1, label="abs_diff = tolerance")
ax2.set_xscale("log"); ax2.set_yscale("log"); ax2.set_xlim(*lim); ax2.set_ylim(*lim)
ax2.set_xlabel("declared tolerance"); ax2.set_ylabel("|quoted - recomputed|")
ax2.set_title("Every claim against its declared tolerance")
ax2.legend(loc="upper left")
plt.tight_layout(); plt.show()

print(f"\\nverdicts reproducing the archived run: {agree}/{len(replayed)}")
print(f"match rate {k}/{n} = {k/n:.4f}  wilson95 [{wlo:.4f}, {whi:.4f}]")''')

nb = {"cells": C, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
      "language_info": {"name": "python", "version": "3.12.12"}}, "nbformat": 4, "nbformat_minor": 5}
p = "/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins/code_demo.ipynb"
json.dump(nb, open(p, "w"), indent=1)
print("wrote", p, len(C), "cells")
PYEOF
python3 /tmp/claude-0/-ai-inventor-aii-data-runs-run-UtpduT-D2IS2-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-4-art-ckuwEkspyins/dbd2ef6a-2da1-4fdc-98a4-a2d87c8eb624/scratchpad/mk.py
```

### [29] TOOL RESULT — Bash · 2026-08-14 07:40:30 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins/code_demo.ipynb 19 cells", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] TOOL CALL — Bash · 2026-08-14 07:40:42 UTC

```
/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel && time .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -30
```

### [31] TOOL RESULT — Bash · 2026-08-14 07:48:42 UTC

```
{"stdout": "[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: python3.12 -m pip install --upgrade pip\n    return loop.run_until_complete(inner)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/usr/local/lib/python3.12/asyncio/base_events.py\", line 691, in run_until_complete\n    return future.result()\n           ^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins/.nb_env/lib/python3.12/site-packages/nbclient/client.py\", line 1062, in async_execute_cell\n    await self._check_raise_for_error(cell, cell_index, exec_reply)\n  File \"/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins/.nb_env/lib/python3.12/site-packages/nbclient/client.py\", line 918, in _check_raise_for_error\n    raise CellExecutionError.from_cell_and_msg(cell, exec_reply_content)\nnbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:\n------------------\ndata = load_data()\nprint(data[\"metadata\"][\"evaluation_name\"])\nprint(\"subset rows:\", len(data[\"examples\"]), \"| full-run rows:\", data[\"metadata\"][\"n_assertions_full\"])\nprint(\"full-run verdicts:\", data[\"metadata\"][\"assertion_verdict_counts_full\"])\nprint(\"declared tolerances:\", json.dumps(data[\"metadata\"][\"assertion_tolerances\"], indent=2))\n------------------\n\n\n\u001b[31m---------------------------------------------------------------------------\u001b[39m\n\u001b[31mKeyError\u001b[39m                                  Traceback (most recent call last)\n\u001b[36mCell\u001b[39m\u001b[36m \u001b[39m\u001b[32mIn[4]\u001b[39m\u001b[32m, line 2\u001b[39m\n\u001b[32m      1\u001b[39m data = load_data()\n\u001b[32m----> \u001b[39m\u001b[32m2\u001b[39m print(data[\u001b[33m\"metadata\"\u001b[39m][\u001b[33m\"evaluation_name\"\u001b[39m])\n\u001b[32m      3\u001b[39m print(\u001b[33m\"subset rows:\"\u001b[39m, len(data[\u001b[33m\"examples\"\u001b[39m]), \u001b[33m\"| full-run rows:\"\u001b[39m, data[\u001b[33m\"metadata\"\u001b[39m][\u001b[33m\"n_assertions_full\"\u001b[39m])\n\u001b[32m      4\u001b[39m print(\u001b[33m\"full-run verdicts:\"\u001b[39m, data[\u001b[33m\"metadata\"\u001b[39m][\u001b[33m\"assertion_verdict_counts_full\"\u001b[39m])\n\u001b[32m      5\u001b[39m print(\u001b[33m\"declared tolerances:\"\u001b[39m, json.dumps(data[\u001b[33m\"metadata\"\u001b[39m][\u001b[33m\"assertion_tolerances\"\u001b[39m], indent=\u001b[32m2\u001b[39m))\n\n\u001b[31mKeyError\u001b[39m: 'metadata'\n\n\nreal\t2m5.010s\nuser\t0m6.364s\nsys\t0m0.943s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] TOOL CALL — Bash · 2026-08-14 07:48:52 UTC

```
python3 -c "
import urllib.request,json
d=json.loads(urllib.request.urlopen('https://raw.githubusercontent.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/main/round-4/evaluation-1/demo/mini_demo_data.json').read())
print(type(d), list(d)[:8] if isinstance(d,dict) else len(d))"
```

### [33] TOOL RESULT — Bash · 2026-08-14 07:48:52 UTC

```
{"stdout": "<class 'dict'> ['description', 'source', 'panel_rows', 'score_column_orientation', 'orientation_map', 'pass_rule_thresholds', 'panel_assertions', 'archived_reference_values']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [34] TOOL CALL — Read · 2026-08-14 07:48:56 UTC

```
/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins/code_demo.ipynb
```

### [35] TOOL RESULT — Read · 2026-08-14 07:48:56 UTC

```
{"type": "notebook", "file": {"filePath": "/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins/code_demo.ipynb", "cells": [{"cellType": "markdown", "source": "# Rechecking every number in the draft — demo\n\nThis artifact is a **pure re-analysis**: `$0.00` of LLM spend, **0** model weights loaded,\n**0** forward passes, **0** generations, **0** Hub fetches. The original `eval.py` reads six\narchived experiment trees and re-derives every number the paper draft quotes, emitting an\n**assertion table** where each row carries `(draft_quoted_value, recomputed_value, tolerance,\nverdict, provenance)`.\n\nFull run: **110 claim_ids -> 105 MATCH / 5 MISMATCH / 0 UNAVAILABLE** (~21 s on 4 CPUs).\n\nThis notebook replays the *comparison core* of that evaluation on a curated 100-row subset of the\nshipped assertion table (all 5 MISMATCH rows plus 95 MATCH rows stratified across the five\ntolerance classes). The verdict logic (`TOL`, `_row`) and the interval helpers (`wilson95`,\n`boot_rate_ci`) are copied verbatim from `ws_assert.py` / `lib_arch.py`; we re-run them on the\narchived `(quoted, recomputed)` pairs and check that every verdict reproduces.", "cell_id": "cell-0"}, {"cellType": "code", "source": "import subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# Core packages (pre-installed on Colab, install locally to match Colab env)\nif 'google.colab' not in sys.modules:\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')", "cell_id": "cell-1", "language": "python"}, {"cellType": "code", "source": "# Imports as in the original scripts (eval.py / ws_assert.py / lib_arch.py), plus matplotlib\nfrom __future__ import annotations\n\nimport json\nimport math\nimport os\nfrom typing import Any\n\nimport numpy as np\nimport matplotlib.pyplot as plt", "cell_id": "cell-2", "language": "python"}, {"cellType": "code", "source": "GITHUB_DATA_URL = \"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/main/round-4/evaluation-1/demo/mini_demo_data.json\"\n\ndef load_data():\n    try:\n        import urllib.request\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\n            return json.loads(response.read().decode())\n    except Exception: pass\n    if os.path.exists(\"mini_demo_data.json\"):\n        with open(\"mini_demo_data.json\") as f: return json.load(f)\n    raise FileNotFoundError(\"Could not load mini_demo_data.json\")", "cell_id": "cell-3", "language": "python"}, {"cellType": "code", "source": "data = load_data()\nprint(data[\"metadata\"][\"evaluation_name\"])\nprint(\"subset rows:\", len(data[\"examples\"]), \"| full-run rows:\", data[\"metadata\"][\"n_assertions_full\"])\nprint(\"full-run verdicts:\", data[\"metadata\"][\"assertion_verdict_counts_full\"])\nprint(\"declared tolerances:\", json.dumps(data[\"metadata\"][\"assertion_tolerances\"], indent=2))", "cell_id": "cell-4", "language": "python"}, {"cellType": "markdown", "source": "## Config\n\nAll tunable parameters. `N_ASSERTIONS` is how many rows of the archived assertion table we replay,\n`BOOT_B` is the bootstrap replicate count (original: 10,000), `SEED` is the original run's seed.", "cell_id": "cell-5"}, {"cellType": "code", "source": "# --- tunable parameters (original values in comments) ---\nN_ASSERTIONS = 100      # rows of the assertion table to replay (full run: 110)\nBOOT_B       = 10000    # bootstrap replicates for the rate CI (original: 10000)\nSEED         = data[\"metadata\"][\"seed\"]   # 20260814, the original run's seed\n\nrows_in = data[\"examples\"][:N_ASSERTIONS]\nprint(f\"replaying {len(rows_in)} assertion rows | BOOT_B={BOOT_B} | SEED={SEED}\")", "cell_id": "cell-6", "language": "python"}, {"cellType": "markdown", "source": "## 1. The verdict logic, verbatim\n\n`TOL` and `_row` are copied unchanged from `ws_assert.py`. Every claim is compared under a\ntolerance declared **up front** by its class: `1e-6` for values copied verbatim out of an archive,\n`1e-4` for float re-derivations, `0.005` for rates rebuilt from reconstructed counts, exact string\nequality for repo_ids and evidence spans, and `5.001e-4` for a draft value quoted at 3 dp against\nits full-precision source.", "cell_id": "cell-7"}, {"cellType": "code", "source": "# Tolerances declared up front.\nTOL = {\n    \"verbatim\": 1e-6,       # values copied verbatim from an archive\n    \"float_rederive\": 1e-4,  # float re-derivations\n    \"rate_reconstructed\": 0.005,  # rates re-derived from reconstructed counts\n    \"exact_string\": 0.0,     # repo_ids and evidence spans\n    \"quoted_rounding\": 5.001e-4,  # a draft value quoted at 3 dp against its full-precision source\n}\n\n\ndef _row(claim_id: str, quoted: Any, recomputed: Any, tol_key: str, provenance: str) -> dict[str, Any]:\n    tol = TOL[tol_key]\n    if recomputed is None:\n        return {\"claim_id\": claim_id, \"draft_quoted_value\": quoted, \"recomputed_value\": None,\n                \"abs_diff\": None, \"tolerance\": tol, \"tolerance_class\": tol_key,\n                \"verdict\": \"UNAVAILABLE\", \"provenance\": provenance}\n    if not isinstance(quoted, (int, float)) or not isinstance(recomputed, (int, float)) \\\n            or isinstance(quoted, bool) or isinstance(recomputed, bool):\n        ok = quoted == recomputed\n        return {\"claim_id\": claim_id, \"draft_quoted_value\": quoted, \"recomputed_value\": recomputed,\n                \"abs_diff\": 0.0 if ok else None, \"tolerance\": tol, \"tolerance_class\": tol_key,\n                \"verdict\": \"MATCH\" if ok else \"MISMATCH\", \"provenance\": provenance}\n    d = abs(float(quoted) - float(recomputed))\n    return {\"claim_id\": claim_id, \"draft_quoted_value\": quoted, \"recomputed_value\": recomputed,\n            \"abs_diff\": d, \"tolerance\": tol, \"tolerance_class\": tol_key,\n            \"verdict\": \"MATCH\" if d <= tol else \"MISMATCH\", \"provenance\": provenance}", "cell_id": "cell-8", "language": "python"}, {"cellType": "markdown", "source": "## 2. Replay the assertion table\n\nThe archived rows store the quoted / recomputed pair as strings (that is how they are shipped in\n`eval_out.json`). We coerce back to float where the pair is numeric — a value that cannot be parsed\nas a float stays a string and falls through `_row`'s exact-equality branch, which is exactly what\nthe original does for `repo_id` and evidence-span claims. A `None` recomputed value yields\n`UNAVAILABLE`.\n\nEach replayed verdict is then checked against the verdict the original run emitted.", "cell_id": "cell-9"}, {"cellType": "code", "source": "def _maybe_float(x):\n    \"\"\"Archived rows ship values as strings; restore numerics, leave genuine strings alone.\"\"\"\n    if x is None:\n        return None\n    if isinstance(x, (int, float)):\n        return x\n    try:\n        return float(x)\n    except (TypeError, ValueError):\n        return x\n\n\nreplayed = []\nfor ex in rows_in:\n    q = _maybe_float(ex[\"predict_draft_quoted_value\"])\n    r = _maybe_float(ex[\"predict_recomputed_value\"])\n    replayed.append(_row(ex[\"input\"], q, r, ex[\"metadata_tolerance_class\"], ex[\"metadata_provenance\"]))\n\ncounts = {\"MATCH\": 0, \"MISMATCH\": 0, \"UNAVAILABLE\": 0}\nfor row in replayed:\n    counts[row[\"verdict\"]] += 1\n\nagree = sum(1 for row, ex in zip(replayed, rows_in) if row[\"verdict\"] == ex[\"output\"])\nprint(\"replayed verdict counts:\", counts)\nprint(f\"verdicts reproducing the archived run: {agree}/{len(replayed)}\")\nprint(\"match rate on this subset:\", round(counts[\"MATCH\"] / len(replayed), 6))", "cell_id": "cell-10", "language": "python"}, {"cellType": "markdown", "source": "## 3. Wilson + bootstrap interval on the match rate\n\n`wilson95` and `boot_rate_ci` are copied verbatim from `lib_arch.py`. Wilson is the **primary**\ninterval throughout the evaluation (it is the one that behaves for small `n` and for rates near 0\nor 1); the item-level nonparametric bootstrap is reported beside it as a cross-check.", "cell_id": "cell-11"}, {"cellType": "code", "source": "def wilson95(k: int, n: int) -> tuple[float, float]:\n    \"\"\"Wilson score interval (primary for small n and rates near 0).\"\"\"\n    if n <= 0:\n        return (float(\"nan\"), float(\"nan\"))\n    z = 1.959963984540054\n    p = k / n\n    d = 1.0 + z * z / n\n    c = p + z * z / (2 * n)\n    hw = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))\n    return ((c - hw) / d, (c + hw) / d)\n\n\ndef boot_rate_ci(k: int, n: int, rng: np.random.Generator, b: int = BOOT_B) -> tuple[float, float]:\n    \"\"\"Item-level nonparametric bootstrap of a binomial rate.\"\"\"\n    if n <= 0:\n        return (float(\"nan\"), float(\"nan\"))\n    items = np.zeros(n)\n    items[:k] = 1.0\n    draws = rng.integers(0, n, size=(b, n))\n    reps = items[draws].mean(axis=1)\n    return (float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5)))\n\n\nrng = np.random.default_rng(SEED)\nk, n = counts[\"MATCH\"], len(replayed)\nwlo, whi = wilson95(k, n)\nblo, bhi = boot_rate_ci(k, n, rng)\nprint(f\"match rate {k}/{n} = {k/n:.4f}\")\nprint(f\"  wilson95    [{wlo:.4f}, {whi:.4f}]\")\nprint(f\"  bootstrap95 [{blo:.4f}, {bhi:.4f}]   (B={BOOT_B})\")\nprint(f\"  full-run match rate (110 rows): {data['metadata']['assertion_match_rate_full']:.4f}\")", "cell_id": "cell-12", "language": "python"}, {"cellType": "markdown", "source": "## 4. The disagreements — the actual product\n\nThe five MISMATCH rows are the point of the whole evaluation: each one is a number in the draft\nthat does not survive recomputation, classified rather than merely flagged (stale denominators, a\nstale count, an undercount of unreproduced quoted values, and one case where the *value* was right\nbut the **subset label** was not).", "cell_id": "cell-13"}, {"cellType": "code", "source": "mismatches = [row for row in replayed if row[\"verdict\"] != \"MATCH\"]\nprint(f\"{len(mismatches)} disagreement(s) in this subset\\n\")\nfor row in mismatches:\n    print(f\"claim_id   : {row['claim_id']}\")\n    print(f\"  quoted     : {row['draft_quoted_value']}\")\n    print(f\"  recomputed : {row['recomputed_value']}\")\n    print(f\"  abs_diff   : {row['abs_diff']}   tol={row['tolerance']} ({row['tolerance_class']})\")\n    print(f\"  provenance : {row['provenance']}\")\n    print(f\"  verdict    : {row['verdict']}\\n\")", "cell_id": "cell-14", "language": "python"}, {"cellType": "markdown", "source": "## 5. Cross-check gates and scope\n\nTwo gates guard the re-analysis itself, both carried in the archived metadata: the arm-2\n`verify.py` re-run (17/17 PASS) and the arm-1 weight-statistics gate (`max|dW05|` ~ 1e-5, Spearman\n1.0000, ordering preserved). The scope constraints record what the evaluation deliberately did\n*not* do.", "cell_id": "cell-15"}, {"cellType": "code", "source": "gates = data[\"metadata\"][\"cross_check_gates\"]\nfor name, g in gates.items():\n    print(f\"[{name}]\")\n    for kk, vv in g.items():\n        print(f\"   {kk}: {vv}\")\n    print()\nprint(\"scope constraints:\")\nfor kk, vv in data[\"metadata\"][\"scope_constraints\"].items():\n    print(f\"   {kk}: {vv}\")", "cell_id": "cell-16", "language": "python"}, {"cellType": "markdown", "source": "## 6. Results\n\nLeft: replayed verdicts broken out by tolerance class. Right: `abs_diff` against its declared\ntolerance on log axes — every point below the diagonal is a MATCH, every point above it is a\ndisagreement. Exact-string claims (tolerance 0) and non-numeric rows are plotted at the axis floor.", "cell_id": "cell-17"}, {"cellType": "code", "source": "# ---- summary table -------------------------------------------------------\nclasses = sorted(TOL.keys())\nprint(f\"{'tolerance_class':<22}{'tol':>10}{'n':>6}{'MATCH':>8}{'MISMATCH':>10}\")\nprint(\"-\" * 56)\nfor c in classes:\n    sub = [r for r in replayed if r[\"tolerance_class\"] == c]\n    if not sub:\n        continue\n    m = sum(1 for r in sub if r[\"verdict\"] == \"MATCH\")\n    print(f\"{c:<22}{TOL[c]:>10.2e}{len(sub):>6}{m:>8}{len(sub)-m:>10}\")\nprint(\"-\" * 56)\nprint(f\"{'TOTAL':<22}{'':>10}{len(replayed):>6}{counts['MATCH']:>8}{counts['MISMATCH']:>10}\")\n\n# ---- figure --------------------------------------------------------------\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.6))\n\npresent = [c for c in classes if any(r[\"tolerance_class\"] == c for r in replayed)]\nnmatch = [sum(1 for r in replayed if r[\"tolerance_class\"] == c and r[\"verdict\"] == \"MATCH\") for c in present]\nnmiss = [sum(1 for r in replayed if r[\"tolerance_class\"] == c and r[\"verdict\"] != \"MATCH\") for c in present]\nx = np.arange(len(present))\nax1.bar(x, nmatch, color=\"#2e7d32\", label=\"MATCH\")\nax1.bar(x, nmiss, bottom=nmatch, color=\"#c62828\", label=\"MISMATCH\")\nax1.set_xticks(x); ax1.set_xticklabels(present, rotation=20, ha=\"right\")\nax1.set_ylabel(\"assertions\"); ax1.set_title(f\"Replayed verdicts by tolerance class (n={len(replayed)})\")\nax1.legend()\nfor xi, (a, b) in enumerate(zip(nmatch, nmiss)):\n    if b: ax1.text(xi, a + b + 0.6, str(b), ha=\"center\", color=\"#c62828\", fontweight=\"bold\")\n\nFLOOR = 1e-8\nfor verdict, color, mark in ((\"MATCH\", \"#2e7d32\", \"o\"), (\"MISMATCH\", \"#c62828\", \"X\")):\n    sub = [r for r in replayed if r[\"verdict\"] == verdict]\n    if not sub:\n        continue\n    xs = [max(r[\"tolerance\"], FLOOR) for r in sub]\n    ys = [max(r[\"abs_diff\"], FLOOR) if r[\"abs_diff\"] is not None else 1.0 for r in sub]\n    ax2.scatter(xs, ys, c=color, marker=mark, s=48 if verdict == \"MISMATCH\" else 26,\n                alpha=0.85, label=verdict, zorder=3 if verdict == \"MISMATCH\" else 2)\nlim = [FLOOR / 2, 10]\nax2.plot(lim, lim, \"k--\", lw=1, label=\"abs_diff = tolerance\")\nax2.set_xscale(\"log\"); ax2.set_yscale(\"log\"); ax2.set_xlim(*lim); ax2.set_ylim(*lim)\nax2.set_xlabel(\"declared tolerance\"); ax2.set_ylabel(\"|quoted - recomputed|\")\nax2.set_title(\"Every claim against its declared tolerance\")\nax2.legend(loc=\"upper left\")\nplt.tight_layout(); plt.show()\n\nprint(f\"\\nverdicts reproducing the archived run: {agree}/{len(replayed)}\")\nprint(f\"match rate {k}/{n} = {k/n:.4f}  wilson95 [{wlo:.4f}, {whi:.4f}]\")", "cell_id": "cell-18", "language": "python"}]}}
```

### [36] TOOL CALL — NotebookEdit · 2026-08-14 07:49:06 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins/code_demo.ipynb', 'cell_id': 'cell-3', 'new_source': 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/main/round-4/evaluation-1/demo/mini_demo_data.json"\n\ndef _ok(d):\n    # this demo needs the assertion-table payload; guard against a stale file at the URL\n    return isinstance(d, dict) and "examples" in d and "metadata" in d\n\ndef load_data():\n    try:\n        import urllib.request\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\n            d = json.loads(response.read().decode())\n        if _ok(d): return d\n    except Exception: pass\n    if os.path.exists("mini_demo_data.json"):\n        with open("mini_demo_data.json") as f:\n            d = json.load(f)\n        if _ok(d): return d\n    raise FileNotFoundError("Could not load mini_demo_data.json")'}
```

### [37] TOOL RESULT — NotebookEdit · 2026-08-14 07:49:06 UTC

```
{"new_source": "GITHUB_DATA_URL = \"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/main/round-4/evaluation-1/demo/mini_demo_data.json\"\n\ndef _ok(d):\n    # this demo needs the assertion-table payload; guard against a stale file at the URL\n    return isinstance(d, dict) and \"examples\" in d and \"metadata\" in d\n\ndef load_data():\n    try:\n        import urllib.request\n        with urllib.request.urlope... [truncated, 34333 chars total]
```

### [38] TOOL CALL — Bash · 2026-08-14 07:49:14 UTC

```
time .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -20
```

### [39] TOOL RESULT — Bash · 2026-08-14 07:49:54 UTC

```
{"stdout": "[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_4/art_ckuwEkspyins/.nb_env/lib/python3.12/site-packages/nbformat/validator.py:434: MissingIDFieldWarning: Cell is missing an id field, this will become a hard error in future nbformat versions. You may want to use `normalize()` on your notebooks before validations (available since nbformat 5.1.4). Previous versions of nbformat are fixing this issue transparently, and will stop doing so in the future.\n  _validate(nbdict, ref, version, version_minor, relax_add_props)\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 111537 bytes to code_demo.ipynb\n\nreal\t0m42.683s\nuser\t0m2.692s\nsys\t0m0.379s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [40] ASSISTANT · 2026-08-14 07:49:58 UTC

```
Passed in 43 s. Checking the outputs:
```

### [41] TOOL CALL — Bash · 2026-08-14 07:49:58 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code': continue
    for o in c.get('outputs',[]):
        t=''.join(o.get('text',[])) if 'text' in o else ('<'+o.get('output_type','')+' '+','.join(o.get('data',{}).keys())+'>')
        if t.strip(): print(f'--- cell {i} ---'); print(t[:1400])
" | head -120
```

### [42] TOOL RESULT — Bash · 2026-08-14 07:49:58 UTC

```
{"stdout": "--- cell 1 ---\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n--- cell 4 ---\nRecheck every number in the draft\nsubset rows: 100 | full-run rows: 110\nfull-run verdicts: {'MATCH': 105, 'MISMATCH': 5, 'UNAVAILABLE': 0}\ndeclared tolerances: {\n  \"float_rederivation\": 0.0001,\n  \"rate_from_reconstructed_counts\": 0.005,\n  \"repo_ids_and_evidence_spans\": \"exact string match\",\n  \"verbatim_copy\": 1e-06\n}\n\n--- cell 6 ---\nreplaying 100 assertion rows | BOOT_B=10000 | SEED=20260814\n\n--- cell 10 ---\nreplayed verdict counts: {'MATCH': 95, 'MISMATCH': 5, 'UNAVAILABLE': 0}\nverdicts reproducing the archived run: 100/100\nmatch rate on this subset: 0.95\n\n--- cell 12 ---\nmatch rate 95/100 = 0.9500\n  wilson95    [0.8882, 0.9785]\n  bootstrap95 [0.9000, 0.9900]   (B=10000)\n  full-run match rate (110 rows): 0.9545\n\n--- cell 14 ---\n5 disagreement(s) in this subset\n\nclaim_id   : W2.n_real_intensity_axes_quoted_as_6\n  quoted     : 6.0\n  recomputed : 7.0\n  abs_diff   : 1.0   tol=1e-06 (verbatim)\n  provenance : A2 crossing dataset, rows with a real intensity axis\n  verdict    : MISMATCH\n\nclaim_id   : W4.B09_abs_rho_member_0.766_against_28_member_contract_subset\n  quoted     : 0.766\n  recomputed : 0.67\n  abs_diff   : 0.09599999999999997   tol=0.0001 (float_rederive)\n  provenance : A5/numbers.json correlations.member.B09.harmful_refusal_rate (n=28) - EXPECTED MISMATCH: this is the subset the draft states\n  verdict    : MISMATCH\n\nclaim_id   : W4.n_subset_corrected_values_quoted_as_4\n  quoted     : 4.0\n  recomputed : 5.0\n  abs_diff   : 1.0   tol=1e-06 (verbatim)\n  provenance : A5/numbers.json quoted_value_forensics.closest_match_per_quoted_value - the plan says FOUR draft-quoted 'correlations' are paired differences on a different subset; the forensics block carries this many\n  verdict    : MISMATCH\n\nclaim_id   : W5.skipped_7\n  quoted     : 7.0\n  recomputed : 8.0\n  abs_diff   : 1.0   tol=1e-06 (verbatim)\n  provenance : A2/results/scan.jsonl\n  verdict    : MISMATCH\n\nclaim_id   : W5.unresolved_quoted_as_65\n  quoted     : 65.0\n  recomputed : 81.0\n  abs_diff   : 16.0   tol=1e-06 (verbatim)\n  provenance : recomputed from scan.jsonl rows - the 65-vs-81 discrepancy, adjudicated mechanically\n  verdict    : MISMATCH\n\n\n--- cell 16 ---\n[verify_py]\n   exit_code: 0\n   gate_17_of_17: True\n   n_pass: 17\n   n_total: 17\n   ran: True\n   stderr_tail: \n   summary_line: 17/17 cross-checks pass\n\n[wstats_gate]\n   attributable_divergences_not_smoothed: {'W01_on_abliterated_members': 'reproduces to 1e-4 on non-abliterated members but drifts up to 0.048 on ABLITERATED ones (lambda_min sits at the float noise floor exactly where the scar is); NOT a load-dtype effect', 'W03': 'systematic +0.015..+0.034 DEFINITIONAL difference: the published formula takes q05 of the per-direction MEAN energy; the iteration-2 code pools all (direction x matrix) energies first', 'revision_drift': 'zero'}\n   bound_applied: 1e-05\n   bound_note: The archive quotes 'max|dW05| = 9.9e-06'. The full-precision value in results/gate.json is 9.908662263136137e-06, i.e. the quote is that number at 2 significant figures. A literal <= 9.9e-06 test therefore fails on a rounding artefact, not on a reproduction failure; the bound actually applied is 1.0e-05 and both numbers are printed.\n   gate_json_pass: PASS\n   gate_json_reported_max_abs_dW05: 9.908662263136137e-06\n   gate_json_spearman: 0.9999999999999999\n   gate_json_w05_ordering_preserved: True\n   max_abs_delta_W05_member: huihui-ai/Llama-3.2-1B-Instruct-abliterated\n   max_abs_delta_W05_vs_archive: 9.91e-06\n   n_gate_members: 10\n   rows: [{'abs_delta_W05_vs_archive': 8e-08, 'delta_all_stats': {'W01': -1.57\n--- cell 18 ---\ntolerance_class              tol     n   MATCH  MISMATCH\n--------------------------------------------------------\nexact_string            0.00e+00    10      10         0\nfloat_rederive          1.00e-04    34      33         1\nquoted_rounding         5.00e-04     2       2         0\nrate_reconstructed      5.00e-03     7       7         0\nverbatim                1.00e-06    47      43         4\n--------------------------------------------------------\nTOTAL                              100      95         5\n\n--- cell 18 ---\n<display_data image/png,text/plain>\n--- cell 18 ---\n\nverdicts reproducing the archived run: 100/100\nmatch rate 95/100 = 0.9500  wilson95 [0.8882, 0.9785]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] ASSISTANT · 2026-08-14 07:50:10 UTC

```
All 100/100 verdicts reproduce the archived run, all 5 disagreements surface, figure renders. Config is already at full fidelity (all 100 subset rows, B=10000 bootstrap — the original value), so no scaling rounds are needed.
```

### [44] TOOL CALL — Bash · 2026-08-14 07:50:10 UTC

```
rm -rf .nb_env && grep -c 'raw.githubusercontent.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa/main/round-4/evaluation-1/demo/mini_demo_data.json' code_demo.ipynb && cat > .terminal_claude_agent_struct_out.json <<'EOF'
{
  "out_expected_files": {
    "notebook": "code_demo.ipynb",
    "mini_data_file": "mini_demo_data.json"
  }
}
EOF
ls -la
```

### [45] TOOL RESULT — Bash · 2026-08-14 07:50:46 UTC

```
{"stdout": "1\ntotal 4761\ndrwxr-xr-x 2 root root 1077746 Aug 14 07:50 .\ndrwxr-xr-x 6 root root 3000185 Aug 14 07:37 ..\n-rw-r--r-- 1 root root  641649 Aug 14 07:50 .repl_agent.ptylog\n-rw-r--r-- 1 root root     113 Aug 14 07:50 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root  111545 Aug 14 07:49 code_demo.ipynb\n-rw-r--r-- 1 root root   43042 Aug 14 07:39 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [46] ASSISTANT · 2026-08-14 07:50:59 UTC

```
Done.

**Deliverables** (in the workspace):
- `mini_demo_data.json` (42 KB) — curated subset of the shipped `assertions` dataset: **100 rows** (all 5 MISMATCH + 95 MATCH stratified across the five tolerance classes), plus the metadata the demo needs (declared tolerances, full-run verdict counts, both cross-check gates, scope constraints).
- `code_demo.ipynb` (19 cells) — title/description → install cell (aii-colab guard pattern, numpy+matplotlib only) → imports → GitHub-URL loader with local fallback → `data = load_data()` → config cell → six annotated sections.

**What the notebook replays**, with code copied verbatim from the artifact:
- `TOL` and `_row` from `ws_assert.py` — the tolerance-class verdict logic.
- `wilson95` and `boot_rate_ci` from `lib_arch.py` — Wilson primary, 10k bootstrap beside it.

**Verified run** (43 s end-to-end including installs, well under the 10-min budget):
- 100/100 replayed verdicts reproduce the archived run; 95 MATCH / 5 MISMATCH / 0 UNAVAILABLE.
- Match rate 0.9500, Wilson95 [0.8882, 0.9785], bootstrap95 [0.9000, 0.9900] — against the full-run 0.9545.
- All five disagreements print with quoted/recomputed/tolerance/provenance (the 6-vs-7 axes, 65-vs-81 unresolved, 7-vs-8 skipped, 4-vs-5 unreproduced quoted values, and the B09 0.766-vs-0.670 subset-label case).
- Final cell: per-tolerance-class summary table + a two-panel figure (stacked verdicts by class; `abs_diff` vs declared tolerance on log axes with the `abs_diff = tolerance` diagonal).

One thing to flag: the GitHub raw URL currently serves a **different artifact's** `mini_demo_data.json` (a panel-assertions payload) at that exact path — it will be overwritten by this file at deployment. To keep the notebook working both now and after deployment, `load_data()` validates the fetched payload has `examples`/`metadata` and falls back to the local file if not. The URL string itself is exactly as specified.

`.terminal_claude_agent_struct_out.json` written.
```
