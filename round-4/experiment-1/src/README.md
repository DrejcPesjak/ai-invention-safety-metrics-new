# Is the parent-free abliteration weight scar about UNIFORMITY?

`W05 = log10( min_m ||v1^T W_m||^2 / (||W_m||_F^2 / d) )`, where `v1` is the
eigenvector of the **smallest** eigenvalue of the shared Gram matrix
`A = sum_m (W_m W_m^T)/||W_m||_F^2` over the residual-write matrices
(`self_attn.o_proj`, `mlp.down_proj`) of every layer.

It needs **no parent, no prompt and no forward pass**. Iteration 2 reported it
separating 8 abliterated checkpoints from 36 non-abliterated ones at AUROC
1.000 on a 0.0763 log-margin. This artifact asks what its boundary actually
*is*, and answers it mechanically rather than by adding checkpoints.

**Claim under test.** W05 fires when the edit is a *uniformly complete,
rank-reducing* projection across the whole stack, and misses when the same
direction is removed by a depth-weighted kernel, a layer band, a sub-unit
weight, or an orthogonal factor — regardless of who uploaded the checkpoint or
what architecture it is.

## What came out

**The detector is precise and nearly blind.** Specificity is 1.000 — zero false
positives on 32 negatives, including 20 freshly measured Hub parents. Sensitivity
is not: on a recipe- and uploader-diverse sample of **44 real edited checkpoints
from 27 uploaders across 9 recipe classes, it fires on 7 (0.159)**, while the
five archived panel members it was calibrated on all still fire (1.000). Five of
those seven detections are a single uploader's norm-preserving family; a sixth
(`huihui-ai/Qwen2.5-Coder-0.5B-Instruct-abliterated`, W05 = −2.829) clears
τ = −2.7415 by 0.09.

**It does not beat a filename regex.** On the same Arm A rows, a plain regex over
the repo id scores sensitivity **0.727** at specificity 1.000, against W05's
**0.159**. The set of checkpoints W05 catches that the name misses is **empty**.

**The misses are not near-misses.** For most undetected edits the paired
child-minus-parent shift in W05 is ~0: `mlabonne/Qwen3-0.6B-abliterated` reads
−0.9637 against its parent's −0.9641. The edit leaves no trace in this statistic
at all.

**The in-house sweep says why, and the mechanism is not the stamped one.**
Holding the host and the refusal direction fixed and varying only the kernel,
detection needs two things at once, and a post-hoc rule combining them reproduces
**19/19** of the applicable kernels:

1. *discovery* — enough of the stack is edited along `r` that `r` becomes the
   Gram's minimal direction (`|cos(v1, r)| → 1`);
2. *completion* — some matrix is annihilated along `r` deeply enough to cross τ.

Uniformity was the wrong predicate. The Gaussian sweep makes this concrete: every
spread annihilates the peak layer completely (`log10 min_m e_r` = −4.53 at *all*
spreads), yet detection only switches on between spread 8 and 16 — where the
*minimum* depth weight crosses somewhere in [0.08, 0.53], nowhere near the
stamped `w* = 0.9533`. The transition occupies 2 sweep steps, so the stamped
*shape* (threshold, not ramp) held while the stamped *critical spread* was wrong
by 3.6×. The middle-50% band edits half the stack completely and is still missed,
because the untouched half keeps `r` from ever becoming the minimal direction.

Leave-one-recipe-class-out splits the same way. Scored at the ±0.5 tolerance the
stamped rule uses, it matches **7/7** Arm B classes — where the removed direction
is known and correct — and **4/6** Arm A classes, where the detector has to
discover the direction itself. The two Arm A misses are `R_MULTIDIR_SVD`
(held-out sensitivity 0.000, n=5) and `R_GLOBAL_RANK1` (0.333, n=6), both
predicted 1.0. One Arm B row is a marginal pass rather than a clean one:
`ARMB_GAUSSIAN_DEPTH__NONUNIFORM` was predicted 0.0 and observed 0.286, because
the two widest Gaussians in the sweep *are* detected — which is the same
threshold effect P10 describes, not an independent confirmation.
Specificity is 1.000 in every leave-one-out cell.

**Effective edits are the ones it misses.** Of 10 fluency-passing in-house edits
that actually remove refusal (judge-scored ≤ 0.50 on the frozen 40-item core,
against the host's 0.925), only **4** are detected. The two *most* effective are
both invisible: ORBA's Householder drops refusal to **0.100** and moves W05 by
4.1e−5 — *less* than a Householder about an unrelated random direction moves it
(7.3e−5), i.e. below the measured noise floor; the Heretic-style kernel drops it
to **0.125** and is missed.

**A reproducibility finding fell out of the gate.** The rebuilt in-house root is
**bit-identical** to the archive (`write_matrix_sha256` matches), and W02/W03/W05
reproduce to 1.3e−5 — yet W01 and W04 differ by 3.1e−2. With byte-identical
weights that gap cannot be the model: both are log ratios against `lam[0]`, which
on an abliterated checkpoint sits ~5 orders below the trace and is at the float32
Gram-accumulation floor. Recomputing in float64 moves W01 by exactly the amount
the archive disagrees by (4.7894e−2 vs 4.7894e−2). W01 and W04 are not
reproducible below ~0.05 on abliterated checkpoints; W05 is, and nothing here
depends on W01 or W04.

**Storage precision caps the scar.** The same complete uniform projection reads
W05 = −4.59 stored in bf16 and −12.70 stored in float32. bf16 rounding, not the
edit, sets the archived depth.

Scored verdicts on the 13 stamped predictions: P1 P2 P3 P6 P7 P9 P11 confirmed,
P8 confirmed at the measured noise floor, P10 shape-confirmed / critical-spread
refuted, P12 partial, **P4 P5 P13 refuted**. Two falsifiers fired and are the
headline, not a footnote.

## How to run

```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r reqs.txt
.venv/bin/python method.py                      # all stages
.venv/bin/python method.py --stages s5,s6       # re-analyse what is on disk
```

Every stage appends and fsyncs its own `results/*.jsonl` before moving on, so a
timeout leaves a reportable tier rather than nothing.

## Design

| stage | what it does |
|---|---|
| `s0` | hardware limits; sha256 of every vendored archive library |
| `t` | six synthetic unit tests on a toy stack (d=64, L=12) |
| `s1` | reproduction gate against the archived iteration-3 numbers, plus a fast-path agreement test and a float32→float64 conditioning diagnostic |
| `s2` | the **signed prediction table**, stamped and hashed *before* any new checkpoint is downloaded |
| `s4a` | rebuild the archived in-house abliteration root and check it reproduces; measure `W05_ref` and stamp the derived `w*` and critical spread |
| `s4b` | Arm B: every edit kernel, weights only, at two storage precisions |
| `s4c` | Arm B: WikiText perplexity, distinct-3 and greedy harmful-refusal screens |
| `s3` | Arm A: real public recipe-diverse checkpoints from the Hub |
| `s5` | fixed-threshold confusion by class, leave-one-recipe-class-out, leave-one-uploader-out, the uniformity scatter, the Gaussian sweep, the sub-unit closed form, the E_1 head-to-head, prediction scoring |
| `s6` | `method_out.json` |

### Two arms, one independent variable

**Arm B** holds the host (`Qwen/Qwen3-1.7B`) and the refusal direction `r` fixed
— `r` is taken *verbatim* from the archived `root_recipe.json`, so the only
thing that varies across ~30 checkpoints is the **kernel**: uniform at
w ∈ {0.5, 0.7, 0.85, 1.0}; a Gaussian depth kernel at spread ∈ {0.5 … 64, ∞};
a middle-50% layer band; ORBA's Householder reflection at λ ∈ {0.25, 0.5, 1.0};
MPOA's norm-preserving projection; rank-k at k ∈ {2, 4, 8}; and Heretic's
per-component kernel with a float direction index of 17.89 and per-component
weights 0.84 / 1.15.

**Arm A** scores real public sub-4.2B checkpoints, selected without ever looking
at the repo name: eligibility first, then the recipe class **re-derived from the
full model card fetched at the pinned revision** (the dependency manifest only
stores a ~250-character evidence window, which is usually too short to name the
kernel), then round-robin over classes, smallest-first.

### Baselines

1. **E_1**, the published *parent-requiring* weight signal:
   `E_1 = mean_m sigma_1^2(dW) / sum_i sigma_i^2(dW)` with `dW = W_parent - W_child`,
   at three depth bands, for every row whose parent is also in the plan.
2. **The repo-name regex.** The dependency manifest measures that a plain regex
   on the repo id alone already flags 50.5% (259/513) of self-declared edited
   checkpoints. That, not chance, is the operational baseline.
3. **The archived panel-fitted τ** itself — what the previous iteration would
   predict knowing nothing about the recipe.

## Three things worth knowing before reading the numbers

**1. bf16 storage is load-bearing.** The archived recipe writes
`(W - outer(r, r@W)).to(bf16)`, and every Hub checkpoint is stored the same way.
After a *complete* projection the energy surviving along `r` is therefore not
zero but bf16 rounding noise — which is exactly why the archived root lands at
W05 = −4.59 and not at the −30 floor. Arm B casts back to bf16 for that reason,
and re-runs the quantitative families at float32 as a precision control.

**2. The plan's closed form is a leading-order form.** The residual energy along
`r` really does scale as `(1-w)^2`, but the statistic normalises by the
**edited** matrix's own Frobenius norm, which shrinks by exactly the removed
energy. The exact prediction is

```
e_m(w) = (1-w)^2 a_m d / (F_m - (1 - (1-w)^2) a_m),   a_m = ||r^T W_m||^2
```

Both are stamped and both are scored; they differ by ~1/d.

**3. "Uniform" is not the predicate; "uniformly complete and rank-reducing" is.**
Two Arm B kernels are uniform in depth yet predicted to be *missed*, and are
labelled apart so they cannot spuriously trip the falsifier:
`UNIFORM_BUT_ORTHOGONAL` (ORBA — a Householder removes no rank, so the Gram
spectrum is invariant by construction) and `UNIFORM_BUT_INCOMPLETE`
(w < 1 leaves `(1-w)^2` of the energy in every layer, annihilating nothing
anywhere).

## Falsifiers

Named in `results/predictions.json` before the run, so the artifact can lose:
(i) a uniform recipe is missed, (ii) a depth-weighted recipe is caught,
(iii) ORBA moves W05 by more than 1e-6, (iv) the Gaussian sweep is a smooth ramp
with no threshold. Any of these is the headline, and `P13` reports it as such.

## Files

- `method.py` — the pipeline
- `wstats.py` — the statistic, the uniformity indices, the closed form, E_1
- `kernels.py` — the eight edit kernels
- `armA_select.py` — Arm A eligibility and recipe re-derivation
- `vendored_lib_*.py` — byte-identical copies of the iteration-3 libraries
  (sha256 recorded in `method_out.json`); `lib_*.py` are import shims so the
  vendored files need no patching
- `results/` — one file per stage, plus `layer_profiles.jsonl` (per-layer
  suppressed-energy profile for every checkpoint) and `cards.json`
- `method_out.json` — the deliverable
