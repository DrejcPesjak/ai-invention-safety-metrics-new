# Cutting the novelty claim to what survives

## Summary

Iteration-5 positioning dossier. Verdict on the windowed object: NOVEL-NARROW, with two three-of-four near-misses newly identified. Ships seven paste-ready paragraphs in both outcome variants, seven positioning corrections with verbatim quotes, a ten-item re-verification log with two MISMATCHes and four UNREACHABLEs, and seventeen numbered wording corrections. Verdict NOVEL-NARROW on the four-qualifier conjunction (parent-free, calibration-free, bottom-of-spectrum, sliding-extremum): no work carries all four; two carry three and BOTH are new to this dossier -- arXiv:2410.17770 (bottom-of-spectrum RMT, parent- and calibration-free, not windowed, not a detector; the largest uncited risk) and EigenTrack 2509.15735 (sliding, but over time across activations). 2607.23711 Intruder Threshold RESOLVED as near-miss (needs sigma_1(BA), reads the top, is a LoRA law not a detector). Two MISMATCHes: 2607.01854's registry is 273 but only 71 processed / 94 evaluated, and the weights-only signal is AUROC 0.90 not 0.84. New obligatory citation: E_1 is the WeightWatch primitive (2508.00161, ICLR 2026). Heretic's triangular-tent kernel and reverse-abliterate's filename-only detection re-confirmed at code level. MP null convention FOUND and nameable; multiple-window FWER convention NONE FOUND (import max-statistic permutation, labelled ANALOGOUS). Ships 7 paste-ready paragraphs in both outcome variants, 7 positioning corrections, 17 numbered wording corrections, a 10-item re-verification log with 4 UNREACHABLEs reported not silently carried, and a 10th recipe class (concept-registry ridge residualization, 2601.08489). research_out.json carries the prose answer plus the full dossier under structured_answer.

## Research Findings

# Cut the Novelty Claim to What Survives

Iteration-5 positioning dossier. All fetches dated 2026-08-14; web tools only. The full machine-readable
deliverable (paste-ready paragraphs, four-qualifier table, re-verification log, corrections) is in the
`structured_answer` field of this file and in `research_report.md`. Every quoted string below is a verbatim
substring of the cited document.

## 1. Verdict on the windowed object: NOVEL-NARROW

The object under test carries four qualifiers simultaneously: parent-free (no base, sibling or attested
reference checkpoint), calibration-free (no threshold fitted on a labelled panel of edited vs clean models),
bottom-of-spectrum (smallest eigenvalues / near-null Gram energy, not top singular values or a heavy-tail
exponent), and sliding-window-with-extremum-scoring (per-window over consecutive layers, scored by an
extremum, not one pooled or band-averaged value). A prior work defeats novelty only by carrying all four.

**No published work carries all four.** Two carry three, along different axes, and both were surfaced by
this dossier -- neither appears in any dependency or in the current draft.

**arXiv:2410.17770, Thamm & Rosenow, "Small Singular Values Matter" [11], is the closest work on the
bottom-of-spectrum qualifier and the largest citation risk in the current positioning.** It is parent-free,
calibration-free and reads the low end: "Surprisingly, we observe pronounced departures from RMT not only
among the largest singular values - the usual outliers - but also among the smallest ones", and "zeroing out
the singular values that deviate from RMT raises language-model perplexity far more than removing values
from the bulk" [11]. It lacks only the sliding window -- plus the application: it asks where information is
stored in pretrained transformers, scores no checkpoint, and carries no edited/clean label. Presenting the
low end of the spectrum as unexamined territory would be refutable from its abstract alone.

**EigenTrack, arXiv:2509.15735 [13], is the closest work on the sliding qualifier**: "EigenTrack computes
covariance spectra over a sliding window of hidden activations and streams the resulting spectral statistics
into a lightweight recurrent classifier" [13]. It is calibration-requiring, top-of-spectrum, and decisively
it slides over *time* across *activations*, requiring input data and a forward pass, where the object under
test slides over *layers* across *weights* and requires neither. The paper must state that distinction
rather than leave it implicit.

The honest reading is that the novelty is one construction step from published work -- slide 2410.17770's
statistic and take an extremum -- not a wide-open gap. Saturation was reached at 26 queries, with the final
six consecutive queries returning zero new relevant items; saturation is claimed on the weights-only
edit-detection lane only, not on the random-matrix-theory literature generally.

### 1a. The most dangerous unadjudicated candidate, resolved

arXiv:2607.23711, "The Intruder Threshold" [8], was flagged in planning as the paper most likely to turn
NOVEL-NARROW into NOT NOVEL, because a planning snippet described it as parent-free and per-layer. It is a
NEAR-MISS, not a defeater, on three independent grounds. It derives "a per-layer critical update strength
s* = theta_bar/(gamma sigma_1(BA)), computed from the measured spectrum of W alone through the rectangular
spiked-deformation transform" [8] -- but the quantity compared against that threshold is sigma_1(BA), the
top singular value of the LoRA update, so evaluating the criterion requires the update matrix and the method
is not parent-free in the operational sense. It reads the top of the spectrum by construction ("the full
edge uses sigma_1 itself") [8]. And it is a law about when LoRA training creates intruder dimensions, not a
detector of a completed edit: its classification target is "intruder-bearing from intruder-free layers" of a
known adapter at "a mean AUC of 0.89" [8], not edited versus clean checkpoints.

### 1b. The other near-misses

PL_Alpha_Hill [9] is ruled out by something stronger than a metric difference: it is designed to be the
quantity that does *not* move when a model is edited. Its own abstract states the signature "captures
intrinsic properties of pretrained models and remains robust during post-training" [9], which is exactly the
wrong property for an edit detector; its lineage use is additionally parent-requiring, comparing layerwise
profiles across models derived from a shared backbone. The Marchenko-Pastur outlier work [10] is parent-free
and per-layer but reads the outliers *above* the MP edge and targets learned structure -- "spectral outliers
encode a dominant component of the learned structure; Q projections carry the most outliers" [10] -- with no
edited/clean label anywhere. The Koopman identifiability paper [14], newly surfaced, is conceptually nearest
to sliding over layers through its depth-as-time framing, but the spectrum "is recoverable from M calibration
samples" [14] of activations, so it is neither weights-only nor calibration-free. reverse-abliterate [7]
computes no statistic of tensor content at all.

## 2. Two MISMATCHes against recorded dependency values

Ten load-bearing quotes were re-fetched. Two came back wrong, and both would have printed in the paper.

**MISMATCH 1 -- the registry size is not the evaluation size.** The two-signal audit's registry is 273
checkpoints, but "of the 273-checkpoint registry we fully processed 71 (those with both a Qwen3Guard label
and detector output)", and "The 57 uncensored among them, plus a separate 37 benign edits, form the
94-checkpoint evaluation set" [1]. Any scale comparison against 273 is misleading; against 94 it is honest.

**MISMATCH 2 -- the weights-only competitor scores 0.90, not 0.84.** The abstract reads "AUROC 0.95,
significantly above either signal alone (0.84, 0.90)" [1], and Table 1 assigns them: activation gap rho 0.84
[.75,.92], weight energy E_1 0.90 [.84,.96], combined z-sum 0.95 [.90,.98], with held-out
leave-one-family-out balanced accuracy 0.89 and FPR 0.11 [1]. Quoting 0.84 as the weights-only number
understates the nearest weights-only rival by 0.06 AUROC and is checkable in a single grep.

**A new obligatory citation was found in the same sentence.** The band-averaging definition credits its own
primitive: E_1 is "the rank-1 energy fraction of the edit, band-averaged; WeightWatch, Zhong & Raghunathan,
2025" [1]. E_1 is therefore the WeightWatch primitive [12], which reads "the top singular vectors of the
weight difference between a fine-tuned model and its base model" and then monitors activation cosine along
them [12] -- parent-requiring and, at monitoring time, prompt-requiring. WeightWatch is an ICLR 2026 paper;
attributing E_1 to the audit alone is an attribution error reviewers are likely to catch.

## 3. Four UNREACHABLE items, reported rather than silently carried

Four dependency-recorded strings did not re-fetch on 2026-08-14. In each case the *conclusion* survives on
re-observed evidence and a substitute is supplied, but the specific string must not be printed as freshly
verified. (i) Abliterlitics' METHODOLOGY code lines are not present in the README served at master; the
parent requirement is instead carried by the setup sentence and schema, which did re-verify [2]. (ii) The
Heretic 23/32-layer fingerprint and (iii) the 0.997-versus-0.00017 direction-cosine pair were not
re-observed; an equivalent sub-4.5B depth/completeness fingerprint was obtained instead from a Qwen3-VL-4B
Heretic report -- 50 to 64 tensors changed across four trials, "The averaged variant spreads its edits across
34 layers, the most of any variant", and "t122's 54 tensors are a strict subset of t174's 62" [23] -- along
with a re-verified statement of the same argument the cosine pair was carrying, that trials "overlap by 96%.
But they disagree on the exact orientation of the refusal direction" [23]. (iv) OBLITERATUS's certify()
signature was not re-fetched from raw source, but the conclusion is corroborated on two mirrors: the hosted
Space describes an "OBLITERATUS prompt set - 512 harmful/harmless pairs across 7 severity tiers. Spectral
Certification (BBP Phase Transition) - Formal completeness guarantee via random matrix theory" [21], and the
Space commit log carries "# knee_cosmic: OBLITERATUS default (knee detection + COSMIC fusion)" [22]. A
512-pair prompt set is what an activation-consuming certifier needs and a weights-only statistic does not.

## 4. The strongest confirmations

**Heretic's kernel, at code level [4].** The source contains, contiguously: "distance = cast(float,
abs(layer_index - params.max_weight_position))", then "# Don't orthogonalize layers that are more than #
min_weight_distance away from max_weight_position. if distance > params.min_weight_distance: continue", then
"# Interpolate linearly between max_weight and min_weight # over min_weight_distance." [4]. That is a
triangular tent with a hard cutoff, not a Gaussian or bell curve: layers beyond the cutoff are skipped
outright rather than down-weighted, which is what produces the partial-depth coverage delta-based forensics
observes. The shipped default is also row-magnitude preserving, "row_normalization = \"full\"" [5].

**reverse-abliterate reads names, not weights [7].** Its own comparison table claims "Abliteration detection
| scans metadata, weights, hooks", but the detection table resolves that to `abliteration_metadata.json`,
LoRA adapter files, "Repo name -OBLITERATED | Standard abliteration naming convention", embedded toolchain
commit hashes, forward-hook registration, and "Weight anomalies | Suspicious shard sizes and filenames" [7].
Its only tensor-level check is a SHA-256 manifest requiring a trusted prior manifest of the same checkpoint
[7]. The filename baseline is therefore the deployed state of the art for unattested uploads, not a strawman
constructed to be beaten.

**Abliterlitics is parent-mandatory [2].** "Create a directory with your base model and variants, plus a
`comparison.json`" [2], with `base` a required top-level key of the schema and no single-checkpoint mode in
the command table; licence re-verified as AGPL-3.0 [2]. Nothing in it is computable from one checkpoint.

**ORBA is two recipes [6].** "At lambda = 1 the refusal component of w is rotated exactly to its orthogonal
complement - zeroed without reflection", whereas the Householder path is "isometric and analytically exact"
and makes "misdirected sign-flips the characteristic failure mode rather than incomplete zeroing" [6].
Annihilation removes rank; a reflection does not. Conflating them makes the isometry falsification vacuous,
because annihilation is the case any rank-sensitive statistic is expected to catch.

**The 2604.08844 precedent is confounded by its own authors [3].** The headline negative is "A binary
classifier trained on DPO-drifted vs. healthy adapters, tested on steering-derived adapters: AUC = 0.00
(nbootstrap = 972, CI [0.00, 0.00])" [3]. But the same paper reports: "H5-asr-steering: Technically passed;
substantively invalid. Language generation collapsed on all steered adapters at all intensities tested. ...
GPT-4o scored 0/300 steered responses as harmful, confirming the output is incoherent." [3]. The checkpoints
on which cross-method transfer failed were not coherent models, and the paper's detector is a fitted
classifier -- "We train l2-regularized logistic regression classifiers with stratified 70/30 train/test
splits" [3]. The two sentences must always be cited together; cross-recipe transfer failure is an open
question, not a settled negative.

## 5. Baseline bias: a published convention exists, so follow it

Our 0.727 filename-regex sensitivity was measured on a pool discovered by name search, with regex terms
overlapping the search vocabulary, so it is an upper bound presented as a baseline. The provenance-testing
literature supplies the exact precedent verbatim: "We collect model candidates for all provenance pairs from
the Hugging Face (HF) platform. To avoid selection bias, we used download counts as our selection criterion,
taking the most popular models subject only to hardware constraints on model size" [15]. The same paper
supplies the reporting shape -- "we create two distinct benchmarks BENCH-A and BENCH-B, that differ in
aspects such as model sizes, choice of pre-trained models, and ground-truth verification procedure" [15] --
and a name-free comparator in our size class: "our tester achieves 90-95% precision and 80-90% recall in
identifying derived models" [15] across 600+ Hugging Face models from 30M to 4B parameters.

The naming literature is deliberately two-edged, and both edges come from one paper, so they must be cited
together [16]. Names carry real signal: "architectural information alone is sufficient to detect these
inconsistencies, achieving an accuracy of 94% in identifying model types" [16], which makes the regex a
serious baseline rather than a convenient one. And names are unreliable: "prior research has shown that
model names are not always well chosen and can sometimes be inaccurate and misleading" [16], which is
precisely the mechanism by which a name-discovered population overstates what a name-based detector achieves
in the wild. The dossier ships a paste-ready reporting convention built on these three quotes: name the
discovery mechanism before any number, stratify and report name-discovered and uploader-discovered pools
separately, and label the name-discovered figure an upper bound in the same sentence.

## 6. The null convention exists; the multiple-window convention does not

For the null itself there is an established, nameable convention, and the paper should adopt it rather than
invent one: Marchenko-Pastur / random-matrix theory as the zero-information hypothesis. "Using Random Matrix
Theory (RMT) as a zero information hypothesis, we associate agreement with RMT as evidence of randomness and
deviations as evidence for learning" [11], applied at both ends of the spectrum -- which is the precedent
that licenses a bottom-of-spectrum null. The same MP split is applied to attention projections and validated
causally by zeroing the identified outliers [10], and EigenTrack uses divergence from an MP baseline on
activation covariances [13]. A random-direction control is the correct complement rather than a substitute:
MP asks whether a window departs from an unstructured matrix, a random direction asks whether the departure
is specific to refusal rather than arbitrary.

For the family-wise error rate across many windows, the finding is negative and should be reported as such.
Twenty-six queries, four aimed squarely at this question, surfaced no convention in the interpretability or
weight-forensics literature for controlling error across a statistic evaluated at every layer or window. The
papers that compute per-layer spectral statistics [8, 9, 10, 11] report or aggregate per-layer values and
none corrects for the number of layers inspected. The mature treatment of this exact shape -- a statistic
evaluated at every element of a large indexed family where the reported result is the extremum -- is
max-statistic permutation inference from neuroimaging [24], which builds the null distribution of the
maximum over the family and controls the whole family with one threshold. It is the right shape for an
extremum-over-windows score, because the calibrated object is the maximum, which is what the detector
reports. It must be labelled ANALOGOUS. Operationally: calibrate the max-over-windows distribution directly
and report a checkpoint-level FPR; an uncorrected per-window rate understates it by roughly the number of
windows.

## 7. Recipe-class coverage and adjacent work

One new recipe class was found that the nine-class taxonomy lacks: concept-registry ridge residualization
[18], which "constructs a registry of independent Concept Atoms representing protected capabilities and
stylistic confounds, then uses ridge-regularized spectral residualization to orthogonalize the refusal
vector against these directions" [18], reporting 0-2% refusal at first-token KL 0.044 where standard ablation
on Qwen3-VL-4B gives KL 2.088 [18]. It is distinct from plain ridge rank-k because the residualization
target is a curated concept set rather than a regularizer, and its public checkpoints sit on the Qwen3-VL-4B
family -- our own scale. Three further works were classified and are not detectors: a four-tool comparison
across sixteen 7B-14B models reporting GSM8K change from +1.51 pp to -18.81 pp and KL divergence 0.043-1.646
[17]; a generation-only granular study of safety pretraining under abliteration whose useful contribution is
that judge selection changes evaluation outcomes [19]; and an off-target-effects study whose provenance
audit "caught two independent contamination channels - a mismatched-quantizer pilot pair and a stale
community chat template that silently mangled the rendered prompt" [20], direct external support for
treating toolchain artifacts as the rule in community-checkpoint studies.

## 8. What is delivered

Seven paste-ready paragraphs written as final prose, including the novelty claim in both outcome variants --
P-D assumes the windowed arm recovers the discovery failures and earns the fourth qualifier, P-E assumes it
does not, claims three qualifiers, demotes the windowed statistic to a labelled proposal, and converts the
section into a boundary result written with equal conviction. Style constraints enforced and self-checked:
no backward references to earlier drafts, "novel" and "first" once each and only inside the four-qualifier
sentence, concession before claim. Also: seven positioning corrections with quotes and anchors (five
specified, two added because they surfaced here -- the WeightWatch attribution and the 2410.17770
bottom-of-spectrum citation), seventeen numbered wording corrections of which five are new, a ten-item
re-verification log, and a twenty-one-row source ledger with access status.

## 9. Confidence and what would change it

Confidence is **high** on the four-qualifier verdict, on both MISMATCHes, and on the Heretic and
reverse-abliterate corrections: all rest on verbatim primary text re-fetched on 2026-08-14 [1, 4, 5, 7].
Confidence is **moderate** on saturation -- 26 queries is a lane sweep, not a proof, and three genuinely
relevant works [11, 12, 14] surfaced late in it, which is itself evidence the lane was less well-mapped
going in than the dependencies suggested. Confidence is **low-to-moderate** on the four UNREACHABLE items,
which is why they are flagged rather than carried. The verdict would flip to NOT NOVEL on discovery of a
single work computing a bottom-of-spectrum statistic on a sliding window of consecutive layers from one
checkpoint's own weights with no reference and no fitted threshold; [11] is one construction step from that.
It would also drop to a three-qualifier claim if the windowed arm fails to recover the discovery failures,
which is an experimental outcome, not a literature question. Finally, the measured figures used inside the
paste-ready paragraphs P-B and P-F -- 0.727, 0.159, 4.1e-5 and 7.3e-5 -- come from this project's own
experiments, are reproduced as the drafter supplied them, and were **not** independently checked here.


## Sources

[1] [Has This Checkpoint Been Abliterated? A Two-Signal Audit and Its Failure Map (Hurtado, 2026)](https://arxiv.org/pdf/2607.01854) — Supplied the verbatim band-averaged E_1 definition, the WeightWatch attribution, the registry/evaluation-set split (273 registry, 71 processed, 94 evaluated) and the corrected AUROC triple 0.95/0.90/0.84.

[2] [Abliterlitics README (dreamfast)](https://raw.githubusercontent.com/dreamfast/abliterlitics/master/README.md) — Re-verified the mandatory `base` key, the setup sentence, the comparison.json schema and the AGPL-3.0 licence; the METHODOLOGY code lines were not present at this URL on this date.

[3] [Weight-space drift fingerprinting of fine-tuned adapters (Paul, 2026)](https://arxiv.org/pdf/2604.08844) — Supplied both halves of correction C1 verbatim: the AUC 0.00 / n_bootstrap 972 sentence and the declared confound (generation collapse; GPT-4o scored 0/300).

[4] [Heretic source, ablation-weight loop](https://raw.githubusercontent.com/p-e-w/heretic/master/src/heretic/model.py) — Code-level confirmation that the kernel is a triangular tent with a hard cutoff: the distance computation, the `if distance > params.min_weight_distance: continue` skip, and the linear interpolation.

[5] [Heretic default configuration](https://raw.githubusercontent.com/p-e-w/heretic/master/config.default.toml) — Confirmed the shipped default row_normalization = "full", i.e. row-magnitude preserving by default.

[6] [Orthogonal Reflection Bounded Ablation (Lai, 2026-03-24)](https://huggingface.co/blog/grimjim/orthogonal-reflection-bounded-ablation) — Supplied the two-recipe distinction (geodesic lambda=1 zeroed without reflection versus the Householder isometry) and the author's own misdirected-sign-flips negative.

[7] [reverse-abliterate package metadata (Carlos-Projects, MIT)](https://pypi.org/pypi/reverse-abliterate/json) — Supplied the full detection table showing filename/metadata/hook checks only, with SHA-256 manifests as the sole tensor-level check; establishes the name baseline as a shipped tool.

[8] [The Intruder Threshold: A Spectral Law for LoRA Fine-Tuning (Xie, 2026)](https://arxiv.org/pdf/2607.23711) — The dossier's most dangerous unadjudicated near-miss, resolved: parent-spectrum-derived but update-requiring via sigma_1(BA), top-of-spectrum, per-layer not sliding, and a law about LoRA dynamics rather than an edit detector.

[9] [Spectral Signatures of Large Language Models (Zhang et al., KDD 2026)](https://arxiv.org/pdf/2607.03377) — Confirmed PL_Alpha_Hill is a heavy-tail top-of-spectrum exponent explicitly designed to remain robust during post-training - a stronger ruling-out than metric difference.

[10] [Spectral Outliers Reveal Dominant Learned Structure in Transformer Attention (Dewage et al., ICMLA 2026)](https://arxiv.org/abs/2608.07921) — Confirmed the MP bulk/outlier split reads outliers above the edge and targets learned structure in pretrained models, with no edited/clean labels anywhere.

[11] [Small Singular Values Matter: A Random Matrix Analysis of Transformer Models (Thamm & Rosenow)](https://arxiv.org/pdf/2410.17770) — NEWLY SURFACED and absent from every dependency. The closest prior art on the bottom-of-spectrum qualifier - parent-free, calibration-free, reads the smallest singular values against an RMT null - and the source of the null convention the paper should adopt by name.

[12] [Watch the Weights: Unsupervised monitoring and control of fine-tuned LLMs (Zhong & Raghunathan, ICLR 2026)](https://arxiv.org/abs/2508.00161) — NEWLY SURFACED. The WeightWatch primitive that E_1 is credited to; top singular vectors of the weight difference plus activation-cosine monitoring, so parent-requiring and prompt-requiring. An obligatory citation the dependencies lacked.

[13] [EigenTrack: Spectral Activation Feature Tracking (Ettori et al.)](https://arxiv.org/pdf/2509.15735) — Supplied the sliding-window sentence verbatim; the closest published use of the sliding half of the claim, over time across activations rather than over layers across weights.

[14] [Intrinsic Structure: Spectral Identifiability for Mechanistic Interpretability (Dhor & Chen, 2026)](https://arxiv.org/abs/2608.10172) — NEWLY SURFACED. Koopman spectrum with depth as time - conceptually nearest to sliding over layers - but recovered from M calibration samples of activations, so neither weights-only nor calibration-free.

[15] [Model Provenance Testing for Large Language Models](https://arxiv.org/pdf/2502.00706) — The direct precedent for naming a hub-harvest selection criterion to avoid selection bias, for reporting two differently-constructed populations, and a name-free provenance comparator at 80-90% recall on 600+ models of 30M-4B parameters.

[16] [Naming Practices of Pre-Trained Models on Hugging Face (Jiang et al.)](https://arxiv.org/pdf/2310.01642) — The two-edged naming citation: DARA identifies model types from names at 94% accuracy, and the same paper documents that names are often inaccurate and misleading.

[17] [Comparative Analysis of LLM Abliteration Methods (Young)](https://arxiv.org/abs/2512.13655) — Classified STUDY: tool comparison with capability and KL metrics, no weights-only detector.

[18] [Surgical Refusal Ablation: Concept-Guided Spectral Cleaning (Cristofano, 2026)](https://arxiv.org/abs/2601.08489) — Classified RECIPE and flagged as a tenth recipe class - concept-registry ridge residualization - with public checkpoints on the Qwen3-VL-4B family.

[19] [A Granular Study of Safety Pretraining under Model Abliteration (Agnihotri et al., NeurIPS 2025 workshop)](https://arxiv.org/abs/2510.02768) — Classified STUDY: generation-based only; its judge-sensitivity result supports treating behavioural labels as noisy.

[20] [Abliteration Is Not a Scalpel (Fafula, 2026)](https://arxiv.org/abs/2607.17427) — NEWLY SURFACED, classified STUDY. Supplies external support that abliterated checkpoints differ from base on refusal-free tasks, and that toolchain contamination is the rule in community-checkpoint studies.

[21] [OBLITERATUS hosted Space](https://kicfk-obliteratus.hf.space/) — Corroborated that certification consumes a 512-pair harmful/harmless prompt set via a BBP phase-transition test, i.e. activations rather than weights.

[22] [OBLITERATUS spectral_certification.py commit](https://huggingface.co/spaces/pliny-the-prompter/obliteratus/commit/f0084ba4c8de46caf272ebe02a6ef925277bc743) — Confirmed the COSMIC-fused knee detection default verbatim, establishing layer-selectivity.

[23] [Qwen3-VL-4B Heretic abliteration report](https://nathan.sapwell.net/posts/qwen3-vl-4b-heretic/) — A re-observed sub-4.5B depth/completeness fingerprint (50-64 tensors changed, 34 layers for the averaged variant, strict-subset structure) usable in place of the unverified 23/32 figure.

[24] [Permutation inference for the general linear model (Winkler et al., NeuroImage 2014)](https://doi.org/10.1016/j.neuroimage.2014.01.060) — The ANALOGOUS convention imported for the multiple-window family-wise error problem: calibrate the null distribution of the maximum statistic over the family.

## Follow-up Questions

- Does arXiv:2410.17770's bottom-of-spectrum RMT deviation move under abliteration at all? It is the one near-miss that is a single construction step away from the claim, so running its exact statistic - deviation of the smallest singular values from the Marchenko-Pastur null, per matrix, no window - as a baseline on our panel would either establish that the sliding window is what buys the separation or reveal that an already-published statistic does the job, which changes the verdict from NOVEL-NARROW to an application claim.
- What is the checkpoint-level false-positive rate of an extremum-over-windows score once the maximum is calibrated directly, and how much higher is it than the per-window rate? No in-field convention exists, so this number has to be measured rather than cited, and it determines whether the windowed arm can be claimed at all.
- Does the concept-registry ridge residualization class (arXiv:2601.08489) fall inside or outside the analytic boundary? It is rank-reducing rather than isometric, so it should be detectable, but its whole design goal is to minimize spectral disruption to capability subspaces - which is precisely the property that would make a low-energy edit hard to see from the bottom of the spectrum.

---
*Generated by AI Inventor Pipeline*
