# Discussion: why W05/W05w does not fire on the GaMS Heretic trials

Date: 2026-10-20. Q&A between Drejc and Claude after scoring trial69 (see REPORT.md for the numbers).
No code was changed and nothing was run for this discussion; the paper text (paper_latex/paper.tex) was consulted.

Numbers referred to throughout (0-FP thresholds from Qwen3-14B, phi-4, Mistral-Nemo-12B):

| model | W05 (pooled) | W05w k=2 | W05w k=4 | k=2 median adjacent cos | longest run cos>0.9 |
|---|---|---|---|---|---|
| 0-FP threshold | -1.526 | -2.252 | -2.220 | | |
| GaMS3-12B original (parent) | -0.658 | -1.696 | -1.358 | 0.769 | 9 |
| GaMS3-12B trial98 (Heretic) | -1.241 | -1.697 | -1.421 | 0.958 | 15 |
| GaMS3-12B trial69 (Heretic) | -1.523 | -1.686 | -1.704 | 0.972 | 24 |
| phi-4 (clean negative) | -1.053 | -1.691 | -1.586 | 0.914 | 13 |

Heretic parameters: trial98 o_proj 1.20-1.36, down_proj 0.52-0.82; trial69 o_proj 1.39-1.44, down_proj 0.84-1.23,
direction_index 20.64. Per Abdul (who ran Heretic), only trial69 achieves a good abliteration (low refusal rate).

---

## Q1. Why does W05w work on the paper's 44 pairs but fail on this independent test? Am I reading the results wrong?

The reading is correct: none of the three GaMS checkpoints fires on any statistic. But "fails miserably" compares
against a claim the paper never makes, and the misses are the ones the paper predicts.

**What the paper claims.** The 44-checkpoint figure is where the *pooled* W05 fails (sensitivity 0.159). The windowed
W05w(k=2) reaches 0.70 on 50 real edited checkpoints. For the Heretic per-component class it catches 5 of 8. So three
of eight real Heretic checkpoints were already missed in the paper, and the text names the reason: completion failure.

**Why these two trials are invisible by construction.** The statistic reads how completely some matrix was annihilated
along the removed direction. For a projection at weight w the residual energy along that direction is (1-w)^2. The
paper's P4 result: a sub-unit uniform kernel at w=0.85 is undetected at every window size even though it un-censors
as well as the full edit. Both trials are in that regime or worse (residual energy 0.03-0.23 for trial98; 0.15-0.19 on
trial69's o_proj). The over-unit o_proj weights are the nasty part: over-projection re-injects energy along the
direction, so from the Gram's viewpoint o_proj was never removed. A k=2 window contains both o_proj and down_proj and
its minimum eigenvector is chosen by the *sum*; even where the down_proj tent passes near 1.0 (plausible in trial69),
the o_proj energy in the same window makes the removed direction lose to the parent's own intrinsic quiet directions.
That is why W05w(k=2) sits at the parent's value (layer-13 o_proj) for all three models. Windowing fixes discovery
failures caused by depth dilution; it cannot fix a kernel that never annihilates.

**Evidence the statistic works rather than being broken.** Pooled W05 tracks edit strength monotonically
(-0.66 -> -1.24 -> -1.52). In both Heretic models the pooled minimum direction moves from the parent's attention
matrices to mid-depth down_proj, where Heretic's tent peaks. Adjacent-window eigenvectors line up across 24
consecutive windows for trial69 versus 9 on the parent. The instrument found the direction, then reported the
completion level (about 3% of original energy), which is not deeper than three clean 12B models show intrinsically.

**Why this test is harder than the paper's panel, independently of Heretic.**
- Scale and lineage: the panel is <=4.2B. At 12B (d=3840) the clean negatives' windowed floor is -1.5 to -2.25, so an
  edit must push a window below -2.25, i.e. |1-w| < 0.075 for every matrix in the window.
- Only three negatives: the 0-FP threshold is set by a single model (Mistral-Nemo). trial69's pooled value is 0.003
  above it; with a properly fitted threshold it would be a coin flip, which is what a completion-boundary case looks like.
- The Gemma3 parent itself is deep at k=2 (-1.70), so there is little headroom; a reason to keep the no-Gemma-negatives
  rule, but also a larger margin to clear than on a Qwen host.

Summary for the write-up: W05w generalises to Heretic outputs whose weights reach 1.0 somewhere; the paper's 0.625 recall
on that class already encodes that. These two trials are an out-of-sample confirmation of the completion boundary, not a
counterexample. A test that bears on the windowing claim would be a Heretic trial whose o_proj and down_proj ranges both
include 1.0, or a sub-unit sweep like P4 on this host.

---

## Q2. The abstract only names the sub-unit uniform kernel and the Householder edit, not Heretic. Shouldn't Heretic be detectable? And the eigenvector line-up (24 vs 9) looks easily detectable; what does "adjacent eigenvectors line up" mean? Is that GaMS-specific, Heretic-specific, or general? Would a different abliteration on the same GaMS be caught?

**Is Heretic supposed to be detectable?** Partly, and the paper says so in the body rather than the abstract. On 8 real
Heretic checkpoints W05w(k=2) catches 5; the in-house Heretic tent kernel is caught at the pre-registered threshold. So
Heretic is "detectable when its sampled weights reach 1.0 somewhere", not detectable as a class. The abstract's
"sub-unit uniform kernel" is the clean analytic case of the completion boundary; a Heretic tent whose weights never touch
1.0 is the same mechanism in non-uniform form (that extrapolation is Claude's, not a sentence in the paper). P4 at
w=0.85 has perfect discovery (cos 0.999 to the removed direction) and is still invisible, which is the pattern here.
The two Pareto trials both landed off 1.0 on every matrix: chance from the Optuna search, or simply where the
KL-vs-refusal trade-off lands on this model. Either way it is the conceded boundary.

**What "adjacent eigenvectors line up" means.** Each window of 2 layers has a quietest direction: the single direction
in the 3840-dim residual space along which those layers write the least. In a clean model that is whatever weak spot
those two layers happen to have, so window 13's and window 14's quietest directions are unrelated and their cosine
(1 = identical, 0 = perpendicular) is low. An abliteration removes one shared direction from a whole band of layers, so
every window in the band has the same quietest direction and the cosines stay near 1 in a long unbroken run: 24
consecutive windows above 0.9 on trial69 versus 9 on the parent. The paper already has a consistency term, but it is the
*minimum* cosine over all windows, which is near 0 for every model here and carries nothing. Run length or median is a
different, discovery-only reading of the same numbers.

**Is it easily detectable?** Not yet, because of phi-4: a clean phi-4 has median cosine 0.914 and a run of 13, so
trial98's 15 is barely above a clean model; only trial69's 24 separates. Clean models can have one structurally quiet
direction across many layers (e.g. an outlier channel). With 3 negatives no threshold can be set. The right next step is
a re-analysis: score run length on the paper's 57 wild negatives and 50 positives from existing caches.

**How general would that reading be?**
- Works for any recipe that removes one direction, fully or partially, from a contiguous band of a few layers or more:
  Heretic, uniform sub-unit kernels, Gaussian-depth, partial-layer. It is a discovery signal, so completion no longer matters.
- Fails for Householder edits: a reflection rotates every window's eigenvector by the same map, cosines between rotated
  vectors are unchanged, so the paper's invisibility proof covers this reading too.
- Weak or absent for SFT uncensoring (no direction removed) and for recipes with a different direction per layer.
- Not specific to GaMS; specific to "one direction, many layers".

**Would a different abliteration on the same GaMS be caught by W05w as it stands?** Yes for the standard recipes,
because they annihilate at weight 1.0. A classic uniform projection on every layer drives each matrix's energy along the
removed direction to about 1e-4, so W05w lands near -4 against a cutoff of -2.25; even pooled W05 would fire since the
edit is not depth-localised. A partial-layer or Gaussian-depth edit with peak weight 1.0 over >=2 layers is caught by the
windowed form (0.80 on real partial-layer checkpoints). Another Heretic run would be a coin flip, as in the paper.
Remaining caveats for this host: the thin negative panel, and the Gemma3 parent already at -1.70 at k=2; a weight-1.0
edit clears the margin by two orders of magnitude regardless.

---

## Q3. What does "weights equal 1.0" have to do with our method? Maybe I don't understand how W05w works. (Also: Abdul says only trial69 is a good abliteration, so the line-up might be a good metric despite phi-4.)

W05w measures silence, and the weight w controls how silent the edit makes a matrix.

**What an abliteration does to one matrix.** The edit replaces W with W minus w times the part of W that writes along
the refusal direction r. After the edit the matrix still writes along r, scaled by (1-w):

| weight w | amplitude left along r | energy left (1-w)^2 | log10 |
|---|---|---|---|
| 1.00 | 0 | ~0 | -4 or lower |
| 0.85 | 0.15 | 0.023 | -1.6 |
| 0.82 (trial98 down_proj max) | 0.18 | 0.032 | -1.5 |
| 0.52 (trial98 down_proj min) | 0.48 | 0.23 | -0.6 |
| 1.40 (trial69 o_proj) | -0.40, sign flipped | 0.16 | -0.8 |

Only w=1 silences the matrix. Anything else turns the volume down; anything above 1 turns it down and flips it, which
the energy cannot distinguish from turning it down.

**What W05w reads.** For each window of k layers it builds the summed Gram (a table of how loudly those layers write in
every direction) and finds the quietest direction. Then, for each matrix in the window, it asks how much energy that
matrix writes along that direction relative to a random direction. The score is the smallest such energy, in log10:
"how silent is the most silent matrix, along the window's quietest direction". The threshold -2.25 means energy below
0.0056, i.e. amplitude below about 7.5%.

**Why that makes w the whole story.** A matrix edited at weight w has energy (1-w)^2 along r. To clear -2.25 you need
|1-w| < 0.075. No window choice changes that, because windowing only changes which direction is found, not how much the
matrix was turned down. trial69's deepest possible value, if the window found r perfectly, is around -1.6 (down_proj at
w=0.84). A clean 12B model already has directions at 2-3% energy (parent -1.70, Mistral-Nemo -2.25), so a 3% residual
sits inside the clean range. The paper's sub-unit kernels at 0.5, 0.7, 0.85 are this same table.

**On the line-up as a metric.** Line-up asks a different question: is the same direction turned down across many
consecutive layers, regardless of how much. That is why trial69 shows it strongly (24 windows over its 27-layer band) and
trial98's shorter run goes with the weaker edit Abdul reported. Two cautions: (1) it still needs a real negative panel,
since phi-4 at run 13 shows a clean model can have a persistent quiet direction; (2) it measures "an edit is present and
spans many layers", not refusal rate. The paper shows the weight verdict and behaviour dissociate in both directions, so
the match with Abdul's refusal numbers is a two-point observation, not a claim.

---

## Q4. Is it right to say (simplified) that W05w looks for a direction that is abnormally quiet? What are discovery, completion, and the third term? Heretic uses Optuna TPE to search intervention settings instead of the same direction and strength everywhere; shouldn't the line-up then fail, since it looks for the exact same direction silenced across layers?

**Yes, the simplification is right.** W05w asks: is there a direction along which some layer writes abnormally little?
"Abnormally" means quieter than the quietest directions of clean models, which is what the negatives' threshold encodes.
The refinement: the direction is chosen by the window (quietest direction of a few neighbouring layers), and the score
is the single quietest matrix along it.

**Discovery and completion.**
- Discovery: does the statistic find the removed direction at all, i.e. does the window's quietest direction point along
  the direction the editor removed? Pooling over all layers breaks this when the edit is depth-localised (untouched
  layers drown it out). Windowing exists to repair discovery.
- Completion: given the direction, how silent did the edit make some matrix along it, i.e. the (1-w)^2 table. Section 3
  of the paper shows that once discovery holds, W05 equals the completion quantity up to a small bound, so the score *is*
  the completion. No window choice touches it.
- Consistency (probably the third term): the paper's gate requiring adjacent windows' quietest directions to agree,
  measured as the minimum cosine over all windows. Same idea as the line-up, but the minimum over all windows is near zero
  for every model, so it carries nothing here; run length or median reads much better. (If the third term meant was
  "isometric": that is the Householder boundary, a reflection changes nothing about how quiet any direction is.)

**Heretic and TPE.** TPE searches across *trials*, not across layers. One trial has one direction, given by its single
direction_index (20.64 here, the refusal direction measured around layer 20), applied to every layer in the band with a
strength that varies by depth along the tent. So within trial69 the same direction is turned down at every edited layer,
by different amounts. The line-up is blind to the amount and sensitive to the sameness, which is exactly this situation.
TPE varies which direction index, peak position and strengths get picked between trial69 and trial98, not within either.
Refinements: methods that compute a separate direction per layer would weaken the line-up but not kill it (refusal
directions in neighbouring mid layers are highly similar; the paper cites delta forensics finding cosine 0.997 between two
recipes' directions on one base); and a clean model can have one direction quiet across many layers for structural
reasons (phi-4), so the line-up is strong evidence of an edit, not proof, and the cutoff must come from a negative panel.

---

## Q5. Why would the one annihilated direction coincide with the lowest eigenvector?

Because "lowest eigenvector" and "quietest direction" are the same thing by definition, not by coincidence.

**The Gram is an energy meter.** For a window, the summed Gram A is built so that for any unit direction u, u^T A u is
the total energy the window's matrices write along u. Each term is the squared length of u^T W divided by the matrix's
total size: non-negative, and zero only if that matrix writes nothing along u.

**The smallest eigenvector is the minimiser of that meter.** For a symmetric matrix the eigenvectors are the principal
axes of the quadratic form u^T A u, and the smallest eigenvalue is the smallest value that form takes over unit vectors
(Rayleigh quotient). The direction that makes u^T A u smallest is exactly the eigenvector of the smallest eigenvalue.
Asking for the lowest eigenvector is asking "along which direction does this window write the least?"

**Put in an annihilated direction.** If every matrix in the window had its component along r removed at weight 1, each
matrix writes zero along r, so r^T A r = 0. Energies cannot go below zero, so no direction can beat r: r is the smallest
eigenvector with eigenvalue zero (up to floating point). That is discovery holding.

**When it does not coincide** (the two failure modes):
- Only some matrices in the window were edited, or the window is the whole stack: r^T A r is the energy the untouched
  matrices still write along r, which can exceed some intrinsically quiet direction's total. The quietest direction is
  then that intrinsic one and r is never looked at. This is the pooling failure windowing fixes.
- The edit was partial (w off 1): r^T A r is (1-w)^2 times the original, roughly 0.03-0.2 here, competing with the
  model's born-in quiet directions at about 0.02. Sometimes r still wins the window (trial69's eigenvectors line up across
  24 windows), but the score read along it is then only -1.5 to -1.7, inside the clean range. Discovery held, completion failed.

So the eigenvector method finds the direction exactly when the edit made r the globally quietest direction within the
window. A weight-1 edit on all the window's matrices guarantees that; anything weaker is a contest against the model's
own quiet directions.

---

## Open items (not done, not committed)
- Fit a cutoff for the adjacent-eigenvector run length / median on the paper's 57 wild negatives and 50 positives
  (re-analysis of existing caches); report it as a discovery-only companion to W05w, not a safety score.
- If more GaMS Heretic trials exist, prefer one whose o_proj and down_proj weight ranges both include 1.0, to test the
  windowing claim rather than the completion boundary.
- All results in this folder are uncommitted by request.
