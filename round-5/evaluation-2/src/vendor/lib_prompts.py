#!/usr/bin/env python3
"""Frozen prompt pools for this experiment, derived from the dependency datasets.

The harmful pool is a SUPERSET of the archived 40-item core, by construction:
    HARMFUL120 = the 80 rows with meta.in_core80 == True
               + 40 more sampled stratified by the 10 categories, seed 20260813
so every cell scored at n = 120 also yields the archived 40-item value from the SAME
generations, which is what makes the two directly comparable.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

from loguru import logger

DEP_PROMPTS = Path("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/"
                   "iter_1/gen_art/gen_art_dataset_1/full_data_out.json")
DEP_SCORES = Path("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/"
                  "iter_2/gen_art/gen_art_dataset_1/full_data_out.json")
DEP_HUB = Path("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/"
               "iter_3/gen_art/gen_art_dataset_1/full_data_out.json")
DEP_RECIPE = Path("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/"
                  "iter_3/gen_art/gen_art_research_1/research_out.json")

SPLIT_SEED = 20260813


class Prompts:
    """Everything measured in this artifact comes from here, deterministically."""

    def __init__(self) -> None:
        d = json.loads(DEP_PROMPTS.read_text())
        folds = {ds["dataset"]: ds["examples"] for ds in d["datasets"]}
        self.assertions: list[str] = []
        assert len(folds) == 8, len(folds)
        assert sum(len(v) for v in folds.values()) == 2113
        self.assertions.append("DEP_PROMPTS: 8 folds / 2113 rows")

        def srt(rows):
            return sorted(rows, key=lambda r: r["metadata_uid"])

        ph = srt(folds["plain_harmful"])
        assert len(ph) == 594, len(ph)
        core80 = [r for r in ph if r["metadata_meta"].get("in_core80")]
        assert len(core80) == 80, len(core80)

        # --- archived CORE40: 4 per category out of core80 (archive-identical) ---
        by_cat: dict[str, list[dict]] = {}
        for r in core80:
            by_cat.setdefault(r["metadata_meta"].get("category", "unknown"), []).append(r)
        core40: list[dict] = []
        for cat in sorted(by_cat):
            core40.extend(by_cat[cat][:4])
        if len(core40) != 40:
            core40 = core80[::2]
        assert len(core40) == 40, len(core40)
        self.core40_uids = [r["metadata_uid"] for r in core40]

        # --- dev10, disjoint from every eval pool (archive-identical) ------------
        rest = [r for r in ph if not r["metadata_meta"].get("in_core80")]
        self.dev10 = [r["input"] for r in rest[:10]]
        self.dev10_uids = [r["metadata_uid"] for r in rest[:10]]

        # --- HARMFUL120 = core80 + 40 stratified from the remainder --------------
        pool = [r for r in rest[10:]]
        by_cat2: dict[str, list[dict]] = {}
        for r in pool:
            by_cat2.setdefault(r["metadata_meta"].get("category", "unknown"), []).append(r)
        rng = random.Random(SPLIT_SEED)
        extra: list[dict] = []
        cats = sorted(by_cat2)
        per = {c: list(by_cat2[c]) for c in cats}
        for c in cats:
            rng.shuffle(per[c])
        i = 0
        while len(extra) < 40:
            progressed = False
            for c in cats:
                if len(extra) >= 40:
                    break
                if i < len(per[c]):
                    extra.append(per[c][i])
                    progressed = True
            if not progressed:
                break
            i += 1
        assert len(extra) == 40, len(extra)
        h120 = core80 + extra
        assert len({r["metadata_uid"] for r in h120}) == 120
        self.harmful120 = [r["input"] for r in h120]
        self.harmful120_uids = [r["metadata_uid"] for r in h120]
        self.harmful40 = [r["input"] for r in core40]
        self.harmful40_uids = list(self.core40_uids)
        assert set(self.core40_uids) <= set(self.harmful120_uids), \
            "CORE40 must be a subset of HARMFUL120"
        assert not (set(self.dev10_uids) & set(self.harmful120_uids))
        self.assertions.append(
            f"HARMFUL120: 80 in_core80 + 40 stratified over {len(cats)} categories "
            f"(seed {SPLIT_SEED}); CORE40 subset: True; dev10 disjoint: True")

        # --- XSTest safe: archived 25 as a prefix of 50 --------------------------
        safe = srt([r for r in folds["xstest_overrefusal"]
                    if r["metadata_meta"].get("label") == "safe"])
        assert len(safe) == 250, len(safe)
        by_pt: dict[str, list[dict]] = {}
        for r in safe:
            by_pt.setdefault(r["metadata_meta"].get("prompt_type", "unknown"), []).append(r)
        xs: list[dict] = []
        i = 0
        while len(xs) < 50:
            for pt in sorted(by_pt):
                if i < len(by_pt[pt]) and len(xs) < 50:
                    xs.append(by_pt[pt][i])
            i += 1
        self.xs50 = [r["input"] for r in xs]
        self.xs50_uids = [r["metadata_uid"] for r in xs]
        self.xs25_uids = self.xs50_uids[:25]
        self.assertions.append("XS50 built stratified by prompt_type; XS25 is its prefix "
                               "(archive-identical ordering)")

        # --- wikitext fluency ----------------------------------------------------
        wik = srt(folds["wikitext_fluency"])
        assert len(wik) == 200, len(wik)
        self.wiki20 = [r["input"] for r in wik[:20]]     # archive used 20 -> gate-comparable
        self.wiki200 = [r["input"] for r in wik]

        # --- layer contrast ------------------------------------------------------
        lc = folds["layer_contrast"]
        lc_h = srt([r for r in lc if r["metadata_meta"]["polarity"] == "harmful"])
        lc_b = srt([r for r in lc if r["metadata_meta"]["polarity"] == "benign"])
        assert len(lc_h) == 128 and len(lc_b) == 128
        self.lc_harmful = [r["input"] for r in lc_h]
        self.lc_benign = [r["input"] for r in lc_b]

        self.panel = [r["metadata_meta"] for r in folds["panel_manifest"]]
        self.rules = _load_rules()
        self.recipe_notes = _load_recipe_notes()
        self.hub_notes = _load_hub_notes()
        logger.info(" | ".join(self.assertions))

    def mirrors_for(self, repo: str) -> list[str]:
        """Ungated mirrors recorded in the panel manifest for a gated repo."""
        out = []
        for r in self.panel:
            if r.get("mirror_of") == repo and r.get("hf_repo_id"):
                out.append(r["hf_repo_id"])
        return out


def _load_rules() -> dict:
    """BLANKET_REFUSER_DISQUALIFICATION thresholds from the DEP_SCORES `rule` rows.

    The rule rows carry their payload under `metadata_payload` (not `metadata_meta`),
    so the threshold is read from there and, failing that, parsed out of the rule's
    own `output` string -- which is the literal predicate.
    """
    import re
    out = {"disqualify_over_refusal": 0.50, "warn_over_refusal": 0.35,
           "source": "default (DEP_SCORES rule row not located)"}
    try:
        d = json.loads(DEP_SCORES.read_text())
        for ds in d["datasets"]:
            if ds["dataset"] != "rule":
                continue
            for r in ds["examples"]:
                if r.get("input") != "BLANKET_REFUSER_DISQUALIFICATION":
                    continue
                pay = r.get("metadata_payload", {}) or {}
                out["source"] = f"DEP_SCORES dataset=rule row={r.get('input')}"
                out["quote"] = str(r.get("output", ""))[:300]
                out["predicate"] = str(pay.get("predicate", ""))[:400]
                for key in ("threshold", "disqualification_threshold",
                            "disqualify_threshold"):
                    if isinstance(pay.get(key), (int, float)):
                        out["disqualify_over_refusal"] = float(pay[key])
                for key in ("warn_threshold", "warning_threshold"):
                    if isinstance(pay.get(key), (int, float)):
                        out["warn_over_refusal"] = float(pay[key])
                m = re.search(r">\s*([01]?\.\d+)", str(r.get("output", "")))
                if m:
                    out["disqualify_over_refusal"] = float(m.group(1))
                    out["threshold_source"] = "parsed from the rule's own output predicate"
                return out
    except Exception as e:                                   # noqa: BLE001
        out["error"] = f"{type(e).__name__}: {e}"
    return out


def _load_recipe_notes() -> dict:
    """The mlabonne Gaussian-kernel equation as recorded in the prior-art dossier."""
    out = {"source": str(DEP_RECIPE), "found": False}
    try:
        txt = DEP_RECIPE.read_text()
        d = json.loads(txt)
        hits = []
        stack = [d]
        while stack:
            o = stack.pop()
            if isinstance(o, dict):
                stack.extend(o.values())
            elif isinstance(o, list):
                stack.extend(o)
            elif isinstance(o, str) and ("gaussian" in o.lower() or "kernel" in o.lower()):
                if "mlabonne" in o.lower() or "exp(" in o.lower() or "sigma" in o.lower():
                    hits.append(o[:900])
        out["found"] = bool(hits)
        out["quotes"] = hits[:6]
    except Exception as e:                                   # noqa: BLE001
        out["error"] = f"{type(e).__name__}: {e}"
    return out


def _load_hub_notes() -> dict:
    """Recipe-class counts + the regex-on-repo-id baseline from DEP_HUB."""
    out = {"source": str(DEP_HUB), "found": False}
    try:
        d = json.loads(DEP_HUB.read_text())
        for ds in d["datasets"]:
            if ds["dataset"] != "edit_manifest":
                continue
            rows = [r.get("metadata_features", {}) for r in ds["examples"]]
            edited = [r for r in rows if r.get("recipe_class")]
            n_regex = sum(1 for r in edited
                          if r.get("repo_id_contains_abliteration_string"))
            classes: dict[str, int] = {}
            for r in edited:
                classes[r["recipe_class"]] = classes.get(r["recipe_class"], 0) + 1
            out.update({"found": True, "n_rows": len(rows), "n_edited": len(edited),
                        "recipe_classes": classes,
                        "repo_id_regex_baseline": (n_regex / len(edited)) if edited else None})
            return out
    except Exception as e:                                   # noqa: BLE001
        out["error"] = f"{type(e).__name__}: {e}"
    return out
