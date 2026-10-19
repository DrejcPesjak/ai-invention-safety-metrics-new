# Does a sliding window catch hidden edits?

`demo/` — Self-contained demo (Colab-ready notebook or markdown). Run without setup.  
`src/` — Full source code, data, and outputs from the experiment execution.

**Type:** experiment  
**ID:** `art_-wY3_BLZ_sCu`

## Layman Summary

Scanning a model's weights in small sliding chunks, instead of averaging them all together, more than doubles how many secretly safety-stripped models get caught, with no false alarms.

## Full Summary

EXECUTED end to end. $0.00 OpenRouter spend, zero prompts, zero forward passes. ALL THREE Arm A tiers COMPLETE (78/78 Hub checkpoints scored, 71 OK, 7 UNRESOLVED excluded from every denominator) plus 47/47 in-memory kernels. verify.py (standalone, imports nothing from the pipeline) exits 0 with 60/60 entries re-derived from the raw rows; re-running the analysis leaves numbers.json and method_out.json BYTE-IDENTICAL.

HEADLINE, the first clear positive for windowing. On 50 real edited Hub checkpoints at specificity 1.000 (57 eligible undeclared negatives): W05w(k=2) sensitivity 0.700 [0.562, 0.809] versus pooled W05 0.300 [0.191, 0.438]. Windowing MORE THAN DOUBLES real-checkpoint recall at zero false positives. It ties the 11-term repo-name regex baseline (0.700) and beats the frozen 8-term feature (0.580) while using no repo name at all, which matters because a name regex is a declaration detector and cannot fire on an undeclared edit. catch_by_recipe_class is populated for every k (it was EMPTY in iteration 4): at k=2, W05w vs W05 is partial-layer 0.80 vs 0.00, multi-direction SVD 0.80 vs 0.00, merge 0.75 vs 0.00, Heretic 0.62 vs 0.12, uncensoring SFT 0.62 vs 0.00. On the kernel family, 8 of 22 pooled misses are recovered at the same pre-registered threshold (BAND_MID50, Gaussian spreads 2/4/8 at both storage precisions, HERETIC_TENT).

GATES. G1 max |dW05| = 1.54e-5; across 71 real Hub checkpoints the recomputed W05 matches the archive to 9.6e-6 (an independent third reproduction). G2 write_matrix_sha256 matches cd8392d0... EXACTLY. G3 resolved honestly under BOTH comparisons: (a) W05w(k=L) vs W05_f64 = 0.0 exactly at the 1e-9 tolerance, the comparison that actually tests the window code; (b) vs the float32 W05 = 1.09e-6, reported as FAILING iteration 4's declared 1e-9 and passing a DERIVED float32 accumulation bound log10(1+gamma_d) = 5.30e-5 at d=2048. The tolerance was not moved silently.

PREDICTIONS, stamped by sha256 before any scoring: 6 CONFIRMED, 2 REFUTED, both refutations reported with mechanism. P2 REFUTED 3/5 -- Gaussian spreads 0.5 and 1 confine the edit to ONE layer, so even k=2 always contains an unedited layer that sets the minimum: the smallest detectable edit width equals the smallest usable k. P5 REFUTED on the letter of a pre-registered rule that was NOT moved (k=4,6 exceed the 4-seed control max by ~2x), though both quantities are float32 Gram noise, 2.1e-4 log units against a 1.73 log-unit margin. P4 CONFIRMED: sub-unit uniform w in {0.5,0.7,0.85} invisible at every k and every tau_c -- windowing changes pooling SCOPE, never removal COMPLETENESS.

ARM 2, a substantive negative. BOTH calibrations reject the UNEDITED control, for two separately diagnosed reasons: the random-direction null because v1_win is the MINIMISING eigenvector rather than a random draw (parent at several hundred sigma), and the layer-subset null because contiguous windows are systematically deeper than random layer subsets (parent gap -0.293 log units) from ordinary depth continuity. Conclusion: the multiple-window hazard CANNOT be bounded by any within-model null; it is bounded here by measured specificity on real undeclared checkpoints. A third defect was found and fixed rather than shipped: the naive min-over-windows-vs-single-subset p never falls below 0.3297 for ANY kernel, not even a complete rank-one projection; the corrected per-window Sidak construction spans [0, 0.909] and discriminates.

ARM 3: generalised subspace discovery via principal angles, agreement 1.000 on 47 applicable kernels, P8 applicability complete. Two corrections were required and are in the code: j must be at least dim(R), and j_star is the SMALLEST containing j, not the largest. Arm A is INAPPLICABLE BY CONSTRUCTION (removed direction unknown; imputing it would be circular) -- only a labelled parent-requiring surrogate is reported.

ARM 4: the plan's small RELATIVE residual does not exist and cannot -- at the argmin matrix both energies sit at the annihilation floor, so the relative residual reaches 7.93 even at cos^2(theta) > 0.999. What holds is a LAW with a measured constant: |residual| / sin^2(theta) <= 1.726 (median 0.780, n=22).

CAVEATS. Iteration 4 did NOT persist the per-layer diff-in-means or SVD directions, so the archived heretic_percomponent W05 = -1.7156 is NOT reproducible without forward passes; a deterministic substitute is used and every affected row carries direction_substituted. kernels.edit_percomponent uses the SAME direction for attn and mlp, so the plan's '2-dim span [r0_attn, r0_mlp]' does not exist -- the removed span is 1-dimensional.

## Dependencies

- `art_8OlSrcw-hzgO` — dataset
- `art_CKWQh2cOQLLQ` — prompts
- `art_gqCRODISeyg2` — recipe spec
- `art_sHF0cggp2IvT` — recipe spec

## Output Files

- `method.py`
- `full_method_out.json`
- `mini_method_out.json`
- `preview_method_out.json`

## Demo Files

- **method.py** — Research methodology implementation

---
*Generated by AI Inventor Pipeline*
