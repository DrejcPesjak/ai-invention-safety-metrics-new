# Recompute every number in the paper

Pure re-analysis of the archived iteration-2 trees. **No model weights are loaded, no
forward pass is run, no text is generated.** The only compute that leaves the machine is
LLM re-labelling of already-archived generations, content-addressed into a cache and
hard-capped at $0.90.

## What is here

| file | what it is |
|---|---|
| `eval.py` | entry point: `uv run eval.py` (add `--no-judge` to skip the adjudicator) |
| `analysis.py` | the centrepiece: one seeded, versioned script that recomputes every statistic the paper quotes |
| `lib_contract.py` | the analysis contract — seed, B, resampling scheme, singleton rule, tie handling, exclusion rule, NaN policy. Printed before any number and echoed into `numbers.json` |
| `lib_stats.py` | estimators: rank-average Spearman, Mann-Whitney AUROC with 0.5 tie credit, Wilson interval, Cohen's kappa, Spearman-Brown |
| `lib_judge.py` | the independent adjudicator over archived generations (cached, ledgered, hard-stopped) |
| `warm_judge_cache.py` | fills the adjudicator cache on its own, so `analysis.py` can be iterated for free |
| `numbers.json` | **the machine-readable numerals the paper generates from, never transcribes** |
| `eval_out.json` / `full_eval_out.json` / `mini_eval_out.json` / `preview_eval_out.json` | schema-valid (`exp_eval_sol_out`) evaluation output, all four validated |
| `results/tables.txt` | human-readable dump of the same tables |
| `results/reproducibility.json` | byte-identity check across two consecutive runs |
| `verify_reproducible.py` | runs `analysis.py` a second time with the cache warm and asserts `numbers.json` is unchanged |
| `cache/judge_cache.jsonl` | content-addressed judge labels; makes a rerun cost $0 |
| `cost_ledger.jsonl` | per-call LLM cost |

## Reproduce

```bash
./run_all.sh          # ~10 min on 48 cores; $0 if cache/judge_cache.jsonl is present
```

A smoke run (seconds, no API calls):

```bash
AII_B_BOOT=200 AII_B_POWER=200 AII_N_POWER_SIMS=20 \
AII_N_POWER_SIMS_NSWEEP=20 AII_SKIP_JUDGE=1 .venv/bin/python analysis.py
```

Whatever `B` a run actually used is echoed into `numbers.json`'s contract block, so a
shrunken run can never be mistaken for a full one.

## The six arms

1. **POWER** — minimum detectable `|drho|` at 80% power for the actual paired cluster
   bootstrap, the achieved CI half-widths, and the `n_lineage` needed at delta 0.10 / 0.20 / 0.30.
   Converts "the falsifier fired" into a bounded claim.
2. **COMPARATOR** — paired differences against the *pre-specified* `B01_logit_gap_harmful`
   as well as the post-hoc best-of-11 `B09`, plus a selection-corrected variant that
   re-argmaxes the black-box winner *inside every resample* and prices the optimism.
3. **RELIABILITY AND ATTENUATION** — per-item labels were never persisted, so they are
   re-derived: the frozen prompt folds are rebuilt from `lib_data.py`, paired to the
   archived responses, and re-adjudicated with rubric B verbatim by an independent model.
   Split-half, Wilson intervals, kappa, and attenuation-corrected correlations.
4. **DEPTH AND CENSORING** — marked **PARTIAL**, with the reason stated in `numbers.json`:
   only two depth-varying quantities are archived per checkpoint. Nothing was fabricated
   for the rest.
5. **PRE-REGISTRATION FIDELITY** — every "pre-registered" / "SHA-stamped" claim mapped to
   the artifact, file and line that actually records it, with corrected wording supplied
   for every non-SUPPORTED row.
6. **REPORTING-HONESTY REGENERATION** — the class-wise table for *every* member class (not
   just the abliterated column), the boundary facts, the W03 count, and the positive-control
   disambiguation, each with its provenance.

## The headline finding of the audit

Four values the draft presents as **correlations** of a white-box metric with the ground
truth — `A01 -0.161 [-0.501, +0.208]`, `A02 +0.036 [-0.225, +0.303]`,
`W01 -0.373 [-0.731, -0.039]`, `alpha_50 -0.453` — are in fact **paired differences**
`|rho_X| - |rho_B09|`, computed on a **26-member subset defined by the `renderer` field**,
not the 28-member `member_class != 'base'` subset the draft says it uses.

Read as correlations they are wrong by up to 0.67 and one has the wrong sign. Read as
paired differences on that subset, three of the four reproduce to four decimals. The
arithmetic was never wrong; the labels were, and no artifact recorded either the quantity
or the subset. `numbers.json` records both, and `draft_convention_rerun` re-runs the whole
falsifier on the draft's own subset so the conclusion does not depend on which subset the
re-analyst prefers. The verdict is unchanged on both.

Two further corrections fall out of the same audit: `B09` is **not** the best black-box
metric at either aggregation unit (it is the in-resample argmax in ~11-14% of cluster
resamples), and `W05`'s "AUROC 1.000" is the *oriented* value — the raw AUROC is 0.000
because abliterated members sit at the low end, and the other four scar metrics reach
0.986 / 0.950, not 1.000.

## Reading `numbers.json`

Top-level keys: `contract`, `input_integrity`, `panel`, `classwise_distribution`,
`classwise_overlaps`, `weights_auroc`, `weights_auroc_generalisation`, `W05_boundary`,
`behaviour_arm_counts`, `correlations`, `paired_differences`,
`selection_corrected_comparator`, `power`, `reliability`, `attenuation`, `depth`,
`preregistration_fidelity`, `provenance`, `disagreements`, `headline`, `partial_arms`,
`runtime`.

Finding disagreements with the quoted values is part of the deliverable, not an
embarrassment: `disagreements.rows` classifies each as `MATCH`, `TRANSCRIPTION_ERROR`,
`STALE_INPUT` or `RECOMPUTE_DIFFERS_METHOD`, and carries the source string for the quoted
value so a reader can check the provenance of both sides.
