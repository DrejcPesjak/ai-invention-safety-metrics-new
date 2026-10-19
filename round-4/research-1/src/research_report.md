# Who Else Can Spot an Edited Model

## Summary

Primary-source dossier closing Abliterlitics and the windowed-statistic novelty question. (A) ABLITERLITICS documented from source: AGPL-3.0, repo created 2026-04-24, 10 model reports (~2B-59B MoE), four axes. Every weight metric is DELTA-based -- METHODOLOGY 1.1 is `diff = (variant-base).abs().mean()`, 1.2 is `svd(delta_matrix)`, 1.3 needs the base PLUS two variants -- so W01-W05 have NO counterpart and W06-W11 are ANALOGOUS-BUT-DISJOINT (not identical, unlike 2604.08844). Parent requirement quoted: "Create a directory with your base model and variants, plus a comparison.json"; `base` is a mandatory key, no single-checkpoint mode. PLAN WAS WRONG about scale: FOUR reports are at/below ~4.5B, including a full weight report on Qwen3-4B-Instruct-2507, OUR OWN PANEL FAMILY (Heretic 33/36 layers, Huihui 36/36; all three peak at L12-19, L16 #1), plus a 13-variant Gemma4-E2B report with an explicit early/mid/late band table (coverage 7/35 to 35/35, early share 0%-31%). So A4 is EXTERNAL SUPPORT AT OUR SCALE. Verdict SUPPORTS. All planner Qwen3.5-9B numbers re-verified EXACTLY (42/68/62 tensors; 23/29/31 of 32 layers; 2.83/4.89/2.72%; cosine 1.0 / mean 0.997 / 100% of principal angles). Mandatory cosine-caveat reconciliation written out, and DEFUSED by a fact the plan lacked: the same Heretic-Huihui pair is essentially orthogonal (median cosine 0.00017) on Qwen3.5-4B, so 0.997 is a property of one base, not the pair. Abliterlitics NAMES our axis first ("Uniform (33/33/33%)" for LEACE vs "Mid-to-late focused (42-44% late)" for rank-1), as does Gabliteration ("Unlike the uniform layer modification approach in traditional abliteration"). (B) RECIPES from source with signed predictions. HERETIC'S KERNEL IS A TRIANGULAR TENT WITH A HARD CUTOFF, not Gaussian/bell-curve as the plan, the dependency and OBLITERATUS all say: `if distance > min_weight_distance: continue` then LINEAR interpolation; and max_weight_position is sampled in [0.6L,1.0L], direction_index in [0.4L,0.9L], max_weight up to 1.5 -- the peak is CODE-LEVEL forbidden from the early stack, predicting the measured "Layers 0 through 8 have no real edits". MPOA verbatim four-step with layers [11..41] of [0..47]; ORBA H=I-2uu^T with the author's own "misdirected sign-flips" negative result; OBLITERATUS presets 1/4/8/8/4/8/8 re-verified. THREE PLAN REVISIONS: Heretic's shipped default is ALREADY norm-preserving (row_normalization="full") but "PR #52" is UNCONFIRMED; OBLITERATUS is LAYER-SELECTIVE (COSMIC), so W05 DETECTED -> DEGRADED; ORBA is TWO recipes (lambda=1 is "zeroed WITHOUT reflection" = annihilation; only v3 Householder is the isometry) and conflating them makes the falsification test vacuous. W05 and the windowed statistic DISAGREE on six recipes -- that set is the payoff. (B3) Census: 1068 hits, 116 sub-4.2B; all Qwen3-4B variants at 4,022,468,096; ORBA STILL 0 (reimplement); gabliterated 54; Apostate 1, Abliterix 1, AEON 0 genuine; huihui-ai NOT gated (contradicts dependency); two traps -- ?search=&full=true carries NO safetensors, and safetensors.total counts QUANTIZED tensors. (C) C1/C2/C3 all re-verified verbatim (AUC 0.00 n_bootstrap=972 + "GPT-4o scored 0/300"; certify() takes harmful/harmless ACTIVATIONS; reverse-abliterate reads filenames/metadata only). (D) NOVELTY = NOVEL-NARROW, and the plan's premise was wrong: arXiv:2607.01854's E1 is ALREADY "band-averaged" over "each layer in the mid-stack band B", so the band idea is published prior art. Four load-bearing qualifiers survive: parent-free, calibration-free, BOTTOM-of-spectrum, SLIDING/extremum-scored. Two new must-cite competitors ruled out (2607.03377 PL_Alpha_Hill -- parent-free but designed to be INVARIANT to post-training and reads the top; 2608.07921 MP outliers -- parent-free per-layer but detects structure not edits). Multiple-window FPR warning issued. COSLETT CLOSED via DataCite: full abstract obtained, instrument is an inference-time output-geometry/logprob PUF (NOT weights-only), scars "7.6 to over 2,300 times the instrument's acceptance threshold" across two model families -- ADJACENT confirmed on primary evidence, risk downgraded to SMALL. Ships 16 numbered corrections_to_draft and 9 must-cite additions.

## Research Findings

## Headline

Four findings change what the paper says, and one of them is bad news caught in time.

**(1) The "band" idea is already published — cite it or get scooped in review.** The plan
treated a per-band spectral statistic as wholly new. It is not: arXiv:2607.01854's weight
signal E1 is explicitly **band-averaged**, defined over "the set of attention-output
(`o_proj`) and MLP-down (`down_proj`) weight matrices from each layer in the **mid-stack
band** ℬ", and the same band ℬ defines its activation gap ρ [16]. The novelty verdict is
therefore **NOVEL-NARROW**, not NOVEL, and the four load-bearing qualifiers must all be
stated: parent-free, calibration-free, bottom-of-spectrum, and *sliding/extremum-scored*
rather than one fixed band [16, 19, 20, 22, 28, 29, 30].

**(2) Coslett is closed — the dependency's largest residual risk is gone, and the
adjacency verdict now rests on primary evidence.** Six access routes failed previously; the
DataCite REST API works and returns the full author abstract [24]. The instrument is an
**inference-time output-geometry / logprob-order-statistic PUF** anchored to a claimed
identity, not a weights-only statistic — the series it belongs to opens with "Inference-Time
Physical Unclonable Functions from Architecture-Invariant Output Geometry" and "Logprob
Order-Statistic Geometry" [24]. Headline number, quoted: scars "ranging from **7.6 to over
2,300 times the instrument's acceptance threshold**" across published checkpoints from
multiple toolchains in **two model families** [24]. ADJACENT confirmed; residual risk
downgraded to SMALL.

**(3) Heretic's kernel is a triangular tent with a hard cutoff, and its search is
code-level forbidden from editing the early stack.** Everyone — the plan, the dependency,
and OBLITERATUS's own comparison table ("**Bell-curve** layer weighting", [12]) — describes
it as Gaussian. The source says otherwise: `distance = abs(layer_index -
max_weight_position)`; **`if distance > min_weight_distance: continue`**; then *linear*
interpolation [8]. And `max_weight_position` is sampled in `[0.6·L, 1.0·L]`, `direction_index`
in `[0.4·L, 0.9·L]` [9]. Heretic therefore produces genuine *partial coverage* by
construction, with the peak structurally confined to the last 40 % of the stack — an
a-priori prediction that Abliterlitics independently confirmed by measurement ("Layers 0
through 8 have no real edits" [3]; GLM-4.7 E/M/L = **0 % early / 46 % mid / 53 % late**
[7]).

**(4) The external support for the uniform-versus-depth-weighted mechanism exists, is
third-party, and is at our own scale.** The plan feared 7B+ only. Four of Abliterlitics'
ten reports are at or below ~4.5B, including a full weight report on **Qwen3-4B-Instruct-2507
— our own panel's base model** [2, 4, 5, 6]. Verdict: **SUPPORTS**.

## A — Abliterlitics

Abliterlitics [1] is an AGPL-3.0 abliteration-forensics toolkit (repo `created_at`
2026-04-24T23:53:27Z, 32 commits, 21 stars [10, 11]) with four axes — weight analysis, KL
divergence, capability benchmarks, HarmBench — and ten published model reports spanning ~2B
to a 59 GB MoE [2].

**Every one of its weight metrics is delta-based, so the parent requirement is structural,
not incidental.** METHODOLOGY §1.1: "Load corresponding tensors **from base and variant**",
`diff = (variant - base).abs().mean().item()`; §1.2: `svd(delta_matrix)`; §1.3 QR/Grassmann
subspace alignment across *two variants plus* the base; §1.5 cosine between two techniques'
edit vectors; §1.7 stacking on `D_a = variant_a − base` [7]. The README's requirement is
quotable in one line — "**Create a directory with your base model and variants, plus a
`comparison.json`**" — with `base` a mandatory key and `./abliterlitics.sh auto
./my-comparison/` the entry point [1]. There is no single-checkpoint mode anywhere in the
command table. Consequence: **not one Abliterlitics metric has a counterpart to W01–W05**,
and W06–W11 are ANALOGOUS-BUT-DISJOINT rather than identical — same spectral vocabulary,
incompatible input (`ΔW` versus the candidate's own matrices). That is a weaker collision
than the dependency found for arXiv:2604.08844, two of whose features were formula-identical
to ours [22].

**The coverage evidence.** On a shared Qwen3.5-9B base: Heretic 42 tensors / **23 of 32
layers** / 2.83 % relative edit, peaking L17 (4.560); HauhauCS 68 / **29 of 32** / 4.89 %,
peaking L25 (12.329); Huihui 62 / **31 of 32** / 2.72 %, peaking L10 (5.276) [3]. On
Qwen3.5-4B: 29/32, 28/32, 32/32 [5]. On GLM-4.7-Flash: 34/48 (71 %), 47/48 (98 %), 48/48
(100 %) [7]. On Gemma4-E2B, 13 independent abliterations of one ~2B base span **7 of 35
layers to 35 of 35**, with an explicit early/mid/late band table whose early share runs from
**0 % to 31 %** [6]. Every planner-supplied Qwen3.5-9B number re-verified exactly; no
discrepancy found.

Abliterlitics also **names our axis before we do**. Its method-signature table gives a
"Layer distribution" per method: rank-1 Heretic-style "Mid-to-late focused (42–44 % late)"
versus LEACE "**Uniform (33/33/33 %)**", whose identifying feature is "~100 % edit density
with near-zero individual edits" [7]. Gabliteration says the same from the other side:
"**Unlike the uniform layer modification approach in traditional abliteration**…" [21]. The
framing is corroborated, not invented — and both sources must be cited at the point of use.

**The caveat that must be stated first.** Heretic's and Huihui's Qwen3.5-9B edits have
median per-tensor cosine 1.0, global mean 0.997, "100 % of principal angles exceed 0.9
cosine similarity", with Heretic's 42 tensors a strict subset of Huihui's 62 [3]. Read
carelessly that says the recipes are interchangeable. It does not: cosine is computed only
on tensors *both* techniques modify and is silent about coverage and magnitude. The recipes
agree on **which direction** to remove and differ on **where in the stack** and **how
completely** — the one axis a minimum-over-layers statistic keys on and a cosine cannot see.
The report refutes the misreading itself: the identical Heretic–Huihui pair on Qwen3.5-4B
has median cosine **0.00017**, essentially orthogonal, while Heretic remains a proper subset
[5]. A paste-ready reconciliation paragraph is in
`structured_answer.uniformity_external_support.cosine_caveat_paragraph`.

Honest limits: their "layers modified" is a *delta support count*, not our energy minimum;
their numbers are parent-derived, so they show recipes differ in coverage but not that a
parent-free statistic can see that difference; and the richest alignment analysis is on the
9B and 27B [3, 5, 7].

## B — Recipes and signed predictions

Verbatim parameter evidence was re-fetched for all six recipes plus two new ones. Heretic's
kernel and Optuna bounds from source [8, 9]; MPOA's exact four-step row-norm-preserving
update with the guarantee `‖W_new,i,:‖₂ = ‖W_i,:‖₂` and the partial-coverage quote "we
applied a default scale factor of 1.0, intervening on **layers [11..41]**" of a 48-layer
model [17]; ORBA's `H = I − 2uuᵀ`, the geodesic `θ = λ·arccos(ĥ·f̂)`, and the author's own
negative result that reflection makes "**misdirected sign-flips the characteristic failure
mode**" [18]; OBLITERATUS's preset table (directions **1/4/8/8/4/8/8**, re-verified exactly)
[12]; Gabliteration's `ℓ* = arg max_ℓ S_ℓ` "excluding the first *s* and last *e* layers",
ridge `P = R(RᵀR + λI_k)⁻¹Rᵀ`, and depth-peaked `α_ℓ` [21].

Three findings revise the plan. **Heretic's shipped default is already norm-preserving**
(`row_normalization = "full"`, `full_normalization_lora_rank = 3` [13]) — but the "merged in
PR #52" claim could **not** be confirmed; the releases API returns no match [14], so cite the
default, not the PR. **OBLITERATUS is layer-selective, not uniform** (COSMIC layer selection;
the `informed` method decides "which layers are safe to modify" [12]), moving its W05
prediction from DETECTED to DEGRADED. **ORBA is two recipes, not one**: at λ = 1 the author
states the component is "zeroed **without** reflection" [18] — that is annihilation, and only
the separate v3 Householder release is the isometry that leaves no null direction. Conflating
them makes the ORBA falsification test vacuous.

**Where the two statistics disagree is the payoff.** W05 and the windowed statistic agree on
plain rank-one, Apostate and AEON (DETECTED) and on Householder-ORBA (MISSED). They
**disagree on six recipes** — Heretic, mlabonne v2, MPOA, ORBA-λ1, OBLITERATUS and
Gabliteration. That disagreement set is the scientific justification for the windowed
statistic existing, and it is falsifiable in advance in both directions: if the windowed
statistic misses a Heretic or MPOA checkpoint whose edited band is known, the mechanism is
wrong; if it fires on Householder-ORBA, it is wrong the other way.

One negative result to carry: the mlabonne v2 "normal distribution … spread and peak layer"
sentence was **not obtained this session** — huggingface.co served page chrome only [15]. Do
not transcribe it. The depth-weighting claim is supportable instead from Heretic's README,
which independently names that model as the prior art for "Non-constant ablation weights"
[8].

## B3 — Availability

Two-pass HF census: 13 terms, 1,068 raw hits, 380 name-prefiltered candidates, 192 resolved,
**116 at ≤ 4.2 B** [25]. All the Qwen3-4B-Instruct-2507 variants resolve to exactly
**4,022,468,096**: MPOA (YanLabs), Heretic (p-e-w, heretic-org, DreamFast), SOM-MPOA,
OBLITERATUS, Huihui (**not gated**, contradicting the dependency), Gabliteration
(Josiefied-v2) and the DreamFast safetensors conversion of HauhauCS [25].

**ORBA is still empty at our scale** (0 of 35 `ORBA` and 7 `orthogonal-reflection-bounded`
hits) — re-checked, dependency confirmed — so the sharpest falsification target must be
reimplemented in-house. **Gabliteration is abundant (54)**; Apostate and Abliterix each have
exactly one genuine sub-4.2B instance; AEON has **zero** (all 10 name matches are the
unrelated "Aeonium" family, just as 9 `reaper` hits are the username `reaperdoesntknow`).

Two mechanical traps worth more than they look. The `?search=&full=true` endpoint **does not
return `safetensors`**, so a naive census reports "no sub-4.2B instances exist" for every
recipe. And `safetensors.total` counts *quantized* tensors, so
`gemma-4-26B-…-MLX-2bit` passes a 4.2 B ceiling at 3,810,036,302 [25] — reading
`safetensors.total` is necessary but not sufficient, and quantized re-uploads must be
excluded explicitly.

## C — Positioning corrections

All three re-verified from source. **C1**: 2604.08844's cross-method AUC = 0.00
(n_bootstrap = 972, CI [0.00, 0.00]) [22], together with its self-declared confound —
"Language generation collapsed on all steered adapters at all intensities tested … **GPT-4o
scored 0/300 steered responses as harmful**, confirming the output is incoherent" — and no
fix evaluated [22]. **C2**: OBLITERATUS's `certify(harmful_activations, harmless_activations,
layer_idx)` consumes **activations**, so parent-free yes, prompt-free no, forward-pass-free
no, and it audits a self-performed edit rather than screening unknown checkpoints [26]; our
claim is strengthened. **C3**: `reverse-abliterate` scans `abliteration_metadata.json`,
adapter files, the `-OBLITERATED` repo-name convention, embedded commit hashes, shard sizes
and filenames, and forward hooks — no tensor-value statistic anywhere [27]; naming it first
as the software instantiation of the 50.5 % string-match baseline is strictly better than
letting a reviewer name it.

## D — Novelty and the design warning

**NOVEL-NARROW.** Ten competitors ruled out with reasons [16, 19, 20, 22, 26, 27, 28, 29,
30, 7]. The two newly surfaced ones matter most. arXiv:2607.03377 is the closest parent-free
spectral statistic and must be cited: PL_Alpha_Hill is layer-wise, data-free and
scale-invariant — but it reads the **top** of the spectrum (Hill estimator over the top n/2
eigenvalues), aggregates to a model-level signature, and its stated design prerequisite is
the *opposite* of edit detection ("robustness across downstream adaptations … the impact of
post-training on the weight ESD is minimal") [19]. arXiv:2608.07921 is the closest
random-matrix neighbour — parent-free per-layer Marchenko-Pastur bulk/outlier separation —
but it detects learned structure rather than edits, reads outliers, and its "band outliers"
are row/column bands *within* a matrix, not depth bands across the stack [20].

**Design warning for the experiment executor:** a per-band statistic scored by the extremum
over B windows is a maximum of B **correlated** statistics, so at a fixed per-band threshold
the false-positive rate rises with the number of effectively independent windows — and
neither B nor a naive Bonferroni B is the right multiplier. Fix window width and stride
before looking at any candidate; calibrate the threshold on the *extremum* statistic over the
negative population, not on a single band; report the number of windows alongside every
threshold. This **inherits and amplifies** the existing threshold-brittleness problem (the S2
cutoff-transfer failure) rather than solving it, and the paper should quantify both sides of
the trade.

## Confidence

**High** for everything quoted from source: the Abliterlitics metric map, parent requirement,
licence and date, and all numeric fingerprints; Heretic's kernel code and Optuna bounds;
MPOA's four steps; ORBA's formulation; OBLITERATUS's presets and `certify()` signature;
Gabliteration's `ℓ*`, `P`, `α_ℓ`; 2604.08844's numbers; 2607.01854's band-averaged E1; the HF
param counts. **Medium** for the interpretive step in A4(a) — the coverage numbers are real,
but the inference that a minimum-over-layers statistic must therefore miss Heretic is ours
and untested externally — and for the B2 predictions, which are reasoned from published
formulas rather than measured. **Low or explicitly unverified**: the mlabonne v2 kernel
sentence [15]; "MPOA merged in PR #52" [14]; the OBLITERATUS "Spectral certification RED is
common" pitfall sentence (carried from the dependency, not re-fetched); the COSMIC arXiv id
2506.00085 (read from OBLITERATUS's README, not fetched); true parameter counts of quantized
repos; and everything inside Coslett's body text, which remains behind a CC BY-NC-ND
"Confidential and Proprietary, Patent Pending" record [24].


## Sources

[1] [Abliterlitics README (raw, fetched in full)](https://raw.githubusercontent.com/dreamfast/abliterlitics/master/README.md) — Four analysis axes; the verbatim parent requirement ('Create a directory with your base model and variants, plus a comparison.json'); comparison.json schema with mandatory 'base'; CLI './abliterlitics.sh auto ./my-comparison/'; 'weights' = 'panel, edit, SVD, correlation, fingerprint, etc.'; src/weight/ = '11 weight analysis scripts'; 234 tests; AGPL-3.0.

[2] [Abliterlitics project home](https://abliterlitics.dev/) — Model index: 10 reports (gemma4-e4b ~4.5B/23 variants, gemma4-e2b ~2B/13 techniques, qwen25-7b, qwen3.6-27b, glm-4.7-flash, qwen3.5-27b/9b/4b/2b, qwen3-4b). Confirms four of ten reports are at or below ~4.5B.

[3] [Qwen3.5-9B Abliteration Comparison (Abliterlitics)](https://abliterlitics.dev/models/qwen3.5-9b/) — THE load-bearing per-layer report. Tensors changed 42/9.9%, 68/16.0%, 62/14.6%; layers modified 23/32, 29/32, 31/32; 'Layers 0 through 8 have no real edits'; relative edit 2.83/4.89/2.72%; tensor types 3/5/3; top-3 layers with magnitudes; median cosine 1.0, global mean 0.997, '100% of principal angles exceed 0.9 cosine similarity', 42 overlapping, strict subset, corr +0.269; Heretic-HauhauCS 33 tensors/0.136/-0.243; HauhauCS-Huihui 43/0.101/-0.907. Every planner-supplied number re-verified exactly. 'Last updated: August 1, 2026'.

[4] [Qwen3-4B-Instruct-2507 Abliteration Comparison (Abliterlitics)](https://abliterlitics.dev/models/qwen3-4b/) — SUB-4.2B report on OUR OWN PANEL FAMILY (36 layers). Heretic 57 tensors/33-36 layers/2.49%; HauhauCS ~50 real of 253/~28-36/~2.5%; Huihui 108/36-36/2.13%. 'All three techniques concentrate changes in layers 12 through 19. Layer 16 is the number one most modified layer across all three techniques.' HauhauCS-Heretic median cosine 0.966, regression slope 1.06. 253 = PEFT LoRA 7x36+1 with most adapters near-zero.

[5] [Qwen3.5-4B Abliteration Comparison (Abliterlitics)](https://abliterlitics.dev/models/qwen3.5-4b/) — Second sub-4.2B report (32 layers hybrid). 29/83/120 tensors; 29/32, 28/32, 32/32 layers; 2.52/1.10/9.97% relative edit; top layers L19(0.447)/L23(0.324)/L27(2.907). Heretic-Huihui median cosine 0.00017 (essentially orthogonal) with Heretic still a proper subset - the counterexample that defuses the 0.997 alignment caveat. 27 norm artefacts excluded.

[6] [Gemma4-E2B: 13 Techniques Compared (Abliterlitics)](https://abliterlitics.dev/models/gemma4-e2b/) — ~2B, 35 layers, 13 independent variants on one base with an explicit E/M/L band table (early 0-10 / mid 11-22 / late 23-34). Layer coverage ranges 7/35 to 35/35. Three tiers: surgical (<=3%, 1 type, 'a narrow band of mid-to-late layers, L16 to L32'), moderate (69-86% coverage), aggressive. '10 of 13 variants are perfect rank-1', eff rank 1.00, top-1 energy 94.9-99.9%. Alignment clusters; 'many technique pairs are nearly orthogonal at cosine around 0.01'.

[7] [Abliterlitics METHODOLOGY.md](https://raw.githubusercontent.com/dreamfast/abliterlitics/master/docs/METHODOLOGY.md) — Definitions for every weight metric. Sec 1.1 'Load corresponding tensors from base and variant' + diff=(variant-base).abs().mean(); 1.2 svd(delta_matrix), effective rank, energy; 1.3 QR/Grassmann/overlap; 1.4 fingerprint incl. 'Counter by layer index, revealing depth preferences'; 1.5 cosine; 1.7 stacking D_a/D_b/D_r. Sec 5.2 method-signature table with layer-distribution column: rank-1 'Mid-to-late focused (42-44% late)' vs LEACE 'Uniform (33/33/33%)'. Sec 5.4 GLM-4.7 case study E/M/L percentages 0/46/53, 33/35/33, 32/34/34.

[8] [Heretic model.py (Model.abliterate) + README 'How Heretic works'](https://raw.githubusercontent.com/p-e-w/heretic/master/src/heretic/model.py) — THE kernel formula, from source: distance=abs(layer_index-max_weight_position); 'if distance > min_weight_distance: continue'; weight = max_weight + (distance/min_weight_distance)*(min_weight-max_weight). TRIANGULAR with compact support, NOT Gaussian. direction_index float via math.modf + lerp + F.normalize. README: per-component parameters, 'Non-constant ablation weights were previously explored by Maxime Labonne in gemma-3-12b-it-abliterated-v2'.

[9] [Heretic main.py Optuna search bounds](https://raw.githubusercontent.com/p-e-w/heretic/master/src/heretic/main.py) — Verbatim: direction_index in [0.4L,0.9L]; max_weight_lower_bound=-0.25 for mlp.down_proj else 0.8, upper 1.5, clamped max(0.0,...); max_weight_position in [0.6L,1.0L]; min_weight as a FRACTION in [0,1]; min_weight_distance in [1.0, max(0.6L,1.0)]. Code-level guarantee that the edit peak sits in the last 40% of the stack and that weights above 1 (over-subtraction) are in range.

[10] [GitHub API - dreamfast/abliterlitics](https://api.github.com/repos/dreamfast/abliterlitics) — created_at 2026-04-24T23:53:27Z; pushed_at 2026-07-25; updated_at 2026-08-10; license key agpl-3.0 / spdx AGPL-3.0; 21 stars; size 1572.

[11] [Abliterlitics repo page](https://github.com/dreamfast/abliterlitics) — 32 commits, 21 stars, 2 forks; directory tree (src/, docs/, runners/, docker/, tests/); LICENSE present.

[12] [OBLITERATUS README](https://raw.githubusercontent.com/elder-plinius/OBLITERATUS/main/README.md) — Preset table re-verified: basic 1 / advanced 4 / aggressive 8 / surgical 8 / optimized 4 / inverted 8 / nuclear 8 directions. Layer-SELECTIVE by design ('Which layers are safe to modify vs. which are too entangled'; COSMIC layer selection arXiv:2506.00085; steering target_layers=[10..15]). Describes Heretic's kernel as 'Bell-curve layer weighting' - contradicted by Heretic's own source [8].

[13] [Heretic config.default.toml](https://raw.githubusercontent.com/p-e-w/heretic/master/config.default.toml) — row_normalization = 'full' is the DEFAULT ('renormalizes to preserve original row magnitudes') with full_normalization_lora_rank = 3; orthogonalize_direction = true; n_trials 200 / n_startup_trials 60; winsorization_quantile 1.0. Confirms MPOA-style norm preservation is Heretic's shipped default. No max_weight/min_weight keys here (they are Optuna-sampled, see [9]).

[14] [Heretic releases API](https://api.github.com/repos/p-e-w/heretic/releases?per_page=30) — NEGATIVE RESULT: no match for MPOA|row.normalization|norm-preserving|#52 across 30 releases. The plan's 'MPOA merged in PR #52' could NOT be confirmed; the shipped default in [13] confirms the feature, not the PR number.

[15] [mlabonne gemma-3-12b-it-abliterated-v2 model card](https://huggingface.co/mlabonne/gemma-3-12b-it-abliterated-v2) — NEGATIVE / PARTIAL: the fetch returned HF page chrome; the 'normal distribution with a certain spread and peak layer' sentence was NOT retrieved this session and no numeric spread or peak-layer value was found published anywhere. Reported as UNOBTAINED rather than transcribed.

[16] [Has This Checkpoint Been Abliterated? (arXiv:2607.01854)](https://arxiv.org/html/2607.01854v1) — CRITICAL for novelty: E1 = mean over W of sigma_1^2(dW)/sum sigma_i^2(dW) with dW = W_b - W_c, where W is 'o_proj and down_proj weight matrices from each layer in the MID-STACK BAND B ... the rank-1 energy fraction of the edit, BAND-AVERAGED'. The band idea is already published. Also: auditor holds candidate + attested reference; combined z-sum AUROC 0.95 [.90,.98], E1 alone 0.90; AMS Tier-2 0.66, Tier-1 det 0.35; Coslett DOI 10.5281/zenodo.19383019 and the 'direction-agnostic deviation in activation-geometry fingerprint' characterisation.

[17] [MPOA - Norm-Preserving Biprojected Abliteration (grimjim, 2025-11-06)](https://huggingface.co/blog/grimjim/norm-preserving-biprojected-abliteration) — Four-step row-norm-preserving update verbatim (normalize r; decompose W into M and W_hat; p = r_hat^T W_hat, W_hat - alpha*r_hat p^T, renormalize rows; recombine W_new = M W_hat_new) guaranteeing ||W_new,i,:|| = ||W_i,:||. PARTIAL COVERAGE quoted: 'we applied a default scale factor of 1.0, intervening on layers [11..41]' of [0..47]. Layer selection heuristic quality = snr x (1-cos_sim); layers 23 and 29 chosen for Gemma3-12B. Hydra-effect ~70% self-repair justification for multi-layer.

[18] [ORBA - Orthogonal Reflection Bounded Ablation (grimjim)](https://huggingface.co/blog/grimjim/orthogonal-reflection-bounded-ablation) — H = I - 2uu^T; Hw = w - 2(u^T w)u; geodesic w' = w + (cos theta - 1)(w.u)u with theta = lambda*arccos(h_hat.f_hat); 'At lambda = 1 the refusal component of w is rotated exactly to its orthogonal complement - zeroed without reflection'. Twice-applied modified Gram-Schmidt ('twice is enough'), with the admission it 'breaks isometry'. Author's own negative result: reflection makes 'misdirected sign-flips the characteristic failure mode'; v4 released as directional ablation, v3 as Householder.

[19] [Spectral Signatures of Large Language Models (arXiv:2607.03377)](https://arxiv.org/abs/2607.03377) — NEW competitor, parent-free and data-free: PL_Alpha_Hill (Hill estimator over the top n/2 eigenvalues of W^T W) computed layer-wise then aggregated to a model-level signature; scale-invariant; used for lineage, clustering and performance prediction. RULED OUT because its stated prerequisite is the OPPOSITE of edit detection: 'A critical prerequisite ... is its robustness across downstream adaptations ... the impact of post-training on the weight ESD is minimal.' Reads the top of the spectrum. Also does report depth-wise layer-wise perturbation profiles - the honest caveat.

[20] [Spectral Outliers Reveal Dominant Learned Structure in Transformer Attention (arXiv:2608.07921)](https://arxiv.org/abs/2608.07921) — NEW competitor, parent-free per-layer spectral: Marchenko-Pastur separation of each projection matrix into random-like bulk and outliers, across 11 pre-trained transformers, ICMLA 2026. RULED OUT - identifies learned structure, not edits; no safety/abliteration; reads OUTLIERS (top of spectrum); its 'band outliers' are row/column bands WITHIN a matrix, not depth bands across the stack.

[21] [Gabliteration (arXiv:2512.18901v3, Guelmez)](https://arxiv.org/html/2512.18901v3) — Ridge projection P = R(R^T R + lambda I_k)^-1 R^T (NOT an exact projector unless lambda=0), k in {1,2,3}; W <- W - alpha_l (W P); dynamic layer selection l* = argmax_l S_l with S_l = ||mu_h - mu_n||_2 over 'the candidate set of layers (excluding the first s and last e layers)'; adaptive alpha_l = alpha_base(1+beta[1-|xi_l|]), xi_l = (2l-|L_eff|-1)/(|L_eff|-1), 'maximum scaling to middle layers ... reduced scaling toward boundaries'. KEY QUOTABLE: 'Unlike the uniform layer modification approach in traditional abliteration' - a published statement of our own uniform-vs-selective contrast.

[22] [Paul (arXiv:2604.08844) - LoRA weight-space alignment drift](https://arxiv.org/html/2604.08844v1) — C1 re-verified verbatim: cross-method AUC = 0.00 (n_bootstrap = 972, CI [0.00,0.00]); 'AUC 0.00 is not a null result ... perfect discriminative power with inverted labels'. Self-declared confound Sec 5.8.3: 'Language generation collapsed on all steered adapters at all intensities tested ... GPT-4o scored 0/300 steered responses as harmful, confirming the output is incoherent.' No fix evaluated. rho >= 0.956 severity; rho = 0.72 on N=24 (p<0.001). Features are per-layer spectral features of LoRA weight DELTAS.

[23] [Abliteration Techniques Compared (Abliterlitics)](https://abliterlitics.dev/techniques/) — Six technique profiles incl. the three absent from our taxonomy. Apostate: 'orthogonal projection with a balanced profile ... spreads edits across almost all layers with moderate intensity per tensor' - a near-uniform counterexample. Abliterix: Heretic + per-model search. AEON: LEACE-style concept erasure. Huihui: 'gently adjusts a bunch of different parts ... by a small amount each' vs Heretic surgical. Ecosystem ranges: tensors changed 3-53%, relative edit 1-6%, KL 0.001-1.10, ASR 85-100%.

[24] [DataCite record - Coslett (2026), Zenodo 10.5281/zenodo.19383019](https://api.datacite.org/dois/10.5281/zenodo.19383019) — CLOSES the dependency's largest residual risk. Full author abstract obtained: scars 'ranging from 7.6 to over 2,300 times the instrument's acceptance threshold' in 'tested published checkpoints from multiple toolchains across two model families'. The Neural Network Identity Series shows the instrument is inference-time output geometry (Paper 1 'Inference-Time Physical Unclonable Functions from Architecture-Invariant Output Geometry'; Paper 2 'Logprob Order-Statistic Geometry'), plus a note bounding file-level verification. Issued 2026-04-02; ORCID 0009-0006-5518-1218; CC BY-NC-ND-4.0 + All Rights Reserved + Patent Pending. Zenodo OAI-PMH still 403; wayback 404.

[25] [HuggingFace Hub API - two-pass census (this session)](https://huggingface.co/api/models) — 13 search terms, 1068 raw hits, 380 name-prefiltered candidates, 192 resolved, 116 at <=4.2B. All param counts from safetensors.total. Confirms 4,022,468,096 for every Qwen3-4B-Instruct-2507 variant; ORBA/orthogonal-reflection-bounded still ZERO sub-4.2B; gabliterated 54; Apostate 1; Abliterix ~1 genuine; AEON/reaper 0 genuine (name collisions). New traps: the ?search=&full=true endpoint carries no safetensors; quantized MLX re-uploads pass a raw param ceiling. huihui-ai NOT gated, contradicting the dependency.

[26] [OBLITERATUS spectral_certification.py (source)](https://huggingface.co/spaces/pliny-the-prompter/obliteratus/raw/main/obliteratus/analysis/spectral_certification.py) — C2 re-verified: def certify(self, harmful_activations: torch.Tensor, harmless_activations: torch.Tensor, layer_idx: int = -1); docstring 'computes the covariance of residual activations and applies the BBP phase transition'; tiers GREEN certified_complete / YELLOW distributed_refusal / RED incomplete; Marchenko-Pastur noise floor. Consumes ACTIVATIONS, not weights: parent-free YES, prompt-free NO, forward-pass-free NO.

[27] [reverse-abliterate (PyPI JSON)](https://pypi.org/pypi/reverse-abliterate/json) — C3 re-verified: detection = abliteration_metadata.json, LoRA adapter files, '-OBLITERATED' repo-name convention, 'Weight anomalies | Suspicious shard sizes and filenames', missing quantization config, embedded OBLITERATUS commit hashes, forward-hook registration. Hardening = SHA-256 manifests verified 'against a trusted manifest'. No tensor-value statistic anywhere.

[28] [Watch the Weights / WeightWatch (arXiv:2508.00161, Zhong & Raghunathan)](https://arxiv.org/abs/2508.00161) — Confirmed parent-requiring: 'the top singular vectors of the weight difference between a fine-tuned model and its base model correspond to newly acquired behaviors', then monitors activation cosine along those directions. Stops up to 100% of backdoor attacks at <1% FPR.

[29] [Detecting backdoored LoRA adapters from weights alone (arXiv:2602.15195)](https://arxiv.org/html/2602.15195v3) — Ruled out with reasons: explicit adapter/base separation ('Let F_theta denote the frozen base model and let A denote a LoRA adapter attached to that model'); single selected layer; 20-dim projection-wise descriptor; SUPERVISED calibration on 400 benign + 100 poisoned adapters per backbone, standardized then thresholded. Backbones Llama-3.2-3B, Qwen2.5-3B, Gemma-2-2B - our exact size class.

[30] [Matrix-Driven Identification and Reconstruction of LLM Weight Homology (arXiv:2508.06309)](https://arxiv.org/abs/2508.06309) — Ruled out: MDIR detects weight CORRESPONDENCES between models via polar decomposition + Large Deviation Theory and 'compares only a single pair of matrices at a time' - it answers 'are these two models related', not 'was this one edited'. Inference-free, perfect AUC on LeaFBench.

## Follow-up Questions

- Does any later version of arXiv:2607.01854 replace its single fixed mid-stack band B with a swept or sliding band, and does the paper report how E1's AUROC varies with the band's position and width? That single ablation would either confirm the sliding variant as the remaining novelty or collapse it.
- Can Abliterlitics' published per-layer edit-magnitude profiles for the Qwen3-4B and Gemma4-E2B reports be obtained as raw numbers (SVG graph data or a results JSON) rather than top-3 summaries, so that the correlation between their delta-support coverage and our parent-free windowed statistic can be computed directly on shared checkpoints without downloading any base model?
- Does an in-house Householder-ORBA reimplementation at 3-4B actually leave every singular value intact in bf16, or does the accumulated floating-point error the ORBA author warns about ('misdirected sign-flips') create a spurious near-null direction that makes the sharpest falsification test unreliable in the precision the panel actually uses?

---
*Generated by AI Inventor Pipeline*
