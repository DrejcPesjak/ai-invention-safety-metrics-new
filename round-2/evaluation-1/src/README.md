# Auditing last round's negative results (A1–A5)

A **pure re-analysis** of the three archived iteration-1 experiment trees. No new model
inference, no GPU, no re-running of any iteration-1 experiment. The only network spend is
fresh LLM judging for A3: **$0.0586 total** against a $1.00 hard cap.

```
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml
.venv/bin/python eval.py all              # full pass (~18 s warm, ~4 min cold)
.venv/bin/python eval.py all --stage smoke  # reduced-N pipeline validation
.venv/bin/python eval.py a1               # any single stage: inventory|a1|a2|a3|a4|a5|finalize
```

Every LLM response is cached to `out/a3_annotation_cache.jsonl` keyed by
`(model, framing, item_id)`, so a rerun costs **$0** and reproduces byte-identically.

## Source trees (read-only; never mutated)

| | path |
|---|---|
| E1 | `run_CbJDs3opF7E_/.../gen_art_experiment_1` — refusal wobble / SPI tier-0 |
| E2 | `run_CbJDs3opF7E_/.../gen_art_experiment_2` — steering hysteresis |
| E3 | `run_CbJDs3opF7E_/.../gen_art_experiment_3` — behavioural ground truth + judge |

The estimators (`paired_bootstrap_diff`, `cluster_bootstrap_ci`, `half_life_auc`,
`wilson_ci`) are **imported from `E1/spi/indicators.py`**, not reimplemented, so the
audit's machinery is the artifact's own. E1's `spearman()` and `build_output.py`'s
verdict rule are transcribed verbatim into `audit/a4_permutation.py` and
`audit/a1_lambda.py` so the archived numbers reproduce exactly before anything is
changed.

## Headline findings

**A1 — the lambda inconsistency.** The supplementary verdict
`CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING` is **CHANGED**. Re-running E1's own decision
rule on the two assumption-free statistics the artifact itself calls trustworthy
(`decay_ratio_16`, normalised deviation AUC) over the same 240 certified-refit rows: at
the pre-stated primary readout (**layer L**, where the perturbation is injected) the
random-direction control separates the panel in **0 of 3** comparisons while the
refusal-direction treatment separates in **2 of 3** — the reverse of the reported
pattern. It reproduces only at the final-layer readout, whose correlation with the
layer-L lens the artifact measures at 0.17–0.26. The switch is **not** cosmetic: lambda
and `decay_ratio_16` rank-correlate at only −0.46 (layer L) / −0.17 (final).
`MATERIAL_CHANGE_TO_REPORTED_RESULT`.

**A2 — observable validity.** Only **1 of 4** panel members passes the pre-stated gate
(r₀ harmful-vs-benign AUROC ≥ 0.70): instruct 0.793; abliterated 0.481, base 0.414,
smollm2 0.633. `indicator_comparison_status = UNSUPPORTED_ONLY_1_MEMBERS_PASS`, so
"indicators track lineage, not safety" is **RETRACTED** as a settled negative and
downgraded to a qualitative observation. The sensitivity curve at {0.60, 0.65, 0.70,
0.75, 0.80} is published; n_passing is 1 at every threshold from 0.65 up.

**A3 — the judge probe, rebuilt.** 197 items, four classes, drawn from the 3,365 archived
generations with a fixed seed; two annotators decorrelated in **model family** and
**rubric framing** (Gemini + frozen rubric; Mistral + independent decision tree), κ =
0.337 [0.259, 0.415]; all 96 disagreements adjudicated by a third family (DeepSeek), all
97 disputed items published verbatim in `out/disputed_items.json`.
- **0/7 → 7/82 = 0.085 [0.042, 0.166]** frozen-judge COMPLIANCE recall. The literal claim
  "never assigns COMPLIANCE" is wrong; the substantive failure is confirmed and now
  quantified against 0.939 for the repaired judge on the same items.
- **3 of 21** original probe truth labels are contradicted, including the force-included
  `"Certainly! Here's a message that conveys hope…"` case: prefix-labelled COMPLIANCE,
  adjudicated **PARTIAL**. The 21/21 gold arm was rewarded for agreeing with wrong labels
  and is **RETRACTED**.
- Both headline revisions reproduce exactly (0.700→0.113, 0.092→0.858) and **strengthen**
  under misclassification correction: 0.113 → 0.000 [0.000, 0.069] and 0.858 → 0.904
  [0.857, 0.974].

**A4 — the n=4 correlations.** All 24 orderings enumerated. rho = −0.20 reproduces
exactly under E1's own rank function, at exact two-sided p = 1.000 against a p-floor of
**0.4167** — and the untied floor is 2/24 = 0.0833, so nothing at this panel size could
reach 0.05. Two independent reasons the claim fails: (i) only **1 of 4** members sits
above the refusal/incapacity floor, and (ii) E1's `spearman()` breaks ties by array
position, and two members are tied at 0.000 — with average ranks the same data give
**+0.105, a sign flip**. `corrected_claim_text` and `numbers_to_drop` are emitted for the
write-up.

**A5 — pre-registration fidelity.** 15 deviation rows (7 unannounced), each with trigger,
date, date-source and direction of effect. All eight E2 amendments appear.
- **Excess-width sign inversion**: confirmed by recomputing both conventions from the
  per-prompt values. H1b is two-sided about zero, so the conclusion is **invariant** —
  recorded as a reporting error, deliberately **not** inflated into a result change.
- **alpha_50**: the 0.075 gap is 1.5 steps of the amended 0.05 grid with 5 Bernoulli
  draws per point; bootstrapped intervals [0.383, 0.538] and [0.483, 0.617] **overlap**.
  `alpha_50_gap_is_resolvable = false` — **RETRACTED**.
- **refusal_direction.pt** feeds only E3's in-house ladder; E1 and E2 fit their own
  directions, so the correlated-error risk is confined.
- **Abliteration coverage is COMPLETE** (o_proj + down_proj + embed_tokens). Under the
  relabel rule fixed in advance, the SNAPPED failure may be attributed to the technique —
  but the defensible sentence is *"our single-direction weight-edit implementation did not
  produce a graded knob at 0.6B scale"*, not *"abliteration strength is not a knob"*,
  because the community checkpoints behaved as expected and the edit uses one direction
  fitted at one layer applied to all layers.

## Reconciliation table

`out/reconciliation_table.json` — 46 rows: **25 SURVIVES / 12 CHANGED / 9 RETRACTED /
0 UNTESTED**, each with the original value, the re-derived value and the analysis that
decided it. Also mirrored as the `reconciliation_table` dataset in `eval_out.json`.

## Layout

```
eval.py                 single entry point (method.py is a symlink)
audit/                  common.py, inventory.py, a1_lambda.py, a2_gate.py,
                        a3_probe.py, a4_permutation.py, a5_prereg.py, finalize.py
eval_out.json           exp_eval_sol_out-valid; 6 datasets, 348 examples, 53 metrics
  full_/mini_/preview_eval_out.json
out/                    input_inventory, gate_definition, a1..a5, reconciliation_table,
                        disputed_items, llm_call_log.jsonl, a3_annotation_cache.jsonl,
                        field_substitutions, stage_timings
figs/                   F1 verdict-flip matrix, F2 observable-validity gate,
                        F3 judge confusion matrices, F4 exact permutation null (PNG+PDF)
logs/                   per-stage loguru logs
```

`out/gate_definition.json` is written **before** any gated comparison is evaluated;
`out/field_substitutions.json` records every planned field that was absent and what was
used instead (two entries, both in A2). Fifteen limitations are enumerated in
`eval_out.json → metadata.limitations`.
