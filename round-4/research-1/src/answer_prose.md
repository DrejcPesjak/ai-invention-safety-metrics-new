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
