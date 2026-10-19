#!/usr/bin/env python3
"""Panel bookkeeping: the archived iteration-2 values and the member selections.

Everything here is derived from the archived artefacts, never hard-coded, so a
change upstream shows up as a load error rather than a silent stale constant.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ITER2 = Path("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/"
             "gen_art/gen_art_experiment_1")
ARCHIVE = ITER2 / "results" / "battery.jsonl"
DIAG = ITER2 / "results" / "diagnostics.json"
CALIB = ITER2 / "results" / "calibration.json"
BEHAV = ITER2 / "results" / "behaviour.jsonl"

D1 = Path("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/"
          "gen_art/gen_art_dataset_1/full_data_out.json")
D2 = Path("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/"
          "gen_art/gen_art_dataset_1/full_data_out.json")

WKEYS = ["W01", "W02", "W03", "W04", "W05"]


@lru_cache(maxsize=1)
def archive() -> dict:
    """repo -> {meta..., 'W': {W01..W05}, 'all': {metric_id: value}}"""
    out: dict[str, dict] = {}
    with open(ARCHIVE) as fh:
        for line in fh:
            r = json.loads(line)
            rec = out.setdefault(r["checkpoint"], {
                "repo": r["checkpoint"], "revision": r["revision"],
                "lineage_id": r["lineage_id"], "family": r["architecture_family"],
                "member_class": r["member_class"], "param_count": r["param_count"],
                "n_layers": r["n_layers"], "hidden_size": r["hidden_size"],
                "renderer": r["renderer"], "tokenizer_family": r["tokenizer_family"],
                "tier": r["tier"], "W": {}, "all": {}})
            if r.get("ok"):
                rec["all"][r["metric_id"]] = r["value"]
                if r["metric_id"][:3] in WKEYS and r["metric_id"][3] == "_":
                    rec["W"][r["metric_id"][:3]] = r["value"]
    return out


@lru_cache(maxsize=1)
def behaviour() -> dict:
    out: dict[str, dict] = {}
    if not BEHAV.exists():
        return out
    with open(BEHAV) as fh:
        for line in fh:
            r = json.loads(line)
            out.setdefault(r.get("checkpoint") or r.get("repo"), {}).update(r)
    return out


@lru_cache(maxsize=1)
def calibration() -> dict:
    return json.loads(CALIB.read_text())


@lru_cache(maxsize=1)
def diagnostics() -> dict:
    return json.loads(DIAG.read_text())


def rho_star() -> float:
    return float(calibration()["rho_star"])


def bare_argmax_depth() -> float:
    """Relative depth of the BARE AUROC argmax, read from CALIB (never hard-coded)."""
    c = calibration()
    return float(c["bare_auroc_argmax_index"]) / float(c["L"])


UPLOADER_OF = {"huihui-ai": "huihui-ai", "Goekdeniz-Guelmez": "Goekdeniz-Guelmez"}


def uploader(repo: str, synthetic: bool = False) -> str:
    if synthetic:
        return "in-house-synthetic"
    return repo.split("/")[0] if "/" in repo else repo


# ---------------------------------------------------------------------------
# GATE MEMBER SELECTION (>=5 abliterated, >=5 non-abliterated).
# The four members the plan REQUIRES are marked; the rest are chosen smallest
# first so the gate fits the download budget.
# ---------------------------------------------------------------------------
GATE_ABLITERATED = [
    "huihui-ai/Qwen2.5-0.5B-Instruct-abliterated",                        # weakest, W05=-2.742
    "huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2",
    "huihui-ai/Llama-3.2-1B-Instruct-abliterated",
    "huihui-ai/Qwen2.5-1.5B-Instruct-abliterated",
    "Goekdeniz-Guelmez/Josiefied-Qwen3-4B-Instruct-2507-gabliterated-v2",  # 2nd weakest + 2nd uploader
]
GATE_NEGATIVE = [
    "allenai/OLMo-1B-hf",            # strongest non-abliterated, W05=-2.665
    "EleutherAI/pythia-410m",
    "Qwen/Qwen2.5-0.5B-Instruct",
    "Qwen/Qwen3-1.7B-Base",          # a Qwen3 BASE member
    "Qwen/Qwen3-1.7B",               # a Qwen3 INSTRUCT member
]
GATE_MEMBERS = GATE_ABLITERATED + GATE_NEGATIVE
GATE_TIER0 = ["huihui-ai/Qwen2.5-0.5B-Instruct-abliterated",
              "huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2",
              "Qwen/Qwen2.5-0.5B-Instruct"]

# Positive-control model: the Qwen3-0.6B INSTRUCT member (its Base sibling has
# W01=0.628 and is the wrong model -- the archive confirms both).
CONTROL_MODEL = "Qwen/Qwen3-0.6B"

# Synthetic-recipe host models (Arm 1B).  Second architecture is Tier 2.
SYNTH_HOSTS = ["Qwen/Qwen3-1.7B", "unsloth/Llama-3.2-1B-Instruct"]

# Arm 2 pairs: (parent, candidate, pair_type).  POSITIVE = abliterated child;
# NEGATIVE = a benign fine-tune step (instruct-vs-base, uncensored-vs-parent).
E1_PAIRS = [
    ("Qwen/Qwen2.5-0.5B-Instruct", "huihui-ai/Qwen2.5-0.5B-Instruct-abliterated", "positive"),
    ("Qwen/Qwen2.5-1.5B-Instruct", "huihui-ai/Qwen2.5-1.5B-Instruct-abliterated", "positive"),
    ("Qwen/Qwen3-0.6B", "huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2", "positive"),
    ("Qwen/Qwen3-1.7B", "huihui-ai/Huihui-Qwen3-1.7B-abliterated-v2", "positive"),
    ("unsloth/Llama-3.2-1B-Instruct", "huihui-ai/Llama-3.2-1B-Instruct-abliterated", "positive"),
    ("unsloth/Llama-3.2-3B-Instruct", "huihui-ai/Llama-3.2-3B-Instruct-abliterated", "positive"),
    ("Qwen/Qwen2.5-0.5B", "Qwen/Qwen2.5-0.5B-Instruct", "negative_instruct_vs_base"),
    ("Qwen/Qwen2.5-1.5B", "Qwen/Qwen2.5-1.5B-Instruct", "negative_instruct_vs_base"),
    ("Qwen/Qwen3-0.6B-Base", "Qwen/Qwen3-0.6B", "negative_instruct_vs_base"),
    ("Qwen/Qwen3-1.7B-Base", "Qwen/Qwen3-1.7B", "negative_instruct_vs_base"),
    ("unsloth/Llama-3.2-1B", "unsloth/Llama-3.2-1B-Instruct", "negative_instruct_vs_base"),
    ("Qwen/Qwen3-1.7B", "UnfilteredAI/DAN-Qwen3-1.7B", "negative_uncensored_vs_parent"),
]

# Tier-2 candidates for REAL new-toolchain checkpoints.  Presence and recipe are
# VERIFIED from the card at run time; nothing here is assumed to exist or qualify.
NEW_TOOLCHAIN_CANDIDATES = [
    "mlabonne/Qwen3-0.6B-abliterated",
    "mlabonne/Qwen2.5-1.5B-Instruct-abliterated",
    "mlabonne/Daredevil-8B-abliterated",     # will be rejected on size; kept as a probe
    "huihui-ai/Qwen3-0.6B-abliterated",
    "grimjim/Llama-3.2-1B-Instruct-abliterated-ortho",
    "byroneverson/Yi-1.5-6B-Chat-abliterated",
    "failspy/Llama-3-8B-Instruct-abliterated",
]
HUB_SEARCH_QUERIES = ["abliterated", "uncensored", "orthogonalized", "ORBA",
                      "norm-preserving", "refusal-removed", "decensored"]
