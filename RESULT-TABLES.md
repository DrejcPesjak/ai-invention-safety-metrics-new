# Result tables

Generated directly from the shipped JSON outputs. No number is hand-typed.

## 0. Lineage key — L1 to L7

The archived-19 block labels its lineages `L1`–`L7`; the newly measured 33 members use the
full base-model path instead. A **lineage** is one pretrained base plus everything derived
from it, and it is the resampling unit for every model-level claim in the paper.

| lineage | base model | family | layers | d_model | members | levels present |
|---------|------------|--------|-------:|--------:|--------:|----------------|
| **L1** | Qwen3-0.6B | qwen3 | 28 | 1024 | 4 | base, instruct, abliterated |
| **L2** | Qwen3-1.7B | qwen3 | 28 | 2048 | 4 | base, instruct, abliterated, uncensored |
| **L3** | Llama-3.2-1B | llama | 16 | 2048 | 3 | base, instruct, abliterated |
| **L4** | Qwen2.5-1.5B | qwen2 | 28 | 1536 | 3 | base, instruct, abliterated |
| **L5** | SmolLM2-1.7B | llama | 24 | 2048 | 2 | base, instruct |
| **L6** | SmolLM2-360M | llama | 32 | 960 | 2 | base, instruct |
| **L7** | TinyLlama-1.1B | llama | 22 | 2048 | 2 | base, instruct |

Members of each:

| lineage | level | repo |
|---------|-------|------|
| L1 | base | `Qwen/Qwen3-0.6B-Base` |
| L1 | instruct | `Qwen/Qwen3-0.6B` |
| L1 | abliterated | `huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2` |
| L1 | abliterated | `mlabonne/Qwen3-0.6B-abliterated` |
| L2 | base | `Qwen/Qwen3-1.7B-Base` |
| L2 | instruct | `Qwen/Qwen3-1.7B` |
| L2 | abliterated | `huihui-ai/Huihui-Qwen3-1.7B-abliterated-v2` |
| L2 | uncensored | `UnfilteredAI/DAN-Qwen3-1.7B` |
| L3 | base | `unsloth/Llama-3.2-1B` |
| L3 | instruct | `unsloth/Llama-3.2-1B-Instruct` |
| L3 | abliterated | `huihui-ai/Llama-3.2-1B-Instruct-abliterated` |
| L4 | base | `Qwen/Qwen2.5-1.5B` |
| L4 | instruct | `Qwen/Qwen2.5-1.5B-Instruct` |
| L4 | abliterated | `huihui-ai/Qwen2.5-1.5B-Instruct-abliterated` |
| L5 | base | `HuggingFaceTB/SmolLM2-1.7B` |
| L5 | instruct | `HuggingFaceTB/SmolLM2-1.7B-Instruct` |
| L6 | base | `HuggingFaceTB/SmolLM2-360M` |
| L6 | instruct | `HuggingFaceTB/SmolLM2-360M-Instruct` |
| L7 | base | `TinyLlama/TinyLlama_v1.1` |
| L7 | instruct | `TinyLlama/TinyLlama-1.1B-Chat-v1.0` |

Note: `L3` is labelled `llama` family but its base and instruct members are `unsloth`
re-uploads of `meta-llama/Llama-3.2-1B`. `L5`, `L6` and `L7` have no abliterated member,
which is why the within-lineage table in section 2 has 6 rows and not 7.

## 1. Scale panel — round-5 / experiment-1

All 52 members. `gap` = first-decoding-step logit-gap margin on the 80-item harmful core
(higher = predicted safer). `refusal` = judged plain-harmful refusal rate, the benchmark it is
validated against. Sorted by gap. Spearman over the 47 scored members = **0.6941**.

Source: `round-5/experiment-1/src/results/iter5_member_*.json`

| # | gap | refusal | lineage | level | family | block | repo |
|--:|----:|--------:|---------|-------|--------|-------|------|
| 1 | 15.77 | 0.900 | L3 | instruct | llama | archived19 | `unsloth/Llama-3.2-1B-Instruct` |
| 2 | 14.22 | 0.812 | meta-llama/Llama-3.2-3B | instruct | llama | new33 | `unsloth/Llama-3.2-3B-Instruct` |
| 3 | 7.65 | 0.950 | google/gemma-2-2b | instruct | gemma2 | new33 | `unsloth/gemma-2-2b-it` |
| 4 | 6.62 | 0.887 | tiiuae/Falcon3-1B-Base | instruct | llama | new33 | `tiiuae/Falcon3-1B-Instruct` |
| 5 | 6.47 | 0.338 | meta-llama/Llama-3.2-3B | abliterated | llama | new33 | `huihui-ai/Llama-3.2-3B-Instruct-abliterated` |
| 6 | 6.21 | 0.800 | ibm-granite/granite-3.1-2b-base | instruct | granite | new33 | `ibm-granite/granite-3.1-2b-instruct` |
| 7 | 5.74 | 0.975 | L4 | instruct | qwen2 | archived19 | `Qwen/Qwen2.5-1.5B-Instruct` |
| 8 | 5.40 | 0.787 | Qwen/Qwen3-4B-Base | instruct | qwen3 | new33 | `Qwen/Qwen3-4B` |
| 9 | 1.65 | 0.812 | Qwen/Qwen2.5-0.5B | instruct | qwen2 | new33 | `Qwen/Qwen2.5-0.5B-Instruct` |
| 10 | 1.62 | 0.887 | ibm-granite/granite-3.1-2b-base | base | granite | new33 | `ibm-granite/granite-3.1-2b-base` |
| 11 | 1.37 | 0.600 | Qwen/Qwen2.5-0.5B | behavioral_uncensored | qwen2 | new33 | `reallexi/lexi-rm-agent` |
| 12 | 1.31 | 0.750 | L2 | instruct | qwen3 | archived19 | `Qwen/Qwen3-1.7B` |
| 13 | 0.51 | 0.562 | Qwen/Qwen2.5-0.5B | behavioral_uncensored | qwen2 | new33 | `reallexi/lexi-resume-v6` |
| 14 | 0.39 | 0.150 | L4 | base | qwen2 | archived19 | `Qwen/Qwen2.5-1.5B` |
| 15 | 0.30 | 0.637 | L3 | base | llama | archived19 | `unsloth/Llama-3.2-1B` |
| 16 | -0.18 | 0.500 | HuggingFaceTB/SmolLM2-135M | base | llama | new33 | `HuggingFaceTB/SmolLM2-135M` |
| 17 | -0.24 | 0.600 | L5 | base | llama | archived19 | `HuggingFaceTB/SmolLM2-1.7B` |
| 18 | -0.46 | 0.487 | L6 | base | llama | archived19 | `HuggingFaceTB/SmolLM2-360M` |
| 19 | -0.62 | 0.725 | L7 | base | llama | archived19 | `TinyLlama/TinyLlama_v1.1` |
| 20 | -0.80 | 0.150 | L2 | base | qwen3 | archived19 | `Qwen/Qwen3-1.7B-Base` |
| 21 | -0.92 | 0.362 | Qwen/Qwen3-4B-Base | base | qwen3 | new33 | `Qwen/Qwen3-4B-Base` |
| 22 | -1.01 | 0.362 | L5 | instruct | llama | archived19 | `HuggingFaceTB/SmolLM2-1.7B-Instruct` |
| 23 | -1.04 | 0.150 | tiiuae/Falcon3-1B-Base | base | llama | new33 | `tiiuae/Falcon3-1B-Base` |
| 24 | -1.51 | 0.250 | L6 | instruct | llama | archived19 | `HuggingFaceTB/SmolLM2-360M-Instruct` |
| 25 | -1.66 | 0.212 | HuggingFaceTB/SmolLM2-135M | instruct | llama | new33 | `HuggingFaceTB/SmolLM2-135M-Instruct` |
| 26 | -2.19 | 0.412 | L3 | abliterated | llama | archived19 | `huihui-ai/Llama-3.2-1B-Instruct-abliterated` |
| 27 | -2.27 | 0.287 | h2oai/h2o-danube3-500m-base | base | llama | new33 | `h2oai/h2o-danube3-500m-base` |
| 28 | -2.58 | 0.150 | L1 | base | qwen3 | archived19 | `Qwen/Qwen3-0.6B-Base` |
| 29 | -2.61 | 0.487 | EleutherAI/pythia-160m | base | gpt_neox | new33 | `EleutherAI/pythia-160m` |
| 30 | -2.64 | 0.225 | Qwen/Qwen2.5-0.5B | base | qwen2 | new33 | `Qwen/Qwen2.5-0.5B` |
| 31 | -2.78 | 0.600 | allenai/OLMo-1B-hf | base | olmo | new33 | `allenai/OLMo-1B-hf` |
| 32 | -3.03 | 0.338 | Qwen/Qwen3-4B-Instruct-2507 | abliterated | qwen3 | new33 | `Goekdeniz-Guelmez/Josiefied-Qwen3-4B-Instruct-2507-gabliterated-v2` |
| 33 | -3.07 | 0.575 | EleutherAI/pythia-410m | base | gpt_neox | new33 | `EleutherAI/pythia-410m` |
| 34 | -3.08 | 0.163 | L7 | instruct | llama | archived19 | `TinyLlama/TinyLlama-1.1B-Chat-v1.0` |
| 35 | -3.18 | 0.613 | EleutherAI/pythia-1b | base | gpt_neox | new33 | `EleutherAI/pythia-1b` |
| 36 | -3.24 | 0.138 | h2oai/h2o-danube3-500m-base | instruct | llama | new33 | `h2oai/h2o-danube3-500m-chat` |
| 37 | -3.33 | 0.138 | Qwen/Qwen2.5-0.5B | abliterated | qwen2 | new33 | `huihui-ai/Qwen2.5-0.5B-Instruct-abliterated` |
| 38 | -3.64 | 0.662 | EleutherAI/pythia-1.4b | base | gpt_neox | new33 | `EleutherAI/pythia-1.4b` |
| 39 | -3.68 | 0.037 | Qwen/Qwen2.5-3B | abliterated | qwen2 | new33 | `Goekdeniz-Guelmez/Josiefied-Qwen2.5-3B-Instruct-abliterated-v1` |
| 40 | -4.37 | 0.312 | L2 | uncensored | qwen3 | archived19 | `UnfilteredAI/DAN-Qwen3-1.7B` |
| 41 | -4.63 | 0.312 | L1 | instruct | qwen3 | archived19 | `Qwen/Qwen3-0.6B` |
| 42 | -5.08 | 0.188 | Qwen/Qwen3.5-4B-Base | behavioral_uncensored | qwen3_5_text | new33 | `UnfilteredAI/Helvete-nano` |
| 43 | -5.21 | 0.212 | L4 | abliterated | qwen2 | archived19 | `huihui-ai/Qwen2.5-1.5B-Instruct-abliterated` |
| 44 | -5.62 | 0.425 | OEvortex/BabyMistral | behavioral_uncensored | mistral | new33 | `UnfilteredAI/BADMISTRAL-1.5B` |
| 45 | -10.16 | 0.113 | L1 | abliterated | qwen3 | archived19 | `mlabonne/Qwen3-0.6B-abliterated` |
| 46 | -10.23 | 0.125 | L1 | abliterated | qwen3 | new33 | `huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2` |
| 47 | -13.96 | 0.175 | L2 | abliterated | qwen3 | archived19 | `huihui-ai/Huihui-Qwen3-1.7B-abliterated-v2` |

Excluded — 5 members with no empirical refusal-onset lexicon for their tokenizer family
(`MISSING_FAMILY_LEXICON`). Primary columns are NULL, never back-filled:

| lineage | level | family | lexicon status | repo |
|---------|-------|--------|----------------|------|
| microsoft/Phi-4-mini-instruct | behavioral_uncensored | phi3 | `MISSING_FAMILY` | `reallexi/lexi-coder-v4.1` |
| microsoft/Phi-4-mini-instruct | behavioral_uncensored | phi3 | `MISSING_FAMILY` | `reallexi/lexi-coder-v4.3` |
| UnfilteredAI/Mia-001 | behavioral_uncensored | llama | `MISSING_FAMILY` | `UnfilteredAI/Mia-001` |
| UnfilteredAI/Promt-generator | behavioral_uncensored | bloom | `MISSING_FAMILY` | `UnfilteredAI/Promt-generator` |
| UnfilteredAI/UNfilteredAI-1B | behavioral_uncensored | llama | `MISSING_FAMILY` | `UnfilteredAI/UNfilteredAI-1B` |

## 2. Within-lineage — instruct vs abliterated

The comparison the paper never ran for the score. Same base model, one edit applied,
both numbers compared directly. No confounding from size, architecture or training data.

| lineage | gap instruct | gap abliterated | Δ gap | refusal instruct | refusal abliterated | Δ refusal | same direction |
|---------|-------------:|----------------:|------:|-----------------:|--------------------:|----------:|:--------------:|
| L1 | -4.63 | -10.23 | -5.60 | 0.312 | 0.125 | -0.188 | yes |
| L2 | 1.31 | -13.96 | -15.27 | 0.750 | 0.175 | -0.575 | yes |
| L3 | 15.77 | -2.19 | -17.96 | 0.900 | 0.412 | -0.488 | yes |
| L4 | 5.74 | -5.21 | -10.96 | 0.975 | 0.212 | -0.762 | yes |
| Llama-3.2-3B | 14.22 | 6.47 | -7.75 | 0.812 | 0.338 | -0.475 | yes |
| Qwen2.5-0.5B | 1.65 | -3.33 | -4.98 | 0.812 | 0.138 | -0.675 | yes |

**6 of 6 pairs agree.** Every abliteration lowers both the cheap score and the benchmark.

Note: lineage L1 carries two abliterated members (`mlabonne/Qwen3-0.6B-abliterated` at -10.16
and `huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2` at -10.23). The row above uses the huihui one.
Substituting mlabonne changes Δ gap from -5.60 to -5.53 and does not change the verdict.

## 3. XSTest, both rates — round-1 / experiment-3

16 members, repaired judge. Safe items n=50, want the rate **low**. Unsafe contrast items
n=25, want the rate **high**. `Δ` is unsafe minus safe: how well the model separates them.
AdvBench refusal is shown alongside for comparison.

Source: `round-1/experiment-3/src/results/analysis.json`

| member | safe RR ↓ | unsafe RR ↑ | Δ | AdvBench RR | repo |
|--------|----------:|------------:|--:|------------:|------|
| llama32_instruct | 0.080 | 0.760 | +0.680 | 0.975 | `meta-llama/Llama-3.2-1B-Instruct` |
| smollm2_instruct | 0.120 | 0.640 | +0.520 | 0.250 | `HuggingFaceTB/SmolLM2-360M-Instruct` |
| tv_t0.75 | 0.060 | 0.520 | +0.460 | 0.500 | *(derived checkpoint)* |
| smollm2_base | 0.180 | 0.600 | +0.420 | 0.575 | `HuggingFaceTB/SmolLM2-360M` |
| qwen3_instruct | 0.160 | 0.560 | +0.400 | 0.525 | `Qwen/Qwen3-0.6B` |
| abl_c0.50 | 0.260 | 0.640 | +0.380 | 0.525 | *(derived checkpoint)* |
| abl_c0.75 | 0.340 | 0.720 | +0.380 | 0.550 | *(derived checkpoint)* |
| abl_c0.25 | 0.260 | 0.560 | +0.300 | 0.575 | *(derived checkpoint)* |
| abl_c1.00 | 0.420 | 0.720 | +0.300 | 0.512 | *(derived checkpoint)* |
| pythia_410m | 0.240 | 0.520 | +0.280 | 0.550 | `EleutherAI/pythia-410m` |
| tv_t0.50 | 0.100 | 0.320 | +0.220 | 0.388 | *(derived checkpoint)* |
| qwen3_abliterated | 0.060 | 0.240 | +0.180 | 0.113 | `mlabonne/Qwen3-0.6B-abliterated` |
| tv_t0.25 | 0.040 | 0.200 | +0.160 | 0.237 | *(derived checkpoint)* |
| llama32_base | 0.020 | 0.080 | +0.060 | 0.725 | `meta-llama/Llama-3.2-1B` |
| qwen3_base | 0.020 | 0.080 | +0.060 | 0.062 | `Qwen/Qwen3-0.6B-Base` |
| qwen3_base_generictmpl | — | — | — | 0.350 | `Qwen/Qwen3-0.6B-Base` |

Item counts are small: unsafe n=25 gives very wide intervals. `abl_c0.25` at 0.560 has a
95% CI of [0.371, 0.733]. Most rows cannot be told apart. The frozen corpus holds 250 safe
and 200 unsafe XSTest items; only 50 and 25 were run.

## 4. XSTest joined to the cheap score

The overlap between the 52-member scale panel and the 16-member XSTest panel.
This join does not exist anywhere in the repository — the two panels were never connected.

| repo | gap | safe RR | unsafe RR |
|------|----:|--------:|----------:|
| `meta-llama/Llama-3.2-1B-Instruct` | 15.77 | 0.080 | 0.760 |
| `meta-llama/Llama-3.2-1B` | 0.30 | 0.020 | 0.080 |
| `HuggingFaceTB/SmolLM2-360M` | -0.46 | 0.180 | 0.600 |
| `HuggingFaceTB/SmolLM2-360M-Instruct` | -1.51 | 0.120 | 0.640 |
| `Qwen/Qwen3-0.6B-Base` | -2.58 | 0.020 | 0.080 |
| `EleutherAI/pythia-410m` | -3.07 | 0.240 | 0.520 |
| `Qwen/Qwen3-0.6B` | -4.63 | 0.160 | 0.560 |
| `mlabonne/Qwen3-0.6B-abliterated` | -10.16 | 0.060 | 0.240 |

Two rows match on model identity but not on the exact repo string: the scale panel scored
`unsloth/Llama-3.2-1B-Instruct` and `unsloth/Llama-3.2-1B`, while the XSTest panel scored the
`meta-llama` originals. The unsloth repos are re-uploads of the same weights, so the join is
treated as valid here, but it was not verified by revision SHA.

n = 8.

- gap vs XSTest **unsafe** refusal: rho = **0.347** — want high, same job as AdvBench where it scores 0.694
- gap vs XSTest **safe** refusal (over-refusal): rho = **-0.180** — want negative

n=8 is far too small to conclude anything. But on the axis the score is meant to be good at,
it drops from 0.694 on AdvBench to 0.347 on XSTest-unsafe. Worth a real run.
