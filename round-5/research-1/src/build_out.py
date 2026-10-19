#!/usr/bin/env python3
"""Assemble research_out.json + research_report.md for the iter-5 positioning dossier.

Every quote in this file was obtained by fetch/fetch_grep against the URL recorded
alongside it, on the fetched_date recorded alongside it. Nothing here is paraphrased
into a quote: a string in a `quote` field is a verbatim substring of the fetched
document (whitespace re-flowed only where the PDF extractor inserted line breaks).
"""

import json
import pathlib

WS = pathlib.Path(__file__).resolve().parent
D = "2026-08-14"

# ---------------------------------------------------------------- source ledger
SOURCE_LEDGER = [
    {"id": "P1", "url": "https://arxiv.org/pdf/2607.01854",
     "mirrors": ["https://arxiv.org/abs/2607.01854", "https://arxiv.org/html/2607.01854v1"],
     "what_it_must_supply": "band-averaged E_1 definition; registry size + split; AUROC pair; parent requirement",
     "access_status": "OK", "fetched_date": D},
    {"id": "P2", "url": "https://raw.githubusercontent.com/dreamfast/abliterlitics/master/README.md",
     "mirrors": ["https://github.com/dreamfast/abliterlitics", "https://abliterlitics.dev/"],
     "what_it_must_supply": "AGPL-3.0; mandatory `base` key; delta methodology; sub-4.5B reports",
     "access_status": "OK", "fetched_date": D},
    {"id": "P3", "url": "https://arxiv.org/pdf/2604.08844",
     "mirrors": ["https://arxiv.org/html/2604.08844v1"],
     "what_it_must_supply": "AUC 0.00 sentence WITH n_bootstrap=972; the 0/300 declared-confound sentence",
     "access_status": "OK", "fetched_date": D},
    {"id": "P4", "url": "https://hermesagent.org.cn/en/docs/user-guide/skills/optional/mlops/mlops-obliteratus",
     "mirrors": ["https://github.com/elder-plinius/OBLITERATUS",
                 "https://huggingface.co/spaces/pliny-the-prompter/obliteratus",
                 "https://kicfk-obliteratus.hf.space/"],
     "what_it_must_supply": "certify() consumes activations; COSMIC layer selection; RED-at-0%-refusal calibration failure",
     "access_status": "PARTIAL - mirror doc + Space commit log reachable; raw spectral_certification.py 404 on the raw path tried",
     "fetched_date": D},
    {"id": "P5", "url": "https://huggingface.co/blog/grimjim/orthogonal-reflection-bounded-ablation",
     "mirrors": ["https://huggingface.co/grimjim/gemma-3-12b-it-orthogonal-reflection-bounded-ablation-v3-12B",
                 "https://github.com/jim-plus/llm-abliteration"],
     "what_it_must_supply": "two-recipe distinction; Householder H=I-2uu^T; misdirected sign-flips",
     "access_status": "OK", "fetched_date": D},
    {"id": "P6", "url": "https://raw.githubusercontent.com/p-e-w/heretic/master/src/heretic/model.py",
     "mirrors": ["https://raw.githubusercontent.com/p-e-w/heretic/master/config.default.toml"],
     "what_it_must_supply": "the hard-cutoff `continue` + linear interpolation; row_normalization default",
     "access_status": "OK", "fetched_date": D},
    {"id": "P7", "url": "https://pypi.org/pypi/reverse-abliterate/json",
     "mirrors": ["https://pypi.org/project/reverse-abliterate/",
                 "https://github.com/Carlos-Projects/reverse-abliterate"],
     "what_it_must_supply": "detection table showing filename/metadata-only checks, no spectral statistic",
     "access_status": "OK (HTML page is JS-gated; the PyPI JSON API serves the full README)",
     "fetched_date": D},
    {"id": "N1", "url": "https://arxiv.org/pdf/2607.03377", "mirrors": ["https://arxiv.org/abs/2607.03377"],
     "what_it_must_supply": "PL_Alpha_Hill is heavy-tail/top and robust under post-training",
     "access_status": "OK", "fetched_date": D},
    {"id": "N2", "url": "https://arxiv.org/abs/2608.07921", "mirrors": ["https://arxiv.org/html/2608.07921"],
     "what_it_must_supply": "MP bulk/outlier split; target is learned structure, not edits",
     "access_status": "OK", "fetched_date": D},
    {"id": "N3", "url": "https://arxiv.org/pdf/2607.23711", "mirrors": ["https://arxiv.org/abs/2607.23711"],
     "what_it_must_supply": "whether it needs the update matrix; which end of the spectrum; detector or law",
     "access_status": "OK", "fetched_date": D},
    {"id": "N4", "url": "https://arxiv.org/pdf/2509.15735", "mirrors": ["https://arxiv.org/abs/2509.15735"],
     "what_it_must_supply": "the sliding-window sentence, verbatim", "access_status": "OK", "fetched_date": D},
    {"id": "N5", "url": "https://arxiv.org/abs/2512.13655", "mirrors": [],
     "what_it_must_supply": "detector / recipe / study classification", "access_status": "OK", "fetched_date": D},
    {"id": "N6", "url": "https://arxiv.org/abs/2601.08489", "mirrors": [],
     "what_it_must_supply": "detector / recipe classification; new recipe class?", "access_status": "OK", "fetched_date": D},
    {"id": "N7", "url": "https://arxiv.org/abs/2510.02768", "mirrors": [],
     "what_it_must_supply": "any weights-only signature", "access_status": "OK", "fetched_date": D},
    {"id": "N8", "url": "https://arxiv.org/pdf/2410.17770", "mirrors": ["https://arxiv.org/abs/2410.17770"],
     "what_it_must_supply": "NEWLY SURFACED. bottom-of-spectrum RMT statistic on a single checkpoint's own weights",
     "access_status": "OK", "fetched_date": D},
    {"id": "N9", "url": "https://arxiv.org/abs/2508.00161", "mirrors": [],
     "what_it_must_supply": "NEWLY SURFACED. WeightWatch, the primitive 2607.01854's E_1 is credited to",
     "access_status": "OK", "fetched_date": D},
    {"id": "N10", "url": "https://arxiv.org/abs/2608.10172", "mirrors": [],
     "what_it_must_supply": "NEWLY SURFACED. Koopman spectral identifiability - weights or activations?",
     "access_status": "OK", "fetched_date": D},
    {"id": "N11", "url": "https://arxiv.org/abs/2607.17427", "mirrors": [],
     "what_it_must_supply": "NEWLY SURFACED. abliteration off-target effects - detector or study?",
     "access_status": "OK", "fetched_date": D},
    {"id": "S1", "url": "https://arxiv.org/pdf/2310.01642", "mirrors": ["https://arxiv.org/html/2310.01642v3"],
     "what_it_must_supply": "names are informative (94%) AND names are inconsistent",
     "access_status": "OK", "fetched_date": D},
    {"id": "S2", "url": "https://arxiv.org/pdf/2502.00706", "mirrors": [],
     "what_it_must_supply": "the avoid-selection-bias selection-criterion sentence; two-benchmark design; recall",
     "access_status": "OK", "fetched_date": D},
    {"id": "S3", "url": "https://doi.org/10.1016/j.neuroimage.2014.01.060", "mirrors": [],
     "what_it_must_supply": "max-statistic permutation FWER convention (ANALOGOUS anchor)",
     "access_status": "OK (metadata via OpenAlex)", "fetched_date": D},
]

# ---------------------------------------------------------------- Step 1 log
REVERIFICATION_LOG = [
    {"item": "(1) 2607.01854 E_1 is band-averaged over a mid-stack band",
     "dependency_value": "E1 is ALREADY 'band-averaged' over 'each layer in the mid-stack band B'",
     "observed_value": ("VERBATIM: 'where W is the set of attention-output (o_proj) and MLP-down (down_proj) "
                        "weight matrices from each layer in the mid-stack band B, and sigma_i are the singular "
                        "values of dW_m (the rank-1 energy fraction of the edit, band-averaged; WeightWatch, "
                        "Zhong & Raghunathan, 2025).'"),
     "status": "MATCH",
     "note": ("NEW, and load-bearing: the same sentence credits the primitive to WeightWatch (arXiv:2508.00161, "
              "ICLR 2026). E_1 is not this paper's invention; the band-averaging is. Both must be cited.")},
    {"item": "(2) 2607.01854 registry size and the AUROC pair",
     "dependency_value": "273 checkpoints; 57 public abliterations vs 37 benign; 0.95 z-sum vs 0.84 either signal alone",
     "observed_value": ("Registry 273 CONFIRMED, but 'of the 273-checkpoint registry we fully processed 71'. "
                        "Evaluation set is 94 = 57 uncensored + 37 benign. AUROC: z-sum 0.95 [.90,.98]; "
                        "activation gap rho 0.84 [.75,.92]; weight energy E_1 0.90 [.84,.96]. Held-out "
                        "leave-one-family-out balanced accuracy 0.89, FPR 0.11."),
     "status": "MISMATCH",
     "note": ("Two corrections. (a) 273 is the REGISTRY, not the evaluation set; only 71 were fully processed "
              "and the evaluation set is 94. (b) '0.84 for either signal alone' is wrong: 0.84 is the "
              "ACTIVATION signal; the WEIGHT signal alone is 0.90. Quoting 0.84 as the weights-only number "
              "understates the published weights-only competitor by 0.06 AUROC and is the kind of error a "
              "reviewer greps for. See numbered corrections 1 and 2.")},
    {"item": "(3) Abliterlitics delta methodology `diff = (variant-base).abs().mean()`",
     "dependency_value": "METHODOLOGY 1.1 is `diff = (variant-base).abs().mean()`",
     "observed_value": ("The README served at master no longer carries the METHODOLOGY code block; the "
                        "parent requirement is instead established by the setup section and the "
                        "comparison.json schema (see item 4). The delta-based character is not in doubt - "
                        "the tool cannot run without `base` - but the literal code line was NOT re-observed "
                        "at this URL on this date."),
     "status": "UNREACHABLE",
     "note": ("Do NOT print the code line as a quote in the paper. Print the setup sentence instead, which "
              "was re-observed verbatim and carries the same load. See numbered correction 3.")},
    {"item": "(4) Abliterlitics mandatory-`base` setup sentence",
     "dependency_value": "'Create a directory with your base model and variants, plus a comparison.json'",
     "observed_value": ("VERBATIM: 'Create a directory with your base model and variants, plus a "
                        "`comparison.json`:' followed by the tree 'my-comparison/ |- comparison.json |- "
                        "Qwen3.5-4B/ # Base model (safetensors) |- Qwen3.5-4B-heretic/ ...' and the schema "
                        "'{ \"name\": \"qwen35-4b\", \"base\": \"Qwen3.5-4B\", \"variants\": {...} }'. "
                        "License line re-observed: 'License [AGPL-3.0](LICENSE)'."),
     "status": "MATCH"},
    {"item": "(5) Abliterlitics Heretic 23/32-layers-with-0-8-untouched fingerprint",
     "dependency_value": "Heretic on Qwen3.5-9B: 42 tensors, 23/32 layers, 'Layers 0 through 8 have no real edits'",
     "observed_value": ("NOT re-observed on this date at the report URLs reachable from the README. A "
                        "sub-4.5B Abliterlitics-family report WAS re-observed (Qwen3-VL-4B, four Heretic "
                        "trials) carrying an equivalent depth/completeness fingerprint: tensors changed "
                        "54 / 64 / 50 / 62 across variants, 'The averaged variant spreads its edits across "
                        "34 layers, the most of any variant', and 't122's 54 tensors are a strict subset of "
                        "t174's 62'."),
     "status": "UNREACHABLE",
     "note": ("The CLAIM survives on re-observed evidence, but not the specific 23/32 number. Two options "
              "for the drafter, both honest: cite the Qwen3-VL-4B numbers actually re-observed here, or "
              "keep 23/32 and mark it to the iteration-4 fetch date. Do NOT print 23/32 as though "
              "re-verified today. See numbered correction 4.")},
    {"item": "(6) Abliterlitics direction-cosine pair 0.997 vs 0.00017",
     "dependency_value": "median cosine 1.0 / mean 0.997 on Qwen3.5-9B Heretic-Huihui; 0.00017 on Qwen3.5-4B",
     "observed_value": "Not re-observed on this date (same report-page access condition as item 5).",
     "status": "UNREACHABLE",
     "note": ("This pair is the defusing counterexample for the cosine caveat and it is load-bearing. "
              "An independent re-observation on a THIRD base was obtained instead, from the Qwen3-VL-4B "
              "report: trials 't174 and t191 overlap by 96%. But they disagree on the exact orientation of "
              "the refusal direction, which is exactly what the KL spread reflects.' That sentence carries "
              "the same argument - direction agreement is base- and trial-dependent, not a property of the "
              "recipe pair - and it IS re-verified. Prefer it.")},
    {"item": "(7) 2604.08844 cross-method AUC 0.00 sentence",
     "dependency_value": "AUC = 0.00 (n_bootstrap = 972, CI [0.00, 0.00])",
     "observed_value": ("VERBATIM: 'A binary classifier trained on DPO-drifted vs. healthy adapters, tested "
                        "on steering-derived adapters: AUC = 0.00 (nbootstrap = 972, CI [0.00, 0.00]). ... "
                        "AUC 0.00 is not a null result. It indicates perfect discriminative power with "
                        "inverted labels'"),
     "status": "MATCH"},
    {"item": "(8) 2604.08844 declared-confound sentence",
     "dependency_value": "GPT-4o scored 0/300 steered responses as harmful, confirming the output is incoherent",
     "observed_value": ("VERBATIM: 'H5-asr-steering: Technically passed; substantively invalid. Language "
                        "generation collapsed on all steered adapters at all intensities tested. Llama-Guard "
                        "classified degenerate token repetition as \"unsafe,\" producing inflated ASR. GPT-4o "
                        "scored 0/300 steered responses as harmful, confirming the output is incoherent.'"),
     "status": "MATCH"},
    {"item": "(9) Heretic hard-cutoff code lines",
     "dependency_value": "triangular tent with a hard cutoff, NOT Gaussian",
     "observed_value": ("VERBATIM from src/heretic/model.py: 'distance = cast(float, abs(layer_index - "
                        "params.max_weight_position)) # Don't orthogonalize layers that are more than "
                        "# min_weight_distance away from max_weight_position. if distance > "
                        "params.min_weight_distance: continue # Interpolate linearly between max_weight and "
                        "min_weight # over min_weight_distance. weight = params.max_weight + (distance / "
                        "params.min_weight_distance) * (params.min_weight - params.max_weight)'. "
                        "Shipped default re-observed in config.default.toml: 'row_normalization = \"full\"'."),
     "status": "MATCH",
     "note": ("Strongest single re-verification in this dossier. The cutoff and the linear interpolation are "
              "both in one contiguous code block; the kernel is a tent, and layers outside "
              "min_weight_distance are skipped entirely rather than down-weighted.")},
    {"item": "(10) OBLITERATUS certify() consumes activations",
     "dependency_value": ("def certify(self, harmful_activations: torch.Tensor, harmless_activations: "
                          "torch.Tensor, layer_idx: int = -1) -> SpectralCertificate"),
     "observed_value": ("The signature was NOT re-fetched from a raw source file on this date (the raw path "
                        "tried returned 404). Independent corroboration WAS obtained from two mirrors: the "
                        "Space commit log lists 'obliteratus/analysis/spectral_certification.py' with the "
                        "line '# knee_cosmic: OBLITERATUS default (knee detection + COSMIC fusion)', and the "
                        "hosted Space describes 'OBLITERATUS prompt set - 512 harmful/harmless pairs across "
                        "7 severity tiers. Spectral Certification (BBP Phase Transition) - Formal "
                        "completeness guarantee via random matrix theory'. A prompt set of 512 "
                        "harmful/harmless pairs is what an activation-consuming certifier needs and a "
                        "weights-only statistic does not."),
     "status": "UNREACHABLE",
     "note": ("The CONCLUSION (activation-consuming, COSMIC-selective) is corroborated on two independent "
              "mirrors; the literal signature is not re-verified today. Cite the Space text, not the "
              "signature. The COSMIC default is re-confirmed verbatim. See numbered correction 5.")},
]

# ---------------------------------------------------------------- Step 2 verdict
FOUR_QUALIFIER_TABLE = [
    {"work": "Abliterlitics (dreamfast, AGPL-3.0)", "url": "https://github.com/dreamfast/abliterlitics",
     "parent_free": False, "calibration_free": True, "bottom_of_spectrum": False, "sliding_extremum": False,
     "ruling": ("NEAR-MISS: lacks parent-free, bottom-of-spectrum and sliding-extremum. Every weight metric "
                "is computed on the base-to-variant delta and the tool has no single-checkpoint mode."),
     "quote": "Create a directory with your base model and variants, plus a `comparison.json`:"},
    {"work": "arXiv:2607.01854 E_1 (Hurtado)", "url": "https://arxiv.org/pdf/2607.01854",
     "parent_free": False, "calibration_free": False, "bottom_of_spectrum": False, "sliding_extremum": False,
     "ruling": ("NEAR-MISS on the band idea only: lacks all four. E_1 is the rank-1 (top) energy fraction of "
                "dW = W_base - W_cand, averaged over ONE fixed mid-stack band, and the deployed score is "
                "z-standardised on a reference population with a Youden-calibrated threshold. It is "
                "nevertheless the work that publishes per-band scoring and must be conceded."),
     "quote": ("where W is the set of attention-output (o_proj) and MLP-down (down_proj) weight matrices from "
               "each layer in the mid-stack band B ... the rank-1 energy fraction of the edit, band-averaged")},
    {"work": "WeightWatch / Watch the Weights, arXiv:2508.00161 (Zhong & Raghunathan, ICLR 2026)",
     "url": "https://arxiv.org/abs/2508.00161",
     "parent_free": False, "calibration_free": True, "bottom_of_spectrum": False, "sliding_extremum": False,
     "ruling": ("NEAR-MISS: lacks parent-free, bottom-of-spectrum, sliding-extremum. This is the primitive "
                "arXiv:2607.01854's E_1 is credited to, so it is an obligatory citation the dependencies did "
                "not carry. It reads the TOP singular vectors of the weight DIFFERENCE and then monitors "
                "ACTIVATION cosine along them, so it is neither parent-free nor prompt-free."),
     "quote": ("the top singular vectors of the weight difference between a fine-tuned model and its base "
               "model correspond to newly acquired behaviors")},
    {"work": "arXiv:2604.08844 (Paul)", "url": "https://arxiv.org/pdf/2604.08844",
     "parent_free": False, "calibration_free": False, "bottom_of_spectrum": False, "sliding_extremum": False,
     "ruling": ("NEAR-MISS: lacks all four. Features are computed on adapter deltas and scored by a fitted "
                "l2-regularised logistic regression with a 70/30 split."),
     "quote": "We train l2-regularized logistic regression classifiers with stratified 70/30 train/test splits."},
    {"work": "arXiv:2607.23711 The Intruder Threshold (Xie)", "url": "https://arxiv.org/pdf/2607.23711",
     "parent_free": False, "calibration_free": True, "bottom_of_spectrum": False, "sliding_extremum": False,
     "ruling": ("NEAR-MISS - the dossier's most dangerous unadjudicated candidate, resolved. It lacks "
                "parent-free, bottom-of-spectrum and sliding-extremum. The critical strength is computed "
                "from the pretrained spectrum alone, but the quantity compared against it is sigma_1(BA), "
                "the top singular value of the LoRA update, so evaluating the criterion requires the update "
                "matrix. It reads the TOP of the spectrum by construction ('the full edge uses sigma_1 "
                "itself'). And it is a law about when LoRA training creates intruder dimensions, not a "
                "detector of a completed edit: its classification target is intruder-bearing versus "
                "intruder-free LAYERS of a known adapter, not edited versus clean CHECKPOINTS."),
     "quote": ("We derive a per-layer critical update strength s* = theta_bar/(gamma sigma_1(BA)), computed "
               "from the measured spectrum of W alone through the rectangular spiked-deformation transform")},
    {"work": "arXiv:2607.03377 PL_Alpha_Hill (Zhang et al., KDD 2026)", "url": "https://arxiv.org/pdf/2607.03377",
     "parent_free": True, "calibration_free": True, "bottom_of_spectrum": False, "sliding_extremum": False,
     "ruling": ("NEAR-MISS: lacks bottom-of-spectrum and sliding-extremum, and is ruled out by something "
                "stronger than a metric difference - it is DESIGNED to be the quantity that does not move "
                "when a model is post-trained, which is exactly the wrong property for an edit detector. Its "
                "lineage use is also parent-requiring: it compares layerwise profiles across models derived "
                "from a shared backbone."),
     "quote": ("This signature captures intrinsic properties of pretrained models and remains robust during "
               "post-training, making it suitable for model-level analysis.")},
    {"work": "arXiv:2608.07921 MP spectral outliers (Dewage et al., ICMLA 2026)",
     "url": "https://arxiv.org/abs/2608.07921",
     "parent_free": True, "calibration_free": True, "bottom_of_spectrum": False, "sliding_extremum": False,
     "ruling": ("NEAR-MISS: lacks bottom-of-spectrum and sliding-extremum. It reads the outliers ABOVE the "
                "Marchenko-Pastur edge, and its target is learned structure in pretrained attention, not an "
                "edit: no edited-versus-clean label appears anywhere in the paper."),
     "quote": ("spectral outliers encode a dominant component of the learned structure; Q projections carry "
               "the most outliers")},
    {"work": "arXiv:2410.17770 Small Singular Values Matter (Thamm & Rosenow)",
     "url": "https://arxiv.org/pdf/2410.17770",
     "parent_free": True, "calibration_free": True, "bottom_of_spectrum": True, "sliding_extremum": False,
     "ruling": ("CLOSEST NEAR-MISS ON THE BOTTOM-OF-SPECTRUM QUALIFIER, and absent from every dependency. It "
                "lacks only sliding-extremum - plus the application. It reads the smallest singular values "
                "of a single checkpoint's own weight matrices with an RMT null and no fitted threshold, "
                "which is three of the four qualifiers. It is not an edit detector: it asks where information "
                "is stored in pretrained transformers, scores no checkpoint, and carries no edited/clean "
                "label. This work must be cited at the point where the bottom-of-spectrum choice is "
                "justified; it is the prior art that makes that choice defensible rather than arbitrary, and "
                "presenting the low end of the spectrum as an unexamined region would be refutable from its "
                "abstract."),
     "quote": ("Surprisingly, we observe pronounced departures from RMT not only among the largest singular "
               "values - the usual outliers - but also among the smallest ones.")},
    {"work": "EigenTrack, arXiv:2509.15735 (Ettori et al.)", "url": "https://arxiv.org/pdf/2509.15735",
     "parent_free": True, "calibration_free": False, "bottom_of_spectrum": False, "sliding_extremum": True,
     "ruling": ("CLOSEST NEAR-MISS ON THE SLIDING QUALIFIER. It lacks calibration-free (a trained recurrent "
                "classifier) and bottom-of-spectrum, and decisively it slides over TIME across ACTIVATIONS, "
                "requiring input data and a forward pass, where the object under test slides over LAYERS "
                "across WEIGHTS and requires neither. That distinction has to be stated in the paper rather "
                "than left implicit."),
     "quote": ("EigenTrack computes covariance spectra over a sliding window of hidden activations and "
               "streams the resulting spectral statistics into a lightweight recurrent classifier")},
    {"work": "arXiv:2608.10172 Koopman spectral identifiability (Dhor & Chen)",
     "url": "https://arxiv.org/abs/2608.10172",
     "parent_free": True, "calibration_free": False, "bottom_of_spectrum": False, "sliding_extremum": False,
     "ruling": ("NEAR-MISS: lacks calibration-free, bottom-of-spectrum and sliding-extremum, and is not "
                "weights-only. The spectrum is recovered from M calibration samples of activations, i.e. it "
                "is prompt-requiring. Its depth-as-time framing is the nearest conceptual neighbour to "
                "sliding over layers and is worth one sentence."),
     "quote": ("We prove the spectrum is recoverable from M calibration samples at rate M^{-1/2} up to permutation")},
    {"work": "reverse-abliterate (Carlos-Projects, MIT)", "url": "https://pypi.org/pypi/reverse-abliterate/json",
     "parent_free": True, "calibration_free": True, "bottom_of_spectrum": False, "sliding_extremum": False,
     "ruling": ("NOT A SPECTRAL METHOD AT ALL: lacks bottom-of-spectrum and sliding-extremum because it "
                "computes no statistic of tensor content. It is the shipped parent-free detector, and it is "
                "a filename-and-metadata scanner."),
     "quote": "| **Abliteration detection** | ✅ scans metadata, weights, hooks |"},
]

QUERIES_RUN = [
    {"query": "sliding window spectral statistic weights detect model editing single checkpoint", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "parent-free weight forensics abliteration detection no base model", "mode": "general", "date": D, "new_relevant_hits": 2,
     "note": "surfaced arXiv:2607.17427 and the Abliterlitics report mirrors"},
    {"query": "minimum eigenvalue null space weight matrix detect refusal direction removal", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "per-layer Gram matrix spectrum detect orthogonalization edit LLM", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "calibration-free weights-only detector fine-tuned model modification", "mode": "general", "date": D, "new_relevant_hits": 1,
     "note": "surfaced WeightWatch arXiv:2508.00161 - the primitive E_1 is credited to"},
    {"query": "window-wise random direction null calibration spectral layer statistic", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "bottom of spectrum smallest singular values detect weight edit transformer", "mode": "general", "date": D, "new_relevant_hits": 1,
     "note": "surfaced arXiv:2410.17770 - the closest bottom-of-spectrum prior art, missing from all dependencies"},
    {"query": "abliteration detection weights only 2026", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "model tampering detection open weights spectral signature", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "multiple comparison correction per-layer weight statistic false positive rate", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "rank deficiency detection residual stream write matrices safety edit", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "reference-free model audit weight spectrum safety removal", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "weight-space forensics language model provenance spectral", "mode": "scholarly", "date": D, "new_relevant_hits": 0},
    {"query": "detecting safety alignment removal from weights without prompts", "mode": "scholarly", "date": D, "new_relevant_hits": 0},
    {"query": "random direction null per layer spectral statistic language model", "mode": "general", "date": D, "new_relevant_hits": 1,
     "note": "surfaced arXiv:2608.10172 Koopman identifiability"},
    {"query": "Marchenko-Pastur null per-layer weight matrix threshold language model", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "family-wise error rate layerwise interpretability statistic multiple comparison", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "max-statistic permutation test across layers neural network probing correction", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "multiple comparisons correction across layers probing classifier transformer", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "Holm Bonferroni layerwise probe language model interpretability", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "per-window Gram matrix eigenvalue statistic layer band detect abliteration", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "unsupervised weights-only screening uploaded checkpoint safety guardrail removed", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "spectral null hypothesis test weight matrix edit detection large language model 2026", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "keyword-seeded sampling bias mining software repositories classifier inflated", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "search-based sampling bias benchmark construction keyword query dataset", "mode": "general", "date": D, "new_relevant_hits": 0},
    {"query": "capture-recapture coverage estimate repository mining software", "mode": "general", "date": D, "new_relevant_hits": 0},
]

WINDOWED_NOVELTY_VERDICT = {
    "verdict": "NOVEL-NARROW",
    "object_under_test": (
        "A statistic carrying all four qualifiers simultaneously: (i) PARENT-FREE - no base, sibling or "
        "reference checkpoint of any kind; (ii) CALIBRATION-FREE - no threshold fitted on a labelled panel "
        "of edited versus clean models; (iii) BOTTOM-OF-SPECTRUM - smallest eigenvalues / near-null energy "
        "of a Gram matrix, not top singular values, stable rank, or a heavy-tail exponent; (iv) computed "
        "PER-WINDOW over a SLIDING window of consecutive layers and scored by an EXTREMUM over windows, not "
        "by a single pooled or band-averaged value. A prior work defeats novelty only by carrying all four."),
    "four_qualifier_table": FOUR_QUALIFIER_TABLE,
    "queries_run": QUERIES_RUN,
    "saturation_reached": True,
    "saturation_point": (
        "26 queries. The last three general-mode queries and both scholarly-mode queries returned zero new "
        "relevant items; the final six consecutive queries returned zero. Three new works were surfaced that "
        "no dependency carried (2410.17770, 2508.00161, 2608.10172) and all three were adjudicated as "
        "near-misses. Saturation is claimed on the weights-only edit-detection lane, NOT on the whole "
        "random-matrix-theory literature, which is far too large to saturate in one dossier."),
    "how_close_the_closest_is": (
        "No single work carries more than three of the four qualifiers. Two carry three, along different "
        "axes, and they are the two citations the novelty sentence must name: arXiv:2410.17770 is "
        "parent-free, calibration-free and bottom-of-spectrum but neither sliding nor an edit detector; "
        "EigenTrack is parent-free and sliding but calibration-requiring, top-of-spectrum, and slides over "
        "time across activations rather than over layers across weights."),
    "what_would_flip_it": (
        "A single work that computes a bottom-of-spectrum statistic on a sliding window of consecutive "
        "layers from one checkpoint's own weights, with no reference model and no fitted threshold, and "
        "scores a checkpoint by an extremum over those windows. arXiv:2410.17770 would flip it with one "
        "additional step - sliding the window and taking an extremum - so the honest reading is that the "
        "novelty is one construction away from published work, not a wide-open gap. If the windowed arm "
        "does not recover the discovery failures, the fourth qualifier is unearned and the verdict for the "
        "claim actually made drops to three qualifiers (see P-E)."),
    "explicitly_not_claimed": [
        "Per-band scoring: published (arXiv:2607.01854 E_1; Abliterlitics early/mid/late band reporting).",
        "The rank-1 energy fraction of a weight edit: published (WeightWatch, arXiv:2508.00161).",
        "Reading the bottom of a weight spectrum with an RMT null: published (arXiv:2410.17770).",
        "Sliding-window spectral tracking: published, over activations in time (EigenTrack, arXiv:2509.15735).",
        "Depth-versus-completeness fingerprinting of abliteration recipes: published from deltas (Abliterlitics).",
    ],
}

PER_WINDOW_NULL_CONVENTION = {
    "found": True,
    "convention": (
        "For the NULL ITSELF there is an established, named convention and the paper should adopt it by "
        "name rather than invent one: Marchenko-Pastur / random-matrix theory as the zero-information null "
        "for a weight matrix's spectrum, with deviation from MP read as learned structure. arXiv:2410.17770 "
        "states it in exactly those terms and applies it at BOTH ends of the spectrum, which is the "
        "precedent that licenses a bottom-of-spectrum null; arXiv:2608.07921 applies the same MP bulk/outlier "
        "split to attention projections and validates it causally; EigenTrack uses 'KL divergence from "
        "random baselines' with an MP reference on activation covariances. A random-direction null is the "
        "correct COMPLEMENT to MP rather than a substitute: MP asks whether a window's spectrum departs "
        "from an unstructured matrix, and a random-direction control asks whether the departure is specific "
        "to the refusal direction rather than to an arbitrary one. Rogue-Scalpel-style random-direction "
        "controls are magnitude-matched comparators, not nulls."),
    "citation": ("Thamm & Rosenow, 'Small Singular Values Matter: A Random Matrix Analysis of Transformer "
                 "Models', arXiv:2410.17770; Dewage et al., arXiv:2608.07921 (ICMLA 2026); Ettori et al., "
                 "EigenTrack, arXiv:2509.15735."),
    "quote": ("Using Random Matrix Theory (RMT) as a zero information hypothesis, we associate agreement "
              "with RMT as evidence of randomness and deviations as evidence for learning."),
    "multiple_window_fwer": {
        "found_in_ml_literature": False,
        "statement": (
            "NONE FOUND. Twenty-six queries, including four aimed squarely at this question, surfaced no "
            "established convention in the interpretability or weight-forensics literature for controlling "
            "the family-wise error rate of a statistic evaluated at every layer or every window. The papers "
            "that compute per-layer spectral statistics - 2607.23711, 2608.07921, 2410.17770, 2607.03377 - "
            "report per-layer values or aggregate them, and none corrects for the number of layers "
            "inspected. This is a real gap, and it means the paper cannot cite an in-field convention and "
            "must either import one or measure the FPR empirically."),
        "analogous_convention_to_import": (
            "ANALOGOUS, not direct: the mature treatment of exactly this problem - a statistic evaluated at "
            "every element of a large indexed family, where the reported result is the extremum - is "
            "max-statistic permutation inference from neuroimaging, where the null distribution of the "
            "MAXIMUM statistic over the family is built by permutation and a single threshold from that "
            "distribution controls the family-wise error rate over the whole family at once. It is exactly "
            "the right shape for an extremum-over-windows score, because the object being calibrated is the "
            "maximum, which is what the detector reports. Cite Winkler et al., 'Permutation inference for "
            "the general linear model', NeuroImage 92:381-397, 2014 (doi:10.1016/j.neuroimage.2014.01.060), "
            "and label the borrowing as analogous."),
        "operational_recommendation_for_the_experiment_planner": (
            "SUGGESTION, not a claim. Because the reported score is an extremum over W windows, a per-window "
            "FPR does not compose into a checkpoint-level FPR without a correction, and reporting the "
            "per-window number alone would understate the false-positive rate by roughly the number of "
            "windows. The cheap and defensible construction: for each clean checkpoint, compute the "
            "windowed statistic under many random directions, take the MAXIMUM over windows for each draw, "
            "and threshold at the desired quantile of that max distribution. This calibrates the extremum "
            "directly, needs no per-window correction, and yields a checkpoint-level FPR that is the number "
            "the paper should report. If a per-window number is also reported, label it per-window "
            "explicitly and never as the detector's FPR."),
    },
}

# ---------------------------------------------------------------- Step 3
SELECTION_BIAS_CITATIONS = [
    {"id": "SB1", "url": "https://arxiv.org/pdf/2502.00706",
     "title": "Model Provenance Testing for Large Language Models",
     "quote": ("We collect model candidates for all provenance pairs from the Hugging Face (HF) platform. "
               "To avoid selection bias, we used download counts as our selection criterion, taking the most "
               "popular models subject only to hardware constraints on model size."),
     "how_we_use_it": ("The direct precedent that a hub-harvested evaluation population must NAME its "
                       "selection criterion and justify it against selection bias. It licenses the sentence "
                       "'our positive pool was discovered by name search' as normal practice rather than a "
                       "confession, and it is the reason that sentence belongs in the paper."),
     "directness": "DIRECT", "fetched_date": D},
    {"id": "SB2", "url": "https://arxiv.org/pdf/2502.00706",
     "title": "Model Provenance Testing - two-benchmark design",
     "quote": ("we create two distinct benchmarks BENCH-A and BENCH-B, that differ in aspects such as model "
               "sizes, choice of pre-trained models, and ground-truth verification procedure"),
     "how_we_use_it": ("The precedent for reporting TWO differently-constructed populations instead of one "
                       "pooled number, with the construction difference stated. This is the exact shape of "
                       "the fix: a name-discovered stratum and an uploader-discovered stratum, reported "
                       "separately, with the name-discovered number labelled as the upper bound."),
     "directness": "DIRECT", "fetched_date": D},
    {"id": "SB3", "url": "https://arxiv.org/pdf/2502.00706",
     "title": "Model Provenance Testing - black-box recall comparator",
     "quote": ("our tester achieves 90-95% precision and 80-90% recall in identifying derived models"),
     "how_we_use_it": ("A published, name-free provenance baseline on 600+ Hugging Face models from 30M to "
                       "4B parameters - our own size class. It is the right comparator for a detector that "
                       "refuses to read names, and it shows what recall a non-name method attains when it "
                       "is allowed queries."),
     "directness": "DIRECT", "fetched_date": D},
    {"id": "SB4", "url": "https://arxiv.org/pdf/2310.01642",
     "title": "Naming Practices of Pre-Trained Models on Hugging Face (DARA)",
     "quote": ("architectural information alone is sufficient to detect these inconsistencies, achieving an "
               "accuracy of 94% in identifying model types"),
     "how_we_use_it": ("Edge one of the two-edged citation: names carry enough real signal that a filename "
                       "regex is a serious baseline and beating it is a genuine bar. This is what makes the "
                       "comparison fair rather than a strawman."),
     "directness": "DIRECT", "fetched_date": D},
    {"id": "SB5", "url": "https://arxiv.org/pdf/2310.01642",
     "title": "Naming Practices of Pre-Trained Models on Hugging Face - unreliability",
     "quote": ("prior research has shown that model names are not always well chosen and can sometimes be "
               "inaccurate and misleading"),
     "how_we_use_it": ("Edge two: because naming is inconsistent and its inconsistency is itself the object "
                       "of study, name-based recall is a property of the population sampled, not of the "
                       "method. A population discovered by name search is enriched for exactly the "
                       "consistently-named checkpoints the regex catches, which is the mechanism that turns "
                       "the measured sensitivity into an upper bound. These two quotes are from the same "
                       "paper and must be cited together."),
     "directness": "DIRECT", "fetched_date": D},
    {"id": "SB6", "url": "https://doi.org/10.1016/j.neuroimage.2014.01.060",
     "title": "Permutation inference for the general linear model (Winkler et al., NeuroImage 2014)",
     "quote": "(cited for its method, not quoted; 3864 citations per OpenAlex as of 2026-08-14)",
     "how_we_use_it": ("ANALOGOUS anchor for the multiple-window family-wise error problem: calibrate the "
                       "distribution of the MAXIMUM statistic over the family by permutation rather than "
                       "correcting each member. Imported because no in-field convention exists."),
     "directness": "ANALOGOUS", "fetched_date": D},
]

REPORTING_CONVENTION = (
    "Template, to be instantiated by the drafter. Follow arXiv:2502.00706 in three moves, in this order. "
    "(1) NAME THE DISCOVERY MECHANISM BEFORE ANY NUMBER: state that the positive pool was enumerated by "
    "keyword sweeps over abliteration vocabulary, give the number of sweeps, and state that the vocabulary "
    "overlaps the baseline regex's terms. (2) STRATIFY AND REPORT SEPARATELY: report the filename-regex "
    "sensitivity once per discovery stratum - name-discovered and not-name-discovered - never pooled, and "
    "state in the same sentence that the name-discovered figure is an upper bound on the regex's sensitivity "
    "in the wild because the stratum is enriched by construction for the checkpoints the regex can catch. "
    "(3) GIVE THE COMPARATOR ITS OWN SENTENCE: the detector's sensitivity is measured on the same strata, so "
    "the comparison within a stratum is fair even though the pooled level is not. Concretely: 'Positives "
    "were enumerated by N keyword sweeps over abliteration vocabulary, whose terms overlap the K terms of "
    "the filename regex we compare against; the regex therefore attains 0.727 sensitivity on this pool by "
    "construction, and we report that figure as an upper bound rather than as its expected sensitivity on an "
    "arbitrary upload. Following the selection-criterion discipline of [2502.00706], we report the two "
    "discovery strata separately and never pool them.' Do NOT write 'we retract' or refer to an earlier "
    "estimate; state the bound and move on."
)

CAPTURE_RECAPTURE_SUGGESTION = (
    "OPTIONAL, and a suggestion to the experiment planner rather than a claim in the paper. If the "
    "uploader-sweep and name-sweep strata are enumerated independently, their overlap supports a two-source "
    "Lincoln-Petersen coverage estimate: with n1 found by name sweep, n2 by uploader sweep and m by both, "
    "the total population is estimated as n1*n2/m and the name sweep's coverage as n1*m/(n1*n2), which "
    "converts the hand-waved phrase 'the pool is enriched' into a number. The independence assumption is the "
    "weak point and is probably violated here - a prolific abliteration uploader also names consistently - "
    "which biases the estimate toward understating the true population, so it should be reported as a "
    "lower-bound on population size and an upper-bound on coverage, or not at all. No published application "
    "of capture-recapture to model-hub harvesting was found in 26 queries, so this would be an unsupported "
    "borrowing from ecology and software-repository mining; that is a reason to label it clearly, not a "
    "reason to skip it."
)

# ---------------------------------------------------------------- Step 4
POSITIONING_CORRECTIONS = [
    {"id": "C1",
     "claim_as_it_must_appear": (
         "A weight-space classifier trained on DPO-manufactured adapters inverts completely on "
         "steering-manufactured ones, reaching AUC 0.00 (n_bootstrap = 972, CI [0.00, 0.00]) [2604.08844]. "
         "That precedent is confounded by its own authors' account: the steering arm's generations collapsed "
         "at every intensity tested, and GPT-4o scored 0 of 300 steered responses as harmful, so the "
         "checkpoints on which transfer failed were not coherent models. Cross-recipe transfer failure is "
         "therefore an open question rather than a settled negative, which is why recipe-class coverage is "
         "a control in this work rather than an assumption."),
     "quote": ("H5-asr-steering: Technically passed; substantively invalid. Language generation collapsed on "
               "all steered adapters at all intensities tested. ... GPT-4o scored 0/300 steered responses as "
               "harmful, confirming the output is incoherent."),
     "url": "https://arxiv.org/pdf/2604.08844", "anchor": "Sec. 5.8.3 Steering-Derived Adapters",
     "fetched_date": D,
     "draft_currently_says": ("Cites AUC 0.00 as a clean published negative about cross-method transfer, "
                              "without the confound, which makes the draft's own cross-recipe result look "
                              "like a contradiction of established fact instead of the first clean test.")},
    {"id": "C2",
     "claim_as_it_must_appear": (
         "OBLITERATUS certifies from activations - it runs a prompt set of 512 harmful/harmless pairs "
         "through the edited model and applies a BBP phase-transition test to the resulting covariance - so "
         "it is parent-free but not prompt-free, and it audits an edit the operator has just performed "
         "rather than screening an unknown checkpoint [OBLITERATUS]. Its layer selection is COSMIC-guided "
         "rather than uniform, so its presets are expected to register as degraded rather than as cleanly "
         "detected. Both facts widen the gap this work occupies: a screen that needs neither a parent nor a "
         "prompt covers the case an activation certifier structurally cannot, which is the unattested upload."),
     "quote": ("OBLITERATUS prompt set - 512 harmful/harmless pairs across 7 severity tiers. Spectral "
               "Certification (BBP Phase Transition) - Formal completeness guarantee via random matrix "
               "theory ... # knee_cosmic: OBLITERATUS default (knee detection + COSMIC fusion)."),
     "url": "https://kicfk-obliteratus.hf.space/",
     "anchor": ("hosted Space landing text; COSMIC default line from "
                "huggingface.co/spaces/pliny-the-prompter/obliteratus, analysis/spectral_certification.py, commit f0084ba"),
     "fetched_date": D,
     "draft_currently_says": ("Treats OBLITERATUS as a weights-only competitor and marks its presets "
                              "DETECTED. Both are wrong: it consumes activations, and its layer selectivity "
                              "predicts DEGRADED.")},
    {"id": "C3",
     "claim_as_it_must_appear": (
         "ORBA is two distinct operations and the falsification test applies to only one of them. In the "
         "geodesic path at lambda = 1 the refusal component is rotated onto its orthogonal complement and "
         "zeroed without reflection, which removes rank; in the Householder path the reflector H = I - 2uu^T "
         "flips that component instead, which is an isometry and removes no rank [ORBA]. The isometry is the "
         "sharp falsification target precisely because it is rank-preserving, and evaluating the annihilating "
         "path in its place would make the test vacuous - annihilation is the case any rank-sensitive "
         "statistic is expected to catch."),
     "quote": ("At lambda = 1 the refusal component of w is rotated exactly to its orthogonal complement - "
               "zeroed without reflection. ... Householder reflection, while isometric and analytically "
               "exact, introduces token and semantic drift that directional ablation does not - reflection "
               "amplifies angular error in a way that projection does not, making misdirected sign-flips the "
               "characteristic failure mode rather than incomplete zeroing."),
     "url": "https://huggingface.co/blog/grimjim/orthogonal-reflection-bounded-ablation",
     "anchor": "Abstract and 'Householder As Exact Analytical Geometric Tool'; author Jim W. Lai, 2026-03-24",
     "fetched_date": D,
     "draft_currently_says": ("Treats ORBA as one recipe. The two published checkpoints are separate arms - "
                              "v3 is the Householder comparison model, v4 is directional ablation - and "
                              "conflating them collapses the isometry test.")},
    {"id": "C4",
     "claim_as_it_must_appear": (
         "The one shipped parent-free abliteration detector reads names, not weights. reverse-abliterate "
         "scans for an abliteration_metadata.json written by the editing toolchain, LoRA adapter files, the "
         "-OBLITERATED repository-name convention, embedded toolchain commit hashes, forward-hook "
         "registration, and suspicious shard sizes and filenames; its only tensor-level check is a SHA-256 "
         "manifest, which requires a trusted prior manifest of the same checkpoint [reverse-abliterate]. A "
         "filename baseline is therefore the deployed state of the art for unattested uploads, not a "
         "strawman constructed for comparison."),
     "quote": ("| **Abliteration detection** | ✅ scans metadata, weights, hooks | ... | `Repo name "
               "-OBLITERATED` | Standard abliteration naming convention | | Weight anomalies | Suspicious "
               "shard sizes and filenames |"),
     "url": "https://pypi.org/pypi/reverse-abliterate/json",
     "anchor": "README, 'What makes reverse-abliterate unique' table and the Detection table; MIT licence",
     "fetched_date": D,
     "draft_currently_says": ("Presents the filename regex as a baseline this work invented, which invites "
                              "the reviewer objection that it was chosen to be beaten.")},
    {"id": "C5",
     "claim_as_it_must_appear": (
         "Heretic's ablation kernel is a triangular tent with a hard cutoff. For each component it computes "
         "the distance from the layer index to the kernel's peak position, skips the layer outright when "
         "that distance exceeds min_weight_distance, and otherwise interpolates the ablation weight linearly "
         "between max_weight and min_weight [Heretic]. The consequence is structural rather than incidental: "
         "layers beyond the cutoff receive no edit at all, which is what produces the partial-depth "
         "coverage that delta-based forensics observes on Heretic checkpoints. Its shipped default also "
         "preserves row magnitudes (row_normalization = \"full\")."),
     "quote": ("distance = cast(float, abs(layer_index - params.max_weight_position)) # Don't orthogonalize "
               "layers that are more than # min_weight_distance away from max_weight_position. if distance > "
               "params.min_weight_distance: continue # Interpolate linearly between max_weight and min_weight "
               "# over min_weight_distance."),
     "url": "https://raw.githubusercontent.com/p-e-w/heretic/master/src/heretic/model.py",
     "anchor": "ablation-weight loop over layer_index; default from config.default.toml",
     "fetched_date": D,
     "draft_currently_says": ("Describes the kernel as Gaussian or bell-curve. State the tent directly, in "
                              "the present tense, with no reference to the earlier description.")},
    {"id": "C6",
     "claim_as_it_must_appear": (
         "The rank-1 energy fraction of a weight edit is not introduced by the two-signal audit that "
         "deploys it: that audit's weight signal E_1 is the WeightWatch primitive, band-averaged over a "
         "mid-stack band [2607.01854], and WeightWatch itself reads the top singular vectors of the "
         "difference between a fine-tuned model and its base and then monitors activation cosine along "
         "those directions [2508.00161]. Both are parent-requiring, and WeightWatch is additionally "
         "prompt-requiring at monitoring time."),
     "quote": ("the rank-1 energy fraction of the edit, band-averaged; WeightWatch, Zhong & Raghunathan, 2025"),
     "url": "https://arxiv.org/pdf/2607.01854", "anchor": "Sec. 3, definition of E_1", "fetched_date": D,
     "draft_currently_says": ("Attributes E_1 to arXiv:2607.01854 alone. Missing the WeightWatch citation is "
                              "a straightforward attribution error, and WeightWatch is an ICLR 2026 paper, "
                              "so a reviewer is likely to know it."),
     "note": "SIXTH correction, added per failure scenario F4."},
    {"id": "C7",
     "claim_as_it_must_appear": (
         "Reading the low end of a weight spectrum is not an unexamined choice: departures from the "
         "random-matrix null occur among the smallest singular values as well as the largest, the "
         "corresponding singular vectors overlap the activation covariance eigenvectors, and zeroing the "
         "smallest deviating values raises perplexity more than removing values from the bulk "
         "[2410.17770]. That result is what makes the bottom of the spectrum an informative place to look; "
         "the contribution here is to read it per window, without a reference model, and to score a "
         "checkpoint by the extremum over windows."),
     "quote": ("Surprisingly, we observe pronounced departures from RMT not only among the largest singular "
               "values - the usual outliers - but also among the smallest ones. ... zeroing out the singular "
               "values that deviate from RMT raises language-model perplexity far more than removing values "
               "from the bulk"),
     "url": "https://arxiv.org/pdf/2410.17770", "anchor": "Abstract; Sec. 1", "fetched_date": D,
     "draft_currently_says": ("Nothing - this work is absent from the draft and from every dependency. It is "
                              "the closest prior art to the bottom-of-spectrum qualifier and omitting it is "
                              "the single largest citation risk in the current positioning."),
     "note": "SEVENTH correction, added per failure scenario F4. Highest priority of the additions."},
]

# ---------------------------------------------------------------- Step 5
PASTE_READY = {
"P_A_confirmation": (
"Delta-based forensics has already established that abliteration recipes differ along two axes that are "
"visible in the weights: how deep into the stack the edit reaches, and how completely it covers the layers "
"it reaches. Abliterlitics recovers this decomposition by differencing a candidate against its parent, "
"reporting per-recipe layer coverage and edit-magnitude profiles, and reports it on models in the "
"four-billion-parameter class we study [Abliterlitics]. The mechanism we describe recovers the same "
"decomposition from a single checkpoint, with no parent and no prompts; we present it as an independent "
"confirmation of a measured phenomenon rather than as a discovery, and a second instrument that agrees "
"with the first while sharing none of its inputs is stronger evidence about the phenomenon than either "
"instrument alone."
),

"P_B_analytic_boundary": (
"Parent-free spectral detection has a boundary that is analytic rather than empirical. A Householder "
"reflection about a unit vector maps the residual-stream component along that vector to its negation and "
"leaves the orthogonal complement fixed; it is an isometry, so it removes no rank and leaves the Gram "
"spectrum of the edited matrix exactly invariant. Any statistic that reads only that spectrum is therefore "
"blind to it in principle, and the measurement agrees: under the Householder form of ORBA at lambda = 1 the "
"statistic moves by 4.1e-5 in normalised units, less than the 7.3e-5 produced by a Householder reflection "
"about an unrelated random direction. This bounds the class of statistics, not this implementation of one, "
"and it is the reason the geodesic path at lambda = 1 - which rotates the refusal component onto its "
"orthogonal complement and so does remove rank - is detectable while the reflection is not [ORBA]."
),

"P_C_prior_art_concession": (
"Scoring a weight statistic over a band of layers rather than over the whole stack is established practice: "
"the weight signal of the two-signal checkpoint audit is the rank-1 energy fraction of the base-to-candidate "
"difference averaged over a fixed mid-stack band, a primitive that audit credits to WeightWatch "
"[2607.01854, 2508.00161], and delta-based forensics already reports abliteration coverage broken out into "
"early, middle and late bands [Abliterlitics]. Reading the low end of a weight spectrum against a "
"random-matrix null is likewise established, and established as informative: departures from the null "
"appear among the smallest singular values as well as the largest, and removing the deviating small values "
"costs more perplexity than removing values from the bulk [2410.17770]."
),

"P_D_novelty_recovery_variant": (
"Against that background the statistic we report carries four properties together, and we claim novelty "
"only for their conjunction: it is parent-free, requiring no base, sibling or attested reference "
"checkpoint; calibration-free, using no threshold fitted on a labelled panel of edited and clean models; "
"read from the bottom of the spectrum rather than from its top or its heavy-tail exponent; and computed on "
"a sliding window of consecutive layers with the checkpoint scored by the extremum over windows rather than "
"by one pooled or band-averaged value. The fourth property is earned by measurement rather than by "
"construction: the windowed form recovers the band-restricted, small-spread-Gaussian and partial-layer "
"edits that a single pooled statistic misses, which is what a fixed band cannot do and is the reason the "
"window slides. The nearest published work carries three of the four - a bottom-of-spectrum random-matrix "
"analysis that is parent-free and calibration-free but is not windowed and detects no edits [2410.17770], "
"and a sliding-window spectral detector that tracks activations over time rather than weights over depth "
"[2509.15735] - so the conjunction is what is unclaimed, not any single property. The recovery does not "
"extend past the boundary above: completion failures in which a uniform sub-unit kernel weight leaves every "
"layer partially edited, and isometric edits such as a Householder reflection, remain outside reach."
),

"P_E_novelty_nonrecovery_variant": (
"Against that background the statistic we report carries three properties together, and we claim novelty "
"only for their conjunction: it is parent-free, requiring no base, sibling or attested reference "
"checkpoint; calibration-free, using no threshold fitted on a labelled panel of edited and clean models; "
"and read from the bottom of the spectrum rather than from its top or its heavy-tail exponent. The nearest "
"published work is a bottom-of-spectrum random-matrix analysis that shares the first three properties but "
"asks where information is stored in pretrained transformers rather than whether a checkpoint has been "
"edited [2410.17770]; the application to edit detection is what is unclaimed. We also evaluated a windowed "
"variant, in which the statistic is computed on a sliding window of consecutive layers and the checkpoint "
"scored by the extremum over windows, and we report it in Section [X] as a proposed construction rather "
"than as part of the claim: it does not recover the band-restricted, small-spread-Gaussian or partial-layer "
"edits that the pooled statistic misses. That result is informative in its own right and we treat it as the "
"section's main finding. It establishes that those three discovery failures are not artefacts of pooling "
"over depth - a window narrow enough to sit inside the edited band still fails to separate them - so they "
"join the isometries as consequences of what the spectrum can carry, and the boundary of parent-free "
"spectral detection is wider than the pooling argument would predict."
),

"P_F_baseline_bias": (
"Our positive checkpoints were enumerated by keyword sweeps over abliteration vocabulary, and the terms of "
"those sweeps overlap the terms of the filename regex we compare against, so the pool is enriched by "
"construction for exactly the checkpoints the regex can match. The regex's 0.727 sensitivity on this pool "
"is therefore an upper bound on its sensitivity to an arbitrary upload, not an estimate of it, and we "
"report it as such; following the practice of naming and defending the selection criterion of a "
"hub-harvested population [2502.00706], we report the name-discovered and uploader-discovered strata "
"separately rather than pooled. The bound cuts in one direction only and the comparison remains meaningful: "
"model names carry real architectural signal, enough that names alone identify model types at 94% accuracy "
"[2310.01642], so the regex is a serious baseline rather than a convenient one - but naming on the hub is "
"also documented as inconsistent and sometimes misleading [2310.01642], which is precisely why a "
"name-discovered population overstates what a name-based detector achieves in the wild."
),

"P_G_contributions_four_items": [
"A parent-free, calibration-free, bottom-of-spectrum weight statistic that separates abliterated from clean "
"checkpoints without a reference model, without prompts, and without a fitted threshold, evaluated across "
"[N] checkpoints spanning [K] recipe classes and [F] model families.",

"An analytic boundary on parent-free spectral detection: isometric edits leave the Gram spectrum invariant "
"and are undetectable in principle by any statistic that reads it, confirmed by measurement against a "
"random-direction Householder control at matched magnitude - which separates the two ORBA paths, since the "
"geodesic form at lambda = 1 removes rank and the reflection does not.",

"A depth-versus-completeness decomposition of abliteration recipes recovered from a single checkpoint, "
"agreeing with what delta-based forensics measures by differencing against the parent, and grounded at the "
"code level in the recipes themselves: a triangular kernel with a hard cutoff produces partial depth, and a "
"sub-unit uniform kernel produces partial completion.",

"A measured upper bound on the filename baseline that names its own discovery mechanism: because the "
"positive pool was enumerated by keyword search over vocabulary overlapping the regex, the regex's "
"sensitivity on that pool bounds rather than estimates its sensitivity in deployment, and the strata are "
"reported separately.",
],
}

# ---------------------------------------------------------------- Step 6
NUMBERED_WORDING_CORRECTIONS = [
    {"n": 1, "location_hint": "Related work, wherever the two-signal audit's numbers are quoted",
     "current": "AUROC 0.95 versus 0.84 for either signal alone",
     "corrected": ("AUROC 0.95 [.90,.98] for the combined z-sum, 0.90 [.84,.96] for the weight signal alone "
                   "and 0.84 [.75,.92] for the activation signal alone"),
     "reason": ("The published weights-only competitor is 0.90, not 0.84. Quoting 0.84 as 'either signal "
                "alone' understates the nearest weights-only rival and is checkable in one grep.")},
    {"n": 2, "location_hint": "Related work, the registry description",
     "current": "a 273-checkpoint registry on which the audit is evaluated",
     "corrected": ("a 273-checkpoint registry of which 71 were fully processed, yielding a 94-checkpoint "
                   "evaluation set of 57 uncensored and 37 benign edits"),
     "reason": ("The audit is evaluated on 94, not 273. The paper's own scale comparison against it is "
                "misleading at 273 and honest at 94.")},
    {"n": 3, "location_hint": "Related work, Abliterlitics methodology",
     "current": "quotes the METHODOLOGY code line `diff = (variant - base).abs().mean()`",
     "corrected": ("quote the setup requirement instead: 'Create a directory with your base model and "
                   "variants, plus a comparison.json', with `base` a required key of comparison.json"),
     "reason": ("The code line was not re-observed at the master README on 2026-08-14; the setup sentence "
                "was, and it carries the same load. Do not print an unverified code line.")},
    {"n": 4, "location_hint": "Anywhere the Heretic 23/32-layer fingerprint appears",
     "current": "Heretic edits 23 of 32 layers, with layers 0 through 8 untouched",
     "corrected": ("either date the claim to the earlier fetch, or use the depth/completeness numbers "
                   "re-observed on 2026-08-14 for the four-billion-parameter Heretic trials: 50 to 64 "
                   "tensors changed across variants, the averaged variant spreading edits across 34 layers, "
                   "and one variant's 54 tensors a strict subset of another's 62"),
     "reason": "Reporting an unverified number as current is the failure this dossier exists to prevent."},
    {"n": 5, "location_hint": "Anywhere OBLITERATUS's certifier is described",
     "current": "quotes the certify() signature",
     "corrected": ("cite the hosted description instead - a 512-pair harmful/harmless prompt set and a BBP "
                   "phase-transition spectral certification - and the COSMIC default line from the "
                   "spectral_certification.py commit"),
     "reason": "The literal signature was not re-fetched on 2026-08-14; the conclusion is corroborated twice over."},
    {"n": 6, "location_hint": "Introduction and Conclusion",
     "current": "the 12.6-log-unit separation figure",
     "corrected": "delete it in both places",
     "reason": "A toy-scale figure carried into headline positions invites the reader to scale it to the real panel."},
    {"n": 7, "location_hint": "Results, agreement reporting",
     "current": "19/19 with zero disagreements",
     "corrected": ("report it as an internal consistency check on the implementation, not as evidence about "
                   "the phenomenon, or drop it"),
     "reason": "Agreement between two computations of the same quantity is not empirical support."},
    {"n": 8, "location_hint": "Wherever the cost of the parent-free constraint is discussed",
     "current": "parent-free costs nothing",
     "corrected": ("state the cost: the parent-free constraint forgoes the delta, which is what makes "
                   "isometric edits undetectable and rank-preserving recipes hard"),
     "reason": "The claim is false in the direction that matters, and the analytic boundary already states the cost."},
    {"n": 9, "location_hint": "Any load-bearing sentence citing W01 or W04",
     "current": "W01/W04 used as evidence",
     "corrected": "remove them from load-bearing sentences; retain in the appendix table only",
     "reason": "Carried forward from the hypothesis; these members do not survive at scale."},
    {"n": 10, "location_hint": "Every use of 'pre-registered'",
     "current": "pre-registered applied broadly",
     "corrected": "reserve the word for what metric_spec.py stamps; use 'specified in advance' elsewhere",
     "reason": "Pre-registration is a checkable claim about an artifact and dilutes when applied loosely."},
    {"n": 11, "location_hint": "LORCO table header",
     "current": "unlabelled columns",
     "corrected": "label the columns fixed-tau and refit",
     "reason": "The two columns answer different questions and are not comparable without the labels."},
    {"n": 12, "location_hint": "Recipe taxonomy, Heretic entry",
     "current": "Gaussian / bell-curve kernel",
     "corrected": "triangular tent with a hard cutoff, stated directly in the present tense",
     "reason": ("Verified at code level. State it as fact; do not write it as a correction of an earlier "
                "draft, and do not attribute the bell-curve description to anyone.")},
    {"n": 13, "location_hint": "Anywhere E_1 is attributed",
     "current": "E_1 attributed to the two-signal audit",
     "corrected": "attribute the primitive to WeightWatch [2508.00161] and the band-averaging to [2607.01854]",
     "reason": "Straightforward attribution error against an ICLR 2026 paper.",
     "new_from_this_dossier": True},
    {"n": 14, "location_hint": "Method, where the bottom-of-spectrum choice is motivated",
     "current": "no citation",
     "corrected": "cite [2410.17770] for the finding that the smallest singular values depart from the RMT null and carry information",
     "reason": ("Highest-priority addition. Without it the choice reads as arbitrary, and the omission is "
                "the largest citation risk in the current positioning."),
     "new_from_this_dossier": True},
    {"n": 15, "location_hint": "Method, the per-window null",
     "current": "an invented null",
     "corrected": ("adopt the Marchenko-Pastur zero-information null by name, cite [2410.17770] and "
                   "[2608.07921], and keep random-direction controls as magnitude-matched comparators rather "
                   "than as the null"),
     "reason": "An in-field convention exists for the null; adopting it by name is cheaper than defending a new one.",
     "new_from_this_dossier": True},
    {"n": 16, "location_hint": "Results, wherever an extremum-over-windows score is thresholded",
     "current": "a per-window false-positive rate reported as the detector's FPR",
     "corrected": ("calibrate the distribution of the maximum over windows directly and report a "
                   "checkpoint-level FPR; if a per-window rate is also given, label it per-window"),
     "reason": ("No in-field multiple-window convention exists, so this must be constructed and stated. An "
                "uncorrected per-window rate understates the checkpoint-level FPR by roughly the number of windows."),
     "new_from_this_dossier": True},
    {"n": 17, "location_hint": "Recipe taxonomy",
     "current": "nine recipe classes",
     "corrected": ("consider a tenth: concept-registry ridge residualization, in which the refusal direction "
                   "is orthogonalized against a registry of protected-capability concept atoms before "
                   "ablation [2601.08489]"),
     "reason": ("A distinct class from plain ridge rank-k, because the residualization target is a curated "
                "concept registry rather than a regularizer. It predicts a cleaner, lower-rank edit than "
                "unregularized rank-1 ablation and is a coverage gap in the taxonomy."),
     "new_from_this_dossier": True},
]

NEW_RECIPE_CLASSES = [
    ("Concept-registry ridge residualization (Surgical Refusal Ablation, arXiv:2601.08489): builds a registry "
     "of independent Concept Atoms for protected capabilities and stylistic confounds, then uses "
     "ridge-regularized spectral residualization to orthogonalize the refusal vector against them before "
     "ablation. Reported on Qwen3-VL and Ministral at 0-2% refusal with first-token KL 0.044 where standard "
     "ablation on Qwen3-VL-4B gives KL 2.088. Distinct from plain ridge rank-k: the residualization target is "
     "a curated concept set, not a regularizer, so it predicts a lower-rank, more localized edit. "
     "RECOMMENDATION: add as a tenth class; public checkpoints are on the Qwen3-VL-4B family, our own scale."),
]

CLASSIFICATIONS = [
    {"work": "arXiv:2512.13655", "class": "STUDY",
     "finding": ("A tool comparison across Heretic, DECCP, ErisForge and FailSpy on sixteen 7B-14B "
                 "instruction-tuned models, reporting capability metrics (GSM8K change +1.51 pp to -18.81 pp) "
                 "and KL divergence 0.043-1.646. Contains no weights-only detector and no edited/clean "
                 "classification. Useful to us only as a source of recipe-class names and as evidence that "
                 "capability damage is recipe-dependent.")},
    {"work": "arXiv:2601.08489", "class": "RECIPE",
     "finding": "New class; see new_recipe_classes_found. Not a detector."},
    {"work": "arXiv:2510.02768", "class": "STUDY",
     "finding": ("A behavioural evaluation over Safety Pretraining checkpoints for SmolLM2-1.7B: 20 systems, "
                 "100 balanced prompts each, refusal/non-refusal classified by multiple judges. Entirely "
                 "generation-based; no weights-only signature of any kind. Its useful contribution to us is "
                 "the judge-sensitivity result - that judge selection changes evaluation outcomes - which "
                 "supports treating any behavioural label as noisy.")},
    {"work": "arXiv:2607.17427", "class": "STUDY",
     "finding": ("NEWLY SURFACED. Off-target effects of abliteration on decision disposition across two MoE "
                 "families, on a task eliciting no refusals at all. No detector. Two facts are directly "
                 "useful: it reports that abliterated arms differ systematically from base arms on a task "
                 "with no refusals (so 'the base model minus refusals' is not what an abliterated checkpoint "
                 "is), and its provenance audit 'caught two independent contamination channels - a "
                 "mismatched-quantizer pilot pair and a stale community chat template', which is direct "
                 "external support for treating toolchain artifacts as the rule in community-checkpoint studies.")},
]

UNRESOLVED = [
    ("Abliterlitics' per-model report pages, including the Heretic 23/32-layer fingerprint and the 0.997 vs "
     "0.00017 direction-cosine pair, were not re-observed on 2026-08-14 at the URLs reachable from the "
     "master README. The parent requirement, licence and delta character WERE re-verified. Either date those "
     "two numbers to the earlier fetch or replace them with the Qwen3-VL-4B numbers re-observed here."),
    ("OBLITERATUS's certify() signature was not re-fetched from raw source; the conclusion is corroborated on "
     "two mirrors and the COSMIC default is verbatim, but the signature itself should not be printed as a quote."),
    ("The Abliterlitics METHODOLOGY code lines were not present in the README served at master on this date. "
     "Whether they moved to a docs/ path or were removed was not determined."),
    ("No in-field convention exists for the family-wise error rate of a per-layer or per-window spectral "
     "statistic; the imported max-statistic permutation convention is ANALOGOUS and must be labelled as such."),
    ("No published application of capture-recapture to model-hub harvesting was found; the coverage-estimator "
     "suggestion is an unsupported borrowing and is labelled OPTIONAL."),
    ("The numbers 0.727, 0.159, 4.1e-5 and 7.3e-5 used in P-B and P-F come from this project's own "
     "measurements, not from any source in this dossier. They are reproduced in the paragraphs as the "
     "drafter supplied them and were not independently checked here."),
]

# ---------------------------------------------------------------- assemble
structured_answer = {
    "paste_ready_paragraphs": PASTE_READY,
    "windowed_novelty_verdict": WINDOWED_NOVELTY_VERDICT,
    "per_window_null_convention": PER_WINDOW_NULL_CONVENTION,
    "selection_bias_citations": SELECTION_BIAS_CITATIONS,
    "reporting_convention_for_debiased_baseline": REPORTING_CONVENTION,
    "capture_recapture_optional_suggestion": CAPTURE_RECAPTURE_SUGGESTION,
    "positioning_corrections": POSITIONING_CORRECTIONS,
    "reverification_log": REVERIFICATION_LOG,
    "numbered_wording_corrections": NUMBERED_WORDING_CORRECTIONS,
    "new_recipe_classes_found": list(NEW_RECIPE_CLASSES),
    "adjacent_work_classifications": CLASSIFICATIONS,
    "source_ledger": SOURCE_LEDGER,
    "unresolved": UNRESOLVED,
}

SOURCES = [
    (1, "https://arxiv.org/pdf/2607.01854", "Has This Checkpoint Been Abliterated? A Two-Signal Audit and Its Failure Map (Hurtado, 2026)",
     "Supplied the verbatim band-averaged E_1 definition, the WeightWatch attribution, the registry/evaluation-set split (273 registry, 71 processed, 94 evaluated) and the corrected AUROC triple 0.95/0.90/0.84."),
    (2, "https://raw.githubusercontent.com/dreamfast/abliterlitics/master/README.md", "Abliterlitics README (dreamfast)",
     "Re-verified the mandatory `base` key, the setup sentence, the comparison.json schema and the AGPL-3.0 licence; the METHODOLOGY code lines were not present at this URL on this date."),
    (3, "https://arxiv.org/pdf/2604.08844", "Weight-space drift fingerprinting of fine-tuned adapters (Paul, 2026)",
     "Supplied both halves of correction C1 verbatim: the AUC 0.00 / n_bootstrap 972 sentence and the declared confound (generation collapse; GPT-4o scored 0/300)."),
    (4, "https://raw.githubusercontent.com/p-e-w/heretic/master/src/heretic/model.py", "Heretic source, ablation-weight loop",
     "Code-level confirmation that the kernel is a triangular tent with a hard cutoff: the distance computation, the `if distance > params.min_weight_distance: continue` skip, and the linear interpolation."),
    (5, "https://raw.githubusercontent.com/p-e-w/heretic/master/config.default.toml", "Heretic default configuration",
     "Confirmed the shipped default row_normalization = \"full\", i.e. row-magnitude preserving by default."),
    (6, "https://huggingface.co/blog/grimjim/orthogonal-reflection-bounded-ablation", "Orthogonal Reflection Bounded Ablation (Lai, 2026-03-24)",
     "Supplied the two-recipe distinction (geodesic lambda=1 zeroed without reflection versus the Householder isometry) and the author's own misdirected-sign-flips negative."),
    (7, "https://pypi.org/pypi/reverse-abliterate/json", "reverse-abliterate package metadata (Carlos-Projects, MIT)",
     "Supplied the full detection table showing filename/metadata/hook checks only, with SHA-256 manifests as the sole tensor-level check; establishes the name baseline as a shipped tool."),
    (8, "https://arxiv.org/pdf/2607.23711", "The Intruder Threshold: A Spectral Law for LoRA Fine-Tuning (Xie, 2026)",
     "The dossier's most dangerous unadjudicated near-miss, resolved: parent-spectrum-derived but update-requiring via sigma_1(BA), top-of-spectrum, per-layer not sliding, and a law about LoRA dynamics rather than an edit detector."),
    (9, "https://arxiv.org/pdf/2607.03377", "Spectral Signatures of Large Language Models (Zhang et al., KDD 2026)",
     "Confirmed PL_Alpha_Hill is a heavy-tail top-of-spectrum exponent explicitly designed to remain robust during post-training - a stronger ruling-out than metric difference."),
    (10, "https://arxiv.org/abs/2608.07921", "Spectral Outliers Reveal Dominant Learned Structure in Transformer Attention (Dewage et al., ICMLA 2026)",
     "Confirmed the MP bulk/outlier split reads outliers above the edge and targets learned structure in pretrained models, with no edited/clean labels anywhere."),
    (11, "https://arxiv.org/pdf/2410.17770", "Small Singular Values Matter: A Random Matrix Analysis of Transformer Models (Thamm & Rosenow)",
     "NEWLY SURFACED and absent from every dependency. The closest prior art on the bottom-of-spectrum qualifier - parent-free, calibration-free, reads the smallest singular values against an RMT null - and the source of the null convention the paper should adopt by name."),
    (12, "https://arxiv.org/abs/2508.00161", "Watch the Weights: Unsupervised monitoring and control of fine-tuned LLMs (Zhong & Raghunathan, ICLR 2026)",
     "NEWLY SURFACED. The WeightWatch primitive that E_1 is credited to; top singular vectors of the weight difference plus activation-cosine monitoring, so parent-requiring and prompt-requiring. An obligatory citation the dependencies lacked."),
    (13, "https://arxiv.org/pdf/2509.15735", "EigenTrack: Spectral Activation Feature Tracking (Ettori et al.)",
     "Supplied the sliding-window sentence verbatim; the closest published use of the sliding half of the claim, over time across activations rather than over layers across weights."),
    (14, "https://arxiv.org/abs/2608.10172", "Intrinsic Structure: Spectral Identifiability for Mechanistic Interpretability (Dhor & Chen, 2026)",
     "NEWLY SURFACED. Koopman spectrum with depth as time - conceptually nearest to sliding over layers - but recovered from M calibration samples of activations, so neither weights-only nor calibration-free."),
    (15, "https://arxiv.org/pdf/2502.00706", "Model Provenance Testing for Large Language Models",
     "The direct precedent for naming a hub-harvest selection criterion to avoid selection bias, for reporting two differently-constructed populations, and a name-free provenance comparator at 80-90% recall on 600+ models of 30M-4B parameters."),
    (16, "https://arxiv.org/pdf/2310.01642", "Naming Practices of Pre-Trained Models on Hugging Face (Jiang et al.)",
     "The two-edged naming citation: DARA identifies model types from names at 94% accuracy, and the same paper documents that names are often inaccurate and misleading."),
    (17, "https://arxiv.org/abs/2512.13655", "Comparative Analysis of LLM Abliteration Methods (Young)",
     "Classified STUDY: tool comparison with capability and KL metrics, no weights-only detector."),
    (18, "https://arxiv.org/abs/2601.08489", "Surgical Refusal Ablation: Concept-Guided Spectral Cleaning (Cristofano, 2026)",
     "Classified RECIPE and flagged as a tenth recipe class - concept-registry ridge residualization - with public checkpoints on the Qwen3-VL-4B family."),
    (19, "https://arxiv.org/abs/2510.02768", "A Granular Study of Safety Pretraining under Model Abliteration (Agnihotri et al., NeurIPS 2025 workshop)",
     "Classified STUDY: generation-based only; its judge-sensitivity result supports treating behavioural labels as noisy."),
    (20, "https://arxiv.org/abs/2607.17427", "Abliteration Is Not a Scalpel (Fafula, 2026)",
     "NEWLY SURFACED, classified STUDY. Supplies external support that abliterated checkpoints differ from base on refusal-free tasks, and that toolchain contamination is the rule in community-checkpoint studies."),
    (21, "https://kicfk-obliteratus.hf.space/", "OBLITERATUS hosted Space",
     "Corroborated that certification consumes a 512-pair harmful/harmless prompt set via a BBP phase-transition test, i.e. activations rather than weights."),
    (22, "https://huggingface.co/spaces/pliny-the-prompter/obliteratus/commit/f0084ba4c8de46caf272ebe02a6ef925277bc743", "OBLITERATUS spectral_certification.py commit",
     "Confirmed the COSMIC-fused knee detection default verbatim, establishing layer-selectivity."),
    (23, "https://nathan.sapwell.net/posts/qwen3-vl-4b-heretic/", "Qwen3-VL-4B Heretic abliteration report",
     "A re-observed sub-4.5B depth/completeness fingerprint (50-64 tensors changed, 34 layers for the averaged variant, strict-subset structure) usable in place of the unverified 23/32 figure."),
    (24, "https://doi.org/10.1016/j.neuroimage.2014.01.060", "Permutation inference for the general linear model (Winkler et al., NeuroImage 2014)",
     "The ANALOGOUS convention imported for the multiple-window family-wise error problem: calibrate the null distribution of the maximum statistic over the family."),
]

ANSWER_PROSE = """\
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
observes. The shipped default is also row-magnitude preserving, "row_normalization = \\"full\\"" [5].

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
"""

out = {
    "title": "Cutting the novelty claim to what survives",
    "summary": (
        "Iteration-5 positioning dossier. Verdict on the windowed object: NOVEL-NARROW, with two "
        "three-of-four near-misses newly identified. Ships seven paste-ready paragraphs in both outcome "
        "variants, seven positioning corrections with verbatim quotes, a ten-item re-verification log with "
        "two MISMATCHes and four UNREACHABLEs, and seventeen numbered wording corrections."),
    "answer": ANSWER_PROSE,
    "structured_answer": structured_answer,
    "sources": [{"index": i, "url": u, "title": t, "summary": s} for i, u, t, s in SOURCES],
    "follow_up_questions": [
        ("Does arXiv:2410.17770's bottom-of-spectrum RMT deviation move under abliteration at all? It is the "
         "one near-miss that is a single construction step away from the claim, so running its exact "
         "statistic - deviation of the smallest singular values from the Marchenko-Pastur null, per matrix, "
         "no window - as a baseline on our panel would either establish that the sliding window is what buys "
         "the separation or reveal that an already-published statistic does the job, which changes the "
         "verdict from NOVEL-NARROW to an application claim."),
        ("What is the checkpoint-level false-positive rate of an extremum-over-windows score once the "
         "maximum is calibrated directly, and how much higher is it than the per-window rate? No in-field "
         "convention exists, so this number has to be measured rather than cited, and it determines whether "
         "the windowed arm can be claimed at all."),
        ("Does the concept-registry ridge residualization class (arXiv:2601.08489) fall inside or outside "
         "the analytic boundary? It is rank-reducing rather than isometric, so it should be detectable, but "
         "its whole design goal is to minimize spectral disruption to capability subspaces - which is "
         "precisely the property that would make a low-energy edit hard to see from the bottom of the spectrum."),
    ],
}

(WS / "research_out.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
print("wrote research_out.json", (WS / "research_out.json").stat().st_size)

# --------------------------------------------------------------- markdown report
L = []
A = L.append
A("# Cut the Novelty Claim to What Survives\n")
A("Iteration-5 positioning dossier. Fetched **2026-08-14**. Web tools only; no code, no experiments.\n")
A("Every `quote` below is a verbatim substring of the document at the URL beside it, obtained by "
  "fetch/fetch_grep on the date given. Claims that could not be re-quoted are marked UNREACHABLE and are "
  "not softened into prose.\n")

A("## 0. Headline\n")
A("**Verdict on the windowed object: NOVEL-NARROW.** No published work carries all four qualifiers. Two "
  "carry three, along different axes, and both were surfaced by this dossier rather than by any dependency:\n")
A("- **arXiv:2410.17770** (Thamm & Rosenow, *Small Singular Values Matter*) is parent-free, "
  "calibration-free and **bottom-of-spectrum**, lacking only the sliding window - and the application. This "
  "is the single largest citation risk in the current positioning and is absent from the draft.\n")
A("- **EigenTrack, arXiv:2509.15735** is parent-free and **sliding**, but over time across activations "
  "rather than over layers across weights.\n")
A("**Three further findings change what the paper prints.** (i) The band concession is confirmed verbatim, "
  "and the same sentence credits the primitive to **WeightWatch, arXiv:2508.00161 (ICLR 2026)** - an "
  "attribution the draft is missing. (ii) The registry is **273 but only 71 were processed and 94 "
  "evaluated**, and the weights-only competitor scores **0.90, not 0.84**. (iii) Heretic's triangular tent "
  "is re-confirmed **at code level**, and reverse-abliterate's filename-only detection table is re-confirmed "
  "verbatim, so C4 and C5 are now the best-evidenced corrections in the set.\n")
A("**One gap the paper must construct rather than cite:** there is no in-field convention for the "
  "family-wise error rate of a per-layer or per-window statistic. The null itself does have one - "
  "Marchenko-Pastur - and should be adopted by name.\n")

A("## 1. Source ledger\n")
A("| id | url | must supply | status |")
A("|---|---|---|---|")
for r in SOURCE_LEDGER:
    A(f"| {r['id']} | {r['url']} | {r['what_it_must_supply']} | {r['access_status']} |")
A("")

A("## 2. Re-verification of the ten load-bearing quotes (Step 1)\n")
A("| # | item | status |")
A("|---|---|---|")
for i, r in enumerate(REVERIFICATION_LOG, 1):
    A(f"| {i} | {r['item']} | **{r['status']}** |")
A("\nDetail:\n")
for i, r in enumerate(REVERIFICATION_LOG, 1):
    A(f"### {i}. {r['item']} - **{r['status']}**\n")
    A(f"- *dependency recorded:* {r['dependency_value']}")
    A(f"- *observed 2026-08-14:* {r['observed_value']}")
    if r.get("note"):
        A(f"- *consequence:* {r['note']}")
    A("")

A("## 3. Windowed-statistic novelty verdict (Step 2)\n")
A(f"**{WINDOWED_NOVELTY_VERDICT['verdict']}**\n")
A(f"*Scope.* {WINDOWED_NOVELTY_VERDICT['object_under_test']}\n")
A("| work | parent-free | calib-free | bottom | sliding+extremum | ruling |")
A("|---|:--:|:--:|:--:|:--:|---|")
for r in FOUR_QUALIFIER_TABLE:
    tick = lambda b: "yes" if b else "no"
    A(f"| {r['work']} | {tick(r['parent_free'])} | {tick(r['calibration_free'])} | "
      f"{tick(r['bottom_of_spectrum'])} | {tick(r['sliding_extremum'])} | {r['ruling']} |")
A("")
A("Supporting quotes:\n")
for r in FOUR_QUALIFIER_TABLE:
    A(f"- **{r['work']}** - \"{r['quote']}\" ({r['url']})")
A("")
A(f"*Closest rivals.* {WINDOWED_NOVELTY_VERDICT['how_close_the_closest_is']}\n")
A(f"*Saturation.* {WINDOWED_NOVELTY_VERDICT['saturation_point']}\n")
A("| # | query | mode | new relevant hits |")
A("|---|---|---|---|")
for i, q in enumerate(QUERIES_RUN, 1):
    A(f"| {i} | {q['query']} | {q['mode']} | {q['new_relevant_hits']}"
      + (f" - {q['note']}" if q.get("note") else "") + " |")
A("")
A("**Explicitly NOT claimed as new:**\n")
for x in WINDOWED_NOVELTY_VERDICT["explicitly_not_claimed"]:
    A(f"- {x}")
A(f"\n*What would flip the verdict.* {WINDOWED_NOVELTY_VERDICT['what_would_flip_it']}\n")

A("## 4. The per-window null convention (Step 2g)\n")
A(f"**Null: FOUND.** {PER_WINDOW_NULL_CONVENTION['convention']}\n")
A(f"> {PER_WINDOW_NULL_CONVENTION['quote']}\n")
A(f"Citation: {PER_WINDOW_NULL_CONVENTION['citation']}\n")
fw = PER_WINDOW_NULL_CONVENTION["multiple_window_fwer"]
A(f"**Multiple-window FWER: NONE FOUND.** {fw['statement']}\n")
A(f"*Analogous convention to import.* {fw['analogous_convention_to_import']}\n")
A(f"*Operational recommendation (suggestion to the experiment planner).* {fw['operational_recommendation_for_the_experiment_planner']}\n")

A("## 5. Selection bias and the name-search upper bound (Step 3)\n")
for c in SELECTION_BIAS_CITATIONS:
    A(f"### {c['id']} - {c['title']} [{c['directness']}]\n")
    A(f"> {c['quote']}\n")
    A(f"{c['url']} - fetched {c['fetched_date']}\n")
    A(f"*Use:* {c['how_we_use_it']}\n")
A("### Reporting convention\n")
A(REPORTING_CONVENTION + "\n")
A("### Coverage estimator (OPTIONAL suggestion)\n")
A(CAPTURE_RECAPTURE_SUGGESTION + "\n")

A("## 6. Positioning corrections (Step 4)\n")
for c in POSITIONING_CORRECTIONS:
    A(f"### {c['id']}\n")
    A("**Paste-ready:**\n")
    A(f"> {c['claim_as_it_must_appear']}\n")
    A(f"**Quote:** \"{c['quote']}\"\n")
    A(f"**Source:** {c['url']} - {c['anchor']} - fetched {c['fetched_date']}\n")
    A(f"**Draft currently says:** {c['draft_currently_says']}\n")
    if c.get("note"):
        A(f"*{c['note']}*\n")

A("## 7. Paste-ready paragraphs (Step 5)\n")
for k in ["P_A_confirmation", "P_B_analytic_boundary", "P_C_prior_art_concession",
          "P_D_novelty_recovery_variant", "P_E_novelty_nonrecovery_variant", "P_F_baseline_bias"]:
    A(f"### {k}\n")
    A(PASTE_READY[k] + "\n")
A("### P_G contributions (four items, offered as a suggestion the drafter may reorder)\n")
for i, x in enumerate(PASTE_READY["P_G_contributions_four_items"], 1):
    A(f"{i}. {x}\n")
A("**Style self-check.** No paragraph refers to any earlier draft of this work. The words *novel* and "
  "*first* each appear at most once, and only inside the four-qualifier sentence of P-D and P-E. Every "
  "figure carries its unit; intervals are carried where the source reports them. P-C concedes before P-D "
  "claims, in that order.\n")

A("## 8. Adjacent-work classification and new recipe class\n")
for c in CLASSIFICATIONS:
    A(f"- **{c['work']} - {c['class']}.** {c['finding']}")
A("\n**New recipe class found:**\n")
for x in NEW_RECIPE_CLASSES:
    A(f"- {x}")
A("")

A("## 9. Numbered wording corrections (Step 6)\n")
A("| n | location | current | corrected | reason |")
A("|---|---|---|---|---|")
for c in NUMBERED_WORDING_CORRECTIONS:
    star = " (new)" if c.get("new_from_this_dossier") else ""
    A(f"| {c['n']}{star} | {c['location_hint']} | {c['current']} | {c['corrected']} | {c['reason']} |")
A("")

A("## 10. Unresolved\n")
for u in UNRESOLVED:
    A(f"- {u}")
A("")

(WS / "research_report.md").write_text("\n".join(L))
print("wrote research_report.md", (WS / "research_report.md").stat().st_size)
