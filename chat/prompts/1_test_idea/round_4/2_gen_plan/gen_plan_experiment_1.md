# gen_plan_experiment_1 — test_idea

> Phase: `invention_loop` · round 4 · `gen_plan`
> Run: `iter1_33370088803c` — Catching Edited Safety Models by Reading Weights in Sliding Windows
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-13 23:49:42 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A plan generator (Step 3.2: GEN_PLAN in the invention loop)

You received the hypothesis, an artifact direction to elaborate, and dependency artifacts relevant to the plan.
Your job: elaborate this direction into a detailed, actionable plan for the executor agent.

Specific, actionable plan → valuable artifact. Vague plan → wasted execution.
</your_role>
</ai_inventor_context>

<artifact_type_info>
You are expanding an artifact direction of type: EXPERIMENT

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance
</artifact_type_info>

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

<time_budget>

The experiment executor has 6h total (including writing code, debugging, testing, and fixing errors).

</time_budget>

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

<plan_guidelines>
You are expanding an artifact direction from the strategy into a detailed plan.
The artifact direction specifies what to do at a high level (type, objective, approach, dependencies).
Your job is to make it concrete and actionable as a detailed plan.
Use web research to look up technical details, verify feasibility, and find reference materials
that will make your plan more concrete and actionable for the executor.

GOOD PLANS:
- Make each component SPECIFIC and actionable (not vague platitudes)
- Consider both success AND failure scenarios
- Build on the approach in the artifact direction
- Add concrete details the executor needs

BAD PLANS:
- Vague hand-waving ("do research on X")
- Ignoring the approach in the artifact direction
- Missing critical details the executor needs
</plan_guidelines>

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
kind: hypothesis
title: Spotting an edited safety model from weights
hypothesis: |-
  CORE CLAIM, STILL SPLIT IN TWO, WITH CLAIM A NOW MECHANISTICALLY RESTATED. The original claim — safety behaviour is legible from the model alone, cheaply, better than from its outputs — remains resolved into one supported half and one bounded negative. Iteration 3 executed the scope, laundering, head-to-head, power and audit arms and changed WHAT the supported half is a claim about. It is not a claim about abliteration, nor about uploaders. It is a claim about UNIFORMITY.

  CLAIM A (SUPPORTED, NARROWED, AND NOW WITH A MECHANISM): a checkpoint carrying a UNIFORM, COMPLETE, ALL-LAYER directional annihilation can be certified from its tensors alone — no parent, no reference model, no prompts, no forward passes, ~7 s of CPU linear algebra. W05 = log10 min_l e_W(v1) over the pooled residual-write Gram is a MINIMUM over layers, so it fires only when the suppression admits NO exception anywhere in the stack. Every measured failure of W05 is one failure mode wearing different costumes: the edit is not uniform.
  CLAIM B (REFUTED AS ORIGINALLY STATED, NOW QUANTITATIVELY BOUNDED): for GRADED BEHAVIOURAL SAFETY, no interior observable in the frozen 53-metric battery beats a trivial black-box baseline — but the design could only have detected an advantage of |drho| >= 0.32 at n = 19 lineages, so the honest sentence is bounded, not universal.

  WHAT ITERATION 3 SETTLED (do not re-litigate; do not re-run).
  T1. THE SCAR IS SPECIFIC IN THE WILD. 160 sub-4B undeclared Hub checkpoints scored from stored tensors: ZERO hits inside the abliterated region, Wilson 95% [0, 0.023], 8/8 positive and 12/12 negative controls through the identical path, median 7.0 s CPU / 2.7 s GPU, $0 (art_gCgia-6VUZJb). Only W05 earns it: W01/W03/W04 sit at sensitivity 0.875, W02 flags 23/160 undeclared repos so its threshold separates nothing, and the hardened W05q10 buys specificity at 0.875 sensitivity.
  T2. THE 'UPLOADER EFFECT' IS A RECIPE EFFECT — THE REVIEWER IS RIGHT AND THE ARTIFACT'S OWN CARDS PROVE IT. Four real published <=4.2B abliterated checkpoints from unseen uploaders were missed (AUROC 0.382, 0/4 at threshold), and the experiment labelled all four recipe_class = global_diff_in_means, mechanically_different = false. The verbatim card evidence stored in those same rows contradicts the label: MagicalAlchemist/Qwen3-1.7B-Magic_decensored is 'made using Heretic v1.1.0' (direction_index 17.89, attn.o_proj.max_weight 0.84), prithivMLmods/VibeThinker-3B-heretic_decensored is 'modified using the Heretic abliteration toolkit', and mlabonne/Qwen3-0.6B-abliterated states its subtraction weights 'follow a normal distribution with a certain spread and peak layer'. Heretic is recipe [14] and mlabonne v2 is recipe [13] in this paper's OWN taxonomy — per-component optimised and Gaussian DEPTH-WEIGHTED kernels, explicitly not the uniform all-layer projection the archived positives use. At least three of four misses are therefore depth-weighted or sub-unit-weight kernels. This also explains E_1 = 0.995–0.997 on all three: the per-matrix delta is still near rank one, but the annihilation is INCOMPLETE in some layers, which is exactly what a minimum-over-layers statistic cannot survive.
  T3. THE UNIFORMITY STATEMENT UNIFIES THREE PREVIOUSLY SEPARATE 'MYSTERIES'. (a) The layer-fraction sweep gives f* = 1.00 on BOTH hosts — only the fully global edit is visible. (b) A projection confined to the middle 50% of layers drives harmful refusal 0.45 -> 0.00, exactly as effective as the full-stack edit, while W05 moves -1.0098 -> -1.0088. (c) The depth-weighted-kernel misses of T2. All three are the same fact. A synthetic unit test shows why it is a THRESHOLD, not a ramp: with 4 of 12 matrices edited, v1 is no longer the injected direction at all (W02 = 0) because the Gram pools every matrix. Detected at AUROC 1.000: plain, norm-preserving, and rank-k (k = 2,4,8) — all uniform. Missed: per-head surgery (0.556), any layer-band edit, any depth-weighted kernel.
  T4. THE FLAG IS EVADABLE, AND THE ORDER OF THE TWO DEATHS IS MEASURED — BUT THE BEHAVIOURAL AXIS HAS NO ERROR BARS AND MUST GET THEM. 34-stage ladder on an in-house abliteration of Qwen3-1.7B (root: refusal 0.923 -> 0.162, W05 -4.592, WikiText ppl 27.08 -> 26.25). EVADABLE in 4 of 6 real axes; NEITHER_DIES for argmin-only add-back, random-direction add-back and LoRA-SFT. Two pre-registered predictions REVERSED in the detector's favour: the argmin attack fails (a local patch rotates v1 and lifts EVERY matrix's energy — a local edit has a global effect on the statistic; 4 matrices must be patched), and 200 benign LoRA steps move W05 only -4.592 -> -4.381 while RESTORING refusal 0.162 -> 0.368. CAVEAT THE PAPER MUST FIX: every stage scores 40 harmful items (achieved 34–40), binomial SE ~0.075 at p = 0.2, so the quoted 'evasion cost -0.004' and 'int4 refusal 0.135 BELOW the root's 0.162' are NOT resolvable differences. The ORDERING is the result; the decimals are not.
  T5. THE PARENT-FREE CONSTRAINT COSTS NOTHING ON THE UNIFORM RECIPE AND IS COMPLEMENTARY, NOT DOMINATED. E_1 vs W05: tie at AUROC 1.000 on 12 pre-declared pairs (paired diff +0.000); -0.167 [-0.444, 0.000] on 15 pairs including new uploaders (E_1 3/3, W05 0/3 — underpowered as an interval, unambiguous descriptively); -0.186 [-0.382, -0.079] including 26 in-house synthetics. Failure modes are DISJOINT: E_1 degrades on multi-direction edits (0.17–0.67, k = 8..2) where W05 is perfect, and holds at 0.995 on the band edits W05 cannot see. The E_1 band (0.25L–0.75L) is OUR reading of 'mid-stack' and was never varied.
  T6. THE BEHAVIOURAL NEGATIVE IS NOW A MEASUREMENT, NOT A VERDICT (art_0T8jhUa0zxmu). Minimum detectable |drho| = 0.32 at 19 lineages; power 0.012 at 0.20, 0.70 at 0.30; ~50 lineages for 0.30, ~150 for 0.20, unreachable at 0.10; falsifier_could_have_failed = TRUE. B09 is NOT the best black-box metric (B08 first-token entropy asymmetry |rho| 0.782 at lineage level, B01 logit gap 0.708 at member level; B09 is the in-resample argmax in only 11.2%/14.4%; selection optimism +0.182) — correcting this STRENGTHENS the negative. Split-half r_xx = 0.968 so attenuation correction is 1.016: the negative is NOT an attenuation artefact. Depth is INVARIANT: BLACKBOX_WINS at 0.143, 0.500 and 0.679 over 26 members / 1014 rows, and the near-win (A19 +0.770 vs B09 +0.766) has paired difference +0.0045 [-0.225, +0.260] — point estimates alone would have called it a win.
  T7. OUR OWN REPORTING WAS THE LARGEST SOURCE OF ERROR. Four values the draft called CORRELATIONS are PAIRED DIFFERENCES |rho_X| - |rho_B09| on a 26-member renderer == 'chatml' subset, not the stated 28-member non-base subset (read as correlations they are wrong by up to 0.67 and one has the wrong sign; the falsifier verdict is unchanged on both subsets). W05's 'AUROC 1.000' is the ORIENTED value (raw 0.000); W01/W03/W04 give 0.986, W02 0.950 with 21 tied pairs; margin 0.0763 log10; '-2.742 = abliterated minimum' is its MAXIMUM (true min -4.820). W03 uses 256 random directions, not 64. Pre-registration audit: 4 SUPPORTED / 2 PLAN-ONLY / 6 UNSUPPORTED — metric_spec.py stamps 53 metric declarations and nothing else.
  T8. TWO DISSOCIATIONS. Held-out harmful/benign AUROC SATURATES (11 layers >= 0.997, 4 tied at exactly 1.000) and cannot select the refusal direction; the AUROC pick reproduces the full weight signature while leaving refusal at 0.333 vs the behavioural pick's 0.162 — SCAR AND UN-CENSORING ARE DISSOCIABLE AT CONSTRUCTION TIME. And the Arditi 12-substring screen reads 0.000 on every abliterated-derived stage where the judge reads 0.13–0.37 (rate-level r = 0.952): the screen is the broken instrument, not the judge.
  T9. THE HUB LANDSCAPE IS MEASURED (art_8OlSrcw-hzgO). 513 self-declared edited sub-4.2B checkpoints from 189 uploaders; UNKNOWN recipe = 23.4%; repo_id contains an abliteration string in 50.5% — a plain regex already solves HALF the detection task, and that, not chance, is the baseline. R5 spectral/DCT is EMPTY and unrunnable at this scale.

  THE REVISED CLAIMS FOR ITERATION 4. No new battery, no new panel-scale sweep. Six things, most of them re-analysis of tensors and rows we already hold.

  H1 (RELABEL AND RE-DERIVE: RECIPE IS PRIMARY, UPLOADER IS SECONDARY — the reviewer's decisive point, and nearly free). Re-derive recipe_class for all four new-uploader checkpoints from their cards, quoting the Heretic parameter table and mlabonne's normal-distribution sentence in the text; correct results/arm1_real.jsonl's recipe_class and mechanically_different flags; re-run the grouping analysis with RECIPE as the primary grouping variable and uploader as secondary. Then rewrite the headline everywhere from 'three of four unseen uploaders running the same nominal recipe escape' to the mechanism the data support: 'W05 requires a uniform, complete annihilation in every layer; any depth-weighted or sub-unit-weight kernel (mlabonne v2 Gaussian, Heretic per-component optimised) escapes it, exactly as a band-limited edit does.' Fold f* = 1.00, the middle-50% invisibility and the kernel misses into ONE statement about uniformity rather than three separate mysteries. DELETE the '>=14.9B constraint' limitation: our own prior-art artifact (art_sHF0cggp2IvT) records public MPOA, Heretic and OBLITERATUS checkpoints at 4,022,468,096 params on the panel's own Qwen3-4B family, and the experiment measured two Heretic checkpoints without recognising them. Measure W01–W05 on those sub-4.2B MPOA / Heretic / OBLITERATUS checkpoints and on an in-house ORBA (Householder) reimplementation — ORBA is the sharpest falsification target because a reflection flips the component along u instead of removing it and preserves ||w|| exactly, leaving no null direction for W05 to find. PREDICTION, stated so it can fail: uniform-kernel recipes (plain, norm-preserving, rank-k, OBLITERATUS rank-k presets) are detected; depth-weighted kernels (mlabonne v2, Heretic) and reflections (ORBA) are not.

  H2 (FIX THE DEPLOYMENT NUMBER'S DENOMINATOR). The 0/160 rests on a population that does not match its description: ~30 unit-test fixtures at hidden_size = 8 / n_layers = 2 (trl-internal-testing/tiny-*, peft-internal-testing, llamafactory, echarlaix, yujiepan, MaxJeblick, hmellor), three single-layer EAGLE3 speculator draft heads, several sub-30 MB toys — 44 of 160 degenerate — plus at least one 14B MLX-4bit repo admitted by a download-ranked candidate list. A minimum of per-layer write energy over an eigenvector of a pooled Gram is not defined on a two-layer 8-dimensional stub, and a one-layer draft head has one term in the minimum. Declare an eligibility rule BEFORE reporting the rate (n_layers >= 8, hidden_size >= 128, tensor bytes consistent with <= 4.2B at the declared dtype, exclude cards/tags identifying test fixtures, speculator/draft heads and quantized re-uploads), report the false-positive rate and Wilson interval on the FILTERED denominator as primary with raw 0/160 as a secondary row, ship a model_type x count composition table, and state in Method the layer-count floor below which the statistic is degenerate. Also reconcile the counts mechanically from scan.jsonl (270 rows of which 20 are labelled controls; 65 vs 81 UNRESOLVED is stale in one artifact) instead of transcribing them.

  H3 (SPLIT THE QUANTIZATION FINDING IN TWO, AND RUN THE ONE-AFTERNOON REMEDY). (a) MEASURED: a dequantized int4 round-trip of an abliterated model scores clean on W05 (-4.59 -> -1.95) while remaining un-censored. (b) OPERATIONAL: in the wild-scan pipeline a quantized upload is UNRESOLVED, not clean — GPTQ/bitsandbytes weights are among the stated causes of the 81 unresolved repos — so at hub scale the effect is refusal-to-score, which is itself an auditable signal, not a silent false negative. Then run the follow-up already flagged as a limitation: dequantize the int4 stage to fp16 and recompute W01–W05. If the scar returns, the limitation shrinks from 'cheaply evadable' to 'requires dequantization before scoring', which is a materially better sentence. Report int4's perplexity cost honestly: 26.25 -> 37.7 (+43%) is a quality cost a deployer notices, so 'for free' overstates it — the fluency screen is distinct-3, not perplexity.

  H4 (PUT ERROR BARS ON THE LADDER AND ADD A SECOND ROOT). Add Wilson or bootstrap intervals to every harmful-refusal rate in the ladder table and figure, and restate every crossing as an ORDERING with overlap made explicit ('at the intensity where the flag first dies, harmful refusal is statistically indistinguishable from the unlaundered root: 0.158 [0.07, 0.31] vs 0.162 [0.07, 0.32]'). Drop the signed evasion cost to one significant figure or replace it with an interval on the difference. Separately, the ladder generalises from ONE in-house abliteration of ONE model with ONE direction and ONE selection rule, and since the central scope finding is that the statistic keys on uniformity, the crossing intensities are plausibly recipe-dependent: repeat the three cheapest families (merge, quantization, add-back-all) on at least one second root — ideally an in-house DEPTH-WEIGHTED (Heretic-style Gaussian kernel) edit, and one on a different architecture (the Llama-3.2-1B-Instruct host is already in the arm-1 code path). Prediction: a non-uniform root starts closer to the boundary and dies sooner. Even one extra root turns 'the flag dies at w = 0.10' from an anecdote into a range.

  H5 (THRESHOLD BRITTLENESS AND E_1 BAND SENSITIVITY — both pure re-analysis). (a) The scan threshold is the panel-fitted boundary -2.7415117804288127, carried by two individual checkpoints across a 0.0763 log10 margin, deployed on a population two orders of magnitude larger with no out-of-panel calibration; the two nearest scan neighbours (rinna/japanese-gpt-neox-small -2.614, stabilityai/stablelm-3b-4e1t -2.515) sit within about two margin-widths. Report the wild-scan hit count as a function of threshold from -2.4 to -3.0 in steps of 0.1, give the smallest threshold shift producing a first false positive, and state plainly that the threshold is panel-fitted and never validated out of panel. (b) Report E_1 at three bands (0.25L–0.75L primary, full stack, 0.4L–0.6L) and state whether the paired difference and the 'complementary failure modes' conclusion are invariant. Both are re-analysis of quantities already computed; if a conclusion moves, say so.

  H6 (POSITIONING AND PRACTITIONER-FACING FRAMING). (i) Cite Abliterlitics (github.com/dreamfast/abliterlitics, reports at abliterlitics.dev) in the community-practice paragraph: an open-source abliteration-forensics toolkit whose Weight Analysis axis does SVD, effective rank, energy spectra, edit-vector fingerprints, subspace alignment, low-rank reconstruction and per-layer magnitude profiles, and which publishes side-by-side Heretic vs Huihui vs HauhauCS comparisons on shared bases. It REQUIRES a base plus variants in a comparison directory, so it is parent-requiring and sharpens rather than blunts the parent-free claim — and its published cross-technique fingerprints are directly usable EXTERNAL support for the uniform-vs-depth-weighted distinction of H1. (ii) Keep the existing corrections: arXiv:2604.08844 (Paul) is cited at point of use with its declared confound (the steering arm produced incoherent text, GPT-4o 0/300 harmful, so its AUC 0.00 cross-method precedent is confounded); OBLITERATUS's certification consumes ACTIVATIONS not weights, so it is parent-free but not prompt-free and audits a self-performed edit — our novelty claim is stronger, not weaker; reverse-abliterate is the software instantiation of the 50.5% string-match baseline. (iii) Add a cost annotation (prompts required, forward passes, wall-clock) to the behavioural table so the reader sees the falsifier is about MARGINAL VALUE OVER A CHEAPER INSTRUMENT, not about whether interior observables carry signal — A19 reaches rho +0.763 [+0.592, +0.864] member / +0.800 lineage, comparable to B01 and better than B09. The practitioner-facing sentence: interior observables ARE predictive of harmful-refusal rate, but they do not beat a 40-prompt greedy refusal rate, which is already the cheapest thing anyone would run.

  H7 (REPORTING FIDELITY, cheap and mandatory in a paper whose argument IS measurement discipline). Generate the Panel and scan counts from scan.jsonl rather than transcribing them, printing the control/non-control split; fix the 65-vs-81 UNRESOLVED discrepancy in whichever artifact is stale; keep [min, max] for EVERY class in the weights table (base W01 max 1.992 overlaps abliterated min 1.438; W02 base max 1.000 equals the abliterated median); name allenai/OLMo-1B-hf (-2.6652) as the nearest non-abliterated neighbour and flag that boundary-adjacent checkpoints come from single-member families (olmo, gpt_neox); keep W03 at 256 directions; disambiguate the positive control (Qwen/Qwen3-0.6B instruct, unedited W01 0.6239, vs Base 0.6281) and reword so 4.869 and -4.82 are not adjacent; reserve 'pre-registered' for what metric_spec.py actually stamps and publish the claim-to-artifact-line mapping table.

  WHAT IS RETIRED. The 53-metric battery is not rebuilt. alpha_50 and the steering-price family remain retired as metrics (NOT_A_TRIAGE_SCORE, R = 0.73, perm p = 0.76, sign reverses across lineages), surviving as the S4 negative plus the scorer-artefact finding — which T8 now corroborates a second time. The early-warning-signal / critical-slowing-down arm remains retired entirely. 'Leave-one-architecture-family-out' is retired as the generalisation control; 'leave-one-uploader-out' is DEMOTED to a secondary control, replaced as primary by leave-one-RECIPE-CLASS-out. The framing 'safety behaviour is legible from the model alone' stays retired.

  CONFIDENCE. Mixed, and the asymmetry has sharpened. HIGH that a uniform, complete, all-layer directional edit leaves a cheap parent-free structural certificate: independent reimplementation to 9.9e-6, injected positive control, held-out lineage split, 8/8 and 12/12 controls, 0 false positives on the undeclared scan, survival of 200 LoRA steps and of a single-matrix adversarial patch. HIGH — and this is the change this iteration forces — that the boundary is UNIFORMITY, not architecture and not uploader: three independent measurements (f* = 1.00, the middle-50% invisibility, the depth-weighted-kernel misses) now say the same thing, and the synthetic unit test supplies the mechanism. MODERATE that the 0/160 specificity survives an eligibility filter, since 44 of the 160 are degenerate stubs on which the statistic is not defined. LOW that the flag survives ordinary deployment: an int4 round-trip erases it, though the operational consequence at hub scale is UNRESOLVED rather than a clean read, and a dequantize-then-score remedy is untested and cheap. HIGH that graded behavioural safety is not better read from the interior than from a 40-prompt greedy refusal rate at this panel size, and HIGH that the bound is |drho| ~ 0.32 at 19 lineages rather than zero. The most likely outcome of iteration 4 is that the recipe relabelling converts the paper's central weakness into its central mechanism, the eligibility filter leaves specificity intact on a smaller honest denominator, and dequantization restores the scar — yielding: 'a free, prompt-free certificate that a checkpoint carries a UNIFORM, unlaundered, all-layer directional edit, with a measured uniformity boundary and a measured, partially remediable evasion surface'. Smaller than iteration 1 hoped, and the only version of the claim the evidence actually licenses.
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
  Same frame; the supported half is re-grounded from an uploader effect to a measured uniformity requirement.
_confidence_delta: unchanged
_key_changes:
- >-
  RE-GROUNDED CLAIM A's boundary: the four new-uploader misses are a RECIPE effect, not an uploader effect — the artifact's
  own stored card evidence names Heretic v1.1.0 (direction_index 17.89, max_weight 0.84) and mlabonne's Gaussian depth kernel,
  both explicitly non-uniform, while arm1_real.jsonl labelled them global_diff_in_means / mechanically_different=false.
- >-
  UNIFIED three previously separate findings into one mechanism: f*=1.00 layer-fraction threshold, the middle-50% edit that
  un-censors fully (0.45->0.00) while W05 moves 0.001, and the depth-weighted-kernel misses are the same fact — W05 requires
  uniform, complete annihilation in every layer; the pooled Gram makes it a threshold, not a ramp (4/12 edited => v1 is no
  longer the injected direction, W02=0).
- >-
  DELETED the '>=14.9B constraint' limitation as refuted by our own prior-art artifact (public MPOA/Heretic/OBLITERATUS at
  4,022,468,096 params on the panel's Qwen3-4B family) and made leave-one-RECIPE-CLASS-out the primary generalisation control,
  demoting leave-one-uploader-out to secondary; ORBA Householder named as sharpest falsification target.
- >-
  REQUIRED an eligibility rule before the 0/160 deployment number: 44 of 160 scored repos are degenerate (~30 hidden_size=8/n_layers=2
  CI fixtures, 3 single-layer EAGLE3 draft heads, sub-30MB toys) plus a 14B MLX-4bit admission; report the filtered denominator
  as primary, raw 0/160 as secondary, plus a model_type x count table and a stated layer-count floor.
- >-
  SPLIT the quantization finding into (a) dequantized int4 scores clean while un-censored and (b) in the scan pipeline a quantized
  upload is UNRESOLVED, not a false negative; added the cheap dequantize-to-fp16-then-rescore test that could shrink the limitation
  to 'requires dequantization before scoring'; corrected 'for free' (ppl 26.25 -> 37.7, +43%).
- >-
  ADDED uncertainty to the laundering ladder: 40-item binomial SE ~0.075 makes the quoted -0.004 evasion cost and the 0.135-vs-0.162
  int4 comparison unresolvable; crossings must be restated as orderings with Wilson intervals, and a SECOND root (in-house
  depth-weighted Heretic-style edit + a Llama-3.2-1B host) is required to turn point thresholds into ranges.
- >-
  ADDED threshold-brittleness reporting (scan hits as a function of threshold -2.4..-3.0, smallest shift producing a first
  false positive, explicit statement that -2.7415 is panel-fitted and never validated out of panel) and an E_1 band-sensitivity
  check at 0.25-0.75L / full stack / 0.4-0.6L.
- >-
  CARRIED FORWARD the quantitative negative: minimum detectable |drho|=0.32 at 19 lineages, falsifier could have failed, B08/B01
  beat B09 with selection optimism +0.182, r_xx=0.968 so not attenuation, BLACKBOX_WINS invariant at three depths with the
  near-win A19 +0.770 vs +0.766 shown to be paired-difference null (+0.0045 [-0.225,+0.260]).
- >-
  ADDED a cost annotation (prompts / forward passes / wall-clock) to the behavioural table and the practitioner-facing conclusion:
  interior observables ARE predictive (A19 rho +0.763 member, +0.800 lineage) but do not beat a 40-prompt greedy refusal rate
  — the falsifier is about marginal value over a cheaper instrument.
- >-
  ADDED Abliterlitics as required community prior art (parent-requiring weight-spectral abliteration forensics with published
  Heretic vs Huihui cross-technique fingerprints) — it sharpens the parent-free claim and independently supports the uniform-vs-depth-weighted
  distinction.
- >-
  KEPT the self-audit results as first-class: four draft 'correlations' are paired differences on a 26-member chatml subset,
  W05's AUROC 1.000 is oriented (raw 0.000), the margin is 0.0763, '-2.742' is the abliterated maximum not minimum, W03 uses
  256 directions, and 12 'pre-registered' claims reduce to 4 SUPPORTED / 2 PLAN-ONLY / 6 UNSUPPORTED.
- >-
  ADDED the construction-time dissociation as the paper's sharpest mechanistic statement: held-out AUROC saturates (11 layers
  >=0.997, 4 tied at 1.000) and two directions indistinguishable on detection differ twofold in un-censoring (0.333 vs 0.162),
  so direction selection must be behavioural.
relation_type: evolution
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: experiment_iter4_dir1
type: experiment
objective: >-
  Establish, as a measured and pre-signed claim, that W05's boundary is UNIFORMITY of the edit - not architecture, not uploader
  - by scoring real public sub-4.2B checkpoints from mechanically different recipes and in-house reimplementations of the
  two recipes with no public sub-4.2B instance, with leave-one-RECIPE-CLASS-out as the primary generalisation control.
approach: >-
  Reuse the vendored, gate-passing wstats.py reimplementation (reproduces archived W05 to 9.9e-6; write it as an explicit
  reproduction gate again on >=5 archived abliterated and >=5 non-abliterated members before anything else, and report deltas).
  WRITE THE SIGNED PREDICTION TABLE FIRST, to a stamped file, before any new checkpoint is downloaded: uniform-kernel recipes
  (plain all-layer rank-one projection, norm-preserving/MPOA, rank-k / OBLITERATUS rank-k presets, Gabliteration) => DETECTED
  (W05 <= -2.7415); depth-weighted or sub-unit-weight kernels (mlabonne v2 Gaussian, Heretic per-component optimised with
  float direction index and weights != 1) => MISSED; Householder reflections (ORBA, H = I - 2uu^T, geodesic lambda = 1) =>
  MISSED, and for a DIFFERENT reason (a reflection preserves ||w|| exactly and leaves no approximate null direction, so v1
  should not align with u at all - report |cos(v1,u)| explicitly as the mechanism check, predicting near-zero for ORBA versus
  1.000 for projection). ARM A, REAL PUBLIC RECIPE-DIVERSE CHECKPOINTS. Our own prior-art dossier records public MPOA, Heretic
  and OBLITERATUS checkpoints at 4,022,468,096 params on the panel's own Qwen3-4B family; the edit_manifest block of the dataset
  dependency enumerates 513 edited sub-4.2B repos across 189 uploaders with verbatim recipe_evidence spans and 6 populated
  recipe classes. Select, verify from card/config evidence (never repo name), and measure W01-W05 on at least 8, target 14,
  checkpoints spanning at least four recipe classes and including: the two already-measured Heretic checkpoints (MagicalAlchemist/Qwen3-1.7B-Magic_decensored,
  prithivMLmods/VibeThinker-3B-heretic_decensored) now correctly labelled, mlabonne/Qwen3-0.6B-abliterated (Gaussian kernel),
  BennyDaBall/Qwen3-4b-Z-Image-Turbo-AbliteratedV1, and public MPOA / OBLITERATUS / Gabliteration instances at <=4.2B. For
  every row store the recipe_class re-derived from the card with the quoted evidence span, any published kernel parameters
  (Heretic's direction_index, per-component max_weight; mlabonne's spread and peak layer), and the parent where resolvable
  so E_1 can be computed as the incomplete-annihilation cross-check (the reviewer's mechanism: E_1 ~ 0.995-0.997 means the
  per-matrix delta is still near rank one while the annihilation is incomplete in some layers - report per-LAYER e_W(v1) profiles
  for these checkpoints, which is the direct visual proof that the suppression has exceptions). ARM B, IN-HOUSE RECIPE REIMPLEMENTATIONS
  on Qwen3-1.7B-Instruct and Llama-3.2-1B-Instruct, each with a fluency screen (within-response distinct-3, WikiText perplexity)
  and a greedy harmful-refusal rate on the frozen 40-item core so 'the edit worked' and 'the edit is visible' stay separable:
  (i) ORBA Householder reflection with the geodesic lambda = 1 variant; (ii) mlabonne v2 Gaussian depth kernel w_l ~ N(peak,
  spread) sweeping spread so uniformity becomes a CONTINUUM - the single most informative curve in this artifact, since it
  interpolates between the detected uniform edit and the missed depth-weighted one and should locate a threshold, not a ramp;
  (iii) a Heretic-style per-component kernel with distinct attention/MLP weights and at least one weight > 1 (over-subtraction
  / sign flip); (iv) sub-unit-weight uniform edits w = {0.5, 0.7, 0.85, 1.0} to separate INCOMPLETE-but-uniform from COMPLETE-but-non-uniform,
  which the current evidence conflates. ANALYSIS. Recompute AUROC with RECIPE_CLASS as the primary grouping variable (leave-one-recipe-class-out:
  fit the threshold on all classes but one, evaluate on the held-out class) and uploader as secondary, over the archived 36
  negatives plus the eligible new negatives; report each prediction as CONFIRMED / REFUTED against the stamped table, and
  report the confusion honestly if a uniform recipe is missed or a depth-weighted one is caught (either would be the headline).
  Also emit, for every measured checkpoint, the per-layer e_W(v1) profile and a scalar UNIFORMITY index (e.g. the interquartile
  spread or max/min ratio of per-layer suppressed energy) so the mechanism claim is quantitative rather than narrative, and
  the profiles are directly reusable by the windowed-statistic artifact and by the paper's figures. IMPLEMENTATION NOTES that
  cost days if rediscovered: use svdvals for square attention matrices (sqrt(eigvalsh(WW^T)) squares the condition number);
  accumulate the Gram in float64 (float32 drifts W01 up to 0.048 exactly where lambda_min sits at the noise floor); some tokenizers
  ship no chat_template under transformers 5.x - substitute standard ChatML and record it; base models need the PLAIN renderer;
  download sequentially and delete snapshots after measuring; report which tier completed rather than promising a target.
  ARCHIVE ACCESS NOTE: the iteration-3 experiment trees are not passed as dependencies (an experiment may depend only on datasets
  and research), so read them directly from their workspace paths under run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_art/
  — gen_art_experiment_1 supplies wstats.py, the vendored W01-W05 reimplementation, results/arm1_real.jsonl, results/arm2.json
  and results/long_table_depth.jsonl; gen_art_experiment_2 supplies results/root_recipe.json (rebuilds the abliteration root
  in ~9 s, 311/311 tensors bit-identical), results/ladder.jsonl, results/scan.jsonl and scan_enumeration.json. Re-run the
  reproduction gate against the archived values before using any of it, and report the deltas.
depends_on:
- id: art_8OlSrcw-hzgO
  label: dataset
  relation_type:
  relation_rationale:
- id: art_sHF0cggp2IvT
  label: recipe spec
  relation_type:
  relation_rationale:
- id: art_CKWQh2cOQLLQ
  label: prompts
  relation_type:
  relation_rationale:
- id: art_lMTPOpnFwKnw
  label: prior art
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

--- Dependency 1 ---
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

--- Dependency 2 ---
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

--- Dependency 3 ---
id: art_sHF0cggp2IvT
type: research
title: Who Else Detects Edited Safety Models
summary: >-
  Four-part prior-art and taxonomy dossier for the parent-free weights-only abliteration detector (Claim A). (A) arXiv:2604.08844
  (Paul) extracted from full text: two of its five features are FORMULA-IDENTICAL to our W06-W09 (stable rank, singular-value
  entropy with the same sigma-hat normalisation) and must be cited at point of use; its MOST informative feature (cosine of
  top-k left singular vectors to a healthy-adapter centroid, 10x shape / 30x magnitude coefficients) is parent- AND reference-requiring,
  so W01-W05 have NO counterpart. Numbers verified with two corrections: rho>=0.956 is the MINIMUM of three ordinal values
  (0.976/1.000/0.956); rho=0.72 is Spearman on N=24 with NO CI reported. Cross-method AUC 0.00 confirmed verbatim (n_bootstrap=972,
  CI [0.00,0.00], trained on 10 healthy + 14 DPO, tested on 6+4 steering, score is a fitted probability, NO fix attempted)
  -- but the paper DECLARES ITS OWN CONFOUND: the steering arm generated incoherent text at every intensity (GPT-4o 0/300
  harmful), so the precedent is confounded and must be cited that way. (B) OBLITERATUS's spectral certification READ IN FULL
  FROM SOURCE and the plan's premise INVERTS: it consumes ACTIVATIONS (harmful/harmless post-edit), not weights -- parent-free
  but NOT prompt-free, and it audits a self-performed edit rather than detecting unknown checkpoints. Our novelty claim gets
  STRONGER. Its documented 'RED at 0% refusal' calibration failure is transcribed verbatim from three mirrors and is an independent
  mirror of our S2. Dated: first public 2026-03-04. (C) Eight recipes with reimplementation-grade equations (rank-one projection,
  mlabonne Gaussian kernel, Heretic per-component optimised kernel with FLOAT direction index and weights >1 i.e. sign flip,
  MPOA exact row-norm-preserving four-step, ORBA Householder + geodesic lambda=1, Gabliteration ridge rank-k, OBLITERATUS
  rank-k presets, SFT). PLAN WAS WRONG on availability: MPOA, Heretic and OBLITERATUS ALL have public sub-4.2B checkpoints
  at 4,022,468,096 params on the panel's own Qwen3-4B family; only ORBA is empty (7 repos, all 12.187B) and must be reimplemented.
  FIFTH FINDING, unasked: the iteration-2 positive set ALREADY contains a second recipe -- the gabliterated member is a Gabliteration
  and scores at HALF the margin (W01 2.237 vs 4.16-4.82), so H1 is half-answered as graded loss not collapse; the AUROC 1.000
  rests on a 0.077 log-margin; W02=1.00 on four pre-2023 BASE models. (D) Coslett resolved as ADJACENT (activation-geometry
  fingerprint against a claimed identity, per the only reachable characterisation); Zenodo record/DOI/REST API all 403 and
  the publisher host is unreachable, so risk drops LARGE -> SMALL-but-open. Two new works: arXiv:2602.15195 (weights-only
  but adapter-delta + supervised calibration, our exact size class, currently uncited) and reverse-abliterate (the only shipped
  parent-free detector -- pure filename/metadata scanning, no spectral statistic). Ships 12 numbered corrections including
  a FACTUAL ERROR in the current hypothesis, a signed W05 prediction table with Householder-ORBA as the sharpest falsification
  target, a 5-model shortlist, and a 14-entry must-cite list.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
out_dependency_files:
  file_list:
  - research_out.json

--- Dependency 4 ---
id: art_8OlSrcw-hzgO
type: dataset
title: Who Edited This Model, and How
summary: |-
  Ships ONE schema-validated full_data_out.json with five datasets (7,381 examples, 16.5 MiB) in three blocks. DATA ONLY: no weights downloaded, no forward passes, no training, no W01-W05, no AUROC, $0.00 OpenRouter spend. Built offline by `uv run data.py` from temp/datasets/ + results/ (48 deps pinned exactly in pyproject.toml).

  BLOCK 1 `edit_manifest` (672 rows = 513 edited + 159 parents). Harvested from 61 Hub sweeps (20 search terms, 20 uploaders, 20 architectures, 1 global top-downloads) over 20,313 enumerated repos. Spans **189 distinct uploaders** against the plan's floor of 5 -- iteration 2's 8 positives came from only TWO uploaders, so this directly removes that confound. **6 of 7** recipe classes populated: R1_GLOBAL_RANK1_DIM 78, R2_NORM_PRESERVING_PROJECTED 20, R3_MULTIDIRECTION_SVD 26, R4_PARTIAL_LAYER_OR_PER_HEAD 235, R6_BEHAVIOURAL_SFT_UNCENSORED 19, R7_MERGE_OF_ABLITERATED 15, UNKNOWN 120. **388 complete parent-child pairs** for the H3 head-to-head; all 8 iteration-2 members present and flagged `is_iter2_class_member`; 1,536 over-ceiling near-misses recorded separately; every row `status=ok`.

  THREE NUMBERS THAT SHOULD DRIVE THE PAPER. (i) **UNKNOWN = 23.4%** of edited rows: nearly a quarter of self-declared edited checkpoints name no mechanism, which is the ceiling on Hub recipe provenance. (ii) **repo_id_contains_abliteration_string = 50.5%** (259/513): a plain regex on the repo id alone already solves HALF the detection task, so that -- not chance -- is the baseline any detector must beat. This is the reviewer's previously unmeasured point, now quantified. (iii) **R5_SPECTRAL_CASCADE_DCT is EMPTY**, and that is a finding, not a gap: the OBLITERATUS README we fetched contains ZERO occurrences of 'spectral', 'frequency', 'Fourier' or 'DCT' (its profiles are basic/advanced/aggressive/surgical/optimized/inverted over diff-in-means, SVD, whitened SVD). Any H1 arm needing a frequency-domain recipe is UNRUNNABLE at this scale.

  BLOCK 2, three laundering corpora. 2a `sft_benign` 3,370 English single-turn pairs from OpenAssistant/oasst1 (Apache-2.0, sha fdf72ae0), 627 safety-topic pairs and 6,695 duplicate instructions dropped. 2b `fluency_wikitext` 1,000 paragraphs from Salesforce/wikitext wikitext-2-raw-v1 test (sha b08601e0), median 148 GPT-2 tokens, 163,496 total; the @-@ artifact is documented, not silently carried. 2c `heldout_benign_prompts` 200 prompts from databricks-dolly-15k (sha bdd27f4d) -- a DIFFERENT repo from 2a, then exact dedupe (1 dropped) and 5-gram Jaccard >= 0.5 (0 dropped); measured max Jaccard vs any 2a instruction is **0.273**. NC sources excluded throughout (alpaca, no_robots rejected).

  BLOCK 3 `hub_scan_pool` 2,139 metadata-only rows, all strata floors beaten: 407 declared / 1,105 non-declaring chat / 627 non-declaring base. Ranked by `scan_rank` (undeclared chat by descending downloads first) with `cumulative_bytes`, so a scan stopping at rank k has a stateable coverage and a cost in GB; 7.3 TB total with per-decile cumulative gigabytes.

  INTEGRITY, ALL VERIFIED ON THE SHIPPED FILE: 0 rows with a missing or 'main' sha; 0 rows missing a param count; 0 rows above either ceiling; **482/482 recipe_evidence spans verified as verbatim substrings of the cards they cite (0 fabricated)**; 482/482 carry an evidence_url; 0 parent rows wrongly carrying a recipe_class; 2a leaks no safety terms and has no duplicates.

  TWO BUG CLASSES FOUND AND FIXED, both consequential downstream. (1) A three-seed 10-row hand-check (27/30 survived, failures and objections recorded in coverage.block_1.hand_check) exposed four labeller defects, including 'trained' matching inside `from_pretrained(...)` in a usage snippet and corpus-sense 'unfiltered' labelling a pedagogy study as an uncensoring fine-tune. (2) **The Hub's safetensors index is not always right**: samuelcardillo/Qwen3-Coder-Next-Opus-4.6-Reasoning-Distilled reports 6,208,256 parameters while shipping 159 GB of shards, and two 35B checkpoints report 664,944. Taking it at face value silently admits 32-35B models into a sub-4B pool. The ceiling is now enforced TWICE -- once from the index, once from on-disk safetensors bytes divided by the repo's widest declared dtype -- which rejected 25 such rows. Any downstream artifact resolving parameter counts from the Hub should apply the same cross-check.

  A bare 'this is an abliterated version' is deliberately labelled UNKNOWN/ambiguous rather than folded into R1, which would have inflated R1 until the class meant nothing. Ten HF dataset candidates were downloaded and evaluated; three are shipped and each of the seven other verdicts is recorded in metadata.dataset_selection (GAIR/lima is gated; tulu-3-sft-mixture is partly non-commercial; oasst2/oasst_top1/guanaco are not independent of 2a and guanaco is multilingual).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_art/gen_art_dataset_1
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
</dependencies>

<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results
</artifact_executor_scope>

<artifact_planning_rules>
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for experiment artifacts:
  - gpu: 1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models (fallback: GPUs cheap→expensive: 2000 Ada → A4000 → 4000 Ada → L4 → 4090 → 5090)
  - cpu_heavy: 4 vCPUs, 32GB RAM — large datasets, memory-intensive processing (fallback: CPUs cheap→expensive, then GPU hosts cheap→expensive (all ≥32GB RAM))

Set runpod_compute_profile to one of these exact tier names.
</compute_profiles>
GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
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
  "description": "Plan for an EXPERIMENT artifact.",
  "properties": {
    "title": {
      "description": "Plan title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_light",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu', 'cpu_heavy', 'cpu_light'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "implementation_pseudocode": {
      "description": "High-level pseudocode for the experiment implementation",
      "title": "Implementation Pseudocode",
      "type": "string"
    },
    "fallback_plan": {
      "description": "What to do if the primary approach fails - alternative methods, simplified versions",
      "title": "Fallback Plan",
      "type": "string"
    },
    "testing_plan": {
      "description": "How to validate the experiment works: start with small/fast tests, look for confirmation signals before running full-scale experiments",
      "title": "Testing Plan",
      "type": "string"
    }
  },
  "required": [
    "title",
    "implementation_pseudocode",
    "fallback_plan",
    "testing_plan"
  ],
  "title": "ExperimentPlan",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-13 23:49:42 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```
