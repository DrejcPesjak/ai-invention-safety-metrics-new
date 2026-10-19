# One numbers file the paper must obey

Pure re-analysis of the archived iteration-2/3/4 trees. **Zero model weights loaded, zero
forward passes, zero Hub fetches, zero LLM calls, $0.00 of the $10 cap.** Wall clock ~45 s.
Every number is either recomputed from archived raw rows or carried forward verbatim with
provenance `{file, key_path, raw_value}`. A required key that is absent becomes
`status="UNAVAILABLE"` with the path probed — never an estimate.

```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python numpy scipy loguru
.venv/bin/python eval.py                 # full: builds twice, diffs, verifies, emits eval_out.json
.venv/bin/python eval.py --outdir DIR    # single build into DIR
.venv/bin/python verify_numbers.py       # standalone checker; exits 1 on any FAIL
```

## Headline results

| | |
|---|---|
| assertions | **102 MATCH / 2 MISMATCH / 0 UNAVAILABLE** (both mismatches became corrections) |
| `verify_numbers.py` | **151 PASS / 0 FAIL / 0 UNAVAILABLE**, exit 0 |
| determinism | **byte-identical** across two builds in two OS processes (8 files, sha256 each) |
| numbers.json | 211 entries, schema-compatible with `iter_4/.../experiment_2/results/numbers.json` |

**The operating point is essentially arbitrary.** Holding out one recipe class moves the
fitted threshold by **1.026 log10 units** (−2.7415 → −1.7156), about **8.0×** the 0.128
shift that already produces the first false positive on the eligible undeclared population.

**Specificity does not survive refitting.** 0/139 eligible undeclared checkpoints fire at
the panel operating point, but **13/139** fire at the class-held-out refit threshold
(rate 0.094, Wilson 95% [0.055, 0.153]). Zero false positives is a property of a threshold
fitted on the panel, not of the statistic. The chat/instruction-tuned subset is n=36 with
0 firing, Wilson [0.000, 0.096] — too small to stand in for the population at risk.

**AUROC orientation was flipped per cell.** The archived `auroc_oriented` column reports
`max(raw, 1−raw)` and records which orientation it chose. Holding the orientation fixed at
lower-is-positive, as the rule `W05 ≤ tau` requires, **8 of 19 classes fall below chance**.
This is the single most consequential correction in the table.

**Discovery ⇒ detection = completion, by definition.** Over discovery-holding rows where
the Cauchy–Schwarz bound is informative, `|W05 − log10 min_m e_r|` is at most **0.029**
log10 units (n=5), inside the analytic bound on **every** row (0 violations over 25 rows).
"19/19 with zero disagreements" is therefore retired as evidence.

**Isometric edits are permanently invisible** (Proposition 1): ORBA moves W05 by
4.08e-05, *below* a random-direction Householder control at 7.26e-05. The proposition
covers W05w, so the windowed arm cannot recover them regardless of outcome.

**Detectability and effectiveness are near-orthogonal**: 10 kernels remove refusal,
only 4 are detected; Spearman ρ = 0.113, bootstrap 95% [−0.641, 0.700] over 25 kernels.

## Files

| file | contents |
|---|---|
| `eval.py` | the analysis, stages 0–5 + determinism + verify (`archlib.py` holds shared helpers) |
| `verify_numbers.py` | standalone checker — **imports nothing** from `eval.py`/`archlib.py` |
| `numbers.json` | **the** file the paper regenerates every numeral from |
| `eval_out.json` (+ `mini_`/`preview_`) | `exp_eval_sol_out` schema, PASSED |
| `results/archive_inventory.json` | 59 archive paths, sha256 + sizes + key lists, 0 missing |
| `results/lorco_table.json` | the four-column table, tau shift, specificity at both taus |
| `results/derivation.json` | the bound, the ladder, retirements, undefinedness, Proposition 1 |
| `results/corrections.json` | 24 corrections, each with provenance and a paste-ready sentence |
| `results/edit_list.json` | 34 numbered edits (33 blocking), 25 backward references located |
| `results/carry_forward.json` | 130 values with `{file, key_path, raw_value}` |
| `results/assertions.json`, `results/verify_report.json`, `results/determinism.json` | audit |

## What the pools are, and why they are trustworthy

Rebuilt **from rows**, never from summaries:

- **Positives (67)** = 44 real Hub edited checkpoints (Arm A) + 23 in-house kernels (Arm B).
  The pooling assumption reproduces `n_fit_positives = 67 − n_held_out` for **all 19** cells.
- **Negatives (32)** = 20 Arm-A declared parents + 11 unique archived iteration-3 parents +
  the Arm-B host. **Gate:** all nine Arm-A class AUROCs reproduce the archive at
  Δ = 0.00e+00. That exact reproduction is what licenses the pool.

Arm-B class labels are derived by an explicit rule (uniform_subunit by `w`, gaussian_depth
by `min_depth_weight ≥ w*`, …) and every per-cell count is checked against the archive.

## The two mismatches (both are findings, not bugs)

1. **`fp_rate_filtered_primary.n` 139 vs archived 122** — the archived rate file was written
   *mid-scan*; recounted from the rows now on disk the eligible undeclared population is
   82 archived + 57 newly scanned = 139. The numerator is still 0, so this makes the
   precision claim **stronger**. (Correction C22.)
2. **Undefinedness count 12 vs the draft's 13** — the single-direction discovery rule is
   undefined on 12 of the 44 scored edited checkpoints (R_MULTIDIR_SVD ∪ R_HERETIC).
   (Correction C20.)

Per policy, MISMATCHes are never silently fixed: each becomes a `corrections[]` entry and
the archive's row-level value wins over any prose value.

## Statistics discipline

- Wilson intervals for every proportion, formula printed in `numbers.json`,
  `continuity_correction=False` stated explicitly.
- Percentile bootstrap, `n_boot=10000`, `numpy.random.default_rng(20260814)` (never the
  legacy global RNG), resampling unit named per statistic.
- The power calculation is stated in full: two-sided two-proportion z-test, pooled-variance
  null, α=0.05, power=0.80, n=40/group, grid step 1e-4 — giving a smallest detectable
  *difference* of 0.294 at p₁=0.20 (note: a **difference**, not an alternative rate).
- `numbers.json` is **never rounded**. Rounding appears only inside ready-to-paste sentence
  strings, and the rule is stated there.
- AUROC orientation is fixed at lower-is-positive for every cell of the recomputed column.

## Determinism

Sources of nondeterminism eliminated up front: every key list `sorted()`, `json.dumps`
with `sort_keys=True` and full float precision, seeded `default_rng`, no timestamps in any
output, sorted globs. Run 2 executes in a **separate OS process**, so the check covers
process-level determinism and not just function purity.
