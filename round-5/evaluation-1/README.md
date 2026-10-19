# One numbers file the paper must obey

`demo/` — Self-contained demo (Colab-ready notebook or markdown). Run without setup.  
`src/` — Full source code, data, and outputs from the experiment execution.

**Type:** evaluation  
**ID:** `art_gSQc4W6QUHvZ`

## Layman Summary

Re-checks every number in the paper against the raw saved data, finds two dozen that were wrong or overstated, and ships a checker that refuses to pass if any number stops matching.

## Full Summary

PURE RE-ANALYSIS of the archived iteration-2/3/4 trees. ZERO model weights, ZERO forward passes, ZERO Hub fetches, ZERO LLM calls, $0.00 of the $10 cap, ~45 s wall clock. Ships numbers.json (211 entries, schema-EXTENDED from A2/results/numbers.json so the two merge: the same nine keys plus key_path/raw_value/recomputed_from_rows/orientation_convention/status/note) and verify_numbers.py, which imports NOTHING from the analysis and recomputes from raw rows: 151 PASS / 0 FAIL / 0 UNAVAILABLE, exit 0. Determinism BYTE-IDENTICAL across two builds in two OS processes (8 files, sha256 each). Assertions 102 MATCH / 2 MISMATCH / 0 UNAVAILABLE; neither mismatch was silently fixed -- each became a corrections[] entry with the archive's row-level value winning.

POOLS REBUILT FROM ROWS, WITH A GATE. Positives 67 = 44 real Hub edits (Arm A) + 23 in-house kernels (Arm B); the pooling assumption REPRODUCES n_fit_positives = 67 - n_held_out for ALL 19 lorco cells. Negatives 32 = 20 Arm-A declared parents + 11 unique archived iteration-3 parents + the Arm-B host, and ALL NINE Arm-A class AUROCs reproduce the archive at delta 0.00e+00 -- that exact reproduction is what licenses the pool. NOTE: the archive carries 19 lorco cells, not the 20 the plan expected (C18).

HEADLINE FINDINGS. (1) THE OPERATING POINT IS ARBITRARY: holding out one recipe class moves tau by 1.0259 log10 (-2.7415 -> -1.7156), 8.04x the 0.1276 shift that already yields the first false positive. (2) SPECIFICITY DOES NOT SURVIVE REFITTING: 0/139 eligible undeclared checkpoints fire at the panel tau, but 13/139 fire at the refit tau (0.094, Wilson [0.055, 0.153]); the chat/instruct subset is n=36 with 0 firing, Wilson [0.000, 0.096] -- too small to stand in for the at-risk population. A ready-to-paste narrower-claim sentence is emitted. (3) NEW, HIGH-VALUE: the archived auroc_oriented column reports max(raw, 1-raw) and records its orientation PER CELL, so 8 of 19 cells print under the OPPOSITE orientation to the rule W05 <= tau; holding orientation fixed at lower-is-positive, those same 8 classes fall BELOW CHANCE (C24). (4) The archived 0/122 denominator is a MID-SCAN SNAPSHOT: recounted from rows it is 82 archived + 57 newly scanned = 139, numerator still 0, so precision is STRONGER (C22).

DERIVATION SETTLED BY A NUMBER. The Cauchy-Schwarz bound is emitted as a formula string plus a callable and EVALUATED on 25 archived rows: 0 violations, and over discovery-holding rows where the bound is informative max |W05 - log10 min_m e_r| = 0.029 log10 (n=5), reproducing the three quoted anchors. '19/19 with zero disagreements' is therefore RETIRED as evidence, alongside W05rel, W01/W04, the dequantization remedy, and uniformity-as-predicate, each with the licensing row. |cos| is clipped at 1-2^-23 because abscos_v1_r is stored in float32. Undefinedness is COMPUTED not asserted: 12 of 44 scored edited rows (draft said 13 -> C20), repo_ids listed; the principal-angle generalisation is stated as a DEFINITION, labelled NOT-YET-EVALUATED. Proposition 1 (isometry impossibility) carries proof sketch, the ORBA two-recipe caveat, an explicit note that it covers W05w, and measurement: ORBA moves W05 by 4.08e-05, BELOW a random-direction control at 7.26e-05. Effectiveness vs detectability: 10 effective kernels, 4 detected; Spearman 0.113, bootstrap [-0.641, 0.700] over 25 kernels -- the CI is what makes 'near-orthogonal' sayable.

ALSO SHIPS. results/corrections.json: 24 entries, each {id, claim_as_previously_reported, corrected_value, provenance{file,key,raw_value}, recomputed_from_rows, one_sentence_for_the_paper}, including 81 unresolved / 8 skipped / 270=20+250 arithmetic asserted, five unreproduced quoted values, B09 0.766-vs-0.670, ladder denominators 31-40 with 13 ambiguous, the power calc (smallest detectable DIFFERENCE 0.294 at n=40/p=0.20 -- a difference, not a rate), judge r 0.822 / kappa 0.149, the bit-width curve (scar dies at 5 bits), storage precision -4.592 bf16 vs -12.705 float32, E_1 13/32 vs W05 7/35 agreeing 0.829 under the archived convention, and the 0.727 regex as a NAME-SEARCH UPPER BOUND. results/edit_list.json: 34 numbered mechanical edits, 33 blocking, with 25 backward references LOCATED in the iteration-4 draft on disk (not merely rules), the numbered section skeleton + cross-reference map, Contributions cut to four finding-shaped strings plus a REMOVE list, the self-audit moved to Appendix A (both text variants), the 12.6 toy figure deleted with both pre-written fallbacks, the k=L tolerance question with both sentences and which the numbers support, and arm-dependent sentences flagged from A2's zero-positive markers. results/carry_forward.json: 130 values with full provenance. Statistics discipline: Wilson formula and continuity flag printed, percentile bootstrap n_boot=10000 with default_rng(20260814) and the resampling unit named per statistic, numbers.json never rounded.

## Dependencies

- `art_dp7WBo6hhVBX` — reanalyzes
- `art_VFF9Dum9x3KJ` — reanalyzes
- `art_VLI4IOs9Xy9P` — reanalyzes
- `art_xyUlckdGtbjc` — battery
- `art_BCxIq6GX4WIw` — dataset

## Output Files

- `eval.py`
- `full_eval_out.json`
- `mini_eval_out.json`
- `preview_eval_out.json`

## Demo Files

- **eval.py** — Evaluation script with metrics computation

---
*Generated by AI Inventor Pipeline*
