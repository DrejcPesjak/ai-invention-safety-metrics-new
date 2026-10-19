URL: https://huggingface.co/blog/grimjim/projected-abliteration
Type: HTML
Length: 19725 chars

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

#  Projected Abliteration 

[ Community Article](/blog/community)

Published October 25, 2025

[ Upvote 46 ](/login?next=%2Fblog%2Fgrimjim%2Fprojected-abliteration)

  * [](/diwank "diwank")
  * [](/etomoscow "etomoscow")
  * [](/mlabonne "mlabonne")
  * [](/s3nh "s3nh")
  * [](/EquinoxElahin "EquinoxElahin")
  * [](/dvdtoth "dvdtoth")
  * +40



[](/grimjim)

[Jim Lai grimjim Follow ](/grimjim)

  * Refusal Direction
  * Decomposition Relative to $\vec{\mu}_A$ (Harmless Mean)
  * Projected abliteration
  * Methodology and Implementation Details
  * Python/PyTorch Implementation
  * Result
  * References



Abliteration is a technique for removing refusal behaviors from language models by identifying and intervening on "refusal directions" in activation space, notionally represented via a single mean refusal direction. We present a refinement called "projected abliteration" that improves upon the conventional approach by removing only the mechanistically relevant components of the refusal direction.

Below we propose a refinement to conventional abliteration.

##  Refusal Direction 

In conventional abliteration, the refusal direction is often calculated as: r⃗=μ⃗H−μ⃗A\vec{r} = \vec{\mu}_{H} - \vec{\mu}_{A}r=μ​H​−μ​A​ Where $\mu_{H}$ is the mean of harmful-refusal activations/directions, and $\mu_{A}$ is the mean of harmless-acceptance activations/directions.

We observe that the refusal direction can be decomposed into two projections based on our choice of either of the two mean directions.

##  Decomposition Relative to $\vec{\mu}_A$ (Harmless Mean) 

r⃗=r⃗∥μA+r⃗⊥μA\vec{r} = \vec{r}_{\parallel \mu_A} + \vec{r}_{\perp \mu_A}r=r∥μA​​+r⊥μA​​

Can be expressed as:

r⃗⋅μ⃗A∥μ⃗A∥2μ⃗A+r⃗⊥μA\frac{\vec{r} \cdot \vec{\mu}_A}{\|\vec{\mu}_A\|^2} \vec{\mu}_A + \vec{r}_{\perp \mu_A}∥μ​A​∥2r⋅μ​A​​μ​A​+r⊥μA​​

Where $\vec{r}_{\parallel \mu_A} is the component parallel to harmless direction, and $\vec{r}_{\perp \mu_A} is the component orthogonal to harmless direction.

Furthermore, if $\mu_{A}$ is (normalized to) a unit vector, the parallel contribution simplifies to:

r⃗∥μA=(r⃗⋅μ⃗A)μ⃗A\vec{r}_{\parallel \mu_A} = (\vec{r} \cdot \vec{\mu}_A) \vec{\mu}_Ar∥μA​​=(r⋅μ​A​)μ​A​

**The meaning of the parallel component $\vec{r}_{\parallel \mu_A}$ is unclear:**

  * It represents the extent to which the refusal direction aligns with the model's general "helpful/harmless assistance" representation
  * This could mean:
    1. **Confounded interpretation** : An unimportant difference in how "helpfulness" is represented between contexts
    2. **Necessary coupling** : Refusal may require modulating helpfulness representations
    3. **Artifact** : Statistical noise from finite sampling of activation space



**The meaning of the orthogonal component $\vec{r}_{\perp \mu_A}$ is relatively straightforward:**

  * It captures what distinguishes refusal _beyond_ general helpfulness patterns
  * Is more likely to represent refusal-specific mechanism
  * But we can't be certain _a priori_ it's the "complete" refusal direction without the parallel part



However, in an empirical measurement of directions over the layers of [Gemma 3 12B Instruct](https://huggingface.co/google/gemma-3-12b-it), we found that the cosine similarity between the refusal direction and the harmful direction was positive (as expected and predicted), while the cosine similarity between the refusal direction and the harmless direction was _negative_.

We propose that the conventional interpretation of refusal being characterized by a single direction (Arditi et al, 2024) is inaccurate, that it is instead of composed of a direction which pushes toward refusal and another direction which pushes away from compliance.

However, for the purposes of abliteration, where the refusal direction is to be ablated to allow a model to comply with a harmful prompt, removing a push away from compliance is ungrounded as compliance is the goal. Removing the component which comprises a push away from correct compliance, however, has no theoretical justification. As released Instruct models are intended to be correctly trained and fine-tuned, it is likely that unprincipled intervention away from compliance would degrade model performance. (Performance drop was noted by Labonne, 2024.) Therefore, we argue that this component should be removed from the refusal direction prior to ablation. To this end, we propose a modification to abliteration that we term _projected abliteration_.

##  Projected abliteration 

For projected abliteration, we decompose $\vec{r}$ and remove only the theoretically principled component as follows:

r⃗proj=r⃗⊥μA=r⃗−(r⃗⋅μ⃗A)μ⃗A\vec{r}_{proj} = \vec{r}_{\perp \mu_A} = \vec{r} - (\vec{r} \cdot \vec{\mu}_A) \vec{\mu}_Arproj​=r⊥μA​​=r−(r⋅μ​A​)μ​A​

Where $\vec{\mu}_A$ is normalized to a unit vector here to simplify the computation, avoiding potential introduction of precision errors.

**Rationale:** The component $\vec{r}_{\parallel \mu_A}$ represents variation in the magnitude of general helpfulness representations between contexts—a confound. The orthogonal component $\vec{r}_{\perp \mu_A}$ captures the mechanistically specific refusal behavior.

This projection approach is conceptually related to other orthogonalization-based refusal modulation techniques, though it differs in removing specific directional components rather than scaling intervention strength (Wang et al., 2024).

The additional computation required for this modification is trivial, and all required information is on hand when computing the conventional refusal direction.

##  Methodology and Implementation Details 

In our empirical measurements using Gemma 3 12B Instruct, we encountered several numerical challenges:

  * High magnitude outliers: Activation measurements contained high-magnitude outlier values that complicated discrimination between harmful and harmless directions, resulting in artificially high cosine alignment between the two mean directions. These outliers are symptomatic of the GeGLU activation function employed in Gemma 3.
  * Precision requirements: We found it necessary to perform intermediate calculations in full 32-bit floating point precision, rather than the bfloat16 precision that the model weights shipped with, to avoid numerical instability.
  * Winsorization: To separate the directions effectively, we applied magnitude clipping via Winsorization at a strength of 0.995 (clipping values beyond the 99.5th percentile) to each activation measurement prior to feeding into Welford accumulation (an online algorithm for numerically stable mean calculation) for each of the harmful and harmless mean calculations. Without this preprocessing step, conventional abliteration resulted in incoherent models (outputs were no longer grammatical). Winsorization strength was determined empirically via trial and error, though not optimized.
  * Quantized measurement feasibility: We measured activations from prompts on a 4-bit bitsandbytes quantized version of the model, computed refusal directions from these measurements, then applied these directions as interventions on the full bfloat16-precision model, achieving model coherence in subsequent inference. This result is interesting despite the introduction of quantization error. We posit that mean accumulation across many samples moderates quantization error, and that this cross-precision transfer reflects the fundamental robustness of refusal and compliance encodings in the model's representation space.
  * Cross-model quantization validity: To validate this approach, we separately measured activations on both 4-bit quantized and full-weight versions of [Nemo Instruct 2407 12B](https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407), finding that cosine similarities of the refusal directions across layers also tracked closely between precision levels, with only mild divergence reflecting quantization error. Notably, the Nemo model required no Winsorization preprocessing, suggesting the outlier challenges were specific to Gemma 3's architecture.
  * Batched inference: We performed inference and activation measurement with batch size 32 for efficiency. This partially replicates the activation shifts present in production batched inference environments, improving ecological validity of our measurements.
  * Layer-wise intervention strategy: Gemma 3 comprises repeating blocks of 5 local attention layers followed by 1 global attention layer (48 layers total, numbered 0-47). We measured refusal directions at two global attention layers (23 and 29), reasoning that global attention captures semantically coherent refusal awareness, particularly in middle to late-middle layers as previously observed in abliteration efforts. We then applied these measured directions across spans of both local and global layers: the direction from layer 23 was applied to layers 11-23, and the direction from layer 29 to layers 24-41. This strategy assumes that local attention layers propagate refusal signal between global layers despite their more limited attention scope. The need for such extensive multi-layer intervention indicates that refusal mechanisms are robustly distributed across the model's depth rather than localized to specific layers. Safety refusal persisted when early layers were not modified; extending interventions to later layers improved the quality and consistency of refusal removal. This demonstrates that effective abliteration may require spatially consistent intervention to counter a robustly distributed encoding of safety refusal. This is a departure from naive abliteration which intervenes only on a single layer.



##  Python/PyTorch Implementation 

Winsorization is easily defined as a function in PyTorch:
    
    
    def magnitude_clip(vector: torch.Tensor, percentile: float = 0.995) -> torch.Tensor:
        """
        Perform symmetric magnitude Winsorization.
        Clip components to [-threshold, threshold] where threshold is at the percentile.
        
        Args:
            vector: Input tensor
            percentile: Percentile of absolute values to clip at (0.0 to 1.0)
        
        Returns:
            Clipped vector
        """
    
        original_dtype = vector.dtype
        vector_float = vector.float()
        abs_vector = torch.abs(vector_float)
        threshold = torch.quantile(abs_vector, percentile)
        clipped = torch.clamp(vector_float, min=-threshold, max=threshold)
        return clipped.to(original_dtype)
    

The projection can be implemented concisely in PyTorch:
    
    
    # Calculate refusal direction
    refusal_dir = harmful_mean - harmless_mean
    
    # Normalize harmless_mean to avoid numerical issues
    harmless_normalized = torch.nn.functional.normalize(harmless_mean.float(), dim=0)
    
    # Project and subtract contribution along harmless direction
    projection_scalar = refusal_dir @ harmless_normalized
    refined_refusal_dir = refusal_dir - projection_scalar * harmless_normalized
    

##  Result 

We abliterated Gemma 3 12B Instruct with the revised formula, and were able to bypass refusal with harmful test prompts. Additionally, we confirmed the finding (Zhao et al, 2025) that harmfulness and refusal were encoded separately, as the resulting model demonstrated awareness of harms (e.g., couching for safety, providing disclaimers) despite compliance.

##  References 

  * [Arditi et al, "Refusal in LLMs is mediated by a single direction", lesswrong.com, 2024.](https://www.lesswrong.com/posts/jGuXSZgv6qfdhMCuJ/refusal-in-llms-is-mediated-by-a-single-direction)
  * [Labonne, "Uncensor any LLM with abliteration", huggingface.co, 2024.](https://huggingface.co/blog/mlabonne/abliteration)
  * [Wang et al, "Surgical, Cheap, and Flexible: Mitigating False Refusal in Language Models via Single Vector Ablation", arXiv preprint, 2024.](https://arxiv.org/abs/2410.03415)
  * [Zhao et al, "LLMs Encode Harmfulness and Refusal Separately", arXiv preprint, 2025.](https://arxiv.org/abs/2507.11878)



_Initial publication date: October 25, 2025._

##  Models mentioned in this article 2

#### [google/gemma-3-12b-it Image-Text-to-Text • 12B • Updated Mar 21, 2025 • 1.23M • 806 ](/google/gemma-3-12b-it)#### [mistralai/Mistral-Nemo-Instruct-2407 12B • Updated Jul 28, 2025 • 403k • 1.69k ](/mistralai/Mistral-Nemo-Instruct-2407)

More from this author

## [ORBA: Orthogonal Reflection Bounded Ablation — A Geometrically Exact Detour in Directional Activation Editing

  *   * 
7 March 25, 2026 ](/blog/grimjim/orthogonal-reflection-bounded-ablation)

## [DeLERP: Decomposed Linear Interpolation for Model Merging

  *   * 
8 November 20, 2025 ](/blog/grimjim/delerp-merge-method)

### Community

[p-e-w](/p-e-w)

Oct 27, 2025

Hi there, I'm working on a generic abliteration engine and have read this article with great interest! The implementation details are particularly enlightening, and Winsorizing the activations is a brilliant idea that I intend to copy.

I tried your "Projected Abliteration" proposal in my own engine today, which uses TPE optimization to find abliteration parameters, with a compound score that combines refusals on harmful prompts with KL divergence on harmless prompts to guide the optimizer. I found that replacing the standard refusal direction computation with a form that is essentially equivalent to what you described causes the optimization process to converge towards slightly worse scores, but that doesn't mean the idea isn't correct in general.

The theoretical justification, though, is somewhat less convincing. In particular, you claim that

> [refusal] is instead of composed of a direction which pushes toward refusal and another direction which pushes away from compliance.

It's hard to see why the model would develop such a distinction internally, considering that it has never seen that distinction during training. Indeed, during instruction training, the model is shown exactly two classes of prompts:

  * Harmless prompts, with compliant responses
  * Harmful prompts, with refusal (and thus non-compliant) responses



Therefore, from the perspective of the model, refusal and non-compliance are the same thing. It has never seen a non-compliant response that wasn't also a refusal.

Then there is this part, which I am perhaps misunderstanding:

> However, for the purposes of abliteration, where the refusal direction is to be ablated to allow a model to comply with a harmful prompt, removing a push away from compliance is ungrounded as compliance is the goal.

Isn't the exact opposite the case? If we _remove_ a push _away_ from compliance, we should expect to be moving towards compliance, no?

Like yourself, I have found that Gemma 3 (and Qwen 3, Phi 4, and GPT-OSS) are substantially more resistant to abliteration than earlier models. My own theory has been that those models are far "denser" than previous generations, meaning that crude interventions like orthogonalization are more likely to cause damage, so for a given amount of model damage, the effect of suppressing refusals is less pronounced. This is supported by the observation that those same models are also more sensitive to low-bit quantization than their predecessors.

See translation

  * [](/grimjim "grimjim")
  * [](/p-e-w "p-e-w")
  * 3 replies

·

🔥

1

1

+

[grimjim](/grimjim)

Article author  Oct 28, 2025

•

edited Oct 28, 2025

The projected component is a push away from the harmless direction. Conventional abliteration subtracts the refusal direction, meaning that it subtracts a push away from the harmless direction; but when faced with a harmless prompt again, the result is a divergence from the existing harmless direction, was already optimized due to Instruct fine-tuning. Removing a push away from tuned compliance might mean... overcompliance? Which might lead to hallucination?

Tangentially, it's been found that active steering can be used increase "truthfulness", reducing hallucination:  
[Wang et al, "Adaptive Activation Steering: A Tuning-Free LLM Truthfulness Improvement Method for Diverse Hallucinations Categories", arXiv preprint, 2024](https://arxiv.org/abs/2406.00034)

My intution here for the interaction between harmless direction and intervention can be summed up in the motto "if it ain't broke, don't fix it".

The existence of high magnitude outliers that tend to align the harmless and harmful directions in Gemma 3 12B made conventional abliteration highly damaging in my experimentation. I resorted to magnitude clipping as mentioned above in order to resolve the relatively weaker refusal direction.

See translation

🧠

1

1

+

Expand 2 replies

[grimjim](/grimjim)

Article author  Nov 3, 2025

Recent UCI benchmarks, sorted by W/10 (willingness).  
[](https://cdn-uploads.huggingface.co/production/uploads/65c992424936ab38ecf706b0/lrd1rmiW1GksfKjAckaT-.png)

See translation

  * [](/ItzPingCat "ItzPingCat")
  * [](/grimjim "grimjim")
  * 4 replies

·

[ItzPingCat](/ItzPingCat)

Nov 5, 2025

Why is the score itself so low?

See translation

Expand 3 replies

[grimjim](/grimjim)

Article author  Nov 11, 2025

Here's a comparison sorted by NatInt ratings:

[](https://cdn-uploads.huggingface.co/production/uploads/65c992424936ab38ecf706b0/i5v2dY7MDE04fQqmWJ9_7.png)

See translation

Reply

[TroyDoesAI](/TroyDoesAI)

Nov 12, 2025

•

edited Nov 12, 2025

biprojected is brilliant! =]

See translation

Reply

EditPreview

Upload images, audio, and videos by dragging in the text input, pasting, or clicking here.

Tap or paste here to upload images

Comment

· [Sign up](/join?next=%2Fblog%2Fgrimjim%2Fprojected-abliteration) or [log in](/login?next=%2Fblog%2Fgrimjim%2Fprojected-abliteration) to comment

[ Upvote 46 ](/login?next=%2Fblog%2Fgrimjim%2Fprojected-abliteration)

  * [](/diwank "diwank")
  * [](/etomoscow "etomoscow")
  * [](/mlabonne "mlabonne")
  * [](/s3nh "s3nh")
  * [](/EquinoxElahin "EquinoxElahin")
  * [](/dvdtoth "dvdtoth")
  * [](/bunnycore "bunnycore")
  * [](/lenankamp "lenankamp")
  * [](/T33 "T33")
  * [](/Sychar "Sychar")
  * [](/NanGongMoon "NanGongMoon")
  * [](/win10 "win10")
  * +34



##  Models mentioned in this article 2

#### [google/gemma-3-12b-it Image-Text-to-Text • 12B • Updated Mar 21, 2025 • 1.23M • 806 ](/google/gemma-3-12b-it)#### [mistralai/Mistral-Nemo-Instruct-2407 12B • Updated Jul 28, 2025 • 403k • 1.69k ](/mistralai/Mistral-Nemo-Instruct-2407)

System theme

Company

[TOS](/terms-of-service) [Privacy](/privacy) [About](/huggingface) [Careers](https://apply.workable.com/huggingface/) [](/)

Website

[Models](/models) [Datasets](/datasets) [Spaces](/spaces) [Pricing](/pricing) [Docs](/docs)

