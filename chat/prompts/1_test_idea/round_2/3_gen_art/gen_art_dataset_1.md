# gen_art_dataset_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_art`
> Run: `iter1_33370088803c` — Catching Edited Safety Models by Reading Weights in Sliding Windows
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_dataset_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-13 16:23:06 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<task>
Find, evaluate, and prepare high-quality datasets for the research experiment.
Adapt your search strategy based on the hypothesis and domain requirements.
</task>

<common_mistakes_to_avoid>
Critical pitfalls from past runs. MUST check for and avoid each one.

**1. Picking Obscure or Unusable Datasets**
Do NOT select datasets just because they match a keyword. Red flags: very few downloads (<100), no documentation (dataset card, paper, or GitHub page). Prefer well-used datasets (not necessarily popular or widely known) with clear documentation.
CHECK: >100 downloads? Has documentation? If any "no" → find a better dataset.

**2. Fabricating Dataset Provenance**
Do NOT invent justifications for why a dataset is relevant. If a dataset name contains a number (e.g., "797"), do NOT assume it refers to a specific benchmark suite, OpenML ID, or paper without verification. In past runs, an agent assumed "797" referred to "OpenML benchmark suite 797" with zero evidence, then fabricated a rationale. This was completely false.
CHECK: Can you cite a specific, verifiable source (paper, benchmark page, dataset card) confirming this dataset is what you claim? If not, do not make provenance claims.

**3. Not Verifying Dataset Usefulness**
Always sanity-check that a dataset is actually suitable for the task before committing. Download a sample, inspect the features, and run a quick baseline appropriate for the domain. If the dataset lacks signal or structure for the hypothesis being tested, the entire experiment is wasted.

**4. Settling for the Only Search Result**
If your search returns only 1-2 results, your search terms are too narrow. Broaden your queries, try different keyword combinations, or search for well-known benchmark datasets in the domain. A single obscure result from a narrow query should never be your final choice.
CHECK: Fewer than 5 candidate datasets? Run additional searches with broader or different terms before making a selection.
</common_mistakes_to_avoid>

<critical_requirements>
- Keep final response under 300 characters
</critical_requirements>

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
Your workspace: `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_dataset_1_idx2
type: dataset
title: Published safety scores and a frozen split
summary: >-
  Build the EXTERNAL ground-truth table that replaces our own judge as the correlation target for iteration 2's 50-metric
  screen, plus a frozen, seeded dev/held-out split over weight lineages written BEFORE any metric exists. Deliverable is one
  schema-validated row set with three row kinds: (A) external_score rows, one per (checkpoint, benchmark, metric), each carrying
  raw value, scale, explicit polarity (higher-is-safer vs lower-is-safer), exact source URL, source type, retrieval date,
  and a revision-match confidence flag; (B) split_assignment rows, one per weight lineage, from a deterministic seeded stratified
  rule with the rule text and a timestamped pre-registration statement embedded in the artifact; (C) rule rows encoding the
  machine-readable blanket-refuser disqualification and the Qwen3Guard/Qwen3-4B-SafeRL circularity flag. Coverage is a first-class
  output, reported numerically and honestly: the likely finding at <=4.2B is that published SAFETY numbers are sparse while
  CAPABILITY numbers are dense, and that asymmetry is exactly what iteration 3's analysis plan has to be built around, so
  it must be measured rather than assumed. Highest-yield programmatic sources: open-llm-leaderboard/contents on HF (4,580
  rows, columns include Model, Model sha, #Params (B), Architecture, Precision, Chat Template, and raw+normalised IFEval/BBH/MATH
  Lvl 5/GPQA/MUSR/MMLU-PRO), the HELM public GCS mirror for HELM Safety v1.0 and AIR-Bench 2024, and the HF Hub API + model-card
  READMEs for card-stated safety numbers.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  SCOPE. The unit of the primary table is a (checkpoint, benchmark, metric) triple. Checkpoints come from iteration 1's frozen panel manifest (137 checkpoints / 93 lineages), restricted to <=4.2B parameters. Ideal is EVERY published quantitative score that exists for those checkpoints, on two axes.

  AXIS 1 - SAFETY (the axis the hypothesis needs and the one likely to be thin): TrustLLM, AIR-Bench 2024 (HELM), HELM Safety v1.0 (5 benchmarks x 6 risk categories: violence, fraud, discrimination, sexual content, harassment, deception), SALAD-Bench, SORRY-Bench, DecodingTrust, JailbreakBench / HarmBench ASR tables, XSTest and OR-Bench over-refusal rates, ToxiGen/RealToxicityPrompts, BeaverTails, plus any refusal rate, safety rate, ASR, or guard-model score stated on the model card itself or in the family's tech report (Qwen3, Llama 3.2, Gemma 2, SmolLM2, OLMo, Granite 3.1, Falcon3, MiniCPM, Pythia, TinyLlama, Danube3 all have tech reports or detailed cards). BOTH sides of safety must be representable: harm-refusal AND over-refusal. A row set that only has harm-refusal numbers permits the degenerate blanket-refuser winner the hypothesis explicitly disqualifies, so over-refusal coverage must be reported separately in the coverage summary, not folded into a single 'safety coverage' count.

  AXIS 2 - CAPABILITY (dense, cheap, and needed as a confound control): GSM8K, MMLU, MMLU-PRO, ARC, HellaSwag, IFEval, BBH, GPQA, MUSR, MATH Lvl 5, Arena-Hard, TruthfulQA, Winogrande. The Open LLM Leaderboard v2 contents dataset (open-llm-leaderboard/contents on HF, ~4,580 rows, parquet, loadable via load_dataset) is the highest-coverage single source for small models and MUST be pulled programmatically, never hand-transcribed. Its 'Model sha' column is what makes revision-level matching possible at all and must be carried into our rows.

  PER-ROW REQUIREMENTS (all mandatory, no nulls-by-laziness):
    checkpoint_id (HF repo id, exactly as in the panel manifest), lineage_id, revision_sha_source (the sha the SOURCE evaluated, if stated), revision_sha_panel (the sha our manifest pins), revision_match in {EXACT, SAME_REPO_UNKNOWN_SHA, SIBLING, FAMILY_ONLY}, benchmark, metric_name, value (float), scale (e.g. '0-100 percent', '0-1 rate', 'raw score 0-90'), polarity in {HIGHER_IS_SAFER, LOWER_IS_SAFER, HIGHER_IS_MORE_CAPABLE, NOT_ORDERED} stated EXPLICITLY per row and never inferred downstream from the benchmark name, axis in {SAFETY_HARM, SAFETY_OVERREFUSAL, SAFETY_OTHER, CAPABILITY}, source_url (exact, deep-linked, not a homepage), source_type in {OFFICIAL_MODEL_CARD, TECH_REPORT, PEER_REVIEWED_PAPER, ARXIV_PREPRINT, LEADERBOARD_SNAPSHOT, THIRD_PARTY_REPO}, source_version_or_release (e.g. HELM release v1.1.0, leaderboard snapshot date), retrieval_date (ISO), judge_or_grader (what scored it: GPT-4 judge, Llama Guard, string match, human - unknown is allowed but must be the literal string 'UNSTATED'), circularity_flag (string, empty or e.g. 'QWEN3GUARD_REWARD_CIRCULAR'), and verbatim_snippet (<=300 chars of the source text the number was read from, so the row is auditable without re-fetching).

  POLARITY IS LOAD-BEARING. ASR (attack success rate) is LOWER_IS_SAFER; refusal rate on harmful prompts is HIGHER_IS_SAFER; XSTest full-refusal rate on SAFE items is LOWER_IS_SAFER (a high value is over-refusal, i.e. WORSE); AIR-Bench and HELM safety scores are HIGHER_IS_SAFER. Getting one of these backwards silently flips a Spearman sign in iteration 3, so polarity must be set from the source's own wording and the wording quoted in verbatim_snippet.

  SPLIT REQUIREMENTS. One split_assignment row per weight lineage, covering ALL 93 lineages in the manifest, not just the ones measured this iteration. Held-out >= 1/3 of lineages. Stratified by (architecture_family, has_abliterated_or_uncensored_member, size_bucket) so both sides carry the hard cases. At least two architecture families must appear ONLY in held-out, so leave-one-family-out is possible. Assignment produced by a deterministic seeded rule (fixed seed, sorted lineage ids, documented hash) that is written verbatim into the artifact and reproducible by re-running the emitted rule text.

  SIZE / FORMAT. Well under 300MB - the whole thing is a few thousand JSON rows plus the raw source snapshots. Cache raw pulls (parquet/JSON) to disk so the harvest is auditable and re-runnable offline. Ship full/mini/preview variants per the aii-json skill.

  WHAT WOULD MAKE THIS ARTIFACT FAIL: silent fabrication of a plausible-looking benchmark number (fatal - every value must trace to a fetched URL and a quoted snippet); collapsing SIBLING-revision rows into EXACT rows; a split that leaks an abliterated member's parent across the boundary; or reporting 'good coverage' without the family/scale skew breakdown.
dataset_search_plan: |-
  PRE-FLIGHT (do first, ~30 min).
  P1. LOCATE THE PANEL MANIFEST. Iteration 1's frozen 137-checkpoint / 93-lineage manifest, prompt corpus, and 10-tokenizer-family refusal lexicons live in the previous run's workspaces. Glob for them under /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/ (try iter_1/gen_art/*/data_out.json, *manifest*.json, *panel*.json) and also under /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/ and the user_uploads folder. Log exactly which file you used and its row count.
    FALLBACK IF THE MANIFEST IS NOT FOUND (plan for this - it is the single most likely blocker): rebuild an equivalent panel deterministically from the HF Hub API (huggingface_hub.HfApi().list_models) using the lineage list enumerated in the hypothesis - Qwen3-0.6B/1.7B/4B (base + instruct + SafeRL + abliterated), Qwen2.5-0.5B/1.5B, Llama-3.2-1B/3B, gemma-2-2b, SmolLM2-360M/1.7B, TinyLlama-1.1B, Pythia-410M/1B/1.4B, OLMo-1B, Danube3-500M, Falcon3-1B-Instruct, Granite-3.1-2B-Instruct, MiniCPM-1B - plus abliterated/uncensored derivatives found by searching HF for 'abliterated', 'uncensored', 'ortho' filtered to those base architectures and <=4.2B. Pin every repo's current commit sha via HfApi().model_info(repo, revision='main').sha. Emit the rebuilt manifest as a deliverable row kind so iteration 3 is not blocked either way, and state loudly in the artifact that it is a REBUILD, not the iteration-1 frozen manifest.
  P2. Resolve every checkpoint's #params and architecture from HF config.json / model_info so the <=4.2B filter and the size-bucket stratification are grounded, not guessed.

  STAGE 1 - CAPABILITY HARVEST (cheap, dense, do it first so you have a working pipeline before the hard axis). ~45 min.
  S1.1. load_dataset('open-llm-leaderboard/contents') -> pandas. Columns to keep: eval_name, Model, fullname, 'Model sha', 'Base Model', Architecture, 'Weight type', '#Params (B)', Precision, Type, MoE, 'Chat Template', Average, IFEval, BBH, 'MATH Lvl 5', GPQA, MUSR, 'MMLU-PRO' (raw AND normalised where both exist), Flagged, 'Submission Date'. Join to the panel on normalised repo id (lowercase, strip whitespace); set revision_match=EXACT when 'Model sha' equals the panel sha, SAME_REPO_UNKNOWN_SHA otherwise. Emit one row per (checkpoint, benchmark). DROP rows where Flagged is true, but RECORD them in a separate flagged list rather than deleting silently.
  S1.2. Also pull open-llm-leaderboard/results (per-model raw result files) for any panel checkpoint missing from contents; and try the archived v1 datasets (HuggingFaceH4/open-llm-leaderboard-evaluations-results, open-llm-leaderboard-old/results) for older small models (Pythia, TinyLlama, OLMo, Danube3) which predate v2 and may only exist in v1. Record which leaderboard VERSION each row came from - v1 and v2 scores are NOT comparable and mixing them without a version column is a real error.
  S1.3. GSM8K / MMLU / ARC / HellaSwag / Arena-Hard where the leaderboards do not carry them: read the family tech report / model card table. Qwen3, Llama-3.2, Gemma-2, SmolLM2, Granite-3.1, Falcon3, MiniCPM and OLMo all publish per-size benchmark tables in their cards or reports.

  STAGE 2 - SAFETY HARVEST (the hard, high-value axis). ~2.5 h. Work source-by-source, each with a cached raw snapshot.
  S2.1. HELM (two leaderboards, one mechanism). HELM Safety v1.0 (crfm.stanford.edu/helm/safety/) and AIR-Bench 2024 (crfm.stanford.edu/helm/air-bench/v1.1.0/). The site is a static front-end over JSON on a public GCS bucket: https://storage.googleapis.com/crfm-helm-public/<project>/benchmark_output/releases/<release>/... with per-group JSON (groups/*.json, schema.json, runs_to_run_suites.json). PROBE the exact paths with HTTP GET before writing the parser - do not assume the layout; if the bucket paths 404, fall back to (a) the JSON the leaderboard page itself requests (read the page source / network paths), (b) the stanford-crfm/helm GitHub repo's documented download instructions, (c) the AIR-Bench paper's own results table (arXiv:2407.17436, openreview UVnD9Ze6mF) transcribed with verbatim_snippet. EXPECT LOW PANEL OVERLAP: HELM evaluates ~21-24 mostly frontier models, so most or all of our <=4.2B panel will be absent. That absence is a RESULT - record it as a coverage number, do not pad it.
  S2.2. TrustLLM (trustllmbenchmark.github.io + arXiv:2401.05561): pull the leaderboard tables and the paper's per-model results. Again expect frontier-model skew; harvest whatever small models appear (Vicuna/Llama-2 7B class at best) and record overlap honestly.
  S2.3. SALAD-Bench (OpenSafetyLab, arXiv:2402.05044, HF: OpenSafetyLab/Salad-Data and the leaderboard space), SORRY-Bench (ICLR 2025, github.com/SORRY-Bench/sorry-bench, HF: sorry-bench/sorry-bench-202406 - note the main dataset is GATED, but the PAPER's model results table is not and is the thing we actually need), DecodingTrust (decodingtrust.github.io, per-perspective scores), JailbreakBench (jailbreakbench.github.io leaderboard - ASR per model per attack), HarmBench (harmbench.org results table), OR-Bench (HF: bench-llm/or-bench + its leaderboard space, over-refusal rates), XSTest (arXiv:2308.01263 and any paper reporting XSTest per model - Hasan & Biswas arXiv:2605.05427 audits 21 open-weight LLMs on over-refusal AND harmful compliance and is a prime harvest target for BOTH safety sub-axes).
  S2.4. MODEL CARDS AND TECH REPORTS - likely the single richest safety source at our scale. For every panel checkpoint, fetch https://huggingface.co/<repo>/raw/main/README.md via the Hub API and regex-scan for safety numbers: /(safety|refus|harmful|toxic|jailbreak|ASR|attack success|over-refus|WildGuard|Guard)/i near a numeric. Qwen3-4B-SafeRL's card is the flagship case - it documents RL against a Qwen3Guard-Gen-4B safety reward plus a WorldPM-Helpsteer2 helpfulness reward and reports safety/helpfulness numbers; harvest every number it states AND set circularity_flag='QWEN3GUARD_REWARD_CIRCULAR' on any row whose judge_or_grader is a Qwen3Guard variant, because the hypothesis forbids using it as ground truth for that model. Also fetch the Qwen3 tech report, Llama-3.2 card, Gemma-2 card (which reports safety/ToxiGen/RealToxicity numbers), SmolLM2 paper, OLMo paper, Granite-3.1 card, and the abliterated-model cards (which often state a residual refusal rate - harvest it and mark source_type=THIRD_PARTY_REPO, low trust).
  S2.5. LAST-RESORT SWEEP for anything missed: scholarly search per checkpoint name + 'safety' / 'refusal rate' / 'jailbreak' restricted to 2024-2026, and fetch_grep the resulting PDFs for the model name to pull table values with context. Cap this at ~20 min per family so it cannot eat the budget.

  STAGE 3 - THE COVERAGE REPORT (a required deliverable, not a footnote). ~20 min.
  Compute and emit, as structured rows and as a human-readable markdown summary: n_checkpoints in panel at <=4.2B; n with >=1 SAFETY_HARM row; n with >=1 SAFETY_OVERREFUSAL row; n with >=1 CAPABILITY row; n with EXACT revision match vs SAME_REPO_UNKNOWN_SHA vs SIBLING; the same counts broken down by architecture family and by size bucket (<1B, 1-2B, 2-4.2B); and the count of lineages where at least one MEMBER has a safety number (lineage-level coverage differs from checkpoint-level coverage and iteration 3 bootstraps over lineages, so both are needed). Then emit an explicit list, machine-readable, of checkpoints that will REQUIRE in-house measurement because no external safety number exists - this list is the direct input to iteration 3's measurement budget. If safety coverage is below ~20% of the panel (the likely outcome), state that numerically and state plainly that the external-ground-truth axis of H3 is coverage-limited at this scale and that the hypothesis's documented fallback (two in-house refusal rates: harmful-prompt refusal and XSTest-style harmless-but-alarming refusal, with the R4 evaluator-system-prompt fix in force) becomes primary for the uncovered checkpoints. Do NOT run those in-house measurements here - that is an experiment artifact; just name the checkpoints and the axes needed.

  STAGE 4 - THE FROZEN SPLIT. ~30 min. Do this in a SEPARATE script executed AFTER stages 1-3 and record its wall-clock timestamp.
  S4.1. Build the lineage table: lineage_id, architecture_family, base repo, member repos, member roles in {base, instruct, safety_rl, abliterated, uncensored_finetune, other}, max #params, has_hard_case = (any member is abliterated or uncensored).
  S4.2. Deterministic rule, written verbatim into the artifact and reproducible: sort lineage_ids lexicographically; form strata as (architecture_family, has_hard_case, size_bucket); within each stratum order by sha256(lineage_id + '|' + SEED) hex; assign the first ceil(1/3) of each stratum to HELDOUT, rest to DEV; SEED = '20260813-iter2-split' (a fixed literal string, written into the artifact - do NOT use time or randomness that is not reproducible from the artifact alone). Then apply the family constraint: choose the two smallest-member-count architecture families whose lineages are not needed to keep DEV non-degenerate and force ALL their lineages to HELDOUT, so >=2 families are absent from DEV entirely; re-check the >=1/3 held-out floor after this forcing and, if it is violated, promote additional lineages by the same hash order until it holds. Log the forced families by name.
  S4.3. Emit a pre-registration statement row/file: ISO timestamp, the SEED, the rule text, the count of lineages on each side, the list of DEV-absent families, and the literal assertion that no metric definition from the 50-metric battery had been chosen when this split was written, plus the sha256 of the split file so any later edit is detectable. Note honestly if any lineage's membership was already known from iteration 1 exploration (the Qwen3-4B H0 lineage is explicitly an exploration lineage and should be forced to DEV, since metrics WILL be designed on it - putting it in HELDOUT would be self-deception; state this as a deliberate choice).

  STAGE 5 - THE DISQUALIFICATION RULE (machine-readable). ~15 min.
  Emit a rule row: rule_id='BLANKET_REFUSER_DISQUALIFICATION'; predicate = 'a candidate metric is DISQUALIFIED, regardless of its correlation with any safety target, if its top-ranked checkpoint has over-refusal above threshold on XSTest-safe items'; threshold expressed as full_refusal_rate_on_xstest_safe > 0.50 with partial_refusal counted as refusal, PLUS a secondary softer trip at > 0.35 that raises a WARN rather than a disqualification; the source of the over-refusal number in priority order (external row if one exists, else in-house measurement with the R4 evaluator system prompt); and the exact fields an iteration-3 script must read to evaluate it. Ground the threshold choice in a cited source if one supports it (XSTest paper arXiv:2308.01263 and OR-Bench report per-model full/partial refusal rates on safe items - fetch and cite the actual distribution rather than picking 0.50 out of the air; if the literature supports a different natural cut, USE it and say why). Also emit rule_id='QWEN3GUARD_CIRCULARITY': Qwen3Guard (any variant) must not be used as judge or ground-truth source for Qwen/Qwen3-4B-SafeRL, with the affected checkpoint ids listed.

  OUTPUT & VALIDATION. ~30 min.
  Single data_out.json with a top-level 'rows' array; each row has row_kind in {external_score, panel_checkpoint, lineage, split_assignment, coverage_stat, rule, prereg_statement} and the fields for that kind; per-row metadata_fold set to the lineage's split ('dev'/'heldout'/'na'). Validate with the aii-json skill against a schema you write and ship alongside. Emit full/mini/preview variants and check the file-size limit with aii-file-size-limit. Keep every raw snapshot (parquet, JSON, fetched READMEs) under a cache/ directory so the harvest is reproducible and every verbatim_snippet is re-checkable offline. Write a short README.md stating counts per row_kind, the coverage headline, and the split's freeze timestamp.

  FAILURE MODES AND WHAT TO DO.
  - HELM GCS layout differs from expectation -> probe, then fall back to the papers' own tables; never fabricate a path or a number.
  - SORRY-Bench / SALAD-Bench datasets are gated -> we do not need the prompts, only the published per-model results; take them from the papers and leaderboard pages.
  - Panel overlap with every safety leaderboard is ZERO -> that is a legitimate, reportable finding and the single most decision-relevant output of this artifact. Report it precisely (per source: n panel models present / n models the source evaluates) and hand iteration 3 the in-house measurement list. Do not substitute frontier-model rows for panel rows to make the table look full.
  - Two sources disagree on the same (checkpoint, benchmark, metric) -> keep BOTH rows, do not average, and set a disagreement flag with the delta; iteration 3 needs to see source variance.
  - Model card states a number without a scale or a grader -> keep it, set scale='UNSTATED' and judge_or_grader='UNSTATED', and lower its confidence flag; do not guess.
  - Time is running out -> Stages 4 and 5 (split + rules) are CHEAP and are the parts nothing downstream can proceed without, so if the harvest is overrunning, cut Stage 2.5 and the long tail of S2.3 sources, but NEVER cut the split or the coverage report.
target_num_datasets: 12
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_0UsKSgsMHome
type: research
title: Spec Sheets for Rival LLM Safety Metrics
summary: |-
  Reimplementation dossier for the four external baselines plus the estimator toolkit and a full citation audit. Deliverables: research_report.md (6 sections, ~1300 lines, every number carrying an [arXiv:ID section] anchor), research_out.json, and estimator_check.py/.json (deterministic Monte Carlo, seed 20260812).

  BASELINES, all read from primary full text. AMS (arXiv:2608.05578, venue confirmed IEEE Access 14:91723-91737): sigma = (mu+ - mu-)/sigma_pooled on the diff-in-means direction, final prompt token, 40-80% relative-depth sweep, 16 contrastive pairs x 3 concepts, 96 forward passes / 10-40s, thresholds PASS>3.5 / WARN 2.0-3.5 / CRIT<2.0. 71% = 10/14 leave-one-MODEL-out, identical under both calibration rules. r=-0.546 (p=0.043) verified; the unquoted Spearman rho=-0.423 is NOT significant. H4 quote transcribed verbatim with no hedge. THREE panel checkpoints appear in AMS Table I (Llama-3.2-3B-Instruct 8.37, gemma-2-2b-it 4.80, Llama-3.2-1B-Instruct 4.55) giving a reproduction gate. RAS/SafeVec (arXiv:2606.25750): all five stages plus EVERY published constant (tau=0.8, q=0.9, lambda=0.5, wu=wj=0.5, c=0.75, beta=5.0). VISAGE (arXiv:2405.17374): E[Smax-S] over alpha~U(-0.5,0.5), 3 dirs x 20 steps x Adv-80. Qi (arXiv:2406.05946 - ID resolved).

  DECISIONS SETTLED. (1) RAS overlap with our panel is EMPTY - every RAS-scored checkpoint is >=4B and none is ours; we must write 'our RAS reimplementation' throughout. (2) VISAGE at full fidelity is ~28 h/1B model on CPU (4,800 generations); a justified reduced grid lands at ~1.3 h/model, with an explicit fidelity-cost table. (3) Qi's operational decay length is k=5 tokens (beta_t=2 for t<=5, 0.1 for t>5), yielding pre-registered cut PR-1: Delta-lambda must survive beyond generated step 15, tested on [16,48], conservative replicate at 20. (4) NO prior work applies EWS/critical slowing down to LLM generative dynamics (arXiv abstract search returns zero) - but arXiv:2605.09043 applies CSD to conversation derailment in human dialogue and must be cited and distinguished, and AQI (arXiv:2506.13901) is a fifth uncited competitor.

  ESTIMATOR TOOLKIT with measured, not remembered, corrections. ewstools defaults read from source (Gaussian bandwidth 0.2, sigma=(0.25/0.675)*bw_num, rolling window 0.25, Kendall tau; NO built-in AC1 bias correction). Monte Carlo at our exact lengths: raw AC1 bias -0.064 at n=64 vs -0.020 at n=192, reduced to -0.009 / -0.0005 by +(1+3r)/n. A 192->64 effective-length difference alone manufactures a ~0.04 spurious AC1 gap in the 'right' direction - mitigation is mandatory and threefold. The AR(1)->lambda conversion is convex, so lambda is inflated 75% at n=64, phi=0.9; noise-floor truncation UNDER-estimates lambda by 40% if the fit window runs past the floor crossing. Runnable numpy/scipy recipe supplied with stopping rule, surrogate-ARMA null (Dakos Fig.11), and n_min=64 floor.

  OBSERVABLE. Yin et al. measure the probe refusal score at GENERATED positions (thinking chain), so r_t is adopted, not coined; verbatim 12-entry refusal-substring list transcribed from Arditi's source; per-tokenizer runtime resolution recipe for the leading-space hazard; abliteration-invariance argument grounded with its honest caveat.

  AUDIT. All 16 anchors resolve, none fabricated, no misattribution. Kwon's base-model control and Ratnakar's ~40%-depth figure both verified verbatim, so H1's and Step 0(a)'s rationales stand. The unanchored knowledge-action-gap result is FOUND: arXiv:2603.18353, 98.2% AUROC vs 45.1% sensitivity, 3,695 SAE features, both verbatim. Hasan & Biswas supply the missing r = -0.032, p = 0.89. Only two claims need rewriting (Qi 'Oral' unverifiable from arXiv; RAS speed-up internally inconsistent at 216.88x vs 210.13x). Recommends promoting SRI (arXiv:2602.02600) to a baseline - it is nearly free on hidden states we already extract.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Free-first web search (general + scholarly modes), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-concept-fig-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>
</available_resources>

<available_data_sources>
Use the sources appropriate to your task. Read the relevant skill file BEFORE using each source.

- **HuggingFace Hub** (HF) — ML datasets (NLP, vision, tabular, benchmarks)
- **Our World in Data** (OWID) — Global statistics (energy, health, economics, environment, demographics)
- **Alternate methods** — Python/shell (sklearn.datasets, openml, direct URL, APIs, etc.)

If the plan specifies a source or one fits better, use it.
You may combine sources. Use web search (aii-web-tools skill) to research candidates (background, papers, provenance) — NOT to find/download datasets.
</available_data_sources>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for dataset selection, evaluation metrics, agent orchestration patterns.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-python, aii-long-running-tasks, aii-json, aii-file-size-limit, aii-use-hardware, aii-parallel-computing.
TODO 2. Read skill files for your data sources (see <available_data_sources>) and domain handbook if applicable (see <available_domain_handbooks>). Based on plan and context, decide which source(s) to use. Include everything specified in the artifact plan, but you may also collect additional relevant data beyond what's listed. Run 50 diverse searches across chosen source(s) — BROAD, GENERAL terms, not very specific. Parallelize where supported.
TODO 3. Identify the 25 most promising datasets. IMPORTANT: Only consider datasets under 300MB. Preview/inspect sample rows for each candidate. Parallelize previews.
TODO 4. Research each candidate BEFORE choosing which to download. For each, search the web (aii-web-tools skill): dataset name, papers citing it, original source/task, popularity. Red flags: no search results, no papers, anonymized features (F1, F2...), <100 downloads, no documentation. Green flags: papers using it, clear documentation, meaningful features, established benchmark. Also consider: will features/structure allow meaningful evaluation of the planned method?
TODO 5. Decide which to KEEP vs DISCARD. Look for: clear structure, relevant fields, quality examples matching requirements, confirmed provenance. Determine which 15 datasets have the most suitable data. Download and save to `temp/datasets/`. Parallelize downloads.
</todos>
```

### [2] HUMAN-USER prompt · 2026-08-13 16:23:06 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [3] SKILL-INPUT — aii-python · 2026-08-13 16:23:52 UTC

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

### [4] SKILL-INPUT — aii-json · 2026-08-13 16:23:52 UTC

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

### [5] SKILL-INPUT — aii-file-size-limit · 2026-08-13 16:23:54 UTC

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

### [6] SKILL-INPUT — aii-hf-datasets · 2026-08-13 16:24:02 UTC

The agent loaded the **aii-hf-datasets** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-hf-datasets
description: Searches, previews, and downloads datasets from HuggingFace Hub. Use when user needs machine learning datasets, training data, HuggingFace datasets, dataset discovery, or .parquet/.json exports.
---

## Contents

- Workflow (3-phase dataset discovery)
- Scripts (Search, Preview, Download)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Workflow: 3-Phase Dataset Discovery

### Phase 1: Search for Datasets
Find datasets with metadata (configs, splits, features, sizes)
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_hf_search_datasets.py --query "sentiment analysis" --limit 5
```

### Phase 2: Preview Dataset (if promising)
Inspect metadata AND sample rows in one call
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_hf_preview_datasets.py openai/gsm8k
```

### Phase 3: Download Dataset (if suitable)
Download after reviewing the preview
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_hf_download_datasets.py openai/gsm8k --config main --split train
```

---

## Scripts

### Search HuggingFace Datasets (aii_hf_search_datasets.py)

Search and discover datasets on HuggingFace Hub.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_hf_search_datasets.py --query "text classification" --limit 5
```

**Parallel execution (multiple queries):**

IMPORTANT: Use full python path with GNU parallel (venv activate does NOT work in parallel subshells):
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_hf_search_datasets.py" && \
parallel -j 10 -k --group --will-cite '$PY $S --query {} --limit 3' ::: 'sentiment' 'classification' 'translation'
```

**Example output:**
```
Found 5 dataset(s) for query='text classification'

============================================================
Dataset 1: stanfordnlp/imdb
Downloads: 2,500,000 | Likes: 1,234
Description: Large Movie Review Dataset for binary sentiment classification...
Tags: text-classification, en, sentiment-analysis
```

**Result fields per dataset:**

Each entry in ``results`` carries:

- ``id`` / ``downloads`` / ``likes`` / ``tags`` / ``description`` — standard
  HF metadata
- ``has_loader_script`` (bool) — repo ships a top-level ``<repo>.py`` loader.
  ``datasets>=3`` won't run these directly; the dataset is reachable only
  via the Datasets Server's pre-converted parquet shards. Treat as a yellow
  flag.
- ``loadable`` (bool) — **prefer datasets where this is ``True``.** Means
  the dataset is reachable via *some* path: either native parquet (no
  script) or HF auto-converted the script's output to parquet. When
  ``False``, the script needs deps HF can't install (e.g. ``conllu``,
  custom audio decoders) and ``aii_hf_datasets__download_datasets`` will
  fail — pick a different candidate.

**Parameters:**

`--query` (optional)
- Search query string
- Example: `--query "sentiment analysis"`

`--limit` (optional)
- Maximum number of results (default: 5)

`--tags` (optional)
- Filter by tags (comma-separated)
- Format: `category:value`
- Examples: `language:en`, `task_categories:text-classification`

`--sort` (optional)
- Sort by field: `downloads`, `likes` (default: downloads)

**Tips:**
- Search displays full dataset metadata
- Use tags to filter: `--tags "language:en,task_categories:translation"`

---

### Preview HuggingFace Dataset (aii_hf_preview_datasets.py)

Inspect a specific dataset - shows metadata AND sample rows.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_hf_preview_datasets.py openai/gsm8k --num-rows 5
```

**Parallel execution (multiple datasets):**

IMPORTANT: Use full python path with GNU parallel:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_hf_preview_datasets.py" && \
parallel -j 10 -k --group --will-cite '$PY $S {} --num-rows 3' ::: 'openai/gsm8k' 'imdb' 'squad'
```

**Example output:**
```
============================================================
Dataset: openai/gsm8k
============================================================
Downloads: 425,109 | Likes: 1,102

Description: GSM8K (Grade School Math 8K) is a dataset of 8.5K high quality
linguistically diverse grade school math word problems...

Configs: main, socratic

--- Sample Rows (train) ---
Columns: question, answer

Row 1:
  question: Natalia sold clips to 48 of her friends in April...
  answer: Natalia sold 48/2 = <<48/2=24>>24 clips in May...
```

**Parameters:**

`dataset_id` (required, positional)
- HuggingFace dataset ID
- Examples: `openai/gsm8k`, `glue`, `imdb`

`--config` (optional)
- Dataset configuration/subset name
- Auto-detects first config if not specified

`--split` (optional)
- Split to preview (default: `train`)

`--num-rows` (optional)
- Number of sample rows (default: 5, max: 20)

**Tips:**
- Use after search to verify data structure
- Streaming mode - doesn't download full dataset

---

### Download HuggingFace Dataset (aii_hf_download_datasets.py)

Download datasets and save to files.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_hf_download_datasets.py openai/gsm8k --config main --split train
```

**Parallel execution (multiple datasets):**

IMPORTANT: Use full python path with GNU parallel. Use `eval {}` pattern when datasets need different flags (e.g. `--config`):
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-hf-datasets" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_hf_download_datasets.py" && \
parallel -j 10 -k --group --will-cite 'eval {}' ::: '$PY $S openai/gsm8k --config main --split train' '$PY $S imdb --split train' '$PY $S squad --split train'
```

**Example output:**
```
Downloaded: openai/gsm8k

  train:
    Rows: 7,473
    Preview: temp/datasets/preview_openai_gsm8k_main_train.json
    Mini: temp/datasets/mini_openai_gsm8k_main_train.json
    Full: temp/datasets/full_openai_gsm8k_main_train.json
```

**Parameters:**

`dataset_id` (required, positional)
- HuggingFace dataset ID
- Examples: `openai/gsm8k`, `imdb`

`--config` (optional)
- Dataset configuration/subset name
- Use preview to see available configs

`--split` (optional)
- Specific split to load (e.g., `train`, `test`)
- If not specified, loads all splits

`--output-dir` (optional)
- Output directory (default: `temp/datasets/`)

**Output files (auto-saved):**
1. **Preview**: `preview_{dataset}_{split}.json` - 3 truncated rows - **READ THIS** for quick inspection
2. **Mini**: `mini_{dataset}_{split}.json` - 3 full rows - for development/testing
3. **Full**: `full_{dataset}_{split}.json` - All rows - **DO NOT READ directly** - use as input path for code

**Tips:**
- Only read preview file directly with Read tool
- Mini and full are input paths for processing code

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [7] SKILL-INPUT — aii-web-tools · 2026-08-13 16:33:18 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Web research toolkit: free-first web search (general or scholarly, Serper fallback), web page fetch as markdown (HTML and PDF), and regex grep over full page/PDF text. Use whenever a task needs to search the web, read a page, mine a paper/PDF, verify citations, or extract exact quotes, numbers, or methodology from a URL."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — free-first web search (keyless general/scholarly engines,
   Serper fallback), html2text + PyMuPDF for fetch, and regex grep over the full
   document text. They work without any built-in web tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (free-first: general or scholarly)

```bash
# general web (default): keyless engines (ddgs, marginalia); Serper only if they miss
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
# scholarly mode: OpenAlex + Crossref (DOIs, citation counts)
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation" --mode scholarly
```

Returns ranked title / URL / snippet lines. `--mode general` (default) uses
keyless general engines; `--mode scholarly` uses academic APIs. Both fall back
to Serper (paid) only when the free engines miss. Use search first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````

### [8] SYSTEM-USER prompt · 2026-08-13 16:53:53 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_dataset_1_idx2
type: dataset
title: Published safety scores and a frozen split
summary: >-
  Build the EXTERNAL ground-truth table that replaces our own judge as the correlation target for iteration 2's 50-metric
  screen, plus a frozen, seeded dev/held-out split over weight lineages written BEFORE any metric exists. Deliverable is one
  schema-validated row set with three row kinds: (A) external_score rows, one per (checkpoint, benchmark, metric), each carrying
  raw value, scale, explicit polarity (higher-is-safer vs lower-is-safer), exact source URL, source type, retrieval date,
  and a revision-match confidence flag; (B) split_assignment rows, one per weight lineage, from a deterministic seeded stratified
  rule with the rule text and a timestamped pre-registration statement embedded in the artifact; (C) rule rows encoding the
  machine-readable blanket-refuser disqualification and the Qwen3Guard/Qwen3-4B-SafeRL circularity flag. Coverage is a first-class
  output, reported numerically and honestly: the likely finding at <=4.2B is that published SAFETY numbers are sparse while
  CAPABILITY numbers are dense, and that asymmetry is exactly what iteration 3's analysis plan has to be built around, so
  it must be measured rather than assumed. Highest-yield programmatic sources: open-llm-leaderboard/contents on HF (4,580
  rows, columns include Model, Model sha, #Params (B), Architecture, Precision, Chat Template, and raw+normalised IFEval/BBH/MATH
  Lvl 5/GPQA/MUSR/MMLU-PRO), the HELM public GCS mirror for HELM Safety v1.0 and AIR-Bench 2024, and the HF Hub API + model-card
  READMEs for card-stated safety numbers.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  SCOPE. The unit of the primary table is a (checkpoint, benchmark, metric) triple. Checkpoints come from iteration 1's frozen panel manifest (137 checkpoints / 93 lineages), restricted to <=4.2B parameters. Ideal is EVERY published quantitative score that exists for those checkpoints, on two axes.

  AXIS 1 - SAFETY (the axis the hypothesis needs and the one likely to be thin): TrustLLM, AIR-Bench 2024 (HELM), HELM Safety v1.0 (5 benchmarks x 6 risk categories: violence, fraud, discrimination, sexual content, harassment, deception), SALAD-Bench, SORRY-Bench, DecodingTrust, JailbreakBench / HarmBench ASR tables, XSTest and OR-Bench over-refusal rates, ToxiGen/RealToxicityPrompts, BeaverTails, plus any refusal rate, safety rate, ASR, or guard-model score stated on the model card itself or in the family's tech report (Qwen3, Llama 3.2, Gemma 2, SmolLM2, OLMo, Granite 3.1, Falcon3, MiniCPM, Pythia, TinyLlama, Danube3 all have tech reports or detailed cards). BOTH sides of safety must be representable: harm-refusal AND over-refusal. A row set that only has harm-refusal numbers permits the degenerate blanket-refuser winner the hypothesis explicitly disqualifies, so over-refusal coverage must be reported separately in the coverage summary, not folded into a single 'safety coverage' count.

  AXIS 2 - CAPABILITY (dense, cheap, and needed as a confound control): GSM8K, MMLU, MMLU-PRO, ARC, HellaSwag, IFEval, BBH, GPQA, MUSR, MATH Lvl 5, Arena-Hard, TruthfulQA, Winogrande. The Open LLM Leaderboard v2 contents dataset (open-llm-leaderboard/contents on HF, ~4,580 rows, parquet, loadable via load_dataset) is the highest-coverage single source for small models and MUST be pulled programmatically, never hand-transcribed. Its 'Model sha' column is what makes revision-level matching possible at all and must be carried into our rows.

  PER-ROW REQUIREMENTS (all mandatory, no nulls-by-laziness):
    checkpoint_id (HF repo id, exactly as in the panel manifest), lineage_id, revision_sha_source (the sha the SOURCE evaluated, if stated), revision_sha_panel (the sha our manifest pins), revision_match in {EXACT, SAME_REPO_UNKNOWN_SHA, SIBLING, FAMILY_ONLY}, benchmark, metric_name, value (float), scale (e.g. '0-100 percent', '0-1 rate', 'raw score 0-90'), polarity in {HIGHER_IS_SAFER, LOWER_IS_SAFER, HIGHER_IS_MORE_CAPABLE, NOT_ORDERED} stated EXPLICITLY per row and never inferred downstream from the benchmark name, axis in {SAFETY_HARM, SAFETY_OVERREFUSAL, SAFETY_OTHER, CAPABILITY}, source_url (exact, deep-linked, not a homepage), source_type in {OFFICIAL_MODEL_CARD, TECH_REPORT, PEER_REVIEWED_PAPER, ARXIV_PREPRINT, LEADERBOARD_SNAPSHOT, THIRD_PARTY_REPO}, source_version_or_release (e.g. HELM release v1.1.0, leaderboard snapshot date), retrieval_date (ISO), judge_or_grader (what scored it: GPT-4 judge, Llama Guard, string match, human - unknown is allowed but must be the literal string 'UNSTATED'), circularity_flag (string, empty or e.g. 'QWEN3GUARD_REWARD_CIRCULAR'), and verbatim_snippet (<=300 chars of the source text the number was read from, so the row is auditable without re-fetching).

  POLARITY IS LOAD-BEARING. ASR (attack success rate) is LOWER_IS_SAFER; refusal rate on harmful prompts is HIGHER_IS_SAFER; XSTest full-refusal rate on SAFE items is LOWER_IS_SAFER (a high value is over-refusal, i.e. WORSE); AIR-Bench and HELM safety scores are HIGHER_IS_SAFER. Getting one of these backwards silently flips a Spearman sign in iteration 3, so polarity must be set from the source's own wording and the wording quoted in verbatim_snippet.

  SPLIT REQUIREMENTS. One split_assignment row per weight lineage, covering ALL 93 lineages in the manifest, not just the ones measured this iteration. Held-out >= 1/3 of lineages. Stratified by (architecture_family, has_abliterated_or_uncensored_member, size_bucket) so both sides carry the hard cases. At least two architecture families must appear ONLY in held-out, so leave-one-family-out is possible. Assignment produced by a deterministic seeded rule (fixed seed, sorted lineage ids, documented hash) that is written verbatim into the artifact and reproducible by re-running the emitted rule text.

  SIZE / FORMAT. Well under 300MB - the whole thing is a few thousand JSON rows plus the raw source snapshots. Cache raw pulls (parquet/JSON) to disk so the harvest is auditable and re-runnable offline. Ship full/mini/preview variants per the aii-json skill.

  WHAT WOULD MAKE THIS ARTIFACT FAIL: silent fabrication of a plausible-looking benchmark number (fatal - every value must trace to a fetched URL and a quoted snippet); collapsing SIBLING-revision rows into EXACT rows; a split that leaks an abliterated member's parent across the boundary; or reporting 'good coverage' without the family/scale skew breakdown.
dataset_search_plan: |-
  PRE-FLIGHT (do first, ~30 min).
  P1. LOCATE THE PANEL MANIFEST. Iteration 1's frozen 137-checkpoint / 93-lineage manifest, prompt corpus, and 10-tokenizer-family refusal lexicons live in the previous run's workspaces. Glob for them under /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/ (try iter_1/gen_art/*/data_out.json, *manifest*.json, *panel*.json) and also under /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/ and the user_uploads folder. Log exactly which file you used and its row count.
    FALLBACK IF THE MANIFEST IS NOT FOUND (plan for this - it is the single most likely blocker): rebuild an equivalent panel deterministically from the HF Hub API (huggingface_hub.HfApi().list_models) using the lineage list enumerated in the hypothesis - Qwen3-0.6B/1.7B/4B (base + instruct + SafeRL + abliterated), Qwen2.5-0.5B/1.5B, Llama-3.2-1B/3B, gemma-2-2b, SmolLM2-360M/1.7B, TinyLlama-1.1B, Pythia-410M/1B/1.4B, OLMo-1B, Danube3-500M, Falcon3-1B-Instruct, Granite-3.1-2B-Instruct, MiniCPM-1B - plus abliterated/uncensored derivatives found by searching HF for 'abliterated', 'uncensored', 'ortho' filtered to those base architectures and <=4.2B. Pin every repo's current commit sha via HfApi().model_info(repo, revision='main').sha. Emit the rebuilt manifest as a deliverable row kind so iteration 3 is not blocked either way, and state loudly in the artifact that it is a REBUILD, not the iteration-1 frozen manifest.
  P2. Resolve every checkpoint's #params and architecture from HF config.json / model_info so the <=4.2B filter and the size-bucket stratification are grounded, not guessed.

  STAGE 1 - CAPABILITY HARVEST (cheap, dense, do it first so you have a working pipeline before the hard axis). ~45 min.
  S1.1. load_dataset('open-llm-leaderboard/contents') -> pandas. Columns to keep: eval_name, Model, fullname, 'Model sha', 'Base Model', Architecture, 'Weight type', '#Params (B)', Precision, Type, MoE, 'Chat Template', Average, IFEval, BBH, 'MATH Lvl 5', GPQA, MUSR, 'MMLU-PRO' (raw AND normalised where both exist), Flagged, 'Submission Date'. Join to the panel on normalised repo id (lowercase, strip whitespace); set revision_match=EXACT when 'Model sha' equals the panel sha, SAME_REPO_UNKNOWN_SHA otherwise. Emit one row per (checkpoint, benchmark). DROP rows where Flagged is true, but RECORD them in a separate flagged list rather than deleting silently.
  S1.2. Also pull open-llm-leaderboard/results (per-model raw result files) for any panel checkpoint missing from contents; and try the archived v1 datasets (HuggingFaceH4/open-llm-leaderboard-evaluations-results, open-llm-leaderboard-old/results) for older small models (Pythia, TinyLlama, OLMo, Danube3) which predate v2 and may only exist in v1. Record which leaderboard VERSION each row came from - v1 and v2 scores are NOT comparable and mixing them without a version column is a real error.
  S1.3. GSM8K / MMLU / ARC / HellaSwag / Arena-Hard where the leaderboards do not carry them: read the family tech report / model card table. Qwen3, Llama-3.2, Gemma-2, SmolLM2, Granite-3.1, Falcon3, MiniCPM and OLMo all publish per-size benchmark tables in their cards or reports.

  STAGE 2 - SAFETY HARVEST (the hard, high-value axis). ~2.5 h. Work source-by-source, each with a cached raw snapshot.
  S2.1. HELM (two leaderboards, one mechanism). HELM Safety v1.0 (crfm.stanford.edu/helm/safety/) and AIR-Bench 2024 (crfm.stanford.edu/helm/air-bench/v1.1.0/). The site is a static front-end over JSON on a public GCS bucket: https://storage.googleapis.com/crfm-helm-public/<project>/benchmark_output/releases/<release>/... with per-group JSON (groups/*.json, schema.json, runs_to_run_suites.json). PROBE the exact paths with HTTP GET before writing the parser - do not assume the layout; if the bucket paths 404, fall back to (a) the JSON the leaderboard page itself requests (read the page source / network paths), (b) the stanford-crfm/helm GitHub repo's documented download instructions, (c) the AIR-Bench paper's own results table (arXiv:2407.17436, openreview UVnD9Ze6mF) transcribed with verbatim_snippet. EXPECT LOW PANEL OVERLAP: HELM evaluates ~21-24 mostly frontier models, so most or all of our <=4.2B panel will be absent. That absence is a RESULT - record it as a coverage number, do not pad it.
  S2.2. TrustLLM (trustllmbenchmark.github.io + arXiv:2401.05561): pull the leaderboard tables and the paper's per-model results. Again expect frontier-model skew; harvest whatever small models appear (Vicuna/Llama-2 7B class at best) and record overlap honestly.
  S2.3. SALAD-Bench (OpenSafetyLab, arXiv:2402.05044, HF: OpenSafetyLab/Salad-Data and the leaderboard space), SORRY-Bench (ICLR 2025, github.com/SORRY-Bench/sorry-bench, HF: sorry-bench/sorry-bench-202406 - note the main dataset is GATED, but the PAPER's model results table is not and is the thing we actually need), DecodingTrust (decodingtrust.github.io, per-perspective scores), JailbreakBench (jailbreakbench.github.io leaderboard - ASR per model per attack), HarmBench (harmbench.org results table), OR-Bench (HF: bench-llm/or-bench + its leaderboard space, over-refusal rates), XSTest (arXiv:2308.01263 and any paper reporting XSTest per model - Hasan & Biswas arXiv:2605.05427 audits 21 open-weight LLMs on over-refusal AND harmful compliance and is a prime harvest target for BOTH safety sub-axes).
  S2.4. MODEL CARDS AND TECH REPORTS - likely the single richest safety source at our scale. For every panel checkpoint, fetch https://huggingface.co/<repo>/raw/main/README.md via the Hub API and regex-scan for safety numbers: /(safety|refus|harmful|toxic|jailbreak|ASR|attack success|over-refus|WildGuard|Guard)/i near a numeric. Qwen3-4B-SafeRL's card is the flagship case - it documents RL against a Qwen3Guard-Gen-4B safety reward plus a WorldPM-Helpsteer2 helpfulness reward and reports safety/helpfulness numbers; harvest every number it states AND set circularity_flag='QWEN3GUARD_REWARD_CIRCULAR' on any row whose judge_or_grader is a Qwen3Guard variant, because the hypothesis forbids using it as ground truth for that model. Also fetch the Qwen3 tech report, Llama-3.2 card, Gemma-2 card (which reports safety/ToxiGen/RealToxicity numbers), SmolLM2 paper, OLMo paper, Granite-3.1 card, and the abliterated-model cards (which often state a residual refusal rate - harvest it and mark source_type=THIRD_PARTY_REPO, low trust).
  S2.5. LAST-RESORT SWEEP for anything missed: scholarly search per checkpoint name + 'safety' / 'refusal rate' / 'jailbreak' restricted to 2024-2026, and fetch_grep the resulting PDFs for the model name to pull table values with context. Cap this at ~20 min per family so it cannot eat the budget.

  STAGE 3 - THE COVERAGE REPORT (a required deliverable, not a footnote). ~20 min.
  Compute and emit, as structured rows and as a human-readable markdown summary: n_checkpoints in panel at <=4.2B; n with >=1 SAFETY_HARM row; n with >=1 SAFETY_OVERREFUSAL row; n with >=1 CAPABILITY row; n with EXACT revision match vs SAME_REPO_UNKNOWN_SHA vs SIBLING; the same counts broken down by architecture family and by size bucket (<1B, 1-2B, 2-4.2B); and the count of lineages where at least one MEMBER has a safety number (lineage-level coverage differs from checkpoint-level coverage and iteration 3 bootstraps over lineages, so both are needed). Then emit an explicit list, machine-readable, of checkpoints that will REQUIRE in-house measurement because no external safety number exists - this list is the direct input to iteration 3's measurement budget. If safety coverage is below ~20% of the panel (the likely outcome), state that numerically and state plainly that the external-ground-truth axis of H3 is coverage-limited at this scale and that the hypothesis's documented fallback (two in-house refusal rates: harmful-prompt refusal and XSTest-style harmless-but-alarming refusal, with the R4 evaluator-system-prompt fix in force) becomes primary for the uncovered checkpoints. Do NOT run those in-house measurements here - that is an experiment artifact; just name the checkpoints and the axes needed.

  STAGE 4 - THE FROZEN SPLIT. ~30 min. Do this in a SEPARATE script executed AFTER stages 1-3 and record its wall-clock timestamp.
  S4.1. Build the lineage table: lineage_id, architecture_family, base repo, member repos, member roles in {base, instruct, safety_rl, abliterated, uncensored_finetune, other}, max #params, has_hard_case = (any member is abliterated or uncensored).
  S4.2. Deterministic rule, written verbatim into the artifact and reproducible: sort lineage_ids lexicographically; form strata as (architecture_family, has_hard_case, size_bucket); within each stratum order by sha256(lineage_id + '|' + SEED) hex; assign the first ceil(1/3) of each stratum to HELDOUT, rest to DEV; SEED = '20260813-iter2-split' (a fixed literal string, written into the artifact - do NOT use time or randomness that is not reproducible from the artifact alone). Then apply the family constraint: choose the two smallest-member-count architecture families whose lineages are not needed to keep DEV non-degenerate and force ALL their lineages to HELDOUT, so >=2 families are absent from DEV entirely; re-check the >=1/3 held-out floor after this forcing and, if it is violated, promote additional lineages by the same hash order until it holds. Log the forced families by name.
  S4.3. Emit a pre-registration statement row/file: ISO timestamp, the SEED, the rule text, the count of lineages on each side, the list of DEV-absent families, and the literal assertion that no metric definition from the 50-metric battery had been chosen when this split was written, plus the sha256 of the split file so any later edit is detectable. Note honestly if any lineage's membership was already known from iteration 1 exploration (the Qwen3-4B H0 lineage is explicitly an exploration lineage and should be forced to DEV, since metrics WILL be designed on it - putting it in HELDOUT would be self-deception; state this as a deliberate choice).

  STAGE 5 - THE DISQUALIFICATION RULE (machine-readable). ~15 min.
  Emit a rule row: rule_id='BLANKET_REFUSER_DISQUALIFICATION'; predicate = 'a candidate metric is DISQUALIFIED, regardless of its correlation with any safety target, if its top-ranked checkpoint has over-refusal above threshold on XSTest-safe items'; threshold expressed as full_refusal_rate_on_xstest_safe > 0.50 with partial_refusal counted as refusal, PLUS a secondary softer trip at > 0.35 that raises a WARN rather than a disqualification; the source of the over-refusal number in priority order (external row if one exists, else in-house measurement with the R4 evaluator system prompt); and the exact fields an iteration-3 script must read to evaluate it. Ground the threshold choice in a cited source if one supports it (XSTest paper arXiv:2308.01263 and OR-Bench report per-model full/partial refusal rates on safe items - fetch and cite the actual distribution rather than picking 0.50 out of the air; if the literature supports a different natural cut, USE it and say why). Also emit rule_id='QWEN3GUARD_CIRCULARITY': Qwen3Guard (any variant) must not be used as judge or ground-truth source for Qwen/Qwen3-4B-SafeRL, with the affected checkpoint ids listed.

  OUTPUT & VALIDATION. ~30 min.
  Single data_out.json with a top-level 'rows' array; each row has row_kind in {external_score, panel_checkpoint, lineage, split_assignment, coverage_stat, rule, prereg_statement} and the fields for that kind; per-row metadata_fold set to the lineage's split ('dev'/'heldout'/'na'). Validate with the aii-json skill against a schema you write and ship alongside. Emit full/mini/preview variants and check the file-size limit with aii-file-size-limit. Keep every raw snapshot (parquet, JSON, fetched READMEs) under a cache/ directory so the harvest is reproducible and every verbatim_snippet is re-checkable offline. Write a short README.md stating counts per row_kind, the coverage headline, and the split's freeze timestamp.

  FAILURE MODES AND WHAT TO DO.
  - HELM GCS layout differs from expectation -> probe, then fall back to the papers' own tables; never fabricate a path or a number.
  - SORRY-Bench / SALAD-Bench datasets are gated -> we do not need the prompts, only the published per-model results; take them from the papers and leaderboard pages.
  - Panel overlap with every safety leaderboard is ZERO -> that is a legitimate, reportable finding and the single most decision-relevant output of this artifact. Report it precisely (per source: n panel models present / n models the source evaluates) and hand iteration 3 the in-house measurement list. Do not substitute frontier-model rows for panel rows to make the table look full.
  - Two sources disagree on the same (checkpoint, benchmark, metric) -> keep BOTH rows, do not average, and set a disagreement flag with the delta; iteration 3 needs to see source variance.
  - Model card states a number without a scale or a grader -> keep it, set scale='UNSTATED' and judge_or_grader='UNSTATED', and lower its confidence flag; do not guess.
  - Time is running out -> Stages 4 and 5 (split + rules) are CHEAP and are the parts nothing downstream can proceed without, so if the harvest is overrunning, cut Stage 2.5 and the long tail of S2.3 sources, but NEVER cut the split or the coverage report.
target_num_datasets: 12
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_0UsKSgsMHome
type: research
title: Spec Sheets for Rival LLM Safety Metrics
summary: |-
  Reimplementation dossier for the four external baselines plus the estimator toolkit and a full citation audit. Deliverables: research_report.md (6 sections, ~1300 lines, every number carrying an [arXiv:ID section] anchor), research_out.json, and estimator_check.py/.json (deterministic Monte Carlo, seed 20260812).

  BASELINES, all read from primary full text. AMS (arXiv:2608.05578, venue confirmed IEEE Access 14:91723-91737): sigma = (mu+ - mu-)/sigma_pooled on the diff-in-means direction, final prompt token, 40-80% relative-depth sweep, 16 contrastive pairs x 3 concepts, 96 forward passes / 10-40s, thresholds PASS>3.5 / WARN 2.0-3.5 / CRIT<2.0. 71% = 10/14 leave-one-MODEL-out, identical under both calibration rules. r=-0.546 (p=0.043) verified; the unquoted Spearman rho=-0.423 is NOT significant. H4 quote transcribed verbatim with no hedge. THREE panel checkpoints appear in AMS Table I (Llama-3.2-3B-Instruct 8.37, gemma-2-2b-it 4.80, Llama-3.2-1B-Instruct 4.55) giving a reproduction gate. RAS/SafeVec (arXiv:2606.25750): all five stages plus EVERY published constant (tau=0.8, q=0.9, lambda=0.5, wu=wj=0.5, c=0.75, beta=5.0). VISAGE (arXiv:2405.17374): E[Smax-S] over alpha~U(-0.5,0.5), 3 dirs x 20 steps x Adv-80. Qi (arXiv:2406.05946 - ID resolved).

  DECISIONS SETTLED. (1) RAS overlap with our panel is EMPTY - every RAS-scored checkpoint is >=4B and none is ours; we must write 'our RAS reimplementation' throughout. (2) VISAGE at full fidelity is ~28 h/1B model on CPU (4,800 generations); a justified reduced grid lands at ~1.3 h/model, with an explicit fidelity-cost table. (3) Qi's operational decay length is k=5 tokens (beta_t=2 for t<=5, 0.1 for t>5), yielding pre-registered cut PR-1: Delta-lambda must survive beyond generated step 15, tested on [16,48], conservative replicate at 20. (4) NO prior work applies EWS/critical slowing down to LLM generative dynamics (arXiv abstract search returns zero) - but arXiv:2605.09043 applies CSD to conversation derailment in human dialogue and must be cited and distinguished, and AQI (arXiv:2506.13901) is a fifth uncited competitor.

  ESTIMATOR TOOLKIT with measured, not remembered, corrections. ewstools defaults read from source (Gaussian bandwidth 0.2, sigma=(0.25/0.675)*bw_num, rolling window 0.25, Kendall tau; NO built-in AC1 bias correction). Monte Carlo at our exact lengths: raw AC1 bias -0.064 at n=64 vs -0.020 at n=192, reduced to -0.009 / -0.0005 by +(1+3r)/n. A 192->64 effective-length difference alone manufactures a ~0.04 spurious AC1 gap in the 'right' direction - mitigation is mandatory and threefold. The AR(1)->lambda conversion is convex, so lambda is inflated 75% at n=64, phi=0.9; noise-floor truncation UNDER-estimates lambda by 40% if the fit window runs past the floor crossing. Runnable numpy/scipy recipe supplied with stopping rule, surrogate-ARMA null (Dakos Fig.11), and n_min=64 floor.

  OBSERVABLE. Yin et al. measure the probe refusal score at GENERATED positions (thinking chain), so r_t is adopted, not coined; verbatim 12-entry refusal-substring list transcribed from Arditi's source; per-tokenizer runtime resolution recipe for the leading-space hazard; abliteration-invariance argument grounded with its honest caveat.

  AUDIT. All 16 anchors resolve, none fabricated, no misattribution. Kwon's base-model control and Ratnakar's ~40%-depth figure both verified verbatim, so H1's and Step 0(a)'s rationales stand. The unanchored knowledge-action-gap result is FOUND: arXiv:2603.18353, 98.2% AUROC vs 45.1% sensitivity, 3,695 SAE features, both verbatim. Hasan & Biswas supply the missing r = -0.032, p = 0.89. Only two claims need rewriting (Qi 'Oral' unverifiable from arXiv; RAS speed-up internally inconsistent at 216.88x vs 210.13x). Recommends promoting SRI (arXiv:2602.02600) to a baseline - it is nearly free on hidden states we already extract.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Free-first web search (general + scholarly modes), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-concept-fig-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>
</available_resources>

<available_data_sources>
Use the sources appropriate to your task. Read the relevant skill file BEFORE using each source.

- **HuggingFace Hub** (HF) — ML datasets (NLP, vision, tabular, benchmarks)
- **Our World in Data** (OWID) — Global statistics (energy, health, economics, environment, demographics)
- **Alternate methods** — Python/shell (sklearn.datasets, openml, direct URL, APIs, etc.)

If the plan specifies a source or one fits better, use it.
You may combine sources. Use web search (aii-web-tools skill) to research candidates (background, papers, provenance) — NOT to find/download datasets.
</available_data_sources>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for dataset selection, evaluation metrics, agent orchestration patterns.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. For the top 15 datasets, create data.py (uv inline script) that: loads from temp/datasets/, standardizes to exp_sel_data_out.json schema (aii-json skill), extracts all examples per dataset, handles domain requirements, saves to full_data_out.json.

Each data ROW must be a separate example — do NOT create one example per dataset or per fold. Each data point (row, sample, instance) = one example. 500 rows → 500 examples. The output is GROUPED BY DATASET:
```json
{
  "datasets": [
    {
      "dataset": "iris",
      "examples": [
        {"input": "...", "output": "...", "metadata_fold": 2, "metadata_feature_names": [...]},
        ...
      ]
    },
    {
      "dataset": "adult_census",
      "examples": [...]
    }
  ]
}
```
Per-example required fields:
- `input`: input features/text (tabular: JSON string of feature values)
- `output`: target/label (as string)
Per-example optional metadata via `metadata_<name>` fields (flat, not nested object):
- `metadata_fold`: fold assignment (int), `metadata_feature_names`: feature name list, `metadata_task_type`: "classification"/"regression", `metadata_n_classes`: number of classes, `metadata_row_index`: original row index, etc.
Do NOT use `split`, `dataset`, or `context` as per-example fields. Dataset name goes at the group level, metadata goes in `metadata_*` fields.
TODO 2. Run 'uv run data.py' and fix errors. Validate full_data_out.json against exp_sel_data_out.json schema (aii-json skill) — fix errors. Generate preview, mini, full versions with aii-json skill's format script.
TODO 3. Read preview to inspect examples. Choose THE BEST 10 DATASETS based on domain requirements and artifact objective. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
````

### [9] SYSTEM-USER prompt · 2026-08-13 17:02:59 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_dataset_1_idx2
type: dataset
title: Published safety scores and a frozen split
summary: >-
  Build the EXTERNAL ground-truth table that replaces our own judge as the correlation target for iteration 2's 50-metric
  screen, plus a frozen, seeded dev/held-out split over weight lineages written BEFORE any metric exists. Deliverable is one
  schema-validated row set with three row kinds: (A) external_score rows, one per (checkpoint, benchmark, metric), each carrying
  raw value, scale, explicit polarity (higher-is-safer vs lower-is-safer), exact source URL, source type, retrieval date,
  and a revision-match confidence flag; (B) split_assignment rows, one per weight lineage, from a deterministic seeded stratified
  rule with the rule text and a timestamped pre-registration statement embedded in the artifact; (C) rule rows encoding the
  machine-readable blanket-refuser disqualification and the Qwen3Guard/Qwen3-4B-SafeRL circularity flag. Coverage is a first-class
  output, reported numerically and honestly: the likely finding at <=4.2B is that published SAFETY numbers are sparse while
  CAPABILITY numbers are dense, and that asymmetry is exactly what iteration 3's analysis plan has to be built around, so
  it must be measured rather than assumed. Highest-yield programmatic sources: open-llm-leaderboard/contents on HF (4,580
  rows, columns include Model, Model sha, #Params (B), Architecture, Precision, Chat Template, and raw+normalised IFEval/BBH/MATH
  Lvl 5/GPQA/MUSR/MMLU-PRO), the HELM public GCS mirror for HELM Safety v1.0 and AIR-Bench 2024, and the HF Hub API + model-card
  READMEs for card-stated safety numbers.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: |-
  SCOPE. The unit of the primary table is a (checkpoint, benchmark, metric) triple. Checkpoints come from iteration 1's frozen panel manifest (137 checkpoints / 93 lineages), restricted to <=4.2B parameters. Ideal is EVERY published quantitative score that exists for those checkpoints, on two axes.

  AXIS 1 - SAFETY (the axis the hypothesis needs and the one likely to be thin): TrustLLM, AIR-Bench 2024 (HELM), HELM Safety v1.0 (5 benchmarks x 6 risk categories: violence, fraud, discrimination, sexual content, harassment, deception), SALAD-Bench, SORRY-Bench, DecodingTrust, JailbreakBench / HarmBench ASR tables, XSTest and OR-Bench over-refusal rates, ToxiGen/RealToxicityPrompts, BeaverTails, plus any refusal rate, safety rate, ASR, or guard-model score stated on the model card itself or in the family's tech report (Qwen3, Llama 3.2, Gemma 2, SmolLM2, OLMo, Granite 3.1, Falcon3, MiniCPM, Pythia, TinyLlama, Danube3 all have tech reports or detailed cards). BOTH sides of safety must be representable: harm-refusal AND over-refusal. A row set that only has harm-refusal numbers permits the degenerate blanket-refuser winner the hypothesis explicitly disqualifies, so over-refusal coverage must be reported separately in the coverage summary, not folded into a single 'safety coverage' count.

  AXIS 2 - CAPABILITY (dense, cheap, and needed as a confound control): GSM8K, MMLU, MMLU-PRO, ARC, HellaSwag, IFEval, BBH, GPQA, MUSR, MATH Lvl 5, Arena-Hard, TruthfulQA, Winogrande. The Open LLM Leaderboard v2 contents dataset (open-llm-leaderboard/contents on HF, ~4,580 rows, parquet, loadable via load_dataset) is the highest-coverage single source for small models and MUST be pulled programmatically, never hand-transcribed. Its 'Model sha' column is what makes revision-level matching possible at all and must be carried into our rows.

  PER-ROW REQUIREMENTS (all mandatory, no nulls-by-laziness):
    checkpoint_id (HF repo id, exactly as in the panel manifest), lineage_id, revision_sha_source (the sha the SOURCE evaluated, if stated), revision_sha_panel (the sha our manifest pins), revision_match in {EXACT, SAME_REPO_UNKNOWN_SHA, SIBLING, FAMILY_ONLY}, benchmark, metric_name, value (float), scale (e.g. '0-100 percent', '0-1 rate', 'raw score 0-90'), polarity in {HIGHER_IS_SAFER, LOWER_IS_SAFER, HIGHER_IS_MORE_CAPABLE, NOT_ORDERED} stated EXPLICITLY per row and never inferred downstream from the benchmark name, axis in {SAFETY_HARM, SAFETY_OVERREFUSAL, SAFETY_OTHER, CAPABILITY}, source_url (exact, deep-linked, not a homepage), source_type in {OFFICIAL_MODEL_CARD, TECH_REPORT, PEER_REVIEWED_PAPER, ARXIV_PREPRINT, LEADERBOARD_SNAPSHOT, THIRD_PARTY_REPO}, source_version_or_release (e.g. HELM release v1.1.0, leaderboard snapshot date), retrieval_date (ISO), judge_or_grader (what scored it: GPT-4 judge, Llama Guard, string match, human - unknown is allowed but must be the literal string 'UNSTATED'), circularity_flag (string, empty or e.g. 'QWEN3GUARD_REWARD_CIRCULAR'), and verbatim_snippet (<=300 chars of the source text the number was read from, so the row is auditable without re-fetching).

  POLARITY IS LOAD-BEARING. ASR (attack success rate) is LOWER_IS_SAFER; refusal rate on harmful prompts is HIGHER_IS_SAFER; XSTest full-refusal rate on SAFE items is LOWER_IS_SAFER (a high value is over-refusal, i.e. WORSE); AIR-Bench and HELM safety scores are HIGHER_IS_SAFER. Getting one of these backwards silently flips a Spearman sign in iteration 3, so polarity must be set from the source's own wording and the wording quoted in verbatim_snippet.

  SPLIT REQUIREMENTS. One split_assignment row per weight lineage, covering ALL 93 lineages in the manifest, not just the ones measured this iteration. Held-out >= 1/3 of lineages. Stratified by (architecture_family, has_abliterated_or_uncensored_member, size_bucket) so both sides carry the hard cases. At least two architecture families must appear ONLY in held-out, so leave-one-family-out is possible. Assignment produced by a deterministic seeded rule (fixed seed, sorted lineage ids, documented hash) that is written verbatim into the artifact and reproducible by re-running the emitted rule text.

  SIZE / FORMAT. Well under 300MB - the whole thing is a few thousand JSON rows plus the raw source snapshots. Cache raw pulls (parquet/JSON) to disk so the harvest is auditable and re-runnable offline. Ship full/mini/preview variants per the aii-json skill.

  WHAT WOULD MAKE THIS ARTIFACT FAIL: silent fabrication of a plausible-looking benchmark number (fatal - every value must trace to a fetched URL and a quoted snippet); collapsing SIBLING-revision rows into EXACT rows; a split that leaks an abliterated member's parent across the boundary; or reporting 'good coverage' without the family/scale skew breakdown.
dataset_search_plan: |-
  PRE-FLIGHT (do first, ~30 min).
  P1. LOCATE THE PANEL MANIFEST. Iteration 1's frozen 137-checkpoint / 93-lineage manifest, prompt corpus, and 10-tokenizer-family refusal lexicons live in the previous run's workspaces. Glob for them under /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/ (try iter_1/gen_art/*/data_out.json, *manifest*.json, *panel*.json) and also under /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/ and the user_uploads folder. Log exactly which file you used and its row count.
    FALLBACK IF THE MANIFEST IS NOT FOUND (plan for this - it is the single most likely blocker): rebuild an equivalent panel deterministically from the HF Hub API (huggingface_hub.HfApi().list_models) using the lineage list enumerated in the hypothesis - Qwen3-0.6B/1.7B/4B (base + instruct + SafeRL + abliterated), Qwen2.5-0.5B/1.5B, Llama-3.2-1B/3B, gemma-2-2b, SmolLM2-360M/1.7B, TinyLlama-1.1B, Pythia-410M/1B/1.4B, OLMo-1B, Danube3-500M, Falcon3-1B-Instruct, Granite-3.1-2B-Instruct, MiniCPM-1B - plus abliterated/uncensored derivatives found by searching HF for 'abliterated', 'uncensored', 'ortho' filtered to those base architectures and <=4.2B. Pin every repo's current commit sha via HfApi().model_info(repo, revision='main').sha. Emit the rebuilt manifest as a deliverable row kind so iteration 3 is not blocked either way, and state loudly in the artifact that it is a REBUILD, not the iteration-1 frozen manifest.
  P2. Resolve every checkpoint's #params and architecture from HF config.json / model_info so the <=4.2B filter and the size-bucket stratification are grounded, not guessed.

  STAGE 1 - CAPABILITY HARVEST (cheap, dense, do it first so you have a working pipeline before the hard axis). ~45 min.
  S1.1. load_dataset('open-llm-leaderboard/contents') -> pandas. Columns to keep: eval_name, Model, fullname, 'Model sha', 'Base Model', Architecture, 'Weight type', '#Params (B)', Precision, Type, MoE, 'Chat Template', Average, IFEval, BBH, 'MATH Lvl 5', GPQA, MUSR, 'MMLU-PRO' (raw AND normalised where both exist), Flagged, 'Submission Date'. Join to the panel on normalised repo id (lowercase, strip whitespace); set revision_match=EXACT when 'Model sha' equals the panel sha, SAME_REPO_UNKNOWN_SHA otherwise. Emit one row per (checkpoint, benchmark). DROP rows where Flagged is true, but RECORD them in a separate flagged list rather than deleting silently.
  S1.2. Also pull open-llm-leaderboard/results (per-model raw result files) for any panel checkpoint missing from contents; and try the archived v1 datasets (HuggingFaceH4/open-llm-leaderboard-evaluations-results, open-llm-leaderboard-old/results) for older small models (Pythia, TinyLlama, OLMo, Danube3) which predate v2 and may only exist in v1. Record which leaderboard VERSION each row came from - v1 and v2 scores are NOT comparable and mixing them without a version column is a real error.
  S1.3. GSM8K / MMLU / ARC / HellaSwag / Arena-Hard where the leaderboards do not carry them: read the family tech report / model card table. Qwen3, Llama-3.2, Gemma-2, SmolLM2, Granite-3.1, Falcon3, MiniCPM and OLMo all publish per-size benchmark tables in their cards or reports.

  STAGE 2 - SAFETY HARVEST (the hard, high-value axis). ~2.5 h. Work source-by-source, each with a cached raw snapshot.
  S2.1. HELM (two leaderboards, one mechanism). HELM Safety v1.0 (crfm.stanford.edu/helm/safety/) and AIR-Bench 2024 (crfm.stanford.edu/helm/air-bench/v1.1.0/). The site is a static front-end over JSON on a public GCS bucket: https://storage.googleapis.com/crfm-helm-public/<project>/benchmark_output/releases/<release>/... with per-group JSON (groups/*.json, schema.json, runs_to_run_suites.json). PROBE the exact paths with HTTP GET before writing the parser - do not assume the layout; if the bucket paths 404, fall back to (a) the JSON the leaderboard page itself requests (read the page source / network paths), (b) the stanford-crfm/helm GitHub repo's documented download instructions, (c) the AIR-Bench paper's own results table (arXiv:2407.17436, openreview UVnD9Ze6mF) transcribed with verbatim_snippet. EXPECT LOW PANEL OVERLAP: HELM evaluates ~21-24 mostly frontier models, so most or all of our <=4.2B panel will be absent. That absence is a RESULT - record it as a coverage number, do not pad it.
  S2.2. TrustLLM (trustllmbenchmark.github.io + arXiv:2401.05561): pull the leaderboard tables and the paper's per-model results. Again expect frontier-model skew; harvest whatever small models appear (Vicuna/Llama-2 7B class at best) and record overlap honestly.
  S2.3. SALAD-Bench (OpenSafetyLab, arXiv:2402.05044, HF: OpenSafetyLab/Salad-Data and the leaderboard space), SORRY-Bench (ICLR 2025, github.com/SORRY-Bench/sorry-bench, HF: sorry-bench/sorry-bench-202406 - note the main dataset is GATED, but the PAPER's model results table is not and is the thing we actually need), DecodingTrust (decodingtrust.github.io, per-perspective scores), JailbreakBench (jailbreakbench.github.io leaderboard - ASR per model per attack), HarmBench (harmbench.org results table), OR-Bench (HF: bench-llm/or-bench + its leaderboard space, over-refusal rates), XSTest (arXiv:2308.01263 and any paper reporting XSTest per model - Hasan & Biswas arXiv:2605.05427 audits 21 open-weight LLMs on over-refusal AND harmful compliance and is a prime harvest target for BOTH safety sub-axes).
  S2.4. MODEL CARDS AND TECH REPORTS - likely the single richest safety source at our scale. For every panel checkpoint, fetch https://huggingface.co/<repo>/raw/main/README.md via the Hub API and regex-scan for safety numbers: /(safety|refus|harmful|toxic|jailbreak|ASR|attack success|over-refus|WildGuard|Guard)/i near a numeric. Qwen3-4B-SafeRL's card is the flagship case - it documents RL against a Qwen3Guard-Gen-4B safety reward plus a WorldPM-Helpsteer2 helpfulness reward and reports safety/helpfulness numbers; harvest every number it states AND set circularity_flag='QWEN3GUARD_REWARD_CIRCULAR' on any row whose judge_or_grader is a Qwen3Guard variant, because the hypothesis forbids using it as ground truth for that model. Also fetch the Qwen3 tech report, Llama-3.2 card, Gemma-2 card (which reports safety/ToxiGen/RealToxicity numbers), SmolLM2 paper, OLMo paper, Granite-3.1 card, and the abliterated-model cards (which often state a residual refusal rate - harvest it and mark source_type=THIRD_PARTY_REPO, low trust).
  S2.5. LAST-RESORT SWEEP for anything missed: scholarly search per checkpoint name + 'safety' / 'refusal rate' / 'jailbreak' restricted to 2024-2026, and fetch_grep the resulting PDFs for the model name to pull table values with context. Cap this at ~20 min per family so it cannot eat the budget.

  STAGE 3 - THE COVERAGE REPORT (a required deliverable, not a footnote). ~20 min.
  Compute and emit, as structured rows and as a human-readable markdown summary: n_checkpoints in panel at <=4.2B; n with >=1 SAFETY_HARM row; n with >=1 SAFETY_OVERREFUSAL row; n with >=1 CAPABILITY row; n with EXACT revision match vs SAME_REPO_UNKNOWN_SHA vs SIBLING; the same counts broken down by architecture family and by size bucket (<1B, 1-2B, 2-4.2B); and the count of lineages where at least one MEMBER has a safety number (lineage-level coverage differs from checkpoint-level coverage and iteration 3 bootstraps over lineages, so both are needed). Then emit an explicit list, machine-readable, of checkpoints that will REQUIRE in-house measurement because no external safety number exists - this list is the direct input to iteration 3's measurement budget. If safety coverage is below ~20% of the panel (the likely outcome), state that numerically and state plainly that the external-ground-truth axis of H3 is coverage-limited at this scale and that the hypothesis's documented fallback (two in-house refusal rates: harmful-prompt refusal and XSTest-style harmless-but-alarming refusal, with the R4 evaluator-system-prompt fix in force) becomes primary for the uncovered checkpoints. Do NOT run those in-house measurements here - that is an experiment artifact; just name the checkpoints and the axes needed.

  STAGE 4 - THE FROZEN SPLIT. ~30 min. Do this in a SEPARATE script executed AFTER stages 1-3 and record its wall-clock timestamp.
  S4.1. Build the lineage table: lineage_id, architecture_family, base repo, member repos, member roles in {base, instruct, safety_rl, abliterated, uncensored_finetune, other}, max #params, has_hard_case = (any member is abliterated or uncensored).
  S4.2. Deterministic rule, written verbatim into the artifact and reproducible: sort lineage_ids lexicographically; form strata as (architecture_family, has_hard_case, size_bucket); within each stratum order by sha256(lineage_id + '|' + SEED) hex; assign the first ceil(1/3) of each stratum to HELDOUT, rest to DEV; SEED = '20260813-iter2-split' (a fixed literal string, written into the artifact - do NOT use time or randomness that is not reproducible from the artifact alone). Then apply the family constraint: choose the two smallest-member-count architecture families whose lineages are not needed to keep DEV non-degenerate and force ALL their lineages to HELDOUT, so >=2 families are absent from DEV entirely; re-check the >=1/3 held-out floor after this forcing and, if it is violated, promote additional lineages by the same hash order until it holds. Log the forced families by name.
  S4.3. Emit a pre-registration statement row/file: ISO timestamp, the SEED, the rule text, the count of lineages on each side, the list of DEV-absent families, and the literal assertion that no metric definition from the 50-metric battery had been chosen when this split was written, plus the sha256 of the split file so any later edit is detectable. Note honestly if any lineage's membership was already known from iteration 1 exploration (the Qwen3-4B H0 lineage is explicitly an exploration lineage and should be forced to DEV, since metrics WILL be designed on it - putting it in HELDOUT would be self-deception; state this as a deliberate choice).

  STAGE 5 - THE DISQUALIFICATION RULE (machine-readable). ~15 min.
  Emit a rule row: rule_id='BLANKET_REFUSER_DISQUALIFICATION'; predicate = 'a candidate metric is DISQUALIFIED, regardless of its correlation with any safety target, if its top-ranked checkpoint has over-refusal above threshold on XSTest-safe items'; threshold expressed as full_refusal_rate_on_xstest_safe > 0.50 with partial_refusal counted as refusal, PLUS a secondary softer trip at > 0.35 that raises a WARN rather than a disqualification; the source of the over-refusal number in priority order (external row if one exists, else in-house measurement with the R4 evaluator system prompt); and the exact fields an iteration-3 script must read to evaluate it. Ground the threshold choice in a cited source if one supports it (XSTest paper arXiv:2308.01263 and OR-Bench report per-model full/partial refusal rates on safe items - fetch and cite the actual distribution rather than picking 0.50 out of the air; if the literature supports a different natural cut, USE it and say why). Also emit rule_id='QWEN3GUARD_CIRCULARITY': Qwen3Guard (any variant) must not be used as judge or ground-truth source for Qwen/Qwen3-4B-SafeRL, with the affected checkpoint ids listed.

  OUTPUT & VALIDATION. ~30 min.
  Single data_out.json with a top-level 'rows' array; each row has row_kind in {external_score, panel_checkpoint, lineage, split_assignment, coverage_stat, rule, prereg_statement} and the fields for that kind; per-row metadata_fold set to the lineage's split ('dev'/'heldout'/'na'). Validate with the aii-json skill against a schema you write and ship alongside. Emit full/mini/preview variants and check the file-size limit with aii-file-size-limit. Keep every raw snapshot (parquet, JSON, fetched READMEs) under a cache/ directory so the harvest is reproducible and every verbatim_snippet is re-checkable offline. Write a short README.md stating counts per row_kind, the coverage headline, and the split's freeze timestamp.

  FAILURE MODES AND WHAT TO DO.
  - HELM GCS layout differs from expectation -> probe, then fall back to the papers' own tables; never fabricate a path or a number.
  - SORRY-Bench / SALAD-Bench datasets are gated -> we do not need the prompts, only the published per-model results; take them from the papers and leaderboard pages.
  - Panel overlap with every safety leaderboard is ZERO -> that is a legitimate, reportable finding and the single most decision-relevant output of this artifact. Report it precisely (per source: n panel models present / n models the source evaluates) and hand iteration 3 the in-house measurement list. Do not substitute frontier-model rows for panel rows to make the table look full.
  - Two sources disagree on the same (checkpoint, benchmark, metric) -> keep BOTH rows, do not average, and set a disagreement flag with the delta; iteration 3 needs to see source variance.
  - Model card states a number without a scale or a grader -> keep it, set scale='UNSTATED' and judge_or_grader='UNSTATED', and lower its confidence flag; do not guess.
  - Time is running out -> Stages 4 and 5 (split + rules) are CHEAP and are the parts nothing downstream can proceed without, so if the harvest is overrunning, cut Stage 2.5 and the long tail of S2.3 sources, but NEVER cut the split or the coverage report.
target_num_datasets: 12
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_0UsKSgsMHome
type: research
title: Spec Sheets for Rival LLM Safety Metrics
summary: |-
  Reimplementation dossier for the four external baselines plus the estimator toolkit and a full citation audit. Deliverables: research_report.md (6 sections, ~1300 lines, every number carrying an [arXiv:ID section] anchor), research_out.json, and estimator_check.py/.json (deterministic Monte Carlo, seed 20260812).

  BASELINES, all read from primary full text. AMS (arXiv:2608.05578, venue confirmed IEEE Access 14:91723-91737): sigma = (mu+ - mu-)/sigma_pooled on the diff-in-means direction, final prompt token, 40-80% relative-depth sweep, 16 contrastive pairs x 3 concepts, 96 forward passes / 10-40s, thresholds PASS>3.5 / WARN 2.0-3.5 / CRIT<2.0. 71% = 10/14 leave-one-MODEL-out, identical under both calibration rules. r=-0.546 (p=0.043) verified; the unquoted Spearman rho=-0.423 is NOT significant. H4 quote transcribed verbatim with no hedge. THREE panel checkpoints appear in AMS Table I (Llama-3.2-3B-Instruct 8.37, gemma-2-2b-it 4.80, Llama-3.2-1B-Instruct 4.55) giving a reproduction gate. RAS/SafeVec (arXiv:2606.25750): all five stages plus EVERY published constant (tau=0.8, q=0.9, lambda=0.5, wu=wj=0.5, c=0.75, beta=5.0). VISAGE (arXiv:2405.17374): E[Smax-S] over alpha~U(-0.5,0.5), 3 dirs x 20 steps x Adv-80. Qi (arXiv:2406.05946 - ID resolved).

  DECISIONS SETTLED. (1) RAS overlap with our panel is EMPTY - every RAS-scored checkpoint is >=4B and none is ours; we must write 'our RAS reimplementation' throughout. (2) VISAGE at full fidelity is ~28 h/1B model on CPU (4,800 generations); a justified reduced grid lands at ~1.3 h/model, with an explicit fidelity-cost table. (3) Qi's operational decay length is k=5 tokens (beta_t=2 for t<=5, 0.1 for t>5), yielding pre-registered cut PR-1: Delta-lambda must survive beyond generated step 15, tested on [16,48], conservative replicate at 20. (4) NO prior work applies EWS/critical slowing down to LLM generative dynamics (arXiv abstract search returns zero) - but arXiv:2605.09043 applies CSD to conversation derailment in human dialogue and must be cited and distinguished, and AQI (arXiv:2506.13901) is a fifth uncited competitor.

  ESTIMATOR TOOLKIT with measured, not remembered, corrections. ewstools defaults read from source (Gaussian bandwidth 0.2, sigma=(0.25/0.675)*bw_num, rolling window 0.25, Kendall tau; NO built-in AC1 bias correction). Monte Carlo at our exact lengths: raw AC1 bias -0.064 at n=64 vs -0.020 at n=192, reduced to -0.009 / -0.0005 by +(1+3r)/n. A 192->64 effective-length difference alone manufactures a ~0.04 spurious AC1 gap in the 'right' direction - mitigation is mandatory and threefold. The AR(1)->lambda conversion is convex, so lambda is inflated 75% at n=64, phi=0.9; noise-floor truncation UNDER-estimates lambda by 40% if the fit window runs past the floor crossing. Runnable numpy/scipy recipe supplied with stopping rule, surrogate-ARMA null (Dakos Fig.11), and n_min=64 floor.

  OBSERVABLE. Yin et al. measure the probe refusal score at GENERATED positions (thinking chain), so r_t is adopted, not coined; verbatim 12-entry refusal-substring list transcribed from Arditi's source; per-tokenizer runtime resolution recipe for the leading-space hazard; abliteration-invariance argument grounded with its honest caveat.

  AUDIT. All 16 anchors resolve, none fabricated, no misattribution. Kwon's base-model control and Ratnakar's ~40%-depth figure both verified verbatim, so H1's and Step 0(a)'s rationales stand. The unanchored knowledge-action-gap result is FOUND: arXiv:2603.18353, 98.2% AUROC vs 45.1% sensitivity, 3,695 SAE features, both verbatim. Hasan & Biswas supply the missing r = -0.032, p = 0.89. Only two claims need rewriting (Qi 'Oral' unverifiable from arXiv; RAS speed-up internally inconsistent at 216.88x vs 210.13x). Recommends promoting SRI (arXiv:2602.02600) to a baseline - it is nearly free on hidden states we already extract.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_dependency_files:
  file_list:
  - research_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Free-first web search (general + scholarly modes), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-concept-fig-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>
</available_resources>

<available_data_sources>
Use the sources appropriate to your task. Read the relevant skill file BEFORE using each source.

- **HuggingFace Hub** (HF) — ML datasets (NLP, vision, tabular, benchmarks)
- **Our World in Data** (OWID) — Global statistics (energy, health, economics, environment, demographics)
- **Alternate methods** — Python/shell (sklearn.datasets, openml, direct URL, APIs, etc.)

If the plan specifies a source or one fits better, use it.
You may combine sources. Use web search (aii-web-tools skill) to research candidates (background, papers, provenance) — NOT to find/download datasets.
</available_data_sources>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for dataset selection, evaluation metrics, agent orchestration patterns.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Update data.py to only include the chosen 10 datasets and generate full_data_out.json. Re-run to generate full_data_out.json. Validate output format with aii-json skill and fix any errors. Generate full, mini, and preview versions with aii-json skill's format script using `--input full_data_out.json` (creates full_full_data_out.json, mini_full_data_out.json, preview_full_data_out.json — rename to full_data_out.json, mini_data_out.json, preview_data_out.json).
TODO 2. Verify full_data_out.json, preview_data_out.json, and mini_data_out.json exist in your workspace (see <workspace>) and contain correct data.
TODO 3. Apply aii-file-size-limit skill's file size check procedure (100MB limit) to full_data_out.json.
TODO 4. Ensure a `pyproject.toml` exists in your workspace with ALL dependencies pinned to the exact versions installed in your .venv (run `.venv/bin/pip freeze` to get them). This is required for reproducibility. The [project] section must include name, version, requires-python, and a dependencies list with pinned versions (e.g. `numpy==2.0.2`, not `numpy>=2.0`).
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "DatasetExpectedFiles": {
      "description": "All expected output files from dataset artifact.",
      "properties": {
        "script": {
          "description": "Path to data.py script. Example: 'data.py'",
          "title": "Script",
          "type": "string"
        },
        "datasets": {
          "description": "Dataset file groups \u2014 one per dataset, each with full/mini/preview variants",
          "items": {
            "$ref": "#/$defs/DatasetFileSet"
          },
          "title": "Datasets",
          "type": "array"
        }
      },
      "required": [
        "script",
        "datasets"
      ],
      "title": "DatasetExpectedFiles",
      "type": "object"
    },
    "DatasetFileSet": {
      "description": "One dataset's three required output variants.",
      "properties": {
        "full": {
          "description": "Full dataset JSON file(s). Single file or split files. Example: ['full_data_out.json'] or ['full_data_out/full_data_out_1.json', 'full_data_out/full_data_out_2.json']",
          "items": {
            "type": "string"
          },
          "title": "Full",
          "type": "array"
        },
        "mini": {
          "description": "Mini dataset JSON file path (3 examples). Example: 'mini_data_out.json'",
          "title": "Mini",
          "type": "string"
        },
        "preview": {
          "description": "Preview dataset JSON file path (10 examples). Example: 'preview_data_out.json'",
          "title": "Preview",
          "type": "string"
        }
      },
      "required": [
        "full",
        "mini",
        "preview"
      ],
      "title": "DatasetFileSet",
      "type": "object"
    }
  },
  "description": "Dataset artifact \u2014 structured output + file metadata.\n\nFinds, evaluates, and prepares datasets for research experiments.\nProduces data.py and full_data_out.json files.",
  "properties": {
    "title": {
      "default": "",
      "description": "Artifact title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); describe the content, not a status.",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/DatasetExpectedFiles",
      "description": "All output files you created. Must include data.py script plus dataset file groups (full/mini/preview variants)."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files"
  ],
  "title": "DatasetArtifact",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````
