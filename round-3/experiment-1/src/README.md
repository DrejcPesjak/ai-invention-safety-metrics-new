# How far does the weight scar reach?

Iteration 2 reported a **parent-free** abliteration detector: five statistics
(W01–W05) read off a checkpoint's residual-write matrices, no prompts, no
forward passes, no parent model — AUROC 1.000 on an 8-positive panel. This
artifact asks the only question that matters next: **does it generalise?**

Four things were run. All three arms plus a blocking reproduction gate.

---

## 1. GATE — does the published definition reproduce the archived numbers?

`wstats.py` is an **independent reimplementation** written from the published
formulae *before* `lib_metrics.py` was read, so agreement is a reproduction and
not a copy. Ten members (5 abliterated, 5 not) were re-downloaded at their
archived revisions.

**PASS.** `max|ΔW05| = 9.9e-06`, ordering preserved, Spearman 1.0000.

Three attributable divergences were found and are reported rather than smoothed:

| statistic | behaviour | cause |
|---|---|---|
| W05 | reproduces to 1e-5 | — |
| W01 | reproduces to 1e-4 on non-abliterated members, but drifts up to **0.048 on abliterated ones** | `λ_min` sits near the float noise floor exactly where the scar is; iteration 2 accumulated the Gram in float32, this artifact in float64. Not a load-dtype effect — the float32-load column is identical. |
| W03 | differs systematically by **+0.015 … +0.034** | a **definitional** difference: the published formula takes the 5th percentile of the per-direction *mean* energy; the iteration-2 code pools all (direction × matrix) energies first. Two different statistics. |

Positive controls reproduce: injected global rank-one edit gives
`|cos(v1, r)| = 1.000000`, `W02 = 1.00`, `W01 0.624 → 4.869`; the band-limited
middle-third edit gives `W02 = 0.0`.

---

## 2. ARM 1 — recipe scope. **The detector is bounded to one recipe *and* two uploaders.**

### The real-checkpoint result

The Hub search (7 queries, 70 candidates verified from card evidence, quantised
repos excluded) established a fact that forced the pre-registered fallback:
**mechanically different recipes exist — norm-preserving, multi-direction,
biprojected — but every one of them is ≥ 14.9B**, far above the 4.2B ceiling. At
≤4.2B, every abliteration checkpoint found resolves to the same all-layer global
diff-in-means recipe.

So four real, published, ≤4.2B abliterated/decensored checkpoints from **four
uploaders the detector had never seen** were measured instead:

| checkpoint | W05 | detected? |
|---|---|---|
| `mlabonne/Qwen3-0.6B-abliterated` | −0.964 | ✗ |
| `MagicalAlchemist/Qwen3-1.7B-Magic_decensored` | −1.010 | ✗ |
| `prithivMLmods/VibeThinker-3B-heretic_decensored` | −0.990 | ✗ |
| `BennyDaBall/Qwen3-4b-Z-Image-Turbo-AbliteratedV1` | −2.161 | ✗ |
| *(archived 8, huihui-ai + Goekdeniz-Guelmez)* | −2.74 … −4.82 | ✓ 8/8 |

**W05 AUROC: 1.000 on the two uploaders it was characterised on, 0.382 on the
four it was not — 0/4 caught at the fitted threshold.**

This is **not** an unedited-re-upload artefact. `realcheck.py` verifies each
against its declared parent: all three with a resolvable parent are genuine
near-rank-one edits (E_1 = 0.995, 0.995, 0.997; relative Frobenius change
2.5–3.0%; 0% bit-identical matrices). The parent-*requiring* incumbent sees them
all. The parent-*free* detector sees none.

### The synthetic recipe ablation

Twelve in-house variants on two architectures, each with a fluency check and a
greedy harmful-refusal rate so "the edit worked" and "the edit is visible" stay
separable. No variant was degenerate.

- **normpres, rank-k (k=2,4,8): AUROC 1.000** — detected.
- **per-head (top 25% of heads): AUROC 0.556** — missed.
- **layer-fraction sweep: f\* = 1.00 on both hosts.** Only the *fully global*
  edit is detectable.

The sharpest finding is in that sweep. On Qwen3-1.7B, a projection confined to
the middle 50% of layers drives the harmful-refusal rate **0.45 → 0.00 — exactly
as effective as the full-stack edit** — while W05 moves from −1.0098 to
−1.0088, i.e. **indistinguishable from the unedited model**. E_1, which has the
parent, sees it at 0.995.

> **Scope sentence (generated from the numbers):** W05 detects the all-layer
> global diff-in-means recipe from the uploaders it was calibrated on, plus
> norm-preserving and rank-k variants of it (AUROC ≥ 0.95); it misses the same
> recipe from new uploaders (0.382) and per-head surgery (0.556). Its blind spot
> is any edit confined to a proper subset of layers, and inside that blind spot
> an edit can be fully effective behaviourally.

---

## 3. ARM 2 — head-to-head against E_1, the parent-requiring incumbent

`E_1 = mean_m σ₁²(ΔW)/Σσᵢ²(ΔW)` over mid-stack (0.25L–0.75L) write matrices.

| subset | n | E_1 AUROC | W05 AUROC | paired difference |
|---|---|---|---|---|
| pre-declared 12 pairs (2 uploaders) | 12 | **1.000** | **1.000** | +0.000 [0.000, 0.000] |
| + 3 new-uploader pairs | 15 | **1.000** | **0.833** | −0.167 [−0.444, 0.000] |

On the recipes and uploaders it was tuned on, parent-free costs nothing. Adding
three new-uploader pairs makes E_1 hold at 1.000 while W05 falls. The interval
reaches zero at its boundary, so at n=15 this is **underpowered as an interval
claim**; descriptively it is unambiguous (E_1 3/3, W05 0/3).

The two are also complementary on the synthetic variants: E_1 degrades on
multi-direction edits (0.17–0.67 for k=8…2) where W05 is perfect, and E_1 holds
at 0.995 on the band-limited edits that W05 cannot see at all.

**The parent-free constraint does not cost accuracy on the recipes it was tuned
on; it costs generalisation.**

---

## 4. ARM 3 — is the falsifier a depth artefact? **No.**

Iteration 2's activation arm lost to a black-box baseline at one pre-declared
depth (ρ\* = 0.679) chosen from a *saturated* AUROC plateau. All depth-sensitive
metrics were recomputed at three depths — the bare AUROC argmax (0.143, read
from the archived calibration), 0.50, and ρ\* — over 26 chat-rendered members:
**1,014 rows in `results/long_table_depth.jsonl`**.

**Verdict: INVARIANT.** The black-box baseline wins at all three depths.

This required the *right* test. Four activation metrics have a larger point
estimate than a baseline at ρ\* — `A19_refusal_axis_unembed_cosine` reaches
ρ = +0.770 against B09's +0.766. Comparing point estimates would have called
that a win. The **paired** lineage-bootstrap difference gives +0.0045
[−0.225, +0.260]: nothing. All four collapse the same way.

A separate, decision-relevant finding: **α_50's ceiling censoring is strongly
depth-dependent** — 25/26 censored at the bare argmax, **15/26 at 0.50**, 19/26
at the pre-declared ρ\*. The pre-declared depth is *not* the one that yields the
most usable values. Depth selection for the AUROC plateau and depth selection
for steering headroom are different problems, and iteration 2 conflated them.

---

## Controls

- **Synthetic-tensor unit tests** (`wstats.py --selftest`), which found a
  *stronger* blind spot than expected: with 4 of 12 matrices edited, `v1` is no
  longer the injected direction at all (W02 = 0), because the Gram pools every
  matrix. The blind spot is a threshold, not a ramp.
- **Random-direction control on real models.** W05 is a minimum over many
  matrices, so a low value could be an artefact of minimising over a large set.
  It is not: true `v1` gives −2.742 on the abliterated member where five random
  unit directions give −0.085 (min −0.113); on the hardest negative (OLMo-1B)
  true −2.665 vs random −0.033.
- **Revision stability.** Both probed repos' `main` still resolves to the
  archived commit, so the deltas are exactly 0.0 — the control passes, but it is
  weaker than intended because there was no drift to detect.
- **Permutation nulls** alongside every bootstrap CI, with the exact null floor
  `1/C(n,k)` reported (an AUROC of 1.000 with few positives has a non-trivial
  exact null).
- **Assertion block.** `analysis.py` prints its full resampling contract and
  `assemble.py` recomputes every quoted number from the raw files; a mismatch
  blocks assembly. It fired for real during development when Arm 3 was still
  writing.

---

## Verdicts

```
GATE               PASS
SCAR_SCOPE         RECIPE_CLASS_BOUNDED
E1_TRADE           PARENT_FREE_COSTS_0.167_UNDERPOWERED
DEPTH_INVARIANCE   INVARIANT
```

## Reproducing

```bash
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml
uv run method.py --stage smoke      # synthetic unit tests, no downloads
uv run method.py --stage gate       # 10-member reproduction gate
uv run method.py --stage control    # injected rank-one + band-limited controls
uv run method.py --stage arm1 --tier2
uv run method.py --stage arm1c      # Hub search + real checkpoints only
uv run method.py --stage arm2
uv run method.py --stage arm3
uv run realcheck.py && uv run extra_controls.py
uv run method.py --stage assemble   # writes method_out.json, asserts every number
```

Cost: **$0.00** in LLM API spend (no judge calls, no generation scoring).
Wall clock ≈ 1 h on one RTX 4090. Snapshots are fetched sequentially and deleted
after measurement.

### Files

| file | role |
|---|---|
| `wstats.py` | independent W01–W05 reimplementation + synthetic unit tests |
| `e1.py` | E_1, the parent-requiring incumbent baseline |
| `edits.py` | synthetic abliteration recipes (projection, norm-preserving, rank-k, per-head, layer-band) |
| `arm1.py` / `arm2.py` / `arm3.py` | the three arms |
| `realcheck.py` | miss-vs-re-upload disambiguation for real checkpoints |
| `extra_controls.py` | revision stability + random-direction control |
| `analysis.py` | every AUROC / Spearman / bootstrap CI, with the contract printed |
| `assemble.py` | statistics, verdicts, `method_out.json`, assertion block |
| `vendored_lib_*.py` | **byte-identical** copies of the iteration-2 stack (sha256 recorded); `lib_*.py` are pure alias shims so no patch was needed |
| `results/long_table_depth.jsonl` | the Arm 3 deliverable: 1,014 (member, metric, depth) rows |
