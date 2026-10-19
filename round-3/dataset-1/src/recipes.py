#!/usr/bin/env python3
"""Recipe-class controlled vocabulary and the card->class labelling rules.

Every pattern below was written against a document actually fetched into
evidence/ (see EVIDENCE_DOCS). The labeller returns the matched span verbatim so
`recipe_evidence` is always a real substring of the card, never a paraphrase.

Precedence is deliberate: the most mechanically specific claim wins, because a
norm-preserving biprojected card also says "abliterated" and would otherwise be
mislabelled R1.
"""

from __future__ import annotations

import re

R1 = "R1_GLOBAL_RANK1_DIM"
R2 = "R2_NORM_PRESERVING_PROJECTED"
R3 = "R3_MULTIDIRECTION_SVD"
R4 = "R4_PARTIAL_LAYER_OR_PER_HEAD"
R5 = "R5_SPECTRAL_CASCADE_DCT"
R6 = "R6_BEHAVIOURAL_SFT_UNCENSORED"
R7 = "R7_MERGE_OF_ABLITERATED"
UNKNOWN = "UNKNOWN"

CLASSES = [R1, R2, R3, R4, R5, R6, R7, UNKNOWN]

EVIDENCE_DOCS = {
    "grimjim_projected": {
        "url": "https://huggingface.co/blog/grimjim/projected-abliteration",
        "supports": [R2],
    },
    "grimjim_normpreserved": {
        "url": "https://huggingface.co/blog/grimjim/norm-preserving-biprojected-abliteration",
        "supports": [R2],
    },
    "mlabonne_abliteration": {
        "url": "https://huggingface.co/blog/mlabonne/abliteration",
        "supports": [R1],
    },
    "heretic_readme": {
        "url": "https://github.com/p-e-w/heretic/blob/master/README.md",
        "supports": [R4],
    },
    "jimplus_readme": {
        "url": "https://github.com/jim-plus/llm-abliteration",
        "supports": [R2, R3],
    },
    "obliteratus_readme": {
        "url": "https://github.com/elder-plinius/OBLITERATUS",
        "supports": [R3, R4],
    },
}

# (class, rule-name, pattern). Order IS precedence.
RULES: list[tuple[str, str, re.Pattern]] = [
    # -- R5 first: the narrowest claim, and the one we most want not to over-assign
    (R5, "spectral_dct", re.compile(r"(?i)(spectral[ _-]?cascade|discrete cosine transform|\bDCT\b|frequency[- ]domain (decomposition|ablation))")),
    # -- R2: norm preservation / projected component removal
    (R2, "norm_preserving", re.compile(r"(?i)(norm[- _]?preserv\w*|biprojected|bi-projected|projected abliterat\w*|--normpreserve|--projected|preserv\w+ (the )?(weight )?norms?|magnitude[- ]preserv\w*)")),
    # -- R3: several directions / an SVD subspace
    (R3, "multi_direction_svd", re.compile(r"(?i)(\bSVD\b|singular value decomposition|multi[- ]?direction\w*|multiple (refusal )?directions|refusal subspace|whitened svd|rank-?[2-9k]\b)")),
    # -- R4: layer band / selected modules / per-head / Heretic's per-layer directions
    (R4, "partial_layer_or_head", re.compile(r"(?i)(heretic|per[- ]layer (refusal |residual )?direction|layer[- ]?range|selected layers|layer band|attention heads?\b.{0,40}(ablat|edit|surg)|per[- ]head|head surgery|only layers \d)")),
    # -- R7: merge lineage
    (R7, "merge_lineage", re.compile(r"(?i)(mergekit|merge(d)? (of|with|using)\b.{0,80}(abliterat|uncensor)|slerp|task[- ]arithmetic|dare[_-]?ties|model stock)")),
    # -- R6: ordinary fine-tuning, no directional weight edit
    # The gap is 300, not 120: cards routinely put a full markdown URL between the
    # verb and the object ("fine-tuned with [BAdam](https://arxiv.org/…) on
    # [org/WizardLM_…_unfiltered_…]"), and a 120-char window silently under-called
    # those to UNKNOWN. Caught by the 10-row hand-check; R6 is vetoed by
    # DIRECTIONAL_EDIT anyway, so widening cannot steal rows from R1-R5.
    # Two hand-check fixes are baked into this pattern:
    #  * LEADING \b on the verbs. Without it "trained" matched inside
    #    `from_pretrained(...)` in a usage snippet, so a code block was being
    #    quoted as a method statement.
    #  * bare "unfiltered" is NOT an object on its own. It has a second, common
    #    sense -- an unfiltered *training corpus* -- and it was labelling a
    #    pedagogy study (unfiltered FineWeb-Edu) as an uncensoring fine-tune.
    #    It now only counts next to explicit censorship language.
    (R6, "behavioural_sft", re.compile(r"(?i)(\b(fine[- ]?tun\w+|trained on|sft|dpo|orpo|kto|rlhf|lora)\b.{0,300}\b(uncensor\w*|unalign\w*|amoral|toxic[- ]dpo)|\b(uncensor\w*)\b.{0,300}\b(fine[- ]?tun\w+|dataset|sft|dpo)|\bunfiltered\b.{0,80}\b(uncensor\w*|refusal|censor\w*)|\b(uncensor\w*|refusal|censor\w*)\b.{0,80}\bunfiltered\b)")),
    # -- R1: the classic single diff-in-means direction, global orthogonalisation.
    #    NOTE the bare word "abliterated" is deliberately NOT here. A card that only
    #    says "this is an abliterated version" states no mechanism, and folding those
    #    into R1 would inflate it until the class meant nothing. They fall through to
    #    AMBIGUOUS -> UNKNOWN, which is the honest reading and the number the coverage
    #    report is actually asking for.
    (R1, "global_rank1_diffmeans", re.compile(r"(?i)(diff\w*[- ]?(in|of)[- ]?means|difference of the means|mean difference between the activations|refusal direction|orthogonaliz\w+|orthogonalis\w+|ablation of the refusal|ablate[sd]? the refusal|project\w+ out (of|the)?\s*(this|that|the)? ?(refusal|direction))")),
    # -- rule (ii): the card names/links a tool whose recipe is documented elsewhere
    (R1, "linked_tool_r1", re.compile(r"(?i)(mlabonne/blog/abliteration|blog/mlabonne/abliteration|Uncensor any LLM with abliteration|remove-refusals-with-transformers|failspy/abliterator|abliterator\.py|refusal_direction)")),
]

# Any claim of a directional weight edit at all. Used to veto R6.
DIRECTIONAL_EDIT = re.compile(
    r"(?i)(abliterat\w+|gabliterat\w+|obliterat\w+|orthogonaliz\w+|orthogonalis\w+|"
    r"refusal direction|refusal subspace|project\w+ out|directional ablation|heretic)"
)

# Card says it was edited but names no mechanism -> UNKNOWN with the phrase quoted.
# Any bare claim of being edited, with no mechanism named anywhere in the card.
# This is the dominant real-world case and its count is a headline number.
# "unfiltered" is excluded here for the same reason it is excluded from R6: on its
# own it more often describes a training corpus than a removed guardrail.
AMBIGUOUS = re.compile(
    r"(?i)(abliterat\w+|gabliterat\w+|obliterat\w+|uncensor\w+|decensor\w+|refusal[- ]?(free|removed)|unalign\w+)"
)


def label(card_text: str | None, base_models: list[str]) -> tuple[str, str, str | None]:
    """-> (recipe_class, label_rule, verbatim_evidence_span or None)."""
    if not card_text:
        # a merge can still be inferred from the declared parent alone
        for bm in base_models:
            if re.search(r"(?i)(abliterat|uncensor|decensor|heretic)", bm) and len(base_models) > 1:
                return R7, "base_model_chain", None
        return UNKNOWN, "no_card", None

    directional = DIRECTIONAL_EDIT.search(card_text)
    for cls, rule, pat in RULES:
        m = pat.search(card_text)
        if not m:
            continue
        # "uncensored fine-tune" phrasing appears on plenty of cards that ALSO
        # describe a weight edit; R6 is the no-directional-edit class by
        # definition, so it may only fire when no such edit is claimed.
        if cls == R6 and directional:
            continue
        # a "merge of X-abliterated" hit only counts as R7 if a parent backs it
        if cls == R7 and not (
            len(base_models) > 1
            or any(re.search(r"(?i)(abliterat|uncensor|heretic)", b) for b in base_models)
            or re.search(r"(?i)mergekit", card_text)
        ):
            continue
        s = max(0, m.start() - 90)
        span = card_text[s : m.end() + 150].strip().replace("\n", " ")
        return cls, rule, re.sub(r"\s+", " ", span)[:300]

    m = AMBIGUOUS.search(card_text)
    if m:
        s = max(0, m.start() - 40)
        span = card_text[s : m.end() + 120].strip().replace("\n", " ")
        return UNKNOWN, "ambiguous", re.sub(r"\s+", " ", span)[:300]

    return UNKNOWN, "no_method_statement", None
