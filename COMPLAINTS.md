# Review complaints

Objections raised against this experiment, written from the perspective of the
original seed prompt. Each item is one line.

## Panel design

- Base vs instruct is not comparable — completely different prompt format.
- Instruct means instruction-finetuned, not safety-finetuned. That substitution is wrong.
- An official safety Qwen exists on HuggingFace and was never used.
- You cannot pool members within a lineage; you must compare inside it — instruct vs abliterated.

## What is being measured

- The metric only measures refusal rate, which is not the same as safety.
- A model that always refuses automatically wins when you only test harmful prompts.
- No harmless prompts from dangerous topics, like "how do I secure my password".
- Refusal rate is the wrong outcome variable to validate against.
- XSTest should be reported as two separate rates: low on safe, high on unsafe.

## Validation

- No correlation analysis of the metric against an actual published safety benchmark.

## How the score works

- Deciding from only the first token is unreliable.
- "I" can open a refusal or a compliance — "I cannot" versus "I am happy to".
- Different tokenizers split words differently — one has "cannot", another has "can" + "not".

## Scope of the work

- Only two metrics were tested in total.
- Nothing new was actually invented — both metrics came from other papers.

## Status

Checked against the repository contents:

| # | Complaint | Status |
|---|---|---|
| 1 | Base vs instruct format mismatch | **Unpatched.** `round-2/experiment-1/src/method.py:99-111` sets base to `plain`, tuned arms to `chatml`. Confound measured at 0.238 in `round-1/experiment-3`, never applied to the activation contrast. |
| 2 | Instruct is not safety-tuned | **Unpatched.** No safety-specific Qwen anywhere in the frozen panel. |
| 3 | Official safety Qwen unused | **Unpatched.** `Qwen/Qwen3-4B-SafeRL` exists (Apache 2.0, 4.02B, RL against Qwen3Guard-Gen reward). `Qwen3Guard` repos appear in a round-1 HF listing and were never picked up. |
| 4 | Must compare within lineage | **Partly unpatched.** A paired within-lineage test exists for the abliteration refusal-rate claim (10/10, sign test p = 0.0020) but never for the score-vs-benchmark correlation. Flagged internally as claim `C0799`. |
| 5 | Refusal rate is not safety | **Unpatched.** Sole outcome is `"outcome": "y_refusal >= median"`. |
| 6 | Always-refusing model wins | **Unpatched.** Nothing penalises over-refusal in the headline. Cited Hasan & Biswas show over-refusal and harmful compliance are uncorrelated (r = -0.032, p = 0.89). |
| 7 | No safe-but-scary prompts | **Unpatched in the headline.** XSTest is frozen in the corpus (250 safe / 200 unsafe) but never correlated with the score. |
| 8 | Wrong outcome variable | **Unpatched.** Same as 5. |
| 9 | XSTest needs two separate rates | **Data exists, never used.** `round-1/experiment-3` reports both rates on 16 members (50 safe / 25 unsafe items). Never carried into the 52-member panel. |
| 10 | No correlation vs a real benchmark | **Unpatched as stated.** rho = 0.694 is against `judged_refusal_rate` — a home-made 80-item AdvBench slice scored by an LLM judge with kappa = 0.391. No published benchmark score was ever run. |
| 11 | First token is unreliable | **Better than expected.** The score is a soft margin averaged over 80 prompts, not a single hard decision. |
| 12 | "I" is ambiguous | **Handled.** Token list is harvested empirically from 240 real rollouts. For Qwen2, token `I` opened 167 refusals and 0 compliances. An earlier rate-ratio version wrongly admitted `Creating`, `Writing`, `Hack`, `Script`; that was found and fixed. Residual weakness: hand-written tokens with `empirical_count: 0` are unioned in (`" As"`, `"D"` for Désolé). |
| 13 | Tokenizer differences | **Handled.** Per-tokenizer-family empirical lexicon, never back-filled. Five members with no family lexicon get NULL, not a guess. Union fallback drops rho from 0.694 to 0.579. |
| 14 | Only two metrics | **Accurate.** Four table rows, two ideas: logit-gap (3 variants) and a reimplementation of AMS. |
| 15 | Nothing invented | **Accurate.** The paper states "We do not claim the scalar" — the margin is Li & Liu's, AMS is Messenger's. The two metrics this project did invent, alpha_50 and the SPI early-warning indicators, both failed their own controls. |

## Unreported results found in the output files

Two results sit in the shipped JSON but not in the paper.

**Within-lineage instruct vs abliterated**, from `round-5/experiment-1/src/results/`.
The score and the benchmark move the same direction in 6 of 6 pairs:

| lineage | gap instruct | gap abliterated | delta gap | delta refusal |
|---|---:|---:|---:|---:|
| L1 (Qwen3-0.6B) | -4.63 | -10.23 | -5.60 | -0.188 |
| L2 (Qwen3-1.7B) | 1.31 | -13.96 | -15.27 | -0.575 |
| L3 (Llama-3.2-1B) | 15.77 | -2.19 | -17.96 | -0.488 |
| L4 (Qwen2.5-1.5B) | 5.74 | -5.21 | -10.96 | -0.762 |
| Llama-3.2-3B | 14.22 | 6.47 | -7.75 | -0.475 |
| Qwen2.5-0.5B | 1.65 | -3.33 | -4.98 | -0.675 |

**Cross-model refusal-direction cosine.** Exactly one such number exists in the
whole repository: `cos(instruct, abliterated) = 0.8355` at Qwen3-0.6B, layer 15/28,
with the direction norm falling 13.18 to 8.19 while AUROC holds at 0.992. It never
reached the paper. The base arm is `null` only because of loop ordering — base is
`MODEL_PANEL[0]` but the reference is `qwen3-0.6b/instruct`, so `d_ref_vec` is still
unset when base is processed.

## Suggested next experiment

A four-arm panel on one lineage, three of four sharing a chat template:

| arm | checkpoint | wrapper |
|---|---|---|
| base | `Qwen/Qwen3-4B-Base` | plain |
| instruct | `Qwen/Qwen3-4B` | chatml |
| safety-RL | `Qwen/Qwen3-4B-SafeRL` | chatml |
| abliterated | `huihui-ai/Huihui-Qwen3-4B-abliterated-v2` | chatml |

Instruct to SafeRL and instruct to abliterated are two opposite edits from one
shared, format-matched parent. Report XSTest as two rates, keep the base arm
quarantined as the known-confounded contrast, and fix the `cosine_with_parent`
ordering so every arm gets a value.

Note on scoring: SafeRL was trained with Qwen3Guard-Gen as its reward signal, so a
Qwen3Guard-based judge would score it against its own training objective. Use a
different judge.
