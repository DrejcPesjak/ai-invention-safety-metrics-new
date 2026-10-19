#!/usr/bin/env python3
"""Shared constants, dependency loading, and the frozen selection predicates.

Everything downstream (method.py, verify.py) imports its constants from here so a
number can never be typed twice.  The three that matter:

  TAU_PANEL  the panel-fitted detection threshold, detect <=> W05 <= TAU_PANEL
  TAU_REFIT  the leave-one-recipe-class-out refit threshold
  REGEX_11   the eleven repo-name substrings the archived baseline used, copied
             verbatim out of iter_4/gen_art_experiment_1/method.py lines 1518-1519
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = Path("/ai-inventor/aii_data/runs")

# ---------------------------------------------------------------- dependencies
DEP_PROMPTS = RUNS / "run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json"
DEP_RULES = RUNS / "run_UtpduT_D2IS2/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/full_data_out.json"
DEP_EDIT = RUNS / "run_UtpduT_D2IS2/3_invention_loop/iter_3/gen_art/gen_art_dataset_1/full_data_out.json"
DEP_EDIT_DIR = DEP_EDIT.parent
DEP_RECIPE = RUNS / "run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_research_1/research_out.json"

ARCH4 = RUNS / "run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art"
ARCH4_E1 = ARCH4 / "gen_art_experiment_1"
ARCH4_E2 = ARCH4 / "gen_art_experiment_2"
ARCH4_E3 = ARCH4 / "gen_art_experiment_3"

RESULTS = HERE / "results"
CACHE = HERE / "hf_cache"
LOGS = HERE / "logs"

# ---------------------------------------------------------------- constants
TAU_PANEL = -2.7415117804288127
TAU_REFIT = -1.7156

# VERBATIM from ARCH4_E1/method.py -- do not retype from memory.
REGEX_11 = ("abliterat", "uncensor", "decensor", "heretic", "obliterat",
            "amoral", "unalign", "nsfw", "gabliterat", "jailbr", "dolphin")

PARAM_CEILING = 4.2e9
MIN_LAYERS = 8
MIN_HIDDEN = 128

# the 61 iteration-3 Hub sweeps, copied verbatim from
# iter_3/gen_art_dataset_1/harvest_enumerate.py
SEARCH_TERMS = [
    "abliterated", "gabliterated", "obliterated", "uncensored", "decensored",
    "orthogonalized", "norm-preserved", "biprojected", "refusal", "Josiefied",
    "lorablated", "heretic", "unaligned", "refusal-removed",
    "projected abliteration", "amoral", "toxic-dpo", "unfiltered", "no-refusal",
    "safetensors abliterated",
]
SWEEP_AUTHORS = [
    "huihui-ai", "Goekdeniz-Guelmez", "mlabonne", "grimjim", "failspy",
    "byroneverson", "NousResearch", "lunahr", "prithivMLmods", "DavidAU",
    "cognitivecomputations", "TheDrummer", "nicoboss", "bunnycore", "Undi95",
    "Delta-Vector", "ClaudioItaly", "nbeerbower", "p-e-w", "SicariusSicariiStuff",
]
SWEEP_ARCHES = [
    "qwen2", "qwen3", "llama", "gemma2", "gemma3", "phi3", "mistral", "olmo",
    "olmo2", "gpt_neox", "stablelm", "granite", "falcon", "minicpm", "smollm",
    "smollm3", "exaone", "internlm2", "cohere", "bloom",
]

QUANT_FILE_RE = re.compile(r"gptq|awq|bnb|4bit|8bit|mlx|gguf|quantiz", re.IGNORECASE)


# ---------------------------------------------------------------- predicates
def name_hit(repo_id: str) -> bool:
    """The archived repo-name-regex baseline: any of the 11 terms as a substring."""
    low = str(repo_id).lower()
    return any(t in low for t in REGEX_11)


def term_reachable(repo_id: str) -> str | None:
    """Which of the 20 iteration-3 SEARCH TERMS a plain name search would match.

    Multi-word terms ('projected abliteration') are matched token-wise, which is
    the CONSERVATIVE reading: it makes the term-reachable set LARGER and therefore
    the name-free stratum smaller and purer.
    """
    low = str(repo_id).lower()
    for t in SEARCH_TERMS:
        if all(tok in low for tok in t.lower().split()):
            return t
    return None


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def rate_ci(k: int, n: int) -> dict:
    lo, hi = wilson(k, n)
    return {"k": int(k), "n": int(n),
            "rate": (float(k) / n) if n else None,
            "wilson_lo": lo, "wilson_hi": hi,
            "ci_method": "Wilson score, z=1.96"}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ---------------------------------------------------------------- dep loading
class Deps:
    """The four dependency artefacts, loaded once."""

    def __init__(self) -> None:
        d = json.loads(DEP_EDIT.read_text())
        folds = {ds["dataset"]: ds["examples"] for ds in d["datasets"]}
        self.edit_manifest = [e["metadata_features"] for e in folds["edit_manifest"]]
        self.hub_scan_pool = [e["metadata_features"] for e in folds["hub_scan_pool"]]
        self.sft_benign = folds["sft_benign"]
        self.fluency_wikitext = folds["fluency_wikitext"]
        self.heldout_benign_prompts = folds["heldout_benign_prompts"]
        self.edited = [r for r in self.edit_manifest if not r.get("is_parent")]
        self.parents = [r for r in self.edit_manifest if r.get("is_parent")]
        self.by_repo = {r["repo_id"]: r for r in self.edit_manifest}

        # stored sweep provenance -- `found_by` per repo, and the per-query hit
        # lists.  The plan assumed this was unrecoverable; it is not.
        en = json.loads((DEP_EDIT_DIR / "results/enumerated.json").read_text())
        self.sweep_queries = en["queries"]
        self.found_by = {m["repo_id"]: (m.get("found_by") or []) for m in en["models"]}
        self.n_enumerated = len(en["models"])

        # iteration-2 rules / external scores / frozen split
        r2 = json.loads(DEP_RULES.read_text())
        self.rules_blocks = {ds["dataset"]: ds["examples"] for ds in r2["datasets"]}
        self.rules_metadata = r2.get("metadata", {})

        # iteration-4 recipe dossier
        self.recipe_dossier = json.loads(DEP_RECIPE.read_text())

    # -- discovery channels ------------------------------------------------
    def channels(self, repo_id: str) -> set[str]:
        return {q.split(":")[0] for q in self.found_by.get(repo_id, [])}

    def is_name_free_discovered(self, repo_id: str) -> bool:
        """Discovered ONLY by a channel that cannot see abliteration vocabulary.

        arch:<model_type> enumerates a whole architecture; top:all enumerates by
        download count.  Neither can be biased toward names containing the 11
        regex terms.  search:<term> and author:<uploader> both can.
        """
        ch = self.channels(repo_id)
        return bool(ch) and ch <= {"arch", "top"}


def safetensors_bytes(rec: dict) -> int:
    wb = rec.get("weight_bytes_by_format") or {}
    v = wb.get("safetensors")
    if v:
        return int(v)
    return int(rec.get("total_safetensors_bytes") or 0)


def prescreen(rec: dict, max_bytes: float = 12e9) -> str | None:
    """armA_select-style prescreen.  Returns the FIRST failing reason, or None."""
    p = rec.get("param_count_hub") or 0
    if p <= 0:
        return "no_param_count"
    if p > PARAM_CEILING:
        return "param_ceiling"
    if rec.get("model_type") in ("gpt2", "gptj", "gpt_bigcode"):
        return "unsupported_arch"
    sb = safetensors_bytes(rec)
    if sb <= 0:
        return "no_safetensors"
    if sb > max_bytes:
        return "too_big"
    files = " ".join(f.get("rfilename", "").lower() for f in (rec.get("files") or []))
    if files and QUANT_FILE_RE.search(files):
        return "quantized"
    return None
