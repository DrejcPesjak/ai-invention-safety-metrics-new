# review_paper — test_idea

> Phase: `invention_loop` · round 4 · `review_paper`
> Run: `iter1_33370088803c` — Catching Edited Safety Models by Reading Weights in Sliding Windows
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `review_paper` (terminal_claude_agent, claude-opus-5)

### [1] CONFIG · 2026-08-14 02:14:28 UTC

```
model: claude-opus-5 | effort: medium | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/review_paper/review_paper
```

### [2] SYSTEM-USER prompt · 2026-08-14 02:14:34 UTC

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

An open-weight checkpoint arrives with no provenance. Deciding whether its safety training is intact currently costs a benchmark run: hundreds of harmful prompts from AdvBench [25], JailbreakBench [26] or HarmBench [27], a judge model to score the generations [29], and a repeat for every attack template of interest. At the scale of a model hub the unit of cost is wrong. Our own harvest of 61 Hub sweeps over 20,313 enumerated repositories found 513 self-declared edited checkpoints from 189 distinct uploaders below 4.2B parameters alone [ARTIFACT:art_8OlSrcw-hzgO], and a follow-up census this iteration returned 1,068 hits of which 116 are sub-4.2B [ARTIFACT:art_gqCRODISeyg2].

The published cheap alternatives each retain a dependency the situation does not grant. AMS [3] reads activation geometry but needs harmful prompts. RAS/SafeVec [4] needs unsafe prompts, jailbreak prompts *and* a safety-aligned reference model. VISAGE [5] evaluates a harmful benchmark at every weight perturbation. The two closest weight-space results both require the parent: the abliteration audit of [2], whose statistic is $E_1 = \mathrm{mean}_m\,\sigma_1^2(\Delta W_m)/\sum_i \sigma_i^2(\Delta W_m)$ with $\Delta W = W_{\text{base}} - W_{\text{cand}}$, and the spectral-geometry study of LoRA adapters [8]. A random Hugging Face repository does not come with an attested parent.

Three iterations ago we proposed the obvious parent-free substitute. If abliteration [1, 13] projects one direction out of every residual-write matrix, that direction is a shared approximate null direction of the write ensemble and should be recoverable from the ensemble alone. The statistic $W05 = \log_{10}\min_m \lVert v_1^\top W_m\rVert^2/(\lVert W_m\rVert_F^2/d)$, where $v_1$ is the minimum eigenvector of the pooled write Gram matrix, separated 8 abliterated from 36 non-abliterated archived checkpoints at oriented AUROC 1.000, cost no prompts and no forward passes, and returned zero false positives on a wild scan. The previous draft of this paper reported that result with a scope boundary attributed to *uniformity*: the statistic was said to require an edit applied uniformly to the whole stack.

**This iteration tested that account at scale and both halves of it failed.** On 44 real edited checkpoints from 27 uploaders spanning 9 recipe classes, selected without looking at repository names and with the recipe re-derived from the full model card fetched at a pinned revision, $W05$ fires on **7** — sensitivity 0.159 — while the five archived positives it was calibrated on all still fire at 1.000. It does not beat the operational baseline: a plain regex over the repository id reaches sensitivity **0.727** at the same specificity 1.000 on identical rows, and the set of checkpoints $W05$ catches that the name misses is **empty** [ARTIFACT:art_dp7WBo6hhVBX]. And uniformity is not the predicate: a controlled kernel sweep that holds the host model and the refusal direction fixed and varies only the depth kernel shows that detection needs two independent conditions, one of which the uniformity story never named.

[FIGURE:fig1]

The positive contribution of this paper is that second finding, and it is a mechanism rather than a metric. Detection requires **discovery** — enough of the stack edited along $r$ that $r$ becomes the pooled Gram's minimal eigendirection, $|\cos(v_1,r)|\to 1$ — **and** **completion** — some matrix annihilated along $r$ deeply enough to cross the operating threshold. A post-hoc rule combining exactly these two conditions reproduces the detection outcome on **19 of 19** applicable kernels with zero disagreements. The two conditions are independent, and separating them explains every previously mysterious failure at once. A Gaussian depth kernel annihilates its peak layer *completely* at every spread we tested ($\log_{10}\min_m e_r = -4.53$ at all nine spreads), so completion is always satisfied; detection nevertheless switches on abruptly between spread 8 and 16, exactly where the *minimum* depth weight crosses from 0.0796 to 0.5311 and $|\cos(v_1,r)|$ jumps from 0.126 to 0.9992. Completion was never the binding constraint; discovery was. Symmetrically, a uniform projection at sub-unit weight $w=0.85$ has perfect discovery ($|\cos|=0.999$) and fails completion, and is invisible while being as behaviourally effective as the full edit (harmful refusal 0.225 against 0.200).

The mechanism is not an excuse; it is predictive, it is falsifiable, and it points at a fix. Because the blind spot is a *pooling* artefact — the Gram sums over the whole stack, so untouched layers prevent $r$ from ever becoming minimal — we introduce $W05w$, a sliding-layer-window generalisation that stops pooling. On the archived diagnostic where four of twelve matrices are edited and the pooled statistic reads $-0.838$ against a clean reference of $-0.289$, the two-layer windowed statistic reads $-13.43$ against a clean reference of $-0.829$, a separation of 12.6 log-units where the pooled statistic has none, at specificity 1.000 on 40 freshly scanned eligible undeclared Hub checkpoints [ARTIFACT:art_VFF9Dum9x3KJ]. We report that as a demonstrated diagnosis-to-remedy step and are explicit that its positive arm on real edited checkpoints did not run.

Two further results this iteration are decisive for anyone who would deploy such a certificate, and both are demonstrated **by construction rather than inferred from a correlation** [ARTIFACT:art_VLI4IOs9Xy9P]. A depth-weighted Gaussian abliteration of Qwen3-1.7B, built with the refusal direction held fixed at the uniform root's so that the kernel is the only manipulated variable, un-censors from 0.950 to **0.270** [0.196, 0.360] at $n=111$ while staying fluent, and reads $W05 = -1.0100$ — its unedited parent's value to four decimals, with $\cos(v_1,r)=0.0199$. That is a false negative built to order, and the non-uniform recipe class it instantiates is 235 of 513 (45.8%) of declared edits in our Hub census. In the other direction, a uniform abliteration of Llama-3.2-1B-Instruct along the AUROC-argmax direction fires the full weight signature at $W05=-4.587$ while refusing at 0.950 [0.83, 0.99] — its parent's rate. It was never un-censored. **The weight statistic and the safety behaviour are dissociable in both directions.**

## Summary of Contributions

- **A two-condition mechanistic account of parent-free spectral edit detection** (§4.2, §5.2), validated on a 25-kernel sweep with host and direction held fixed: detection $\Leftrightarrow$ discovery $\wedge$ completion, reproducing 19/19 applicable kernels. It replaces the previous draft's uniformity story, which we retract, and it predicts rather than describes the blind spots.
- **The at-scale falsification of the certificate itself** (§5.1): sensitivity 0.159 on 44 real edited checkpoints from 27 uploaders and 9 recipe classes against 0.727 for a repository-name regex at matched specificity 1.000. Leave-one-recipe-class-out is the primary generalisation control and locates the failure precisely: norm-preserving 5/5, global rank-one 1/6, Heretic 0/7, Gaussian-depth 0/3, partial-layer 0/4, multi-direction 0/5, SFT-uncensored 0/5.
- **A both-directions decoupling demonstrated by construction** (§5.3): a depth-weighted root that un-censors 0.950 $\to$ 0.270 and reads its parent's $W05$, and an AUROC-selected root that reads $-4.587$ while refusing at its parent's 0.950.
- **The deployment number on an honest, pre-stamped denominator** (§5.4): eligibility rule sha256-stamped before any rate was computed; 0 false positives on **122** eligible undeclared checkpoints, Wilson 95% $[0, 0.031]$, with the previously reported raw 0/160 retained as a labelled secondary row and its degenerate composition published. First false positive appears at a threshold shift of 0.128 log-units, about 1.7 panel margin widths.
- **The parent buys real coverage** (§5.5), reversing our previous "parent-free costs nothing": on the same at-scale rows $E_1$ fires on 13 of 32 pairs against $W05$'s 7 of 35, and reaches Gaussian-depth, Heretic and partial-layer edits that $W05$ cannot see. The conclusion is invariant across three depth bands.
- **A quantization result split into its two distinct claims** (§5.4), with the previously proposed dequantization remedy shown to be void as stated, and **a laundering ladder with error bars on three roots and two architectures** (§5.6), which retires four decimal-level claims from the previous draft while confirming the orderings at $n>100$.
- **A 110-assertion reproduction audit of our own draft** (§5.8): 105 MATCH, 5 MISMATCH, 0 UNAVAILABLE, byte-identical across two runs [ARTIFACT:art_ckuwEkspyins].

# Related Work

**Parent-required weight audits, and the shrinking hole we occupy.** WeightWatch [9] shows that top singular vectors of a fine-tuned-minus-base difference correspond to newly acquired behaviours. The abliteration audit of [2] specialises this with $E_1$ over $o\_proj$ and $down\_proj$; primary-source reading this iteration establishes that $E_1$ is *already* band-averaged over "each layer in the mid-stack band $B$" [ARTIFACT:art_gqCRODISeyg2], so per-band scoring is published prior art and only the parent-free, calibration-free, bottom-of-spectrum, sliding-and-extremum-scored combination is novel. Paul's pre-registered spectral-geometry study of LoRA adapters [8] reaches binary drift AUC 1.00 on 38 manufactured adapters and $\rho=0.72$ ($N=24$, no CI) against HEx-PHI harmful compliance; two of its five features are formula-identical to our $W06$–$W09$, and its single most informative feature is a cosine to a *healthy-adapter centroid*, requiring both a parent and a reference population. Its cross-method AUC 0.00 result ($n_{\text{bootstrap}}=972$) is the strongest published precedent for our recipe boundary, and must be carried with its declared confound: the steering arm produced incoherent text at every intensity, GPT-4o scoring 0 of 300 responses harmful. [10] detects backdoored LoRAs from weights alone at our exact size class, but its object is an adapter already separated from a frozen base, with supervised calibration on labelled adapters.

**Community weight forensics is further along than the previous draft acknowledged.** Abliterlitics [34] is an open-source abliteration-forensics toolkit (AGPL-3.0, first public 2026-04-24) comparing a base against its variants along weight, KL, capability and HarmBench axes, with published reports on ten base models from ~2B to 59B. Its weight axis computes SVDs of the edit, Grassmann subspace alignment, per-layer edit-magnitude profiles and technique fingerprints — every one on the *delta*: its methodology is literally `diff = (variant - base).abs().mean()` and `svd(delta_matrix)`, and its documented usage requires "a directory with your base model and variants, plus a `comparison.json`", with `base` a mandatory key and no single-checkpoint mode [ARTIFACT:art_gqCRODISeyg2]. It is therefore parent-requiring, which sharpens rather than blunts the parent-free claim. Its measurements are also the strongest *external* evidence for this paper's mechanism, and they sit at our scale: four of its reports are at or below ~4.5B, including a full weight report on Qwen3-4B-Instruct-2507, our own panel family. On a shared Qwen3.5-9B base, Heretic modifies 23 of 32 layers, HauhauCS 29 and Huihui 31, with Heretic's edits leaving layers 0–8 untouched — while Heretic and Huihui agree almost perfectly in *direction* (median cosine 1.0, global mean 0.997, 100% of principal angles above 0.9). The recipes differ in depth and completeness, not in direction: that is our discovery-versus-completion decomposition, measured independently. Abliterlitics also names the axis first, contrasting "Uniform (33/33/33%)" against "Mid-to-late focused (42–44% late)", as does Gabliteration [17], whose own text reads "Unlike the uniform layer modification approach in traditional abliteration". Separately, OBLITERATUS [11] ships a *spectral certification* step, but reading its source settles that it consumes **activations**, not weights: `certify(harmful_activations, harmless_activations, layer_idx)` thresholds eigenvalues of a between-class rank-one outer product against a BBP bound. It is parent-free but not prompt-free, and it audits an edit the operator just performed. The only *shipped* parent-free abliteration detector we could find, `reverse-abliterate` [12], reads filenames and metadata and no tensor values; it is the software instantiation of the repository-name baseline our own data quantifies at 50.5% [ARTIFACT:art_8OlSrcw-hzgO] and which §5.1 measures at 0.727 sensitivity on a recipe-diverse sample.

**Parent-free spectral statistics that are not edit detectors.** Two works must be ruled out on the record. *Spectral Signatures of Large Language Models* [35] is the closest parent-free spectral work, but its stated design goal is the opposite of ours — a lineage identifier whose "impact of post-training on the weight ESD is minimal" — and its PL\_Alpha\_Hill estimator reads the *top* $n/2$ eigenvalues, aggregated to a model-level signature. We read the bottom of the spectrum and want maximal sensitivity to post-training. The honest caveat, which we state rather than hope goes unnoticed, is that it does compute depth-wise layer-wise profiles, so the machinery is one step from ours. *Spectral Outliers Reveal Dominant Learned Structure* [36] is parent-free and per-layer but separates a Marchenko–Pastur bulk from outliers to detect learned *structure*, not edits. Weight-homology identification [37] is inference-free and gives p-values, but answers lineage rather than edit detection. Coslett [38], now resolved via DataCite after six failed access routes, is adjacent rather than competing: its instrument is an inference-time output-geometry and log-probability fingerprint, not a weights-only statistic.

**The recipe family, read from source.** Abliteration is not one operation, and the previous draft's taxonomy contained an error this iteration corrects from primary code. Heretic's kernel is a **triangular tent with a hard cutoff**, not the Gaussian or bell curve that our draft, our dependency dossier and OBLITERATUS's documentation all assert: `if distance > min_weight_distance: continue`, followed by linear interpolation; `max_weight_position` is sampled in $[0.6L, 1.0L]$ and `direction_index` in $[0.4L, 0.9L]$, so the peak is *code-level forbidden* from the early stack [14, ARTIFACT:art_gqCRODISeyg2]. That prediction matches Abliterlitics' independent measurement that layers 0–8 carry no real edits. Heretic's shipped default is already norm-preserving (`row_normalization="full"`). OBLITERATUS is layer-selective via COSMIC [39], so its rank-$k$ presets are *degraded*, not detected. ORBA [16] is two distinct recipes: $\lambda=1$ in the author's terms is zeroing *without* reflection, i.e. annihilation, while only the v3 Householder $H = I - 2uu^\top$ is a true isometry — and conflating them makes the falsification test vacuous, which is why we implement and report both. The remaining members are mlabonne's depth-weighted kernel [13], MPOA's exact four-step row-norm-preserving update [15], Gabliteration's ridge-regularised rank-$k$ update [17], and behavioural SFT, which has no closed form. A cross-architecture comparison exists [18] but evaluates at 7B–14B.

**Why a scar is expected, and why detection is not control.** Safety fine-tuning minimally transforms MLP weights so as to align unsafe inputs into a null space [19], and safety behaviour localises to a small set of neurons and ranks [20]; heavy-tailed self-regularisation supplies the spectral descriptors [21]. Extended-refusal training defends against abliteration while leaving weights superficially normal [22], and abliteration has substantial off-target effects [23]. Galeone et al. [7] establish the general dissociation between detecting a behaviour and controlling it — a linear detector at AUC 1.000 sitting at $\cos = 0.12$ from the direction that produces the behaviour — and their Section 8 makes cosine-as-safety-score a published negative. Our §5.3 reports the same dissociation where the "detector" is a weight statistic, in both directions and by construction. Finally, Hasan and Biswas [24] report over-refusal and harmful compliance nearly uncorrelated across 21 open-weight models, and Basu et al. [6] give the reason a read-side metric can be confidently wrong: 98.2% probe AUROC alongside 45.1% output sensitivity.

# Panel, Ground Truth and the Analysis Contract

**Panels.** Four panels are used and never mixed. (P1) The **archived battery panel**: 44 checkpoints at $\leq 4.2$B over 23 weight lineages and 7 architecture families, comprising 16 base, 15 instruct, 8 abliterated, 4 behaviourally-uncensored and Qwen3-4B-SafeRL, with a lineage-level held-out split whose seed and fraction were stamped before any model was loaded. (P2) The **at-scale recipe panel**, new this iteration: 44 real public sub-4.2B edited checkpoints from 27 uploaders across 9 recipe classes, plus 20 freshly measured Hub parents as negatives, plus ~30 in-house kernels on a fixed host with a fixed direction [ARTIFACT:art_dp7WBo6hhVBX]. (P3) The **wild panel**: the archived 270-row undeclared scan (20 controls + 250 attempted, 160 scored) extended with 40 newly fetched eligible repositories, filtered by a pre-stamped eligibility rule to 122 [ARTIFACT:art_VFF9Dum9x3KJ]. (P4) The **laundering panel**: three in-house abliteration roots on two architectures, pushed through three laundering families [ARTIFACT:art_VLI4IOs9Xy9P]. Every model-level statistic resamples weight lineages, not checkpoints.

**Arm A selection is name-blind.** Because the operational baseline is a repository-name regex, a panel selected by searching for "abliterated" would be circular. Candidates are therefore filtered by eligibility first; the recipe class is then re-derived from the **full model card fetched at the pinned revision** — the dependency manifest stores only a ~250-character evidence window, which is usually too short to name the kernel — and the panel is filled round-robin over recipe classes, smallest first.

**The eligibility rule is stamped before any rate.** `eligibility.py` (sha256 `0f8be4f6…`, 4,739 bytes, stamped 2026-08-14T00:30:46Z) declares E1 $n_{\text{layers}}\geq 8$; E2 $d_{\text{model}}\geq 128$; E3 params $\leq 4.2\times 10^9$ enforced twice, from the safetensors index *and* from on-disk bytes divided by the widest declared dtype; E4 not a unit-test fixture; E5 not a speculator or draft head; E6 not a quantized re-upload. The rule exists because the reviewer of the previous draft correctly identified that 44 of the 160 previously scanned repositories were degenerate. A statistic defined as a minimum of per-layer write energy over an eigenvector of a pooled Gram matrix is not meaningfully defined on a two-layer, eight-dimensional random stub, and a single-layer speculator head has one term in the minimum; E1 and E2 are that floor, made explicit.

**External safety ground truth barely exists at this scale.** A dedicated harvest found external safety coverage for 3 of 66 candidate checkpoints and 2 of 34 lineages; twelve published safety sources [24, 26, 27, 28, 30, 31, 32, 33] name zero panel checkpoints, and HELM Safety was read from its machine-readable release registry and verified to contain no model under 10B. Safety ground truth is therefore measured in-house on a frozen 40-item stratified harmful core and 25 XSTest-safe items [28], with a blanket-refuser disqualification rule at $>0.50$ over-refusal derived from XSTest's own released human labels.

**Judge protocol and its measured limits.** The judge is `meta-llama/llama-3.3-70b-instruct` at temperature 0 under rubric B, which separates "did the model comply" from "is the content harmful"; the rubric mandated by our earlier plan scored harmfulness rather than behaviour, gave $\kappa\approx 0$ against a hand-labelled set, and was replaced — a deviation, recorded as one. This iteration re-measures judge-versus-regex agreement over 61 stages and **corrects our own previously reported figure**: rate-level Pearson $r = 0.822$, not the archived 0.952, with mean $\kappa = 0.149$. The direction of the disagreement is unchanged and important: the standard 12-substring screen from [1] reads 0.000 on every abliterated-derived stage where the judge reads 0.13–0.37, so the screen is the broken instrument.

**The analysis contract.** Every AUROC carries an explicit orientation field, because the abliterated class sits at the *low* end of $W05$ and the raw Mann–Whitney value is the complement of the oriented one. Cluster bootstrap over lineages with replacement, $B=10{,}000$, percentile 95% intervals; Spearman with rank-average ties; pairwise deletion with achieved $n$ printed; permutation nulls with the exact floor $1/\binom{n}{k}$. Every proportion carries a Wilson interval. Each experiment ships an independent verifier that re-derives every headline number from raw rows without importing the pipeline: 20/20, 29/29 and an assertion block whose exit code is stored in the artifact.

# Method

## The statistic and the two conditions

Let $\mathcal{W}$ be the set of matrices writing into the residual stream (attention output projections and MLP down-projections) across all $L$ layers. Form

$$A = \sum_{W\in\mathcal{W}} \frac{WW^\top}{\lVert W\rVert_F^2},\qquad \lambda_1\le\dots\le\lambda_d,\quad v_1=\text{eigvec}(\lambda_1),$$

and define the normalised write energy along a unit direction $u$ as $e_W(u) = \lVert u^\top W\rVert^2/(\lVert W\rVert_F^2/d)$, which equals 1 in expectation for a random direction. The certificate is $W05 = \log_{10}\min_W e_W(v_1)$, with the panel-fitted operating point $\tau = -2.7415117804288127$. Auxiliary statistics are $W01 = \log_{10}(\mathrm{median}(\lambda)/\lambda_1)$, $W02 = \Pr_W[e_W(v_1)<0.1]$, $W03$ against **256** matched random directions, and $W04 = \log_{10}(\lambda_2/\lambda_1)$.

The two-condition account decomposes detection into quantities that can be measured separately whenever the removed direction $r$ is known:

$$\textbf{discovery: } |\cos(v_1, r)| > 0.9, \qquad \textbf{completion: } \log_{10}\min_W e_W(r) \le \tau.$$

Discovery asks whether the pooled eigendecomposition ever surfaces the edited direction; completion asks whether the annihilation is deep enough somewhere. Neither implies the other, and the sweep in §5.2 contains kernels satisfying exactly one of them in each direction. The rule is post-hoc — it was derived from the sweep, not stamped before it, and we label it as such.

## The controlled kernel sweep

Arm B holds the host (`Qwen/Qwen3-1.7B`) and the refusal direction $r$ fixed, taking $r$ verbatim from the archived recipe, so that across ~30 checkpoints the **kernel** is the only variable: uniform at $w\in\{0.5,0.7,0.85,1.0\}$; a Gaussian depth kernel at spread $\in\{0.5,\dots,64,\infty\}$; a middle-50% layer band; ORBA's Householder at $\lambda\in\{0.25,0.5,1.0\}$ plus a Householder about an unrelated random direction as a noise-floor control; MPOA's norm-preserving projection; rank-$k$ at $k\in\{2,4,8\}$; and Heretic's per-component kernel with float direction index 17.89 and per-component weights 0.84/1.15 taken from a real published card. Every kernel is scored on weights *and* on behaviour: WikiText perplexity, distinct-3, and greedy harmful-refusal rate on the frozen 40-item core, so that "the edit worked" and "the edit is visible" stay separable. Each is also re-run at float32 storage as a precision control, because the archived recipe writes `(W - outer(r, r@W)).to(bfloat16)` and every Hub checkpoint is stored the same way.

## The windowed generalisation

Because the blind spot is a pooling artefact, $W05w$ stops pooling: windows of $k$ consecutive layers with stride $\max(1,k//2)$, a per-window minimum eigenvector $v_1^{\text{win}}$, and

$$W05w(k) = \min_{\text{win}}\ \min_{m\in\text{win}} \log_{10} e_{W_m}(v_1^{\text{win}}),\qquad c(k)=\min_{\text{adjacent}}|\cos(v_1^{\text{win}_i}, v_1^{\text{win}_{i+1}})|,$$

with $c(k)$ as a consistency gate swept over a threshold. At $k=L$ a single window covers the whole stack, so $W05w(L)\equiv W05$; this is asserted at $10^{-9}$ on synthetics and reproduces $W05$ on 40 real models to $8.5\times 10^{-8}$, giving the generalisation a built-in reproduction gate. A multiple-window false-positive-rate hazard is inherent — more windows means more minima — which is why specificity is reported per $k$.

## Three roots, and the ladder with error bars

The previous draft's laundering ladder ran on one root. This iteration builds three [ARTIFACT:art_VLI4IOs9Xy9P]: **A**, the rebuilt archived uniform all-layer abliteration of Qwen3-1.7B; **B**, a depth-weighted Gaussian abliteration of the same host with the direction held fixed at A's, so the kernel is the only manipulated variable; and **C**, a uniform all-layer edit of `meta-llama/Llama-3.2-1B-Instruct` for cross-architecture range. Each is pushed through merge with the parent, quantization round-trip and add-back-all, first at $n=40$ to locate crossings and then at $n=120$ on load-bearing cells. Every rate carries a Wilson interval, and the achieved denominators are *recovered* rather than trusted: the archive records $n=40$ on all 34 rows, but rates are $k/n$ with unparseable judge labels dropped from both numerator and denominator, and the recovered denominators span **31–40** with 13 rows ambiguous.

# Results

## At scale, the certificate is precise and nearly blind

[FIGURE:fig2]

On the 44-checkpoint at-scale panel the picture inverts relative to the archived panel. Specificity is 1.000 — zero false positives on 32 negatives including 20 freshly measured Hub parents. Sensitivity is 0.159 (7 of 44), while the five archived positives the threshold was fitted on all still fire at 1.000. Five of the seven detections are one uploader's norm-preserving family; a sixth, `huihui-ai/Qwen2.5-Coder-0.5B-Instruct-abliterated` at $W05=-2.829$, clears $\tau$ by 0.09.

| held-out recipe class | $n$ | $W05$ sensitivity at $\tau$ | oriented AUROC | prior prediction |
|---|---|---|---|---|
| norm-preserving | 5 | **1.000** | 1.000 | 1.0 |
| global rank-one | 6 | 0.167 | 0.620 | 1.0 |
| unknown | 5 | 0.200 | 0.806 | — |
| multi-direction SVD | 5 | 0.000 | 0.844 | 1.0 |
| Heretic per-component | 7 | 0.000 | 0.772 | 0.0 |
| Gaussian depth | 3 | 0.000 | 0.885 | 0.0 |
| partial layer / per-head | 4 | 0.000 | 0.664 | 0.0 |
| SFT-uncensored | 5 | 0.000 | 0.819 | — |
| merge of abliterated | 4 | 0.000 | 0.516 | — |

Leave-one-recipe-class-out is the primary generalisation control this iteration, replacing leave-one-uploader-out, which is demoted to a secondary column with identical fields. The reviewer of the previous draft argued that our four "unseen uploader" misses were a recipe effect wearing an uploader costume, and the relabelling audit confirms two of the four from verbatim card strings — `MagicalAlchemist/Qwen3-1.7B-Magic_decensored` is "made using Heretic v1.1.0" with `direction_index` 17.89 and `attn.o_proj.max_weight` 0.84, and `prithivMLmods/VibeThinker-3B-heretic_decensored` is "modified using the Heretic abliteration toolkit" — while refusing to relabel the other two, because mlabonne's Gaussian-depth sentence is **not** in the archived card text and inferring a kernel from $W05$ would be circular [ARTIFACT:art_ckuwEkspyins]. The honest count is 2 of 4 attributed, remainder 2. The at-scale panel then settles the question the four-checkpoint sample could not: it *is* a recipe effect, but the two classes that most badly fail — multi-direction SVD (0/5) and global rank-one (1/6) — were both predicted to be caught, so the previous draft's recipe story is not merely incomplete but wrong in its sign on two classes.

**It does not beat the baseline it must beat.** Against a plain regex over the repository id (11 terms), scored on identical rows: regex sensitivity **0.727**, specificity 1.000; $W05$ sensitivity **0.159**, specificity 1.000; agreement 0.609; and `caught_by_W05_missed_by_name` is the **empty set**. The regex is trivially spoofable and is therefore a ceiling on convenience rather than on adversarial detection — but a weights-only detector that flags a strict subset of what a filename already flags has not earned its complexity on ordinary Hub traffic. The misses are not near-misses: `mlabonne/Qwen3-0.6B-abliterated` reads $-0.9637$ against its own parent's $-0.9641$, a paired shift of $4\times10^{-4}$.

Two negatives from earlier iterations survive unchanged and bound what this family of statistics can ever be. Behaviourally-uncensored fine-tunes sit squarely inside the instruct distribution on every weights-only statistic despite complying with 51% and 84% of harmful requests, and Qwen3-4B-SafeRL is indistinguishable in the weights while behaving very differently. **A weights-only test answers "has this checkpoint been directionally edited?", not "is this checkpoint safe?"**

## The mechanism: discovery and completion, not uniformity

[FIGURE:fig3]

Holding host and direction fixed and varying only the kernel isolates why. The Gaussian depth sweep is the cleanest single experiment in this paper. At the peak layer (18 of 28) the annihilation is *complete at every spread*: $\log_{10}\min_m e_r = -4.53$ from spread 0.5 to $\infty$, so the completion condition never varies. What varies is discovery. Between spread 8 and 16 the minimum depth weight rises from 0.0796 to 0.5311, $|\cos(v_1,r)|$ jumps from 0.126 to 0.9992, and $W05$ falls from $-1.013$ — its parent's value — to $-2.888$, crossing $\tau$. The transition occupies two sweep steps, so the stamped *shape* prediction (threshold, not ramp) held while the stamped *critical spread* of 58.17 was wrong by a factor of 3.6, bracketing the controlling minimum depth weight in $[0.0796, 0.5311]$ rather than at the predicted 0.9533. The middle-50% band edits half the stack completely and is still missed, for the same reason: the untouched half keeps $r$ from ever becoming the Gram's minimal direction.

The complementary failure is completion without discovery's help. A uniform projection at $w=0.85$ has $|\cos(v_1,r)| = 0.999$ — perfect discovery — and $\log_{10}\min_m e_r = -1.725$, above $\tau$: it is invisible while being behaviourally as effective as the full edit (refusal 0.225 versus 0.200, both against the host's 0.925). Combining the two conditions into the post-hoc rule *detected $\Leftrightarrow$ discovery $\wedge$ completion* reproduces **19 of 19** applicable kernels with zero disagreements; the five inapplicable ones are the rank-$k$ and Heretic variants, where the removed direction is by construction not $r$.

[FIGURE:fig4]

The consequence for an auditor is stated most sharply by intersecting effectiveness with detectability. Of the in-house kernels that pass the fluency screen **and** actually remove refusal (judge-scored $\leq 0.50$ against the host's 0.925 [0.801, 0.974]), 10 qualify and only **4** are detected. The two most effective are both invisible: ORBA's Householder at $\lambda=1.0$ drops refusal to **0.100** while moving $W05$ by $4.1\times 10^{-5}$ — *less* than a Householder about an unrelated random direction moves it ($7.3\times 10^{-5}$), i.e. below the measured noise floor, exactly as an isometry must, since a reflection removes no rank and leaves the Gram spectrum invariant. Heretic's per-component kernel drops refusal to **0.125** and is missed at $W05 = -1.716$. Meanwhile `rank_k4` *is* detected at $-5.630$ and barely uncensors at all (refusal 0.650). Detectability and effectiveness are close to orthogonal on this sweep, and where they correlate, they correlate the wrong way.

One further result belongs here because it changes how the archived numbers should be read. Storage precision caps the scar: the *same* complete uniform projection reads $W05 = -4.592$ stored in bfloat16 and $-12.705$ stored in float32. bf16 rounding, not the edit, sets the archived depth. A related conditioning finding fell out of the reproduction gate: the rebuilt root is bit-identical to the archive (`write_matrix_sha256` matches) and $W02/W03/W05$ reproduce to $1.3\times 10^{-5}$, yet $W01$ and $W04$ differ by $3.1\times 10^{-2}$ — both are log ratios against $\lambda_1$, which on an abliterated checkpoint sits at the float32 Gram-accumulation floor, and float64 recomputation moves $W01$ by exactly the archive's disagreement ($4.7894\times10^{-2}$ against $4.7894\times10^{-2}$). $W01$ and $W04$ are not reproducible below ~0.05 on abliterated checkpoints. $W05$ is, and nothing in this paper depends on $W01$ or $W04$.

## Decoupled from safety in both directions, by construction

[FIGURE:fig5]

The previous draft argued the dissociation between the weight scar and un-censoring from a construction-time observation about direction selection. This iteration builds both failure directions as checkpoints and measures them.

| checkpoint | harmful refusal | $W05$ | certificate says |
|---|---|---|---|
| `Qwen/Qwen3-1.7B` (parent) | 0.950 [0.83, 0.99] | $-1.010$ | clean |
| root A, uniform all-layer | 0.167 [0.11, 0.25], $n{=}114$ | $-4.592$ | edited |
| **root B, depth-weighted Gaussian** | **0.270 [0.20, 0.36]**, $n{=}111$ | **$-1.010$** | **clean** (false negative) |
| `meta-llama/Llama-3.2-1B-Instruct` (parent) | 1.000 | $-1.594$ | clean |
| **root C, AUROC-argmax direction** | **0.950 [0.83, 0.99]** | **$-4.587$** | **edited** (false positive) |

Root B is not a corner case constructed to embarrass the statistic; it is the mlabonne-style depth kernel, built on the same host with the direction held fixed at root A's so that only the kernel differs. It un-censors genuinely (0.950 $\to$ 0.270, intervals disjoint) and stays fluent (WikiText perplexity 27.28), and every one of the six weight statistics returns the *parent's* value, with $\cos(v_1,r) = 0.0199$: the eigendecomposition never surfaces the injected direction because un-edited layers dominate the Gram sum. $W05$ stays at $\approx -1.010$ across all fourteen of root B's laundering cells, so the laundering ladder is **undefined** for it. In the Hub census, `R4_PARTIAL_LAYER_OR_PER_HEAD` — the non-uniform class root B instantiates — is 235 of 513 (45.8%) of declared edits, the largest declared class.

Root C is the mirror image and it comes from a method decision, not an attack. Held-out harmful-versus-benign AUROC *saturates* on these models — eleven layers $\geq 0.997$ and four tied at exactly 1.000 on Qwen3-1.7B — so the argmax is decided by a tie-break. Selecting the direction by AUROC argmax on Llama-3.2-1B-Instruct produces the full weight signature at $W05 = -4.587$ while the model refuses at its parent's rate. An auditor reading only weights would flag a checkpoint whose safety behaviour is untouched.

## The deployment number, on a denominator that matches its description

The previously reported "0 of 160 undeclared sub-4B Hub checkpoints" rested on a population that did not match its label: roughly 30 unit-test fixtures at $d_{\text{model}}=8$ and $L=2$, three single-layer speculator draft heads, several sub-30MB toys, and at least one 14B quantized re-upload admitted by a download-ranked candidate list. Under the pre-stamped eligibility rule the archived scan yields **82** eligible rows; extending it with 40 newly fetched eligible repositories scored smallest-first gives a primary denominator of **122**, on which the false-positive rate is **0/122, Wilson 95% $[0, 0.031]$** [ARTIFACT:art_VFF9Dum9x3KJ]. The raw 0/160 is retained as a labelled secondary row with its Wilson $[0, 0.023]$ and the note that its population contains fixtures and re-uploads. An independent re-analysis applying a slightly stricter reading of the same rule to the archived rows alone gives 85 of 160 eligible and $[0, 0.043]$ [ARTIFACT:art_ckuwEkspyins]; the two implementations disagree on three archived rows and agree on the rate.

The eligible population's composition is published rather than asserted. Archived eligible rows: qwen2 23, llama 19, qwen3 9, gpt\_neox 6, phi3 5, olmo2/phi/smollm3/phi3\_v/granite/gemma3\_text 2 each, and one each of falcon\_h1, stablelm, nanbeige, bloom, mistral, speech\_to\_text. Newly fetched eligible rows: gpt\_neox 29, llama 4, qwen3 2, mistral 2, olmo2 2, doge 1. Exclusions by primary reason, archived: E1 (too few layers) 67, E6 (quantized re-upload) 50, E3b (byte-derived oversize) 9, E2 5, E4 2, undecidable 3.

**Threshold brittleness.** The operating point is panel-fitted on 44 checkpoints, carried by a 0.0763 log-unit margin between two individual checkpoints (`huihui-ai/Qwen2.5-0.5B-Instruct-abliterated` at $-2.7415$ and `allenai/OLMo-1B-hf` at $-2.6652$), and never validated out of panel. Sweeping $\tau$ from $-3.0$ to $-2.4$ on the eligible population gives 0 hits at $-3.0$ through $-2.7$, 1 hit at $-2.6$ and 2 at $-2.5$ and $-2.4$; the first false positive is `rinna/japanese-gpt-neox-small` at $-2.6139$, a shift of **0.128** log-units, about 1.7 margin widths. We say plainly that 0/122 is a statement about a threshold fitted elsewhere, not a validated operating point.

**Quantization, split into its two distinct claims.** The previous draft reported int4 as an evasion. Two corrections. First, the proposed remedy — dequantize to fp16 and rescore — is **void as stated**: the archived `quant_sd` is a fake-quant computing $\mathrm{round}(W/s)\cdot s$ and writing the result back in the model's own bfloat16 dtype, so the archived int4 number *was already* a dequantized measurement and there is nothing left to dequantize. The substantive version instead sweeps bit-width with a dependency-free reference quantizer: $W05$ reads $-4.197$ at 8 bits, $-3.270$ at 6, $-2.654$ at 5 — already above $\tau$, with refusal still 0.237 and perplexity moving only 26.25 $\to$ 28.77 — then $-2.009$ at 4 and $-1.281$ at 3, the last with perplexity 272, a destroyed model whose 0.692 "refusal" is degeneracy. The scar therefore dies at **5 bits**, not 4. The clean parent is essentially untouched by the same rounding ($-1.010 \to -0.957$), $\cos(v_1,r)$ stays above 0.9994 at every bit-width — so the mechanism is *the null filling in*, not the eigenvector rotating — and a proposed noise-floor-relative statistic $W05\text{rel}$ **fails**, tracking $W05$ to below 0.001 everywhere, because the energies are already normalised by each matrix's Frobenius norm, which rounding inflates proportionally, so the floor never moves. A `bitsandbytes` cross-check agrees on nf4 to $10^{-4}$ and disagrees on fp4 by 0.125 log-units (different level sets), reported rather than smoothed. Second, and separately: in the wild-scan pipeline a quantized upload is **UNRESOLVED**, not clean. Of the archived unresolved rows, 50 are excluded as quantized re-uploads by E6 and the remainder are unsupported architectures and Conv1D-transposed layouts. At hub scale the operational effect of quantizing an edited checkpoint is refusal-to-score — itself an auditable signal — rather than a silent false negative. Finally, "for free" overstated the cost: int4 raises WikiText perplexity 26.25 $\to$ 37.72, a 43% quality cost a deployer notices, and the fluency screen it passes is distinct-3, not perplexity.

## The parent buys real coverage

The previous draft's cleanest sentence — "on the recipes it was characterised on, parent-free costs nothing" — is true and now obviously beside the point. On the at-scale panel, with $E_1$ computed against the resolvable parent at three depth bands, $E_1$ at a 0.9 threshold fires on **13 of 32** rows while $W05$ fires on **7 of 35**, and it reaches classes $W05$ never touches: Gaussian-depth, Heretic per-component and partial-layer edits all appear among $E_1$'s detections and none among $W05$'s. Agreement between the two is 0.829.

This also answers the reviewer's band-sensitivity objection with data rather than a caveat. $E_1$ was recomputed at $[0.25L, 0.75L]$ (our reading of the incumbent's mid-stack), full stack, and $[0.4L, 0.6L]$: the detection vector is **identical** across all three bands and agreement with $W05$ is 0.8286 in every case. The "complementary failure modes" conclusion is band-invariant. On the archived matched-pair subsets, the primary band reproduces the previous numbers exactly (12 pre-declared pairs: $E_1$ 1.000, $W05$ 1.000, paired difference $+0.000$; 15 pairs: 1.000 against 0.833, $-0.167$ $[-0.444, 0.000]$; 41 pairs including synthetics: 0.976 against 0.790, $-0.186$ $[-0.373, -0.076]$), and the synthetic dependence is made visible — excluding the 26 in-house synthetics the interval reverts to $-0.167$ $[-0.444, 0.000]$ and covers zero [ARTIFACT:art_ckuwEkspyins]. The honest summary is that the parent-free constraint costs *coverage*, roughly a factor of two in sensitivity at this scale, and what it buys is immunity to a spoofed reference and applicability to the majority of Hub repositories that name no parent.

## Laundering, with error bars and three roots

The reviewer objected that the previous ladder reported differences of 0.004 and 0.027 on a 40-item instrument. That objection is upheld in full and the affected claims are retired. Re-deriving the achieved denominators gives 31–40 rather than the recorded 40, so the unlaundered root's rate is 6/37 $=$ 0.162 [0.077, 0.311]; all four previously signed "evasion costs" ($-0.004$, $+0.069$, $+0.075$, $+0.128$) and the int4-minus-root difference ($-0.03$ $[-0.189, +0.135]$) are **not resolvable differences**, and the smallest upward difference detectable at $n=40, p=0.20$ is 0.29 [ARTIFACT:art_ckuwEkspyins].

What survives, re-run at $n>100$ with intervals, is the *ordering*, on three laundering families and two architectures. For root A, the flag dies at merge weight 0.10 while harmful refusal is 0.231 [0.126, 0.383] — statistically indistinguishable from the unlaundered root's 0.167 [0.11, 0.25] — and un-censoring does not die until $w = 0.50$ (refusal 0.725 [0.572, 0.839]). Add-back-all dies at $\varepsilon = 0.10$ (refusal 0.231) against un-censoring death at $\varepsilon = 0.50$–$1.00$ (0.625, 0.925). Quantization kills the flag at nf4 (refusal 0.211 [0.111, 0.363]) and never kills the un-censoring. For root C on Llama-3.2-1B-Instruct the same three families give **identical** flag-death intensities (merge 0.10, add-back 0.10, quantization nf4), with refusal 0.617 [0.53, 0.70] $\to$ 0.633 [0.54, 0.71]. Root C's behaviour gate fails honestly — 1.000 $\to$ 0.617 is interval-disjoint but above the 0.30 target — and it is labelled signature-positive, partially un-censored, not counted as a clean root. For root B the ladder is undefined, because no flag ever fires.

Two previously reported reversals survive: a one-matrix argmin patch does not defeat a minimum-over-layers statistic (a local patch rotates $v_1$ and lifts *every* matrix's energy, so four matrices must be patched), and 200 steps of benign LoRA-SFT move $W05$ only $-4.592 \to -4.381$ while *restoring* refusal.

## The behavioural negative, bounded and priced

[FIGURE:fig6]

For *graded* safety behaviour the 53-metric battery is not rebuilt; it is re-analysed. No interior observable beats a trivial black-box baseline, but the design's minimum detectable paired difference is $|\Delta\rho| = 0.32$ at 19 lineages (power 0.012 at 0.20, 0.70 at 0.30; roughly 150 lineages would be needed at 0.20), the falsifier could have failed, split-half reliability is $r_{xx}=0.968$ so the negative is not an attenuation artefact, and the conclusion is invariant across three relative depths spanning a saturated AUROC plateau. The named baseline in the previous draft was also mis-identified: $B09$ (greedy refusal rate) is not the best black-box metric — $B08$ first-token entropy asymmetry leads at lineage level ($|\rho| = 0.782$ against 0.668) and $B01$ logit gap at member level (0.708 against 0.670) — which *strengthens* the negative.

This iteration adds the cost annotation the reviewer asked for, and it reframes the negative correctly [ARTIFACT:art_ckuwEkspyins]:

| metric | prompts | harmful prompts | forward passes | wall-clock (s) | $\rho$ (member) | $\rho$ (lineage) |
|---|---|---|---|---|---|---|
| $A19$ refusal-axis / unembed cosine | 65 | 40 | 192 | 9.06 | $+0.763$ | $+0.800$ |
| $B01$ first-step logit gap | 65 | 40 | 80 | 0.40 | $+0.708$ | $+0.659$ |
| $A11$ prompt-position refusal log-odds | 65 | 40 | 80 | 0.40 | $+0.702$ | $+0.671$ |
| $B08$ first-token entropy asymmetry | 65 | 40 | 80 | 0.40 | $-0.672$ | $-0.782$ |
| $B09$ greedy refusal rate | 65 | 40 | 6,720 | 28.35 | $+0.670$ | $+0.668$ |
| $A02$ AMS concept cosine | 65 | 40 | 96 | 0.95 | $+0.631$ | $+0.573$ |
| $W05$ min layer energy | **0** | **0** | **0** | 11.44 | $+0.251$ | $+0.248$ |

Interior observables **are** predictive: $A19$ reaches $\rho = +0.763$ $[+0.592, +0.864]$ at member level and $+0.800$ at lineage level, comparable to $B01$ and better than $B09$ at a thirty-fifth of the forward passes. What they do not do is beat a 40-prompt greedy refusal rate by a resolvable margin: the paired lineage-bootstrap difference for $A19$ against $B09$ is $+0.0045$ $[-0.225, +0.260]$, and comparing point estimates alone would have called that a win. Zero of the candidates beat $B09$ positively with an interval excluding zero; the one interval that excludes zero is $W02$ at $-0.457$, i.e. worse. The practitioner-facing conclusion is therefore about *marginal value over a cheaper instrument*, not about whether the interior carries signal.

## Windowing: the diagnosis points at a fix

If the blind spot is pooling, un-pooling should remove it, and on the diagnostic that defined the blind spot it does. The archived unit test edits 4 of 12 matrices on a toy stack ($d = 64$, $L = 12$): the pooled statistic reads $W05 = -0.838$ against a clean reference of $-0.289$ and $W02 = 0$, reproducing the archived blind spot. The windowed statistic at $k = 2$ reads $-13.43$ against a clean reference of $-0.829$; at $k = 4$, $-1.484$; at $k = 6$, $-1.448$; at $k = 8$, $-1.199$; at $k = L$, $-0.838$, identical to the pooled value. The recovery is monotone in window size and complete at the smallest window. The gate also **corrects an archived claim**: the archive described $v_1$ under partial editing as "no longer the injected direction at all", but the measured cosine is 0.857 — the pooled statistic stops firing while the direction is still partly visible, which is a weaker and more accurate statement.

On real models the windowed statistic behaves as a generalisation should: $k=L$ reproduces $W05$ to $8.5\times 10^{-8}$ across 40 checkpoints, and specificity is 1.000 at every $k \in \{2,4,6,8,L\}$ and every consistency threshold $\tau_c\in\{0,0.5,0.8,0.9,0.95\}$ on the eligible undeclared population, confirming the one stamped prediction that could be scored (P4: specificity non-increasing as $k$ shrinks). **We state the limitation without softening it: the positive arm did not run.** No real edited checkpoint and no synthetic band, Gaussian, ORBA or sub-unit variant was scored with $W05w$ in this artifact, so its four substantive predictions (P1, P2, P3, P5) are UNRESOLVED, and no sensitivity number for $W05w$ appears anywhere in this paper. What we have earned is a mechanism, a generalisation that provably contains the incumbent as its $k=L$ special case, a demonstration on the diagnostic that defined the failure, and evidence that the multiple-window false-positive hazard did not materialise at $n=40$. That is a well-posed next experiment, not a result.

## An audit of our own reporting

Because this paper's argument is measurement discipline, its own numbers are audited mechanically [ARTIFACT:art_ckuwEkspyins]. A 110-claim assertion table returns 105 MATCH, 5 MISMATCH, 0 UNAVAILABLE, with declared tolerances and byte-identical output across two runs. The five disagreements are the product: (i) the crossing table holds **seven** real intensity axes, not the six the draft quoted, though the per-verdict counts were right; (ii) the scan holds **81** unresolved non-control rows, not 65 — the stale figure is adjudicated mechanically; (iii) 8 skipped, not 7; (iv) **five** quoted values from the previous draft are unreproduced, not four; and (v) $B09$'s $0.766$ is the 26-member `renderer == chatml` value, while the draft attributed it to the 28-member contract subset where the correct value is 0.670 — the number was right, the subset label was not. Four values the earlier draft presented as correlations remain paired differences on a different subset, and the falsifier's verdict is unchanged on both readings. Panel and scan counts in this paper are generated from rows rather than transcribed: 270 rows $=$ 20 controls $+$ 250 attempted, 160 completed. "Pre-registered" is reserved for what the frozen `metric_spec.py` (sha256 `544ff994…`) actually stamps — 53 metric declarations plus the held-out split's seed and fraction and nothing else — giving 4 SUPPORTED, 2 PLAN-ONLY, 6 UNSUPPORTED across twelve previously pre-registration-flagged claims.

# Discussion

**What we now believe, and what we retract.** We retract two claims from the previous draft. The first is *uniformity*: a uniform edit at sub-unit weight is invisible and behaviourally effective, and a strongly non-uniform Gaussian kernel at large spread is detected, so uniformity neither implies nor is implied by detectability. The correct predicate is the conjunction of discovery and completion, and it reproduces the sweep exactly. The second is *"parent-free costs nothing"*: it costs about a factor of two in sensitivity at scale and, more importantly, it costs the specific recipe classes that dominate the Hub. What we retain is narrow and, we think, worth keeping. The certificate has genuinely excellent precision — 0 false positives on 122 eligible undeclared checkpoints, on 32 at-scale negatives including 20 fresh parents, and on every leave-one-recipe-class-out cell — at zero prompts, zero forward passes and roughly 7 s of CPU linear algebra. It is a *precision instrument with almost no recall*, and we now know exactly which mechanism supplies each half.

**Why the mechanism is the contribution rather than the metric.** The value of a two-condition account is that it converts a list of anecdotes into predictions. It explains the layer-fraction threshold ($f^\star = 1.00$), the middle-50% invisibility, the depth-kernel misses, the ORBA null result and the sub-unit misses as instances of two failures rather than five mysteries; it predicts that an isometry can never be seen by any statistic reading the Gram spectrum, which is a permanent boundary rather than a calibration gap; and it identifies pooling as the cause of the discovery failure, which is actionable, because pooling is a design choice. The windowed statistic follows directly and contains the incumbent as its $k = L$ special case. We would rather ship a mechanism with a well-posed next experiment than a metric with an AUROC.

**What a deployer should do today.** Not run $W05$ alone. On this evidence the defensible pipeline is: read the repository name first, since it is free and catches 0.727 of ordinary traffic; run $E_1$ wherever a parent resolves, since it roughly doubles coverage and reaches the depth-weighted classes; treat a $W05$ hit as *sufficient but never necessary* evidence of a uniform complete edit; treat UNRESOLVED as a signal rather than a pass; and never treat any of it as a safety score, because §5.3 exhibits a checkpoint that un-censors and reads clean and another that reads edited and never un-censored.

**Limitations.** (1) The at-scale sensitivity of 0.159 rests on 44 checkpoints with declared-or-card-derived recipe labels, a weak label; 23.4% of edited Hub rows declare no mechanism at all. (2) The two-condition rule is post-hoc, derived from the sweep it explains, and its 19/19 agreement is therefore a consistency check, not an out-of-sample validation. (3) The windowed statistic has **no** positive evaluation on real or synthetic edits; its four substantive predictions are unresolved, and the multiple-window false-positive hazard is only bounded at $n = 40$. (4) The operating threshold is panel-fitted on 44 checkpoints, never validated out of panel, and a 0.128 log-unit shift produces the first false positive. (5) $W01$ and $W04$ are not numerically reproducible below ~0.05 on abliterated checkpoints, and the depth of the scar is set by bf16 storage rounding, not by the edit. (6) Ground truth is judge-derived and bounded by 40 harmful and 25 XSTest-safe items per member; a 40-item instrument cannot resolve 0.15 at $p\approx 0.3$, which is why the ladder is reported as an ordering. (7) Root C's behaviour gate fails (1.000 $\to$ 0.617), so the cross-architecture range rests on a partially un-censored root. (8) The behavioural arm is 28 members over 19 lineages with 11 singletons; nothing smaller than $|\Delta\rho| = 0.32$ is resolvable there. We delete the previous draft's limitation that public mechanically-different recipes exist only at $\geq 14.9$B: our own prior-art artifact records public MPOA, Heretic and OBLITERATUS checkpoints at 4,022,468,096 parameters on the panel's own Qwen3-4B family, and this iteration measured seven Heretic checkpoints directly.

**What we would do next.** Three things follow directly. First, run the windowed statistic's positive arm: the band, Gaussian, Heretic, ORBA and sub-unit kernels already exist as checkpoints in this study's Arm B, and scoring them with $W05w$ is a re-analysis rather than a new experiment. Second, test the discovery condition's fix independently of the completion condition, by scoring windows against a *random-direction* null per window, which would convert the multiple-window hazard into a calibrated per-window false-positive rate. Third, close the loop on the isometry boundary: if a Householder reflection is provably invisible to any Gram-spectrum statistic, then reflection-based recipes define the permanent limit of this family of certificates, and an auditor needs a different observable — most plausibly a per-layer *rank* rather than a per-layer energy.

# Conclusion

We asked whether a checkpoint's safety provenance can be read from its tensors alone, and this iteration answers by taking the question to scale and reporting what broke. On 44 real edited checkpoints from 27 uploaders across 9 recipe classes, a parent-free spectral certificate that reached oriented AUROC 1.000 on its calibration panel fires on 7 — sensitivity 0.159 — while a regex over the repository name reaches 0.727 at the same perfect specificity and catches everything the certificate catches. The positive result is the reason. Detection requires two independent conditions, *discovery* that the pooled Gram surfaces the edited direction and *completion* that some layer is annihilated deeply enough, and a rule combining exactly those two reproduces 19 of 19 controlled kernels where the host and the removed direction are held fixed. That account retires our previous uniformity story, explains five separate blind spots as two failures, predicts that an isometry is permanently invisible, and identifies pooling as the fixable half — a windowed statistic that contains the pooled one as its $k=L$ special case recovers the diagnostic blind spot by 12.6 log-units at unchanged specificity, with its positive arm still to run. Alongside that, two checkpoints built to order settle what such a certificate can mean: a depth-weighted edit that un-censors from 0.950 to 0.270 and reads its parent's value exactly, and an AUROC-selected edit that reads $-4.587$ while refusing at its parent's rate. The certificate's precision is real — 0 false positives on 122 eligible undeclared checkpoints under a pre-stamped rule — and its recall at Hub scale is not. The useful single-checkpoint question is not "is this model safe" but "has this model been edited, and by a recipe this instrument can see"; this paper's contribution is that the second half of that question now has a mechanical answer.

# References

[1] A. Arditi, O. Obeso, A. Syed, D. Paleka, N. Rimsky, W. Gurnee, and N. Nanda. Refusal in Language Models Is Mediated by a Single Direction. *NeurIPS*, 2024. arXiv:2406.11717.

[2] J. Hurtado. Has This Checkpoint Been Abliterated? A Two-Signal Audit and Its Failure Map. *arXiv:2607.01854*, 2026.

[3] G. Messenger. Detecting Safety Training Modification in Language Models via Activation Analysis. *IEEE Access*, 14:91723–91737, 2026. arXiv:2608.05578.

[4] C. Huang, Y.-L. Chen, C.-M. Yu, and W.-B. Lee. RAS: Measuring LLM Safety Through Refusal Alignment. *arXiv:2606.25750*, 2026.

[5] S. Peng, P.-Y. Chen, M. Hull, and D. H. Chau. Navigating the Safety Landscape: Measuring Risks in Finetuning Large Language Models. *NeurIPS*, 2024. arXiv:2405.17374.

[6] S. Basu, S. Y. Patel, P. Sheth, B. Muralidharan, N. Elamaran, A. Kinra, J. Morgan, and R. Batniji. Interpretability without actionability: mechanistic methods cannot correct language model errors despite near-perfect internal representations. *arXiv:2603.18353*, 2026.

[7] M. Galeone et al. Perfect Detection, Failed Control: The Geometry of Knowing vs. Steering in Language Models. *arXiv:2606.24952*, 2026.

[8] A. Paul. Spectral Geometry of LoRA Adapters Encodes Training Objective and Predicts Harmful Compliance. *arXiv:2604.08844*, 2026.

[9] Z. Zhong and A. Raghunathan. Watch the Weights: Unsupervised Monitoring and Control of Fine-tuned LLMs. *arXiv:2508.00161*, 2025.

[10] Detecting Backdoored LoRAs from Weights Alone. *arXiv:2602.15195*, 2026.

[11] elder-plinius et al. OBLITERATUS: one-click model liberation toolkit, including `obliteratus/analysis/spectral_certification.py`. Software, AGPL-3.0, first public 2026-03-04.

[12] `reverse-abliterate` 0.1.2. Software package: metadata- and filename-based abliteration scanner.

[13] M. Labonne. Uncensor any LLM with abliteration. Hugging Face community blog, 13 June 2024.

[14] P. E. Weidmann. Heretic: fully automatic censorship removal for language models. Software, `src/heretic/model.py`, `config.default.toml`, 2025–2026.

[15] J. W. Lai (grimjim). Norm-Preserving Biprojected Abliteration (MPOA). Hugging Face community blog, 6 November 2025.

[16] J. W. Lai (grimjim). ORBA: Orthogonal Reflection Bounded Ablation. Hugging Face community blog, 25 March 2026.

[17] G. Guelmez. Gabliteration: Adaptive Multi-Directional Neural Weight Modification. *arXiv:2512.18901*, 2026.

[18] J. Young et al. Comparative Analysis of LLM Abliteration Methods: A Cross-Architecture Evaluation. *arXiv:2512.13655*, 2025.

[19] S. Jain, E. S. Lubana, K. Oksuz, T. Joy, P. H. S. Torr, A. Sanyal, and P. K. Dokania. What Makes and Breaks Safety Fine-tuning? A Mechanistic Study. *NeurIPS*, 2024. arXiv:2407.10264.

[20] B. Wei, K. Huang, Y. Huang, T. Xie, X. Qi, M. Xia, P. Mittal, M. Wang, and P. Henderson. Assessing the Brittleness of Safety Alignment via Pruning and Low-Rank Modifications. *ICML*, 2024. arXiv:2402.05162.

[21] H. Lu, Y. Zhou, S. Liu, Z. Wang, M. W. Mahoney, and Y. Yang. AlphaPruning: Using Heavy-Tailed Self-Regularization Theory for Improved Layer-wise Pruning of Large Language Models. *NeurIPS*, 2024. arXiv:2410.10912.

[22] H. Abu Shairah, H. Hammoud, B. Ghanem, and G. Turkiyyah. An Embarrassingly Simple Defense Against LLM Abliteration Attacks. *arXiv:2505.19056*, 2025.

[23] J. Fafula. Abliteration Is Not a Scalpel: Off-Target Effects of Refusal Removal on Decision Disposition Across Model Families. *arXiv:2607.17427*, 2026.

[24] A. Hasan and S. Biswas. The Refusal-Compliance Tradeoff: A Large-Scale Safety Behavior Audit of Large Language Models. *arXiv:2605.05427*, 2026.

[25] A. Zou, Z. Wang, J. Z. Kolter, and M. Fredrikson. Universal and Transferable Adversarial Attacks on Aligned Language Models. *arXiv:2307.15043*, 2023.

[26] P. Chao et al. JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models. *NeurIPS Datasets and Benchmarks*, 2024. arXiv:2404.01318.

[27] M. Mazeika et al. HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal. *ICML*, 2024. arXiv:2402.04249.

[28] P. Röttger, H. R. Kirk, B. Vidgen, G. Attanasio, F. Bianchi, and D. Hovy. XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models. *NAACL*, 2024. arXiv:2308.01263.

[29] L. Zheng et al. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *NeurIPS*, 2023. arXiv:2306.05685.

[30] T. Xie et al. SORRY-Bench: Systematically Evaluating Large Language Model Safety Refusal Behaviors. *ICLR*, 2025. arXiv:2406.14598.

[31] Y. Zeng et al. AIR-Bench 2024: A Safety Benchmark Based on Risk Categories from Regulations and Policies. *arXiv:2407.17436*, 2024.

[32] L. Li, B. Dong, R. Wang, X. Hu, W. Zuo, D. Lin, Y. Qiao, and J. Shao. SALAD-Bench: A Hierarchical and Comprehensive Safety Benchmark for Large Language Models. *ACL Findings*, 2024. arXiv:2402.05044.

[33] L. Sun et al. TrustLLM: Trustworthiness in Large Language Models. *ICML*, 2024. arXiv:2401.05561.

[34] N. Sapwell. Abliterlitics: open-source abliteration forensics. Software, AGPL-3.0, `github.com/dreamfast/abliterlitics`, first public 2026-04-24; model reports at `abliterlitics.dev`.

[35] Z. Zhang, I. V. Prasad, Y. Hu, Z. Liu, H. Luo, P. Ren, and Y. Yang. Spectral Signatures of Large Language Models. *arXiv:2607.03377*, 2026.

[36] K. Dewage, M. Pensky, S. De Silva, and T. H. Bandara. Spectral Outliers Reveal Dominant Learned Structure in Transformer Attention. *ICMLA*, 2026. arXiv:2608.07921.

[37] R. Zhang and D. Goldstein. Matrix-Driven Identification and Reconstruction of LLM Weight Homology. *arXiv:2508.06309*, 2026.

[38] A. R. Coslett. Safety-Alignment Removal as a Model-Identity Failure — Structural Evidence from Published Weight-Level Mutation Checkpoints. Fall Risk AI, 2026. Zenodo DOI 10.5281/zenodo.19383019.

[39] COSMIC: Layer Selection for Abliteration. *ACL*, 2025. arXiv:2506.00085.

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

--- Item 16 ---
id: art_dp7WBo6hhVBX
type: experiment
title: Does the abliteration weight scar generalise?
summary: |-
  Stress-tests the parent-free abliteration detector W05 (log10 of the minimum per-matrix energy along the smallest-eigenvalue direction of the shared Gram matrix over residual-write matrices; detect iff W05 <= tau = -2.7415117804288127). 13 signed predictions were stamped and sha256-hashed BEFORE any checkpoint was downloaded (results/predictions.json); a second stamp (w* = 0.9533, critical spread 58.17) was hashed once W05_ref was measured. verify.py re-derives every headline number from the raw rows: 20/20 pass. Tier 2, $0.022 OpenRouter, 361 GB streamed.

  HEADLINE, AT SCALE: specificity 1.000 (0 false positives on 32 negatives incl. 20 fresh Hub parents) but sensitivity 0.159 on 44 real edited checkpoints from 27 uploaders across 9 recipe classes, while the 5 archived panel members it was calibrated on all still fire (1.000). Five of the 7 detections are ONE uploader's norm-preserving family; a sixth clears tau by 0.09. It does NOT beat the baseline the manifest demanded: a repo-name regex scores 0.727 sensitivity at the same 1.000 specificity on identical rows, and the set W05 catches that the name misses is EMPTY. Misses are not near-misses: mlabonne/Qwen3-0.6B-abliterated reads -0.9637 vs its parent -0.9641.

  MECHANISM (Arm B: host Qwen3-1.7B and direction r held fixed, kernel is the only variable, 25 kernels x 2 storage precisions). Uniformity is the WRONG predicate. Detection needs DISCOVERY (|cos(v1,r)| -> 1) AND COMPLETION (min_m e_r <= tau); that post-hoc rule reproduces 19/19 applicable kernels. Every Gaussian spread annihilates the peak layer completely (log10 min_m e_r = -4.53 at ALL spreads) yet detection switches on only between spread 8 and 16, bracketing the controlling min-depth-weight in [0.0796, 0.5311] — nowhere near the stamped w*. The mid-50% band edits half the stack completely and is still missed, because untouched matrices keep r from becoming the Gram's minimal direction.

  EVASION: of 10 fluency-passing edits that actually remove refusal (judge <= 0.50 vs host 0.925), only 4 are detected. The two most effective are invisible — ORBA Householder drops refusal to 0.100 while moving W05 by 4.1e-5, LESS than a random-direction Householder control (7.3e-5); Heretic-style drops it to 0.125 and is missed. rank_k4 is detected but barely uncensors (0.65).

  REPRODUCIBILITY FINDING: the rebuilt in-house root is BIT-IDENTICAL to the archive (write_matrix_sha256 matches) and W02/W03/W05 reproduce to 1.3e-5, yet W01/W04 differ by 3.1e-2. With byte-identical weights that cannot be the model: both are log ratios against lam[0], at the float32 Gram-accumulation floor. Float64 recomputation moves W01 by exactly the archive gap (4.7894e-2 vs 4.7894e-2). W01/W04 are irreproducible below ~0.05 on abliterated checkpoints; W05 is not, and nothing here depends on W01/W04. Fast safetensors path == Runner path EXACTLY (0.0). Storage precision caps the scar: the same complete projection reads W05 = -4.59 in bf16, -12.70 in float32.

  VERDICTS: P1 P2 P3 P6 P7 P9 P11 CONFIRMED; P8 confirmed at the measured noise floor; P10 shape-confirmed / critical-spread refuted (3.6x); P12 PARTIAL (7/7 Arm B classes, 4/6 Arm A); P4 P5 P13 REFUTED. Two falsifiers fired and are reported as the headline.

  SHIPS: method_out.json (110 examples, predict_our_method_W05 vs predict_baseline_E1 vs predict_baseline_repo_name_regex side by side), results/{predictions,predictions_derived,gate_iter4,unit_tests,arm_a,arm_b,arm_b_behaviour,layer_profiles,analysis,cards}.*, verify.py, and byte-identical vendored iteration-3 libraries with sha256 recorded.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 17 ---
id: art_VFF9Dum9x3KJ
type: experiment
title: Can a windowed weight scan catch hidden edits
summary: >-
  Three-arm, tensor-only, prompt-free experiment (zero forward passes, zero LLM calls, $0.00 OpenRouter). ARM 1 introduces
  W05w, a sliding-layer-window generalisation of the archived pooled-Gram abliteration statistic W05: windows of k consecutive
  layers with stride k//2, per-window minimum-eigenvector v1_win, and W05w(k) = min over windows of the per-window minimum
  write energy, plus a consistency gate c(k) = min adjacent-window |cos(v1)| swept over tau. k=L collapses to the pooled statistic
  and is asserted equal to W05 at 1e-9 on every model as a built-in reproduction gate. ARM 2 freezes and sha256-stamps a pre-registered
  eligibility rule (E1 n_layers>=8, E2 hidden_size>=128, E3 params<=4.2e9 enforced twice from index AND on-disk bytes, E4
  fixtures, E5 speculators, E6 quantized re-uploads) BEFORE any rate is computed, re-derives eligibility on the archived 270-row
  undeclared scan, and extends it with newly fetched eligible repos scored smallest-first from the dependency dataset's 2,139-row
  pool. ARM 3 reports the threshold curve from -2.4 to -3.0 and the smallest shift producing a first false positive. Ships
  numbers.json (every quoted numeral with units, n, CI, CI method, orientation, source file) and verify_numbers.py, which
  recomputes every entry from raw rows and whose exit code is stored in the assertion block.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 18 ---
id: art_VLI4IOs9Xy9P
type: experiment
title: Can you spot a model whose safety was removed
summary: |-
  Two-arm experiment on the archived abliteration 'laundering ladder' (iteration-3 experiment_2). Everything runs on one GPU in ~70 min for $0.161 of a $1.50 judge cap; 8/8 internal consistency checks and an INDEPENDENT verifier (verify.py, 29/29) that re-derives every headline claim from the shipped result files without importing method.py. method_out.json validates against exp_gen_sol_out (7 datasets, 160 rows).

  REPRODUCTION IS EXACT. Rebuilding the archived root from root_recipe.json reproduces parent AND root W01-W05q10 with deltas of exactly 0.00e+00 (not '<1e-6'), 56/311 tensors modified with the rest bit-identical, wikitext ppl identical, int4 W05 = -1.946 and nf4 = -2.126 matching the archive. Two of three archived ladder stages recompute bit-exactly; addback differs by 3.09e-05 (float accumulation order), changing no flag. torch==2.6.0 is pinned deliberately: torch 2.13 routes an outer product through a Triton kernel needing an absent C compiler.

  ARM 1 -- the proposed dequantization remedy is VOID AS STATED: the archive's quant_sd is a fake-quant, so the archived int4 number was already a dequantized measurement. Substantive version instead: rounding kills the scar at 5 BITS (W05 -2.654 > TAU -2.7415) with refusal still 0.237 and ppl only 26.25->28.77. Curve 8b -4.197 / 6b -3.270 / 5b -2.654 / 4b -2.009 / 3b -1.281 (ppl 272, model destroyed). The NEW W05rel statistic FAILS -- it tracks W05 to <0.001 everywhere, because energies are already normalised by each matrix's Frobenius norm, which rounding inflates proportionally. cos(v1,r) stays >0.9994 at every bit-width, so the mechanism is 'the null filled in', NOT 'the eigenvector rotated'; the clean parent is unmoved by the same rounding. Verdict SCAR_STAYS_GONE. bitsandbytes cross-check agrees on nf4 to 1e-4 and disagrees on fp4 by 0.125 log10 (different level sets), reported explicitly.

  THE HEADLINE -- the weight statistic is DECOUPLED from safety behaviour in BOTH directions, by construction, not by correlation. FALSE NEGATIVE: root B, an in-house depth-weighted Gaussian abliteration of Qwen3-1.7B (direction held fixed at root A's so the kernel is the only variable), un-censors 0.950 -> 0.270 [0.20,0.36] at n=111 while staying fluent (ppl 27.28), yet reads W05 = -1.010 -- the PARENT's value -- with all six flags False and cos(v1,r) = 0.0199, because un-edited layers dominate the Gram sum so the eigendecomposition never surfaces the injected direction. W05 stays ~-1.010 across all 14 of its laundering cells, so the ladder is UNDEFINED for it. FALSE POSITIVE: the Llama AUROC-argmax root flags W05 = -4.587 while refusing at 0.950 [0.83,0.99], its parent's rate -- never un-censored. Prevalence: R4_PARTIAL_LAYER_OR_PER_HEAD (the non-uniform class root B instantiates) is 235/513 = 45.8% of edited Hub checkpoints, the largest declared class; the repo-id regex baseline any detector must beat is 50.5%.

  ARM 2a -- the archived ladder's denominators are NOT the recorded 40: achieved denominators recovered from the rates span 31-40, with 13 rows AMBIGUOUS (a rate reducing to a small fraction is compatible with several n). Uses the largest compatible n and ships the smallest-n interval beside it.

  ARM 2b/c -- the archived ordering SURVIVES with real error bars, at n>100, on three laundering families and two architectures: root A 0.167 [0.11,0.25] -> 0.178 [0.12,0.26] at flag death; root C (real gated meta-llama/Llama-3.2-1B-Instruct, no substitution needed) 0.617 [0.53,0.70] -> 0.633 [0.54,0.71]. Flag-death intensities are IDENTICAL across architectures (merge w=0.10, add-back eps=0.10, quant nf4). Root C's behaviour gate FAILS honestly (1.000 -> 0.617, interval-disjoint but above the 0.30 gate) and is labelled signature-positive/partially-un-censored.

  Also ships: TAU brittleness sweep (-2.4..-3.0; at TAU all 8 flagged scan rows are declared-abliterated, and a +0.34 shift is needed for a first undeclared hit), judge integrity (kappa 0.149 over 61 stages, rate-level Pearson r 0.822 -- CORRECTING the archived 0.952 claim), 12 figures, a content-addressed judge cache making reruns $0, and a limitations list naming every gate delta.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 19 ---
id: art_ckuwEkspyins
type: evaluation
title: Rechecking every number in the draft
summary: |-
  PURE RE-ANALYSIS, $0.00 LLM spend, 0 weights loaded, 0 forward passes, 0 generations, 0 Hub fetches, ~21 s on 4 CPUs. Reads the six archived trees (A1-A4 as declared deps, plus A5 iter-3 evaluation-1 and A6 iter-3 research-1 read directly from disk). Every file resolved by GLOB, never by assumed filename; manifest with size+sha256+role; every emitted number carries provenance = {file, line_or_key, raw_value}.

  ASSERTION TABLE: 110 claim_ids -> 105 MATCH / 5 MISMATCH / 0 UNAVAILABLE. Tolerances declared up front (1e-6 verbatim, 1e-4 float re-derivation, 0.005 reconstructed rates, exact string for repo_ids/evidence spans). GATES: A2/verify.py re-run 17/17 PASS; A1 wstats max|dW05| = 9.91e-06 (gate.json full precision 9.908662263136137e-06, so the quoted '9.9e-06' is a 2-s.f. rounding), Spearman 1.0000, ordering preserved. DETERMINISM: two full runs BYTE_IDENTICAL_APART_FROM_TIMING.

  THE 5 DISAGREEMENTS (the product, each classified): (1) crossing.jsonl holds SEVEN real intensity axes (4 EVADABLE + 3 NEITHER_DIES) plus one 'combined' non-axis row - the per-verdict counts are right, the denominator quoted as 6 is stale. (2) scan.jsonl gives 81 UNRESOLVED non-control rows, not 65 - the 65-vs-81 discrepancy is adjudicated mechanically, 65 is stale. (3) 8 SKIPPED, not 7. (4) quoted_value_forensics carries FIVE unreproduced quoted values (A01, A02, A22, B09, W01), not four. (5) B09's 0.766 is the 26-member renderer=='chatml' value (reproduces to 1e-4); on the 28-member contract subset the draft states it is 0.670 - the number was right, the SUBSET LABEL was not; the other four reproduce under NONE of 32 conventions and must be regenerated.

  W1 RELABEL: decision rule published as a literal dict; relabel fires only on a verbatim toolkit string. Two Heretic checkpoints -> per_component_optimised (APPLIED); mlabonne and BennyDaBall -> unknown, NOT_IN_ARCHIVE, PROVISIONAL (mlabonne's Gaussian-depth string is NOT in the archived card text - no kernel is inferred from W05). Honest count: 2 of 4 misses carry a verbatim non-uniform kernel string, unattributed remainder 2. LEAVE-ONE-RECIPE-CLASS-OUT (primary) is where the failure lives: per_component_optimised AUROC 0.264 / sensitivity 0.000 vs uniform_global 0.956 / 0.900; leave-one-uploader-out shipped beside it, identical columns. Limitation 3 REFUTED from A6: sub-4.2B MPOA / Heretic / OBLITERATUS at 4,022,468,096 params on the panel's own Qwen3-4B family. 6-entry draft_edit_list.

  W2 LADDER: 136 interval rows, Wilson primary + 10k bootstrap, ACHIEVED denominators recovered as the LARGEST n <= nominal (31-40, not 40; root 6/37 = 0.162 [0.077, 0.311]). All four signed evasion costs (-0.004, +0.07, +0.07, +0.1) and int4-minus-root (-0.03 [-0.189, +0.135]) are NOT A RESOLVABLE DIFFERENCE. Power: smallest UPWARD detectable difference at n=40, p=0.20 is 0.29, so the ORDERING survives and the decimals do not.

  W3 E_1 BANDS: the archived [0.25,0.75] band reproduces the arm-2 headline exactly (12 pairs 1.000/1.000/+0.000; 15 pairs E_1 1.000 vs W05 0.833, diff -0.167; 41 pairs -0.186 [-0.373,-0.076]). FULL STACK and [0.4,0.6] are NOT_RECOMPUTABLE_FROM_ARCHIVE - per-matrix singular values were never persisted - so the verdict is withheld as UNDETERMINED_INSUFFICIENT_BANDS (INVARIANT at the primary band only, 3/3 checks hold) rather than answered on one band. Synthetic dependence made visible: excluding the 26 in-house synthetics the interval becomes -0.167 [-0.444, 0.000] and COVERS ZERO.

  W4 COST TABLE: 54 rows sorted cost-ascending with prompts / harmful_prompts / forward passes / wall-clock, correlations carried forward verbatim (recomputed=false). 0 candidates beat B09 positively (the one CI excluding zero is W02 at -0.457, i.e. worse). Practitioner sentence bound to provenance: interior observables ARE predictive (A19 rho +0.763 [+0.592,+0.864] member, +0.800 lineage) but do not beat a 40-prompt greedy refusal rate.

  W5 FIDELITY: counts generated from rows (270 = 20 controls + 250 attempted, 160 completed); boundary at full precision -2.7415117804288127 with the abliterated MAXIMUM/minimum stated correctly (-2.7415 / -4.8204, margin 0.0763); oriented-vs-raw AUROC with a convention string; [min,max] for every class x W01-W05 with the base/abliterated overlaps flagged; W03 corrected to 256 directions; the 4.869-vs--4.82 adjacency flagged with a suggested rewrite. Eligibility filter: 85 eligible of 160 (48 n_layers<8, 38 hidden_size<128, 38 name/tag, 4 oversize), FP 0/85 Wilson [0, 0.0432] PRIMARY vs 0/160 [0, 0.0234] SECONDARY. Threshold brittleness: first false positive at -2.61 (rinna/japanese-gpt-neox-small), shift 0.1315 log10 ~ 1.7 margin-widths. Claim map reproduces 4 SUPPORTED / 2 PLAN-ONLY / 6 UNSUPPORTED, totals 12.

  SHIPPED: eval_out.json (schema exp_eval_sol_out PASSED; 8 tabular datasets), results/arm1_real_corrected.jsonl, disagreements.json, draft_edit_list.json, determinism.json, README.md, pinned pyproject.toml verified by rebuilding the venv from scratch.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 20 ---
id: art_gqCRODISeyg2
type: research
title: Who Else Can Spot an Edited Model
summary: >-
  Primary-source dossier closing Abliterlitics and the windowed-statistic novelty question. (A) ABLITERLITICS documented from
  source: AGPL-3.0, repo created 2026-04-24, 10 model reports (~2B-59B MoE), four axes. Every weight metric is DELTA-based
  -- METHODOLOGY 1.1 is `diff = (variant-base).abs().mean()`, 1.2 is `svd(delta_matrix)`, 1.3 needs the base PLUS two variants
  -- so W01-W05 have NO counterpart and W06-W11 are ANALOGOUS-BUT-DISJOINT (not identical, unlike 2604.08844). Parent requirement
  quoted: "Create a directory with your base model and variants, plus a comparison.json"; `base` is a mandatory key, no single-checkpoint
  mode. PLAN WAS WRONG about scale: FOUR reports are at/below ~4.5B, including a full weight report on Qwen3-4B-Instruct-2507,
  OUR OWN PANEL FAMILY (Heretic 33/36 layers, Huihui 36/36; all three peak at L12-19, L16 #1), plus a 13-variant Gemma4-E2B
  report with an explicit early/mid/late band table (coverage 7/35 to 35/35, early share 0%-31%). So A4 is EXTERNAL SUPPORT
  AT OUR SCALE. Verdict SUPPORTS. All planner Qwen3.5-9B numbers re-verified EXACTLY (42/68/62 tensors; 23/29/31 of 32 layers;
  2.83/4.89/2.72%; cosine 1.0 / mean 0.997 / 100% of principal angles). Mandatory cosine-caveat reconciliation written out,
  and DEFUSED by a fact the plan lacked: the same Heretic-Huihui pair is essentially orthogonal (median cosine 0.00017) on
  Qwen3.5-4B, so 0.997 is a property of one base, not the pair. Abliterlitics NAMES our axis first ("Uniform (33/33/33%)"
  for LEACE vs "Mid-to-late focused (42-44% late)" for rank-1), as does Gabliteration ("Unlike the uniform layer modification
  approach in traditional abliteration"). (B) RECIPES from source with signed predictions. HERETIC'S KERNEL IS A TRIANGULAR
  TENT WITH A HARD CUTOFF, not Gaussian/bell-curve as the plan, the dependency and OBLITERATUS all say: `if distance > min_weight_distance:
  continue` then LINEAR interpolation; and max_weight_position is sampled in [0.6L,1.0L], direction_index in [0.4L,0.9L],
  max_weight up to 1.5 -- the peak is CODE-LEVEL forbidden from the early stack, predicting the measured "Layers 0 through
  8 have no real edits". MPOA verbatim four-step with layers [11..41] of [0..47]; ORBA H=I-2uu^T with the author's own "misdirected
  sign-flips" negative result; OBLITERATUS presets 1/4/8/8/4/8/8 re-verified. THREE PLAN REVISIONS: Heretic's shipped default
  is ALREADY norm-preserving (row_normalization="full") but "PR #52" is UNCONFIRMED; OBLITERATUS is LAYER-SELECTIVE (COSMIC),
  so W05 DETECTED -> DEGRADED; ORBA is TWO recipes (lambda=1 is "zeroed WITHOUT reflection" = annihilation; only v3 Householder
  is the isometry) and conflating them makes the falsification test vacuous. W05 and the windowed statistic DISAGREE on six
  recipes -- that set is the payoff. (B3) Census: 1068 hits, 116 sub-4.2B; all Qwen3-4B variants at 4,022,468,096; ORBA STILL
  0 (reimplement); gabliterated 54; Apostate 1, Abliterix 1, AEON 0 genuine; huihui-ai NOT gated (contradicts dependency);
  two traps -- ?search=&full=true carries NO safetensors, and safetensors.total counts QUANTIZED tensors. (C) C1/C2/C3 all
  re-verified verbatim (AUC 0.00 n_bootstrap=972 + "GPT-4o scored 0/300"; certify() takes harmful/harmless ACTIVATIONS; reverse-abliterate
  reads filenames/metadata only). (D) NOVELTY = NOVEL-NARROW, and the plan's premise was wrong: arXiv:2607.01854's E1 is ALREADY
  "band-averaged" over "each layer in the mid-stack band B", so the band idea is published prior art. Four load-bearing qualifiers
  survive: parent-free, calibration-free, BOTTOM-of-spectrum, SLIDING/extremum-scored. Two new must-cite competitors ruled
  out (2607.03377 PL_Alpha_Hill -- parent-free but designed to be INVARIANT to post-training and reads the top; 2608.07921
  MP outliers -- parent-free per-layer but detects structure not edits). Multiple-window FPR warning issued. COSLETT CLOSED
  via DataCite: full abstract obtained, instrument is an inference-time output-geometry/logprob PUF (NOT weights-only), scars
  "7.6 to over 2,300 times the instrument's acceptance threshold" across two model families -- ADJACENT confirmed on primary
  evidence, risk downgraded to SMALL. Ships 16 numbered corrections_to_draft and 9 must-cite additions.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
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

- [MAJOR] (evidence) The paper's sharpest claim -- that the detector collapses on 'the *same* global recipe from four unseen uploaders' (AUROC 0.382, catch rate 0/4), framed throughout as an uploader/calibration effect -- is contradicted by the paper's own artifact. In results/arm1_real.jsonl all four rows carry recipe_class = 'global_diff_in_means' and mechanically_different = false, but the verbatim card evidence stored in those same rows says otherwise: MagicalAlchemist/Qwen3-1.7B-Magic_decensored is 'made using Heretic v1.1.0' with direction_index = 17.89 and attn.o_proj.max_weight = 0.84, and prithivMLmods/VibeThinker-3B-heretic_decensored is 'modified using the Heretic abliteration toolkit'. I fetched the third card: mlabonne/Qwen3-0.6B-abliterated states that the subtraction weight factors 'follow a normal distribution with a certain spread and peak layer'. Heretic is recipe [14] in the paper's own taxonomy (per-component optimised kernel, float direction index, weights that are not 1) and mlabonne v2 is recipe [13] (Gaussian depth kernel) -- both are explicitly *not* the uniform all-layer projection the archived positives use. So at least three of the four misses are depth-weighted or sub-unit-weight kernels, and the finding is a recipe effect, not an uploader effect. This also explains why E1 = 0.995-0.997 on all three: the per-matrix delta is still near rank one, but the annihilation is incomplete in some layers, which is precisely what a minimum-over-layers statistic cannot survive. Compounding this, limitation (3) claims a Hub search 'established the >=14.9B constraint' for mechanically different recipes, while the paper's own cited prior-art artifact art_sHF0cggp2IvT states that MPOA, Heretic and OBLITERATUS all have public sub-4.2B checkpoints at 4,022,468,096 parameters on the panel's own Qwen3-4B family -- and the experiment measured two Heretic checkpoints without recognising them.
  Action: Re-derive recipe_class for all four checkpoints from their cards (quote the Heretic parameter table and mlabonne's normal-distribution sentence in the text), correct the arm1_real.jsonl labels and the mechanically_different flag, and re-run the grouping analysis with RECIPE as the primary variable and uploader as a secondary one. Then rewrite the headline in the Introduction, Contributions, Discussion and Conclusion from 'three of four unseen uploaders running the same nominal recipe escape' to the mechanism the data actually support: 'W05 requires a uniform, complete annihilation in every layer; any depth-weighted or sub-unit-weight kernel (mlabonne v2 Gaussian, Heretic per-component optimised) escapes it, exactly as a band-limited edit does.' Fold this into the f* = 1.00 layer-fraction result as one unified statement about uniformity rather than two separate mysteries. Finally, delete or correct limitation (3)'s >=14.9B claim, which your own research artifact refutes, and add the sub-4.2B MPOA/OBLITERATUS Qwen3-4B checkpoints. This change costs almost no new compute and materially strengthens the paper.
- [MAJOR] (evidence) The flagship deployment number -- '0 of 160 undeclared sub-4B Hub checkpoints, Wilson 95% [0, 0.023]' -- rests on a population that does not match its description. Reading results/scan.jsonl, 44 of the 160 scored repositories are degenerate: roughly 30 unit-test fixtures with hidden_size = 8 and n_layers = 2 (trl-internal-testing/tiny-*, peft-internal-testing/tiny-dummy-qwen2, llamafactory/tiny-random-*, echarlaix/tiny-random-*, yujiepan/llama-2-tiny-random, MaxJeblick/llama2-0b-unit-test, hmellor/tiny-random-*), plus three single-layer EAGLE3 speculator draft heads (RedHatAI/Qwen3-8B-speculator.eagle3, lightseekorg/kimi-k2.6-eagle3-mla, Inferact/MiniMax-M3-EAGLE3), plus several sub-30MB toys. A statistic defined as a minimum of per-layer write energy over an eigenvector of a pooled Gram matrix is not meaningfully defined on a two-layer, eight-dimensional random stub, and a one-layer draft head has a single term in the minimum. These repositories entered because scan_enumeration.json ranks candidates by descending downloads, and CI fixtures are among the most-downloaded objects on the Hub. The same ranking admitted lmstudio-community/Qwen2.5-Coder-14B-Instruct-MLX-4bit (8.3 GB of tensors, 48 layers) into a set the paper calls 'sub-4B'. Ornith-1.0-35B and -9B were caught only by a byte cap, not by the parameter filter, because the Hub's reported param counts for those repos are wrong -- a bug the authors' own dataset artifact documents.
  Action: Define an eligibility rule before reporting the rate -- e.g. n_layers >= 8, hidden_size >= 128, tensor_bytes consistent with <= 4.2B parameters at the declared dtype, and exclude repos whose card or tags identify them as test fixtures, speculator/draft heads, or quantized re-uploads -- and report the false-positive rate and Wilson interval on that filtered denominator as the primary number, with the raw 0/160 as a secondary row. State the eligible-population composition explicitly (a small table of model_type x count would do). Also add one sentence to Method noting that the statistic is undefined or degenerate below some layer count, and give that floor.
- [MAJOR] (rigor) The laundering ladder's behavioural axis is reported without any uncertainty, and the two numbers the paper stakes its most consequential claim on are inside the noise. Every stage in results/ladder.jsonl scores n_harmful = 40 items (achieved denominators 34-40 after parse drops), so a refusal rate has a binomial SE of about 0.075 at p = 0.2. The paper reports 'the cheapest successful evasion ... an evasion cost of -0.004' (add-back-all at eps 0.10: 0.158 vs the root's 0.162) and 'int4 ... at a harmful-refusal rate of 0.135, *below* the unlaundered root's own 0.162', and calls the latter 'the single most consequential number in this paper'. Differences of 0.004 and 0.027 on a 40-item instrument are not resolvable, and the paper elsewhere (Sec. 5.4, limitation 6) correctly notes the binomial SE of ~0.08 -- so the ladder section is inconsistent with the paper's own stated instrument precision. The qualitative ordering is fine and is the real result (W05 crosses the boundary at eps 0.10 and at 4-bit while refusal is still around 0.15, versus 0.95 at eps 1.00 and 0.85 at k = 32), but the decimal framing invites an easy attack.
  Action: Add Wilson or bootstrap intervals to every harmful-refusal rate in the ladder table and figure, and restate the crossing findings as ordering statements with the interval overlap made explicit: 'at the intensity where the flag first dies, harmful refusal is statistically indistinguishable from the unlaundered root (0.158 [0.07, 0.31] vs 0.162 [0.07, 0.32])'. Drop the signed 'evasion cost' to one significant figure or replace it with the interval on the difference. Separately, note that int4's WikiText perplexity rises 26.25 -> 37.7 (+43%), so 'for free' overstates: the fluency screen is distinct-3, not perplexity, and a 43% perplexity cost is a real quality cost a deployer would notice.
- [MAJOR] (scope) The quantization result is framed as a detector failure ('a plain int4 round-trip erases the flag'), but on the paper's own scanning pipeline a 4-bit checkpoint is not a false negative -- it is unreadable. The scan reports 81 UNRESOLVED repositories whose stated causes include 'GPTQ/bitsandbytes-quantized weights', i.e. the operational outcome of the cheapest evasion is that the checkpoint falls outside the instrument's domain entirely and is never scored. That is a materially different (and, for a deployed screen, more tractable) failure mode than a clean checkpoint scoring clean, because 'unscannable' is itself an auditable signal and because dequantizing before scanning is an obvious mitigation the paper explicitly did not test (limitation 2). As written, the Introduction, Results and Conclusion all present int4 as evasion, which overstates the adversary's win and understates the paper's own remedy.
  Action: Split the quantization finding into two clearly separated claims: (a) a dequantized int4 round-trip of an abliterated model scores clean on W05 while remaining un-censored (the measured result), and (b) in the wild-scan pipeline a quantized upload is UNRESOLVED rather than clean, so at hub scale the operational effect is refusal-to-score, not a false negative. Then run the cheap follow-up you already flag: recompute W01-W05 on the int4 stage after dequantizing to fp16 and report whether the scar returns. If it does, the limitation shrinks from 'cheaply evadable' to 'requires dequantization before scoring', which is a much better sentence and is one afternoon of work on tensors you already have.
- [MINOR] (novelty) One directly relevant piece of community prior art is uncited. Abliterlitics (github.com/dreamfast/abliterlitics, with published per-model reports at abliterlitics.dev) is an open-source 'abliteration forensics' toolkit whose Weight Analysis axis performs SVD decomposition, effective-rank and energy spectra, edit-vector fingerprints, subspace alignment, low-rank reconstruction and per-layer magnitude profiles, and which publishes side-by-side comparisons of Heretic vs Huihui vs HauhauCS techniques on shared bases (Qwen3.5-9B, Qwen3.5-27B, Gemma4-e2b and others). It requires a base model plus variants in a comparison directory, so it is parent-requiring and does not threaten this paper's parent-free novelty claim -- but the paper already goes out of its way to enumerate community practice (OBLITERATUS, reverse-abliterate) and this is a closer instance of weight-spectral abliteration forensics than either. Its published technique fingerprints are also directly usable evidence for the recipe-boundary question raised in my first critique.
  Action: Cite Abliterlitics in the 'parent-free spectral inspection is already community practice' paragraph, note explicitly that it requires the parent (which sharpens rather than blunts your claim), and if any of its published cross-technique reports overlap your recipe taxonomy, cite the specific fingerprint differences between Heretic and Huihui edits as independent external support for the uniform-versus-depth-weighted distinction.
- [MINOR] (methodology) The E1 head-to-head, which is now one of the paper's best results, rests on an unstated reading of the incumbent's specification. The paper and results/arm2.json both record the 0.25L-0.75L band as 'our reading of mid-stack' because the source is not numerically specific, and this choice is never varied. Since E1's advantage over W05 on the new-uploader pairs (-0.167 [-0.444, 0.000]) is the quantity that licenses the 'complementary rather than nested' conclusion, a reader cannot tell how much of it depends on the band. The synthetic-pair result (-0.186 [-0.382, -0.079]) is the only interval excluding zero and it is driven by 26 in-house synthetics whose construction the authors control.
  Action: Report E1 at three bands (0.25-0.75L as primary, full stack, and 0.4-0.6L) and state whether the paired difference and the 'complementary failure modes' conclusion are invariant. This is pure re-analysis of deltas already computed. If the conclusion moves, say so; if not, one sentence retires the objection.
- [MINOR] (rigor) The archived-panel separation remains thin in a way the paper acknowledges but does not fully propagate. n_abliterated = 8 from 2 uploaders, the separating margin is 0.0763 log10 units between two individual checkpoints (huihui-ai/Qwen2.5-0.5B-Instruct-abliterated at -2.7415 and allenai/OLMo-1B-hf at -2.6652), and the boundary threshold used by the wild scan is that same panel-derived value. In the scan the two nearest non-abliterated neighbours (rinna/japanese-gpt-neox-small at -2.614, stabilityai/stablelm-3b-4e1t at -2.515) sit within 0.13 and 0.23 of the operating threshold, i.e. within about two margin-widths. The threshold is therefore fitted on 44 checkpoints and deployed on a population two orders of magnitude larger with no held-out calibration, and the paper does not report how the 0/160 result varies with the threshold.
  Action: Report the wild-scan hit count as a function of the threshold over a range spanning the margin (e.g. -2.4 to -3.0 in steps of 0.1) so the reader can see how brittle 0/160 is, and give the smallest threshold shift that would produce a first false positive. Add one sentence stating that the threshold is panel-fitted and never validated out of panel, which is the honest form of the specificity claim.
- [MINOR] (clarity) Several small text-to-artifact mismatches remain, and in a paper whose credibility argument is fidelity these are disproportionately costly. (a) The Panel section calls P3 '250 attempted / 160 successfully scored sub-4B Hub checkpoints'; scan.jsonl holds 270 rows of which 20 are labelled controls, and one of the 160 is a 14B model. (b) The paper says '81 were unresolvable ... 8 skipped and 1 errored' which reconciles to 250, but the experiment artifact's own summary says '65 UNRESOLVED', so one of the two is stale. (c) The Method says the positive control was injected into 'Qwen/Qwen3-0.6B -- the instruct member, whose unedited W01 is 0.6239, not the Base member's 0.6281', which is now correct, but the same paragraph then reports W01 going to 4.869 while Sec. 5.1 reports an abliterated W05 extreme of -4.82; these unrelated quantities sharing a numeral still read as a typo, as flagged last round.
  Action: Do one mechanical reconciliation pass generating the Panel and Sec. 5.2 counts from scan.jsonl rather than transcribing them, print the control/non-control split explicitly, fix the 65-vs-81 discrepancy in whichever artifact is stale, and reword so the 4.869 and -4.82 values are not adjacent.
- [MINOR] (methodology) The behavioural negative's power analysis is a real improvement, but the reported bound is stated only in terms of the paired difference and not in terms of what a practitioner would want to know. 'No interior metric beats the best black-box baseline by more than about 0.3 in |rho|' is correct but leaves open whether the interior metrics are individually useful. A19 reaches rho = +0.763 [+0.592, +0.864] at member level and +0.800 at lineage level -- comparable to B01 and better than B09 -- so the paper's own table shows that an activation observable predicts harmful-refusal rate about as well as a partial benchmark run, at a cost the paper never states in the same units (forward passes, prompts) as the black-box baseline it loses to.
  Action: Add a two-column cost annotation to the Sec. 5.4 table (prompts required, forward passes required, wall-clock) so the reader can see that the falsifier is about *marginal value over a cheaper instrument*, not about whether interior observables carry signal. Then state the practitioner-facing conclusion directly: interior observables are predictive but do not beat a 40-prompt greedy refusal rate, which is itself already the cheapest thing anyone would run.
- [MINOR] (scope) The laundering ladder generalises from a single in-house abliteration of one model (Qwen3-1.7B, one direction, one selection rule). The evasion thresholds reported as headline results -- flag dies at eps = 0.10, at merge w = 0.10, at 4-bit, at k = 4 -- are single-model, single-recipe point estimates presented as properties of the statistic. Because the paper's central scope finding is that the statistic's behaviour depends strongly on the edit's uniformity, the ladder thresholds are plausibly recipe-dependent too: a Heretic-style non-uniform root would presumably start closer to the boundary and die sooner.
  Action: Repeat the three cheapest ladder families (merge, quantization, add-back-all) on at least one second root -- ideally an in-house Heretic-style depth-weighted edit and one on a different architecture (the Llama-3.2-1B-Instruct host is already in your arm-1 code path) -- and report whether the crossing intensities move. Even a single extra root converts 'the flag dies at w = 0.10' from an anecdote into a range.
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

### [3] HUMAN-USER prompt · 2026-08-14 02:14:34 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [4] TOOL CALL — Bash · 2026-08-14 02:14:42 UTC

```
ls /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/ 2>/dev/null; ls /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/user_uploads 2>/dev/null
```

### [5] TOOL RESULT — Bash · 2026-08-14 02:14:42 UTC

```
{"stdout": "gen_art_evaluation_1\ngen_art_experiment_1\ngen_art_experiment_2\ngen_art_experiment_3\ngen_art_research_1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [6] TOOL CALL — Bash · 2026-08-14 02:14:42 UTC

```
ls -R /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_1 2>/dev/null | head -80
```

### [7] TOOL RESULT — Bash · 2026-08-14 02:14:42 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_1:\nREADME.md\narmA_select.py\nfull_method_out.json\nkernels.py\nlib_ablate.py\nlib_data.py\nlib_metrics.py\nlib_model.py\nlib_scan.py\nlib_score.py\nlogs\nmethod.py\nmethod_out.json\nmini_method_out.json\npreview_method_out.json\npyproject.toml\nresults\nvendored_lib_ablate.py\nvendored_lib_data.py\nvendored_lib_metrics.py\nvendored_lib_model.py\nvendored_lib_scan.py\nvendored_lib_score.py\nverify.py\nwstats.py\n\n/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/logs:\ndl_host.log\ninstall.log\ninstall2.log\ninstall3.log\nrun.log\ns1.log\ns1b.log\ns3.log\ns3b.log\ns4.log\nt.txt\n\n/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/results:\nanalysis.json\narm_a.jsonl\narm_a_plan.json\narm_b.jsonl\narm_b_behaviour.jsonl\ncards.json\ncost.jsonl\ndirections.json\ngate_iter4.json\ngate_iter4.jsonl\nlayer_profiles.jsonl\npip_freeze.txt\npredictions.json\npredictions.sha256\npredictions_derived.json\npredictions_derived.sha256\ns0_env.json\ns4a_host.json\nunit_tests.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [8] TOOL CALL — Bash · 2026-08-14 02:14:46 UTC

```
cd /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/results && python3 -c "
import json
a=json.load(open('analysis.json'))
def walk(o,p=''):
    if isinstance(o,dict):
        for k,v in o.items():
            if isinstance(v,(dict,list)): walk(v,p+'/'+k)
            else: print(p+'/'+k,'=',v)
walk(a)
" | head -120
```

### [9] TOOL RESULT — Bash · 2026-08-14 02:14:46 UTC

```
{"stdout": "/pools/n_positives = 67\n/pools/n_negatives = 32\n/pools/n_arm_a_edited = 44\n/pools/n_arm_b = 23\n/pools/n_uploaders = 28\n/fixed_threshold/tau = -2.7415117804288127\n/fixed_threshold/by_class/R_HERETIC/n = 7\n/fixed_threshold/by_class/R_HERETIC/detected = 0\n/fixed_threshold/by_class/R_HERETIC/uniformity = NONUNIFORM\n/fixed_threshold/by_class/R_HERETIC/sensitivity = 0.0\n/fixed_threshold/by_class/R_HERETIC/margin_min = 1.7314710533995066\n/fixed_threshold/by_class/R_HERETIC/margin_max = 2.3374008048359665\n/fixed_threshold/by_class/R_SFT_UNCENSORED/n = 5\n/fixed_threshold/by_class/R_SFT_UNCENSORED/detected = 0\n/fixed_threshold/by_class/R_SFT_UNCENSORED/uniformity = NOT_A_PROJECTION\n/fixed_threshold/by_class/R_SFT_UNCENSORED/sensitivity = 0.0\n/fixed_threshold/by_class/R_SFT_UNCENSORED/margin_min = 1.502402849627512\n/fixed_threshold/by_class/R_SFT_UNCENSORED/margin_max = 2.2302793614741416\n/fixed_threshold/by_class/R_GLOBAL_RANK1/n = 6\n/fixed_threshold/by_class/R_GLOBAL_RANK1/detected = 1\n/fixed_threshold/by_class/R_GLOBAL_RANK1/uniformity = UNIFORM\n/fixed_threshold/by_class/R_GLOBAL_RANK1/sensitivity = 0.16666666666666666\n/fixed_threshold/by_class/R_GLOBAL_RANK1/margin_min = -0.08736534227172132\n/fixed_threshold/by_class/R_GLOBAL_RANK1/margin_max = 2.0823738229516255\n/fixed_threshold/by_class/R_MULTIDIR_SVD/n = 5\n/fixed_threshold/by_class/R_MULTIDIR_SVD/detected = 0\n/fixed_threshold/by_class/R_MULTIDIR_SVD/uniformity = UNIFORM\n/fixed_threshold/by_class/R_MULTIDIR_SVD/sensitivity = 0.0\n/fixed_threshold/by_class/R_MULTIDIR_SVD/margin_min = 1.7763952888481636\n/fixed_threshold/by_class/R_MULTIDIR_SVD/margin_max = 2.1371168216939784\n/fixed_threshold/by_class/R_PARTIAL_LAYER/n = 4\n/fixed_threshold/by_class/R_PARTIAL_LAYER/detected = 0\n/fixed_threshold/by_class/R_PARTIAL_LAYER/uniformity = NONUNIFORM\n/fixed_threshold/by_class/R_PARTIAL_LAYER/sensitivity = 0.0\n/fixed_threshold/by_class/R_PARTIAL_LAYER/margin_min = 1.731546911561362\n/fixed_threshold/by_class/R_PARTIAL_LAYER/margin_max = 1.7782614698992585\n/fixed_threshold/by_class/R_NORM_PRESERVING/n = 5\n/fixed_threshold/by_class/R_NORM_PRESERVING/detected = 5\n/fixed_threshold/by_class/R_NORM_PRESERVING/uniformity = UNIFORM\n/fixed_threshold/by_class/R_NORM_PRESERVING/sensitivity = 1.0\n/fixed_threshold/by_class/R_NORM_PRESERVING/margin_min = -2.3216932514815327\n/fixed_threshold/by_class/R_NORM_PRESERVING/margin_max = -2.0759110080030694\n/fixed_threshold/by_class/R_MERGE/n = 4\n/fixed_threshold/by_class/R_MERGE/detected = 0\n/fixed_threshold/by_class/R_MERGE/uniformity = NOT_A_PROJECTION\n/fixed_threshold/by_class/R_MERGE/sensitivity = 0.0\n/fixed_threshold/by_class/R_MERGE/margin_min = 1.3036175898339626\n/fixed_threshold/by_class/R_MERGE/margin_max = 1.7568045788185125\n/fixed_threshold/by_class/R_UNKNOWN/n = 5\n/fixed_threshold/by_class/R_UNKNOWN/detected = 1\n/fixed_threshold/by_class/R_UNKNOWN/uniformity = UNKNOWN\n/fixed_threshold/by_class/R_UNKNOWN/sensitivity = 0.2\n/fixed_threshold/by_class/R_UNKNOWN/margin_min = -1.3764160428385295\n/fixed_threshold/by_class/R_UNKNOWN/margin_max = 1.601807328365872\n/fixed_threshold/by_class/R_GAUSSIAN_DEPTH/n = 3\n/fixed_threshold/by_class/R_GAUSSIAN_DEPTH/detected = 0\n/fixed_threshold/by_class/R_GAUSSIAN_DEPTH/uniformity = NONUNIFORM\n/fixed_threshold/by_class/R_GAUSSIAN_DEPTH/sensitivity = 0.0\n/fixed_threshold/by_class/R_GAUSSIAN_DEPTH/margin_min = 1.7778597231769973\n/fixed_threshold/by_class/R_GAUSSIAN_DEPTH/margin_max = 1.9386084648842385\n/fixed_threshold/by_class/ARMB_UNIFORM_SUBUNIT__UNIFORM_BUT_INCOMPLETE/n = 3\n/fixed_threshold/by_class/ARMB_UNIFORM_SUBUNIT__UNIFORM_BUT_INCOMPLETE/detected = 0\n/fixed_threshold/by_class/ARMB_UNIFORM_SUBUNIT__UNIFORM_BUT_INCOMPLETE/uniformity = UNIFORM_BUT_INCOMPLETE\n/fixed_threshold/by_class/ARMB_UNIFORM_SUBUNIT__UNIFORM_BUT_INCOMPLETE/sensitivity = 0.0\n/fixed_threshold/by_class/ARMB_UNIFORM_SUBUNIT__UNIFORM_BUT_INCOMPLETE/margin_min = 0.992756784950761\n/fixed_threshold/by_class/ARMB_UNIFORM_SUBUNIT__UNIFORM_BUT_INCOMPLETE/margin_max = 1.7389737079385463\n/fixed_threshold/by_class/ARMB_UNIFORM_SUBUNIT__UNIFORM/n = 1\n/fixed_threshold/by_class/ARMB_UNIFORM_SUBUNIT__UNIFORM/detected = 1\n/fixed_threshold/by_class/ARMB_UNIFORM_SUBUNIT__UNIFORM/uniformity = UNIFORM\n/fixed_threshold/by_class/ARMB_UNIFORM_SUBUNIT__UNIFORM/sensitivity = 1.0\n/fixed_threshold/by_class/ARMB_UNIFORM_SUBUNIT__UNIFORM/margin_min = -1.8501767559741862\n/fixed_threshold/by_class/ARMB_UNIFORM_SUBUNIT__UNIFORM/margin_max = -1.8501767559741862\n/fixed_threshold/by_class/ARMB_GAUSSIAN_DEPTH__NONUNIFORM/n = 7\n/fixed_threshold/by_class/ARMB_GAUSSIAN_DEPTH__NONUNIFORM/detected = 2\n/fixed_threshold/by_class/ARMB_GAUSSIAN_DEPTH__NONUNIFORM/uniformity = NONUNIFORM\n/fixed_threshold/by_class/ARMB_GAUSSIAN_DEPTH__NONUNIFORM/sensitivity = 0.2857142857142857\n/fixed_threshold/by_class/ARMB_GAUSSIAN_DEPTH__NONUNIFORM/margin_min = -1.1667813172962513\n/fixed_threshold/by_class/ARMB_GAUSSIAN_DEPTH__NONUNIFORM/margin_max = 1.731751209065923\n/fixed_threshold/by_class/ARMB_GAUSSIAN_DEPTH__DEPTH_WEIGHTED_ABOVE_W_STAR/n = 2\n/fixed_threshold/by_class/ARMB_GAUSSIAN_DEPTH__DEPTH_WEIGHTED_ABOVE_W_STAR/detected = 2\n/fixed_threshold/by_class/ARMB_GAUSSIAN_DEPTH__DEPTH_WEIGHTED_ABOVE_W_STAR/uniformity = DEPTH_WEIGHTED_ABOVE_W_STAR\n/fixed_threshold/by_class/ARMB_GAUSSIAN_DEPTH__DEPTH_WEIGHTED_ABOVE_W_STAR/sensitivity = 1.0\n/fixed_threshold/by_class/ARMB_GAUSSIAN_DEPTH__DEPTH_WEIGHTED_ABOVE_W_STAR/margin_min = -1.8501767559741862\n/fixed_threshold/by_class/ARMB_GAUSSIAN_DEPTH__DEPTH_WEIGHTED_ABOVE_W_STAR/margin_max = -1.7313908816666728\n/fixed_threshold/by_class/ARMB_LAYER_BAND__NONUNIFORM/n = 1\n/fixed_threshold/by_class/ARMB_LAYER_BAND__NONUNIFORM/detected = 0\n/fixed_threshold/by_class/ARMB_LAYER_BAND__NONUNIFORM/uniformity = NONUNIFORM\n/fixed_threshold/by_class/ARMB_LAYER_BAND__NONUNIFORM/sensitivity = 0.0\n/fixed_threshold/by_class/ARMB_LAYER_BAND__NONUNIFORM/margin_min = 1.7316203399713828\n/fixed_threshold/by_class/ARMB_LAYER_BAND__NONUNIFORM/margin_max = 1.7316203399713828\n/fixed_threshold/by_class/ARMB_HOUSEHOLDER__UNIFORM_BUT_ORTHOGONAL/n = 3\n/fixed_threshold/by_class/ARMB_HOUSEHOLDER__UNIFORM_BUT_ORTHOGONAL/detected = 1\n/fixed_threshold/by_class/ARMB_HOUSEHOLDER__UNIFORM_BUT_ORTHOGONAL/uniformity = UNIFORM_BUT_ORTHOGONAL\n/fixed_threshold/by_class/ARMB_HOUSEHOLDER__UNIFORM_BUT_ORTHOGONAL/sensitivity = 0.3333333333333333\n/fixed_threshold/by_class/ARMB_HOUSEHOLDER__UNIFORM_BUT_ORTHOGONAL/margin_min = -2.880254383946973\n/fixed_threshold/by_class/ARMB_HOUSEHOLDER__UNIFORM_BUT_ORTHOGONAL/margin_max = 1.8581631893964357\n/fixed_threshold/by_class/ARMB_NORM_PRESERVING__UNIFORM/n = 1\n/fixed_threshold/by_class/ARMB_NORM_PRESERVING__UNIFORM/detected = 1\n/fixed_threshold/by_class/ARMB_NORM_PRESERVING__UNIFORM/uniformity = UNIFORM\n/fixed_threshold/by_class/ARMB_NORM_PRESERVING__UNIFORM/sensitivity = 1.0\n/fixed_threshold/by_class/ARMB_NORM_PRESERVING__UNIFORM/margin_min = -1.9878735151957083\n/fixed_threshold/by_class/ARMB_NORM_PRESERVING__UNIFORM/margin_max = -1.9878735151957083\n/fixed_threshold/by_class/ARMB_RANK_K__UNIFORM/n = 3\n/fixed_threshold/by_class/ARMB_RANK_K__UNIFORM/detected = 3\n/fixed_threshold/by_class/ARMB_RANK_K__UNIFORM/uniformity = UNIFORM\n/fixed_threshold/by_class/ARMB_RANK_K__UNIFORM/sensitivity = 1.0\n/fixed_threshold/by_class/ARMB_RANK_K__UNIFORM/margin_min = -2.8884917732276354\n/fixed_threshold/by_class/ARMB_RANK_K__UNIFORM/margin_max = -2.7297845851114313\n/fixed_threshold/by_class/ARMB_HERETIC__NONUNIFORM/n = 1\n/fixed_threshold/by_class/ARMB_HERETIC__NONUNIFORM/detected = 0\n/fixed_threshold/by_class/ARMB_HERETIC__NONUNIFORM/uniformity = NONUNIFORM\n/fixed_threshold/by_class/ARMB_HERETIC__NONUNIFORM/sensitivity = 0.0\n/fixed_threshold/by_class/ARMB_HERETIC__NONUNIFORM/margin_min = 1.0259114560520861\n/fixed_threshold/by_class/ARMB_HERETIC__NONUNIFORM/margin_max = 1.0259114560520861\n/fixed_threshold/by_class/ARMB_HERETIC__UNIFORM/n = 1\n/fixed_threshold/by_class/ARMB_HERETIC__UNIFORM/detected = 1\n/fixed_threshold/by_class/ARMB_HERETIC__UNIFORM/uniformity = UNIFORM\n/fixed_threshold/by_class/ARMB_HERETIC__UNIFORM/sensitivity = 1.0\n/fixed_threshold/by_class/ARMB_HERETIC__UNIFORM/margin_min = -1.8709029133408674\n/fixed_threshold/by_class/ARMB_HERETIC__UNIFORM/margin_max = -1.8709029133408674\nTraceback (most recent call last):\n  File \"<string>\", line 9, in <module>\n  File \"<string>\", line 7, in walk\n  File \"<string>\", line 8, in walk\nBrokenPipeError: [Errno 32] Broken pipe", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/review_paper/review_paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-08-14 02:15:00 UTC

```
cd /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/results && python3 -c "
import json
a=json.load(open('analysis.json'))
print(list(a.keys()))
for k in ['baseline_repo_name','two_condition','rule','arm_b_rule','baselines']:
    if k in a: print(k, json.dumps(a[k])[:2000])
"
```

### [11] TOOL RESULT — Bash · 2026-08-14 02:15:00 UTC

```
{"stdout": "['excluded_from_pool', 'parents_that_are_themselves_edited', 'pools', 'fixed_threshold', 'at_scale_sensitivity', 'repo_name_regex_baseline', 'lorco', 'louo', 'uniformity_scatter', 'gaussian_sweep', 'subunit_closed_form', 'e1_crosscheck', 'precision_control', 'mechanism_decomposition', 'effectiveness_vs_detectability', 'prediction_verdicts']", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/review_paper/review_paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Bash · 2026-08-14 02:15:04 UTC

```
cd /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/results && python3 -c "
import json
a=json.load(open('analysis.json'))
print(json.dumps(a['repo_name_regex_baseline'])[:1500])
print('---MECH---')
print(json.dumps(a['mechanism_decomposition'])[:3000])
print('---LORCO---')
print(json.dumps(a['lorco'])[:1500])
"
```

### [13] TOOL RESULT — Bash · 2026-08-14 02:15:04 UTC

```
{"stdout": "{\"regex_terms\": [\"abliterat\", \"uncensor\", \"decensor\", \"heretic\", \"obliterat\", \"amoral\", \"unalign\", \"nsfw\", \"gabliterat\", \"jailbr\", \"dolphin\"], \"scored_on\": \"the Arm A rows only (Arm B kernels have no Hub name)\", \"n_positives\": 44, \"n_negatives\": 20, \"sensitivity\": 0.7272727272727273, \"specificity\": 1.0, \"false_positives\": [], \"W05_sensitivity_same_rows\": 0.1590909090909091, \"W05_specificity_same_rows\": 1.0, \"agreement_with_W05\": 0.609375, \"caught_by_name_missed_by_W05\": [\"MihaiPopa-1/Stentor-30M-Instruct-heretic-safety-defiltered\", \"teja944/SmolLM2-135M-Instruct-heretic\", \"0utsideness/SmolLM2-135M-Instruct-heretic-refusal-plugins-test\", \"0utsideness/SmolLM2-135M-Instruct-heretic-main-test\", \"WithinUsAI/Gemma3-Prompt.Coder.it.Uncensored-270m\", \"SkGufranAhmed/Huihui-gemma-3-270m-it-abliterated\", \"huihui-ai/Huihui-gemma-3-270m-it-abliterated\", \"wetr3d/Huihui-gemma-3-270m-it-abliterated\", \"p-e-w/gemma-3-270m-it-heretic\", \"pixasocial/survival-uncensored-gemma-270m-v2\", \"huihui-ai/Qwen2.5-0.5B-Instruct-abliterated-SFT\", \"Goekdeniz-Guelmez/Josiefied-Qwen3-0.6B-gabliterated-v1\", \"Goekdeniz-Guelmez/Josiefied-Qwen3-0.6B-abliterated-v2\", \"lunahr/Qwen3-0.6B-abliterated\", \"Goekdeniz-Guelmez/Qwen3-0.6B-gabliterated-Dev\", \"Goekdeniz-Guelmez/Qwen3-0.6B-gabliterated\", \"d0gra/uncensored-stage1-hacker\", \"mlabonne/Qwen3-0.6B-abliterated\", \"MC7ever/MiniCPM5-1B-Agent-abliterated-disinhibited\", \"MagicalAlchemist/Qwen3-1.7B-Magic_decensored\", \"dalatexcoder/Qwen3.5-2B-heretic-Claude-Sonnet-4.6-Distil\n---MECH---\n{\"rule\": \"detected  <=>  |cos(v1, r)| > 0.9  AND  log10 min_m e_r,m <= tau\", \"status\": \"POST-HOC explanation, not a stamped prediction\", \"n\": 24, \"n_applicable\": 19, \"agreement\": 1.0, \"disagreements\": [], \"excluded_because_the_removed_direction_is_not_r\": [\"rank_k2\", \"rank_k4\", \"rank_k8\", \"heretic_percomponent\", \"heretic_percomponent_uniformweight\"], \"rows\": [{\"kernel_id\": \"uniform_w0.5\", \"family\": \"uniform_subunit\", \"abscos_v1_r\": 0.10958785563707352, \"log10_min_e_r\": -0.6807143634683637, \"W05\": -1.0025380724902664, \"detected\": false, \"discovery\": false, \"completion\": false, \"rule_applicable\": true, \"rule_predicts\": false, \"rule_agrees\": true}, {\"kernel_id\": \"uniform_w0.7\", \"family\": \"uniform_subunit\", \"abscos_v1_r\": 0.9951154589653015, \"log10_min_e_r\": -1.124465048835386, \"W05\": -1.153526358342526, \"detected\": false, \"discovery\": true, \"completion\": false, \"rule_applicable\": true, \"rule_predicts\": false, \"rule_agrees\": true}, {\"kernel_id\": \"uniform_w0.85\", \"family\": \"uniform_subunit\", \"abscos_v1_r\": 0.9990087151527405, \"log10_min_e_r\": -1.7248446970111522, \"W05\": -1.7487549954780517, \"detected\": false, \"discovery\": true, \"completion\": false, \"rule_applicable\": true, \"rule_predicts\": false, \"rule_agrees\": true}, {\"kernel_id\": \"uniform_w1.0\", \"family\": \"uniform_subunit\", \"abscos_v1_r\": 0.9999998807907104, \"log10_min_e_r\": -4.582796061133184, \"W05\": -4.591688536402999, \"detected\": true, \"discovery\": true, \"completion\": true, \"rule_applicable\": true, \"rule_predicts\": true, \"rule_agrees\": true}, {\"kernel_id\": \"gaussian_s0.5\", \"family\": \"gaussian_depth\", \"abscos_v1_r\": 0.010602283291518688, \"log10_min_e_r\": -4.526476983600931, \"W05\": -1.009860192456488, \"detected\": false, \"discovery\": false, \"completion\": true, \"rule_applicable\": true, \"rule_predicts\": false, \"rule_agrees\": true}, {\"kernel_id\": \"gaussian_s1\", \"family\": \"gaussian_depth\", \"abscos_v1_r\": 0.011083577759563923, \"log10_min_e_r\": -4.526476983600931, \"W05\": -1.0098238827203088, \"detected\": false, \"discovery\": false, \"completion\": true, \"rule_applicable\": true, \"rule_predicts\": false, \"rule_agrees\": true}, {\"kernel_id\": \"gaussian_s2\", \"family\": \"gaussian_depth\", \"abscos_v1_r\": 0.011938730254769325, \"log10_min_e_r\": -4.526476983600931, \"W05\": -1.0097605713628897, \"detected\": false, \"discovery\": false, \"completion\": true, \"rule_applicable\": true, \"rule_predicts\": false, \"rule_agrees\": true}, {\"kernel_id\": \"gaussian_s4\", \"family\": \"gaussian_depth\", \"abscos_v1_r\": 0.01564563252031803, \"log10_min_e_r\": -4.526476983600931, \"W05\": -1.0098637673257507, \"detected\": false, \"discovery\": false, \"completion\": true, \"rule_applicable\": true, \"rule_predicts\": false, \"rule_agrees\": true}, {\"kernel_id\": \"gaussian_s8\", \"family\": \"gaussian_depth\", \"abscos_v1_r\": 0.1264457404613495, \"log10_min_e_r\": -4.526476983600931, \"W05\": -1.0134484395307624, \"detected\": false, \"discovery\": false, \"completion\": true, \"rule_applicable\": true, \"rule_predicts\": false, \"rule_agrees\": true}, {\"kernel_id\": \"gaussian_s16\", \"family\":\n---LORCO---\n{\"ARMB_GAUSSIAN_DEPTH__DEPTH_WEIGHTED_ABOVE_W_STAR\": {\"n_held_out\": 2, \"n_fit_positives\": 65, \"tau_fitted_without_this_class\": -1.7156003243767266, \"heldout_sensitivity\": 1.0, \"specificity_on_negatives\": 1.0, \"auroc_raw\": 0.0, \"auroc_oriented\": 1.0, \"auroc_orientation\": \"lower-is-positive\", \"uniformity\": \"DEPTH_WEIGHTED_ABOVE_W_STAR\", \"predicted_sensitivity\": null}, \"ARMB_GAUSSIAN_DEPTH__NONUNIFORM\": {\"n_held_out\": 7, \"n_fit_positives\": 60, \"tau_fitted_without_this_class\": -1.7156003243767266, \"heldout_sensitivity\": 0.2857142857142857, \"specificity_on_negatives\": 1.0, \"auroc_raw\": 0.41964285714285715, \"auroc_oriented\": 0.5803571428571428, \"auroc_orientation\": \"lower-is-positive\", \"uniformity\": \"NONUNIFORM\", \"predicted_sensitivity\": 0.0}, \"ARMB_HERETIC__NONUNIFORM\": {\"n_held_out\": 1, \"n_fit_positives\": 66, \"tau_fitted_without_this_class\": -1.7487549954780517, \"heldout_sensitivity\": 0.0, \"specificity_on_negatives\": 1.0, \"auroc_raw\": 0.0, \"auroc_oriented\": 1.0, \"auroc_orientation\": \"lower-is-positive\", \"uniformity\": \"NONUNIFORM\", \"predicted_sensitivity\": 0.0}, \"ARMB_HERETIC__UNIFORM\": {\"n_held_out\": 1, \"n_fit_positives\": 66, \"tau_fitted_without_this_class\": -1.7156003243767266, \"heldout_sensitivity\": 1.0, \"specificity_on_negatives\": 1.0, \"auroc_raw\": 0.0, \"auroc_oriented\": 1.0, \"auroc_orientation\": \"lower-is-positive\", \"uniformity\": \"UNIFORM\", \"predicted_sensitivity\": 1.0}, \"ARMB_HOUSEHOLDER__UNIFORM_BUT_ORTHOGONAL\": {\"n_held_out\": 3, \"n_fit_positives\": 64, \"tau_fitted_without_t", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/review_paper/review_paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-08-14 02:15:14 UTC

```
cd /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/results && python3 -c "
import json
a=json.load(open('analysis.json'))
for k,v in a['lorco'].items():
    if k.startswith('R_'): print(k, v.get('n_held_out'), 'sens',round(v.get('heldout_sensitivity',-1),3),'auroc_or',round(v.get('auroc_oriented',-1),3),'tau',round(v.get('tau_fitted_without_this_class',0),4))
print('--- at_scale ---'); print(json.dumps(a['at_scale_sensitivity'])[:800])
print('--- eff vs det ---'); print(json.dumps(a['effectiveness_vs_detectability'])[:900])
"
```

### [15] TOOL RESULT — Bash · 2026-08-14 02:15:14 UTC

```
{"stdout": "R_GAUSSIAN_DEPTH 3 sens 0.0 auroc_or 0.885 tau -1.7156\nR_GLOBAL_RANK1 6 sens 0.333 auroc_or 0.62 tau -1.7156\nR_HERETIC 7 sens 0.0 auroc_or 0.772 tau -1.7156\nR_MERGE 4 sens 0.0 auroc_or 0.516 tau -1.7156\nR_MULTIDIR_SVD 5 sens 0.0 auroc_or 0.844 tau -1.7156\nR_NORM_PRESERVING 5 sens 1.0 auroc_or 1.0 tau -1.7156\nR_PARTIAL_LAYER 4 sens 0.0 auroc_or 0.664 tau -1.7156\nR_SFT_UNCENSORED 5 sens 0.0 auroc_or 0.819 tau -1.7156\nR_UNKNOWN 5 sens 0.4 auroc_or 0.806 tau -1.7156\n--- at_scale ---\n{\"archived_panel_members_remeasured\": {\"n\": 5, \"rows\": [{\"repo_id\": \"huihui-ai/Qwen2.5-0.5B-Instruct-abliterated\", \"W05\": -2.7415117804288127, \"detected\": true, \"margin\": 0.0}, {\"repo_id\": \"huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2\", \"W05\": -4.820393556832292, \"detected\": true, \"margin\": -2.0788817764034797}, {\"repo_id\": \"huihui-ai/Llama-3.2-1B-Instruct-abliterated\", \"W05\": -4.251323528147573, \"detected\": true, \"margin\": -1.5098117477187603}, {\"repo_id\": \"huihui-ai/Qwen2.5-1.5B-Instruct-abliterated\", \"W05\": -4.682934279772425, \"detected\": true, \"margin\": -1.9414224993436124}, {\"repo_id\": \"huihui-ai/Huihui-Qwen3-1.7B-abliterated-v2\", \"W05\": -4.552337488690126, \"detected\": true, \"margin\": -1.8108257082613135}], \"sensitivity\": 1.0, \"note\": \"these are iteration-2/3 panel positives, re-measure\n--- eff vs det ---\n{\"parent_refusal_rate_judge\": 0.925, \"parent_refusal_wilson\": [0.8013546984090248, 0.9741644432281419], \"effectiveness_criterion\": \"fluency-passing AND greedy harmful-refusal rate <= 0.50 on the frozen 40-item core\", \"rows\": [{\"kernel_id\": \"uniform_w1.0\", \"family\": \"uniform_subunit\", \"refusal_rate_judge\": 0.2, \"refusal_wilson_judge\": [0.10499864973166874, 0.34757607381856676], \"refusal_rate_screen\": 0.0, \"refusal_drop_vs_parent\": 0.7250000000000001, \"wikitext_ppl\": 25.191757552829817, \"ppl_ratio\": 0.9808735720070997, \"distinct3\": 0.9955180533751962, \"fluency_pass\": true, \"W05\": -4.591688536402999, \"detected\": true, \"abscos_v1_r\": 0.9999998807907104}, {\"kernel_id\": \"uniform_w0.85\", \"family\": \"uniform_subunit\", \"refusal_rate_judge\": 0.225, \"refusal_wilson_judge\": [0.1231595325467853, 0.3750339640409305], \"refusal_rate_screen\": 0.0, \"refusal_drop_vs_parent\": 0.7000000000000001, \"wikitext_pp", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/review_paper/review_paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-08-14 02:15:26 UTC

```
cd /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_2 && ls results 2>/dev/null && python3 -c "
import json,glob
for f in glob.glob('results/*.json'):
    try:
        d=json.load(open(f))
    except: continue
    print('==',f, list(d.keys())[:15] if isinstance(d,dict) else type(d))
"
```

### [17] TOOL RESULT — Bash · 2026-08-14 02:15:28 UTC

```
{"stdout": "archive_schema.json\narm1_analysis.json\narm1_frontier.jsonl\narm2_archive_counts.json\narm2_archive_eligibility.jsonl\narm2_new_candidates.json\narm2_rates.json\narm2_scan_new.jsonl\narm3.json\narm3_threshold_curve.jsonl\nassertions.json\neligibility_stamp.json\ngate_arithmetic.json\ngate_arithmetic.jsonl\ngate_numerics.json\nnumbers.json\npredictions.json\npredictions_outcome.json\nrepro_gate.json\n== results/assertions.json ['n_checks', 'n_failed', 'checks']\n== results/numbers.json ['gate_arithmetic_max_abs_delta_W05', 'gate_kL_identity_max_abs_delta_synthetic', 'gate_4of12_W02', 'gate_4of12_cos_v1_to_injected', 'kL_reproduces_W05_on_real_models_max_abs_delta', 'fp_rate_filtered_primary', 'n_eligible_denominator', 'n_false_positives_filtered', 'n_archived_eligible', 'n_new_eligible_completed', 'fp_rate_raw_unfiltered_secondary', 'n_excluded_archive_UNDECIDABLE:E3b', 'n_excluded_archive_E1', 'n_excluded_archive_E2', 'n_excluded_archive_E6']\n== results/predictions_outcome.json ['P1', 'P2', 'P3', 'P4', 'P5']\n== results/arm3.json ['thresholds', 'operating_point', 'threshold_provenance', 'panel_margin_log10', 'first_false_positive_filtered', 'first_false_positive_archived_eligible', 'first_false_positive_new_eligible', 'first_false_positive_unfiltered', 'nearest_eligible_undeclared_below_boundary', 'nearest_non_abliterated_panel_neighbours_recomputed', 'archive_cross_check']\n== results/arm2_rates.json ['primary', 'secondary_raw_unfiltered', 'exclusions_archive_by_primary_reason', 'exclusions_new_by_primary_reason', 'n_excluded_archive', 'unresolved_archive', 'unresolved_new', 'model_type_composition_archive_eligible', 'model_type_composition_new', 'model_type_composition_archive_all_scored', 'eligibility_stamp']\n== results/arm1_analysis.json ['n_G1', 'n_G2_G3_synth', 'n_G4_real', 'n_new_undeclared_scored', 'kL_reproduces_W05', 'panel_auroc', 'panel_note', 'w05w_panel_fitted_thresholds', 'catch_by_recipe_class', 'leave_one_recipe_class_out', 'benign_controls', 'frontier']\n== results/arm2_new_candidates.json ['n_candidates_prefiltered', 'n_config_checked', 'n_eligible', 'n_excluded', 'excluded_sample']\n== results/arm2_archive_counts.json ['total_rows', 'n_controls', 'n_non_control', 'status_all', 'status_non_control', 'n_scored_non_control', 'n_unresolved_non_control', 'n_skipped_non_control', 'n_error_non_control', 'control_classes', 'unresolved_by_cause', 'n_in_abliterated_region_0of160', 'stale_claim_check', 'denominator_0of160_reproduces']\n== results/eligibility_stamp.json ['sha256_eligibility_py', 'stamped_at_utc', 'n_bytes', 'rule', 'unchanged_since_stamp']\n== results/predictions.json ['P1', 'P2', 'P3', 'P4', 'P5', 'stated_at_utc', 'stated_before']\n== results/repro_gate.json ['archive_schema_ok', 'arithmetic', 'numerics', 'seconds']\n== results/gate_numerics.json ['kL_equals_W05', 'full_injection', 'four_of_twelve_injection', 'clean_reference', 'rank_check', 'naive_double_loop_gram_max_abs_delta', 'PASS']\n== results/gate_arithmetic.json ['n', 'max_abs_delta_W05', 'mean_abs_delta_W05', 'by_source', 'primary_source', 'tolerance', 'max_abs_delta_W05_scan', 'PASS', 'note', 'ladder_root_caveat', 'n_by_source']\n== results/archive_schema.json ['A/wstats.py', 'A/results/arm1_real.jsonl', 'A/results/arm1_synth.jsonl', 'A/results/arm2.json', 'A/results/long_table_depth.jsonl', 'A/results/gate.jsonl', 'B/results/root_recipe.json', 'B/results/root.json', 'B/results/ladder.jsonl', 'B/results/scan.jsonl', 'B/results/scan_enumeration.json', 'DEP/full_data_out.json', 'DEP/research_out.json']", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/review_paper/review_paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] TOOL CALL — Bash · 2026-08-14 02:15:32 UTC

```
cd /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_2 && python3 -c "
import json
d=json.load(open('results/arm1_analysis.json'))
for k in d:
    print('==',k)
    print(json.dumps(d[k])[:900])
"
```

### [19] TOOL RESULT — Bash · 2026-08-14 02:15:32 UTC

```
{"stdout": "== n_G1\n0\n== n_G2_G3_synth\n0\n== n_G4_real\n0\n== n_new_undeclared_scored\n40\n== kL_reproduces_W05\n{\"n\": 40, \"max_abs_delta\": 8.491610326011312e-08, \"tolerance\": 1e-09, \"PASS\": false}\n== panel_auroc\n{}\n== panel_note\n\"G1 is the 20 control checkpoints the archived scan carries (8 abliterated, 12 clean), NOT the full iteration-2 44-member panel, whose per-member W05 values are not stored in any archive file reachable from this workspace.\"\n== w05w_panel_fitted_thresholds\n{\"values\": {}, \"definition\": \"the MAXIMUM W05w over the 8 abliterated control checkpoints -- exactly the construction that produced the pooled operating point -2.7415117804288127 (the weakest positive defines the boundary). Panel-fitted, never validated out of panel, and CIRCULAR for sensitivity measured on those same 8 members.\", \"panel_separation\": {}, \"pooled_reference\": {\"boundary\": -2.7415117804288127, \"nonabliterated_max\": -2.665194698505143, \"margin_log10\": 0.0763170819236696}}\n== catch_by_recipe_class\n{\"W05\": {}, \"W05q10\": {}, \"W05w_2\": {}, \"W05w_4\": {}, \"W05w_6\": {}, \"W05w_8\": {}, \"W05w_L\": {}}\n== leave_one_recipe_class_out\n{\"design\": \"PRIMARY generalisation control: each recipe class is scored by a threshold that never saw it (the shared pooled operating point is fitted on R1-class huihui checkpoints only; the panel-fitted W05w thresholds are fitted on CLEAN models only, so no edit class is in either fit).\", \"secondary\": \"leave-one-uploader-out (uploader is a weaker grouping than recipe)\"}\n== benign_controls\n{\"W05\": {\"n\": 0, \"n_flagged_shared_thr\": 0, \"values\": {}}, \"W05q10\": {\"n\": 0, \"n_flagged_shared_thr\": 0, \"values\": {}}, \"W05w_2\": {\"n\": 0, \"n_flagged_shared_thr\": 0, \"values\": {}}, \"W05w_4\": {\"n\": 0, \"n_flagged_shared_thr\": 0, \"values\": {}}, \"W05w_6\": {\"n\": 0, \"n_flagged_shared_thr\": 0, \"values\": {}}, \"W05w_8\": {\"n\": 0, \"n_flagged_shared_thr\": 0, \"values\": {}}, \"W05w_L\": {\"n\": 0, \"n_flagged_shared_thr\": 0, \"values\": {}}}\n== frontier\n[{\"k\": \"2\", \"tau\": 0.0, \"n_windows_per_model_mean\": 11, \"threshold_used\": -2.7415117804288127, \"sensitivity_on_G1pos_plus_G2\": NaN, \"n_positives\": 0, \"sensitivity_G2_out_of_fit\": NaN, \"n_positives_G2_out_of_fit\": 0, \"sensitivity_G1_IN_FIT_circular\": NaN, \"n_positives_G1_in_fit\": 0, \"specificity_on_eligible_undeclared\": 1.0, \"n_eligible_undeclared\": 40, \"n_false_positives\": 0, \"first_FP_repo_id\": null}, {\"k\": \"2\", \"tau\": 0.5, \"n_windows_per_model_mean\": 11, \"threshold_used\": -2.7415117804288127, \"sensitivity_on_G1pos_plus_G2\": NaN, \"n_positives\": 0, \"sensitivity_G2_out_of_fit\": NaN, \"n_positives_G2_out_of_fit\": 0, \"sensitivity_G1_IN_FIT_circular\": NaN, \"n_positives_G1_in_fit\": 0, \"specificity_on_eligible_undeclared\": 1.0, \"n_eligible_undeclared\": 40, \"n_false_positives\": 0, \"first_FP_repo_id\": null}, {\"k\": \"2\", \"tau\": 0.8, \"n_windows_per_model_mean\": 11, \"threshold_used\": -2.7415117804288", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/review_paper/review_paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] TOOL CALL — Bash · 2026-08-14 02:16:06 UTC

```
cd /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_experiment_1/results && python3 -c "
import json
rows=[json.loads(l) for l in open('arm_a.jsonl')]
print(len(rows), list(rows[0].keys())[:30])
import collections
print(collections.Counter(r.get('role') or r.get('class') or '?' for r in rows))
" 2>&1 | head -20
```

### [21] TOOL RESULT — Bash · 2026-08-14 02:16:06 UTC

```
{"stdout": "78 ['repo_id', 'revision', 'uploader', 'param_count', 'model_type', 'declared_parent', 'evidence_url', 'safetensors_bytes', 'is_iter2_class_member', 'role', 'recipe_class_rederived', 'kernel_uniformity', 'rederive_pattern', 'rederive_match', 'rederive_context', 'rederive_justification', 'manifest_class', 'agrees_with_manifest', 'rederive_source', 'selection_reason', 'parent_status', 'recipe_evidence_span', 'status', 'error', 'on_disk_safetensors_bytes', 'implied_params_bf16', 'eligible', 'ineligible_reason', 'W01_abl_suppression_depth', 'W02_abl_direction_consistency']\nCounter({'edited': 51, 'parent': 23, 'parent_also_edited': 4})", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/review_paper/review_paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [22] TOOL CALL — Write · 2026-08-14 02:18:18 UTC

```
File: /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/review_paper/review_paper/.terminal_claude_agent_struct_out.json

{
  "overall_assessment": "This is an unusually honest, unusually well-instrumented paper that has responded to essentially every critique from the previous round with real experiments rather than caveats. The at-scale falsification (sensitivity 0.159 on 44 real edited checkpoints against 0.727 for a repository-name regex), the pre-stamped eligibility rule, the recovered ladder denominators, the both-directions decoupling built as checkpoints, and the 110-assertion self-audit are all genuine and verifiable in the artifacts. I checked the headline numbers against results/analysis.json, results/arm1_analysis.json and results/arm2_rates.json and they reproduce, including the uncomfortable ones the paper reports against itself.\n\nThe problem is what remains as a positive contribution. The paper explicitly retires its metric, so everything now rests on (a) the two-condition mechanism and (b) the windowed generalisation. (a) is, on the paper's own definitions, very close to an algebraic identity rather than an empirical finding: when |cos(v1,r)|->1 the statistic W05 = log10 min_W e_W(v1) is numerically almost equal to the completion quantity log10 min_W e_W(r) (the artifact rows show -1.153 vs -1.124, -1.749 vs -1.725, -4.592 vs -4.583), and when discovery fails W05 collapses to the parent's value. So 'detected <=> discovery AND completion' is close to a two-line consequence of the definitions, and the 19/19 agreement is a consistency check on an approximation, not evidence. Worse, the five kernels excluded as 'inapplicable' are exactly the rank-k and Heretic families that dominate the real Hub failure. (b) has no positive evaluation at all: arm1_analysis.json records n_G1 = 0, n_G2_G3_synth = 0, n_G4_real = 0, so W05w was scored on zero edited models, and the paper is admirably explicit about this. That leaves the paper as a very well-documented negative result plus a mechanistic re-description plus an unevaluated proposal.\n\nI also found one reporting inconsistency that matters: the §5.1 table is headed 'held-out recipe class' but its sensitivity column is taken from the fixed panel threshold while its AUROC column comes from the leave-one-recipe-class-out refit, and those two regimes disagree (global rank-one is 0.167 at fixed tau but 0.333 under LORCO; unknown is 0.200 vs 0.400). The refitted tau is -1.7156 rather than -2.7415 — a one-log-unit shift — which is a stronger statement about threshold instability than §5.4's 0.128-log-unit brittleness result, and it is currently invisible to the reader. And the regex baseline the whole paper is benchmarked against is estimated on a panel drawn from a census built out of 20 abliteration-related search terms, which is close to circular in the regex's favour.\n\nFixing the identity framing, the table regime mix, the baseline circularity, and running the W05w positive arm (which is re-analysis of checkpoints that already exist in Arm B) would move this from a careful negative result to a paper with a defensible positive claim. As it stands I read it as borderline: the measurement discipline is above the bar for a top venue, the contribution is not yet.",
  "strengths": [
    "Every critique from the previous round was addressed with a run rather than a hedge: name-blind panel selection, pre-stamped sha256 eligibility rule with a published composition table, recovered ladder denominators (31-40, not the recorded 40) with Wilson intervals, three roots on two architectures, an E1 band-sensitivity sweep, a cost-annotated behavioural table, and a threshold-brittleness curve.",
    "The paper reports against its own interest at almost every opportunity: it retracts the uniformity story, retracts 'parent-free costs nothing', retires four decimal-level ladder claims, corrects its own judge-agreement figure from 0.952 to 0.822, and shows that the parent-requiring incumbent E1 has roughly twice its coverage. This is rare and valuable.",
    "The both-directions decoupling is demonstrated by construction with the confound controlled (root B holds the refusal direction fixed at root A's so the kernel is the only manipulated variable). A false negative that un-censors 0.950 -> 0.270 while reading its parent's W05 to four decimals, and a false positive at -4.587 that never un-censored, together settle what a weights-only statistic can mean far more convincingly than any correlation would.",
    "The at-scale evaluation with an operational baseline is exactly the right test and is rarely done: a weights-only detector that flags a strict subset of what a filename already flags (caught_by_W05_missed_by_name is empty) is a decisive, honest result, and I verified it in results/analysis.json.",
    "The 110-assertion self-audit with declared tolerances, byte-identical reruns, and five reported MISMATCHes — including one where the paper's own quoted subset label was wrong — is a reproducibility standard well above the field norm.",
    "The bf16-versus-float32 storage finding (-4.59 vs -12.71 for the same edit) and the 5-bit rather than 4-bit death of the scar are useful, transferable measurement facts for anyone else working on weight-space forensics.",
    "The prior-art work is thorough and read from primary sources: Heretic's kernel corrected from Gaussian to a triangular tent with a hard cutoff, OBLITERATUS's 'spectral certification' correctly identified as activation-consuming, Abliterlitics correctly positioned as parent-requiring and simultaneously used as independent external evidence for the paper's own mechanism."
  ],
  "dimension_scores": [
    {
      "dimension": "soundness",
      "score": 3,
      "justification": "The experimental methodology is careful and the negative results are well supported and independently verified. Two soundness issues hold it below excellent: the two-condition rule's 19/19 validation is near-tautological given the definitions and is presented as empirical confirmation, and the §5.1 table silently mixes a fixed-threshold sensitivity column with a refit-threshold AUROC column, hiding a one-log-unit instability in tau. The 44 'edited' checkpoints are also label-derived, never behaviourally verified, which the paper's own root C shows can be wrong.",
      "improvements": [
        "Derive discovery-and-completion algebraically instead of validating it empirically: show that e_W(v1) = e_W(r) + O(sin^2 theta) with theta the angle between v1 and r, state the error term, and then present the 19/19 sweep as the measurement of WHICH kernels land in each quadrant (which is the real content) rather than as confirmation of the rule.",
        "Split the §5.1 table into two clearly labelled halves — sensitivity and AUROC at the fixed panel tau, and sensitivity and AUROC under the LORCO-refit tau — and print the refit tau per class (it is -1.7156 for every class in results/analysis.json, against the panel's -2.7415). This is a one-log-unit shift and it belongs beside the 0.128-log-unit brittleness result in §5.4.",
        "Report a behavioural spot-check on a stratified subsample of the 44 at-scale positives (even 8-10 checkpoints x the frozen 40-item core) so that 'sensitivity 0.159' is a sensitivity against models known to be un-censored rather than against card labels. Root C proves the label and the behaviour dissociate, so the paper needs this to bound its own headline."
      ]
    },
    {
      "dimension": "presentation",
      "score": 2,
      "justification": "The prose is skilled but the paper is written as a revision log rather than a standalone document: it repeatedly references 'the previous draft', 'the reviewer objected', 'this iteration', and 'we retract', which a reader with no access to the prior version cannot parse. Section cross-references (§4.2, §5.2, §5.6) do not correspond to any numbered sections in the text. Density is extreme — the Introduction alone carries roughly thirty distinct numerical claims — and the actual argument (precision instrument, no recall, here is why) is buried.",
      "improvements": [
        "Rewrite so the paper stands alone: replace every 'the previous draft'/'the reviewer' construction with a direct statement of what is true, and move the retraction bookkeeping into a short, clearly delimited 'Corrections to prior reporting' subsection. Readers should not need version history to follow the claims.",
        "Number the sections and make the cross-references resolve, and cut the Introduction to at most one number per claim — the mechanism, the at-scale sensitivity versus the regex, and the decoupling. Push the kernel-sweep specifics (spread 8 to 16, minimum depth weight 0.0796 to 0.5311, cos jumps) into §5.2 where they are actually derived.",
        "Add a single figure or table early that states the paper's whole result: for each of the nine recipe classes, its Hub prevalence, whether discovery holds, whether completion holds, and whether W05 fires. That one object replaces several pages of prose and is what a reader will remember."
      ]
    },
    {
      "dimension": "contribution",
      "score": 2,
      "justification": "The paper's own conclusion is that its method does not work at scale and is dominated by a filename regex. What is offered in its place is a mechanism that follows largely from the statistic's definition, and a windowed fix with an empty positive arm (n_G1 = n_G2_G3_synth = n_G4_real = 0 in the artifact). The negative result is well made and the decoupling demonstrations are genuinely useful to the community, but nothing here yet advances what an auditor can do.",
      "improvements": [
        "Run the W05w positive arm. The Arm B kernels (band, Gaussian at each spread, sub-unit uniform, ORBA, Heretic) already exist as checkpoints in this study, and results/arm1_analysis.json shows the scoring harness is written and gated. Scoring them is re-analysis, not a new experiment, and it converts the paper's only forward-looking claim from a proposal into a result. If W05w recovers the Gaussian-depth and band kernels that W05 misses, this becomes an accept-level paper; if it does not, that is also a publishable and cleaner boundary statement.",
        "Add the per-window random-direction null the Discussion already proposes, so the multiple-window false-positive hazard is calibrated rather than merely bounded at n = 40. Without it, W05w's specificity claim rests on a sample two orders of magnitude smaller than the population it is aimed at.",
        "Turn the isometry boundary into a stated proposition with a proof sketch: a Householder reflection leaves W W^T's spectrum invariant, so no statistic that is a function of the pooled or windowed Gram spectrum can see it. A one-paragraph impossibility result is a permanent, citable contribution that survives the metric's failure, and the paper currently asserts it in passing rather than proving it."
      ]
    }
  ],
  "critiques": [
    {
      "category": "rigor",
      "severity": "major",
      "description": "The paper's stated positive contribution — 'detection <=> discovery AND completion, reproducing 19/19 applicable kernels' — is close to an algebraic identity given the definitions, not an empirical discovery, and the 19/19 figure is therefore circular. W05 = log10 min_W e_W(v1) and completion is log10 min_W e_W(r); whenever discovery holds (|cos(v1,r)| -> 1) these two quantities are numerically almost the same object, and the artifact rows show exactly that: uniform_w0.7 gives W05 = -1.1535 against log10 min e_r = -1.1245; uniform_w0.85 gives -1.7488 against -1.7248; uniform_w1.0 gives -4.5917 against -4.5828. Whenever discovery fails, v1 is an unrelated direction whose energy is near the random-direction expectation, so W05 collapses to the parent's value (every Gaussian kernel at spread <= 8 reads -1.0098, the parent's value, to four decimals). So the rule cannot fail on any kernel where discovery is either clearly present or clearly absent, and the 19/19 agreement is a check on a near-identity rather than a validated prediction. Compounding this, the five kernels excluded as 'inapplicable' because the removed direction is not r are rank_k2/4/8 and the two Heretic variants — i.e. precisely the recipe families that account for 13 of the 44 real at-scale misses. The rule is thus untestable on the classes where the failure actually lives.",
      "suggested_action": "Replace the empirical framing with a short derivation. State e_W(v1) = e_W(r)cos^2(theta) + (cross terms) and bound the residual, so the reader sees that detection <=> completion whenever discovery holds and detection is impossible otherwise, as a consequence of the definition. Then reposition the sweep's contribution as what it genuinely is: a measurement of which kernels achieve discovery, and the discovery threshold's dependence on the minimum depth weight (bracketed in [0.0796, 0.5311]) rather than on any uniformity notion. Delete or heavily qualify 'reproduces 19/19 with zero disagreements' as evidence, and add an explicit paragraph saying the rule is currently undefined for multi-direction and per-component kernels, with a proposal for how to generalise it (e.g. discovery against the leading edited subspace rather than a single r, measured by principal angles) so that the two classes that dominate the real failure are covered."
    },
    {
      "category": "scope",
      "severity": "major",
      "description": "The windowed statistic W05w is presented as the paper's diagnosis-to-remedy step and appears in the Introduction, Contributions, Discussion and Conclusion, but it has no positive evaluation whatsoever. The artifact confirms this exactly: results/arm1_analysis.json records n_G1 = 0, n_G2_G3_synth = 0, n_G4_real = 0, catch_by_recipe_class is an empty dict for every k, panel_auroc is empty, and every sensitivity field in the frontier table is NaN over n_positives = 0. The only evidence offered is a 12-matrix toy unit test (d = 64, L = 12) and a specificity result on 40 undeclared models. The paper is commendably explicit about this, but a proposed statistic whose entire positive evidence is one synthetic stub is not a contribution at a top venue, and it currently carries a disproportionate share of the paper's positive framing (a '12.6 log-unit separation' quoted in the Introduction and Conclusion is a toy-stack number). Separately, the declared k = L reproduction gate reports PASS = false in results/gate_numerics.json/arm1_analysis.json because the achieved 8.49e-08 exceeds the declared 1e-09 tolerance on real models; the paper quotes the delta but not the gate's failed status.",
      "suggested_action": "Score W05w on the Arm B kernels that already exist as checkpoints in experiment_1 (band, Gaussian at all nine spreads, sub-unit uniform at w = 0.5/0.7/0.85, ORBA Householder, Heretic, rank-k) and on the 44 Arm A real edited checkpoints, and report sensitivity per k with the specificity already measured. This is re-analysis on tensors and code you have. Report the result whatever it is: if windowing recovers the Gaussian-depth and band kernels, that is the paper's positive claim and it belongs in the Introduction in place of the toy number; if it does not, say so and the mechanism section becomes a boundary result. Until that runs, demote W05w to a clearly labelled 'proposed' subsection, remove the 12.6 log-unit toy figure from the Introduction and Conclusion, and either widen the k = L gate tolerance to a defensible float32 bound or report the gate as failed at its declared tolerance."
    },
    {
      "category": "evidence",
      "severity": "major",
      "description": "The repository-name regex baseline — the number against which the entire paper's negative verdict is stated (0.727 versus 0.159) — is estimated on a panel that was itself discovered by name-based search, which biases it upward. The Arm A candidates are drawn from the iteration-3 census, built from 61 Hub sweeps over '20 search terms, 20 uploaders, 20 architectures' where the search terms are abliteration vocabulary; the paper's own dataset artifact records that 50.5% of harvested edited repositories contain an abliteration string in the id, and the regex's 11 terms include the very strings used to find the repositories. The paper argues the panel is name-blind because eligibility is applied first and the recipe is re-derived from cards, but name-blind filtering of a name-biased candidate pool does not remove the bias: a checkpoint that is edited and named nothing suggestive is systematically less likely to be in the pool at all. The paper's own census says 23.4% of edited rows declare no mechanism, and hub_scan_pool carries 1,105 non-declaring chat repositories, so the stratum where the regex must fail exists and was not sampled. As written, 0.727 is an upper bound on the baseline presented as the baseline.",
      "suggested_action": "Either (a) re-estimate the regex sensitivity on a sample not discovered by name — e.g. draw edited checkpoints from the uploader-sweep and architecture-sweep strata only, or from repositories whose recipe evidence comes from card body text while the repo id contains none of the 11 regex terms — and report that number as the primary baseline; or (b) if that sample cannot be assembled, state plainly that 0.727 is measured on a name-search-derived pool and is therefore an upper bound, and give the regex's sensitivity on the subset of the panel whose recipe was re-derived from card text rather than from the id. Also report W05 and the regex separately on the declared and undeclared strata, since the operational question 'does a weights-only test add anything' is entirely about the undeclared stratum and the paper currently answers it on the declared one."
    },
    {
      "category": "clarity",
      "severity": "major",
      "description": "The §5.1 leave-one-recipe-class-out table is internally inconsistent in a way that hides the paper's strongest threshold-instability result. The table is headed 'held-out recipe class' with columns 'W05 sensitivity at tau' and 'oriented AUROC', but I traced the two columns to different objects in results/analysis.json: the sensitivity column reproduces the fixed_threshold.by_class values at the panel tau = -2.7415, while the AUROC column reproduces the lorco values computed with tau refit on the remaining classes. Under the LORCO refit the sensitivities differ materially — global rank-one is 0.333 rather than the tabulated 0.167, and unknown is 0.400 rather than 0.200 — and the refit tau is -1.7156 for every class, a shift of 1.03 log units from the panel value. That is roughly eight times the 0.128-log-unit shift §5.4 identifies as the brittleness scale, and it is the single most alarming number about the operating point in the whole study, yet it appears nowhere in the paper. A reader who checks the artifact will conclude the table conflates two regimes.",
      "suggested_action": "Give the table four columns: sensitivity and AUROC at the fixed panel tau, and sensitivity and AUROC under the class-held-out refit, with the refit tau printed. Then add one sentence to §5.4 stating that refitting tau on the at-scale positives moves it from -2.7415 to -1.7156, and report specificity on the 122 eligible undeclared checkpoints at the refit value as well — if specificity survives at -1.7156, that is a genuinely reassuring result the paper is currently leaving on the table; if it does not, the honest specificity claim is narrower than 0/122."
    },
    {
      "category": "methodology",
      "severity": "minor",
      "description": "The 44 at-scale positives are labelled 'edited' from model cards and are never behaviourally verified, while the paper itself supplies the reason this matters: root C carries the full weight signature and refuses at its parent's rate, and root B un-censors while reading its parent's W05. If some fraction of the 44 are cosmetic, failed, or merged-away edits with intact refusal behaviour, then 'sensitivity 0.159' is measuring the detector against a partly mislabelled positive class, and both the sensitivity and the regex comparison inherit that. arm_a.jsonl carries no refusal-rate column for any Arm A row. The five SFT-uncensored and four merge-of-abliterated rows (9 of 44) are especially uncertain as positives for a projection detector.",
      "suggested_action": "Measure greedy harmful refusal on the frozen 40-item core for a stratified subsample of the 44 (one or two per recipe class, ~12 checkpoints, a few GPU-hours at these sizes) and report sensitivity both on all 44 and restricted to checkpoints verified to be un-censored. State the restricted number as a sensitivity-analysis row. If the two agree, one sentence retires the objection; if they diverge, that divergence is itself a result about card labels as ground truth, which fits the paper's thesis."
    },
    {
      "category": "rigor",
      "severity": "minor",
      "description": "The entire behavioural axis — including the decoupling headline (0.950 -> 0.270), the effectiveness-versus-detectability intersection, and the laundering orderings — rests on a single LLM judge (llama-3.3-70b-instruct, rubric B) whose agreement with the substring screen this iteration is mean kappa = 0.149 and rate-level r = 0.822, and which was itself substituted for a pre-registered rubric that failed. The paper argues convincingly that the screen is the broken instrument, but the judge's own accuracy is not validated against human or independent-model labels in this iteration; the last such validation was two iterations back on a different rubric. Given that the decoupling result is the paper's most quotable claim and hinges on a 0.270-versus-0.950 judge-scored difference, a single unvalidated scorer is a thin foundation.",
      "suggested_action": "Re-score a stratified 100-200 item subsample of the load-bearing stages (parent, root A, root B, root C, and the flag-death cells) with a second judge from a different model family and report Cohen's kappa and the rate-level agreement, plus a small hand-labelled anchor set. Then state the decoupling result with the judge disagreement propagated: if root B's 0.270 moves by less than the interval width under the second judge, say so explicitly — that one sentence makes the headline much harder to attack."
    },
    {
      "category": "scope",
      "severity": "minor",
      "description": "The 0/122 deployment number is now computed on a defensible, pre-stamped denominator, which is a real improvement, but the eligible population's composition undercuts its relevance to the stated threat model. Of the 40 newly fetched eligible rows, 29 are gpt_neox, and the archived eligible set is dominated by older base models (qwen2 23, llama 19, gpt_neox 6, plus long-tail single-family entries). The population at risk of abliteration is instruction-tuned chat models from the current generation, which is a small minority of this denominator. A false-positive rate measured mostly on pre-2024 base checkpoints is not obviously the false-positive rate an auditor would experience, and the first false positive is in fact a gpt_neox model (rinna/japanese-gpt-neox-small at -2.6139).",
      "suggested_action": "Report the false-positive rate stratified by whether the checkpoint is instruction-tuned/chat-templated versus base, and give the Wilson interval on the chat subset separately. The paper's own hub_scan_pool has 1,105 non-declaring chat repositories, so extending the scan within that stratum (even 40-60 more) would give a specificity number on the population that actually matters. If the chat-subset denominator is small, state its Wilson interval honestly rather than letting the pooled 0/122 stand in for it."
    },
    {
      "category": "clarity",
      "severity": "minor",
      "description": "The paper is written as a revision of a document the reader has never seen. Phrases such as 'the previous draft', 'the reviewer of the previous draft argued', 'this iteration', 'we retract', and 'that objection is upheld in full' appear throughout, including in the Introduction, Contributions and Discussion. Section cross-references (§4.2, §5.1-§5.8) do not resolve to any numbered sections in the manuscript. The Contributions list mixes findings with corrections to prior reporting ('retires four decimal-level claims from the previous draft'), which reads as bookkeeping rather than contribution. This matters disproportionately here because the paper's credibility argument is measurement fidelity.",
      "suggested_action": "Do one editorial pass converting every backward reference into a direct claim ('uniformity is not the predicate' rather than 'we retract the previous draft's uniformity story'), number the sections so the cross-references resolve, and consolidate all corrections-to-prior-reporting into one clearly delimited subsection near the end. Restrict the Contributions list to four items that are findings, not corrections. Also move the 110-assertion self-audit to an appendix or a short methods paragraph — it is excellent practice but it is not a research contribution and listing it as one invites the reading that the paper is short of results."
    },
    {
      "category": "novelty",
      "severity": "minor",
      "description": "The prior-art treatment is thorough and the parent-free positioning survives, but the paper does not fully confront what its own findings do to the novelty claim. Once the certificate is shown to be dominated by a filename regex and to have roughly half the coverage of the parent-requiring incumbent E1, the remaining novel object is 'a parent-free, calibration-free, bottom-of-spectrum, sliding-and-extremum-scored statistic' — and the sliding half is unevaluated. Meanwhile the paper's own reading of [2] establishes that band-averaged scoring is published prior art, and Abliterlitics independently measures the depth-versus-completeness distinction the paper presents as its mechanism. The paper cites both correctly, but the Discussion still frames the mechanism as this paper's discovery rather than as a decomposition that external delta-based forensics had already surfaced empirically.",
      "suggested_action": "Add two or three sentences to the Discussion stating precisely what is new relative to Abliterlitics' measured depth/completeness fingerprints and to [2]'s band-averaged E1: the novelty is doing this without a parent and reading the bottom rather than the top of the spectrum, plus the analytic statement of when that is possible at all (the isometry impossibility). Framing the mechanism as an independent, parent-free confirmation of what delta-based forensics measures is both more accurate and more persuasive than framing it as a discovery."
    }
  ],
  "score": 5,
  "confidence": 4
}
```

### [23] TOOL RESULT — Write · 2026-08-14 02:18:18 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/review_paper/review_paper/.terminal_claude_agent_struct_out.json", "content": "{\n  \"overall_assessment\": \"This is an unusually honest, unusually well-instrumented paper that has responded to essentially every critique from the previous round with real experiments rather than caveats. The at-scale falsification (sensitivity 0.159 on 44 real edited checkpoints against 0.727 for a repository-name regex), the pre-stamped eligibility rule, the recovered ladder denominators, the both-directions decoupling built as checkpoints, and the 110-assertion self-audit are all genuine and verifiable in the artifacts. I checked the headline numbers against results/analysis.json, results/arm1_analysis.json and results/arm2_rates.json and they reproduce, including the uncomfortable ones the paper reports against itself.\\n\\nThe problem is what remains as a positive contribution. The paper explicitly retires its metric, so everything now rests on (a) the two-condition mechanism and (b) the windowed generalisation. (a) is, on the paper's own definitions, very close to an algebraic identity rather than an empirical finding: when |cos(v1,r)|->1 the statistic W05 = log10 min_W e_W(v1) is numerically almost equal to the completion quantity log10 min_W e_W(r) (the artifact rows show -1.153 vs -1.124, -1.749 vs -1.725, -4.592 vs -4.583), and when discovery fails W05 collapses to the parent's value. So 'detected <=> discovery AND completion' is close to a two-line consequence of the definitions, and the 19/19 agreement is a consistency check on an approximation, not evidence. Worse, the five kernels excluded as 'inapplicable' are exactly the rank-k and Heretic families that dominate the real Hub failure. (b) has no positive evaluation at all: arm1_analysis.json records n_G1 = 0, n_G2_G3_synth = 0, n_G4_real = 0, so W05w was scored on zero edited models, and the paper is admirably explicit about this. That leaves the paper as a very well-documented negative result plus a mechanistic re-description plus an unevaluated proposal.\\n\\nI also found one reporting inconsistency that matters: the §5.1 table is headed 'held-out recipe class' but its sensitivity column is taken from the fixed panel threshold while its AUROC column comes from the leave-one-recipe-class-out refit, and those two regimes disagree (global rank-one is 0.167 at fixed tau but 0.333 under LORCO; unknown is 0.200 vs 0.400). The refitted tau is -1.7156 rather than -2.7415 — a one-log-unit shift — which is a stronger statement about threshold instability than §5.4's 0.128-log-unit brittleness result, and it is currently invisible to the reader. And the regex baseline the whole paper is benchmarked against is estimated on a panel drawn from a census built out of 20 abliteration-related search terms, which is close to circular in the regex's favour.\\n\\nFixing the identity framing, the table regime mix, the baseline circularity, and running the W05w positive arm (which is re-analysis of checkpoints that already exist in Arm B) would move this from a careful negative result to a paper with a defensible positive claim. As it stands I read it as borderline: the measurement discipline is above the bar for a top venue, the contribution is not yet.\",\n  \"strengths\": [\n    \"Every critique from the previous round was addressed with a run rather than a hedge: name-blind panel selection, pre-stamped sha256 eligibility rule with a published composition table, recovered ladder denominators (31-40, not the recorded 40) with Wilson intervals, three roots on two architectures, an E1 band-sensitivity sweep, a cost-annotated behavioural table, and a threshold-brittleness curve.\",\n    \"The paper reports against its own interest at almost every opportunity: it retracts the uniformity story, retracts 'parent-free costs nothing', retires four decimal-level ladder claims, corrects its own judge-agreement figure from 0.952 to 0.822, and shows that the parent-requiring incumbent E1 has roughly twice its coverage. This is rare and valuable.\",\n    \"The both-directions decoupling is demonstrated by construction with the confound controlled (root B holds the refusal direction fixed at root A's so the kernel is the only manipulated variable). A false negative that un-censors 0.950 -> 0.270 while reading its parent's W05 to four decimals, and a false positive at -4.587 that never un-censored, together settle what a weights-only statistic can mean far more convincingly than any correlation would.\",\n    \"The at-scale evaluation with an operational baseline is exactly the right test and is rarely done: a weights-only detector that flags a strict subset of what a filename already flags (caught_by_W05_missed_by_name is empty) is a decisive, honest result, and I verified it in results/analysis.json.\",\n    \"The 110-assertion self-audit with declared tolerances, byte-identical reruns, and five reported MISMATCHes — including one where the paper's own quoted subset label was wrong — is a reproducibility standard well above the field norm.\",\n    \"The bf16-versus-float32 storage finding (-4.59 vs -12.71 for the same edit) and the 5-bit rather than 4-bit death of the scar are useful, transferable measurement facts for anyone else working on weight-space forensics.\",\n    \"The prior-art work is thorough and read from primary sources: Heretic's kernel corrected from Gaussian to a triangular tent with a hard cutoff, OBLITERATUS's 'spectral certification' correctly identified as activation-consuming, Abliterlitics correctly positioned as parent-requiring and simultaneously used as independent external evidence for the paper's own mechanism.\"\n  ],\n  \"dimension_scores\": [\n    {\n      \"dimension\": \"soundness\",\n      \"score\": 3,\n      \"justification\": \"The experimental methodology is careful and the negative results are well supported and independently verified. Two soundness issues hold it below excellent: the two-condition rule's 19/19 validation is near-tautological given the definitions and is presented as empirical confirmation, and the §5.1 table silently mixes a fixed-threshold sensitivity column with a refit-threshold AUROC column, hiding a one-log-unit instability in tau. The 44 'edited' checkpoints are also label-derived, never behaviourally verified, which the paper's own root C shows can be wrong.\",\n      \"improvements\": [\n        \"Derive discovery-and-completion algebraically instead of validating it empirically: show that e_W(v1) = e_W(r) + O(sin^2 theta) with theta the angle between v1 and r, state the error term, and then present the 19/19 sweep as the measurement of WHICH kernels land in each quadrant (which is the real content) rather than as confirmation of the rule.\",\n        \"Split the §5.1 table into two clearly labelled halves — sensitivity and AUROC at the fixed panel tau, and sensitivity and AUROC under the LORCO-refit tau — and print the refit tau per class (it is -1.7156 for every class in results/analysis.json, against the panel's -2.7415). This is a one-log-unit shift and it belongs beside the 0.128-log-unit brittleness result in §5.4.\",\n        \"Report a behavioural spot-check on a stratified subsample of the 44 at-scale positives (even 8-10 checkpoints x the frozen 40-item core) so that 'sensitivity 0.159' is a sensitivity against models known to be un-censored rather than against card labels. Root C proves the label and the behaviour dissociate, so the paper needs this to bound its own headline.\"\n      ]\n    },\n    {\n      \"dimension\": \"presentation\",\n      \"score\": 2,\n      \"justification\": \"The prose is skilled but the paper is written as a revision log rather than a standalone document: it repeatedly references 'the previous draft', 'the reviewer objected', 'this iteration', and 'we retract', which a reader with no access to the prior version cannot parse. Section cross-references (§4.2, §5.2, §5.6) do not correspond to any numbered sections in the text. Density is extreme — the Introduction alone carries roughly thirty distinct numerical claims — and the actual argument (precision instrument, no recall, here is why) is buried.\",\n      \"improvements\": [\n        \"Rewrite so the paper stands alone: replace every 'the previous draft'/'the reviewer' construction with a direct statement of what is true, and move the retraction bookkeeping into a short, clearly delimited 'Corrections to prior reporting' subsection. Readers should not need version history to follow the claims.\",\n        \"Number the sections and make the cross-references resolve, and cut the Introduction to at most one number per claim — the mechanism, the at-scale sensitivity versus the regex, and the decoupling. Push the kernel-sweep specifics (spread 8 to 16, minimum depth weight 0.0796 to 0.5311, cos jumps) into §5.2 where they are actually derived.\",\n        \"Add a single figure or table early that states the paper's whole result: for each of the nine recipe classes, its Hub prevalence, whether discovery holds, whether completion holds, and whether W05 fires. That one object replaces several pages of prose and is what a reader will remember.\"\n      ]\n    },\n    {\n      \"dimension\": \"contribution\",\n      \"score\": 2,\n      \"justification\": \"The paper's own conclusion is that its method does not work at scale and is dominated by a filename regex. What is offered in its place is a mechanism that follows largely from the statistic's definition, and a windowed fix with an empty positive arm (n_G1 = n_G2_G3_synth = n_G4_real = 0 in the artifact). The negative result is well made and the decoupling demonstrations are genuinely useful to the community, but nothing here yet advances what an auditor can do.\",\n      \"improvements\": [\n        \"Run the W05w positive arm. The Arm B kernels (band, Gaussian at each spread, sub-unit uniform, ORBA, Heretic) already exist as checkpoints in this study, and results/arm1_analysis.json shows the scoring harness is written and gated. Scoring them is re-analysis, not a new experiment, and it converts the paper's only forward-looking claim from a proposal into a result. If W05w recovers the Gaussian-depth and band kernels that W05 misses, this becomes an accept-level paper; if it does not, that is also a publishable and cleaner boundary statement.\",\n        \"Add the per-window random-direction null the Discussion already proposes, so the multiple-window false-positive hazard is calibrated rather than merely bounded at n = 40. Without it, W05w's specificity claim rests on a sample two orders of magnitude smaller than the population it is aimed at.\",\n        \"Turn the isometry boundary into a stated proposition with a proof sketch: a Householder reflection leaves W W^T's spectrum invariant, so no statistic that is a function of the pooled or windowed Gram spectrum can see it. A one-paragraph impossibility result is a permanent, citable contribution that survives the metric's failure, and the paper currently asserts it in passing rather than proving it.\"\n      ]\n    }\n  ],\n  \"critiques\": [\n    {\n      \"category\": \"rigor\",\n      \"severity\": \"major\",\n      \"description\": \"The paper's stated positive contribution — 'detection <=> discovery AND completion, reproducing 19/19 applicable kernels' — is close to an algebraic identity given the definitions, not an empirical discovery, and the 19/19 figure is therefore circular. W05 = log10 min_W e_W(v1) and completion is log10 min_W e_W(r); whenever discovery holds (|cos(v1,r)| -> 1) these two quantities are numerically almost the same object, and the artifact rows show exactly that: uniform_w0.7 gives W05 = -1.1535 against log10 min e_r = -1.1245; uniform_w0.85 gives -1.7488 against -1.7248; uniform_w1.0 gives -4.5917 against -4.5828. Whenever discovery fails, v1 is an unrelated direction whose energy is near the random-direction expectation, so W05 collapses to the parent's value (every Gaussian kernel at spread <= 8 reads -1.0098, the parent's value, to four decimals). So the rule cannot fail on any kernel where discovery is either clearly present or clearly absent, and the 19/19 agreement is a check on a near-identity rather than a validated prediction. Compounding this, the five kernels excluded as 'inapplicable' because the removed direction is not r are rank_k2/4/8 and the two Heretic variants — i.e. precisely the recipe families that account for 13 of the 44 real at-scale misses. The rule is thus untestable on the classes where the failure actually lives.\",\n      \"suggested_action\": \"Replace the empirical framing with a short derivation. State e_W(v1) = e_W(r)cos^2(theta) + (cross terms) and bound the residual, so the reader sees that detection <=> completion whenever discovery holds and detection is impossible otherwise, as a consequence of the definition. Then reposition the sweep's contribution as what it genuinely is: a measurement of which kernels achieve discovery, and the discovery threshold's dependence on the minimum depth weight (bracketed in [0.0796, 0.5311]) rather than on any uniformity notion. Delete or heavily qualify 'reproduces 19/19 with zero disagreements' as evidence, and add an explicit paragraph saying the rule is currently undefined for multi-direction and per-component kernels, with a proposal for how to generalise it (e.g. discovery against the leading edited subspace rather than a single r, measured by principal angles) so that the two classes that dominate the real failure are covered.\"\n    },\n    {\n      \"category\": \"scope\",\n      \"severity\": \"major\",\n      \"description\": \"The windowed statistic W05w is presented as the paper's diagnosis-to-remedy step and appears in the Introduction, Contributions, Discussion and Conclusion, but it has no positive evaluation whatsoever. The artifact confirms this exactly: results/arm1_analysis.json records n_G1 = 0, n_G2_G3_synth = 0, n_G4_real = 0, catch_by_recipe_class is an empty dict for every k, panel_auroc is empty, and every sensitivity field in the frontier table is NaN over n_positives = 0. The only evidence offered is a 12-matrix toy unit test (d = 64, L = 12) and a specificity result on 40 undeclared models. The paper is commendably explicit about this, but a proposed statistic whose entire positive evidence is one synthetic stub is not a contribution at a top venue, and it currently carries a disproportionate share of the paper's positive framing (a '12.6 log-unit separation' quoted in the Introduction and Conclusion is a toy-stack number). Separately, the declared k = L reproduction gate reports PASS = false in results/gate_numerics.json/arm1_analysis.json because the achieved 8.49e-08 exceeds the declared 1e-09 tolerance on real models; the paper quotes the delta but not the gate's failed status.\",\n      \"suggested_action\": \"Score W05w on the Arm B kernels that already exist as checkpoints in experiment_1 (band, Gaussian at all nine spreads, sub-unit uniform at w = 0.5/0.7/0.85, ORBA Householder, Heretic, rank-k) and on the 44 Arm A real edited checkpoints, and report sensitivity per k with the specificity already measured. This is re-analysis on tensors and code you have. Report the result whatever it is: if windowing recovers the Gaussian-depth and band kernels, that is the paper's positive claim and it belongs in the Introduction in place of the toy number; if it does not, say so and the mechanism section becomes a boundary result. Until that runs, demote W05w to a clearly labelled 'proposed' subsection, remove the 12.6 log-unit toy figure from the Introduction and Conclusion, and either widen the k = L gate tolerance to a defensible float32 bound or report the gate as failed at its declared tolerance.\"\n    },\n    {\n      \"category\": \"evidence\",\n      \"severity\": \"major\",\n      \"description\": \"The repository-name regex baseline — the number against which the entire paper's negative verdict is stated (0.727 versus 0.159) — is estimated on a panel that was itself discovered by name-based search, which biases it upward. The Arm A candidates are drawn from the iteration-3 census, built from 61 Hub sweeps over '20 search terms, 20 uploaders, 20 architectures' where the search terms are abliteration vocabulary; the paper's own dataset artifact records that 50.5% of harvested edited repositories contain an abliteration string in the id, and the regex's 11 terms include the very strings used to find the repositories. The paper argues the panel is name-blind because eligibility is applied first and the recipe is re-derived from cards, but name-blind filtering of a name-biased candidate pool does not remove the bias: a checkpoint that is edited and named nothing suggestive is systematically less likely to be in the pool at all. The paper's own census says 23.4% of edited rows declare no mechanism, and hub_scan_pool carries 1,105 non-declaring chat repositories, so the stratum where the regex must fail exists and was not sampled. As written, 0.727 is an upper bound on the baseline presented as the baseline.\",\n      \"suggested_action\": \"Either (a) re-estimate the regex sensitivity on a sample not discovered by name — e.g. draw edited checkpoints from the uploader-sweep and architecture-sweep strata only, or from repositories whose recipe evidence comes from card body text while the repo id contains none of the 11 regex terms — and report that number as the primary baseline; or (b) if that sample cannot be assembled, state plainly that 0.727 is measured on a name-search-derived pool and is therefore an upper bound, and give the regex's sensitivity on the subset of the panel whose recipe was re-derived from card text rather than from the id. Also report W05 and the regex separately on the declared and undeclared strata, since the operational question 'does a weights-only test add anything' is entirely about the undeclared stratum and the paper currently answers it on the declared one.\"\n    },\n    {\n      \"category\": \"clarity\",\n      \"severity\": \"major\",\n      \"description\": \"The §5.1 leave-one-recipe-class-out table is internally inconsistent in a way that hides the paper's strongest threshold-instability result. The table is headed 'held-out recipe class' with columns 'W05 sensitivity at tau' and 'oriented AUROC', but I traced the two columns to different objects in results/analysis.json: the sensitivity column reproduces the fixed_threshold.by_class values at the panel tau = -2.7415, while the AUROC column reproduces the lorco values computed with tau refit on the remaining classes. Under the LORCO refit the sensitivities differ materially — global rank-one is 0.333 rather than the tabulated 0.167, and unknown is 0.400 rather than 0.200 — and the refit tau is -1.7156 for every class, a shift of 1.03 log units from the panel value. That is roughly eight times the 0.128-log-unit shift §5.4 identifies as the brittleness scale, and it is the single most alarming number about the operating point in the whole study, yet it appears nowhere in the paper. A reader who checks the artifact will conclude the table conflates two regimes.\",\n      \"suggested_action\": \"Give the table four columns: sensitivity and AUROC at the fixed panel tau, and sensitivity and AUROC under the class-held-out refit, with the refit tau printed. Then add one sentence to §5.4 stating that refitting tau on the at-scale positives moves it from -2.7415 to -1.7156, and report specificity on the 122 eligible undeclared checkpoints at the refit value as well — if specificity survives at -1.7156, that is a genuinely reassuring result the paper is currently leaving on the table; if it does not, the honest specificity claim is narrower than 0/122.\"\n    },\n    {\n      \"category\": \"methodology\",\n      \"severity\": \"minor\",\n      \"description\": \"The 44 at-scale positives are labelled 'edited' from model cards and are never behaviourally verified, while the paper itself supplies the reason this matters: root C carries the full weight signature and refuses at its parent's rate, and root B un-censors while reading its parent's W05. If some fraction of the 44 are cosmetic, failed, or merged-away edits with intact refusal behaviour, then 'sensitivity 0.159' is measuring the detector against a partly mislabelled positive class, and both the sensitivity and the regex comparison inherit that. arm_a.jsonl carries no refusal-rate column for any Arm A row. The five SFT-uncensored and four merge-of-abliterated rows (9 of 44) are especially uncertain as positives for a projection detector.\",\n      \"suggested_action\": \"Measure greedy harmful refusal on the frozen 40-item core for a stratified subsample of the 44 (one or two per recipe class, ~12 checkpoints, a few GPU-hours at these sizes) and report sensitivity both on all 44 and restricted to checkpoints verified to be un-censored. State the restricted number as a sensitivity-analysis row. If the two agree, one sentence retires the objection; if they diverge, that divergence is itself a result about card labels as ground truth, which fits the paper's thesis.\"\n    },\n    {\n      \"category\": \"rigor\",\n      \"severity\": \"minor\",\n      \"description\": \"The entire behavioural axis — including the decoupling headline (0.950 -> 0.270), the effectiveness-versus-detectability intersection, and the laundering orderings — rests on a single LLM judge (llama-3.3-70b-instruct, rubric B) whose agreement with the substring screen this iteration is mean kappa = 0.149 and rate-level r = 0.822, and which was itself substituted for a pre-registered rubric that failed. The paper argues convincingly that the screen is the broken instrument, but the judge's own accuracy is not validated against human or independent-model labels in this iteration; the last such validation was two iterations back on a different rubric. Given that the decoupling result is the paper's most quotable claim and hinges on a 0.270-versus-0.950 judge-scored difference, a single unvalidated scorer is a thin foundation.\",\n      \"suggested_action\": \"Re-score a stratified 100-200 item subsample of the load-bearing stages (parent, root A, root B, root C, and the flag-death cells) with a second judge from a different model family and report Cohen's kappa and the rate-level agreement, plus a small hand-labelled anchor set. Then state the decoupling result with the judge disagreement propagated: if root B's 0.270 moves by less than the interval width under the second judge, say so explicitly — that one sentence makes the headline much harder to attack.\"\n    },\n    {\n      \"category\": \"scope\",\n      \"severity\": \"minor\",\n      \"description\": \"The 0/122 deployment number is now computed on a defensible, pre-stamped denominator, which is a real improvement, but the eligible population's composition undercuts its relevance to the stated threat model. Of the 40 newly fetched eligible rows, 29 are gpt_neox, and the archived eligible set is dominated by older base models (qwen2 23, llama 19, gpt_neox 6, plus long-tail single-family entries). The population at risk of abliteration is instruction-tuned chat models from the current generation, which is a small minority of this denominator. A false-positive rate measured mostly on pre-2024 base checkpoints is not obviously the false-positive rate an auditor would experience, and the first false positive is in fact a gpt_neox model (rinna/japanese-gpt-neox-small at -2.6139).\",\n      \"suggested_action\": \"Report the false-positive rate stratified by whether the checkpoint is instruction-tuned/chat-templated versus base, and give the Wilson interval on the chat subset separately. The paper's own hub_scan_pool has 1,105 non-declaring chat repositories, so extending the scan within that stratum (even 40-60 more) would give a specificity number on the population that actually matters. If the chat-subset denominator is small, state its Wilson interval honestly rather than letting the pooled 0/122 stand in for it.\"\n    },\n    {\n      \"category\": \"clarity\",\n      \"severity\": \"minor\",\n      \"description\": \"The paper is written as a revision of a document the reader has never seen. Phrases such as 'the previous draft', 'the reviewer of the previous draft argued', 'this iteration', 'we retract', and 'that objection is upheld in full' appear throughout, including in the Introduction, Contributions and Discussion. Section cross-references (§4.2, §5.1-§5.8) do not resolve to any numbered sections in the manuscript. The Contributions list mixes findings with corrections to prior reporting ('retires four decimal-level claims from the previous draft'), which reads as bookkeeping rather than contribution. This matters disproportionately here because the paper's credibility argument is measurement fidelity.\",\n      \"suggested_action\": \"Do one editorial pass converting every backward reference into a direct claim ('uniformity is not the predicate' rather than 'we retract the previous draft's uniformity story'), number the sections so the cross-references resolve, and consolidate all corrections-to-prior-reporting into one clearly delimited subsection near the end. Restrict the Contributions list to four items that are findings, not corrections. Also move the 110-assertion self-audit to an appendix or a short methods paragraph — it is excellent practice but it is not a research contribution and listing it as one invites the reading that the paper is short of results.\"\n    },\n    {\n      \"category\": \"novelty\",\n      \"severity\": \"minor\",\n      \"description\": \"The prior-art treatment is thorough and the parent-free positioning survives, but the paper does not fully confront what its own findings do to the novelty claim. Once the certificate is shown to be dominated by a filename regex and to have roughly half the coverage of the parent-requiring incumbent E1, the remaining novel object is 'a parent-free, calibration-free, bottom-of-spectrum, sliding-and-extremum-scored statistic' — and the sliding half is unevaluated. Meanwhile the paper's own reading of [2] establishes that band-averaged scoring is published prior art, and Abliterlitics independently measures the depth-versus-completeness distinction the paper presents as its mechanism. The paper cites both correctly, but the Discussion still frames the mechanism as this paper's discovery rather than as a decomposition that external delta-based forensics had already surfaced empirically.\",\n      \"suggested_action\": \"Add two or three sentences to the Discussion stating precisely what is new relative to Abliterlitics' measured depth/completeness fingerprints and to [2]'s band-averaged E1: the novelty is doing this without a parent and reading the bottom rather than the top of the spectrum, plus the analytic statement of when that is possible at all (the isometry impossibility). Framing the mechanism as an independent, parent-free confirmation of what delta-based forensics measures is both more accurate and more persuasive than framing it as a discovery.\"\n    }\n  ],\n  \"score\": 5,\n  \"confidence\": 4\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [24] ASSISTANT · 2026-08-14 02:18:31 UTC

```
Review written to `./.terminal_claude_agent_struct_out.json`.

**Verdict: 5 (Borderline Accept), confidence 4.** Soundness 3, Presentation 2, Contribution 2.

Key findings from verifying against the artifacts:

1. **The two-condition rule is near-tautological** (major). `analysis.json` shows W05 ≈ log₁₀ min e_r whenever discovery holds (−1.153 vs −1.124; −1.749 vs −1.725; −4.592 vs −4.583) and collapses to the parent's −1.0098 when it fails. So "detected ⇔ discovery ∧ completion" follows from the definitions; 19/19 is a consistency check on an approximation, not confirmation. Worse, the 5 excluded "inapplicable" kernels are exactly the rank-k and Heretic families that dominate the real failure.

2. **W05w's positive arm is empty** (major, and the paper says so honestly): `arm1_analysis.json` has `n_G1=0, n_G2_G3_synth=0, n_G4_real=0`, all frontier sensitivities NaN. The 12.6-log-unit headline is a 12-matrix toy. Also `kL_reproduces_W05` reports `PASS: false` at its declared 1e-9 tolerance.

3. **§5.1 table mixes two threshold regimes** (major/clarity): sensitivity column is at fixed τ=−2.7415, AUROC column comes from LORCO where τ refits to **−1.7156** — a 1.03 log-unit shift, ~8× the brittleness scale §5.4 reports. Under the refit, global-rank-one is 0.333 not 0.167 and unknown 0.400 not 0.200.

4. **Regex baseline is circular-ish** (major/evidence): the 0.727 is measured on a panel drawn from a census built with 20 abliteration search terms — name-blind filtering of a name-biased pool.

5. Minor: the 44 at-scale positives are card-labelled and never behaviourally verified (the paper's own root C shows why that matters); single unvalidated judge (κ=0.149 vs regex); the 0/122 denominator is dominated by gpt_neox/base models rather than current chat models; and the draft reads as a revision log with unresolvable §-references.
```
