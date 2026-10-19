# Who else detects edited safety models — a four-part dossier

Full artifact: `research_report.md` (sections A/B/C/D, every number anchored to primary full text)
and the `structured_answer` object in this file's JSON (14 keys: the 2604.08844 extraction and
mapping table, two ready-to-paste citation paragraphs, the reconciliation paragraph, the
OBLITERATUS certification spec, the reframed novelty sentence, an 8-recipe taxonomy with exact
update equations, a candidate-checkpoint table, a signed W05 prediction table, the parent-free
detector verdict, 12 numbered corrections, and the must-cite list).

**Four of the plan's expectations were wrong, and one finding was not on anyone's list. All five
are reported plainly below.**

## A. arXiv:2604.08844 — verified, and it collides on six statistics but not on the headline

Paul's pre-registered study manufactures 38 LoRA adapters on Llama-3.2-3B-Instruct (r=8, α=16,
q_proj+v_proj, all 28 layers; DPO β=0.1, lr=5e-5, 200 examples, seed 42) across healthy SFT
(n=10), DPO on inverted harmlessness (n=8), DPO on inverted helpfulness (n=6), and
activation-steering-derived adapters (n=6+4 held out) [1, 2]. Every headline number checks out,
with two corrections to how they were stated:

- Binary drift **AUC 1.00, CI [1.00, 1.00], on 23 train / 11 test adapters** with zero
  misclassifications [2, §5.2].
- **All six** pairwise objective comparisons at AUC 1.00 [2, §5.3, Table 2], including the hardest
  (inverted-harmlessness vs inverted-helpfulness, same method and hyperparameters, data axis only).
- **Correction:** "ρ ≥ 0.956" is the **minimum of three** ordinal-severity values, not one number:
  0.976 (inv. harmlessness), 1.000 (inv. helpfulness), 0.956 (refusal steering), all p<0.01, with
  the ordinal scale being the DPO step count 50→2000 [2, §5.3].
- **Correction:** the behavioural correlation is **Spearman ρ = 0.72 on N = 24** non-steered
  adapters, p<0.001, and **no confidence interval is reported** [2, §5.8.4]. Including the six
  steered adapters inflates it to 0.84, which the paper itself discards as a Llama-Guard artefact
  of generation collapse (GPT-4o scored 0/300 steered responses harmful) [2, §5.8.3–4].

**Feature mapping.** Their stable rank ‖ΔW‖²_F/σ₁² and singular-value entropy
H = −Σσ̂ᵢlogσ̂ᵢ (with σ̂ᵢ = σᵢ/Σσⱼ) are **formula-identical** to our W06/W07 and W08/W09 [2, §3.2]
and must be cited at the point of use. Effective rank exp(H), top-k concentration and the spectral
norm are **analogous** to W10 and (at the opposite end of the spectrum) W11. Their *most
informative* feature — cosine of the top-k left singular vectors to a **healthy centroid**,
carrying 10× the coefficient of shape features and 30× of magnitude features [2, §5.9] — is
**parent- and reference-requiring by construction** and is not computable in our setting. Nothing
in that paper pools a Gram matrix across the residual-write ensemble or takes a minimum over
layers, so **W01–W05 have no counterpart**. That is the sharpest novelty axis and it survives as
an item-level claim.

**The cross-method AUC 0.00 is real and verified, and it is confounded.** A classifier trained on
DPO-drifted vs healthy adapters, tested on steering-derived adapters, scores AUC = 0.00
(n_bootstrap = 972, CI [0.00, 0.00]) [2, §5.5]. The anti-ranking reading is confirmed verbatim:
"every steering adapter is classified as more healthy than every DPO adapter, with maximum
confidence" [2, §5.5]. **No fix was attempted** — §6.2 proposes a multi-head monitor but does not
evaluate it. And the paper declares its own confound: the steering arm produced incoherent
generation at every intensity tested, so "the geometric opposition may reflect a broken injection
method rather than a general property of non-DPO training regimes" [2, §6.2]. Anyone citing this as
"the failure mode is already in the literature once" must carry that caveat in the same breath. The
analogy is also **inverted relative to us**: their classifier was trained on *gradient* edits and
failed on a *rank-1 algebraic* edit; ours is built for the rank-1 algebraic edit.

**The counterweight.** ρ = 0.72 is a direct counterexample to any universal claim that weight
geometry carries no behavioural signal — but the paper itself says the correlation "primarily
reflects which side of the boundary, not fine-grained severity within DPO" (healthy cluster at
drift probability 0.001, DPO at 0.999) [2, §5.8.4], i.e. it is a two-class separation reported as a
rank correlation, between classes that differ by a *manufacturing operation*. Our
behaviourally-uncensored class was made by ordinary SFT with no directional edit, so there is no
low-rank scar to find. The corrected, scoped wording for every affected draft sentence is in
`structured_answer.corrections_to_draft`.

## B. OBLITERATUS — **the plan's premise inverts, and our position gets stronger**

The certification code was located and read in full [3]. It is computed **from ACTIVATIONS, not
from weights**: `certify(harmful_activations, harmless_activations, layer_idx)`, on
"post-abliteration activations on harmful prompts" [3]. It forms `diff = mean(harmful) −
mean(harmless)`, estimates a noise variance from the pooled *within-class* covariance by the
median-eigenvalue method (de-biased with an MP-median approximation `(1−√γ)² + γ^(1/3)`), builds a
BBP threshold `σ²(1+√γ)²` inflated by `√κ` (declared in the source as an "OBLITERATUS heuristic
extension"), and thresholds the eigenvalues of the **rank-1** `outer(diff, diff)`. Verdicts are
GREEN / YELLOW / RED with the **worst layer winning**; defaults are confidence 0.95,
distribution_threshold 0.3, min_samples 30 [3].

So: **parent-free yes, prompt-free no, forward-pass-free no, and not a detector of unknown
checkpoints** — it audits an edit the operator has just performed. We were not scooped on the
operation. We *were* preceded on the idea of parent-free spectral inspection and on the observation
that such a verdict mis-calibrates, which is documented verbatim: "**Spectral certification RED is
common** — the spectral check often flags 'incomplete' even when practical refusal rate is 0%.
Check actual refusal rate rather than relying on spectral certification alone" (Common Pitfalls,
item 12, identically worded across three independent mirrors) [5, 6, 7]. That is an independent,
anecdotal mirror of our S2 finding that the ranking transfers and the cutoff does not. **Dates
established:** the file first appears 2026-03-04 and is touched again 2026-03-08 [9]; the Space was
created 2026-02-13 [10] — both predate our work. Two technical observations offered at medium-high
confidence explain the RED bias: the thresholded quantity is an un-normalised between-class
mean-difference energy compared against a within-class noise floor (a units mismatch that grows
with the gap), and because the between-class scatter is rank 1 the YELLOW tier is near-unreachable,
degenerating the certifier to a two-tier test on one number [3].

## C. The recipe taxonomy — and the finding nobody was looking for

**C0. The iteration-2 positive set is already two recipes, not one, and the second one's margin is
halved.** Read from our own `battery.jsonl`, `Goekdeniz-Guelmez/Josiefied-Qwen3-4B-Instruct-2507-
gabliterated-v2` is a **Gabliteration** — `W ← W − α_ℓ(WP)` with `P = R(RᵀR + λI_k)⁻¹Rᵀ`, k∈{1,2,3},
α<1, over dynamically selected layers [11, §2.3, §2.6, §2.7]. Its statistics: **W01 2.237, W04
1.772, W05 −3.522**, against the huihui range W01 4.16–4.82, W04 3.54–4.19, W05 −4.21…−4.82. The
three shrinking mechanisms (λ>0 makes P inexact, α<1 leaves a fraction, only some layers are
touched) predict exactly that, and H1's core question is therefore already half-answered: **graded
margin loss, not collapse**. Two further facts a reviewer will find: the AUROC 1.000 rests on a
**0.077 log-margin** (weakest positive −2.742 vs strongest negative, OLMo-1B-hf, −2.665), and
**W02 = 1.00 on four pre-2023 base models** (pythia-160m/410m/1.4b, OLMo-1B) exactly as on
abliterated ones.

**Eight recipes with reimplementation-grade equations** are in
`structured_answer.recipe_taxonomy`: global all-layer rank-one projection `W ← (I−r̂r̂ᵀ)W` [14, 15];
mlabonne's v2 Gaussian depth kernel `W_ℓ ← W_ℓ − w_ℓ(W_ℓr̂)r̂ᵀ` [16]; Heretic's per-component
optimised kernel with a **float-interpolated** direction index and published weights as high as
**3.22 > 1**, i.e. over-subtraction and a sign flip rather than annihilation [17, 19]; MPOA's exact
four-step row-norm-preserving update `W_new = M·rownormalize(M⁻¹W − α r̂ pᵀ)` [23]; ORBA's
Householder `H = I − 2uuᵀ` with its geodesic λ=1 variant that "zeroes without reflection", its
twice-applied Gram-Schmidt boundary condition, and the authors' own negative result that reflection
makes misdirected sign-flips the characteristic failure mode [25]; Gabliteration [11]; OBLITERATUS's
rank-k `(I − U_kU_kᵀ)W` presets with bias projection and multi-direction norm preservation [4];
per-head/EGA surgery [4]; and SFT uncensoring (no closed form).

**PLAN WAS WRONG on availability.** Three of the four "missing" recipes have public sub-4.2B
checkpoints, all at 4,022,468,096 parameters on the **panel's own Qwen3-4B family**, so a W05 miss
cannot be blamed on architecture: `YanLabs/Qwen3-4B-Instruct-2507-MPOA` ("using the norm-preserving
biprojected abliteration technique") [27], `heretic-org/Qwen3-4B-Instruct-2507-heretic` (Heretic
v1.2.0, `attn.o_proj.max_weight 3.22`) [19], `OBLITERATUS/Qwen3-4B-OBLITERATED` ("abliterated using
the `aggressive` method") [28], and `0xA50C1A1/Qwen3-4B-Instruct-2507-SOM-MPOA` (eight per-direction
weights) [20]. **Only ORBA comes back empty** — an exhaustive Hub search returns 7 repos, all
gemma-3-12b-it at 12.187 B [26, 29] — so it must be reimplemented in-house, which is why its
equations are transcribed at reimplementation grade. Two traps: `gemma-3n-E2B-…-MPOA` is
**5.44 B**, above the ceiling despite its name [30]; and **`huihui-ai/*` is now access-gated** [36],
which affects reproducing six of our eight positives.

**The signed prediction table** (`structured_answer.shared_null_prediction_table`) orders the
predicted margin `R1 > ORBA-v4 ≈ Gabliteration > OBLITERATUS-k > MPOA > Heretic > per-head ≈
Householder-ORBA ≈ SFT`. The single sharpest falsification target is **Householder ORBA**: a
reflection flips the component along u instead of removing it and preserves ‖w‖ exactly, so there
is no null direction for W05 to find at all [25]. Second sharpest is **Heretic**, where
`min_weight` values of 0.51–0.92 shrink the weakest layer's suppression (and W05 is a *minimum*
over layers) while `max_weight = 3.22` over-subtracts [19].

## D. No published parent-free spectral edit detector — the residual risk drops

**Coslett = ADJACENT.** Six access routes were attempted; Zenodo's record, DOI **and REST API all
return HTTP 403** (the plan's expectation that the API serves when the HTML 403s did not hold), the
Crossref route is mis-specified (Zenodo DOIs are DataCite — HTTP 404), and the publisher host is
**unreachable from this machine** (two timeouts plus `connect ECONNREFUSED 66.29.148.24:443`)
[32]. The decisive evidence is the citing paper's characterisation, verbatim: it "detects
abliteration as a **direction-agnostic deviation in activation-geometry fingerprint** (Coslett
2026)", contrasted as detecting "lineage or **structural drift**" [31, §2]. On that
characterisation the signal is in **activations**, anchored to a **claimed identity** — corroborated
by the publisher's own positioning and by its sibling challenge-response IT-PUF work [33]. No
collision; risk **downgraded from LARGE to SMALL-but-open**, with a precise one-sentence
restatement supplied for the draft.

**Saturation met** (queries 6 and 7 — two consecutive on-lane queries — returned nothing new), with
one honest instrument failure: scholarly mode is backed by OpenAlex/Crossref and returned only
biomedical and IoT survey noise for all three on-lane scholarly queries, so general mode carried the
search. Two genuinely new works surfaced. **arXiv:2602.15195** ("Detecting Backdoored LoRAs from
Weights Alone") is weights-only — "This decision is made from weights alone" — and is evaluated on
Qwen2.5-3B, Llama-3.2-3B-Instruct and Gemma-2-2B, our exact size class; but its object is a LoRA
adapter already separated from a frozen base, and §4.3 fits a supervised calibration rule on
labelled adapters [34]. It does not collide, it is currently uncited, and it must be added.
**`reverse-abliterate` 0.1.2** is the only *shipped* parent-free abliteration detector found — and
it scans for `abliteration_metadata.json`, `adapter_config.json` pairs, a `-OBLITERATED` repo-name
suffix, OBLITERATUS commit hashes in config files, shard-size anomalies and registered forward
hooks, generating SHA-256 manifests; **it contains no spectral statistic and reads no tensor
values** [35]. It is the software instantiation of exactly the string-match baseline our H2 says
trivially solves the current positive set, and the paper is much better off naming it first. Zero
citing papers are indexed for 2607.01854, 2604.08844 or 2602.15195 — absence of evidence, with
indexing lag a sufficient explanation.

**Overall D verdict:** no published work computes a spectral or geometric edit detector from a
single full checkpoint without a parent, a sibling, an adapter/base separation, or a labelled
calibration set. The narrow claim survives. The broad claim — "nobody inspects an edited
checkpoint's spectrum parent-free" — does **not**, because of OBLITERATUS, and the paper must say so.
