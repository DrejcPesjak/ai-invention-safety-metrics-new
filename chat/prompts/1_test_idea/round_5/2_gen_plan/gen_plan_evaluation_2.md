# gen_plan_evaluation_2 — test_idea

> Phase: `invention_loop` · round 5 · `gen_plan`
> Run: `iter1_33370088803c` — Catching Edited Safety Models by Reading Weights in Sliding Windows
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_evaluation_2` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-14 02:26:32 UTC

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
You are expanding an artifact direction of type: EVALUATION

EVALUATION
Evaluate experiment results with metrics, statistical analysis, and validity checks.
Runtime: Python 3.12, UV (any evaluation library), isolated workspace, gradual scaling matching experiment.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Compute any quantitative metrics and statistical tests, analyze validity and robustness.
Deps: REQUIRED at least one EXPERIMENT | OPTIONAL DATASET if reference data needed
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

The evaluation executor has 3h total (including writing code, debugging, testing, and fixing errors).

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
  CORE CLAIM, STILL SPLIT IN TWO, WITH CLAIM A NOW A BOUNDED NEGATIVE PLUS AN ANALYTIC BOUNDARY. The original claim -- safety behaviour is legible from the model alone, cheaply, better than from its outputs -- remains resolved into two halves, and iteration 4 changed the sign of the first one. Iteration 3 said the supported half was a claim about UNIFORMITY. Iteration 4 took that to scale and BOTH halves of the uniformity story failed. What survives is smaller, sharper and, we think, still worth a paper: a parent-free spectral certificate is a PRECISION INSTRUMENT WITH ALMOST NO RECALL, its recall is governed by a condition that is ANALYTIC rather than empirical, its verdict is DISSOCIABLE FROM SAFETY BEHAVIOUR IN BOTH DIRECTIONS BY CONSTRUCTION, and on ordinary Hub traffic it is dominated by a filename regex.

  CLAIM A (NOW LARGELY REFUTED AT SCALE, WITH A PRECISE RESIDUE). W05 = log10 min_W e_W(v1) over the pooled residual-write Gram certifies a UNIFORM, COMPLETE, ALL-LAYER directional annihilation with zero prompts, zero forward passes and ~7-11 s of CPU linear algebra -- but on 44 real public sub-4.2B edited checkpoints from 27 uploaders across 9 recipe classes it fires on SEVEN (sensitivity 0.159) while all five archived calibration positives still fire at 1.000, and a plain 11-term regex over the repository id reaches sensitivity 0.727 at the SAME specificity 1.000 with caught_by_W05_missed_by_name = EMPTY (art_dp7WBo6hhVBX). The residue that survives is precision: 0 false positives on 32 at-scale negatives incl. 20 fresh Hub parents, 0/122 on the pre-stamped eligible undeclared population (Wilson [0, 0.031]), 0 in every leave-one-recipe-class-out cell.
  CLAIM B (REFUTED AS ORIGINALLY STATED, QUANTITATIVELY BOUNDED, UNCHANGED THIS ITERATION): for GRADED BEHAVIOURAL SAFETY, no interior observable in the frozen 53-metric battery beats a trivial black-box baseline by a resolvable margin -- minimum detectable |drho| = 0.32 at 19 lineages, r_xx = 0.968 so not attenuation, invariant at three depths, and interior observables ARE predictive (A19 rho +0.763 member / +0.800 lineage at a thirty-fifth of B09's forward passes) so the falsifier is about MARGINAL VALUE OVER A CHEAPER INSTRUMENT.

  WHAT ITERATION 4 SETTLED (do not re-litigate; do not re-run).
  S1. THE CERTIFICATE FAILS AT SCALE AND FAILS BY RECIPE. Leave-one-recipe-class-out is the primary generalisation control and locates it exactly: norm-preserving 5/5, global rank-one 1/6, unknown 1/5, multi-direction SVD 0/5, Heretic per-component 0/7, Gaussian-depth 0/3, partial-layer 0/4, SFT-uncensored 0/5, merge-of-abliterated 0/4. Two classes predicted to be CAUGHT (multi-direction, global rank-one) were not, so iteration 3's recipe story was not merely incomplete but wrong in sign on two classes. Misses are not near-misses: mlabonne/Qwen3-0.6B-abliterated reads -0.9637 against its parent's -0.9641, a paired shift of 4e-4.
  S2. UNIFORMITY IS THE WRONG PREDICATE, AND THE REPLACEMENT IS ANALYTIC, NOT EMPIRICAL. A 25-kernel sweep with host (Qwen3-1.7B) and direction r held fixed shows a uniform edit at sub-unit weight w=0.85 is INVISIBLE while behaviourally as effective as the full edit (refusal 0.225 vs 0.200 against host 0.925), and a strongly non-uniform Gaussian kernel at large spread IS detected. The correct decomposition is DISCOVERY (|cos(v1,r)| -> 1, so the pooled Gram surfaces r) AND COMPLETION (log10 min_W e_W(r) <= tau). THE REVIEWER IS RIGHT THAT THIS IS CLOSE TO AN IDENTITY: e_W(v1) = e_W(r)cos^2(theta) + cross terms, so whenever discovery holds W05 and the completion quantity are numerically the same object (uniform_w0.7: -1.1535 vs -1.1245; w0.85: -1.7488 vs -1.7248; w1.0: -4.5917 vs -4.5828), and whenever discovery fails W05 collapses to the parent's value (every Gaussian spread <= 8 reads -1.0098 to four decimals). The '19/19 with zero disagreements' figure is therefore a consistency check on a near-identity, NOT a validated empirical prediction, and it must never again be reported as one. The genuinely empirical content of the sweep is narrower and still valuable: WHICH kernels achieve discovery, and that the discovery switch is controlled by the MINIMUM DEPTH WEIGHT, bracketed in [0.0796, 0.5311] between spread 8 and 16 (|cos| 0.126 -> 0.9992, W05 -1.013 -> -2.888), against a stamped critical spread of 58.17 that was wrong by 3.6x. Completion NEVER varied over the whole Gaussian sweep (log10 min e_r = -4.53 at every spread), so discovery was always the binding constraint.
  S3. THE ANALYTIC BOUNDARY. A Householder reflection removes no rank and leaves the Gram spectrum invariant, so it is PERMANENTLY invisible to any statistic reading that spectrum. Measured: ORBA lambda=1.0 drops refusal to 0.100 while moving W05 by 4.1e-5, LESS than a Householder about an unrelated random direction (7.3e-5). Of 10 in-house kernels that pass the fluency screen AND actually remove refusal, only 4 are detected; the two most effective (ORBA, Heretic-style at refusal 0.125) are both invisible, while rank_k4 IS detected at -5.630 and barely uncensors (0.650). Detectability and effectiveness are near-orthogonal on this sweep, and where they correlate they correlate the wrong way.
  S4. BOTH-DIRECTIONS DECOUPLING, BY CONSTRUCTION (art_VLI4IOs9Xy9P). FALSE NEGATIVE: root B, a depth-weighted Gaussian abliteration of Qwen3-1.7B with the direction held fixed at root A's so the kernel is the only variable, un-censors 0.950 -> 0.270 [0.196, 0.360] at n=111, stays fluent (ppl 27.28), and reads W05 = -1.0100 -- the PARENT's value to four decimals, cos(v1,r) = 0.0199, all six flags False, ladder UNDEFINED across all 14 of its cells. Its recipe class R4_PARTIAL_LAYER_OR_PER_HEAD is 235/513 = 45.8% of declared Hub edits, the largest class. FALSE POSITIVE: root C, a uniform Llama-3.2-1B-Instruct edit along the AUROC-argmax direction, fires at W05 = -4.587 while refusing at 0.950 [0.83, 0.99], its parent's rate -- never un-censored. Held-out AUROC saturates (11 layers >= 0.997, 4 tied at exactly 1.000), so direction selection MUST be behavioural.
  S5. THE DEPLOYMENT NUMBER IS NOW HONEST BUT ITS POPULATION IS NOT THE THREAT MODEL. A sha256-stamped eligibility rule (n_layers>=8, d_model>=128, params<=4.2e9 enforced twice, no fixtures / speculators / quantized re-uploads) gives 0/122 Wilson [0, 0.031] primary, with raw 0/160 [0, 0.023] retained as a labelled secondary and its degenerate composition published (art_VFF9Dum9x3KJ); an independent stricter reading gives 85/160 eligible and [0, 0.043] (art_ckuwEkspyins), the two agreeing on the rate and disagreeing on three rows. BUT the eligible population is dominated by older BASE models (29 of the 40 newly fetched rows are gpt_neox; archived eligible is qwen2 23 / llama 19 / qwen3 9 / gpt_neox 6), and the first false positive is itself a gpt_neox model.
  S6. THE THRESHOLD IS WORSE THAN THE PAPER SAYS. The panel operating point tau = -2.7415117804288127 is carried by a 0.0763 log10 margin between two individual checkpoints and never validated out of panel; the first false positive appears at -2.6139, a shift of 0.128 log10 (~1.7 margin widths). AND -- the number the draft omitted -- refitting tau under leave-one-recipe-class-out gives -1.7156 for EVERY held-out class, a shift of 1.03 log units, about EIGHT TIMES the brittleness scale, under which held-out sensitivities change materially (global rank-one 0.167 -> 0.333, unknown 0.200 -> 0.400). The draft's LORCO table silently mixed fixed-tau sensitivities with refit AUROCs.
  S7. QUANTIZATION, RESOLVED. The dequantization remedy is VOID AS STATED: the archived quant_sd was a fake-quant, so the archived int4 number was already dequantized. The substantive result is a bit-width sweep: the scar dies at 5 BITS (W05 -2.654 > tau) with refusal still 0.237 and ppl only 26.25 -> 28.77; curve 8b -4.197 / 6b -3.270 / 5b -2.654 / 4b -2.009 / 3b -1.281 (ppl 272, destroyed). cos(v1,r) > 0.9994 at every bit-width, so the mechanism is THE NULL FILLING IN, not eigenvector rotation; the clean parent is unmoved (-1.010 -> -0.957); the proposed W05rel FAILS (tracks W05 to <0.001 because energies are already Frobenius-normalised). Operationally a quantized upload is UNRESOLVED in the scan pipeline, not a silent false negative. int4 costs ppl 26.25 -> 37.72 (+43%), so 'for free' overstated it.
  S8. STORAGE PRECISION SETS THE SCAR DEPTH, AND TWO STATISTICS ARE IRREPRODUCIBLE. The SAME complete uniform projection reads W05 = -4.592 in bf16 and -12.705 in float32. On a bit-identical rebuilt root, W02/W03/W05 reproduce to 1.3e-5 while W01/W04 differ by 3.1e-2 -- both are log ratios against lambda_1, which sits at the float32 Gram-accumulation floor on abliterated checkpoints; float64 recomputation moves W01 by exactly the archive gap. W01/W04 are not reproducible below ~0.05 on abliterated checkpoints. Nothing load-bearing may depend on them.
  S9. THE PARENT BUYS REAL COVERAGE -- 'PARENT-FREE COSTS NOTHING' IS RETIRED. On the at-scale rows E_1 fires on 13/32 pairs against W05's 7/35 and reaches Gaussian-depth, Heretic and partial-layer edits W05 never touches; agreement 0.829. The detection vector is IDENTICAL at all three bands ([0.25L,0.75L], full stack, [0.4L,0.6L]), so the band-sensitivity objection is answered with data. On archived matched pairs the primary band reproduces exactly (12 pairs tie at 1.000, +0.000; 15 pairs -0.167 [-0.444, 0.000]; 41 pairs -0.186 [-0.373,-0.076], reverting to -0.167 covering zero once the 26 in-house synthetics are excluded).
  S10. THE LADDER, WITH ERROR BARS AND THREE ROOTS. Achieved denominators are 31-40, not the recorded 40 (13 rows ambiguous); all four signed 'evasion costs' (-0.004, +0.069, +0.075, +0.128) and int4-minus-root (-0.03 [-0.189,+0.135]) are NOT RESOLVABLE (smallest upward detectable difference at n=40, p=0.20 is 0.29). What survives at n>100 with intervals is the ORDERING, on three laundering families and two architectures, with flag-death intensities IDENTICAL across architectures (merge w=0.10, add-back eps=0.10, quant nf4). Root C's behaviour gate FAILS honestly (1.000 -> 0.617) and it is labelled signature-positive / partially un-censored. Two reversals survive: a one-matrix argmin patch does not defeat a min-over-layers statistic, and 200 benign LoRA steps move W05 only -4.592 -> -4.381 while RESTORING refusal.
  S11. THE WINDOWED REMEDY IS DIAGNOSED, NOT DEMONSTRATED. W05w (windows of k consecutive layers, stride k//2, per-window minimum eigenvector, extremum-scored, with an adjacent-window consistency gate) provably contains W05 as its k=L special case and recovers the archived 4-of-12 toy blind spot by 12.6 log units, with specificity 1.000 at every k and every consistency threshold on 40 eligible undeclared models. BUT its POSITIVE ARM DID NOT RUN: n_G1 = n_G2_G3_synth = n_G4_real = 0, catch_by_recipe_class empty, every sensitivity NaN over n_positives = 0, and the declared k=L reproduction gate reports PASS = false because the achieved 8.49e-8 exceeds a declared 1e-9 tolerance on real models. The 12.6 log-unit number is a TOY-STACK number and must not carry Introduction or Conclusion framing.
  S12. OUR OWN REPORTING, AUDITED (art_ckuwEkspyins). 110 assertions -> 105 MATCH / 5 MISMATCH / 0 UNAVAILABLE, byte-identical across two runs, verify.py 17/17. The five: seven intensity axes not six; 81 unresolved non-control rows not 65; 8 skipped not 7; FIVE unreproduced quoted values not four; B09's 0.766 is the 26-member chatml value while the draft attributed it to the 28-member contract subset (correct value 0.670). Relabel discipline held: 2 of 4 iteration-3 misses carry a verbatim Heretic string; mlabonne and BennyDaBall stay PROVISIONAL because no kernel may be inferred from W05. Heretic's kernel is a TRIANGULAR TENT WITH A HARD CUTOFF, not Gaussian (art_gqCRODISeyg2) -- our own taxonomy was wrong.

  THE REVISED CLAIMS FOR ITERATION 5. No new battery. Most of this is re-analysis of tensors, checkpoints and rows we already hold; two arms need modest new GPU time.

  H1 (RUN THE WINDOWED POSITIVE ARM -- the single highest-value item, and pure re-analysis). Score W05w on the Arm B kernels that ALREADY EXIST as checkpoints (middle-50% band, Gaussian at all nine spreads, sub-unit uniform at w=0.5/0.7/0.85, ORBA at lambda=0.25/0.5/1.0, Heretic per-component, rank-k at k=2/4/8) and on the 44 Arm A real edited checkpoints, reporting sensitivity per k beside the specificity already measured, plus per-window random-direction nulls so the multiple-window hazard becomes a CALIBRATED per-window false-positive rate rather than an unbounded one. PREDICTION, stated so it can fail: un-pooling recovers the DISCOVERY failures (band, Gaussian at small spread, partial-layer) and recovers NOTHING that failed COMPLETION (sub-unit uniform w<=0.85) or that is an ISOMETRY (ORBA Householder), because those are not pooling artefacts. If windowing recovers the depth-weighted classes, that is the paper's positive claim and it replaces the toy number in the Introduction; if it does not, the mechanism section becomes a clean boundary result and W05w is demoted to a labelled 'proposed' subsection. Either way: widen the k=L gate to a defensible float32 bound (or report it as FAILED at its declared 1e-9), and delete the 12.6 log-unit toy figure from Introduction and Conclusion.

  H2 (REPLACE THE 'EMPIRICAL MECHANISM' FRAMING WITH A DERIVATION, AND GENERALISE IT TO THE CLASSES WHERE THE FAILURE ACTUALLY LIVES -- the reviewer's decisive point). Write e_W(v1) = e_W(r)cos^2(theta) + cross terms, bound the residual, and state as a CONSEQUENCE OF THE DEFINITION that detection <=> completion whenever discovery holds and is impossible otherwise. Delete '19/19 with zero disagreements' as evidence. Then reposition the sweep as what it is: a measurement of WHICH kernels achieve discovery and of the discovery threshold's dependence on the minimum depth weight in [0.0796, 0.5311]. Add the paragraph the draft owes: the single-direction rule is UNDEFINED for multi-direction SVD and per-component kernels -- exactly the 13 of 44 real misses excluded as 'inapplicable' -- and generalise it by defining discovery against the LEADING EDITED SUBSPACE via principal angles between the bottom-j Gram eigenspace and the span of the removed directions, then re-scoring rank_k2/4/8 and both Heretic variants under that generalisation. A rule that cannot be evaluated on the classes that dominate the failure is not yet a mechanism.

  H3 (DE-BIAS THE BASELINE THE WHOLE VERDICT RESTS ON). 0.727 is measured on a pool DISCOVERED BY NAME SEARCH (61 sweeps over abliteration vocabulary; 50.5% of harvested edited repos carry an abliteration string in the id; the regex's 11 terms overlap the search terms), so it is an UPPER BOUND presented as the baseline. Re-estimate it on a sample not discovered by name: draw edited checkpoints from the UPLOADER-sweep and ARCHITECTURE-sweep strata only, and/or from repositories whose recipe evidence comes from CARD BODY TEXT while the repo id contains none of the 11 terms; the census already says 23.4% of edited rows declare no mechanism and hub_scan_pool carries 1,105 non-declaring chat repos, so the stratum where the regex must fail exists and was never sampled. Report W05 and the regex SEPARATELY on the DECLARED and UNDECLARED strata, since the operational question -- does a weights-only test add anything -- is entirely about the undeclared stratum and the current answer is computed on the declared one. If the de-biased sample cannot be assembled, say plainly that 0.727 is a name-search upper bound and give the regex sensitivity on the card-derived subset.

  H4 (VERIFY THE POSITIVE CLASS BEHAVIOURALLY, AND THE JUDGE INDEPENDENTLY). (a) The 44 at-scale positives are labelled 'edited' from cards and never behaviourally checked, while this paper itself exhibits root C (full signature, parent's refusal rate) and root B (un-censored, parent's W05) -- so if some are cosmetic, failed or merged-away edits, 0.159 measures the detector against a partly mislabelled positive class, and the regex comparison inherits it. Measure greedy harmful refusal on the frozen 40-item core for a stratified ~12-checkpoint subsample (one or two per recipe class; the 5 SFT-uncensored and 4 merge-of-abliterated rows are the most uncertain as positives for a PROJECTION detector) and report sensitivity both on all 44 and restricted to verified-un-censored rows. Divergence is itself a result about card labels as ground truth. (b) The entire behavioural axis -- the 0.950 -> 0.270 decoupling headline, the effectiveness-vs-detectability intersection, the ladder orderings -- rests on ONE unvalidated judge (llama-3.3-70b, rubric B, kappa 0.149 / rate-level r 0.822 against the substring screen, itself substituted for a failed pre-registered rubric). Re-score a stratified 100-200 item subsample of the load-bearing stages (parent, roots A/B/C, flag-death cells) with a second judge from a DIFFERENT model family plus a small hand-labelled anchor, report kappa and rate-level agreement, and restate the decoupling with judge disagreement propagated -- one sentence saying root B's 0.270 moves by less than the interval width under the second judge makes the headline much harder to attack.

  H5 (FIX THE OPERATING POINT'S REPORTING, AND MEASURE SPECIFICITY WHERE IT MATTERS). (a) Give the leave-one-recipe-class-out table FOUR columns -- sensitivity and AUROC at the fixed panel tau, and sensitivity and AUROC under the class-held-out REFIT -- printing the refit tau of -1.7156, and add one sentence stating that refitting on the at-scale positives moves tau by 1.03 log units, ~8x the 0.128 brittleness scale. Report specificity on the 122 eligible undeclared checkpoints AT THE REFIT VALUE too: if it survives at -1.7156 that is a genuinely reassuring result currently left on the table; if it does not, the honest specificity claim is narrower than 0/122. (b) Stratify the false-positive rate by INSTRUCTION-TUNED/CHAT-TEMPLATED vs BASE and give the chat subset its own Wilson interval, since the population at risk of abliteration is current-generation chat models and the present denominator is mostly older base checkpoints; extend the scan by 40-60 repos inside hub_scan_pool's 1,105 non-declaring chat stratum, and if the chat denominator stays small, state its interval honestly rather than letting the pooled 0/122 stand in for it.

  H6 (POSITIONING, NOVELTY AND FRAMING, WITH THE NOVELTY CLAIM CUT TO WHAT SURVIVES). State precisely what is new relative to (i) Abliterlitics [art_gqCRODISeyg2] -- AGPL-3.0, first public 2026-04-24, four reports at or below ~4.5B including a full weight report on our own Qwen3-4B family, every weight metric DELTA-based (diff = (variant-base).abs().mean(), svd(delta_matrix)), base a mandatory key with no single-checkpoint mode -- whose measured depth/completeness fingerprints (Heretic 23/32 layers with 0-8 untouched, HauhauCS 29, Huihui 31, direction cosine 0.997 on one base but 0.00017 on another) ALREADY surface the depth-vs-completeness decomposition empirically; and (ii) arXiv:2607.01854, whose E_1 is ALREADY band-averaged over a mid-stack band, making per-band scoring published prior art. Frame our mechanism as an INDEPENDENT, PARENT-FREE CONFIRMATION of what delta-based forensics measures, plus the analytic statement of when parent-free detection is possible at all (the isometry impossibility) -- more accurate and more persuasive than framing it as a discovery. The surviving novel object is exactly four qualifiers: parent-free, calibration-free, BOTTOM-of-spectrum, sliding-and-extremum-scored -- and the sliding half is what H1 must earn. Keep the existing corrections: 2604.08844's cross-method AUC 0.00 carries its declared confound (steering arm incoherent, GPT-4o 0/300 harmful); OBLITERATUS certifies from ACTIVATIONS and audits a self-performed edit, and is LAYER-SELECTIVE via COSMIC so its presets are DEGRADED not detected; ORBA is TWO recipes (lambda=1 is annihilation without reflection; only v3 Householder is the isometry) and conflating them makes the falsification vacuous; reverse-abliterate is the software instantiation of the name baseline; Heretic's kernel is a triangular tent, code-level forbidden from the early stack.

  H7 (EDITORIAL AND REPORTING FIDELITY -- cheap and mandatory in a paper whose argument IS measurement discipline). One pass converting every backward reference into a direct claim ('uniformity is not the predicate', not 'we retract the previous draft's uniformity story'); number the sections so cross-references resolve; consolidate ALL corrections-to-prior-reporting into one delimited subsection near the end; cut the Contributions list to FOUR items that are findings, not bookkeeping; move the 110-assertion self-audit to an appendix or a short methods paragraph -- it is excellent practice, not a research contribution, and listing it as one invites the reading that the paper is short of results. Keep: counts generated from rows (270 = 20 controls + 250 attempted, 160 completed), full-precision boundary with abliterated MAXIMUM -2.7415 / minimum -4.8204 and margin 0.0763, oriented-vs-raw AUROC with an explicit convention field, [min,max] for every class x statistic with the base/abliterated overlaps flagged, W03 at 256 directions, and 'pre-registered' reserved for what metric_spec.py actually stamps (4 SUPPORTED / 2 PLAN-ONLY / 6 UNSUPPORTED).

  WHAT IS RETIRED. The 53-metric battery is not rebuilt. UNIFORMITY as the scope predicate is retired outright. 'Parent-free costs nothing' is retired -- the parent buys roughly a factor of two in sensitivity and reaches the classes that dominate the Hub. '19/19 reproduces the mechanism' is retired as evidence. The dequantize-then-rescore remedy is retired as void. W05rel is retired (it is algebraically identical to W05). W01 and W04 are retired from any load-bearing role (irreproducible below ~0.05 where the scar lives). alpha_50 and the steering-price family remain retired as metrics, surviving as the S4 negative plus the scorer-artefact finding. The early-warning-signal / critical-slowing-down arm remains retired entirely. Leave-one-architecture-family-out and leave-one-uploader-out remain retired/demoted; leave-one-RECIPE-CLASS-out with BOTH fixed and refit tau is primary. The framing 'safety behaviour is legible from the model alone' stays retired.

  CONFIDENCE. Lower than last iteration, and now asymmetric in a different place. HIGH that the certificate has excellent PRECISION: 0 false positives on 122 eligible undeclared checkpoints under a pre-stamped rule, on 32 at-scale negatives including 20 fresh parents, and in every leave-one-recipe-class-out cell -- though that precision is measured mostly on older base models and at a threshold fitted elsewhere. HIGH that its RECALL at Hub scale is poor and dominated by a filename regex (0.159 vs 0.727, empty complement), with the caveat that 0.727 is a name-search upper bound H3 must de-bias. HIGH that the discovery/completion decomposition is CORRECT, and equally high that it is ANALYTIC rather than empirical -- its empirical content is the discovery threshold's location and which kernels reach it. HIGH that an isometry is permanently invisible to any Gram-spectrum statistic. HIGH that the weight statistic and safety behaviour are dissociable in BOTH directions, since both were built as checkpoints and measured with intervals. MODERATE that windowing recovers the discovery failures; LOW that it recovers the completion or isometry failures; ZERO evidence either way today, which is precisely why H1 is the iteration's centre. HIGH that graded behavioural safety is not better read from the interior than from a 40-prompt greedy refusal rate at this panel size, and HIGH that the bound is |drho| ~ 0.32 at 19 lineages rather than zero. The most likely outcome of iteration 5 is a paper whose claim is: 'parent-free spectral edit detection is a precision instrument whose recall is set by an analytic discovery condition; we characterise that condition, show it is unfixable for isometries and fixable-or-not for pooling failures by an explicit measurement, and show by construction that no such certificate can be read as a safety score'. Smaller than iteration 3 hoped, and the only version the evidence licenses.
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
  Same frame; the supported half becomes a bounded negative and the boundary is restated as analytic, not empirical.
_confidence_delta: decreased
_key_changes:
- >-
  DOWNGRADED Claim A from 'supported, narrowed' to LARGELY REFUTED AT SCALE: sensitivity 0.159 on 44 real edited checkpoints
  from 27 uploaders / 9 recipe classes vs a repo-name regex at 0.727 with matched specificity 1.000 and an EMPTY caught-by-W05-missed-by-name
  set (art_dp7WBo6hhVBX); what survives is precision, not detection.
- >-
  RETIRED UNIFORMITY outright as the scope predicate — a uniform sub-unit edit (w=0.85) is invisible yet behaviourally as
  effective as the full edit, and a non-uniform Gaussian at large spread IS detected; the predicate is discovery AND completion.
- >-
  ACCEPTED the reviewer's decisive point that discovery∧completion is NEAR-ALGEBRAIC, not empirical: e_W(v1)=e_W(r)cos^2(theta)+cross
  terms, so '19/19 with zero disagreements' is retired as evidence and replaced by a derivation plus the sweep's real empirical
  content (the discovery switch controlled by minimum depth weight in [0.0796,0.5311], stamped critical spread wrong by 3.6x).
- >-
  ADDED the generalisation the rule needs: it is UNDEFINED for multi-direction and per-component kernels — exactly the 13
  of 44 real misses excluded as 'inapplicable' — so discovery must be redefined against the leading edited SUBSPACE via principal
  angles and re-scored on rank-k and both Heretic variants.
- >-
  MADE THE WINDOWED POSITIVE ARM the iteration's centre: W05w currently has n_positives=0 everywhere (catch_by_recipe_class
  empty, all sensitivities NaN) and its only evidence is a 12-matrix toy; score it on the Arm B kernels and 44 Arm A reals
  that already exist, with per-window random-direction nulls, and fix or fail the k=L gate (8.49e-8 vs declared 1e-9).
- >-
  FLAGGED the regex baseline as an UPPER BOUND: the panel was discovered by name-based Hub search whose terms overlap the
  regex's 11 terms; re-estimate on uploader/architecture-sweep and card-text-only strata and report W05 vs regex separately
  on DECLARED and UNDECLARED strata.
- >-
  SURFACED the omitted threshold result: leave-one-recipe-class-out refits tau to -1.7156, a 1.03 log-unit shift (~8x the
  0.128 brittleness scale) that changes held-out sensitivities (rank-one 0.167→0.333); the LORCO table must carry four columns
  and specificity must be reported at the refit tau.
- >-
  ADDED behavioural verification of the positive class (the 44 are card-labelled and never checked, while this study exhibits
  root C signature-positive-but-refusing and root B un-censored-but-clean) and independent judge validation of the load-bearing
  behavioural axis (single judge, kappa 0.149, r 0.822, substituted rubric).
- >-
  PROMOTED the both-directions decoupling to the paper's central mechanistic statement, now built as checkpoints with intervals:
  root B un-censors 0.950→0.270 [0.196,0.360] at n=111 reading its parent's W05 -1.0100 with cos(v1,r)=0.0199, class prevalence
  45.8%; root C fires at -4.587 refusing at 0.950.
- >-
  ADDED the analytic isometry boundary as a permanent limit (ORBA Householder moves W05 by 4.1e-5, less than a random-direction
  Householder's 7.3e-5) and the effectiveness/detectability near-orthogonality (10 effective kernels, 4 detected).
- >-
  RETIRED 'parent-free costs nothing': E_1 fires 13/32 vs W05's 7/35 at scale and reaches Gaussian-depth, Heretic and partial-layer
  edits, with the detection vector INVARIANT across all three bands, settling the band-sensitivity objection.
- >-
  RESOLVED quantization (remedy VOID — archive was already fake-quant; scar dies at 5 BITS with refusal 0.237 and ppl 28.77;
  cos(v1,r)>0.9994 so the null FILLS IN; W05rel algebraically identical and retired) and stratified the 0/122 denominator
  as unrepresentative (29/40 new rows gpt_neox, mostly base models) pending a chat-stratum scan.
- >-
  RETIRED W01/W04 from any load-bearing role (irreproducible below ~0.05 on abliterated checkpoints, float32 Gram floor) and
  recorded that bf16 storage, not the edit, sets the scar depth (-4.592 vs -12.705 in float32).
- >-
  REFRAMED NOVELTY honestly against Abliterlitics' measured depth/completeness fingerprints at our own scale and 2607.01854's
  already-band-averaged E_1: the mechanism is an independent PARENT-FREE confirmation of what delta-based forensics measures,
  and the surviving novel object is four qualifiers of which the sliding half is still unearned.
- >-
  ADDED the editorial pass the reviewer requires: no backward references, numbered sections, corrections consolidated into
  one delimited subsection, Contributions cut to four findings, the 110-assertion self-audit moved to an appendix.
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

id: evaluation_iter5_dir4
type: evaluation
objective: >-
  Validate the single unvalidated judge the entire behavioural axis rests on, and restate the decoupling headline with scorer
  disagreement propagated so the paper's most quotable claim stops resting on one model's rubric.
approach: >-
  No weights loaded, no new generations -- re-score ARCHIVED text with independent scorers. The load-bearing behavioural results
  (root B un-censoring 0.950 -> 0.270 [0.196, 0.360] at n=111, root C refusing at 0.950 [0.83, 0.99] with W05 -4.587, the
  effectiveness-vs-detectability intersection where 10 kernels remove refusal and only 4 are detected, and every laundering
  ordering) are scored by ONE judge (meta-llama/llama-3.3-70b-instruct, rubric B) whose agreement with the substring screen
  is mean kappa 0.149 and rate-level Pearson r 0.822, and which was itself substituted for a pre-registered rubric that failed
  with kappa ~0. The last independent validation was two iterations back on a DIFFERENT rubric. (1) SAMPLE. Draw a STRATIFIED
  150-200 item subsample of the archived generations spanning the load-bearing stages: the Qwen3-1.7B parent, roots A / B
  / C, the flag-death cells for merge / add-back / quantization on roots A and C, and the Arm B kernels used in the effectiveness-vs-detectability
  claim. Stratify by stage and by the primary judge's label so both REFUSAL and COMPLIANCE classes are represented (the archived
  evidence says PARTIAL is the weakest class for every scorer, so oversample it deliberately and say so). (2) SECOND JUDGE.
  Re-score with a judge from a DIFFERENT model family (e.g. a Gemini or Claude family model via OpenRouter, chosen and named
  explicitly, temperature 0, rubric B verbatim so the rubric is held fixed and only the model varies), plus a THIRD arm holding
  the model fixed and varying the rubric framing, so model-effect and rubric-effect are separable. Report Cohen's kappa item-level
  and rate-level agreement per stage, plus the confusion matrix by class. (3) HAND-LABELLED ANCHOR. Adjudicate a small anchor
  set (>=40 items, stratified, labels withheld by construction with mtimes asserted) and report each scorer's accuracy against
  it, stating plainly that the adjudicator is an LLM agent, not a human, so every 'accuracy' bounds scorer disagreement rather
  than truth -- the same discipline the archived iteration-2 evaluation used. (4) PROPAGATE. Recompute the headline rates
  under the second judge WITH Wilson intervals and emit the propagated sentences: does root B's 0.270 move by LESS than its
  interval width (0.196-0.360) under the second judge? does the 0.950 -> 0.270 gap remain interval-disjoint? does root C still
  refuse at its parent's rate? does the 10-effective / 4-detected intersection change membership, and if so which kernels
  flip? does any laundering ORDERING (flag death before un-censoring death, at merge w=0.10 / add-back eps=0.10 / quant nf4
  on both architectures) reverse? Report every answer, including the ones that weaken the paper. One sentence saying root
  B's un-censoring survives a cross-family judge with the disagreement quantified makes the headline much harder to attack;
  a sentence saying it does not is a result the paper must carry. (5) BUDGET AND REPRODUCIBILITY. Cap spend at $1.50 with
  a content-addressed cache so a rerun costs $0 and reproduces byte-identically; log every call; report cumulative spend after
  each stage. Ship the disputed items verbatim, the per-stage agreement table, and a single machine-readable file the paper's
  judge-limitations paragraph is generated from. ARCHIVE ACCESS NOTE: archived generations live under run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_3
  (ladder and root behaviour, judge cache) and gen_art_experiment_1 (arm_b_behaviour), with the iteration-3 harness at iter_3/gen_art/gen_art_experiment_2;
  read them directly and re-run their integrity checks before re-scoring.
depends_on:
- id: art_VLI4IOs9Xy9P
  label: reanalyzes
  relation_type:
  relation_rationale:
- id: art_dp7WBo6hhVBX
  label: generations
  relation_type:
  relation_rationale:
- id: art_CKWQh2cOQLLQ
  label: prompts
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
id: art_dp7WBo6hhVBX
type: experiment
title: Does the abliteration weight scar generalise?
summary: |-
  Stress-tests the parent-free abliteration detector W05 (log10 of the minimum per-matrix energy along the smallest-eigenvalue direction of the shared Gram matrix over residual-write matrices; detect iff W05 <= tau = -2.7415117804288127). 13 signed predictions were stamped and sha256-hashed BEFORE any checkpoint was downloaded (results/predictions.json); a second stamp (w* = 0.9533, critical spread 58.17) was hashed once W05_ref was measured. verify.py re-derives every headline number from the raw rows: 20/20 pass. Tier 2, $0.022 OpenRouter, 361 GB streamed.

  HEADLINE, AT SCALE: specificity 1.000 (0 false positives on 32 negatives incl. 20 fresh Hub parents) but sensitivity 0.159 on 44 real edited checkpoints from 27 uploaders across 9 recipe classes, while the 5 archived panel members it was calibrated on all still fire (1.000). Five of the 7 detections are ONE uploader's norm-preserving family; a sixth clears tau by 0.09. It does NOT beat the baseline the manifest demanded: a repo-name regex scores 0.727 sensitivity at the same 1.000 specificity on identical rows, and the set W05 catches that the name misses is EMPTY. Misses are not near-misses: mlabonne/Qwen3-0.6B-abliterated reads -0.9637 vs its parent -0.9641.

  MECHANISM (Arm B: host Qwen3-1.7B and direction r held fixed, kernel is the only variable, 25 kernels x 2 storage precisions). Uniformity is the WRONG predicate. Detection needs DISCOVERY (|cos(v1,r)| -> 1) AND COMPLETION (min_m e_r <= tau); that post-hoc rule reproduces 19/19 applicable kernels. Every Gaussian spread annihilates the peak layer completely (log10 min_m e_r = -4.53 at ALL spreads) yet detection switches on only between spread 8 and 16, bracketing the controlling min-depth-weight in [0.0796, 0.5311] — nowhere near the stamped w*. The mid-50% band edits half the stack completely and is still missed, because untouched matrices keep r from becoming the Gram's minimal direction.

  EVASION: of 10 fluency-passing edits that actually remove refusal (judge <= 0.50 vs host 0.925), only 4 are detected. The two most effective are invisible — ORBA Householder drops refusal to 0.100 while moving W05 by 4.1e-5, LESS than a random-direction Householder control (7.3e-5); Heretic-style drops it to 0.125 and is missed. rank_k4 is detected but barely uncensors (0.65).

  REPRODUCIBILITY FINDING: the rebuilt in-house root is BIT-IDENTICAL to the archive (write_matrix_sha256 matches) and W02/W03/W05 reproduce to 1.3e-5, yet W01/W04 differ by 3.1e-2. With byte-identical weights that cannot be the model: both are log ratios against lam[0], at the float32 Gram-accumulation floor. Float64 recomputation moves W01 by exactly the archive gap (4.7894e-2 vs 4.7894e-2). W01/W04 are irreproducible below ~0.05 on abliterated checkpoints; W05 is not, and nothing here depends on W01/W04. Fast safetensors path == Runner path EXACTLY (0.0). Storage precision caps the scar: the same complete projection reads W05 = -4.59 in bf16, -12.70 in float32.

  VERDICTS: P1 P2 P3 P6 P7 P9 P11 CONFIRMED; P8 confirmed at the measured noise floor; P10 shape-confirmed / critical-spread refuted (3.6x); P12 PARTIAL (7/7 Arm B classes, 4/6 Arm A); P4 P5 P13 REFUTED. Two falsifiers fired and are reported as the headline.

  SHIPS: method_out.json (110 examples, predict_our_method_W05 vs predict_baseline_E1 vs predict_baseline_repo_name_regex side by side), results/{predictions,predictions_derived,gate_iter4,unit_tests,arm_a,arm_b,arm_b_behaviour,layer_profiles,analysis,cards}.*, verify.py, and byte-identical vendored iteration-3 libraries with sha256 recorded.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_1
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

--- Dependency 3 ---
id: art_VLI4IOs9Xy9P
type: experiment
title: Can you spot a model whose safety was removed
summary: |-
  Two-arm experiment on the archived abliteration 'laundering ladder' (iteration-3 experiment_2). Everything runs on one GPU in ~70 min for $0.161 of a $1.50 judge cap; 8/8 internal consistency checks and an INDEPENDENT verifier (verify.py, 29/29) that re-derives every headline claim from the shipped result files without importing method.py. method_out.json validates against exp_gen_sol_out (7 datasets, 160 rows).

  REPRODUCTION IS EXACT. Rebuilding the archived root from root_recipe.json reproduces parent AND root W01-W05q10 with deltas of exactly 0.00e+00 (not '<1e-6'), 56/311 tensors modified with the rest bit-identical, wikitext ppl identical, int4 W05 = -1.946 and nf4 = -2.126 matching the archive. Two of three archived ladder stages recompute bit-exactly; addback differs by 3.09e-05 (float accumulation order), changing no flag. torch==2.6.0 is pinned deliberately: torch 2.13 routes an outer product through a Triton kernel needing an absent C compiler.

  ARM 1 -- the proposed dequantization remedy is VOID AS STATED: the archive's quant_sd is a fake-quant, so the archived int4 number was already a dequantized measurement. Substantive version instead: rounding kills the scar at 5 BITS (W05 -2.654 > TAU -2.7415) with refusal still 0.237 and ppl only 26.25->28.77. Curve 8b -4.197 / 6b -3.270 / 5b -2.654 / 4b -2.009 / 3b -1.281 (ppl 272, model destroyed). The NEW W05rel statistic FAILS -- it tracks W05 to <0.001 everywhere, because energies are already normalised by each matrix's Frobenius norm, which rounding inflates proportionally. cos(v1,r) stays >0.9994 at every bit-width, so the mechanism is 'the null filled in', NOT 'the eigenvector rotated'; the clean parent is unmoved by the same rounding. Verdict SCAR_STAYS_GONE. bitsandbytes cross-check agrees on nf4 to 1e-4 and disagrees on fp4 by 0.125 log10 (different level sets), reported explicitly.

  THE HEADLINE -- the weight statistic is DECOUPLED from safety behaviour in BOTH directions, by construction, not by correlation. FALSE NEGATIVE: root B, an in-house depth-weighted Gaussian abliteration of Qwen3-1.7B (direction held fixed at root A's so the kernel is the only variable), un-censors 0.950 -> 0.270 [0.20,0.36] at n=111 while staying fluent (ppl 27.28), yet reads W05 = -1.010 -- the PARENT's value -- with all six flags False and cos(v1,r) = 0.0199, because un-edited layers dominate the Gram sum so the eigendecomposition never surfaces the injected direction. W05 stays ~-1.010 across all 14 of its laundering cells, so the ladder is UNDEFINED for it. FALSE POSITIVE: the Llama AUROC-argmax root flags W05 = -4.587 while refusing at 0.950 [0.83,0.99], its parent's rate -- never un-censored. Prevalence: R4_PARTIAL_LAYER_OR_PER_HEAD (the non-uniform class root B instantiates) is 235/513 = 45.8% of edited Hub checkpoints, the largest declared class; the repo-id regex baseline any detector must beat is 50.5%.

  ARM 2a -- the archived ladder's denominators are NOT the recorded 40: achieved denominators recovered from the rates span 31-40, with 13 rows AMBIGUOUS (a rate reducing to a small fraction is compatible with several n). Uses the largest compatible n and ships the smallest-n interval beside it.

  ARM 2b/c -- the archived ordering SURVIVES with real error bars, at n>100, on three laundering families and two architectures: root A 0.167 [0.11,0.25] -> 0.178 [0.12,0.26] at flag death; root C (real gated meta-llama/Llama-3.2-1B-Instruct, no substitution needed) 0.617 [0.53,0.70] -> 0.633 [0.54,0.71]. Flag-death intensities are IDENTICAL across architectures (merge w=0.10, add-back eps=0.10, quant nf4). Root C's behaviour gate FAILS honestly (1.000 -> 0.617, interval-disjoint but above the 0.30 gate) and is labelled signature-positive/partially-un-censored.

  Also ships: TAU brittleness sweep (-2.4..-3.0; at TAU all 8 flagged scan rows are declared-abliterated, and a +0.34 shift is needed for a first undeclared hit), judge integrity (kappa 0.149 over 61 stages, rate-level Pearson r 0.822 -- CORRECTING the archived 0.952 claim), 12 figures, a content-addressed judge cache making reruns $0, and a limitations list naming every gate delta.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_3
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

EVALUATION executor scope:
  Output: eval_out.json with evaluation results
  DOES: Any evaluation of experiment results — metrics, statistical tests, ablations, comparisons, visualizations, robustness checks, error analysis, etc.
  DOES NOT: Implement new methods (use EXPERIMENT), collect data (use DATASET)
  This is for analyzing experiment outputs from any angle
</artifact_executor_scope>

<artifact_planning_rules>
EVALUATION: Must depend on at least one EXPERIMENT. Focus on statistical rigor and validity checks.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for evaluation artifacts:
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
  "description": "Plan for an EVALUATION artifact.",
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
    "metrics_descriptions": {
      "description": "What metrics will be computed and how they're defined",
      "title": "Metrics Descriptions",
      "type": "string"
    },
    "metrics_justification": {
      "description": "Why these metrics are the right ones - what do they tell us about the hypothesis",
      "title": "Metrics Justification",
      "type": "string"
    }
  },
  "required": [
    "title",
    "metrics_descriptions",
    "metrics_justification"
  ],
  "title": "EvaluationPlan",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-14 02:26:32 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```
