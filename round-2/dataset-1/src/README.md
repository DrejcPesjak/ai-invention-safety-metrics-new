# Published safety scores and a frozen split (iteration 2)

External ground truth to replace our own judge as the correlation target for the
50-metric screen, plus a seeded dev/held-out split over weight lineages written
**before** any metric exists, plus two machine-readable rules iteration 3 must apply.

Deliverable: `full_data_out.json` (13,311 rows, 22 MB — under the 100 MB limit, so it
ships whole and unsplit) + `mini_data_out.json` (3 examples per block) +
`preview_data_out.json` (3 truncated examples per block, rebuilt by
`src/make_preview.py` so it covers all 20 blocks rather than the first 3 the format
script would keep), built by `uv run data.py`. `pyproject.toml` pins all 40 packages
to the exact versions installed in `.venv`. Schema-valid against
`exp_sel_data_out`; the per-row-kind payload schema is `schema_row_kinds.json`,
checked by `src/validate_rows.py`.

The file holds **two families of blocks**:

* **1,509 artifact rows** (10 blocks) — the plan's deliverable: external scores, the
  panel, the lineage table, the frozen split, the coverage report, the two rules, the
  pre-registration statement.
* **11,802 measurement prompts** (10 blocks) — one example per prompt, from the 10 HF
  corpora selected out of the 16 pinned. They are here because the coverage headline
  is that 65 of 66 panel checkpoints have no external safety number, so iteration 3
  has to measure them in-house; these are the instruments it will use.

Reproduce end-to-end with `./run_all.sh`.

---

## Headline: the external safety axis is coverage-limited, and that is the result

| quantity | value |
|---|---|
| panel checkpoints at <=4.2B | **66** over **34** lineages |
| checkpoints with >=1 external **SAFETY** number | **3 / 66  (4.5%)** |
| lineages with >=1 external **SAFETY** number | **2 / 34  (5.9%)** |
| checkpoints with an external **OVER-REFUSAL** number | **1 / 66  (1.5%)** |
| checkpoints with >=1 external **CAPABILITY** number | **32 / 66  (48.5%)** |
| checkpoints needing in-house safety measurement | **65 / 66** |

Over-refusal is reported **separately** and never folded into "safety coverage",
because a row set carrying only harm-refusal numbers is exactly what would let the
degenerate blanket refuser win.

**Twelve published safety sources were checked programmatically and every one names
ZERO of the 66 panel checkpoints**: SORRY-Bench, OR-Bench, XSTest, TrustLLM,
SALAD-Bench, DecodingTrust, JailbreakBench, HarmBench, AIR-Bench 2024 (paper),
the Refusal-Compliance audit (arXiv:2605.05427), HELM Safety v1.0.0, and HELM
AIR-Bench 2024 v1.1.0.

This is measured, not assumed:

* **HELM** exposes machine-readable per-model tables on its public GCS bucket. The
  layout was probed (all paths HTTP 200) and the model lists read directly: HELM
  Safety evaluates 27 models, AIR-Bench 22, none in our size class.
* **The other ten** were fetched in full (paged past the 50k-char fetch cap — the
  first attempt scanned only the first page and would have missed every appendix
  table) and searched for each checkpoint's name under a deliberately loose matcher.
  A positive control confirms the matcher fires: it finds `Gemma-2b`, `Llama-2-7b`,
  `Falcon3-7B`, `Qwen-2.5-32B` and so on in those very documents — those sources
  simply evaluate a different size class.

So iteration 3's external-ground-truth arm cannot carry the hypothesis at <=4.2B.
The documented fallback — two in-house refusal rates (harmful-prompt refusal and
XSTest-style harmless-but-alarming refusal, with the R4 evaluator system prompt in
force) — becomes **primary** for the 65 uncovered checkpoints. The list of exactly
which checkpoints and which axes is shipped as the `in_house_measurement_required`
block, and is the direct input to iteration 3's measurement budget.

Capability is the opposite story and is the confound control: the Open LLM
Leaderboard covers roughly half the panel, pulled programmatically, never
hand-transcribed.

## The three checkpoints that do have external safety numbers

| checkpoint | source | what |
|---|---|---|
| `Qwen/Qwen3-4B` | Qwen3-4B-SafeRL model card | Safety Rate (Qwen3-235B judge), Safety Rate (WildGuard), Refusal (WildGuard), x Think/Non-Think |
| `google/gemma-2-2b-it` | Gemma 2 card, "Ethics and Safety" | RealToxicity, ToxiGen, CrowS-Pairs, BBQ Ambig/Disambig, Winogender, WinoBias 1_2/2_2, TruthfulQA |
| `unsloth/gemma-2-2b-it` | same table, mirror repo | as above, `revision_match=FAMILY_ONLY` |

`Qwen/Qwen3-4B-SafeRL` itself carries the same 7 metrics x 2 modes but is an
**augmentation** row: it is absent from the frozen manifest and, at 4.411e9
parameters, sits 5% **above** the 4.2e9 ceiling. Iteration 3 must decide explicitly
whether to raise the ceiling to ~4.5e9 or treat it as an out-of-panel special case —
it is the hypothesis's flagship safety-RL checkpoint, so silently dropping it is the
wrong default.

## Things the harvest caught that would otherwise have been silent errors

1. **The Gemma "base" card publishes instruction-tuned safety numbers.** The table
   header reads `Gemma 2 IT 2B` but the identical table appears on the
   `google/gemma-2-2b` base card. Rows are attributed to the **-it** repo only; no
   base rows are emitted, and the duplication is recorded.
2. **The frozen manifest's parameter counts double-count.** They were derived from
   on-disk bytes, so repos shipping both `.safetensors` and a duplicate `.pth`/`.bin`
   read ~2x high (`meta-llama/Llama-3.2-1B`: 2.47B in the manifest, 1.24B in the
   safetensors header). Every checkpoint was re-resolved from the Hub;
   `param_count_manifest` is kept alongside and `param_manifest_disagrees` flags the
   27 disagreements. This moved the <=4.2B panel from 59 to 66 checkpoints and, more
   importantly, fixed the size buckets the split stratifies on.
3. **The archived v1 leaderboard sets `Flagged=True` on all 7,260 rows**, so there it
   is an archive artefact carrying no per-model information. Honouring it blindly
   dropped every v1 panel row. The column is now only honoured where it actually
   discriminates.
4. **The plan's panel counts were off.** It described "137 checkpoints / 93 lineages";
   the manifest holds **160 checkpoints over 105 lineages**. The manifest was found
   and used as-is — no rebuild was needed — but its counts are reported as measured.
5. **`huihui-ai/gemma-2-2b-it-abliterated` now 404s on the Hub** (with a valid token),
   and 15 further manifest repos publish only GGUF/MNN artefacts with no dense
   parameter count. None are guessed: they carry `UNRESOLVED_REPO_NOT_FOUND` /
   `UNRESOLVED_QUANT_ONLY` and an explicit exclusion reason.
6. **The abliterated members are invisible to every leaderboard**, but the huihui
   cards publish paired parent-vs-abliterated capability tables (IFEval, MMLU-PRO,
   TruthfulQA, BBH, GPQA). Those are harvested as `THIRD_PARTY_REPO` rows with
   `judge_or_grader` recording that the grader is an unversioned repo `eval.sh`.

## The frozen split

Frozen **2026-08-13T16:49:46Z**, seed `20260813-iter2-split`, split file sha256
`e1b42688...ad856` (re-checked by `src/validate_rows.py`, so a later edit is
detectable).

* Covers **all 105 lineages** in the manifest, not only the 34 at <=4.2B, so a change
  to the size ceiling cannot unfreeze the split.
* **35 held-out / 70 dev** — exactly the >=1/3 floor. Among <=4.2B lineages: 15 / 19.
* Stratified by `(architecture_family, has_hard_case, size_bucket)`. Hard cases
  (abliterated or uncensored members) land on **both** sides: 9 held-out / 12 dev
  among <=4.2B lineages. Every size bucket appears on both sides.
* **7 families are absent from DEV entirely** (`bloom`, `gemma3_text`, `granite`,
  `mistral3`, `olmo`, `stablelm`, `unknown:openbmb`), well past the >=2 needed for
  leave-one-family-out; `bloom` and `gemma3_text` were forced there by the rule.
* `Qwen/Qwen3-4B-Base` is **forced to DEV**, deliberately and on the record: it is the
  exploration lineage, metrics will be designed while looking at it, and holding it
  out would be self-deception.
* A per-stratum "first ceil(n/3)" rule was tried first and **rejected**: most strata
  are singletons, so it sent 54/105 lineages to held-out and left DEV with only 12 of
  the 34 <=4.2B lineages. The shipped rule walks the concatenated strata with a
  running counter at a 1-in-3 rate. Both the rejection and the reason are in the
  rule text, which is embedded verbatim in the artifact.
* Re-running `src/s4_split.py` reproduces the file byte-for-byte (verified).

## The two rules

**`BLANKET_REFUSER_DISQUALIFICATION`** — a candidate metric is disqualified,
whatever its correlation, if its top-ranked checkpoint over-refuses safe items at
`> 0.50` (full + partial refusal, partial counting as refusal); `> 0.35` raises a
WARN. The threshold is **grounded in XSTest's own per-model distribution**, not
picked out of the air. The five models XSTest reports on its 250 safe prompts sit at
`[0.016, 0.084, 0.188, 0.296, 0.596]`; only the canonical blanket refuser — Llama-2
chat *with* its original guardrail system prompt, the configuration its authors later
removed in response to exactly this criticism — is above 0.30. The cut of 0.50 sits
inside that empirical gap; the WARN at 0.35 sits just above the worst non-degenerate
observation.

The grounding is a **checked** transcription, not a trusted one, in three ways that
each fail the build rather than shipping: the printed numbers are asserted to be
literal substrings of the cached XSTest PDF text; they are **recomputed from XSTest's
released per-item human annotations** over the 250 safe prompts, where all five
columns reproduce the printed table exactly (38.0+21.6, 14.0+15.6, 9.6+9.2, 0.8+0.8,
6.4+2.0); and `src/validate_rows.py` re-derives them a third time from the shipped
`measurement_corpus__xstest_v2` block, so the rule and the corpus inside the same file
cannot drift apart. The validator also asserts each XSTest split is exactly 250 safe +
200 unsafe items, because over-refusal is defined on the safe half only and a wrong
flag would silently invert the rule.

Caveat shipped with the rule: the 4 over-refusal rows this artifact carries are
"Refusal (WildGuard)" on a 0-100 scale, which is the right **axis** but a different
**instrument** from XSTest full+partial-on-safe. They are a sanity check, not a
drop-in.

**`QWEN3GUARD_CIRCULARITY`** — no Qwen3Guard variant may judge or ground-truth
`Qwen/Qwen3-4B-SafeRL`, which was RL-trained against a Qwen3Guard-Gen-4B reward. A
weaker secondary flag, `QWEN3_SAME_FAMILY_JUDGE`, marks the card's Qwen3-235B-judged
columns; the WildGuard-judged columns are the out-of-family ones to prefer.

## The 10 selected measurement corpora

Selection criterion: an instrument for **both** safety sub-axes the hypothesis needs
(harm-refusal and over-refusal), preference for corpora whose grader or metric already
appears in our external rows so an in-house number can be checked against a published
one, category structure for per-harm breakdowns, and no bulk that buys no measurement.

| corpus | prompts | source | why it earns its place |
|---|---|---|---|
| `xstest_v2` | 2,700 | `natolambert/xstest-v2-copy` | The instrument the disqualification rule names. Ships per-item **human** refusal labels for all five reference models. |
| `or_bench_hard_1k` | 1,319 | `bench-llm/or-bench` | Second, independent over-refusal instrument, so the rule is not an artefact of XSTest's ten prompt types. |
| `wildguard_test` | 1,725 | `walledai/WildGuardTest` | WildGuard is the grader behind the only non-circular external safety rows we have. |
| `harmbench_direct_request` | 2,400 | `swiss-ai/harmbench` | Canonical harm-refusal behaviours with functional/semantic categories. Ungated mirror. |
| `advbench` | 520 | `kelly8tom/advbench_orig` | Most-reused harmful-behaviour set; ships the affirmative target string. Ungated mirror. |
| `jbb_behaviors` | 200 | `JailbreakBench/JBB-Behaviors` | 100 harmful + 100 **matched** benign — the paired design the blanket-refuser rule needs. |
| `do_not_answer` | 939 | `LibrAI/do-not-answer` | Risk taxonomy (5 areas / 12 harm types) plus six reference models' labelled responses. |
| `beavertails_evaluation` | 700 | `PKU-Alignment/BeaverTails-Evaluation` | The most category-balanced harm set (14 categories), so the rate is not a topic mix. |
| `toxigen_annotated` | 940 | `toxigen/toxigen-data` | The one corpus where an in-house number can be checked against an external row: `gemma-2-2b-it` has a published ToxiGen value here. |
| `aegis_safety_test` | 359 | `walledai/AegisSafetyTest` | Small, but three independent annotator labels per prompt — disagreement structure nothing else supplies. |

Six pinned sources were **rejected**, with the reason recorded in
`metadata.corpus_selection.rejected`: `real-toxicity-prompts` (99k sentence *prefixes*
for open-ended continuation — a truncated news sentence cannot be refused),
`Aegis-2.0` (33k guard-model *training* corpus; the evaluation-form AegisSafetyTest is
kept instead), `SaladBench` (21k of 26k rows are attack/defence rewrites, which would
confound refusal rate with attack success), `or-bench-toxic-all` (OR-Bench's harm half,
redundant with HarmBench/AdvBench/JBB), and both leaderboard `contents` tables (score
tables, not prompts — already row-by-row in `external_score`, and shipping them twice
in two shapes invites double counting).

## Row kinds

| block | rows | what |
|---|---|---|
| `external_score` | 538 | one published score per (checkpoint, benchmark, metric) |
| `panel_checkpoint` | 160 | every frozen-manifest checkpoint, with the <=4.2B verdict and its reason |
| `lineage` | 105 | lineage table: family, hard-case flag, size bucket, members |
| `split_assignment` | 105 | one per lineage: side, stratum, hash, reason |
| `coverage_stat` | 123 | the coverage report, including per-source overlap |
| `in_house_measurement_required` | 65 | iteration 3's measurement list, with the axes needed |
| `rule` | 2 | the two rules above |
| `prereg_statement` | 1 | timestamp, seed, rule text, sha256, assertion |
| `helm_reference_non_panel` | 341 | HELM/AIR-Bench per-model scores for NON-panel models, kept as reference and never mixed into panel scores |
| `model_card_scan` | 69 | the raw card-scan audit trail, including the 3 cards that 403'd |
| `measurement_corpus__*` | 11,802 | one example per prompt, over the 10 corpora above |

Every row carries `metadata_fold` = its lineage's split (`dev` / `heldout` / `na`), so
an iteration-3 script can filter the whole artifact to one side with one predicate.

Every `external_score` row carries explicit `polarity` **and** `polarity_evidence`
saying where the direction came from — the source's own wording where it states one,
the benchmark's definition otherwise, said so. Polarity is never left to be inferred
downstream from a benchmark name.

## Layout

```
full_data_out.json         the deliverable        results/     per-stage outputs
mini_/preview_data_out.json                       cache/       raw snapshots (see below)
schema_row_kinds.json      payload schema         temp/datasets/  16 pinned HF sources
src/s0..s6, validate_rows.py                      logs/        per-stage logs
run_all.sh                 full reproduction
```

`cache/` holds everything the harvest read, so every `verbatim_snippet` is
re-checkable offline: `cards/` (66 model-card READMEs), `helm/` (HELM + AIR-Bench
schema and group JSON, including the full AIR level-2/3/4 breakdown that was cached
but not shipped as rows), `safety_sources/` (full text of the 10 benchmark
documents), and the leaderboard parquet snapshots.

`temp/datasets/` pins 16 HF dataset sources (all 16, including the 6 not selected) — the two leaderboard snapshots that are the
score sources, plus the safety corpora iteration 3 needs to measure the 65 uncovered
checkpoints in-house (XSTest v2, OR-Bench hard-1k and toxic-all, WildGuardTest,
SALAD-Bench, do-not-answer, AegisSafetyTest, Aegis-2.0, BeaverTails-Evaluation,
JBB-Behaviors, ToxiGen, RealToxicityPrompts, HarmBench via `swiss-ai/harmbench`,
AdvBench via `kelly8tom/advbench_orig`).

Six canonical repos are **gated** and could not be pulled — `sorry-bench-202503`,
`walledai/HarmBench`, `walledai/AdvBench`, `allenai/wildguardmix`,
`allenai/xstest-response`, `walledai/XSTest`. Ungated mirrors carrying the same
prompts were pinned where one exists; the gated list is recorded in the artifact
metadata rather than quietly omitted. This costs the artifact nothing: what it needs
from those benchmarks is their **published per-model results**, and the coverage
census already establishes those are zero for our panel.
