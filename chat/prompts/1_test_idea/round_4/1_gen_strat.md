# gen_strat_1 — test_idea

> Phase: `invention_loop` · round 4 · `gen_strat`
> Run: `iter1_33370088803c` — Catching Edited Safety Models by Reading Weights in Sliding Windows
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_strat_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-13 23:44:08 UTC

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
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for study design, proper baselines, and the evaluation/validity norms this field demands.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<iteration_status>
Current iteration: 4 of 5
Remaining (including this one): 2
</iteration_status>

<previous_strategies>
Strategies from the PREVIOUS iteration. You can CONTINUE these directions,
ADAPT based on what worked and what didn't in the artifacts produced, or PIVOT if results suggest a better path.

--- Strategy 1 ---
kind: strategy
id: gen_strat_1_idx1
title: Find where the weight fingerprint breaks
objective: >-
  Convert iteration 2's two results into claims that survive a hostile reviewer, by measuring their SCOPE instead of restating
  them. The positive (a parent-free spectral scar of abliteration: W05 AUROC 1.000, 0 prompts, 0 forward passes, 11.4 s) is
  currently established on 8 checkpoints from 2 uploaders running ONE recipe (global all-layer diff-in-means projection),
  with every positive solved for free by a repository-name string match, and with the parent-requiring incumbent E_1 described
  but never computed. The negative (for graded behavioural safety no interior metric beats greedy refusal rate B09, rho +0.766)
  is currently a verdict from an underpowered paired bootstrap against a best-of-11 comparator, on judge-derived rates whose
  reliability was never estimated, at a depth chosen by a d'-tiebreak on a 22-layer AUROC plateau, and with ZERO of the headline
  AUROCs, Spearmans, bootstraps or paired differences computed inside any versioned artifact. This iteration delivers four
  things and retires the battery: (1) the true RECIPE-CLASS scope of the scar, tested against mechanically different abliteration
  toolchains and reported with leave-one-UPLOADER-out beside leave-one-family-out, plus the first head-to-head against E_1
  on the matched sibling subset where the parent exists; (2) the deployment premise instantiated - a laundering ladder (LoRA-SFT,
  50/50 parent merge, int8/int4 round-trip, added-back random rank-one) reporting W01-W05 AND harmful-refusal rate at every
  stage so the ORDER OF THE TWO DEATHS is measured, plus a Hub scan of undeclared checkpoints; (3) analysis.py as a first-class
  deliverable that emits every statistic in the paper with seed, B, resampling scheme and tie-handling printed, together with
  a power simulation, a pre-specified comparator, attenuation correction and a depth-invariance check that together turn the
  negative from a verdict into a measurement; (4) honest positioning against two prior works that were missed, one of which
  (arXiv:2604.08844) both overlaps our spectral feature set and independently documents the exact cross-method collapse we
  are testing for. The novel contribution being built toward is the first measured, held-out-validated characterisation of
  PARENT-FREE spectral abliteration detection, complete with its recipe-class boundary, its evasion boundary and its calibration
  failure - a smaller claim than iteration 1 hoped for and one that can actually be defended.
rationale: >-
  Every MAJOR reviewer critique is a scope or discipline defect, not a data defect, and each has a cheap decisive fix that
  fits inside this iteration. The toolchain confound is the sharpest: architecture is not what W05 keys on, the edit recipe
  is, our own band-limited control already proves blindness to non-global edits, and arXiv:2604.08844 has ALREADY published
  this exact failure mode once (a spectral classifier trained on one editing method scores every out-of-method adapter below
  every in-method one, AUC 0.00). Finding the collapse is therefore a confirmation, not finding it is a genuine surprise,
  and either way the sentence we can defend improves. The same logic makes the laundering arm mandatory rather than optional:
  W05 is a MINIMUM over layers and so is by construction the most fragile of the five statistics to anything touching a single
  layer, which means an evasion boundary certainly exists and the only question is whether it sits before or after the un-censoring
  dies. That is a measurable question with in-house machinery we already built (the rank-one and band-limited controls), and
  the answer is publishable in both directions. The E_1 head-to-head is nearly free - pure tensor arithmetic on sibling pairs
  we have already downloaded - and it converts the paper's central trade from an assertion into a number. On the negative
  side, the reviewer's power objection is correct and fatal if unanswered: at 18 lineages a paired-rho CI half-width near
  0.25-0.5 means the falsifier could barely have failed, so 'the interior buys nothing' and 'we cannot tell' are currently
  indistinguishable; a two-line simulation settles which sentence we own, and a pre-specified comparator (B01, which has a
  published prior) removes the best-of-11 selection advantage that currently makes the headline awkward given A02 numerically
  leads B09 at both aggregation units. The reliability and depth repairs are the same move applied twice - propagate a known
  source of noise or arbitrariness into the reported number instead of leaving it as an unquantified caveat. And the missing
  analysis.py is existential for a paper whose entire credibility argument IS measurement discipline: no reviewer will accept
  headline numbers that exist nowhere in the artifact, and the same file fixes the 'pre-registered' overreach by forcing every
  claimed rule to point at a stamped line. The five artifacts split cleanly along what each executor is good at - two weights-heavy
  experiments that download and compute, one pure re-analysis evaluation that ships the statistics code, one literature pass
  that cannot be run in code, and one provenance-grade dataset that both makes the recipe taxonomy citable and stocks iterations
  4-5 with the candidate pool a bigger scope test will need. None blocks another; each is reportable alone.
artifact_directions:
- id: research_iter3_dir1
  type: research
  objective: >-
    Close the two uncited prior works the reviewer named, establish the mechanical taxonomy of 2026 abliteration recipes with
    enough precision to reimplement each one, and return a defensible novelty sentence for the parent-free weights-only arm.
  approach: >-
    Four questions, answered from primary full text with exact numbers and section anchors; use scholarly search plus fetch_grep
    on PDFs and on repository/tool documentation. (A) arXiv:2604.08844 (Paul, 'Spectral Geometry of LoRA Adapters Encodes
    Training Objective and Predicts Harmful Compliance'). Extract verbatim: the exact per-layer feature list (norms, stable
    rank, singular-value entropy, effective rank, singular-vector cosine to a healthy centroid) and map it item-by-item onto
    our W06-W16; the manufacture protocol for the 38 adapters (base model, objectives, dose ladder if any); AUC 1.00 for binary
    drift and for all six pairwise objective comparisons; rho >= 0.956 ordinal severity; rho = 0.72 against HEx-PHI harmful
    compliance; and CRITICALLY the cross-method result reported as AUC 0.00 - transcribe the exact experimental setup that
    produced it, since it is our closest published precedent for the toolchain collapse we are testing. Write the three-axis
    distinction paragraph (parent-free vs delta-based; real community checkpoints vs manufactured adapters; edit-detection
    vs behaviour-prediction) AND the explanation of why our behaviourally-uncensored members show none of its behavioural
    signal. Its rho = 0.72 is a direct counterweight to any sentence of ours claiming weight geometry cannot carry behavioural
    signal - find every such sentence in the current draft and supply a corrected wording. (B) OBLITERATUS and community 'spectral
    certification'. Locate the toolkit (repo, docs, release notes, any write-up), and document verbatim: what its parent-free
    certification step computes from an abliterated checkpoint's own weights, what 'complete' vs 'incomplete' means operationally,
    and the documented cases where certification reads incomplete while practical refusal rate is 0%. This is prior community
    practice for the operation we claim as new and it independently mirrors our 'the ranking transfers, the calibration does
    not' finding; return the reframed novelty sentence. (C) RECIPE TAXONOMY, the input the scope experiment needs. For each
    of at least six mechanically distinct abliteration/uncensoring recipes - (i) global all-layer diff-in-means rank-one projection
    (huihui-ai / Josiefied class, our 8 positives), (ii) mlabonne's published notebook recipe, (iii) norm-preserving / projected
    abliteration (grimjim class), (iv) ORBA orthogonal-reflection bounded ablation, (v) multi-direction / SVD-subspace ablation,
    (vi) per-head or per-module surgery, (vii) DCT / spectral-cascade modes, (viii) behavioural uncensoring by ordinary SFT
    - write the EXACT weight update in equations, state which matrices it touches (o_proj / down_proj / embed_tokens / per-head
    slices), whether it is norm-preserving, whether it is rank-one, and whether it touches all layers. Then name concrete
    PUBLIC checkpoints at <= 4.2B parameters produced by each recipe, with repository id, uploader and the card or config
    evidence proving the recipe; flag which recipes have NO public sub-4B checkpoint, because those must be reimplemented
    in-house. Also state which of these recipes would and would not produce a shared approximate null direction across the
    whole write ensemble - a mechanistic prediction our experiment can then test. (D) Verify whether any published work computes
    a spectral or geometric abliteration/edit detector from a single checkpoint WITHOUT the parent, beyond OBLITERATUS's certification,
    and re-check the one source characterised in arXiv:2607.01854 that our previous draft could not reach (HTTP 403) - it
    is currently named as the largest residual risk to the novelty claim, so either resolve it or restate the risk precisely.
    Deliverable: a dossier with the reimplementable recipe equations, the two required citation paragraphs written out, a
    candidate-checkpoint table, and a list of numbered corrections to the current draft's wording.
  depends_on:
  - id: art_lMTPOpnFwKnw
    label: extends
    relation_type:
    relation_rationale:
- id: dataset_iter3_dir2
  type: dataset
  objective: >-
    Ship a provenance-grade, recipe-labelled checkpoint manifest that makes the scope claim citable, plus the two auxiliary
    corpora the laundering arm needs and the enumerated sub-4B Hub pool that a full undeclared-positive scan will draw from
    in later iterations.
  approach: >-
    Three row blocks in one schema-validated file, every row carrying pinned repo id, revision sha, resolved parameter count
    from the Hub API (never from on-disk bytes - the previous iteration found that double-counts repos shipping both .safetensors
    and .bin), file list with sizes, and an evidence field holding a <= 300-char quoted snippet from the card, config or linked
    code that justifies its label. (1) RECIPE-LABELLED EDIT MANIFEST, the headline block. Enumerate at least 25 sub-4.2B checkpoints
    that claim to be abliterated / uncensored / decensored / gabliterated / orthogonalised, spanning at least five DISTINCT
    uploaders and, where the card permits it, at least four distinct recipe classes (global rank-one diff-in-means; norm-preserving
    or projected; multi-direction / SVD subspace; per-head or partial-layer; behavioural SFT uncensoring). For each, record:
    uploader, declared parent, declared recipe with the quoted evidence, whether the recipe is inferable at all (a large fraction
    will be UNDECLARED - report that count as a first-class number, it is the honest measure of how much provenance a hub
    actually carries), and a recipe_class field with an explicit UNKNOWN value rather than a guess. Include the 8 members
    of the current abliterated class so the manifest is a superset, and mark them. Also record, for every row, whether the
    repository id contains an abliteration string - this quantifies exactly how much of the detection task a string match
    solves for free, which the reviewer correctly identified as unmeasured. (2) LAUNDERING CORPORA. A benign instruction-tuning
    split suitable for a 200-step LoRA SFT (a few thousand instruction/response pairs from a permissively licensed, non-safety-related
    source; record the license, and prefer sources without the CC-BY-NC constraint that limits two of our existing blocks),
    plus a WikiText-derived fluency evaluation split for perplexity screening of laundered checkpoints, plus a small held-out
    benign prompt set disjoint from the SFT data. (3) HUB SCAN POOL. Enumerate several hundred sub-4B text-generation checkpoints
    from the Hub with metadata only (no weights): repo id, downloads, parameter count, architecture family, full card text
    hash, and a boolean for whether the card or repo id declares abliteration/uncensoring. Stratify so the pool contains both
    declared and non-declaring chat models, and report the size distribution so a later scan can be costed in gigabytes rather
    than guessed. Ship the pool as a ranked scan order (most-downloaded undeclared chat models first) so the scan is reproducible
    and its coverage is stateable. Report honest coverage counts throughout, and validate the file against the standard dataset
    schema with full/mini/preview variants.
  depends_on:
  - id: art_lMTPOpnFwKnw
    label: guidance
    relation_type:
    relation_rationale:
- id: experiment_iter3_dir3
  type: experiment
  objective: >-
    Measure the true scope of BOTH iteration-2 results: the recipe-class boundary of the parent-free scar (with leave-one-uploader-out
    and the first E_1 head-to-head), and the depth-invariance of the falsifier that produced the negative.
  approach: >-
    Three arms, all on tensors, sharing one download budget. Re-implement the weights statistics from the published definitions
    rather than importing them, and GATE the reimplementation before anything else: form A = sum over residual-write matrices
    (attention o_proj, MLP down_proj) of W W^T / ||W||_F^2, take v1 = eigenvector of the minimum eigenvalue, define e_W(u)
    = ||u^T W||^2 / (||W||_F^2 / d), and compute W01 = log10(median(lam)/lam_1), W02 = fraction of write matrices with e_W(v1)
    < 0.1, W03 = log10(q05(e_W(u_rand)) / mean e_W(v1)) over 256 random directions (256, not 64 - the previous text was wrong),
    W04 = log10(lam_2/lam_1), W05 = log10(min_W e_W(v1)). REPRODUCTION GATE: recompute on at least five of the eight original
    abliterated members and five non-abliterated ones and require agreement with the archived values - weakest abliterated
    W05 = -2.742 (huihui-ai/Qwen2.5-0.5B-Instruct-abliterated), next-weakest -3.522, strongest non-abliterated -2.665 (allenai/OLMo-1B-hf),
    abliterated W01 median 4.26, base W01 max 1.992. Report the reproduction deltas; if they do not reproduce, that is the
    headline and everything downstream is conditioned on it. ARM 1, RECIPE SCOPE. Acquire and measure at least three, target
    six, abliterated/uncensored checkpoints at <= 4.2B produced by MECHANICALLY DIFFERENT toolchains from the huihui/Josiefied
    class - verify the recipe from the card, config or linked code and record the evidence, do not trust the repo name. Concrete
    starting candidates to verify: mlabonne/Qwen3-0.6B-abliterated (this project already used it in iteration 1 and it is
    NOT among the 8 positives, so it is the cheapest recipe-diversity win available), grimjim-class projected / norm-preserving
    variants, ORBA orthogonal-reflection outputs, OBLITERATUS 'advanced' multi-direction runs, and per-head or partial-layer
    surgeries. Where a recipe class has no public sub-4B checkpoint, REIMPLEMENT it in-house on Qwen3-1.7B-Instruct and label
    it synthetic: (a) norm-preserving projection (project out r then rescale each W to its original Frobenius norm), (b) multi-direction
    ablation removing a rank-k subspace for k in {2, 4, 8}, (c) per-head surgery touching only attention heads whose refusal-direction
    write energy is highest, (d) a partial-layer variant sweeping the fraction of edited layers from 0.33 to 1.0 so the blind
    spot becomes a CURVE rather than the single band-limited point already reported. Report W01-W05 for every checkpoint,
    plus the recomputed AUROC of each statistic under three groupings: all abliterated vs all else, LEAVE-ONE-UPLOADER-OUT
    (train the ranking on all uploaders but one, evaluate on the held-out uploader's members), and leave-one-architecture-family-out
    for comparison. State the scope sentence the data supports, in the form 'detects <recipe class>' with the classes it misses
    named. ARM 2, E_1 HEAD-TO-HEAD, the matched-panel comparison the paper owes its closest competitor. For every instruct/abliterated
    sibling pair in the panel where the parent is present (at least Qwen2.5-0.5B, Qwen2.5-1.5B, Qwen3-0.6B, Qwen3-1.7B, Llama-3.2-1B,
    Llama-3.2-3B), compute E_1 = mean over matrices of sigma_1^2(dW)/sum_i sigma_i^2(dW) with dW = W_parent - W_candidate
    over o_proj and down_proj in the published mid-stack band, and compute the SAME quantity for benign fine-tune pairs (instruct
    vs its own base, and any behaviourally-uncensored member vs its parent) so E_1 has negatives. Report W05 vs E_1 AUROC
    on exactly that matched subset with bootstrap CIs, and state the trade in one sentence: either parent-free matches parent-required
    at zero prompt cost, or the price of the constraint in AUROC. Also apply E_1 to the new-toolchain checkpoints where a
    parent is resolvable, since the cross-method question applies to the incumbent too. ARM 3, DEPTH INVARIANCE OF THE NEGATIVE.
    The held-out AUROC depth profile saturates at 1.0 across indices 4-25 of 28, so rho* = 0.679 was fixed by a d'-tiebreak
    on a 22-layer plateau and the activation arm's poor showing may be a property of the depth, not the arm. Recompute the
    depth-sensitive activation metrics (diff-in-means separation, d', AUROC, AMS sigma and its concept cosine, refusal-axis-to-unembedding
    cosine, prompt-position and generated-step logit-lens refusal log-odds) at THREE relative depths spanning the plateau
    - the bare argmax (~0.14), 0.50, and the pre-declared 0.679 - on the chat-rendered members, using the frozen prompt folds
    and the plain-vs-chat renderer rule (base models plain, excluded from correlations). Emit a tidy long table of (member,
    metric, depth, value) so the falsifier can be re-tested at each depth downstream, and report alpha_50's ceiling-censoring
    count at each depth (it was 37/44 at 0.679) so depth and metric are separable. IMPLEMENTATION NOTES that cost days if
    rediscovered: HF derives positions from cache_position, so LEFT-padded batches need explicit position_ids = (mask.cumsum(-1)-1).clamp_min(0)
    on the forward and every decode step; use svdvals rather than sqrt(eigvalsh(W W^T)) for square attention matrices; download
    sequentially and delete weights after measuring; report which tier completed.
  depends_on:
  - id: art_CKWQh2cOQLLQ
    label: dataset
    relation_type:
    relation_rationale:
  - id: art_BCxIq6GX4WIw
    label: dataset
    relation_type:
    relation_rationale:
  - id: art_lMTPOpnFwKnw
    label: spec
    relation_type:
    relation_rationale:
- id: experiment_iter3_dir4
  type: experiment
  objective: >-
    Instantiate the deployment premise the paper currently only asserts: measure whether the scar survives ordinary post-processing
    and deliberate evasion, in what ORDER the flag and the un-censoring die, and whether any undeclared Hub checkpoint carries
    the signature.
  approach: >-
    Two arms. ARM 1, THE LAUNDERING LADDER, the decisive one. Using in-house edit machinery, abliterate Qwen3-1.7B-Instruct
    with a faithful global diff-in-means rank-one projection over every residual-write matrix (o_proj, down_proj, and embed_tokens
    if the reference implementation includes it - record which), verify the edit landed by requiring the same signature the
    panel's abliterated members show (W02 near 1.0, W01 above 3, W05 well below -3) and by requiring harmful-refusal rate
    to collapse relative to the parent. Then take that checkpoint through five laundering treatments, each a separate branch
    from the SAME abliterated root: (a) LoRA-SFT for 200 steps on benign instruction data (report rank, alpha, target modules,
    learning rate, and merge the adapter before measuring so the weights are directly comparable); (b) linear merge with the
    instruct parent at weights 0.25 / 0.50 / 0.75, giving a merge ladder rather than one point; (c) round-trip int8 and int4
    quantization and dequantization back to the original dtype; (d) added-back random rank-one term epsilon * u u^T W at increasing
    epsilon, the metric-aware adversary who knows W05 is a minimum over layers and only needs to lift the smallest one; (e)
    a combined worst case (quantize then merge at 0.25). At EVERY stage report all five weight statistics AND the behavioural
    readout on the same items used for the panel's ground truth - harmful-refusal rate on the 40-item stratified harmful core
    and over-refusal on the 25 XSTest-safe items, greedy, with the behaviour-scoring judge rubric that separates 'did the
    model comply' from 'is the content harmful' (the harmfulness-scoring rubric gives kappa ~0 and must not be used), plus
    a fluency screen (WikiText perplexity and within-response distinct-3) so a stage that merely broke the model is not scored
    as evasion. Judge spend capped at $1.50 and logged after every call. THE LOAD-BEARING OUTPUT is a single figure and table
    showing the two curves - flag strength (W05, and W01/W04 alongside) and un-censoring strength (harmful compliance) - against
    treatment intensity, with the crossing point stated: if the flag dies only AFTER the model stops being uncensored, the
    scar is a robust provenance signal and that is a strong result; if it dies first, the scar is evadable and the paper says
    so plainly and quantifies the evasion cost. Report which of the five statistics is most robust - the prediction is that
    W05, being a minimum, is the most fragile and W01/W02, being aggregates, degrade more gracefully, which if true is an
    immediate and cheap methodological improvement to the metric. ARM 2, THE HUB SCAN. Score sub-4B checkpoints that do NOT
    declare abliteration in their repo id or card, from stored tensors only, in downloads-ranked order, deleting each after
    measurement; state the number completed rather than promising a target, and prioritise the smallest models so coverage
    is maximised within the time budget (aim for at least 40 completed, more if bandwidth permits). Report the full score
    distribution, name every checkpoint scoring inside or near the abliterated region defined by the panel (W05 below -2.742,
    and the warning band -2.742 to -2.5), and for each such hit fetch its card and lineage and adjudicate whether it is a
    genuine undeclared edit, a merge of an abliterated ancestor, or a false positive - quoting the evidence either way. Report
    the false-positive count against the number scanned as the deployment-relevant number, and note that architectures outside
    the seven tested are where false positives are expected to concentrate (the three nearest-boundary non-abliterated members
    are all from single-member families, olmo and gpt_neox). Even a handful of confirmed undeclared positives makes the deployment
    claim concrete; zero hits over N scanned is also a reportable and useful specificity number.
  depends_on:
  - id: art_CKWQh2cOQLLQ
    label: dataset
    relation_type:
    relation_rationale:
  - id: art_BCxIq6GX4WIw
    label: dataset
    relation_type:
    relation_rationale:
  - id: art_lMTPOpnFwKnw
    label: spec
    relation_type:
    relation_rationale:
- id: evaluation_iter3_dir5
  type: evaluation
  objective: >-
    Ship analysis.py as a first-class versioned deliverable that recomputes every statistic in the paper, and use it to turn
    the negative from a verdict into a measurement - power, pre-specified comparator, reliability-corrected correlations -
    while auditing every 'pre-registered' claim and every numeral against the artifact that records it.
  approach: >-
    Pure re-analysis of the archived iteration-2 trees; no new model inference beyond LLM judging for the reliability arm.
    (1) ANALYSIS.PY, the centrepiece. One script reading long_table.jsonl / battery + behaviour.jsonl and emitting EVERY AUROC,
    Spearman, bootstrap CI and paired difference that appears in the paper - the Sec 5.1 weights-arm AUROCs, the Sec 5.2 correlation
    table at both aggregation units, and all seven paired |rho_X| - |rho_B09| differences. Print in the file header, and echo
    into the output: the RNG seed, B, whether lineages are resampled with or without replacement, exactly how the 9 singleton
    lineages are handled, the tie-handling rule for Spearman (rank-average, explicitly - the project's own audit found position-based
    tie-breaking flipped the sign of a previous result), the AUROC tie convention, and the base-model exclusion rule. Include
    an assertion block checking each recomputed value against the number quoted in the current draft, and emit a table of
    every disagreement - transcription errors are expected and finding them is part of the deliverable. Also emit, machine-readable,
    the numerals the draft must regenerate rather than transcribe: [min, max] for EVERY class in the weights table (not only
    the abliterated column - base W01 max 1.992 genuinely overlaps abliterated min 1.438, and base W02 max 1.000 equals the
    abliterated median), the nearest non-abliterated neighbour on W05 by name (allenai/OLMo-1B-hf, -2.665), the family membership
    of the three checkpoints nearest the boundary, the correct random-direction count for W03 (256, not 64), and the exact
    positive-control checkpoint and revision (Qwen/Qwen3-0.6B, the instruct member, whose unedited W01 is 0.624 - distinct
    from the Base member's 0.628, and distinct from the unrelated 4.82 values that currently read as a typo). (2) POWER. Simulate
    the actual paired lineage bootstrap at n = 18 lineages under the observed rank structure and report the minimum detectable
    |rho| difference at 80% power, plus the achieved CI half-widths. State explicitly whether the falsifier COULD have failed,
    and emit the restated conclusion sentence in the form the data supports: 'at this panel size no interior metric shows
    an advantage over the best black-box baseline larger than ~X in |rho|; distinguishing smaller advantages needs roughly
    N lineages.' (3) COMPARATOR. B09 was selected as best-of-11 black-box declarations on the same data, so the current headline
    is best-of-11 against a fixed white-box candidate. Report the paired comparison against the PRE-SPECIFIED B01 (first-step
    logit gap, which has a published prior) alongside the post-hoc winner, and quantify the selection advantage by re-running
    the best-of-11 selection inside the bootstrap. Reconcile explicitly the awkward fact that A02 leads B09 numerically at
    both aggregation units (+0.802/+0.819 vs +0.766/+0.852) - state whether the headline should be 'no interior metric beats
    black-box with a CI excluding zero' or the weaker-but-true 'the numerically best metric is an interior one whose advantage
    is not resolvable'. (4) RELIABILITY AND ATTENUATION. Each checkpoint's harmful-refusal rate rests on 40 items scored by
    a single judge with judge-vs-screen kappa ~0.30 - a binomial SE of ~0.08 at p = 0.5 before judge noise. Estimate reliability
    by split-half over the 40 items (Spearman-Brown corrected) and by re-judging a stratified subsample of the archived generations
    with an independent adjudicator model under the behaviour-scoring rubric, reporting agreement; then report attenuation-corrected
    versions of every Sec 5.2 correlation and every paired difference alongside the raw ones, plus per-member binomial error
    bars, and state whether ANY ordering moves. LLM spend capped at $1.00 with per-call logging and response caching so a
    rerun costs $0. (5) DEPTH AND CENSORING. Re-run the Sec 5.2 correlation table at the three plateau depths and state whether
    the falsifier conclusion is invariant; if any activation metric beats the black-box baseline at some depth in the plateau,
    disclose it prominently even though 0.679 is the pre-declared primary. Report alpha_50's censoring rate at each depth.
    If the depth-swept activation values from this iteration's scope experiment are unavailable, run this arm on whatever
    depth-varying quantities the archive already contains and say exactly which depths were reachable. (6) PRE-REGISTRATION
    FIDELITY. Audit the SHA-stamped metric_spec.py against every claim in the paper of the form 'pre-registered'. That file
    declares 53 metrics with family, prompt requirement and declared cost, and NOTHING ELSE - no falsifier, no analysis plan,
    no base-model exclusion rule, no blanket-refuser threshold, no bootstrap specification. Emit a table mapping every such
    claim to the artifact and line that actually records it, marked SUPPORTED / PLAN-ONLY / UNSUPPORTED, and supply the corrected
    wording for each unsupported one ('we adopted the rule that...'), reserving 'SHA-stamped pre-registration' for the metric
    declarations alone. Deliverable: analysis.py plus a machine-readable numbers file that the paper generates its numerals
    from.
  depends_on:
  - id: art_xyUlckdGtbjc
    label: reanalyzes
    relation_type:
    relation_rationale:
  - id: art_CbL-EUQlwgfw
    label: reanalyzes
    relation_type:
    relation_rationale:
  - id: art_BCxIq6GX4WIw
    label: reference
    relation_type:
    relation_rationale:
expected_outcome: >-
  By the end of this iteration the paper's two claims are bounded rather than merely stated. (1) SCOPE: W01-W05 measured on
  at least three, target six, abliterated checkpoints from mechanically different toolchains plus in-house reimplementations
  of norm-preserving, multi-direction, per-head and partial-layer recipes, with leave-one-UPLOADER-out reported beside leave-one-family-out
  and a partial-layer sweep turning the band-limited blind spot into a curve - yielding a defensible scope sentence naming
  the recipe class detected and the classes missed. Plus the first computed E_1 head-to-head on the matched sibling subset,
  which quantifies what the parent-free constraint costs instead of asserting the trade. Plus a depth-swept activation table
  letting the falsifier be re-tested at three depths spanning the 22-layer plateau. (2) DEPLOYMENT: a laundering ladder reporting
  flag strength and un-censoring strength at every stage of LoRA-SFT, three merge ratios, int8/int4 round-trip, an adversarial
  added-back rank-one term and a combined worst case, with the crossing point of the two curves stated explicitly, plus a
  Hub scan of undeclared sub-4B checkpoints reporting hits, adjudicated evidence, and a specificity number. (3) DISCIPLINE:
  analysis.py recomputing every headline statistic with seed, B, resampling scheme and rank-average tie handling printed and
  asserted against the quoted values; a power simulation stating whether the falsifier could have failed and the restated
  conclusion; the pre-specified B01 comparison beside the best-of-11 winner with the selection advantage quantified; split-half
  and adjudicator reliability with attenuation-corrected correlations and per-member error bars; and a SUPPORTED / PLAN-ONLY
  / UNSUPPORTED table for every 'pre-registered' claim with corrected wording. (4) POSITIONING: arXiv:2604.08844 and OBLITERATUS's
  spectral certification cited at their points of use with the three-axis distinction written out, a reimplementable taxonomy
  of six-plus abliteration recipes, and a resolved or precisely restated novelty risk. (5) A recipe-labelled, evidence-carrying
  manifest of 25+ edited checkpoints, laundering corpora, and a ranked Hub scan pool that stocks iterations 4-5. Negative
  outcomes are all reportable and several are likely by design: the most probable single result is that the scar survives
  quantization and merging but not LoRA-SFT, and misses at least one new toolchain - which turns the headline into 'a recipe-class
  provenance signal, free at hub scale, with a measured evasion boundary'. If instead the cross-toolchain AUROC holds, that
  is a genuine surprise against the published AUC-0.00 precedent and a considerably stronger paper. Either way iterations
  4-5 inherit a bounded claim, working analysis code, and a candidate pool for scaling the scope test.
summary: >-
  Iteration 3 stops adding metrics and starts bounding the two results it already has. Two weights-heavy experiments measure
  the scar's recipe-class scope (new toolchains, in-house norm-preserving / multi-direction / per-head / partial-layer reimplementations,
  leave-one-uploader-out, and the first E_1 parent-required head-to-head) and its evasion boundary (LoRA-SFT, merge ladder,
  int8/int4 round-trip, adversarial added-back rank-one, plus a Hub scan for undeclared positives), reporting flag death against
  un-censoring death. One evaluation ships analysis.py - every AUROC, Spearman, bootstrap and paired difference with seed,
  B, resampling scheme and tie-handling printed and asserted - and converts the negative into a measurement via a power simulation,
  a pre-specified comparator, reliability-corrected correlations and a depth-invariance check, while auditing every 'pre-registered'
  claim against the file that actually records it. One research pass closes the two uncited prior works and returns a reimplementable
  recipe taxonomy; one dataset ships the evidence-carrying, recipe-labelled checkpoint manifest and the scan pool for later
  iterations.
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

--- Item 11 ---
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

--- Item 12 ---
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

--- Item 13 ---
id: art_fvWfzRrcoKux
type: experiment
title: Testing how far the weight scar reaches
summary: |-
  $0 LLM spend, ~1h on one RTX 4090; every number re-derived by an assertion block that blocks assembly.

  GATE = PASS. wstats.py is an INDEPENDENT reimplementation of W01-W05 from the published formulae (written before lib_metrics.py was read). On 10 members (5 abliterated / 5 not) at archived revisions it reproduces the archive to max|dW05|=9.9e-06, ordering preserved, Spearman 1.0000, bit-identical across two independent runs. Three attributable divergences are reported, not smoothed: (a) W01 reproduces to 1e-4 on non-abliterated members but drifts up to 0.048 on ABLITERATED ones, because lambda_min sits at the float noise floor exactly where the scar is (iter2 accumulated the Gram in float32, here float64; NOT a load-dtype effect -- the float32-load column is identical); (b) W03 differs systematically by +0.015..+0.034, a DEFINITIONAL difference -- the published formula takes q05 of the per-direction MEAN energy, the iter2 code pools all (direction x matrix) energies first; (c) revision drift zero. Controls reproduce: injected rank-one gives |cos(v1,r)|=1.000000, W02=1.00, W01 0.624->4.869; band-limited middle-third gives W02=0.0.

  ARM 1 = RECIPE_CLASS_BOUNDED, and the binding limit is UPLOADER, not recipe. Hub search (7 queries, 70 candidates verified from card evidence) established that mechanically different recipes DO exist (norm-preserving, multi-direction, biprojected) but EVERY one is >=14.9B, far above the 4.2B ceiling -- forcing the pre-registered fallback. Four real published <=4.2B abliterated checkpoints from four UNSEEN uploaders were measured instead: W05 = -0.964 mlabonne/Qwen3-0.6B-abliterated, -1.010 MagicalAlchemist/Qwen3-1.7B-Magic_decensored, -0.990 prithivMLmods/VibeThinker-3B-heretic_decensored, -2.161 BennyDaBall/Qwen3-4b-Z-Image-Turbo-AbliteratedV1, against an archived abliterated range of -2.74..-4.82. W05 AUROC 1.000 on the two calibration uploaders vs 0.382 on the four new ones, 0/4 caught at the fitted threshold. realcheck.py rules out the re-upload explanation: all three with a resolvable parent are GENUINE near-rank-one edits (E_1 0.995/0.995/0.997, relative Frobenius change 2.5-3.0%, 0% bit-identical matrices). Twelve in-house synthetic variants on two architectures: normpres and rank-k (k=2,4,8) AUROC 1.000; per-head (top 25%) 0.556; LAYER-FRACTION SWEEP gives f*=1.00 on BOTH hosts -- only the fully global edit is detectable. Sharpest: on Qwen3-1.7B a projection confined to the middle 50% of layers drives harmful refusal 0.45->0.00, exactly as effective as the full-stack edit, while W05 moves -1.0098 -> -1.0088, indistinguishable from unedited. No variant was degenerate.

  ARM 2 = PARENT_FREE_COSTS_0.167_UNDERPOWERED. E_1 = mean_m sigma_1^2(dW)/sum sigma_i^2(dW) over the 0.25L-0.75L band (recorded as OUR reading of 'mid-stack'). On the pre-declared 12 pairs (positives all from the two calibration uploaders) E_1 and W05 TIE at AUROC 1.000, paired diff +0.000. Adding the 3 new-uploader pairs: E_1 holds at 1.000, W05 falls to 0.833, paired lineage-bootstrap difference -0.167 [-0.444, 0.000] -- the interval reaches zero at its boundary, so UNDERPOWERED as an interval claim at n=15, but descriptively unambiguous (E_1 3/3, W05 0/3). Complementary on synthetics: E_1 degrades on multi-direction (0.17-0.67, k=8..2) where W05 is perfect, and holds at 0.995 on the band edits W05 cannot see.

  ARM 3 = INVARIANT. Depth-sensitive activation metrics recomputed at three relative depths (bare AUROC argmax 0.143 read from CALIB, 0.50, pre-declared rho*=0.679) over 26 chat-rendered members -> results/long_table_depth.jsonl, 1014 (member, metric, depth) rows, the downstream deliverable. The black-box baseline wins at ALL three depths, so iteration 2's falsifier is NOT a depth artefact. This needed the right test: four activation metrics have a LARGER point estimate than a baseline at rho* (A19_refusal_axis_unembed_cosine rho=+0.770 vs B09 +0.766), but the PAIRED lineage-bootstrap difference is +0.0045 [-0.225,+0.260] -- comparing point estimates alone would have called that a win. Also: alpha_50's ceiling censoring is strongly DEPTH-DEPENDENT (25/26 censored at the bare argmax, 15/26 at 0.50, 19/26 at rho*), so the pre-declared depth is NOT the one giving the most usable values.

  CONTROLS: synthetic-tensor unit tests found a STRONGER blind spot than expected (with 4/12 matrices edited, v1 is no longer the injected direction at all, W02=0, because the Gram pools every matrix -- a threshold, not a ramp); random-direction control on real models PASSES decisively (true v1 -2.742 on the abliterated member vs -0.085 for 5 random directions); revision stability STABLE but weaker than intended (main had not moved); permutation nulls with exact floor 1/C(n,k) beside every CI. Three abliterated members were recovered after their tokenizers shipped no chat_template under transformers 5.x, by substituting standard ChatML. vendored_lib_*.py are BYTE-IDENTICAL (zero patches); lib_*.py are alias shims.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_art/gen_art_experiment_1
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

--- Item 14 ---
id: art_gCgia-6VUZJb
type: experiment
title: Can you scrub the abliteration scar?
summary: |-
  BOTH ARMS EXECUTED AT FULL SCALE. Verdict SCAR_IS_CHEAPLY_EVADABLE. 34 ladder stages on Qwen3-1.7B + 160 scanned Hub checkpoints, $0.107 judge spend, all 4 gates pass, 17/17 cross-checks pass (verify.py recomputes headline numbers straight from results/*.jsonl).

  ROOT IS CLEAN. In-house diff-in-means abliteration of Qwen/Qwen3-1.7B: harmful refusal 0.923 -> 0.162 (rubric-B judge, frozen 40-item core), W01 4.571 / W02 1.000 / W05 -4.592 (inside the abliterated region), WikiText ppl UNCHANGED 27.08 -> 26.25. Both gates pass on V_A; V_B (embed projected) and V_AUROC ship as sensitivity rows. NO stage tripped the BROKEN fluency screen or the blanket-refuser rule.

  ARM 1 CROSSING (flag death vs un-censoring death). EVADABLE in 4 of 6 real intensity axes: add-back-all eps 0.10 vs 1.00 (cost -0.004), merge w 0.10 vs 0.50 (+0.069), quantization 4-bit vs never (+0.075), add-back-topk k=4 vs k=32 (+0.128). NEITHER_DIES for argmin-only add-back, random-direction add-back, LoRA-SFT. CHEAPEST EVASION IS NOT AN ATTACK: a plain int4 round-trip kills the flag (W05 -4.59 -> -1.95) at harmful refusal 0.135, BELOW the root's own 0.162, ppl 37.7 vs root 26.25, inside the fluency screen. An ordinary deployment step erases the scar for free.

  THREE RESULTS REVERSE THE PRE-REGISTERED PREDICTIONS. (1) The argmin attack FAILS: at eps=1.00 it moves W05 only to -3.080 and never crosses. Abliteration suppresses all 56 write matrices roughly equally, so the minimum has 55 runner-ups; k=4 must be patched. Because v1 is recomputed from the treated model, a local patch ROTATES the eigenvector and lifts EVERY matrix's energy -- a local edit has a global effect on the statistic. (2) Dense benign fine-tuning does NOT scrub it: 200 LoRA steps (r=16, alpha=32, alpaca-cleaned, merged) move W05 only -4.592 -> -4.381 while RESTORING refusal 0.162 -> 0.368. (3) W05 is NOT the most fragile statistic (survival 0.559 vs W02 0.647), but W02 flags 23/160 undeclared repos, so its robustness is a threshold that separates nothing.

  HEAD-TO-HEAD BASELINES (metadata.statistic_head_to_head, labelled controls): only W05 reaches sensitivity 1.000 / specificity 1.000 with 0/160 undeclared flagged. W01/W03/W04 sit at 0.875 sensitivity; W02 flags 14.4% of undeclared repos. The hardened W05q10 (10th percentile, not min) keeps perfect specificity but drops to 0.875 sensitivity -- hardening has a measured cost.

  ARM 2 (tensor-only, zero prompts, zero forward passes). 250 attempted / 160 completed (65 UNRESOLVED with reasons: Conv1D-transposed GPT-2-style, quantized GPTQ/bnb, bad configs; 7 SKIPPED, 1 ERROR -- never counted as scanned). ZERO hits inside the abliterated region; false-positive rate 0/160, Wilson 95% [0, 0.023]. Two warning-band repos (rinna/japanese-gpt-neox-small -2.614, stabilityai/stablelm-3b-4e1t -2.515), both adjudicated FALSE_POSITIVE with quoted card evidence, both in families the panel barely covered -- as predicted. Controls 8/8 positive and 12/12 negative through the identical path. Enumeration counts shipped (1500 listed; 73 DECLARED, 587 oversize, 54 gated, 30 in-panel dropped). Audit cost: median 7.4 s CPU per checkpoint, 2.7 s on GPU at 1.7B.

  METHOD CORRECTIONS DOWNSTREAM WORK MUST INHERIT. (a) Held-out AUROC SATURATES and cannot select the refusal direction: 11 layers >= 0.997 and 4 tie at exactly 1.000 on Qwen3-1.7B, so the argmax is decided by the tie-break; the AUROC-picked direction reproduces the full signature while leaving refusal at 0.333 vs the behavioural pick's 0.162 -- scar and un-censoring are DISSOCIABLE AT CONSTRUCTION TIME. At 0.6B the argmax lands at block 1 and does not un-censor at all; selection must be behavioural (Arditi-style sweep on a dev subset disjoint from the eval core). (b) The panel boundary is -2.7415117804288127, not the rounded -2.742: at the rounded value the member DEFINING it falls outside and the positive control reads 7/8. (c) Only W05 separates the iteration-2 panel; W02's non-abliterated max is 1.0000, so no W02 threshold separates anything. (d) The merge curve is monotone in w only UP TO SATURATION at the parent's own W05 (-1.010); the 0.008 dip at w=0.75 is eigenvector switching, not a bug. (e) judge_kappa_vs_regex ~0 is the REGEX failing (0.000 on every abliterated stage), not the judge: rate-level r = 0.952, judge primary for all 34 stages, T3 calibration 6/6. (f) Gate T4: the tensor-only path is BIT-IDENTICAL to the Runner path on the same device; W01/W04 carry ~8e-3 of float32 CPU-vs-GPU noise, decision statistics agree to 1e-6.

  SHIPPED: method_out.json (7 datasets: ladder, ladder_e_v1_profiles, crossing, robustness, scan, scan_hits, diagnostics; per-row predict_w01..predict_w05q10 make the baseline comparison machine-readable), 6 vector figures rendered from the artifact, README. The 3.8 GB root state_dict is NOT persisted: results/root_recipe.json (52 KB) holds the direction, keys and a sha256 fingerprint; rebuild_root() reconstructs it in ~9 s, verified 311/311 tensors bit-identical.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_art/gen_art_experiment_2
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

--- Item 15 ---
id: art_0T8jhUa0zxmu
type: evaluation
title: Recomputing every number the paper quotes
summary: |-
  PURE RE-ANALYSIS of the archived iteration-2 trees. No weights loaded, no forward passes, no text generated; the only outbound compute is cached LLM re-labelling of already-archived generations ($0.1703 of the $0.90 cap, 2,865/2,866 items, rerun costs $0). `uv run eval.py` -> analysis.py (2,230 lines) in 547 s on 48 cores; numbers.json is BYTE-IDENTICAL across two runs (timings stripped); eval_out.json + full/mini/preview all pass exp_eval_sol_out.

  HEADLINE FINDING. Four values the draft presents as CORRELATIONS -- A01 -0.161 [-0.501,+0.208], A02 +0.036 [-0.225,+0.303], W01 -0.373 [-0.731,-0.039], alpha_50 -0.453 -- are in fact PAIRED DIFFERENCES |rho_X|-|rho_B09| computed on a 26-member `renderer=='chatml'` subset, NOT the 28-member `member_class != 'base'` subset the draft states. Identified because B09's quoted +0.766 reproduces to 1e-4 on that subset and on none of 16 other (subset, target, unit) conventions; all four quoted |rho| (0.802/0.819 vs 0.766/0.852) reproduce there to <4e-4. Read as correlations they are wrong by up to 0.67 and one has the wrong sign; read correctly, A01/A02/W01 match to four decimals (alpha_50 does not, n=7). The arithmetic was never wrong -- the LABELS were, and no artifact recorded either the quantity or the subset. The falsifier is re-run on the draft's own subset: verdict UNCHANGED on both.

  TWO MORE CORRECTIONS. (1) B09 is NOT the best black-box metric: B08_first_token_entropy_asymmetry |rho| 0.782 beats it at lineage level, B01 0.708 at member level; B09 is the in-resample argmax in only 11.2%/14.4% of resamples; selection optimism +0.182. (2) W05's 'AUROC 1.000' is the ORIENTED value -- raw AUROC is 0.000 because abliterated members sit LOW -- and W01/W03/W04 give 0.9861, W02 0.9497 with 21 tied pairs. Separating margin 0.0763 log10 (allenai/OLMo-1B-hf -2.665 vs huihui Qwen2.5-0.5B -2.742); OLMo is a ONE-MEMBER family. The draft's 'abliterated minimum -2.742' is the abliterated MAXIMUM (true min -4.820).

  ARMS. POWER: minimum detectable |drho| = 0.32 at n=19 lineages (2,000 sims x B=2,000); ~150 lineages needed at delta 0.20, 50 at 0.30, unreachable at 0.10; falsifier_could_have_failed=True. RELIABILITY: split-half Spearman-Brown r_xx = 0.968, so attenuation correction is a factor of 1.016 -- the negative is NOT an attenuation artefact (and a common factor cannot reorder anything, stated rather than sold as survival). Independent adjudicator 6/6 on the hand-labelled set, kappa 0.403 vs the regex screen (regex refusal share 0.19 vs judge 0.43), checkpoint-level Spearman 0.927 vs the archived llama-3.3-70b rates; item-level judge-vs-judge kappa is UNRECOMPUTABLE (E1 kept rates only). DEPTH: PARTIAL -- only auroc_profile and margin_profile are archived per depth; nothing beats B09 at any reachable depth. PRE-REGISTRATION: 4 SUPPORTED / 2 PLAN-ONLY / 6 UNSUPPORTED (metric_spec.py sha 544ff994 stamps 53 metrics and NOTHING else -- no falsifier, exclusion rule, bootstrap spec, candidate list or B09 baseline; rubric B was written after rubric A failed; the blanket-refuser and split-seed rules belong to the DATASET artifact and ARE pre-specified). DISAGREEMENTS: 54 checked -> 32 MATCH, 20 RECOMPUTE_DIFFERS_METHOD, 2 TRANSCRIPTION_ERROR.

  ALSO CORRECTED: W03 uses 256 random directions (lib_metrics.py:105), not 64; the behaviour arm is 28 members over 19 lineages, not 18; renderer values are 'chatml'/'plain' (26/18) and that partition DISAGREES with member_class on 2 members; battery.jsonl matches method_out.json long_table row-for-row (61 nulls differ only in encoding); 9-of-23 singleton lineages CONFIRMED. numbers.json ships the full class-wise [n, median, min, max] for every member_class x metric (the overlaps the abliterated-only column hides), the boundary families, the positive-control disambiguation (instruct 0.6239 vs base 0.6281), and a note that THREE unrelated quantities round to 4.82.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_art/gen_art_evaluation_1
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

An open-weight checkpoint arrives with no provenance. Deciding whether its safety training is intact currently costs a benchmark run: hundreds of harmful prompts from AdvBench [30], JailbreakBench [31] or HarmBench [32], a judge model to score the generations [35], and a repeat for every attack template of interest. The evaluator must hold and transmit harmful content, must pay for a judge, and must trust that the checkpoint was not tuned to refuse exactly the items it will be shown. At the scale of a model hub the unit of cost is wrong: our own harvest of 61 Hub sweeps over 20,313 enumerated repositories found 513 self-declared edited checkpoints from **189 distinct uploaders** below 4.2B parameters alone [ARTIFACT:art_8OlSrcw-hzgO].

The published cheap alternatives each retain a dependency the situation does not grant. AMS [3] reads activation geometry but needs harmful prompts and reports that behavioural uncensored fine-tunes are undetectable by it. RAS/SafeVec [4] needs unsafe prompts, jailbreak prompts *and* a safety-aligned reference model. VISAGE [5] evaluates a harmful benchmark at every weight perturbation. The two closest weight-space results both require the parent: the abliteration audit of [2], whose weight statistic is $E_1 = \mathrm{mean}_m\,\sigma_1^2(\Delta W_m)/\sum_i \sigma_i^2(\Delta W_m)$ with $\Delta W = W_{\text{base}} - W_{\text{cand}}$, and the spectral-geometry study of LoRA adapters [8], which reaches AUC 1.00 for binary drift detection from per-layer spectral features of a weight *delta*. A random Hugging Face repository does not come with an attested parent.

This paper adopts a hard operating constraint and reports exactly what survives it: **the metric sees one checkpoint's tensors**. No sibling, no base to diff against, no reference model, no prompt, no forward pass. The previous iteration of this work reported that under that constraint one statistic separates abliterated checkpoints from everything else at AUROC 1.000 over 44 checkpoints. This iteration was written to find out whether that number means what it appears to mean, and the answer is that it does not — not because the signal is spurious, but because *abliteration* names a family of at least eight mechanically distinct recipes and eight positives from two uploaders sample one corner of it.

[FIGURE:fig1]

Four measurements decide the paper. **First, the scar is real, and it is extremely specific in the wild.** On 160 sub-4B Hub checkpoints that declare no edit, scored from stored tensors only — zero prompts, zero forward passes, a median of 7.0 s of CPU linear algebra each — the statistic returns **zero** hits inside the abliterated region, a false-positive rate of 0/160 (Wilson 95% $[0, 0.023]$), while flagging 8 of 8 known-abliterated positive controls and 0 of 12 known-clean negative controls through the identical code path [ARTIFACT:art_gCgia-6VUZJb]. **Second, the parent-free constraint costs nothing on the recipe it was characterised on and everything off it.** On 12 pre-declared instruct/abliterated sibling pairs, the parent-free statistic and the parent-requiring $E_1$ tie at AUROC 1.000, paired difference $+0.000$; on four real published abliterated checkpoints at $\leq$4.2B from four uploaders the detector had never seen, it collapses to AUROC 0.382 and catches 0 of 4 at the fitted threshold, while $E_1$ — which has the parent — sees 3 of 3 of the pairs it can form, all confirmed genuine near-rank-one edits [ARTIFACT:art_fvWfzRrcoKux]. **Third, the flag dies before the un-censoring does.** In a 34-stage laundering ladder on an in-house abliteration of Qwen3-1.7B, the cheapest successful evasion is not an attack: a plain **int4 round-trip** erases the flag ($W05: -4.59 \to -1.95$) at a harmful-refusal rate of 0.135, *below* the unlaundered root's own 0.162, inside the fluency screen [ARTIFACT:art_gCgia-6VUZJb]. **Fourth, the scar and the un-censoring are dissociable at construction time**: a projection confined to the middle 50% of layers drives harmful refusal from 0.45 to 0.00 — exactly as effective as the full-stack edit — while the statistic moves from $-1.0098$ to $-1.0088$, indistinguishable from the unedited model.

The honest product of those four is not "a detector for abliteration" but something narrower, cheaper and still useful: **a free, prompt-free certificate that a checkpoint carries an unlaundered global directional edit**, with a fully measured scope boundary on all four axes that matter (recipe, uploader, layer support, post-processing). We report the boundary as a first-class result rather than a limitation, because a hub-scale screen whose failure modes are unmeasured is worse than useless.

A second, independent contribution is negative and is now quantitative rather than merely stated. For *graded* safety behaviour — how often a model actually refuses harmful requests — no interior observable in a frozen 53-metric battery beats a trivial black-box baseline. The previous draft reported that as a fired falsifier; a dedicated re-analysis artifact recomputed every number in it and found that the design's **minimum detectable paired difference is $|\Delta\rho| = 0.32$ at $n = 19$ lineages**, that roughly 150 lineages would be needed to resolve an advantage of 0.20, and that the named baseline was *not even the best black-box metric* — first-token entropy asymmetry beats it at $|\rho| = 0.782$ against 0.668 [ARTIFACT:art_0T8jhUa0zxmu]. The negative therefore stands in a bounded form, and we state the bound.

## Summary of Contributions

- **A parent-free, prompt-free weight statistic for global directional refusal ablation, with its scope measured on four axes** (§4.1, §5.1). $W05$ separates 8 abliterated from 36 non-abliterated archived checkpoints at oriented AUROC 1.000 (raw AUROC 0.000: abliterated members sit at the *low* end, and we report the orientation because it was read off the data). It generalises to norm-preserving and rank-$k$ synthetic variants (AUROC 1.000) and fails on per-head surgery (0.556), on layer-band edits (undetectable at any fraction below 1.00), and — the sharpest finding — on the *same* global recipe from four unseen uploaders (0.382, catch rate 0/4).
- **A deployment test rather than a benchmark: 160 undeclared Hub checkpoints scanned from stored tensors** (§5.2). Zero false positives, Wilson 95% $[0, 0.023]$, 8/8 and 12/12 controls, at a median 7.0 s CPU per checkpoint. Two warning-band repositories are named and adjudicated against their cards.
- **A laundering ladder that finds the flag is cheaply evadable, and says so** (§5.2). Four of six real intensity axes kill the flag before the un-censoring, the cheapest at an evasion cost of $-0.004$ in harmful refusal. Two pre-registered predictions reverse: a one-matrix argmin patch does **not** defeat a minimum-over-layers statistic, and 200 steps of benign LoRA-SFT do not scrub it (it *restores* refusal 0.162 $\to$ 0.368 while moving $W05$ only $-4.592 \to -4.381$).
- **The parent-required head-to-head the reviewer asked for** (§5.3). $E_1$ computed on every sibling pair in the panel: a tie at AUROC 1.000 on the 12 pre-declared pairs, $-0.167$ $[-0.444, 0.000]$ on 15 pairs including new uploaders, and complementary failure modes — $E_1$ degrades on multi-direction edits (0.17–0.67) where $W05$ is perfect, and holds at 0.995 on the band edits $W05$ cannot see.
- **The behavioural negative, made quantitative** (§5.4). Minimum detectable $|\Delta\rho| = 0.32$ at 19 lineages; the falsifier *could* have failed; a pre-specified comparator (B01 logit gap) reported alongside the post-hoc winner with its selection optimism priced at $+0.182$; split-half reliability $r_{xx} = 0.968$, so the attenuation correction is a factor of 1.016 and the negative is not an attenuation artifact; and the conclusion invariant across three depths spanning a 22-layer AUROC plateau.
- **A measurement-discipline audit of our own claims** (§5.5). Four values the previous draft presented as correlations were paired differences on a different subset; the frozen `metric_spec.py` stamps the 53 metric declarations **and nothing else**, so 6 of 12 "pre-registered" claims are downgraded to analysis-time conventions, with the mapping table published.

# Related Work

**Parent-required weight audits, and the exact hole we occupy.** WeightWatch [9] shows that the top singular vectors of a fine-tuned-minus-base weight difference correspond to newly acquired behaviours. The abliteration audit of [2] specialises this, combining an activation signal with the weight-recovery energy $E_1$ over $o\_proj$ and $down\_proj$ in a mid-stack band, over a 273-checkpoint registry. Closest of all, and uncited in our previous draft, is Paul's pre-registered spectral-geometry study of LoRA adapters [8]: 38 manufactured adapters on Llama-3.2-3B-Instruct, per-layer spectral features extracted from weight deltas, binary drift AUC 1.00 with CI $[1.00, 1.00]$, all six pairwise training-objective comparisons at AUC 1.00, ordinal severity $\rho \geq 0.956$ (the minimum of 0.976 / 1.000 / 0.956) and Spearman $\rho = 0.72$ on $N = 24$ against HEx-PHI harmful compliance, with no CI reported. Two of its five features — stable rank $\lVert \Delta W\rVert_F^2/\sigma_1^2$ and singular-value entropy $H = -\sum \hat\sigma_i \log \hat\sigma_i$ with $\hat\sigma_i = \sigma_i/\sum_j\sigma_j$ — are formula-identical to our $W06$–$W09$, and we cite it at the point of use in §4.1. We differ on three axes and each is load-bearing: it needs the parent (its single most informative feature is a cosine to a *healthy-adapter centroid*, requiring both a parent and a reference population), it is evaluated on manufactured adapters with a controlled 50–2000-step dose ladder rather than on real community checkpoints, and it predicts behaviour where we detect an edit. Its $\rho = 0.72$ is a direct counterweight to any universal claim that weight geometry carries no behavioural signal, and we do not make that claim: the paper itself notes the correlation "primarily reflects which side of the boundary" (healthy cluster at drift probability 0.001, DPO at 0.999), i.e. a two-class separation between groups that differ by a manufacturing operation. Our behaviourally-uncensored members were made by ordinary SFT with no directional edit, so there is no low-rank scar for either method to find.

Paul's study also supplies the strongest published precedent for this paper's central scope finding: a classifier trained on DPO-drifted adapters and tested on steering-derived ones scores **AUC 0.00** ($n_{\text{bootstrap}} = 972$, CI $[0.00, 0.00]$) — every out-of-method adapter ranked healthier than every in-method one. That precedent must be carried with its own declared confound: the steering arm generated incoherent text at every intensity (GPT-4o scored 0 of 300 responses harmful), so the paper says the geometric opposition "may reflect a broken injection method". The analogy is also inverted relative to ours — their classifier was trained on gradient edits and failed on an algebraic one; ours is built for the algebraic edit. Finally, [10] detects backdoored LoRAs "from weights alone" on Qwen2.5-3B, Llama-3.2-3B-Instruct and Gemma-2-2B, our exact size class, but its object is an adapter already separated from a frozen base and §4.3 fits a supervised calibration rule on labelled adapters.

**Parent-free spectral inspection is already community practice, and we say so.** The OBLITERATUS toolkit [11] ships a *spectral certification* step that decides whether a directional edit is complete. Reading its source settles a question our plan got backwards: it consumes **activations**, not weights — `certify(harmful_activations, harmless_activations, layer_idx)` forms a between-class mean difference, estimates a noise floor from the pooled within-class covariance by a median-eigenvalue/Marchenko-Pastur method, and thresholds the eigenvalues of the rank-1 outer product against a BBP bound inflated by $\sqrt{\kappa}$. It is therefore parent-free but not prompt-free or forward-pass-free, and it audits an edit the operator has just performed rather than deciding whether an unknown checkpoint was edited. Its documentation records, verbatim and identically across three mirrors, that "spectral certification RED is common — the spectral check often flags 'incomplete' even when practical refusal rate is 0%", which is an independent, anecdotal mirror of our own finding that the ranking transfers while the calibration does not. Its first public commit predates this work. The correctly scoped novelty claim is therefore not "nobody inspects an edited checkpoint's spectrum parent-free" but: *the weights-only, prompt-free, forward-pass-free form of that question, measured rather than asserted, with held-out lineages, leave-one-uploader-out, an injected positive control, a quantified calibration failure and a measured recipe-class boundary* [ARTIFACT:art_sHF0cggp2IvT]. Separately, the only *shipped* parent-free abliteration detector we could find, `reverse-abliterate` 0.1.2 [12], scans for `abliteration_metadata.json`, adapter-config pairs, repository-name suffixes and toolkit commit hashes: it reads no tensor values. It is the software instantiation of the string-match baseline our own data quantifies at 50.5% (259 of 513 self-declared edited repositories carry "abliterat" in the repository id) [ARTIFACT:art_8OlSrcw-hzgO].

**The recipe family.** Abliteration is not one operation. The taxonomy we assembled has eight members with reimplementation-grade update equations [ARTIFACT:art_sHF0cggp2IvT]: the global all-layer rank-one projection $W \leftarrow (I - \hat r\hat r^\top)W$ [1, 13]; mlabonne's v2 Gaussian depth kernel $W_\ell \leftarrow W_\ell - w_\ell (W_\ell \hat r)\hat r^\top$ [13]; Heretic's per-component optimised kernel with a float-interpolated direction index and published weights as high as 3.22, i.e. over-subtraction and a sign flip rather than annihilation [14]; MPOA's exact four-step row-norm-preserving update [15]; ORBA's Householder reflection $H = I - 2uu^\top$ with a geodesic $\lambda = 1$ variant [16]; Gabliteration's ridge-regularised rank-$k$ update $W \leftarrow W - \alpha_\ell(WP)$ with $P = R(R^\top R + \lambda I_k)^{-1}R^\top$ [17]; OBLITERATUS's rank-$k$ presets [11]; and behavioural SFT, which has no closed form. A cross-architecture comparison of these methods exists [18] but evaluates at 7B–14B, above our ceiling. One consequence lands directly on our previous headline: one of our eight archived positives is a *Gabliteration*, not a plain projection, and it scores at roughly half the margin ($W01 = 2.237$, $W05 = -3.522$ against the huihui range $W01$ 4.16–4.82, $W05$ $-4.21$ to $-4.82$). The recipe question was already half-answered inside our own positive set, as graded margin loss rather than collapse.

**Why a weight-space scar is expected at all.** Safety fine-tuning has been shown to minimally transform MLP weights so as to align unsafe inputs into a null space [19], and safety behaviour localises to a small set of neurons and ranks that can be pruned or low-rank-modified away [20]. Abliteration is the extreme case: an explicit rank-one projection applied to every residual-write matrix [1]. Heavy-tailed self-regularisation supplies mature spectral descriptors for trained weight matrices [21]. Community practice complicates the picture in ways we measure rather than assume: extended-refusal training defends against abliteration while leaving weights superficially normal [22], and abliteration has substantial off-target effects on behaviours that elicit no refusals [23].

**Detection is not control.** Galeone et al. [7] establish the general dissociation: a linear detector reaching AUC $=1.000$ from layer 5 sits at $\cos = 0.12$ (about 83°) from the direction that actually produces the behaviour, essentially unchanged by instruction tuning. Their Section 8 is an explicit negative — the detector-to-intervention cosine sits at chance for steerable and unsteerable behaviours alike — so a cosine-as-safety-score metric is a published negative, and we enter one only as a declared control. Our §5.5 reports the same dissociation in a new place: two refusal directions indistinguishable on held-out AUROC (11 layers $\geq 0.997$, four tied at exactly 1.000) differ twofold in how much they actually un-censor.

**Steering strength, and what we retired.** Logit-Gap Steering [24] takes the first-step gap between refusal and affirmative logits as a forward-pass diagnostic on our exact size class, and is the pre-specified black-box comparator in §5.4. The Rogue Scalpel [25] shows random steering directions raise harmful compliance from 0% to 1–13%, which converts a random direction from a null into a magnitude-matched comparator. Three further results bound what a scalar steering measurement can mean: steering strength acts non-monotonically on next-token probability [26], the optimal steering layer is input-dependent [27], and scalar steerability measures conceal behavioural shifts in open-ended generation [28]. Our own $\alpha_{50}$ steering-price metric was measured at 60,040 generations in the previous iteration and refuted as a triage score; it survives in this paper only as a battery member and as the methodological finding of §5.5 about refusal-substring screens.

**Ground truth.** Hasan and Biswas [29] report over-refusal and harmful compliance nearly uncorrelated across 21 open-weight models, which is why we predict two axes separately. Basu et al. [6] give the reason a read-side metric can be confidently wrong: 98.2% probe AUROC alongside 45.1% output sensitivity.

# Panel, Ground Truth and the Analysis Contract

**Panels.** Three panels are used and never mixed. (P1) The **archived battery panel**: 44 checkpoints at $\leq 4.2$B over 23 weight lineages and 7 architecture families (qwen3, qwen2, llama, gemma2, gpt\_neox, granite, olmo), comprising 16 base, 15 instruct, 8 abliterated, 4 behaviourally-uncensored and the official Qwen3-4B-SafeRL checkpoint, with a lineage-level held-out split whose seed and fraction were stamped before any model was loaded. (P2) The **scope panel**: four real published abliterated/decensored checkpoints at $\leq 4.2$B from four uploaders absent from P1, plus 12 in-house synthetic recipe variants on two architectures, plus a layer-fraction sweep, plus 15 matched parent/child pairs for the $E_1$ head-to-head. (P3) The **wild panel**: 250 attempted / 160 successfully scored sub-4B Hub checkpoints that declare no edit, drawn by descending downloads from a 2,139-row metadata pool with declared, undeclared-chat and undeclared-base strata [ARTIFACT:art_8OlSrcw-hzgO]. Every model-level statistic resamples weight lineages, not checkpoints.

**External safety ground truth barely exists at this scale, and we measured that rather than assuming it.** A dedicated harvest found external safety coverage for 3 of 66 candidate checkpoints and 2 of 34 lineages; twelve published safety sources — SORRY-Bench [36], OR-Bench, XSTest [33], TrustLLM [39], SALAD-Bench [38], DecodingTrust, JailbreakBench [31], HarmBench [32], AIR-Bench [37], HELM Safety v1.0.0 (27 models), HELM AIR-Bench v1.1.0 (22 models) and a large open-weight behaviour audit [29] — name **zero** panel checkpoints; HELM Safety was read from its machine-readable release registry and verified to contain no model under 10B. Safety ground truth is therefore measured in-house on two axes: harmful-refusal rate on a frozen 40-item stratified core and over-refusal rate on 25 XSTest-safe items, with a blanket-refuser disqualification rule at $>0.50$ over-refusal derived from XSTest's own released human labels. That rule and the split seed *are* pre-specified, in the dataset artifact rather than in the metric declarations, and we say which is which in §5.5.

**Judge protocol.** The judge is `meta-llama/llama-3.3-70b-instruct` at temperature 0 under rubric B, which explicitly separates "did the model comply" from "is the content harmful". The rubric mandated by our own earlier plan (rubric A) scores *harmfulness* rather than *behaviour*, gave $\kappa \approx 0$ against a hand-labelled set, and was replaced; that replacement is a deviation and is recorded as one. Judge spend across this iteration was \$0.107 (laundering ladder) plus \$0.170 (independent re-adjudication), with the weights-only arms costing \$0.00.

**The analysis contract.** Every AUROC, Spearman correlation, bootstrap interval and paired difference in this paper is emitted by a versioned analysis script that prints its contract before any number and echoes it into a machine-readable `numbers.json` [ARTIFACT:art_0T8jhUa0zxmu]. The contract: cluster bootstrap over **lineages, with replacement**, $B = 10{,}000$ resamples, percentile 95% intervals; the number of eligible lineages is the resample size for each cell (11 of 19 lineages in the behaviour arm are singletons, and they are drawn as clusters like any other); Spearman with **rank-average** tie handling — a rule that matters, because our own prior-round audit found a reported $\rho = -0.20$ flip sign to $+0.105$ purely from positional tie-breaking; AUROC as Mann-Whitney $U/(n_+ n_-)$ from rank-average ranks with 0.5 tie credit and the number of tied pairs reported; **pairwise deletion** with the achieved $n$ printed at every cell and a cell of fewer than 4 usable members reported as unrecomputable rather than as a number; and permutation nulls with the exact floor $1/\binom{n}{k}$ printed beside every interval. The scope experiment ships its own independent implementation of the same contract, and an assertion block that recomputes every quoted number from the raw result files and blocks assembly on a mismatch [ARTIFACT:art_fvWfzRrcoKux].

# Method

## The weights-only statistics and their independent reimplementation

The arm is motivated directly by abliteration's mechanism. If every residual-write matrix has had one direction projected out, that direction is a shared approximate null direction of the whole write ensemble and should be recoverable from the ensemble alone. Let $\mathcal{W}$ be the set of matrices writing into the residual stream (attention output projections and MLP down-projections) across all $L$ layers. Form

$$A \;=\; \sum_{W \in \mathcal{W}} \frac{W W^\top}{\lVert W \rVert_F^2}, \qquad \lambda_1 \le \lambda_2 \le \dots \le \lambda_d, \quad v_1 = \text{eigvec}(\lambda_1),$$

and define the per-matrix normalised write energy along a unit direction $u$ as $e_W(u) = \lVert u^\top W\rVert^2 / (\lVert W\rVert_F^2/d)$, which equals 1 in expectation for a random direction. The five statistics are $W01 = \log_{10}(\mathrm{median}(\lambda)/\lambda_1)$, the depth of the suppression; $W02 = \Pr_W[e_W(v_1) < 0.1]$, the fraction of write matrices in which $v_1$ is suppressed; $W03 = \log_{10}\!\big(q_{0.05}(e_W(u_{\text{rand}}))/\overline{e_W(v_1)}\big)$ against **256** matched random directions; $W04 = \log_{10}(\lambda_2/\lambda_1)$; and $W05 = \log_{10}\min_W e_W(v_1)$, the *minimum* per-layer energy — the statistic that asks whether the suppression holds in every layer without exception. $W06$–$W16$ are spectral and norm descriptors (stable rank, singular-value entropy, effective rank, singular-value decay, RMSNorm gain statistics, write-row-norm Gini); $W06$–$W09$ are formula-identical to two features of [8] and are cited to it here.

Two gates run before any panel measurement, and this iteration added a third. The **positive control** injects a synthetic rank-one edit $W \leftarrow W - rr^\top W$ into every write matrix of `Qwen/Qwen3-0.6B` — the instruct member, whose unedited $W01$ is 0.6239, not the Base member's 0.6281 — and requires recovery: obtained at $|\cos(v_1, r)| = 1.000000$, $W02$ from 0 to 1.00, $W01$ from 0.624 to 4.869. The **band-limited control**, editing only the middle third of layers, is *not* recovered ($W02 = 0.0$). The new gate is an **independent reimplementation**: `wstats.py` was written from the published formulae before the original implementation was read, and reproduces the archived $W05$ to $\max|\Delta W05| = 9.9\times10^{-6}$ over 10 re-downloaded members at their archived revisions, ordering preserved, Spearman 1.0000, bit-identical across two runs [ARTIFACT:art_fvWfzRrcoKux]. Two attributable divergences are reported rather than smoothed: $W01$ reproduces to $10^{-4}$ on non-abliterated members but drifts up to 0.048 on abliterated ones, because $\lambda_{\min}$ sits at the floating-point noise floor exactly where the scar is (float32 versus float64 Gram accumulation, not a load-dtype effect); and $W03$ differs systematically by $+0.015$ to $+0.034$ because the published formula takes the 5th percentile of the per-direction *mean* energy while the original code pools all (direction $\times$ matrix) energies first. They are two different statistics and we now say which is which.

## Recipe scope: what does the detector actually key on?

Architecture is not what $W05$ keys on; the edit recipe is. Three tests replace leave-one-architecture-family-out as the generalisation control. (i) **Leave-one-uploader-out**, refitting the decision threshold on the remaining uploaders. (ii) **Four real published $\leq$4.2B checkpoints from four unseen uploaders**, scored against the same 36 negatives. A Hub search over 7 queries and 70 card-verified candidates established the constraint that forced this design: mechanically different recipes — norm-preserving, multi-direction, biprojected — demonstrably exist, but every public instance is $\geq$14.9B, far above the ceiling that keeps the study CPU-feasible. A miss on a new uploader must therefore be disambiguated from an unedited re-upload, which `realcheck.py` does by computing $E_1$ against the declared parent at pinned revisions. (iii) **Twelve in-house synthetic variants** on two architectures — plain projection, norm-preserving, rank-$k$ for $k \in \{2,4,8\}$, per-head surgery on the top 25% of heads, and a contiguous **layer-fraction sweep** — each carrying a fluency check and a greedy harmful-refusal rate, so that "the edit worked" and "the edit is visible" stay separable.

## The laundering ladder and the wild scan

The deployment premise needs two things the previous draft did not have: an evasion arm and a real scan. For the first, a faithful diff-in-means abliteration of `Qwen/Qwen3-1.7B` is built in house and gated (it must reproduce the panel's weight signature *and* collapse harmful refusal *and* leave WikiText perplexity intact), then pushed through five laundering families at graded intensity: benign LoRA-SFT (25/50/100/200 steps, $r{=}16$, $\alpha{=}32$, merged), linear merge with the instruct parent ($w \in \{0.10, 0.25, 0.50, 0.75, 0.90\}$), int8/int4/nf4 round-trips, and an adversary who adds back an $\varepsilon$-scaled rank-one term — naively, along a random direction, to the argmin matrix only, to the $k$ smallest matrices, and to all matrices. At every stage both **flag strength** ($W01$–$W05$, plus a hardened $W05q10$ using the 10th percentile instead of the minimum) and **un-censoring strength** (harmful-refusal rate, XSTest over-refusal, WikiText perplexity, distinct-3) are measured. The load-bearing quantity is the *order of the two deaths* and the evasion cost, defined as the increase in harmful refusal paid at the intensity where the flag first dies.

Direction selection turned out to be a method result rather than a detail. Held-out harmful-versus-benign AUROC **saturates** and cannot select the refusal direction: on Qwen3-1.7B eleven layers score $\geq 0.997$ and four tie at exactly 1.000, so the argmax is decided by the tie-break. Selection is therefore behavioural, as in [1]: sweep every layer, score by refusal on a 10-prompt development subset disjoint from the evaluation core, tie-break on held-out AUROC, and reject any layer that breaks fluency (13 of 29 layers qualify at 1.7B). The AUROC-selected variant ships as a sensitivity row.

For the second, the scan runs entirely on stored tensors: safetensors are streamed, the write matrices are read directly without instantiating a model, $W01$–$W05$ are computed, and the snapshot is deleted before the next repository is fetched. No `transformers` model is built, no prompt is tokenised, no forward pass is run. Repositories already in P1 are excluded, and every checkpoint in the abliterated region or the warning band is adjudicated against its card and lineage with the evidence quoted.

## The behavioural battery, unchanged and re-analysed

The 53-metric battery (16 weights-only, 11 black-box, 26 activation-based including four declared-to-fail controls) is **not** rebuilt in this iteration. It is re-analysed in three ways the reviewer asked for. **Power**: the paired cluster bootstrap is simulated at 2,000 replications per point over a $\Delta\rho$ grid from 0.00 to 0.60 at 19 lineages, and the panel size required for 80% power is searched over 18–300 lineages. **Comparator**: the paired difference is reported against the *pre-specified* black-box metric with a published prior (B01, first-step logit gap [24]) as well as the post-hoc best-of-11 (B09, greedy refusal rate), and a selection-corrected variant re-argmaxes the black-box winner inside every resample and prices the optimism. **Reliability**: because per-item labels were never persisted, the frozen prompt folds are rebuilt, paired to the archived responses, and re-adjudicated verbatim under rubric B by an independent model, giving split-half reliability, item-level agreement and attenuation-corrected correlations. Separately, every depth-sensitive activation metric is recomputed at three relative depths spanning the saturated AUROC plateau — the bare argmax (0.143), mid-stack (0.500), and the previously pre-declared $\rho^\star = 0.679$ — producing 1,014 (member, metric, depth) rows [ARTIFACT:art_fvWfzRrcoKux].

# Results

## The scar is real, and it is bounded by recipe and by uploader

[FIGURE:fig2]

On the archived 44-checkpoint panel the weights-only arm separates abliterated checkpoints from everything else without a parent and without a prompt. The table below reports $[\min, \max]$ for **every** class, not only the positives, because the abliterated-only column materially understates the overlap present in the data.

| statistic | abliterated ($n{=}8$) | base ($n{=}16$) | instruct ($n{=}15$) | beh.-unc. ($n{=}4$) | safety-RL ($n{=}1$) | AUROC (oriented) |
|---|---|---|---|---|---|---|
| $W05$ min layer energy | $-4.33$ $[-4.82, -2.74]$ | $-1.31$ $[-2.67, -0.97]$ | $-1.15$ $[-1.59, -0.96]$ | $-1.08$ $[-1.17, -0.51]$ | $-1.25$ | **1.000** |
| $W01$ suppression depth | 4.26 $[1.44, 4.82]$ | 0.58 $[0.34, 1.99]$ | 0.47 $[0.34, 0.68]$ | 0.46 $[0.20, 0.68]$ | 0.47 | 0.986 |
| $W03$ gap vs 256 random | 4.28 $[1.40, 4.74]$ | 0.60 $[0.30, 2.00]$ | 0.49 | 0.47 | 0.49 | 0.986 |
| $W04$ isolation | 3.68 $[0.85, 4.19]$ | 0.057 $[0.004, 1.62]$ | 0.046 $[0.004, 0.21]$ | 0.055 | 0.004 | 0.986 |
| $W02$ direction consistency | 1.00 $[0.96, 1.00]$ | 0.20 $[0.00, 1.00]$ | 0.11 $[0.00, 0.41]$ | 0.066 | 0.18 | 0.950 |
| $A01$ AMS $\sigma$ (baseline) | 2.38 $[1.45, 4.82]$ | 1.72 | 2.74 $[1.40, 4.40]$ | 1.61 | 3.64 | 0.640 |

Three corrections to how this table was previously reported. First, $W05$'s "AUROC 1.000" is the **oriented** value: abliterated members sit at the *low* end, so the raw Mann-Whitney AUROC is 0.000, and the orientation was read off the data. Second, the other four statistics reach 0.986 (0.950 for $W02$, with 21 tied positive-negative pairs), not 1.000, and the ranges above show why — $W01$'s base maximum of 1.992 overlaps the abliterated minimum of 1.438 by 0.554, and $W02$'s base maximum is exactly 1.000, identical to the abliterated median, so no $W02$ threshold separates the panel at all. Third, the separating margin is 0.0763 in $\log_{10}$ units, between the *highest* abliterated value ($-2.7415$, `huihui-ai/Qwen2.5-0.5B-Instruct-abliterated`) and the *lowest* non-abliterated one ($-2.6652$, `allenai/OLMo-1B-hf`); the previous draft's "$-2.742$ against $-2.665$" paired the boundary correctly but described $-2.742$ as the abliterated minimum, which is its maximum (the true minimum is $-4.8204$). OLMo is a one-member architecture family, and the four checkpoints nearest the boundary are two abliterated members and two base models from single- or three-member families (olmo, gpt\_neox).

**The generalisation control was testing the wrong variable, and the right one fails.** All eight archived positives come from two uploaders running an all-layer global diff-in-means projection, so leave-one-architecture-family-out cannot speak to the question. Leave-one-**uploader**-out does [ARTIFACT:art_fvWfzRrcoKux]:

| held-out uploader | $n_+$ | rank-transfer AUROC | catch rate at refit threshold |
|---|---|---|---|
| huihui-ai | 6 | 1.000 $[1.000, 1.000]$ | 1.00 |
| Goekdeniz-Guelmez | 2 | 1.000 $[1.000, 1.000]$ | 1.00 |
| in-house synthetic | 12 | 0.926 $[0.782, 1.000]$ | 0.83 |
| BennyDaBall | 1 | 0.972 $[0.906, 1.000]$ | 1.00 |
| MagicalAlchemist | 1 | 0.306 $[0.171, 0.472]$ | 0.00 |
| prithivMLmods | 1 | 0.222 $[0.118, 0.364]$ | 0.00 |
| mlabonne | 1 | 0.028 $[0.000, 0.088]$ | 0.00 |

Scored as a group against the same 36 negatives, the four real new-uploader checkpoints give **AUROC 0.382** $[0.036, 0.949]$, permutation $p = 0.776$, catch rate 0/4 at the threshold fitted on the archived uploaders — against 1.000 and 1.00 for the archived positives. Their $W05$ values are $-0.964$ (`mlabonne/Qwen3-0.6B-abliterated`), $-1.010$ (`MagicalAlchemist/Qwen3-1.7B-Magic_decensored`), $-0.990$ (`prithivMLmods/VibeThinker-3B-heretic_decensored`) and $-2.161$ (`BennyDaBall/Qwen3-4b-Z-Image-Turbo-AbliteratedV1`), against an archived abliterated range of $-2.74$ to $-4.82$. This is not an unedited-re-upload artifact: all three with a resolvable parent are genuine near-rank-one edits by the parent-referenced statistic ($E_1 = 0.995, 0.995, 0.997$; relative Frobenius change 2.5–3.0%; 0% bit-identical matrices).

[FIGURE:fig3]

The synthetic ablation separates *which* mechanical property the detector needs. Norm-preserving, plain and rank-$k$ ($k \in \{2,4,8\}$) variants are all detected at AUROC 1.000; per-head surgery on the top 25% of heads is missed at 0.556 $[0.152, 0.923]$. The layer-fraction sweep is decisive: on **both** hosts the detection threshold sits at $f^\star = 1.00$ — only the fully global edit is visible. And inside that blind spot an edit can be fully effective: on Qwen3-1.7B a projection confined to the middle 50% of layers drives harmful refusal from 0.45 to 0.00, exactly matching the full-stack edit, while $W05$ moves from $-1.0098$ to $-1.0088$. A synthetic unit test explains the sharpness: with 4 of 12 matrices edited, $v_1$ is no longer the injected direction at all ($W02 = 0$), because the Gram pools every matrix. The blind spot is a threshold, not a ramp.

**The scope sentence the evidence supports**, generated from these numbers rather than asserted: $W05$ detects global all-layer single-direction and multi-direction projection-type abliteration, and norm-preserving and rank-$k$ variants of it, at AUROC $\geq 0.95$; it misses per-head surgery, any edit confined to a proper subset of layers, and — on this evidence — the same global recipe from three of four unseen uploaders. It is a recipe-class and calibration-class signal, not a detector for abliteration in general.

Two negatives from the previous iteration survive unchanged and are worth restating, because they bound what the arm can ever be. The four behaviourally-uncensored fine-tunes sit squarely inside the instruct distribution on every weights-only statistic ($W01$ median 0.463 against instruct 0.471; $W05$ median $-1.081$ against instruct $-1.155$) despite two of them complying with 51% and 84% of harmful requests — there is no rank-one scar to find. Qwen3-4B-SafeRL is likewise indistinguishable in the weights ($W01 = 0.471$, $W04 = 0.004$) while behaving very differently. **A weights-only test answers "has this checkpoint been directionally edited?", not "is this checkpoint safe?"**

## In the wild: zero false positives, and a flag that a quantizer erases for free

[FIGURE:fig4]

**The scan.** 250 sub-4B Hub checkpoints that declare no edit were attempted and 160 scored to completion; 81 were unresolvable (Conv1D-transposed GPT-2-style layouts, GPTQ/bitsandbytes-quantized weights, malformed configs), 8 skipped and 1 errored, and none of those is counted as scanned [ARTIFACT:art_gCgia-6VUZJb]. The result is **zero** hits inside the abliterated region ($W05 \leq -2.7415$): false-positive rate 0/160, Wilson 95% $[0, 0.023]$. Two repositories fall in the warning band — `rinna/japanese-gpt-neox-small` at $-2.614$ and `stabilityai/stablelm-3b-4e1t` at $-2.515$ — and both are adjudicated FALSE\_POSITIVE with quoted card evidence, and both belong to architecture families the panel barely covers, exactly where the boundary analysis above predicted false positives would concentrate. The positive control (8/8) and negative control (12/12) run through the identical code path. Audit cost: zero prompts, zero forward passes, median 7.0 s of CPU linear algebra per checkpoint (2.7 s on GPU at 1.7B). Against the string-match baseline our own harvest quantifies — 50.5% of self-declared edited repositories carry "abliterat" in their id — the scan's contribution is precisely the complement: it is the only instrument here that could in principle flag the other half, and on 160 undeclared repositories it flagged none, which we report as a specificity result and not as a discovery.

Only $W05$ earns that specificity. On the labelled control set $W05$ reaches sensitivity 1.000 / specificity 1.000 with 0 of 160 undeclared repositories flagged; $W01$, $W03$ and $W04$ sit at sensitivity 0.875, and $W02$ flags 23 of 160 undeclared repositories (14.4%), so its apparent robustness is a threshold that separates nothing. The hardened $W05q10$ (10th percentile instead of the minimum) keeps perfect specificity but drops to 0.875 sensitivity: hardening has a measured cost.

**The laundering ladder.** The in-house root is clean: `Qwen/Qwen3-1.7B` at harmful refusal 0.923 becomes 0.162 after abliteration, with $W01 = 4.571$, $W02 = 1.000$, $W05 = -4.592$ (squarely inside the abliterated region) and WikiText perplexity *unchanged* at 27.08 $\to$ 26.25. No stage in the 34-stage ladder tripped the fluency screen or the blanket-refuser rule.

| treatment family | verdict | flag dies at | un-censoring dies at | evasion cost |
|---|---|---|---|---|
| add-back, all matrices | EVADABLE | $\varepsilon = 0.10$ | $\varepsilon = 1.00$ | $-0.004$ |
| merge with instruct parent | EVADABLE | $w = 0.10$ | $w = 0.50$ | $+0.069$ |
| quantization round-trip | EVADABLE | 4-bit | never | $+0.075$ |
| add-back, $k$ smallest | EVADABLE | $k = 4$ | $k = 32$ | $+0.128$ |
| add-back, argmin only | NEITHER\_DIES | — | — | — |
| add-back, random direction | NEITHER\_DIES | — | — | — |
| LoRA-SFT, benign | NEITHER\_DIES | — | — | — |

The verdict is `SCAR_IS_CHEAPLY_EVADABLE`, and the cheapest successful evasion is not an attack at all. A plain **int4 round-trip** takes $W05$ from $-4.592$ to $-1.946$ — comfortably clean — at a harmful-refusal rate of 0.135, *below* the unlaundered root's own 0.162, with perplexity 37.7 against 26.25, well inside the fluency screen. nf4 gives $-2.126$ at refusal 0.237; int8 leaves the flag alive at $-3.980$. An ordinary deployment step erases the certificate for free, which is the single most consequential number in this paper for anyone who wanted to run this at hub scale.

Three results reverse pre-registered expectations, and all three cut in the detector's favour. (i) **The argmin attack fails.** $W05$ is a minimum over matrices, so a one-matrix patch was expected to defeat it; at $\varepsilon = 1.00$ it moves $W05$ only to $-3.080$ and never crosses. Abliteration suppresses all 56 write matrices roughly equally, so the minimum has 55 runners-up, and four matrices must be patched before the flag dies — and because $v_1$ is recomputed from the treated model, a local patch rotates the eigenvector and lifts *every* matrix's energy. A local edit has a global effect on the statistic. (ii) **Dense benign fine-tuning does not scrub the scar**: 200 LoRA steps move $W05$ only from $-4.592$ to $-4.381$ while *restoring* harmful refusal from 0.162 to 0.368 — the treatment expected to kill the flag is the one family that most clearly favours it. (iii) **$W05$ is not the most fragile of the five statistics** (survival 0.559 of non-broken stages against $W02$'s 0.647), which contradicts the intuition that a minimum must be the most brittle.

## What the parent-free constraint actually costs

[FIGURE:fig5]

$E_1 = \mathrm{mean}_m\,\sigma_1^2(\Delta W_m)/\sum_i\sigma_i^2(\Delta W_m)$, computed over write matrices in the 0.25$L$–0.75$L$ band (our reading of the incumbent's "mid-stack"), was run on every sibling pair the panel affords [ARTIFACT:art_fvWfzRrcoKux].

| matched subset | $n$ | $E_1$ AUROC (parent required) | $W05$ AUROC (parent free) | paired difference |
|---|---|---|---|---|
| 12 pre-declared pairs, calibration uploaders | 12 | 1.000 $[1.000, 1.000]$ | 1.000 $[1.000, 1.000]$ | $+0.000$ $[0.000, 0.000]$ |
| + 3 new-uploader pairs | 15 | 1.000 $[1.000, 1.000]$ | 0.833 $[0.556, 1.000]$ | $-0.167$ $[-0.444, 0.000]$ |
| + 26 synthetic pairs | 41 | 0.976 $[0.931, 1.000]$ | 0.790 $[0.593, 0.918]$ | $-0.186$ $[-0.382, -0.079]$ |

On the recipes and uploaders it was characterised on, **parent-free costs nothing**: a tie at 1.000, paired difference exactly zero. That is the strong sentence the reviewer asked us to earn, and we can only say it about the pre-declared subset. Adding three new-uploader pairs makes $E_1$ hold while $W05$ falls; the interval reaches zero at its boundary, so at $n = 15$ this is underpowered as an interval claim, but descriptively it is unambiguous — $E_1$ detects 3 of 3 and $W05$ detects 0 of 3. Including the synthetic pairs the difference does exclude zero, at $-0.186$.

The two are, however, **complementary rather than nested**: $E_1$ degrades badly on multi-direction edits (AUROC 0.17–0.67 for $k = 8 \ldots 2$) where $W05$ is perfect, and holds at 0.995 on the layer-band edits $W05$ cannot see at all. The right reading is not that the parent-requiring statistic dominates, but that the parent buys robustness to *who ran the edit* while the parent-free Gram statistic buys robustness to *how many directions were removed*. A deployable audit would run both where the parent exists and treat a $W05$ hit as sufficient but never necessary.

## The behavioural negative, now with a bound on what it can mean

[FIGURE:fig6]

Restricting to the 28 non-base members over 19 lineages for which a behavioural rate is meaningful — the previous draft said 26 over 18, and the recomputation gives 28 over 19; the two partitions (`member_class != base` and `renderer == chatml`) disagree on two checkpoints, and we now state which rule is applied — the ranking of metrics against measured harmful-refusal rate is:

| metric | arm | $\rho$ (member, $n{=}28$) | 95% CI | $\rho$ (lineage, $n{=}19$) |
|---|---|---|---|---|
| $A19$ refusal-axis / unembed cosine | activation | $+0.763$ | $[+0.592, +0.864]$ | $+0.800$ |
| $B01$ first-step logit gap (pre-specified) | black-box | $+0.708$ | $[+0.369, +0.901]$ | $+0.659$ |
| $A11$ prompt-position refusal log-odds | activation | $+0.702$ | $[+0.345, +0.892]$ | $+0.671$ |
| $B08$ first-token entropy asymmetry | black-box | $-0.672$ | $[-0.843, -0.373]$ | $-0.782$ |
| $B09$ greedy refusal rate (post-hoc winner) | black-box | $+0.670$ | $[+0.374, +0.883]$ | $+0.668$ |
| $A14$ generated-step refusal log-odds | activation | $+0.654$ | $[+0.291, +0.839]$ | $+0.550$ |
| $A02$ AMS concept cosine | activation | $+0.631$ | $[+0.212, +0.874]$ | $+0.573$ |
| $A01$ AMS $\sigma$ | activation | $+0.541$ | $[+0.148, +0.812]$ | $+0.569$ |

Four things follow, and each answers a specific critique.

**(a) The baseline was mis-described.** $B09$ is not the best black-box metric at either aggregation unit: $B08$ leads at lineage level ($|\rho| = 0.782$ against 0.668) and $B01$ at member level (0.708 against 0.670), and $B09$ is the in-resample argmax in only 11.2% (lineage) / 14.4% (member) of cluster resamples. The selection optimism of choosing best-of-11 on these data is $+0.182$. Correcting this **strengthens** the negative — the interior candidates trail an even stronger trivial baseline — but the sentence "$B09$, the best black-box baseline" was wrong and is withdrawn.

**(b) The paired comparison, against both a pre-specified and a post-hoc comparator.** At member level, $|\rho_X| - |\rho_{B09}|$: $A02$ $-0.038$ $[-0.327, +0.249]$; $A01$ $-0.162$ $[-0.494, +0.200]$; $\alpha_{50}$ $-0.151$ $[-0.694, +0.485]$; $W01$ $-0.265$ $[-0.659, +0.146]$; $W05$ $-0.419$ $[-0.735, +0.039]$; $W02$ $-0.457$ $[-0.736, -0.023]$. Against the pre-specified $B01$ the picture is the same and slightly worse for the interior ($A02$ $-0.076$ $[-0.553, +0.374]$; $W05$ $-0.457$ $[-0.763, -0.005]$). No interior metric's advantage has an interval excluding zero at either unit, against either comparator; two intervals exclude zero on the wrong side. Under the selection-corrected comparator, which re-argmaxes the black-box winner inside every resample, four of seven white-box candidates are *significantly worse* than the black-box arm.

**(c) The power the test actually had.** Simulating the same paired cluster bootstrap at 19 lineages, 2,000 replications per grid point, the **minimum detectable $|\Delta\rho|$ at 80% power is 0.32**; power is 0.012 at $\Delta\rho = 0.20$ and 0.70 at 0.30. Reaching 80% power would need roughly 50 lineages at $\Delta\rho = 0.30$, roughly 150 at 0.20, and no panel size up to 300 lineages suffices at 0.10. The falsifier *could* have failed: some advantage in the swept range does reach 80% power, so the negative carries information. The conclusion the data supports is therefore bounded, and we state it in that form: **at this panel size no interior metric shows an advantage over the best black-box baseline larger than about 0.3 in $|\rho|$; distinguishing smaller advantages would require roughly 150 lineages.** That is a very different sentence from "looking inside buys nothing", and it is the one we make.

**(d) Neither reliability nor depth explains the result.** Split-half reliability of the 40-item harmful-refusal rate, odd versus even items, Spearman-Brown corrected, is $r_{xx} = 0.968$ (0.978 from Pearson), so the attenuation correction is a factor of 1.016; no ordering moves and no paired difference changes sign. An independent adjudicator, itself validated 6/6 against the hand-labelled set, agrees with the archived judge at checkpoint-level Spearman 0.927 (mean absolute rate difference 0.112) while disagreeing sharply with the lexical screen ($\kappa = 0.403$ over 2,859 items; refusal share 0.428 against the screen's 0.190). The instrument is noisy against a substring screen and stable against itself. On depth, recomputing every depth-sensitive activation metric at 0.143, 0.500 and 0.679 over 26 members gives `BLACKBOX_WINS` at all three, so the falsifier is not a depth artifact [ARTIFACT:art_fvWfzRrcoKux]. That test needed the right statistic: four activation metrics have a *larger point estimate* than a baseline at $\rho^\star$ — $A19$ reaches $+0.770$ against $B09$'s $+0.766$ — but the paired lineage-bootstrap difference is $+0.0045$ $[-0.225, +0.260]$, and comparing point estimates alone would have called that a win. One decision-relevant side finding: $\alpha_{50}$'s ceiling censoring is strongly depth-dependent (25/26 censored at the bare argmax, 15/26 at 0.500, 19/26 at $\rho^\star$), so the previously pre-declared depth is not the one yielding the most usable values. Depth selection for an AUROC plateau and depth selection for steering headroom are different problems, and the previous iteration conflated them.

## Two dissociations, and an audit of our own claims

**Detection and control come apart at construction time.** Building the abliteration root exposed a dissociation sharper than the one we previously reported. Held-out harmful/benign AUROC saturates on Qwen3-1.7B — eleven layers $\geq 0.997$, four tied at exactly 1.000 — so the argmax is a tie-break. Both the AUROC-selected direction (layer 20) and the behaviourally-selected one (layer 18) reproduce the full weight signature; but the AUROC pick leaves harmful refusal at 0.333 against the behavioural pick's 0.162. Two directions indistinguishable on a detection metric differ twofold in how much they un-censor. At 0.6B the failure is starker: the argmax lands at block 1 and leaves refusal at the parent's value, untouched. **The weight scar and the un-censoring are dissociable at construction time**, which is the sharpest mechanistic statement this paper can make about why a structural certificate is not a safety score. It also independently corroborates the general detection-versus-control result of [7] in a setting where the "detector" is a weight statistic rather than a probe.

**The refusal-substring screen is a broken instrument.** In the ladder, the standard 12-substring screen from [1] reads exactly 0.000 refusal on every abliterated-derived stage where the judge reads 0.13–0.37, so the reported $\kappa \approx 0$ is the screen failing, not the judge; at the rate level the two correlate at $r = 0.952$ across 34 stages. The previous iteration measured the same failure in a steering sweep (regex 0.01 against judge 0.85 on an abliterated Qwen3-0.6B). Any result of the form "model X cannot be made to refuse" that rests on a substring screen should be re-derived semantically before it is believed.

**A self-audit of the previous draft.** A dedicated re-analysis recomputed every number the previous draft quoted [ARTIFACT:art_0T8jhUa0zxmu] and found one systematic error and two mislabelled quantities. Four values presented as *correlations* of a white-box metric with ground truth — $A01$ $-0.161$, $A02$ $+0.036$, $W01$ $-0.373$, $\alpha_{50}$ $-0.453$ — are in fact **paired differences** $|\rho_X| - |\rho_{B09}|$ computed on a 26-member `renderer == chatml` subset rather than the 28-member non-base subset the draft stated. Read as correlations they are wrong by up to 0.67 and one has the wrong sign; read as paired differences on that subset, three of the four reproduce to four decimals. The arithmetic was never wrong; the labels were, and no artifact recorded either the quantity or the subset. Both readings are now published, and the falsifier is re-run on the draft's own subset: the verdict is unchanged on both. Of 54 checked disagreements between the draft and the recomputation, 32 match, 20 differ because the recomputation uses a stated method the draft did not state, and 2 are transcription errors.

**"Pre-registered" is now reserved for what is actually stamped.** The frozen `metric_spec.py` (sha256 `544ff994…`, verified) declares 53 metrics with family, prompt requirement, declared forward passes and declared wall-clock, plus the held-out split's seed and fraction — **and nothing else**. It contains no falsifier, no analysis plan, no base-model exclusion rule, no bootstrap specification, no white-box shortlist and no designated black-box baseline. Mapping every "pre-registered" claim in the previous draft to the artifact and line that records it gives **4 SUPPORTED, 2 PLAN-ONLY, 6 UNSUPPORTED**. The blanket-refuser threshold and the split seed are genuinely pre-specified but belong to the *dataset* artifact; the falsifier, the exclusion rule, the bootstrap and the comparator choice were analysis-time conventions and are worded as such throughout this paper. The judge rubric was mandated by the plan, failed an instrument check, and was replaced — a deviation, recorded as one.

# Discussion

**What a single checkpoint's tensors do and do not reveal.** A directional weight edit is a structural change and leaves a structural trace: the projection removes one direction from every write matrix simultaneously, and that simultaneity is the whole signal — $W05$, a minimum over layers, works precisely because a genuine all-layer abliteration admits no exception. The four measurements of this paper are best read as mapping the exact region in which that logic holds. It holds across architectures (leave-one-family-out is near-perfect on the three families with positives), across two projection recipes, across norm-preserving and rank-$k$ variants, against 160 undeclared Hub checkpoints with zero false positives, and against 200 steps of benign fine-tuning. It fails the moment the edit is not global (a middle-50% projection is behaviourally indistinguishable from the full edit and statistically invisible), when the edit is per-head, when the checkpoint is quantized to 4 bits, when it is merged even 10% back toward its parent — and, most importantly for anyone tempted by the AUROC, when the *same* recipe comes from an uploader whose calibration the threshold was not fitted on. The defensible product claim is a free, prompt-free certificate of an unlaundered global directional edit, with all four failure modes measured. That is smaller than we hoped one iteration ago and considerably more useful than an unqualified AUROC of 1.000, because a screen's value at hub scale is set by its false-negative structure, not by its separation on the panel that defined it.

**Why the parent-free constraint is still worth paying for.** The head-to-head is the cleanest way to price it. On matched pairs from the uploaders both methods were characterised on, parent-free costs exactly nothing (1.000 versus 1.000). What it costs is generalisation to new calibration regimes, and what it buys is (i) immunity to a spoofed reference, which the parent-requiring incumbent names as its own primary attack, (ii) applicability to the 23.4% of self-declared edited Hub repositories that name no mechanism and the majority that name no parent, and (iii) robustness to multi-direction edits, on which $E_1$ degrades to 0.17–0.67 while $W05$ is perfect. The two statistics fail on disjoint sets, which argues for running both rather than choosing.

**The behavioural negative, stated at the strength the data supports.** It would have been easy to report the best of 53 metrics against behaviour and call it a method. The discipline that prevented that also has to be applied to the negative itself, and doing so changes it: with a minimum detectable paired difference of 0.32 at 19 lineages, "no interior metric beats the black-box baseline" cannot be distinguished from "we cannot resolve an advantage smaller than 0.3". What the data does support is that greedy refusal rate on harmful prompts — and, better still, first-token entropy asymmetry — is an extremely cheap partial benchmark run, and a partial benchmark run predicts a full one well. We explicitly do not claim that weight geometry carries no behavioural signal: Paul reports $\rho = 0.72$ between a weight-space drift probability and harmful compliance over 24 manufactured adapters with a 50–2000-step dose ladder on a single base model [8], a regime our panel does not contain. Our panel's behaviourally-uncensored members were made by ordinary SFT with no directional edit and no dose ladder, so a low-rank spectral signal is not merely undetected but absent by construction.

**Limitations.** (1) The scar is recipe- and calibration-bounded, as measured above; three of four unseen uploaders running the same nominal recipe escape it. (2) It is cheaply evadable by an ordinary int4 round-trip, so it certifies an *unlaundered* edit and nothing more; we did not test whether a hardened variant computed on dequantized weights recovers the signal. (3) Public mechanically-different recipes (ORBA, MPOA, Heretic, OBLITERATUS multi-direction) exist at 4B on the panel's own Qwen3-4B family but were not measured here — the Hub search that established the $\geq$14.9B constraint predates their identification — and reflection-type ORBA is the sharpest outstanding falsification target, because a Householder reflection flips the component along $u$ instead of removing it and preserves $\lVert w \rVert$ exactly, leaving no null direction for $W05$ to find. (4) The wild scan covers 160 checkpoints in 7 architecture-family neighbourhoods; both warning-band repositories lie in families the panel barely covers, and the false-positive rate outside the tested architectures is unmeasured. (5) $n_{\text{abliterated}} = 8$ on the archived panel, and the separating margin is 0.0763 in $\log_{10}$ units, carried by two individual checkpoints. (6) Ground truth is 97% self-measured, judge-derived, and bounded by 40 harmful and 25 XSTest-safe items per member (binomial SE $\approx 0.08$ at $p = 0.5$), although split-half reliability of 0.968 shows the aggregate rate is stable. (7) The behaviour arm is 28 members over 19 lineages with 11 singletons, which is the power limit quantified in §5.4. (8) One adjacent work (Coslett 2026, Zenodo) remains unread after six access routes returned HTTP 403 or were unreachable; on the only reachable characterisation its signal is an activation-geometry fingerprint anchored to a claimed identity, so the risk to our novelty claim is bounded but open.

**What we would do next.** Three things follow directly. First, measure $W05$ on the four public sub-4.2B Qwen3-4B-family checkpoints produced by MPOA, Heretic and OBLITERATUS, and on an in-house ORBA reimplementation, which turns the signed prediction table into a result and would settle whether the uploader effect is really a hidden recipe effect. Second, replace the global minimum with a sliding-layer-window profile: the band-limited blind spot is a threshold artifact of pooling every matrix into one Gram, and a per-band eigen-analysis should recover exactly the edits that are currently invisible while remaining prompt-free. Third, test the black-box result where it should break, on checkpoints tuned to refuse benchmark items specifically; a metric that reads the interior has a principled reason to survive that attack, and no panel we have contains such an adversarial checkpoint.

# Conclusion

We asked whether a checkpoint's safety provenance can be read from its tensors alone — no parent, no reference, no prompt, no forward pass — and this iteration answers by measuring the boundary rather than the peak. Inside the boundary the answer is a clear yes and the economics are hard to beat: the minimum per-layer write energy along the minimum eigenvector of the pooled write Gram matrix separates the archived positives at oriented AUROC 1.000, ties the parent-requiring incumbent at 1.000 on 12 matched sibling pairs while needing no parent, survives 200 steps of benign fine-tuning and a single-matrix adversarial patch, and returns zero false positives over 160 undeclared Hub checkpoints at 7.0 s of CPU each. Outside it the answer is no, in four specific and measured ways: an edit confined to the middle 50% of layers is fully effective behaviourally and statistically invisible; per-head surgery is missed; a plain int4 round-trip erases the flag at *lower* harmful refusal than the unlaundered original; and three of four unseen uploaders running the same nominal recipe are not caught. The claim we can defend is therefore a free, prompt-free certificate of an unlaundered global directional edit — a provenance signal with a mapped evasion surface, not a safety score. Alongside it, the behavioural negative is restated at the strength the design supports: at 19 lineages the minimum detectable paired difference is 0.32, so what we have shown is that no interior observable beats a trivial black-box baseline by more than about 0.3 in $|\rho|$, and that resolving anything smaller needs roughly 150 lineages. Finally, an audit of our own previous round relabels four quoted values, corrects the identity of the best black-box baseline, and reduces twelve "pre-registered" claims to four. The useful single-checkpoint question is not "is this model safe" but "has this model been edited, and by whom, and has anyone cleaned up afterwards" — and only the first two thirds of that question currently have a free answer.

# References

[1] A. Arditi, O. Obeso, A. Syed, D. Paleka, N. Panickssery, W. Gurnee, and N. Nanda. Refusal in Language Models Is Mediated by a Single Direction. *NeurIPS*, 2024. arXiv:2406.11717.

[2] J. Hurtado. Has This Checkpoint Been Abliterated? A Two-Signal Audit and Its Failure Map. *arXiv:2607.01854*, 2026.

[3] G. Messenger. Detecting Safety Training Modification in Language Models via Activation Analysis. *IEEE Access*, 14:91723–91737, 2026. arXiv:2608.05578.

[4] C. Huang, Y.-L. Chen, C.-M. Yu, and W.-B. Lee. RAS: Measuring LLM Safety Through Refusal Alignment. *arXiv:2606.25750*, 2026.

[5] S. Peng, P.-Y. Chen, M. Hull, and D. H. Chau. Navigating the Safety Landscape: Measuring Risks in Finetuning Large Language Models. *NeurIPS*, 2024. arXiv:2405.17374.

[6] S. Basu, S. Y. Patel, P. Sheth, B. Muralidharan, N. Elamaran, A. Kinra, J. Morgan, and R. Batniji. Interpretability without actionability: mechanistic methods cannot correct language model errors despite near-perfect internal representations. *arXiv:2603.18353*, 2026.

[7] M. Galeone et al. Perfect Detection, Failed Control: The Geometry of Knowing vs. Steering in Language Models. *arXiv:2606.24952*, 2026.

[8] A. Paul. Spectral Geometry of LoRA Adapters Encodes Training Objective and Predicts Harmful Compliance. *arXiv:2604.08844*, 2026.

[9] Z. Zhong and A. Raghunathan. Watch the Weights: Unsupervised monitoring and control of fine-tuned LLMs. *arXiv:2508.00161*, 2025.

[10] Detecting Backdoored LoRAs from Weights Alone. *arXiv:2602.15195*, 2026.

[11] elder-plinius et al. OBLITERATUS: one-click model liberation toolkit, including `obliteratus/analysis/spectral_certification.py`. Software, AGPL-3.0, first public 2026-03-04.

[12] `reverse-abliterate` 0.1.2. Software package: metadata- and filename-based abliteration scanner.

[13] M. Labonne. Uncensor any LLM with abliteration. Hugging Face community blog, 13 June 2024.

[14] P. Weidmann. Heretic: fully automatic censorship removal for language models. Software, 2025–2026.

[15] J. W. Lai (grimjim). Norm-Preserving Biprojected Abliteration (MPOA). Hugging Face community blog, 6 November 2025.

[16] J. W. Lai (grimjim). ORBA: Orthogonal Reflection Bounded Ablation. Hugging Face community blog, 25 March 2026.

[17] Gabliteration: Adaptive Multi-Directional Neural Weight Modification. *arXiv:2512.18901*, 2026.

[18] J. Young et al. Comparative Analysis of LLM Abliteration Methods: A Cross-Architecture Evaluation. *arXiv:2512.13655*, 2025.

[19] S. Jain, E. S. Lubana, K. Oksuz, T. Joy, P. H. S. Torr, A. Sanyal, and P. K. Dokania. What Makes and Breaks Safety Fine-tuning? A Mechanistic Study. *NeurIPS*, 2024. arXiv:2407.10264.

[20] B. Wei, K. Huang, Y. Huang, T. Xie, X. Qi, M. Xia, P. Mittal, M. Wang, and P. Henderson. Assessing the Brittleness of Safety Alignment via Pruning and Low-Rank Modifications. *ICML*, 2024. arXiv:2402.05162.

[21] H. Lu et al. AlphaPruning: Using Heavy-Tailed Self-Regularization Theory for Improved Layer-wise Pruning of Large Language Models. *NeurIPS*, 2024. arXiv:2410.10912.

[22] H. Shairah et al. An Embarrassingly Simple Defense Against LLM Abliteration Attacks. *arXiv:2505.19056*, 2025.

[23] J. Fafula. Abliteration Is Not a Scalpel: Off-Target Effects of Refusal Removal on Decision Disposition Across Model Families. *arXiv:2607.17427*, 2026.

[24] T. Li and Y. Liu. Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness. *arXiv:2506.24056*, 2026.

[25] A. Korznikov, A. Galichin, A. Dontsov, E. Rogov, I. Oseledets, and E. Tutubalina. The Rogue Scalpel: Activation Steering Compromises LLM Safety. *arXiv:2509.22067*, 2026.

[26] B. Taimeskhanov, S. Vaiter, and D. Garreau. Towards Understanding Steering Strength. *ICML*, 2026. arXiv:2602.02712.

[27] S. Gadgil, T. Lin, and K. Lee. Where to Steer: Input-Dependent Layer Selection for Steering Improves LLM Alignment. *arXiv:2604.03867*, 2026.

[28] T. Chang, T. Schnabel, A. Swaminathan, and J. Wiens. A Course Correction in Steerability Evaluation: Revealing Miscalibration and Side Effects in LLMs. *arXiv:2505.23816*, 2025.

[29] A. Hasan and S. Biswas. The Refusal-Compliance Tradeoff: A Large-Scale Safety Behavior Audit of Large Language Models. *arXiv:2605.05427*, 2026.

[30] A. Zou, Z. Wang, N. Carlini, M. Nasr, J. Z. Kolter, and M. Fredrikson. Universal and Transferable Adversarial Attacks on Aligned Language Models. *arXiv:2307.15043*, 2023.

[31] P. Chao et al. JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models. *NeurIPS Datasets and Benchmarks*, 2024. arXiv:2404.01318.

[32] M. Mazeika et al. HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal. *ICML*, 2024. arXiv:2402.04249.

[33] P. Röttger, H. R. Kirk, B. Vidgen, G. Attanasio, F. Bianchi, and D. Hovy. XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models. *NAACL*, 2024. arXiv:2308.01263.

[34] S. Han et al. WildGuard: Open One-Stop Moderation Tools for Safety Risks, Jailbreaks, and Refusals of LLMs. *NeurIPS Datasets and Benchmarks*, 2024. arXiv:2406.18495.

[35] L. Zheng et al. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *NeurIPS*, 2023. arXiv:2306.05685.

[36] T. Xie et al. SORRY-Bench: Systematically Evaluating Large Language Model Safety Refusal Behaviors. *ICLR*, 2025. arXiv:2406.14598.

[37] Y. Zeng et al. AIR-Bench 2024: A Safety Benchmark Based on Risk Categories from Regulations and Policies. *arXiv:2407.17436*, 2024.

[38] L. Li et al. SALAD-Bench: A Hierarchical and Comprehensive Safety Benchmark for Large Language Models. *ACL Findings*, 2024. arXiv:2402.05044.

[39] L. Sun et al. TrustLLM: Trustworthiness in Large Language Models. *ICML*, 2024. arXiv:2401.05561.

[40] H. Zhao et al. Qwen3Guard Technical Report. *arXiv:2510.14276*, 2025.

[41] A. Yang et al. Qwen3 Technical Report. *arXiv:2505.09388*, 2025.

[42] L. B. Allal et al. SmolLM2: When Smol Goes Big — Data-Centric Training of a Small Language Model. *arXiv:2502.02737*, 2025.

[43] S. Biderman et al. Pythia: A Suite for Analyzing Large Language Models Across Training and Scaling. *ICML*, 2023. arXiv:2304.01373.

[44] A. Dubey et al. The Llama 3 Herd of Models. *arXiv:2407.21783*, 2024.

[45] G. Ilharco, M. T. Ribeiro, M. Wortsman, S. Gururangan, L. Schmidt, H. Hajishirzi, and A. Farhadi. Editing Models with Task Arithmetic. *ICLR*, 2023. arXiv:2212.04089.

[46] Y. Li, H. Hu, J. Sang, Y. Ma, X. Nie, Q. Zhang, Y. Yu, J. Su, Y. Huang, and J. Zhou. Prefill-level Jailbreak: A Black-Box Risk Analysis of Large Language Models. *arXiv:2504.21038*, 2025.

[47] G. Chen, T. Xia, H. Jia, C. Li, P. Torr, and J. Gu. LLM Jailbreak Detection for (Almost) Free! *arXiv:2509.14558*, 2026.

[48] B. Candogan, Y. Wu, E. Abad Rocamora, G. Chrysos, and V. Cevher. Single-pass Detection of Jailbreaking Input in Large Language Models. *TMLR*, 2025. arXiv:2502.15435.

[49] V. Siu, N. Crispino, J. Park, Z. Henry, D. Wang, Y. Liu, D. Song, and C. Wang. SteeringSafety: Benchmarking Representation Steering in LLMs Across Safety Perspectives. *arXiv:2509.13450*, 2026.

[50] A. Mishra, D. Khashabi, and A. Liu. Steered LLM Activations are Non-Surjective. *arXiv:2604.09839*, 2026.

</current_paper>

<reviewer_feedback>
Paper reviewer feedback from the previous iteration. Your strategy MUST address these critiques.
Prioritize major issues — these are the most impactful improvements to make.

- [MAJOR] (evidence) The paper's sharpest claim -- that the detector collapses on 'the *same* global recipe from four unseen uploaders' (AUROC 0.382, catch rate 0/4), framed throughout as an uploader/calibration effect -- is contradicted by the paper's own artifact. In results/arm1_real.jsonl all four rows carry recipe_class = 'global_diff_in_means' and mechanically_different = false, but the verbatim card evidence stored in those same rows says otherwise: MagicalAlchemist/Qwen3-1.7B-Magic_decensored is 'made using Heretic v1.1.0' with direction_index = 17.89 and attn.o_proj.max_weight = 0.84, and prithivMLmods/VibeThinker-3B-heretic_decensored is 'modified using the Heretic abliteration toolkit'. I fetched the third card: mlabonne/Qwen3-0.6B-abliterated states that the subtraction weight factors 'follow a normal distribution with a certain spread and peak layer'. Heretic is recipe [14] in the paper's own taxonomy (per-component optimised kernel, float direction index, weights that are not 1) and mlabonne v2 is recipe [13] (Gaussian depth kernel) -- both are explicitly *not* the uniform all-layer projection the archived positives use. So at least three of the four misses are depth-weighted or sub-unit-weight kernels, and the finding is a recipe effect, not an uploader effect. This also explains why E1 = 0.995-0.997 on all three: the per-matrix delta is still near rank one, but the annihilation is incomplete in some layers, which is precisely what a minimum-over-layers statistic cannot survive. Compounding this, limitation (3) claims a Hub search 'established the >=14.9B constraint' for mechanically different recipes, while the paper's own cited prior-art artifact art_sHF0cggp2IvT states that MPOA, Heretic and OBLITERATUS all have public sub-4.2B checkpoints at 4,022,468,096 parameters on the panel's own Qwen3-4B family -- and the experiment measured two Heretic checkpoints without recognising them.
  Action: Re-derive recipe_class for all four checkpoints from their cards (quote the Heretic parameter table and mlabonne's normal-distribution sentence in the text), correct the arm1_real.jsonl labels and the mechanically_different flag, and re-run the grouping analysis with RECIPE as the primary variable and uploader as a secondary one. Then rewrite the headline in the Introduction, Contributions, Discussion and Conclusion from 'three of four unseen uploaders running the same nominal recipe escape' to the mechanism the data actually support: 'W05 requires a uniform, complete annihilation in every layer; any depth-weighted or sub-unit-weight kernel (mlabonne v2 Gaussian, Heretic per-component optimised) escapes it, exactly as a band-limited edit does.' Fold this into the f* = 1.00 layer-fraction result as one unified statement about uniformity rather than two separate mysteries. Finally, delete or correct limitation (3)'s >=14.9B claim, which your own research artifact refutes, and add the sub-4.2B MPOA/OBLITERATUS Qwen3-4B checkpoints. This change costs almost no new compute and materially strengthens the paper.
- [MAJOR] (evidence) The flagship deployment number -- '0 of 160 undeclared sub-4B Hub checkpoints, Wilson 95% [0, 0.023]' -- rests on a population that does not match its description. Reading results/scan.jsonl, 44 of the 160 scored repositories are degenerate: roughly 30 unit-test fixtures with hidden_size = 8 and n_layers = 2 (trl-internal-testing/tiny-*, peft-internal-testing/tiny-dummy-qwen2, llamafactory/tiny-random-*, echarlaix/tiny-random-*, yujiepan/llama-2-tiny-random, MaxJeblick/llama2-0b-unit-test, hmellor/tiny-random-*), plus three single-layer EAGLE3 speculator draft heads (RedHatAI/Qwen3-8B-speculator.eagle3, lightseekorg/kimi-k2.6-eagle3-mla, Inferact/MiniMax-M3-EAGLE3), plus several sub-30MB toys. A statistic defined as a minimum of per-layer write energy over an eigenvector of a pooled Gram matrix is not meaningfully defined on a two-layer, eight-dimensional random stub, and a one-layer draft head has a single term in the minimum. These repositories entered because scan_enumeration.json ranks candidates by descending downloads, and CI fixtures are among the most-downloaded objects on the Hub. The same ranking admitted lmstudio-community/Qwen2.5-Coder-14B-Instruct-MLX-4bit (8.3 GB of tensors, 48 layers) into a set the paper calls 'sub-4B'. Ornith-1.0-35B and -9B were caught only by a byte cap, not by the parameter filter, because the Hub's reported param counts for those repos are wrong -- a bug the authors' own dataset artifact documents.
  Action: Define an eligibility rule before reporting the rate -- e.g. n_layers >= 8, hidden_size >= 128, tensor_bytes consistent with <= 4.2B parameters at the declared dtype, and exclude repos whose card or tags identify them as test fixtures, speculator/draft heads, or quantized re-uploads -- and report the false-positive rate and Wilson interval on that filtered denominator as the primary number, with the raw 0/160 as a secondary row. State the eligible-population composition explicitly (a small table of model_type x count would do). Also add one sentence to Method noting that the statistic is undefined or degenerate below some layer count, and give that floor.
- [MAJOR] (rigor) The laundering ladder's behavioural axis is reported without any uncertainty, and the two numbers the paper stakes its most consequential claim on are inside the noise. Every stage in results/ladder.jsonl scores n_harmful = 40 items (achieved denominators 34-40 after parse drops), so a refusal rate has a binomial SE of about 0.075 at p = 0.2. The paper reports 'the cheapest successful evasion ... an evasion cost of -0.004' (add-back-all at eps 0.10: 0.158 vs the root's 0.162) and 'int4 ... at a harmful-refusal rate of 0.135, *below* the unlaundered root's own 0.162', and calls the latter 'the single most consequential number in this paper'. Differences of 0.004 and 0.027 on a 40-item instrument are not resolvable, and the paper elsewhere (Sec. 5.4, limitation 6) correctly notes the binomial SE of ~0.08 -- so the ladder section is inconsistent with the paper's own stated instrument precision. The qualitative ordering is fine and is the real result (W05 crosses the boundary at eps 0.10 and at 4-bit while refusal is still around 0.15, versus 0.95 at eps 1.00 and 0.85 at k = 32), but the decimal framing invites an easy attack.
  Action: Add Wilson or bootstrap intervals to every harmful-refusal rate in the ladder table and figure, and restate the crossing findings as ordering statements with the interval overlap made explicit: 'at the intensity where the flag first dies, harmful refusal is statistically indistinguishable from the unlaundered root (0.158 [0.07, 0.31] vs 0.162 [0.07, 0.32])'. Drop the signed 'evasion cost' to one significant figure or replace it with the interval on the difference. Separately, note that int4's WikiText perplexity rises 26.25 -> 37.7 (+43%), so 'for free' overstates: the fluency screen is distinct-3, not perplexity, and a 43% perplexity cost is a real quality cost a deployer would notice.
- [MAJOR] (scope) The quantization result is framed as a detector failure ('a plain int4 round-trip erases the flag'), but on the paper's own scanning pipeline a 4-bit checkpoint is not a false negative -- it is unreadable. The scan reports 81 UNRESOLVED repositories whose stated causes include 'GPTQ/bitsandbytes-quantized weights', i.e. the operational outcome of the cheapest evasion is that the checkpoint falls outside the instrument's domain entirely and is never scored. That is a materially different (and, for a deployed screen, more tractable) failure mode than a clean checkpoint scoring clean, because 'unscannable' is itself an auditable signal and because dequantizing before scanning is an obvious mitigation the paper explicitly did not test (limitation 2). As written, the Introduction, Results and Conclusion all present int4 as evasion, which overstates the adversary's win and understates the paper's own remedy.
  Action: Split the quantization finding into two clearly separated claims: (a) a dequantized int4 round-trip of an abliterated model scores clean on W05 while remaining un-censored (the measured result), and (b) in the wild-scan pipeline a quantized upload is UNRESOLVED rather than clean, so at hub scale the operational effect is refusal-to-score, not a false negative. Then run the cheap follow-up you already flag: recompute W01-W05 on the int4 stage after dequantizing to fp16 and report whether the scar returns. If it does, the limitation shrinks from 'cheaply evadable' to 'requires dequantization before scoring', which is a much better sentence and is one afternoon of work on tensors you already have.
- [MINOR] (novelty) One directly relevant piece of community prior art is uncited. Abliterlitics (github.com/dreamfast/abliterlitics, with published per-model reports at abliterlitics.dev) is an open-source 'abliteration forensics' toolkit whose Weight Analysis axis performs SVD decomposition, effective-rank and energy spectra, edit-vector fingerprints, subspace alignment, low-rank reconstruction and per-layer magnitude profiles, and which publishes side-by-side comparisons of Heretic vs Huihui vs HauhauCS techniques on shared bases (Qwen3.5-9B, Qwen3.5-27B, Gemma4-e2b and others). It requires a base model plus variants in a comparison directory, so it is parent-requiring and does not threaten this paper's parent-free novelty claim -- but the paper already goes out of its way to enumerate community practice (OBLITERATUS, reverse-abliterate) and this is a closer instance of weight-spectral abliteration forensics than either. Its published technique fingerprints are also directly usable evidence for the recipe-boundary question raised in my first critique.
  Action: Cite Abliterlitics in the 'parent-free spectral inspection is already community practice' paragraph, note explicitly that it requires the parent (which sharpens rather than blunts your claim), and if any of its published cross-technique reports overlap your recipe taxonomy, cite the specific fingerprint differences between Heretic and Huihui edits as independent external support for the uniform-versus-depth-weighted distinction.
- [MINOR] (methodology) The E1 head-to-head, which is now one of the paper's best results, rests on an unstated reading of the incumbent's specification. The paper and results/arm2.json both record the 0.25L-0.75L band as 'our reading of mid-stack' because the source is not numerically specific, and this choice is never varied. Since E1's advantage over W05 on the new-uploader pairs (-0.167 [-0.444, 0.000]) is the quantity that licenses the 'complementary rather than nested' conclusion, a reader cannot tell how much of it depends on the band. The synthetic-pair result (-0.186 [-0.382, -0.079]) is the only interval excluding zero and it is driven by 26 in-house synthetics whose construction the authors control.
  Action: Report E1 at three bands (0.25-0.75L as primary, full stack, and 0.4-0.6L) and state whether the paired difference and the 'complementary failure modes' conclusion are invariant. This is pure re-analysis of deltas already computed. If the conclusion moves, say so; if not, one sentence retires the objection.
- [MINOR] (rigor) The archived-panel separation remains thin in a way the paper acknowledges but does not fully propagate. n_abliterated = 8 from 2 uploaders, the separating margin is 0.0763 log10 units between two individual checkpoints (huihui-ai/Qwen2.5-0.5B-Instruct-abliterated at -2.7415 and allenai/OLMo-1B-hf at -2.6652), and the boundary threshold used by the wild scan is that same panel-derived value. In the scan the two nearest non-abliterated neighbours (rinna/japanese-gpt-neox-small at -2.614, stabilityai/stablelm-3b-4e1t at -2.515) sit within 0.13 and 0.23 of the operating threshold, i.e. within about two margin-widths. The threshold is therefore fitted on 44 checkpoints and deployed on a population two orders of magnitude larger with no held-out calibration, and the paper does not report how the 0/160 result varies with the threshold.
  Action: Report the wild-scan hit count as a function of the threshold over a range spanning the margin (e.g. -2.4 to -3.0 in steps of 0.1) so the reader can see how brittle 0/160 is, and give the smallest threshold shift that would produce a first false positive. Add one sentence stating that the threshold is panel-fitted and never validated out of panel, which is the honest form of the specificity claim.
- [MINOR] (clarity) Several small text-to-artifact mismatches remain, and in a paper whose credibility argument is fidelity these are disproportionately costly. (a) The Panel section calls P3 '250 attempted / 160 successfully scored sub-4B Hub checkpoints'; scan.jsonl holds 270 rows of which 20 are labelled controls, and one of the 160 is a 14B model. (b) The paper says '81 were unresolvable ... 8 skipped and 1 errored' which reconciles to 250, but the experiment artifact's own summary says '65 UNRESOLVED', so one of the two is stale. (c) The Method says the positive control was injected into 'Qwen/Qwen3-0.6B -- the instruct member, whose unedited W01 is 0.6239, not the Base member's 0.6281', which is now correct, but the same paragraph then reports W01 going to 4.869 while Sec. 5.1 reports an abliterated W05 extreme of -4.82; these unrelated quantities sharing a numeral still read as a typo, as flagged last round.
  Action: Do one mechanical reconciliation pass generating the Panel and Sec. 5.2 counts from scan.jsonl rather than transcribing them, print the control/non-control split explicitly, fix the 65-vs-81 discrepancy in whichever artifact is stale, and reword so the 4.869 and -4.82 values are not adjacent.
- [MINOR] (methodology) The behavioural negative's power analysis is a real improvement, but the reported bound is stated only in terms of the paired difference and not in terms of what a practitioner would want to know. 'No interior metric beats the best black-box baseline by more than about 0.3 in |rho|' is correct but leaves open whether the interior metrics are individually useful. A19 reaches rho = +0.763 [+0.592, +0.864] at member level and +0.800 at lineage level -- comparable to B01 and better than B09 -- so the paper's own table shows that an activation observable predicts harmful-refusal rate about as well as a partial benchmark run, at a cost the paper never states in the same units (forward passes, prompts) as the black-box baseline it loses to.
  Action: Add a two-column cost annotation to the Sec. 5.4 table (prompts required, forward passes required, wall-clock) so the reader can see that the falsifier is about *marginal value over a cheaper instrument*, not about whether interior observables carry signal. Then state the practitioner-facing conclusion directly: interior observables are predictive but do not beat a 40-prompt greedy refusal rate, which is itself already the cheapest thing anyone would run.
- [MINOR] (scope) The laundering ladder generalises from a single in-house abliteration of one model (Qwen3-1.7B, one direction, one selection rule). The evasion thresholds reported as headline results -- flag dies at eps = 0.10, at merge w = 0.10, at 4-bit, at k = 4 -- are single-model, single-recipe point estimates presented as properties of the statistic. Because the paper's central scope finding is that the statistic's behaviour depends strongly on the edit's uniformity, the ladder thresholds are plausibly recipe-dependent too: a Heretic-style non-uniform root would presumably start closer to the boundary and die sooner.
  Action: Repeat the three cheapest ladder families (merge, quantization, add-back-all) on at least one second root -- ideally an in-house Heretic-style depth-weighted edit and one on a different architecture (the Llama-3.2-1B-Instruct host is already in your arm-1 code path) -- and report whether the crossing intensities move. Even a single extra root converts 'the flag dies at w = 0.10' from an anecdote into a range.
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

### [2] HUMAN-USER prompt · 2026-08-13 23:44:08 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [3] SYSTEM-USER prompt · 2026-08-13 23:48:47 UTC

```
<verification_results>
Your previous response had issues that need fixing:

DEPENDENCY ERRORS (depends_on can ONLY reference IDs from <existing_artifacts>):
  - Strategy 1: Artifact 'experiment_iter4_dir1' (experiment): dependency 'art_fvWfzRrcoKux' has type 'experiment' which is not allowed (allowed: {'research', 'dataset'})
  - Strategy 1: Artifact 'experiment_iter4_dir2' (experiment): dependency 'art_gCgia-6VUZJb' has type 'experiment' which is not allowed (allowed: {'research', 'dataset'})
  - Strategy 1: Artifact 'experiment_iter4_dir2' (experiment): dependency 'art_fvWfzRrcoKux' has type 'experiment' which is not allowed (allowed: {'research', 'dataset'})
  - Strategy 1: Artifact 'experiment_iter4_dir3' (experiment): dependency 'art_gCgia-6VUZJb' has type 'experiment' which is not allowed (allowed: {'research', 'dataset'})
  - Strategy 1: Artifact 'evaluation_iter4_dir4' (evaluation): dependency 'art_0T8jhUa0zxmu' has type 'evaluation' which is not allowed (allowed: {'experiment', 'dataset'})
  - Strategy 1: Artifact 'evaluation_iter4_dir4' (evaluation): dependency 'art_sHF0cggp2IvT' has type 'research' which is not allowed (allowed: {'experiment', 'dataset'})

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
