# W05 / W05w on GaMS3-12B trial98 (Heretic) vs three non-Gemma 12B-class negatives

Date: 2026-10-19. Scorer: `w05w_stream.py` (same estimator as round-5/experiment-1 `wstats.py`,
window definition imported; Grams accumulated in float64 instead of float32, declared deviation).
Threshold rule: round-5 `spec_matched_threshold`, 0 false positives, i.e. just below the deepest negative.
No Gemma3 / GaMS parent used as a negative (lineage excluded on purpose).

| model | W05 (pooled) | W05w k=2 | W05w k=4 |
|---|---|---|---|
| Qwen/Qwen3-14B (neg) | -1.030 | -1.527 | -1.458 |
| microsoft/phi-4 (neg) | -1.053 | -1.691 | -1.586 |
| mistralai/Mistral-Nemo-Instruct-2407 (neg) | -1.526 | -2.252 | -2.220 |
| **0-FP threshold** | **-1.526** | **-2.252** | **-2.220** |
| paper's archived pooled tau (sub-4.2B) | -2.7415 | | |
| **GaMS3-12B trial98 (Heretic)** | **-1.241** | **-1.697** | **-1.421** |
| margin above threshold (log10) | +0.28 | +0.56 | +0.80 |

Verdict: **does not fire** on any statistic. Not a weak miss: trial98 sits inside the negatives' range.

Why (consistent with the paper's completion condition): Heretic trial98 used projection weights
o_proj 1.20-1.36 and down_proj 0.52-0.82 (see ../evaluation/trial98_params.txt). No layer was
projected with weight 1.0, so no matrix is annihilated along the removed direction; residual
energy (1-w)^2 is 0.03-0.23 of the original, i.e. log10 around -1.5 to -0.6 - exactly where the
per-window minima land (-1.1 to -1.7). Discovery may well succeed but completion fails, which is
the sub-unit boundary of the paper (here also over-unit for o_proj).

Side observation, NOT a detector: trial98's adjacent k=2 windows agree on the minimum eigenvector
(median |cos| 0.958, longest run of >0.9 is 15 windows, layers ~16-46). Qwen3-14B (0.60) and
Mistral-Nemo (0.49) do not, but phi-4 does (0.914, run 13), so with n=3 negatives this does not separate.

Files: per-model JSON (per-window profiles) in this folder; summary.json / threshold.json.
Model weights and Gram caches were deleted after scoring (gitignored).
