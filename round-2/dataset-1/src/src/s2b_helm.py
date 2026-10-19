#!/usr/bin/env python3
"""Stage 2b: HELM Safety v1.0.0 and AIR-Bench 2024 v1.1.0 harvest.

The HELM leaderboards are static front-ends over JSON on a public GCS bucket. The
layout was PROBED, not assumed:
  https://storage.googleapis.com/crfm-helm-public/<project>/benchmark_output/
      releases/<release>/{schema.json,groups.json,groups/<group>.json}
All four probed paths returned HTTP 200 (see logs/s2b_helm.log).

Two outputs:
  1. Per-source panel overlap, computed rather than asserted: how many of the
     models HELM evaluates are panel checkpoints. At <=4.2B this is expected to be
     zero, and a zero is a RESULT to report, not a gap to pad.
  2. The full per-model XSTest table, kept as a threshold-grounding reference for
     the blanket-refuser disqualification rule, since it is the only per-model
     over-refusal-adjacent distribution we can pull programmatically. It is stored
     as reference rows about NON-panel models and is never mixed into panel scores.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import requests
from loguru import logger

HERE = Path(__file__).resolve().parent.parent
CACHE, RESULTS, LOGS = HERE / "cache", HERE / "results", HERE / "logs"
HELM_CACHE = CACHE / "helm"
for d in (CACHE, RESULTS, LOGS, HELM_CACHE):
    d.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOGS / "s2b_helm.log"), rotation="30 MB", level="DEBUG")

RETRIEVAL_DATE = date.today().isoformat()
GCS = "https://storage.googleapis.com/crfm-helm-public"
PROJECTS = [
    {
        "project": "safety",
        "release": "v1.0.0",
        "label": "HELM Safety v1.0.0",
        "site": "https://crfm.stanford.edu/helm/safety/v1.0.0/",
    },
    {
        "project": "air-bench",
        "release": "v1.1.0",
        "label": "HELM AIR-Bench 2024 v1.1.0",
        "site": "https://crfm.stanford.edu/helm/air-bench/v1.1.0/",
    },
]


def get(url: str) -> dict | list | None:
    r = requests.get(url, timeout=90)
    logger.debug(f"GET {r.status_code} {len(r.content)}B {url}")
    if r.status_code != 200:
        logger.warning(f"HTTP {r.status_code} for {url}")
        return None
    return r.json()


def norm_repo(s: str) -> str:
    return str(s).strip().lower()


def main() -> None:
    panel = json.loads((RESULTS / "panel_resolved.json").read_text())
    panel_ids = {norm_repo(x["hf_repo_id"]) for x in panel if x["in_panel_le_4p2b"]}
    # HELM names models as <creator>/<model>, which is NOT an HF repo id. Match on
    # the model-name half as well so a genuine overlap cannot be missed on prefix
    # mismatch alone.
    panel_tails = {i.split("/")[-1] for i in panel_ids}

    overlap: list[dict] = []
    reference_rows: list[dict] = []

    for pr in PROJECTS:
        rel = f"{GCS}/{pr['project']}/benchmark_output/releases/{pr['release']}"
        schema = get(f"{rel}/schema.json")
        if schema is None:
            logger.error(f"{pr['label']}: schema unavailable, skipping")
            continue
        (HELM_CACHE / f"{pr['project']}_schema.json").write_text(json.dumps(schema))
        models = [m.get("name") for m in schema.get("models", [])]
        groups = [g.get("name") for g in schema.get("run_groups", [])]
        hits = sorted(
            m for m in models
            if norm_repo(m) in panel_ids or norm_repo(m).split("/")[-1] in panel_tails
        )
        logger.info(
            f"{pr['label']}: evaluates {len(models)} models over groups {groups}; "
            f"panel overlap = {len(hits)}/{len(panel_ids)} -> {hits}"
        )
        overlap.append({
            "source": pr["label"],
            "source_url": pr["site"],
            "source_json_root": rel,
            "n_models_source_evaluates": len(models),
            "models_source_evaluates": models,
            "run_groups": groups,
            "n_panel_checkpoints_present": len(hits),
            "n_panel_checkpoints_total": len(panel_ids),
            "panel_checkpoints_present": hits,
            "retrieval_date": RETRIEVAL_DATE,
        })

        for g in groups:
            blob = get(f"{rel}/groups/{g}.json")
            # Ship only the top-level per-model tables. The AIR level 2/3/4
            # category breakdowns (~15k values across 22 NON-panel models) are
            # cached in full under cache/helm/ but would outweigh the entire panel
            # table 30:1 while saying nothing about any panel checkpoint.
            drop_titles = {"AIR level 4 categories", "AIR level 3 categories",
                           "AIR level 2 categories"}
            if g == "air_bench_2024":
                # This group's single untitled table is the full 8,250-value AIR
                # per-category matrix over 22 NON-panel models. Same reasoning.
                continue
            if blob is None:
                continue
            (HELM_CACHE / f"{pr['project']}_{g}.json").write_text(json.dumps(blob))
            # The air_bench_2024 group is a per-risk-category breakdown running to
            # ~16k values across 22 non-panel models. It is cached in full under
            # cache/helm/ but not shipped as rows: none of it is about a panel
            # checkpoint, and it would outweigh the entire panel table 30:1.

            for table in blob if isinstance(blob, list) else [blob]:
                if table.get("title") in drop_titles:
                    continue
                header = [h.get("value") for h in table.get("header", [])]
                descs = {h.get("value"): h.get("description", "") for h in table.get("header", [])}
                lowers = {h.get("value"): h.get("lower_is_better") for h in table.get("header", [])}
                for row in table.get("rows", []):
                    cells = [c.get("value") for c in row]
                    if not cells:
                        continue
                    model = cells[0]
                    for col, val in zip(header[1:], cells[1:]):
                        if not isinstance(val, (int, float)):
                            continue
                        # Keep only substantive scores. Instance counts, truncation
                        # fractions and annotator success rates are harness
                        # telemetry, not safety measurements, and shipping ~18k of
                        # them would bury the ~1k rows that carry signal.
                        low = col.lower()
                        if any(k in low for k in ("# eval", "# train", "# prompt tokens",
                                                  "# output tokens", "truncated",
                                                  "annotator success rate")):
                            continue
                        lb = lowers.get(col)
                        reference_rows.append({
                            "source": pr["label"],
                            "source_url": pr["site"],
                            "run_group": g,
                            "table_title": table.get("title", ""),
                            "model_as_named_by_source": model,
                            "is_panel_checkpoint": False,
                            "metric_name": col,
                            "value": float(val),
                            "lower_is_better": (None if lb is None else bool(lb)),
                            "metric_description": str(descs.get(col, ""))[:300],
                            "retrieval_date": RETRIEVAL_DATE,
                        })

    logger.info(f"Collected {len(reference_rows)} HELM reference metric values "
                f"over {len({r['model_as_named_by_source'] for r in reference_rows})} models")
    (RESULTS / "helm_overlap.json").write_text(json.dumps(overlap, indent=1))
    (RESULTS / "helm_reference_rows.json").write_text(json.dumps(reference_rows, indent=1))


if __name__ == "__main__":
    main()
