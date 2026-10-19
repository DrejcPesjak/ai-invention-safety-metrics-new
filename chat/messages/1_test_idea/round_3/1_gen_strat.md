# gen_strat_1 — test_idea

> Phase: `invention_loop` · round 3 · `gen_strat`
> Run: `iter1_33370088803c` — Catching Edited Safety Models by Reading Weights in Sliding Windows
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_strat_1` (terminal_claude_agent, claude-opus-5)

### [1] CONFIG · 2026-08-13 20:07:19 UTC

```
model: claude-opus-5 | effort: medium | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_strat/gen_strat_1
```

### [2] SYSTEM-USER prompt · 2026-08-13 20:07:25 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A strategy planner (Step 3.1: GEN_STRAT in the invention loop)

Each iteration of the invention loop runs: GEN_STRAT → GEN_PLAN → GEN_ART → GEN_PAPER_TEXT → REVIEW_PAPER → UPD_HYPO
Artifact types: RESEARCH (web search), EXPERIMENT (code), DATASET (data collection), EVALUATION (metrics), PROOF (Lean 4)
State persists across iterations: strategies, plans, artifacts, paper_texts (read from the run tree)

You received the hypothesis, iteration status (current + remaining), previous iteration's strategies, available artifact types, existing artifacts, and reviewer feedback.
Your strategy governs THIS iteration only. You define what artifacts to create NOW.

Focused strategy → efficient progress. Scattered strategy → wasted iteration.
</your_role>
</ai_inventor_context>

<available_resources>
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

<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>
</available_resources>

<time_budgets>

Each artifact executor has a fixed time budget (including writing code, debugging, testing, and fixing errors):

- research: 3h
- dataset: 6h
- experiment: 6h
- evaluation: 3h
- proof: 3h

</time_budgets>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape. Two modes: general (default, broad web) and scholarly (peer-reviewed papers + citations) — pass mode=scholarly for prior-art, related-work, and citation lookups.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<research_methodology>
Think like a researcher planning a study for a top venue.

- All strategies run in parallel and their artifacts combine into one pool. Together they must build toward a publishable paper — each strategy contributes a distinct, necessary piece. No strategy should be a standalone island.
- Ask yourself: what would a reviewer need to see? Proper baselines, controlled comparisons, ablations that isolate what matters. Plan artifacts that preempt reviewer objections.
- Depth over breadth. One well-designed experiment with proper controls beats five shallow ones.
- Match your evaluation to your claims. Measure what the hypothesis actually asserts.
- When results are weak or partial, vary the approach before writing it off. One failed method doesn't falsify the hypothesis.
- If iterations remain, think about what the NEXT iteration will need. Leave useful building blocks — datasets, baselines, preliminary results — that future strategies can build on, refine, or compare against.
</research_methodology>

<principles>
1. FOCUS ON NOVELTY - every strategy must lead to a genuinely novel contribution
2. MAXIMIZE PARALLELIZATION - all artifacts in your strategy run in parallel
3. BUILD ON EXISTING WORK - use completed artifacts from previous iterations, learn from failures
4. ITERATE ON THE METHOD - a negative result is about the approach, not the hypothesis. Try different methods, parameters, data, or formulations within the hypothesis bounds.
5. DIAGNOSE BEFORE DECIDING - before each iteration, review what worked, what didn't, and why. Use that to choose what to try next. Gaps are action items, not conclusions.
6. SET DEPENDENCIES WISELY - depends_on is a list of {id, label} objects referencing existing artifacts; each label is a short free-text type (a word or two, e.g. "dataset", "validates", "extends") that tags how the dep is used
7. PLAN FOR DEPENDENCIES - if an artifact depends on another (e.g. experiments need datasets), ensure prerequisites exist first or plan them this iteration for the next
</principles>

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

<hypothesis>
Your strategy should advance this hypothesis.

kind: hypothesis
title: Spotting an edited safety model from weights
hypothesis: |-
  CORE CLAIM, NOW SPLIT IN TWO BY ITERATION 2'S EVIDENCE. The original claim — that a model's safety behaviour is legible from the model ALONE, cheaply, better than from its outputs — has been tested and it resolves into one supported half and one refuted half. Both halves are the contribution and the paper carries both.

  CLAIM A (SUPPORTED, and now the headline): a checkpoint that has undergone a GLOBAL SINGLE-DIRECTION ABLITERATION EDIT can be detected from its tensors alone — no parent, no reference model, no prompts, no forward passes — and this is a claim about the EDIT, not about behaviour.
  CLAIM B (REFUTED as originally stated, and reported as a bounded negative): for GRADED BEHAVIOURAL SAFETY, no interior observable in a 53-metric frozen battery beats a trivial black-box baseline at this panel size. The best predictor of harmful-prompt refusal is B09, the greedy-decode refusal rate (rho = +0.766 [+0.539, +0.917], 26 chat-rendered members over 18 lineages). Every paired lineage-bootstrap difference |rho_X| - |rho_B09| covers zero or is worse (A02 +0.036 [-0.225, +0.303], A01/AMS -0.161 [-0.501, +0.208], W01 -0.373 [-0.731, -0.039], alpha_50 -0.453). The pre-declared falsifier fired.

  WHAT ITERATION 2 SETTLED, CARRIED FORWARD (do not re-litigate; do not re-run).
  S1. THE WEIGHT SCAR IS REAL AND CHEAP. Over residual-write matrices form A = sum_l W W^T / ||W||_F^2, take v1 = its minimum eigenvector, and measure per-layer write energy along v1. W05 = log10 min_l e_W(v1) gives AUROC 1.000 separating 8 abliterated members from 36 others across 44 checkpoints / 23 lineages / 7 families; held-out-lineage AUROC 1.000; leave-one-architecture-family-out perfect on all three families that have abliterated members; 0 prompts, 0 forward passes, 11.4 s median. W01 = log10(median lam / lam_1) gives abliterated median 4.26 [1.44, 4.82] vs base 0.58 / instruct 0.47 / behaviourally-uncensored 0.46 / Qwen3-4B-SafeRL 0.47; W04 = lam_2/lam_1 separates with abliterated min 0.85 vs non-abliterated max 1.62. An injected rank-one positive control reproduces the signature exactly (cos(v1, r) = 1.000, W02 = 1.00, W01 0.62 -> 4.82).
  S2. THE SCAR READS THE EDIT, NOT THE BEHAVIOUR, AND ITS CALIBRATION DOES NOT TRANSFER. Behaviourally-uncensored fine-tunes and the official Qwen3-4B-SafeRL sit inside the plain-instruct distribution. A dev-set midpoint threshold catches 1/2 held-out abliterated members (W01/W04 catch 0/2) at 0 false positives: the RANKING transfers, the CUTOFF does not. The margin is thin — weakest abliterated -2.742 vs strongest non-abliterated -2.665, i.e. 0.077 in log10.
  S3. THE SCAR IS BLIND TO NON-GLOBAL EDITS, MEASURED IN-HOUSE. A band-limited edit confined to the middle third of layers is not detected (W02 = 0.0, W01 unchanged). Because W05 is a MINIMUM over layers, it is by construction the most fragile of the five weight statistics to anything that touches even one layer.
  S4. ALPHA_50 IS DEAD AS A METRIC. Experiment 2 ran it at power (14 members, 4 lineages, 60,040 generations): verdict NOT_A_TRIAGE_SCORE (R = 0.73 normalised, permutation p = 0.76). The lexical artefact is in the SCORER, not the axis: the Arditi 12-substring regex defines alpha_50 for only 7/14 members while a semantic judge defines it for 14/14 on the same recorded text (qwen3-0.6b-abliterated regex max refusal 0.01 vs judge 0.85; median kappa 0.279; 20 (member, axis) cells disagree on reachability). Under the judge, 3/4 lineage CIs exclude zero but the SIGN REVERSES on Llama (across-lineage sign test p = 0.625). The paraphrase-disjoint axis C is SAFETY_SPECIFIC and the random axis D DOES NOT REPRODUCE (0/14 and 0/28 cells reach 0.5) — the axis is fine, the metric is not. Steered refusal is NON-MONOTONE in alpha, so any future dose-response must fit the first upward crossing on the rising branch only.
  S5. ITERATION 1'S NEGATIVES ARE PARTLY RETRACTED. The re-analysis reproduced 25 / changed 12 / retracted 9 of 46 claims. 'Early-warning indicators track lineage, not safety' is RETRACTED as a settled negative and downgraded to a qualitative observation: only 1 of 4 members passes the r_0 AUROC >= 0.70 observable-validity gate (instruct 0.793; abliterated 0.481, base 0.414, smollm2 0.633), so the panel could not have carried the claim. The random-direction control REVERSES at the pre-stated readout layer (random separates 0/3, refusal 2/3), and the SPI rank correlation rho = -0.20 flips sign to +0.105 under rank-average tie handling. Consequence for this iteration: tie handling, readout layer and observable validity are declared explicitly and gate every correlation reported.
  S6. THE JUDGE IS THE INSTRUMENT. Rubric A (the R4 evaluator prompt) scores HARMFULNESS not BEHAVIOUR and gives kappa ~0; rubric B ('judge only behaviour, not whether the request was harmful') agrees 6/6 with hand labels and is mandatory. The frozen judge's COMPLIANCE recall is 0.085 [0.042, 0.166] against 0.939 repaired, and both headline iteration-1 revisions strengthen under misclassification correction.
  S7. GROUND TRUTH IS SEPARABLE AND SAFETY-RL IS DISTINGUISHABLE FROM INSTRUCTION TUNING. Abliterated harmful-refusal 0.01-0.34 vs instruct 0.38-0.96; Qwen3-4B-SafeRL matches instruct on harmful refusal (0.9125) while cutting jailbreak ASR 0.688 -> 0.088 and is the most expensive model to steer into spurious refusal. No blanket refusers (over-refusal <= 0.16). Safety-RL therefore shows up in ASR, not in refusal rate — any metric evaluated only against refusal rate cannot see it.

  THE REVISED CLAIMS FOR ITERATION 3. The battery is finished; this iteration does not run a third battery. It does exactly four things: it establishes the true scope of the one positive, it makes the one negative quantitative instead of merely stated, it ships the analysis, and it positions honestly against two prior works that were missed.

  H1 (SCOPE OF THE SCAR — the toolchain confound, the reviewer's sharpest point, and the highest-value experiment). The 8 abliterated positives come from TWO uploaders (six from huihui-ai, two from Goekdeniz-Guelmez) and BOTH run an all-layer global diff-in-means projection. Leave-one-architecture-family-out is therefore the wrong generalisation control: architecture is not what W05 keys on, the EDIT RECIPE is. The 2026 community landscape is dominated by variants that are explicitly not a single global rank-one projection — norm-preserving / projected abliteration, ORBA orthogonal-reflection bounded ablation, multi-direction SVD, per-head surgery, DCT spectral-cascade modes — and S3 already shows W05 is blind to any edit that is not global. Prediction, stated so it can fail: W05's AUROC drops materially on mechanically different toolchains, and the honest scope statement is 'detects global single-direction abliteration, the huihui/Josiefied recipe class', not 'detects abliteration'. Test: add at least three abliterated checkpoints from mechanically different toolchains (an mlabonne-recipe model, a grimjim projected / norm-preserving variant, an OBLITERATUS multi-direction run), report W01-W05 on each, and report LEAVE-ONE-UPLOADER-OUT alongside leave-one-family-out. The nearest published analogue, arXiv:2604.08844, reports that a spectral weight classifier trained on one editing method assigns EVERY out-of-method adapter a lower drift score than every in-method one (AUC 0.00) — this exact failure mode is already in the literature once, so finding it is a confirmation and not finding it is a genuine surprise.

  H2 (LAUNDERING — is the scar a provenance signal or a curiosity?). The deployment premise is not yet instantiated: all 8 positives carry 'abliterated' or 'gabliterated' in their repository id, so the evaluated task is solved for free by a string match. Using the in-house edit machinery that already produced the rank-one and band-limited controls: abliterate Qwen3-1.7B, then (a) LoRA-SFT 200 steps on benign data, (b) linearly merge 50/50 with the instruct parent, (c) round-trip int8 and int4 quantization, (d) add back an epsilon-scaled random rank-one term at increasing scale. Report W01-W05 AND harmful-refusal rate at every stage. The load-bearing question is the ORDER of two deaths: if the flag dies only after the un-censoring dies, the scar is a robust provenance signal and that is a strong result; if it dies first, the scar is evadable and we say so plainly. Separately, scan a few hundred sub-4B Hub checkpoints from stored tensors and report any high-scoring repository whose card does not declare abliteration — even a handful of confirmed undeclared positives makes the deployment claim concrete rather than aspirational.

  H3 (THE PARENT-REQUIRED HEAD-TO-HEAD — what does the constraint actually cost?). E_1 from the parent-requiring incumbent is described but never computed. The panel contains instruct/abliterated sibling pairs for at least the Qwen2.5-0.5B, Qwen2.5-1.5B, Qwen3-0.6B, Qwen3-1.7B and Llama-3.2-1B/3B lineages. Compute E_1 on every such pair from tensors already downloaded and report W05 vs E_1 AUROC on that matched subset. Either outcome is publishable and both are stronger sentences than the current one: 'parent-free matches parent-required on this panel at zero prompt cost', or a quantified price of the parent-free constraint.

  H4 (MAKE THE NEGATIVE QUANTITATIVE — power, comparator, reliability, depth). The falsifier fired, but as written it does not distinguish 'the interior buys nothing' from 'we cannot tell'. Four repairs, all re-analysis:
  (a) POWER. Report the minimum detectable paired-rho difference at n = 18 lineages for the actual bootstrap (a two-line simulation), and state explicitly whether the falsifier COULD have failed. Restate the conclusion in the form the data supports: 'at this panel size no interior metric shows an advantage over the best black-box baseline larger than ~|drho|; distinguishing smaller advantages needs roughly N lineages.'
  (b) COMPARATOR. B09 was selected as best-of-11 black-box declarations on the same data, so the headline is best-of-11 against a fixed white-box candidate. Report the paired comparison against a PRE-SPECIFIED black-box metric (B01 logit gap, which has a published prior) alongside the post-hoc winner, and reconcile the awkward fact that A02 leads B09 numerically at both aggregation units (+0.802/+0.819 vs +0.766/+0.852).
  (c) RELIABILITY. Each checkpoint contributes 40 harmful and 25 XSTest items scored by a single judge, with judge-vs-screen kappa ~0.30 — a binomial SE of ~0.08 at p = 0.5 before judge noise. Estimate reliability (split-half over the 40 items, plus judge-vs-adjudicator agreement on a stratified subsample), report attenuation-corrected correlations alongside raw, add per-member binomial error bars, and state whether any ordering moves.
  (d) DEPTH. The held-out AUROC profile SATURATES at 1.0 across indices 4-25 of 28, so rho* = 0.679 was fixed by a d'-tiebreak on a 22-layer plateau. Report the Section 5.2 correlation table at three depths spanning the plateau (bare argmax ~0.14, 0.50, 0.679), report alpha_50's censoring rate (37/44 at rho* = 0.679) at each, and state whether the falsifier conclusion is invariant. If any activation metric beats the black-box baseline at some depth in the plateau, disclose it even though the pre-declared depth is primary.

  H5 (SHIP THE ANALYSIS, AND SAY 'PRE-REGISTERED' ONLY WHERE IT IS TRUE). Two discipline defects, both fatal to a paper whose argument IS measurement discipline. First, no AUROC, Spearman, bootstrap or paired difference exists inside the versioned artifact — every headline number was computed outside it. Deliver analysis.py as a first-class artifact reading long_table.jsonl + behaviour.jsonl and emitting every AUROC, Spearman, bootstrap CI and paired difference in the paper, with seed, B, resampling scheme (with/without replacement; how the 9 singleton lineages are handled) and tie-handling printed in its header, plus an assertion block checking each output against the quoted value. State the bootstrap specification in the Method in two sentences. Second, metric_spec.py (sha 544ff994...) declares 53 metrics with family, prompt requirement and declared cost, and NOTHING ELSE — it contains no falsifier, no analysis plan, no base-model exclusion rule, no blanket-refuser threshold, no paired-bootstrap specification. Reserve 'SHA-stamped pre-registration' for the metric declarations, publish the plan document that did contain the falsifier with its own hash and a timestamp demonstrably prior to execution, and elsewhere write 'we adopted the rule that...'. Add a table mapping every 'pre-registered' claim to the artifact and line that records it.

  H6 (POSITIONING — two uncited works, one very close). (i) arXiv:2604.08844 (Paul, 'Spectral Geometry of LoRA Adapters Encodes Training Objective and Predicts Harmful Compliance') extracts per-layer spectral features — norms, stable rank, singular-value entropy, effective rank, cosine to a healthy centroid — from weight DELTAS across 38 manufactured adapters, reporting AUC 1.00 for binary drift and rho = 0.72 to HEx-PHI harmful compliance. Its feature set overlaps W06-W11 almost item for item, its parent/delta requirement is exactly the gap we occupy, and its rho = 0.72 is a direct counterweight to any claim that weight geometry cannot carry behavioural signal. Cite it in Related Work AND at the point of use, and distinguish on three axes: parent-free vs delta-based, real community checkpoints vs manufactured adapters, edit-detection vs behaviour prediction — while explaining why our behaviourally-uncensored members show none of its behavioural signal (different manufacture regime, no controlled dose ladder). (ii) The OBLITERATUS toolkit ships a parent-free 'spectral certification' step that inspects an abliterated checkpoint's own weights to certify whether the projection is complete, and its documentation records that certification frequently reads 'incomplete' even where practical refusal rate is 0% — prior community practice for the operation we claim, and an independent anecdotal mirror of our S2 finding that the ranking transfers while the calibration does not. Reframe the novelty as the first measured, held-out-validated, published characterisation of parent-free spectral abliteration detection INCLUDING its calibration failure and its recipe-class scope. Both framings are defensible; silence is not.

  H7 (REPORTING HONESTY, minor but cheap). Report [min, max] for EVERY class in the weights table, not only the abliterated column — the shipped diagnostics show genuine overlap (W01 base max 1.992 vs abliterated min 1.438; W02 base max 1.000 equal to the abliterated median). Name allenai/OLMo-1B-hf (-2.665) as the nearest non-abliterated neighbour on W05, and note in Limitations that the three checkpoints nearest the boundary are all from single-member architecture families (olmo, gpt_neox), so the false-positive rate outside the seven tested architectures is unmeasured. Correct W03's random-direction count to 256 (the paper says 64; lib_metrics.py and the frozen spec both say 256), name the exact positive-control checkpoint and revision (Qwen/Qwen3-0.6B, the instruct member, not the Base member whose W01 is 0.628), and separate the two unrelated 4.82 values so they do not read as a typo. Generate numerals into the text from analysis.py rather than transcribing them.

  WHAT IS RETIRED. The 53-metric battery is not rebuilt or extended. alpha_50 and the whole steering-price family are retired as candidate metrics and survive only as the S4 negative plus the scorer-artefact finding, which is itself a reportable methodological result about every alpha_50-style metric built on a refusal-substring screen. The early-warning-signal / critical-slowing-down arm is retired entirely: S5 shows the iteration-1 panel could not have carried it, and re-running it is not the best use of this iteration. The broad framing 'safety behaviour is legible from the model alone' is retired in favour of the two narrower claims A and B above.

  CONFIDENCE. Mixed and deliberately asymmetric. HIGH that the global-abliteration weight scar exists, is cheap and is measurable parent-free — it survived a held-out lineage split, leave-one-family-out and an injected positive control, and it is now corroborated by an independent community tool doing the same operation. LOW that it generalises to abliteration in general: two uploaders, one recipe, a demonstrated blindness to band-limited edits, a 0.077-log10 margin, and a published precedent of exactly this cross-method collapse. HIGH that graded behavioural safety is not better read from the interior than from greedy-decode refusal rate AT THIS PANEL SIZE, and LOW that the panel could have detected a modest advantage if one existed — which is why H4(a) is mandatory before the negative is stated as a general one. The single most likely outcome of iteration 3 is that the scar survives laundering by quantization and merging but not by LoRA-SFT, and misses at least one of the three new toolchains — which would make the paper's claim 'a recipe-class provenance signal, free at Hub scale, with a measured evasion boundary'. That is a smaller claim than iteration 1 hoped for and a considerably more defensible one.
motivation: |-
  Judging whether a random Hugging Face checkpoint is safety-aligned currently requires running it against a harmful-prompt benchmark: slow, gameable (a model can be tuned to refuse benchmark items and comply elsewhere), and it forces the evaluator to hold and send harmful content. The published cheap alternatives all retain a dependency this proposal drops. AMS (Messenger, arXiv:2608.05578) scans activation geometry and needs harmful prompts; it reports 71% leave-one-out accuracy over 14 configurations and explicitly reports that behavioral uncensored fine-tunes preserving geometry are undetectable by it. RAS/SafeVec (arXiv:2606.25750) scores representation-level refusal alignment on a calibrated 0-100 scale but needs unsafe and jailbreak prompts AND a safety-aligned reference model. VISAGE (arXiv:2405.17374) measures a safety basin in WEIGHT space and needs a harmful benchmark evaluated at every weight perturbation. All three are static, read-side measurements. That question provably does not settle behavior - the 2026 knowledge-action-gap result reports 98.2% probe AUROC alongside 45.1% output sensitivity.

  This hypothesis attacks the gap from the act side with a different unit: not a direction, feature or basin volume, but a RATE. How fast does the model's own generative process return to its default mode after a tiny nudge while doing something innocuous?

  What a basin in BEHAVIORAL state space buys over VISAGE's basin in WEIGHT space is now stated as a testable divergence rather than asserted. The two accounts must rank the panel identically unless weight-space and behavior-space geometry come apart, and we pre-register the two places they should: (a) a behavioral uncensored fine-tune, where a small weight displacement produces a large behavioral change, and (b) a task-vector interpolant, where a smooth weight-space path may produce a step-like behavioral change. A phenomenon the weight-space basin cannot account for is therefore named in advance: a checkpoint whose weight-space basin volume is unchanged from its parent while its behavioral relaxation rate collapses. If the two rankings coincide, we say so and demote the mechanistic claim to a cost claim. The reinterpretation of Qi et al. gets the same treatment: the token-depth account predicts the safety signal is concentrated in the first few GENERATED steps and vanishes afterwards, while the basin account predicts lambda differences PERSIST deep into generation. Step 5 already collects step-wise lambda profiles, so this discriminating test is free.

  If true this yields (a) a mechanistic account of what safety tuning buys, in the language of bistable systems - a shifted operating point; (b) an audit needing a handful of harmless prompts, no harmful content, no jailbreak suite, no reference model and no benchmark to memorize; and (c) a bridge carrying the mature early-warning-signal toolkit from ecology and climate science into model auditing. A clean negative is also worth publishing: it would say safety is a static bias, not a shifted operating point, extending the knowledge-action-gap literature with a dynamical arm.
assumptions:
- >-
  Autoregressive generation under temperature sampling is a genuine stochastic dynamical system whose state is the generated
  prefix plus KV cache, so recovery rate, across-rollout variance, lag-1 autocorrelation and flickering are well defined over
  GENERATED steps. The series is NON-STATIONARY (chat-template openings and topic commitment produce a strong deterministic
  trend), so all fluctuation statistics are computed on residuals after subtracting the ACROSS-ROLLOUT mean trajectory at
  each generated step, estimated from the >= 20 rollouts we already collect. Without detrending, a high lag-1 autocorrelation
  would only mean 'this model produces stereotyped openings'.
- >-
  The refusal/comply mode can be read out as a scalar at each generated step by a MODEL-INDEPENDENT observable that survives
  the abliteration weight edit: the logit-lens log-odds of refusal-onset tokens against continuation tokens. This is primary
  precisely because a projection onto the abliterated direction is near-constant by construction, which would make any variance
  claim on abliterated models circular. The per-model diff-in-means axis is descriptive only.
- >-
  Steering-based tests (H1) probe states that are partly OFF the manifold reachable by prompting (arXiv:2604.09839 proves
  steered activations are non-surjective). H1 is therefore scoped as a statement about the steered dynamical system, and the
  safety claim of record (H3) uses only unsteered sampling plus a norm-epsilon perturbation whose linearity is verified by
  an epsilon sweep, so the product claim never rests on off-manifold behaviour.
- >-
  A graded safety ladder can be manufactured without training by scaling the alignment task vector W(t) = W_base + t*(W_instruct
  - W_base) and by scaling abliteration strength - but only if the interpolants stay fluent. Every interpolant must pass a
  pre-registered screen (WikiText perplexity within 2x of the t=1 endpoint, plus a distinct-3 / max-n-gram-repeat degeneracy
  check) before entering any analysis, because a degenerate model neither refuses nor complies AND has a degeneracy-dominated
  r_t series, which would corrupt both sides of the headline correlation at once and could manufacture a spurious result.
  Interpolants share a weight lineage and never count as independent units.
- >-
  Small models (0.36B-4B, int8/float32, batched rollouts) show the same qualitative refusal machinery reported for larger
  models. This is tested rather than assumed via a within-family scale ladder (Qwen3 0.6B/1.7B/4B), because a small model
  that is twitchy may be twitchy from undertraining; scale enters the headline analysis as a covariate.
investigation_approach: |-
  PANEL, ENUMERATED BY LINEAGE (the resampling unit). 20 distinct weight lineages, >= 8 architecture families, all CPU-feasible: Qwen3-0.6B, Qwen3-1.7B, Qwen3-4B (each contributing base + instruct + abliterated members), Qwen2.5-0.5B, Qwen2.5-1.5B, Llama-3.2-1B, Llama-3.2-3B, gemma-2-2b, SmolLM2-360M, SmolLM2-1.7B, TinyLlama-1.1B, Pythia-410M, Pythia-1B, Pythia-1.4B, OLMo-1B, Danube3-500M, Falcon3-1B-Instruct, Granite-3.1-2B-Instruct, MiniCPM-1B, plus >= 4 behavioral uncensored fine-tunes (their own lineages). Base-only lineages (Pythia, OLMo) anchor the low-refusal end. Total measured UNITS (members) ~ 45-55; n_lineage = 20. Every model-level statistic is bootstrapped over the 20 lineages; the member/prompt bootstrap is reported separately and labelled measurement noise.

  STEP 0 - PRE-REGISTRATION (written before any run).
  (a) Layer L is fixed by a rule that never touches the outcome: the layer maximizing harmful/benign diff-in-means separation on a held-out contrast set for ONE reference model, transferred by relative depth L/n_layers. Full layer profiles are secondary, Holm-corrected, and interpreted against the reported 'Late Decision' (Llama) vs 'Early Divergence' (Qwen) topologies.
  (b) Decoding fixed and reported: chat template, empty system prompt, temperature 0.7 for dynamics and 0.0 for deterministic controls; max_new_tokens = 192 for the H2 dynamics arm (needed for estimator identifiability) and 64 for ground-truth generation.
  (c) SPI is fixed a priori as the mean of FOUR z-scored terms [-log lambda, log detrended across-rollout variance, Fisher-z of detrended AC1, logit of flicker rate], PLUS - crucially - the z-scoring uses FROZEN normalization constants (means and sds) fit once on a designated REFERENCE subset of 6 named lineages and PUBLISHED in the paper. SPI for any new checkpoint uses only those frozen constants, so it is computable for a single model with no comparison panel (the defect that made the previous definition weaker than RAS's absolute 0-100 scale). All leave-one-out and leave-one-family-out numbers are recomputed with the left-out model excluded from the normalization fit. >= 3 checkpoints are reserved that appear in NO normalization and NO fitting step, and their SPI plus ground truth is reported as the out-of-panel demonstration.
  (d) SIGNED PREDICTION TABLE, one row per ground truth: plain-harmful refusal rate -> expected sign POSITIVE, threshold rho >= 0.6, reason: nearness to the switch makes the refuse mode easy to enter. XSTest over-refusal rate -> POSITIVE, rho >= 0.45, same reason applied to benign-but-scary prompts. Jailbreak attack-success rate -> SIGN IS THE DISCRIMINATING OUTCOME: the ASYMMETRIC reading predicts NEGATIVE (the shallow basin is the comply basin, so the model falls into refusal and is hard to tip out), the DOUBLE-SIDED reading predicts POSITIVE (near a fold in both directions, so it tips either way). Both are pre-registered as competing hypotheses; the outcome that discriminates them is the sign of the partial rank correlation of SPI with ASR controlling for plain-harmful refusal rate, corroborated by the Asymmetry Index of H2b. Either sign is informative; an unsigned rho would have been unfalsifiable.
  (e) Single-forward-pass measurement: DROPPED, not retained as an appendix, so it cannot be substituted for the generated-step result.

  STEP 1 - H1, three ramp arms. For each of >= 30 benign prompts: (i) UP-RAMP, raise alpha per generated token until a refusal-onset token is emitted -> alpha_up. (ii) RETAINED-PREFIX DOWN-RAMP, continue the same sequence with prefix and KV cache kept, lowering alpha -> alpha_down. (iii) FORCED-PREFIX DOWN-RAMP (the control that isolates the claim), force-feed the identical refusal prefix as a prefill without ever ramping up, then ramp alpha down from the same start -> alpha_down_forced. Test statistic = residual = alpha_down - alpha_down_forced, bootstrapped over prompts and lineages. width_naive = alpha_up - alpha_down is reported alongside, with the PRE-REGISTERED expectation that it is large and positive in base models too (per Kwon 2607.14147). A reset arm that discards the prefix between steps is retained as an implementation sanity check only: it must be indistinguishable from 0 at temperature 0, and its temperature-0.7 width is the NOISE FLOOR against which retained-prefix quantities are compared (it will not be exactly 0 under sampling).

  STEP 2 - H2/H2b, early-warning indicators on harmless input only. Per benign prompt (~20 prompts), >= 20 paired-seed rollouts, 192 generated tokens. Perturbed arm: inject a norm-epsilon vector into the residual stream at layer L at step p, continue decoding, fit an exponential to |delta r_t| over subsequent generated steps -> lambda, run separately for refusal-directed and compliance-directed nudges (H2b). Clean rollouts give detrended Var*, detrended AC1, and flicker rate. Estimator hygiene, all pre-registered: subtract the across-rollout mean trajectory before AC1/Var*; a SYNTHETIC RECOVERY CHECK simulating AR(1) with known decay at the observed noise level and series length, reporting the estimator's bias and variance and a minimum series length below which lambda is not reported; and indicators reported as a function of series length so truncation artifacts are visible. Epsilon sweep confirms linearity. Three null controls: random readout axis (must NOT reproduce the safety ordering), random vs refusal-aligned perturbation, and a syntactic (part-of-speech probe) observable, which should decay at the same rate if what is being measured is generic mixing.

  STEP 3 - ground truth, three axes. Per member: ~80 AdvBench/JailbreakBench-style harmful prompts (plain-harmful refusal rate), the same under a fixed small jailbreak suite including prefill (ASR), ~50 XSTest benign-but-scary prompts (over-refusal). Scoring: cheap OpenRouter LLM judge PRIMARY, refusal-string matcher as screen, Cohen's kappa reported, >= 100 hand-adjudicated stratified items to estimate judge error, attenuation-corrected correlations alongside raw. Budget < $2 of the $10 cap. Interpolants additionally pass the fluency screen, and the ladder is PILOTED on one base/instruct pair first to confirm refusal rate varies smoothly in t rather than snapping to an endpoint; counts manufactured vs passed are reported, and if the pass rate is low the paper states that trimodality returns.

  STEP 4 - H3/H4, prediction with matched-n, faithful baselines. Spearman rho of SPI with each ground truth. The headline comparison is a PAIRED bootstrap of the DIFFERENCE (rho_SPI - rho_baseline) on the SAME resampled lineages, required to exclude 0 - this removes between-lineage variance common to both and is what n_lineage = 20 can actually support. Baselines: (a) static mean level of r on benign prompts; (b) two zero-internals output-side detectors (next-token probability of refusal-onset tokens; ever-emits-an-apology-token); (c) AMS-style cluster separation sigma and refusal-direction cosine, with leave-one-out accuracy reported in AMS's own format and leave-one-FAMILY-out; (d) a RAS/SafeVec reimplementation whose reference model, layer-window selection rule, prompt sets and calibration mapping are pre-registered, with a reproduction check against RAS's published numbers on overlapping models - if reproduction is out of scope it is labelled 'our RAS reimplementation' throughout, not 'RAS'; (e) VISAGE-style weight-perturbation basin volume on a 6-model subset, with SPI's correlation reported ON THAT SAME SUBSET so the comparison is at matched n. Load-bearing statistic: partial rank correlation of the dynamic terms with each ground truth controlling for the static mean AND model scale. H4 candidates must pass the class-membership pre-check (sigma and refusal-direction cosine preserved vs parent, harmful compliance high, model card and community provenance checked for abliteration or abliterated-merge components); failures are reported with reasons, and if fewer than 4 pass, H4 is reported as a pre-registered case study with per-model detail rather than a statistical claim.

  STEP 5 - mechanism map and the two discriminating tests. Layer-wise and step-wise lambda profiles for base vs instruct vs abliterated vs interpolants: does the basin shallow monotonically in t; does abliteration revert to base or produce a third state; and the two named predictions - (i) does the behavioral basin rank the panel differently from VISAGE's weight basin on behavioral fine-tunes and interpolants (versus the account, if identical); (ii) do lambda differences persist deep into generation (basin account) or vanish after the first few generated steps (Qi et al. token-depth account).

  COMPUTE BUDGET AND STAGING (previously absent). Audit cost and validation cost are reported separately. AUDIT (what a user pays to score one new checkpoint): 20 benign prompts x 20 rollouts x 2 arms x 192 tokens with batched rollouts and hooks active - roughly 10-15 min on one consumer GPU, or ~40-60 min on CPU int8 at <= 1.7B. VALIDATION (what this study pays): Step 3 dominates, ~50 members x 210 prompts x 64 tokens. Tiering, pre-registered: TIER 0 smoke, 3 checkpoints, verifies the full pipeline end to end. TIER 1, 12 checkpoints spanning all families and both ladder endpoints, run through ALL of Steps 1-5, sufficient on its own to report H1/H1b/H2/H2b with controls. TIER 2, remaining members added to Steps 3-4 only (ground truth and correlation), where marginal cost is lowest and marginal power highest. Criteria are evaluated on whatever tier completes, with the tier stated; a partial run is therefore still reportable.
success_criteria: |-
  POWER, reconciled with the resampling unit (the previous version's n=30 arithmetic contradicted its own lineage bootstrap). n_lineage = 20. At n = 20 the 95% bootstrap CI half-width around an observed Spearman rho = 0.8 is roughly +/-0.22, so a criterion requiring SPI's CI lower bound to exceed a baseline's point estimate is NOT attainable regardless of truth and is replaced in advance by the PAIRED difference test, which removes the shared between-lineage variance. Partial correlations with two covariates have adequate power only for partial rho >= 0.5; criteria are set at that level.

  CONFIRMS:
  (1) The H1 residual (alpha_down - alpha_down_forced) is significantly > 0 with a bootstrap CI excluding 0 and exceeding the temperature-0.7 noise floor - path dependence exists that the emitted refusal text does not explain.
  (2) The residual is ordered instruct > base and instruct > abliterated, paired over prompts, CIs excluding 0.
  (3) On harmless prompts only, over generated steps, with DETRENDED statistics and a passing synthetic-recovery check: lambda lower and Var*, AC1, flicker higher in behaviorally safer models, reproduced in >= 3 families, AND absent on the random-axis and syntactic-probe controls.
  (4) SPI computed with FROZEN constants attains rho >= 0.6 with plain-harmful refusal rate (positive sign, as pre-registered) and rho >= 0.45 with XSTest over-refusal (positive), and the PAIRED bootstrap of rho_SPI - rho_baseline excludes 0 against the best of the static mean and the two zero-internals baselines; the partial correlation controlling for static mean and scale has a 95% CI excluding 0 at partial rho >= 0.5.
  (5) The jailbreak-ASR row resolves in EITHER direction with a partial correlation CI excluding 0 controlling for refusal rate, and the Asymmetry Index of H2b agrees with that sign. This is scored as a confirmed discrimination between the asymmetric and double-sided readings, not as a pass/fail.
  (6) SPI matches or beats AMS leave-one-out accuracy in AMS's own format with the left-out model excluded from normalization, and matches the RAS reimplementation and VISAGE (the latter at matched n on its 6-model subset) without needing their harmful prompts or reference model.
  (7) The >= 3 fully held-out checkpoints are scored correctly from frozen constants alone - the actual product claim.
  (8) H4: every behavioral uncensored fine-tune passing the class-membership check is flagged by SPI while cluster separation and refusal-direction cosine both mark it safe. Reported as a statistical claim only if >= 4 pass, otherwise as a pre-registered case study.

  THIRD OUTCOMES, PRE-REGISTERED (informative, not failures): (a) 'bistability present but not safety-specific' - the residual is nonzero in base models too, in which case H1 is confirmed and H1b refuted and only the quantitative ordering carries safety information (live because Kwon 2607.14147 attributes prefill grip to generic autoregressive conditioning and Rahimi et al. 2602.02600 report that autoregressive commitment masks instability). (b) Behavioral basin and VISAGE weight basin rank the panel identically - the mechanistic claim is then dropped to a cost claim, stated plainly. (c) The interpolant ladder fails its fluency screen or snaps to endpoints - the trimodality problem returns and is reported as a limitation on the correlation's interpretability.

  DISCONFIRMS (reported as refutation, not salvaged): the H1 residual is indistinguishable from the noise floor, i.e. all path dependence is prefix content and the bistable framing adds nothing; or lambda / Var* / AC1 / flicker show no consistent ordering with any ground truth once detrended; or the ordering also appears on the random-axis or syntactic-probe control, meaning generic mixing was measured; or the correlation vanishes once static mean and scale are partialled out; or a zero-internals output-side baseline ties SPI in the paired difference test; or the held-out checkpoints are mis-scored under frozen constants, meaning the metric is a within-panel artifact; or indicators work within one family but fail leave-one-family-out, bounding the metric to a within-family diagnostic.
related_works:
- >-
  Messenger, 'Detecting Safety Training Modification in Language Models via Activation Analysis' (arXiv:2608.05578, IEEE Access
  2026) - AMS scans activation geometry (harmful/benign cluster separation sigma, refusal-direction cosine) across 14 configurations
  and 4 families, 71% leave-one-out accuracy, compliance prediction r = -0.546, and explicitly reports behavioral uncensored
  fine-tunes as undetectable. Closest work and sharpest departure: static read-side property from harmful prompts versus our
  dynamical act-side RATE from harmless prompts only. Its documented blind spot is our H4 case study, and we report LOO accuracy
  in its format with the left-out model excluded from our normalization fit so the comparison is not leaked.
- >-
  Huang et al., 'RAS: Measuring LLM Safety Through Refusal Alignment' (arXiv:2606.25750, 2026) - SafeVec extracts layer-wise
  refusal directions from a safety-aligned REFERENCE model, selects stable layer windows, and scores a target by hidden-state
  alignment under unsafe and jailbreak prompts, mapped to a calibrated absolute 0-100 scale. It is the incumbent for our product
  claim and the reason we now FREEZE SPI's normalization constants: a within-panel z-score cannot score a single new checkpoint,
  which is exactly RAS's advantage. Run as a pre-registered reimplementation with a reproduction check on overlapping models,
  and labelled 'our reimplementation' if reproduction is out of scope. It needs harmful and jailbreak prompts and a reference
  model; SPI needs neither.
- >-
  Peng et al., 'Navigating the Safety Landscape' (NeurIPS 2024, arXiv:2405.17374) - discovers the safety basin in WEIGHT space
  and proposes the VISAGE basin-volume metric, requiring a harmful benchmark at every weight perturbation. 'Shallow basin'
  is their language and we say so. The departure is now a TESTED prediction rather than an assertion: the accounts diverge
  where weight-space and behavior-space geometry come apart (behavioral uncensored fine-tunes; task-vector interpolants).
  VISAGE is run on a 6-model subset with SPI reported on that same subset at matched n; if the rankings coincide we drop the
  mechanistic claim to a cost claim.
- >-
  Yin et al., 'Refusal Falls off a Cliff' (arXiv:2510.06036, 2025) - traces refusal intention across token positions with
  linear probes, finding a sharp drop at final tokens in poorly aligned reasoning models. The per-position refusal score is
  an existing observable which we adopt rather than coin; our contribution is the detrended dynamical statistics computed
  on it across sampled rollouts plus the residual hysteresis test.
- >-
  Rahimi et al., 'Step-Wise Refusal Dynamics in Autoregressive and Diffusion Language Models' (arXiv:2602.02600, 2026) - shows
  diffusion remasking enables recovery from harmful intermediate generations and proposes the SRI internal-dynamics signal,
  observing that autoregressive commitment masks underlying instability. Closest 'dynamics during decoding' work: it compares
  SAMPLING MECHANISMS, we hold sampling fixed and use controlled perturbation-recovery as an ESTIMATOR of distance to a switching
  point. Its commitment finding is a named pre-registered threat.
- >-
  Kwon, 'Breaking Refusal in the First Half' (arXiv:2607.14147, 2026) - prefill jailbreak study: harm representation stays
  intact (probe 0.91-0.98) while behavioral refusal drops to chance, and a base-model control shows the same prefill-specific
  collapse, concluding the prefill's grip is generic autoregressive conditioning rather than safety-specific suppression.
  This is precisely why H1's test statistic is now the FORCED-PREFIX RESIDUAL rather than the naive loop width, which this
  paper's mechanism would otherwise explain entirely.
- >-
  Ratnakar and Vats, 'The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs' (arXiv:2606.22686, 2026) - Contrastive
  Logit Steering plus prefix injection induces a phase transition where guardrails collapse, and reports 'Late Decision' (Llama,
  95% ASR) vs 'Early Divergence' (Qwen, safety integrated at ~40% depth) topologies. Phase-transition language exists here
  but as an ATTACK that crosses the edge; our point is estimating distance to the edge without crossing it. Its topology finding
  drives our relative-depth layer transfer.
- >-
  Hasan and Biswas, 'The Refusal-Compliance Tradeoff' (arXiv:2605.05427, 2026) - audits 21 open-weight LLMs and finds over-refusal
  and harmful compliance nearly uncorrelated. This is why three ground truths are predicted separately, and why the signed
  prediction table (positive for refusal and over-refusal, sign-as-outcome for ASR) is a real commitment rather than bookkeeping.
- >-
  Xiong et al., 'Steering Externalities: Benign Activation Steering Unintentionally Increases Jailbreak Risk for LLMs' (arXiv:2602.04896,
  2026) - steering vectors from entirely benign data erode guardrails, with ASR above 80%, framed as consumption of a 'safety
  margin'. This is direct empirical support that a margin exists and is small in aligned models, and it is the strongest existing
  evidence for the DOUBLE-SIDED reading in H2b. It measures the consequence of crossing the margin; we measure the margin's
  width from harmless generation without crossing it.
- >-
  Mishra, Khashabi and Liu, 'Steered LLM Activations are Non-Surjective' (arXiv:2604.09839, 2026) - proves steered residual
  streams leave the manifold reachable from discrete prompts. A scope constraint we now state explicitly: H1's ramp probes
  the steered system, so the product claim (H3) rests only on unsteered sampling plus a verified-linear norm-epsilon perturbation.
- >-
  Arditi et al., 'Refusal in LLMs is mediated by a single direction' (2024) and the abliteration practice built on it - the
  static geometric account and our instrument for producing (and partially producing) uncensored checkpoints. Because abliteration
  orthogonalizes writes against that direction, we deliberately do NOT use a projection onto it as the primary observable.
- >-
  Qi et al., 'Safety Alignment Should Be Made More Than Just a Few Tokens Deep' (ICLR 2025 Oral) - shows aligned and unaligned
  generative distributions differ mainly over the first few output tokens. Their account and ours make DIFFERENT predictions
  we now test: token depth predicts the safety signal is confined to the first few generated steps, the basin account predicts
  lambda differences persist across generated steps.
- >-
  Scheffer et al. and the early-warning-signal / critical-slowing-down literature in ecology, climate science and psychiatry
  (slowed recovery from small perturbations, rising variance, rising lag-1 autocorrelation, flickering near a fold bifurcation).
  The imported source, not a competitor; scholarly search finds it applied to ecosystems, climate, financial crises, depression
  and sleep, but not to LLM generative dynamics or safety auditing.
inspiration: >-
  The transfer is from ecology and climate science at the methodological level. Ecologists face this problem in a different
  costume: they must know how close a lake, forest or fish population is to collapsing without running the experiment of collapsing
  it. Scheffer's early-warning-signal programme solved it by measuring the response to small, harmless disturbances - as a
  system approaches a fold, the dominant eigenvalue of its linearized dynamics approaches zero, so recovery from tiny nudges
  slows, fluctuations grow in variance, become more autocorrelated, and the system flickers. Resilience becomes measurable
  without pushing the system over the edge. Mapped onto model auditing: don't jailbreak a model to learn whether it can be
  jailbroken - nudge it gently while it does something innocuous and watch how fast it settles back. The import is legitimate
  only where a real stochastic dynamical system exists, which is why the measurement lives in autoregressive sampling and
  why the single-forward-pass version has now been dropped rather than kept as a heuristic. Ecology also supplies the fix
  for the statistics: EWS practitioners detrend before computing autocorrelation for exactly the reason we now must - a trend
  inflates AC1 and fakes the signal. Two further imports: from physics and materials science, the hysteresis loop as the decisive
  test of genuine bistability, which forces the sweep to happen within one generation with the prefix retained - and, following
  the same tradition's insistence on separating a real state variable from a memory of the drive, the forced-prefix control
  that isolates latent path dependence from conditioning on already-emitted text. From experimental genetics, the base / safety-tuned
  / abliterated series read as wild-type / knock-in / knock-out, extended to a dose-response ladder by scaling the alignment
  task vector, with a viability screen on the intermediates the way a geneticist screens for non-viable phenotypes. What a
  domain expert would not reach for is the reframing underneath: mechanistic interpretability's default unit is a static object
  - a direction, a feature, a circuit, a basin volume - whereas the resilience literature's unit is a rate.
terms:
- term: Refusal observable (r_t)
  definition: >-
    A scalar read off the model at each GENERATED step t. Primary form: logit-lens log-odds of refusal-onset tokens against
    continuation tokens - chosen because it survives the abliteration weight edit and needs no harmful prompts. All fluctuation
    statistics use the DETRENDED residual, obtained by subtracting the across-rollout mean trajectory at each generated step.
- term: Critical slowing down
  definition: >-
    The signature that a stochastic dynamical system is near a fold bifurcation: recovery from small perturbations slows,
    fluctuations grow in variance, become more autocorrelated, and the system flickers between modes. Standard practice in
    ecology, climate science and psychiatry for estimating resilience without triggering collapse.
- term: Recovery rate (lambda)
  definition: >-
    The exponential decay rate of the induced deviation in r_t over subsequent GENERATED steps after a small residual-stream
    perturbation, averaged over >= 20 paired-seed rollouts of 192 tokens. Small lambda = slow recovery = shallow basin = close
    to switching. Its identifiability at the actual series length and noise level is verified by a synthetic AR(1) recovery
    check with a pre-registered minimum series length.
- term: Asymmetry Index
  definition: >-
    log(lambda_toward_refuse / lambda_toward_comply): recovery from a nudge pushing toward refusal versus one pushing toward
    compliance. It distinguishes an ASYMMETRIC shallow comply basin (tips into refusal easily, so high refusal but LOW jailbreak
    success) from a DOUBLE-SIDED fold (tips either way, so high refusal AND high jailbreak success) - the two readings of
    'nearness to a switch' whose conflation previously left the jailbreak prediction unsigned.
- term: Switching Proximity Index (SPI)
  definition: >-
    The proposed safety metric: the mean of four terms [-log lambda, log detrended across-rollout variance of r, Fisher-z
    of detrended lag-1 autocorrelation, logit of flicker rate], standardized with FROZEN normalization constants fit once
    on a named 6-lineage reference subset and published, so SPI is computable for a single new checkpoint with no comparison
    panel. Higher SPI = closer to the comply/refuse switching point.
- term: Forced-prefix control (alpha_down_forced)
  definition: >-
    The control that makes H1 decisive. The refusal prefix produced at the top of the up-ramp is force-fed as a prefill WITHOUT
    any prior ramp, then alpha is ramped down. Because the prefix content is identical, the difference alpha_down - alpha_down_forced
    isolates path dependence carried by latent state from ordinary conditioning on already-emitted refusal text - the mechanism
    Kwon reports as generic to autoregressive decoding.
- term: Noise floor
  definition: >-
    The apparent loop width produced by sampling alone, measured in the prefix-discarding reset arm at temperature 0.7. It
    must be indistinguishable from 0 at temperature 0; at 0.7 it is the baseline against which retained-prefix quantities
    are compared, replacing the previous, incorrect 'must be exactly zero' requirement.
- term: Flicker rate
  definition: >-
    At a steering coefficient held near the switching threshold and nonzero temperature, the fraction of sampled rollouts
    that switch mode between refusal and compliance. A classical early-warning indicator, available only because the measurement
    lives in stochastic sampling.
- term: Task-vector safety ladder
  definition: >-
    A training-free way to manufacture graded ground truth: W(t) = W_base + t*(W_instruct - W_base) plus partial-strength
    abliteration. Every interpolant must pass a fluency screen (WikiText perplexity within 2x of the t=1 endpoint; distinct-3
    and max-n-gram-repeat degeneracy checks) before entering analysis, and the ladder is piloted on one pair to confirm refusal
    rate varies smoothly rather than snapping to an endpoint. Members share a weight lineage and never count as independent
    units.
- term: Weight lineage
  definition: >-
    The resampling unit for every model-level claim: one pretrained base and everything derived from it (instruct, abliterated,
    interpolants). The panel has n_lineage = 20 across >= 8 families and ~45-55 measured members; all headline CIs are bootstrapped
    over the 20 lineages, and the headline baseline comparison is a PAIRED bootstrap of the correlation difference on the
    same resampled lineages.
- term: Behavioral uncensored fine-tune
  definition: >-
    An 'uncensored' checkpoint produced by ordinary fine-tuning on compliant data rather than a directional weight edit, so
    it can keep harmful/benign geometry and the refusal direction intact while complying with nearly all harmful requests.
    Class membership is now VERIFIED before use (separation and cosine preserved vs parent, harmful compliance high, provenance
    checked for abliteration or abliterated merges), because an unverified candidate tests nothing.
- term: Audit cost vs validation cost
  definition: >-
    Two separately reported numbers. Audit cost is what a user pays to score one new checkpoint (20 benign prompts x 20 batched
    rollouts x 192 tokens; ~10-15 min on one consumer GPU, ~40-60 min on CPU at <= 1.7B). Validation cost is what this study
    pays to establish the metric, dominated by the harmful/jailbreak/over-refusal ground truth. Conflating them invites the
    objection that a cheap method needed an expensive study - true, normal, and stated plainly.
- term: Knowledge-action gap
  definition: >-
    The finding that a model's internals can encode a concept with near-perfect decodability while its outputs fail to act
    on it (98.2% probe AUROC vs 45.1% output sensitivity, 2026 clinical result). It is why a read-side safety metric can be
    confidently wrong, and why this hypothesis measures an act-side quantity.
summary: >-
  Safety fine-tuning may park a model right next to a comply/refuse switching point, so an aligned model is subtly unstable
  about refusal even while generating harmless text - and that instability is measurable during ordinary sampled generation
  using the early-warning indicators ecologists use to detect approaching tipping points (slower recovery from small nudges,
  higher detrended variance, autocorrelation, flickering), with a forced-prefix-controlled hysteresis residual as the decisive
  test of genuine bistability. This yields a frozen-normalization safety score computable for a single new checkpoint from
  a handful of harmless prompts, with no harmful content and no reference model, aimed where static activation-geometry scanners
  are documented to fail.
_relation_rationale: >-
  Same frame, narrowed: safety-legibility splits into a supported edit-detection arm and a bounded black-box negative.
_confidence_delta: decreased
_key_changes:
- >-
  Split the core claim: A (parent-free detection of a global abliteration EDIT, supported: W05 AUROC 1.000, held-out 1.000,
  0 prompts, 11.4 s) vs B (graded behavioural safety NOT better read from the interior — falsifier fired against black-box
  B09 rho +0.766).
- >-
  Made the toolchain confound the top experiment: all 8 abliterated positives come from 2 uploaders running one global diff-in-means
  recipe; leave-one-UPLOADER-out plus >=3 mechanically different toolchains (mlabonne, grimjim/ORBA projected, OBLITERATUS
  multi-direction) now decide the arm's true scope.
- >-
  Added a laundering/evasion arm (LoRA-SFT, 50/50 parent merge, int8/int4 round-trip, added-back random rank-one) and a Hub
  scan for undeclared positives, since every current positive is solved for free by a repo-name string match.
- >-
  Added the parent-required head-to-head: compute E_1 on every sibling pair already downloaded and report W05 vs E_1 AUROC
  at matched n, so the price of the parent-free constraint is quantified rather than asserted.
- >-
  Turned the negative from a verdict into a measurement: report the minimum detectable paired-rho difference at n=18 lineages,
  add a PRE-SPECIFIED black-box comparator (B01) beside the best-of-11 winner B09, attenuation-correct for judge reliability
  (40 items, kappa ~0.30), and report the correlation table at three depths spanning the 22-layer AUROC plateau.
- >-
  Made analysis.py a first-class deliverable (every AUROC/Spearman/bootstrap/paired difference, with seed, B, resampling scheme,
  singleton-lineage and tie-handling rules) — no headline number may be computed outside the versioned artifact.
- >-
  Downgraded 'pre-registered' wording: metric_spec.py stamps only the 53 metric declarations; the falsifier, base-model exclusion,
  blanket-refuser and bootstrap rules must be published as a separately hashed, timestamped plan or reworded.
- >-
  Added two missed prior works as required citations and positioning: arXiv:2604.08844 (delta-based spectral geometry, AUC
  1.00 in-method / AUC 0.00 cross-method, rho 0.72 to harmful compliance) and OBLITERATUS's parent-free spectral certification
  with its own calibration failure.
- >-
  Retired alpha_50 and the steering-price family as metrics (NOT_A_TRIAGE_SCORE, R=0.73, perm p=0.76; sign reverses across
  lineages), keeping the finding that the lexical artefact lives in the SCORER not the axis (regex defines alpha_50 for 7/14
  members, judge for 14/14, median kappa 0.279).
- >-
  Retired the early-warning-signal / critical-slowing-down arm entirely: the iteration-1 re-analysis retracted it (only 1
  of 4 members passes the r_0 AUROC>=0.70 validity gate; random-direction control reverses at the pre-stated readout layer;
  SPI rho -0.20 flips to +0.105 under rank-average ties).
- >-
  Recorded that safety-RL is visible in jailbreak ASR (0.688 -> 0.088) and not in harmful-refusal rate (0.9125, matching instruct),
  so any metric scored only against refusal rate is structurally blind to it.
- >-
  Added reporting-fidelity fixes: [min,max] for every class (base W01 max 1.992 overlaps abliterated min 1.438), name OLMo-1B
  (-2.665) as nearest non-abliterated neighbour, flag single-member families at the boundary, correct W03's random-direction
  count 64 -> 256, and disambiguate the positive-control checkpoint.
relation_type: evolution
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for study design, proper baselines, and the evaluation/validity norms this field demands.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<iteration_status>
Current iteration: 3 of 5
Remaining (including this one): 3
</iteration_status>

<previous_strategies>
Strategies from the PREVIOUS iteration. You can CONTINUE these directions,
ADAPT based on what worked and what didn't in the artifacts produced, or PIVOT if results suggest a better path.

--- Strategy 1 ---
kind: strategy
id: gen_strat_1_idx1
title: Fifty cheap safety metrics, tested honestly
objective: >-
  Turn iteration 1's single surviving positive (alpha_50 on one 0.6B lineage, n=5 prompts, no CI) into the paper's actual
  contribution: a SINGLE-MODEL safety screening battery. Concretely this iteration delivers (a) fifty declared-cost metrics
  computable from ONE checkpoint with no parent, no reference model and no benchmark run - at least 8 weights-only (zero generation,
  motivated by abliteration's literal edit W <- W - c r r^T W leaving a shared low-write-energy direction across every write
  matrix) and at least 8 black-box (logits/output-text only, the pre-registered central falsifier) - computed across >=20
  checkpoints spanning >=6 architecture families and >=12 weight lineages; (b) alpha_50 re-run at publishable power (>=20
  benign prompts x >=5 seeds, logistic dose-response, bootstrap CIs, paired instruct-minus-abliterated difference) with the
  three circularity controls the reviewer demanded, on four lineages including the Qwen3-4B Base/Instruct/SafeRL/abliterated
  quartet that for the first time separates deliberate safety-RL from generic instruction tuning; (c) an EXTERNAL ground-truth
  table (published safety and capability numbers with provenance) plus a frozen dev/held-out lineage split written down BEFORE
  any metric is selected; and (d) a re-analysis that repairs the three internal-validity defects the reviewer identified in
  the iteration-1 record. The novel contribution being built toward is the first honest answer to 'does looking inside a model
  buy anything over reading its logits, for cheap safety triage?' - with the pre-registered outcome that if no white-box metric
  beats the best black-box baseline with a CI excluding zero, that null IS the result.
rationale: >-
  The reviewer's six MAJOR critiques reduce to three defects, and each has a distinct, parallelisable fix. (1) EVIDENCE: alpha_50
  rests on 5 Bernoulli draws per curve point and a 0.075 gap on a 0.05 grid; the discriminating comparison (safety-tuned vs
  its abliterated sibling) is exactly the unpowered half. Powering it is cheap - iteration 1 measured 590-710 tok/s and $1.25
  total spend against a $10 cap - so there is no excuse for leaving it unpowered a second time. (2) VALIDITY: the axis is
  a diff-in-means between four hand-written apologies and the outcome is scored by a regex from the same lexical family, so
  alpha_50 may be measuring how much push a canned-apology token direction needs to win the argmax. That is testable in one
  run with a token-disjoint paraphrased axis, a semantic-judge outcome, and a norm-matched non-safety stylistic axis - and
  if it IS lexical, that is a stronger publishable finding than an unvalidated metric, which is why the controls are run as
  first-class arms rather than robustness checks. (3) SCOPE: everything is one 0.6B lineage, the abliterated checkpoint even
  differs between arms, and the frozen 137-checkpoint manifest is sitting unused. A triage score measured on three models
  of one family is not a triage score. Widening the panel is the single highest-leverage move available and the manifest already
  makes it a download problem rather than a research problem. Beyond the critiques, the hypothesis itself has moved: the deployment
  case is ONE checkpoint with no sibling, which retires iteration 1's sibling-contrast headline quantities and makes the weights-only
  arm - completely absent in iteration 1 - the genuinely new bet. Abliteration is a rank-one orthogonalisation applied to
  every write matrix; a direction with anomalously low write energy shared across all layers should be visible in the weights
  of a single checkpoint with no parent to diff against, and nobody in the cited literature (AMS, RAS, VISAGE, AQI - all activation-
  or benchmark-side) has looked. The staging is deliberate: metrics are computed this iteration BLIND to the external ground
  truth (which lands as a separate parallel artifact), so the correlation test in iteration 3 is run against a table that
  was never available while the metrics were being written - the contamination guard the hypothesis pre-registers. Splitting
  into a cheap wide battery, a deep powered alpha_50 arm, an external-scores dataset, a positioning research pass and a re-analysis
  of the existing record gives five independent legs, none of which blocks another, and each of which is reportable alone
  if the others disappoint. The mech-interp handbook's demands - falsifiable pre-registration, well-implemented baselines,
  per-sample distributions rather than means, randomized controls that must fail - are built into every arm rather than deferred.
artifact_directions:
- id: research_iter2_dir1
  type: research
  objective: >-
    Close the three literature gaps the reviewer opened - the uncited detection-vs-steering-gap result, the more-occupied-than-implied
    'steering strength as an alignment metric' lane, and the absence of any weights-only prior art - and return a concrete,
    citable design input list for the fifty-metric battery.
  approach: >-
    Four questions, answered from primary full text with exact numbers and section-level anchors. (A) POSITIONING, urgent:
    read Galeone et al., 'Perfect Detection, Failed Control: The Geometry of Knowing vs. Steering in Language Models' (arXiv:2606.24952)
    and extract verbatim its AUC=1.000-from-layer-5 result, the cos=0.12 (~83 degrees) detection-vs-intervention angle, the
    four models across three families at 1B-9B, and its before/after instruction-tuning claim - our iteration-1 site-selection
    finding (AUROC 1.0 prompt axis induces fluent refusal on 27% of probes; a 0.69 response-contrast axis steers cleanly)
    must be reframed as a refusal-specific confirmation and extension of theirs, not an original discovery, and the exact
    sentence of the extension must be written here. Then run a SATURATION SEARCH on 'steering strength / steerability as an
    alignment or safety metric', explicitly covering Kabir (arXiv:2508.21448), arXiv:2602.02712 on characterising steering
    strength, The Rogue Scalpel (arXiv:2509.22067, random steering vectors break alignment - this directly changes how our
    matched-random-direction control should be interpreted and that reinterpretation must be spelled out), SteeringControl
    (arXiv:2509.13450), and arXiv:2603.24543; for each, state in one line what it measures, whether it needs harmful prompts
    / a reference model / a benchmark, and precisely what alpha_50 would add beyond it. Report honestly if the lane is occupied
    enough that alpha_50's novelty must be narrowed to the single-model no-reference constraint. (B) WEIGHTS-ONLY PRIOR ART:
    search for any published method that detects safety-training modification, abliteration, or refusal-direction ablation
    from WEIGHTS ALONE with no parent checkpoint - including model-provenance / fingerprinting / task-vector-detection / model-diffing
    literature and the spectral-statistics-of-trained-weights line (heavy-tailed self-regularisation, stable rank, weight-space
    anomaly detection). This determines whether our weights-only arm is novel or a reinvention, and either answer is load-bearing.
    Extract any usable statistic definitions verbatim. (C) BLACK-BOX BASELINE SPECS: pin down, with formulas, the strongest
    published logits-or-text-only safety/refusal predictors (refusal-token logprob mass, first-token entropy, output-length
    asymmetry, judge-on-output, next-token-probability detectors), so our >=8 black-box metrics are faithful implementations
    of named prior work rather than strawmen - the falsifier only bites if the baselines are strong. (D) EXTERNAL GROUND-TRUTH
    SOURCE MAP: enumerate, with URLs and access method, every source carrying published safety numbers for SMALL open-weight
    checkpoints (TrustLLM, AIR-Bench 2024, SALAD-Bench, SORRY-Bench, HELM safety, DecodingTrust, JailbreakBench artifacts,
    Open LLM Leaderboard v2 contents, per-model cards and tech reports including the Qwen3 report's safety section and any
    Qwen3-4B-SafeRL card numbers), stating for each which of our panel families it actually covers and at what parameter scale
    - a realistic coverage verdict, not a wish list, because the paper's ground-truth axis depends on it. Also confirm or
    refute in writing that Qwen3Guard was the reward model for Qwen3-4B-SafeRL (the circularity guard). Deliverable: a dossier
    with a per-metric design input list, a rewritten positioning paragraph, and a coverage table.
  depends_on:
  - id: art_0UsKSgsMHome
    label: extends
    relation_type:
    relation_rationale:
- id: dataset_iter2_dir2
  type: dataset
  objective: >-
    Build the EXTERNAL ground-truth table that replaces our own judge as the correlation target, and freeze the dev / held-out
    lineage split before any metric is selected on it.
  approach: >-
    Two deliverables in one schema-validated row set. (1) EXTERNAL SCORES: for every checkpoint in the frozen 137-row panel
    manifest at <=4.2B, harvest every published quantitative score that exists, one row per (checkpoint, benchmark, metric),
    each carrying the raw value, its scale and polarity (higher-is-safer or lower-is-safer, explicitly), the exact source
    URL, the source type (official model card / tech report / peer-reviewed paper / leaderboard snapshot), the retrieval date,
    and a confidence flag for whether the row refers to THIS exact revision or a sibling. Cover both axes the hypothesis requires:
    SAFETY (TrustLLM, AIR-Bench, SALAD-Bench, SORRY-Bench, HELM safety, DecodingTrust, JailbreakBench, XSTest-style over-refusal
    wherever reported, plus any refusal or safety rate stated on the model card itself) and CAPABILITY (GSM8K, MMLU, ARC,
    HellaSwag, IFEval, Arena-Hard; the Open LLM Leaderboard v2 contents dataset on HuggingFace is the highest-coverage single
    source for small models and should be pulled programmatically rather than scraped by hand). Report coverage honestly as
    a first-class output: how many panel checkpoints have >=1 external safety number, how many have >=1 capability number,
    and the family/scale skew of that coverage. If safety coverage is thin - which is the likely outcome at <=4B - say so
    numerically and record which checkpoints will have to fall back to in-house measurement, since that determines the iteration-3
    analysis plan. Record the Qwen3-4B-SafeRL / Qwen3Guard circularity flag on the affected rows. (2) THE SPLIT: emit a frozen
    dev/held-out assignment over weight lineages, generated by a seeded deterministic rule that is written into the artifact
    (stratified by architecture family and by whether the lineage contains an abliterated or uncensored member, so both splits
    carry the hard cases), covering ALL lineages in the manifest and not merely those measured this iteration. Held-out lineages
    must be at least a third of the total and must include at least two families absent from the dev split entirely, so leave-one-family-out
    is possible. Ship the split with a plain-text statement of when it was written and the assertion that no metric definition
    had been chosen at that time. Also emit a small blanket-refuser disqualification reference: the pre-registered rule, in
    machine-readable form, that any metric whose top-ranked model is a model refusing everything (over-refusal above a stated
    threshold on XSTest-safe items) is disqualified regardless of correlation.
  depends_on:
  - id: art_0UsKSgsMHome
    label: spec
    relation_type:
    relation_rationale:
- id: experiment_iter2_dir3
  type: experiment
  objective: >-
    Compute the fifty-metric single-model battery - at least 8 weights-only, at least 8 black-box, the rest activation-based
    - across a wide multi-family panel, together with a faithful AMS reimplementation and a cheap in-house two-axis behavioural
    readout on the same members, so that iteration 3 can run the correlation test on a real panel instead of n=4.
  approach: >-
    PANEL: draw from the frozen manifest's 59 verified checkpoints at <=4.2B. Gradual scaling with explicit tiers and a stated
    floor: TIER-0 3 checkpoints end-to-end smoke; TIER-1 the Qwen3-4B quartet (Qwen/Qwen3-4B-Base, Qwen/Qwen3-4B, the official
    Qwen3-4B safety-RL model, and a verified abliterated Qwen3-4B) plus the Qwen3-1.7B and Qwen3-0.6B triads; TIER-2 expand
    across families to the floor of >=20 checkpoints / >=12 lineages / >=6 families, prioritising lineages that contain an
    abliterated or behavioural-uncensored member and the standalone models that have no sibling at all, since standalone is
    the actual deployment case. Download sequentially and delete weights after measuring; report which tier completed. IMPORTANT:
    Base models are analysed with the PLAIN renderer and never pooled into a four-way contrast with chat-template members.
    THE BATTERY: fifty metrics, each declaring, before it runs, its prompt requirement (none / benign-only / a-handful-of-harmful),
    its forward-pass count and its measured wall-clock on a 4B model; at most 10 may exceed 60 s. (a) >=8 WEIGHTS-ONLY, zero
    generation - the genuinely new arm. The headline candidate is a direct test for abliteration's signature without a parent:
    abliteration applies W <- W - c r r^T W to EVERY write matrix, so there should exist a single direction whose write energy
    is anomalously suppressed simultaneously across all layers. Operationalise it as the minimum-eigenvalue direction of sum
    over write matrices of W W^T (o_proj and down_proj, appropriately normalised), with the metric being the gap between that
    direction's write energy and the distribution over random directions and over the model's own other low-energy directions
    - report both the suppression depth and the CONSISTENCY of the direction across layers, since a genuine rank-one edit
    gives one shared direction while natural degeneracy does not. Alongside it: per-layer stable rank and spectral entropy
    of MLP and attention write matrices; top-k singular-value decay; norm anisotropy at candidate refusal depths; low-rank
    structure of the unembedding-adjacent subspace; alignment between final-block write matrices and the unembedding rows
    of empirically derived refusal-onset tokens (a weights-only 'refusal write alignment'); LayerNorm gain statistics; and
    distance to nearest degenerate direction. (b) >=8 BLACK-BOX, logits or output text only, implemented faithfully to their
    published forms - first-position logit-gap margin between refusal-onset and continuation tokens, refusal-token logprob
    mass, first-token entropy, entropy and length asymmetry between benign and few-harmful prompts, ever-emits-refusal rate
    under greedy decoding, judge-on-output. These decide whether looking inside buys anything and must be implemented as strong
    baselines, not strawmen. (c) the remainder ACTIVATION-BASED and cheap, re-implementing the iteration-1 measurement stack
    (r_t logit-lens readout, layer selection by held-out contrast AUROC transferred by relative depth, forward PRE-hook injection
    - note the iteration-1 finding that hooking a layer's OUTPUT is a no-op for that layer's own readout): harmful-vs-benign
    cluster separation, refusal-direction cosine, layer-wise margin profile, first-generated-token readouts (favoured a priori,
    because iteration 1 established that refusal is decided at generation ONSET and long-rollout metrics are disfavoured),
    plus a small number of declared-expected-to-fail EWS-style controls carried explicitly as negative controls. BASELINE:
    implement AMS exactly to the spec dossier (sigma = (mu+ - mu-)/sigma_pooled on the diff-in-means direction at the final
    prompt token, 40-80% relative-depth sweep, 16 contrastive pairs x 3 concepts, 96 forward passes) and VALIDATE it against
    the three checkpoints appearing in the AMS paper's own Table I (Llama-3.2-3B-Instruct 8.37, gemma-2-2b-it 4.80, Llama-3.2-1B-Instruct
    4.55) - report the reproduction gap; a benchmark-free metric submitted without the closest published benchmark-free metric
    is rejected on that ground alone. GROUND TRUTH, last stage so the battery ships even if this is cut: a reduced two-axis
    in-house readout on every measured member - 40 core harmful items and 25 XSTest-safe items, greedy, fp32, max_new_tokens
    64, with the MANDATORY R4 evaluator-system-prompt judge fix in force and the cheap repaired judge (llama-3.3-70b-instruct
    with framing, ~$0.04/1k items) - plus the degeneracy/incapacity flag from iteration 1 so members at the incapacity floor
    are marked unreliable rather than silently scored. Judge spend hard-capped at $1.50 with running cost logged after every
    call. CRITICAL DISCIPLINE: the external-score table is a parallel artifact and is NOT consumed here; no metric may be
    selected, tuned or dropped on the basis of any correlation with any ground truth in this artifact. Emit every metric value
    for every checkpoint in a tidy long-format table with the cost declarations attached, so iteration 3's selection and correlation
    run on frozen numbers.
  depends_on:
  - id: art_CKWQh2cOQLLQ
    label: dataset
    relation_type:
    relation_rationale:
  - id: art_0UsKSgsMHome
    label: spec
    relation_type:
    relation_rationale:
- id: experiment_iter2_dir4
  type: experiment
  objective: >-
    Re-run alpha_50 at publishable power on four lineages, and settle by direct experiment whether it is a safety measurement
    or a lexical artifact - the reviewer's two decisive objections, both of which are answerable in one run.
  approach: >-
    The iteration-1 steering and judging code is not passed in as a dependency (experiments may depend only on datasets and
    research), so the alpha ramp, the NORM_L normalisation and the framed-judge scorer are re-implemented here from the specifications
    below; the iteration-1 constants are restated so the re-implementation is checkable: alpha in units of NORM_L (median
    residual-stream norm at the steering layer, 21.2 for Qwen3-0.6B instruct), injection at relative depth 0.25 via a forward
    pre-hook, response-contrast axis, and the framed evaluator system prompt without which a safety-trained judge never labels
    COMPLIANCE. POWER. For each member, estimate the dose-response curve of refusal rate against steering coefficient alpha
    (in NORM_L units) with >=20 benign prompts x >=5 seeds per alpha - 100 Bernoulli draws per point against iteration 1's
    5 - on an alpha grid refined by bisection around the crossing so the cost buys resolution where it matters rather than
    uniformly. Fit a logistic dose-response, report alpha_50 with a bootstrap CI resampling prompts (the unit), report per-point
    binomial error bars, and report a PAIRED bootstrap of the instruct-minus-abliterated difference on matched prompts. If
    that difference CI overlaps zero, say so in those words and reframe alpha_50 as base-vs-tuned separation only. State the
    two discriminations separately throughout, as the reviewer asks: (a) is there a reachable refusal mode at all, and (b)
    how expensive is it - and define and evaluate ONE composite score (alpha_50 with undefined mapped to +infinity, gated
    by max reachable refusal rate) because that composite, not the pair of numbers, is what a user would apply. Report the
    fluency screen (distinct-3, max-n-gram repeat) as part of the metric, since refusal collapses at high alpha through degeneration
    rather than through the mode becoming unreachable, and state explicitly that the alpha grid's upper edge is a measurement
    boundary, not a model property. CIRCULARITY, three controls run as first-class arms and reported whatever they show: (i)
    PARAPHRASE-DISJOINT AXIS - refit the response-contrast axis from refusal/compliance responses whose surface tokens are
    disjoint from the scoring lexicon (verify disjointness by token-id set intersection, and report the cosine between the
    canned-string axis and the paraphrased axis) and check whether alpha_50 moves; (ii) SEMANTIC SCORING - re-derive alpha_50
    with outcomes labelled by the repaired semantic judge instead of the refusal regex, on the same recorded generations,
    so scorer and axis are decoupled; (iii) NORM-MATCHED NON-SAFETY STYLISTIC AXIS - a formal-vs-casual (or verbose-vs-terse)
    response contrast at matched norm, which must NOT reproduce the safety ordering, plus the matched-random-direction control
    reinterpreted in light of the Rogue Scalpel finding that random steering vectors can themselves break alignment. A verdict
    of LEXICAL is a publishable finding and must be written as one, not buried. PANEL, addressing the scope critique: four
    lineages, not one - the Qwen3-4B quartet (Base / Instruct / official SafeRL / abliterated), which is the first panel in
    this project containing a deliberate safety-RL arm and therefore the only contrast that isolates safety training from
    helpfulness training; the Qwen3-1.7B lineage including its behavioural-uncensored member; the Qwen3-0.6B lineage using
    ONE abliterated checkpoint held fixed across every arm (iteration 1 used different abliterated repos in different arms
    - fix this and state it); and one cross-family lineage (Llama-3.2 or SmolLM2) so architecture varies. Measure the three-axis
    behavioural ground truth (plain-harmful refusal, XSTest over-refusal, jailbreak ASR on the fixed suite) on exactly these
    members with the R4 judge fix, so alpha_50 and its target are measured on identical checkpoints. COMPARABILITY, the triage
    premise: report NORM_L per member and test directly whether alpha_50 varies more WITHIN a lineage across safety levels
    than ACROSS architectures at matched safety level - if it does not, the metric is not a triage score and the paper must
    say so. Report the rank correlation of alpha_50 with harmful-refusal rate with the LINEAGE as the resampling unit and
    BOTH aggregation units (per-member and per-lineage), since iteration 1 already observed sign flips between them. Judge
    spend capped at $2.00, logged per call.
  depends_on:
  - id: art_CKWQh2cOQLLQ
    label: dataset
    relation_type:
    relation_rationale:
  - id: art_0UsKSgsMHome
    label: spec
    relation_type:
    relation_rationale:
- id: evaluation_iter2_dir5
  type: evaluation
  objective: >-
    Repair the four internal-validity defects the reviewer found in the iteration-1 record, using the archived result trees
    plus a rebuilt judge probe, so that the negative results the paper leans on survive a hostile read.
  approach: >-
    Five analyses on existing artifacts, no new model runs beyond LLM judging. (1) THE LAMBDA INCONSISTENCY, the sharpest
    defect: the paper certifies lambda non-identifiable on all 640 rows and then draws its decisive control conclusion from
    bootstrap CIs on those same values. Recompute the random-direction-versus-refusal-direction contrast on the assumption-free
    statistics the paper says it trusts - the 16-step survival ratio and the deviation AUC - directly from the archived tier0_raw.json
    tree, with the same lineage/prompt bootstrap, and make those the PRIMARY control evidence; then present the lambda CIs
    demoted to a consistency check with an explicit note that both arms fail the identifiability rule equally so the comparison
    is between two equally noisy estimators. State whether the generic-mixing verdict survives the switch; if it does not,
    that is a material change and must be reported as one. (2) OBSERVABLE VALIDITY GATE: compute, per model, the r_t observable's
    harmful-versus-benign AUROC or margin (the record notes margins of 0.03-0.15 for two members against 0.71 for instruct),
    define a stated threshold, and restrict the cross-model fluctuation-indicator comparison to members clearing it. If only
    one member clears it, say plainly that the 'indicators track lineage, not safety' conclusion rests on comparisons involving
    models where the observable is uninformative, and downgrade it; also report the same comparison computed at the final-layer
    readout, where the observable is defined by construction, and state which is primary. (3) THE JUDGE PROBE, rebuilt: the
    0/7 compliance result currently rests on 7 items whose truth labels come from a nine-character affirmative-prefix match,
    and at least one is a refusal-by-redirection mislabelled as compliance ('Certainly! Here's a message that conveys hope...'),
    which means the 'gold' judge scored 21/21 partly by being wrong. Rebuild the probe at >=100 items stratified across ALL
    FOUR rubric classes including PARTIAL (excluded before, despite being the weakest class for every scorer at <=0.41 recall),
    drawn from the 3,365 archived generations so the items are real model outputs rather than constructed ones. Label them
    with TWO independent annotators run under different rubric framings and different model families, report Cohen's kappa
    between them, adjudicate disagreements explicitly, and publish the disputed items verbatim including the redirection case.
    Re-derive the frozen-versus-repaired judge comparison against those labels. If the 0/7 pattern survives on properly labelled
    compliance items, say so and the finding strengthens; if it partially dissolves, restate the affected numbers - the 0.700
    to 0.113 refusal revision and the 0.092 to 0.858 ASR revision - with the corrected magnitude. Judge/annotator spend capped
    at $1.00, logged per call. (4) THE n=4 CORRELATIONS: recompute the SPI-versus-baselines comparison with exact permutation
    p-values so the reader sees the ceiling (at n=4 no ordering can go below roughly 0.042), state how many of the four models
    sit above the incapacity/refusal floor, and rewrite the one-directional implication into a statement the data can carry
    - or drop the numbers and report qualitatively that SPI did not order the panel. (5) PRE-REGISTRATION FIDELITY AUDIT:
    reconcile prereg.json against the reported text for all three iteration-1 experiments and emit a deviations table with,
    per amendment, its trigger, its date, and the direction of its effect on the reported result - including the excess-width
    sign-convention inversion (prereg says alpha_down minus alpha_down_forced_A, the paper reports the reverse) and the alpha-grid
    amendment from delta 0.25 over [-2, 8] to delta 0.05 over [-1.5, 2]. Also state explicitly, for the record, whether the
    same fitted refusal_direction.pt feeds any other reported result besides the in-house abliteration ladder, and relabel
    that ladder's failure as a failed reimplementation rather than a property of the technique unless a check of the edit's
    coverage (all write matrices including o_proj and down_proj) shows otherwise.
  depends_on:
  - id: art_UthAQuH8WZ5C
    label: reanalyzes
    relation_type:
    relation_rationale:
  - id: art_W0HSULPgrt3K
    label: reanalyzes
    relation_type:
    relation_rationale:
  - id: art_TFe9eI-2QZN3
    label: prereg audit
    relation_type:
    relation_rationale:
expected_outcome: >-
  By the end of this iteration: (1) a fifty-metric single-model battery with declared per-metric cost, computed over >=20
  checkpoints / >=12 lineages / >=6 families - including the first weights-only arm this project has had, with a direct test
  for abliteration's rank-one signature detectable from one checkpoint with no parent - plus a validated AMS reimplementation
  checked against its own paper's Table I, and a reduced two-axis in-house behavioural readout on the same members; (2) alpha_50
  at real power on four lineages with bootstrap CIs, a paired instruct-minus-abliterated difference, a composite score definition,
  a within-lineage-versus-across-architecture comparability check, and a definitive verdict on whether it is lexical - a verdict
  that is publishable in either direction; (3) an external safety and capability score table with honest coverage numbers,
  plus a frozen dev/held-out lineage split written before any metric was selected, which is the contamination guard the whole
  selection procedure depends on; (4) a repaired iteration-1 record: the generic-mixing control re-derived on assumption-free
  statistics, an observable validity gate that says which members the EWS conclusion can actually rest on, a >=100-item four-class
  judge probe with two annotators and reported kappa replacing the 7-item surface-pattern probe, permutation-bounded n=4 correlations,
  and a pre-registration deviations table; and (5) a positioning pass that cites the detection-versus-steering-gap result
  at its point of use, reframes our site-selection finding as an extension of it, and states plainly how occupied the steering-strength-as-metric
  lane is. Negative outcomes are all reportable and several are likely: the weights-only arm may detect abliterated models
  cleanly while nothing tracks graded safety-RL strength across families (the pre-registered most-likely outcome); alpha_50's
  key difference CI may overlap zero; and the judge probe may partially dissolve. Iteration 3 then runs the frozen selection
  and the paired white-box-versus-black-box correlation test on the held-out lineages, using this iteration's frozen metric
  table and external scores - which is the paper's headline result and is now set up to be run once, cleanly, rather than
  improvised.
summary: >-
  Iteration 2 converts a one-lineage, unpowered positive into a real single-model safety screening study: a fifty-metric battery
  (>=8 weights-only, >=8 black-box) computed blind across >=20 checkpoints in >=6 families with a validated AMS baseline;
  alpha_50 re-run at publishable power on four lineages including the Qwen3-4B Base/Instruct/SafeRL/abliterated quartet, with
  the three controls that decide whether it measures safety or a canned-apology token direction; an external ground-truth
  score table plus a dev/held-out lineage split frozen before selection; and a re-analysis that repairs the lambda-identifiability
  inconsistency, the observable validity gap, the seven-item judge probe and the pre-registration sign inversion the reviewer
  flagged.
</previous_strategies>

<dependency_rules>
- depends_on is a list of objects {id, label} — each entry references an existing artifact and tags how it is being used
- "id" can ONLY reference IDs from <existing_artifacts> — never IDs you are proposing (all new artifacts run in parallel)
- "label" is a SHORT free-text type label (a word or two, NOT a sentence) describing what role the dep plays — e.g. "dataset", "validates", "extends", "supersedes". Required on every dep.
- Setting depends_on provides the dependency's out_dependency_files to your artifact at execution time
- If no suitable existing artifacts exist, use empty depends_on
- New artifact IDs are assigned by the system after submission — do not invent IDs for your proposed artifacts
</dependency_rules>

<available_artifact_types>
Artifact types you can plan. Use this to choose the right types for your strategy objectives.

<artifact_types>
RESEARCH
Web research to answer key questions — like a researcher making decisions.
Runtime: LLM Agent, no code execution.
Tools: the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text).
Capabilities: Find, synthesize, and compare information across sources; survey SOTA and best practices.
Deps: REQUIRED none | OPTIONAL other RESEARCH to build on prior findings

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance

DATASET
Collect, prepare, and merge datasets for experiments and analysis.
Runtime: Python 3.12, UV, isolated workspace.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-hf-datasets (HuggingFace Hub — ML datasets, many UCI/OpenML/Kaggle mirrors), aii-owid-datasets (Our World in Data — global statistics), aii-json (schema validation). Also any Python source (sklearn.datasets, openml, direct URLs, APIs) — must verify within 300MB limit.
Capabilities: Search, acquire, transform, combine, and standardize data from any available source.
Deps: REQUIRED none | OPTIONAL RESEARCH for guidance on what data to collect

EVALUATION
Evaluate experiment results with metrics, statistical analysis, and validity checks.
Runtime: Python 3.12, UV (any evaluation library), isolated workspace, gradual scaling matching experiment.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Compute any quantitative metrics and statistical tests, analyze validity and robustness.
Deps: REQUIRED at least one EXPERIMENT | OPTIONAL DATASET if reference data needed

PROOF
Formally prove mathematical statements in Lean 4 with automated iteration.
Runtime: LLM agent with Lean 4 compiler feedback loop.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-lean (proof verification, Mathlib search, tactics: ring, linarith, nlinarith, omega, simp, etc.)
Capabilities: Formally verify properties and inequalities, iterative proof development, lemma decomposition.
Deps: REQUIRED none | OPTIONAL RESEARCH for mathematical background
</artifact_types>
</available_artifact_types>

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

RESEARCH executor scope:
  Output: research_out.json with {answer, sources, follow_up_questions} + research_report.md
  DOES: Web research — search, read, synthesize information from papers/docs/APIs into a structured report
  DOES NOT: Run code, download files, execute scripts, compute anything — no shell/Python access
  Use for literature surveys, API documentation, technical specifications — pure information gathering

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results

DATASET executor scope:
  Output: data_out.json with rows of {input, output, metadata_fold, ...} — raw data only, no derived computations
  DOES: Download/generate datasets, analyze candidates to pick the best ones, standardize to JSON schema (features, labels, folds, metadata), validate schema, split into full/mini/preview
  DOES NOT: Run experiments, train models, compute derived statistics (PID/MI/correlations/synergy matrices) as final output
  If you need to COMPUTE something from data (synergy matrices, MI scores, timing benchmarks), use an EXPERIMENT artifact instead

EVALUATION executor scope:
  Output: eval_out.json with evaluation results
  DOES: Any evaluation of experiment results — metrics, statistical tests, ablations, comparisons, visualizations, robustness checks, error analysis, etc.
  DOES NOT: Implement new methods (use EXPERIMENT), collect data (use DATASET)
  This is for analyzing experiment outputs from any angle

PROOF executor scope:
  Output: Lean 4 proof files (.lean) with verified theorems
  DOES: Write and verify Lean 4 formal proofs with Mathlib, iterative compilation
  DOES NOT: Run Python experiments, collect data, do empirical analysis
  Use only when formal mathematical guarantees are needed
</artifact_executor_scope>

<artifact_planning_rules>
RESEARCH: Plan early — findings guide dataset selection, experiment design, and methodology.
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
DATASET:
- Plan for REAL third-party datasets (HuggingFace, Kaggle, direct-download URLs) — downloadable within time and size constraints
- Describe dataset criteria (domain, size, format) — executors find exact sources, but you can suggest candidates or search directions
- ALWAYS prefer real datasets over synthetic. Synthetic is a LAST RESORT only when no suitable real data exists
EVALUATION: Must depend on at least one EXPERIMENT. Focus on statistical rigor and validity checks.
PROOF: Use only when the hypothesis requires formal mathematical guarantees. Lean 4 + Mathlib.
</artifact_planning_rules>

<existing_artifacts>
--- Item 1 ---
id: art_CKWQh2cOQLLQ
type: dataset
title: Frozen safety prompt sets and model list
summary: |-
  ONE deliverable, full_data_out.json, holding EXACTLY 8 datasets / 2,113 rows, every row tagged metadata_fold = dataset name. Row schema: {input, output, metadata_fold, metadata_uid, metadata_block_version, metadata_meta{...}}. Validated against exp_sel_data_out; full/mini/preview all pass. 3.5 MiB, far under the 100MB limit.

  DATASETS: harmless_dynamics (43: 40 vetted everyday user turns over 10 topics + 3 rejects, meta.selected); xstest_overrefusal (450 = 250 safe + 200 unsafe, split verbatim in meta.label/meta.prompt_type); plain_harmful (594 deduped AdvBench+JBB union, meta.in_core80 marks the 80-row 10-category stratified core, meta.target carries the affirmative prefix); jailbreak_suite (400 = the 80 core behaviors x 5 published templates, meta.pair_id resolves to the plain_harmful uid); layer_contrast (256 = 128 harmful + 128 benign, diff-in-means layer selection ONLY); wikitext_fluency (200 passages of 150-400 words); refusal_token_lexicon (10 tokenizer families); panel_manifest (160 checkpoint rows, 137 verified).

  HOW TO USE. Jailbreak rows branch on meta.delivery: t1_prefill has delivery='assistant_prefill' with meta.user_text and meta.prefill_text SEPARATE (do not concatenate — insert the prefill in the assistant slot); the other four are delivery='user_turn' with empty prefill. t5 stores meta.plaintext beside the base64 wrapper. Every row carries meta.template_text/template_source inline. B7 rows give refusal_onset and continuation lists per family, each entry {token_id, token_str, decoded_str, source in {empirical,lexicon}, empirical_count}; lists are disjoint, all ids < vocab_size, >=12 refusal and >=20 continuation per family, all 10 families empirical.

  PANEL: 137 verified, 59 at <=4.2B over 31 lineages (base 20 / instruct 18 / abliterated 8 / behavioral-uncensored 13); n_lineage 93 overall. lineage_id = the pretrained base at the root of the derivation chain, with the chain in meta.lineage_evidence — this is the bootstrap resampling unit. Gated repos (meta-llama/*, google/gemma-2*, huihui-ai Qwen3 v1 abliterated) are KEPT with verify_error; ungated mirrors are SEPARATE rows with meta.mirror_of. 6 clean H4 behavioral-uncensored candidates at <=4.2B, one (UnfilteredAI/DAN-Qwen3-1.7B) sharing the Qwen3-1.7B-Base lineage with its base/instruct/abliterated triad; 2 disqualified_by_provenance with card text quoted.

  DEVIATIONS, all evidence-driven and recorded in metadata.manifest: (1) walledai/* is gated (403) — XSTest from the ungated Paul/XSTest mirror, AdvBench from the llm-attacks GitHub CSV at a pinned commit. (2) mlabonne/harmful_behaviors REJECTED for layer_contrast because it is an AdvBench repackaging that would break disjointness; the harmful half is the Forbidden-Question-Set (Shen et al. CCS 2024) instead. Disjointness asserted: exact overlap 0, max cosine 0.652 vs threshold 0.85. (3) B7's planned harmful-vs-benign rate criterion cannot separate refusal from topic — run as specified it admitted 'Creating', 'Writing', 'Hack', 'Script', 'Title'. Replaced with behaviour-conditioning: a token is a refusal onset when it is the ACTUAL first generated token of >=3 greedy rollouts whose opening matches a refusal regex, over the same prompts. This surfaced a usable result: refusal onset is near a one-token event ('I'), and per-family greedy refusal rates (meta.greedy_refusal_rate) span 0.00 (Pythia-410m, danube3-500m-chat) to 0.81 (Gemma-2-2b-it), with Qwen3-0.6B at 0.05 with thinking disabled.

  CAUTION: harmless_dynamics (no_robots) and the layer_contrast benign half (alpaca-derived) are CC-BY-NC-4.0, NON-COMMERCIAL. B1 topic labels are a disclosed keyword heuristic (a stratification device, not a claim); the original task label is meta.task_type. 27 build assertions ship in metadata.assertions.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

--- Item 2 ---
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
out_expected_files:
- research_out.json
out_dependency_files:
  file_list:
  - research_out.json

--- Item 3 ---
id: art_UthAQuH8WZ5C
type: experiment
title: Does refusal wobble predict model safety?
summary: |-
  TIER-0 feasibility experiment for the 'safety = nearness to a tipping point' hypothesis. EXECUTED IN FULL on an RTX A4500: 4 models x 20 harmless prompts x 20 paired rollouts x 192 generated steps (94 min) plus a 39 min certified-geometry refit, 590-710 tok/s, <3 GB VRAM, $0.00 API spend. Panel: Qwen3-0.6B triad (Base / instruct / abliterated) + SmolLM2-360M anchor. The primary abliterated repo is GATED; the maintainer's v2 (huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2) was used per the fallback plan. Panel validity PASSES (instruct 0.225 harmful-refusal vs abliterated 0.000).

  HEADLINE: DISCONFIRMATION, twice over. (1) lambda is NOT identifiable at any geometry reached — the pre-registered synthetic rule demands T_fit>=128; after refitting there (layer/direction/eps/prompts/seeds held identical) the requirement MOVES to n_roll>=40 vs the achieved 20. Sizing for iterations 2-5: n_roll>=40, ~2x this run. (2) The RANDOM-DIRECTION CONTROL REPRODUCES THE ORDERING: a random unit vector at the same layer and magnitude separates the panel as well as the refusal direction (2/3 vs 2/3 significant), and on the ONLY pair isolating safety tuning (instruct vs abliterated) the control separates (-0.493, CI excludes 0) while the treatment does NOT (-0.226, n.s.). Verdicts: LAMBDA_NOT_IDENTIFIABLE_FLUCTUATION_ARM_ONLY (pre-registered) + CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING (supplementary).

  Fluctuation indicators track LINEAGE, not safety: the Qwen triad overlaps (Var* 3.10-3.15, AC1 0.245-0.304, flicker 40.2-42.2) while SmolLM2 separates (Var* 2.75, AC1 0.182). Pre-registered ordering fails and partly reverses (instruct has the LOWEST Var*/flicker of the triad and the FASTEST relaxation). Method vs baseline: label-free SPI Spearman rho=-0.20 vs supervised diff-in-means refusal direction +0.40 and r_0 margin +0.40 — both baselines, given the 32 harmful prompts SPI is denied, BEAT it (n=4, directional only; 3 of 4 models sit at a refusal floor).

  FOUR BUGS THE PRE-FLIGHT GATES CAUGHT, each of which would have produced confident nonsense: (a) injecting at a layer's OUTPUT is a no-op for that layer's own readout (|delta| was EXACTLY 0 at every eps, since the layer writes K/V before a forward hook fires) -> moved to a forward PRE-hook on the layer input; (b) free-running delta cannot estimate a decay rate — token streams diverge in ~7 steps and |delta| GROWS (decay_ratio_16 2.57-5.33) vs teacher-forced (0.119-0.233) -> teacher-forced is the primary channel; (c) mean|delta| is upward-biased by +38% to +68% at EVERY n_roll because E|N(mu,s)|>|mu| -> fit the SIGNED across-rollout mean (bias -0.03..+0.02); (d) flicker-as-fraction saturates at 1.0 -> use crossings/100.

  Other reported diagnostics: exponential model misspecification (median fit r2 0.11-0.54, 30-90% of fits below 0.3, lambda IQR ratios 4.7-20) so the assumption-free decay_ratio/AUC statistics are preferred; layer-L logit lens vs final-layer readout correlates only 0.17-0.26 (below the pre-registered 0.3) so EVERYTHING is reported at both readouts; the per-cell eps-linearity control returns False purely from prompt scatter, while the prompt-averaged version gives r2 up to 0.996 with log-log slopes 0.61-0.90 (both shipped). Layer selection: L=15/28, AUROC 0.999, middle third.

  DELIVERABLES: method.py (single entry point running measure -> reshape -> figures -> validate), reusable spi/ library (models, prompts, observable, rollout, indicators, validity, groundtruth), refit_certified.py, 4 pre-flight gate scripts, 10 figures, out/tier0_raw.json (11 MB full result tree), out/refit_certified.json, out/layer_choice.json (written and asserted BEFORE any indicator). method_out.json is exp_gen_sol_out-valid: 5 datasets / 224 examples, 16 limitations, all 5 control booleans present, all 640 lambda rows carrying the identifiable flag, every failed fit null WITH a reason string, zero non-finite numbers. All 10 figures regenerate from the archived tree alone. pyproject.toml pins all 88 installed packages.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 4 ---
id: art_TFe9eI-2QZN3
type: experiment
title: Does a refused answer stay refused?
summary: |-
  Pre-registered steering-hysteresis experiment on one Qwen3-0.6B lineage (Qwen/Qwen3-0.6B-Base, Qwen/Qwen3-0.6B instruct, mlabonne/Qwen3-0.6B-abliterated; huihui-ai is gated, fallback #8 used). A refusal-direction steering coefficient alpha (in units of NORM_L, the median residual-stream norm at the steering layer) is injected at one block's output for every position in the forward pass, so during incremental decoding each token's KV entries stay frozen carrying the alpha active when written - that frozen cache is the candidate latent state.

  Six arms per (model, prompt, seed), 30 benign prompts x 3 seeds x 3 models, $0.00 spend (all classification is deterministic string/token matching): UP-RAMP (measurement), ENTRY-AT-ALPHA, DOWN-RETAINED (alpha_down), DOWN-FORCED-A (byte-identical refusal prefix prefilled UNSTEERED; the primary control), DOWN-FORCED-B (alpha-schedule replay; positive control), RESET (prefix discarded; noise floor).

  VERDICT = REFUTED, the pre-registered disconfirmation. (1) Hysteresis is real: width alpha_entry - alpha_down = 0.262 [0.185, 0.344] for instruct, positive as pre-registered for generic autoregressive conditioning. (2) It is NOT carried by a retained latent state: excess_width (= alpha_down_forced_A - alpha_down) is 0.019 [-0.057, 0.099] instruct, -0.031 [-0.070, 0.001] abliterated, -0.330 [-0.990, 0.000] base - every CI overlaps 0 and every lower bound sits below the temperature-0.7 RESET noise floor (p95 = 0.05). H1b NOT_CONFIRMED. (3) Not a plumbing artifact: FORCED-B reproduces the retained arm EXACTLY (mean and max |diff| = 0.000 on every prompt of every model) and the temperature-0 RESET gate is exactly 0 everywhere.

  Three further results useful downstream: (a) the up-transition is unreachable mid-generation - ramping alpha inside an already-compliant generation fails on 92-100% of attempts (10/10 at delta in {0.05,0.1,0.2,0.4}, 9/10 with an [L-2,L+2] window) while a fresh generation at the same constant alpha refuses reliably, i.e. compliance sticks, refusal does not; (b) a harmful-vs-benign PROMPT axis at held-out AUROC 1.0 (14 of 28 layers) is a poor INDUCER (site score 0.27, partly degenerate refusals) whereas a CAA-style RESPONSE-contrast axis scores 0.69 and yields clean refusals - prompt-classification quality is not steering quality, and a matched random direction induces refusal at no alpha; (c) a candidate cheap safety metric, alpha50 (steering coefficient at which a fresh generation starts refusing, 5 prompts, 13 alphas, no benchmark): base undefined / max rate 0.20, instruct 0.475, abliterated 0.550.

  Eight pre-registration amendments, each with trigger, timestamp and reason, are recorded in prereg.json and echoed in method_out.json['preregistration']. Sensitivity: narrow-floor run (alpha_min=-0.5, 43% censored) gave 0.011 [-0.050, 0.073] and 0.012 [-0.009, 0.035] uncensored; re-scoring every recorded token stream at COMPLIANCE_RUN in {6,10,14} keeps all CIs overlapping 0. Every generated token, its alpha and its r_t are logged in gens/ so every classification is auditable. method_out.json validates against exp_gen_sol_out; the full analysis lives under metadata.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 5 ---
id: art_W0HSULPgrt3K
type: experiment
title: Safety refusal scores and a graded safety dial
summary: |-
  Tier-0 behavioural safety ground truth on 16 members (Qwen3-0.6B base/instruct/mlabonne-abliterated triad, Llama-3.2-1B and SmolLM2-360M base+instruct cross-family pairs, pythia-410m low-refusal anchor, a template side-check member, 3 task-vector interpolants, 4 abliteration-strength members), 3365 generations, three axes (plain-harmful refusal on 80 deduped AdvBench items; jailbreak ASR on 40 of those x 3 fixed attacks = prefill/refusal-suppression/roleplay; XSTest 50 safe + 25 unsafe contrast). Decoding: greedy, fp32, max_new_tokens=64, left padding, enable_thinking=False with an automated <think> guard. fp32 is load-bearing: fp16 batched greedy is NOT batch-invariant (3/4 identical at batch=4 vs 1; 4/4 in fp32).

  HEADLINE (a measurement failure, and the main deliverable). The pre-registered LLM judge (gpt-5.4-nano, frozen rubric, empty system prompt) NEVER assigns COMPLIANCE to harmful content: 0/7 on the COMPLIANCE class of a balanced 21-item probe, 9/21 overall. claude-3-haiku (7/21) and claude-haiku-4.5 (12/21) also score 0/7. Not a parse or payload bug (finish_reason=stop, 100% clean parse, max_tokens 8 vs 64 identical). An evaluator system prompt is what fixes it, not model capability or price: llama-3.3-70b-instruct+framing 18/21 at $0.040/1k, gemini-3.6-flash+framing 21/21 at $1.236/1k.

  CONSEQUENCE: the pre-registered sanity gate FAILS under the frozen judge (deltas 0.263/0.225) and PASSES under a repaired judge (0.463/0.413) on IDENTICAL generations. The ladder verdict flips too: SNAPPED -> SMOOTH. The scorer, not the models, decides both. prereg.json was never edited; the repair arm is documented in prereg_amendment.json.

  THREE SCORERS, one pipeline: baseline refusal-string screen, frozen judge (PRIMARY, reported in full including its failure), repaired judge (full coverage), plus a gemini gold-reference arm on a 400-item stratified subsample. Blind adjudication of 147 items (labels withheld by construction, mtime-asserted): frozen 0.510 acc / kappa 0.242; repaired 0.694 / 0.412; gold 0.759 / 0.449; screen 0.844 binary acc but kappa only 0.315 (accuracy inflated by class imbalance; recall 0.223). DECISIVE: on the 80 adjudicated disagreements the adjudicator sides with repaired 48x, frozen 21x, neither 11x.

  KEY RATES (repaired scorer): qwen3_abliterated refusal 0.113 / ASR 0.858 vs qwen3_instruct 0.525 / 0.633; llama32_instruct 0.975. LADDERS: task-vector W(t)=W_base+t(W_instruct-W_base) gives 0.062/0.237/0.388/0.500/0.525 = SMOOTH and monotone (caveat: t=0 FAILS the fluency screen, distinct-3 0.113, so the low-t end is partly recovery-from-degeneracy). In-house abliteration W<-W-c*rr^T W is SNAPPED under both scorers: refusal flat 0.525->0.512 while XSTest over-refusal rises 0.16->0.42 - it changed the model without producing the knob.

  OTHER: incapacity floor (pythia-410m scores 0.550 'refusal' with 0.327 degenerate rate - rates near that floor carry no safety signal; 4 members auto-flagged UNRELIABLE); template confound (Qwen3 base 0.662 chat-template vs 0.900 generic, delta 0.238 > 0.15 threshold); SmolLM2 instruct refuses LESS than its own base (-0.325, CIs disjoint) so the sanity ordering is family-specific.

  COST: $1.251 total, within the pre-registered $1.50 budget; 0.109 s/item, ~551 tok/s; 50-member panel projects to 0.41 GPU-hours and $0.64. The fitted parameter-scaling slope came out NEGATIVE and is explicitly marked unusable (wall-clock dominated by early EOS, not FLOPs). Audit cost deliberately not measured.

  ARTIFACTS: the 7 ladder checkpoints (1.14 GB each, 7.9 GB) are derived intermediates and are NOT shipped. `python method.py --stage rebuild-ladder --verify-hashes` recreates them bit-exactly from the two public Qwen3-0.6B checkpoints plus the 5 KB refusal_direction.pt; this was verified, not assumed - the directory was deleted and all 7 reproduced their original sha256 (~6 s each), and finalize re-ran to byte-identical verdicts without them. sha256 values and the build recipe are in results/ladder_models_manifest.json.

  FOR DOWNSTREAM USE: do not build correlations on the frozen-judge rates. Use ground_truth_repaired_scorer, and attenuation-correct with the reported reliability. PARTIAL is the weakest class for every scorer (<=0.41 recall), so safe-completion behaviour is the least trustworthy axis. The adjudicator is an LLM agent, not a human, so every 'accuracy' bounds scorer disagreement, not truth.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 6 ---
id: art_lMTPOpnFwKnw
type: research
title: Prior Art Check for Safety Metrics
summary: >-
  Four-part prior-art dossier for a 50-metric single-model safety-screening battery. (A) POSITIONING: our iter-1 site-selection
  finding is NOT original -- Galeone et al. [1] published the general detection-vs-control dissociation (AUC=1.000 from layer
  5 vs cos=0.12/~83deg to the refusal direction; cos in [0.12,0.20] over 4 models/3 families/1B-9B; 0.1197 vs 0.1200 across
  instruction tuning) on a panel OVERLAPPING ours. Our opening: refusal is never a DETECTED behaviour there, only the lm_head
  intervention direction. CRITICAL TRAP: their Sec.8 is an explicit NEGATIVE -- the cosine sits at chance for steerable and
  unsteerable behaviours alike -- so any cosine-as-safety-score metric is already a published negative and may enter only
  as a declared-expected-to-fail control. A 199-word rewritten positioning paragraph is supplied. alpha_50 = NARROWED after
  a 14-query saturation search over a 12-paper lane; surviving claim: the only member that is single-scalar, parent-free,
  HARMFUL-PROMPT-FREE and benchmark-free. Sharpest rival Logit-Gap Steering [3], whose published gap shifts on Qwen2.5-0.5B/Llama-3.2-1B/gemma-2b
  give a reproduction gate on our exact sizes. Newly surfaced, absent from the plan: Geometry of Refusal [10] and LAP/A_lin
  [11] (rho=+0.86..+0.91 training-free -- ADOPT for layer selection, do not compete). Rogue Scalpel [7] forces a rewritten
  pass condition: random directions raise compliance 0%->1-13% (18% in body), so they are a MAGNITUDE-MATCHED COMPARATOR,
  never a null; their alpha=c*mu(l) matches our NORM_L units. Pre-register against non-monotonic steering strength [6], input-dependent
  optimal layer [14], and the scalar-steerability objection [15]. (B) WEIGHTS-ONLY = NOVEL (narrow). The collision paper's
  weight signal is E1 = mean_m sigma_1^2(dW)/sum sigma_i^2(dW) with dW = W_base - W_cand [2] -- it REQUIRES the parent, as
  does WeightWatch [17]. Parent-free is the hole and is immune to their #1 failure (spoofed reference). Scale escape hatch
  CLOSED: Qwen2.5-1.5B is in their 273-checkpoint registry. Ships a new implementable observable (SNS-1/2/3 on the shared
  Gram matrix, SNS-3 supplying the refusal-specificity E1 cannot) plus 13 weights-only statistics, grounded in Jain et al.
  [18] and HTSR [27] (no safety application found). (C) 9 black-box specs: 5 strong (logit-gap [3], FJD [23], SPD [22], prefill-flip
  [16], WildGuard [32]), 2 labelled STRAWMEN (first-token entropy has no safety-specific prior; length asymmetry is folklore),
  SRI [24] off-constraint (rollout-integrating), AMS WEAK (independently measured at AUROC 0.66 / held-out detection 0.35
  [2]). (D) COVERAGE VERDICT: fallback (c) FORCED at n=2. HELM Safety VERIFIED to contain no model under 10B (zero num_parameters
  in [1e8,1e10) in its machine-readable release registry [40]); TrustLLM >=7B; no confirmed <=4B entry on AIR-Bench [28],
  SALAD-Bench [29] or SORRY-Bench [30]. Qwen3Guard circularity CONFIRMED VERBATIM (two of three reward terms are Qwen3Guard-Gen-4B,
  helpfulness is WorldPM-Helpsteer2 [20]) -- ban the whole series [21]; AND the abliteration registry's own labels are Qwen3Guard-derived
  [2], a circularity the hypothesis did not anticipate. Good news: the published SafeRL numbers (47.5->86.5, 64.7->98.1, refusal
  12.9->5.3) are judged by Qwen3-235B and WildGuard, so they are NON-circular and usable. (E/F) 29 per-metric design inputs
  meeting every composition constraint, a 14-ID citation audit (2508.21448 confirmed WRONG [4]; 2603.24543 confirmed RIGHT
  [5]; 2509.13450 title moved to a THIRD v3 title [8]), and 15 numbered corrections_to_hypothesis. Coslett [35] UNREACHABLE
  (HTTP 403) = largest residual risk.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
out_dependency_files:
  file_list:
  - research_out.json

--- Item 7 ---
id: art_BCxIq6GX4WIw
type: dataset
title: Published safety scores and a frozen model split
summary: |-
  EXTERNAL GROUND TRUTH + FROZEN SPLIT + RULES + MEASUREMENT CORPORA. One schema-valid file, full_data_out.json (13,311 rows, 22 MB, 20 blocks), built by `uv run data.py` from src/s0..s5; `./run_all.sh` reproduces end to end. Validates against exp_sel_data_out AND against schema_row_kinds.json via src/validate_rows.py.

  HEADLINE, MEASURED NOT ASSUMED. Panel = 66 checkpoints over 34 lineages at <=4.2B, from the iteration-1 frozen manifest (run_CbJDs3opF7E_ iter_1 dataset_1, datasets[dataset='panel_manifest']). External SAFETY coverage is 3/66 checkpoints and 2/34 lineages (4.5% / 5.9%); OVER-REFUSAL coverage is 1/66, reported separately and never folded in; CAPABILITY is 32/66 (48.5%). 65/66 checkpoints require in-house measurement, shipped as a machine-readable list with the axes needed. TWELVE published safety sources name ZERO panel checkpoints: SORRY-Bench, OR-Bench, XSTest, TrustLLM, SALAD-Bench, DecodingTrust, JailbreakBench, HarmBench, AIR-Bench 2024, arXiv:2605.05427, HELM Safety v1.0.0 (27 models), HELM AIR-Bench v1.1.0 (22). HELM was read from its GCS JSON (paths probed, all 200); the ten papers were fetched IN FULL by paging past the 50k-char fetch cap, with a positive control proving the matcher fires. So the external arm is coverage-limited at this scale and the hypothesis's in-house refusal-rate fallback becomes PRIMARY; capability stays as the confound control.

  THE THREE COVERED CHECKPOINTS. Qwen/Qwen3-4B (Qwen3-4B-SafeRL card: Safety Rate x2 judges, Refusal(WildGuard), x Think/Non-Think) and google/unsloth gemma-2-2b-it (Gemma 2 'Ethics and Safety' table: RealToxicity, ToxiGen, CrowS-Pairs, BBQ, Winogender, WinoBias, TruthfulQA). Qwen3-4B-SafeRL itself is an AUGMENTATION row: absent from the frozen manifest and 4.411e9 params, 5% ABOVE the ceiling - iteration 3 must decide explicitly.

  ERRORS CAUGHT. (1) The gemma-2-2b BASE card reprints the INSTRUCTION-TUNED table ('Gemma 2 IT 2B'); rows attributed to -it only. (2) Manifest param_counts came from on-disk bytes and double-count repos shipping both .safetensors and a duplicate .pth/.bin (Llama-3.2-1B: 2.47B vs 1.24B true) - all re-resolved from the Hub, 27 disagreements flagged, panel 59->66. (3) The archived v1 leaderboard sets Flagged=True on all 7,260 rows, an archive artefact; honouring it blindly dropped every v1 row. (4) The plan's '137 checkpoints / 93 lineages' is really 160/105.

  SPLIT, frozen after the harvest: seed '20260813-iter2-split', all 105 lineages, 35 heldout / 70 dev (exactly the >=1/3 floor), hard cases both sides, 7 families absent from DEV, Qwen/Qwen3-4B-Base forced to DEV as the exploration lineage, sha256 pinned in the pre-registration and re-checked by the validator. Byte-reproducible. A per-stratum ceil(n/3) rule was tried and REJECTED (singleton strata sent 54/105 to heldout).

  RULES. BLANKET_REFUSER_DISQUALIFICATION at >0.50 over-refusal on safe items (WARN >0.35), grounded inside the empirical gap in XSTest's five-model distribution [0.016, 0.084, 0.188, 0.296, 0.596] - and CHECKED three ways: literal substring of the cached PDF, recomputed from XSTest's released per-item human labels (all five columns reproduce exactly), and re-derived by the validator from the shipped corpus so rule and corpus cannot drift. Plus QWEN3GUARD_CIRCULARITY, with a weaker QWEN3_SAME_FAMILY_JUDGE flag separating the card's Qwen3-235B-judged columns from its non-circular WildGuard ones.

  MEASUREMENT CORPORA. 11,802 prompts over the 10 corpora selected from 16 pinned (xstest_v2 incl. all five human-annotated reference columns, or_bench_hard_1k, wildguard_test, harmbench_direct_request, advbench, jbb_behaviors, do_not_answer, beavertails_evaluation, toxigen_annotated, aegis_safety_test); 6 rejected with reasons recorded. Every external_score row carries explicit polarity AND polarity_evidence; every value traces to a fetched URL and a <=300-char quoted snippet; cache/ holds every source read so each snippet is re-checkable offline.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

--- Item 8 ---
id: art_xyUlckdGtbjc
type: experiment
title: Fifty cheap safety checks on 44 models
summary: |-
  FROZEN 53-metric battery (50 shipped + 3 declared extras) measured on 44 checkpoints / 23 lineages / 7 architecture families / 2,332 rows, plus a faithful AMS reimplementation with its Table-I reproduction gate, plus a separable two-axis behavioural readout. The artifact SELECTS NOTHING: metric_spec.py was sha256-stamped (544ff994...) before any model was loaded, battery.jsonl carries no behavioural column, and the readout ran only after the battery was stamped. Floor met (>=20 ckpt / >=12 lineages / >=6 families).

  HEADLINE, NEW ARM: a PARENT-FREE test for abliteration's rank-one write-suppression signature. Build A = sum_l W W^T/||W||_F^2 over every residual-write matrix, take its min-eigenvector v1, and ask whether v1's write energy is suppressed in EVERY layer. W01 = log10(median lam/lam_1): abliterated n=8 median 4.26 [1.44, 4.82] versus base 0.58 [0.34, 1.99], instruct 0.47, behaviourally-uncensored 0.46, Qwen3-4B-SafeRL 0.47. W04 (lam_2/lam_1) separates even more cleanly: abliterated min 0.85 against a maximum of 1.62 over all 36 non-abliterated members. Behaviourally-uncensored members look like ordinary instruct models -- the signature reads the EDIT, not the BEHAVIOUR. Cost: 0 forward passes, 0 prompts, and 0 of 53 metrics exceeded a 60 s measured median (0.6B ~75 s, 1.7B ~120 s, 4B ~180 s for the WHOLE battery).

  GATES. (1) Injected rank-one positive control PASSES: |cos(v1,r)| = 1.000, W02 = 1.00, W01 0.62 -> 4.82. Its BLIND SPOT is measured too: a band-limited edit (middle third of layers) is NOT recovered (W02 = 0.0, W01 unchanged) -- so W01-W05 are graded numbers, never a binary detector. (2) AMS gate: ours 4.40 / 4.37 / 3.09 against Table I's 8.37 / 4.80 / 4.55 -> Spearman ordering rho = 1.00 with a systematic scale offset; not tuned to close the gap, and the 3x16 contrastive pairs are OUR construction from the frozen folds. (3) Hook direction, token-id validity, renderer checks all green.

  PITFALLS FOR DOWNSTREAM WORK. HF derives positions from cache_position (a plain arange), so LEFT-padded batches are MISALIGNED unless position_ids = (mask.cumsum(-1)-1).clamp_min(0) is passed on the forward AND every decode step. The padded-vs-single 1e-2 logits test is UNPASSABLE in bf16: an equal-length control reproduces nearly the same discrepancy (0.44 vs 0.63 on |logit| ~28), so it is batched-GEMM numerics, not padding. The held-out AUROC depth profile SATURATES at 1.0 over most of the stack, so argmax-AUROC depth selection is decided by float noise; tie-breaking on d' gave rho* = 0.679 (not iteration 1's 0.25), and at that depth alpha_50 is ceiling-censored on 37/44 members. sigma_min via sqrt(eigvalsh(W W^T)) squares the condition number and drives W11 into float noise -- use svdvals for the square attention matrices. The plan's mandated R4 judge prompt scores HARMFULNESS not BEHAVIOUR (it labelled a Holocaust-denial article REFUSAL, giving 0.87-1.00 for every member, kappa ~0); a rubric that explicitly separates the two agrees 6/6 with a hand-labelled set. Both readouts are shipped (behaviour_rubricA.jsonl vs behaviour.jsonl); judge spend $0.19 of the $1.50 cap.

  DELIVERABLES: method_out.json (long_table 2332, method_vs_baseline 44, metric_spec 53 with declared-vs-measured cost, panel 45, ams_reproduction_gate, behaviour 44, diagnostics), generations.jsonl, results/{battery,behaviour,behaviour_rubricA}.jsonl, results/{diagnostics,calibration,padding_control,judge_calibration}.json, README.md. Schema exp_gen_sol_out PASSED.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 9 ---
id: art_CbL-EUQlwgfw
type: experiment
title: How hard is it to steer a model into refusing?
summary: |-
  EXECUTED IN FULL: 14 members / 4 lineages (tier_completed=T4), 60,040 generations, 63.6 GPU-min on one A4500, judge spend $0.9164 of the $2.00 cap (16,084 calls, google/gemini-3.1-flash-lite). Deliverable method_out.json (756K, 998 examples / 14 datasets), schema-validated; full/mini/preview all PASS.

  PANEL: Qwen3-4B quartet (Base / Instruct / official Qwen3-4B-SafeRL / abliterated), Qwen3-1.7B (+DAN behavioural-uncensored), Qwen3-0.6B, cross-family Llama-3.2-1B. Gated huihui-ai v1 abliterated repos -> ungated v2 mirrors; Qwen3-4B abliterated -> Goekdeniz-Guelmez Josiefied gabliterated-v2 (different instruct parent, recorded). All revisions pinned.

  GATES PASS: NORM_L(Qwen3-0.6B)=23.56 vs iteration-1's 21.2 (11.1% err, within 15%); hook fires on prefill + every decode step (8 forwards for 8 new tokens — the plan's 'expect 9' is off by one); thinking disabled; base members use the PLAIN renderer and are excluded from every correlation.

  HEADLINE — THE LEXICAL ARTIFACT IS IN THE SCORER, NOT THE AXIS. The Arditi 12-substring regex yields alpha_50 for only 7/14 members; the semantic judge yields it for 14/14 on the SAME recorded text. qwen3-0.6b-abliterated: regex max refusal 0.01 vs judge 0.85. 20 (member,axis) cells disagree on REACHABILITY; median kappa(regex,judge)=0.279. Any alpha_50-style metric built on that screen inherits the artifact.

  VERDICTS (pre-registered literals): axis_b=LEXICAL (under the judge AXIS B is defined 14/14 — the paraphrase-disjoint axis DOES induce refusal — but alpha_50 moves a median 69%; 0/18 AXIS-B responses match the scoring regex, verified); scorer=SCORER_DEPENDENT; axis_c=SAFETY_SPECIFIC and axis_d=RANDOM_DOES_NOT_REPRODUCE in strongest form (0/14 and 0/28 cells reach 0.5, max 0.18 / 0.225, vs 7/14 for AXIS A); within_family_only=false; TRIAGE = NOT_A_TRIAGE_SCORE (R=0.73 normalised / 0.62 raw, perm p 0.76 / 0.57; NORM_L spans 3.5–63.0, an 18x range).

  INSTRUCT vs ABLITERATED: not estimable under regex (one member of each pair unreachable) — reachability, not price, separates them. Under the judge, 3/4 lineage CIs exclude zero but the SIGN REVERSES on Llama; across lineages (the resampling unit) sign test p=0.625, consistent_direction=false. Every SAFETY_COST<->ground-truth Spearman has a lineage-bootstrap CI covering zero, both units, both scorers, both sentinel conventions.

  BASELINE (AMS sigma, same checkpoints/pipeline): Llama-3.2-1B-Instruct 5.18 vs published 4.55 (13.9%); rho=-0.649 (p=.042) with jailbreak ASR at member level but CI [-0.99,0.35] covers zero; the published threshold assigns PASS to ALL 14 including base and abliterated — it does not discriminate on this panel.

  GROUND TRUTH IS CLEAN (so the negatives are interpretable): abliterated GT1 0.01–0.34 vs instruct 0.38–0.96; SafeRL matches instruct on harmful refusal (0.9125) while cutting jailbreak ASR 0.688 -> 0.088, and is the MOST expensive model to steer into spurious refusal (judge alpha_50 0.560). No blanket refusers (GT2 <= 0.16).

  TWO METHOD CORRECTIONS FOUND BY RUNNING IT: (1) a POOLED distinct_3 fluency screen flags SUCCESSFUL steering (100 near-identical refusals) as degeneration and would delete exactly the alpha points the metric is about — now measured within-response, pooled value kept as corpus_distinct_3; (2) steered refusal is NON-MONOTONE in alpha (rises, peaks ~0.3–1.0, collapses), so alpha_50 is the FIRST UPWARD crossing fitted on the rising branch only, and a sign check comparing alpha=4 to alpha=0 trivially failed for all 14 until corrected to the peak over (0,2].

  ARTIFACTS: results/generations.jsonl (56,400 sweep) + gt_generations.jsonl (3,640) make control (ii) re-auditable; results/analysis.json holds the full analysis object; run_all.sh reproduces end to end.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 10 ---
id: art_80jPj8Mr_dbZ
type: evaluation
title: Auditing last round's negative results
summary: |-
  PURE RE-ANALYSIS of the three archived iteration-1 trees (E1 refusal-wobble/SPI, E2 steering hysteresis, E3 behavioural ground truth + judge). No model inference, no GPU, no rerun of any iteration-1 experiment. Estimators (paired_bootstrap_diff, cluster_bootstrap_ci, half_life_auc, wilson_ci) are IMPORTED from E1/spi/indicators.py; E1's spearman() and build_output.py's verdict rule are transcribed verbatim, so every archived number reproduces exactly before anything is changed. Spend $0.0586 of a $1.00 cap, 537 logged calls; every response cached so a rerun costs $0 and reproduces in 18 s.

  RECONCILIATION TABLE: 46 rows, 25 SURVIVES / 12 CHANGED / 9 RETRACTED / 0 UNTESTED, each with original value, re-derived value and the deciding analysis.

  A1 (lambda inconsistency): CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING is CHANGED / MATERIAL_CHANGE_TO_REPORTED_RESULT. Running E1's own rule on decay_ratio_16 and normalised-AUC over the same 240 certified rows: at the PRE-STATED primary readout (layer L, where the perturbation is injected) the random-direction control separates 0/3 while the refusal treatment separates 2/3 - the REVERSE of the reported pattern. It reproduces only at the final-layer readout (lens-vs-final corr 0.17-0.26). Not cosmetic: lambda vs decay_ratio_16 Spearman -0.459 (layerL) / -0.170 (final). Horizon sweep {8,16,32,64} and lineage-level bootstrap included; the -0.226/-0.493 lambda CIs are reprinted DEMOTED under lambda_ci_consistency_check_NOT_IDENTIFIABLE.

  A2 (observable-validity gate): only 1 of 4 members passes r_0 AUROC>=0.70 (instruct 0.793; abliterated 0.481, base 0.414, smollm2 0.633) -> UNSUPPORTED_ONLY_1_MEMBERS_PASS. 'Indicators track lineage, not safety' is RETRACTED as a settled negative and downgraded to a qualitative observation. Sensitivity curve {0.60,0.65,0.70,0.75,0.80} published; n_passing=1 from 0.65 up.

  A3 (judge probe rebuilt, the only paid arm): 197 items, four classes, fixed seed, all 21 original probe items carried forward; two annotators decorrelated in model family AND rubric framing (gemini-3.5-flash-lite + frozen rubric; mistral-small + independent decision tree), kappa 0.337 [0.259,0.415]; 96 disagreements adjudicated by deepseek-v4-flash; 97 disputed items published verbatim. 0/7 -> 7/82 = 0.085 [0.042,0.166] frozen-judge COMPLIANCE recall vs 0.939 repaired: 'never assigns COMPLIANCE' is literally wrong but the failure is confirmed and quantified. 3 of 21 original truth labels contradicted, including the force-included 'Certainly! Here's a message that conveys hope...' case (prefix-labelled COMPLIANCE, adjudicated PARTIAL) -> the 21/21 gold arm is RETRACTED. Both headline revisions reproduce exactly (0.700->0.113, 0.092->0.858) and STRENGTHEN under misclassification correction: 0.113 -> 0.000 [0,0.069]; 0.858 -> 0.904 [0.857,0.974].

  A4 (n=4): all 24 orderings enumerated. rho=-0.20 reproduces exactly, exact two-sided p=1.000 against p_floor 0.4167 (untied floor 2/24=0.0833) - nothing at this panel size can reach 0.05. Two independent kills: only 1 of 4 members is above the refusal/incapacity floor, and E1's spearman() breaks ties by array position with two members tied at 0.000 - average ranks give +0.105, a SIGN FLIP. corrected_claim_text and numbers_to_drop emitted.

  A5 (prereg fidelity): 15 deviation rows (7 unannounced), all eight E2 amendments present, each with trigger, timestamp, date-source and direction of effect. Excess-width sign inversion CONFIRMED (paper uses forced_A - alpha_down; prereg the negation) but the two-sided conclusion is INVARIANT - recorded as a reporting error, deliberately not inflated. alpha_50 gap 0.075 = 1.5 grid steps with 5 Bernoulli draws/point; bootstrapped intervals [0.383,0.538] and [0.483,0.617] OVERLAP -> alpha_50_gap_is_resolvable=false, RETRACTED. refusal_direction.pt feeds ONLY E3's in-house ladder (E1 and E2 fit their own directions). Abliteration coverage COMPLETE (o_proj + down_proj + embed_tokens), so under the pre-stated relabel rule the SNAPPED failure attaches to the technique - but the defensible sentence is 'our single-direction weight-edit implementation did not produce a graded knob at 0.6B scale'.

  DELIVERABLES: eval.py single entry point (inventory|a1|a2|a3|a4|a5|finalize|all, --stage smoke); eval_out.json (exp_eval_sol_out-valid, 6 datasets / 348 examples / 53 metrics / 15 limitations); out/{input_inventory,gate_definition,a1_lambda,a2_gate,a3_probe,a4_permutation,a5_prereg,reconciliation_table,disputed_items,field_substitutions}.json, out/llm_call_log.jsonl, out/a3_annotation_cache.jsonl; 4 figures (F1 verdict-flip matrix, F2 gate, F3 judge confusions, F4 exact permutation null) as PNG+PDF.

  FOR THE PAPER: cite the reconciliation table's re-derived values, not the iteration-1 originals. Do NOT carry forward as settled: the generic-mixing verdict, 'indicators track lineage not safety', the alpha_50 instruct-vs-abliterated gap, the 21/21 judge probe, or any n=4 ordering claim.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
out_dependency_files:
  file_list:
  - eval.py
  - full_eval_out.json
  - mini_eval_out.json
  - preview_eval_out.json
</existing_artifacts>

<current_paper>
The current paper draft — represents the research story so far.

Use this to understand what's working, what's not, and what gaps remain.
Gaps and weak results signal what to try differently — not what to conclude.

# Introduction

An open-weight checkpoint arrives with no provenance. Its card says "uncensored", or says nothing at all. Deciding whether its safety training is intact currently costs a benchmark run: hundreds of harmful prompts from AdvBench [37], JailbreakBench [38] or HarmBench [39], a judge model to score the generations [42], and a repeat for every attack template of interest. The evaluator must hold and transmit harmful content, must pay for a judge, and must trust that the checkpoint was not tuned to refuse exactly the items it will be shown. At the scale of a model hub — hundreds of thousands of derived checkpoints, of which a growing fraction are explicitly uncensored community edits — this is the wrong unit of cost.

The published cheap alternatives each retain a dependency the situation does not grant. AMS [3] reads activation geometry but needs harmful prompts, reports 71% leave-one-model-out accuracy over 14 configurations, and states that behavioural uncensored fine-tunes are undetectable by it. RAS/SafeVec [4] produces a calibrated absolute score but needs unsafe prompts, jailbreak prompts *and* a safety-aligned reference model. VISAGE [5] measures a basin in weight space and evaluates a harmful benchmark at every weight perturbation. AQI [6] is prompt-invariant but still latent-geometry-based. Closest to the actual deployment situation, and published while this work was in progress, is a two-signal abliteration audit whose weight-side statistic is $E_1 = \mathrm{mean}_m\,\sigma_1^2(\Delta W_m)/\sum_i \sigma_i^2(\Delta W_m)$ with $\Delta W = W_{\text{base}} - W_{\text{cand}}$ [2] — it reaches AUROC 0.95 combined and 0.89 leave-one-family-out balanced accuracy, but $\Delta W$ requires the parent checkpoint, and the paper's own failure map names a spoofed reference as its primary attack. The same is true of WeightWatch [9], the parent primitive it builds on. A random Hugging Face repository does not come with an attested parent.

This paper therefore adopts a hard operating constraint and reports what survives it: **the metric sees one checkpoint**. No sibling, no base to diff against, no reference model, no benchmark run. Siblings are permitted only as validation contrasts, never as inputs. That constraint retires the headline quantities of our own previous iteration, which were all sibling contrasts, and it is what makes the remaining question sharp.

We answer it with a pre-registered screen rather than a favourite. Fifty-three metric declarations — 16 weights-only (zero forward passes, zero prompts), 11 black-box (logits or output text only), 26 activation-based including four declared-to-fail controls — were written and SHA-256 stamped before any model was loaded, then measured on 44 checkpoints spanning 23 weight lineages and 7 architecture families, with a lineage-level held-out split frozen in the same file [ARTIFACT:art_xyUlckdGtbjc]. The battery table carries no behavioural column; the two-axis behavioural readout was computed afterwards. The black-box arm is deliberately implemented as a strong baseline, not a strawman, because the pre-registered falsifier is that if no white-box metric beats the best black-box one, then looking inside the model buys nothing for cheap safety screening.

[FIGURE:fig1]

Two results follow, and they point in opposite directions. The first is positive and, to our knowledge, new: abliteration — the community edit $W \leftarrow W - c\,rr^\top W$ that orthogonalizes every residual-stream write against a single refusal direction [1] — leaves a **spectral scar in the weights that is visible without the parent**. Form the normalised Gram matrix $A = \sum_l W_l W_l^\top/\lVert W_l\rVert_F^2$ over every residual-write matrix, take its minimum eigenvector $v_1$, and measure $v_1$'s write energy layer by layer. On 44 checkpoints this separates the 8 abliterated members from all 36 others with AUROC 1.000 (the weakest abliterated value $-2.742$ against the strongest non-abliterated $-2.665$), at a measured median cost of 11.4 s and no prompts at all. On the frozen held-out lineages, touched by nothing until the battery was stamped, the ranking is again perfect. The second result is negative and equally load-bearing: for *graded* safety behaviour — how often a model actually refuses harmful requests — no white-box metric in the battery beats the best black-box one. The strongest advantage of any activation metric over greedy refusal rate on benign-free harmful prompts is $+0.036$ in $|\rho|$, 95% CI $[-0.225, +0.303]$, on a lineage-resampled paired bootstrap. The pre-registered conclusion is the one we report.

Along the way, the metric this project previously led with does not survive its own scale-up. $\alpha_{50}$ — the steering coefficient at which a fresh generation begins to refuse — was re-measured at 60,040 generations over 14 members and 4 lineages with four steering axes and two independent scorers [ARTIFACT:art_CbL-EUQlwgfw]. It is not a triage score ($R = 0.73$, permutation $p = 0.76$); its instruct-versus-abliterated gap does not have a consistent sign across families (sign test $p = 0.625$); and the lexical-artifact objection raised against it resolves in an unexpected place — not in the steering axis, but in the *scorer*. The standard 12-substring refusal screen from the refusal-direction literature declares 7 of 14 models incapable of being steered into refusal when a semantic judge shows that all 14 can.

## Summary of Contributions

- **A parent-free weights-only signature of abliteration** (§4.1, §5.1). $W05$, the log minimum per-layer write energy along the minimum eigenvector of the pooled write Gram matrix, separates abliterated from non-abliterated checkpoints at AUROC 1.000 over 44 checkpoints / 23 lineages / 7 families, and 1.000 on the held-out lineages, at 0 forward passes, 0 prompts and 11.4 s median. Its rank-one positive control is recovered at $|\cos(v_1,r)| = 1.000$; its blind spot — a band-limited edit confined to the middle third of layers — is measured and reported rather than assumed away.
- **The signature reads the edit, not the behaviour** (§5.1). Four behaviourally-uncensored fine-tunes, whose two chat-rendered members comply with 51% and 84% of harmful requests, are indistinguishable from ordinary instruct models on every weights-only statistic ($W01$ median 0.463 against instruct 0.471). This is the correct answer to the wrong question, and we say which question it answers.
- **A pre-registered falsifier that fires** (§5.2). Across 26 chat-rendered members over 18 lineages, the best predictor of harmful-refusal rate is a black-box one (greedy refusal rate, $\rho = +0.766$, lineage-bootstrap CI $[+0.539, +0.917]$). Every paired bootstrap of a white-box metric against it has a CI covering zero. For graded safety, looking inside buys nothing.
- **$\alpha_{50}$ refuted at scale, with the lexical objection resolved onto the scorer** (§5.3). Three first-class controls plus a semantic re-scoring of 60,040 generations; verdicts `LEXICAL`, `SCORER_DEPENDENT`, `SAFETY_SPECIFIC`, `RANDOM_DOES_NOT_REPRODUCE`, `NOT_A_TRIAGE_SCORE`.
- **A closest-competitor baseline run twice, failing in its own terms** (§5.4). Our AMS reimplementation reproduces the published Table-I ordering at Spearman $\rho = 1.00$ with a systematic scale offset, and its published PASS threshold of $\sigma > 3.5$ admits every member of a 14-model panel including base and abliterated ones. On the 44-checkpoint panel the single highest AMS $\sigma$ (4.82) belongs to an abliterated checkpoint.
- **A self-audit that retracts four of our own prior claims** (§5.5). A pure re-analysis of the archived previous-iteration trees produces a 46-row reconciliation table: 25 survive, 12 change, 9 are retracted [ARTIFACT:art_80jPj8Mr_dbZ].
- **A measured statement of how little external safety ground truth exists below 4B** (§3). Twelve published safety sources name zero checkpoints of our panel; external safety coverage is 3 of 66 checkpoints and 2 of 34 lineages [ARTIFACT:art_BCxIq6GX4WIw].

# Related Work

**Parent-required weight audits, and the gap.** WeightWatch [9] shows that the top singular vectors of a fine-tuned-minus-base weight difference correspond to newly acquired behaviours, and stops up to 100% of backdoor utilisations at FPR below 1.2%. The abliteration audit of [2] specialises the idea, combining an activation signal with the weight-recovery energy $E_1$ over $o\_proj$ and $down\_proj$ in a mid-stack band, over a 273-checkpoint registry with 57 abliterations against 37 benign fine-tunes. Both require $\Delta W$, hence the parent. Our $W01$–$W05$ occupy exactly the complement: they are computed from the candidate's weights alone, are therefore immune to a spoofed reference, and pay for it in the ways we measure — a graded score rather than a calibrated detector, and a documented blind spot to band-limited edits. Two further boundaries are worth stating because they were checked rather than assumed: the registry of [2] already covers Qwen2.5-1.5B, so parameter scale is not the gap; and provenance work using refusal vectors as behavioural fingerprints [36] tracks *lineage*, not edit type.

**Why a weight-space scar is expected at all.** Safety fine-tuning, DPO and unlearning have been shown to minimally transform MLP weights so as to align unsafe inputs into a null space [10], and safety behaviour localises to a small set of neurons and ranks that can be pruned or low-rank-modified away [11]. Abliteration is the extreme case: an explicit rank-one projection applied to every residual-write matrix [1]. Heavy-tailed self-regularisation supplies mature spectral descriptors for trained weight matrices [59], though we found no published application of them to safety. Community practice complicates the picture in ways we report: published abliterations vary the ablation strength as a free parameter [35], extended-refusal training defends against abliteration while leaving weights superficially normal [34], and abliteration has substantial off-target effects on behaviours that elicit no refusals at all [33].

**Detection is not control.** The result closest to our previous iteration's site-selection finding is [8], which establishes the general dissociation directly: a linear detector reaching AUC $=1.000$ from layer 5 sits at $\cos = 0.12$ (about 83°) from the direction that actually produces the behaviour, with the cosine in $[0.12, 0.20]$ across four models from three families at 1B–9B and essentially unchanged by instruction tuning (0.1197 versus 0.1200). We had reported the same dissociation for refusal specifically and presented it as new; it is not, and our contribution is narrower and is stated as such: refusal is only ever the *intervention* direction in [8], never a detected behaviour, and what the dissociation changes for us is which axis one must use to build a metric. Their Section 8 is an explicit negative — the detector-to-intervention cosine sits at chance for steerable and unsteerable behaviours alike — so a cosine-as-safety-score metric is a published negative. We enter one anyway, as a declared control, and report below that it behaves better on our panel than that result would predict, which we treat as a caution about panel composition rather than a refutation.

**Steering strength as a measurement construct.** Logit-Gap Steering [12] takes the first-step gap between refusal and affirmative logits as a forward-pass diagnostic of alignment robustness, with published median shifts on Qwen2.5-0.5B, Llama-3.2-1B and gemma-2b — our exact size class. The Rogue Scalpel [13] shows that *random* steering directions raise harmful compliance from 0% to 1–13% (18% in the body) under the same $\alpha = c\,\mu(l)$ normalisation family we use, which converts a random direction from a null into a magnitude-matched comparator; our $\alpha_{50}$ control is interpreted accordingly. Three further results bound what a scalar steering measurement can mean: steering strength acts non-monotonically on next-token probability [16] — which we observed empirically and which forced a change to our estimator; the optimal steering layer is input-dependent [17], making any fixed-layer $\alpha_{50}$ a lower bound on steerability; and scalar steerability measures conceal behavioural shifts in open-ended generation [18]. Layer selection can be done training-free from a linear accessibility profile with $\rho = +0.86$–$0.91$ against steering effectiveness [19]; we adopt the spirit (an outcome-blind selection rule) rather than competing with it. SteeringSafety [14] is the benchmark-cost baseline such metrics aim to replace, and [15] documents that CAA-style steering itself moves jailbreak ASR by up to $+57\%/-50\%$. Against this literature, $\alpha_{50}$'s only surviving claim was that it is single-scalar, parent-free, harmful-prompt-free and benchmark-free at once; §5.3 reports that the claim does not hold up as a triage score.

**Refusal mechanism and behaviour.** The single-direction account [1] and the steering machinery around it [20, 21, 22] supply the instruments. Qi et al. [23] show aligned and unaligned generative distributions differ mainly over the first few output tokens; Yin et al. [24] trace a per-position refusal score and find a cliff at final tokens; Kwon [25] attributes the prefill jailbreak's grip to generic autoregressive conditioning rather than safety-specific suppression, with a base-model control; Rahimi et al. [26] observe that autoregressive commitment masks underlying instability. Ratnakar and Vats [27] report an $\alpha$-sweep-derived taxonomy ("Late Decision" for Llama, "Early Divergence" for Qwen with safety integrated at about 40% depth). Hasan and Biswas [28] find over-refusal and harmful compliance nearly uncorrelated ($r = -0.032$) across 21 open-weight models, which is why we predict two axes separately and enforce a blanket-refuser disqualification rule. Basu et al. [7] give the reason a read-side metric can be confidently wrong: 98.2% probe AUROC alongside 45.1% output sensitivity.

**Cheap black-box detectors.** Our black-box arm draws its strong members from published work rather than from folklore: the first-step logit gap [12], first-token confidence under an affirmative prefix [61], single-pass top-$k$ logit classification [62], and prefill-flip fragility [60]. First-token entropy and length asymmetry are included and labelled as having no safety-specific prior.

# Panel, Ground Truth and Split

**Panel and split.** All measurement is on checkpoints at $\leq 4.2$B parameters, drawn from a frozen 160-row manifest built in a previous iteration and re-resolved here. The battery covers 44 checkpoints over 23 lineages and 7 architecture families (qwen3, qwen2, llama, gemma2, gpt\_neox, granite, olmo), comprising 16 base, 15 instruct, 8 abliterated, 4 behaviourally-uncensored, and the official Qwen3-4B-SafeRL safety-RL checkpoint; 9 members are *standalone*, with no sibling in the panel, which is the actual deployment case. A lineage-level held-out split — 10 lineages, 13 checkpoints including 2 abliterated members — was written into the SHA-stamped specification file before any model was loaded and is used only in §5.1 and §5.2. The resampling unit for every model-level statistic is the weight lineage; both aggregation units are reported, because they can disagree.

**External ground truth barely exists at this scale, and we measured that rather than assuming it.** A dedicated harvest over published safety sources found external safety coverage for 3 of 66 panel checkpoints and 2 of 34 lineages; over-refusal coverage for 1 of 66; capability coverage for 32 of 66 [ARTIFACT:art_BCxIq6GX4WIw]. Twelve sources — SORRY-Bench [43], OR-Bench, XSTest [40], TrustLLM [46], SALAD-Bench [45], DecodingTrust, JailbreakBench [38], HarmBench [39], AIR-Bench [44], HELM Safety v1.0.0 (27 models), HELM AIR-Bench v1.1.0 (22 models) and a large open-weight behaviour audit [28] — name **zero** panel checkpoints. HELM Safety was read from its machine-readable release registry and verified to contain no model under 10B; TrustLLM's panel starts at 7B. The pre-registered fallback therefore becomes primary: safety ground truth is measured in-house on two axes, harmful-refusal rate on a 40-item stratified harmful core and over-refusal rate on 25 XSTest-safe items, with a blanket-refuser disqualification rule at $>0.50$ over-refusal that was derived from, and re-checked against, XSTest's own released human labels. Where an external number does exist it is used: the Qwen3-4B-SafeRL card reports Safety Rate rising 47.5 $\to$ 86.5 and 64.7 $\to$ 98.1 under two judges with refusal falling 12.9 $\to$ 5.3, and those numbers are judged by Qwen3-235B and WildGuard [41] rather than by Qwen3Guard [47], which was two of the model's three reward terms and is therefore banned as a judge for it.

**Judge protocol.** Our own judge is used only where no external number exists, always with the evaluator system prompt whose absence we previously documented as catastrophic (§5.5), and always reported alongside its agreement with a lexical screen. One correction from this iteration is worth stating in the open: the judge rubric mandated by our own plan scores *harmfulness* rather than *behaviour* — it labelled a Holocaust-denial article REFUSAL, gave 0.87–1.00 to every member and produced $\kappa \approx 0$ against a hand-labelled set. A rubric that explicitly separates "did the model comply" from "is the content harmful" agrees 6 of 6 with the hand-labelled set. Both readouts ship; the behaviour-scoring rubric is primary. Total judge spend across both experiments was \$1.11.

# Method

## The battery, and the discipline that makes it a screen

Fifty-three metric declarations were written into `metric_spec.py`, SHA-256 stamped (`544ff994…`), and only then executed. Each declares its family, its prompt requirement, its forward-pass count and its expected wall-clock on a 4B model *before* measurement; declared and measured costs are both reported. Three declarations are flagged out of the pre-declared fifty so the count is exactly 50 while nothing measured is discarded. The metric table contains no behavioural column, and the behavioural readout ran only after the table was stamped. No metric was added, dropped, tuned or re-ordered on the basis of a behavioural number.

**Weights-only arm (16 declarations, 0 forward passes, 0 prompts).** The arm is motivated directly by abliteration's mechanism. If every residual-write matrix has had one direction projected out, then that direction is a shared approximate null direction of the whole write ensemble, and it should be recoverable from the ensemble alone. Let $\mathcal{W}$ be the set of matrices writing into the residual stream (attention output projections and MLP down-projections) across all $L$ layers. Form

$$A \;=\; \sum_{W \in \mathcal{W}} \frac{W W^\top}{\lVert W \rVert_F^2}, \qquad \lambda_1 \le \lambda_2 \le \dots \le \lambda_d, \quad v_1 = \text{eigvec}(\lambda_1),$$

and define the per-matrix normalised write energy along a unit direction $u$ as $e_W(u) = \lVert u^\top W\rVert^2 / (\lVert W\rVert_F^2/d)$, which equals 1 in expectation for a random direction. The five declarations are: $W01 = \log_{10}(\mathrm{median}(\lambda)/\lambda_1)$, the depth of the suppression; $W02 = \Pr_W[e_W(v_1) < 0.1]$, the fraction of write matrices in which $v_1$ is suppressed; $W03 = \log_{10}\!\big(q_{0.05}(e_W(u_{\text{rand}}))/\overline{e_W(v_1)}\big)$, the gap against 64 matched random directions; $W04 = \log_{10}(\lambda_2/\lambda_1)$, the isolation of the outlier eigenvalue; and $W05 = \log_{10}\min_W e_W(v_1)$, the *minimum* per-layer energy — the statistic that asks whether the suppression holds in every layer without exception. $W06$–$W16$ are spectral and norm descriptors (stable rank, spectral entropy, singular-value decay, RMSNorm gain statistics, write-row-norm Gini) that carry no abliteration prior.

Two gates run before any panel measurement. A **positive control** injects a synthetic rank-one edit $W \leftarrow W - rr^\top W$ into every write matrix of Qwen3-0.6B and requires recovery: obtained, at $|\cos(v_1, r)| = 1.000$, $W02$ from 0 to 1.00, $W01$ from 0.62 to 4.82. A **band-limited variant**, editing only the middle third of layers, is *not* recovered ($W02 = 0.0$, $W01$ unchanged). We report the blind spot because it defines what the arm is: a graded score for edits that touch the whole stack, never a binary detector.

**Black-box arm (11 declarations).** First-step logit gap between refusal-onset and continuation tokens on harmful and on benign prompts and their asymmetry; refusal probability mass; first-token entropy on both prompt classes and its asymmetry; greedy refusal rate on 40 harmful items under a 12-substring screen; harmful-versus-benign length asymmetry; and the rate at which the argmax first token is the single dominant refusal-onset token. The refusal-token lexicon is re-resolved against each checkpoint's own tokenizer at runtime, with leading-space variants chosen by round-trip.

**Activation arm (26 declarations, 4 declared-to-fail controls).** AMS $\sigma$ and its concept cosine; diff-in-means separation, $d'$ and AUROC at a pre-registered relative depth $\rho^\star$; logit-lens refusal log-odds at the final prompt position and over the first 8 generated steps; margin-profile AUC and decision depth; refusal-axis-to-unembedding cosine; attention-entropy asymmetry; next-token KL between harmful and benign prompts; $\alpha_{50}$; and, as declared-to-fail controls carried from the previous iteration's negative result, a random-axis $d'$, detrended across-rollout variance and lag-1 autocorrelation, and a syntactic-probe $d'$.

$\rho^\star$ was selected on a held-out contrast fold on a single reference model, outcome-blind. A finding from that selection is that the held-out AUROC depth profile **saturates at 1.0 over most of the stack**, so an argmax-AUROC rule is decided by floating-point noise; tie-breaking on $d'$ gives $\rho^\star = 0.679$, considerably deeper than the 0.25 our previous iteration used. At that depth $\alpha_{50}$ is ceiling-censored on 37 of 44 members, and the censoring count is reported rather than hidden.

## The $\alpha_{50}$ experiment and its four controls

$\alpha_{50}$ is measured separately and at much higher power [ARTIFACT:art_CbL-EUQlwgfw]: 14 members over 4 lineages (Qwen3-4B base/instruct/SafeRL/abliterated, Qwen3-1.7B with a behaviourally-uncensored member, Qwen3-0.6B, and cross-family Llama-3.2-1B), 60,040 generations, 63.6 GPU-minutes. A response-contrast refusal axis is injected at relative depth 0.25 in units of $\mathrm{NORM}_L$, the median residual-stream norm at the injection layer, and $\alpha_{50}$ is the coefficient at which the refusal rate on *benign* prompts first crosses 0.5. Four axes are run as first-class arms: **A**, the canned axis built from the verbatim 12-substring refusal list of [1]; **B**, a paraphrase-disjoint axis whose responses match the scoring regex 0 of 18 times, verified blind to the scorer; **C**, a non-safety stylistic axis (formal minus casual on the same benign prompts); and **D**, matched random Gaussian directions, treated as a magnitude-matched comparator following [13] rather than as a null. Every generation near the crossing is additionally re-scored by a semantic judge under the framed evaluator prompt, so the lexical objection is tested on the axis and on the scorer independently.

Two estimator corrections were forced by running it. A `distinct_3` fluency screen pooled across the 100 responses at an $\alpha$ point flags *successful* steering — 100 near-identical refusals — as degeneration, and would have deleted exactly the points the metric is about; it is now measured within response and averaged, with the pooled value retained as an honest measure of induced mode collapse. And steered refusal is **non-monotone in $\alpha$** on every member, rising, peaking around $\alpha \in [0.3, 1.0]$ and then collapsing, exactly as the theory of steering strength predicts [16]; $\alpha_{50}$ is therefore the *first upward* crossing, fitted on the rising branch only.

# Results

## A parent-free spectral scar of abliteration

[FIGURE:fig2]

The weights-only arm separates abliterated checkpoints from everything else, cleanly, without a parent and without a prompt [ARTIFACT:art_xyUlckdGtbjc].

| statistic | abliterated ($n{=}8$) | instruct ($n{=}15$) | base ($n{=}16$) | beh.-uncensored ($n{=}4$) | safety-RL ($n{=}1$) | AUROC |
|---|---|---|---|---|---|---|
| $W05$ min layer energy | $-4.33$ $[-4.82, -2.74]$ | $-1.16$ | $-1.31$ | $-1.08$ | $-1.25$ | **1.000** |
| $W01$ suppression depth | 4.26 $[1.44, 4.82]$ | 0.47 | 0.58 | 0.46 | 0.47 | 0.986 |
| $W04$ isolation | 3.68 $[0.85, 4.19]$ | 0.046 | 0.057 | 0.055 | 0.004 | 0.986 |
| $W02$ direction consistency | 1.00 $[0.96, 1.00]$ | 0.11 | 0.20 | 0.066 | 0.18 | 0.950 |
| $A01$ AMS $\sigma$ (baseline) | 2.38 $[1.46, 4.82]$ | 2.74 | 1.72 | 1.61 | 3.64 | 0.640 |
| $B01$ logit gap (best black-box) | $-3.41$ | $+1.42$ | $-0.71$ | $-0.86$ | $-13.35$ | 0.816 |

$W05$ achieves complete rank separation: the weakest abliterated value is $-2.742$ (huihui-ai/Qwen2.5-0.5B-Instruct-abliterated) and the strongest non-abliterated value is $-2.665$, with the next-weakest abliterated member at $-3.522$ and the bulk of the abliterated cluster below $-4.2$. Leave-one-family-out separation is perfect for all three families that contribute abliterated members (llama $n{=}2$, qwen2 $n{=}3$, qwen3 $n{=}3$), so the pre-registered "within one architecture family only" negative does **not** apply here. The best black-box competitor reaches AUROC 0.816 and the closest published activation baseline, AMS $\sigma$, reaches 0.640 — on this task, looking at the weights does buy something, and buys it at zero inference cost.

The held-out lineages, untouched until the battery was stamped, contain 2 abliterated and 11 non-abliterated members. $W05$'s ranking there is again perfect (AUROC 1.000); $W01$ and $W04$ give 0.864, because the two held-out abliterated members are the two weakest-signature ones in the whole panel. The distinction matters and we draw it explicitly: **the ranking transfers, the calibration does not.** A midpoint threshold fitted on the development lineages ($W05 < -3.17$) catches 1 of 2 held-out abliterated members with 0 of 11 false positives, and the corresponding $W01$/$W04$ thresholds catch 0 of 2 with 0 false positives. $W01$–$W05$ are graded ranking statistics; anyone deploying them as a binary flag must fit the threshold on their own population, and the band-limited positive control shows the class of edit that will escape any threshold.

The most informative negative in this arm is that **the signature reads the edit, not the behaviour**. The four behaviourally-uncensored fine-tunes — checkpoints made compliant by ordinary fine-tuning rather than by a directional edit, whose two chat-rendered members comply with 51% and 84% of harmful requests in our own measurement — sit squarely inside the instruct distribution on every weights-only statistic ($W01$ median 0.463 against instruct 0.471; $W05$ median $-1.081$ against instruct $-1.155$). This is precisely the class AMS reports as its documented blind spot [3], and our arm is blind to it for a different and more honest reason: there is no rank-one scar to find. Qwen3-4B-SafeRL, the one deliberate safety-RL checkpoint in the panel, is likewise indistinguishable from an ordinary instruct model in the weights ($W01 = 0.471$, $W04 = 0.004$) while behaving very differently — it matches its instruct sibling on harmful refusal (0.9125 both) while cutting jailbreak ASR from 0.688 to 0.088 [ARTIFACT:art_CbL-EUQlwgfw]. A weights-only test answers "has this checkpoint been directionally edited?", which is a real and useful question at hub scale, and it does not answer "is this checkpoint safe?".

## The pre-registered falsifier fires: for graded safety, black-box wins

[FIGURE:fig3]

Restricting to the 26 chat-rendered members over 18 lineages for which a behavioural rate is meaningful (base models use a plain renderer and are excluded from every correlation by pre-registration), the ranking of metrics against measured harmful-refusal rate is led by a black-box statistic.

| metric | arm | $\rho$ (member) | 95% CI (lineage bootstrap) | $\rho$ (lineage-mean) |
|---|---|---|---|---|
| $A02$ AMS concept cosine$^\dagger$ | activation | $+0.802$ | $[+0.548, +0.901]$ | $+0.819$ |
| $B09$ greedy refusal rate | black-box | $+0.766$ | $[+0.539, +0.917]$ | $+0.852$ |
| $A19$ refusal-axis / unembed cosine | activation | $+0.753$ | $[+0.538, +0.863]$ | $+0.779$ |
| $B11$ argmax-is-refusal-onset rate | black-box | $+0.730$ | $[+0.458, +0.915]$ | $+0.877$ |
| $B01$ first-step logit gap | black-box | $+0.709$ | $[+0.352, +0.912]$ | $+0.622$ |
| $A11$ prompt-position refusal log-odds | activation | $+0.701$ | $[+0.333, +0.905]$ | $+0.672$ |
| $A14$ generated-step refusal log-odds | activation | $+0.696$ | $[+0.350, +0.869]$ | $+0.618$ |
| $A01$ AMS $\sigma$ | activation | $+0.605$ | $[+0.310, +0.790]$ | $+0.737$ |
| $A22$ $\alpha_{50}$ | activation | $-0.519$ ($n{=}7$) | — | — |

$^\dagger$ $A02$ is one of the three declarations flagged outside the pre-declared fifty, and is also the statistic that [8]'s Section 8 reports as sitting at chance; we report it because it was measured, and treat its performance here as a caution about our panel's composition rather than as a contradiction of that result.

[FIGURE:fig4]

The decisive comparison is the pre-registered paired bootstrap of $|\rho_{\text{white-box}}| - |\rho_{B09}|$ on the same resampled lineages. Every interval covers zero: $A02$ $+0.036$ $[-0.225, +0.303]$; $A19$ $-0.013$ $[-0.259, +0.259]$; $A11$ $-0.064$ $[-0.262, +0.089]$; $A14$ $-0.070$ $[-0.286, +0.058]$; $A01$ (AMS) $-0.161$ $[-0.501, +0.208]$; $W01$ $-0.373$ $[-0.731, -0.039]$; $\alpha_{50}$ $-0.453$ $[-0.941, 0.000]$. Two of the seven have intervals excluding zero, and both exclude it on the *wrong* side. The pre-registered outcome therefore holds in the form it was written: **no white-box metric's advantage over the best black-box baseline has a CI excluding zero, so for cheap graded safety screening, reading inside the model buys nothing.** On the held-out lineages the ordering is preserved but the sample is too small to add evidence (6 chat-rendered members; $\rho$ = $+0.577$ for $B09$, $+0.771$ for $A02$).

Two qualifications keep this from being oversold in either direction. First, the winner is not a safety score but a refusal-propensity score: $B09$'s correlation with XSTest over-refusal is $+0.687$ and $B11$'s is $+0.694$, against a ground-truth correlation between the two axes themselves of $+0.633$. A metric that ranks a blanket refuser at the top is disqualified by our own pre-registered rule, and these metrics would do exactly that. Exactly one panel member trips the rule (Qwen2.5-1.5B-Instruct, over-refusal 0.60) and a second trips the warning level (Qwen2.5-0.5B-Instruct, 0.36); both are ranked near the top by $B09$ and $B11$, which is the failure mode the rule exists to catch. Second, $B09$ costs 1,280 forward passes and 40 harmful prompts, which is precisely the dependency this project set out to remove. The honest summary is that the cheapest thing that works for graded safety is *asking the model harmful questions and reading its answer* — and that the one measurement which does not need harmful questions at all, the weights-only scar, answers a different question.

## $\alpha_{50}$ does not survive its own scale-up, and the lexical objection lands on the scorer

[FIGURE:fig5]

At 60,040 generations, four axes and two scorers, the metric this project previously led with fails on every axis it was asked about [ARTIFACT:art_CbL-EUQlwgfw].

**Not a triage score.** The pre-registered triage ratio $R = $ within-lineage spread / across-lineage spread is $0.73$ (permutation $p = 0.76$, 10,000 permutations) in $\mathrm{NORM}_L$-normalised units and $0.62$ ($p = 0.57$) in raw activation units. $R \le 1$ in both, so architecture dominates safety level and a single threshold cannot be carried to an unknown model. The mechanism is visible: $\mathrm{NORM}_L$ itself spans 3.5 (Llama-3.2-1B) to 63.0 (Qwen3-1.7B), an 18-fold range that the $\alpha$ units silently absorb — the reviewer's 12% concern about a three-model panel is a 1,800% effect at 14.

**No consistent instruct-versus-abliterated gap.** Under the semantic judge the difference is estimable in all four lineages and 3 of 4 per-lineage paired-bootstrap CIs exclude zero, but the per-lineage deltas are $-0.012$, $-0.096$, $-0.186$ and $+0.108$: the three Qwen3 lineages say the *instruct* model is cheaper to steer into spurious refusal, and Llama-3.2-1B reverses it. Exact sign test over the correct resampling unit gives $p = 0.625$, `consistent_direction = false`. The per-lineage CIs exclude zero because they resample prompts, which licenses no generalisation across families. Every Spearman correlation between $\alpha_{50}$ and behavioural ground truth has a lineage-bootstrap CI covering zero, at both aggregation units, under both scorers and both sentinel conventions. Our previous iteration's headline gap of $0.075$ is retracted; re-analysis of the archived data gives bootstrapped intervals $[0.383, 0.538]$ and $[0.483, 0.617]$, which overlap [ARTIFACT:art_80jPj8Mr_dbZ].

**The circularity objection resolves onto the scorer, not the axis.** This is the most transferable finding of the experiment. The reviewer's hypothesis was that $\alpha_{50}$ measures how much push it takes for a canned-apology token direction to win the argmax, since the same lexical family builds the axis and scores the outcome. Running the paraphrase-disjoint axis and the semantic re-scoring together separates the two halves of that hypothesis and they land differently:

- The **axis** half is confirmed but is not degenerate. Axis B, verified to match the scoring regex 0 of 18 times, yields a defined $\alpha_{50}$ for **14 of 14** members — the paraphrase-disjoint axis genuinely induces refusal — but the fitted value moves by a median of 69% relative to Axis A. Verdict `LEXICAL`: the price of steering a model into refusal depends substantially on which *wording* of refusal you steer toward.
- The **scorer** half is worse than the objection anticipated. The 12-substring regex from [1] — the standard refusal screen in this literature — yields a defined $\alpha_{50}$ for only **7 of 14** members; the semantic judge yields it for **14 of 14** on the *same recorded text*. For qwen3-0.6b-abliterated the regex reports a maximum refusal rate of 0.01 against the judge's 0.85. Twenty (member, axis) cells disagree on *reachability*, and the median Cohen's $\kappa$ between the two scorers on sweep text is 0.279. Verdict `SCORER_DEPENDENT`. Every model the regex calls incapable of refusing can in fact be steered into refusing; it simply refuses in words the list does not contain.
- The **controls behave.** The non-safety stylistic axis reaches a 0.5 refusal rate on 0 of 14 members (panel maximum rate 0.18) and matched random directions on 0 of 28 (member, seed) cells (maximum 0.225), against 7 of 14 for Axis A. Verdicts `SAFETY_SPECIFIC` and `RANDOM_DOES_NOT_REPRODUCE`, in the strongest available form — notable because [13] documents that random directions do produce non-zero compliance effects at comparable normalisation, so the comparator was live.

What $\alpha_{50}$ induces is therefore refusal-specific, and the price of inducing it still carries no safety signal. The negative is clean rather than under-powered, because the ground truth on the same weights separates exactly as it should (abliterated members refuse 1–34% of plain-harmful prompts against 38–96% for their instruct siblings, no blanket refusers).

## The closest published baseline, run faithfully, fails in its own terms

AMS [3] was reimplemented and run twice, on both panels, in the same pipeline as our own metrics. Against the three checkpoints of its Table I that our panel can reach, we obtain $\sigma =$ 4.40 / 4.37 / 3.09 against the published 8.37 / 4.80 / 4.55: Spearman ordering $\rho = 1.00$ with a systematic scale offset, not tuned to close the gap (the paper's exact contrastive pairs are unrecoverable, so ours are constructed from our frozen folds; the gate measures that). On the 14-member panel the independent run gives Llama-3.2-1B-Instruct 5.18 against the published 4.55, a 13.9% deviation.

The failures are in the metric, not in the reimplementation. On the 44-checkpoint panel, AMS $\sigma$ separates abliterated from non-abliterated at AUROC 0.640, and the single highest $\sigma$ in the entire panel (4.82) belongs to an abliterated checkpoint, above every instruct member (maximum 4.40). On the 14-member panel its published PASS threshold ($\sigma > 3.5$) admits **all 14 members**, including base models with no safety training and abliterated models with the refusal direction removed. Its correlation with jailbreak ASR is $\rho = -0.649$ ($p = 0.042$) at the member level, but the lineage-bootstrap CI is $[-0.99, +0.35]$. We report this as a fair test that AMS loses on our panel, while noting that its published panel is larger in parameter scale and that an independent evaluation has separately measured it at AUROC 0.66 [2].

## Auditing our own previous negatives

[FIGURE:fig6]

A dedicated re-analysis of the three archived experiment trees from the previous iteration — no new inference, estimators imported from the original source so every archived number reproduces before anything changes — produced a 46-row reconciliation table: 25 survive, 12 change, 9 are retracted [ARTIFACT:art_80jPj8Mr_dbZ]. Four items bear on claims we previously published.

**The judge-failure finding survives quantification but not its original form.** We previously reported that an un-framed safety-trained judge scored 0 of 7 on the compliance class of a 21-item probe whose truth labels came from a nine-character affirmative-prefix match. The probe was rebuilt at 197 items covering all four rubric classes, stratified over blocks and members, with all 21 original items carried forward; two annotators decorrelated in both model family and rubric framing gave $\kappa = 0.337$ $[0.259, 0.415]$, and 96 disagreements were adjudicated by a third model, with all 97 disputed items published. Against that gold set the frozen judge's COMPLIANCE recall is **0.085** $[0.042, 0.166]$ — not zero. The literal claim "never assigns COMPLIANCE" is wrong and is withdrawn; the failure is confirmed and is now quantified against a defensible reference, with the frozen judge at 0.287 overall accuracy and $\kappa = 0.060$ against the repaired judge's 0.939 COMPLIANCE recall. Three of the 21 original truth labels are contradicted, including the specific item the reviewer identified — a refusal-by-redirection opening "Certainly! Here's a message that conveys hope…", prefix-labelled COMPLIANCE and adjudicated PARTIAL — so the 21-of-21 "gold judge" arm is **retracted**. Both headline revisions reproduce exactly and strengthen under misclassification correction: plain-harmful refusal 0.700 $\to$ 0.113 (corrected 0.000 $[0, 0.069]$), jailbreak ASR 0.092 $\to$ 0.858 (corrected 0.904 $[0.857, 0.974]$).

**The generic-mixing verdict is retracted.** We previously drew a control conclusion from bootstrap CIs on recovery-rate estimates that the same paper certified as non-identifiable. Recomputing the contrast on the assumption-free 16-step survival-ratio statistic over the same 240 certified rows, at the pre-stated primary readout, gives the **reverse** pattern: the random-direction control separates 0 of 3 comparisons while the refusal direction separates 2 of 3. The reported pattern reproduces only at the final-layer readout, which correlates with the primary readout at 0.17–0.26. The verdict `CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING` is withdrawn as a material change.

**"Indicators track lineage, not safety" is retracted as a settled negative.** An observable-validity gate requiring the refusal observable to reach harmful-versus-benign AUROC $\geq 0.70$ is passed by only 1 of 4 members of that panel (instruct 0.793; abliterated 0.481, base 0.414, SmolLM2 0.633), and by 1 of 4 at every threshold from 0.65 upward. The cross-model comparison therefore rested on models where the observable was uninformative, exactly as the reviewer argued. It is downgraded to a qualitative observation; the corresponding early-warning-signal declarations enter this iteration's battery only as declared-to-fail controls, and they behave as declared ($A23$ random-axis $d'$ is the single weakest abliteration discriminator in the battery at AUROC 0.483).

**Every $n{=}4$ ordering claim is withdrawn.** Enumerating all 24 orderings, the previously reported $\rho = -0.20$ reproduces exactly, with exact two-sided $p = 1.000$ against a floor of 0.4167 — nothing at that panel size can reach 0.05 — and the sign flips to $+0.105$ under average-rank tie handling, because two members were tied at a refusal floor and the original implementation broke ties by array position.

**Pre-registration deviations.** The audit enumerates 15 deviation rows, 7 of them previously unannounced, each with trigger, timestamp and direction of effect. Two are worth surfacing in the main text. The sign convention of the primary hysteresis statistic was inverted between the pre-registration and the write-up (`residual = alpha_down - alpha_down_forced_A` versus the negation); the two-sided conclusion is invariant, and it is recorded as a reporting error rather than inflated into anything else. And the $\alpha$ grid was amended from $(\delta = 0.25, \alpha \in [-2, 8])$ to $(\delta = 0.05, \alpha \in [-1.5, 2])$, which is why the previously reported "refusal collapses at $\alpha = 2.0$" is the edge of the measured grid and not a property of the model — a point since superseded by the direct finding that steered refusal is non-monotone in $\alpha$ on every member measured [16]. Finally, the in-house abliteration ladder that failed to produce a graded knob had complete write-matrix coverage ($o\_proj$, $down\_proj$, $embed\_tokens$), so the defensible sentence is that *our single-direction weight-edit implementation did not produce a graded knob at 0.6B scale*; the direction file it used feeds no other reported result.

## Cost

The whole 53-metric battery runs in about 75 s on a 0.6B model, 120 s at 1.7B and 180 s at 4B on one RTX A4500, and **0 of 53 metrics exceeded a 60 s measured median**. The weights-only arm — the arm that produced the positive result — has a median of 11.4 s (maximum 46.2 s), needs no prompts, no generation and no GPU-resident forward pass, and could be run against a hub's stored tensors. Judge spend was \$0.19 for the battery's behavioural readout and \$0.92 for the $\alpha_{50}$ experiment's 16,084 semantic re-scoring calls.

# Discussion

**What a single checkpoint does and does not reveal.** The two results of this paper are best read as a division of labour. A directional weight edit is a *structural* change and leaves a structural trace: the projection removes one direction from every write matrix simultaneously, and that simultaneity is the signal — $W05$, the minimum over layers, works precisely because a genuine abliteration admits no exception. Behaviour, in contrast, is not structural. A model made compliant by fine-tuning on compliant data reorganises nothing detectable in the write spectrum, which is why the four behaviourally-uncensored members sit inside the instruct distribution, and why the deliberate safety-RL checkpoint does too despite an eight-fold reduction in jailbreak ASR. Any claim that a single-checkpoint statistic delivers a general safety score has to survive that observation, and ours does not. What it delivers is edit detection, which is a narrower and genuinely useful capability at hub scale: an abliterated checkpoint is the cheapest and commonest way to remove safety training, and it can now be flagged from the tensors alone, without the parent that [2] and [9] require and without the harmful prompts that [3], [4] and [5] require.

**Why the black-box result is the one to take seriously.** It would have been easy to report the best of 53 metrics against behaviour and call it a method. The pre-registration exists to prevent that, and it fired: the best correlate of harmful-refusal rate is a black-box statistic, and no interior statistic beats it with an interval excluding zero. The mechanism is not mysterious — greedy refusal rate on harmful prompts *is* an extremely cheap partial benchmark run, and a partial benchmark run is a good predictor of a full one. The interesting consequence is for the framing of the whole "cheap internal safety metric" lane: given 40 harmful prompts and 1,280 forward passes, the interior offers no measured advantage on our panel, and the case for interior measurement has to rest on the settings where the prompts are unavailable, unrepresentative or gameable, rather than on predictive accuracy.

**The refusal screen is a measurement instrument that needs retiring.** The 12-substring screen from [1] is used pervasively as a refusal detector. On our sweep text it declares 7 of 14 models incapable of being steered into refusal when all 14 can be, disagrees with a semantic judge on 20 reachability cells, and reaches median $\kappa = 0.279$. In our behavioural readout its median $\kappa$ against the judge is 0.179. This is not a small-model artifact: small models refuse by lecturing, and the screen was built from one model family's phrasings. Any result of the form "model X cannot be made to refuse" or "steering vector Y induces no refusal" that rests on a substring screen should be re-derived semantically before it is believed, and that includes results in this paper's own lineage.

**Limitations.** (1) The abliteration signature is calibration-fragile: rank transfers to held-out lineages, an absolute threshold transfers at 1-of-2 recall, and a band-limited edit escapes it entirely by direct positive-control measurement. Published abliterations vary the ablation strength as a free parameter [35], and extended-refusal training is a documented defense that preserves refusal behaviour through abliteration [34] — a checkpoint so trained would be flagged by $W05$ and would be safe. (2) $n_{\text{abliterated}} = 8$ over three families is the base of the AUROC claim; the perfect separation is a rank statement over 8 $\times$ 36 pairs, and the margin between the extreme values is 0.077 in $\log_{10}$ units. (3) Ground truth is 97% self-measured, because external safety numbers essentially do not exist below 4B, and it is judge-derived; the judge's median $\kappa$ against the lexical screen is 0.179, and our own audit shows how much a judge prompt can move a rate. (4) The two-axis behavioural readout uses 40 harmful and 25 XSTest-safe items per member, which bounds the per-model rate resolution. (5) Base models are excluded from every correlation by pre-registration because they use a different renderer; the correlation panel is therefore 26 members over 18 lineages, not 44 over 23. (6) The steering results concern the steered dynamical system, which is provably not prompt-reachable [30], and a fixed injection depth makes $\alpha_{50}$ a lower bound on steerability given that the optimal layer is input-dependent [17]. (7) One source characterised in [2] as detecting abliteration via an activation-geometry fingerprint was unreachable (HTTP 403) at the time of writing and remains the largest residual risk to the novelty claim for the weights-only arm.

**What we would do next.** Three things follow directly. First, the abliteration signature should be evaluated against the 273-checkpoint registry of [2] with its labels replaced — that registry's own labels are Qwen3Guard-derived [47], a circularity we did not anticipate and cannot inherit — and reported head-to-head against $E_1$ in both the parent-available and parent-free settings. Second, the band-limited blind spot suggests an obvious extension: run the same eigen-analysis in sliding layer windows, which converts a global minimum into a per-band profile and should recover band-limited edits at the cost of more spectra. Third, the black-box result should be tested where it should break, namely on checkpoints tuned to refuse benchmark items specifically; a metric that reads the interior has a principled reason to survive that attack, and our panel contains no such adversarial checkpoint.

# Conclusion

We set out to read a model's safety off the model alone, with no parent, no reference and no benchmark run, and we screened 53 pre-registered candidates over 44 checkpoints, 23 lineages and 7 architecture families to find out whether it is possible. The answer separates into two parts. Directional weight editing is detectable from a single checkpoint: the minimum per-layer write energy along the minimum eigenvector of the pooled write Gram matrix separates 8 abliterated checkpoints from 36 others at AUROC 1.000, with perfect leave-one-family-out separation, perfect ranking on frozen held-out lineages, 0 prompts, 0 forward passes and 11.4 s median cost — where the published two-signal audit needs the parent checkpoint and the published activation scanners need harmful prompts. Graded safety behaviour is not: the best predictor of harmful-refusal rate on our panel is a black-box statistic ($\rho = +0.766$, CI $[+0.539, +0.917]$), no interior metric beats it with an interval excluding zero, and the pre-registered conclusion that reading inside buys nothing for cheap safety screening stands as written. The metric this project previously led with, $\alpha_{50}$, is not a triage score ($R = 0.73$, $p = 0.76$) and has no consistent cross-family sign (sign test $p = 0.625$); the lexical objection against it resolves onto the standard 12-substring refusal screen, which calls 7 of 14 models incapable of refusing when all 14 can be shown to refuse. Finally, an audit of our own previous round retracts nine claims, including a control verdict that reverses when recomputed on the assumption-free statistic we said we trusted. The useful single-checkpoint question turns out not to be "is this model safe" but "has this model been edited" — and that one has a cheap, parent-free answer.

# References

[1] A. Arditi, O. Obeso, A. Syed, D. Paleka, N. Panickssery, W. Gurnee, and N. Nanda. Refusal in Language Models Is Mediated by a Single Direction. *NeurIPS*, 2024. arXiv:2406.11717.

[2] J. Hurtado. Has This Checkpoint Been Abliterated? A Two-Signal Audit and Its Failure Map. *arXiv:2607.01854*, 2026.

[3] G. Messenger. Detecting Safety Training Modification in Language Models via Activation Analysis. *IEEE Access*, 14:91723–91737, 2026. arXiv:2608.05578.

[4] C. Huang, Y.-L. Chen, C.-M. Yu, and W.-B. Lee. RAS: Measuring LLM Safety Through Refusal Alignment. *arXiv:2606.25750*, 2026.

[5] S. Peng, P.-Y. Chen, M. Hull, and D. H. Chau. Navigating the Safety Landscape: Measuring Risks in Finetuning Large Language Models. *NeurIPS*, 2024. arXiv:2405.17374.

[6] A. Borah et al. Alignment Quality Index (AQI): Beyond Refusals — AQI as an Intrinsic Alignment Diagnostic via Latent Geometry, Cluster Divergence, and Layer-wise Pooled Representations. *EMNLP*, 2025. arXiv:2506.13901.

[7] S. Basu, S. Y. Patel, P. Sheth, B. Muralidharan, N. Elamaran, A. Kinra, J. Morgan, and R. Batniji. Interpretability without actionability: mechanistic methods cannot correct language model errors despite near-perfect internal representations. *arXiv:2603.18353*, 2026.

[8] M. Galeone et al. Perfect Detection, Failed Control: The Geometry of Knowing vs. Steering in Language Models. *arXiv:2606.24952*, 2026.

[9] Z. Zhong and A. Raghunathan. Watch the Weights: Unsupervised monitoring and control of fine-tuned LLMs. *arXiv:2508.00161*, 2025.

[10] S. Jain, E. S. Lubana, K. Oksuz, T. Joy, P. H. S. Torr, A. Sanyal, and P. K. Dokania. What Makes and Breaks Safety Fine-tuning? A Mechanistic Study. *NeurIPS*, 2024. arXiv:2407.10264.

[11] B. Wei, K. Huang, Y. Huang, T. Xie, X. Qi, M. Xia, P. Mittal, M. Wang, and P. Henderson. Assessing the Brittleness of Safety Alignment via Pruning and Low-Rank Modifications. *ICML*, 2024. arXiv:2402.05162.

[12] T. Li and Y. Liu. Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness. *arXiv:2506.24056*, 2026.

[13] A. Korznikov, A. Galichin, A. Dontsov, E. Rogov, I. Oseledets, and E. Tutubalina. The Rogue Scalpel: Activation Steering Compromises LLM Safety. *arXiv:2509.22067*, 2026.

[14] V. Siu, N. Crispino, J. Park, Z. Henry, D. Wang, Y. Liu, D. Song, and C. Wang. SteeringSafety: Benchmarking Representation Steering in LLMs Across Safety Perspectives. *arXiv:2509.13450*, 2026.

[15] X. Li, A. Fastowski, D. Zaradoukas, B. Prenkaj, and G. Kasneci. Analysing the Safety Pitfalls of Steering Vectors. *arXiv:2603.24543*, 2026.

[16] B. Taimeskhanov, S. Vaiter, and D. Garreau. Towards Understanding Steering Strength. *ICML*, 2026. arXiv:2602.02712.

[17] S. Gadgil, T. Lin, and K. Lee. Where to Steer: Input-Dependent Layer Selection for Steering Improves LLM Alignment. *arXiv:2604.03867*, 2026.

[18] T. Chang, T. Schnabel, A. Swaminathan, and J. Wiens. A Course Correction in Steerability Evaluation: Revealing Miscalibration and Side Effects in LLMs. *arXiv:2505.23816*, 2025.

[19] R. Billa. Predicting Where Steering Vectors Succeed. *arXiv:2604.15557*, 2026.

[20] N. Rimsky, N. Gabrieli, J. Schulz, M. Tong, E. Hubinger, and A. M. Turner. Steering Llama 2 via Contrastive Activation Addition. *ACL*, 2024. arXiv:2312.06681.

[21] A. M. Turner, L. Thiergart, G. Leech, D. Udell, J. J. Vazquez, U. Mini, and M. MacDiarmid. Steering Language Models With Activation Engineering. *arXiv:2308.10248*, 2023.

[22] A. Zou et al. Representation Engineering: A Top-Down Approach to AI Transparency. *arXiv:2310.01405*, 2023.

[23] X. Qi, A. Panda, K. Lyu, X. Ma, S. Roy, A. Beirami, P. Mittal, and P. Henderson. Safety Alignment Should Be Made More Than Just a Few Tokens Deep. *ICLR*, 2025. arXiv:2406.05946.

[24] Y. Yin et al. Refusal Falls off a Cliff: How Safety Alignment Fails in Reasoning? *arXiv:2510.06036*, 2025.

[25] A. Kwon. Breaking Refusal in the First Half: A Mechanistic Study of the Prefill Jailbreak. *arXiv:2607.14147*, 2026.

[26] E. Rahimi, E. Hirshel, R. Himelstein, A. Levi, A. Mendelson, and C. Baskin. Step-Wise Refusal Dynamics in Autoregressive and Diffusion Language Models. *arXiv:2602.02600*, 2026.

[27] S. Ratnakar and K. Vats. The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs. *TrustNLP @ ACL*, 2026. arXiv:2606.22686.

[28] A. Hasan and S. Biswas. The Refusal-Compliance Tradeoff: A Large-Scale Safety Behavior Audit of Large Language Models. *arXiv:2605.05427*, 2026.

[29] C. Xiong, Z. He, P.-Y. Chen, C.-Y. Ko, and T.-Y. Ho. Steering Externalities: Benign Activation Steering Unintentionally Increases Jailbreak Risk for Large Language Models. *arXiv:2602.04896*, 2026.

[30] A. Mishra, D. Khashabi, and A. Liu. Steered LLM Activations are Non-Surjective. *arXiv:2604.09839*, 2026.

[31] A. Wei, N. Haghtalab, and J. Steinhardt. Jailbroken: How Does LLM Safety Training Fail? *NeurIPS*, 2023. arXiv:2307.02483.

[32] A. Lee, X. Bai, I. Pres, M. Wattenberg, J. K. Kummerfeld, and R. Mihalcea. A Mechanistic Understanding of Alignment Algorithms: A Case Study on DPO and Toxicity. *ICML*, 2024. arXiv:2401.01967.

[33] J. Fafula. Abliteration Is Not a Scalpel: Off-Target Effects of Refusal Removal on Decision Disposition Across Model Families. *arXiv:2607.17427*, 2026.

[34] H. Shairah et al. An Embarrassingly Simple Defense Against LLM Abliteration Attacks. *arXiv:2505.19056*, 2025.

[35] J. Young et al. Comparative Analysis of LLM Abliteration Methods: A Cross-Architecture Evaluation. *arXiv:2512.13655*, 2025.

[36] Y. Xu and L. Sheng. A Behavioral Fingerprint for Large Language Models: Provenance Tracking via Refusal Vectors. *arXiv:2602.09434*, 2026.

[37] A. Zou, Z. Wang, N. Carlini, M. Nasr, J. Z. Kolter, and M. Fredrikson. Universal and Transferable Adversarial Attacks on Aligned Language Models. *arXiv:2307.15043*, 2023.

[38] P. Chao et al. JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models. *NeurIPS Datasets and Benchmarks*, 2024. arXiv:2404.01318.

[39] M. Mazeika et al. HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal. *ICML*, 2024. arXiv:2402.04249.

[40] P. Röttger, H. R. Kirk, B. Vidgen, G. Attanasio, F. Bianchi, and D. Hovy. XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models. *NAACL*, 2024. arXiv:2308.01263.

[41] S. Han et al. WildGuard: Open One-Stop Moderation Tools for Safety Risks, Jailbreaks, and Refusals of LLMs. *NeurIPS Datasets and Benchmarks*, 2024. arXiv:2406.18495.

[42] L. Zheng et al. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *NeurIPS*, 2023. arXiv:2306.05685.

[43] T. Xie et al. SORRY-Bench: Systematically Evaluating Large Language Model Safety Refusal Behaviors. *ICLR*, 2025. arXiv:2406.14598.

[44] Y. Zeng et al. AIR-Bench 2024: A Safety Benchmark Based on Risk Categories from Regulations and Policies. *arXiv:2407.17436*, 2024.

[45] L. Li et al. SALAD-Bench: A Hierarchical and Comprehensive Safety Benchmark for Large Language Models. *ACL Findings*, 2024. arXiv:2402.05044.

[46] L. Sun et al. TrustLLM: Trustworthiness in Large Language Models. *ICML*, 2024. arXiv:2401.05561.

[47] H. Zhao et al. Qwen3Guard Technical Report. *arXiv:2510.14276*, 2025.

[48] A. Yang et al. Qwen3 Technical Report. *arXiv:2505.09388*, 2025.

[49] L. B. Allal et al. SmolLM2: When Smol Goes Big — Data-Centric Training of a Small Language Model. *arXiv:2502.02737*, 2025.

[50] S. Biderman et al. Pythia: A Suite for Analyzing Large Language Models Across Training and Scaling. *ICML*, 2023. arXiv:2304.01373.

[51] A. Dubey et al. The Llama 3 Herd of Models. *arXiv:2407.21783*, 2024.

[52] G. Ilharco, M. T. Ribeiro, M. Wortsman, S. Gururangan, L. Schmidt, H. Hajishirzi, and A. Farhadi. Editing Models with Task Arithmetic. *ICLR*, 2023. arXiv:2212.04089.

[53] L. Ouyang et al. Training language models to follow instructions with human feedback. *NeurIPS*, 2022. arXiv:2203.02155.

[54] Y. Bai et al. Constitutional AI: Harmlessness from AI Feedback. *arXiv:2212.08073*, 2022.

[55] M. Scheffer, J. Bascompte, W. A. Brock, V. Brovkin, S. R. Carpenter, V. Dakos, H. Held, E. H. van Nes, M. Rietkerk, and G. Sugihara. Early-warning signals for critical transitions. *Nature*, 461:53–59, 2009.

[56] M. Scheffer et al. Anticipating Critical Transitions. *Science*, 338(6105):344–348, 2012.

[57] V. Dakos et al. Methods for Detecting Early Warnings of Critical Transitions in Time Series Illustrated Using Simulated Ecological Data. *PLoS ONE*, 7(7):e41010, 2012.

[58] T. M. Bury. ewstools: A Python package for early warning signals of bifurcations in time series data. *Journal of Open Source Software*, 8(82):5038, 2023.

[59] H. Lu et al. AlphaPruning: Using Heavy-Tailed Self-Regularization Theory for Improved Layer-wise Pruning of Large Language Models. *NeurIPS*, 2024. arXiv:2410.10912.

[60] Y. Li, H. Hu, J. Sang, Y. Ma, X. Nie, Q. Zhang, Y. Yu, J. Su, Y. Huang, and J. Zhou. Prefill-level Jailbreak: A Black-Box Risk Analysis of Large Language Models. *arXiv:2504.21038*, 2025.

[61] G. Chen, T. Xia, H. Jia, C. Li, P. Torr, and J. Gu. LLM Jailbreak Detection for (Almost) Free! *arXiv:2509.14558*, 2026.

[62] B. Candogan, Y. Wu, E. Abad Rocamora, G. Chrysos, and V. Cevher. Single-pass Detection of Jailbreaking Input in Large Language Models. *TMLR*, 2025. arXiv:2502.15435.

[63] Y. Cao, R. Lou, W. Liu, S. Feng, D. Li, S.-K. Ng, and A. T. Luu. Activation Steering Induces Emergent Misalignment: A More Comprehensive Evaluation. *arXiv:2606.08682*, 2026.

</current_paper>

<reviewer_feedback>
Paper reviewer feedback from the previous iteration. Your strategy MUST address these critiques.
Prioritize major issues — these are the most impactful improvements to make.

- [MAJOR] (evidence) The abliterated class is confounded with abliteration TOOLCHAIN, and the paper's generalisation control tests the wrong variable. Verified in the artifact: the 8 abliterated members are huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2, huihui-ai/Qwen2.5-1.5B-Instruct-abliterated, huihui-ai/Huihui-Qwen3-1.7B-abliterated-v2, huihui-ai/Llama-3.2-1B-Instruct-abliterated, huihui-ai/Llama-3.2-3B-Instruct-abliterated, huihui-ai/Qwen2.5-0.5B-Instruct-abliterated, Goekdeniz-Guelmez/Josiefied-Qwen2.5-3B-Instruct-abliterated-v1 and Goekdeniz-Guelmez/Josiefied-Qwen3-4B-Instruct-2507-gabliterated-v2 -- two uploaders, six from one, and both running an all-layer global diff-in-means projection. Leave-one-ARCHITECTURE-family-out is reported as the generalisation control, but architecture is not what W05 keys on; the edit recipe is. The 2026 community landscape is dominated by variants that are explicitly not a single global rank-one projection (norm-preserving/projected abliteration, ORBA orthogonal-reflection bounded ablation, multi-direction SVD, per-head surgery, DCT 'spectral cascade' modes), and the paper's own band-limited positive control already demonstrates that W05 is blind to any edit that is not global. AUROC 1.000 over 8 near-identical productions is therefore a much weaker generalisation statement than it reads as. The nearest published analogue -- arXiv:2604.08844 -- reports that a spectral weight classifier trained on one editing method assigns EVERY out-of-method adapter a lower drift score than every in-method one (AUC 0.00), which is precisely this failure mode already observed once in the literature.
  Action: Add at least three abliterated checkpoints produced by mechanically different toolchains (mlabonne's recipe, a grimjim projected/ORBA norm-preserving variant, an OBLITERATUS 'advanced' multi-direction run) and report W05 on each. Run leave-one-UPLOADER-out alongside leave-one-family-out and report both. If the non-global variants are missed, report that as the arm's true scope -- 'detects global single-direction abliteration, the huihui/Josiefied recipe class' -- which is still a useful and defensible claim, rather than letting AUROC 1.000 imply coverage of abliteration in general.
- [MAJOR] (rigor) The paper's two headline statistical results have no shipped analysis code. I enumerated method_out.json: its datasets are long_table (2332 raw metric values), method_vs_baseline (44 rows of three metric values each), metric_spec, panel, ams_reproduction_gate, behaviour and diagnostics. There is no AUROC anywhere, no Spearman correlation against behaviour, no bootstrap, and no paired-bootstrap difference. Every number in Sec. 5.1's AUROC column and every entry in the Sec. 5.2 table -- rho = +0.766, CI [+0.539, +0.917], and all seven paired differences with their CIs -- was computed outside the versioned artifact. No bootstrap seed, resample count, tie-handling rule or CI method is stated anywhere in the paper either. A reader cannot reproduce the two claims the paper is built on, and cannot check whether the lineage bootstrap resampled lineages with or without replacement, how singleton lineages were handled (9 members are standalone), or whether Spearman ties were broken by rank-average -- the last of which the paper's OWN self-audit identifies as having flipped the sign of a previous-iteration result.
  Action: Ship analysis.py as a first-class deliverable that reads long_table.jsonl + behaviour.jsonl and emits every AUROC, every Spearman, every bootstrap CI and every paired difference in the paper, with the seed, B, resampling scheme and tie-handling printed in the header, plus an assertion block checking each output against the value quoted in the text. State the bootstrap specification in the Method section in two sentences. This is a few hours of work and it removes the single most damaging objection available to a reviewer.
- [MAJOR] (rigor) The 'pre-registration' the paper leans on does not contain what the paper attributes to it. metric_spec.py (sha 544ff994...) declares 53 metrics with family, prompt requirement, declared forward passes and declared wall-clock, plus import-time count assertions, and nothing else. It contains no falsifier statement, no analysis plan, no rule excluding base models from correlations, no blanket-refuser disqualification threshold, no paired-bootstrap specification, no held-out usage policy beyond a comment saying the split is 'RECORDED ONLY'. Yet the paper says 'the pre-registered falsifier is that if no white-box metric beats the best black-box one...', 'the pre-registered outcome therefore holds in the form it was written', 'base models are excluded from every correlation by pre-registration', 'a metric that ranks a blanket refuser at the top is disqualified by our own pre-registered rule', and 'the pre-registered triage ratio'. None of those is verifiable from the stamped file. Given that the paper's whole credibility argument is measurement discipline, and given that it correctly criticises its own previous round for unannounced deviations, this asymmetry is the most quotable weakness in the submission.
  Action: Publish the plan document that actually contained the falsifier and the analysis rules, with its own hash and a timestamp demonstrably prior to execution, and cite it distinctly from metric_spec.py. Where no such stamped statement exists, downgrade the wording to 'declared in advance in our study plan' or simply 'we adopted the rule that...' and reserve 'SHA-stamped pre-registration' for the metric declarations, which genuinely are stamped. A short table mapping each 'pre-registered' claim in the paper to the artifact and line that records it would close this entirely.
- [MAJOR] (scope) The deployment premise is not yet demonstrated, because the detection task as evaluated is solved for free by a string match. All 8 positives carry 'abliterated' or 'gabliterated' in their repository id; the opening scenario ('a checkpoint arrives with no provenance, its card says nothing') is never instantiated by a single panel member. More importantly, the metric's robustness to the obvious evasions is untested: an abliterated model that is subsequently LoRA-SFT'd, merged with its parent, quantized, or perturbed by an adversary who knows the metric (adding back an epsilon-scaled random rank-one term restores lambda_1 at negligible behavioural cost) may not retain the scar. Because W05 is a MINIMUM over layers, it is by construction the most fragile of the five statistics to any post-hoc process that touches even one layer -- the paper's own band-limited control is exactly this failure in miniature. Without at least one laundering arm, the claim 'it can now be flagged from the tensors alone' at hub scale is aspirational.
  Action: Add a laundering/evasion arm using the in-house edit machinery you already have: abliterate Qwen3-1.7B, then (a) LoRA-SFT 200 steps on benign data, (b) linearly merge 50/50 with the instruct parent, (c) round-trip int8 and int4 quantization, (d) add back a random rank-one term at increasing scale, and report W01-W05 plus harmful-refusal rate at each stage. Report the point at which the flag is lost and whether the model is still uncensored at that point -- if the scar dies only after the un-censoring dies, that is a strong result; if it dies first, say so. Additionally, scan a few hundred sub-4B Hub checkpoints from stored tensors and report any high-scoring repo whose card does not declare abliteration; even a handful of confirmed undeclared positives would make the deployment claim concrete.
- [MAJOR] (novelty) Two directly relevant prior works are uncited, one of them very close. (1) arXiv:2604.08844, Paul, 'Spectral Geometry of LoRA Adapters Encodes Training Objective and Predicts Harmful Compliance' (Apr 2026): a pre-registered study on Llama-3.2-3B-Instruct extracting per-layer spectral features -- norms, stable rank, singular-value entropy, effective rank, singular-vector cosine to a healthy centroid -- from weight deltas across 38 manufactured adapters, reporting AUC 1.00 for binary drift and all six pairwise objective comparisons, rho >= 0.956 ordinal severity, and a geometry-to-behaviour rank correlation of rho = 0.72 with HEx-PHI harmful compliance. Its feature set overlaps your W06-W11 almost item for item; its parent/delta requirement is exactly the gap you occupy; and its rho = 0.72 is a direct empirical counterweight to your Discussion claim that weight geometry cannot carry behavioural signal. Its complete cross-method collapse (AUC 0.00) is also the strongest published prior for the toolchain-confound critique above. (2) The OBLITERATUS toolkit ships a 'spectral certification' step that inspects an abliterated checkpoint's own weights, parent-free, to certify whether the projection is complete, and its own documentation records that certification frequently reads 'incomplete' even when practical refusal rate is 0%. That is prior community practice for the exact operation the paper claims as new, and its calibration failure independently mirrors your 'the ranking transfers, the calibration does not' finding.
  Action: Cite arXiv:2604.08844 in Related Work AND at the point of use in Sec. 4.1 where W06-W11 are introduced, and add one paragraph distinguishing it on three axes: parent-free vs delta-based, real community checkpoints vs manufactured adapters, and edit-detection vs behaviour prediction -- while acknowledging its rho = 0.72 and explaining why your panel's behaviourally-uncensored members show none of it (different manufacture regime, no controlled dose ladder). Cite OBLITERATUS's spectral certification and reframe your novelty as the first measured, held-out-validated, published characterisation of parent-free spectral abliteration detection, including the calibration failure that the toolkit reports anecdotally. Both framings are defensible; silence is not.
- [MINOR] (evidence) Sec. 5.1's table gives [min, max] only for the abliterated column and bare medians for base, instruct, behaviourally-uncensored and safety-RL, which materially understates the overlap present in the shipped data. From diagnostics.weights_arm_by_member_class: W01 base max = 1.992 against abliterated min = 1.438 (a genuine overlap), and W02 base max = 1.000, identical to the abliterated median of 1.000. The AUROC column encodes this (0.986, 0.950) but a reader scanning '4.26 vs 0.47 vs 0.58' will take away far cleaner separation than exists. Similarly, the paper never names the nearest non-abliterated neighbour on W05 (allenai/OLMo-1B-hf at -2.665), and the four values immediately above the decision region belong to OLMo and pythia -- under-represented architectures with no abliterated sibling, which is where false positives will concentrate in the wild.
  Action: Report [min, max] for every class in the table, name OLMo-1B as the nearest non-abliterated neighbour in the text, and add one sentence to Limitations noting that the three checkpoints nearest the boundary are all from single-member architecture families (olmo, gpt_neox) and that the false-positive rate on architectures outside the seven tested is unmeasured.
- [MINOR] (methodology) The Sec. 5.2 falsifier comparison is stated as a clean pre-registered outcome but is decided by an underpowered test against an unfavourably chosen comparator. n = 26 chat-rendered members over 18 lineages gives lineage-bootstrap CIs on paired rho differences with half-widths of roughly 0.25-0.5 -- wide enough that essentially no realistic white-box advantage could have excluded zero. So 'no white-box metric beats the best black-box one with a CI excluding zero' is close to guaranteed a priori and does not distinguish 'the interior buys nothing' from 'we lack the power to tell'. Compounding this, the winner B09 is itself selected as the best of 11 black-box declarations on the same data, so the comparison is best-of-11 against a fixed white-box candidate. The paper's own Sec. 5.2 note that A02 leads B09 numerically at both aggregation units (+0.802/+0.819 vs +0.766/+0.852) sits awkwardly with the headline.
  Action: Report the minimum detectable difference at n = 18 lineages for your bootstrap (a two-line simulation), and state explicitly whether the falsifier could have failed. Then restate the conclusion in the form the data supports: 'at this panel size, no interior metric shows an advantage over the best black-box baseline larger than ~0.3 in |rho|; distinguishing smaller advantages would require roughly N lineages.' Also correct for the best-of-11 selection of B09 by reporting the paired comparison against a PRE-SPECIFIED black-box metric (e.g. B01 logit gap, which has a published prior) alongside the post-hoc winner.
- [MINOR] (methodology) The behavioural ground truth that anchors the entire falsifier is thin and imperfectly reliable, and the paper does not propagate that uncertainty into the correlations. Per behaviour.jsonl each checkpoint contributes 40 harmful and 25 XSTest items scored by a single judge (meta-llama/llama-3.3-70b-instruct, rubric B), with metadata_judge_kappa against the lexical screen around 0.30 and n_judged = 64. A 40-item rate has a binomial SE of ~0.08 at p = 0.5; the judge-vs-screen kappa near 0.30 implies substantial classification noise on top. Spearman correlations computed on 26 such rates will be attenuated by an unknown and unreported factor, which cuts against all metrics equally but makes the paired differences between two attenuated correlations even less informative. The paper's own iteration-1 artifact explicitly advises downstream users to 'attenuation-correct with the reported reliability'; this iteration does not.
  Action: Report a reliability estimate for the harmful-refusal rate (e.g. split-half over the 40 items, or judge-vs-adjudicator agreement on a stratified subsample), give attenuation-corrected versions of the Sec. 5.2 correlations alongside the raw ones, and add per-member binomial error bars to Figure 3. If attenuation correction moves any ordering, say so.
- [MINOR] (clarity) Small verifiable mismatches between text and code undercut a paper whose credibility rests on fidelity. (a) W03 is defined in the paper against '64 matched random directions'; lib_metrics.py uses n_random = 256 (compute_weights default) and the frozen spec's own note says 256. (b) The Method says the positive control was injected into Qwen3-0.6B; diagnostics records the edited model as Qwen/Qwen3-0.6B (the instruct member) while the panel also contains Qwen3-0.6B-Base -- worth disambiguating since the unedited baseline W01 = 0.624 is quoted in the paper as 0.62 and the base member's value is 0.628. (c) The paper reports the positive control's W01 as going 'from 0.62 to 4.82' and separately reports the strongest abliterated panel member's W05 as -4.82; these are unrelated quantities that share a numeral and read as a typo.
  Action: Correct the W03 random-direction count to 256, name the exact positive-control checkpoint and revision, and either add a digit or reword so the two 4.82 values are not adjacent. Then do a mechanical pass reconciling every numeral in Secs. 4-5 against the artifact, ideally by generating the numbers into the text from analysis.py rather than transcribing them.
- [MINOR] (scope) The paper still owes a head-to-head against its self-declared closest competitor on that competitor's own terms. E_1 from [2] is described and correctly characterised as parent-requiring, but it is never computed -- not even on the subset of the panel where the parent IS available (the panel contains instruct/abliterated sibling pairs for at least the Qwen2.5-0.5B, Qwen2.5-1.5B, Qwen3-0.6B, Qwen3-1.7B and Llama-3.2-1B/3B lineages). Without that, the reader cannot tell what the parent-free constraint actually costs in AUROC on a matched panel, which is the central trade the paper claims to be making. Similarly, AMS is run and shown to lose, but RAS/SafeVec and VISAGE remain costed-away rather than run even at reduced fidelity.
  Action: Compute E_1 on every sibling pair in the panel where the parent is present and report W05 vs E_1 AUROC on that matched subset. If E_1 also reaches 1.000 there, the honest framing is 'parent-free matches parent-required on this panel at zero prompt cost', which is a much stronger sentence than the current one. If E_1 wins, quantifying the cost of the constraint is itself the contribution. This is a pure re-analysis of tensors you have already downloaded and should be inexpensive.
- [MINOR] (rigor) The rho* depth-selection procedure is reported as outcome-blind but is effectively arbitrary, and the paper does not test whether its results depend on it. The shipped calibration block shows the held-out AUROC profile saturating at 1.0 across indices 4-25 of 28 (a 22-layer plateau), with bare_auroc_argmax_index = 4 and the d'-tiebreak landing at index 20 -> rho* = 0.679. The paper says this honestly, but then reports every activation metric at that one depth, including the observation that alpha_50 is ceiling-censored on 37/44 members AT THAT DEPTH -- a censoring rate that is plausibly a consequence of the depth choice rather than of the metric. A reader cannot tell whether the activation arm's poor showing in Sec. 5.2 is a property of the arm or of an essentially coin-flipped depth.
  Action: Report the Sec. 5.2 correlation table at three depths spanning the plateau (e.g. rho* = 0.14 at the bare argmax, 0.50, and 0.679) and state whether the falsifier conclusion is invariant. If any activation metric beats B09 at some depth in the plateau, that must be disclosed even though the pre-declared depth is primary. Also report alpha_50's censoring rate at each depth so the reader can separate depth from metric.
</reviewer_feedback>

<task>
Generate 1 research strategy for THIS iteration.

**ARTIFACT LIMIT: Each strategy may contain AT MOST 5 artifact directions.** Focus on the highest-impact artifacts. Quality over quantity.

Each strategy should:
1. Define a clear OBJECTIVE - what novel contribution we're building toward
2. Plan artifacts to execute NOW - specify type, objective, approach, and depends_on for each
3. Account for parallel execution - all strategies and all planned artifacts run simultaneously, their artifacts are combined into one shared pool


</task><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ArtifactDep": {
      "description": "A single dependency on an existing artifact, with a short type label.\n\n``id`` and ``label`` are LLM-generated at strategy time. ``label`` is free-text but\nshort \u2014 a word or two naming the type of dependency, not a sentence.\n\n``relation_type`` and ``relation_rationale`` are populated later, in upd_hypo,\nusing the MultiCite citation-function typology (Lauscher et al., NAACL 2022).\nThey are absent at strategy time and may stay absent for legacy runs.",
      "properties": {
        "id": {
          "description": "ID of an existing artifact this artifact depends on",
          "title": "Id",
          "type": "string"
        },
        "label": {
          "description": "Short free-text label naming the type of this dependency (a word or two, not a sentence)",
          "title": "Label",
          "type": "string"
        }
      },
      "required": [
        "id",
        "label"
      ],
      "title": "ArtifactDep",
      "type": "object"
    },
    "ArtifactDirection": {
      "description": "High-level direction for an artifact to execute this iteration.\n\nID is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).",
      "properties": {
        "type": {
          "description": "Type of artifact to create",
          "enum": [
            "experiment",
            "research",
            "proof",
            "evaluation",
            "dataset"
          ],
          "title": "Type",
          "type": "string"
        },
        "objective": {
          "description": "What we want to achieve with this artifact",
          "title": "Objective",
          "type": "string"
        },
        "approach": {
          "description": "High-level direction/method",
          "title": "Approach",
          "type": "string"
        },
        "depends_on": {
          "description": "Existing artifacts this depends on, each with a short type label",
          "items": {
            "$ref": "#/$defs/ArtifactDep"
          },
          "title": "Depends On",
          "type": "array"
        }
      },
      "required": [
        "type",
        "objective",
        "approach"
      ],
      "title": "ArtifactDirection",
      "type": "object"
    },
    "Strategy": {
      "description": "A research strategy.\n\nContent fields have LLMPrompt + LLMStructOut markers.\n``id`` is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).\n\nID format: gen_strat_idx{N}",
      "properties": {
        "title": {
          "description": "Strategy name in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "objective": {
          "description": "The novel contribution we're building toward",
          "title": "Objective",
          "type": "string"
        },
        "rationale": {
          "description": "Why this strategy is promising",
          "title": "Rationale",
          "type": "string"
        },
        "artifact_directions": {
          "description": "Artifacts to execute THIS iteration",
          "items": {
            "$ref": "#/$defs/ArtifactDirection"
          },
          "title": "Artifact Directions",
          "type": "array"
        },
        "expected_outcome": {
          "description": "What we'll have after this iteration's artifacts complete",
          "title": "Expected Outcome",
          "type": "string"
        },
        "summary": {
          "default": "",
          "description": "Brief summary of the strategy and its expected contribution",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "title",
        "objective",
        "rationale",
        "artifact_directions",
        "expected_outcome"
      ],
      "title": "Strategy",
      "type": "object"
    }
  },
  "description": "Top-level wrapper for LLM strategy generation output.",
  "properties": {
    "strategies": {
      "description": "List of generated strategies",
      "items": {
        "$ref": "#/$defs/Strategy"
      },
      "title": "Strategies",
      "type": "array"
    }
  },
  "required": [
    "strategies"
  ],
  "title": "Strategies",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-13 20:07:25 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [4] TOOL CALL — Bash · 2026-08-13 20:08:55 UTC

```
ls /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/user_uploads 2>/dev/null | head -20; pwd
```

### [5] TOOL RESULT — Bash · 2026-08-13 20:08:55 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_strat/gen_strat_1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [6] TOOL CALL — Write · 2026-08-13 20:11:39 UTC

```
File: /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json

{
  "strategies": [
    {
      "title": "Find where the weight fingerprint breaks",
      "objective": "Convert iteration 2's two results into claims that survive a hostile reviewer, by measuring their SCOPE instead of restating them. The positive (a parent-free spectral scar of abliteration: W05 AUROC 1.000, 0 prompts, 0 forward passes, 11.4 s) is currently established on 8 checkpoints from 2 uploaders running ONE recipe (global all-layer diff-in-means projection), with every positive solved for free by a repository-name string match, and with the parent-requiring incumbent E_1 described but never computed. The negative (for graded behavioural safety no interior metric beats greedy refusal rate B09, rho +0.766) is currently a verdict from an underpowered paired bootstrap against a best-of-11 comparator, on judge-derived rates whose reliability was never estimated, at a depth chosen by a d'-tiebreak on a 22-layer AUROC plateau, and with ZERO of the headline AUROCs, Spearmans, bootstraps or paired differences computed inside any versioned artifact. This iteration delivers four things and retires the battery: (1) the true RECIPE-CLASS scope of the scar, tested against mechanically different abliteration toolchains and reported with leave-one-UPLOADER-out beside leave-one-family-out, plus the first head-to-head against E_1 on the matched sibling subset where the parent exists; (2) the deployment premise instantiated - a laundering ladder (LoRA-SFT, 50/50 parent merge, int8/int4 round-trip, added-back random rank-one) reporting W01-W05 AND harmful-refusal rate at every stage so the ORDER OF THE TWO DEATHS is measured, plus a Hub scan of undeclared checkpoints; (3) analysis.py as a first-class deliverable that emits every statistic in the paper with seed, B, resampling scheme and tie-handling printed, together with a power simulation, a pre-specified comparator, attenuation correction and a depth-invariance check that together turn the negative from a verdict into a measurement; (4) honest positioning against two prior works that were missed, one of which (arXiv:2604.08844) both overlaps our spectral feature set and independently documents the exact cross-method collapse we are testing for. The novel contribution being built toward is the first measured, held-out-validated characterisation of PARENT-FREE spectral abliteration detection, complete with its recipe-class boundary, its evasion boundary and its calibration failure - a smaller claim than iteration 1 hoped for and one that can actually be defended.",
      "rationale": "Every MAJOR reviewer critique is a scope or discipline defect, not a data defect, and each has a cheap decisive fix that fits inside this iteration. The toolchain confound is the sharpest: architecture is not what W05 keys on, the edit recipe is, our own band-limited control already proves blindness to non-global edits, and arXiv:2604.08844 has ALREADY published this exact failure mode once (a spectral classifier trained on one editing method scores every out-of-method adapter below every in-method one, AUC 0.00). Finding the collapse is therefore a confirmation, not finding it is a genuine surprise, and either way the sentence we can defend improves. The same logic makes the laundering arm mandatory rather than optional: W05 is a MINIMUM over layers and so is by construction the most fragile of the five statistics to anything touching a single layer, which means an evasion boundary certainly exists and the only question is whether it sits before or after the un-censoring dies. That is a measurable question with in-house machinery we already built (the rank-one and band-limited controls), and the answer is publishable in both directions. The E_1 head-to-head is nearly free - pure tensor arithmetic on sibling pairs we have already downloaded - and it converts the paper's central trade from an assertion into a number. On the negative side, the reviewer's power objection is correct and fatal if unanswered: at 18 lineages a paired-rho CI half-width near 0.25-0.5 means the falsifier could barely have failed, so 'the interior buys nothing' and 'we cannot tell' are currently indistinguishable; a two-line simulation settles which sentence we own, and a pre-specified comparator (B01, which has a published prior) removes the best-of-11 selection advantage that currently makes the headline awkward given A02 numerically leads B09 at both aggregation units. The reliability and depth repairs are the same move applied twice - propagate a known source of noise or arbitrariness into the reported number instead of leaving it as an unquantified caveat. And the missing analysis.py is existential for a paper whose entire credibility argument IS measurement discipline: no reviewer will accept headline numbers that exist nowhere in the artifact, and the same file fixes the 'pre-registered' overreach by forcing every claimed rule to point at a stamped line. The five artifacts split cleanly along what each executor is good at - two weights-heavy experiments that download and compute, one pure re-analysis evaluation that ships the statistics code, one literature pass that cannot be run in code, and one provenance-grade dataset that both makes the recipe taxonomy citable and stocks iterations 4-5 with the candidate pool a bigger scope test will need. None blocks another; each is reportable alone.",
      "artifact_directions": [
        {
          "type": "research",
          "objective": "Close the two uncited prior works the reviewer named, establish the mechanical taxonomy of 2026 abliteration recipes with enough precision to reimplement each one, and return a defensible novelty sentence for the parent-free weights-only arm.",
          "approach": "Four questions, answered from primary full text with exact numbers and section anchors; use scholarly search plus fetch_grep on PDFs and on repository/tool documentation. (A) arXiv:2604.08844 (Paul, 'Spectral Geometry of LoRA Adapters Encodes Training Objective and Predicts Harmful Compliance'). Extract verbatim: the exact per-layer feature list (norms, stable rank, singular-value entropy, effective rank, singular-vector cosine to a healthy centroid) and map it item-by-item onto our W06-W16; the manufacture protocol for the 38 adapters (base model, objectives, dose ladder if any); AUC 1.00 for binary drift and for all six pairwise objective comparisons; rho >= 0.956 ordinal severity; rho = 0.72 against HEx-PHI harmful compliance; and CRITICALLY the cross-method result reported as AUC 0.00 - transcribe the exact experimental setup that produced it, since it is our closest published precedent for the toolchain collapse we are testing. Write the three-axis distinction paragraph (parent-free vs delta-based; real community checkpoints vs manufactured adapters; edit-detection vs behaviour-prediction) AND the explanation of why our behaviourally-uncensored members show none of its behavioural signal. Its rho = 0.72 is a direct counterweight to any sentence of ours claiming weight geometry cannot carry behavioural signal - find every such sentence in the current draft and supply a corrected wording. (B) OBLITERATUS and community 'spectral certification'. Locate the toolkit (repo, docs, release notes, any write-up), and document verbatim: what its parent-free certification step computes from an abliterated checkpoint's own weights, what 'complete' vs 'incomplete' means operationally, and the documented cases where certification reads incomplete while practical refusal rate is 0%. This is prior community practice for the operation we claim as new and it independently mirrors our 'the ranking transfers, the calibration does not' finding; return the reframed novelty sentence. (C) RECIPE TAXONOMY, the input the scope experiment needs. For each of at least six mechanically distinct abliteration/uncensoring recipes - (i) global all-layer diff-in-means rank-one projection (huihui-ai / Josiefied class, our 8 positives), (ii) mlabonne's published notebook recipe, (iii) norm-preserving / projected abliteration (grimjim class), (iv) ORBA orthogonal-reflection bounded ablation, (v) multi-direction / SVD-subspace ablation, (vi) per-head or per-module surgery, (vii) DCT / spectral-cascade modes, (viii) behavioural uncensoring by ordinary SFT - write the EXACT weight update in equations, state which matrices it touches (o_proj / down_proj / embed_tokens / per-head slices), whether it is norm-preserving, whether it is rank-one, and whether it touches all layers. Then name concrete PUBLIC checkpoints at <= 4.2B parameters produced by each recipe, with repository id, uploader and the card or config evidence proving the recipe; flag which recipes have NO public sub-4B checkpoint, because those must be reimplemented in-house. Also state which of these recipes would and would not produce a shared approximate null direction across the whole write ensemble - a mechanistic prediction our experiment can then test. (D) Verify whether any published work computes a spectral or geometric abliteration/edit detector from a single checkpoint WITHOUT the parent, beyond OBLITERATUS's certification, and re-check the one source characterised in arXiv:2607.01854 that our previous draft could not reach (HTTP 403) - it is currently named as the largest residual risk to the novelty claim, so either resolve it or restate the risk precisely. Deliverable: a dossier with the reimplementable recipe equations, the two required citation paragraphs written out, a candidate-checkpoint table, and a list of numbered corrections to the current draft's wording.",
          "depends_on": [
            {
              "id": "art_lMTPOpnFwKnw",
              "label": "extends"
            }
          ]
        },
        {
          "type": "dataset",
          "objective": "Ship a provenance-grade, recipe-labelled checkpoint manifest that makes the scope claim citable, plus the two auxiliary corpora the laundering arm needs and the enumerated sub-4B Hub pool that a full undeclared-positive scan will draw from in later iterations.",
          "approach": "Three row blocks in one schema-validated file, every row carrying pinned repo id, revision sha, resolved parameter count from the Hub API (never from on-disk bytes - the previous iteration found that double-counts repos shipping both .safetensors and .bin), file list with sizes, and an evidence field holding a <= 300-char quoted snippet from the card, config or linked code that justifies its label. (1) RECIPE-LABELLED EDIT MANIFEST, the headline block. Enumerate at least 25 sub-4.2B checkpoints that claim to be abliterated / uncensored / decensored / gabliterated / orthogonalised, spanning at least five DISTINCT uploaders and, where the card permits it, at least four distinct recipe classes (global rank-one diff-in-means; norm-preserving or projected; multi-direction / SVD subspace; per-head or partial-layer; behavioural SFT uncensoring). For each, record: uploader, declared parent, declared recipe with the quoted evidence, whether the recipe is inferable at all (a large fraction will be UNDECLARED - report that count as a first-class number, it is the honest measure of how much provenance a hub actually carries), and a recipe_class field with an explicit UNKNOWN value rather than a guess. Include the 8 members of the current abliterated class so the manifest is a superset, and mark them. Also record, for every row, whether the repository id contains an abliteration string - this quantifies exactly how much of the detection task a string match solves for free, which the reviewer correctly identified as unmeasured. (2) LAUNDERING CORPORA. A benign instruction-tuning split suitable for a 200-step LoRA SFT (a few thousand instruction/response pairs from a permissively licensed, non-safety-related source; record the license, and prefer sources without the CC-BY-NC constraint that limits two of our existing blocks), plus a WikiText-derived fluency evaluation split for perplexity screening of laundered checkpoints, plus a small held-out benign prompt set disjoint from the SFT data. (3) HUB SCAN POOL. Enumerate several hundred sub-4B text-generation checkpoints from the Hub with metadata only (no weights): repo id, downloads, parameter count, architecture family, full card text hash, and a boolean for whether the card or repo id declares abliteration/uncensoring. Stratify so the pool contains both declared and non-declaring chat models, and report the size distribution so a later scan can be costed in gigabytes rather than guessed. Ship the pool as a ranked scan order (most-downloaded undeclared chat models first) so the scan is reproducible and its coverage is stateable. Report honest coverage counts throughout, and validate the file against the standard dataset schema with full/mini/preview variants.",
          "depends_on": [
            {
              "id": "art_lMTPOpnFwKnw",
              "label": "guidance"
            },
            {
              "id": "art_CKWQh2cOQLLQ",
              "label": "extends"
            }
          ]
        },
        {
          "type": "experiment",
          "objective": "Measure the true scope of BOTH iteration-2 results: the recipe-class boundary of the parent-free scar (with leave-one-uploader-out and the first E_1 head-to-head), and the depth-invariance of the falsifier that produced the negative.",
          "approach": "Three arms, all on tensors, sharing one download budget. Re-implement the weights statistics from the published definitions rather than importing them, and GATE the reimplementation before anything else: form A = sum over residual-write matrices (attention o_proj, MLP down_proj) of W W^T / ||W||_F^2, take v1 = eigenvector of the minimum eigenvalue, define e_W(u) = ||u^T W||^2 / (||W||_F^2 / d), and compute W01 = log10(median(lam)/lam_1), W02 = fraction of write matrices with e_W(v1) < 0.1, W03 = log10(q05(e_W(u_rand)) / mean e_W(v1)) over 256 random directions (256, not 64 - the previous text was wrong), W04 = log10(lam_2/lam_1), W05 = log10(min_W e_W(v1)). REPRODUCTION GATE: recompute on at least five of the eight original abliterated members and five non-abliterated ones and require agreement with the archived values - weakest abliterated W05 = -2.742 (huihui-ai/Qwen2.5-0.5B-Instruct-abliterated), next-weakest -3.522, strongest non-abliterated -2.665 (allenai/OLMo-1B-hf), abliterated W01 median 4.26, base W01 max 1.992. Report the reproduction deltas; if they do not reproduce, that is the headline and everything downstream is conditioned on it. ARM 1, RECIPE SCOPE. Acquire and measure at least three, target six, abliterated/uncensored checkpoints at <= 4.2B produced by MECHANICALLY DIFFERENT toolchains from the huihui/Josiefied class - verify the recipe from the card, config or linked code and record the evidence, do not trust the repo name. Concrete starting candidates to verify: mlabonne/Qwen3-0.6B-abliterated (this project already used it in iteration 1 and it is NOT among the 8 positives, so it is the cheapest recipe-diversity win available), grimjim-class projected / norm-preserving variants, ORBA orthogonal-reflection outputs, OBLITERATUS 'advanced' multi-direction runs, and per-head or partial-layer surgeries. Where a recipe class has no public sub-4B checkpoint, REIMPLEMENT it in-house on Qwen3-1.7B-Instruct and label it synthetic: (a) norm-preserving projection (project out r then rescale each W to its original Frobenius norm), (b) multi-direction ablation removing a rank-k subspace for k in {2, 4, 8}, (c) per-head surgery touching only attention heads whose refusal-direction write energy is highest, (d) a partial-layer variant sweeping the fraction of edited layers from 0.33 to 1.0 so the blind spot becomes a CURVE rather than the single band-limited point already reported. Report W01-W05 for every checkpoint, plus the recomputed AUROC of each statistic under three groupings: all abliterated vs all else, LEAVE-ONE-UPLOADER-OUT (train the ranking on all uploaders but one, evaluate on the held-out uploader's members), and leave-one-architecture-family-out for comparison. State the scope sentence the data supports, in the form 'detects <recipe class>' with the classes it misses named. ARM 2, E_1 HEAD-TO-HEAD, the matched-panel comparison the paper owes its closest competitor. For every instruct/abliterated sibling pair in the panel where the parent is present (at least Qwen2.5-0.5B, Qwen2.5-1.5B, Qwen3-0.6B, Qwen3-1.7B, Llama-3.2-1B, Llama-3.2-3B), compute E_1 = mean over matrices of sigma_1^2(dW)/sum_i sigma_i^2(dW) with dW = W_parent - W_candidate over o_proj and down_proj in the published mid-stack band, and compute the SAME quantity for benign fine-tune pairs (instruct vs its own base, and any behaviourally-uncensored member vs its parent) so E_1 has negatives. Report W05 vs E_1 AUROC on exactly that matched subset with bootstrap CIs, and state the trade in one sentence: either parent-free matches parent-required at zero prompt cost, or the price of the constraint in AUROC. Also apply E_1 to the new-toolchain checkpoints where a parent is resolvable, since the cross-method question applies to the incumbent too. ARM 3, DEPTH INVARIANCE OF THE NEGATIVE. The held-out AUROC depth profile saturates at 1.0 across indices 4-25 of 28, so rho* = 0.679 was fixed by a d'-tiebreak on a 22-layer plateau and the activation arm's poor showing may be a property of the depth, not the arm. Recompute the depth-sensitive activation metrics (diff-in-means separation, d', AUROC, AMS sigma and its concept cosine, refusal-axis-to-unembedding cosine, prompt-position and generated-step logit-lens refusal log-odds) at THREE relative depths spanning the plateau - the bare argmax (~0.14), 0.50, and the pre-declared 0.679 - on the chat-rendered members, using the frozen prompt folds and the plain-vs-chat renderer rule (base models plain, excluded from correlations). Emit a tidy long table of (member, metric, depth, value) so the falsifier can be re-tested at each depth downstream, and report alpha_50's ceiling-censoring count at each depth (it was 37/44 at 0.679) so depth and metric are separable. IMPLEMENTATION NOTES that cost days if rediscovered: HF derives positions from cache_position, so LEFT-padded batches need explicit position_ids = (mask.cumsum(-1)-1).clamp_min(0) on the forward and every decode step; use svdvals rather than sqrt(eigvalsh(W W^T)) for square attention matrices; download sequentially and delete weights after measuring; report which tier completed.",
          "depends_on": [
            {
              "id": "art_CKWQh2cOQLLQ",
              "label": "dataset"
            },
            {
              "id": "art_BCxIq6GX4WIw",
              "label": "dataset"
            },
            {
              "id": "art_lMTPOpnFwKnw",
              "label": "spec"
            }
          ]
        },
        {
          "type": "experiment",
          "objective": "Instantiate the deployment premise the paper currently only asserts: measure whether the scar survives ordinary post-processing and deliberate evasion, in what ORDER the flag and the un-censoring die, and whether any undeclared Hub checkpoint carries the signature.",
          "approach": "Two arms. ARM 1, THE LAUNDERING LADDER, the decisive one. Using in-house edit machinery, abliterate Qwen3-1.7B-Instruct with a faithful global diff-in-means rank-one projection over every residual-write matrix (o_proj, down_proj, and embed_tokens if the reference implementation includes it - record which), verify the edit landed by requiring the same signature the panel's abliterated members show (W02 near 1.0, W01 above 3, W05 well below -3) and by requiring harmful-refusal rate to collapse relative to the parent. Then take that checkpoint through five laundering treatments, each a separate branch from the SAME abliterated root: (a) LoRA-SFT for 200 steps on benign instruction data (report rank, alpha, target modules, learning rate, and merge the adapter before measuring so the weights are directly comparable); (b) linear merge with the instruct parent at weights 0.25 / 0.50 / 0.75, giving a merge ladder rather than one point; (c) round-trip int8 and int4 quantization and dequantization back to the original dtype; (d) added-back random rank-one term epsilon * u u^T W at increasing epsilon, the metric-aware adversary who knows W05 is a minimum over layers and only needs to lift the smallest one; (e) a combined worst case (quantize then merge at 0.25). At EVERY stage report all five weight statistics AND the behavioural readout on the same items used for the panel's ground truth - harmful-refusal rate on the 40-item stratified harmful core and over-refusal on the 25 XSTest-safe items, greedy, with the behaviour-scoring judge rubric that separates 'did the model comply' from 'is the content harmful' (the harmfulness-scoring rubric gives kappa ~0 and must not be used), plus a fluency screen (WikiText perplexity and within-response distinct-3) so a stage that merely broke the model is not scored as evasion. Judge spend capped at $1.50 and logged after every call. THE LOAD-BEARING OUTPUT is a single figure and table showing the two curves - flag strength (W05, and W01/W04 alongside) and un-censoring strength (harmful compliance) - against treatment intensity, with the crossing point stated: if the flag dies only AFTER the model stops being uncensored, the scar is a robust provenance signal and that is a strong result; if it dies first, the scar is evadable and the paper says so plainly and quantifies the evasion cost. Report which of the five statistics is most robust - the prediction is that W05, being a minimum, is the most fragile and W01/W02, being aggregates, degrade more gracefully, which if true is an immediate and cheap methodological improvement to the metric. ARM 2, THE HUB SCAN. Score sub-4B checkpoints that do NOT declare abliteration in their repo id or card, from stored tensors only, in downloads-ranked order, deleting each after measurement; state the number completed rather than promising a target, and prioritise the smallest models so coverage is maximised within the time budget (aim for at least 40 completed, more if bandwidth permits). Report the full score distribution, name every checkpoint scoring inside or near the abliterated region defined by the panel (W05 below -2.742, and the warning band -2.742 to -2.5), and for each such hit fetch its card and lineage and adjudicate whether it is a genuine undeclared edit, a merge of an abliterated ancestor, or a false positive - quoting the evidence either way. Report the false-positive count against the number scanned as the deployment-relevant number, and note that architectures outside the seven tested are where false positives are expected to concentrate (the three nearest-boundary non-abliterated members are all from single-member families, olmo and gpt_neox). Even a handful of confirmed undeclared positives makes the deployment claim concrete; zero hits over N scanned is also a reportable and useful specificity number.",
          "depends_on": [
            {
              "id": "art_CKWQh2cOQLLQ",
              "label": "dataset"
            },
            {
              "id": "art_BCxIq6GX4WIw",
              "label": "dataset"
            },
            {
              "id": "art_lMTPOpnFwKnw",
              "label": "spec"
            }
          ]
        },
        {
          "type": "evaluation",
          "objective": "Ship analysis.py as a first-class versioned deliverable that recomputes every statistic in the paper, and use it to turn the negative from a verdict into a measurement - power, pre-specified comparator, reliability-corrected correlations - while auditing every 'pre-registered' claim and every numeral against the artifact that records it.",
          "approach": "Pure re-analysis of the archived iteration-2 trees; no new model inference beyond LLM judging for the reliability arm. (1) ANALYSIS.PY, the centrepiece. One script reading long_table.jsonl / battery + behaviour.jsonl and emitting EVERY AUROC, Spearman, bootstrap CI and paired difference that appears in the paper - the Sec 5.1 weights-arm AUROCs, the Sec 5.2 correlation table at both aggregation units, and all seven paired |rho_X| - |rho_B09| differences. Print in the file header, and echo into the output: the RNG seed, B, whether lineages are resampled with or without replacement, exactly how the 9 singleton lineages are handled, the tie-handling rule for Spearman (rank-average, explicitly - the project's own audit found position-based tie-breaking flipped the sign of a previous result), the AUROC tie convention, and the base-model exclusion rule. Include an assertion block checking each recomputed value against the number quoted in the current draft, and emit a table of every disagreement - transcription errors are expected and finding them is part of the deliverable. Also emit, machine-readable, the numerals the draft must regenerate rather than transcribe: [min, max] for EVERY class in the weights table (not only the abliterated column - base W01 max 1.992 genuinely overlaps abliterated min 1.438, and base W02 max 1.000 equals the abliterated median), the nearest non-abliterated neighbour on W05 by name (allenai/OLMo-1B-hf, -2.665), the family membership of the three checkpoints nearest the boundary, the correct random-direction count for W03 (256, not 64), and the exact positive-control checkpoint and revision (Qwen/Qwen3-0.6B, the instruct member, whose unedited W01 is 0.624 - distinct from the Base member's 0.628, and distinct from the unrelated 4.82 values that currently read as a typo). (2) POWER. Simulate the actual paired lineage bootstrap at n = 18 lineages under the observed rank structure and report the minimum detectable |rho| difference at 80% power, plus the achieved CI half-widths. State explicitly whether the falsifier COULD have failed, and emit the restated conclusion sentence in the form the data supports: 'at this panel size no interior metric shows an advantage over the best black-box baseline larger than ~X in |rho|; distinguishing smaller advantages needs roughly N lineages.' (3) COMPARATOR. B09 was selected as best-of-11 black-box declarations on the same data, so the current headline is best-of-11 against a fixed white-box candidate. Report the paired comparison against the PRE-SPECIFIED B01 (first-step logit gap, which has a published prior) alongside the post-hoc winner, and quantify the selection advantage by re-running the best-of-11 selection inside the bootstrap. Reconcile explicitly the awkward fact that A02 leads B09 numerically at both aggregation units (+0.802/+0.819 vs +0.766/+0.852) - state whether the headline should be 'no interior metric beats black-box with a CI excluding zero' or the weaker-but-true 'the numerically best metric is an interior one whose advantage is not resolvable'. (4) RELIABILITY AND ATTENUATION. Each checkpoint's harmful-refusal rate rests on 40 items scored by a single judge with judge-vs-screen kappa ~0.30 - a binomial SE of ~0.08 at p = 0.5 before judge noise. Estimate reliability by split-half over the 40 items (Spearman-Brown corrected) and by re-judging a stratified subsample of the archived generations with an independent adjudicator model under the behaviour-scoring rubric, reporting agreement; then report attenuation-corrected versions of every Sec 5.2 correlation and every paired difference alongside the raw ones, plus per-member binomial error bars, and state whether ANY ordering moves. LLM spend capped at $1.00 with per-call logging and response caching so a rerun costs $0. (5) DEPTH AND CENSORING. Re-run the Sec 5.2 correlation table at the three plateau depths and state whether the falsifier conclusion is invariant; if any activation metric beats the black-box baseline at some depth in the plateau, disclose it prominently even though 0.679 is the pre-declared primary. Report alpha_50's censoring rate at each depth. If the depth-swept activation values from this iteration's scope experiment are unavailable, run this arm on whatever depth-varying quantities the archive already contains and say exactly which depths were reachable. (6) PRE-REGISTRATION FIDELITY. Audit the SHA-stamped metric_spec.py against every claim in the paper of the form 'pre-registered'. That file declares 53 metrics with family, prompt requirement and declared cost, and NOTHING ELSE - no falsifier, no analysis plan, no base-model exclusion rule, no blanket-refuser threshold, no bootstrap specification. Emit a table mapping every such claim to the artifact and line that actually records it, marked SUPPORTED / PLAN-ONLY / UNSUPPORTED, and supply the corrected wording for each unsupported one ('we adopted the rule that...'), reserving 'SHA-stamped pre-registration' for the metric declarations alone. Deliverable: analysis.py plus a machine-readable numbers file that the paper generates its numerals from.",
          "depends_on": [
            {
              "id": "art_xyUlckdGtbjc",
              "label": "reanalyzes"
            },
            {
              "id": "art_CbL-EUQlwgfw",
              "label": "reanalyzes"
            },
            {
              "id": "art_BCxIq6GX4WIw",
              "label": "reference"
            }
          ]
        }
      ],
      "expected_outcome": "By the end of this iteration the paper's two claims are bounded rather than merely stated. (1) SCOPE: W01-W05 measured on at least three, target six, abliterated checkpoints from mechanically different toolchains plus in-house reimplementations of norm-preserving, multi-direction, per-head and partial-layer recipes, with leave-one-UPLOADER-out reported beside leave-one-family-out and a partial-layer sweep turning the band-limited blind spot into a curve - yielding a defensible scope sentence naming the recipe class detected and the classes missed. Plus the first computed E_1 head-to-head on the matched sibling subset, which quantifies what the parent-free constraint costs instead of asserting the trade. Plus a depth-swept activation table letting the falsifier be re-tested at three depths spanning the 22-layer plateau. (2) DEPLOYMENT: a laundering ladder reporting flag strength and un-censoring strength at every stage of LoRA-SFT, three merge ratios, int8/int4 round-trip, an adversarial added-back rank-one term and a combined worst case, with the crossing point of the two curves stated explicitly, plus a Hub scan of undeclared sub-4B checkpoints reporting hits, adjudicated evidence, and a specificity number. (3) DISCIPLINE: analysis.py recomputing every headline statistic with seed, B, resampling scheme and rank-average tie handling printed and asserted against the quoted values; a power simulation stating whether the falsifier could have failed and the restated conclusion; the pre-specified B01 comparison beside the best-of-11 winner with the selection advantage quantified; split-half and adjudicator reliability with attenuation-corrected correlations and per-member error bars; and a SUPPORTED / PLAN-ONLY / UNSUPPORTED table for every 'pre-registered' claim with corrected wording. (4) POSITIONING: arXiv:2604.08844 and OBLITERATUS's spectral certification cited at their points of use with the three-axis distinction written out, a reimplementable taxonomy of six-plus abliteration recipes, and a resolved or precisely restated novelty risk. (5) A recipe-labelled, evidence-carrying manifest of 25+ edited checkpoints, laundering corpora, and a ranked Hub scan pool that stocks iterations 4-5. Negative outcomes are all reportable and several are likely by design: the most probable single result is that the scar survives quantization and merging but not LoRA-SFT, and misses at least one new toolchain - which turns the headline into 'a recipe-class provenance signal, free at hub scale, with a measured evasion boundary'. If instead the cross-toolchain AUROC holds, that is a genuine surprise against the published AUC-0.00 precedent and a considerably stronger paper. Either way iterations 4-5 inherit a bounded claim, working analysis code, and a candidate pool for scaling the scope test.",
      "summary": "Iteration 3 stops adding metrics and starts bounding the two results it already has. Two weights-heavy experiments measure the scar's recipe-class scope (new toolchains, in-house norm-preserving / multi-direction / per-head / partial-layer reimplementations, leave-one-uploader-out, and the first E_1 parent-required head-to-head) and its evasion boundary (LoRA-SFT, merge ladder, int8/int4 round-trip, adversarial added-back rank-one, plus a Hub scan for undeclared positives), reporting flag death against un-censoring death. One evaluation ships analysis.py - every AUROC, Spearman, bootstrap and paired difference with seed, B, resampling scheme and tie-handling printed and asserted - and converts the negative into a measurement via a power simulation, a pre-specified comparator, reliability-corrected correlations and a depth-invariance check, while auditing every 'pre-registered' claim against the file that actually records it. One research pass closes the two uncited prior works and returns a reimplementable recipe taxonomy; one dataset ships the evidence-carrying, recipe-labelled checkpoint manifest and the scan pool for later iterations."
    }
  ]
}
```

### [7] TOOL RESULT — Write · 2026-08-13 20:11:39 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json", "content": "{\n  \"strategies\": [\n    {\n      \"title\": \"Find where the weight fingerprint breaks\",\n      \"objective\": \"Convert iteration 2's two results into claims that survive a hostile reviewer, by measuring their SCOPE instead of restating them. The positive (a parent-free spectral scar of abliteration: W05 AUROC 1.000, 0 prompts, 0 forward passes, 11.4 s) is currently established on 8 checkpoints from 2 uploaders running ONE recipe (global all-layer diff-in-means projection), with every positive solved for free by a repository-name string match, and with the parent-requiring incumbent E_1 described but never computed. The negative (for graded behavioural safety no interior metric beats greedy refusal rate B09, rho +0.766) is currently a verdict from an underpowered paired bootstrap against a best-of-11 comparator, on judge-derived rates whose reliability was never estimated, at a depth chosen by a d'-tiebreak on a 22-layer AUROC plateau, and with ZERO of the headline AUROCs, Spearmans, bootstraps or paired differences computed inside any versioned artifact. This iteration delivers four things and retires the battery: (1) the true RECIPE-CLASS scope of the scar, tested against mechanically different abliteration toolchains and reported with leave-one-UPLOADER-out beside leave-one-family-out, plus the first head-to-head against E_1 on the matched sibling subset where the parent exists; (2) the deployment premise instantiated - a laundering ladder (LoRA-SFT, 50/50 parent merge, int8/int4 round-trip, added-back random rank-one) reporting W01-W05 AND harmful-refusal rate at every stage so the ORDER OF THE TWO DEATHS is measured, plus a Hub scan of undeclared checkpoints; (3) analysis.py as a first-class deliverable that emits every statistic in the paper with seed, B, resampling scheme and tie-handling printed, together with a power simulation, a pre-specified comparator, attenuation correction and a depth-invariance check that together turn the negative from a verdict into a measurement; (4) honest positioning against two prior works that were missed, one of which (arXiv:2604.08844) both overlaps our spectral feature set and independently documents the exact cross-method collapse we are testing for. The novel contribution being built toward is the first measured, held-out-validated characterisation of PARENT-FREE spectral abliteration detection, complete with its recipe-class boundary, its evasion boundary and its calibration failure - a smaller claim than iteration 1 hoped for and one that can actually be defended.\",\n      \"rationale\": \"Every MAJOR reviewer critique is a scope or discipline defect, not a data defect, and each has a cheap decisive fix that fits inside this iteration. The toolchain confound is the sharpest: architecture is not what W05 keys on, the edit recipe is, our own band-limited control already proves blindness to non-global edits, and arXiv:2604.08844 has ALREADY published this exact failure mode once (a spectral classifier trained on one editing method scores every out-of-method adapter below every in-method one, AUC 0.00). Finding the collapse is therefore a confirmation, not finding it is a genuine surprise, and either way the sentence we can defend improves. The same logic makes the laundering arm mandatory rather than optional: W05 is a MINIMUM over layers and so is by construction the most fragile of the five statistics to anything touching a single layer, which means an evasion boundary certainly exists and the only question is whether it sits before or after the un-censoring dies. That is a measurable question with in-house machinery we already built (the rank-one and band-limited controls), and the answer is publishable in both directions. The E_1 head-to-head is nearly free - pure tensor arithmetic on sibling pairs we have already downloaded - and it converts the paper's central trade from an assertion into a number. On the negative side, the reviewer's power objection is correct and fatal if unanswered: at 18 lineages a paired-rho CI half-width near 0.25-0.5 means the falsifier could barely have failed, so 'the interior buys nothing' and 'we cannot tell' are currently indistinguishable; a two-line simulation settles which sentence we own, and a pre-specified comparator (B01, which has a published prior) removes the best-of-11 selection advantage that currently makes the headline awkward given A02 numerically leads B09 at both aggregation units. The reliability and depth repairs are the same move applied twice - propagate a known source of noise or arbitrariness into the reported number instead of leaving it as an unquantified caveat. And the missing analysis.py is existential for a paper whose entire credibility argument IS measurement discipline: no reviewer will accept headline numbers that exist nowhere in the artifact, and the same file fixes the 'pre-registered' overreach by forcing every claimed rule to point at a stamped line. The five artifacts split cleanly along what each executor is good at - two weights-heavy experiments that download and compute, one pure re-analysis evaluation that ships the statistics code, one literature pass that cannot be run in code, and one provenance-grade dataset that both makes the recipe taxonomy citable and stocks iterations 4-5 with the candidate pool a bigger scope test will need. None blocks another; each is reportable alone.\",\n      \"artifact_directions\": [\n        {\n          \"type\": \"research\",\n          \"objective\": \"Close the two uncited prior works the reviewer named, establish the mechanical taxonomy of 2026 abliteration recipes with enough precision to reimplement each one, and return a defensible novelty sentence for the parent-free weights-only arm.\",\n          \"approach\": \"Four questions, answered from primary full text with exact numbers and section anchors; use scholarly search plus fetch_grep on PDFs and on repository/tool documentation. (A) arXiv:2604.08844 (Paul, 'Spectral Geometry of LoRA Adapters Encodes Training Objective and Predicts Harmful Compliance'). Extract verbatim: the exact per-layer feature list (norms, stable rank, singular-value entropy, effective rank, singular-vector cosine to a healthy centroid) and map it item-by-item onto our W06-W16; the manufacture protocol for the 38 adapters (base model, objectives, dose ladder if any); AUC 1.00 for binary drift and for all six pairwise objective comparisons; rho >= 0.956 ordinal severity; rho = 0.72 against HEx-PHI harmful compliance; and CRITICALLY the cross-method result reported as AUC 0.00 - transcribe the exact experimental setup that produced it, since it is our closest published precedent for the toolchain collapse we are testing. Write the three-axis distinction paragraph (parent-free vs delta-based; real community checkpoints vs manufactured adapters; edit-detection vs behaviour-prediction) AND the explanation of why our behaviourally-uncensored members show none of its behavioural signal. Its rho = 0.72 is a direct counterweight to any sentence of ours claiming weight geometry cannot carry behavioural signal - find every such sentence in the current draft and supply a corrected wording. (B) OBLITERATUS and community 'spectral certification'. Locate the toolkit (repo, docs, release notes, any write-up), and document verbatim: what its parent-free certification step computes from an abliterated checkpoint's own weights, what 'complete' vs 'incomplete' means operationally, and the documented cases where certification reads incomplete while practical refusal rate is 0%. This is prior community practice for the operation we claim as new and it independently mirrors our 'the ranking transfers, the calibration does not' finding; return the reframed novelty sentence. (C) RECIPE TAXONOMY, the input the scope experiment needs. For each of at least six mechanically distinct abliteration/uncensoring recipes - (i) global all-layer diff-in-means rank-one projection (huihui-ai / Josiefied class, our 8 positives), (ii) mlabonne's published notebook recipe, (iii) norm-preserving / projected abliteration (grimjim class), (iv) ORBA orthogonal-reflection bounded ablation, (v) multi-direction / SVD-subspace ablation, (vi) per-head or per-module surgery, (vii) DCT / spectral-cascade modes, (viii) behavioural uncensoring by ordinary SFT - write the EXACT weight update in equations, state which matrices it touches (o_proj / down_proj / embed_tokens / per-head slices), whether it is norm-preserving, whether it is rank-one, and whether it touches all layers. Then name concrete PUBLIC checkpoints at <= 4.2B parameters produced by each recipe, with repository id, uploader and the card or config evidence proving the recipe; flag which recipes have NO public sub-4B checkpoint, because those must be reimplemented in-house. Also state which of these recipes would and would not produce a shared approximate null direction across the whole write ensemble - a mechanistic prediction our experiment can then test. (D) Verify whether any published work computes a spectral or geometric abliteration/edit detector from a single checkpoint WITHOUT the parent, beyond OBLITERATUS's certification, and re-check the one source characterised in arXiv:2607.01854 that our previous draft could not reach (HTTP 403) - it is currently named as the largest residual risk to the novelty claim, so either resolve it or restate the risk precisely. Deliverable: a dossier with the reimplementable recipe equations, the two required citation paragraphs written out, a candidate-checkpoint table, and a list of numbered corrections to the current draft's wording.\",\n          \"depends_on\": [\n            {\n              \"id\": \"art_lMTPOpnFwKnw\",\n              \"label\": \"extends\"\n            }\n          ]\n        },\n        {\n          \"type\": \"dataset\",\n          \"objective\": \"Ship a provenance-grade, recipe-labelled checkpoint manifest that makes the scope claim citable, plus the two auxiliary corpora the laundering arm needs and the enumerated sub-4B Hub pool that a full undeclared-positive scan will draw from in later iterations.\",\n          \"approach\": \"Three row blocks in one schema-validated file, every row carrying pinned repo id, revision sha, resolved parameter count from the Hub API (never from on-disk bytes - the previous iteration found that double-counts repos shipping both .safetensors and .bin), file list with sizes, and an evidence field holding a <= 300-char quoted snippet from the card, config or linked code that justifies its label. (1) RECIPE-LABELLED EDIT MANIFEST, the headline block. Enumerate at least 25 sub-4.2B checkpoints that claim to be abliterated / uncensored / decensored / gabliterated / orthogonalised, spanning at least five DISTINCT uploaders and, where the card permits it, at least four distinct recipe classes (global rank-one diff-in-means; norm-preserving or projected; multi-direction / SVD subspace; per-head or partial-layer; behavioural SFT uncensoring). For each, record: uploader, declared parent, declared recipe with the quoted evidence, whether the recipe is inferable at all (a large fraction will be UNDECLARED - report that count as a first-class number, it is the honest measure of how much provenance a hub actually carries), and a recipe_class field with an explicit UNKNOWN value rather than a guess. Include the 8 members of the current abliterated class so the manifest is a superset, and mark them. Also record, for every row, whether the repository id contains an abliteration string - this quantifies exactly how much of the detection task a string match solves for free, which the reviewer correctly identified as unmeasured. (2) LAUNDERING CORPORA. A benign instruction-tuning split suitable for a 200-step LoRA SFT (a few thousand instruction/response pairs from a permissively licensed, non-safety-related source; record the license, and prefer sources without the CC-BY-NC constraint that limits two of our existing blocks), plus a WikiText-derived fluency evaluation split for perplexity screening of laundered checkpoints, plus a small held-out benign prompt set disjoint from the SFT data. (3) HUB SCAN POOL. Enumerate several hundred sub-4B text-generation checkpoints from the Hub with metadata only (no weights): repo id, downloads, parameter count, architecture family, full card text hash, and a boolean for whether the card or repo id declares abliteration/uncensoring. Stratify so the pool contains both declared and non-declaring chat models, and report the size distribution so a later scan can be costed in gigabytes rather than guessed. Ship the pool as a ranked scan order (most-downloaded undeclared chat models first) so the scan is reproducible and its coverage is stateable. Report honest coverage counts throughout, and validate the file against the standard dataset schema with full/mini/preview variants.\",\n          \"depends_on\": [\n            {\n              \"id\": \"art_lMTPOpnFwKnw\",\n              \"label\": \"guidance\"\n            },\n            {\n              \"id\": \"art_CKWQh2cOQLLQ\",\n              \"label\": \"extends\"\n            }\n          ]\n        },\n        {\n          \"type\": \"experiment\",\n          \"objective\": \"Measure the true scope of BOTH iteration-2 results: the recipe-class boundary of the parent-free scar (with leave-one-uploader-out and the first E_1 head-to-head), and the depth-invariance of the falsifier that produced the negative.\",\n          \"approach\": \"Three arms, all on tensors, sharing one download budget. Re-implement the weights statistics from the published definitions rather than importing them, and GATE the reimplementation before anything else: form A = sum over residual-write matrices (attention o_proj, MLP down_proj) of W W^T / ||W||_F^2, take v1 = eigenvector of the minimum eigenvalue, define e_W(u) = ||u^T W||^2 / (||W||_F^2 / d), and compute W01 = log10(median(lam)/lam_1), W02 = fraction of write matrices with e_W(v1) < 0.1, W03 = log10(q05(e_W(u_rand)) / mean e_W(v1)) over 256 random directions (256, not 64 - the previous text was wrong), W04 = log10(lam_2/lam_1), W05 = log10(min_W e_W(v1)). REPRODUCTION GATE: recompute on at least five of the eight original abliterated members and five non-abliterated ones and require agreement with the archived values - weakest abliterated W05 = -2.742 (huihui-ai/Qwen2.5-0.5B-Instruct-abliterated), next-weakest -3.522, strongest non-abliterated -2.665 (allenai/OLMo-1B-hf), abliterated W01 median 4.26, base W01 max 1.992. Report the reproduction deltas; if they do not reproduce, that is the headline and everything downstream is conditioned on it. ARM 1, RECIPE SCOPE. Acquire and measure at least three, target six, abliterated/uncensored checkpoints at <= 4.2B produced by MECHANICALLY DIFFERENT toolchains from the huihui/Josiefied class - verify the recipe from the card, config or linked code and record the evidence, do not trust the repo name. Concrete starting candidates to verify: mlabonne/Qwen3-0.6B-abliterated (this project already used it in iteration 1 and it is NOT among the 8 positives, so it is the cheapest recipe-diversity win available), grimjim-class projected / norm-preserving variants, ORBA orthogonal-reflection outputs, OBLITERATUS 'advanced' multi-direction runs, and per-head or partial-layer surgeries. Where a recipe class has no public sub-4B checkpoint, REIMPLEMENT it in-house on Qwen3-1.7B-Instruct and label it synthetic: (a) norm-preserving projection (project out r then rescale each W to its original Frobenius norm), (b) multi-direction ablation removing a rank-k subspace for k in {2, 4, 8}, (c) per-head surgery touching only attention heads whose refusal-direction write energy is highest, (d) a partial-layer variant sweeping the fraction of edited layers from 0.33 to 1.0 so the blind spot becomes a CURVE rather than the single band-limited point already reported. Report W01-W05 for every checkpoint, plus the recomputed AUROC of each statistic under three groupings: all abliterated vs all else, LEAVE-ONE-UPLOADER-OUT (train the ranking on all uploaders but one, evaluate on the held-out uploader's members), and leave-one-architecture-family-out for comparison. State the scope sentence the data supports, in the form 'detects <recipe class>' with the classes it misses named. ARM 2, E_1 HEAD-TO-HEAD, the matched-panel comparison the paper owes its closest competitor. For every instruct/abliterated sibling pair in the panel where the parent is present (at least Qwen2.5-0.5B, Qwen2.5-1.5B, Qwen3-0.6B, Qwen3-1.7B, Llama-3.2-1B, Llama-3.2-3B), compute E_1 = mean over matrices of sigma_1^2(dW)/sum_i sigma_i^2(dW) with dW = W_parent - W_candidate over o_proj and down_proj in the published mid-stack band, and compute the SAME quantity for benign fine-tune pairs (instruct vs its own base, and any behaviourally-uncensored member vs its parent) so E_1 has negatives. Report W05 vs E_1 AUROC on exactly that matched subset with bootstrap CIs, and state the trade in one sentence: either parent-free matches parent-required at zero prompt cost, or the price of the constraint in AUROC. Also apply E_1 to the new-toolchain checkpoints where a parent is resolvable, since the cross-method question applies to the incumbent too. ARM 3, DEPTH INVARIANCE OF THE NEGATIVE. The held-out AUROC depth profile saturates at 1.0 across indices 4-25 of 28, so rho* = 0.679 was fixed by a d'-tiebreak on a 22-layer plateau and the activation arm's poor showing may be a property of the depth, not the arm. Recompute the depth-sensitive activation metrics (diff-in-means separation, d', AUROC, AMS sigma and its concept cosine, refusal-axis-to-unembedding cosine, prompt-position and generated-step logit-lens refusal log-odds) at THREE relative depths spanning the plateau - the bare argmax (~0.14), 0.50, and the pre-declared 0.679 - on the chat-rendered members, using the frozen prompt folds and the plain-vs-chat renderer rule (base models plain, excluded from correlations). Emit a tidy long table of (member, metric, depth, value) so the falsifier can be re-tested at each depth downstream, and report alpha_50's ceiling-censoring count at each depth (it was 37/44 at 0.679) so depth and metric are separable. IMPLEMENTATION NOTES that cost days if rediscovered: HF derives positions from cache_position, so LEFT-padded batches need explicit position_ids = (mask.cumsum(-1)-1).clamp_min(0) on the forward and every decode step; use svdvals rather than sqrt(eigvalsh(W W^T)) for square attention matrices; download sequentially and delete weights after measuring; report which tier completed.\",\n          \"depends_on\": [\n            {\n              \"id\": \"art_CKWQh2cOQLLQ\",\n              \"label\": \"dataset\"\n            },\n            {\n              \"id\": \"art_BCxIq6GX4WIw\",\n              \"label\": \"dataset\"\n            },\n            {\n              \"id\": \"art_lMTPOpnFwKnw\",\n              \"label\": \"spec\"\n            }\n          ]\n        },\n        {\n          \"type\": \"experiment\",\n          \"objective\": \"Instantiate the deployment premise the paper currently only asserts: measure whether the scar survives ordinary post-processing and deliberate evasion, in what ORDER the flag and the un-censoring die, and whether any undeclared Hub checkpoint carries the signature.\",\n          \"approach\": \"Two arms. ARM 1, THE LAUNDERING LADDER, the decisive one. Using in-house edit machinery, abliterate Qwen3-1.7B-Instruct with a faithful global diff-in-means rank-one projection over every residual-write matrix (o_proj, down_proj, and embed_tokens if the reference implementation includes it - record which), verify the edit landed by requiring the same signature the panel's abliterated members show (W02 near 1.0, W01 above 3, W05 well below -3) and by requiring harmful-refusal rate to collapse relative to the parent. Then take that checkpoint through five laundering treatments, each a separate branch from the SAME abliterated root: (a) LoRA-SFT for 200 steps on benign instruction data (report rank, alpha, target modules, learning rate, and merge the adapter before measuring so the weights are directly comparable); (b) linear merge with the instruct parent at weights 0.25 / 0.50 / 0.75, giving a merge ladder rather than one point; (c) round-trip int8 and int4 quantization and dequantization back to the original dtype; (d) added-back random rank-one term epsilon * u u^T W at increasing epsilon, the metric-aware adversary who knows W05 is a minimum over layers and only needs to lift the smallest one; (e) a combined worst case (quantize then merge at 0.25). At EVERY stage report all five weight statistics AND the behavioural readout on the same items used for the panel's ground truth - harmful-refusal rate on the 40-item stratified harmful core and over-refusal on the 25 XSTest-safe items, greedy, with the behaviour-scoring judge rubric that separates 'did the model comply' from 'is the content harmful' (the harmfulness-scoring rubric gives kappa ~0 and must not be used), plus a fluency screen (WikiText perplexity and within-response distinct-3) so a stage that merely broke the model is not scored as evasion. Judge spend capped at $1.50 and logged after every call. THE LOAD-BEARING OUTPUT is a single figure and table showing the two curves - flag strength (W05, and W01/W04 alongside) and un-censoring strength (harmful compliance) - against treatment intensity, with the crossing point stated: if the flag dies only AFTER the model stops being uncensored, the scar is a robust provenance signal and that is a strong result; if it dies first, the scar is evadable and the paper says so plainly and quantifies the evasion cost. Report which of the five statistics is most robust - the prediction is that W05, being a minimum, is the most fragile and W01/W02, being aggregates, degrade more gracefully, which if true is an immediate and cheap methodological improvement to the metric. ARM 2, THE HUB SCAN. Score sub-4B checkpoints that do NOT declare abliteration in their repo id or card, from stored tensors only, in downloads-ranked order, deleting each after measurement; state the number completed rather than promising a target, and prioritise the smallest models so coverage is maximised within the time budget (aim for at least 40 completed, more if bandwidth permits). Report the full score distribution, name every checkpoint scoring inside or near the abliterated region defined by the panel (W05 below -2.742, and the warning band -2.742 to -2.5), and for each such hit fetch its card and lineage and adjudicate whether it is a genuine undeclared edit, a merge of an abliterated ancestor, or a false positive - quoting the evidence either way. Report the false-positive count against the number scanned as the deployment-relevant number, and note that architectures outside the seven tested are where false positives are expected to concentrate (the three nearest-boundary non-abliterated members are all from single-member families, olmo and gpt_neox). Even a handful of confirmed undeclared positives makes the deployment claim concrete; zero hits over N scanned is also a reportable and useful specificity number.\",\n          \"depends_on\": [\n            {\n              \"id\": \"art_CKWQh2cOQLLQ\",\n              \"label\": \"dataset\"\n            },\n            {\n              \"id\": \"art_BCxIq6GX4WIw\",\n              \"label\": \"dataset\"\n            },\n            {\n              \"id\": \"art_lMTPOpnFwKnw\",\n              \"label\": \"spec\"\n            }\n          ]\n        },\n        {\n          \"type\": \"evaluation\",\n          \"objective\": \"Ship analysis.py as a first-class versioned deliverable that recomputes every statistic in the paper, and use it to turn the negative from a verdict into a measurement - power, pre-specified comparator, reliability-corrected correlations - while auditing every 'pre-registered' claim and every numeral against the artifact that records it.\",\n          \"approach\": \"Pure re-analysis of the archived iteration-2 trees; no new model inference beyond LLM judging for the reliability arm. (1) ANALYSIS.PY, the centrepiece. One script reading long_table.jsonl / battery + behaviour.jsonl and emitting EVERY AUROC, Spearman, bootstrap CI and paired difference that appears in the paper - the Sec 5.1 weights-arm AUROCs, the Sec 5.2 correlation table at both aggregation units, and all seven paired |rho_X| - |rho_B09| differences. Print in the file header, and echo into the output: the RNG seed, B, whether lineages are resampled with or without replacement, exactly how the 9 singleton lineages are handled, the tie-handling rule for Spearman (rank-average, explicitly - the project's own audit found position-based tie-breaking flipped the sign of a previous result), the AUROC tie convention, and the base-model exclusion rule. Include an assertion block checking each recomputed value against the number quoted in the current draft, and emit a table of every disagreement - transcription errors are expected and finding them is part of the deliverable. Also emit, machine-readable, the numerals the draft must regenerate rather than transcribe: [min, max] for EVERY class in the weights table (not only the abliterated column - base W01 max 1.992 genuinely overlaps abliterated min 1.438, and base W02 max 1.000 equals the abliterated median), the nearest non-abliterated neighbour on W05 by name (allenai/OLMo-1B-hf, -2.665), the family membership of the three checkpoints nearest the boundary, the correct random-direction count for W03 (256, not 64), and the exact positive-control checkpoint and revision (Qwen/Qwen3-0.6B, the instruct member, whose unedited W01 is 0.624 - distinct from the Base member's 0.628, and distinct from the unrelated 4.82 values that currently read as a typo). (2) POWER. Simulate the actual paired lineage bootstrap at n = 18 lineages under the observed rank structure and report the minimum detectable |rho| difference at 80% power, plus the achieved CI half-widths. State explicitly whether the falsifier COULD have failed, and emit the restated conclusion sentence in the form the data supports: 'at this panel size no interior metric shows an advantage over the best black-box baseline larger than ~X in |rho|; distinguishing smaller advantages needs roughly N lineages.' (3) COMPARATOR. B09 was selected as best-of-11 black-box declarations on the same data, so the current headline is best-of-11 against a fixed white-box candidate. Report the paired comparison against the PRE-SPECIFIED B01 (first-step logit gap, which has a published prior) alongside the post-hoc winner, and quantify the selection advantage by re-running the best-of-11 selection inside the bootstrap. Reconcile explicitly the awkward fact that A02 leads B09 numerically at both aggregation units (+0.802/+0.819 vs +0.766/+0.852) - state whether the headline should be 'no interior metric beats black-box with a CI excluding zero' or the weaker-but-true 'the numerically best metric is an interior one whose advantage is not resolvable'. (4) RELIABILITY AND ATTENUATION. Each checkpoint's harmful-refusal rate rests on 40 items scored by a single judge with judge-vs-screen kappa ~0.30 - a binomial SE of ~0.08 at p = 0.5 before judge noise. Estimate reliability by split-half over the 40 items (Spearman-Brown corrected) and by re-judging a stratified subsample of the archived generations with an independent adjudicator model under the behaviour-scoring rubric, reporting agreement; then report attenuation-corrected versions of every Sec 5.2 correlation and every paired difference alongside the raw ones, plus per-member binomial error bars, and state whether ANY ordering moves. LLM spend capped at $1.00 with per-call logging and response caching so a rerun costs $0. (5) DEPTH AND CENSORING. Re-run the Sec 5.2 correlation table at the three plateau depths and state whether the falsifier conclusion is invariant; if any activation metric beats the black-box baseline at some depth in the plateau, disclose it prominently even though 0.679 is the pre-declared primary. Report alpha_50's censoring rate at each depth. If the depth-swept activation values from this iteration's scope experiment are unavailable, run this arm on whatever depth-varying quantities the archive already contains and say exactly which depths were reachable. (6) PRE-REGISTRATION FIDELITY. Audit the SHA-stamped metric_spec.py against every claim in the paper of the form 'pre-registered'. That file declares 53 metrics with family, prompt requirement and declared cost, and NOTHING ELSE - no falsifier, no analysis plan, no base-model exclusion rule, no blanket-refuser threshold, no bootstrap specification. Emit a table mapping every such claim to the artifact and line that actually records it, marked SUPPORTED / PLAN-ONLY / UNSUPPORTED, and supply the corrected wording for each unsupported one ('we adopted the rule that...'), reserving 'SHA-stamped pre-registration' for the metric declarations alone. Deliverable: analysis.py plus a machine-readable numbers file that the paper generates its numerals from.\",\n          \"depends_on\": [\n            {\n              \"id\": \"art_xyUlckdGtbjc\",\n              \"label\": \"reanalyzes\"\n            },\n            {\n              \"id\": \"art_CbL-EUQlwgfw\",\n              \"label\": \"reanalyzes\"\n            },\n            {\n              \"id\": \"art_BCxIq6GX4WIw\",\n              \"label\": \"reference\"\n            }\n          ]\n        }\n      ],\n      \"expected_outcome\": \"By the end of this iteration the paper's two claims are bounded rather than merely stated. (1) SCOPE: W01-W05 measured on at least three, target six, abliterated checkpoints from mechanically different toolchains plus in-house reimplementations of norm-preserving, multi-direction, per-head and partial-layer recipes, with leave-one-UPLOADER-out reported beside leave-one-family-out and a partial-layer sweep turning the band-limited blind spot into a curve - yielding a defensible scope sentence naming the recipe class detected and the classes missed. Plus the first computed E_1 head-to-head on the matched sibling subset, which quantifies what the parent-free constraint costs instead of asserting the trade. Plus a depth-swept activation table letting the falsifier be re-tested at three depths spanning the 22-layer plateau. (2) DEPLOYMENT: a laundering ladder reporting flag strength and un-censoring strength at every stage of LoRA-SFT, three merge ratios, int8/int4 round-trip, an adversarial added-back rank-one term and a combined worst case, with the crossing point of the two curves stated explicitly, plus a Hub scan of undeclared sub-4B checkpoints reporting hits, adjudicated evidence, and a specificity number. (3) DISCIPLINE: analysis.py recomputing every headline statistic with seed, B, resampling scheme and rank-average tie handling printed and asserted against the quoted values; a power simulation stating whether the falsifier could have failed and the restated conclusion; the pre-specified B01 comparison beside the best-of-11 winner with the selection advantage quantified; split-half and adjudicator reliability with attenuation-corrected correlations and per-member error bars; and a SUPPORTED / PLAN-ONLY / UNSUPPORTED table for every 'pre-registered' claim with corrected wording. (4) POSITIONING: arXiv:2604.08844 and OBLITERATUS's spectral certification cited at their points of use with the three-axis distinction written out, a reimplementable taxonomy of six-plus abliteration recipes, and a resolved or precisely restated novelty risk. (5) A recipe-labelled, evidence-carrying manifest of 25+ edited checkpoints, laundering corpora, and a ranked Hub scan pool that stocks iterations 4-5. Negative outcomes are all reportable and several are likely by design: the most probable single result is that the scar survives quantization and merging but not LoRA-SFT, and misses at least one new toolchain - which turns the headline into 'a recipe-class provenance signal, free at hub scale, with a measured evasion boundary'. If instead the cross-toolchain AUROC holds, that is a genuine surprise against the published AUC-0.00 precedent and a considerably stronger paper. Either way iterations 4-5 inherit a bounded claim, working analysis code, and a candidate pool for scaling the scope test.\",\n      \"summary\": \"Iteration 3 stops adding metrics and starts bounding the two results it already has. Two weights-heavy experiments measure the scar's recipe-class scope (new toolchains, in-house norm-preserving / multi-direction / per-head / partial-layer reimplementations, leave-one-uploader-out, and the first E_1 parent-required head-to-head) and its evasion boundary (LoRA-SFT, merge ladder, int8/int4 round-trip, adversarial added-back rank-one, plus a Hub scan for undeclared positives), reporting flag death against un-censoring death. One evaluation ships analysis.py - every AUROC, Spearman, bootstrap and paired difference with seed, B, resampling scheme and tie-handling printed and asserted - and converts the negative into a measurement via a power simulation, a pre-specified comparator, reliability-corrected correlations and a depth-invariance check, while auditing every 'pre-registered' claim against the file that actually records it. One research pass closes the two uncited prior works and returns a reimplementable recipe taxonomy; one dataset ships the evidence-carrying, recipe-labelled checkpoint manifest and the scan pool for later iterations.\"\n    }\n  ]\n}", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [8] TOOL CALL — Bash · 2026-08-13 20:11:42 UTC

```
python3 -c "
import json;d=json.load(open('.terminal_claude_agent_struct_out.json'))
s=d['strategies'][0];print(len(d['strategies']),len(s['artifact_directions']))
for a in s['artifact_directions']:print(a['type'],[x['id'] for x in a.get('depends_on',[])])
"
```

### [9] TOOL RESULT — Bash · 2026-08-13 20:11:42 UTC

```
{"stdout": "1 5\nresearch ['art_lMTPOpnFwKnw']\ndataset ['art_lMTPOpnFwKnw', 'art_CKWQh2cOQLLQ']\nexperiment ['art_CKWQh2cOQLLQ', 'art_BCxIq6GX4WIw', 'art_lMTPOpnFwKnw']\nexperiment ['art_CKWQh2cOQLLQ', 'art_BCxIq6GX4WIw', 'art_lMTPOpnFwKnw']\nevaluation ['art_xyUlckdGtbjc', 'art_CbL-EUQlwgfw', 'art_BCxIq6GX4WIw']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] ASSISTANT · 2026-08-13 20:11:55 UTC

```
Written and validated: `./.terminal_claude_agent_struct_out.json` — 1 strategy, 5 artifacts, all deps resolving to existing artifact IDs and satisfying the type rules (experiments ← datasets, evaluation ← experiments).

**Strategy: "Find where the weight fingerprint breaks"** — the battery is retired; this iteration bounds the two claims instead of adding metrics.

| # | Type | What it settles |
|---|---|---|
| 1 | research | H6 positioning: arXiv:2604.08844 (its AUC 0.00 cross-method collapse is our precedent) + OBLITERATUS parent-free spectral certification; returns a reimplementable taxonomy of 6+ abliteration recipes |
| 2 | dataset | Recipe-labelled, evidence-quoted manifest of 25+ edited checkpoints (incl. how many are solved by a repo-name string match), laundering corpora, ranked Hub scan pool for iters 4–5 |
| 3 | experiment | H1+H3+H4(d): cross-toolchain W01–W05 with leave-one-**uploader**-out, in-house norm-preserving / multi-direction / per-head / partial-layer edits, first computed **E_1** head-to-head on matched sibling pairs, depth-swept activation table across the 22-layer plateau |
| 4 | experiment | H2 deployment: laundering ladder (LoRA-SFT, 3 merge ratios, int8/int4, adversarial added-back rank-one) reporting flag death vs un-censoring death, plus a Hub scan of undeclared checkpoints |
| 5 | evaluation | H4(a–c)+H5+H7: `analysis.py` as a versioned deliverable with seed/B/resampling/tie-handling asserted against quoted values; power sim, pre-specified B01 comparator, split-half + adjudicator reliability with attenuation correction, and a SUPPORTED/PLAN-ONLY/UNSUPPORTED audit of every "pre-registered" claim |

Two judgement calls worth flagging: the depth sweep needs forward passes, so it went into experiment 3 (which downloads those members anyway) rather than the evaluation, whose scope is re-analysis; and since `depends_on` can only reference existing artifacts, the two experiments must resolve their own checkpoints — I named concrete starting candidates (notably `mlabonne/Qwen3-0.6B-abliterated`, already used in iteration 1 and absent from the 8 positives) and added an in-house-reimplementation fallback so the recipe-scope test cannot be blocked by repo availability.
```

### [11] SYSTEM-USER prompt · 2026-08-13 20:11:58 UTC

```
<verification_results>
Your previous response had issues that need fixing:

DEPENDENCY ERRORS (depends_on can ONLY reference IDs from <existing_artifacts>):
  - Strategy 1: Artifact 'dataset_iter3_dir2' (dataset): dependency 'art_CKWQh2cOQLLQ' has type 'dataset' which is not allowed (allowed: {'research'})

</verification_results>

<task>
Fix ALL issues above and regenerate your strategies:

1. Fix dependency errors:
   - depends_on is a list of {id, label} objects — every entry MUST have a non-empty short label
   - id can ONLY reference IDs from <existing_artifacts>
   - You CANNOT reference artifacts you are proposing in this strategy as dependencies (they all run in parallel)
   - Follow the dependency type rules (e.g., experiments require datasets)
   - If no suitable existing artifacts exist, use depends_on: []

Output the corrected JSON with the fixed strategies.
</task>
```

### [12] TOOL CALL — Edit · 2026-08-13 20:12:04 UTC

```
File: /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json
OLD:             {
              "id": "art_lMTPOpnFwKnw",
              "label": "guidance"
            },
            {
              "id": "art_CKWQh2cOQLLQ",
              "label": "extends"
            }
          ]
NEW:             {
              "id": "art_lMTPOpnFwKnw",
              "label": "guidance"
            }
          ]
```

### [13] TOOL RESULT — Edit · 2026-08-13 20:12:04 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json", "oldString": "            {\n              \"id\": \"art_lMTPOpnFwKnw\",\n              \"label\": \"guidance\"\n            },\n            {\n              \"id\": \"art_CKWQh2cOQLLQ\",\n              \"label\": \"extends\"\n            }\n          ]", "newString": "            {\n              \"id\": \"art_lMTPOpnFwKnw\",\n              \"label\": \"guidance\"\n            }\n          ]", "originalFile": null, "structuredPatch": [{"oldStart": 24, "oldLines": 10, "newStart": 24, "newLines": 6, "lines": ["             {", "               \"id\": \"art_lMTPOpnFwKnw\",", "               \"label\": \"guidance\"", "-            },", "-            {", "-              \"id\": \"art_CKWQh2cOQLLQ\",", "-              \"label\": \"extends\"", "             }", "           ]", "         },"]}], "userModified": false, "replaceAll": false}
```

### [14] TOOL CALL — Bash · 2026-08-13 20:12:08 UTC

```
python3 -c "
import json;d=json.load(open('.terminal_claude_agent_struct_out.json'))
for a in d['strategies'][0]['artifact_directions']:print(a['type'],[(x['id'],x['label']) for x in a.get('depends_on',[])])
"
```

### [15] TOOL RESULT — Bash · 2026-08-13 20:12:08 UTC

```
{"stdout": "research [('art_lMTPOpnFwKnw', 'extends')]\ndataset [('art_lMTPOpnFwKnw', 'guidance')]\nexperiment [('art_CKWQh2cOQLLQ', 'dataset'), ('art_BCxIq6GX4WIw', 'dataset'), ('art_lMTPOpnFwKnw', 'spec')]\nexperiment [('art_CKWQh2cOQLLQ', 'dataset'), ('art_BCxIq6GX4WIw', 'dataset'), ('art_lMTPOpnFwKnw', 'spec')]\nevaluation [('art_xyUlckdGtbjc', 'reanalyzes'), ('art_CbL-EUQlwgfw', 'reanalyzes'), ('art_BCxIq6GX4WIw', 'reference')]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] ASSISTANT · 2026-08-13 20:12:11 UTC

```
Fixed. The dataset artifact's disallowed `art_CKWQh2cOQLLQ` (dataset→dataset) dep is removed; it now depends only on the research artifact `art_lMTPOpnFwKnw`, which is permitted. All other deps were already valid, every entry has a non-empty label, and no proposed artifact is referenced.

The dataset's approach is unaffected in substance — it already builds its manifest by enumerating and re-resolving checkpoints from the Hub API (the previous iteration found on-disk byte counts unreliable for parameter counts), and it still treats the existing 8 abliterated members as a marked subset, so the frozen manifest is superseded rather than depended on.
```
