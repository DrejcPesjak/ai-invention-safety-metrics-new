#!/usr/bin/env python3
"""PRE-REGISTERED eligibility rule for the undeclared-edit scan denominator.

This file is FROZEN before any false-positive rate is computed.  method.py
records sha256(eligibility.py) together with a UTC timestamp into
results/eligibility_stamp.json and refuses to compute a rate if the stamp is
written after any rate file exists.  The paper quotes that hash.

A checkpoint is ELIGIBLE iff ALL of E1..E6 hold.  Rejections record the FIRST
rule that fires (in order E1..E6) as `primary_reason`, plus every rule violated.

  E1  n_layers >= 8
  E2  hidden_size >= 128
  E3  param count <= 4.2e9, enforced TWICE -- (a) from the safetensors index /
      config, and (b) from total on-disk safetensors bytes divided by the
      repo's widest declared dtype byte-width.  Both must pass.  The Hub index
      is provably wrong on some repos (dep-dataset found a repo reporting
      6,208,256 params while shipping 159 GB, and two 35B checkpoints reporting
      664,944); double enforcement rejected 25 such rows there.
  E4  NOT a unit-test fixture
  E5  NOT a speculator / draft head (and n_layers > 2)
  E6  NOT a quantized re-upload
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

PARAM_CEILING = 4.2e9
MIN_LAYERS = 8
MIN_HIDDEN = 128
MIN_LAYERS_E5 = 2

FIXTURE_UPLOADERS = {
    "trl-internal-testing", "peft-internal-testing", "llamafactory",
    "echarlaix", "yujiepan", "MaxJeblick", "hmellor",
}
FIXTURE_RE = re.compile(r"(?i)tiny-random|tiny-(gpt2|llama|qwen)|test-?fixture|dummy")
SPECULATOR_RE = re.compile(r"(?i)eagle3?|speculat|draft.?(head|model)|medusa")
QUANT_RE = re.compile(r"(?i)\b(mlx|gptq|awq|bnb|bitsandbytes|int4|int8|4bit|8bit|gguf|exl2)\b")

DTYPE_BYTES = {
    "F64": 8, "I64": 8, "F32": 4, "I32": 4, "BF16": 2, "F16": 2, "I16": 2,
    "F8_E4M3": 1, "F8_E5M2": 1, "I8": 1, "U8": 1, "BOOL": 1, "I4": 1, "U4": 1,
    "float64": 8, "float32": 4, "bfloat16": 2, "float16": 2, "int8": 1,
}

RULE_ORDER = ("E1", "E2", "E3a", "E3b", "E4", "E5", "E6")


def widest_dtype_bytes(param_dtypes: dict | None) -> int:
    """Byte width of the WIDEST dtype the repo declares (default 2 = bf16/fp16)."""
    if not param_dtypes:
        return 2
    widths = [DTYPE_BYTES.get(str(k), 2) for k in param_dtypes]
    return max(widths) if widths else 2


def evaluate(rec: dict) -> dict:
    """Apply E1..E6.

    `rec` keys (all optional; a missing value makes the rule UNDECIDABLE and the
    row is reported as such rather than silently admitted):
        repo_id, n_layers, hidden_size, params_index, safetensors_bytes,
        param_dtypes, tags, quantization_config, uploader
    """
    repo = str(rec.get("repo_id") or "")
    uploader = str(rec.get("uploader") or (repo.split("/")[0] if "/" in repo else ""))
    tags = " ".join(str(t) for t in (rec.get("tags") or []))
    n_layers = rec.get("n_layers")
    hidden = rec.get("hidden_size")
    p_index = rec.get("params_index")
    sbytes = rec.get("safetensors_bytes")
    dbytes = widest_dtype_bytes(rec.get("param_dtypes"))
    p_bytes = (float(sbytes) / dbytes) if sbytes else None

    violated: list[str] = []
    undecidable: list[str] = []

    if n_layers is None:
        undecidable.append("E1")
    elif int(n_layers) < MIN_LAYERS:
        violated.append("E1")

    if hidden is None:
        undecidable.append("E2")
    elif int(hidden) < MIN_HIDDEN:
        violated.append("E2")

    if p_index is None:
        undecidable.append("E3a")
    elif float(p_index) > PARAM_CEILING:
        violated.append("E3a")

    if p_bytes is None:
        undecidable.append("E3b")
    elif p_bytes > PARAM_CEILING:
        violated.append("E3b")

    if uploader in FIXTURE_UPLOADERS or FIXTURE_RE.search(repo):
        violated.append("E4")

    if SPECULATOR_RE.search(repo) or (n_layers is not None and int(n_layers) <= MIN_LAYERS_E5):
        violated.append("E5")

    quantized = bool(rec.get("quantization_config"))
    if quantized or QUANT_RE.search(repo) or QUANT_RE.search(tags):
        violated.append("E6")

    primary = next((r for r in RULE_ORDER if r in violated), None)
    return {
        "repo_id": repo,
        "eligible": bool(not violated and not undecidable),
        "primary_reason": primary,
        "all_reasons": violated,
        "undecidable": undecidable,
        "n_layers": None if n_layers is None else int(n_layers),
        "hidden_size": None if hidden is None else int(hidden),
        "params_index": None if p_index is None else float(p_index),
        "params_from_bytes": None if p_bytes is None else float(p_bytes),
        "widest_dtype_bytes": dbytes,
    }


def self_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
