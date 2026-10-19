URL: https://huggingface.co/blog/grimjim/norm-preserving-biprojected-abliteration
Type: HTML
Length: 28234 chars

--- Content ---

[ Hugging Face](/)

  * [ Models ](/models)
  * [ Datasets ](/datasets)
  * [ Spaces ](/spaces)
  * [ Buckets new](/storage)
  * [ Docs ](/docs)
  * [ Enterprise ](/enterprise)
  * [Pricing](/pricing)
  *     * Website

      * [ Tasks](/tasks)
      * [ HuggingChat](/chat)
      * [ Collections](/collections)
      * [ Languages](/languages)
      * [ Organizations](/organizations)
    * Community

      * [ Blog](/blog)
      * [ Posts](/posts)
      * [ Daily Papers](/papers)
      * [ Hardware](/hardware)
      * [ Learn](/learn)
      * [ Discord](/join/discord)
      * [ Forum](https://discuss.huggingface.co/)
      * [ GitHub](https://github.com/huggingface)
    * Solutions

      * [ Team & Enterprise](/enterprise)
      * [ Hugging Face PRO](/pro)
      * [ Enterprise Support](/support)
      * [ Inference Providers](/inference/models)
      * [ Inference Endpoints](/inference-endpoints)
      * [ Storage Buckets](/storage)

  * * * *

  * [Log In](/login)
  * [Sign Up](/join)



[ Back to Articles](/blog)

#  Norm-Preserving Biprojected Abliteration 

[ Community Article](/blog/community)

Published November 6, 2025

[ Upvote 91 ](/login?next=%2Fblog%2Fgrimjim%2Fnorm-preserving-biprojected-abliteration)

  * [](/victor "victor")
  * [](/pearsonkyle "pearsonkyle")
  * [](/diwank "diwank")
  * [](/s0me-0ne "s0me-0ne")
  * [](/mehmet582025 "mehmet582025")
  * [](/etomoscow "etomoscow")
  * +85



[](/grimjim)

[Jim Lai grimjim Follow ](/grimjim)

  * A Refined Mathematical Intervention
  * Sample PyTorch implementation
  * Layer Selection Methodology
  * Result
  * Discussion
  * References



Abliteration is a technique for removing refusal behaviors from language models by identifying and intervening on "refusal directions" in activation space, notionally represented via a single mean refusal direction. This finding has been useful in mechanistic interpretability.

We recently presented a refinement called "projected abliteration" that improves upon the conventional approach by removing only the mechanistically relevant components of the refusal direction, confirming a prior finding that LLMs encode refusal and harmfulness separately. After that, we further refined the technique to "biprojected abliteration", which also removed the corresponding component when removing refusal measured using one layer from another layer entirely; in principle this would avoid disturbing the harmless direction of any layer targeted for intervention. Interestingly, some safety refusal came back.

Upon further consideration, there remained an issue with regard to layer weight modification and weight norms.

In conventional (and our previously modified) abliteration, the normalized refusal direction is subtracted from the layer's residual streams targeted for intervention, specifically _self_attn.o_proj_ and _mlp.down_proj_. Although this is effective in practice for steering, it is mathematically unprincipled because:

  * the direction removed contains a unit magnitude component in addition to the directional component, complicating interpretation,
  * the removal does not respect the relative importance of neurons, resulting in unpredictable scale effects, and
  * disturbs the geometry of the weight matrix in unpredictable ways.



Contrary to conventional wisdom that abliteration significantly degrades model capabilities, our norm-preserving approach improved reasoning performance over the baseline model (NatInt: 21.33 vs 18.72), while achieving effective refusal removal (UGI: 32.61 vs 19.58).

##  A Refined Mathematical Intervention 

Instead of subtracting the refusal direction from the target weights, we propose subtracting only the directional component while preserving the norm of the weights.

Applying norm-preservation is more respectful of existing layer normalization by maintaining the relative activation scale structure that the model's normalization layers were trained to expect. We should therefore expect some improvement over naive abliteration with regard to reducing incidental damage to reasoning. Furthermore, the ablation can still be performed as a rank-1 modification, keeping the overall approach computationally efficient.

Given:

  * Weight matrix $\mathbf{W} \in \mathbb{R}^{d_{\text{out}} \times d_{\text{in}}}$
  * Refusal direction $\mathbf{r} \in \mathbb{R}^{d_{\text{out}}}$ (refined via biprojection)
  * Scaling factor $\alpha \in [0, 1]$



**Step 1: Normalize the refusal direction**

r^=r∥r∥2\hat{\mathbf{r}} = \frac{\mathbf{r}}{\|\mathbf{r}\|_2}r^=∥r∥2​r​

**Step 2: Decompose weight matrix into magnitude and direction**

For each row $i$ of $\mathbf{W}$:

mi=∥Wi,:∥2m_i = \|\mathbf{W}_{i,:}\|_2mi​=∥Wi,:​∥2​

W^i,:=Wi,:∥Wi,:∥2\hat{\mathbf{W}}_{i,:} = \frac{\mathbf{W}_{i,:}}{\|\mathbf{W}_{i,:}\|_2}W^i,:​=∥Wi,:​∥2​Wi,:​​

Or in matrix form: M=diag(∥W1,:∥2,…,∥Wdout,:∥2)\mathbf{M} = \text{diag}(\|\mathbf{W}_{1,:}\|_2, \ldots, \|\mathbf{W}_{d_{\text{out}},:}\|_2)M=diag(∥W1,:​∥2​,…,∥Wdout​,:​∥2​)

W^=M−1W\hat{\mathbf{W}} = \mathbf{M}^{-1}\mathbf{W}W^=M−1W

**Step 3: Ablate refusal direction from the normalized directional component**

Compute projection coefficients (alignment of each input dimension with refusal): p=r^TW^∈Rdin\mathbf{p} = \hat{\mathbf{r}}^T \hat{\mathbf{W}} \in \mathbb{R}^{d_{\text{in}}}p=r^TW^∈Rdin​

Remove the refusal component via rank-1 update: W^ablated=W^−α⋅r^pT\hat{\mathbf{W}}_{\text{ablated}} = \hat{\mathbf{W}} - \alpha \cdot \hat{\mathbf{r}} \mathbf{p}^TW^ablated​=W^−α⋅r^pT

Renormalize each row to unit length, to enable recombination with original magnitudes: W^new=normalize(W^ablated,dim=1)\hat{\mathbf{W}}_{\text{new}} = \text{normalize}(\hat{\mathbf{W}}_{\text{ablated}}, \text{dim}=1)W^new​=normalize(W^ablated​,dim=1)

**Step 4: Recombine with original magnitudes**

Wnew=MW^new\mathbf{W}_{\text{new}} = \mathbf{M} \hat{\mathbf{W}}_{\text{new}}Wnew​=MW^new​

This ensures that $|\mathbf{W}_{\text{new}, i,:}|_2 = |\mathbf{W}_{i,:}|_2$ for all rows $i$, preserving the learned importance structure while redirecting computation away from the refusal direction.

##  Sample PyTorch implementation 
    
    
    import torch
    
    # Core implementation (excerpt from complete function)
    """
        Args:
            W: Weight matrix of shape [out_features, in_features]
            refusal_dir: Refusal direction vector of shape [out_features]
            scale_factor: Scaling factor for ablation strength (default: 1.0)
    """
    
            # Normalize refusal direction
            refusal_normalized = torch.nn.functional.normalize(refusal_dir, dim=0)
    
            # Decompose weight matrix
            W_norm = torch.norm(W, dim=1, keepdim=True)  # [out_features, 1]
            W_direction = torch.nn.functional.normalize(W, dim=1)  # normalized per output neuron
        
            # Apply abliteration to the DIRECTIONAL component
            projection = torch.matmul(refusal_normalized, W_direction)  # [in_features]
            W_direction_new = W_direction - scale_factor * torch.outer(refusal_normalized, projection)
        
            # Re-normalize the adjusted direction to enable recombination
            W_direction_new = torch.nn.functional.normalize(W_direction_new, dim=1)
        
            # Recombine: keep original magnitude, use new direction
            W_new = W_norm * W_direction_new
    

##  Layer Selection Methodology 

We measured refusal directions across all layers but required a principled approach to select which measurements to use for intervention. Our selection employed a composite quality metric combining three factors:

**Signal-to-noise ratio (SNR)** : The magnitude of the refusal direction relative to the mean activations:
    
    
    snr = ||r|| / max(||harmful_mean||, ||harmless_mean||)
    

where the refusal direction $\mathbf{r} = \text{harmful_mean} - \text{harmless_mean}$.

**Cosine dissimilarity** : The angular separation between harmful and harmless activation means:
    
    
    dissimilarity = 1 - cosine_similarity(harmful_mean, harmless_mean)
    

Higher values indicate more distinct representational geometry.

**Composite quality score** :
    
    
    quality = snr × (1 - cos_sim)
    

By charting these metrics across all layers, we selected candidates exhibiting both high SNR and strong cosine dissimilarity, with particular attention to layers showing sharp changes in these metrics. The suitability of a selected refusal direction for application to nearby and preceding layers was informed by tracking the cosine similarity evolution of refusal directions across consecutive layers—stable directional alignment suggested robust cross-layer applicability.

This approach is admittedly heuristic, but grounded in the observed geometric structure of refusal representations. Future work might formalize optimal layer selection through systematic ablation studies.

This heuristic is computationally efficient: a single inference pass captures activations across all layers, and quality metrics are computed post-hoc from this data. Unlike iterative search approaches that require multiple model evaluations, the analysis adds negligible overhead to the standard abliteration workflow, merely extracting more signal from measurements already performed.

For Gemma3 12B Instruct, with layers numbered [0..47], we picked the measurements from layers 23 and 29 for broad application. Keeping the refusal and mean harmless direction measurements proved to be vital in subsequent refinements

##  Result 

With this revised method, we abliterated Gemma3 12B Instruct yet again. As before, we applied a default scale factor of 1.0, intervening on layers [11..41]. As expected, we were able to bypass refusal with harmful test prompts. The model retained more of its capabilities in informal testing, and "grimjim/gemma-3-12b-it-norm-preserved-biprojected-abliterated" scored highest on the UGI and NatInt benchmarks on the [UGI Leaderboard](https://huggingface.co/spaces/DontPlanToEnd/UGI-Leaderboard) compared to our prior published abliteration variants for the same baseline model, and the baseline Instruct model itself.

As before, during measurement of activations, magnitude sparsification at 0.995 strength was applied when obtaining measurements from prompts. This was necessary to distinguish the refusal direction between the mean harmful and harmless directions. The empirical observation was that strong outlier activations characterize the model.

To maximize numerical stability, we continued to employ 32-bit floating point throughout for intermediate calculations even though the model was released in 16-bit bfloat16 floating point format. It was previously noted that performing intermediate calculations in 16-bit bfloat16 led to suboptimal results. We recommend that at least 32-bit floating point be employed in models which evince a large variance in activation magnitudes.

##  Discussion 

By successfully narrowing down the intervention to only the directional component with preserved norms, we establish that refusal direction alone is critical to abliteration outcomes, rather than refusal direction entangled with magnitude effects. However, despite this theoretical grounding, it remains probable that removing even the directional component entangled with harmfulness assessment could reduce safety in unprincipled ways. Korznikov et al. (2025) demonstrated that activation steering on even benign features can compromise LLM safety, suggesting that interventions in representational space may have unintended consequences for safety mechanisms.

Preserving the magnitude was likely important in the case of [Gemma3 12B Instruct](https://huggingface.co/google/gemma-3-12b-it), given that high magnitude outliers obscured the underlying refusal direction almost certainly encode important behavioral information that should be preserved in order to retain functionality, as reported by Sun et al. (2024).

Benchmark results on the [UGI Leaderboard](https://huggingface.co/spaces/DontPlanToEnd/UGI-Leaderboard) demonstrated clear improvements over prior abliteration variants:

Model Variant | UGI Score | NatInt Score  
---|---|---  
Gemma-3 12B Instruct (baseline) | 19.58 | 18.72  
Standard abliterated | 32.08 | 18.64  
Norm-preserved biprojected | **32.61** | **21.33**  
  
Notably, while standard abliteration achieved comparable uncensoring (UGI scores), it showed slight capability degradation (NatInt: 18.64 vs baseline 18.72). The norm-preserving approach not only matched the uncensoring effectiveness but significantly improved reasoning capability (NatInt: 21.33). This finding aligns with recent observations of a 'Safety Tax' phenomenon (Huang et al., 2025), where safety alignment has been shown to degrade reasoning capabilities in language models. The improvement over baseline suggests that removing directionally-encoded safety constraints may unlock latent reasoning capabilities that were suppressed by safety mechanisms, though this relationship warrants further investigation.

Although we had previously empirically established that intervention on multiple layers was required to achieve the desired rate of compliance to harmful prompts, we found theoretical grounding in a 2023 paper by McGrath et al. titled "The Hydra Effect: Emergent Self-repair in Language Model Computations". The authors demonstrated that when individual layers are ablated, other layers adaptively compensate to restore approximately 70% of the original computation. This self-repair mechanism explains why single-layer interventions generally prove insufficient for robust abliteration, as the model inherently routes around localized damage.

A multi-layer intervention strategy directly addresses this challenge: by simultaneously modifying both attention output projections and MLP down projections across multiple layers, one can effectively "cut multiple heads of the hydra" at the same time, preventing the compensatory mechanisms from restoring refusal behavior. Via judicious selection of layer measurements and a set of intervention layers, a structured rank-2L intervention (where L is the number of targeted layers) can provide sufficient coverage to overcome emergent self-repair while remaining computationally efficient through localized rank-1 updates at each weight matrix. This "hydra effect" in retrospect accounted for the partial return of safety refusals during "biprojected abliteration".

We restructured the traditional abliteration pipeline into three distinct phases: (1) measurement across all layers, (2) analytical layer selection via quality metrics, and (3) targeted intervention on selected layers. This separation provides flexibility: rather than committing to a single 'best' layer, practitioners can select multiple high-quality candidates for intervention, enabling the multi-layer strategy necessary to overcome the hydra effect while maintaining computational efficiency through the rank-1 structure of each individual weight modification.

Finally, an interesting practical consequence emerges from this understanding: the number of intervention layers provides a crude but effective mechanism for regulating the compliance-safety tradeoff. Fewer layers allow more self-repair, preserving some refusal capability, while more layers overcome the compensatory mechanisms more thoroughly. This provides practitioners with a tunable parameter for calibrating model behavior according to their use case and risk tolerance.

##  References 

  * [Arditi et al, "Refusal in LLMs is mediated by a single direction", lesswrong.com, 2024.](https://www.lesswrong.com/posts/jGuXSZgv6qfdhMCuJ/refusal-in-llms-is-mediated-by-a-single-direction)
  * [Huang et al, "Safety Tax: Safety Alignment Makes Your Large Reasoning Models Less Reasonable", arXiv preprint, 2025](https://arxiv.org/abs/2503.00555)
  * [Korznikov et al, "The Rogue Scalpel: Activation Steering Compromises LLM Safety", arXiv preprint, 2025](https://arxiv.org/abs/2509.22067)
  * [Labonne, "Uncensor any LLM with abliteration", huggingface.co, 2024.](https://huggingface.co/blog/mlabonne/abliteration)
  * [Lai, "Projected Abliteration", HuggingFace article, 2025](https://huggingface.co/blog/grimjim/projected-abliteration)
  * [McGrath et al, "The Hydra Effect: Emergent Self-repair in Language Model Computations", arXiv preprint, 2023](https://arxiv.org/abs/2307.15771)
  * [Sun et al,, "Massive Activations in Large Language Models", arXiv preprint, 2024](https://arxiv.org/abs/2402.17762v2)
  * [Zhao et al, "LLMs Encode Harmfulness and Refusal Separately", arXiv preprint, 2025.](https://arxiv.org/abs/2507.11878)



_Initial publication date: November 6, 2025._

##  Models mentioned in this article 1

#### [google/gemma-3-12b-it Image-Text-to-Text • 12B • Updated Mar 21, 2025 • 1.23M • 806 ](/google/gemma-3-12b-it)

##  Spaces mentioned in this article 1

[ Running  1.96k UGI Leaderboard 📢 1.96k Uncensored General Intelligence Leaderboard ](/spaces/DontPlanToEnd/UGI-Leaderboard)

More from this author

## [ORBA: Orthogonal Reflection Bounded Ablation — A Geometrically Exact Detour in Directional Activation Editing

  *   * 
7 March 25, 2026 ](/blog/grimjim/orthogonal-reflection-bounded-ablation)

## [DeLERP: Decomposed Linear Interpolation for Model Merging

  *   * 
8 November 20, 2025 ](/blog/grimjim/delerp-merge-method)

### Community

[grimjim](/grimjim)

Article author  Nov 7, 2025

•

edited Nov 7, 2025

In retrospect, a key insight to this approach was to treat the harmless direction as a boundary condition to clamp to. Both the removal of projected interference along the harmless direction and the preservation of per element magnitudes aimed to minimize perturbation along and near the harmless direction.

Activation measurements were done on a 4-bit bitsandbytes quant, but final assembly was performed on the full-weight bfloat16 model.

See translation

  * [](/ItzPingCat "ItzPingCat")
  * 1 reply

·

🚀

1

1

+

[ItzPingCat](/ItzPingCat)

Nov 11, 2025

GPT OSS when

[SeaJay20k](/SeaJay20k)

Nov 16, 2025

Really cool stuff! I look forward to your future worl

See translation

Reply

[teknium](/teknium)

Nov 29, 2025

Any codebases exist for this? ^_^

See translation

  * [](/Nabbers1999 "Nabbers1999")
  * 1 reply

·

[Nabbers1999](/Nabbers1999)

Nov 30, 2025

<https://github.com/jim-plus/llm-abliteration/>

See translation

[p-e-w](/p-e-w)

Jan 8

> After that, we further refined the technique to "biprojected abliteration", which also removed the corresponding component when removing refusal measured using one layer from another layer entirely; in principle this would avoid disturbing the harmless direction of any layer targeted for intervention.

Does this mean that the refusal direction is computed globally (by choosing a reference layer), but the harmless direction is computed per-layer?

If so, what is the reasoning behind this? Why would we expect refusal semantics to be universal in residual space, but harmfulness semantics to be local to each transform?

See translation

  * [](/Nabbers1999 "Nabbers1999")
  * 1 reply

·

[Nabbers1999](/Nabbers1999)

Jan 26

I feel like your question didn't get fully expanded on but from what I understand, yes, refusal direction should be very similar from one layer to another as it is usually a semantically similar output - ie "I can't answer this." When faced with harmful prompts, the moment a model decides a prompt is harmful it follows a similar trajectory regardless of if it's self-harm, racism, or hurting people. Models are lazy (another word for efficient) so when they learn a common response to multiple prompts they tend to create a single shared path to get them there which is the refusal direction we're trying to orthogonalize. It can be a little more difficult to isolate in models with a more expansive refusal - models such as Olmo don't just refuse, they explain why and maybe even offer a support hotline suggestion. But with a harmless prompt each layer contributes a different component of the final output leading to different vectors per layer.

In a Transformer, the residual stream acts like a "shared bus" (like in a computer). Information is written to it and read from it by every layer.  
​Refusal is a "Flag": Once a middle layer decides "This is bad," it writes a "REFUSE" flag to that shared bus. Subsequent layers read that flag and maintain it. That’s why the direction is universal—it's a persistent state.  
​Harmlessness as "Computation": Harmless prompts don't set a single "flag." Instead, the layers are busy doing math: Layer 2 is doing grammar, Layer 8 is doing logic, Layer 15 is doing factual retrieval. Each of those "useful" vectors looks completely different because the task of the layer changes as you go deeper.

Think of the Refusal Direction like a 'Stop' sign. Whether it’s at the beginning, middle, or end of a road trip, that sign always means the same thing, so the model uses a 'universal' vector to represent it across the whole residual stream. It’s efficient—the model doesn’t need to reinvent 'No' at every layer.  
​However, Harmlessness (or general capability) is more like the actual driving. At one point you’re steering, then you’re shifting gears, then you’re checking the map. Each layer is doing a different specific job to build the final answer. Because the work changes at every layer, the 'direction' of that useful work is local and unique to that layer. Biprojected abliteration basically says: 'I’m going to take down that Stop sign, but I’ll make sure I don’t accidentally bump the steering wheel or the gear shift while I'm doing it.

See translation

[grimjim](/grimjim)

Article author  Jan 9

Activations are measured for all layers in one pass, as the cost is only a bit more RAM to hold the results; no significant cost in inference time. This is done for measuring compliance and refusal activations. Directional difference is computed within each layer.

For intervention/ablation, the YML file allows an N-to-M mapping. I can pick 3-4 (notionally high relevance) layer measurements to apply to sequential chunks, with the heuristic that the source measurement layer being closer to the target intervention layer will hopefully limit unwanted side-effects. One could apply each refusal measurement to the same layer, but that approach doesn't provide the most effective ablation in my experience. There's something deeper going on which I've not yet been able to characterize.

See translation

👀

1

1

+

Reply

[Goekdeniz-Guelmez](/Goekdeniz-Guelmez)

Jan 26

Great work!

this is better then my layer selection strategy, which relied on a single scalar separability metric based on the Euclidean distance between the mean hidden activations of harmful and harmless prompts at each layer. While effective as a first-order signal, this criterion has several limitations like: metric is scale-sensitive, ignores angular structure, cross-layer directional stability, etc. Can I use your layer selection for my new Gabliteration version (code/paper).

See translation

Reply

[grimjim](/grimjim)

Article author  Jan 28

•

edited Jan 28

I should get around to documenting my layer selection choice on the relevant model card, which was admittedly empirical and bespoke.

I should have taken better notes regarding my final Gemma 3 12B work, but it appears that I took the measurement from layer 29 (which looked good in charting) and ablated it from layers 11-41, scale 1 throughout; I threw in sparsity 0.001 to layers 35-41, but that may have not have been necessary. Geometric preservation allowed the model to retain most of its knowledge despite the extent of intervention.

Let me know whenever you make your paper available. I'd be interested to see your findings!

See translation

  * [](/Nabbers1999 "Nabbers1999")
  * 1 reply

·

🧠

1

1

+

[Nabbers1999](/Nabbers1999)

Jan 28

I had just gone with the assumption that the yaml you included as an example with your git code was the settings you had used. I ended up doing the 27B and then I ran measurements on the 12B to compare to your yaml and it was pretty similar except that - it's been a minute but I think the 12B had three "chunks" where a strong signal measurement needed applied to the previous few layers and the 27B had, I think it was four. 

Since then I meddled a bit with a couple of Qwen Coders (dense nonthinking) and have leaned into taking the strongest signal measurement and applying it to the layers where harmful to harmless begins to drop. On those I found the deccp flag didn't really make much of a difference. 

And I've also started following this sort of abliteration with a DoRA training on toxic SFT to solidify, which is how I got my 27B to stop occasionally complaining about things it wanted to refuse. 

See translation

[grimjim](/grimjim)

Article author  Jan 29

The yaml included was accurate then. Layer 27 was from an early attempt. The viability of applying refusal measurements to chunks of layers suggests that a signal processing view involving key layers could be a useful framing. Applying refusal direction on a per layer basis underperformed in my experiments.

I expect the deccp dataset seems to be only useful against a subset of refusals, though I didn't test that edge case as it was inhereted from the codebase I started from. Validating that the entries are refused by a particular Chinese model and culling those that pass would be a more targeted approach, as nonrefusals would dilute the refusal direction.

Fine-tuning is a well-established way to smooth over damage resulting from ablation. I'm curious why you picked DoRA.

See translation

  * [](/Nabbers1999 "Nabbers1999")
  * [](/grimjim "grimjim")
  * 3 replies

·

[Nabbers1999](/Nabbers1999)

Feb 1

My main thinking in using DoRA was that - like our norm-preserved abliteration - it also decomposes the updates into magnitude and direction. Since we’ve already orthogonalized the refusal vector, I want to make fine adjustments to the direction (to reinforce the removal) without accidentally drifting the layer norms.

With standard LoRA, magnitude and direction are entangled. With DoRA, I can focus the training on the directional component to align with booting the refusal vector, while explicitly constraining the magnitude scalar to stay close to pretrained norms. My hypothesis is that this should minimize the risk of damaging the model’s general capabilities (layer strength drift).

As an aside, I handle training via my own Python scripts (unsloth/trl) rather than standalone trainers like Axolotl. This allows me to manually manipulate the magnitude and direction components separately—specifically to dampen the magnitude updates during the SFT phase.

See translation

Expand 2 replies

EditPreview

Upload images, audio, and videos by dragging in the text input, pasting, or clicking here.

Tap or paste here to upload images

Comment

· [Sign up](/join?next=%2Fblog%2Fgrimjim%2Fnorm-preserving-biprojected-abliteration) or [log in](/login?next=%2Fblog%2Fgrimjim%2Fnorm-preserving-biprojected-abliteration) to comment

[ Upvote 91 ](/login?next=%2Fblog%2Fgrimjim%2Fnorm-preserving-biprojected-abliteration)

  * [](/victor "victor")
  * [](/pearsonkyle "pearsonkyle")
  * [](/diwank "diwank")
  * [](/s0me-0ne "s0me-0ne")
  * [](/mehmet582025 "mehmet582025")
  * [](/etomoscow "etomoscow")
  * [](/DeathGodlike "DeathGodlike")
  * [](/Rhuan "Rhuan")
  * [](/erus556 "erus556")
  * [](/phi0112358 "phi0112358")
  * [](/dissociativity "dissociativity")
  * [](/teknium "teknium")
  * +79



##  Models mentioned in this article 1

#### [google/gemma-3-12b-it Image-Text-to-Text • 12B • Updated Mar 21, 2025 • 1.23M • 806 ](/google/gemma-3-12b-it)

##  Spaces mentioned in this article 1

[ Running  1.96k UGI Leaderboard 📢 1.96k Uncensored General Intelligence Leaderboard ](/spaces/DontPlanToEnd/UGI-Leaderboard)

System theme

Company

[TOS](/terms-of-service) [Privacy](/privacy) [About](/huggingface) [Careers](https://apply.workable.com/huggingface/) [](/)

Website

[Models](/models) [Datasets](/datasets) [Spaces](/spaces) [Pricing](/pricing) [Docs](/docs)

