#!/usr/bin/env python3
"""Stage 0: resolve the iteration-1 frozen panel manifest into a <=4.2B checkpoint table.

Reads the frozen 160-row panel_manifest block produced by iteration 1
(run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json),
resolves the parameter count for every row whose manifest param_count is null by
reading the repo's safetensors index / config.json from the HF Hub, and emits the
<=4.2B panel plus the lineage table.

No fabrication: a checkpoint whose parameter count cannot be resolved from the Hub
is recorded with param_source='UNRESOLVED' and excluded from the <=4.2B panel with
an explicit reason, never guessed.
"""

from __future__ import annotations

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from loguru import logger

HERE = Path(__file__).resolve().parent.parent
CACHE = HERE / "cache"
RESULTS = HERE / "results"
LOGS = HERE / "logs"
for d in (CACHE, RESULTS, LOGS):
    d.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOGS / "s0_panel.log"), rotation="30 MB", level="DEBUG")

PANEL_SRC = Path(
    "/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/"
    "gen_art/gen_art_dataset_1/full_data_out.json"
)
PARAM_CEILING = 4.2e9
HDRS = {"User-Agent": "aii-iter2-dataset/1.0"}
_TOK = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
if _TOK:
    HDRS["Authorization"] = f"Bearer {_TOK}"
SESSION = requests.Session()

BYTES_PER_PARAM = {"float32": 4, "float16": 2, "bfloat16": 2, "int8": 1}
QUANT_EXT = (".gguf", ".mnn", ".mnn.weight", ".onnx", ".tflite")


def _get_json(url: str, timeout: int = 30) -> dict | None:
    try:
        r = SESSION.get(url, headers=HDRS, timeout=timeout)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as exc:  # noqa: BLE001 - network best effort, logged
        logger.debug(f"GET failed {url}: {exc}")
        return None


def resolve_params(repo: str, revision: str) -> tuple[int | None, str, dict]:
    """Return (param_count, source, extra_fields).

    Resolution ladder, most to least direct:
      1. HF API safetensors header totals (exact param count, no arithmetic).
      2. model.safetensors.index.json total_size / bytes-per-param.
      3. Dense pytorch_model(.bin) file size / bytes-per-param.
    If the repo publishes only quantised artefacts (GGUF / MNN / ONNX) there is
    no dense parameter count to read and none is invented: the verdict is
    UNRESOLVED_QUANT_ONLY and weight_format records what the repo actually ships.
    """
    rev = revision or "main"
    extra: dict = {}
    cfg = _get_json(f"https://huggingface.co/{repo}/raw/{rev}/config.json")
    if cfg:
        extra = {
            "architecture": (cfg.get("architectures") or [None])[0],
            "model_type": cfg.get("model_type"),
            "n_layers": cfg.get("num_hidden_layers"),
            "hidden_size": cfg.get("hidden_size"),
            "vocab_size": cfg.get("vocab_size"),
        }
    dtype = str((cfg or {}).get("torch_dtype") or "bfloat16")
    bpp = BYTES_PER_PARAM.get(dtype, 2)

    info = _get_json(f"https://huggingface.co/api/models/{repo}?revision={rev}&blobs=true")
    files: list[tuple[str, int]] = []
    if info:
        files = [
            (s.get("rfilename", ""), s.get("size") or 0)
            for s in (info.get("siblings") or [])
        ]
        st = info.get("safetensors") or {}
        total = st.get("total")
        if isinstance(total, int) and total > 0:
            extra["weight_format"] = "SAFETENSORS"
            return total, "HF_API_SAFETENSORS_TOTAL", extra
        params = st.get("parameters") or {}
        if params:
            s = sum(v for v in params.values() if isinstance(v, int))
            if s > 0:
                extra["weight_format"] = "SAFETENSORS"
                return s, "HF_API_SAFETENSORS_PARAMETERS", extra

    idx = _get_json(f"https://huggingface.co/{repo}/raw/{rev}/model.safetensors.index.json")
    if idx:
        tot_bytes = (idx.get("metadata") or {}).get("total_size")
        if isinstance(tot_bytes, int) and tot_bytes > 0:
            extra["weight_format"] = "SAFETENSORS"
            return int(tot_bytes / bpp), f"SAFETENSORS_INDEX_TOTAL_SIZE/{dtype}", extra

    bin_bytes = sum(
        sz for fn, sz in files
        if fn.endswith(".bin") and "pytorch_model" in fn and sz
    )
    if bin_bytes > 0:
        extra["weight_format"] = "PYTORCH_BIN"
        return int(bin_bytes / bpp), f"PYTORCH_BIN_FILE_SIZE/{dtype}", extra

    quant = sorted({
        fn.rsplit(".", 1)[-1].lower()
        for fn, _ in files
        if fn.lower().endswith(QUANT_EXT)
    })
    if quant:
        extra["weight_format"] = "QUANT_ONLY:" + ",".join(quant)
        return None, "UNRESOLVED_QUANT_ONLY", extra
    extra.setdefault("weight_format", "UNKNOWN")
    if info is None:
        try:
            code = SESSION.get(
                f"https://huggingface.co/api/models/{repo}", headers=HDRS, timeout=30
            ).status_code
        except Exception:  # noqa: BLE001
            code = 0
        if code in (401, 403):
            return None, "UNRESOLVED_GATED", extra
        if code == 404:
            return None, "UNRESOLVED_REPO_NOT_FOUND", extra
    return None, "UNRESOLVED", extra


def main() -> None:
    logger.info(f"Loading frozen iteration-1 panel from {PANEL_SRC}")
    blob = json.loads(PANEL_SRC.read_text())
    panel_rows = None
    for ds in blob["datasets"]:
        if ds["dataset"] == "panel_manifest":
            panel_rows = ds["examples"]
    if panel_rows is None:
        raise RuntimeError("panel_manifest block not found in iteration-1 data_out")
    metas = [r["metadata_meta"] for r in panel_rows]
    logger.info(f"Frozen panel: {len(metas)} checkpoints, "
                f"{len(set(m['lineage_id'] for m in metas))} lineages")

    # Resolve EVERY checkpoint from the Hub, not only the nulls. The iteration-1
    # manifest derived param_count from on-disk bytes, which double-counts repos
    # that ship both .safetensors and a duplicate .pth/.bin copy of the same
    # weights (meta-llama/Llama-3.2-1B reads as 2.47B there, 1.24B in the
    # safetensors header). The Hub header is authoritative; the manifest value is
    # kept as param_count_manifest and any >5% disagreement is flagged.
    need = list(metas)
    logger.info(f"Resolving parameter counts from the Hub for all {len(need)} checkpoints")

    def work(m: dict) -> tuple[str, tuple]:
        return m["hf_repo_id"], resolve_params(m["hf_repo_id"], m.get("revision", ""))

    resolved: dict[str, tuple] = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        for repo, res in ex.map(work, need):
            resolved[repo] = res
            logger.info(f"  {repo}: {res[0]} via {res[1]}")

    out = []
    for m in metas:
        rec = dict(m)
        # One manifest row (huihui-ai/gemma-2-2b-it-abliterated, whose repo now 404s
        # on the Hub) carries no revision. Normalise the key so downstream consumers
        # can read it unconditionally; the empty value is the honest one.
        rec.setdefault("revision", "")
        man = int(m["param_count"]) if m.get("param_count") else None
        rec["param_count_manifest"] = man
        pc, src, extra = resolved.get(m["hf_repo_id"], (None, "UNRESOLVED", {}))
        for k, v in extra.items():
            if not rec.get(k) and v:
                rec[k] = v
        if pc:
            rec["param_count_resolved"] = pc
            rec["param_source"] = src
        elif man:
            rec["param_count_resolved"] = man
            rec["param_source"] = f"ITER1_MANIFEST_FALLBACK({src})"
        else:
            rec["param_count_resolved"] = None
            rec["param_source"] = src
        rec["param_manifest_disagrees"] = bool(
            pc and man and abs(pc - man) / max(pc, man) > 0.05
        )
        pc = rec["param_count_resolved"]
        rec["in_panel_le_4p2b"] = bool(pc and pc <= PARAM_CEILING)
        rec["panel_exclusion_reason"] = (
            "" if rec["in_panel_le_4p2b"]
            else (f"param_count={pc}>4.2e9" if pc else rec["param_source"].lower())
        )
        out.append(rec)

    keep = [r for r in out if r["in_panel_le_4p2b"]]
    logger.info(f"Panel <=4.2B: {len(keep)} checkpoints, "
                f"{len(set(r['lineage_id'] for r in keep))} lineages")
    unres = [r for r in out if r["param_source"] == "UNRESOLVED"]
    logger.info(f"UNRESOLVED param_count: {len(unres)} -> {[r['hf_repo_id'] for r in unres]}")

    (RESULTS / "panel_resolved.json").write_text(json.dumps(out, indent=1))
    logger.info(f"Wrote {RESULTS / 'panel_resolved.json'}")


if __name__ == "__main__":
    main()
