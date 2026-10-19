# Who Else Detects Edited Safety Models

## Summary

Four-part prior-art and taxonomy dossier for the parent-free weights-only abliteration detector (Claim A). (A) arXiv:2604.08844 (Paul) extracted from full text: two of its five features are FORMULA-IDENTICAL to our W06-W09 (stable rank, singular-value entropy with the same sigma-hat normalisation) and must be cited at point of use; its MOST informative feature (cosine of top-k left singular vectors to a healthy-adapter centroid, 10x shape / 30x magnitude coefficients) is parent- AND reference-requiring, so W01-W05 have NO counterpart. Numbers verified with two corrections: rho>=0.956 is the MINIMUM of three ordinal values (0.976/1.000/0.956); rho=0.72 is Spearman on N=24 with NO CI reported. Cross-method AUC 0.00 confirmed verbatim (n_bootstrap=972, CI [0.00,0.00], trained on 10 healthy + 14 DPO, tested on 6+4 steering, score is a fitted probability, NO fix attempted) -- but the paper DECLARES ITS OWN CONFOUND: the steering arm generated incoherent text at every intensity (GPT-4o 0/300 harmful), so the precedent is confounded and must be cited that way. (B) OBLITERATUS's spectral certification READ IN FULL FROM SOURCE and the plan's premise INVERTS: it consumes ACTIVATIONS (harmful/harmless post-edit), not weights -- parent-free but NOT prompt-free, and it audits a self-performed edit rather than detecting unknown checkpoints. Our novelty claim gets STRONGER. Its documented 'RED at 0% refusal' calibration failure is transcribed verbatim from three mirrors and is an independent mirror of our S2. Dated: first public 2026-03-04. (C) Eight recipes with reimplementation-grade equations (rank-one projection, mlabonne Gaussian kernel, Heretic per-component optimised kernel with FLOAT direction index and weights >1 i.e. sign flip, MPOA exact row-norm-preserving four-step, ORBA Householder + geodesic lambda=1, Gabliteration ridge rank-k, OBLITERATUS rank-k presets, SFT). PLAN WAS WRONG on availability: MPOA, Heretic and OBLITERATUS ALL have public sub-4.2B checkpoints at 4,022,468,096 params on the panel's own Qwen3-4B family; only ORBA is empty (7 repos, all 12.187B) and must be reimplemented. FIFTH FINDING, unasked: the iteration-2 positive set ALREADY contains a second recipe -- the gabliterated member is a Gabliteration and scores at HALF the margin (W01 2.237 vs 4.16-4.82), so H1 is half-answered as graded loss not collapse; the AUROC 1.000 rests on a 0.077 log-margin; W02=1.00 on four pre-2023 BASE models. (D) Coslett resolved as ADJACENT (activation-geometry fingerprint against a claimed identity, per the only reachable characterisation); Zenodo record/DOI/REST API all 403 and the publisher host is unreachable, so risk drops LARGE -> SMALL-but-open. Two new works: arXiv:2602.15195 (weights-only but adapter-delta + supervised calibration, our exact size class, currently uncited) and reverse-abliterate (the only shipped parent-free detector -- pure filename/metadata scanning, no spectral statistic). Ships 12 numbered corrections including a FACTUAL ERROR in the current hypothesis, a signed W05 prediction table with Householder-ORBA as the sharpest falsification target, a 5-model shortlist, and a 14-entry must-cite list.

## Research Findings

# Who else detects edited safety models — a four-part dossier

Full artifact: `research_report.md` (sections A/B/C/D, every number anchored to primary full text) and the `structured_answer` object in `research_out.json` (17 keys). **Four of the plan's expectations were wrong, and one finding was not on anyone's list.**

## A. arXiv:2604.08844 — verified; collides on six statistics, not on the headline

Paul manufactures 38 LoRA adapters on Llama-3.2-3B-Instruct (r=8, α=16, q_proj+v_proj, 28 layers; DPO β=0.1, lr=5e-5, seed 42) across healthy SFT (n=10), DPO-inverted-harmlessness (n=8), DPO-inverted-helpfulness (n=6) and steering-derived adapters (n=6+4) [1, 2]. Binary drift **AUC 1.00, CI [1.00,1.00], 23 train / 11 test**, zero misclassifications [2, §5.2]; **all six** pairwise objective comparisons at 1.00 [2, §5.3]. Two corrections: "ρ ≥ 0.956" is the **minimum of three** ordinal values (0.976 / 1.000 / 0.956, the scale being DPO step count 50→2000) [2, §5.3]; and the behavioural number is **Spearman ρ = 0.72 on N = 24**, p<0.001, with **no CI reported** [2, §5.8.4] — including the six steered adapters inflates it to 0.84, which the paper discards as a Guard artefact (GPT-4o scored 0/300 steered responses harmful) [2, §5.8.3–4].

**Mapping.** Their stable rank ‖ΔW‖²_F/σ₁² and entropy H = −Σσ̂ᵢlogσ̂ᵢ are **formula-identical** to our W06/W07 and W08/W09 [2, §3.2] and must be cited at point of use; effective rank, top-k concentration and spectral norm are analogous to W10/W11. Their *most informative* feature — cosine of top-k left singular vectors to a **healthy centroid**, 10× shape and 30× magnitude coefficients [2, §5.9] — is parent- and reference-requiring. Nothing there pools a Gram matrix across the write ensemble or takes a minimum over layers, so **W01–W05 have no counterpart**.

**Cross-method AUC 0.00 is real and confounded.** Trained on DPO-drifted vs healthy, tested on steering adapters: AUC = 0.00, n_bootstrap = 972, CI [0.00,0.00]; "every steering adapter is classified as more healthy than every DPO adapter, with maximum confidence" [2, §5.5]. **No fix was attempted.** And the paper declares its own confound: the steering arm produced incoherent generation at every intensity, so "the geometric opposition may reflect a broken injection method" [2, §6.2]. The analogy is also inverted — their classifier was trained on *gradient* edits and failed on a *rank-1 algebraic* edit; ours is built for the algebraic edit.

**Counterweight.** ρ = 0.72 refutes any universal "weights carry no behavioural signal" claim, but the paper says it "primarily reflects which side of the boundary, not fine-grained severity" (healthy at drift probability 0.001, DPO at 0.999) [2, §5.8.4] — a two-class separation in Spearman clothing, between classes differing by a manufacturing operation. Our uncensored class was made by ordinary SFT, so there is no low-rank scar to find.

## B. OBLITERATUS — the plan's premise inverts, and our position strengthens

The certification source was read in full [3]: `certify(harmful_activations, harmless_activations, layer_idx)` on "post-abliteration activations". It forms `diff = mean(harmful) − mean(harmless)`, estimates noise from the pooled **within-class** covariance by the median-eigenvalue method (de-biased with `(1−√γ)² + γ^(1/3)`), builds a BBP threshold `σ²(1+√γ)²` inflated by `√κ` (an explicitly "heuristic extension"), and thresholds the eigenvalues of the **rank-1** `outer(diff,diff)`; GREEN/YELLOW/RED with the **worst layer winning**; defaults 0.95 / 0.3 / 30 [3]. So: **parent-free yes, prompt-free no, and not a detector of unknown checkpoints.** We were not scooped on the operation; we *were* preceded on parent-free spectral inspection and on the calibration observation, documented verbatim: "**Spectral certification RED is common** — the spectral check often flags 'incomplete' even when practical refusal rate is 0%. Check actual refusal rate rather than relying on spectral certification alone" (Common Pitfalls item 12, three independent mirrors) [5, 6, 7]. **Dates:** file first appears 2026-03-04, touched 2026-03-08 [9]; Space created 2026-02-13 [10] — both predate our work. At medium-high confidence, the RED bias follows from thresholding an un-normalised between-class mean-difference energy against a within-class noise floor, and from the rank-1 scatter making YELLOW near-unreachable [3].

## C. Recipe taxonomy — and the finding nobody was looking for

**C0.** The iteration-2 positive set is **already two recipes**. `Goekdeniz-Guelmez/Josiefied-Qwen3-4B-Instruct-2507-gabliterated-v2` is a **Gabliteration**, `W ← W − α_ℓ(WP)` with `P = R(RᵀR+λI_k)⁻¹Rᵀ`, k∈{1,2,3}, α<1, dynamically selected layers [11]. Its statistics — **W01 2.237, W04 1.772, W05 −3.522** — sit at roughly half the huihui margins (W01 4.16–4.82, W04 3.54–4.19, W05 −4.21…−4.82), exactly as its three shrinking mechanisms predict. H1 is therefore half-answered: **graded margin loss, not collapse.** Also: the AUROC 1.000 rests on a **0.077 log-margin** (−2.742 vs OLMo-1B-hf at −2.665), and **W02 = 1.00 on four pre-2023 base models**.

**Eight recipes with reimplementation-grade equations** are in `structured_answer.recipe_taxonomy`: `W ← (I−r̂r̂ᵀ)W` [14, 15]; mlabonne's v2 Gaussian depth kernel [16]; Heretic's per-component optimised kernel with a **float-interpolated** direction index and published weights up to **3.22 > 1** (over-subtraction, a sign flip rather than annihilation) [17, 19]; MPOA's exact row-norm-preserving `W_new = M·rownormalize(M⁻¹W − α r̂ pᵀ)` [23]; ORBA's `H = I − 2uuᵀ` plus the geodesic λ=1 variant that "zeroes without reflection", with the authors' own finding that reflection makes misdirected sign-flips the characteristic failure mode [25]; Gabliteration [11]; OBLITERATUS's rank-k presets with bias projection and norm preservation [4]; per-head/EGA surgery [4]; SFT (no closed form).

**PLAN WAS WRONG on availability.** Three of the four "missing" recipes have public sub-4.2 B checkpoints, all at 4,022,468,096 params on the **panel's own Qwen3-4B family**: `YanLabs/Qwen3-4B-Instruct-2507-MPOA` [27], `heretic-org/Qwen3-4B-Instruct-2507-heretic` [19], `OBLITERATUS/Qwen3-4B-OBLITERATED` [28], `0xA50C1A1/Qwen3-4B-Instruct-2507-SOM-MPOA` [20]. **Only ORBA is empty** — 7 repos, all gemma-3-12b-it at 12.187 B [26, 29] — so it must be reimplemented. Traps: `gemma-3n-E2B-…-MPOA` is **5.44 B** despite its name [30]; **`huihui-ai/*` is now access-gated** [36], affecting reproduction of six positives.

The signed prediction table orders margin `R1 > ORBA-v4 ≈ Gabliteration > OBLITERATUS-k > MPOA > Heretic > per-head ≈ Householder-ORBA ≈ SFT`. Sharpest falsification target: **Householder ORBA**, which flips rather than removes the component and preserves ‖w‖ exactly, leaving no null direction [25]; second, **Heretic**, whose `min_weight` 0.51–0.92 shrinks the weakest layer (and W05 is a minimum over layers) while `max_weight = 3.22` over-subtracts [19].

## D. No published parent-free spectral edit detector; residual risk drops

**Coslett = ADJACENT.** Zenodo's record, DOI **and REST API all return 403** (the plan's API expectation did not hold), Crossref is the wrong registry (404 — Zenodo DOIs are DataCite), and the publisher host is unreachable from this machine (`connect ECONNREFUSED 66.29.148.24:443`) [32]. The decisive evidence is the citing paper: it "detects abliteration as a **direction-agnostic deviation in activation-geometry fingerprint**", contrasted as detecting "lineage or **structural drift**" [31, §2] — activations, anchored to a claimed identity, corroborated by the publisher's challenge-response IT-PUF sibling work [33]. No collision; risk **LARGE → SMALL-but-open**.

**Saturation met** (queries 6 and 7 returned nothing new), with one honest instrument failure: scholarly mode (OpenAlex/Crossref) returned only biomedical and IoT noise for all three on-lane scholarly queries, so general mode carried the search. Two new works. **arXiv:2602.15195** is weights-only ("this decision is made from weights alone") on Qwen2.5-3B / Llama-3.2-3B-Instruct / Gemma-2-2B — our exact size class — but its object is a LoRA adapter already separated from a frozen base and §4.3 fits a supervised calibration rule [34]; no collision, currently uncited, must be added. **`reverse-abliterate` 0.1.2** is the only *shipped* parent-free abliteration detector found, and it scans for `abliteration_metadata.json`, adapter files, a `-OBLITERATED` suffix, OBLITERATUS commit hashes, shard-size anomalies and forward hooks — **no spectral statistic, no tensor values read** [35]. It is the software form of the string-match baseline our H2 says trivially solves the current positive set. Zero citing papers are indexed for [2], [31] or [34] — absence of evidence, indexing lag sufficient.

**Verdict:** no published work computes a spectral or geometric edit detector from a single full checkpoint without a parent, a sibling, an adapter/base separation, or a labelled calibration set. The narrow claim survives; the broad claim ("nobody inspects an edited checkpoint's spectrum parent-free") does **not**, because of OBLITERATUS, and the paper must say so.

## Sources

[1] [Spectral Geometry of LoRA Adapters Encodes Training Objective and Predicts Harmful Compliance (abstract)](https://arxiv.org/abs/2604.08844) — Confirmed author (Roi Paul), 10 Apr 2026, pre-registration claim, data repo, and every abstract-level number.

[2] [Same paper, full HTML text](https://arxiv.org/html/2604.08844v1) — FULL TEXT READ (§§3-7). Source of the feature formulae, manufacture protocol, AUC 1.00 with 23/11 split, the six pairwise AUCs, rho 0.976/1.000/0.956, cross-method AUC 0.00 (n_bootstrap=972), rho=0.72 on N=24, the 10x/30x feature importances, and the paper's own declaration of the broken-steering confound.

[3] [OBLITERATUS spectral_certification.py (source)](https://huggingface.co/spaces/pliny-the-prompter/obliteratus/raw/main/obliteratus/analysis/spectral_certification.py) — FULL SOURCE READ. Proves the certification consumes ACTIVATIONS not weights, needs no parent, and gives the exact BBP/Marchenko-Pastur thresholds, the sqrt(kappa) heuristic, the rank-1 between-class scatter, and the GREEN/YELLOW/RED criteria with their constants.

[4] [OBLITERATUS repository README](https://github.com/elder-plinius/OBLITERATUS) — FULL README READ. Seven weight-projection presets with direction counts 1/4/8, bias-term projection, multi-direction norm preservation, EGA, sparse surgery, and the ablation strategies. Notably does NOT contain the word 'certification'.

[5] [OBLITERATUS agent-skill docs (Claude Skills Hub mirror)](https://claudeskills.info/skills/nousresearch/hermes-agent/obliteratus/) — Verbatim source of the Common Pitfalls item 12 calibration-failure quote.

[6] [OBLITERATUS agent-skill docs (LobeHub mirror)](https://lobehub.com/skills/dabbler6900-hermes-config-obliteratus) — Independent second host with identical item-12 wording; used to triangulate.

[7] [OBLITERATUS skill docs (Nous Research)](https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-obliteratus) — Third host. Also the nine CLI methods including spectral_cascade = 'DCT frequency-domain decomposition', and the Step-6 operator thresholds.

[8] [OBLITERATUS Space UI (mirror)](https://kicfk-obliteratus.hf.space/) — Snippet-level; confirms the VERIFY stage lists spectral certification and labels it 'BBP Phase Transition - formal completeness guarantee via random matrix theory'.

[9] [GitHub commits API, path-filtered](https://api.github.com/repos/elder-plinius/OBLITERATUS/commits?path=obliteratus/analysis/spectral_certification.py) — Dating: commits 2026-03-04 and 2026-03-08, both bulk uploads; first public appearance 2026-03-04.

[10] [HuggingFace Spaces API](https://huggingface.co/api/spaces/pliny-the-prompter/obliteratus) — Space createdAt 2026-02-13, lastModified 2026-03-16.

[11] [Gabliteration (Guelmez), full HTML](https://arxiv.org/html/2512.18901v3) — Read §§2.1-2.8: SVD on the difference matrix, ridge projector with its error bound, the W <- W - alpha(WP) updates on o_proj and down_proj, the adaptive per-layer scaling, dynamic layer selection with its four stated limitations, and the reduction to Arditi at k=1/alpha=1/lambda=0.

[12] [Comparative Analysis of LLM Abliteration Methods (Young)](https://arxiv.org/abs/2512.13655) — Four tools across sixteen models at 7B-14B, above our ceiling. GSM8K change +1.51 to -18.81 pp; Heretic KL 0.043-1.646. Confirmed it contains NO equation-level taxonomy table.

[13] [A Granular Study of Safety Pretraining under Model Abliteration](https://arxiv.org/abs/2510.02768) — NeurIPS 2025 Lock-LLM workshop; 20 systems over SmolLM2-1.7B Safety-Pretraining checkpoints with multi-judge validation. Behavioural, at our scale.

[14] [Uncensor any LLM with abliteration (Labonne, 2024)](https://huggingface.co/blog/mlabonne/abliteration) — The canonical recipe: last-token difference-of-means over three residual sites, best-direction selection, inference-time vs weight-orthogonalisation forms, and the DPO heal step.

[15] [jim-plus/llm-abliteration (reference MPOA implementation)](https://github.com/jim-plus/llm-abliteration) — FULL README READ. Ablated streams are self_attn.o_proj and mlp.down_proj; --projected, --normpreserve and --invert are independent flags with conventional abliteration as the default.

[16] [mlabonne gemma-3-12b-it-abliterated-v2 card](https://huggingface.co/mlabonne/gemma-3-12b-it-abliterated-v2) — Evidence for the v2 Gaussian depth kernel ('weight factors follow a normal distribution with a certain spread and peak layer') and the hybrid dictionary + Minos-v1 acceptance evaluation.

[17] [Heretic README](https://github.com/p-e-w/heretic) — FULL README READ. Per-component kernel parameters, per-layer first-token difference-of-means, the FLOAT interpolated direction index, and the Optuna/TPE objective co-minimising refusals and KL, with the three-way comparison table.

[18] [p-e-w Qwen3-4B Heretic v1.0.0](https://huggingface.co/p-e-w/Qwen3-4B-Instruct-2507-heretic) — Sub-4.2B candidate: 4,022,468,096 params; direction_index 30.93, attn.o_proj.max_weight 1.49, min_weight 0.92.

[19] [heretic-org Qwen3-4B Heretic v1.2.0](https://huggingface.co/heretic-org/Qwen3-4B-Instruct-2507-heretic) — RECOMMENDED shortlist member: 4,022,468,096 params; attn.o_proj.max_weight 3.22 (>1, i.e. over-subtraction and sign flip), min_weight 0.51.

[20] [0xA50C1A1 Qwen3-4B SOM-MPOA](https://huggingface.co/0xA50C1A1/Qwen3-4B-Instruct-2507-SOM-MPOA) — Sub-4.2B candidate stacking norm preservation with multi-direction: eight per-direction weights max_weights.0 through .7, Heretic v1.2.0.

[21] [Heretic releases](https://github.com/p-e-w/heretic/releases) — Confirms Magnitude-Preserving Orthogonal Ablation was merged into Heretic as PR #52, and the v1.2 quantisation work.

[22] [grimjim HF post (Nov 2025)](https://huggingface.co/posts/grimjim/803126534676334) — PARTIAL FAILURE: the fetch returned only the comment thread and site chrome, not the post body. The MPOA naming evidence therefore comes from the model cards and the ORBA blog instead.

[23] [Norm-Preserving Biprojected Abliteration / MPOA (Lai, 2025)](https://huggingface.co/blog/grimjim/norm-preserving-biprojected-abliteration) — FULL TEXT READ. The exact four-step row-norm-preserving equation, the three stated defects of conventional abliteration, the NatInt/UGI numbers, and the honest note that biprojection brought some refusal back.

[24] [grimjim MPOA reference card](https://huggingface.co/grimjim/Nemo-Instruct-2407-MPOA-v4-12B) — Naming evidence (MPOA = Magnitude-Preserving Orthogonalized Ablation, aka norm-preserving biprojected abliteration) and layer coverage (layers 10-34, down_proj and o_proj).

[25] [ORBA: Orthogonal Reflection Bounded Ablation (Lai, 2026)](https://huggingface.co/blog/grimjim/orthogonal-reflection-bounded-ablation) — FULL TEXT READ. Householder reflector and its rank-1 action, the proof that unit-normalised difference-of-means is exactly the reflector normal, the twice-applied Gram-Schmidt boundary condition (which they note breaks isometry), the geodesic lambda=1 variant that zeroes without reflection, and their negative result that reflection makes misdirected sign-flips the characteristic failure mode.

[26] [ORBA v4 card + API](https://huggingface.co/grimjim/gemma-3-12b-it-orthogonal-reflection-bounded-ablation-v4-12B) — 12,187,325,040 params, ABOVE the 4.2B ceiling; card confirms down_proj and o_proj coverage plus row-wise norm clamping for Frobenius conservation.

[27] [YanLabs Qwen3-4B-Instruct-2507-MPOA](https://huggingface.co/YanLabs/Qwen3-4B-Instruct-2507-MPOA) — THE KEY AVAILABILITY FINDING: 4,022,468,096 params, card states 'using the norm-preserving biprojected abliteration technique'. Refutes the plan's expectation that MPOA has no public sub-4B checkpoint.

[28] [OBLITERATUS/Qwen3-4B-OBLITERATED](https://huggingface.co/OBLITERATUS/Qwen3-4B-OBLITERATED) — 4,022,468,096 params, base Qwen/Qwen3-4B, card states Method = `aggressive` (whitened SVD, 8 directions, 3 refinement passes).

[29] [HuggingFace Hub model search API](https://huggingface.co/api/models?search=orthogonal-reflection-bounded) — ORBA availability census: exactly 7 repos, all gemma-3-12b-it, none <=4.2B. Also the engine behind the 11-term enumeration (325 candidates -> 79 confirmed <=4.2B).

[30] [MuXodious gemma-3n-E2B-it-absolute-heresy-MPOA](https://huggingface.co/MuXodious/gemma-3n-E2B-it-absolute-heresy-MPOA) — TRAP documented: 'E2B' in the name but 5,439,438,272 total params, above the ceiling. Card documents Heretic v1.1.0 merged with the MPOA PR.

[31] [Has This Checkpoint Been Abliterated? A Two-Signal Audit and Its Failure Map](https://arxiv.org/html/2607.01854v1) — THE decisive Coslett characterisation ('direction-agnostic deviation in activation-geometry fingerprint'), the full reference with the Zenodo DOI, the AMS Tier-1-misses/Tier-2-catches finding, the WeightWatch description, and the E1-fires-on-safety-hardening control.

[32] [Safety-Alignment Removal as a Model-Identity Failure (Coslett) - publisher page](https://fallrisk.ai/research/safety-alignment-removal) — UNREACHABLE FROM THIS HOST: two fetch timeouts and connect ECONNREFUSED 66.29.148.24:443. Only search-index snippets obtained, and quoted as snippets.

[33] [Fall Risk AI site / delta-gene research](https://fallrisk.ai/) — Snippet-level corroboration of the identity-anchored framing ('Prove Which Model Is Running - weights identity + API verification + zero-knowledge attestation') and the sibling IT-PUF enrolment protocol.

[34] [Detecting Backdoored LoRAs from Weights Alone](https://arxiv.org/html/2602.15195v3) — Nearest weights-only neighbour after [2]: 'decision is made from weights alone', but the object is a LoRA adapter against a frozen base and §4.3 fits a supervised calibration rule. Base models Qwen2.5-3B, Llama-3.2-3B-Instruct, Gemma-2-2B - our exact size class.

[35] [reverse-abliterate 0.1.2 (PyPI JSON API)](https://pypi.org/pypi/reverse-abliterate/json) — The only shipped parent-free abliteration DETECTOR found: scans metadata files, adapter pairs, the '-OBLITERATED' suffix, OBLITERATUS commit hashes, shard-size anomalies and forward hooks; generates SHA-256 manifests. Contains no spectral statistic and reads no tensor values.

[36] [huihui-ai repository access check](https://huggingface.co/api/models/huihui-ai/Qwen3-1.7B-abliterated) — Reproducibility finding: the repository is now access-restricted and requires authentication. Six of our eight positives come from this uploader.

## Follow-up Questions

- Does huihui-ai's recipe orthogonalise embed_tokens in addition to o_proj and down_proj? Their repositories are now access-gated, but we already hold the tensors: comparing embed_tokens against the instruct parent settles in minutes whether W05's 'residual-write ensemble' covers the same matrices the edit touched.
- Can the gabliterated half-margin be turned into a dose-response? Gabliteration exposes alpha (partial removal), lambda (ridge) and k (rank) explicitly, and we already observe W01 halving relative to the alpha=1/lambda=0/k=1 case — manufacturing a ladder in-house converts the recipe taxonomy from a categorical scope statement into a measured sensitivity curve.
- Does the RED-bias of OBLITERATUS's certification reproduce, and is it the units mismatch? Its leading eigenvalue is an un-normalised between-class mean-difference energy compared against a within-class BBP threshold; if that is the cause, dividing by n should move the verdict distribution — a cheap diagnosis of a community tool that directly parallels our own cutoff-transfer failure.
- Would a per-band W05 (sliding layer windows instead of a global minimum) recover both the band-limited control and the partial-coverage recipes — MPOA's layers 10-34, Gabliteration's selected subset, ORBA's 'several layers'? The prediction table says the layer-minimum is the single fragility shared by four of the eight recipes.

---
*Generated by AI Inventor Pipeline*
