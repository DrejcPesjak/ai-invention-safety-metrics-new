# review_paper — test_idea

> Phase: `invention_loop` · round 3 · `review_paper`
> Run: `iter1_33370088803c` — Catching Edited Safety Models by Reading Weights in Sliding Windows
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `review_paper` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-13 23:35:06 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An adversarial paper reviewer (Step 3.5: REVIEW_PAPER in the invention loop)

You received a paper draft written by a DIFFERENT model. Review it with fresh eyes.
Provide constructive but rigorous critique that will improve the next iteration.

Specific critiques → better paper. Vague praise → no improvement.
</your_role>
</ai_inventor_context>

ROLE: You are a very experienced and critical conference reviewer.
Your expertise spans the domain of the paper under review.
You have served on program committees at top-tier venues in the relevant field.

TASK: Perform a deep and honest review (at the level of a top-tier venue submission) of the paper.

FIGURES: The paper contains figure specifications with captions and descriptions but the
actual images have not been generated yet. Assume each figure shows exactly what its
caption describes — do not penalize for missing images.

ARTIFACTS: The paper references code artifacts via [ARTIFACT:id] markers. The correct
URLs to the artifact folders will be added later — do not penalize for missing links.

GOAL: Your review feeds directly back to the paper author. The objective is to maximize
the overall review score in subsequent rounds. Every piece of feedback you give should
be written with this goal in mind — prioritize the critiques and suggestions that would
produce the largest score improvement if addressed. Don't waste the author's iteration
budget on low-impact polish when there are score-blocking issues to fix.

STRENGTHS AND WEAKNESSES: Provide a thorough assessment touching on each of these:
(a) Originality: Are the tasks or methods new? Novel combination of known techniques?
    Clear differentiation from prior work? Is related work adequately cited?
(b) Quality: Is the submission technically sound? Are claims well supported by theoretical
    analysis or experimental results? Is the methodology appropriate? Is this a complete
    piece of work? Are the authors honest about limitations?
(c) Clarity: Is the submission clearly written and well organized? Does it provide enough
    information for an expert to reproduce its results?
(d) Significance: Are the results important? Would others build on them? Does it address
    a meaningful problem better than prior work? Does it advance the state of the art?

SUPPLEMENTARY SCORES: Rate each on a 1-4 scale.
Soundness (1-4) — soundness of the technical claims, experimental and research methodology,
and whether central claims are adequately supported with evidence:
  4: excellent  3: good  2: fair  1: poor
Presentation (1-4) — quality of writing, clarity, and contextualization relative to prior work:
  4: excellent  3: good  2: fair  1: poor
Contribution (1-4) — quality of the overall contribution, importance of questions asked,
originality of ideas and execution, value to the broader research community:
  4: excellent  3: good  2: fair  1: poor

OVERALL SCORE (1-10):
  10 — Award quality: Technically flawless with groundbreaking impact on one or more
       areas of the field, with exceptionally strong evaluation, reproducibility,
       and resources, and no unaddressed concerns.
   9 — Very Strong Accept: Technically flawless with groundbreaking impact on at least
       one area and excellent impact on multiple areas, with flawless evaluation,
       resources, and reproducibility, and no unaddressed concerns.
   8 — Strong Accept: Technically strong with novel ideas, excellent impact on at least
       one area or high-to-excellent impact on multiple areas, with excellent evaluation,
       resources, and reproducibility, and no unaddressed concerns.
   7 — Accept: Technically solid, with high impact on at least one sub-area or
       moderate-to-high impact on more than one area, with good-to-excellent evaluation,
       resources, reproducibility, and no unaddressed concerns.
   6 — Weak Accept: Technically solid, moderate-to-high impact, with no major concerns
       with respect to evaluation, resources, reproducibility.
   5 — Borderline Accept: Technically solid where reasons to accept outweigh reasons to
       reject, e.g., limited evaluation. Use sparingly.
   4 — Borderline Reject: Technically solid where reasons to reject, e.g., limited
       evaluation, outweigh reasons to accept. Use sparingly.
   3 — Reject: For instance, technical flaws, weak evaluation, inadequate reproducibility.
   2 — Strong Reject: For instance, major technical flaws, poor evaluation, limited
       impact, poor reproducibility.
   1 — Very Strong Reject: For instance, trivial results or unaddressed concerns.

CONFIDENCE (1-5):
  5: Absolutely certain. Very familiar with related work, checked details carefully.
  4: Confident but not absolutely certain. Unlikely you misunderstood something.
  3: Fairly confident. Possible you missed some related work or details.
  2: Willing to defend your assessment, but quite likely missed central aspects.
  1: Educated guess. Not in your area or difficult to evaluate.

For each dimension, provide a list of specific improvements:
- WHAT needs to change
- HOW to change it (concrete enough for the author to act on immediately)
- EXPECTED SCORE IMPACT: how much would fixing this raise the overall score?

REVIEW PRINCIPLES:
- Be specific and actionable — vague critique is useless
- Ground your review in evidence — search for existing work, accepted papers, known results
- Rank critiques by score impact — address the biggest score blockers first
- Distinguish major issues (would cause rejection) from minor issues (polish)
- Acknowledge genuine strengths — don't be negative for its own sake
- Compare against the bar set by accepted papers at top-tier venues
- Check if figures are well-specified and would effectively communicate the results
- Verify that claims are supported by the artifacts described
- Screen for unattributed reuse. Search the web for the paper's distinctive phrasings, its central claim, and any method name it coins. If wording, a derivation, or a result appears in prior work, say so and name the source. Treat close paraphrase of a source's argument without citation the same as verbatim reuse
- Check that any prior work the paper builds on is cited at the point it is used, not only in a related-work list. An uncited source that the work depends on is a major issue, not a presentation nit
- Check the cited sources exist and say what they are claimed to say. Flag any reference you cannot verify, and any retracted or predatory-venue source

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape. Two modes: general (default, broad web) and scholarly (peer-reviewed papers + citations) — pass mode=scholarly for prior-art, related-work, and citation lookups.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<role>
You are a very experienced and critical conference reviewer specialized in the domain of the work under review.
You have reviewed for top-tier venues in the relevant field. Your reviews are known for
being thorough, fair, and grounded in the actual state of the field.
</role>

<paper>
# Introduction

An open-weight checkpoint arrives with no provenance. Deciding whether its safety training is intact currently costs a benchmark run: hundreds of harmful prompts from AdvBench [30], JailbreakBench [31] or HarmBench [32], a judge model to score the generations [35], and a repeat for every attack template of interest. The evaluator must hold and transmit harmful content, must pay for a judge, and must trust that the checkpoint was not tuned to refuse exactly the items it will be shown. At the scale of a model hub the unit of cost is wrong: our own harvest of 61 Hub sweeps over 20,313 enumerated repositories found 513 self-declared edited checkpoints from **189 distinct uploaders** below 4.2B parameters alone [ARTIFACT:art_8OlSrcw-hzgO].

The published cheap alternatives each retain a dependency the situation does not grant. AMS [3] reads activation geometry but needs harmful prompts and reports that behavioural uncensored fine-tunes are undetectable by it. RAS/SafeVec [4] needs unsafe prompts, jailbreak prompts *and* a safety-aligned reference model. VISAGE [5] evaluates a harmful benchmark at every weight perturbation. The two closest weight-space results both require the parent: the abliteration audit of [2], whose weight statistic is $E_1 = \mathrm{mean}_m\,\sigma_1^2(\Delta W_m)/\sum_i \sigma_i^2(\Delta W_m)$ with $\Delta W = W_{\text{base}} - W_{\text{cand}}$, and the spectral-geometry study of LoRA adapters [8], which reaches AUC 1.00 for binary drift detection from per-layer spectral features of a weight *delta*. A random Hugging Face repository does not come with an attested parent.

This paper adopts a hard operating constraint and reports exactly what survives it: **the metric sees one checkpoint's tensors**. No sibling, no base to diff against, no reference model, no prompt, no forward pass. The previous iteration of this work reported that under that constraint one statistic separates abliterated checkpoints from everything else at AUROC 1.000 over 44 checkpoints. This iteration was written to find out whether that number means what it appears to mean, and the answer is that it does not — not because the signal is spurious, but because *abliteration* names a family of at least eight mechanically distinct recipes and eight positives from two uploaders sample one corner of it.

[FIGURE:fig1]

Four measurements decide the paper. **First, the scar is real, and it is extremely specific in the wild.** On 160 sub-4B Hub checkpoints that declare no edit, scored from stored tensors only — zero prompts, zero forward passes, a median of 7.0 s of CPU linear algebra each — the statistic returns **zero** hits inside the abliterated region, a false-positive rate of 0/160 (Wilson 95% $[0, 0.023]$), while flagging 8 of 8 known-abliterated positive controls and 0 of 12 known-clean negative controls through the identical code path [ARTIFACT:art_gCgia-6VUZJb]. **Second, the parent-free constraint costs nothing on the recipe it was characterised on and everything off it.** On 12 pre-declared instruct/abliterated sibling pairs, the parent-free statistic and the parent-requiring $E_1$ tie at AUROC 1.000, paired difference $+0.000$; on four real published abliterated checkpoints at $\leq$4.2B from four uploaders the detector had never seen, it collapses to AUROC 0.382 and catches 0 of 4 at the fitted threshold, while $E_1$ — which has the parent — sees 3 of 3 of the pairs it can form, all confirmed genuine near-rank-one edits [ARTIFACT:art_fvWfzRrcoKux]. **Third, the flag dies before the un-censoring does.** In a 34-stage laundering ladder on an in-house abliteration of Qwen3-1.7B, the cheapest successful evasion is not an attack: a plain **int4 round-trip** erases the flag ($W05: -4.59 \to -1.95$) at a harmful-refusal rate of 0.135, *below* the unlaundered root's own 0.162, inside the fluency screen [ARTIFACT:art_gCgia-6VUZJb]. **Fourth, the scar and the un-censoring are dissociable at construction time**: a projection confined to the middle 50% of layers drives harmful refusal from 0.45 to 0.00 — exactly as effective as the full-stack edit — while the statistic moves from $-1.0098$ to $-1.0088$, indistinguishable from the unedited model.

The honest product of those four is not "a detector for abliteration" but something narrower, cheaper and still useful: **a free, prompt-free certificate that a checkpoint carries an unlaundered global directional edit**, with a fully measured scope boundary on all four axes that matter (recipe, uploader, layer support, post-processing). We report the boundary as a first-class result rather than a limitation, because a hub-scale screen whose failure modes are unmeasured is worse than useless.

A second, independent contribution is negative and is now quantitative rather than merely stated. For *graded* safety behaviour — how often a model actually refuses harmful requests — no interior observable in a frozen 53-metric battery beats a trivial black-box baseline. The previous draft reported that as a fired falsifier; a dedicated re-analysis artifact recomputed every number in it and found that the design's **minimum detectable paired difference is $|\Delta\rho| = 0.32$ at $n = 19$ lineages**, that roughly 150 lineages would be needed to resolve an advantage of 0.20, and that the named baseline was *not even the best black-box metric* — first-token entropy asymmetry beats it at $|\rho| = 0.782$ against 0.668 [ARTIFACT:art_0T8jhUa0zxmu]. The negative therefore stands in a bounded form, and we state the bound.

## Summary of Contributions

- **A parent-free, prompt-free weight statistic for global directional refusal ablation, with its scope measured on four axes** (§4.1, §5.1). $W05$ separates 8 abliterated from 36 non-abliterated archived checkpoints at oriented AUROC 1.000 (raw AUROC 0.000: abliterated members sit at the *low* end, and we report the orientation because it was read off the data). It generalises to norm-preserving and rank-$k$ synthetic variants (AUROC 1.000) and fails on per-head surgery (0.556), on layer-band edits (undetectable at any fraction below 1.00), and — the sharpest finding — on the *same* global recipe from four unseen uploaders (0.382, catch rate 0/4).
- **A deployment test rather than a benchmark: 160 undeclared Hub checkpoints scanned from stored tensors** (§5.2). Zero false positives, Wilson 95% $[0, 0.023]$, 8/8 and 12/12 controls, at a median 7.0 s CPU per checkpoint. Two warning-band repositories are named and adjudicated against their cards.
- **A laundering ladder that finds the flag is cheaply evadable, and says so** (§5.2). Four of six real intensity axes kill the flag before the un-censoring, the cheapest at an evasion cost of $-0.004$ in harmful refusal. Two pre-registered predictions reverse: a one-matrix argmin patch does **not** defeat a minimum-over-layers statistic, and 200 steps of benign LoRA-SFT do not scrub it (it *restores* refusal 0.162 $\to$ 0.368 while moving $W05$ only $-4.592 \to -4.381$).
- **The parent-required head-to-head the reviewer asked for** (§5.3). $E_1$ computed on every sibling pair in the panel: a tie at AUROC 1.000 on the 12 pre-declared pairs, $-0.167$ $[-0.444, 0.000]$ on 15 pairs including new uploaders, and complementary failure modes — $E_1$ degrades on multi-direction edits (0.17–0.67) where $W05$ is perfect, and holds at 0.995 on the band edits $W05$ cannot see.
- **The behavioural negative, made quantitative** (§5.4). Minimum detectable $|\Delta\rho| = 0.32$ at 19 lineages; the falsifier *could* have failed; a pre-specified comparator (B01 logit gap) reported alongside the post-hoc winner with its selection optimism priced at $+0.182$; split-half reliability $r_{xx} = 0.968$, so the attenuation correction is a factor of 1.016 and the negative is not an attenuation artifact; and the conclusion invariant across three depths spanning a 22-layer AUROC plateau.
- **A measurement-discipline audit of our own claims** (§5.5). Four values the previous draft presented as correlations were paired differences on a different subset; the frozen `metric_spec.py` stamps the 53 metric declarations **and nothing else**, so 6 of 12 "pre-registered" claims are downgraded to analysis-time conventions, with the mapping table published.

# Related Work

**Parent-required weight audits, and the exact hole we occupy.** WeightWatch [9] shows that the top singular vectors of a fine-tuned-minus-base weight difference correspond to newly acquired behaviours. The abliteration audit of [2] specialises this, combining an activation signal with the weight-recovery energy $E_1$ over $o\_proj$ and $down\_proj$ in a mid-stack band, over a 273-checkpoint registry. Closest of all, and uncited in our previous draft, is Paul's pre-registered spectral-geometry study of LoRA adapters [8]: 38 manufactured adapters on Llama-3.2-3B-Instruct, per-layer spectral features extracted from weight deltas, binary drift AUC 1.00 with CI $[1.00, 1.00]$, all six pairwise training-objective comparisons at AUC 1.00, ordinal severity $\rho \geq 0.956$ (the minimum of 0.976 / 1.000 / 0.956) and Spearman $\rho = 0.72$ on $N = 24$ against HEx-PHI harmful compliance, with no CI reported. Two of its five features — stable rank $\lVert \Delta W\rVert_F^2/\sigma_1^2$ and singular-value entropy $H = -\sum \hat\sigma_i \log \hat\sigma_i$ with $\hat\sigma_i = \sigma_i/\sum_j\sigma_j$ — are formula-identical to our $W06$–$W09$, and we cite it at the point of use in §4.1. We differ on three axes and each is load-bearing: it needs the parent (its single most informative feature is a cosine to a *healthy-adapter centroid*, requiring both a parent and a reference population), it is evaluated on manufactured adapters with a controlled 50–2000-step dose ladder rather than on real community checkpoints, and it predicts behaviour where we detect an edit. Its $\rho = 0.72$ is a direct counterweight to any universal claim that weight geometry carries no behavioural signal, and we do not make that claim: the paper itself notes the correlation "primarily reflects which side of the boundary" (healthy cluster at drift probability 0.001, DPO at 0.999), i.e. a two-class separation between groups that differ by a manufacturing operation. Our behaviourally-uncensored members were made by ordinary SFT with no directional edit, so there is no low-rank scar for either method to find.

Paul's study also supplies the strongest published precedent for this paper's central scope finding: a classifier trained on DPO-drifted adapters and tested on steering-derived ones scores **AUC 0.00** ($n_{\text{bootstrap}} = 972$, CI $[0.00, 0.00]$) — every out-of-method adapter ranked healthier than every in-method one. That precedent must be carried with its own declared confound: the steering arm generated incoherent text at every intensity (GPT-4o scored 0 of 300 responses harmful), so the paper says the geometric opposition "may reflect a broken injection method". The analogy is also inverted relative to ours — their classifier was trained on gradient edits and failed on an algebraic one; ours is built for the algebraic edit. Finally, [10] detects backdoored LoRAs "from weights alone" on Qwen2.5-3B, Llama-3.2-3B-Instruct and Gemma-2-2B, our exact size class, but its object is an adapter already separated from a frozen base and §4.3 fits a supervised calibration rule on labelled adapters.

**Parent-free spectral inspection is already community practice, and we say so.** The OBLITERATUS toolkit [11] ships a *spectral certification* step that decides whether a directional edit is complete. Reading its source settles a question our plan got backwards: it consumes **activations**, not weights — `certify(harmful_activations, harmless_activations, layer_idx)` forms a between-class mean difference, estimates a noise floor from the pooled within-class covariance by a median-eigenvalue/Marchenko-Pastur method, and thresholds the eigenvalues of the rank-1 outer product against a BBP bound inflated by $\sqrt{\kappa}$. It is therefore parent-free but not prompt-free or forward-pass-free, and it audits an edit the operator has just performed rather than deciding whether an unknown checkpoint was edited. Its documentation records, verbatim and identically across three mirrors, that "spectral certification RED is common — the spectral check often flags 'incomplete' even when practical refusal rate is 0%", which is an independent, anecdotal mirror of our own finding that the ranking transfers while the calibration does not. Its first public commit predates this work. The correctly scoped novelty claim is therefore not "nobody inspects an edited checkpoint's spectrum parent-free" but: *the weights-only, prompt-free, forward-pass-free form of that question, measured rather than asserted, with held-out lineages, leave-one-uploader-out, an injected positive control, a quantified calibration failure and a measured recipe-class boundary* [ARTIFACT:art_sHF0cggp2IvT]. Separately, the only *shipped* parent-free abliteration detector we could find, `reverse-abliterate` 0.1.2 [12], scans for `abliteration_metadata.json`, adapter-config pairs, repository-name suffixes and toolkit commit hashes: it reads no tensor values. It is the software instantiation of the string-match baseline our own data quantifies at 50.5% (259 of 513 self-declared edited repositories carry "abliterat" in the repository id) [ARTIFACT:art_8OlSrcw-hzgO].

**The recipe family.** Abliteration is not one operation. The taxonomy we assembled has eight members with reimplementation-grade update equations [ARTIFACT:art_sHF0cggp2IvT]: the global all-layer rank-one projection $W \leftarrow (I - \hat r\hat r^\top)W$ [1, 13]; mlabonne's v2 Gaussian depth kernel $W_\ell \leftarrow W_\ell - w_\ell (W_\ell \hat r)\hat r^\top$ [13]; Heretic's per-component optimised kernel with a float-interpolated direction index and published weights as high as 3.22, i.e. over-subtraction and a sign flip rather than annihilation [14]; MPOA's exact four-step row-norm-preserving update [15]; ORBA's Householder reflection $H = I - 2uu^\top$ with a geodesic $\lambda = 1$ variant [16]; Gabliteration's ridge-regularised rank-$k$ update $W \leftarrow W - \alpha_\ell(WP)$ with $P = R(R^\top R + \lambda I_k)^{-1}R^\top$ [17]; OBLITERATUS's rank-$k$ presets [11]; and behavioural SFT, which has no closed form. A cross-architecture comparison of these methods exists [18] but evaluates at 7B–14B, above our ceiling. One consequence lands directly on our previous headline: one of our eight archived positives is a *Gabliteration*, not a plain projection, and it scores at roughly half the margin ($W01 = 2.237$, $W05 = -3.522$ against the huihui range $W01$ 4.16–4.82, $W05$ $-4.21$ to $-4.82$). The recipe question was already half-answered inside our own positive set, as graded margin loss rather than collapse.

**Why a weight-space scar is expected at all.** Safety fine-tuning has been shown to minimally transform MLP weights so as to align unsafe inputs into a null space [19], and safety behaviour localises to a small set of neurons and ranks that can be pruned or low-rank-modified away [20]. Abliteration is the extreme case: an explicit rank-one projection applied to every residual-write matrix [1]. Heavy-tailed self-regularisation supplies mature spectral descriptors for trained weight matrices [21]. Community practice complicates the picture in ways we measure rather than assume: extended-refusal training defends against abliteration while leaving weights superficially normal [22], and abliteration has substantial off-target effects on behaviours that elicit no refusals [23].

**Detection is not control.** Galeone et al. [7] establish the general dissociation: a linear detector reaching AUC $=1.000$ from layer 5 sits at $\cos = 0.12$ (about 83°) from the direction that actually produces the behaviour, essentially unchanged by instruction tuning. Their Section 8 is an explicit negative — the detector-to-intervention cosine sits at chance for steerable and unsteerable behaviours alike — so a cosine-as-safety-score metric is a published negative, and we enter one only as a declared control. Our §5.5 reports the same dissociation in a new place: two refusal directions indistinguishable on held-out AUROC (11 layers $\geq 0.997$, four tied at exactly 1.000) differ twofold in how much they actually un-censor.

**Steering strength, and what we retired.** Logit-Gap Steering [24] takes the first-step gap between refusal and affirmative logits as a forward-pass diagnostic on our exact size class, and is the pre-specified black-box comparator in §5.4. The Rogue Scalpel [25] shows random steering directions raise harmful compliance from 0% to 1–13%, which converts a random direction from a null into a magnitude-matched comparator. Three further results bound what a scalar steering measurement can mean: steering strength acts non-monotonically on next-token probability [26], the optimal steering layer is input-dependent [27], and scalar steerability measures conceal behavioural shifts in open-ended generation [28]. Our own $\alpha_{50}$ steering-price metric was measured at 60,040 generations in the previous iteration and refuted as a triage score; it survives in this paper only as a battery member and as the methodological finding of §5.5 about refusal-substring screens.

**Ground truth.** Hasan and Biswas [29] report over-refusal and harmful compliance nearly uncorrelated across 21 open-weight models, which is why we predict two axes separately. Basu et al. [6] give the reason a read-side metric can be confidently wrong: 98.2% probe AUROC alongside 45.1% output sensitivity.

# Panel, Ground Truth and the Analysis Contract

**Panels.** Three panels are used and never mixed. (P1) The **archived battery panel**: 44 checkpoints at $\leq 4.2$B over 23 weight lineages and 7 architecture families (qwen3, qwen2, llama, gemma2, gpt\_neox, granite, olmo), comprising 16 base, 15 instruct, 8 abliterated, 4 behaviourally-uncensored and the official Qwen3-4B-SafeRL checkpoint, with a lineage-level held-out split whose seed and fraction were stamped before any model was loaded. (P2) The **scope panel**: four real published abliterated/decensored checkpoints at $\leq 4.2$B from four uploaders absent from P1, plus 12 in-house synthetic recipe variants on two architectures, plus a layer-fraction sweep, plus 15 matched parent/child pairs for the $E_1$ head-to-head. (P3) The **wild panel**: 250 attempted / 160 successfully scored sub-4B Hub checkpoints that declare no edit, drawn by descending downloads from a 2,139-row metadata pool with declared, undeclared-chat and undeclared-base strata [ARTIFACT:art_8OlSrcw-hzgO]. Every model-level statistic resamples weight lineages, not checkpoints.

**External safety ground truth barely exists at this scale, and we measured that rather than assuming it.** A dedicated harvest found external safety coverage for 3 of 66 candidate checkpoints and 2 of 34 lineages; twelve published safety sources — SORRY-Bench [36], OR-Bench, XSTest [33], TrustLLM [39], SALAD-Bench [38], DecodingTrust, JailbreakBench [31], HarmBench [32], AIR-Bench [37], HELM Safety v1.0.0 (27 models), HELM AIR-Bench v1.1.0 (22 models) and a large open-weight behaviour audit [29] — name **zero** panel checkpoints; HELM Safety was read from its machine-readable release registry and verified to contain no model under 10B. Safety ground truth is therefore measured in-house on two axes: harmful-refusal rate on a frozen 40-item stratified core and over-refusal rate on 25 XSTest-safe items, with a blanket-refuser disqualification rule at $>0.50$ over-refusal derived from XSTest's own released human labels. That rule and the split seed *are* pre-specified, in the dataset artifact rather than in the metric declarations, and we say which is which in §5.5.

**Judge protocol.** The judge is `meta-llama/llama-3.3-70b-instruct` at temperature 0 under rubric B, which explicitly separates "did the model comply" from "is the content harmful". The rubric mandated by our own earlier plan (rubric A) scores *harmfulness* rather than *behaviour*, gave $\kappa \approx 0$ against a hand-labelled set, and was replaced; that replacement is a deviation and is recorded as one. Judge spend across this iteration was \$0.107 (laundering ladder) plus \$0.170 (independent re-adjudication), with the weights-only arms costing \$0.00.

**The analysis contract.** Every AUROC, Spearman correlation, bootstrap interval and paired difference in this paper is emitted by a versioned analysis script that prints its contract before any number and echoes it into a machine-readable `numbers.json` [ARTIFACT:art_0T8jhUa0zxmu]. The contract: cluster bootstrap over **lineages, with replacement**, $B = 10{,}000$ resamples, percentile 95% intervals; the number of eligible lineages is the resample size for each cell (11 of 19 lineages in the behaviour arm are singletons, and they are drawn as clusters like any other); Spearman with **rank-average** tie handling — a rule that matters, because our own prior-round audit found a reported $\rho = -0.20$ flip sign to $+0.105$ purely from positional tie-breaking; AUROC as Mann-Whitney $U/(n_+ n_-)$ from rank-average ranks with 0.5 tie credit and the number of tied pairs reported; **pairwise deletion** with the achieved $n$ printed at every cell and a cell of fewer than 4 usable members reported as unrecomputable rather than as a number; and permutation nulls with the exact floor $1/\binom{n}{k}$ printed beside every interval. The scope experiment ships its own independent implementation of the same contract, and an assertion block that recomputes every quoted number from the raw result files and blocks assembly on a mismatch [ARTIFACT:art_fvWfzRrcoKux].

# Method

## The weights-only statistics and their independent reimplementation

The arm is motivated directly by abliteration's mechanism. If every residual-write matrix has had one direction projected out, that direction is a shared approximate null direction of the whole write ensemble and should be recoverable from the ensemble alone. Let $\mathcal{W}$ be the set of matrices writing into the residual stream (attention output projections and MLP down-projections) across all $L$ layers. Form

$$A \;=\; \sum_{W \in \mathcal{W}} \frac{W W^\top}{\lVert W \rVert_F^2}, \qquad \lambda_1 \le \lambda_2 \le \dots \le \lambda_d, \quad v_1 = \text{eigvec}(\lambda_1),$$

and define the per-matrix normalised write energy along a unit direction $u$ as $e_W(u) = \lVert u^\top W\rVert^2 / (\lVert W\rVert_F^2/d)$, which equals 1 in expectation for a random direction. The five statistics are $W01 = \log_{10}(\mathrm{median}(\lambda)/\lambda_1)$, the depth of the suppression; $W02 = \Pr_W[e_W(v_1) < 0.1]$, the fraction of write matrices in which $v_1$ is suppressed; $W03 = \log_{10}\!\big(q_{0.05}(e_W(u_{\text{rand}}))/\overline{e_W(v_1)}\big)$ against **256** matched random directions; $W04 = \log_{10}(\lambda_2/\lambda_1)$; and $W05 = \log_{10}\min_W e_W(v_1)$, the *minimum* per-layer energy — the statistic that asks whether the suppression holds in every layer without exception. $W06$–$W16$ are spectral and norm descriptors (stable rank, singular-value entropy, effective rank, singular-value decay, RMSNorm gain statistics, write-row-norm Gini); $W06$–$W09$ are formula-identical to two features of [8] and are cited to it here.

Two gates run before any panel measurement, and this iteration added a third. The **positive control** injects a synthetic rank-one edit $W \leftarrow W - rr^\top W$ into every write matrix of `Qwen/Qwen3-0.6B` — the instruct member, whose unedited $W01$ is 0.6239, not the Base member's 0.6281 — and requires recovery: obtained at $|\cos(v_1, r)| = 1.000000$, $W02$ from 0 to 1.00, $W01$ from 0.624 to 4.869. The **band-limited control**, editing only the middle third of layers, is *not* recovered ($W02 = 0.0$). The new gate is an **independent reimplementation**: `wstats.py` was written from the published formulae before the original implementation was read, and reproduces the archived $W05$ to $\max|\Delta W05| = 9.9\times10^{-6}$ over 10 re-downloaded members at their archived revisions, ordering preserved, Spearman 1.0000, bit-identical across two runs [ARTIFACT:art_fvWfzRrcoKux]. Two attributable divergences are reported rather than smoothed: $W01$ reproduces to $10^{-4}$ on non-abliterated members but drifts up to 0.048 on abliterated ones, because $\lambda_{\min}$ sits at the floating-point noise floor exactly where the scar is (float32 versus float64 Gram accumulation, not a load-dtype effect); and $W03$ differs systematically by $+0.015$ to $+0.034$ because the published formula takes the 5th percentile of the per-direction *mean* energy while the original code pools all (direction $\times$ matrix) energies first. They are two different statistics and we now say which is which.

## Recipe scope: what does the detector actually key on?

Architecture is not what $W05$ keys on; the edit recipe is. Three tests replace leave-one-architecture-family-out as the generalisation control. (i) **Leave-one-uploader-out**, refitting the decision threshold on the remaining uploaders. (ii) **Four real published $\leq$4.2B checkpoints from four unseen uploaders**, scored against the same 36 negatives. A Hub search over 7 queries and 70 card-verified candidates established the constraint that forced this design: mechanically different recipes — norm-preserving, multi-direction, biprojected — demonstrably exist, but every public instance is $\geq$14.9B, far above the ceiling that keeps the study CPU-feasible. A miss on a new uploader must therefore be disambiguated from an unedited re-upload, which `realcheck.py` does by computing $E_1$ against the declared parent at pinned revisions. (iii) **Twelve in-house synthetic variants** on two architectures — plain projection, norm-preserving, rank-$k$ for $k \in \{2,4,8\}$, per-head surgery on the top 25% of heads, and a contiguous **layer-fraction sweep** — each carrying a fluency check and a greedy harmful-refusal rate, so that "the edit worked" and "the edit is visible" stay separable.

## The laundering ladder and the wild scan

The deployment premise needs two things the previous draft did not have: an evasion arm and a real scan. For the first, a faithful diff-in-means abliteration of `Qwen/Qwen3-1.7B` is built in house and gated (it must reproduce the panel's weight signature *and* collapse harmful refusal *and* leave WikiText perplexity intact), then pushed through five laundering families at graded intensity: benign LoRA-SFT (25/50/100/200 steps, $r{=}16$, $\alpha{=}32$, merged), linear merge with the instruct parent ($w \in \{0.10, 0.25, 0.50, 0.75, 0.90\}$), int8/int4/nf4 round-trips, and an adversary who adds back an $\varepsilon$-scaled rank-one term — naively, along a random direction, to the argmin matrix only, to the $k$ smallest matrices, and to all matrices. At every stage both **flag strength** ($W01$–$W05$, plus a hardened $W05q10$ using the 10th percentile instead of the minimum) and **un-censoring strength** (harmful-refusal rate, XSTest over-refusal, WikiText perplexity, distinct-3) are measured. The load-bearing quantity is the *order of the two deaths* and the evasion cost, defined as the increase in harmful refusal paid at the intensity where the flag first dies.

Direction selection turned out to be a method result rather than a detail. Held-out harmful-versus-benign AUROC **saturates** and cannot select the refusal direction: on Qwen3-1.7B eleven layers score $\geq 0.997$ and four tie at exactly 1.000, so the argmax is decided by the tie-break. Selection is therefore behavioural, as in [1]: sweep every layer, score by refusal on a 10-prompt development subset disjoint from the evaluation core, tie-break on held-out AUROC, and reject any layer that breaks fluency (13 of 29 layers qualify at 1.7B). The AUROC-selected variant ships as a sensitivity row.

For the second, the scan runs entirely on stored tensors: safetensors are streamed, the write matrices are read directly without instantiating a model, $W01$–$W05$ are computed, and the snapshot is deleted before the next repository is fetched. No `transformers` model is built, no prompt is tokenised, no forward pass is run. Repositories already in P1 are excluded, and every checkpoint in the abliterated region or the warning band is adjudicated against its card and lineage with the evidence quoted.

## The behavioural battery, unchanged and re-analysed

The 53-metric battery (16 weights-only, 11 black-box, 26 activation-based including four declared-to-fail controls) is **not** rebuilt in this iteration. It is re-analysed in three ways the reviewer asked for. **Power**: the paired cluster bootstrap is simulated at 2,000 replications per point over a $\Delta\rho$ grid from 0.00 to 0.60 at 19 lineages, and the panel size required for 80% power is searched over 18–300 lineages. **Comparator**: the paired difference is reported against the *pre-specified* black-box metric with a published prior (B01, first-step logit gap [24]) as well as the post-hoc best-of-11 (B09, greedy refusal rate), and a selection-corrected variant re-argmaxes the black-box winner inside every resample and prices the optimism. **Reliability**: because per-item labels were never persisted, the frozen prompt folds are rebuilt, paired to the archived responses, and re-adjudicated verbatim under rubric B by an independent model, giving split-half reliability, item-level agreement and attenuation-corrected correlations. Separately, every depth-sensitive activation metric is recomputed at three relative depths spanning the saturated AUROC plateau — the bare argmax (0.143), mid-stack (0.500), and the previously pre-declared $\rho^\star = 0.679$ — producing 1,014 (member, metric, depth) rows [ARTIFACT:art_fvWfzRrcoKux].

# Results

## The scar is real, and it is bounded by recipe and by uploader

[FIGURE:fig2]

On the archived 44-checkpoint panel the weights-only arm separates abliterated checkpoints from everything else without a parent and without a prompt. The table below reports $[\min, \max]$ for **every** class, not only the positives, because the abliterated-only column materially understates the overlap present in the data.

| statistic | abliterated ($n{=}8$) | base ($n{=}16$) | instruct ($n{=}15$) | beh.-unc. ($n{=}4$) | safety-RL ($n{=}1$) | AUROC (oriented) |
|---|---|---|---|---|---|---|
| $W05$ min layer energy | $-4.33$ $[-4.82, -2.74]$ | $-1.31$ $[-2.67, -0.97]$ | $-1.15$ $[-1.59, -0.96]$ | $-1.08$ $[-1.17, -0.51]$ | $-1.25$ | **1.000** |
| $W01$ suppression depth | 4.26 $[1.44, 4.82]$ | 0.58 $[0.34, 1.99]$ | 0.47 $[0.34, 0.68]$ | 0.46 $[0.20, 0.68]$ | 0.47 | 0.986 |
| $W03$ gap vs 256 random | 4.28 $[1.40, 4.74]$ | 0.60 $[0.30, 2.00]$ | 0.49 | 0.47 | 0.49 | 0.986 |
| $W04$ isolation | 3.68 $[0.85, 4.19]$ | 0.057 $[0.004, 1.62]$ | 0.046 $[0.004, 0.21]$ | 0.055 | 0.004 | 0.986 |
| $W02$ direction consistency | 1.00 $[0.96, 1.00]$ | 0.20 $[0.00, 1.00]$ | 0.11 $[0.00, 0.41]$ | 0.066 | 0.18 | 0.950 |
| $A01$ AMS $\sigma$ (baseline) | 2.38 $[1.45, 4.82]$ | 1.72 | 2.74 $[1.40, 4.40]$ | 1.61 | 3.64 | 0.640 |

Three corrections to how this table was previously reported. First, $W05$'s "AUROC 1.000" is the **oriented** value: abliterated members sit at the *low* end, so the raw Mann-Whitney AUROC is 0.000, and the orientation was read off the data. Second, the other four statistics reach 0.986 (0.950 for $W02$, with 21 tied positive-negative pairs), not 1.000, and the ranges above show why — $W01$'s base maximum of 1.992 overlaps the abliterated minimum of 1.438 by 0.554, and $W02$'s base maximum is exactly 1.000, identical to the abliterated median, so no $W02$ threshold separates the panel at all. Third, the separating margin is 0.0763 in $\log_{10}$ units, between the *highest* abliterated value ($-2.7415$, `huihui-ai/Qwen2.5-0.5B-Instruct-abliterated`) and the *lowest* non-abliterated one ($-2.6652$, `allenai/OLMo-1B-hf`); the previous draft's "$-2.742$ against $-2.665$" paired the boundary correctly but described $-2.742$ as the abliterated minimum, which is its maximum (the true minimum is $-4.8204$). OLMo is a one-member architecture family, and the four checkpoints nearest the boundary are two abliterated members and two base models from single- or three-member families (olmo, gpt\_neox).

**The generalisation control was testing the wrong variable, and the right one fails.** All eight archived positives come from two uploaders running an all-layer global diff-in-means projection, so leave-one-architecture-family-out cannot speak to the question. Leave-one-**uploader**-out does [ARTIFACT:art_fvWfzRrcoKux]:

| held-out uploader | $n_+$ | rank-transfer AUROC | catch rate at refit threshold |
|---|---|---|---|
| huihui-ai | 6 | 1.000 $[1.000, 1.000]$ | 1.00 |
| Goekdeniz-Guelmez | 2 | 1.000 $[1.000, 1.000]$ | 1.00 |
| in-house synthetic | 12 | 0.926 $[0.782, 1.000]$ | 0.83 |
| BennyDaBall | 1 | 0.972 $[0.906, 1.000]$ | 1.00 |
| MagicalAlchemist | 1 | 0.306 $[0.171, 0.472]$ | 0.00 |
| prithivMLmods | 1 | 0.222 $[0.118, 0.364]$ | 0.00 |
| mlabonne | 1 | 0.028 $[0.000, 0.088]$ | 0.00 |

Scored as a group against the same 36 negatives, the four real new-uploader checkpoints give **AUROC 0.382** $[0.036, 0.949]$, permutation $p = 0.776$, catch rate 0/4 at the threshold fitted on the archived uploaders — against 1.000 and 1.00 for the archived positives. Their $W05$ values are $-0.964$ (`mlabonne/Qwen3-0.6B-abliterated`), $-1.010$ (`MagicalAlchemist/Qwen3-1.7B-Magic_decensored`), $-0.990$ (`prithivMLmods/VibeThinker-3B-heretic_decensored`) and $-2.161$ (`BennyDaBall/Qwen3-4b-Z-Image-Turbo-AbliteratedV1`), against an archived abliterated range of $-2.74$ to $-4.82$. This is not an unedited-re-upload artifact: all three with a resolvable parent are genuine near-rank-one edits by the parent-referenced statistic ($E_1 = 0.995, 0.995, 0.997$; relative Frobenius change 2.5–3.0%; 0% bit-identical matrices).

[FIGURE:fig3]

The synthetic ablation separates *which* mechanical property the detector needs. Norm-preserving, plain and rank-$k$ ($k \in \{2,4,8\}$) variants are all detected at AUROC 1.000; per-head surgery on the top 25% of heads is missed at 0.556 $[0.152, 0.923]$. The layer-fraction sweep is decisive: on **both** hosts the detection threshold sits at $f^\star = 1.00$ — only the fully global edit is visible. And inside that blind spot an edit can be fully effective: on Qwen3-1.7B a projection confined to the middle 50% of layers drives harmful refusal from 0.45 to 0.00, exactly matching the full-stack edit, while $W05$ moves from $-1.0098$ to $-1.0088$. A synthetic unit test explains the sharpness: with 4 of 12 matrices edited, $v_1$ is no longer the injected direction at all ($W02 = 0$), because the Gram pools every matrix. The blind spot is a threshold, not a ramp.

**The scope sentence the evidence supports**, generated from these numbers rather than asserted: $W05$ detects global all-layer single-direction and multi-direction projection-type abliteration, and norm-preserving and rank-$k$ variants of it, at AUROC $\geq 0.95$; it misses per-head surgery, any edit confined to a proper subset of layers, and — on this evidence — the same global recipe from three of four unseen uploaders. It is a recipe-class and calibration-class signal, not a detector for abliteration in general.

Two negatives from the previous iteration survive unchanged and are worth restating, because they bound what the arm can ever be. The four behaviourally-uncensored fine-tunes sit squarely inside the instruct distribution on every weights-only statistic ($W01$ median 0.463 against instruct 0.471; $W05$ median $-1.081$ against instruct $-1.155$) despite two of them complying with 51% and 84% of harmful requests — there is no rank-one scar to find. Qwen3-4B-SafeRL is likewise indistinguishable in the weights ($W01 = 0.471$, $W04 = 0.004$) while behaving very differently. **A weights-only test answers "has this checkpoint been directionally edited?", not "is this checkpoint safe?"**

## In the wild: zero false positives, and a flag that a quantizer erases for free

[FIGURE:fig4]

**The scan.** 250 sub-4B Hub checkpoints that declare no edit were attempted and 160 scored to completion; 81 were unresolvable (Conv1D-transposed GPT-2-style layouts, GPTQ/bitsandbytes-quantized weights, malformed configs), 8 skipped and 1 errored, and none of those is counted as scanned [ARTIFACT:art_gCgia-6VUZJb]. The result is **zero** hits inside the abliterated region ($W05 \leq -2.7415$): false-positive rate 0/160, Wilson 95% $[0, 0.023]$. Two repositories fall in the warning band — `rinna/japanese-gpt-neox-small` at $-2.614$ and `stabilityai/stablelm-3b-4e1t` at $-2.515$ — and both are adjudicated FALSE\_POSITIVE with quoted card evidence, and both belong to architecture families the panel barely covers, exactly where the boundary analysis above predicted false positives would concentrate. The positive control (8/8) and negative control (12/12) run through the identical code path. Audit cost: zero prompts, zero forward passes, median 7.0 s of CPU linear algebra per checkpoint (2.7 s on GPU at 1.7B). Against the string-match baseline our own harvest quantifies — 50.5% of self-declared edited repositories carry "abliterat" in their id — the scan's contribution is precisely the complement: it is the only instrument here that could in principle flag the other half, and on 160 undeclared repositories it flagged none, which we report as a specificity result and not as a discovery.

Only $W05$ earns that specificity. On the labelled control set $W05$ reaches sensitivity 1.000 / specificity 1.000 with 0 of 160 undeclared repositories flagged; $W01$, $W03$ and $W04$ sit at sensitivity 0.875, and $W02$ flags 23 of 160 undeclared repositories (14.4%), so its apparent robustness is a threshold that separates nothing. The hardened $W05q10$ (10th percentile instead of the minimum) keeps perfect specificity but drops to 0.875 sensitivity: hardening has a measured cost.

**The laundering ladder.** The in-house root is clean: `Qwen/Qwen3-1.7B` at harmful refusal 0.923 becomes 0.162 after abliteration, with $W01 = 4.571$, $W02 = 1.000$, $W05 = -4.592$ (squarely inside the abliterated region) and WikiText perplexity *unchanged* at 27.08 $\to$ 26.25. No stage in the 34-stage ladder tripped the fluency screen or the blanket-refuser rule.

| treatment family | verdict | flag dies at | un-censoring dies at | evasion cost |
|---|---|---|---|---|
| add-back, all matrices | EVADABLE | $\varepsilon = 0.10$ | $\varepsilon = 1.00$ | $-0.004$ |
| merge with instruct parent | EVADABLE | $w = 0.10$ | $w = 0.50$ | $+0.069$ |
| quantization round-trip | EVADABLE | 4-bit | never | $+0.075$ |
| add-back, $k$ smallest | EVADABLE | $k = 4$ | $k = 32$ | $+0.128$ |
| add-back, argmin only | NEITHER\_DIES | — | — | — |
| add-back, random direction | NEITHER\_DIES | — | — | — |
| LoRA-SFT, benign | NEITHER\_DIES | — | — | — |

The verdict is `SCAR_IS_CHEAPLY_EVADABLE`, and the cheapest successful evasion is not an attack at all. A plain **int4 round-trip** takes $W05$ from $-4.592$ to $-1.946$ — comfortably clean — at a harmful-refusal rate of 0.135, *below* the unlaundered root's own 0.162, with perplexity 37.7 against 26.25, well inside the fluency screen. nf4 gives $-2.126$ at refusal 0.237; int8 leaves the flag alive at $-3.980$. An ordinary deployment step erases the certificate for free, which is the single most consequential number in this paper for anyone who wanted to run this at hub scale.

Three results reverse pre-registered expectations, and all three cut in the detector's favour. (i) **The argmin attack fails.** $W05$ is a minimum over matrices, so a one-matrix patch was expected to defeat it; at $\varepsilon = 1.00$ it moves $W05$ only to $-3.080$ and never crosses. Abliteration suppresses all 56 write matrices roughly equally, so the minimum has 55 runners-up, and four matrices must be patched before the flag dies — and because $v_1$ is recomputed from the treated model, a local patch rotates the eigenvector and lifts *every* matrix's energy. A local edit has a global effect on the statistic. (ii) **Dense benign fine-tuning does not scrub the scar**: 200 LoRA steps move $W05$ only from $-4.592$ to $-4.381$ while *restoring* harmful refusal from 0.162 to 0.368 — the treatment expected to kill the flag is the one family that most clearly favours it. (iii) **$W05$ is not the most fragile of the five statistics** (survival 0.559 of non-broken stages against $W02$'s 0.647), which contradicts the intuition that a minimum must be the most brittle.

## What the parent-free constraint actually costs

[FIGURE:fig5]

$E_1 = \mathrm{mean}_m\,\sigma_1^2(\Delta W_m)/\sum_i\sigma_i^2(\Delta W_m)$, computed over write matrices in the 0.25$L$–0.75$L$ band (our reading of the incumbent's "mid-stack"), was run on every sibling pair the panel affords [ARTIFACT:art_fvWfzRrcoKux].

| matched subset | $n$ | $E_1$ AUROC (parent required) | $W05$ AUROC (parent free) | paired difference |
|---|---|---|---|---|
| 12 pre-declared pairs, calibration uploaders | 12 | 1.000 $[1.000, 1.000]$ | 1.000 $[1.000, 1.000]$ | $+0.000$ $[0.000, 0.000]$ |
| + 3 new-uploader pairs | 15 | 1.000 $[1.000, 1.000]$ | 0.833 $[0.556, 1.000]$ | $-0.167$ $[-0.444, 0.000]$ |
| + 26 synthetic pairs | 41 | 0.976 $[0.931, 1.000]$ | 0.790 $[0.593, 0.918]$ | $-0.186$ $[-0.382, -0.079]$ |

On the recipes and uploaders it was characterised on, **parent-free costs nothing**: a tie at 1.000, paired difference exactly zero. That is the strong sentence the reviewer asked us to earn, and we can only say it about the pre-declared subset. Adding three new-uploader pairs makes $E_1$ hold while $W05$ falls; the interval reaches zero at its boundary, so at $n = 15$ this is underpowered as an interval claim, but descriptively it is unambiguous — $E_1$ detects 3 of 3 and $W05$ detects 0 of 3. Including the synthetic pairs the difference does exclude zero, at $-0.186$.

The two are, however, **complementary rather than nested**: $E_1$ degrades badly on multi-direction edits (AUROC 0.17–0.67 for $k = 8 \ldots 2$) where $W05$ is perfect, and holds at 0.995 on the layer-band edits $W05$ cannot see at all. The right reading is not that the parent-requiring statistic dominates, but that the parent buys robustness to *who ran the edit* while the parent-free Gram statistic buys robustness to *how many directions were removed*. A deployable audit would run both where the parent exists and treat a $W05$ hit as sufficient but never necessary.

## The behavioural negative, now with a bound on what it can mean

[FIGURE:fig6]

Restricting to the 28 non-base members over 19 lineages for which a behavioural rate is meaningful — the previous draft said 26 over 18, and the recomputation gives 28 over 19; the two partitions (`member_class != base` and `renderer == chatml`) disagree on two checkpoints, and we now state which rule is applied — the ranking of metrics against measured harmful-refusal rate is:

| metric | arm | $\rho$ (member, $n{=}28$) | 95% CI | $\rho$ (lineage, $n{=}19$) |
|---|---|---|---|---|
| $A19$ refusal-axis / unembed cosine | activation | $+0.763$ | $[+0.592, +0.864]$ | $+0.800$ |
| $B01$ first-step logit gap (pre-specified) | black-box | $+0.708$ | $[+0.369, +0.901]$ | $+0.659$ |
| $A11$ prompt-position refusal log-odds | activation | $+0.702$ | $[+0.345, +0.892]$ | $+0.671$ |
| $B08$ first-token entropy asymmetry | black-box | $-0.672$ | $[-0.843, -0.373]$ | $-0.782$ |
| $B09$ greedy refusal rate (post-hoc winner) | black-box | $+0.670$ | $[+0.374, +0.883]$ | $+0.668$ |
| $A14$ generated-step refusal log-odds | activation | $+0.654$ | $[+0.291, +0.839]$ | $+0.550$ |
| $A02$ AMS concept cosine | activation | $+0.631$ | $[+0.212, +0.874]$ | $+0.573$ |
| $A01$ AMS $\sigma$ | activation | $+0.541$ | $[+0.148, +0.812]$ | $+0.569$ |

Four things follow, and each answers a specific critique.

**(a) The baseline was mis-described.** $B09$ is not the best black-box metric at either aggregation unit: $B08$ leads at lineage level ($|\rho| = 0.782$ against 0.668) and $B01$ at member level (0.708 against 0.670), and $B09$ is the in-resample argmax in only 11.2% (lineage) / 14.4% (member) of cluster resamples. The selection optimism of choosing best-of-11 on these data is $+0.182$. Correcting this **strengthens** the negative — the interior candidates trail an even stronger trivial baseline — but the sentence "$B09$, the best black-box baseline" was wrong and is withdrawn.

**(b) The paired comparison, against both a pre-specified and a post-hoc comparator.** At member level, $|\rho_X| - |\rho_{B09}|$: $A02$ $-0.038$ $[-0.327, +0.249]$; $A01$ $-0.162$ $[-0.494, +0.200]$; $\alpha_{50}$ $-0.151$ $[-0.694, +0.485]$; $W01$ $-0.265$ $[-0.659, +0.146]$; $W05$ $-0.419$ $[-0.735, +0.039]$; $W02$ $-0.457$ $[-0.736, -0.023]$. Against the pre-specified $B01$ the picture is the same and slightly worse for the interior ($A02$ $-0.076$ $[-0.553, +0.374]$; $W05$ $-0.457$ $[-0.763, -0.005]$). No interior metric's advantage has an interval excluding zero at either unit, against either comparator; two intervals exclude zero on the wrong side. Under the selection-corrected comparator, which re-argmaxes the black-box winner inside every resample, four of seven white-box candidates are *significantly worse* than the black-box arm.

**(c) The power the test actually had.** Simulating the same paired cluster bootstrap at 19 lineages, 2,000 replications per grid point, the **minimum detectable $|\Delta\rho|$ at 80% power is 0.32**; power is 0.012 at $\Delta\rho = 0.20$ and 0.70 at 0.30. Reaching 80% power would need roughly 50 lineages at $\Delta\rho = 0.30$, roughly 150 at 0.20, and no panel size up to 300 lineages suffices at 0.10. The falsifier *could* have failed: some advantage in the swept range does reach 80% power, so the negative carries information. The conclusion the data supports is therefore bounded, and we state it in that form: **at this panel size no interior metric shows an advantage over the best black-box baseline larger than about 0.3 in $|\rho|$; distinguishing smaller advantages would require roughly 150 lineages.** That is a very different sentence from "looking inside buys nothing", and it is the one we make.

**(d) Neither reliability nor depth explains the result.** Split-half reliability of the 40-item harmful-refusal rate, odd versus even items, Spearman-Brown corrected, is $r_{xx} = 0.968$ (0.978 from Pearson), so the attenuation correction is a factor of 1.016; no ordering moves and no paired difference changes sign. An independent adjudicator, itself validated 6/6 against the hand-labelled set, agrees with the archived judge at checkpoint-level Spearman 0.927 (mean absolute rate difference 0.112) while disagreeing sharply with the lexical screen ($\kappa = 0.403$ over 2,859 items; refusal share 0.428 against the screen's 0.190). The instrument is noisy against a substring screen and stable against itself. On depth, recomputing every depth-sensitive activation metric at 0.143, 0.500 and 0.679 over 26 members gives `BLACKBOX_WINS` at all three, so the falsifier is not a depth artifact [ARTIFACT:art_fvWfzRrcoKux]. That test needed the right statistic: four activation metrics have a *larger point estimate* than a baseline at $\rho^\star$ — $A19$ reaches $+0.770$ against $B09$'s $+0.766$ — but the paired lineage-bootstrap difference is $+0.0045$ $[-0.225, +0.260]$, and comparing point estimates alone would have called that a win. One decision-relevant side finding: $\alpha_{50}$'s ceiling censoring is strongly depth-dependent (25/26 censored at the bare argmax, 15/26 at 0.500, 19/26 at $\rho^\star$), so the previously pre-declared depth is not the one yielding the most usable values. Depth selection for an AUROC plateau and depth selection for steering headroom are different problems, and the previous iteration conflated them.

## Two dissociations, and an audit of our own claims

**Detection and control come apart at construction time.** Building the abliteration root exposed a dissociation sharper than the one we previously reported. Held-out harmful/benign AUROC saturates on Qwen3-1.7B — eleven layers $\geq 0.997$, four tied at exactly 1.000 — so the argmax is a tie-break. Both the AUROC-selected direction (layer 20) and the behaviourally-selected one (layer 18) reproduce the full weight signature; but the AUROC pick leaves harmful refusal at 0.333 against the behavioural pick's 0.162. Two directions indistinguishable on a detection metric differ twofold in how much they un-censor. At 0.6B the failure is starker: the argmax lands at block 1 and leaves refusal at the parent's value, untouched. **The weight scar and the un-censoring are dissociable at construction time**, which is the sharpest mechanistic statement this paper can make about why a structural certificate is not a safety score. It also independently corroborates the general detection-versus-control result of [7] in a setting where the "detector" is a weight statistic rather than a probe.

**The refusal-substring screen is a broken instrument.** In the ladder, the standard 12-substring screen from [1] reads exactly 0.000 refusal on every abliterated-derived stage where the judge reads 0.13–0.37, so the reported $\kappa \approx 0$ is the screen failing, not the judge; at the rate level the two correlate at $r = 0.952$ across 34 stages. The previous iteration measured the same failure in a steering sweep (regex 0.01 against judge 0.85 on an abliterated Qwen3-0.6B). Any result of the form "model X cannot be made to refuse" that rests on a substring screen should be re-derived semantically before it is believed.

**A self-audit of the previous draft.** A dedicated re-analysis recomputed every number the previous draft quoted [ARTIFACT:art_0T8jhUa0zxmu] and found one systematic error and two mislabelled quantities. Four values presented as *correlations* of a white-box metric with ground truth — $A01$ $-0.161$, $A02$ $+0.036$, $W01$ $-0.373$, $\alpha_{50}$ $-0.453$ — are in fact **paired differences** $|\rho_X| - |\rho_{B09}|$ computed on a 26-member `renderer == chatml` subset rather than the 28-member non-base subset the draft stated. Read as correlations they are wrong by up to 0.67 and one has the wrong sign; read as paired differences on that subset, three of the four reproduce to four decimals. The arithmetic was never wrong; the labels were, and no artifact recorded either the quantity or the subset. Both readings are now published, and the falsifier is re-run on the draft's own subset: the verdict is unchanged on both. Of 54 checked disagreements between the draft and the recomputation, 32 match, 20 differ because the recomputation uses a stated method the draft did not state, and 2 are transcription errors.

**"Pre-registered" is now reserved for what is actually stamped.** The frozen `metric_spec.py` (sha256 `544ff994…`, verified) declares 53 metrics with family, prompt requirement, declared forward passes and declared wall-clock, plus the held-out split's seed and fraction — **and nothing else**. It contains no falsifier, no analysis plan, no base-model exclusion rule, no bootstrap specification, no white-box shortlist and no designated black-box baseline. Mapping every "pre-registered" claim in the previous draft to the artifact and line that records it gives **4 SUPPORTED, 2 PLAN-ONLY, 6 UNSUPPORTED**. The blanket-refuser threshold and the split seed are genuinely pre-specified but belong to the *dataset* artifact; the falsifier, the exclusion rule, the bootstrap and the comparator choice were analysis-time conventions and are worded as such throughout this paper. The judge rubric was mandated by the plan, failed an instrument check, and was replaced — a deviation, recorded as one.

# Discussion

**What a single checkpoint's tensors do and do not reveal.** A directional weight edit is a structural change and leaves a structural trace: the projection removes one direction from every write matrix simultaneously, and that simultaneity is the whole signal — $W05$, a minimum over layers, works precisely because a genuine all-layer abliteration admits no exception. The four measurements of this paper are best read as mapping the exact region in which that logic holds. It holds across architectures (leave-one-family-out is near-perfect on the three families with positives), across two projection recipes, across norm-preserving and rank-$k$ variants, against 160 undeclared Hub checkpoints with zero false positives, and against 200 steps of benign fine-tuning. It fails the moment the edit is not global (a middle-50% projection is behaviourally indistinguishable from the full edit and statistically invisible), when the edit is per-head, when the checkpoint is quantized to 4 bits, when it is merged even 10% back toward its parent — and, most importantly for anyone tempted by the AUROC, when the *same* recipe comes from an uploader whose calibration the threshold was not fitted on. The defensible product claim is a free, prompt-free certificate of an unlaundered global directional edit, with all four failure modes measured. That is smaller than we hoped one iteration ago and considerably more useful than an unqualified AUROC of 1.000, because a screen's value at hub scale is set by its false-negative structure, not by its separation on the panel that defined it.

**Why the parent-free constraint is still worth paying for.** The head-to-head is the cleanest way to price it. On matched pairs from the uploaders both methods were characterised on, parent-free costs exactly nothing (1.000 versus 1.000). What it costs is generalisation to new calibration regimes, and what it buys is (i) immunity to a spoofed reference, which the parent-requiring incumbent names as its own primary attack, (ii) applicability to the 23.4% of self-declared edited Hub repositories that name no mechanism and the majority that name no parent, and (iii) robustness to multi-direction edits, on which $E_1$ degrades to 0.17–0.67 while $W05$ is perfect. The two statistics fail on disjoint sets, which argues for running both rather than choosing.

**The behavioural negative, stated at the strength the data supports.** It would have been easy to report the best of 53 metrics against behaviour and call it a method. The discipline that prevented that also has to be applied to the negative itself, and doing so changes it: with a minimum detectable paired difference of 0.32 at 19 lineages, "no interior metric beats the black-box baseline" cannot be distinguished from "we cannot resolve an advantage smaller than 0.3". What the data does support is that greedy refusal rate on harmful prompts — and, better still, first-token entropy asymmetry — is an extremely cheap partial benchmark run, and a partial benchmark run predicts a full one well. We explicitly do not claim that weight geometry carries no behavioural signal: Paul reports $\rho = 0.72$ between a weight-space drift probability and harmful compliance over 24 manufactured adapters with a 50–2000-step dose ladder on a single base model [8], a regime our panel does not contain. Our panel's behaviourally-uncensored members were made by ordinary SFT with no directional edit and no dose ladder, so a low-rank spectral signal is not merely undetected but absent by construction.

**Limitations.** (1) The scar is recipe- and calibration-bounded, as measured above; three of four unseen uploaders running the same nominal recipe escape it. (2) It is cheaply evadable by an ordinary int4 round-trip, so it certifies an *unlaundered* edit and nothing more; we did not test whether a hardened variant computed on dequantized weights recovers the signal. (3) Public mechanically-different recipes (ORBA, MPOA, Heretic, OBLITERATUS multi-direction) exist at 4B on the panel's own Qwen3-4B family but were not measured here — the Hub search that established the $\geq$14.9B constraint predates their identification — and reflection-type ORBA is the sharpest outstanding falsification target, because a Householder reflection flips the component along $u$ instead of removing it and preserves $\lVert w \rVert$ exactly, leaving no null direction for $W05$ to find. (4) The wild scan covers 160 checkpoints in 7 architecture-family neighbourhoods; both warning-band repositories lie in families the panel barely covers, and the false-positive rate outside the tested architectures is unmeasured. (5) $n_{\text{abliterated}} = 8$ on the archived panel, and the separating margin is 0.0763 in $\log_{10}$ units, carried by two individual checkpoints. (6) Ground truth is 97% self-measured, judge-derived, and bounded by 40 harmful and 25 XSTest-safe items per member (binomial SE $\approx 0.08$ at $p = 0.5$), although split-half reliability of 0.968 shows the aggregate rate is stable. (7) The behaviour arm is 28 members over 19 lineages with 11 singletons, which is the power limit quantified in §5.4. (8) One adjacent work (Coslett 2026, Zenodo) remains unread after six access routes returned HTTP 403 or were unreachable; on the only reachable characterisation its signal is an activation-geometry fingerprint anchored to a claimed identity, so the risk to our novelty claim is bounded but open.

**What we would do next.** Three things follow directly. First, measure $W05$ on the four public sub-4.2B Qwen3-4B-family checkpoints produced by MPOA, Heretic and OBLITERATUS, and on an in-house ORBA reimplementation, which turns the signed prediction table into a result and would settle whether the uploader effect is really a hidden recipe effect. Second, replace the global minimum with a sliding-layer-window profile: the band-limited blind spot is a threshold artifact of pooling every matrix into one Gram, and a per-band eigen-analysis should recover exactly the edits that are currently invisible while remaining prompt-free. Third, test the black-box result where it should break, on checkpoints tuned to refuse benchmark items specifically; a metric that reads the interior has a principled reason to survive that attack, and no panel we have contains such an adversarial checkpoint.

# Conclusion

We asked whether a checkpoint's safety provenance can be read from its tensors alone — no parent, no reference, no prompt, no forward pass — and this iteration answers by measuring the boundary rather than the peak. Inside the boundary the answer is a clear yes and the economics are hard to beat: the minimum per-layer write energy along the minimum eigenvector of the pooled write Gram matrix separates the archived positives at oriented AUROC 1.000, ties the parent-requiring incumbent at 1.000 on 12 matched sibling pairs while needing no parent, survives 200 steps of benign fine-tuning and a single-matrix adversarial patch, and returns zero false positives over 160 undeclared Hub checkpoints at 7.0 s of CPU each. Outside it the answer is no, in four specific and measured ways: an edit confined to the middle 50% of layers is fully effective behaviourally and statistically invisible; per-head surgery is missed; a plain int4 round-trip erases the flag at *lower* harmful refusal than the unlaundered original; and three of four unseen uploaders running the same nominal recipe are not caught. The claim we can defend is therefore a free, prompt-free certificate of an unlaundered global directional edit — a provenance signal with a mapped evasion surface, not a safety score. Alongside it, the behavioural negative is restated at the strength the design supports: at 19 lineages the minimum detectable paired difference is 0.32, so what we have shown is that no interior observable beats a trivial black-box baseline by more than about 0.3 in $|\rho|$, and that resolving anything smaller needs roughly 150 lineages. Finally, an audit of our own previous round relabels four quoted values, corrects the identity of the best black-box baseline, and reduces twelve "pre-registered" claims to four. The useful single-checkpoint question is not "is this model safe" but "has this model been edited, and by whom, and has anyone cleaned up afterwards" — and only the first two thirds of that question currently have a free answer.

# References

[1] A. Arditi, O. Obeso, A. Syed, D. Paleka, N. Panickssery, W. Gurnee, and N. Nanda. Refusal in Language Models Is Mediated by a Single Direction. *NeurIPS*, 2024. arXiv:2406.11717.

[2] J. Hurtado. Has This Checkpoint Been Abliterated? A Two-Signal Audit and Its Failure Map. *arXiv:2607.01854*, 2026.

[3] G. Messenger. Detecting Safety Training Modification in Language Models via Activation Analysis. *IEEE Access*, 14:91723–91737, 2026. arXiv:2608.05578.

[4] C. Huang, Y.-L. Chen, C.-M. Yu, and W.-B. Lee. RAS: Measuring LLM Safety Through Refusal Alignment. *arXiv:2606.25750*, 2026.

[5] S. Peng, P.-Y. Chen, M. Hull, and D. H. Chau. Navigating the Safety Landscape: Measuring Risks in Finetuning Large Language Models. *NeurIPS*, 2024. arXiv:2405.17374.

[6] S. Basu, S. Y. Patel, P. Sheth, B. Muralidharan, N. Elamaran, A. Kinra, J. Morgan, and R. Batniji. Interpretability without actionability: mechanistic methods cannot correct language model errors despite near-perfect internal representations. *arXiv:2603.18353*, 2026.

[7] M. Galeone et al. Perfect Detection, Failed Control: The Geometry of Knowing vs. Steering in Language Models. *arXiv:2606.24952*, 2026.

[8] A. Paul. Spectral Geometry of LoRA Adapters Encodes Training Objective and Predicts Harmful Compliance. *arXiv:2604.08844*, 2026.

[9] Z. Zhong and A. Raghunathan. Watch the Weights: Unsupervised monitoring and control of fine-tuned LLMs. *arXiv:2508.00161*, 2025.

[10] Detecting Backdoored LoRAs from Weights Alone. *arXiv:2602.15195*, 2026.

[11] elder-plinius et al. OBLITERATUS: one-click model liberation toolkit, including `obliteratus/analysis/spectral_certification.py`. Software, AGPL-3.0, first public 2026-03-04.

[12] `reverse-abliterate` 0.1.2. Software package: metadata- and filename-based abliteration scanner.

[13] M. Labonne. Uncensor any LLM with abliteration. Hugging Face community blog, 13 June 2024.

[14] P. Weidmann. Heretic: fully automatic censorship removal for language models. Software, 2025–2026.

[15] J. W. Lai (grimjim). Norm-Preserving Biprojected Abliteration (MPOA). Hugging Face community blog, 6 November 2025.

[16] J. W. Lai (grimjim). ORBA: Orthogonal Reflection Bounded Ablation. Hugging Face community blog, 25 March 2026.

[17] Gabliteration: Adaptive Multi-Directional Neural Weight Modification. *arXiv:2512.18901*, 2026.

[18] J. Young et al. Comparative Analysis of LLM Abliteration Methods: A Cross-Architecture Evaluation. *arXiv:2512.13655*, 2025.

[19] S. Jain, E. S. Lubana, K. Oksuz, T. Joy, P. H. S. Torr, A. Sanyal, and P. K. Dokania. What Makes and Breaks Safety Fine-tuning? A Mechanistic Study. *NeurIPS*, 2024. arXiv:2407.10264.

[20] B. Wei, K. Huang, Y. Huang, T. Xie, X. Qi, M. Xia, P. Mittal, M. Wang, and P. Henderson. Assessing the Brittleness of Safety Alignment via Pruning and Low-Rank Modifications. *ICML*, 2024. arXiv:2402.05162.

[21] H. Lu et al. AlphaPruning: Using Heavy-Tailed Self-Regularization Theory for Improved Layer-wise Pruning of Large Language Models. *NeurIPS*, 2024. arXiv:2410.10912.

[22] H. Shairah et al. An Embarrassingly Simple Defense Against LLM Abliteration Attacks. *arXiv:2505.19056*, 2025.

[23] J. Fafula. Abliteration Is Not a Scalpel: Off-Target Effects of Refusal Removal on Decision Disposition Across Model Families. *arXiv:2607.17427*, 2026.

[24] T. Li and Y. Liu. Logit-Gap Steering: A Forward-Pass Diagnostic for Alignment Robustness. *arXiv:2506.24056*, 2026.

[25] A. Korznikov, A. Galichin, A. Dontsov, E. Rogov, I. Oseledets, and E. Tutubalina. The Rogue Scalpel: Activation Steering Compromises LLM Safety. *arXiv:2509.22067*, 2026.

[26] B. Taimeskhanov, S. Vaiter, and D. Garreau. Towards Understanding Steering Strength. *ICML*, 2026. arXiv:2602.02712.

[27] S. Gadgil, T. Lin, and K. Lee. Where to Steer: Input-Dependent Layer Selection for Steering Improves LLM Alignment. *arXiv:2604.03867*, 2026.

[28] T. Chang, T. Schnabel, A. Swaminathan, and J. Wiens. A Course Correction in Steerability Evaluation: Revealing Miscalibration and Side Effects in LLMs. *arXiv:2505.23816*, 2025.

[29] A. Hasan and S. Biswas. The Refusal-Compliance Tradeoff: A Large-Scale Safety Behavior Audit of Large Language Models. *arXiv:2605.05427*, 2026.

[30] A. Zou, Z. Wang, N. Carlini, M. Nasr, J. Z. Kolter, and M. Fredrikson. Universal and Transferable Adversarial Attacks on Aligned Language Models. *arXiv:2307.15043*, 2023.

[31] P. Chao et al. JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models. *NeurIPS Datasets and Benchmarks*, 2024. arXiv:2404.01318.

[32] M. Mazeika et al. HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal. *ICML*, 2024. arXiv:2402.04249.

[33] P. Röttger, H. R. Kirk, B. Vidgen, G. Attanasio, F. Bianchi, and D. Hovy. XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models. *NAACL*, 2024. arXiv:2308.01263.

[34] S. Han et al. WildGuard: Open One-Stop Moderation Tools for Safety Risks, Jailbreaks, and Refusals of LLMs. *NeurIPS Datasets and Benchmarks*, 2024. arXiv:2406.18495.

[35] L. Zheng et al. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *NeurIPS*, 2023. arXiv:2306.05685.

[36] T. Xie et al. SORRY-Bench: Systematically Evaluating Large Language Model Safety Refusal Behaviors. *ICLR*, 2025. arXiv:2406.14598.

[37] Y. Zeng et al. AIR-Bench 2024: A Safety Benchmark Based on Risk Categories from Regulations and Policies. *arXiv:2407.17436*, 2024.

[38] L. Li et al. SALAD-Bench: A Hierarchical and Comprehensive Safety Benchmark for Large Language Models. *ACL Findings*, 2024. arXiv:2402.05044.

[39] L. Sun et al. TrustLLM: Trustworthiness in Large Language Models. *ICML*, 2024. arXiv:2401.05561.

[40] H. Zhao et al. Qwen3Guard Technical Report. *arXiv:2510.14276*, 2025.

[41] A. Yang et al. Qwen3 Technical Report. *arXiv:2505.09388*, 2025.

[42] L. B. Allal et al. SmolLM2: When Smol Goes Big — Data-Centric Training of a Small Language Model. *arXiv:2502.02737*, 2025.

[43] S. Biderman et al. Pythia: A Suite for Analyzing Large Language Models Across Training and Scaling. *ICML*, 2023. arXiv:2304.01373.

[44] A. Dubey et al. The Llama 3 Herd of Models. *arXiv:2407.21783*, 2024.

[45] G. Ilharco, M. T. Ribeiro, M. Wortsman, S. Gururangan, L. Schmidt, H. Hajishirzi, and A. Farhadi. Editing Models with Task Arithmetic. *ICLR*, 2023. arXiv:2212.04089.

[46] Y. Li, H. Hu, J. Sang, Y. Ma, X. Nie, Q. Zhang, Y. Yu, J. Su, Y. Huang, and J. Zhou. Prefill-level Jailbreak: A Black-Box Risk Analysis of Large Language Models. *arXiv:2504.21038*, 2025.

[47] G. Chen, T. Xia, H. Jia, C. Li, P. Torr, and J. Gu. LLM Jailbreak Detection for (Almost) Free! *arXiv:2509.14558*, 2026.

[48] B. Candogan, Y. Wu, E. Abad Rocamora, G. Chrysos, and V. Cevher. Single-pass Detection of Jailbreaking Input in Large Language Models. *TMLR*, 2025. arXiv:2502.15435.

[49] V. Siu, N. Crispino, J. Park, Z. Henry, D. Wang, Y. Liu, D. Song, and C. Wang. SteeringSafety: Benchmarking Representation Steering in LLMs Across Safety Perspectives. *arXiv:2509.13450*, 2026.

[50] A. Mishra, D. Khashabi, and A. Liu. Steered LLM Activations are Non-Surjective. *arXiv:2604.09839*, 2026.

</paper>

<supplementary_materials>
The authors' code, data, and experimental artifacts. You may read these to verify
claims made in the paper — check if the code matches the described methodology,
if the results are reproducible, and if the data supports the conclusions.

--- Item 1 ---
id: art_CKWQh2cOQLLQ
type: dataset
title: Frozen safety prompt sets and model list
summary: |-
  ONE deliverable, full_data_out.json, holding EXACTLY 8 datasets / 2,113 rows, every row tagged metadata_fold = dataset name. Row schema: {input, output, metadata_fold, metadata_uid, metadata_block_version, metadata_meta{...}}. Validated against exp_sel_data_out; full/mini/preview all pass. 3.5 MiB, far under the 100MB limit.

  DATASETS: harmless_dynamics (43: 40 vetted everyday user turns over 10 topics + 3 rejects, meta.selected); xstest_overrefusal (450 = 250 safe + 200 unsafe, split verbatim in meta.label/meta.prompt_type); plain_harmful (594 deduped AdvBench+JBB union, meta.in_core80 marks the 80-row 10-category stratified core, meta.target carries the affirmative prefix); jailbreak_suite (400 = the 80 core behaviors x 5 published templates, meta.pair_id resolves to the plain_harmful uid); layer_contrast (256 = 128 harmful + 128 benign, diff-in-means layer selection ONLY); wikitext_fluency (200 passages of 150-400 words); refusal_token_lexicon (10 tokenizer families); panel_manifest (160 checkpoint rows, 137 verified).

  HOW TO USE. Jailbreak rows branch on meta.delivery: t1_prefill has delivery='assistant_prefill' with meta.user_text and meta.prefill_text SEPARATE (do not concatenate — insert the prefill in the assistant slot); the other four are delivery='user_turn' with empty prefill. t5 stores meta.plaintext beside the base64 wrapper. Every row carries meta.template_text/template_source inline. B7 rows give refusal_onset and continuation lists per family, each entry {token_id, token_str, decoded_str, source in {empirical,lexicon}, empirical_count}; lists are disjoint, all ids < vocab_size, >=12 refusal and >=20 continuation per family, all 10 families empirical.

  PANEL: 137 verified, 59 at <=4.2B over 31 lineages (base 20 / instruct 18 / abliterated 8 / behavioral-uncensored 13); n_lineage 93 overall. lineage_id = the pretrained base at the root of the derivation chain, with the chain in meta.lineage_evidence — this is the bootstrap resampling unit. Gated repos (meta-llama/*, google/gemma-2*, huihui-ai Qwen3 v1 abliterated) are KEPT with verify_error; ungated mirrors are SEPARATE rows with meta.mirror_of. 6 clean H4 behavioral-uncensored candidates at <=4.2B, one (UnfilteredAI/DAN-Qwen3-1.7B) sharing the Qwen3-1.7B-Base lineage with its base/instruct/abliterated triad; 2 disqualified_by_provenance with card text quoted.

  DEVIATIONS, all evidence-driven and recorded in metadata.manifest: (1) walledai/* is gated (403) — XSTest from the ungated Paul/XSTest mirror, AdvBench from the llm-attacks GitHub CSV at a pinned commit. (2) mlabonne/harmful_behaviors REJECTED for layer_contrast because it is an AdvBench repackaging that would break disjointness; the harmful half is the Forbidden-Question-Set (Shen et al. CCS 2024) instead. Disjointness asserted: exact overlap 0, max cosine 0.652 vs threshold 0.85. (3) B7's planned harmful-vs-benign rate criterion cannot separate refusal from topic — run as specified it admitted 'Creating', 'Writing', 'Hack', 'Script', 'Title'. Replaced with behaviour-conditioning: a token is a refusal onset when it is the ACTUAL first generated token of >=3 greedy rollouts whose opening matches a refusal regex, over the same prompts. This surfaced a usable result: refusal onset is near a one-token event ('I'), and per-family greedy refusal rates (meta.greedy_refusal_rate) span 0.00 (Pythia-410m, danube3-500m-chat) to 0.81 (Gemma-2-2b-it), with Qwen3-0.6B at 0.05 with thinking disabled.

  CAUTION: harmless_dynamics (no_robots) and the layer_contrast benign half (alpaca-derived) are CC-BY-NC-4.0, NON-COMMERCIAL. B1 topic labels are a disclosed keyword heuristic (a stratification device, not a claim); the original task label is meta.task_type. 27 build assertions ship in metadata.assertions.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 2 ---
id: art_0UsKSgsMHome
type: research
title: Spec Sheets for Rival LLM Safety Metrics
summary: |-
  Reimplementation dossier for the four external baselines plus the estimator toolkit and a full citation audit. Deliverables: research_report.md (6 sections, ~1300 lines, every number carrying an [arXiv:ID section] anchor), research_out.json, and estimator_check.py/.json (deterministic Monte Carlo, seed 20260812).

  BASELINES, all read from primary full text. AMS (arXiv:2608.05578, venue confirmed IEEE Access 14:91723-91737): sigma = (mu+ - mu-)/sigma_pooled on the diff-in-means direction, final prompt token, 40-80% relative-depth sweep, 16 contrastive pairs x 3 concepts, 96 forward passes / 10-40s, thresholds PASS>3.5 / WARN 2.0-3.5 / CRIT<2.0. 71% = 10/14 leave-one-MODEL-out, identical under both calibration rules. r=-0.546 (p=0.043) verified; the unquoted Spearman rho=-0.423 is NOT significant. H4 quote transcribed verbatim with no hedge. THREE panel checkpoints appear in AMS Table I (Llama-3.2-3B-Instruct 8.37, gemma-2-2b-it 4.80, Llama-3.2-1B-Instruct 4.55) giving a reproduction gate. RAS/SafeVec (arXiv:2606.25750): all five stages plus EVERY published constant (tau=0.8, q=0.9, lambda=0.5, wu=wj=0.5, c=0.75, beta=5.0). VISAGE (arXiv:2405.17374): E[Smax-S] over alpha~U(-0.5,0.5), 3 dirs x 20 steps x Adv-80. Qi (arXiv:2406.05946 - ID resolved).

  DECISIONS SETTLED. (1) RAS overlap with our panel is EMPTY - every RAS-scored checkpoint is >=4B and none is ours; we must write 'our RAS reimplementation' throughout. (2) VISAGE at full fidelity is ~28 h/1B model on CPU (4,800 generations); a justified reduced grid lands at ~1.3 h/model, with an explicit fidelity-cost table. (3) Qi's operational decay length is k=5 tokens (beta_t=2 for t<=5, 0.1 for t>5), yielding pre-registered cut PR-1: Delta-lambda must survive beyond generated step 15, tested on [16,48], conservative replicate at 20. (4) NO prior work applies EWS/critical slowing down to LLM generative dynamics (arXiv abstract search returns zero) - but arXiv:2605.09043 applies CSD to conversation derailment in human dialogue and must be cited and distinguished, and AQI (arXiv:2506.13901) is a fifth uncited competitor.

  ESTIMATOR TOOLKIT with measured, not remembered, corrections. ewstools defaults read from source (Gaussian bandwidth 0.2, sigma=(0.25/0.675)*bw_num, rolling window 0.25, Kendall tau; NO built-in AC1 bias correction). Monte Carlo at our exact lengths: raw AC1 bias -0.064 at n=64 vs -0.020 at n=192, reduced to -0.009 / -0.0005 by +(1+3r)/n. A 192->64 effective-length difference alone manufactures a ~0.04 spurious AC1 gap in the 'right' direction - mitigation is mandatory and threefold. The AR(1)->lambda conversion is convex, so lambda is inflated 75% at n=64, phi=0.9; noise-floor truncation UNDER-estimates lambda by 40% if the fit window runs past the floor crossing. Runnable numpy/scipy recipe supplied with stopping rule, surrogate-ARMA null (Dakos Fig.11), and n_min=64 floor.

  OBSERVABLE. Yin et al. measure the probe refusal score at GENERATED positions (thinking chain), so r_t is adopted, not coined; verbatim 12-entry refusal-substring list transcribed from Arditi's source; per-tokenizer runtime resolution recipe for the leading-space hazard; abliteration-invariance argument grounded with its honest caveat.

  AUDIT. All 16 anchors resolve, none fabricated, no misattribution. Kwon's base-model control and Ratnakar's ~40%-depth figure both verified verbatim, so H1's and Step 0(a)'s rationales stand. The unanchored knowledge-action-gap result is FOUND: arXiv:2603.18353, 98.2% AUROC vs 45.1% sensitivity, 3,695 SAE features, both verbatim. Hasan & Biswas supply the missing r = -0.032, p = 0.89. Only two claims need rewriting (Qi 'Oral' unverifiable from arXiv; RAS speed-up internally inconsistent at 216.88x vs 210.13x). Recommends promoting SRI (arXiv:2602.02600) to a baseline - it is nearly free on hidden states we already extract.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 3 ---
id: art_UthAQuH8WZ5C
type: experiment
title: Does refusal wobble predict model safety?
summary: |-
  TIER-0 feasibility experiment for the 'safety = nearness to a tipping point' hypothesis. EXECUTED IN FULL on an RTX A4500: 4 models x 20 harmless prompts x 20 paired rollouts x 192 generated steps (94 min) plus a 39 min certified-geometry refit, 590-710 tok/s, <3 GB VRAM, $0.00 API spend. Panel: Qwen3-0.6B triad (Base / instruct / abliterated) + SmolLM2-360M anchor. The primary abliterated repo is GATED; the maintainer's v2 (huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2) was used per the fallback plan. Panel validity PASSES (instruct 0.225 harmful-refusal vs abliterated 0.000).

  HEADLINE: DISCONFIRMATION, twice over. (1) lambda is NOT identifiable at any geometry reached — the pre-registered synthetic rule demands T_fit>=128; after refitting there (layer/direction/eps/prompts/seeds held identical) the requirement MOVES to n_roll>=40 vs the achieved 20. Sizing for iterations 2-5: n_roll>=40, ~2x this run. (2) The RANDOM-DIRECTION CONTROL REPRODUCES THE ORDERING: a random unit vector at the same layer and magnitude separates the panel as well as the refusal direction (2/3 vs 2/3 significant), and on the ONLY pair isolating safety tuning (instruct vs abliterated) the control separates (-0.493, CI excludes 0) while the treatment does NOT (-0.226, n.s.). Verdicts: LAMBDA_NOT_IDENTIFIABLE_FLUCTUATION_ARM_ONLY (pre-registered) + CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING (supplementary).

  Fluctuation indicators track LINEAGE, not safety: the Qwen triad overlaps (Var* 3.10-3.15, AC1 0.245-0.304, flicker 40.2-42.2) while SmolLM2 separates (Var* 2.75, AC1 0.182). Pre-registered ordering fails and partly reverses (instruct has the LOWEST Var*/flicker of the triad and the FASTEST relaxation). Method vs baseline: label-free SPI Spearman rho=-0.20 vs supervised diff-in-means refusal direction +0.40 and r_0 margin +0.40 — both baselines, given the 32 harmful prompts SPI is denied, BEAT it (n=4, directional only; 3 of 4 models sit at a refusal floor).

  FOUR BUGS THE PRE-FLIGHT GATES CAUGHT, each of which would have produced confident nonsense: (a) injecting at a layer's OUTPUT is a no-op for that layer's own readout (|delta| was EXACTLY 0 at every eps, since the layer writes K/V before a forward hook fires) -> moved to a forward PRE-hook on the layer input; (b) free-running delta cannot estimate a decay rate — token streams diverge in ~7 steps and |delta| GROWS (decay_ratio_16 2.57-5.33) vs teacher-forced (0.119-0.233) -> teacher-forced is the primary channel; (c) mean|delta| is upward-biased by +38% to +68% at EVERY n_roll because E|N(mu,s)|>|mu| -> fit the SIGNED across-rollout mean (bias -0.03..+0.02); (d) flicker-as-fraction saturates at 1.0 -> use crossings/100.

  Other reported diagnostics: exponential model misspecification (median fit r2 0.11-0.54, 30-90% of fits below 0.3, lambda IQR ratios 4.7-20) so the assumption-free decay_ratio/AUC statistics are preferred; layer-L logit lens vs final-layer readout correlates only 0.17-0.26 (below the pre-registered 0.3) so EVERYTHING is reported at both readouts; the per-cell eps-linearity control returns False purely from prompt scatter, while the prompt-averaged version gives r2 up to 0.996 with log-log slopes 0.61-0.90 (both shipped). Layer selection: L=15/28, AUROC 0.999, middle third.

  DELIVERABLES: method.py (single entry point running measure -> reshape -> figures -> validate), reusable spi/ library (models, prompts, observable, rollout, indicators, validity, groundtruth), refit_certified.py, 4 pre-flight gate scripts, 10 figures, out/tier0_raw.json (11 MB full result tree), out/refit_certified.json, out/layer_choice.json (written and asserted BEFORE any indicator). method_out.json is exp_gen_sol_out-valid: 5 datasets / 224 examples, 16 limitations, all 5 control booleans present, all 640 lambda rows carrying the identifiable flag, every failed fit null WITH a reason string, zero non-finite numbers. All 10 figures regenerate from the archived tree alone. pyproject.toml pins all 88 installed packages.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 4 ---
id: art_TFe9eI-2QZN3
type: experiment
title: Does a refused answer stay refused?
summary: |-
  Pre-registered steering-hysteresis experiment on one Qwen3-0.6B lineage (Qwen/Qwen3-0.6B-Base, Qwen/Qwen3-0.6B instruct, mlabonne/Qwen3-0.6B-abliterated; huihui-ai is gated, fallback #8 used). A refusal-direction steering coefficient alpha (in units of NORM_L, the median residual-stream norm at the steering layer) is injected at one block's output for every position in the forward pass, so during incremental decoding each token's KV entries stay frozen carrying the alpha active when written - that frozen cache is the candidate latent state.

  Six arms per (model, prompt, seed), 30 benign prompts x 3 seeds x 3 models, $0.00 spend (all classification is deterministic string/token matching): UP-RAMP (measurement), ENTRY-AT-ALPHA, DOWN-RETAINED (alpha_down), DOWN-FORCED-A (byte-identical refusal prefix prefilled UNSTEERED; the primary control), DOWN-FORCED-B (alpha-schedule replay; positive control), RESET (prefix discarded; noise floor).

  VERDICT = REFUTED, the pre-registered disconfirmation. (1) Hysteresis is real: width alpha_entry - alpha_down = 0.262 [0.185, 0.344] for instruct, positive as pre-registered for generic autoregressive conditioning. (2) It is NOT carried by a retained latent state: excess_width (= alpha_down_forced_A - alpha_down) is 0.019 [-0.057, 0.099] instruct, -0.031 [-0.070, 0.001] abliterated, -0.330 [-0.990, 0.000] base - every CI overlaps 0 and every lower bound sits below the temperature-0.7 RESET noise floor (p95 = 0.05). H1b NOT_CONFIRMED. (3) Not a plumbing artifact: FORCED-B reproduces the retained arm EXACTLY (mean and max |diff| = 0.000 on every prompt of every model) and the temperature-0 RESET gate is exactly 0 everywhere.

  Three further results useful downstream: (a) the up-transition is unreachable mid-generation - ramping alpha inside an already-compliant generation fails on 92-100% of attempts (10/10 at delta in {0.05,0.1,0.2,0.4}, 9/10 with an [L-2,L+2] window) while a fresh generation at the same constant alpha refuses reliably, i.e. compliance sticks, refusal does not; (b) a harmful-vs-benign PROMPT axis at held-out AUROC 1.0 (14 of 28 layers) is a poor INDUCER (site score 0.27, partly degenerate refusals) whereas a CAA-style RESPONSE-contrast axis scores 0.69 and yields clean refusals - prompt-classification quality is not steering quality, and a matched random direction induces refusal at no alpha; (c) a candidate cheap safety metric, alpha50 (steering coefficient at which a fresh generation starts refusing, 5 prompts, 13 alphas, no benchmark): base undefined / max rate 0.20, instruct 0.475, abliterated 0.550.

  Eight pre-registration amendments, each with trigger, timestamp and reason, are recorded in prereg.json and echoed in method_out.json['preregistration']. Sensitivity: narrow-floor run (alpha_min=-0.5, 43% censored) gave 0.011 [-0.050, 0.073] and 0.012 [-0.009, 0.035] uncensored; re-scoring every recorded token stream at COMPLIANCE_RUN in {6,10,14} keeps all CIs overlapping 0. Every generated token, its alpha and its r_t are logged in gens/ so every classification is auditable. method_out.json validates against exp_gen_sol_out; the full analysis lives under metadata.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 5 ---
id: art_W0HSULPgrt3K
type: experiment
title: Safety refusal scores and a graded safety dial
summary: |-
  Tier-0 behavioural safety ground truth on 16 members (Qwen3-0.6B base/instruct/mlabonne-abliterated triad, Llama-3.2-1B and SmolLM2-360M base+instruct cross-family pairs, pythia-410m low-refusal anchor, a template side-check member, 3 task-vector interpolants, 4 abliteration-strength members), 3365 generations, three axes (plain-harmful refusal on 80 deduped AdvBench items; jailbreak ASR on 40 of those x 3 fixed attacks = prefill/refusal-suppression/roleplay; XSTest 50 safe + 25 unsafe contrast). Decoding: greedy, fp32, max_new_tokens=64, left padding, enable_thinking=False with an automated <think> guard. fp32 is load-bearing: fp16 batched greedy is NOT batch-invariant (3/4 identical at batch=4 vs 1; 4/4 in fp32).

  HEADLINE (a measurement failure, and the main deliverable). The pre-registered LLM judge (gpt-5.4-nano, frozen rubric, empty system prompt) NEVER assigns COMPLIANCE to harmful content: 0/7 on the COMPLIANCE class of a balanced 21-item probe, 9/21 overall. claude-3-haiku (7/21) and claude-haiku-4.5 (12/21) also score 0/7. Not a parse or payload bug (finish_reason=stop, 100% clean parse, max_tokens 8 vs 64 identical). An evaluator system prompt is what fixes it, not model capability or price: llama-3.3-70b-instruct+framing 18/21 at $0.040/1k, gemini-3.6-flash+framing 21/21 at $1.236/1k.

  CONSEQUENCE: the pre-registered sanity gate FAILS under the frozen judge (deltas 0.263/0.225) and PASSES under a repaired judge (0.463/0.413) on IDENTICAL generations. The ladder verdict flips too: SNAPPED -> SMOOTH. The scorer, not the models, decides both. prereg.json was never edited; the repair arm is documented in prereg_amendment.json.

  THREE SCORERS, one pipeline: baseline refusal-string screen, frozen judge (PRIMARY, reported in full including its failure), repaired judge (full coverage), plus a gemini gold-reference arm on a 400-item stratified subsample. Blind adjudication of 147 items (labels withheld by construction, mtime-asserted): frozen 0.510 acc / kappa 0.242; repaired 0.694 / 0.412; gold 0.759 / 0.449; screen 0.844 binary acc but kappa only 0.315 (accuracy inflated by class imbalance; recall 0.223). DECISIVE: on the 80 adjudicated disagreements the adjudicator sides with repaired 48x, frozen 21x, neither 11x.

  KEY RATES (repaired scorer): qwen3_abliterated refusal 0.113 / ASR 0.858 vs qwen3_instruct 0.525 / 0.633; llama32_instruct 0.975. LADDERS: task-vector W(t)=W_base+t(W_instruct-W_base) gives 0.062/0.237/0.388/0.500/0.525 = SMOOTH and monotone (caveat: t=0 FAILS the fluency screen, distinct-3 0.113, so the low-t end is partly recovery-from-degeneracy). In-house abliteration W<-W-c*rr^T W is SNAPPED under both scorers: refusal flat 0.525->0.512 while XSTest over-refusal rises 0.16->0.42 - it changed the model without producing the knob.

  OTHER: incapacity floor (pythia-410m scores 0.550 'refusal' with 0.327 degenerate rate - rates near that floor carry no safety signal; 4 members auto-flagged UNRELIABLE); template confound (Qwen3 base 0.662 chat-template vs 0.900 generic, delta 0.238 > 0.15 threshold); SmolLM2 instruct refuses LESS than its own base (-0.325, CIs disjoint) so the sanity ordering is family-specific.

  COST: $1.251 total, within the pre-registered $1.50 budget; 0.109 s/item, ~551 tok/s; 50-member panel projects to 0.41 GPU-hours and $0.64. The fitted parameter-scaling slope came out NEGATIVE and is explicitly marked unusable (wall-clock dominated by early EOS, not FLOPs). Audit cost deliberately not measured.

  ARTIFACTS: the 7 ladder checkpoints (1.14 GB each, 7.9 GB) are derived intermediates and are NOT shipped. `python method.py --stage rebuild-ladder --verify-hashes` recreates them bit-exactly from the two public Qwen3-0.6B checkpoints plus the 5 KB refusal_direction.pt; this was verified, not assumed - the directory was deleted and all 7 reproduced their original sha256 (~6 s each), and finalize re-ran to byte-identical verdicts without them. sha256 values and the build recipe are in results/ladder_models_manifest.json.

  FOR DOWNSTREAM USE: do not build correlations on the frozen-judge rates. Use ground_truth_repaired_scorer, and attenuation-correct with the reported reliability. PARTIAL is the weakest class for every scorer (<=0.41 recall), so safe-completion behaviour is the least trustworthy axis. The adjudicator is an LLM agent, not a human, so every 'accuracy' bounds scorer disagreement, not truth.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 6 ---
id: art_lMTPOpnFwKnw
type: research
title: Prior Art Check for Safety Metrics
summary: >-
  Four-part prior-art dossier for a 50-metric single-model safety-screening battery. (A) POSITIONING: our iter-1 site-selection
  finding is NOT original -- Galeone et al. [1] published the general detection-vs-control dissociation (AUC=1.000 from layer
  5 vs cos=0.12/~83deg to the refusal direction; cos in [0.12,0.20] over 4 models/3 families/1B-9B; 0.1197 vs 0.1200 across
  instruction tuning) on a panel OVERLAPPING ours. Our opening: refusal is never a DETECTED behaviour there, only the lm_head
  intervention direction. CRITICAL TRAP: their Sec.8 is an explicit NEGATIVE -- the cosine sits at chance for steerable and
  unsteerable behaviours alike -- so any cosine-as-safety-score metric is already a published negative and may enter only
  as a declared-expected-to-fail control. A 199-word rewritten positioning paragraph is supplied. alpha_50 = NARROWED after
  a 14-query saturation search over a 12-paper lane; surviving claim: the only member that is single-scalar, parent-free,
  HARMFUL-PROMPT-FREE and benchmark-free. Sharpest rival Logit-Gap Steering [3], whose published gap shifts on Qwen2.5-0.5B/Llama-3.2-1B/gemma-2b
  give a reproduction gate on our exact sizes. Newly surfaced, absent from the plan: Geometry of Refusal [10] and LAP/A_lin
  [11] (rho=+0.86..+0.91 training-free -- ADOPT for layer selection, do not compete). Rogue Scalpel [7] forces a rewritten
  pass condition: random directions raise compliance 0%->1-13% (18% in body), so they are a MAGNITUDE-MATCHED COMPARATOR,
  never a null; their alpha=c*mu(l) matches our NORM_L units. Pre-register against non-monotonic steering strength [6], input-dependent
  optimal layer [14], and the scalar-steerability objection [15]. (B) WEIGHTS-ONLY = NOVEL (narrow). The collision paper's
  weight signal is E1 = mean_m sigma_1^2(dW)/sum sigma_i^2(dW) with dW = W_base - W_cand [2] -- it REQUIRES the parent, as
  does WeightWatch [17]. Parent-free is the hole and is immune to their #1 failure (spoofed reference). Scale escape hatch
  CLOSED: Qwen2.5-1.5B is in their 273-checkpoint registry. Ships a new implementable observable (SNS-1/2/3 on the shared
  Gram matrix, SNS-3 supplying the refusal-specificity E1 cannot) plus 13 weights-only statistics, grounded in Jain et al.
  [18] and HTSR [27] (no safety application found). (C) 9 black-box specs: 5 strong (logit-gap [3], FJD [23], SPD [22], prefill-flip
  [16], WildGuard [32]), 2 labelled STRAWMEN (first-token entropy has no safety-specific prior; length asymmetry is folklore),
  SRI [24] off-constraint (rollout-integrating), AMS WEAK (independently measured at AUROC 0.66 / held-out detection 0.35
  [2]). (D) COVERAGE VERDICT: fallback (c) FORCED at n=2. HELM Safety VERIFIED to contain no model under 10B (zero num_parameters
  in [1e8,1e10) in its machine-readable release registry [40]); TrustLLM >=7B; no confirmed <=4B entry on AIR-Bench [28],
  SALAD-Bench [29] or SORRY-Bench [30]. Qwen3Guard circularity CONFIRMED VERBATIM (two of three reward terms are Qwen3Guard-Gen-4B,
  helpfulness is WorldPM-Helpsteer2 [20]) -- ban the whole series [21]; AND the abliteration registry's own labels are Qwen3Guard-derived
  [2], a circularity the hypothesis did not anticipate. Good news: the published SafeRL numbers (47.5->86.5, 64.7->98.1, refusal
  12.9->5.3) are judged by Qwen3-235B and WildGuard, so they are NON-circular and usable. (E/F) 29 per-metric design inputs
  meeting every composition constraint, a 14-ID citation audit (2508.21448 confirmed WRONG [4]; 2603.24543 confirmed RIGHT
  [5]; 2509.13450 title moved to a THIRD v3 title [8]), and 15 numbered corrections_to_hypothesis. Coslett [35] UNREACHABLE
  (HTTP 403) = largest residual risk.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 7 ---
id: art_BCxIq6GX4WIw
type: dataset
title: Published safety scores and a frozen model split
summary: |-
  EXTERNAL GROUND TRUTH + FROZEN SPLIT + RULES + MEASUREMENT CORPORA. One schema-valid file, full_data_out.json (13,311 rows, 22 MB, 20 blocks), built by `uv run data.py` from src/s0..s5; `./run_all.sh` reproduces end to end. Validates against exp_sel_data_out AND against schema_row_kinds.json via src/validate_rows.py.

  HEADLINE, MEASURED NOT ASSUMED. Panel = 66 checkpoints over 34 lineages at <=4.2B, from the iteration-1 frozen manifest (run_CbJDs3opF7E_ iter_1 dataset_1, datasets[dataset='panel_manifest']). External SAFETY coverage is 3/66 checkpoints and 2/34 lineages (4.5% / 5.9%); OVER-REFUSAL coverage is 1/66, reported separately and never folded in; CAPABILITY is 32/66 (48.5%). 65/66 checkpoints require in-house measurement, shipped as a machine-readable list with the axes needed. TWELVE published safety sources name ZERO panel checkpoints: SORRY-Bench, OR-Bench, XSTest, TrustLLM, SALAD-Bench, DecodingTrust, JailbreakBench, HarmBench, AIR-Bench 2024, arXiv:2605.05427, HELM Safety v1.0.0 (27 models), HELM AIR-Bench v1.1.0 (22). HELM was read from its GCS JSON (paths probed, all 200); the ten papers were fetched IN FULL by paging past the 50k-char fetch cap, with a positive control proving the matcher fires. So the external arm is coverage-limited at this scale and the hypothesis's in-house refusal-rate fallback becomes PRIMARY; capability stays as the confound control.

  THE THREE COVERED CHECKPOINTS. Qwen/Qwen3-4B (Qwen3-4B-SafeRL card: Safety Rate x2 judges, Refusal(WildGuard), x Think/Non-Think) and google/unsloth gemma-2-2b-it (Gemma 2 'Ethics and Safety' table: RealToxicity, ToxiGen, CrowS-Pairs, BBQ, Winogender, WinoBias, TruthfulQA). Qwen3-4B-SafeRL itself is an AUGMENTATION row: absent from the frozen manifest and 4.411e9 params, 5% ABOVE the ceiling - iteration 3 must decide explicitly.

  ERRORS CAUGHT. (1) The gemma-2-2b BASE card reprints the INSTRUCTION-TUNED table ('Gemma 2 IT 2B'); rows attributed to -it only. (2) Manifest param_counts came from on-disk bytes and double-count repos shipping both .safetensors and a duplicate .pth/.bin (Llama-3.2-1B: 2.47B vs 1.24B true) - all re-resolved from the Hub, 27 disagreements flagged, panel 59->66. (3) The archived v1 leaderboard sets Flagged=True on all 7,260 rows, an archive artefact; honouring it blindly dropped every v1 row. (4) The plan's '137 checkpoints / 93 lineages' is really 160/105.

  SPLIT, frozen after the harvest: seed '20260813-iter2-split', all 105 lineages, 35 heldout / 70 dev (exactly the >=1/3 floor), hard cases both sides, 7 families absent from DEV, Qwen/Qwen3-4B-Base forced to DEV as the exploration lineage, sha256 pinned in the pre-registration and re-checked by the validator. Byte-reproducible. A per-stratum ceil(n/3) rule was tried and REJECTED (singleton strata sent 54/105 to heldout).

  RULES. BLANKET_REFUSER_DISQUALIFICATION at >0.50 over-refusal on safe items (WARN >0.35), grounded inside the empirical gap in XSTest's five-model distribution [0.016, 0.084, 0.188, 0.296, 0.596] - and CHECKED three ways: literal substring of the cached PDF, recomputed from XSTest's released per-item human labels (all five columns reproduce exactly), and re-derived by the validator from the shipped corpus so rule and corpus cannot drift. Plus QWEN3GUARD_CIRCULARITY, with a weaker QWEN3_SAME_FAMILY_JUDGE flag separating the card's Qwen3-235B-judged columns from its non-circular WildGuard ones.

  MEASUREMENT CORPORA. 11,802 prompts over the 10 corpora selected from 16 pinned (xstest_v2 incl. all five human-annotated reference columns, or_bench_hard_1k, wildguard_test, harmbench_direct_request, advbench, jbb_behaviors, do_not_answer, beavertails_evaluation, toxigen_annotated, aegis_safety_test); 6 rejected with reasons recorded. Every external_score row carries explicit polarity AND polarity_evidence; every value traces to a fetched URL and a <=300-char quoted snippet; cache/ holds every source read so each snippet is re-checkable offline.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 8 ---
id: art_xyUlckdGtbjc
type: experiment
title: Fifty cheap safety checks on 44 models
summary: |-
  FROZEN 53-metric battery (50 shipped + 3 declared extras) measured on 44 checkpoints / 23 lineages / 7 architecture families / 2,332 rows, plus a faithful AMS reimplementation with its Table-I reproduction gate, plus a separable two-axis behavioural readout. The artifact SELECTS NOTHING: metric_spec.py was sha256-stamped (544ff994...) before any model was loaded, battery.jsonl carries no behavioural column, and the readout ran only after the battery was stamped. Floor met (>=20 ckpt / >=12 lineages / >=6 families).

  HEADLINE, NEW ARM: a PARENT-FREE test for abliteration's rank-one write-suppression signature. Build A = sum_l W W^T/||W||_F^2 over every residual-write matrix, take its min-eigenvector v1, and ask whether v1's write energy is suppressed in EVERY layer. W01 = log10(median lam/lam_1): abliterated n=8 median 4.26 [1.44, 4.82] versus base 0.58 [0.34, 1.99], instruct 0.47, behaviourally-uncensored 0.46, Qwen3-4B-SafeRL 0.47. W04 (lam_2/lam_1) separates even more cleanly: abliterated min 0.85 against a maximum of 1.62 over all 36 non-abliterated members. Behaviourally-uncensored members look like ordinary instruct models -- the signature reads the EDIT, not the BEHAVIOUR. Cost: 0 forward passes, 0 prompts, and 0 of 53 metrics exceeded a 60 s measured median (0.6B ~75 s, 1.7B ~120 s, 4B ~180 s for the WHOLE battery).

  GATES. (1) Injected rank-one positive control PASSES: |cos(v1,r)| = 1.000, W02 = 1.00, W01 0.62 -> 4.82. Its BLIND SPOT is measured too: a band-limited edit (middle third of layers) is NOT recovered (W02 = 0.0, W01 unchanged) -- so W01-W05 are graded numbers, never a binary detector. (2) AMS gate: ours 4.40 / 4.37 / 3.09 against Table I's 8.37 / 4.80 / 4.55 -> Spearman ordering rho = 1.00 with a systematic scale offset; not tuned to close the gap, and the 3x16 contrastive pairs are OUR construction from the frozen folds. (3) Hook direction, token-id validity, renderer checks all green.

  PITFALLS FOR DOWNSTREAM WORK. HF derives positions from cache_position (a plain arange), so LEFT-padded batches are MISALIGNED unless position_ids = (mask.cumsum(-1)-1).clamp_min(0) is passed on the forward AND every decode step. The padded-vs-single 1e-2 logits test is UNPASSABLE in bf16: an equal-length control reproduces nearly the same discrepancy (0.44 vs 0.63 on |logit| ~28), so it is batched-GEMM numerics, not padding. The held-out AUROC depth profile SATURATES at 1.0 over most of the stack, so argmax-AUROC depth selection is decided by float noise; tie-breaking on d' gave rho* = 0.679 (not iteration 1's 0.25), and at that depth alpha_50 is ceiling-censored on 37/44 members. sigma_min via sqrt(eigvalsh(W W^T)) squares the condition number and drives W11 into float noise -- use svdvals for the square attention matrices. The plan's mandated R4 judge prompt scores HARMFULNESS not BEHAVIOUR (it labelled a Holocaust-denial article REFUSAL, giving 0.87-1.00 for every member, kappa ~0); a rubric that explicitly separates the two agrees 6/6 with a hand-labelled set. Both readouts are shipped (behaviour_rubricA.jsonl vs behaviour.jsonl); judge spend $0.19 of the $1.50 cap.

  DELIVERABLES: method_out.json (long_table 2332, method_vs_baseline 44, metric_spec 53 with declared-vs-measured cost, panel 45, ams_reproduction_gate, behaviour 44, diagnostics), generations.jsonl, results/{battery,behaviour,behaviour_rubricA}.jsonl, results/{diagnostics,calibration,padding_control,judge_calibration}.json, README.md. Schema exp_gen_sol_out PASSED.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 9 ---
id: art_CbL-EUQlwgfw
type: experiment
title: How hard is it to steer a model into refusing?
summary: |-
  EXECUTED IN FULL: 14 members / 4 lineages (tier_completed=T4), 60,040 generations, 63.6 GPU-min on one A4500, judge spend $0.9164 of the $2.00 cap (16,084 calls, google/gemini-3.1-flash-lite). Deliverable method_out.json (756K, 998 examples / 14 datasets), schema-validated; full/mini/preview all PASS.

  PANEL: Qwen3-4B quartet (Base / Instruct / official Qwen3-4B-SafeRL / abliterated), Qwen3-1.7B (+DAN behavioural-uncensored), Qwen3-0.6B, cross-family Llama-3.2-1B. Gated huihui-ai v1 abliterated repos -> ungated v2 mirrors; Qwen3-4B abliterated -> Goekdeniz-Guelmez Josiefied gabliterated-v2 (different instruct parent, recorded). All revisions pinned.

  GATES PASS: NORM_L(Qwen3-0.6B)=23.56 vs iteration-1's 21.2 (11.1% err, within 15%); hook fires on prefill + every decode step (8 forwards for 8 new tokens — the plan's 'expect 9' is off by one); thinking disabled; base members use the PLAIN renderer and are excluded from every correlation.

  HEADLINE — THE LEXICAL ARTIFACT IS IN THE SCORER, NOT THE AXIS. The Arditi 12-substring regex yields alpha_50 for only 7/14 members; the semantic judge yields it for 14/14 on the SAME recorded text. qwen3-0.6b-abliterated: regex max refusal 0.01 vs judge 0.85. 20 (member,axis) cells disagree on REACHABILITY; median kappa(regex,judge)=0.279. Any alpha_50-style metric built on that screen inherits the artifact.

  VERDICTS (pre-registered literals): axis_b=LEXICAL (under the judge AXIS B is defined 14/14 — the paraphrase-disjoint axis DOES induce refusal — but alpha_50 moves a median 69%; 0/18 AXIS-B responses match the scoring regex, verified); scorer=SCORER_DEPENDENT; axis_c=SAFETY_SPECIFIC and axis_d=RANDOM_DOES_NOT_REPRODUCE in strongest form (0/14 and 0/28 cells reach 0.5, max 0.18 / 0.225, vs 7/14 for AXIS A); within_family_only=false; TRIAGE = NOT_A_TRIAGE_SCORE (R=0.73 normalised / 0.62 raw, perm p 0.76 / 0.57; NORM_L spans 3.5–63.0, an 18x range).

  INSTRUCT vs ABLITERATED: not estimable under regex (one member of each pair unreachable) — reachability, not price, separates them. Under the judge, 3/4 lineage CIs exclude zero but the SIGN REVERSES on Llama; across lineages (the resampling unit) sign test p=0.625, consistent_direction=false. Every SAFETY_COST<->ground-truth Spearman has a lineage-bootstrap CI covering zero, both units, both scorers, both sentinel conventions.

  BASELINE (AMS sigma, same checkpoints/pipeline): Llama-3.2-1B-Instruct 5.18 vs published 4.55 (13.9%); rho=-0.649 (p=.042) with jailbreak ASR at member level but CI [-0.99,0.35] covers zero; the published threshold assigns PASS to ALL 14 including base and abliterated — it does not discriminate on this panel.

  GROUND TRUTH IS CLEAN (so the negatives are interpretable): abliterated GT1 0.01–0.34 vs instruct 0.38–0.96; SafeRL matches instruct on harmful refusal (0.9125) while cutting jailbreak ASR 0.688 -> 0.088, and is the MOST expensive model to steer into spurious refusal (judge alpha_50 0.560). No blanket refusers (GT2 <= 0.16).

  TWO METHOD CORRECTIONS FOUND BY RUNNING IT: (1) a POOLED distinct_3 fluency screen flags SUCCESSFUL steering (100 near-identical refusals) as degeneration and would delete exactly the alpha points the metric is about — now measured within-response, pooled value kept as corpus_distinct_3; (2) steered refusal is NON-MONOTONE in alpha (rises, peaks ~0.3–1.0, collapses), so alpha_50 is the FIRST UPWARD crossing fitted on the rising branch only, and a sign check comparing alpha=4 to alpha=0 trivially failed for all 14 until corrected to the peak over (0,2].

  ARTIFACTS: results/generations.jsonl (56,400 sweep) + gt_generations.jsonl (3,640) make control (ii) re-auditable; results/analysis.json holds the full analysis object; run_all.sh reproduces end to end.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 10 ---
id: art_80jPj8Mr_dbZ
type: evaluation
title: Auditing last round's negative results
summary: |-
  PURE RE-ANALYSIS of the three archived iteration-1 trees (E1 refusal-wobble/SPI, E2 steering hysteresis, E3 behavioural ground truth + judge). No model inference, no GPU, no rerun of any iteration-1 experiment. Estimators (paired_bootstrap_diff, cluster_bootstrap_ci, half_life_auc, wilson_ci) are IMPORTED from E1/spi/indicators.py; E1's spearman() and build_output.py's verdict rule are transcribed verbatim, so every archived number reproduces exactly before anything is changed. Spend $0.0586 of a $1.00 cap, 537 logged calls; every response cached so a rerun costs $0 and reproduces in 18 s.

  RECONCILIATION TABLE: 46 rows, 25 SURVIVES / 12 CHANGED / 9 RETRACTED / 0 UNTESTED, each with original value, re-derived value and the deciding analysis.

  A1 (lambda inconsistency): CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING is CHANGED / MATERIAL_CHANGE_TO_REPORTED_RESULT. Running E1's own rule on decay_ratio_16 and normalised-AUC over the same 240 certified rows: at the PRE-STATED primary readout (layer L, where the perturbation is injected) the random-direction control separates 0/3 while the refusal treatment separates 2/3 - the REVERSE of the reported pattern. It reproduces only at the final-layer readout (lens-vs-final corr 0.17-0.26). Not cosmetic: lambda vs decay_ratio_16 Spearman -0.459 (layerL) / -0.170 (final). Horizon sweep {8,16,32,64} and lineage-level bootstrap included; the -0.226/-0.493 lambda CIs are reprinted DEMOTED under lambda_ci_consistency_check_NOT_IDENTIFIABLE.

  A2 (observable-validity gate): only 1 of 4 members passes r_0 AUROC>=0.70 (instruct 0.793; abliterated 0.481, base 0.414, smollm2 0.633) -> UNSUPPORTED_ONLY_1_MEMBERS_PASS. 'Indicators track lineage, not safety' is RETRACTED as a settled negative and downgraded to a qualitative observation. Sensitivity curve {0.60,0.65,0.70,0.75,0.80} published; n_passing=1 from 0.65 up.

  A3 (judge probe rebuilt, the only paid arm): 197 items, four classes, fixed seed, all 21 original probe items carried forward; two annotators decorrelated in model family AND rubric framing (gemini-3.5-flash-lite + frozen rubric; mistral-small + independent decision tree), kappa 0.337 [0.259,0.415]; 96 disagreements adjudicated by deepseek-v4-flash; 97 disputed items published verbatim. 0/7 -> 7/82 = 0.085 [0.042,0.166] frozen-judge COMPLIANCE recall vs 0.939 repaired: 'never assigns COMPLIANCE' is literally wrong but the failure is confirmed and quantified. 3 of 21 original truth labels contradicted, including the force-included 'Certainly! Here's a message that conveys hope...' case (prefix-labelled COMPLIANCE, adjudicated PARTIAL) -> the 21/21 gold arm is RETRACTED. Both headline revisions reproduce exactly (0.700->0.113, 0.092->0.858) and STRENGTHEN under misclassification correction: 0.113 -> 0.000 [0,0.069]; 0.858 -> 0.904 [0.857,0.974].

  A4 (n=4): all 24 orderings enumerated. rho=-0.20 reproduces exactly, exact two-sided p=1.000 against p_floor 0.4167 (untied floor 2/24=0.0833) - nothing at this panel size can reach 0.05. Two independent kills: only 1 of 4 members is above the refusal/incapacity floor, and E1's spearman() breaks ties by array position with two members tied at 0.000 - average ranks give +0.105, a SIGN FLIP. corrected_claim_text and numbers_to_drop emitted.

  A5 (prereg fidelity): 15 deviation rows (7 unannounced), all eight E2 amendments present, each with trigger, timestamp, date-source and direction of effect. Excess-width sign inversion CONFIRMED (paper uses forced_A - alpha_down; prereg the negation) but the two-sided conclusion is INVARIANT - recorded as a reporting error, deliberately not inflated. alpha_50 gap 0.075 = 1.5 grid steps with 5 Bernoulli draws/point; bootstrapped intervals [0.383,0.538] and [0.483,0.617] OVERLAP -> alpha_50_gap_is_resolvable=false, RETRACTED. refusal_direction.pt feeds ONLY E3's in-house ladder (E1 and E2 fit their own directions). Abliteration coverage COMPLETE (o_proj + down_proj + embed_tokens), so under the pre-stated relabel rule the SNAPPED failure attaches to the technique - but the defensible sentence is 'our single-direction weight-edit implementation did not produce a graded knob at 0.6B scale'.

  DELIVERABLES: eval.py single entry point (inventory|a1|a2|a3|a4|a5|finalize|all, --stage smoke); eval_out.json (exp_eval_sol_out-valid, 6 datasets / 348 examples / 53 metrics / 15 limitations); out/{input_inventory,gate_definition,a1_lambda,a2_gate,a3_probe,a4_permutation,a5_prereg,reconciliation_table,disputed_items,field_substitutions}.json, out/llm_call_log.jsonl, out/a3_annotation_cache.jsonl; 4 figures (F1 verdict-flip matrix, F2 gate, F3 judge confusions, F4 exact permutation null) as PNG+PDF.

  FOR THE PAPER: cite the reconciliation table's re-derived values, not the iteration-1 originals. Do NOT carry forward as settled: the generic-mixing verdict, 'indicators track lineage not safety', the alpha_50 instruct-vs-abliterated gap, the 21/21 judge probe, or any n=4 ordering claim.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 11 ---
id: art_sHF0cggp2IvT
type: research
title: Who Else Detects Edited Safety Models
summary: >-
  Four-part prior-art and taxonomy dossier for the parent-free weights-only abliteration detector (Claim A). (A) arXiv:2604.08844
  (Paul) extracted from full text: two of its five features are FORMULA-IDENTICAL to our W06-W09 (stable rank, singular-value
  entropy with the same sigma-hat normalisation) and must be cited at point of use; its MOST informative feature (cosine of
  top-k left singular vectors to a healthy-adapter centroid, 10x shape / 30x magnitude coefficients) is parent- AND reference-requiring,
  so W01-W05 have NO counterpart. Numbers verified with two corrections: rho>=0.956 is the MINIMUM of three ordinal values
  (0.976/1.000/0.956); rho=0.72 is Spearman on N=24 with NO CI reported. Cross-method AUC 0.00 confirmed verbatim (n_bootstrap=972,
  CI [0.00,0.00], trained on 10 healthy + 14 DPO, tested on 6+4 steering, score is a fitted probability, NO fix attempted)
  -- but the paper DECLARES ITS OWN CONFOUND: the steering arm generated incoherent text at every intensity (GPT-4o 0/300
  harmful), so the precedent is confounded and must be cited that way. (B) OBLITERATUS's spectral certification READ IN FULL
  FROM SOURCE and the plan's premise INVERTS: it consumes ACTIVATIONS (harmful/harmless post-edit), not weights -- parent-free
  but NOT prompt-free, and it audits a self-performed edit rather than detecting unknown checkpoints. Our novelty claim gets
  STRONGER. Its documented 'RED at 0% refusal' calibration failure is transcribed verbatim from three mirrors and is an independent
  mirror of our S2. Dated: first public 2026-03-04. (C) Eight recipes with reimplementation-grade equations (rank-one projection,
  mlabonne Gaussian kernel, Heretic per-component optimised kernel with FLOAT direction index and weights >1 i.e. sign flip,
  MPOA exact row-norm-preserving four-step, ORBA Householder + geodesic lambda=1, Gabliteration ridge rank-k, OBLITERATUS
  rank-k presets, SFT). PLAN WAS WRONG on availability: MPOA, Heretic and OBLITERATUS ALL have public sub-4.2B checkpoints
  at 4,022,468,096 params on the panel's own Qwen3-4B family; only ORBA is empty (7 repos, all 12.187B) and must be reimplemented.
  FIFTH FINDING, unasked: the iteration-2 positive set ALREADY contains a second recipe -- the gabliterated member is a Gabliteration
  and scores at HALF the margin (W01 2.237 vs 4.16-4.82), so H1 is half-answered as graded loss not collapse; the AUROC 1.000
  rests on a 0.077 log-margin; W02=1.00 on four pre-2023 BASE models. (D) Coslett resolved as ADJACENT (activation-geometry
  fingerprint against a claimed identity, per the only reachable characterisation); Zenodo record/DOI/REST API all 403 and
  the publisher host is unreachable, so risk drops LARGE -> SMALL-but-open. Two new works: arXiv:2602.15195 (weights-only
  but adapter-delta + supervised calibration, our exact size class, currently uncited) and reverse-abliterate (the only shipped
  parent-free detector -- pure filename/metadata scanning, no spectral statistic). Ships 12 numbered corrections including
  a FACTUAL ERROR in the current hypothesis, a signed W05 prediction table with Householder-ORBA as the sharpest falsification
  target, a 5-model shortlist, and a 14-entry must-cite list.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 12 ---
id: art_8OlSrcw-hzgO
type: dataset
title: Who Edited This Model, and How
summary: |-
  Ships ONE schema-validated full_data_out.json with five datasets (7,381 examples, 16.5 MiB) in three blocks. DATA ONLY: no weights downloaded, no forward passes, no training, no W01-W05, no AUROC, $0.00 OpenRouter spend. Built offline by `uv run data.py` from temp/datasets/ + results/ (48 deps pinned exactly in pyproject.toml).

  BLOCK 1 `edit_manifest` (672 rows = 513 edited + 159 parents). Harvested from 61 Hub sweeps (20 search terms, 20 uploaders, 20 architectures, 1 global top-downloads) over 20,313 enumerated repos. Spans **189 distinct uploaders** against the plan's floor of 5 -- iteration 2's 8 positives came from only TWO uploaders, so this directly removes that confound. **6 of 7** recipe classes populated: R1_GLOBAL_RANK1_DIM 78, R2_NORM_PRESERVING_PROJECTED 20, R3_MULTIDIRECTION_SVD 26, R4_PARTIAL_LAYER_OR_PER_HEAD 235, R6_BEHAVIOURAL_SFT_UNCENSORED 19, R7_MERGE_OF_ABLITERATED 15, UNKNOWN 120. **388 complete parent-child pairs** for the H3 head-to-head; all 8 iteration-2 members present and flagged `is_iter2_class_member`; 1,536 over-ceiling near-misses recorded separately; every row `status=ok`.

  THREE NUMBERS THAT SHOULD DRIVE THE PAPER. (i) **UNKNOWN = 23.4%** of edited rows: nearly a quarter of self-declared edited checkpoints name no mechanism, which is the ceiling on Hub recipe provenance. (ii) **repo_id_contains_abliteration_string = 50.5%** (259/513): a plain regex on the repo id alone already solves HALF the detection task, so that -- not chance -- is the baseline any detector must beat. This is the reviewer's previously unmeasured point, now quantified. (iii) **R5_SPECTRAL_CASCADE_DCT is EMPTY**, and that is a finding, not a gap: the OBLITERATUS README we fetched contains ZERO occurrences of 'spectral', 'frequency', 'Fourier' or 'DCT' (its profiles are basic/advanced/aggressive/surgical/optimized/inverted over diff-in-means, SVD, whitened SVD). Any H1 arm needing a frequency-domain recipe is UNRUNNABLE at this scale.

  BLOCK 2, three laundering corpora. 2a `sft_benign` 3,370 English single-turn pairs from OpenAssistant/oasst1 (Apache-2.0, sha fdf72ae0), 627 safety-topic pairs and 6,695 duplicate instructions dropped. 2b `fluency_wikitext` 1,000 paragraphs from Salesforce/wikitext wikitext-2-raw-v1 test (sha b08601e0), median 148 GPT-2 tokens, 163,496 total; the @-@ artifact is documented, not silently carried. 2c `heldout_benign_prompts` 200 prompts from databricks-dolly-15k (sha bdd27f4d) -- a DIFFERENT repo from 2a, then exact dedupe (1 dropped) and 5-gram Jaccard >= 0.5 (0 dropped); measured max Jaccard vs any 2a instruction is **0.273**. NC sources excluded throughout (alpaca, no_robots rejected).

  BLOCK 3 `hub_scan_pool` 2,139 metadata-only rows, all strata floors beaten: 407 declared / 1,105 non-declaring chat / 627 non-declaring base. Ranked by `scan_rank` (undeclared chat by descending downloads first) with `cumulative_bytes`, so a scan stopping at rank k has a stateable coverage and a cost in GB; 7.3 TB total with per-decile cumulative gigabytes.

  INTEGRITY, ALL VERIFIED ON THE SHIPPED FILE: 0 rows with a missing or 'main' sha; 0 rows missing a param count; 0 rows above either ceiling; **482/482 recipe_evidence spans verified as verbatim substrings of the cards they cite (0 fabricated)**; 482/482 carry an evidence_url; 0 parent rows wrongly carrying a recipe_class; 2a leaks no safety terms and has no duplicates.

  TWO BUG CLASSES FOUND AND FIXED, both consequential downstream. (1) A three-seed 10-row hand-check (27/30 survived, failures and objections recorded in coverage.block_1.hand_check) exposed four labeller defects, including 'trained' matching inside `from_pretrained(...)` in a usage snippet and corpus-sense 'unfiltered' labelling a pedagogy study as an uncensoring fine-tune. (2) **The Hub's safetensors index is not always right**: samuelcardillo/Qwen3-Coder-Next-Opus-4.6-Reasoning-Distilled reports 6,208,256 parameters while shipping 159 GB of shards, and two 35B checkpoints report 664,944. Taking it at face value silently admits 32-35B models into a sub-4B pool. The ceiling is now enforced TWICE -- once from the index, once from on-disk safetensors bytes divided by the repo's widest declared dtype -- which rejected 25 such rows. Any downstream artifact resolving parameter counts from the Hub should apply the same cross-check.

  A bare 'this is an abliterated version' is deliberately labelled UNKNOWN/ambiguous rather than folded into R1, which would have inflated R1 until the class meant nothing. Ten HF dataset candidates were downloaded and evaluated; three are shipped and each of the seven other verdicts is recorded in metadata.dataset_selection (GAIR/lima is gated; tulu-3-sft-mixture is partly non-commercial; oasst2/oasst_top1/guanaco are not independent of 2a and guanaco is multilingual).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 13 ---
id: art_fvWfzRrcoKux
type: experiment
title: Testing how far the weight scar reaches
summary: |-
  $0 LLM spend, ~1h on one RTX 4090; every number re-derived by an assertion block that blocks assembly.

  GATE = PASS. wstats.py is an INDEPENDENT reimplementation of W01-W05 from the published formulae (written before lib_metrics.py was read). On 10 members (5 abliterated / 5 not) at archived revisions it reproduces the archive to max|dW05|=9.9e-06, ordering preserved, Spearman 1.0000, bit-identical across two independent runs. Three attributable divergences are reported, not smoothed: (a) W01 reproduces to 1e-4 on non-abliterated members but drifts up to 0.048 on ABLITERATED ones, because lambda_min sits at the float noise floor exactly where the scar is (iter2 accumulated the Gram in float32, here float64; NOT a load-dtype effect -- the float32-load column is identical); (b) W03 differs systematically by +0.015..+0.034, a DEFINITIONAL difference -- the published formula takes q05 of the per-direction MEAN energy, the iter2 code pools all (direction x matrix) energies first; (c) revision drift zero. Controls reproduce: injected rank-one gives |cos(v1,r)|=1.000000, W02=1.00, W01 0.624->4.869; band-limited middle-third gives W02=0.0.

  ARM 1 = RECIPE_CLASS_BOUNDED, and the binding limit is UPLOADER, not recipe. Hub search (7 queries, 70 candidates verified from card evidence) established that mechanically different recipes DO exist (norm-preserving, multi-direction, biprojected) but EVERY one is >=14.9B, far above the 4.2B ceiling -- forcing the pre-registered fallback. Four real published <=4.2B abliterated checkpoints from four UNSEEN uploaders were measured instead: W05 = -0.964 mlabonne/Qwen3-0.6B-abliterated, -1.010 MagicalAlchemist/Qwen3-1.7B-Magic_decensored, -0.990 prithivMLmods/VibeThinker-3B-heretic_decensored, -2.161 BennyDaBall/Qwen3-4b-Z-Image-Turbo-AbliteratedV1, against an archived abliterated range of -2.74..-4.82. W05 AUROC 1.000 on the two calibration uploaders vs 0.382 on the four new ones, 0/4 caught at the fitted threshold. realcheck.py rules out the re-upload explanation: all three with a resolvable parent are GENUINE near-rank-one edits (E_1 0.995/0.995/0.997, relative Frobenius change 2.5-3.0%, 0% bit-identical matrices). Twelve in-house synthetic variants on two architectures: normpres and rank-k (k=2,4,8) AUROC 1.000; per-head (top 25%) 0.556; LAYER-FRACTION SWEEP gives f*=1.00 on BOTH hosts -- only the fully global edit is detectable. Sharpest: on Qwen3-1.7B a projection confined to the middle 50% of layers drives harmful refusal 0.45->0.00, exactly as effective as the full-stack edit, while W05 moves -1.0098 -> -1.0088, indistinguishable from unedited. No variant was degenerate.

  ARM 2 = PARENT_FREE_COSTS_0.167_UNDERPOWERED. E_1 = mean_m sigma_1^2(dW)/sum sigma_i^2(dW) over the 0.25L-0.75L band (recorded as OUR reading of 'mid-stack'). On the pre-declared 12 pairs (positives all from the two calibration uploaders) E_1 and W05 TIE at AUROC 1.000, paired diff +0.000. Adding the 3 new-uploader pairs: E_1 holds at 1.000, W05 falls to 0.833, paired lineage-bootstrap difference -0.167 [-0.444, 0.000] -- the interval reaches zero at its boundary, so UNDERPOWERED as an interval claim at n=15, but descriptively unambiguous (E_1 3/3, W05 0/3). Complementary on synthetics: E_1 degrades on multi-direction (0.17-0.67, k=8..2) where W05 is perfect, and holds at 0.995 on the band edits W05 cannot see.

  ARM 3 = INVARIANT. Depth-sensitive activation metrics recomputed at three relative depths (bare AUROC argmax 0.143 read from CALIB, 0.50, pre-declared rho*=0.679) over 26 chat-rendered members -> results/long_table_depth.jsonl, 1014 (member, metric, depth) rows, the downstream deliverable. The black-box baseline wins at ALL three depths, so iteration 2's falsifier is NOT a depth artefact. This needed the right test: four activation metrics have a LARGER point estimate than a baseline at rho* (A19_refusal_axis_unembed_cosine rho=+0.770 vs B09 +0.766), but the PAIRED lineage-bootstrap difference is +0.0045 [-0.225,+0.260] -- comparing point estimates alone would have called that a win. Also: alpha_50's ceiling censoring is strongly DEPTH-DEPENDENT (25/26 censored at the bare argmax, 15/26 at 0.50, 19/26 at rho*), so the pre-declared depth is NOT the one giving the most usable values.

  CONTROLS: synthetic-tensor unit tests found a STRONGER blind spot than expected (with 4/12 matrices edited, v1 is no longer the injected direction at all, W02=0, because the Gram pools every matrix -- a threshold, not a ramp); random-direction control on real models PASSES decisively (true v1 -2.742 on the abliterated member vs -0.085 for 5 random directions); revision stability STABLE but weaker than intended (main had not moved); permutation nulls with exact floor 1/C(n,k) beside every CI. Three abliterated members were recovered after their tokenizers shipped no chat_template under transformers 5.x, by substituting standard ChatML. vendored_lib_*.py are BYTE-IDENTICAL (zero patches); lib_*.py are alias shims.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 14 ---
id: art_gCgia-6VUZJb
type: experiment
title: Can you scrub the abliteration scar?
summary: |-
  BOTH ARMS EXECUTED AT FULL SCALE. Verdict SCAR_IS_CHEAPLY_EVADABLE. 34 ladder stages on Qwen3-1.7B + 160 scanned Hub checkpoints, $0.107 judge spend, all 4 gates pass, 17/17 cross-checks pass (verify.py recomputes headline numbers straight from results/*.jsonl).

  ROOT IS CLEAN. In-house diff-in-means abliteration of Qwen/Qwen3-1.7B: harmful refusal 0.923 -> 0.162 (rubric-B judge, frozen 40-item core), W01 4.571 / W02 1.000 / W05 -4.592 (inside the abliterated region), WikiText ppl UNCHANGED 27.08 -> 26.25. Both gates pass on V_A; V_B (embed projected) and V_AUROC ship as sensitivity rows. NO stage tripped the BROKEN fluency screen or the blanket-refuser rule.

  ARM 1 CROSSING (flag death vs un-censoring death). EVADABLE in 4 of 6 real intensity axes: add-back-all eps 0.10 vs 1.00 (cost -0.004), merge w 0.10 vs 0.50 (+0.069), quantization 4-bit vs never (+0.075), add-back-topk k=4 vs k=32 (+0.128). NEITHER_DIES for argmin-only add-back, random-direction add-back, LoRA-SFT. CHEAPEST EVASION IS NOT AN ATTACK: a plain int4 round-trip kills the flag (W05 -4.59 -> -1.95) at harmful refusal 0.135, BELOW the root's own 0.162, ppl 37.7 vs root 26.25, inside the fluency screen. An ordinary deployment step erases the scar for free.

  THREE RESULTS REVERSE THE PRE-REGISTERED PREDICTIONS. (1) The argmin attack FAILS: at eps=1.00 it moves W05 only to -3.080 and never crosses. Abliteration suppresses all 56 write matrices roughly equally, so the minimum has 55 runner-ups; k=4 must be patched. Because v1 is recomputed from the treated model, a local patch ROTATES the eigenvector and lifts EVERY matrix's energy -- a local edit has a global effect on the statistic. (2) Dense benign fine-tuning does NOT scrub it: 200 LoRA steps (r=16, alpha=32, alpaca-cleaned, merged) move W05 only -4.592 -> -4.381 while RESTORING refusal 0.162 -> 0.368. (3) W05 is NOT the most fragile statistic (survival 0.559 vs W02 0.647), but W02 flags 23/160 undeclared repos, so its robustness is a threshold that separates nothing.

  HEAD-TO-HEAD BASELINES (metadata.statistic_head_to_head, labelled controls): only W05 reaches sensitivity 1.000 / specificity 1.000 with 0/160 undeclared flagged. W01/W03/W04 sit at 0.875 sensitivity; W02 flags 14.4% of undeclared repos. The hardened W05q10 (10th percentile, not min) keeps perfect specificity but drops to 0.875 sensitivity -- hardening has a measured cost.

  ARM 2 (tensor-only, zero prompts, zero forward passes). 250 attempted / 160 completed (65 UNRESOLVED with reasons: Conv1D-transposed GPT-2-style, quantized GPTQ/bnb, bad configs; 7 SKIPPED, 1 ERROR -- never counted as scanned). ZERO hits inside the abliterated region; false-positive rate 0/160, Wilson 95% [0, 0.023]. Two warning-band repos (rinna/japanese-gpt-neox-small -2.614, stabilityai/stablelm-3b-4e1t -2.515), both adjudicated FALSE_POSITIVE with quoted card evidence, both in families the panel barely covered -- as predicted. Controls 8/8 positive and 12/12 negative through the identical path. Enumeration counts shipped (1500 listed; 73 DECLARED, 587 oversize, 54 gated, 30 in-panel dropped). Audit cost: median 7.4 s CPU per checkpoint, 2.7 s on GPU at 1.7B.

  METHOD CORRECTIONS DOWNSTREAM WORK MUST INHERIT. (a) Held-out AUROC SATURATES and cannot select the refusal direction: 11 layers >= 0.997 and 4 tie at exactly 1.000 on Qwen3-1.7B, so the argmax is decided by the tie-break; the AUROC-picked direction reproduces the full signature while leaving refusal at 0.333 vs the behavioural pick's 0.162 -- scar and un-censoring are DISSOCIABLE AT CONSTRUCTION TIME. At 0.6B the argmax lands at block 1 and does not un-censor at all; selection must be behavioural (Arditi-style sweep on a dev subset disjoint from the eval core). (b) The panel boundary is -2.7415117804288127, not the rounded -2.742: at the rounded value the member DEFINING it falls outside and the positive control reads 7/8. (c) Only W05 separates the iteration-2 panel; W02's non-abliterated max is 1.0000, so no W02 threshold separates anything. (d) The merge curve is monotone in w only UP TO SATURATION at the parent's own W05 (-1.010); the 0.008 dip at w=0.75 is eigenvector switching, not a bug. (e) judge_kappa_vs_regex ~0 is the REGEX failing (0.000 on every abliterated stage), not the judge: rate-level r = 0.952, judge primary for all 34 stages, T3 calibration 6/6. (f) Gate T4: the tensor-only path is BIT-IDENTICAL to the Runner path on the same device; W01/W04 carry ~8e-3 of float32 CPU-vs-GPU noise, decision statistics agree to 1e-6.

  SHIPPED: method_out.json (7 datasets: ladder, ladder_e_v1_profiles, crossing, robustness, scan, scan_hits, diagnostics; per-row predict_w01..predict_w05q10 make the baseline comparison machine-readable), 6 vector figures rendered from the artifact, README. The 3.8 GB root state_dict is NOT persisted: results/root_recipe.json (52 KB) holds the direction, keys and a sha256 fingerprint; rebuild_root() reconstructs it in ~9 s, verified 311/311 tensors bit-identical.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 15 ---
id: art_0T8jhUa0zxmu
type: evaluation
title: Recomputing every number the paper quotes
summary: |-
  PURE RE-ANALYSIS of the archived iteration-2 trees. No weights loaded, no forward passes, no text generated; the only outbound compute is cached LLM re-labelling of already-archived generations ($0.1703 of the $0.90 cap, 2,865/2,866 items, rerun costs $0). `uv run eval.py` -> analysis.py (2,230 lines) in 547 s on 48 cores; numbers.json is BYTE-IDENTICAL across two runs (timings stripped); eval_out.json + full/mini/preview all pass exp_eval_sol_out.

  HEADLINE FINDING. Four values the draft presents as CORRELATIONS -- A01 -0.161 [-0.501,+0.208], A02 +0.036 [-0.225,+0.303], W01 -0.373 [-0.731,-0.039], alpha_50 -0.453 -- are in fact PAIRED DIFFERENCES |rho_X|-|rho_B09| computed on a 26-member `renderer=='chatml'` subset, NOT the 28-member `member_class != 'base'` subset the draft states. Identified because B09's quoted +0.766 reproduces to 1e-4 on that subset and on none of 16 other (subset, target, unit) conventions; all four quoted |rho| (0.802/0.819 vs 0.766/0.852) reproduce there to <4e-4. Read as correlations they are wrong by up to 0.67 and one has the wrong sign; read correctly, A01/A02/W01 match to four decimals (alpha_50 does not, n=7). The arithmetic was never wrong -- the LABELS were, and no artifact recorded either the quantity or the subset. The falsifier is re-run on the draft's own subset: verdict UNCHANGED on both.

  TWO MORE CORRECTIONS. (1) B09 is NOT the best black-box metric: B08_first_token_entropy_asymmetry |rho| 0.782 beats it at lineage level, B01 0.708 at member level; B09 is the in-resample argmax in only 11.2%/14.4% of resamples; selection optimism +0.182. (2) W05's 'AUROC 1.000' is the ORIENTED value -- raw AUROC is 0.000 because abliterated members sit LOW -- and W01/W03/W04 give 0.9861, W02 0.9497 with 21 tied pairs. Separating margin 0.0763 log10 (allenai/OLMo-1B-hf -2.665 vs huihui Qwen2.5-0.5B -2.742); OLMo is a ONE-MEMBER family. The draft's 'abliterated minimum -2.742' is the abliterated MAXIMUM (true min -4.820).

  ARMS. POWER: minimum detectable |drho| = 0.32 at n=19 lineages (2,000 sims x B=2,000); ~150 lineages needed at delta 0.20, 50 at 0.30, unreachable at 0.10; falsifier_could_have_failed=True. RELIABILITY: split-half Spearman-Brown r_xx = 0.968, so attenuation correction is a factor of 1.016 -- the negative is NOT an attenuation artefact (and a common factor cannot reorder anything, stated rather than sold as survival). Independent adjudicator 6/6 on the hand-labelled set, kappa 0.403 vs the regex screen (regex refusal share 0.19 vs judge 0.43), checkpoint-level Spearman 0.927 vs the archived llama-3.3-70b rates; item-level judge-vs-judge kappa is UNRECOMPUTABLE (E1 kept rates only). DEPTH: PARTIAL -- only auroc_profile and margin_profile are archived per depth; nothing beats B09 at any reachable depth. PRE-REGISTRATION: 4 SUPPORTED / 2 PLAN-ONLY / 6 UNSUPPORTED (metric_spec.py sha 544ff994 stamps 53 metrics and NOTHING else -- no falsifier, exclusion rule, bootstrap spec, candidate list or B09 baseline; rubric B was written after rubric A failed; the blanket-refuser and split-seed rules belong to the DATASET artifact and ARE pre-specified). DISAGREEMENTS: 54 checked -> 32 MATCH, 20 RECOMPUTE_DIFFERS_METHOD, 2 TRANSCRIPTION_ERROR.

  ALSO CORRECTED: W03 uses 256 random directions (lib_metrics.py:105), not 64; the behaviour arm is 28 members over 19 lineages, not 18; renderer values are 'chatml'/'plain' (26/18) and that partition DISAGREES with member_class on 2 members; battery.jsonl matches method_out.json long_table row-for-row (61 nulls differ only in encoding); 9-of-23 singleton lineages CONFIRMED. numbers.json ships the full class-wise [n, median, min, max] for every member_class x metric (the overlaps the abliterated-only column hides), the boundary families, the positive-control disambiguation (instruct 0.6239 vs base 0.6281), and a note that THREE unrelated quantities round to 4.82.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</supplementary_materials>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for judging whether the paper's contribution is genuinely novel versus already-done or a known dead end in this field.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<previous_review>
Your review from the previous iteration. Check which critiques have been addressed
in the revised paper. Do NOT re-raise critiques that have been adequately fixed.
Only re-raise if the fix is insufficient.

- [MAJOR] (evidence) The abliterated class is confounded with abliteration TOOLCHAIN, and the paper's generalisation control tests the wrong variable. Verified in the artifact: the 8 abliterated members are huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2, huihui-ai/Qwen2.5-1.5B-Instruct-abliterated, huihui-ai/Huihui-Qwen3-1.7B-abliterated-v2, huihui-ai/Llama-3.2-1B-Instruct-abliterated, huihui-ai/Llama-3.2-3B-Instruct-abliterated, huihui-ai/Qwen2.5-0.5B-Instruct-abliterated, Goekdeniz-Guelmez/Josiefied-Qwen2.5-3B-Instruct-abliterated-v1 and Goekdeniz-Guelmez/Josiefied-Qwen3-4B-Instruct-2507-gabliterated-v2 -- two uploaders, six from one, and both running an all-layer global diff-in-means projection. Leave-one-ARCHITECTURE-family-out is reported as the generalisation control, but architecture is not what W05 keys on; the edit recipe is. The 2026 community landscape is dominated by variants that are explicitly not a single global rank-one projection (norm-preserving/projected abliteration, ORBA orthogonal-reflection bounded ablation, multi-direction SVD, per-head surgery, DCT 'spectral cascade' modes), and the paper's own band-limited positive control already demonstrates that W05 is blind to any edit that is not global. AUROC 1.000 over 8 near-identical productions is therefore a much weaker generalisation statement than it reads as. The nearest published analogue -- arXiv:2604.08844 -- reports that a spectral weight classifier trained on one editing method assigns EVERY out-of-method adapter a lower drift score than every in-method one (AUC 0.00), which is precisely this failure mode already observed once in the literature.
  Action: Add at least three abliterated checkpoints produced by mechanically different toolchains (mlabonne's recipe, a grimjim projected/ORBA norm-preserving variant, an OBLITERATUS 'advanced' multi-direction run) and report W05 on each. Run leave-one-UPLOADER-out alongside leave-one-family-out and report both. If the non-global variants are missed, report that as the arm's true scope -- 'detects global single-direction abliteration, the huihui/Josiefied recipe class' -- which is still a useful and defensible claim, rather than letting AUROC 1.000 imply coverage of abliteration in general.
- [MAJOR] (rigor) The paper's two headline statistical results have no shipped analysis code. I enumerated method_out.json: its datasets are long_table (2332 raw metric values), method_vs_baseline (44 rows of three metric values each), metric_spec, panel, ams_reproduction_gate, behaviour and diagnostics. There is no AUROC anywhere, no Spearman correlation against behaviour, no bootstrap, and no paired-bootstrap difference. Every number in Sec. 5.1's AUROC column and every entry in the Sec. 5.2 table -- rho = +0.766, CI [+0.539, +0.917], and all seven paired differences with their CIs -- was computed outside the versioned artifact. No bootstrap seed, resample count, tie-handling rule or CI method is stated anywhere in the paper either. A reader cannot reproduce the two claims the paper is built on, and cannot check whether the lineage bootstrap resampled lineages with or without replacement, how singleton lineages were handled (9 members are standalone), or whether Spearman ties were broken by rank-average -- the last of which the paper's OWN self-audit identifies as having flipped the sign of a previous-iteration result.
  Action: Ship analysis.py as a first-class deliverable that reads long_table.jsonl + behaviour.jsonl and emits every AUROC, every Spearman, every bootstrap CI and every paired difference in the paper, with the seed, B, resampling scheme and tie-handling printed in the header, plus an assertion block checking each output against the value quoted in the text. State the bootstrap specification in the Method section in two sentences. This is a few hours of work and it removes the single most damaging objection available to a reviewer.
- [MAJOR] (rigor) The 'pre-registration' the paper leans on does not contain what the paper attributes to it. metric_spec.py (sha 544ff994...) declares 53 metrics with family, prompt requirement, declared forward passes and declared wall-clock, plus import-time count assertions, and nothing else. It contains no falsifier statement, no analysis plan, no rule excluding base models from correlations, no blanket-refuser disqualification threshold, no paired-bootstrap specification, no held-out usage policy beyond a comment saying the split is 'RECORDED ONLY'. Yet the paper says 'the pre-registered falsifier is that if no white-box metric beats the best black-box one...', 'the pre-registered outcome therefore holds in the form it was written', 'base models are excluded from every correlation by pre-registration', 'a metric that ranks a blanket refuser at the top is disqualified by our own pre-registered rule', and 'the pre-registered triage ratio'. None of those is verifiable from the stamped file. Given that the paper's whole credibility argument is measurement discipline, and given that it correctly criticises its own previous round for unannounced deviations, this asymmetry is the most quotable weakness in the submission.
  Action: Publish the plan document that actually contained the falsifier and the analysis rules, with its own hash and a timestamp demonstrably prior to execution, and cite it distinctly from metric_spec.py. Where no such stamped statement exists, downgrade the wording to 'declared in advance in our study plan' or simply 'we adopted the rule that...' and reserve 'SHA-stamped pre-registration' for the metric declarations, which genuinely are stamped. A short table mapping each 'pre-registered' claim in the paper to the artifact and line that records it would close this entirely.
- [MAJOR] (scope) The deployment premise is not yet demonstrated, because the detection task as evaluated is solved for free by a string match. All 8 positives carry 'abliterated' or 'gabliterated' in their repository id; the opening scenario ('a checkpoint arrives with no provenance, its card says nothing') is never instantiated by a single panel member. More importantly, the metric's robustness to the obvious evasions is untested: an abliterated model that is subsequently LoRA-SFT'd, merged with its parent, quantized, or perturbed by an adversary who knows the metric (adding back an epsilon-scaled random rank-one term restores lambda_1 at negligible behavioural cost) may not retain the scar. Because W05 is a MINIMUM over layers, it is by construction the most fragile of the five statistics to any post-hoc process that touches even one layer -- the paper's own band-limited control is exactly this failure in miniature. Without at least one laundering arm, the claim 'it can now be flagged from the tensors alone' at hub scale is aspirational.
  Action: Add a laundering/evasion arm using the in-house edit machinery you already have: abliterate Qwen3-1.7B, then (a) LoRA-SFT 200 steps on benign data, (b) linearly merge 50/50 with the instruct parent, (c) round-trip int8 and int4 quantization, (d) add back a random rank-one term at increasing scale, and report W01-W05 plus harmful-refusal rate at each stage. Report the point at which the flag is lost and whether the model is still uncensored at that point -- if the scar dies only after the un-censoring dies, that is a strong result; if it dies first, say so. Additionally, scan a few hundred sub-4B Hub checkpoints from stored tensors and report any high-scoring repo whose card does not declare abliteration; even a handful of confirmed undeclared positives would make the deployment claim concrete.
- [MAJOR] (novelty) Two directly relevant prior works are uncited, one of them very close. (1) arXiv:2604.08844, Paul, 'Spectral Geometry of LoRA Adapters Encodes Training Objective and Predicts Harmful Compliance' (Apr 2026): a pre-registered study on Llama-3.2-3B-Instruct extracting per-layer spectral features -- norms, stable rank, singular-value entropy, effective rank, singular-vector cosine to a healthy centroid -- from weight deltas across 38 manufactured adapters, reporting AUC 1.00 for binary drift and all six pairwise objective comparisons, rho >= 0.956 ordinal severity, and a geometry-to-behaviour rank correlation of rho = 0.72 with HEx-PHI harmful compliance. Its feature set overlaps your W06-W11 almost item for item; its parent/delta requirement is exactly the gap you occupy; and its rho = 0.72 is a direct empirical counterweight to your Discussion claim that weight geometry cannot carry behavioural signal. Its complete cross-method collapse (AUC 0.00) is also the strongest published prior for the toolchain-confound critique above. (2) The OBLITERATUS toolkit ships a 'spectral certification' step that inspects an abliterated checkpoint's own weights, parent-free, to certify whether the projection is complete, and its own documentation records that certification frequently reads 'incomplete' even when practical refusal rate is 0%. That is prior community practice for the exact operation the paper claims as new, and its calibration failure independently mirrors your 'the ranking transfers, the calibration does not' finding.
  Action: Cite arXiv:2604.08844 in Related Work AND at the point of use in Sec. 4.1 where W06-W11 are introduced, and add one paragraph distinguishing it on three axes: parent-free vs delta-based, real community checkpoints vs manufactured adapters, and edit-detection vs behaviour prediction -- while acknowledging its rho = 0.72 and explaining why your panel's behaviourally-uncensored members show none of it (different manufacture regime, no controlled dose ladder). Cite OBLITERATUS's spectral certification and reframe your novelty as the first measured, held-out-validated, published characterisation of parent-free spectral abliteration detection, including the calibration failure that the toolkit reports anecdotally. Both framings are defensible; silence is not.
- [MINOR] (evidence) Sec. 5.1's table gives [min, max] only for the abliterated column and bare medians for base, instruct, behaviourally-uncensored and safety-RL, which materially understates the overlap present in the shipped data. From diagnostics.weights_arm_by_member_class: W01 base max = 1.992 against abliterated min = 1.438 (a genuine overlap), and W02 base max = 1.000, identical to the abliterated median of 1.000. The AUROC column encodes this (0.986, 0.950) but a reader scanning '4.26 vs 0.47 vs 0.58' will take away far cleaner separation than exists. Similarly, the paper never names the nearest non-abliterated neighbour on W05 (allenai/OLMo-1B-hf at -2.665), and the four values immediately above the decision region belong to OLMo and pythia -- under-represented architectures with no abliterated sibling, which is where false positives will concentrate in the wild.
  Action: Report [min, max] for every class in the table, name OLMo-1B as the nearest non-abliterated neighbour in the text, and add one sentence to Limitations noting that the three checkpoints nearest the boundary are all from single-member architecture families (olmo, gpt_neox) and that the false-positive rate on architectures outside the seven tested is unmeasured.
- [MINOR] (methodology) The Sec. 5.2 falsifier comparison is stated as a clean pre-registered outcome but is decided by an underpowered test against an unfavourably chosen comparator. n = 26 chat-rendered members over 18 lineages gives lineage-bootstrap CIs on paired rho differences with half-widths of roughly 0.25-0.5 -- wide enough that essentially no realistic white-box advantage could have excluded zero. So 'no white-box metric beats the best black-box one with a CI excluding zero' is close to guaranteed a priori and does not distinguish 'the interior buys nothing' from 'we lack the power to tell'. Compounding this, the winner B09 is itself selected as the best of 11 black-box declarations on the same data, so the comparison is best-of-11 against a fixed white-box candidate. The paper's own Sec. 5.2 note that A02 leads B09 numerically at both aggregation units (+0.802/+0.819 vs +0.766/+0.852) sits awkwardly with the headline.
  Action: Report the minimum detectable difference at n = 18 lineages for your bootstrap (a two-line simulation), and state explicitly whether the falsifier could have failed. Then restate the conclusion in the form the data supports: 'at this panel size, no interior metric shows an advantage over the best black-box baseline larger than ~0.3 in |rho|; distinguishing smaller advantages would require roughly N lineages.' Also correct for the best-of-11 selection of B09 by reporting the paired comparison against a PRE-SPECIFIED black-box metric (e.g. B01 logit gap, which has a published prior) alongside the post-hoc winner.
- [MINOR] (methodology) The behavioural ground truth that anchors the entire falsifier is thin and imperfectly reliable, and the paper does not propagate that uncertainty into the correlations. Per behaviour.jsonl each checkpoint contributes 40 harmful and 25 XSTest items scored by a single judge (meta-llama/llama-3.3-70b-instruct, rubric B), with metadata_judge_kappa against the lexical screen around 0.30 and n_judged = 64. A 40-item rate has a binomial SE of ~0.08 at p = 0.5; the judge-vs-screen kappa near 0.30 implies substantial classification noise on top. Spearman correlations computed on 26 such rates will be attenuated by an unknown and unreported factor, which cuts against all metrics equally but makes the paired differences between two attenuated correlations even less informative. The paper's own iteration-1 artifact explicitly advises downstream users to 'attenuation-correct with the reported reliability'; this iteration does not.
  Action: Report a reliability estimate for the harmful-refusal rate (e.g. split-half over the 40 items, or judge-vs-adjudicator agreement on a stratified subsample), give attenuation-corrected versions of the Sec. 5.2 correlations alongside the raw ones, and add per-member binomial error bars to Figure 3. If attenuation correction moves any ordering, say so.
- [MINOR] (clarity) Small verifiable mismatches between text and code undercut a paper whose credibility rests on fidelity. (a) W03 is defined in the paper against '64 matched random directions'; lib_metrics.py uses n_random = 256 (compute_weights default) and the frozen spec's own note says 256. (b) The Method says the positive control was injected into Qwen3-0.6B; diagnostics records the edited model as Qwen/Qwen3-0.6B (the instruct member) while the panel also contains Qwen3-0.6B-Base -- worth disambiguating since the unedited baseline W01 = 0.624 is quoted in the paper as 0.62 and the base member's value is 0.628. (c) The paper reports the positive control's W01 as going 'from 0.62 to 4.82' and separately reports the strongest abliterated panel member's W05 as -4.82; these are unrelated quantities that share a numeral and read as a typo.
  Action: Correct the W03 random-direction count to 256, name the exact positive-control checkpoint and revision, and either add a digit or reword so the two 4.82 values are not adjacent. Then do a mechanical pass reconciling every numeral in Secs. 4-5 against the artifact, ideally by generating the numbers into the text from analysis.py rather than transcribing them.
- [MINOR] (scope) The paper still owes a head-to-head against its self-declared closest competitor on that competitor's own terms. E_1 from [2] is described and correctly characterised as parent-requiring, but it is never computed -- not even on the subset of the panel where the parent IS available (the panel contains instruct/abliterated sibling pairs for at least the Qwen2.5-0.5B, Qwen2.5-1.5B, Qwen3-0.6B, Qwen3-1.7B and Llama-3.2-1B/3B lineages). Without that, the reader cannot tell what the parent-free constraint actually costs in AUROC on a matched panel, which is the central trade the paper claims to be making. Similarly, AMS is run and shown to lose, but RAS/SafeVec and VISAGE remain costed-away rather than run even at reduced fidelity.
  Action: Compute E_1 on every sibling pair in the panel where the parent is present and report W05 vs E_1 AUROC on that matched subset. If E_1 also reaches 1.000 there, the honest framing is 'parent-free matches parent-required on this panel at zero prompt cost', which is a much stronger sentence than the current one. If E_1 wins, quantifying the cost of the constraint is itself the contribution. This is a pure re-analysis of tensors you have already downloaded and should be inexpensive.
- [MINOR] (rigor) The rho* depth-selection procedure is reported as outcome-blind but is effectively arbitrary, and the paper does not test whether its results depend on it. The shipped calibration block shows the held-out AUROC profile saturating at 1.0 across indices 4-25 of 28 (a 22-layer plateau), with bare_auroc_argmax_index = 4 and the d'-tiebreak landing at index 20 -> rho* = 0.679. The paper says this honestly, but then reports every activation metric at that one depth, including the observation that alpha_50 is ceiling-censored on 37/44 members AT THAT DEPTH -- a censoring rate that is plausibly a consequence of the depth choice rather than of the metric. A reader cannot tell whether the activation arm's poor showing in Sec. 5.2 is a property of the arm or of an essentially coin-flipped depth.
  Action: Report the Sec. 5.2 correlation table at three depths spanning the plateau (e.g. rho* = 0.14 at the bare argmax, 0.50, and 0.679) and state whether the falsifier conclusion is invariant. If any activation metric beats B09 at some depth in the plateau, that must be disclosed even though the pre-declared depth is primary. Also report alpha_50's censoring rate at each depth so the reader can separate depth from metric.
</previous_review>

<task>
Review this paper as you would for a top-tier venue submission.

STEP 1 — READ THE PAPER: Read it carefully. Note claims, methodology, and results.

STEP 2 — CHECK THE CODE: Read the supplementary materials to verify the paper's claims.
Do the experiments match what's described? Are there discrepancies between code and paper?

STEP 3 — SEARCH THE LITERATURE: Ground your review in evidence.
- Search for the closest existing work — is this genuinely novel or incremental?
- Check if the proposed methodology has known failure modes
- What level of contribution gets accepted at top venues in this area?

STEP 4 — WRITE YOUR REVIEW:
For each critique:
1. Categorize: methodology, evidence, novelty, clarity, scope, or rigor
2. Rate severity: major (would cause rejection) or minor (polish)
3. Describe the issue clearly
4. Suggest a concrete action to address it

Focus on the most impactful issues. Provide your review via structured output.
</task><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "Critique": {
      "description": "A single actionable critique from the reviewer.",
      "properties": {
        "category": {
          "description": "Category: 'methodology', 'evidence', 'novelty', 'clarity', 'scope', or 'rigor'",
          "title": "Category",
          "type": "string"
        },
        "severity": {
          "description": "Severity: 'major' or 'minor'",
          "title": "Severity",
          "type": "string"
        },
        "description": {
          "description": "Clear description of the issue",
          "title": "Description",
          "type": "string"
        },
        "suggested_action": {
          "description": "Concrete suggestion for how to address this critique",
          "title": "Suggested Action",
          "type": "string"
        }
      },
      "required": [
        "category",
        "severity",
        "description",
        "suggested_action"
      ],
      "title": "Critique",
      "type": "object"
    },
    "DimensionScore": {
      "description": "Score for a single review dimension with improvement suggestions.",
      "properties": {
        "dimension": {
          "description": "Dimension name: 'soundness', 'presentation', or 'contribution'",
          "title": "Dimension",
          "type": "string"
        },
        "score": {
          "description": "Score from 1 (poor) to 4 (excellent)",
          "title": "Score",
          "type": "integer"
        },
        "justification": {
          "description": "Brief justification for this score",
          "title": "Justification",
          "type": "string"
        },
        "improvements": {
          "description": "Specific improvements to raise the score (what + how + why)",
          "items": {
            "type": "string"
          },
          "title": "Improvements",
          "type": "array"
        }
      },
      "required": [
        "dimension",
        "score",
        "justification"
      ],
      "title": "DimensionScore",
      "type": "object"
    }
  },
  "description": "Adversarial review of the paper draft.\n\nID format: review_it{iteration}__{model}",
  "properties": {
    "overall_assessment": {
      "description": "Overall assessment of the paper's quality and readiness",
      "title": "Overall Assessment",
      "type": "string"
    },
    "strengths": {
      "description": "Key strengths of the paper",
      "items": {
        "type": "string"
      },
      "title": "Strengths",
      "type": "array"
    },
    "dimension_scores": {
      "description": "Scores (1-4) for: soundness, presentation, contribution",
      "items": {
        "$ref": "#/$defs/DimensionScore"
      },
      "title": "Dimension Scores",
      "type": "array"
    },
    "critiques": {
      "description": "Actionable critiques \u2014 specific issues with concrete suggestions",
      "items": {
        "$ref": "#/$defs/Critique"
      },
      "title": "Critiques",
      "type": "array"
    },
    "score": {
      "description": "Overall quality score from 1 (very strong reject) to 10 (award quality)",
      "title": "Score",
      "type": "integer"
    },
    "confidence": {
      "default": 3,
      "description": "Confidence in assessment from 1 (educated guess) to 5 (absolutely certain)",
      "title": "Confidence",
      "type": "integer"
    }
  },
  "required": [
    "overall_assessment",
    "strengths",
    "critiques",
    "score"
  ],
  "title": "ReviewerFeedback",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-13 23:35:06 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [3] SKILL-INPUT — aii-web-tools · 2026-08-13 23:36:46 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Web research toolkit: free-first web search (general or scholarly, Serper fallback), web page fetch as markdown (HTML and PDF), and regex grep over full page/PDF text. Use whenever a task needs to search the web, read a page, mine a paper/PDF, verify citations, or extract exact quotes, numbers, or methodology from a URL."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — free-first web search (keyless general/scholarly engines,
   Serper fallback), html2text + PyMuPDF for fetch, and regex grep over the full
   document text. They work without any built-in web tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (free-first: general or scholarly)

```bash
# general web (default): keyless engines (ddgs, marginalia); Serper only if they miss
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
# scholarly mode: OpenAlex + Crossref (DOIs, citation counts)
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation" --mode scholarly
```

Returns ranked title / URL / snippet lines. `--mode general` (default) uses
keyless general engines; `--mode scholarly` uses academic APIs. Both fall back
to Serper (paid) only when the free engines miss. Use search first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````
