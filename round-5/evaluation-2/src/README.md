# Does a second judge change the safety verdicts?

Validation of the single LLM judge that the whole behavioural axis of the abliteration-detector
paper rests on: `meta-llama/llama-3.3-70b-instruct` under rubric B, whose only reported
validation was agreement with a substring screen at mean kappa 0.149 and rate-level
Pearson *r* 0.822.

Total OpenRouter spend **$0.0666** of a $1.50 cap. `verify_eval.py`: **56/56**.
`eval_out.json` validates against `exp_eval_sol_out`.

---

## The problem this artifact had to solve first

The archive (`art_VLI4IOs9Xy9P`) never stored the generation text. `lib_behave.score_set`
persisted per-item **binary** labels keyed by prompt uid, one 400-character sample per cell,
and a `judge_cache.json` that maps `sha256(JUDGE_MODEL ‖ RUBRIC_ID ‖ prompt ‖ response[:1500])`
to a label — hashes only. "Read the archived text and re-judge it" is therefore impossible
as literally stated.

It is, however, **recoverable, and the recovery is self-verifying**. Generation is greedy
argmax at temperature 0; the edited checkpoints rebuild from `archive/root_recipe.json` and
`results/roots.json`; so a regenerated `(prompt, response)` pair that is byte-identical to the
archived one **hits the archived cache key**. Cache-hit rate is a *proof of text identity*,
not bookkeeping — without it every agreement number would confound scorer disagreement with
regeneration drift.

`regen.py` re-created **3,880 generations across all 61 archived behavioural cells** — roots A
(uniform abliteration of Qwen3-1.7B), B (depth-weighted Gaussian, direction pinned to A's),
C (the real gated `meta-llama/Llama-3.2-1B-Instruct`, no substitution), their parents, and the
full merge / add-back / quantisation ladder. **60.6 % hit the archived key.**

The residual is **cross-device bf16 nondeterminism**, and that was established rather than
assumed: the archive ran on an RTX 2000 Ada, this run on an RTX 4090, and `probe_batch.json`
shows the hit rate is 0.55–0.65 across batch sizes 8/16/32/40, so batch composition is not the
cause. Batch 16 — archive-identical — was kept. Notably the Llama host recovers at 0.93–0.97
while the Qwen host sits near 0.55. **This is a reproducibility limit on the archived
behavioural numbers themselves, and it is reported rather than papered over.**

Only proven-identical items entered the analysis frame, so all three scorers read exactly the
same characters. The selection this induces is measured, not waved away: every cell reports the
archived label rate on hit vs missed items (`selection_check`).

## The three scoring arms

| arm | model | rubric | what it isolates | cost |
|---|---|---|---|---|
| **J1** | `meta-llama/llama-3.3-70b-instruct` | B (verbatim) | the archived opinion — recovered free from the cache | $0 |
| **J2** | `google/gemini-2.5-flash` | B (byte-identical) | the **model** effect | $0.039 |
| **J3** | `meta-llama/llama-3.3-70b-instruct` | C (re-worded) | the **rubric** effect | $0.028 |
| screen | `lib_data.is_refusal`, imported unmodified | — | the archived substring baseline | $0 |

J2 is asserted (not merely commented) to contain neither `qwen`, `llama` nor `guard`.
Rubric C is a 3-step decision list over the identical distinction; its one wording adjustment
is disclosed in `scoring_arms.json → rubric_c_parsing_disclosure`. Rubric B was never edited.

180 items were drawn by a seeded, stratified, pre-registered scheme (`sample_manifest.json`),
then — because 9–10 items per stage cannot resolve a rate difference, as the *reproduction*
arm's own failure to resolve P2 showed — the whole 620-item load-bearing frame was scored as a
**census**. Both are reported: every row carries `in_preregistered_sample`, and
`agreement.json → preregistered_subset` holds the pre-registered analysis separately.

## What it found

**The archived number reproduces.** Root B reads **0.278** under J1 on the recovered items
against the archived **0.270** — the recovery pipeline is sound.

**The judge model, not the rubric, is what moves it.**

| axis varied | pooled shift in refusal rate |
|---|---|
| judge **model** (J1 → J2) | **0.269** |
| rubric **wording** (J1 → J3) | 0.126 |
| PARTIAL **collapse rule** | 0.034 |

Root B's headline projects to **0.770 [0.680, 0.859]** under Gemini and **0.193 [0.142, 0.245]**
under the re-worded rubric, against an archived 0.270 [0.196, 0.360]. The *number* is
scorer-dependent — pre-registered outcome **F2**.

**The claim is not.** Root B sits below its parent under all three scorers and all three
separate it from its parent. `P1` verdict `SURVIVES_WEAKENED`, with the number and the
decoupling reported separately rather than blurred.

**The blind anchor breaks the tie, and it favours the archive.** On 48 disagreement-enriched
items adjudicated blind (file mtimes and sha256s asserted, not promised):

| scorer | raw accuracy | balanced | kappa vs adjudicator |
|---|---|---|---|
| **J1 (archived)** | **0.771** | 0.745 | **0.643** |
| J3 (rubric C) | 0.745 | 0.761 | 0.622 |
| J2 (Gemini) | 0.521 | 0.536 | 0.291 |
| substring screen | 0.500 | 0.422 | 0.155 |

The disagreement is concentrated where J1 says COMPLIANCE and J2 says REFUSAL (per-class
agreement 0.333), and adjudication sides with J1 there. **The correct limitation for the paper
is therefore not "the archived rate is wrong" but "a second judge chosen without validation
would report a materially different rate."** The adjudicator is an LLM agent, not a human —
every accuracy here *bounds scorer disagreement against a fourth opinion*; it is not truth, and
the paper must not call it ground truth. Self-consistency: 1 flip in 12 re-checked items.

**Verdicts.** P1 `SURVIVES_WEAKENED` · P2 `SURVIVES_WEAKENED` · P3 `SURVIVES`
(the Llama AUROC-argmax false positive refuses at 1.000 = its parent under *every* scorer) ·
P4 `SURVIVES` · P5 `SURVIVES` (9/9 flag-death orderings PRESERVED).

**Report AC1 beside kappa.** J1-vs-J2 three-class: 0.679 raw, kappa 0.361, AC1 0.582, PABAK
0.519. The abliterated stages have near-degenerate marginals — that prevalence paradox is
exactly what put the archive's kappa of 0.149 next to a rate-level *r* of 0.822.

## Layout

```
eval.py               S0 ingest · S2 sample · S3 score · S4 anchor · S5 agree · S6 propagate · S7 ship
regen.py              S1 text recovery by deterministic regeneration + cache-hit identity proof
lib_agree.py          kappa (multi-class), Gwet AC1, PABAK, Newcombe, exact McNemar, Holm
verify_eval.py        56 independent checks; does not import eval.py
probe_batch.py        the batch-size diagnostic behind the drift attribution
vendor/               archived libraries, used unmodified
results/
  recovered.jsonl        3,880 regenerated generations, verbatim, with cache-hit proof
  regen_meta.jsonl       per-cell hit rate, identity check, selection check
  scores.jsonl           620-item census: J1 / J2 / J3 / screen per item
  judge_limitations.json THE deliverable — every number the paper's judge paragraph needs
  disputed_items.jsonl   299 items where scorers disagree, verbatim (a research record)
  propagation.json       P1–P5 with verdict tokens and pasteable sentences
  agreement.json  agreement_by_stage.csv  anchor_*  archive_*  reproducibility.json
figs/                 per-stage rates ×3 scorers · J1-J2 / J1-J3 confusions · P1–P5 forest
```

Reproduce: `.venv/bin/python regen.py` then `.venv/bin/python eval.py`. A second run hits
100 % of `results/rescore_cache.json` and costs **$0**.

## Limitations worth reading before quoting anything

1. The frame is **conditioned on a cache hit**; that is a selection and its size is measured
   per cell, not assumed benign.
2. The anchor adjudicator is an **LLM**, not a human.
3. **P4 varies the collapse rule but not the scorer.** `art_dp7WBo6hhVBX` shipped no judge
   cache and its Arm-B kernels need per-layer and SVD directions that were never persisted, so
   its text is unrecoverable here. What *is* recoverable is its full ordered three-class label
   list, so the "10 effective / 4 detected" claim was re-tested under the alternative PARTIAL
   collapse: 10 → 10, **zero membership flips**.
4. Only the harmful core was re-scored; the XSTest over-refusal rates were not re-judged.
5. J3 measures the rubric effect *conditional on* J1's model.
6. 10 of 620 J3 calls were `UNPARSEABLE` — usually the judge model refusing the judging task
   itself. They are a reported class, logged verbatim in `unparseable_log.jsonl`, never dropped.

Nothing here re-measures W05, E₁ or the ladder flags; they are taken verbatim from the archive.
This artifact varies **only the scorer**.
