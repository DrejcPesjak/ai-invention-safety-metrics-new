# Auditing last round's negative results

`demo/` — Self-contained demo (Colab-ready notebook or markdown). Run without setup.  
`src/` — Full source code, data, and outputs from the experiment execution.

**Type:** evaluation  
**ID:** `art_80jPj8Mr_dbZ`

## Layman Summary

Re-checks the previous round's three experiments without rerunning them, and finds that several of its headline negative conclusions do not hold up once the statistics and labels are fixed.

## Full Summary

PURE RE-ANALYSIS of the three archived iteration-1 trees (E1 refusal-wobble/SPI, E2 steering hysteresis, E3 behavioural ground truth + judge). No model inference, no GPU, no rerun of any iteration-1 experiment. Estimators (paired_bootstrap_diff, cluster_bootstrap_ci, half_life_auc, wilson_ci) are IMPORTED from E1/spi/indicators.py; E1's spearman() and build_output.py's verdict rule are transcribed verbatim, so every archived number reproduces exactly before anything is changed. Spend $0.0586 of a $1.00 cap, 537 logged calls; every response cached so a rerun costs $0 and reproduces in 18 s.

RECONCILIATION TABLE: 46 rows, 25 SURVIVES / 12 CHANGED / 9 RETRACTED / 0 UNTESTED, each with original value, re-derived value and the deciding analysis.

A1 (lambda inconsistency): CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING is CHANGED / MATERIAL_CHANGE_TO_REPORTED_RESULT. Running E1's own rule on decay_ratio_16 and normalised-AUC over the same 240 certified rows: at the PRE-STATED primary readout (layer L, where the perturbation is injected) the random-direction control separates 0/3 while the refusal treatment separates 2/3 - the REVERSE of the reported pattern. It reproduces only at the final-layer readout (lens-vs-final corr 0.17-0.26). Not cosmetic: lambda vs decay_ratio_16 Spearman -0.459 (layerL) / -0.170 (final). Horizon sweep {8,16,32,64} and lineage-level bootstrap included; the -0.226/-0.493 lambda CIs are reprinted DEMOTED under lambda_ci_consistency_check_NOT_IDENTIFIABLE.

A2 (observable-validity gate): only 1 of 4 members passes r_0 AUROC>=0.70 (instruct 0.793; abliterated 0.481, base 0.414, smollm2 0.633) -> UNSUPPORTED_ONLY_1_MEMBERS_PASS. 'Indicators track lineage, not safety' is RETRACTED as a settled negative and downgraded to a qualitative observation. Sensitivity curve {0.60,0.65,0.70,0.75,0.80} published; n_passing=1 from 0.65 up.

A3 (judge probe rebuilt, the only paid arm): 197 items, four classes, fixed seed, all 21 original probe items carried forward; two annotators decorrelated in model family AND rubric framing (gemini-3.5-flash-lite + frozen rubric; mistral-small + independent decision tree), kappa 0.337 [0.259,0.415]; 96 disagreements adjudicated by deepseek-v4-flash; 97 disputed items published verbatim. 0/7 -> 7/82 = 0.085 [0.042,0.166] frozen-judge COMPLIANCE recall vs 0.939 repaired: 'never assigns COMPLIANCE' is literally wrong but the failure is confirmed and quantified. 3 of 21 original truth labels contradicted, including the force-included 'Certainly! Here's a message that conveys hope...' case (prefix-labelled COMPLIANCE, adjudicated PARTIAL) -> the 21/21 gold arm is RETRACTED. Both headline revisions reproduce exactly (0.700->0.113, 0.092->0.858) and STRENGTHEN under misclassification correction: 0.113 -> 0.000 [0,0.069]; 0.858 -> 0.904 [0.857,0.974].

A4 (n=4): all 24 orderings enumerated. rho=-0.20 reproduces exactly, exact two-sided p=1.000 against p_floor 0.4167 (untied floor 2/24=0.0833) - nothing at this panel size can reach 0.05. Two independent kills: only 1 of 4 members is above the refusal/incapacity floor, and E1's spearman() breaks ties by array position with two members tied at 0.000 - average ranks give +0.105, a SIGN FLIP. corrected_claim_text and numbers_to_drop emitted.

A5 (prereg fidelity): 15 deviation rows (7 unannounced), all eight E2 amendments present, each with trigger, timestamp, date-source and direction of effect. Excess-width sign inversion CONFIRMED (paper uses forced_A - alpha_down; prereg the negation) but the two-sided conclusion is INVARIANT - recorded as a reporting error, deliberately not inflated. alpha_50 gap 0.075 = 1.5 grid steps with 5 Bernoulli draws/point; bootstrapped intervals [0.383,0.538] and [0.483,0.617] OVERLAP -> alpha_50_gap_is_resolvable=false, RETRACTED. refusal_direction.pt feeds ONLY E3's in-house ladder (E1 and E2 fit their own directions). Abliteration coverage COMPLETE (o_proj + down_proj + embed_tokens), so under the pre-stated relabel rule the SNAPPED failure attaches to the technique - but the defensible sentence is 'our single-direction weight-edit implementation did not produce a graded knob at 0.6B scale'.

DELIVERABLES: eval.py single entry point (inventory|a1|a2|a3|a4|a5|finalize|all, --stage smoke); eval_out.json (exp_eval_sol_out-valid, 6 datasets / 348 examples / 53 metrics / 15 limitations); out/{input_inventory,gate_definition,a1_lambda,a2_gate,a3_probe,a4_permutation,a5_prereg,reconciliation_table,disputed_items,field_substitutions}.json, out/llm_call_log.jsonl, out/a3_annotation_cache.jsonl; 4 figures (F1 verdict-flip matrix, F2 gate, F3 judge confusions, F4 exact permutation null) as PNG+PDF.

FOR THE PAPER: cite the reconciliation table's re-derived values, not the iteration-1 originals. Do NOT carry forward as settled: the generic-mixing verdict, 'indicators track lineage not safety', the alpha_50 instruct-vs-abliterated gap, the 21/21 judge probe, or any n=4 ordering claim.

## Dependencies

- `art_UthAQuH8WZ5C` — reanalyzes
- `art_W0HSULPgrt3K` — reanalyzes
- `art_TFe9eI-2QZN3` — prereg audit

## Output Files

- `eval.py`
- `full_eval_out.json`
- `mini_eval_out.json`
- `preview_eval_out.json`

## Demo Files

- **eval.py** — Evaluation script with metrics computation

---
*Generated by AI Inventor Pipeline*
