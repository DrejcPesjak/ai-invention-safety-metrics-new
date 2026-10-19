# Prior Art Check for Safety Metrics

## Summary

Four-part prior-art dossier for a 50-metric single-model safety-screening battery. (A) POSITIONING: our iter-1 site-selection finding is NOT original -- Galeone et al. [1] published the general detection-vs-control dissociation (AUC=1.000 from layer 5 vs cos=0.12/~83deg to the refusal direction; cos in [0.12,0.20] over 4 models/3 families/1B-9B; 0.1197 vs 0.1200 across instruction tuning) on a panel OVERLAPPING ours. Our opening: refusal is never a DETECTED behaviour there, only the lm_head intervention direction. CRITICAL TRAP: their Sec.8 is an explicit NEGATIVE -- the cosine sits at chance for steerable and unsteerable behaviours alike -- so any cosine-as-safety-score metric is already a published negative and may enter only as a declared-expected-to-fail control. A 199-word rewritten positioning paragraph is supplied. alpha_50 = NARROWED after a 14-query saturation search over a 12-paper lane; surviving claim: the only member that is single-scalar, parent-free, HARMFUL-PROMPT-FREE and benchmark-free. Sharpest rival Logit-Gap Steering [3], whose published gap shifts on Qwen2.5-0.5B/Llama-3.2-1B/gemma-2b give a reproduction gate on our exact sizes. Newly surfaced, absent from the plan: Geometry of Refusal [10] and LAP/A_lin [11] (rho=+0.86..+0.91 training-free -- ADOPT for layer selection, do not compete). Rogue Scalpel [7] forces a rewritten pass condition: random directions raise compliance 0%->1-13% (18% in body), so they are a MAGNITUDE-MATCHED COMPARATOR, never a null; their alpha=c*mu(l) matches our NORM_L units. Pre-register against non-monotonic steering strength [6], input-dependent optimal layer [14], and the scalar-steerability objection [15]. (B) WEIGHTS-ONLY = NOVEL (narrow). The collision paper's weight signal is E1 = mean_m sigma_1^2(dW)/sum sigma_i^2(dW) with dW = W_base - W_cand [2] -- it REQUIRES the parent, as does WeightWatch [17]. Parent-free is the hole and is immune to their #1 failure (spoofed reference). Scale escape hatch CLOSED: Qwen2.5-1.5B is in their 273-checkpoint registry. Ships a new implementable observable (SNS-1/2/3 on the shared Gram matrix, SNS-3 supplying the refusal-specificity E1 cannot) plus 13 weights-only statistics, grounded in Jain et al. [18] and HTSR [27] (no safety application found). (C) 9 black-box specs: 5 strong (logit-gap [3], FJD [23], SPD [22], prefill-flip [16], WildGuard [32]), 2 labelled STRAWMEN (first-token entropy has no safety-specific prior; length asymmetry is folklore), SRI [24] off-constraint (rollout-integrating), AMS WEAK (independently measured at AUROC 0.66 / held-out detection 0.35 [2]). (D) COVERAGE VERDICT: fallback (c) FORCED at n=2. HELM Safety VERIFIED to contain no model under 10B (zero num_parameters in [1e8,1e10) in its machine-readable release registry [40]); TrustLLM >=7B; no confirmed <=4B entry on AIR-Bench [28], SALAD-Bench [29] or SORRY-Bench [30]. Qwen3Guard circularity CONFIRMED VERBATIM (two of three reward terms are Qwen3Guard-Gen-4B, helpfulness is WorldPM-Helpsteer2 [20]) -- ban the whole series [21]; AND the abliteration registry's own labels are Qwen3Guard-derived [2], a circularity the hypothesis did not anticipate. Good news: the published SafeRL numbers (47.5->86.5, 64.7->98.1, refusal 12.9->5.3) are judged by Qwen3-235B and WildGuard, so they are NON-circular and usable. (E/F) 29 per-metric design inputs meeting every composition constraint, a 14-ID citation audit (2508.21448 confirmed WRONG [4]; 2603.24543 confirmed RIGHT [5]; 2509.13450 title moved to a THIRD v3 title [8]), and 15 numbered corrections_to_hypothesis. Coslett [35] UNREACHABLE (HTTP 403) = largest residual risk.

## Research Findings

# Prior-art dossier for a fifty-metric single-model safety-screening battery

Full artifact: `research_report.md` (six sections, 818 lines, every number anchored to primary full
text) and the `structured_answer` object in this file's JSON (17 keys: positioning paragraph,
steering-lane table, weights-only verdict and formulas, black-box baseline specs, ground-truth
coverage table, circularity verdict, 29 per-metric design inputs, citation audit, 15 corrections).
Three of the four questions came back as bad news for the hypothesis; all three are reported plainly.

## A. Positioning — our site-selection finding is NOT original, and the geometric version is a published NEGATIVE

Galeone et al. own the general detection-vs-control dissociation [1]. On Gemma 2-2B-it a fake-entity
probe reaches **AUC = 1.000 from layer 5**, yet the direction carrying that signal sits at
**cos = 0.12 (about 83 degrees)** from the direction that produces a refusal; a second detector built
from activations with no chosen tokens gives **cos = -0.06**; the gap generalises at
**cos in [0.12, 0.20]** across four models in three families at 1B-9B, and is **identical before and
after instruction tuning (0.1197 vs 0.1200)**, placing its origin in pretraining [1]. Their panel is
Gemma 2-2B-it, Llama-3.2-1B-Instruct, Qwen-2.5-1.5B-Instruct, Gemma 2-9B-it and Gemma 2-2B base [1] —
**substantial overlap with ours**, so this cannot be dismissed as a scale difference.

**The opening we genuinely have.** Refusal is never a *detected* behaviour in that work; it enters
only as the **intervention** direction, hand-picked from `lm_head` to promote refusal openers
R = {No, cannot, doesn't, I} against compliant ones O = {The, Yes, is, It} [1], which is the refusal
direction of Arditi et al. [33]. The behaviours whose *detection* is studied are output format
(which collapses onto one axis) and hallucination (which does not) [1].

**The trap the artifact direction did not know about.** Their Section 8 explicitly tests and
*rejects* the reading that this cosine predicts steerability: it "sits near the high-dimensional
chance level for steerable and unsteerable behaviours alike", and is "a signature of the
dissociation, not a predictor of how steerable a behaviour is" [1]. **Any metric of the form
"cosine between a probe direction and a steering direction, used as a safety score" is therefore
already published as a negative result**, and may enter our battery only as a declared-expected-to-fail
control. This is the single most binding design constraint in the dossier. A 199-word rewritten
positioning paragraph — crediting [1] as the general result and naming our extension as
refusal-specific, behavioural rather than geometric, and contrast-site-based — is supplied in
`structured_answer.positioning_paragraph`.

**alpha_50 novelty verdict: NARROWED.** A 14-query saturation search (stopping rule met — the last
two on-lane queries returned no new paper, surfacing only abliteration-*method* comparisons [38][39]
and AlphaSteer [34], a steering method rather than a metric) mapped a **12-paper lane**. The sharpest
competitor is Logit-Gap Steering [3]: `Delta_0 = l_refusal(h0) - l_affirm(h0)` at the first decoding
step, a per-prompt safety margin computable on a single checkpoint with no reference model at one
forward pass per prompt. It widens after alignment on **97.5-99.8%** of toxic prompts, with median
shifts **Qwen2.5-0.5B -3.8 -> +1.5, Llama-3.2-1B +0.8 -> +12.7, gemma-2b +2.4 -> +14.8** across 520
AdvBench prompts [3] — our exact model sizes, hence a reproduction gate. Two further papers absent
from the artifact direction matter: The Geometry of Refusal [10] (TrustNLP 2026) already builds an
alpha-sweep family taxonomy ("Late Decision" vs "Early Divergence" across 7 families, 95% ASR on
Llama-3.1 in about one second), and LAP / `A_lin` [11] already predicts steering effectiveness at
**rho = +0.86 to +0.91** and layer selection at **rho = +0.63 to +0.92**, training-free — we should
*adopt* it for layer selection rather than compete with it. The rest of the lane: Safety Pitfalls of
Steering Vectors [5] (CAA steering moves JailbreakBench ASR by up to +57% / -50%), SteeringSafety [8]
(9 safety perspectives, 18 datasets — the benchmark our metric aims to replace, i.e. the cost
baseline), Activation Steering Induces Emergent Misalignment [12] (a collateral-damage control we
need), Weight Arithmetic [13] (ruled out — it needs two fine-tunes), and Kabir [4].

**The surviving claim, verified row by row:** alpha_50 is the only quantity in the lane that is a
single scalar per checkpoint, parent-free, **harmful-prompt-free**, and benchmark-free. Everything
else fails the harmful-prompt or benchmark condition; the one row that also satisfies all four —
LAP [11] — is a predictor of steering success in general, not a safety quantity.

**Three threats must be pre-registered against.** Steering strength acts **non-monotonically** [6]
(ICML 2026, the only peer-reviewed theory in the lane), the optimal steering **layer is
input-dependent** [14] (so a fixed-layer alpha_50 is a lower bound, not the steerability), and
scalar steerability measures are argued to **conceal behavioural shifts** [15] — the strongest
methodological objection in the lane, which our design does not yet answer.

**The random-direction control is not a null.** Rogue Scalpel reports random directions raising
harmful compliance from **0% to 1-13%** in the abstract, reaching **18%** in the body (Llama3.1-8B at
c = 2.0; Falcon3-7B peaks at 3% at c = 0.75), with 20 aggregated random vectors forming a universal
attack, and SAE "benign" features **1-4% worse** than random [7]. Their normalisation
**alpha = c * mu(l)**, mu(l) being the mean activation norm at layer l with c in {0.25 ... 2.0} [7],
is the same family as our NORM_L units — directly comparable, which makes our normalisation
load-bearing. Replacement pre-registered pass condition: *alpha_50(refusal) < alpha_50(norm-matched
random), with a bootstrap CI on the paired difference excluding zero.*

## B. Weights-only detection — NOVEL (narrow), because the collision paper needs the parent

arXiv:2607.01854 is the direct collision, and reading it in full settles the question [2]. Its
weight-recovery energy is `E1 = mean_m [ sigma_1^2(dW_m) / sum_i sigma_i^2(dW_m) ]` with
**`dW_m = W_m^base - W_m^cand`**, over `o_proj` and `down_proj` matrices in a mid-stack band [2].
**It is a statistic of the difference to the parent and is undefined without it** — the
"reference-anchored" qualifier is not confined to the activation signal, and the same holds for its
parent primitive WeightWatch [17], whose top singular vectors of the fine-tuned-minus-base difference
identify newly acquired behaviours. The paper states the dependency at top level ("it presumes an
attested reference") and names as its most severe failure "a spoofed reference evades both axes with
no training (dW = 0, rho = 1 by construction)" [2]. **A parent-free statistic is structurally immune
to exactly that failure**, which is the cleanest statement of what our arm buys.

Their numbers: **AUROC 0.95** combined versus 0.84 (activation gap) and 0.90 (weight energy) on a
**273-checkpoint registry** separating 57 public abliterations from 37 benign fine-tunes, merges and
instruction-tunes; leave-one-family-out balanced accuracy **0.89** (FPR 0.11), missing 4 of 57;
signals negatively correlated at r = -0.41 [2]. **The scale escape hatch is closed** — Qwen2.5-1.5B
appears explicitly in their registry, so we must not claim <=4B novelty.

Searching for a published test of a **shared near-null direction across a model's write matrices** as
a fingerprint of directional ablation returned nothing on target — only weight-sharing work, SVD
commentary, and Arditi et al. [33], whose `W <- W - c r r^T W` is the operation in question. The
dossier therefore defines one implementably (SNS-1/2/3 on the shared Gram matrix
`G = (1/M) sum_m W_m W_m^T / ||W_m||_F^2`), where **SNS-3 = cos(u_d, r_hat) against an
`lm_head`-derived refusal direction supplies the refusal-specificity that E1 explicitly cannot** —
E1 "cannot by itself distinguish refusal removal from addition" [2]. Caveats are pre-registered:
partial-strength ablation (c < 1) leaves a spectral *outlier* rather than an exact null [38], refusal
removal may be a cone rather than a line, and benign low-rank fine-tunes are a known false-positive
mode [2]. Thirteen weights-only statistics with formulas and CPU costs are supplied, grounded in
Jain et al. [18] (safety fine-tuning "minimally transform[s] MLP weights to specifically align unsafe
inputs into its weights' null space", NeurIPS 2024), the rank-localisation prior of Wei et al. [19],
and HTSR / WeightWatcher alpha [27] (alpha ~ 2 optimal, alpha >~ 5-6 random-like), for which **no
safety application was found** — the nearest 2026 use is anti-grokking detection [36]. Adjacent
literatures were checked and cleared: provenance fingerprinting via refusal vectors tracks *lineage*,
not edit type [26]; parameter-dynamics safety risk scoring needs a training trajectory [37]; and the
whole model-diffing family is ruled out by construction, which is the obvious reviewer question and
must be stated. One caution for the limitations section: extended-refusal models retain refusal after
abliteration while standard models drop 70-80 points [39], and abliteration has off-target effects on
disposition even where refusal is never elicited [9].

## C. Black-box baselines — 5 strong, 2 strawmen, 1 off-constraint, 1 weak

Nine specs are delivered with formulas, token sets, costs and gotchas. Strong enough that beating
them means something: the logit gap [3]; FJD first-token confidence [23], which prepends an
affirmative instruction and temperature-scales the logits because jailbreak prompts yield less
confident first tokens; SPD [22], an RBF-kernel SVM over the top-k logits across the first r output
positions (r = 5, k = 50) in a single forward pass — supervised, hence a *harder* bar than ours;
prefill-flip [16], where a user-controlled response prefill flips the first-token decision from
refusal to compliance; and judge-on-output with WildGuard [32] as primary (94.0% agreement with
adjudicated human labels, kappa = 0.86, F1 0.91 on COMPLY, beating Llama-Guard2 and Aegis-Guard by up
to 25.3% on refusal detection).

**Honest negatives.** First-token entropy has **no safety-specific published instantiation** — the
nearest named methods are hallucination detection and intermediate-layer (hence non-black-box)
jailbreak detection — and output-length asymmetry is **folklore with a documented length bias**;
both must be labelled strawmen in the paper rather than beaten quietly. SRI [24] is published and
strong but **rollout-integrating**, which corrects the dependency artifact's characterisation of it
as nearly free and puts it in tension with our R3 constraint. AMS is a **weak** baseline on this
task: an independent published evaluation puts it at Tier-2 AUROC **0.66** and Tier-1 held-out
detection **0.35** on the 273-checkpoint registry [2] — use it as a reproduction gate, not a scalp.

## D. External ground truth — fallback (c) is FORCED at n = 2

Of roughly 20 lineages, exactly **n = 2** carry a published, externally-judged, directly comparable
safety number. **HELM Safety is verified to contain no model below 10B**: a regex over its
machine-readable release registry for `num_parameters` in [1e8, 1e10) returns **zero matches**, the
smallest declared count being Mixtral-8x22B at 46.7B, with open-weight entries at 72B-class [40].
TrustLLM is Llama-2/Vicuna-era at >=7B. AIR-Bench 2024 [28] (314 risk categories, 5,694 prompts),
SALAD-Bench [29] (6 domains / 16 tasks / 66 categories) and SORRY-Bench [30] (binary fulfil/refuse
with a fine-tuned judge at about 10 s per pass) show no confirmed <=4B entry. Vendor cards report in
non-comparable taxonomies. The archived Open LLM Leaderboard v2 results dataset remains downloadable
and does cover small models, but scores **capability only** [31], making it the capability-covariate
source rather than safety ground truth.

**H3 as written does not stand.** Ground truth must be self-measured as two refusal rates — a
harmful-prompt rate and an XSTest-style over-refusal rate on the 250 safe prompts plus 200 unsafe
contrasts [25] — with the iteration-1 R4 evaluator-prompt fix in force, stated plainly in the paper
as self-measured. Four cheapest benchmarks to run ourselves are listed, with AdvBench chosen because
it buys direct comparability with the published per-family gap shifts of [3].

**Circularity: CONFIRMED verbatim, and wider than the hypothesis states.** The Qwen3-4B-SafeRL card
gives three reward components: Safety "as detected by Qwen3Guard-Gen-4B"; Helpfulness "as evaluated
by the WorldPM-Helpsteer2 model"; and Refusal Minimization "also identified by Qwen3Guard-Gen-4B"
[20]. So (i) Qwen3Guard-Gen-4B is forbidden as a judge for that model — confirmed, two of three
reward terms; (ii) the ban should cover the **whole series**, Generative and Stream at 0.6B/4B/8B
[21], since a same-family guard is not an independent evaluator and the cost of the ban is zero;
(iii) WorldPM-Helpsteer2 is circular for the helpfulness / over-refusal axis; and (iv) — the failure
the hypothesis did not anticipate — **an external source does use a Qwen3Guard judge internally**:
the abliteration registry's labels come from "a behavioral oracle (Qwen3Guard ..., think-traces
stripped)" [2], so validating against those labels inherits a Qwen3Guard-derived ground truth. Their
partial mitigation is a second, different-family guard agreeing at Cohen's kappa = 0.78 [2]; our
design rule is to report with and without Qwen-family checkpoints.

**The good news.** The published SafeRL numbers are judged by Qwen3-235B and WildGuard, **not** by
Qwen3Guard, so they are non-circular and usable: Safety Rate (Qwen3-235B) **47.5 -> 86.5**, Safety
Rate (WildGuard) **64.7 -> 98.1**, Refusal (WildGuard) **12.9 -> 5.3** [20]. A safety gain with a
*simultaneous drop* in over-refusal is exactly the two-axis signature our ground truth needs, on the
one lineage where we have it.

## E-F. Design inputs and citation audit

The dossier delivers **29 candidate metrics** — 9 BLACKBOX, 13 WEIGHTS_ONLY, 5 ACTIVATION, 2
STEERING; 6 rows over 60 s; only 2 genuinely rollout-integrating (per R3); 8 rows declared
expected-to-fail; 10 named prior-art baselines rather than our own candidates; and 3 rows whose spec
the dependency artifact already supplies and which must not be re-derived.

The citation audit covers 14 IDs. Confirmed corrections: **arXiv:2508.21448 is not a
steering-strength safety metric** — it is Kabir's ideological-depth measure combining political
steerability with SAE feature richness (the steerable model activates about 7.3x more distinct
political features), and its "refusal as capability deficit" framing is a **confound** for us rather
than support [4]; **arXiv:2603.24543 does resolve correctly** and is on-lane [5]; and
**arXiv:2509.13450's title has moved again** — the live version is **v3** with a third title,
differing from both the v1 and v2 titles named in the plan [8]. Fifteen numbered
`corrections_to_hypothesis` are supplied, each with corrected wording.

## Confidence, and what would change the verdicts

**High confidence:** the Galeone extraction (full text, all seven questions answered verbatim) [1];
the E1 formula and its parent-dependence, transcribed from primary text [2]; the logit-gap definition
and its per-family shifts [3]; the Rogue Scalpel parameterisation [7]; the three verbatim reward
components and three benchmark rows [20]; and the HELM sub-10B finding, verified against a
machine-readable registry rather than inferred [40].

**Moderate confidence:** the two negative searches — no HTSR-for-safety application [27], and no
published shared-null-direction test — are absence-of-evidence over arXiv and general web for
concepts with no settled name. Coverage rows for AIR-Bench [28], SALAD-Bench [29], SORRY-Bench [30]
and JailbreakBench were assessed by search and paper-level reading rather than by enumerating each
leaderboard, so they remain unverified at item level even though the family-level fallback-(c)
verdict is safe.

**One source is unreachable and it matters.** The Coslett record returned HTTP 403 from both the
record page and the DOI resolver [35]; it is characterised elsewhere as an *activation*-geometry
fingerprint [2], but it is the only known work described as detecting abliteration without an
explicit weight difference, and it is the single largest residual risk to the weights-only NOVEL
verdict. A paper defining a steering-threshold safety scalar computed without harmful prompts would
flip alpha_50 from NARROWED to OCCUPIED; a parent-free weight statistic for edit-type detection would
flip Section B to REINVENTION; and finding <=4B entries on the un-enumerated leaderboards would move
the coverage verdict from fallback (c) to the hybrid (b).

**Two iteration-1 numbers are carried unverified.** The 27% and AUROC-0.69 figures in the
positioning paragraph came from the artifact direction; iteration-1 outputs are not in this
artifact's dependency set, so they are tagged `[iter-1, verify before publication]` inline rather
than asserted.


## Sources

[1] [Galeone et al., Perfect Detection, Failed Control: The Geometry of Knowing vs. Steering in Language Models (arXiv:2606.24952v1, cs.CL, 23 Jun 2026)](https://arxiv.org/abs/2606.24952) — Full text read. AUC=1.000 from layer 5 on fake-entity detection (Gemma 2-2B-it); cos=0.12 (~83 deg) to the refusal-producing direction; cos=-0.06 for the activation-built detector; cos in [0.12,0.20] across 4 models / 3 families / 1B-9B; 0.1197 vs 0.1200 before/after instruction tuning; refusal is the INTERVENTION direction only and is NOT a detected behaviour; Section 8 is an explicit NEGATIVE result killing the cosine-as-steerability-diagnostic reading.

[2] [Hurtado (Moonsong Labs), Has This Checkpoint Been Abliterated? A Two-Signal Audit and Its Failure Map (arXiv:2607.01854v1, cs.CR, 2 Jul 2026)](https://arxiv.org/pdf/2607.01854) — Full text read. DECISIVE: weight-recovery energy E1 = mean_m sigma_1^2(dW_m)/sum_i sigma_i^2(dW_m) with dW_m = W_m^base - W_m^cand, over o_proj and down_proj in a mid-stack band -- REQUIRES the parent checkpoint. AUROC 0.95 combined vs 0.84/0.90 alone; 273-checkpoint registry, 57 abliterations vs 37 benign; LOFO balanced accuracy 0.89 (FPR 0.11), missing 4 of 57; r=-0.41 between signals. Covers Qwen2.5-1.5B, so <=4B is NOT a scale gap. Failure map: spoofed reference (dW=0, rho=1) and white-box evasion. Labels come from Qwen3Guard. Independently evaluates AMS at Tier-2 AUROC 0.66 / Tier-1 held-out detection 0.35.

[3] [Li & Liu (Palo Alto Networks), Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness (arXiv:2506.24056v2, rev 1 May 2026)](https://arxiv.org/pdf/2506.24056) — Sharpest competitor to alpha_50. Delta_0 = l_refusal(h0) - l_affirm(h0) at the first decoding step. Gap widens after alignment on 97.5-99.8% of toxic prompts; median shifts Qwen2.5-0.5B -3.8->+1.5, Llama-3.2-1B +0.8->+12.7, gemma-2b +2.4->+14.8 on 520 AdvBench prompts -- a reproduction gate on our exact model sizes. 1 forward pass per prompt for the gap; ~26,000 fwd-pass-equivalents (~2 min on one A100) for the suffix-discovery half only.

[4] [Shariar Kabir, When Models Refuse: Political Steerability and Feature Richness as Measures of Ideological Depth (arXiv:2508.21448v3, rev 2 Jun 2026)](https://arxiv.org/abs/2508.21448) — CONFIRMS the citation correction: this is an ideological-depth measure (political steerability + SAE feature richness, ~7.3x more distinct political features in the steerable model), NOT a steering-strength safety metric. Its 'refusal as capability deficit' framing is a confound for our design, not support.

[5] [Li, Fastowski, Zaradoukas, Prenkaj, Kasneci, Analysing the Safety Pitfalls of Steering Vectors (arXiv:2603.24543v1, 25 Mar 2026)](https://arxiv.org/abs/2603.24543) — ID resolves correctly and IS on-lane. CAA steering changes JailbreakBench ASR by up to +57% / -50%; attributed to overlap between steering vectors and latent refusal directions.

[6] [Taimeskhanov, Vaiter, Garreau, Towards Understanding Steering Strength (arXiv:2602.02712v2; ICML 2026, 50 pp)](https://arxiv.org/abs/2602.02712) — Peer-reviewed theory of steering magnitude on next-token probability, concept presence and cross-entropy. Its NON-MONOTONICITY result is a threat to alpha_50's well-definedness, not a support. Validated on eleven LMs.

[7] [Korznikov, Galichin, Dontsov, Rogov, Oseledets, Tutubalina, The Rogue Scalpel: Activation Steering Compromises LLM Safety (arXiv:2509.22067v2, rev 15 Feb 2026)](https://arxiv.org/pdf/2509.22067) — Random directions raise harmful compliance 0% -> 1-13% (abstract) and up to 18% in the body (Llama3.1-8B at c=2.0; Falcon3-7B peaks at 3% at c=0.75). 20 aggregated random vectors give a universal attack requiring no harmful data/weights/gradients/logits. SAE 'benign' features are 1-4% WORSE than random. Normalisation alpha = c*mu(l) with mu(l) the mean activation norm at layer l, c in {0.25..2.0} -- identical family to our NORM_L units, so directly comparable. Models 3B-70B.

[8] [Siu, Crispino, Park, Henry, Wang, Liu, Song, Wang, SteeringSafety: Benchmarking Representation Steering in LLMs Across Safety Perspectives (arXiv:2509.13450v3, rev 12 Aug 2026)](https://arxiv.org/abs/2509.13450) — TITLE MOVED AGAIN: v3 title differs from both the v1 (SteeringControl) and v2 (SteeringSafety: A Systematic Safety Evaluation Framework) titles named in the plan. 9 safety perspectives, 18 datasets, DIM/ACE/CAA/PCA/LAT. Panel Gemma-2-2B, Llama-3.1-8B, Qwen-2.5-7B. This is the benchmark cost baseline our metric aims to replace.

[9] [Fafula, Abliteration Is Not a Scalpel: Off-Target Effects of Refusal Removal on Decision Disposition Across Model Families (arXiv:2607.17427v1, 19 Jul 2026)](https://arxiv.org/abs/2607.17427) — Capability-confound citation: abliteration shifts disposition (+12.2 pp Gemma / +7.4 pp Qwen optimism) on a 21,600-decision probe that elicits NO refusals at all, and reverses sign on confidence between families.

[10] [Ratnakar & Vats, The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs (arXiv:2606.22686v2; TrustNLP 2026 @ ACL)](https://arxiv.org/abs/2606.22686) — NEWLY SURFACED, not in the artifact direction. Contrastive Logit Steering with an alpha sweep produces a family taxonomy ('Late Decision' vs 'Early Divergence') across 7 families; 95% ASR on Llama-3.1 in ~1 s; CLS beats activation steering (73% vs 22.6% on Llama 2; 91% vs 79.2% on Qwen 7B). Closest published alpha-sweep-derived model taxonomy; must be cited.

[11] [Billa, Predicting Where Steering Vectors Succeed (arXiv:2604.15557v1)](https://arxiv.org/abs/2604.15557) — Linear Accessibility Profile A_lin: apply the unembedding to intermediate hidden states, training-free. Peak A_lin predicts steering effectiveness at rho=+0.86..+0.91 and layer selection at rho=+0.63..+0.92 across 24 concept families and 5 models (Pythia-2.8B..Llama-8B). Satisfies all four of our constraints -- adopt for layer selection, do not compete.

[12] [Cao, Lou, Liu, Feng, Li, Ng, Luu, Activation Steering Induces Emergent Misalignment: A More Comprehensive Evaluation (arXiv:2606.08682v1)](https://arxiv.org/abs/2606.08682) — Steering induces broad emergent misalignment beyond the target behaviour -- the collateral-damage control our steering arm needs.

[13] [Fierro & Roger, Steering Language Models with Weight Arithmetic (arXiv:2511.05408v2)](https://arxiv.org/abs/2511.05408) — Contrastive weight steering: subtract weight deltas of two opposite fine-tunes; generalises further OOD than activation steering. RULED OUT by our single-checkpoint constraint (needs two fine-tunes) but establishes that behaviour has a weight-space direction.

[14] [Gadgil, Lin, Lee, Where to Steer: Input-Dependent Layer Selection for Steering Improves LLM Alignment (arXiv:2604.03867v1)](https://arxiv.org/abs/2604.03867) — Shows the optimal steering layer varies substantially across inputs, theoretically and empirically. Direct threat to alpha_50's fixed-layer design: our alpha_50 is a lower bound on steerability, not the steerability.

[15] [Chang, Schnabel, Swaminathan, Wiens, A Course Correction in Steerability Evaluation: Revealing Miscalibration and Side Effects in LLMs (arXiv:2505.23816v2)](https://arxiv.org/abs/2505.23816) — The strongest METHODOLOGICAL objection in the lane: argues scalar measures of steerability conceal behavioural shifts in open-ended generation. Must be answered or conceded.

[16] [Li, Hu, Sang, Ma, Nie, Zhang, Yu, Su, Huang, Zhou, Prefill-level Jailbreak: A Black-Box Risk Analysis of LLMs (arXiv:2504.21038v2)](https://arxiv.org/abs/2504.21038) — User-controlled response prefill flips the first-token decision from refusal to compliance -- basis for the prefill-flip black-box baseline (2 forward passes per prompt), a fragility axis distinct from the logit-gap margin.

[17] [Zhong & Raghunathan (CMU), Watch the Weights: Unsupervised monitoring and control of fine-tuned LLMs (arXiv:2508.00161)](https://arxiv.org/abs/2508.00161) — WeightWatch, the parent primitive of 2607.01854's E1. Top singular vectors of the fine-tuned-minus-base weight difference correspond to newly acquired behaviours; computed on o_proj and down_proj; stops up to 100% of backdoor utilisations at FPR<1.2%. REQUIRES the base model by construction -- confirms the parent-free gap.

[18] [Jain, Lubana, Oksuz, Joy, Torr, Sanyal, Dokania, What Makes and Breaks Safety Fine-tuning? A Mechanistic Study (NeurIPS 2024)](https://arxiv.org/abs/2407.10264) — Peer-reviewed foundation for the weights-only arm: supervised safety fine-tuning, DPO and unlearning all 'minimally transform MLP weights to specifically align unsafe inputs into its weights' null space'. Makes a low-rank/null-space weight signature principled rather than ad hoc.

[19] [Wei et al., Assessing the Brittleness of Safety Alignment via Pruning and Low-Rank Modifications (arXiv:2402.05162)](https://arxiv.org/abs/2402.05162) — Localises safety-critical neurons and ranks; supplies the rank-localisation prior the weights-only arm rests on. Needs a benchmark run, so not itself a candidate metric.

[20] [Qwen3-4B-SafeRL model card (Hugging Face)](https://huggingface.co/Qwen/Qwen3-4B-SafeRL) — CIRCULARITY CONFIRMED VERBATIM, three reward components: Safety = 'Penalizes the generation of unsafe content, as detected by Qwen3Guard-Gen-4B'; Helpfulness = 'Rewards responses that are genuinely helpful, as evaluated by the WorldPM-Helpsteer2 model'; Refusal Minimization = 'Applies a moderate penalty for unnecessary refusals, also identified by Qwen3Guard-Gen-4B'. ALSO supplies the only usable external ground truth: Safety Rate (Qwen3-235B) 47.5 -> 86.5; Safety Rate (WildGuard) 64.7 -> 98.1; Refusal (WildGuard) 12.9 -> 5.3 -- judged by Qwen3-235B and WildGuard, NOT Qwen3Guard, so non-circular and usable.

[21] [Qwen3Guard Technical Report (arXiv:2510.14276)](https://arxiv.org/abs/2510.14276) — Confirms the family: Generative and Stream variants, each 'available in three sizes (0.6B, 4B, and 8B parameters)'. Whether variants share training data is UNVERIFIED from the abstract; the prudent series-wide judge ban is recommended on that basis.

[22] [Candogan, Wu, Abad Rocamora, Chrysos, Cevher, Single-pass Detection of Jailbreaking Input in Large Language Models (arXiv:2502.15435v1)](https://arxiv.org/abs/2502.15435) — SPD: an RBF-kernel SVM over the top-k logits at the first r output positions (r=5, k=50) predicts whether the output will be harmful in ONE forward pass. A supervised -- hence harder -- black-box baseline.

[23] [Chen, Xia, Jia, Li, Torr, Gu, LLM Jailbreak Detection for (Almost) Free! (arXiv:2509.14558v2, rev 23 Jan 2026)](https://arxiv.org/pdf/2509.14558) — FJD: prepend an affirmative instruction, temperature-scale the logits, and use the CONFIDENCE OF THE FIRST TOKEN. Jailbreak prompts produce less confident first tokens than benign ones. One forward pass, no auxiliary model.

[24] [Rahimi, Hirshel, Himelstein, LeVi, Mendelson, Baskin, Step-Wise Refusal Dynamics in Autoregressive and Diffusion Language Models (arXiv:2602.02600v3)](https://arxiv.org/abs/2602.02600) — Resolves the dependency artifact's 'SRI' recommendation: SRI = Step-Wise Refusal Internal Dynamics, a per-generation-step trajectory enabling a jailbreak detector trained on benign signals only. CORRECTION: it is rollout-integrating, not a cheap single-position hidden-state readout, so it conflicts with R3 and belongs in the long-rollout minority.

[25] [Rottger et al., XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models (NAACL 2024)](https://arxiv.org/abs/2308.01263) — 250 safe prompts across 10 types plus 200 unsafe contrasts; HF at walledai/XSTest. The over-refusal axis for the forced fallback-(c) self-measured ground truth, and the cheapest credible external item set (450 generations per checkpoint).

[26] [Xu & Sheng, A Behavioral Fingerprint for Large Language Models: Provenance Tracking via Refusal Vectors (arXiv:2602.09434)](https://arxiv.org/html/2602.09434v1) — Refusal vectors used for LINEAGE/provenance, not edit-type detection. Confirms that no provenance work detects a specific edit type without a reference.

[27] [AlphaPruning: Using Heavy-Tailed Self-Regularization to Prune LLMs (NeurIPS 2024) + HTSR theory overview](https://www.stat.berkeley.edu/~mmahoney/pubs/neurips-2024-alphapruning.pdf) — Supplies the HTSR alpha metric: ESD rho_emp(lambda) ~ lambda^-alpha; alpha >~ 5-6 = random-like/little task structure, 2 <= alpha <= 5-6 = well-trained, alpha = 2 ideal, alpha < 2 = overfit. Directly usable as weights-only metrics W5/W6. NO published application of HTSR to SAFETY was found.

[28] [AIR-Bench 2024: A Safety Benchmark Based on Risk Categories from Regulations and Policies (arXiv:2407.17436)](https://arxiv.org/abs/2407.17436) — 314 granular risk categories from 8 government regulations and 16 company policies; 5,694 prompts. HF at stanford-crfm/air-bench-2024. No <=4B open-weight entry confirmed.

[29] [SALAD-Bench: A Hierarchical and Comprehensive Safety Benchmark for LLMs (arXiv:2402.05044v4)](https://arxiv.org/html/2402.05044v4) — 6 domains / 16 tasks / 66 categories; leaderboard at HF OpenSafetyLab/Salad-Bench-Leaderboard. No <=4B coverage confirmed.

[30] [SORRY-Bench: Systematically Evaluating Large Language Model Safety Refusal (ICLR 2025)](https://sorry-bench.github.io/) — Binary fulfil(1)/refuse(0) judging via a fine-tuned small-scale LLM at ~10 s per evaluation pass on one A100 -- the cheapest peer-reviewed JUDGED option if we must manufacture ground truth.

[31] [Open LLM Leaderboard v2 results dataset (archived)](https://huggingface.co/datasets/open-llm-leaderboard/results) — Retired March 2025 but the per-model results dataset is still downloadable (5,500+ commits). Covers IFEval, BBH, MATH-L5, GPQA, MuSR, MMLU-Pro -- CAPABILITY only, no safety axis -- and does cover small models, so it is the capability-covariate source, not the safety ground truth.

[32] [WildGuard (allenai/wildguard) model card](https://huggingface.co/allenai/wildguard) — Recommended PRIMARY judge: 94.0% agreement with adjudicated human labels (kappa=0.86), precision/recall/F1 all 0.91 on the COMPLY class; beats Llama-Guard2 and Aegis-Guard on F1 across all three tasks by up to 25.3% on refusal detection. Also the judge used in the Qwen3-4B-SafeRL card's published numbers, which is why those numbers are non-circular.

[33] [Arditi et al., Refusal in Language Models Is Mediated by a Single Direction (NeurIPS 2024)](https://arxiv.org/pdf/2406.11717) — The abliteration primitive W <- W - c r r^T W applied to residual-stream write matrices, and the refusal-direction construction both Galeone and Hurtado build on. Source of the refusal-substring lexicon already transcribed in the dependency artifact.

[34] [AlphaSteer: Learning Refusal Steering with Principled Null-Space Constraint (arXiv:2506.07022)](https://arxiv.org/abs/2506.07022) — Surfaced repeatedly in the saturation search but OFF-LANE: a refusal-steering METHOD with a null-space constraint, not a steering-strength metric. Its appearance in place of any new on-lane paper is part of the evidence that the saturation search converged.

[35] [Coslett (2026), Safety-alignment removal as a model-identity failure -- structural evidence from published weight-level mutation checkpoints (Zenodo 10.5281/zenodo.19383019)](https://zenodo.org/records/19383019) — FULL TEXT UNREACHABLE: zenodo.org/records/19383019 and the DOI resolver both return HTTP 403. Characterised by Hurtado as detecting abliteration via a 'direction-agnostic deviation in activation-geometry fingerprint' -- i.e. ACTIVATION, not weights. The single largest residual risk to the weights-only novelty verdict; must be opened before publication.

[36] [Late-Stage Generalization Collapse in Grokking: Detecting anti-grokking with WeightWatcher (arXiv:2602.02859)](https://arxiv.org/pdf/2602.02859) — Evidence that HTSR/WeightWatcher alpha is used as a training-state DIAGNOSTIC in 2026 -- but for grokking, not safety, reinforcing that the safety application is unclaimed.

[37] [From Parameter Dynamics to Risk Scoring: Quantifying Sample-Level Safety Degradation in LLM Fine-tuning (arXiv:2605.04572)](https://arxiv.org/pdf/2605.04572) — Weight-side safety risk scoring, but from parameter DYNAMICS (a training trajectory, i.e. many checkpoints), so it does not occupy the single-checkpoint parent-free slot.

[38] [Comparative Analysis of LLM Abliteration Methods (arXiv:2512.13655)](https://arxiv.org/pdf/2512.13655) — Surfaced in the final saturation round; an abliteration METHOD comparison, not a metric. Source of the observation that ablation strength is a configurable parameter (e.g. ErisForge 0.6-1.0), which is why the weights-only observable must be a spectral OUTLIER rather than an exact rank deficiency.

[39] [An Embarrassingly Simple Defense Against LLM Abliteration Attacks (arXiv:2505.19056)](https://arxiv.org/pdf/2505.19056) — Extended-refusal models retain >90% refusal after abliteration while standard models drop 70-80 pp -- a defense that would confound any weights-only detector and belongs in the limitations.

[40] [HELM Safety v1.2.0 release schema (model registry JSON)](https://storage.googleapis.com/crfm-helm-public/safety/benchmark_output/releases/v1.2.0/schema.json) — VERIFIES the coverage verdict at machine-readable level: a regex for num_parameters in [1e8, 1e10) returns ZERO matches; the smallest declared count is Mixtral-8x22B at 46.7B and the open-weight entries are 72B-class (qwen1.5-72b-chat, qwen2-72b-instruct, qwen2.5-72b-instruct-turbo). HELM Safety contains no <=4B model.

## Follow-up Questions

- Can the Coslett 2026 record (Zenodo 10.5281/zenodo.19383019) be obtained through a non-403 route (institutional access, author contact, or a mirrored PDF)? It is the single largest residual risk to the weights-only NOVEL verdict, since it is the only known work characterised as detecting abliteration without an explicit weight-difference -- and if its activation-geometry fingerprint turns out to be parent-free, Section B degrades from NOVEL to NARROWED.
- Does the SNS shared-near-null statistic actually survive the bulk spectrum? A cheap pilot on three checkpoints (one abliterated, one instruct, one safety-RL) computing lambda_d(G) against the Marchenko-Pastur edge would decide, before eight weights-only metrics are written against it, whether a rank-1 removal of energy fraction ~1/d_model is detectable at all at partial ablation strength c<1.
- Is alpha_50 monotone in alpha for our panel? arXiv:2602.02712 (ICML 2026) proves steering strength can act non-monotonically, and arXiv:2604.03867 shows the optimal layer is input-dependent. A pre-registration needs a monotonicity check and a decision rule for what alpha_50 means when the refusal-rate curve is non-monotone or the crossing is layer-dependent.

---
*Generated by AI Inventor Pipeline*
