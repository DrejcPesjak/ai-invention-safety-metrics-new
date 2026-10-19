# gen_paper_text — test_idea

> Phase: `invention_loop` · round 5 · `gen_paper_text`
> Run: `iter1_33370088803c` — Catching Edited Safety Models by Reading Weights in Sliding Windows
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_paper_text` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-14 05:49:34 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A research paper writer (Step 3.4: GEN_PAPER_TEXT in the invention loop)

You received the hypothesis, all artifacts, the previous paper draft (if any), and reviewer feedback.
Write a complete paper draft with figure placeholders.

Publication-quality paper → strong contribution. Weak paper → wasted iteration.
</your_role>
</ai_inventor_context>

<research_methodology>
Write like a researcher drafting a paper, not a chatbot summarizing bullet points.

- Structure as a paper would: research question → methodology → results → analysis → limitations. Not a list of "we did X, then Y."
- Ground every claim in specific artifacts and specific numbers. "Results show improvement" is empty — state effect sizes, baselines, and conditions.
- Be honest about what worked, what didn't, and why. Don't spin failures as "future work."
- The paper's headline contribution should be a positive or surprising finding. Negative results are valuable context but should not be the primary narrative — lead with what works.
- Address reviewer feedback from previous iterations explicitly — show you've thought about each critique.
</research_methodology>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape. Two modes: general (default, broad web) and scholarly (peer-reviewed papers + citations) — pass mode=scholarly for prior-art, related-work, and citation lookups.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for related-work positioning and how this field frames a genuinely novel contribution.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>
<previous_paper>
STARTING POINT: This is your paper draft from the previous iteration.

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

</previous_paper>

<reviewer_feedback>
STEP 1 — REVIEW: A reviewer evaluated the previous paper draft above and produced this feedback.

- [MAJOR] (rigor) The paper's stated positive contribution — 'detection <=> discovery AND completion, reproducing 19/19 applicable kernels' — is close to an algebraic identity given the definitions, not an empirical discovery, and the 19/19 figure is therefore circular. W05 = log10 min_W e_W(v1) and completion is log10 min_W e_W(r); whenever discovery holds (|cos(v1,r)| -> 1) these two quantities are numerically almost the same object, and the artifact rows show exactly that: uniform_w0.7 gives W05 = -1.1535 against log10 min e_r = -1.1245; uniform_w0.85 gives -1.7488 against -1.7248; uniform_w1.0 gives -4.5917 against -4.5828. Whenever discovery fails, v1 is an unrelated direction whose energy is near the random-direction expectation, so W05 collapses to the parent's value (every Gaussian kernel at spread <= 8 reads -1.0098, the parent's value, to four decimals). So the rule cannot fail on any kernel where discovery is either clearly present or clearly absent, and the 19/19 agreement is a check on a near-identity rather than a validated prediction. Compounding this, the five kernels excluded as 'inapplicable' because the removed direction is not r are rank_k2/4/8 and the two Heretic variants — i.e. precisely the recipe families that account for 13 of the 44 real at-scale misses. The rule is thus untestable on the classes where the failure actually lives.
  Action: Replace the empirical framing with a short derivation. State e_W(v1) = e_W(r)cos^2(theta) + (cross terms) and bound the residual, so the reader sees that detection <=> completion whenever discovery holds and detection is impossible otherwise, as a consequence of the definition. Then reposition the sweep's contribution as what it genuinely is: a measurement of which kernels achieve discovery, and the discovery threshold's dependence on the minimum depth weight (bracketed in [0.0796, 0.5311]) rather than on any uniformity notion. Delete or heavily qualify 'reproduces 19/19 with zero disagreements' as evidence, and add an explicit paragraph saying the rule is currently undefined for multi-direction and per-component kernels, with a proposal for how to generalise it (e.g. discovery against the leading edited subspace rather than a single r, measured by principal angles) so that the two classes that dominate the real failure are covered.
- [MAJOR] (scope) The windowed statistic W05w is presented as the paper's diagnosis-to-remedy step and appears in the Introduction, Contributions, Discussion and Conclusion, but it has no positive evaluation whatsoever. The artifact confirms this exactly: results/arm1_analysis.json records n_G1 = 0, n_G2_G3_synth = 0, n_G4_real = 0, catch_by_recipe_class is an empty dict for every k, panel_auroc is empty, and every sensitivity field in the frontier table is NaN over n_positives = 0. The only evidence offered is a 12-matrix toy unit test (d = 64, L = 12) and a specificity result on 40 undeclared models. The paper is commendably explicit about this, but a proposed statistic whose entire positive evidence is one synthetic stub is not a contribution at a top venue, and it currently carries a disproportionate share of the paper's positive framing (a '12.6 log-unit separation' quoted in the Introduction and Conclusion is a toy-stack number). Separately, the declared k = L reproduction gate reports PASS = false in results/gate_numerics.json/arm1_analysis.json because the achieved 8.49e-08 exceeds the declared 1e-09 tolerance on real models; the paper quotes the delta but not the gate's failed status.
  Action: Score W05w on the Arm B kernels that already exist as checkpoints in experiment_1 (band, Gaussian at all nine spreads, sub-unit uniform at w = 0.5/0.7/0.85, ORBA Householder, Heretic, rank-k) and on the 44 Arm A real edited checkpoints, and report sensitivity per k with the specificity already measured. This is re-analysis on tensors and code you have. Report the result whatever it is: if windowing recovers the Gaussian-depth and band kernels, that is the paper's positive claim and it belongs in the Introduction in place of the toy number; if it does not, say so and the mechanism section becomes a boundary result. Until that runs, demote W05w to a clearly labelled 'proposed' subsection, remove the 12.6 log-unit toy figure from the Introduction and Conclusion, and either widen the k = L gate tolerance to a defensible float32 bound or report the gate as failed at its declared tolerance.
- [MAJOR] (evidence) The repository-name regex baseline — the number against which the entire paper's negative verdict is stated (0.727 versus 0.159) — is estimated on a panel that was itself discovered by name-based search, which biases it upward. The Arm A candidates are drawn from the iteration-3 census, built from 61 Hub sweeps over '20 search terms, 20 uploaders, 20 architectures' where the search terms are abliteration vocabulary; the paper's own dataset artifact records that 50.5% of harvested edited repositories contain an abliteration string in the id, and the regex's 11 terms include the very strings used to find the repositories. The paper argues the panel is name-blind because eligibility is applied first and the recipe is re-derived from cards, but name-blind filtering of a name-biased candidate pool does not remove the bias: a checkpoint that is edited and named nothing suggestive is systematically less likely to be in the pool at all. The paper's own census says 23.4% of edited rows declare no mechanism, and hub_scan_pool carries 1,105 non-declaring chat repositories, so the stratum where the regex must fail exists and was not sampled. As written, 0.727 is an upper bound on the baseline presented as the baseline.
  Action: Either (a) re-estimate the regex sensitivity on a sample not discovered by name — e.g. draw edited checkpoints from the uploader-sweep and architecture-sweep strata only, or from repositories whose recipe evidence comes from card body text while the repo id contains none of the 11 regex terms — and report that number as the primary baseline; or (b) if that sample cannot be assembled, state plainly that 0.727 is measured on a name-search-derived pool and is therefore an upper bound, and give the regex's sensitivity on the subset of the panel whose recipe was re-derived from card text rather than from the id. Also report W05 and the regex separately on the declared and undeclared strata, since the operational question 'does a weights-only test add anything' is entirely about the undeclared stratum and the paper currently answers it on the declared one.
- [MAJOR] (clarity) The §5.1 leave-one-recipe-class-out table is internally inconsistent in a way that hides the paper's strongest threshold-instability result. The table is headed 'held-out recipe class' with columns 'W05 sensitivity at tau' and 'oriented AUROC', but I traced the two columns to different objects in results/analysis.json: the sensitivity column reproduces the fixed_threshold.by_class values at the panel tau = -2.7415, while the AUROC column reproduces the lorco values computed with tau refit on the remaining classes. Under the LORCO refit the sensitivities differ materially — global rank-one is 0.333 rather than the tabulated 0.167, and unknown is 0.400 rather than 0.200 — and the refit tau is -1.7156 for every class, a shift of 1.03 log units from the panel value. That is roughly eight times the 0.128-log-unit shift §5.4 identifies as the brittleness scale, and it is the single most alarming number about the operating point in the whole study, yet it appears nowhere in the paper. A reader who checks the artifact will conclude the table conflates two regimes.
  Action: Give the table four columns: sensitivity and AUROC at the fixed panel tau, and sensitivity and AUROC under the class-held-out refit, with the refit tau printed. Then add one sentence to §5.4 stating that refitting tau on the at-scale positives moves it from -2.7415 to -1.7156, and report specificity on the 122 eligible undeclared checkpoints at the refit value as well — if specificity survives at -1.7156, that is a genuinely reassuring result the paper is currently leaving on the table; if it does not, the honest specificity claim is narrower than 0/122.
- [MINOR] (methodology) The 44 at-scale positives are labelled 'edited' from model cards and are never behaviourally verified, while the paper itself supplies the reason this matters: root C carries the full weight signature and refuses at its parent's rate, and root B un-censors while reading its parent's W05. If some fraction of the 44 are cosmetic, failed, or merged-away edits with intact refusal behaviour, then 'sensitivity 0.159' is measuring the detector against a partly mislabelled positive class, and both the sensitivity and the regex comparison inherit that. arm_a.jsonl carries no refusal-rate column for any Arm A row. The five SFT-uncensored and four merge-of-abliterated rows (9 of 44) are especially uncertain as positives for a projection detector.
  Action: Measure greedy harmful refusal on the frozen 40-item core for a stratified subsample of the 44 (one or two per recipe class, ~12 checkpoints, a few GPU-hours at these sizes) and report sensitivity both on all 44 and restricted to checkpoints verified to be un-censored. State the restricted number as a sensitivity-analysis row. If the two agree, one sentence retires the objection; if they diverge, that divergence is itself a result about card labels as ground truth, which fits the paper's thesis.
- [MINOR] (rigor) The entire behavioural axis — including the decoupling headline (0.950 -> 0.270), the effectiveness-versus-detectability intersection, and the laundering orderings — rests on a single LLM judge (llama-3.3-70b-instruct, rubric B) whose agreement with the substring screen this iteration is mean kappa = 0.149 and rate-level r = 0.822, and which was itself substituted for a pre-registered rubric that failed. The paper argues convincingly that the screen is the broken instrument, but the judge's own accuracy is not validated against human or independent-model labels in this iteration; the last such validation was two iterations back on a different rubric. Given that the decoupling result is the paper's most quotable claim and hinges on a 0.270-versus-0.950 judge-scored difference, a single unvalidated scorer is a thin foundation.
  Action: Re-score a stratified 100-200 item subsample of the load-bearing stages (parent, root A, root B, root C, and the flag-death cells) with a second judge from a different model family and report Cohen's kappa and the rate-level agreement, plus a small hand-labelled anchor set. Then state the decoupling result with the judge disagreement propagated: if root B's 0.270 moves by less than the interval width under the second judge, say so explicitly — that one sentence makes the headline much harder to attack.
- [MINOR] (scope) The 0/122 deployment number is now computed on a defensible, pre-stamped denominator, which is a real improvement, but the eligible population's composition undercuts its relevance to the stated threat model. Of the 40 newly fetched eligible rows, 29 are gpt_neox, and the archived eligible set is dominated by older base models (qwen2 23, llama 19, gpt_neox 6, plus long-tail single-family entries). The population at risk of abliteration is instruction-tuned chat models from the current generation, which is a small minority of this denominator. A false-positive rate measured mostly on pre-2024 base checkpoints is not obviously the false-positive rate an auditor would experience, and the first false positive is in fact a gpt_neox model (rinna/japanese-gpt-neox-small at -2.6139).
  Action: Report the false-positive rate stratified by whether the checkpoint is instruction-tuned/chat-templated versus base, and give the Wilson interval on the chat subset separately. The paper's own hub_scan_pool has 1,105 non-declaring chat repositories, so extending the scan within that stratum (even 40-60 more) would give a specificity number on the population that actually matters. If the chat-subset denominator is small, state its Wilson interval honestly rather than letting the pooled 0/122 stand in for it.
- [MINOR] (clarity) The paper is written as a revision of a document the reader has never seen. Phrases such as 'the previous draft', 'the reviewer of the previous draft argued', 'this iteration', 'we retract', and 'that objection is upheld in full' appear throughout, including in the Introduction, Contributions and Discussion. Section cross-references (§4.2, §5.1-§5.8) do not resolve to any numbered sections in the manuscript. The Contributions list mixes findings with corrections to prior reporting ('retires four decimal-level claims from the previous draft'), which reads as bookkeeping rather than contribution. This matters disproportionately here because the paper's credibility argument is measurement fidelity.
  Action: Do one editorial pass converting every backward reference into a direct claim ('uniformity is not the predicate' rather than 'we retract the previous draft's uniformity story'), number the sections so the cross-references resolve, and consolidate all corrections-to-prior-reporting into one clearly delimited subsection near the end. Restrict the Contributions list to four items that are findings, not corrections. Also move the 110-assertion self-audit to an appendix or a short methods paragraph — it is excellent practice but it is not a research contribution and listing it as one invites the reading that the paper is short of results.
- [MINOR] (novelty) The prior-art treatment is thorough and the parent-free positioning survives, but the paper does not fully confront what its own findings do to the novelty claim. Once the certificate is shown to be dominated by a filename regex and to have roughly half the coverage of the parent-requiring incumbent E1, the remaining novel object is 'a parent-free, calibration-free, bottom-of-spectrum, sliding-and-extremum-scored statistic' — and the sliding half is unevaluated. Meanwhile the paper's own reading of [2] establishes that band-averaged scoring is published prior art, and Abliterlitics independently measures the depth-versus-completeness distinction the paper presents as its mechanism. The paper cites both correctly, but the Discussion still frames the mechanism as this paper's discovery rather than as a decomposition that external delta-based forensics had already surfaced empirically.
  Action: Add two or three sentences to the Discussion stating precisely what is new relative to Abliterlitics' measured depth/completeness fingerprints and to [2]'s band-averaged E1: the novelty is doing this without a parent and reading the bottom rather than the top of the spectrum, plus the analytic statement of when that is possible at all (the isometry impossibility). Framing the mechanism as an independent, parent-free confirmation of what delta-based forensics measures is both more accurate and more persuasive than framing it as a discovery.
</reviewer_feedback>

<pipeline_steps>
STEP 2 — STRATEGY: The pipeline's strategy generator (gen_strat) read the reviewer feedback
and designed a new research strategy to address the critiques.

STEP 3 — PLANNING: The planner (gen_plan) turned the strategy into concrete artifact plans —
specific experiments, datasets, or research tasks to execute.

STEP 4 — EXECUTION: The executor (gen_art) ran those plans and produced the new artifacts
shown in <new_artifacts_this_iteration> below.
</pipeline_steps>

<hypothesis>
STEP 5 — HYPOTHESIS UPDATE: The hypothesis was revised based on evidence from previous iterations.

kind: hypothesis
title: Spotting an edited safety model from weights
hypothesis: |-
  CORE CLAIM, STILL SPLIT IN TWO, WITH CLAIM A NOW A BOUNDED NEGATIVE PLUS AN ANALYTIC BOUNDARY. The original claim -- safety behaviour is legible from the model alone, cheaply, better than from its outputs -- remains resolved into two halves, and iteration 4 changed the sign of the first one. Iteration 3 said the supported half was a claim about UNIFORMITY. Iteration 4 took that to scale and BOTH halves of the uniformity story failed. What survives is smaller, sharper and, we think, still worth a paper: a parent-free spectral certificate is a PRECISION INSTRUMENT WITH ALMOST NO RECALL, its recall is governed by a condition that is ANALYTIC rather than empirical, its verdict is DISSOCIABLE FROM SAFETY BEHAVIOUR IN BOTH DIRECTIONS BY CONSTRUCTION, and on ordinary Hub traffic it is dominated by a filename regex.

  CLAIM A (NOW LARGELY REFUTED AT SCALE, WITH A PRECISE RESIDUE). W05 = log10 min_W e_W(v1) over the pooled residual-write Gram certifies a UNIFORM, COMPLETE, ALL-LAYER directional annihilation with zero prompts, zero forward passes and ~7-11 s of CPU linear algebra -- but on 44 real public sub-4.2B edited checkpoints from 27 uploaders across 9 recipe classes it fires on SEVEN (sensitivity 0.159) while all five archived calibration positives still fire at 1.000, and a plain 11-term regex over the repository id reaches sensitivity 0.727 at the SAME specificity 1.000 with caught_by_W05_missed_by_name = EMPTY (art_dp7WBo6hhVBX). The residue that survives is precision: 0 false positives on 32 at-scale negatives incl. 20 fresh Hub parents, 0/122 on the pre-stamped eligible undeclared population (Wilson [0, 0.031]), 0 in every leave-one-recipe-class-out cell.
  CLAIM B (REFUTED AS ORIGINALLY STATED, QUANTITATIVELY BOUNDED, UNCHANGED THIS ITERATION): for GRADED BEHAVIOURAL SAFETY, no interior observable in the frozen 53-metric battery beats a trivial black-box baseline by a resolvable margin -- minimum detectable |drho| = 0.32 at 19 lineages, r_xx = 0.968 so not attenuation, invariant at three depths, and interior observables ARE predictive (A19 rho +0.763 member / +0.800 lineage at a thirty-fifth of B09's forward passes) so the falsifier is about MARGINAL VALUE OVER A CHEAPER INSTRUMENT.

  WHAT ITERATION 4 SETTLED (do not re-litigate; do not re-run).
  S1. THE CERTIFICATE FAILS AT SCALE AND FAILS BY RECIPE. Leave-one-recipe-class-out is the primary generalisation control and locates it exactly: norm-preserving 5/5, global rank-one 1/6, unknown 1/5, multi-direction SVD 0/5, Heretic per-component 0/7, Gaussian-depth 0/3, partial-layer 0/4, SFT-uncensored 0/5, merge-of-abliterated 0/4. Two classes predicted to be CAUGHT (multi-direction, global rank-one) were not, so iteration 3's recipe story was not merely incomplete but wrong in sign on two classes. Misses are not near-misses: mlabonne/Qwen3-0.6B-abliterated reads -0.9637 against its parent's -0.9641, a paired shift of 4e-4.
  S2. UNIFORMITY IS THE WRONG PREDICATE, AND THE REPLACEMENT IS ANALYTIC, NOT EMPIRICAL. A 25-kernel sweep with host (Qwen3-1.7B) and direction r held fixed shows a uniform edit at sub-unit weight w=0.85 is INVISIBLE while behaviourally as effective as the full edit (refusal 0.225 vs 0.200 against host 0.925), and a strongly non-uniform Gaussian kernel at large spread IS detected. The correct decomposition is DISCOVERY (|cos(v1,r)| -> 1, so the pooled Gram surfaces r) AND COMPLETION (log10 min_W e_W(r) <= tau). THE REVIEWER IS RIGHT THAT THIS IS CLOSE TO AN IDENTITY: e_W(v1) = e_W(r)cos^2(theta) + cross terms, so whenever discovery holds W05 and the completion quantity are numerically the same object (uniform_w0.7: -1.1535 vs -1.1245; w0.85: -1.7488 vs -1.7248; w1.0: -4.5917 vs -4.5828), and whenever discovery fails W05 collapses to the parent's value (every Gaussian spread <= 8 reads -1.0098 to four decimals). The '19/19 with zero disagreements' figure is therefore a consistency check on a near-identity, NOT a validated empirical prediction, and it must never again be reported as one. The genuinely empirical content of the sweep is narrower and still valuable: WHICH kernels achieve discovery, and that the discovery switch is controlled by the MINIMUM DEPTH WEIGHT, bracketed in [0.0796, 0.5311] between spread 8 and 16 (|cos| 0.126 -> 0.9992, W05 -1.013 -> -2.888), against a stamped critical spread of 58.17 that was wrong by 3.6x. Completion NEVER varied over the whole Gaussian sweep (log10 min e_r = -4.53 at every spread), so discovery was always the binding constraint.
  S3. THE ANALYTIC BOUNDARY. A Householder reflection removes no rank and leaves the Gram spectrum invariant, so it is PERMANENTLY invisible to any statistic reading that spectrum. Measured: ORBA lambda=1.0 drops refusal to 0.100 while moving W05 by 4.1e-5, LESS than a Householder about an unrelated random direction (7.3e-5). Of 10 in-house kernels that pass the fluency screen AND actually remove refusal, only 4 are detected; the two most effective (ORBA, Heretic-style at refusal 0.125) are both invisible, while rank_k4 IS detected at -5.630 and barely uncensors (0.650). Detectability and effectiveness are near-orthogonal on this sweep, and where they correlate they correlate the wrong way.
  S4. BOTH-DIRECTIONS DECOUPLING, BY CONSTRUCTION (art_VLI4IOs9Xy9P). FALSE NEGATIVE: root B, a depth-weighted Gaussian abliteration of Qwen3-1.7B with the direction held fixed at root A's so the kernel is the only variable, un-censors 0.950 -> 0.270 [0.196, 0.360] at n=111, stays fluent (ppl 27.28), and reads W05 = -1.0100 -- the PARENT's value to four decimals, cos(v1,r) = 0.0199, all six flags False, ladder UNDEFINED across all 14 of its cells. Its recipe class R4_PARTIAL_LAYER_OR_PER_HEAD is 235/513 = 45.8% of declared Hub edits, the largest class. FALSE POSITIVE: root C, a uniform Llama-3.2-1B-Instruct edit along the AUROC-argmax direction, fires at W05 = -4.587 while refusing at 0.950 [0.83, 0.99], its parent's rate -- never un-censored. Held-out AUROC saturates (11 layers >= 0.997, 4 tied at exactly 1.000), so direction selection MUST be behavioural.
  S5. THE DEPLOYMENT NUMBER IS NOW HONEST BUT ITS POPULATION IS NOT THE THREAT MODEL. A sha256-stamped eligibility rule (n_layers>=8, d_model>=128, params<=4.2e9 enforced twice, no fixtures / speculators / quantized re-uploads) gives 0/122 Wilson [0, 0.031] primary, with raw 0/160 [0, 0.023] retained as a labelled secondary and its degenerate composition published (art_VFF9Dum9x3KJ); an independent stricter reading gives 85/160 eligible and [0, 0.043] (art_ckuwEkspyins), the two agreeing on the rate and disagreeing on three rows. BUT the eligible population is dominated by older BASE models (29 of the 40 newly fetched rows are gpt_neox; archived eligible is qwen2 23 / llama 19 / qwen3 9 / gpt_neox 6), and the first false positive is itself a gpt_neox model.
  S6. THE THRESHOLD IS WORSE THAN THE PAPER SAYS. The panel operating point tau = -2.7415117804288127 is carried by a 0.0763 log10 margin between two individual checkpoints and never validated out of panel; the first false positive appears at -2.6139, a shift of 0.128 log10 (~1.7 margin widths). AND -- the number the draft omitted -- refitting tau under leave-one-recipe-class-out gives -1.7156 for EVERY held-out class, a shift of 1.03 log units, about EIGHT TIMES the brittleness scale, under which held-out sensitivities change materially (global rank-one 0.167 -> 0.333, unknown 0.200 -> 0.400). The draft's LORCO table silently mixed fixed-tau sensitivities with refit AUROCs.
  S7. QUANTIZATION, RESOLVED. The dequantization remedy is VOID AS STATED: the archived quant_sd was a fake-quant, so the archived int4 number was already dequantized. The substantive result is a bit-width sweep: the scar dies at 5 BITS (W05 -2.654 > tau) with refusal still 0.237 and ppl only 26.25 -> 28.77; curve 8b -4.197 / 6b -3.270 / 5b -2.654 / 4b -2.009 / 3b -1.281 (ppl 272, destroyed). cos(v1,r) > 0.9994 at every bit-width, so the mechanism is THE NULL FILLING IN, not eigenvector rotation; the clean parent is unmoved (-1.010 -> -0.957); the proposed W05rel FAILS (tracks W05 to <0.001 because energies are already Frobenius-normalised). Operationally a quantized upload is UNRESOLVED in the scan pipeline, not a silent false negative. int4 costs ppl 26.25 -> 37.72 (+43%), so 'for free' overstated it.
  S8. STORAGE PRECISION SETS THE SCAR DEPTH, AND TWO STATISTICS ARE IRREPRODUCIBLE. The SAME complete uniform projection reads W05 = -4.592 in bf16 and -12.705 in float32. On a bit-identical rebuilt root, W02/W03/W05 reproduce to 1.3e-5 while W01/W04 differ by 3.1e-2 -- both are log ratios against lambda_1, which sits at the float32 Gram-accumulation floor on abliterated checkpoints; float64 recomputation moves W01 by exactly the archive gap. W01/W04 are not reproducible below ~0.05 on abliterated checkpoints. Nothing load-bearing may depend on them.
  S9. THE PARENT BUYS REAL COVERAGE -- 'PARENT-FREE COSTS NOTHING' IS RETIRED. On the at-scale rows E_1 fires on 13/32 pairs against W05's 7/35 and reaches Gaussian-depth, Heretic and partial-layer edits W05 never touches; agreement 0.829. The detection vector is IDENTICAL at all three bands ([0.25L,0.75L], full stack, [0.4L,0.6L]), so the band-sensitivity objection is answered with data. On archived matched pairs the primary band reproduces exactly (12 pairs tie at 1.000, +0.000; 15 pairs -0.167 [-0.444, 0.000]; 41 pairs -0.186 [-0.373,-0.076], reverting to -0.167 covering zero once the 26 in-house synthetics are excluded).
  S10. THE LADDER, WITH ERROR BARS AND THREE ROOTS. Achieved denominators are 31-40, not the recorded 40 (13 rows ambiguous); all four signed 'evasion costs' (-0.004, +0.069, +0.075, +0.128) and int4-minus-root (-0.03 [-0.189,+0.135]) are NOT RESOLVABLE (smallest upward detectable difference at n=40, p=0.20 is 0.29). What survives at n>100 with intervals is the ORDERING, on three laundering families and two architectures, with flag-death intensities IDENTICAL across architectures (merge w=0.10, add-back eps=0.10, quant nf4). Root C's behaviour gate FAILS honestly (1.000 -> 0.617) and it is labelled signature-positive / partially un-censored. Two reversals survive: a one-matrix argmin patch does not defeat a min-over-layers statistic, and 200 benign LoRA steps move W05 only -4.592 -> -4.381 while RESTORING refusal.
  S11. THE WINDOWED REMEDY IS DIAGNOSED, NOT DEMONSTRATED. W05w (windows of k consecutive layers, stride k//2, per-window minimum eigenvector, extremum-scored, with an adjacent-window consistency gate) provably contains W05 as its k=L special case and recovers the archived 4-of-12 toy blind spot by 12.6 log units, with specificity 1.000 at every k and every consistency threshold on 40 eligible undeclared models. BUT its POSITIVE ARM DID NOT RUN: n_G1 = n_G2_G3_synth = n_G4_real = 0, catch_by_recipe_class empty, every sensitivity NaN over n_positives = 0, and the declared k=L reproduction gate reports PASS = false because the achieved 8.49e-8 exceeds a declared 1e-9 tolerance on real models. The 12.6 log-unit number is a TOY-STACK number and must not carry Introduction or Conclusion framing.
  S12. OUR OWN REPORTING, AUDITED (art_ckuwEkspyins). 110 assertions -> 105 MATCH / 5 MISMATCH / 0 UNAVAILABLE, byte-identical across two runs, verify.py 17/17. The five: seven intensity axes not six; 81 unresolved non-control rows not 65; 8 skipped not 7; FIVE unreproduced quoted values not four; B09's 0.766 is the 26-member chatml value while the draft attributed it to the 28-member contract subset (correct value 0.670). Relabel discipline held: 2 of 4 iteration-3 misses carry a verbatim Heretic string; mlabonne and BennyDaBall stay PROVISIONAL because no kernel may be inferred from W05. Heretic's kernel is a TRIANGULAR TENT WITH A HARD CUTOFF, not Gaussian (art_gqCRODISeyg2) -- our own taxonomy was wrong.

  THE REVISED CLAIMS FOR ITERATION 5. No new battery. Most of this is re-analysis of tensors, checkpoints and rows we already hold; two arms need modest new GPU time.

  H1 (RUN THE WINDOWED POSITIVE ARM -- the single highest-value item, and pure re-analysis). Score W05w on the Arm B kernels that ALREADY EXIST as checkpoints (middle-50% band, Gaussian at all nine spreads, sub-unit uniform at w=0.5/0.7/0.85, ORBA at lambda=0.25/0.5/1.0, Heretic per-component, rank-k at k=2/4/8) and on the 44 Arm A real edited checkpoints, reporting sensitivity per k beside the specificity already measured, plus per-window random-direction nulls so the multiple-window hazard becomes a CALIBRATED per-window false-positive rate rather than an unbounded one. PREDICTION, stated so it can fail: un-pooling recovers the DISCOVERY failures (band, Gaussian at small spread, partial-layer) and recovers NOTHING that failed COMPLETION (sub-unit uniform w<=0.85) or that is an ISOMETRY (ORBA Householder), because those are not pooling artefacts. If windowing recovers the depth-weighted classes, that is the paper's positive claim and it replaces the toy number in the Introduction; if it does not, the mechanism section becomes a clean boundary result and W05w is demoted to a labelled 'proposed' subsection. Either way: widen the k=L gate to a defensible float32 bound (or report it as FAILED at its declared 1e-9), and delete the 12.6 log-unit toy figure from Introduction and Conclusion.

  H2 (REPLACE THE 'EMPIRICAL MECHANISM' FRAMING WITH A DERIVATION, AND GENERALISE IT TO THE CLASSES WHERE THE FAILURE ACTUALLY LIVES -- the reviewer's decisive point). Write e_W(v1) = e_W(r)cos^2(theta) + cross terms, bound the residual, and state as a CONSEQUENCE OF THE DEFINITION that detection <=> completion whenever discovery holds and is impossible otherwise. Delete '19/19 with zero disagreements' as evidence. Then reposition the sweep as what it is: a measurement of WHICH kernels achieve discovery and of the discovery threshold's dependence on the minimum depth weight in [0.0796, 0.5311]. Add the paragraph the draft owes: the single-direction rule is UNDEFINED for multi-direction SVD and per-component kernels -- exactly the 13 of 44 real misses excluded as 'inapplicable' -- and generalise it by defining discovery against the LEADING EDITED SUBSPACE via principal angles between the bottom-j Gram eigenspace and the span of the removed directions, then re-scoring rank_k2/4/8 and both Heretic variants under that generalisation. A rule that cannot be evaluated on the classes that dominate the failure is not yet a mechanism.

  H3 (DE-BIAS THE BASELINE THE WHOLE VERDICT RESTS ON). 0.727 is measured on a pool DISCOVERED BY NAME SEARCH (61 sweeps over abliteration vocabulary; 50.5% of harvested edited repos carry an abliteration string in the id; the regex's 11 terms overlap the search terms), so it is an UPPER BOUND presented as the baseline. Re-estimate it on a sample not discovered by name: draw edited checkpoints from the UPLOADER-sweep and ARCHITECTURE-sweep strata only, and/or from repositories whose recipe evidence comes from CARD BODY TEXT while the repo id contains none of the 11 terms; the census already says 23.4% of edited rows declare no mechanism and hub_scan_pool carries 1,105 non-declaring chat repos, so the stratum where the regex must fail exists and was never sampled. Report W05 and the regex SEPARATELY on the DECLARED and UNDECLARED strata, since the operational question -- does a weights-only test add anything -- is entirely about the undeclared stratum and the current answer is computed on the declared one. If the de-biased sample cannot be assembled, say plainly that 0.727 is a name-search upper bound and give the regex sensitivity on the card-derived subset.

  H4 (VERIFY THE POSITIVE CLASS BEHAVIOURALLY, AND THE JUDGE INDEPENDENTLY). (a) The 44 at-scale positives are labelled 'edited' from cards and never behaviourally checked, while this paper itself exhibits root C (full signature, parent's refusal rate) and root B (un-censored, parent's W05) -- so if some are cosmetic, failed or merged-away edits, 0.159 measures the detector against a partly mislabelled positive class, and the regex comparison inherits it. Measure greedy harmful refusal on the frozen 40-item core for a stratified ~12-checkpoint subsample (one or two per recipe class; the 5 SFT-uncensored and 4 merge-of-abliterated rows are the most uncertain as positives for a PROJECTION detector) and report sensitivity both on all 44 and restricted to verified-un-censored rows. Divergence is itself a result about card labels as ground truth. (b) The entire behavioural axis -- the 0.950 -> 0.270 decoupling headline, the effectiveness-vs-detectability intersection, the ladder orderings -- rests on ONE unvalidated judge (llama-3.3-70b, rubric B, kappa 0.149 / rate-level r 0.822 against the substring screen, itself substituted for a failed pre-registered rubric). Re-score a stratified 100-200 item subsample of the load-bearing stages (parent, roots A/B/C, flag-death cells) with a second judge from a DIFFERENT model family plus a small hand-labelled anchor, report kappa and rate-level agreement, and restate the decoupling with judge disagreement propagated -- one sentence saying root B's 0.270 moves by less than the interval width under the second judge makes the headline much harder to attack.

  H5 (FIX THE OPERATING POINT'S REPORTING, AND MEASURE SPECIFICITY WHERE IT MATTERS). (a) Give the leave-one-recipe-class-out table FOUR columns -- sensitivity and AUROC at the fixed panel tau, and sensitivity and AUROC under the class-held-out REFIT -- printing the refit tau of -1.7156, and add one sentence stating that refitting on the at-scale positives moves tau by 1.03 log units, ~8x the 0.128 brittleness scale. Report specificity on the 122 eligible undeclared checkpoints AT THE REFIT VALUE too: if it survives at -1.7156 that is a genuinely reassuring result currently left on the table; if it does not, the honest specificity claim is narrower than 0/122. (b) Stratify the false-positive rate by INSTRUCTION-TUNED/CHAT-TEMPLATED vs BASE and give the chat subset its own Wilson interval, since the population at risk of abliteration is current-generation chat models and the present denominator is mostly older base checkpoints; extend the scan by 40-60 repos inside hub_scan_pool's 1,105 non-declaring chat stratum, and if the chat denominator stays small, state its interval honestly rather than letting the pooled 0/122 stand in for it.

  H6 (POSITIONING, NOVELTY AND FRAMING, WITH THE NOVELTY CLAIM CUT TO WHAT SURVIVES). State precisely what is new relative to (i) Abliterlitics [art_gqCRODISeyg2] -- AGPL-3.0, first public 2026-04-24, four reports at or below ~4.5B including a full weight report on our own Qwen3-4B family, every weight metric DELTA-based (diff = (variant-base).abs().mean(), svd(delta_matrix)), base a mandatory key with no single-checkpoint mode -- whose measured depth/completeness fingerprints (Heretic 23/32 layers with 0-8 untouched, HauhauCS 29, Huihui 31, direction cosine 0.997 on one base but 0.00017 on another) ALREADY surface the depth-vs-completeness decomposition empirically; and (ii) arXiv:2607.01854, whose E_1 is ALREADY band-averaged over a mid-stack band, making per-band scoring published prior art. Frame our mechanism as an INDEPENDENT, PARENT-FREE CONFIRMATION of what delta-based forensics measures, plus the analytic statement of when parent-free detection is possible at all (the isometry impossibility) -- more accurate and more persuasive than framing it as a discovery. The surviving novel object is exactly four qualifiers: parent-free, calibration-free, BOTTOM-of-spectrum, sliding-and-extremum-scored -- and the sliding half is what H1 must earn. Keep the existing corrections: 2604.08844's cross-method AUC 0.00 carries its declared confound (steering arm incoherent, GPT-4o 0/300 harmful); OBLITERATUS certifies from ACTIVATIONS and audits a self-performed edit, and is LAYER-SELECTIVE via COSMIC so its presets are DEGRADED not detected; ORBA is TWO recipes (lambda=1 is annihilation without reflection; only v3 Householder is the isometry) and conflating them makes the falsification vacuous; reverse-abliterate is the software instantiation of the name baseline; Heretic's kernel is a triangular tent, code-level forbidden from the early stack.

  H7 (EDITORIAL AND REPORTING FIDELITY -- cheap and mandatory in a paper whose argument IS measurement discipline). One pass converting every backward reference into a direct claim ('uniformity is not the predicate', not 'we retract the previous draft's uniformity story'); number the sections so cross-references resolve; consolidate ALL corrections-to-prior-reporting into one delimited subsection near the end; cut the Contributions list to FOUR items that are findings, not bookkeeping; move the 110-assertion self-audit to an appendix or a short methods paragraph -- it is excellent practice, not a research contribution, and listing it as one invites the reading that the paper is short of results. Keep: counts generated from rows (270 = 20 controls + 250 attempted, 160 completed), full-precision boundary with abliterated MAXIMUM -2.7415 / minimum -4.8204 and margin 0.0763, oriented-vs-raw AUROC with an explicit convention field, [min,max] for every class x statistic with the base/abliterated overlaps flagged, W03 at 256 directions, and 'pre-registered' reserved for what metric_spec.py actually stamps (4 SUPPORTED / 2 PLAN-ONLY / 6 UNSUPPORTED).

  WHAT IS RETIRED. The 53-metric battery is not rebuilt. UNIFORMITY as the scope predicate is retired outright. 'Parent-free costs nothing' is retired -- the parent buys roughly a factor of two in sensitivity and reaches the classes that dominate the Hub. '19/19 reproduces the mechanism' is retired as evidence. The dequantize-then-rescore remedy is retired as void. W05rel is retired (it is algebraically identical to W05). W01 and W04 are retired from any load-bearing role (irreproducible below ~0.05 where the scar lives). alpha_50 and the steering-price family remain retired as metrics, surviving as the S4 negative plus the scorer-artefact finding. The early-warning-signal / critical-slowing-down arm remains retired entirely. Leave-one-architecture-family-out and leave-one-uploader-out remain retired/demoted; leave-one-RECIPE-CLASS-out with BOTH fixed and refit tau is primary. The framing 'safety behaviour is legible from the model alone' stays retired.

  CONFIDENCE. Lower than last iteration, and now asymmetric in a different place. HIGH that the certificate has excellent PRECISION: 0 false positives on 122 eligible undeclared checkpoints under a pre-stamped rule, on 32 at-scale negatives including 20 fresh parents, and in every leave-one-recipe-class-out cell -- though that precision is measured mostly on older base models and at a threshold fitted elsewhere. HIGH that its RECALL at Hub scale is poor and dominated by a filename regex (0.159 vs 0.727, empty complement), with the caveat that 0.727 is a name-search upper bound H3 must de-bias. HIGH that the discovery/completion decomposition is CORRECT, and equally high that it is ANALYTIC rather than empirical -- its empirical content is the discovery threshold's location and which kernels reach it. HIGH that an isometry is permanently invisible to any Gram-spectrum statistic. HIGH that the weight statistic and safety behaviour are dissociable in BOTH directions, since both were built as checkpoints and measured with intervals. MODERATE that windowing recovers the discovery failures; LOW that it recovers the completion or isometry failures; ZERO evidence either way today, which is precisely why H1 is the iteration's centre. HIGH that graded behavioural safety is not better read from the interior than from a 40-prompt greedy refusal rate at this panel size, and HIGH that the bound is |drho| ~ 0.32 at 19 lineages rather than zero. The most likely outcome of iteration 5 is a paper whose claim is: 'parent-free spectral edit detection is a precision instrument whose recall is set by an analytic discovery condition; we characterise that condition, show it is unfixable for isometries and fixable-or-not for pooling failures by an explicit measurement, and show by construction that no such certificate can be read as a safety score'. Smaller than iteration 3 hoped, and the only version the evidence licenses.
motivation: |-
  Judging whether a random Hugging Face checkpoint is safety-aligned currently requires running it against a harmful-prompt benchmark: slow, gameable (a model can be tuned to refuse benchmark items and comply elsewhere), and it forces the evaluator to hold and send harmful content. The published cheap alternatives all retain a dependency this proposal drops. AMS (Messenger, arXiv:2608.05578) scans activation geometry and needs harmful prompts; it reports 71% leave-one-out accuracy over 14 configurations and explicitly reports that behavioral uncensored fine-tunes preserving geometry are undetectable by it. RAS/SafeVec (arXiv:2606.25750) scores representation-level refusal alignment on a calibrated 0-100 scale but needs unsafe and jailbreak prompts AND a safety-aligned reference model. VISAGE (arXiv:2405.17374) measures a safety basin in WEIGHT space and needs a harmful benchmark evaluated at every weight perturbation. All three are static, read-side measurements. That question provably does not settle behavior - the 2026 knowledge-action-gap result reports 98.2% probe AUROC alongside 45.1% output sensitivity.

  This hypothesis attacks the gap from the act side with a different unit: not a direction, feature or basin volume, but a RATE. How fast does the model's own generative process return to its default mode after a tiny nudge while doing something innocuous?

  What a basin in BEHAVIORAL state space buys over VISAGE's basin in WEIGHT space is now stated as a testable divergence rather than asserted. The two accounts must rank the panel identically unless weight-space and behavior-space geometry come apart, and we pre-register the two places they should: (a) a behavioral uncensored fine-tune, where a small weight displacement produces a large behavioral change, and (b) a task-vector interpolant, where a smooth weight-space path may produce a step-like behavioral change. A phenomenon the weight-space basin cannot account for is therefore named in advance: a checkpoint whose weight-space basin volume is unchanged from its parent while its behavioral relaxation rate collapses. If the two rankings coincide, we say so and demote the mechanistic claim to a cost claim. The reinterpretation of Qi et al. gets the same treatment: the token-depth account predicts the safety signal is concentrated in the first few GENERATED steps and vanishes afterwards, while the basin account predicts lambda differences PERSIST deep into generation. Step 5 already collects step-wise lambda profiles, so this discriminating test is free.

  If true this yields (a) a mechanistic account of what safety tuning buys, in the language of bistable systems - a shifted operating point; (b) an audit needing a handful of harmless prompts, no harmful content, no jailbreak suite, no reference model and no benchmark to memorize; and (c) a bridge carrying the mature early-warning-signal toolkit from ecology and climate science into model auditing. A clean negative is also worth publishing: it would say safety is a static bias, not a shifted operating point, extending the knowledge-action-gap literature with a dynamical arm.
assumptions:
- >-
  Autoregressive generation under temperature sampling is a genuine stochastic dynamical system whose state is the generated
  prefix plus KV cache, so recovery rate, across-rollout variance, lag-1 autocorrelation and flickering are well defined over
  GENERATED steps. The series is NON-STATIONARY (chat-template openings and topic commitment produce a strong deterministic
  trend), so all fluctuation statistics are computed on residuals after subtracting the ACROSS-ROLLOUT mean trajectory at
  each generated step, estimated from the >= 20 rollouts we already collect. Without detrending, a high lag-1 autocorrelation
  would only mean 'this model produces stereotyped openings'.
- >-
  The refusal/comply mode can be read out as a scalar at each generated step by a MODEL-INDEPENDENT observable that survives
  the abliteration weight edit: the logit-lens log-odds of refusal-onset tokens against continuation tokens. This is primary
  precisely because a projection onto the abliterated direction is near-constant by construction, which would make any variance
  claim on abliterated models circular. The per-model diff-in-means axis is descriptive only.
- >-
  Steering-based tests (H1) probe states that are partly OFF the manifold reachable by prompting (arXiv:2604.09839 proves
  steered activations are non-surjective). H1 is therefore scoped as a statement about the steered dynamical system, and the
  safety claim of record (H3) uses only unsteered sampling plus a norm-epsilon perturbation whose linearity is verified by
  an epsilon sweep, so the product claim never rests on off-manifold behaviour.
- >-
  A graded safety ladder can be manufactured without training by scaling the alignment task vector W(t) = W_base + t*(W_instruct
  - W_base) and by scaling abliteration strength - but only if the interpolants stay fluent. Every interpolant must pass a
  pre-registered screen (WikiText perplexity within 2x of the t=1 endpoint, plus a distinct-3 / max-n-gram-repeat degeneracy
  check) before entering any analysis, because a degenerate model neither refuses nor complies AND has a degeneracy-dominated
  r_t series, which would corrupt both sides of the headline correlation at once and could manufacture a spurious result.
  Interpolants share a weight lineage and never count as independent units.
- >-
  Small models (0.36B-4B, int8/float32, batched rollouts) show the same qualitative refusal machinery reported for larger
  models. This is tested rather than assumed via a within-family scale ladder (Qwen3 0.6B/1.7B/4B), because a small model
  that is twitchy may be twitchy from undertraining; scale enters the headline analysis as a covariate.
investigation_approach: |-
  PANEL, ENUMERATED BY LINEAGE (the resampling unit). 20 distinct weight lineages, >= 8 architecture families, all CPU-feasible: Qwen3-0.6B, Qwen3-1.7B, Qwen3-4B (each contributing base + instruct + abliterated members), Qwen2.5-0.5B, Qwen2.5-1.5B, Llama-3.2-1B, Llama-3.2-3B, gemma-2-2b, SmolLM2-360M, SmolLM2-1.7B, TinyLlama-1.1B, Pythia-410M, Pythia-1B, Pythia-1.4B, OLMo-1B, Danube3-500M, Falcon3-1B-Instruct, Granite-3.1-2B-Instruct, MiniCPM-1B, plus >= 4 behavioral uncensored fine-tunes (their own lineages). Base-only lineages (Pythia, OLMo) anchor the low-refusal end. Total measured UNITS (members) ~ 45-55; n_lineage = 20. Every model-level statistic is bootstrapped over the 20 lineages; the member/prompt bootstrap is reported separately and labelled measurement noise.

  STEP 0 - PRE-REGISTRATION (written before any run).
  (a) Layer L is fixed by a rule that never touches the outcome: the layer maximizing harmful/benign diff-in-means separation on a held-out contrast set for ONE reference model, transferred by relative depth L/n_layers. Full layer profiles are secondary, Holm-corrected, and interpreted against the reported 'Late Decision' (Llama) vs 'Early Divergence' (Qwen) topologies.
  (b) Decoding fixed and reported: chat template, empty system prompt, temperature 0.7 for dynamics and 0.0 for deterministic controls; max_new_tokens = 192 for the H2 dynamics arm (needed for estimator identifiability) and 64 for ground-truth generation.
  (c) SPI is fixed a priori as the mean of FOUR z-scored terms [-log lambda, log detrended across-rollout variance, Fisher-z of detrended AC1, logit of flicker rate], PLUS - crucially - the z-scoring uses FROZEN normalization constants (means and sds) fit once on a designated REFERENCE subset of 6 named lineages and PUBLISHED in the paper. SPI for any new checkpoint uses only those frozen constants, so it is computable for a single model with no comparison panel (the defect that made the previous definition weaker than RAS's absolute 0-100 scale). All leave-one-out and leave-one-family-out numbers are recomputed with the left-out model excluded from the normalization fit. >= 3 checkpoints are reserved that appear in NO normalization and NO fitting step, and their SPI plus ground truth is reported as the out-of-panel demonstration.
  (d) SIGNED PREDICTION TABLE, one row per ground truth: plain-harmful refusal rate -> expected sign POSITIVE, threshold rho >= 0.6, reason: nearness to the switch makes the refuse mode easy to enter. XSTest over-refusal rate -> POSITIVE, rho >= 0.45, same reason applied to benign-but-scary prompts. Jailbreak attack-success rate -> SIGN IS THE DISCRIMINATING OUTCOME: the ASYMMETRIC reading predicts NEGATIVE (the shallow basin is the comply basin, so the model falls into refusal and is hard to tip out), the DOUBLE-SIDED reading predicts POSITIVE (near a fold in both directions, so it tips either way). Both are pre-registered as competing hypotheses; the outcome that discriminates them is the sign of the partial rank correlation of SPI with ASR controlling for plain-harmful refusal rate, corroborated by the Asymmetry Index of H2b. Either sign is informative; an unsigned rho would have been unfalsifiable.
  (e) Single-forward-pass measurement: DROPPED, not retained as an appendix, so it cannot be substituted for the generated-step result.

  STEP 1 - H1, three ramp arms. For each of >= 30 benign prompts: (i) UP-RAMP, raise alpha per generated token until a refusal-onset token is emitted -> alpha_up. (ii) RETAINED-PREFIX DOWN-RAMP, continue the same sequence with prefix and KV cache kept, lowering alpha -> alpha_down. (iii) FORCED-PREFIX DOWN-RAMP (the control that isolates the claim), force-feed the identical refusal prefix as a prefill without ever ramping up, then ramp alpha down from the same start -> alpha_down_forced. Test statistic = residual = alpha_down - alpha_down_forced, bootstrapped over prompts and lineages. width_naive = alpha_up - alpha_down is reported alongside, with the PRE-REGISTERED expectation that it is large and positive in base models too (per Kwon 2607.14147). A reset arm that discards the prefix between steps is retained as an implementation sanity check only: it must be indistinguishable from 0 at temperature 0, and its temperature-0.7 width is the NOISE FLOOR against which retained-prefix quantities are compared (it will not be exactly 0 under sampling).

  STEP 2 - H2/H2b, early-warning indicators on harmless input only. Per benign prompt (~20 prompts), >= 20 paired-seed rollouts, 192 generated tokens. Perturbed arm: inject a norm-epsilon vector into the residual stream at layer L at step p, continue decoding, fit an exponential to |delta r_t| over subsequent generated steps -> lambda, run separately for refusal-directed and compliance-directed nudges (H2b). Clean rollouts give detrended Var*, detrended AC1, and flicker rate. Estimator hygiene, all pre-registered: subtract the across-rollout mean trajectory before AC1/Var*; a SYNTHETIC RECOVERY CHECK simulating AR(1) with known decay at the observed noise level and series length, reporting the estimator's bias and variance and a minimum series length below which lambda is not reported; and indicators reported as a function of series length so truncation artifacts are visible. Epsilon sweep confirms linearity. Three null controls: random readout axis (must NOT reproduce the safety ordering), random vs refusal-aligned perturbation, and a syntactic (part-of-speech probe) observable, which should decay at the same rate if what is being measured is generic mixing.

  STEP 3 - ground truth, three axes. Per member: ~80 AdvBench/JailbreakBench-style harmful prompts (plain-harmful refusal rate), the same under a fixed small jailbreak suite including prefill (ASR), ~50 XSTest benign-but-scary prompts (over-refusal). Scoring: cheap OpenRouter LLM judge PRIMARY, refusal-string matcher as screen, Cohen's kappa reported, >= 100 hand-adjudicated stratified items to estimate judge error, attenuation-corrected correlations alongside raw. Budget < $2 of the $10 cap. Interpolants additionally pass the fluency screen, and the ladder is PILOTED on one base/instruct pair first to confirm refusal rate varies smoothly in t rather than snapping to an endpoint; counts manufactured vs passed are reported, and if the pass rate is low the paper states that trimodality returns.

  STEP 4 - H3/H4, prediction with matched-n, faithful baselines. Spearman rho of SPI with each ground truth. The headline comparison is a PAIRED bootstrap of the DIFFERENCE (rho_SPI - rho_baseline) on the SAME resampled lineages, required to exclude 0 - this removes between-lineage variance common to both and is what n_lineage = 20 can actually support. Baselines: (a) static mean level of r on benign prompts; (b) two zero-internals output-side detectors (next-token probability of refusal-onset tokens; ever-emits-an-apology-token); (c) AMS-style cluster separation sigma and refusal-direction cosine, with leave-one-out accuracy reported in AMS's own format and leave-one-FAMILY-out; (d) a RAS/SafeVec reimplementation whose reference model, layer-window selection rule, prompt sets and calibration mapping are pre-registered, with a reproduction check against RAS's published numbers on overlapping models - if reproduction is out of scope it is labelled 'our RAS reimplementation' throughout, not 'RAS'; (e) VISAGE-style weight-perturbation basin volume on a 6-model subset, with SPI's correlation reported ON THAT SAME SUBSET so the comparison is at matched n. Load-bearing statistic: partial rank correlation of the dynamic terms with each ground truth controlling for the static mean AND model scale. H4 candidates must pass the class-membership pre-check (sigma and refusal-direction cosine preserved vs parent, harmful compliance high, model card and community provenance checked for abliteration or abliterated-merge components); failures are reported with reasons, and if fewer than 4 pass, H4 is reported as a pre-registered case study with per-model detail rather than a statistical claim.

  STEP 5 - mechanism map and the two discriminating tests. Layer-wise and step-wise lambda profiles for base vs instruct vs abliterated vs interpolants: does the basin shallow monotonically in t; does abliteration revert to base or produce a third state; and the two named predictions - (i) does the behavioral basin rank the panel differently from VISAGE's weight basin on behavioral fine-tunes and interpolants (versus the account, if identical); (ii) do lambda differences persist deep into generation (basin account) or vanish after the first few generated steps (Qi et al. token-depth account).

  COMPUTE BUDGET AND STAGING (previously absent). Audit cost and validation cost are reported separately. AUDIT (what a user pays to score one new checkpoint): 20 benign prompts x 20 rollouts x 2 arms x 192 tokens with batched rollouts and hooks active - roughly 10-15 min on one consumer GPU, or ~40-60 min on CPU int8 at <= 1.7B. VALIDATION (what this study pays): Step 3 dominates, ~50 members x 210 prompts x 64 tokens. Tiering, pre-registered: TIER 0 smoke, 3 checkpoints, verifies the full pipeline end to end. TIER 1, 12 checkpoints spanning all families and both ladder endpoints, run through ALL of Steps 1-5, sufficient on its own to report H1/H1b/H2/H2b with controls. TIER 2, remaining members added to Steps 3-4 only (ground truth and correlation), where marginal cost is lowest and marginal power highest. Criteria are evaluated on whatever tier completes, with the tier stated; a partial run is therefore still reportable.
success_criteria: |-
  POWER, reconciled with the resampling unit (the previous version's n=30 arithmetic contradicted its own lineage bootstrap). n_lineage = 20. At n = 20 the 95% bootstrap CI half-width around an observed Spearman rho = 0.8 is roughly +/-0.22, so a criterion requiring SPI's CI lower bound to exceed a baseline's point estimate is NOT attainable regardless of truth and is replaced in advance by the PAIRED difference test, which removes the shared between-lineage variance. Partial correlations with two covariates have adequate power only for partial rho >= 0.5; criteria are set at that level.

  CONFIRMS:
  (1) The H1 residual (alpha_down - alpha_down_forced) is significantly > 0 with a bootstrap CI excluding 0 and exceeding the temperature-0.7 noise floor - path dependence exists that the emitted refusal text does not explain.
  (2) The residual is ordered instruct > base and instruct > abliterated, paired over prompts, CIs excluding 0.
  (3) On harmless prompts only, over generated steps, with DETRENDED statistics and a passing synthetic-recovery check: lambda lower and Var*, AC1, flicker higher in behaviorally safer models, reproduced in >= 3 families, AND absent on the random-axis and syntactic-probe controls.
  (4) SPI computed with FROZEN constants attains rho >= 0.6 with plain-harmful refusal rate (positive sign, as pre-registered) and rho >= 0.45 with XSTest over-refusal (positive), and the PAIRED bootstrap of rho_SPI - rho_baseline excludes 0 against the best of the static mean and the two zero-internals baselines; the partial correlation controlling for static mean and scale has a 95% CI excluding 0 at partial rho >= 0.5.
  (5) The jailbreak-ASR row resolves in EITHER direction with a partial correlation CI excluding 0 controlling for refusal rate, and the Asymmetry Index of H2b agrees with that sign. This is scored as a confirmed discrimination between the asymmetric and double-sided readings, not as a pass/fail.
  (6) SPI matches or beats AMS leave-one-out accuracy in AMS's own format with the left-out model excluded from normalization, and matches the RAS reimplementation and VISAGE (the latter at matched n on its 6-model subset) without needing their harmful prompts or reference model.
  (7) The >= 3 fully held-out checkpoints are scored correctly from frozen constants alone - the actual product claim.
  (8) H4: every behavioral uncensored fine-tune passing the class-membership check is flagged by SPI while cluster separation and refusal-direction cosine both mark it safe. Reported as a statistical claim only if >= 4 pass, otherwise as a pre-registered case study.

  THIRD OUTCOMES, PRE-REGISTERED (informative, not failures): (a) 'bistability present but not safety-specific' - the residual is nonzero in base models too, in which case H1 is confirmed and H1b refuted and only the quantitative ordering carries safety information (live because Kwon 2607.14147 attributes prefill grip to generic autoregressive conditioning and Rahimi et al. 2602.02600 report that autoregressive commitment masks instability). (b) Behavioral basin and VISAGE weight basin rank the panel identically - the mechanistic claim is then dropped to a cost claim, stated plainly. (c) The interpolant ladder fails its fluency screen or snaps to endpoints - the trimodality problem returns and is reported as a limitation on the correlation's interpretability.

  DISCONFIRMS (reported as refutation, not salvaged): the H1 residual is indistinguishable from the noise floor, i.e. all path dependence is prefix content and the bistable framing adds nothing; or lambda / Var* / AC1 / flicker show no consistent ordering with any ground truth once detrended; or the ordering also appears on the random-axis or syntactic-probe control, meaning generic mixing was measured; or the correlation vanishes once static mean and scale are partialled out; or a zero-internals output-side baseline ties SPI in the paired difference test; or the held-out checkpoints are mis-scored under frozen constants, meaning the metric is a within-panel artifact; or indicators work within one family but fail leave-one-family-out, bounding the metric to a within-family diagnostic.
related_works:
- >-
  Messenger, 'Detecting Safety Training Modification in Language Models via Activation Analysis' (arXiv:2608.05578, IEEE Access
  2026) - AMS scans activation geometry (harmful/benign cluster separation sigma, refusal-direction cosine) across 14 configurations
  and 4 families, 71% leave-one-out accuracy, compliance prediction r = -0.546, and explicitly reports behavioral uncensored
  fine-tunes as undetectable. Closest work and sharpest departure: static read-side property from harmful prompts versus our
  dynamical act-side RATE from harmless prompts only. Its documented blind spot is our H4 case study, and we report LOO accuracy
  in its format with the left-out model excluded from our normalization fit so the comparison is not leaked.
- >-
  Huang et al., 'RAS: Measuring LLM Safety Through Refusal Alignment' (arXiv:2606.25750, 2026) - SafeVec extracts layer-wise
  refusal directions from a safety-aligned REFERENCE model, selects stable layer windows, and scores a target by hidden-state
  alignment under unsafe and jailbreak prompts, mapped to a calibrated absolute 0-100 scale. It is the incumbent for our product
  claim and the reason we now FREEZE SPI's normalization constants: a within-panel z-score cannot score a single new checkpoint,
  which is exactly RAS's advantage. Run as a pre-registered reimplementation with a reproduction check on overlapping models,
  and labelled 'our reimplementation' if reproduction is out of scope. It needs harmful and jailbreak prompts and a reference
  model; SPI needs neither.
- >-
  Peng et al., 'Navigating the Safety Landscape' (NeurIPS 2024, arXiv:2405.17374) - discovers the safety basin in WEIGHT space
  and proposes the VISAGE basin-volume metric, requiring a harmful benchmark at every weight perturbation. 'Shallow basin'
  is their language and we say so. The departure is now a TESTED prediction rather than an assertion: the accounts diverge
  where weight-space and behavior-space geometry come apart (behavioral uncensored fine-tunes; task-vector interpolants).
  VISAGE is run on a 6-model subset with SPI reported on that same subset at matched n; if the rankings coincide we drop the
  mechanistic claim to a cost claim.
- >-
  Yin et al., 'Refusal Falls off a Cliff' (arXiv:2510.06036, 2025) - traces refusal intention across token positions with
  linear probes, finding a sharp drop at final tokens in poorly aligned reasoning models. The per-position refusal score is
  an existing observable which we adopt rather than coin; our contribution is the detrended dynamical statistics computed
  on it across sampled rollouts plus the residual hysteresis test.
- >-
  Rahimi et al., 'Step-Wise Refusal Dynamics in Autoregressive and Diffusion Language Models' (arXiv:2602.02600, 2026) - shows
  diffusion remasking enables recovery from harmful intermediate generations and proposes the SRI internal-dynamics signal,
  observing that autoregressive commitment masks underlying instability. Closest 'dynamics during decoding' work: it compares
  SAMPLING MECHANISMS, we hold sampling fixed and use controlled perturbation-recovery as an ESTIMATOR of distance to a switching
  point. Its commitment finding is a named pre-registered threat.
- >-
  Kwon, 'Breaking Refusal in the First Half' (arXiv:2607.14147, 2026) - prefill jailbreak study: harm representation stays
  intact (probe 0.91-0.98) while behavioral refusal drops to chance, and a base-model control shows the same prefill-specific
  collapse, concluding the prefill's grip is generic autoregressive conditioning rather than safety-specific suppression.
  This is precisely why H1's test statistic is now the FORCED-PREFIX RESIDUAL rather than the naive loop width, which this
  paper's mechanism would otherwise explain entirely.
- >-
  Ratnakar and Vats, 'The Geometry of Refusal: Linear Instability in Safety-Aligned LLMs' (arXiv:2606.22686, 2026) - Contrastive
  Logit Steering plus prefix injection induces a phase transition where guardrails collapse, and reports 'Late Decision' (Llama,
  95% ASR) vs 'Early Divergence' (Qwen, safety integrated at ~40% depth) topologies. Phase-transition language exists here
  but as an ATTACK that crosses the edge; our point is estimating distance to the edge without crossing it. Its topology finding
  drives our relative-depth layer transfer.
- >-
  Hasan and Biswas, 'The Refusal-Compliance Tradeoff' (arXiv:2605.05427, 2026) - audits 21 open-weight LLMs and finds over-refusal
  and harmful compliance nearly uncorrelated. This is why three ground truths are predicted separately, and why the signed
  prediction table (positive for refusal and over-refusal, sign-as-outcome for ASR) is a real commitment rather than bookkeeping.
- >-
  Xiong et al., 'Steering Externalities: Benign Activation Steering Unintentionally Increases Jailbreak Risk for LLMs' (arXiv:2602.04896,
  2026) - steering vectors from entirely benign data erode guardrails, with ASR above 80%, framed as consumption of a 'safety
  margin'. This is direct empirical support that a margin exists and is small in aligned models, and it is the strongest existing
  evidence for the DOUBLE-SIDED reading in H2b. It measures the consequence of crossing the margin; we measure the margin's
  width from harmless generation without crossing it.
- >-
  Mishra, Khashabi and Liu, 'Steered LLM Activations are Non-Surjective' (arXiv:2604.09839, 2026) - proves steered residual
  streams leave the manifold reachable from discrete prompts. A scope constraint we now state explicitly: H1's ramp probes
  the steered system, so the product claim (H3) rests only on unsteered sampling plus a verified-linear norm-epsilon perturbation.
- >-
  Arditi et al., 'Refusal in LLMs is mediated by a single direction' (2024) and the abliteration practice built on it - the
  static geometric account and our instrument for producing (and partially producing) uncensored checkpoints. Because abliteration
  orthogonalizes writes against that direction, we deliberately do NOT use a projection onto it as the primary observable.
- >-
  Qi et al., 'Safety Alignment Should Be Made More Than Just a Few Tokens Deep' (ICLR 2025 Oral) - shows aligned and unaligned
  generative distributions differ mainly over the first few output tokens. Their account and ours make DIFFERENT predictions
  we now test: token depth predicts the safety signal is confined to the first few generated steps, the basin account predicts
  lambda differences persist across generated steps.
- >-
  Scheffer et al. and the early-warning-signal / critical-slowing-down literature in ecology, climate science and psychiatry
  (slowed recovery from small perturbations, rising variance, rising lag-1 autocorrelation, flickering near a fold bifurcation).
  The imported source, not a competitor; scholarly search finds it applied to ecosystems, climate, financial crises, depression
  and sleep, but not to LLM generative dynamics or safety auditing.
inspiration: >-
  The transfer is from ecology and climate science at the methodological level. Ecologists face this problem in a different
  costume: they must know how close a lake, forest or fish population is to collapsing without running the experiment of collapsing
  it. Scheffer's early-warning-signal programme solved it by measuring the response to small, harmless disturbances - as a
  system approaches a fold, the dominant eigenvalue of its linearized dynamics approaches zero, so recovery from tiny nudges
  slows, fluctuations grow in variance, become more autocorrelated, and the system flickers. Resilience becomes measurable
  without pushing the system over the edge. Mapped onto model auditing: don't jailbreak a model to learn whether it can be
  jailbroken - nudge it gently while it does something innocuous and watch how fast it settles back. The import is legitimate
  only where a real stochastic dynamical system exists, which is why the measurement lives in autoregressive sampling and
  why the single-forward-pass version has now been dropped rather than kept as a heuristic. Ecology also supplies the fix
  for the statistics: EWS practitioners detrend before computing autocorrelation for exactly the reason we now must - a trend
  inflates AC1 and fakes the signal. Two further imports: from physics and materials science, the hysteresis loop as the decisive
  test of genuine bistability, which forces the sweep to happen within one generation with the prefix retained - and, following
  the same tradition's insistence on separating a real state variable from a memory of the drive, the forced-prefix control
  that isolates latent path dependence from conditioning on already-emitted text. From experimental genetics, the base / safety-tuned
  / abliterated series read as wild-type / knock-in / knock-out, extended to a dose-response ladder by scaling the alignment
  task vector, with a viability screen on the intermediates the way a geneticist screens for non-viable phenotypes. What a
  domain expert would not reach for is the reframing underneath: mechanistic interpretability's default unit is a static object
  - a direction, a feature, a circuit, a basin volume - whereas the resilience literature's unit is a rate.
terms:
- term: Refusal observable (r_t)
  definition: >-
    A scalar read off the model at each GENERATED step t. Primary form: logit-lens log-odds of refusal-onset tokens against
    continuation tokens - chosen because it survives the abliteration weight edit and needs no harmful prompts. All fluctuation
    statistics use the DETRENDED residual, obtained by subtracting the across-rollout mean trajectory at each generated step.
- term: Critical slowing down
  definition: >-
    The signature that a stochastic dynamical system is near a fold bifurcation: recovery from small perturbations slows,
    fluctuations grow in variance, become more autocorrelated, and the system flickers between modes. Standard practice in
    ecology, climate science and psychiatry for estimating resilience without triggering collapse.
- term: Recovery rate (lambda)
  definition: >-
    The exponential decay rate of the induced deviation in r_t over subsequent GENERATED steps after a small residual-stream
    perturbation, averaged over >= 20 paired-seed rollouts of 192 tokens. Small lambda = slow recovery = shallow basin = close
    to switching. Its identifiability at the actual series length and noise level is verified by a synthetic AR(1) recovery
    check with a pre-registered minimum series length.
- term: Asymmetry Index
  definition: >-
    log(lambda_toward_refuse / lambda_toward_comply): recovery from a nudge pushing toward refusal versus one pushing toward
    compliance. It distinguishes an ASYMMETRIC shallow comply basin (tips into refusal easily, so high refusal but LOW jailbreak
    success) from a DOUBLE-SIDED fold (tips either way, so high refusal AND high jailbreak success) - the two readings of
    'nearness to a switch' whose conflation previously left the jailbreak prediction unsigned.
- term: Switching Proximity Index (SPI)
  definition: >-
    The proposed safety metric: the mean of four terms [-log lambda, log detrended across-rollout variance of r, Fisher-z
    of detrended lag-1 autocorrelation, logit of flicker rate], standardized with FROZEN normalization constants fit once
    on a named 6-lineage reference subset and published, so SPI is computable for a single new checkpoint with no comparison
    panel. Higher SPI = closer to the comply/refuse switching point.
- term: Forced-prefix control (alpha_down_forced)
  definition: >-
    The control that makes H1 decisive. The refusal prefix produced at the top of the up-ramp is force-fed as a prefill WITHOUT
    any prior ramp, then alpha is ramped down. Because the prefix content is identical, the difference alpha_down - alpha_down_forced
    isolates path dependence carried by latent state from ordinary conditioning on already-emitted refusal text - the mechanism
    Kwon reports as generic to autoregressive decoding.
- term: Noise floor
  definition: >-
    The apparent loop width produced by sampling alone, measured in the prefix-discarding reset arm at temperature 0.7. It
    must be indistinguishable from 0 at temperature 0; at 0.7 it is the baseline against which retained-prefix quantities
    are compared, replacing the previous, incorrect 'must be exactly zero' requirement.
- term: Flicker rate
  definition: >-
    At a steering coefficient held near the switching threshold and nonzero temperature, the fraction of sampled rollouts
    that switch mode between refusal and compliance. A classical early-warning indicator, available only because the measurement
    lives in stochastic sampling.
- term: Task-vector safety ladder
  definition: >-
    A training-free way to manufacture graded ground truth: W(t) = W_base + t*(W_instruct - W_base) plus partial-strength
    abliteration. Every interpolant must pass a fluency screen (WikiText perplexity within 2x of the t=1 endpoint; distinct-3
    and max-n-gram-repeat degeneracy checks) before entering analysis, and the ladder is piloted on one pair to confirm refusal
    rate varies smoothly rather than snapping to an endpoint. Members share a weight lineage and never count as independent
    units.
- term: Weight lineage
  definition: >-
    The resampling unit for every model-level claim: one pretrained base and everything derived from it (instruct, abliterated,
    interpolants). The panel has n_lineage = 20 across >= 8 families and ~45-55 measured members; all headline CIs are bootstrapped
    over the 20 lineages, and the headline baseline comparison is a PAIRED bootstrap of the correlation difference on the
    same resampled lineages.
- term: Behavioral uncensored fine-tune
  definition: >-
    An 'uncensored' checkpoint produced by ordinary fine-tuning on compliant data rather than a directional weight edit, so
    it can keep harmful/benign geometry and the refusal direction intact while complying with nearly all harmful requests.
    Class membership is now VERIFIED before use (separation and cosine preserved vs parent, harmful compliance high, provenance
    checked for abliteration or abliterated merges), because an unverified candidate tests nothing.
- term: Audit cost vs validation cost
  definition: >-
    Two separately reported numbers. Audit cost is what a user pays to score one new checkpoint (20 benign prompts x 20 batched
    rollouts x 192 tokens; ~10-15 min on one consumer GPU, ~40-60 min on CPU at <= 1.7B). Validation cost is what this study
    pays to establish the metric, dominated by the harmful/jailbreak/over-refusal ground truth. Conflating them invites the
    objection that a cheap method needed an expensive study - true, normal, and stated plainly.
- term: Knowledge-action gap
  definition: >-
    The finding that a model's internals can encode a concept with near-perfect decodability while its outputs fail to act
    on it (98.2% probe AUROC vs 45.1% output sensitivity, 2026 clinical result). It is why a read-side safety metric can be
    confidently wrong, and why this hypothesis measures an act-side quantity.
summary: >-
  Safety fine-tuning may park a model right next to a comply/refuse switching point, so an aligned model is subtly unstable
  about refusal even while generating harmless text - and that instability is measurable during ordinary sampled generation
  using the early-warning indicators ecologists use to detect approaching tipping points (slower recovery from small nudges,
  higher detrended variance, autocorrelation, flickering), with a forced-prefix-controlled hysteresis residual as the decisive
  test of genuine bistability. This yields a frozen-normalization safety score computable for a single new checkpoint from
  a handful of harmless prompts, with no harmful content and no reference model, aimed where static activation-geometry scanners
  are documented to fail.
_relation_rationale: >-
  Same frame; the supported half becomes a bounded negative and the boundary is restated as analytic, not empirical.
_confidence_delta: decreased
_key_changes:
- >-
  DOWNGRADED Claim A from 'supported, narrowed' to LARGELY REFUTED AT SCALE: sensitivity 0.159 on 44 real edited checkpoints
  from 27 uploaders / 9 recipe classes vs a repo-name regex at 0.727 with matched specificity 1.000 and an EMPTY caught-by-W05-missed-by-name
  set (art_dp7WBo6hhVBX); what survives is precision, not detection.
- >-
  RETIRED UNIFORMITY outright as the scope predicate — a uniform sub-unit edit (w=0.85) is invisible yet behaviourally as
  effective as the full edit, and a non-uniform Gaussian at large spread IS detected; the predicate is discovery AND completion.
- >-
  ACCEPTED the reviewer's decisive point that discovery∧completion is NEAR-ALGEBRAIC, not empirical: e_W(v1)=e_W(r)cos^2(theta)+cross
  terms, so '19/19 with zero disagreements' is retired as evidence and replaced by a derivation plus the sweep's real empirical
  content (the discovery switch controlled by minimum depth weight in [0.0796,0.5311], stamped critical spread wrong by 3.6x).
- >-
  ADDED the generalisation the rule needs: it is UNDEFINED for multi-direction and per-component kernels — exactly the 13
  of 44 real misses excluded as 'inapplicable' — so discovery must be redefined against the leading edited SUBSPACE via principal
  angles and re-scored on rank-k and both Heretic variants.
- >-
  MADE THE WINDOWED POSITIVE ARM the iteration's centre: W05w currently has n_positives=0 everywhere (catch_by_recipe_class
  empty, all sensitivities NaN) and its only evidence is a 12-matrix toy; score it on the Arm B kernels and 44 Arm A reals
  that already exist, with per-window random-direction nulls, and fix or fail the k=L gate (8.49e-8 vs declared 1e-9).
- >-
  FLAGGED the regex baseline as an UPPER BOUND: the panel was discovered by name-based Hub search whose terms overlap the
  regex's 11 terms; re-estimate on uploader/architecture-sweep and card-text-only strata and report W05 vs regex separately
  on DECLARED and UNDECLARED strata.
- >-
  SURFACED the omitted threshold result: leave-one-recipe-class-out refits tau to -1.7156, a 1.03 log-unit shift (~8x the
  0.128 brittleness scale) that changes held-out sensitivities (rank-one 0.167→0.333); the LORCO table must carry four columns
  and specificity must be reported at the refit tau.
- >-
  ADDED behavioural verification of the positive class (the 44 are card-labelled and never checked, while this study exhibits
  root C signature-positive-but-refusing and root B un-censored-but-clean) and independent judge validation of the load-bearing
  behavioural axis (single judge, kappa 0.149, r 0.822, substituted rubric).
- >-
  PROMOTED the both-directions decoupling to the paper's central mechanistic statement, now built as checkpoints with intervals:
  root B un-censors 0.950→0.270 [0.196,0.360] at n=111 reading its parent's W05 -1.0100 with cos(v1,r)=0.0199, class prevalence
  45.8%; root C fires at -4.587 refusing at 0.950.
- >-
  ADDED the analytic isometry boundary as a permanent limit (ORBA Householder moves W05 by 4.1e-5, less than a random-direction
  Householder's 7.3e-5) and the effectiveness/detectability near-orthogonality (10 effective kernels, 4 detected).
- >-
  RETIRED 'parent-free costs nothing': E_1 fires 13/32 vs W05's 7/35 at scale and reaches Gaussian-depth, Heretic and partial-layer
  edits, with the detection vector INVARIANT across all three bands, settling the band-sensitivity objection.
- >-
  RESOLVED quantization (remedy VOID — archive was already fake-quant; scar dies at 5 BITS with refusal 0.237 and ppl 28.77;
  cos(v1,r)>0.9994 so the null FILLS IN; W05rel algebraically identical and retired) and stratified the 0/122 denominator
  as unrepresentative (29/40 new rows gpt_neox, mostly base models) pending a chat-stratum scan.
- >-
  RETIRED W01/W04 from any load-bearing role (irreproducible below ~0.05 on abliterated checkpoints, float32 Gram floor) and
  recorded that bf16 storage, not the edit, sets the scar depth (-4.592 vs -12.705 in float32).
- >-
  REFRAMED NOVELTY honestly against Abliterlitics' measured depth/completeness fingerprints at our own scale and 2607.01854's
  already-band-averaged E_1: the mechanism is an independent PARENT-FREE confirmation of what delta-based forensics measures,
  and the surviving novel object is four qualifiers of which the sliding half is still unearned.
- >-
  ADDED the editorial pass the reviewer requires: no backward references, numbered sections, corrections consolidated into
  one delimited subsection, Contributions cut to four findings, the 110-assertion self-audit moved to an appendix.
relation_type: evolution
</hypothesis>

<all_artifacts>
FULL EVIDENCE BASE: All 25 research artifacts across all iterations.

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

--- Item 21 ---
id: art_-wY3_BLZ_sCu
type: experiment
title: Does a sliding window catch hidden edits?
summary: |-
  EXECUTED end to end. $0.00 OpenRouter spend, zero prompts, zero forward passes. ALL THREE Arm A tiers COMPLETE (78/78 Hub checkpoints scored, 71 OK, 7 UNRESOLVED excluded from every denominator) plus 47/47 in-memory kernels. verify.py (standalone, imports nothing from the pipeline) exits 0 with 60/60 entries re-derived from the raw rows; re-running the analysis leaves numbers.json and method_out.json BYTE-IDENTICAL.

  HEADLINE, the first clear positive for windowing. On 50 real edited Hub checkpoints at specificity 1.000 (57 eligible undeclared negatives): W05w(k=2) sensitivity 0.700 [0.562, 0.809] versus pooled W05 0.300 [0.191, 0.438]. Windowing MORE THAN DOUBLES real-checkpoint recall at zero false positives. It ties the 11-term repo-name regex baseline (0.700) and beats the frozen 8-term feature (0.580) while using no repo name at all, which matters because a name regex is a declaration detector and cannot fire on an undeclared edit. catch_by_recipe_class is populated for every k (it was EMPTY in iteration 4): at k=2, W05w vs W05 is partial-layer 0.80 vs 0.00, multi-direction SVD 0.80 vs 0.00, merge 0.75 vs 0.00, Heretic 0.62 vs 0.12, uncensoring SFT 0.62 vs 0.00. On the kernel family, 8 of 22 pooled misses are recovered at the same pre-registered threshold (BAND_MID50, Gaussian spreads 2/4/8 at both storage precisions, HERETIC_TENT).

  GATES. G1 max |dW05| = 1.54e-5; across 71 real Hub checkpoints the recomputed W05 matches the archive to 9.6e-6 (an independent third reproduction). G2 write_matrix_sha256 matches cd8392d0... EXACTLY. G3 resolved honestly under BOTH comparisons: (a) W05w(k=L) vs W05_f64 = 0.0 exactly at the 1e-9 tolerance, the comparison that actually tests the window code; (b) vs the float32 W05 = 1.09e-6, reported as FAILING iteration 4's declared 1e-9 and passing a DERIVED float32 accumulation bound log10(1+gamma_d) = 5.30e-5 at d=2048. The tolerance was not moved silently.

  PREDICTIONS, stamped by sha256 before any scoring: 6 CONFIRMED, 2 REFUTED, both refutations reported with mechanism. P2 REFUTED 3/5 -- Gaussian spreads 0.5 and 1 confine the edit to ONE layer, so even k=2 always contains an unedited layer that sets the minimum: the smallest detectable edit width equals the smallest usable k. P5 REFUTED on the letter of a pre-registered rule that was NOT moved (k=4,6 exceed the 4-seed control max by ~2x), though both quantities are float32 Gram noise, 2.1e-4 log units against a 1.73 log-unit margin. P4 CONFIRMED: sub-unit uniform w in {0.5,0.7,0.85} invisible at every k and every tau_c -- windowing changes pooling SCOPE, never removal COMPLETENESS.

  ARM 2, a substantive negative. BOTH calibrations reject the UNEDITED control, for two separately diagnosed reasons: the random-direction null because v1_win is the MINIMISING eigenvector rather than a random draw (parent at several hundred sigma), and the layer-subset null because contiguous windows are systematically deeper than random layer subsets (parent gap -0.293 log units) from ordinary depth continuity. Conclusion: the multiple-window hazard CANNOT be bounded by any within-model null; it is bounded here by measured specificity on real undeclared checkpoints. A third defect was found and fixed rather than shipped: the naive min-over-windows-vs-single-subset p never falls below 0.3297 for ANY kernel, not even a complete rank-one projection; the corrected per-window Sidak construction spans [0, 0.909] and discriminates.

  ARM 3: generalised subspace discovery via principal angles, agreement 1.000 on 47 applicable kernels, P8 applicability complete. Two corrections were required and are in the code: j must be at least dim(R), and j_star is the SMALLEST containing j, not the largest. Arm A is INAPPLICABLE BY CONSTRUCTION (removed direction unknown; imputing it would be circular) -- only a labelled parent-requiring surrogate is reported.

  ARM 4: the plan's small RELATIVE residual does not exist and cannot -- at the argmin matrix both energies sit at the annihilation floor, so the relative residual reaches 7.93 even at cos^2(theta) > 0.999. What holds is a LAW with a measured constant: |residual| / sin^2(theta) <= 1.726 (median 0.780, n=22).

  CAVEATS. Iteration 4 did NOT persist the per-layer diff-in-means or SVD directions, so the archived heretic_percomponent W05 = -1.7156 is NOT reproducible without forward passes; a deterministic substitute is used and every affected row carries direction_substituted. kernels.edit_percomponent uses the SAME direction for attn and mlp, so the plan's '2-dim span [r0_attn, r0_mlp]' does not exist -- the removed span is 1-dimensional.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_5/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 22 ---
id: art_BlPNy1aBYVSE
type: experiment
title: Is the name-guess baseline really that good?
summary: |-
  Three arms over one shared download -> eligibility -> W05 -> delete pipeline, reusing archived iteration-3/4 code byte-identically (sha256 of every vendored file in results/provenance.json). Tier completed = ALL. Gates G1-G4 PASS (G1 archived-W05 reproduction delta 6.6e-08, tolerance 1e-3), determinism byte-identical on 3 checkpoints, verify.py 193/193 checks, judge spend $0.048 of the $1.50 cap.

  ARM 1 (the deliverable of record). The plan assumed the Hub-sweep discovery channel was unrecoverable; it is NOT. iter_3/gen_art_dataset_1/results/enumerated.json stores `found_by` per repo plus all 61 per-query hit lists, so the de-biasing is a MEASUREMENT, not a reconstruction. Repo-name-regex sensitivity by discovery channel: name-free (arch/top sweeps) 0.642 [0.507, 0.757] n=53; term-sweep-discovered 0.953 [0.925, 0.970] n=358; uploader-only 0.888 n=80; whole manifest 0.895 (459/513). The archived 0.727 (32/44) lies INSIDE the de-biased interval, so it survives as an estimate -- of a much weaker baseline than the term-swept pool suggests. IMPORTANT CORRECTION for any downstream text: the 11-term REGEX_11 and the dependency's own repo_id_contains_abliteration_string flag are DIFFERENT estimators -- 459/513 vs 259/513; 'heretic' alone contributes 220 hits and is absent from the dependency flag. The '50.5% name baseline' sentence quotes the narrower flag, not the regex scored against W05.

  ARM 1 KEY NEGATIVE RESULT. The 2x2 on 84 measured edited checkpoints (44 archived Arm-A rows reused at their archived W05 + 40 newly measured): W05 at TAU_PANEL fires 10/50 on rows the regex already names and 0/34 on rows it does not (Wilson upper bound 0.102); at TAU_REFIT, 16/50 and 1/34 (KnutJaegersberg/Walter-Falcon-1B, W05 -2.470). caught_by_W05_missed_by_name is EMPTY at the calibrated panel threshold. sens(regex | declared) = 1.0 and sens(regex | undeclared) = 0.0 are labelled in-cell as identities, not measurements. Tier-C card mining over all 1,650 name-clean non-declaring pool cards found only 6 hits (0.36%), so the census's 23.4% UNKNOWN does not imply a large hidden name-clean edited population at the top of the scan pool. w05w_status = NOT_AVAILABLE (plan F5).

  ARM 2. 14 card-labelled positives over 9 re-derived recipe classes plus 12 resolvable parents (23 models generated), greedy on the frozen 40-item core with each model's own chat template, rubric-B judge (meta-llama/llama-3.3-70b-instruct, T=0) behind a content-addressed cache. Verdicts: 4 VERIFIED_UNCENSORED, 3 NOT_UNCENSORED, 5 AMBIGUOUS, 1 INCOHERENT_NOT_ASSESSABLE, 1 generation failure. Card-label error rate 0.250 [0.089, 0.532] among assessable rows -- a quarter of the positive class does not behave as un-censored, so the 44-row denominator is itself uncertain and sensitivity ships as an interval over denominators. sens_verified is NOT estimable at n=4 (< the pre-set floor of 6). Paired regex - W05 = +0.615 [0.308, 0.846] over 13 rows, excluding zero. NEW METHODOLOGICAL GUARD: rubric B scores a degenerate loop as REFUSAL, so a 30M checkpoint reads 1.00 refusal from incapacity; rows with distinct-3 < 0.25 are reported as unknown rather than counted either way.

  ARM 3. 180 repos scanned from the non-declaring chat stratum in ascending scan_rank, 128 eligible under the UNMODIFIED pre-stamped rule (stamp written before any rate file). Denominator 251 (159 chat / 78 base / 14 unlabelled). FPR at TAU_PANEL: 0/251 pooled, 0/159 chat (Wilson hi 0.024), 0/78 base. FPR at TAU_REFIT: 0.080 pooled, 0.044 chat, 0.154 base -- the refit threshold costs real specificity and costs it disproportionately on BASE models. Closest negative W05 = -2.6139, margin 0.128 log10 to TAU_PANEL. Two bookkeeping findings: the archived 0/122 cannot be rebuilt row by row (no per-row list for its 40 new-eligible rows; shipped rows support 138), and theyur/dhamma-parrot-v01 was a card-declaring edit sitting inside the negative denominator and is removed as a contaminant.

  OUTPUT. method_out.json carries metadata.verdicts (six plain-English conclusions written from the computed numbers), headline_numbers, gates, eligibility_stamp, provenance, arm1/arm2/arm3 blocks, determinism, spend and 12 direct-claim limitations; datasets holds 84 arm1 positives, 180 arm3 negatives and 14 arm2 behavioural rows, each with predict_baseline_repo_name_regex beside predict_our_method_W05_tau_panel/tau_refit so the baseline and the method are scored on identical rows. Gotchas for reuse: vendored_lib_behave._is_refusal needs lib_data.py alongside it, and two concurrent `--stage arm2` processes will double-append (kill by PID, delete results/generations and arm2_behaviour.jsonl, restart).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_5/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 23 ---
id: art_gSQc4W6QUHvZ
type: evaluation
title: One numbers file the paper must obey
summary: |-
  PURE RE-ANALYSIS of the archived iteration-2/3/4 trees. ZERO model weights, ZERO forward passes, ZERO Hub fetches, ZERO LLM calls, $0.00 of the $10 cap, ~45 s wall clock. Ships numbers.json (211 entries, schema-EXTENDED from A2/results/numbers.json so the two merge: the same nine keys plus key_path/raw_value/recomputed_from_rows/orientation_convention/status/note) and verify_numbers.py, which imports NOTHING from the analysis and recomputes from raw rows: 151 PASS / 0 FAIL / 0 UNAVAILABLE, exit 0. Determinism BYTE-IDENTICAL across two builds in two OS processes (8 files, sha256 each). Assertions 102 MATCH / 2 MISMATCH / 0 UNAVAILABLE; neither mismatch was silently fixed -- each became a corrections[] entry with the archive's row-level value winning.

  POOLS REBUILT FROM ROWS, WITH A GATE. Positives 67 = 44 real Hub edits (Arm A) + 23 in-house kernels (Arm B); the pooling assumption REPRODUCES n_fit_positives = 67 - n_held_out for ALL 19 lorco cells. Negatives 32 = 20 Arm-A declared parents + 11 unique archived iteration-3 parents + the Arm-B host, and ALL NINE Arm-A class AUROCs reproduce the archive at delta 0.00e+00 -- that exact reproduction is what licenses the pool. NOTE: the archive carries 19 lorco cells, not the 20 the plan expected (C18).

  HEADLINE FINDINGS. (1) THE OPERATING POINT IS ARBITRARY: holding out one recipe class moves tau by 1.0259 log10 (-2.7415 -> -1.7156), 8.04x the 0.1276 shift that already yields the first false positive. (2) SPECIFICITY DOES NOT SURVIVE REFITTING: 0/139 eligible undeclared checkpoints fire at the panel tau, but 13/139 fire at the refit tau (0.094, Wilson [0.055, 0.153]); the chat/instruct subset is n=36 with 0 firing, Wilson [0.000, 0.096] -- too small to stand in for the at-risk population. A ready-to-paste narrower-claim sentence is emitted. (3) NEW, HIGH-VALUE: the archived auroc_oriented column reports max(raw, 1-raw) and records its orientation PER CELL, so 8 of 19 cells print under the OPPOSITE orientation to the rule W05 <= tau; holding orientation fixed at lower-is-positive, those same 8 classes fall BELOW CHANCE (C24). (4) The archived 0/122 denominator is a MID-SCAN SNAPSHOT: recounted from rows it is 82 archived + 57 newly scanned = 139, numerator still 0, so precision is STRONGER (C22).

  DERIVATION SETTLED BY A NUMBER. The Cauchy-Schwarz bound is emitted as a formula string plus a callable and EVALUATED on 25 archived rows: 0 violations, and over discovery-holding rows where the bound is informative max |W05 - log10 min_m e_r| = 0.029 log10 (n=5), reproducing the three quoted anchors. '19/19 with zero disagreements' is therefore RETIRED as evidence, alongside W05rel, W01/W04, the dequantization remedy, and uniformity-as-predicate, each with the licensing row. |cos| is clipped at 1-2^-23 because abscos_v1_r is stored in float32. Undefinedness is COMPUTED not asserted: 12 of 44 scored edited rows (draft said 13 -> C20), repo_ids listed; the principal-angle generalisation is stated as a DEFINITION, labelled NOT-YET-EVALUATED. Proposition 1 (isometry impossibility) carries proof sketch, the ORBA two-recipe caveat, an explicit note that it covers W05w, and measurement: ORBA moves W05 by 4.08e-05, BELOW a random-direction control at 7.26e-05. Effectiveness vs detectability: 10 effective kernels, 4 detected; Spearman 0.113, bootstrap [-0.641, 0.700] over 25 kernels -- the CI is what makes 'near-orthogonal' sayable.

  ALSO SHIPS. results/corrections.json: 24 entries, each {id, claim_as_previously_reported, corrected_value, provenance{file,key,raw_value}, recomputed_from_rows, one_sentence_for_the_paper}, including 81 unresolved / 8 skipped / 270=20+250 arithmetic asserted, five unreproduced quoted values, B09 0.766-vs-0.670, ladder denominators 31-40 with 13 ambiguous, the power calc (smallest detectable DIFFERENCE 0.294 at n=40/p=0.20 -- a difference, not a rate), judge r 0.822 / kappa 0.149, the bit-width curve (scar dies at 5 bits), storage precision -4.592 bf16 vs -12.705 float32, E_1 13/32 vs W05 7/35 agreeing 0.829 under the archived convention, and the 0.727 regex as a NAME-SEARCH UPPER BOUND. results/edit_list.json: 34 numbered mechanical edits, 33 blocking, with 25 backward references LOCATED in the iteration-4 draft on disk (not merely rules), the numbered section skeleton + cross-reference map, Contributions cut to four finding-shaped strings plus a REMOVE list, the self-audit moved to Appendix A (both text variants), the 12.6 toy figure deleted with both pre-written fallbacks, the k=L tolerance question with both sentences and which the numbers support, and arm-dependent sentences flagged from A2's zero-positive markers. results/carry_forward.json: 130 values with full provenance. Statistics discipline: Wilson formula and continuity flag printed, percentile bootstrap n_boot=10000 with default_rng(20260814) and the resampling unit named per statistic, numbers.json never rounded.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_5/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 24 ---
id: art_ajJq7IGjE6dm
type: evaluation
title: Does a second judge change the safety verdicts
summary: |-
  Validates the single LLM judge (meta-llama/llama-3.3-70b-instruct, rubric B) that the entire behavioural axis of the abliteration-detector paper rests on. $0.0666 of a $1.50 cap; verify_eval.py 56/56; eval_out.json validates against exp_eval_sol_out.

  TEXT RECOVERY, SELF-VERIFYING. The archive stored no generation text -- only per-uid BINARY labels and a judge_cache mapping sha256(model||rubric||prompt||response[:1500]) -> label. regen.py re-created 3,880 generations across ALL 61 archived behavioural cells (roots A/B/C incl. the real gated meta-llama/Llama-3.2-1B-Instruct, both parents, the full merge/add-back/quant ladder); 60.6% HIT the archived cache key, which is a PROOF of byte-identical text, not bookkeeping. The residual was diagnosed, not assumed: probe_batch.json shows 0.55-0.65 across batch 8/16/32/40, so batching is not the cause -- it is cross-device bf16 kernel selection (archive RTX 2000 Ada vs RTX 4090). That is a NEW reproducibility limit on the ARCHIVED behavioural numbers. Llama-host cells recover at 0.93-0.97, Qwen-host near 0.55. Only proven-identical items entered the frame; the induced selection is measured per cell (archived label rate on hit vs missed items).

  THREE ARMS on 620 census items over 19 load-bearing stages (the pre-registered seeded 180-item stratified sample is flagged in-place and analysed separately): J1 = archived judge (free, from cache), J2 = google/gemini-2.5-flash on rubric B VERBATIM (model effect, circularity guard asserted), J3 = same model on a re-worded rubric C (rubric effect), plus the unmodified Arditi substring screen.

  HEADLINE. J1 REPRODUCES the archive: root B 0.278 vs archived 0.270. The JUDGE MODEL is the dominant axis: pooled refusal-rate shift 0.269 (model) vs 0.126 (rubric wording) vs 0.034 (PARTIAL collapse rule). Root B's headline projects to 0.770 [0.680,0.859] under Gemini and 0.193 [0.142,0.245] under rubric C -- the NUMBER is scorer-dependent (pre-registered F2). The CLAIM is not: root B sits below its parent under all three scorers and all three separate them. Verdicts: P1 SURVIVES_WEAKENED, P2 SURVIVES_WEAKENED, P3 SURVIVES (Llama AUROC-argmax false positive refuses at 1.000 = parent under EVERY scorer), P4 SURVIVES (10->10 effective kernels, 0 membership flips under PARTIAL re-collapse), P5 SURVIVES (9/9 flag-death orderings PRESERVED).

  THE BLIND ANCHOR BREAKS THE TIE AND FAVOURS THE ARCHIVE. 48 disagreement-enriched items, blinding enforced by asserted sha256/mtime ordering: J1 0.771 acc / kappa 0.643; J3 0.745/0.622; J2 0.521/0.291; screen 0.500/0.155. Disagreement concentrates where J1 says COMPLIANCE and J2 says REFUSAL (per-class agreement 0.333). So the paper's limitation is NOT 'the archived rate is wrong' but 'an unvalidated second judge would report a materially different rate'. The adjudicator is an LLM, not a human -- every accuracy BOUNDS SCORER DISAGREEMENT, never truth (1 flip in 12 re-checks).

  AGREEMENT, with the statistic-choice stated: J1-J2 3-class 0.679 raw / kappa 0.361 / Gwet AC1 0.582 / PABAK 0.519; J1-J3 0.718 / 0.562 / 0.592. Rate-level r 0.703 (J1-J2) vs 0.959 (J1-J3). Screen re-baseline on the same items reproduces the archived pair (kappa 0.312, r 0.782 vs archived 0.149/0.822 over 61 stages). Both archived verifiers still pass unmodified (exp3 29/29, exp1 20/20).

  SHIPS results/judge_limitations.json (the paper's judge paragraph, machine-readable, with pasteable sentences), disputed_items.jsonl (299 items verbatim), recovered.jsonl (3,880 generations), propagation.json, agreement_by_stage.csv, reproducibility.json, 3 figures, and verify_eval.py which re-derives every headline number without importing eval.py. Weight statistics (W05, E1, ladder flags) were NOT recomputed -- taken verbatim from the archive. This artifact varies ONLY the scorer.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_5/gen_art/gen_art_evaluation_2
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 25 ---
id: art_SFTddR644gi0
type: research
title: Cutting the novelty claim to what survives
summary: >-
  Iteration-5 positioning dossier. Verdict on the windowed object: NOVEL-NARROW, with two three-of-four near-misses newly
  identified. Ships seven paste-ready paragraphs in both outcome variants, seven positioning corrections with verbatim quotes,
  a ten-item re-verification log with two MISMATCHes and four UNREACHABLEs, and seventeen numbered wording corrections. Verdict
  NOVEL-NARROW on the four-qualifier conjunction (parent-free, calibration-free, bottom-of-spectrum, sliding-extremum): no
  work carries all four; two carry three and BOTH are new to this dossier -- arXiv:2410.17770 (bottom-of-spectrum RMT, parent-
  and calibration-free, not windowed, not a detector; the largest uncited risk) and EigenTrack 2509.15735 (sliding, but over
  time across activations). 2607.23711 Intruder Threshold RESOLVED as near-miss (needs sigma_1(BA), reads the top, is a LoRA
  law not a detector). Two MISMATCHes: 2607.01854's registry is 273 but only 71 processed / 94 evaluated, and the weights-only
  signal is AUROC 0.90 not 0.84. New obligatory citation: E_1 is the WeightWatch primitive (2508.00161, ICLR 2026). Heretic's
  triangular-tent kernel and reverse-abliterate's filename-only detection re-confirmed at code level. MP null convention FOUND
  and nameable; multiple-window FWER convention NONE FOUND (import max-statistic permutation, labelled ANALOGOUS). Ships 7
  paste-ready paragraphs in both outcome variants, 7 positioning corrections, 17 numbered wording corrections, a 10-item re-verification
  log with 4 UNREACHABLEs reported not silently carried, and a 10th recipe class (concept-registry ridge residualization,
  2601.08489). research_out.json carries the prose answer plus the full dossier under structured_answer.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_5/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</all_artifacts>

<new_artifacts_this_iteration>
NEW THIS ITERATION: These 5 artifacts were created to address the reviewer
feedback. Their findings should be the primary basis for your revisions.

id: art_-wY3_BLZ_sCu
title: Does a sliding window catch hidden edits?
type: experiment
summary: |-
  EXECUTED end to end. $0.00 OpenRouter spend, zero prompts, zero forward passes. ALL THREE Arm A tiers COMPLETE (78/78 Hub checkpoints scored, 71 OK, 7 UNRESOLVED excluded from every denominator) plus 47/47 in-memory kernels. verify.py (standalone, imports nothing from the pipeline) exits 0 with 60/60 entries re-derived from the raw rows; re-running the analysis leaves numbers.json and method_out.json BYTE-IDENTICAL.

  HEADLINE, the first clear positive for windowing. On 50 real edited Hub checkpoints at specificity 1.000 (57 eligible undeclared negatives): W05w(k=2) sensitivity 0.700 [0.562, 0.809] versus pooled W05 0.300 [0.191, 0.438]. Windowing MORE THAN DOUBLES real-checkpoint recall at zero false positives. It ties the 11-term repo-name regex baseline (0.700) and beats the frozen 8-term feature (0.580) while using no repo name at all, which matters because a name regex is a declaration detector and cannot fire on an undeclared edit. catch_by_recipe_class is populated for every k (it was EMPTY in iteration 4): at k=2, W05w vs W05 is partial-layer 0.80 vs 0.00, multi-direction SVD 0.80 vs 0.00, merge 0.75 vs 0.00, Heretic 0.62 vs 0.12, uncensoring SFT 0.62 vs 0.00. On the kernel family, 8 of 22 pooled misses are recovered at the same pre-registered threshold (BAND_MID50, Gaussian spreads 2/4/8 at both storage precisions, HERETIC_TENT).

  GATES. G1 max |dW05| = 1.54e-5; across 71 real Hub checkpoints the recomputed W05 matches the archive to 9.6e-6 (an independent third reproduction). G2 write_matrix_sha256 matches cd8392d0... EXACTLY. G3 resolved honestly under BOTH comparisons: (a) W05w(k=L) vs W05_f64 = 0.0 exactly at the 1e-9 tolerance, the comparison that actually tests the window code; (b) vs the float32 W05 = 1.09e-6, reported as FAILING iteration 4's declared 1e-9 and passing a DERIVED float32 accumulation bound log10(1+gamma_d) = 5.30e-5 at d=2048. The tolerance was not moved silently.

  PREDICTIONS, stamped by sha256 before any scoring: 6 CONFIRMED, 2 REFUTED, both refutations reported with mechanism. P2 REFUTED 3/5 -- Gaussian spreads 0.5 and 1 confine the edit to ONE layer, so even k=2 always contains an unedited layer that sets the minimum: the smallest detectable edit width equals the smallest usable k. P5 REFUTED on the letter of a pre-registered rule that was NOT moved (k=4,6 exceed the 4-seed control max by ~2x), though both quantities are float32 Gram noise, 2.1e-4 log units against a 1.73 log-unit margin. P4 CONFIRMED: sub-unit uniform w in {0.5,0.7,0.85} invisible at every k and every tau_c -- windowing changes pooling SCOPE, never removal COMPLETENESS.

  ARM 2, a substantive negative. BOTH calibrations reject the UNEDITED control, for two separately diagnosed reasons: the random-direction null because v1_win is the MINIMISING eigenvector rather than a random draw (parent at several hundred sigma), and the layer-subset null because contiguous windows are systematically deeper than random layer subsets (parent gap -0.293 log units) from ordinary depth continuity. Conclusion: the multiple-window hazard CANNOT be bounded by any within-model null; it is bounded here by measured specificity on real undeclared checkpoints. A third defect was found and fixed rather than shipped: the naive min-over-windows-vs-single-subset p never falls below 0.3297 for ANY kernel, not even a complete rank-one projection; the corrected per-window Sidak construction spans [0, 0.909] and discriminates.

  ARM 3: generalised subspace discovery via principal angles, agreement 1.000 on 47 applicable kernels, P8 applicability complete. Two corrections were required and are in the code: j must be at least dim(R), and j_star is the SMALLEST containing j, not the largest. Arm A is INAPPLICABLE BY CONSTRUCTION (removed direction unknown; imputing it would be circular) -- only a labelled parent-requiring surrogate is reported.

  ARM 4: the plan's small RELATIVE residual does not exist and cannot -- at the argmin matrix both energies sit at the annihilation floor, so the relative residual reaches 7.93 even at cos^2(theta) > 0.999. What holds is a LAW with a measured constant: |residual| / sin^2(theta) <= 1.726 (median 0.780, n=22).

  CAVEATS. Iteration 4 did NOT persist the per-layer diff-in-means or SVD directions, so the archived heretic_percomponent W05 = -1.7156 is NOT reproducible without forward passes; a deterministic substitute is used and every affected row carries direction_substituted. kernels.edit_percomponent uses the SAME direction for attn and mlp, so the plan's '2-dim span [r0_attn, r0_mlp]' does not exist -- the removed span is 1-dimensional.

id: art_BlPNy1aBYVSE
title: Is the name-guess baseline really that good?
type: experiment
summary: |-
  Three arms over one shared download -> eligibility -> W05 -> delete pipeline, reusing archived iteration-3/4 code byte-identically (sha256 of every vendored file in results/provenance.json). Tier completed = ALL. Gates G1-G4 PASS (G1 archived-W05 reproduction delta 6.6e-08, tolerance 1e-3), determinism byte-identical on 3 checkpoints, verify.py 193/193 checks, judge spend $0.048 of the $1.50 cap.

  ARM 1 (the deliverable of record). The plan assumed the Hub-sweep discovery channel was unrecoverable; it is NOT. iter_3/gen_art_dataset_1/results/enumerated.json stores `found_by` per repo plus all 61 per-query hit lists, so the de-biasing is a MEASUREMENT, not a reconstruction. Repo-name-regex sensitivity by discovery channel: name-free (arch/top sweeps) 0.642 [0.507, 0.757] n=53; term-sweep-discovered 0.953 [0.925, 0.970] n=358; uploader-only 0.888 n=80; whole manifest 0.895 (459/513). The archived 0.727 (32/44) lies INSIDE the de-biased interval, so it survives as an estimate -- of a much weaker baseline than the term-swept pool suggests. IMPORTANT CORRECTION for any downstream text: the 11-term REGEX_11 and the dependency's own repo_id_contains_abliteration_string flag are DIFFERENT estimators -- 459/513 vs 259/513; 'heretic' alone contributes 220 hits and is absent from the dependency flag. The '50.5% name baseline' sentence quotes the narrower flag, not the regex scored against W05.

  ARM 1 KEY NEGATIVE RESULT. The 2x2 on 84 measured edited checkpoints (44 archived Arm-A rows reused at their archived W05 + 40 newly measured): W05 at TAU_PANEL fires 10/50 on rows the regex already names and 0/34 on rows it does not (Wilson upper bound 0.102); at TAU_REFIT, 16/50 and 1/34 (KnutJaegersberg/Walter-Falcon-1B, W05 -2.470). caught_by_W05_missed_by_name is EMPTY at the calibrated panel threshold. sens(regex | declared) = 1.0 and sens(regex | undeclared) = 0.0 are labelled in-cell as identities, not measurements. Tier-C card mining over all 1,650 name-clean non-declaring pool cards found only 6 hits (0.36%), so the census's 23.4% UNKNOWN does not imply a large hidden name-clean edited population at the top of the scan pool. w05w_status = NOT_AVAILABLE (plan F5).

  ARM 2. 14 card-labelled positives over 9 re-derived recipe classes plus 12 resolvable parents (23 models generated), greedy on the frozen 40-item core with each model's own chat template, rubric-B judge (meta-llama/llama-3.3-70b-instruct, T=0) behind a content-addressed cache. Verdicts: 4 VERIFIED_UNCENSORED, 3 NOT_UNCENSORED, 5 AMBIGUOUS, 1 INCOHERENT_NOT_ASSESSABLE, 1 generation failure. Card-label error rate 0.250 [0.089, 0.532] among assessable rows -- a quarter of the positive class does not behave as un-censored, so the 44-row denominator is itself uncertain and sensitivity ships as an interval over denominators. sens_verified is NOT estimable at n=4 (< the pre-set floor of 6). Paired regex - W05 = +0.615 [0.308, 0.846] over 13 rows, excluding zero. NEW METHODOLOGICAL GUARD: rubric B scores a degenerate loop as REFUSAL, so a 30M checkpoint reads 1.00 refusal from incapacity; rows with distinct-3 < 0.25 are reported as unknown rather than counted either way.

  ARM 3. 180 repos scanned from the non-declaring chat stratum in ascending scan_rank, 128 eligible under the UNMODIFIED pre-stamped rule (stamp written before any rate file). Denominator 251 (159 chat / 78 base / 14 unlabelled). FPR at TAU_PANEL: 0/251 pooled, 0/159 chat (Wilson hi 0.024), 0/78 base. FPR at TAU_REFIT: 0.080 pooled, 0.044 chat, 0.154 base -- the refit threshold costs real specificity and costs it disproportionately on BASE models. Closest negative W05 = -2.6139, margin 0.128 log10 to TAU_PANEL. Two bookkeeping findings: the archived 0/122 cannot be rebuilt row by row (no per-row list for its 40 new-eligible rows; shipped rows support 138), and theyur/dhamma-parrot-v01 was a card-declaring edit sitting inside the negative denominator and is removed as a contaminant.

  OUTPUT. method_out.json carries metadata.verdicts (six plain-English conclusions written from the computed numbers), headline_numbers, gates, eligibility_stamp, provenance, arm1/arm2/arm3 blocks, determinism, spend and 12 direct-claim limitations; datasets holds 84 arm1 positives, 180 arm3 negatives and 14 arm2 behavioural rows, each with predict_baseline_repo_name_regex beside predict_our_method_W05_tau_panel/tau_refit so the baseline and the method are scored on identical rows. Gotchas for reuse: vendored_lib_behave._is_refusal needs lib_data.py alongside it, and two concurrent `--stage arm2` processes will double-append (kill by PID, delete results/generations and arm2_behaviour.jsonl, restart).

id: art_gSQc4W6QUHvZ
title: One numbers file the paper must obey
type: evaluation
summary: |-
  PURE RE-ANALYSIS of the archived iteration-2/3/4 trees. ZERO model weights, ZERO forward passes, ZERO Hub fetches, ZERO LLM calls, $0.00 of the $10 cap, ~45 s wall clock. Ships numbers.json (211 entries, schema-EXTENDED from A2/results/numbers.json so the two merge: the same nine keys plus key_path/raw_value/recomputed_from_rows/orientation_convention/status/note) and verify_numbers.py, which imports NOTHING from the analysis and recomputes from raw rows: 151 PASS / 0 FAIL / 0 UNAVAILABLE, exit 0. Determinism BYTE-IDENTICAL across two builds in two OS processes (8 files, sha256 each). Assertions 102 MATCH / 2 MISMATCH / 0 UNAVAILABLE; neither mismatch was silently fixed -- each became a corrections[] entry with the archive's row-level value winning.

  POOLS REBUILT FROM ROWS, WITH A GATE. Positives 67 = 44 real Hub edits (Arm A) + 23 in-house kernels (Arm B); the pooling assumption REPRODUCES n_fit_positives = 67 - n_held_out for ALL 19 lorco cells. Negatives 32 = 20 Arm-A declared parents + 11 unique archived iteration-3 parents + the Arm-B host, and ALL NINE Arm-A class AUROCs reproduce the archive at delta 0.00e+00 -- that exact reproduction is what licenses the pool. NOTE: the archive carries 19 lorco cells, not the 20 the plan expected (C18).

  HEADLINE FINDINGS. (1) THE OPERATING POINT IS ARBITRARY: holding out one recipe class moves tau by 1.0259 log10 (-2.7415 -> -1.7156), 8.04x the 0.1276 shift that already yields the first false positive. (2) SPECIFICITY DOES NOT SURVIVE REFITTING: 0/139 eligible undeclared checkpoints fire at the panel tau, but 13/139 fire at the refit tau (0.094, Wilson [0.055, 0.153]); the chat/instruct subset is n=36 with 0 firing, Wilson [0.000, 0.096] -- too small to stand in for the at-risk population. A ready-to-paste narrower-claim sentence is emitted. (3) NEW, HIGH-VALUE: the archived auroc_oriented column reports max(raw, 1-raw) and records its orientation PER CELL, so 8 of 19 cells print under the OPPOSITE orientation to the rule W05 <= tau; holding orientation fixed at lower-is-positive, those same 8 classes fall BELOW CHANCE (C24). (4) The archived 0/122 denominator is a MID-SCAN SNAPSHOT: recounted from rows it is 82 archived + 57 newly scanned = 139, numerator still 0, so precision is STRONGER (C22).

  DERIVATION SETTLED BY A NUMBER. The Cauchy-Schwarz bound is emitted as a formula string plus a callable and EVALUATED on 25 archived rows: 0 violations, and over discovery-holding rows where the bound is informative max |W05 - log10 min_m e_r| = 0.029 log10 (n=5), reproducing the three quoted anchors. '19/19 with zero disagreements' is therefore RETIRED as evidence, alongside W05rel, W01/W04, the dequantization remedy, and uniformity-as-predicate, each with the licensing row. |cos| is clipped at 1-2^-23 because abscos_v1_r is stored in float32. Undefinedness is COMPUTED not asserted: 12 of 44 scored edited rows (draft said 13 -> C20), repo_ids listed; the principal-angle generalisation is stated as a DEFINITION, labelled NOT-YET-EVALUATED. Proposition 1 (isometry impossibility) carries proof sketch, the ORBA two-recipe caveat, an explicit note that it covers W05w, and measurement: ORBA moves W05 by 4.08e-05, BELOW a random-direction control at 7.26e-05. Effectiveness vs detectability: 10 effective kernels, 4 detected; Spearman 0.113, bootstrap [-0.641, 0.700] over 25 kernels -- the CI is what makes 'near-orthogonal' sayable.

  ALSO SHIPS. results/corrections.json: 24 entries, each {id, claim_as_previously_reported, corrected_value, provenance{file,key,raw_value}, recomputed_from_rows, one_sentence_for_the_paper}, including 81 unresolved / 8 skipped / 270=20+250 arithmetic asserted, five unreproduced quoted values, B09 0.766-vs-0.670, ladder denominators 31-40 with 13 ambiguous, the power calc (smallest detectable DIFFERENCE 0.294 at n=40/p=0.20 -- a difference, not a rate), judge r 0.822 / kappa 0.149, the bit-width curve (scar dies at 5 bits), storage precision -4.592 bf16 vs -12.705 float32, E_1 13/32 vs W05 7/35 agreeing 0.829 under the archived convention, and the 0.727 regex as a NAME-SEARCH UPPER BOUND. results/edit_list.json: 34 numbered mechanical edits, 33 blocking, with 25 backward references LOCATED in the iteration-4 draft on disk (not merely rules), the numbered section skeleton + cross-reference map, Contributions cut to four finding-shaped strings plus a REMOVE list, the self-audit moved to Appendix A (both text variants), the 12.6 toy figure deleted with both pre-written fallbacks, the k=L tolerance question with both sentences and which the numbers support, and arm-dependent sentences flagged from A2's zero-positive markers. results/carry_forward.json: 130 values with full provenance. Statistics discipline: Wilson formula and continuity flag printed, percentile bootstrap n_boot=10000 with default_rng(20260814) and the resampling unit named per statistic, numbers.json never rounded.

id: art_ajJq7IGjE6dm
title: Does a second judge change the safety verdicts
type: evaluation
summary: |-
  Validates the single LLM judge (meta-llama/llama-3.3-70b-instruct, rubric B) that the entire behavioural axis of the abliteration-detector paper rests on. $0.0666 of a $1.50 cap; verify_eval.py 56/56; eval_out.json validates against exp_eval_sol_out.

  TEXT RECOVERY, SELF-VERIFYING. The archive stored no generation text -- only per-uid BINARY labels and a judge_cache mapping sha256(model||rubric||prompt||response[:1500]) -> label. regen.py re-created 3,880 generations across ALL 61 archived behavioural cells (roots A/B/C incl. the real gated meta-llama/Llama-3.2-1B-Instruct, both parents, the full merge/add-back/quant ladder); 60.6% HIT the archived cache key, which is a PROOF of byte-identical text, not bookkeeping. The residual was diagnosed, not assumed: probe_batch.json shows 0.55-0.65 across batch 8/16/32/40, so batching is not the cause -- it is cross-device bf16 kernel selection (archive RTX 2000 Ada vs RTX 4090). That is a NEW reproducibility limit on the ARCHIVED behavioural numbers. Llama-host cells recover at 0.93-0.97, Qwen-host near 0.55. Only proven-identical items entered the frame; the induced selection is measured per cell (archived label rate on hit vs missed items).

  THREE ARMS on 620 census items over 19 load-bearing stages (the pre-registered seeded 180-item stratified sample is flagged in-place and analysed separately): J1 = archived judge (free, from cache), J2 = google/gemini-2.5-flash on rubric B VERBATIM (model effect, circularity guard asserted), J3 = same model on a re-worded rubric C (rubric effect), plus the unmodified Arditi substring screen.

  HEADLINE. J1 REPRODUCES the archive: root B 0.278 vs archived 0.270. The JUDGE MODEL is the dominant axis: pooled refusal-rate shift 0.269 (model) vs 0.126 (rubric wording) vs 0.034 (PARTIAL collapse rule). Root B's headline projects to 0.770 [0.680,0.859] under Gemini and 0.193 [0.142,0.245] under rubric C -- the NUMBER is scorer-dependent (pre-registered F2). The CLAIM is not: root B sits below its parent under all three scorers and all three separate them. Verdicts: P1 SURVIVES_WEAKENED, P2 SURVIVES_WEAKENED, P3 SURVIVES (Llama AUROC-argmax false positive refuses at 1.000 = parent under EVERY scorer), P4 SURVIVES (10->10 effective kernels, 0 membership flips under PARTIAL re-collapse), P5 SURVIVES (9/9 flag-death orderings PRESERVED).

  THE BLIND ANCHOR BREAKS THE TIE AND FAVOURS THE ARCHIVE. 48 disagreement-enriched items, blinding enforced by asserted sha256/mtime ordering: J1 0.771 acc / kappa 0.643; J3 0.745/0.622; J2 0.521/0.291; screen 0.500/0.155. Disagreement concentrates where J1 says COMPLIANCE and J2 says REFUSAL (per-class agreement 0.333). So the paper's limitation is NOT 'the archived rate is wrong' but 'an unvalidated second judge would report a materially different rate'. The adjudicator is an LLM, not a human -- every accuracy BOUNDS SCORER DISAGREEMENT, never truth (1 flip in 12 re-checks).

  AGREEMENT, with the statistic-choice stated: J1-J2 3-class 0.679 raw / kappa 0.361 / Gwet AC1 0.582 / PABAK 0.519; J1-J3 0.718 / 0.562 / 0.592. Rate-level r 0.703 (J1-J2) vs 0.959 (J1-J3). Screen re-baseline on the same items reproduces the archived pair (kappa 0.312, r 0.782 vs archived 0.149/0.822 over 61 stages). Both archived verifiers still pass unmodified (exp3 29/29, exp1 20/20).

  SHIPS results/judge_limitations.json (the paper's judge paragraph, machine-readable, with pasteable sentences), disputed_items.jsonl (299 items verbatim), recovered.jsonl (3,880 generations), propagation.json, agreement_by_stage.csv, reproducibility.json, 3 figures, and verify_eval.py which re-derives every headline number without importing eval.py. Weight statistics (W05, E1, ladder flags) were NOT recomputed -- taken verbatim from the archive. This artifact varies ONLY the scorer.

id: art_SFTddR644gi0
title: Cutting the novelty claim to what survives
type: research
summary: >-
  Iteration-5 positioning dossier. Verdict on the windowed object: NOVEL-NARROW, with two three-of-four near-misses newly
  identified. Ships seven paste-ready paragraphs in both outcome variants, seven positioning corrections with verbatim quotes,
  a ten-item re-verification log with two MISMATCHes and four UNREACHABLEs, and seventeen numbered wording corrections. Verdict
  NOVEL-NARROW on the four-qualifier conjunction (parent-free, calibration-free, bottom-of-spectrum, sliding-extremum): no
  work carries all four; two carry three and BOTH are new to this dossier -- arXiv:2410.17770 (bottom-of-spectrum RMT, parent-
  and calibration-free, not windowed, not a detector; the largest uncited risk) and EigenTrack 2509.15735 (sliding, but over
  time across activations). 2607.23711 Intruder Threshold RESOLVED as near-miss (needs sigma_1(BA), reads the top, is a LoRA
  law not a detector). Two MISMATCHes: 2607.01854's registry is 273 but only 71 processed / 94 evaluated, and the weights-only
  signal is AUROC 0.90 not 0.84. New obligatory citation: E_1 is the WeightWatch primitive (2508.00161, ICLR 2026). Heretic's
  triangular-tent kernel and reverse-abliterate's filename-only detection re-confirmed at code level. MP null convention FOUND
  and nameable; multiple-window FWER convention NONE FOUND (import max-statistic permutation, labelled ANALOGOUS). Ships 7
  paste-ready paragraphs in both outcome variants, 7 positioning corrections, 17 numbered wording corrections, a 10-item re-verification
  log with 4 UNREACHABLEs reported not silently carried, and a 10th recipe class (concept-registry ridge residualization,
  2601.08489). research_out.json carries the prose answer plus the full dossier under structured_answer.
</new_artifacts_this_iteration>

<data_files>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_files>

<task>
Write a research paper draft with LaTeX-ready text, BibTeX citations, and figure placeholders.

YOUR TURN (gen_paper_text): Revise the paper.

You are a researcher improving your paper after receiving a conference review.
Take the feedback seriously and make substantive changes, not cosmetic ones.

1. ADDRESS REVIEWER FEEDBACK: For each critique in <reviewer_feedback>, either fix the
   issue in the paper or argue convincingly why it doesn't apply. Major critiques MUST
   be resolved -- they would cause rejection if left unaddressed.
2. USE THE NEW EVIDENCE: The artifacts in <new_artifacts_this_iteration> were created
   specifically to address the reviewer's concerns. Reference their findings to
   strengthen the sections that were flagged as weak.
3. REWRITE, DON'T PATCH: Don't just append new paragraphs. Restructure and rewrite
   the sections the reviewer identified as problematic.
4. MAINTAIN CONSISTENCY: Ensure the paper aligns with the updated hypothesis.
</task>

<figure_instructions>
FIGURE FORMAT: Use [FIGURE:fig_id] markers in paper_text to indicate where each figure goes.
Then provide the full figure specs in the separate `figures` structured output array.
Each figure in the array must have an `id` matching a marker in the text. Set the `aspect_ratio`
field per figure: 21:9 for architecture / pipeline / flow-chart diagrams (the hero figure should
be one of these — place its marker near the END of the Introduction so it floats to the top of
page 2), 16:9 for comparisons / multi-panel results, 4:3 for dense charts, 1:1 for heatmaps /
confusion matrices / scatter plots.

FIGURE TYPE — set `figure_type` on every figure. One test decides it: does the figure plot numbers?
  "data"    — a DATA FIGURE: bars, curves, scatter, heatmaps, confusion matrices, scaling
              laws, distributions, Pareto fronts, ablation deltas. Rendered deterministically
              from the values you supply, so every bar is exactly the height of its number.
  "concept" — a CONCEPT FIGURE: conceptual artwork, architecture and flow diagrams, anything
              with no underlying dataset. Drawn by an image model.
If the figure has real numbers behind it, ALWAYS use "data". An image model only approximates
values: the bars come back close to, but not equal to, the numbers you asked for, and nothing
downstream detects it.

Example in paper_text:
  "...our method achieves state-of-the-art results as shown below.\n\n[FIGURE:fig3]\n\nThe results demonstrate..."

Example in figures array (results comparison — plots numbers, so a data figure):
  {"id": "fig3", "title": "Performance Comparison", "figure_type": "data", "caption": "Comparison of geometric mean query latency across optimizers.", "image_gen_detailed_description": "Grouped bar chart. Categories: PostgreSQL, Bao, RLQOpt. One series 'Latency'. Values: 4.6, 2.8, 2.0 seconds. Errors: 0.8, 0.5, 0.3. X-axis label 'Optimizer'. Y-axis label 'Latency (s)', range 0-5.", "aspect_ratio": "16:9", "summary": "Compares latency across optimizers"}

Example in figures array (architecture diagram, hero — no dataset, so a concept figure):
  {"id": "fig1", "title": "System Architecture", "figure_type": "concept", "caption": "End-to-end pipeline: encoder feeds latents into the planner, which queries the value head before emitting actions.", "image_gen_detailed_description": "Horizontal flow diagram, left to right. Five labeled boxes: 'Input' (gray), 'Encoder' (blue), 'Latent (z, 256-dim)' (light blue, narrow), 'Planner' (green), 'Action Head' (orange). Arrows labeled with shapes. Value head as separate green box below 'Planner', bidirectional arrow. Sans-serif font, clean white background, no 3D.", "aspect_ratio": "21:9", "summary": "Hero architecture diagram"}

CRITICAL: Before writing figure specs, look through artifact workspace output files (*_out.json)
and code to find ALL the exact values. The figure generator cannot read files — every exact number
and value MUST be in the image_gen_detailed_description. For a "data" figure, list the values per series
plus the axis labels and units; the renderer needs the numbers themselves, not a description of
what they look like.
</figure_instructions>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-writing, aii-semscholar-bib.
TODO 2. LITERATURE REVIEW: Use web search tools to research the landscape — search key terms from
<hypothesis> and <all_artifacts>. Then use aii_semscholar_bib__fetch to batch-fetch real
BibTeX entries. Build a comprehensive Related Work section. Do NOT fabricate entries.
TODO 3. READ ARTIFACTS: Before writing each section, READ the relevant artifact source code, output
files, and data in the workspace. Extract concrete implementation details, technical innovations,
algorithmic specifics, and quantitative results. Do NOT write surface-level descriptions.

ARTIFACT REFERENCES: When you reference results, methodology, or findings from a specific artifact,
place an [ARTIFACT:artifact_id] marker inline. These become footnotes linking to the artifact's code
in the GitHub repository (first mention gets a footnote with URL, subsequent mentions are omitted).
Use the exact artifact ID from <all_artifacts>. Place the marker right after the claim it supports.
Example:
  "Our evaluation showed a 15% improvement over baselines [ARTIFACT:art_4f9d2c81ab37]." 
TODO 4. WRITE PAPER: Write the full paper text with [FIGURE:fig_id] markers per <figure_instructions>,
and provide the figure specs in the figures array. Cite with numeric references [1], [2], etc.
At the end of the paper text, include a full bibliography section. Do NOT compile LaTeX or generate
actual image/figure files. Your ONLY output is the structured JSON.
</todos><user_data>
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
    "FigureSpec": {
      "description": "Figure specification \u2014 structured output from paper writing agent.\n\nThe LLM fills these as a list in PaperText.figures.\nLater converted to Figure objects for viz gen.",
      "properties": {
        "id": {
          "description": "Figure ID matching the [FIGURE:id] marker in paper_text (e.g., 'fig1')",
          "title": "Id",
          "type": "string"
        },
        "title": {
          "description": "Figure title in plain, everyday language \u2014 short and jargon-free. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "caption": {
          "description": "LaTeX figure caption \u2014 appears below the figure in the paper. Should describe what the figure shows and highlight key takeaways.",
          "title": "Caption",
          "type": "string"
        },
        "figure_type": {
          "description": "Which generator draws this figure. Decide by ONE test: does the figure plot numbers? 'data' \u2014 a DATA FIGURE: bars, curves, scatter, heatmaps, confusion matrices, scaling laws, distributions, Pareto fronts, ablation deltas. Rendered deterministically from the numbers, so every bar is exactly the height of its value. 'concept' \u2014 a CONCEPT FIGURE: conceptual artwork, architecture and flow diagrams, anything with no underlying dataset. When a figure has real numbers behind it, ALWAYS choose 'data': an image model only approximates values, producing bars that disagree with their own labels.",
          "enum": [
            "data",
            "concept"
          ],
          "title": "Figure Type",
          "type": "string"
        },
        "image_gen_detailed_description": {
          "description": "The generator's ONLY input \u2014 it cannot read files. For figure_type='data': every numeric value to plot, per series, with axis labels and units, category names, and what the figure has to make the reader see \u2014 the comparison, trend, trade-off or distribution that is the point. Name a chart type only if you actually want a specific one: the figure generator reads its own catalogue of chart types and picks the one that fits, so an enumeration here would only go stale as that catalogue grows. For figure_type='concept': the composition \u2014 what appears where, colours, labels, and what to leave out.",
          "title": "Image Gen Detailed Description",
          "type": "string"
        },
        "aspect_ratio": {
          "default": "21:9",
          "description": "Shape of the figure. '21:9' for architecture diagrams / pipelines / flow charts (the paper's hero diagram is usually one of these), '16:9' for side-by-side comparisons and multi-panel results, '4:3' for dense charts, '1:1' for heatmaps / confusion matrices / scatter plots, '3:4' or '9:16' for vertical layouts.",
          "enum": [
            "1:1",
            "4:3",
            "3:2",
            "16:9",
            "21:9",
            "3:4",
            "9:16"
          ],
          "title": "Aspect Ratio",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this figure communicates",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "id",
        "title",
        "caption",
        "figure_type",
        "image_gen_detailed_description",
        "summary"
      ],
      "title": "FigureSpec",
      "type": "object"
    }
  },
  "description": "Paper text \u2014 structured output from paper writing agent.\n\nStructured output fields (LLMPrompt + LLMStructOut):\n- title, abstract, paper_text, figures, summary\n\npaper_text contains [FIGURE:fig_id] markers for positioning.\nfigures contains the full specs as structured objects.\n\nMetadata fields (plain, set by pipeline code):\n- id",
  "properties": {
    "title": {
      "description": "Paper title \u2014 clear, plain-language, and short so a non-expert understands the main contribution at a glance. Aim for about 6-10 words; avoid jargon and acronyms.",
      "title": "Title",
      "type": "string"
    },
    "abstract": {
      "description": "Paper abstract",
      "title": "Abstract",
      "type": "string"
    },
    "paper_text": {
      "description": "Full paper body text with markdown section headers (# Introduction, # Methods, # Results, # Discussion, # Conclusion). Use [FIGURE:fig_id] markers (e.g. [FIGURE:fig1]) to indicate where each figure should appear.",
      "title": "Paper Text",
      "type": "string"
    },
    "figures": {
      "description": "List of figure specifications. Each must have an id matching a [FIGURE:id] marker in paper_text.",
      "items": {
        "$ref": "#/$defs/FigureSpec"
      },
      "title": "Figures",
      "type": "array"
    },
    "summary": {
      "description": "Brief summary of the paper's main contribution and findings",
      "title": "Summary",
      "type": "string"
    }
  },
  "required": [
    "title",
    "abstract",
    "paper_text",
    "summary"
  ],
  "title": "PaperText",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-14 05:49:34 UTC

```
qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation
```

### [3] SKILL-INPUT — aii-paper-writing · 2026-08-14 05:49:38 UTC

The agent loaded the **aii-paper-writing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-writing
description: Academic paper writing guidance for AI research. Covers paper structure, figure placeholders, bibliography building with Semantic Scholar, and citation rules. Does NOT cover LaTeX compilation or figure file generation — see aii-paper-to-latex for that.
---

## Technical Papers

Guidance for the standard "technical paper" format: propose a method/system/framework, evaluate it experimentally, report results. This is the main track at most CS venues (NeurIPS, ICML, ICLR, ACL, AAAI, etc.). Does NOT cover: pure theory/formal proofs, survey papers, position papers, or dataset/benchmark papers — those have different structures.

### Paper Structure

Target 6-8 pages. Use formal academic language, third person. Support claims with evidence from artifacts.

#### Rough Page Budget (8-page paper)

| Section | Pages | Notes |
|---|---|---|
| Abstract | 0.3 | Problem, approach, key result |
| Introduction | 1.0-1.5 | The most important section |
| Related Work | 0.5-1.0 | Beginning or end (see below) |
| Methods | 1.5-2.0 | Architecture fig on page 1 |
| Experiments | 1.5-2.0 | Setup + results + ablations |
| Discussion | 0.5-1.0 | Limitations go here |
| Conclusion | 0.3-0.5 | Do not repeat the abstract |
| References | 0.5-1.0 | Not counted in page limit |

**Critical rule**: A clear new technical contribution must be articulated by page 3 (quarter of the paper). If the reader doesn't know what you did by then, you've lost them.

#### Section Details

**Abstract** (150-250 words): State the problem, your approach, and the main results. Be factual and comprehensive. Do not repeat the abstract word-for-word later in the paper.

**Introduction** — Follow this 5-paragraph structure:

1. **What is the problem?** Define the task concretely.
2. **Why is it interesting and important?** Real-world impact, scale.
3. **Why is it hard?** Why do naive approaches fail?
4. **Why hasn't it been solved before?** What's wrong with prior solutions? How does yours differ?
5. **What are the key components of your approach and results?** Include specific limitations.

End with a "Summary of Contributions" subsection — bullet list of contributions with section references. This doubles as an outline, saving space.

**Related Work** — Placement decision:
- **Beginning** (Section 2): If it can be short yet detailed, or if you need a strong defensive stance against prior work early.
- **End** (before Conclusions): If comparisons require your technical content, or if it can be summarized briefly in the Introduction. Can be titled "Discussion and Related Work."

**Methods/Approach**: Every section tells a story — the story of the results, NOT the story of how you arrived at them. Use top-down description: readers should see where the material is going and be able to skip ahead. Move gory details to appendices.

**Experiments**: Setup (datasets, metrics, baselines) → main results → ablations → analysis. Every claim needs quantitative evidence.

**Discussion**: Interpret results, compare to prior work, state limitations honestly. Limitations should be specific and actionable, not vague disclaimers.

**Conclusion**: Short summarizing paragraph. Do NOT repeat material from the Abstract or Introduction. Make original claims more concrete (e.g., reference quantitative results). Include future work as bullet list — if actively pursuing follow-up, say so to mark territory.

#### Writing Quality Rules

- Define all notation/terminology before use, only once. Group global definitions in Preliminaries.
- Do NOT use nonreferential "this", "that", "these", "it". Always specify the referent. BAD: "This is important because..." GOOD: "This accuracy gap is important because..."
- Do NOT use "etc." unless remaining items are completely obvious. BAD: "We measure volatility, scalability, etc." GOOD: "We measure volatility and scalability."
- Do NOT write "for various reasons" — state the actual reasons.
- "That" is defining, "which" is nondefining. "The algorithms that are easy to implement" vs "The algorithms, which are easy to implement."
- Use italics for definitions and quotes, not for emphasis. Context alone should provide emphasis.

### Figure Format

Figures use a hybrid marker + structured array approach. ALL figures are generated by a separate pipeline step using an AI image model — your `image_gen_detailed_description` is the ONLY input that model sees. It cannot read files or access data. Do NOT generate actual image files yourself (no matplotlib, no PIL, no image generation scripts).

**In paper_text**: Place `[FIGURE:fig_id]` markers where figures should appear.

**In figures array**: Provide full specs as structured objects with these fields:
- `id` — matches the `[FIGURE:id]` marker in paper_text
- `title` — short descriptive title
- `caption` — LaTeX caption that appears below the figure in the paper
- `image_gen_detailed_description` — detailed prompt for the image generator (axes, ALL values, colors, layout)
- `summary` — brief summary of what the figure communicates

Example in paper_text:
```
...our method achieves state-of-the-art results as shown below.

[FIGURE:fig_1]

The results in Figure 1 demonstrate...
```

Example figure spec in figures array:
```json
{"id": "fig_1", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers on JOB benchmark. RLQOpt achieves 2.3x speedup over PostgreSQL.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: ModelA=0.847, ModelB=0.762, Baseline=0.531. Error bars with std: 0.02, 0.03, 0.05. Sans-serif font, white background.", "summary": "Compares accuracy of proposed methods vs baseline."}
```

Every marker in text MUST have a matching figure in the array, and vice versa.

#### Data Precision Requirement

`image_gen_detailed_description` MUST include exact numbers from artifact output files. Read the actual output files before writing figure specs.

- BAD: "Compare accuracy metrics across configurations"
- GOOD: "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: K=3: 0.765, K=5: 0.729, Baseline: 0.121."

#### Figure vs Table Decision

Do NOT create figures for tabular data (rows/columns of text or numbers). Use `\begin{table}` in LaTeX instead. Figures are for actual visualizations only (charts, plots, diagrams).

#### Figure Placement Strategy

Be intentional with figure ordering. The architectural/method overview figure explaining the proposed approach MUST appear early — in the Introduction or at the start of Methods — so readers can immediately orient themselves. Readers skim papers top-down; if the first figure they see is a results bar chart, they have no mental model for interpreting it.

Recommended ordering:
1. **Architecture/method diagram** — Introduction or early Methods (so readers understand the approach before diving into details)
2. **Conceptual/analogy figures** — Introduction or Methods (to build intuition)
3. **Results figures** (bar charts, line plots, scatter plots) — Results section
4. **Analysis/ablation figures** — Discussion or later Results

#### Guidelines

- Plan 3-6 figures total across the paper
- Place [FIGURE:fig_id] markers INLINE where referenced in text
- Include axes, labels, ALL numeric values in figure descriptions
- Both data-driven figures (bar charts, line plots) and conceptual diagrams (architecture, flowcharts)
- Be as detailed as possible in descriptions: specify aspect ratio, preferred colors, all data values, axis labels, ranges, legend entries, and any other visual details. The more specific the description, the better the generated figure

### Bibliography with Semantic Scholar

Build `./references.bib` using the aii-semscholar-bib skill (real BibTeX from Semantic Scholar):

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in one batch
3. Write the returned .bib text into `./references.bib`

Rules:
- Do NOT fabricate BibTeX entries — always fetch from Semantic Scholar
- If a paper isn't found (very recent preprint), write the entry manually as fallback
- Use `\bibliography{references}` and `\bibliographystyle{plainnat}`
- Do NOT use inline `thebibliography` environment

### Citation Format (for Research Artifacts)

When writing research with numbered citations:

1. Every factual claim MUST have a numbered citation: `[1]`, `[2]`, `[1, 3]`, etc.
2. Each source in the "sources" array MUST have an "index" field
3. The index MUST EXACTLY MATCH citation numbers in the text
4. NEVER cite a number without a matching source index
5. Example: "LLMs show 40% improvement with multi-agent collaboration [1]."
````

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-08-14 05:49:38 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: Build bibliographies using Semantic Scholar. Batch-fetch BibTeX for papers by DOI, ArXiv ID, or title. Use when writing papers, generating reference lists, or building .bib files.
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar. Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Post-process** → fix entry type, fix citation key (AuthorYYYY), inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": ""}],
  "failed": []
}
```

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in **one call**
3. Save `bib_text` from the response to your `references.bib` file
4. Check `failed` — for any missed papers, follow the **fallback procedure** below

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract title, authors, year, venue, DOI/ArXiv ID
3. If DOI/ArXiv found → retry `aii_semscholar_bib__fetch` with it
4. Last resort: write BibTeX by hand using **only verified info from the actual paper page**

---

### CLI (for manual use / debugging)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````
