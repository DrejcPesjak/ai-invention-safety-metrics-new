# Does a sliding window catch hidden edits?

Tensor-only, prompt-free, **zero forward passes, $0.00 of LLM spend**. Everything
here is re-analysis of checkpoints, tensors and rows already held or
re-downloadable at pinned revisions. Arm B's edited checkpoints are rebuilt **in
memory** from the archived host weights and the archived refusal direction; no
checkpoint is ever written to disk.

## The statistic

For residual-write matrices `W_m` (attention `o_proj` and MLP `down_proj`, in the
archive's catalog order — layer, attn before mlp, then name):

```
A       = sum_m  W_m W_m^T / ||W_m||_F^2          (d x d, accumulated in float32)
lam     = eigenvalues of A, ascending;  v1 = eigenvector of lam[0]
e(u,W)  = ||u^T W||^2 / (||W||_F^2 / d)

W05     = log10( min_m e(v1, W_m) )                        <- the BASELINE (pooled)
W05w(k) = min over windows of log10( min_{m in window} e(v1_win, W_m) )   <- OURS
```

A window is `k` **consecutive layers**, stride `max(1, k//2)`, ragged tail
dropped; `v1_win` is the minimum eigenvector of the Gram accumulated over that
window's matrices only. By construction `W05w(L) == W05`.

Two further baselines are carried side by side in the same pipeline:

* **pooled W05** — the iteration-4 statistic, the thing windowing has to beat;
* **an 11-term case-insensitive regex on the repo id** — free, needs no weights,
  and already solves half the Hub detection task. Its numbers are in
  `results/baseline.json` and in `method_out.json` as `predict_baseline_*`,
  beside ours, on the same rows.

## The three gates, and what they returned

Gates run **first**, before any scoring, and their deltas are reported whether
they pass or fail (`results/gates.json`, `results/gate_kL.json`).

| gate | what it asserts | outcome |
|---|---|---|
| **G1** | the vendored estimator reproduces the archived W01–W05 | max abs dW05 reported against the declared 1e-4; W01/W04 emitted, never gated |
| **G2** | the in-house root rebuilds from `root_recipe.json` verbatim | `write_matrix_sha256` must equal `cd8392d0…`, and W05 must equal −4.5916885 to 1e-4 |
| **G3** | the k=L special case really is W05 | reported under **both** comparisons, see below |

### G3, resolved honestly

Iteration 4 declared a 1e-9 tolerance on the k=L identity, achieved 8.49e-8, and
therefore **failed** its own gate. That tolerance was a float64 tolerance applied
to a float32 quantity. This run reports both comparisons rather than moving a
threshold quietly:

* **(a) `W05w(k=L)` vs `W05_f64`** — the same float64 arithmetic path, gated at
  **1e-9**. This is the comparison that actually tests the window code.
* **(b) `W05w(k=L)` vs the float32 vendored `W05`** — bounded by the float32 dot
  accumulation, *derived in the artifact*:

  ```
  e = ||u^T W||^2 / (||W||_F^2/d);  the dot accumulates d terms, so the relative
  error is bounded by gamma_d = d*eps32/(1 - d*eps32),  eps32 = 2^-24 = 5.96e-8.
  For d = 2048:  gamma_d = 1.22e-4  ->  |dW05| <= log10(1+gamma_d) = 5.30e-5.
  ```

  The 1e-9 comparison is **retained and reported as FAILED at its declared
  tolerance**; the derived 5.30e-5 bound supersedes it, with its derivation
  printed beside it.

## What came out

**All three Arm A tiers completed**: 78 Hub checkpoints scored, 71 resolved, 7 UNRESOLVED
and excluded from every denominator. `verify.py` exits 0 with **60/60** entries
re-derived, and re-running the analysis leaves `numbers.json` and
`method_out.json` **byte-identical**.

The gates were additionally re-run **cold, with no weight cache at all**, and
reproduce exactly: `write_matrix_sha256` matches, `dW05` = 1.543e-5, the k=L
identity is 0.0, and the stamped predictions digest is unchanged. Across the
whole of `results/gates.json` exactly **one** leaf differs between the two runs —
`G2_root_rebuild.seconds`, a wall-clock timing. It is deliberately left in the
file rather than suppressed, and it is the reason the determinism claim above
names `numbers.json` and `method_out.json` specifically: no scientific value in
this artifact is run-dependent, but a stopwatch reading is.

### The headline

On **50 real edited Hub checkpoints**, at specificity **1.000** on the 57 eligible
undeclared negatives:

| statistic | sensitivity | 95% Wilson |
|---|---|---|
| pooled `W05` (= `W05w(k=L)`, the iteration-4 baseline) | **0.300** | [0.191, 0.438] |
| `W05w(k=2)` (ours) | **0.700** | [0.562, 0.809] |
| 11-term repo-name regex | 0.700 | [0.562, 0.809] |
| frozen 8-term repo-name feature | 0.580 | [0.442, 0.706] |

Windowing **more than doubles** real-checkpoint recall at zero false positives.
It ties the 11-term name regex and beats the frozen 8-term feature — while using
no repo name at all, which matters because a name regex is a *declaration*
detector and cannot fire on an undeclared edit by construction.

`catch_by_recipe_class` is populated for every k (it was empty last iteration).
At k = 2, W05w versus pooled W05 by class: partial-layer **0.80 vs 0.00**,
multi-direction SVD **0.80 vs 0.00**, merge **0.75 vs 0.00**, Heretic
**0.62 vs 0.12**, uncensoring SFT **0.62 vs 0.00**, norm-preserving
**1.00 vs 0.83**.

On the in-memory kernel family, **8 of 22** kernels that the pooled statistic
misses at the pre-registered threshold are caught by `min_{k<=8} W05w(k)` at the
*same* threshold: `BAND_MID50`, Gaussian spreads 2/4/8 (both storage
precisions), and `HERETIC_TENT`.

### The prediction scorecard — 6 confirmed, 2 refuted

| | verdict | what it turned on |
|---|---|---|
| P1 band recovery | **CONFIRMED** | `BAND_MID50` W05 −1.010 → W05w(2) −4.722 |
| P2 all small Gaussians recovered | **REFUTED** | 3 of 5. Spreads 0.5 and 1 confine the edit to a **single layer**, so even k = 2 always contains an unedited layer and the minimum is set by it. The smallest detectable edit width equals the smallest usable k. |
| P3 partial-layer class | **CONFIRMED** | 8 of 12 caught at k = 2, **0 of 12** by pooled W05, at matched specificity |
| P4 sub-unit uniform not recovered | **CONFIRMED** | w ∈ {0.5, 0.7, 0.85} undetected at every k and every τ_c. Windowing changes the *scope* of pooling, never the *completeness* of a removal. |
| P5 Householder invisible | **REFUTED** | on the letter of a pre-registered rule that is not moved: at k = 4 and 6 the deviation exceeds the 4-seed control maximum by ~2×. Both are float32 Gram noise — the largest deviation at any k is 2.1e-4 log units against a 1.73 log-unit margin to threshold, ~1e-4 of it. T0.5 verifies the invariance as arithmetic. |
| P6 the two ORBA recipes | **CONFIRMED** | λ=1 reflection undetected at every k; the annihilation recipe detected. Merging them would have made the falsification vacuous. |
| P7 calibration costs recall | **CONFIRMED**, in its strongest form | no calibrated rule reaches specificity 1.0 at any α at any k |
| P8 subspace discovery | **CONFIRMED** | applicable on all six named kernels; predicted-vs-observed agreement **1.000** on 47 |

### The derivation, and the bound that does not exist

The plan expected a small *relative* residual in
`e_W(v1) = e_W(r)·cos²θ + residual`. **It does not exist and cannot.** At the
argmin matrix — the one that sets W05 — both `e_W(v1)` and `e_W(r)` sit at the
annihilation floor (~1e-5), so the cross term is the same order as the terms it
corrects; the relative residual reaches **7.93** even where cos²θ > 0.999.

What *is* bounded obeys a law rather than a bound:

```
|residual(argmin)| / sin^2(theta)  <=  1.726     (median 0.780, n = 22 kernels)
```

The leftover is exactly the energy along the component of `v1` orthogonal to `r`
— `sin²θ` times an O(1) energy scale fixed by the d-normalisation. That is a
derivation with a measured constant, not an empirical observation.

### Both calibrations fail, for two different diagnosed reasons

1. **Random-direction null** — rejects the *unedited parent* at several hundred
   sigma, because `v1_win` is the minimising eigenvector, not a random draw.
2. **Layer-subset null** — also rejects the unedited parent. Measured cause:
   contiguous windows are systematically deeper than random layer subsets
   (parent gap **−0.293** log units) because adjacent layers are more alike than
   randomly chosen ones. That is ordinary depth continuity, not an edit.

A third defect was found and fixed rather than shipped: the naive
min-over-windows-versus-single-subset p-value never falls below **0.3297** for
*any* kernel — not even a complete rank-one projection — so it cannot
discriminate at all. The corrected per-window Šidák construction spans
[0, 0.909] and does separate. Both are reported.

The consequence is a substantive claim, not a caveat: **the multiple-window
hazard cannot be bounded by any within-model null**, because the depth structure
a window exploits is present in unedited models too. It is bounded here by
measured specificity on 57 real undeclared checkpoints.

### The gates

| gate | result |
|---|---|
| G1 wstats reproduction | max abs dW05 = **1.54e-5**, inside the declared 1e-4. On 71 real Hub checkpoints the recomputed W05 matches the archive to **9.6e-6** — an independent third reproduction. |
| G2 root rebuild | `write_matrix_sha256` matches `cd8392d0…` **exactly**; dW05 = 1.54e-5 |
| G3 (a) k=L vs W05_f64 | **0.0 exactly**, at the 1e-9 tolerance — the comparison that tests the window code passes cleanly |
| G3 (b) k=L vs float32 W05 | 1.09e-6: **FAILS** iteration 4's declared 1e-9, **passes** the derived float32 bound of 5.30e-5. Both reported. |

## What each stage produces

| stage | arm | output |
|---|---|---|
| `t0` | — | `results/unit_tests.json` — seven synthetic gates with exact expected values; nothing downloads until all seven pass |
| `s0` | — | `results/s0_env.json` — hardware, versions, sha256 of every copied archive file, and the assertion that `eligibility.py` still hashes to `0f8be4f6…` |
| `s1` | — | `results/gates.json`, `results/gate_kL.json` |
| `s2` | — | `results/predictions_iter5.json` + `.sha256`, stamped **before** any scoring |
| `s3` | 1a | `results/armb_w05w.jsonl` — the kernel family, in memory |
| `s4` | 1b | `results/arma_w05w.jsonl` + `results/arma_tier_status.json` — the Hub checkpoints, tiered, download → score → purge, one at a time |
| `s5` | 2 | `results/frontier.jsonl`, `results/arm2_frontier_summary.json` |
| `s6` | 3 | `results/arm3_subspace.json` |
| `s7` | 4 | `results/derivation.jsonl`, `results/derivation_summary.json` |
| `s8` | — | `results/numbers.json`, `results/predictions_outcome.json`, `results/baseline.json`, `method_out.json` |

`verify.py` is standalone — it imports nothing from the pipeline — and
re-derives every entry of `numbers.json` from the raw rows. The rows are the
truth; if an entry disagrees, the number is wrong.

## Reading guide

Four things in this artifact are worth reading before the numbers.

**One.** The positive arm exists at all. Iteration 4 measured `W05w` with
`n_positives = 0` everywhere, so nothing it said about the windowed statistic
was testable. Arm 1a supplies a kernel family whose ground truth is known by
construction — which layers were edited, which direction was removed, at what
depth weight — so every recovery claim is checkable against the recipe, not
against a label.

**Two.** The plan's random-direction null does not work, and that is reported
rather than repaired quietly. `v1_win` is the *minimising* eigenvector of the
window Gram, not a random draw, so "is this direction unusually low-energy?" is
trivially yes for every checkpoint. Measured on the **unedited host parent**,
`z_min` runs to several hundred sigma. A null that rejects the negative control
is not a calibration. The artifact therefore adds the **layer-subset null**,
which asks the question the multiple-window hazard actually poses — how deep does
the window statistic go for an *arbitrary* set of k layers of this same model? —
and yields the exact multiple-window correction `p = 1 - (1 - F(obs))^n_windows`.
A depth-localised edit lands in the tail of that reference distribution; a global
edit does not, because every k-subset sees a global edit equally.

**Three.** The single-direction discovery condition `|cos(v1, r)| > 0.9` is
**undefined** whenever more than one direction is removed — which is exactly the
multi-direction and per-component kernels that dominate the real misses. Arm 3
replaces it with principal angles between the bottom-j eigenspace and the known
removed span R, scored as `SD = sum cos^2(theta_i) / dim(R)`. Two corrections
were needed to make that well posed and both are in the code: `j` must be at
least `dim(R)` (for smaller `j` the angles only say `V_j` sits inside `R`, which
is vacuous), and the informative `j_star` is the *smallest* containing `j`, not
the largest (containment in `V_j` implies containment in every larger one).

**Four.** For Arm A the removed direction is genuinely unknown, so the
parent-free generalised rule is **inapplicable by construction** and is reported
as such. A direction estimated from the edited model itself would make the test
circular. Where a parent was also scored, a clearly-labelled
*parent-requiring surrogate* is reported instead — it is not the parent-free rule
and is never quoted as one.

## Deviations from the plan, all recorded in the outputs

* **Null seeding.** The plan drew a fresh random-direction ensemble per
  `(model, k, window)`. `e(u, W_m)` does not depend on the window, so one draw of
  512 directions per model is reused for every window: the null is then *paired*
  across windows and across models, which is strictly stronger, and it costs one
  matrix pass instead of one per window. Recorded in `results/s0_env.json`.
* **Heretic per-layer directions.** Iteration 4 computed these from per-layer
  diff-in-means *activations* and did not persist them — `results/directions.json`
  records only `l_star`, the AUROC profile and the two ranks. Recomputing them
  needs forward passes, which are out of scope here, so the family is
  **substituted** with a deterministic one (direction `l` is `r` rotated toward a
  fixed seeded orthogonal direction by an angle growing with depth; drift 0
  collapses to `r`). Every affected row carries `direction_substituted: true`, and
  the archived `heretic_percomponent` W05 = −1.7156 is therefore **not**
  reproducible here and is never compared against.
* **The plan's "2-dim span `[r0_attn, r0_mlp]`" for the Heretic kernel does not
  exist.** `kernels.edit_percomponent` uses the *same* interpolated direction for
  attention and MLP and varies only the weight, so the removed span is
  one-dimensional whatever the per-component weights are. Reported as a
  correction rather than implemented as described.
* **`rank_k` subspaces** are built as the plan specifies — orthonormalised
  `[r, r_perp_1 … r_perp_{k-1}]` — not from the iteration-4 SVD directions, which
  were also not persisted. This is what makes `Q` the ground-truth removed span
  that Arm 3 needs.
* **Householder random-direction control seeds** were reduced from 8 to 4 to fit
  the kernel sweep in budget; `n_control_seeds` is reported on the P5 row.
* **The negative population** is the 57 iteration-4 re-scan rows that resolved and
  passed the frozen eligibility rule, because those already carry `W05w`. The
  archived eligible population was scored at **W05 only** and is labelled
  `W05-only, not re-scored at W05w` — it is never pooled into a `W05w`
  denominator.

## Honesty rules this artifact holds itself to

* Gated / 404 / unresolved-architecture rows are recorded with
  `status = "UNRESOLVED"` and a reason, and are **excluded from every
  denominator**, with the exclusion count printed beside every rate.
* Arm A reports **which tier completed**, never a promised target
  (`results/arma_tier_status.json`, and `metadata.tier_completed` in
  `method_out.json`).
* Every threshold says whether it was fitted, on what, and carries a
  `circularity_flag`. Specificity-matched thresholds are fitted on the
  **negatives only** — they never see a positive — but they are quoted on the
  same negative population they were fitted on, and every row says so.
* A refuted prediction is a headline, not a footnote:
  `results/predictions_outcome.json` gives CONFIRMED / REFUTED / UNSCORABLE with
  the observed number for all eight.

## Running it

```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
uv pip install --python=.venv/bin/python numpy scipy safetensors huggingface-hub pandas tqdm loguru requests psutil

.venv/bin/python method.py --stage t0,s0,s1,s2      # gates + stamped predictions
./run_s3.sh                                          # Arm 1a, chunked so RSS stays bounded
.venv/bin/python method.py --stage s4 --arm-a-budget-min 120
.venv/bin/python method.py --stage s5,s6,s7,s8   # purges hf_cache/ at exit
.venv/bin/python verify.py
```

**`hf_cache/` is scratch and is purged automatically.** Each Arm A repo is deleted
the instant it has been scored, but the host snapshot is held for the lifetime of
a run because all 47 kernels are rebuilt from it — about 3.9 GB of Qwen3-1.7B
shards, with individual blobs of 3.3 GB and 594 MB, well over the 100 MB
per-file publication limit. So `method.py` deletes the whole cache at the end of
every run and logs the gigabytes freed; pass `--keep-cache` to retain it for
iterative work. Nothing downstream reads it: the scored rows live in `results/`,
and a cold rerun re-fetches the host in about seven seconds at its pinned
revision. That path is exercised, not assumed — the gate stages above were re-run
from an empty workspace.

`torch==2.6.0` is pinned deliberately: 2.13 routes `torch.outer` through a Triton
kernel that needs a C compiler which is absent here. The chunked `run_s3.sh` is
also not cosmetic — glibc keeps freed arenas per thread, so a loop allocating and
releasing ~1 GB of 2048×2048 float64 workspaces per kernel walks into the cgroup
limit around the fortieth kernel unless `malloc_trim` runs (it does) and the
process is periodically restarted (it is).
