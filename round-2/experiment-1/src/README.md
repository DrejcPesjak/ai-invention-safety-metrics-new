# Fifty cheap safety metrics on many models

A frozen 53-declaration battery (50 shipped + 3 declared extras) computed on every
measured checkpoint of the frozen panel, plus a faithful AMS reimplementation with a
Table-I reproduction gate, plus a two-axis behavioural readout that is computed LAST
and is never used to select anything.

## What this artifact does and does not do

It **measures**. It **selects nothing**. No metric is added, dropped, tuned,
re-parameterised or re-ordered on the basis of any behavioural number here. The
discipline is structural:

| file | role |
|---|---|
| `metric_spec.py` | the 53 declarations, sha256-stamped **before** any model was loaded |
| `lib_data.py` | frozen prompt subsets, refusal-token lexicon, panel + run list, held-out lineages |
| `lib_model.py` | loading, renderers, write-matrix resolution, logit lens, batched decode, steering hooks |
| `lib_metrics.py` | the 53 metric implementations + the AMS baseline |
| `method.py` | driver: `--stage tests / calib / panel / behaviour / assemble` |
| `results/battery.jsonl` | the metric table — **contains no behavioural column** |
| `results/behaviour.jsonl` | the two-axis readout, written only after the battery was stamped |
| `method_out.json` | pure join of the above |

## Reproducing

```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r requirements
.venv/bin/python method.py --stage tests      # positive control + plumbing gates
.venv/bin/python method.py --stage calib      # freeze rho* on the reference model
.venv/bin/python method.py --stage panel --deadline-min 168 --per-model-s 660
.venv/bin/python method.py --stage behaviour  # needs OPENROUTER_API_KEY
.venv/bin/python method.py --stage assemble
```

## The three arms

- **weights-only (16 declarations, 0 forward passes).** The new arm. `W01–W05` test for
  abliteration's rank-one write-suppression signature *without the parent model*: build
  `A = sum_l W W^T / ||W||_F^2` over every residual-write matrix, take its minimum
  eigenvector `v_1`, and ask whether `v_1`'s write energy is suppressed in **every**
  layer. `W06–W16` are spectral/norm descriptors.
- **black-box (11).** Logit gaps, refusal mass, first-token entropy, greedy refusal rate,
  length asymmetry. These are the pre-registered **falsifiers**, implemented as strong
  baselines, not strawmen.
- **activation (26, incl. 4 negative controls).** Diff-in-means separation at a
  pre-registered relative depth, logit-lens refusal log-odds `r_t` at prompt and
  generated positions, AMS, `alpha_50`, and the declared-to-fail EWS controls.

`A02`, `W15` and `A26` are computed and emitted but flagged `is_in_fifty=False`, so the
pre-declared count is exactly 50 and nothing measured is thrown away.

## Gates that ran

1. **Abliteration positive control** (`results/diagnostics.json`) — a rank-one edit is
   injected into every write matrix of Qwen3-0.6B and must be recovered. It is, at
   `|cos(v_1, r)| = 1.000`, `W02 = 1.00`, `W01` 0.62 → 4.82. A **band-limited** variant
   (middle third of layers only) is also reported: it is **not** recovered, which
   calibrates the arm's blind spot honestly.
2. **Hook direction** — a forward PRE-hook at layer *l* moves the layer-*l* readout; a
   post hook does not.
3. **Padded-batch logits** — plus an equal-length control showing the residual
   discrepancy is bf16 batched-GEMM numerics, not padding. (Position ids are derived
   from the attention mask; without that fix the padded batch is genuinely misaligned.)
4. **Token-id validity** — the lexicon is re-resolved against every checkpoint's own
   tokenizer at runtime, with the leading-space variant chosen by round-trip.
5. **AMS reproduction gate** — our sigma against the three AMS Table I anchors, reported
   as a gap and an ordering. The implementation was **not** tuned to close the gap.

## Known limitations, stated rather than hidden

- Published abliterations are frequently *not* exact rank-one edits and some ablate only
  a layer band; `W01–W05` are graded numbers, never a binary detector. The band-limited
  positive control shows exactly where they go blind.
- The AMS 3×16 contrastive pairs are **our** construction from the frozen folds; the
  paper's exact pairs are not recoverable. The reproduction gate is what measures that.
- `rho*` (the pre-registered selected relative depth) came out deeper than iteration 1's
  0.25 because the held-out AUROC profile saturates; the tie-break and both candidate
  values are recorded in `results/calibration.json`. `alpha_50` is ceiling-censored on
  most members at that depth, and the censoring count is reported, not hidden.

## Headline numbers (frozen; this artifact does no selection)

| | |
|---|---|
| checkpoints / lineages / architecture families | **44 / 23 / 7** (floor 20/12/6 met) |
| abliterated or behaviourally-uncensored members | 12 (8 abliterated) |
| standalone members (no sibling in the panel) | 9 |
| metric rows | 2,332 = 44 × 53 |
| metrics whose MEASURED median exceeded 60 s | **0** |
| judge spend | $0.19 (both rubrics, cap $1.50) |

**Parent-free abliteration signature (`W01`, log10 median-λ / min-λ), by declared class:**

| class | n | median | min | max |
|---|---|---|---|---|
| abliterated | 8 | **4.26** | 1.44 | 4.82 |
| base | 16 | 0.58 | 0.34 | 1.99 |
| instruct | 15 | 0.47 | 0.34 | 0.68 |
| behavioural-uncensored | 4 | 0.46 | 0.20 | 0.68 |
| safety-RL (Qwen3-4B-SafeRL) | 1 | 0.47 | — | — |

`W04` (isolation of the outlier eigenvalue) separates even more cleanly: abliterated
median 3.68 (min 0.85) against a maximum of 1.62 over all 36 non-abliterated members.
Behaviourally-uncensored members look like ordinary instruct models here — which is the
point: the signature reads the *edit*, not the *behaviour*.

**AMS reproduction gate:** ours 4.40 / 4.37 / 3.09 against Table I's 8.37 / 4.80 / 4.55.
Spearman ordering **rho = 1.00**, with a systematic scale offset. Reported, not tuned.

**Null rates:** `A22_alpha_50` 37/44 (ceiling-censored at the pre-registered depth),
`A18_decision_depth` 22/44 (the layer-wise refusal margin never crosses 0),
`W14`/`W15` 1/44 (one architecture has no parametric norm gain). Everything else 0/44.
