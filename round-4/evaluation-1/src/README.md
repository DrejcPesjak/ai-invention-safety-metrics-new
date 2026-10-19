# Recheck every number in the draft

Pure re-analysis over the archived iteration-2 and iteration-3 trees.

| | |
|---|---|
| OpenRouter / LLM spend | **$0.00** (no LLM client is imported anywhere in this artifact) |
| Model weights loaded | 0 |
| Forward passes | 0 |
| Generations | 0 |
| HuggingFace Hub fetches | 0 |
| Seed | `20260814` |
| Bootstrap resamples | 10000 |
| Wall clock | 21.37 s |
| Determinism check | BYTE_IDENTICAL_APART_FROM_TIMING |

## Assertion table

110 claim_ids covered across W1-W5 plus the cross-check gates.

| verdict | n |
|---|---|
| MATCH | 105 |
| MISMATCH | 5 |
| UNAVAILABLE | 0 |

A MISMATCH does not abort the run - it is the product. Every disagreement is in
`results/disagreements.json`, annotated with a `finding_class`:

- `DRAFT_ERROR_COUNT` x2
- `DRAFT_ERROR_COUNT_ADJUDICATED` x1
- `DRAFT_ERROR_DENOMINATOR` x1
- `SUBSET_DEFECT_CONFIRMED` x1

## Cross-check gates

- `A2/verify.py` re-run against the archived `results/*.jsonl`:
  **17/17 cross-checks pass**
- `A1` wstats reimplementation vs the archive: max |dW05| =
  `9.91e-06`
  (gate.json full precision `9.908662263136137e-06`),
  W05 ordering preserved =
  `True`.

## Outputs

- `eval_out.json` - blocks `recipe_relabel`, `ladder_intervals`, `e1_bands`, `cost_table`,
  `fidelity`, `assertions`, `provenance`, `manifest` (under `metadata.blocks`)
- `results/arm1_real_corrected.jsonl` - one row per arm-1 new-uploader member, OLD and NEW labels
  side by side with the verbatim evidence span
- `results/disagreements.json` - every MISMATCH / UNAVAILABLE
- `results/draft_edit_list.json` - the numbered draft edit list
- `results/determinism.json` - the two-run byte-identity check

## Reproduce

```bash
uv run eval.py            # writes eval_out.json and results/*
uv run determinism.py     # runs the pipeline twice and diffs the bytes
```
