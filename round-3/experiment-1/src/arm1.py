#!/usr/bin/env python3
"""ARM 1 -- recipe scope: how far does the weight scar reach?

A. REAL new-toolchain checkpoints.  Verified from CARD EVIDENCE, never the repo
   name.  Anything that resolves to 'all-layer global single-direction
   diff-in-means' is labelled as the SAME recipe class as the existing eight and
   is explicitly NOT counted as recipe diversity.
B. SYNTHETIC recipe variants built in house, so the recipe is known exactly:
   norm-preserving projection, rank-k multi-direction (k in 2/4/8), per-head
   surgery, and the LAYER-FRACTION SWEEP that turns the known band-limited blind
   spot into a measured curve with a crossing point f*.

Every synthetic variant also gets a fluency check and a greedy harmful-refusal
rate, so 'the edit worked behaviourally' and 'the edit is visible in the weights'
stay separable -- that is what makes a W05 miss interpretable.
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import torch
from loguru import logger

WS = Path(__file__).resolve().parent
sys.path.insert(0, str(WS))
RES = WS / "results"

import hubio  # noqa: E402
import panel as P  # noqa: E402
import vendored_lib_data as LD  # noqa: E402
import vendored_lib_metrics as LM  # noqa: E402
import wstats  # noqa: E402
from e1 import e1_from_state_dicts  # noqa: E402
from edits import (WriteMatrixStore, measure_edited, rank_k_subspace,  # noqa: E402
                   refusal_direction)
from method import DEV, N_RANDOM, SEED, jdump, jlines, load_model  # noqa: E402

LAYER_FRACTIONS = [0.10, 0.25, 0.33, 0.50, 0.67, 0.80, 1.00]
RANK_KS = [2, 4, 8]

# Pre-registration, written BEFORE arm1 was run (see results/prereg_arm1.json).
PREREGISTERED_PREDICTION = (
    "W05 AUROC drops materially (below 0.8) on abliteration recipes that are "
    "mechanically different from the all-layer global single-direction "
    "diff-in-means class, and the layer-fraction curve has a crossing point "
    "f* strictly above 0.33 -- i.e. the scar is a property of GLOBAL surgery, "
    "not of abliteration as such."
)

GLOBAL_DIM_PATTERNS = [
    r"diff[- ]?in[- ]?means", r"difference[- ]in[- ]means", r"refusal direction",
    r"orthogonaliz", r"ablitera", r"remove[- ]refusals",
]
DIFFERENT_RECIPE_PATTERNS = {
    "norm_preserving": [r"norm[- ]preserv", r"rescal", r"renormalis", r"renormaliz"],
    "multi_direction": [r"multi[- ]direction", r"rank[- ]?k", r"multiple directions",
                        r"top[- ]k directions", r"subspace"],
    "per_head": [r"per[- ]head", r"head[- ]wise", r"individual heads"],
    "layer_range": [r"layer[- ]range", r"selected layers", r"subset of layers",
                    r"partial[- ]layer", r"layer[- ]selective"],
    "orthogonal_reflection": [r"orba", r"reflection", r"householder"],
    "spectral": [r"\bdct\b", r"spectral", r"fourier"],
}


# ===========================================================================
# A. real new-toolchain checkpoints -- Hub search + card verification
# ===========================================================================
def card_text(repo: str) -> tuple[str, str]:
    from huggingface_hub import HfApi
    try:
        info = HfApi().model_info(repo, files_metadata=False)
        card = getattr(info, "card_data", None)
        txt = ""
        try:
            from huggingface_hub import ModelCard
            txt = ModelCard.load(repo).text or ""
        except Exception:  # noqa: BLE001
            txt = json.dumps(card.to_dict() if card else {})
        return txt, f"https://huggingface.co/{repo}"
    except Exception as exc:  # noqa: BLE001
        return "", f"ERROR:{str(exc)[:200]}"


def classify_recipe(text: str) -> dict:
    low = (text or "").lower()
    hits = {}
    for cls, pats in DIFFERENT_RECIPE_PATTERNS.items():
        for p in pats:
            m = re.search(p, low)
            if m:
                s = max(0, m.start() - 140)
                hits[cls] = text[s:m.end() + 160][:300]
                break
    global_hit = None
    for p in GLOBAL_DIM_PATTERNS:
        m = re.search(p, low)
        if m:
            s = max(0, m.start() - 140)
            global_hit = text[s:m.end() + 160][:300]
            break
    if hits:
        cls = sorted(hits)[0]
        return {"recipe_class": cls, "mechanically_different": True,
                "evidence_tier": 1, "evidence_quote": hits[cls],
                "all_class_hits": sorted(hits)}
    if global_hit:
        return {"recipe_class": "global_diff_in_means", "mechanically_different": False,
                "evidence_tier": 1, "evidence_quote": global_hit, "all_class_hits": []}
    return {"recipe_class": "unverified", "mechanically_different": False,
            "evidence_tier": 0, "evidence_quote": "", "all_class_hits": []}


def hub_search(limit_per_query: int = 60) -> dict:
    """Record the search that establishes how many candidates exist at <=4.2B."""
    from huggingface_hub import HfApi
    api = HfApi()
    found, per_q = {}, {}
    for q in P.HUB_SEARCH_QUERIES:
        ms, err = [], None
        for kw in ({"sort": "downloads"}, {}):
            try:
                ms = list(api.list_models(search=q, limit=limit_per_query, **kw))
                err = None
                break
            except Exception as exc:  # noqa: BLE001
                err = str(exc)[:200]
        if err is not None:
            per_q[q] = {"error": err, "n": 0}
            continue
        per_q[q] = {"n_returned": len(ms)}
        for m in ms:
            found.setdefault(m.id, {"repo": m.id, "downloads": getattr(m, "downloads", 0),
                                    "queries": []})["queries"].append(q)
    return {"queries": P.HUB_SEARCH_QUERIES, "per_query": per_q,
            "n_unique_repos": len(found), "repos": found,
            "date": time.strftime("%Y-%m-%d"),
            "note": "search only; size and recipe are VERIFIED per candidate below"}


def param_count(repo: str) -> float | None:
    from huggingface_hub import HfApi
    try:
        info = HfApi().model_info(repo, files_metadata=False)
        st = getattr(info, "safetensors", None)
        if st is not None and getattr(st, "total", None):
            return float(st.total)
        for k in ("safetensors", "config"):
            v = getattr(info, k, None)
            if isinstance(v, dict) and v.get("total"):
                return float(v["total"])
    except Exception:  # noqa: BLE001
        return None
    return None


def verify_candidates(cands: list[str], search: dict) -> list[dict]:
    rows = []
    for repo in cands:
        n = param_count(repo)
        txt, url = card_text(repo)
        cls = classify_recipe(txt)
        rows.append({"repo": repo, "uploader": P.uploader(repo), "params": n,
                     "size_ok": (n is not None and n <= 4.2e9),
                     "evidence_url": url, "card_chars": len(txt),
                     "downloads": search["repos"].get(repo, {}).get("downloads"),
                     **cls})
        logger.info(f"candidate {repo}: params={n} class={cls['recipe_class']} "
                    f"different={cls['mechanically_different']}")
    return rows


# ===========================================================================
# B. synthetic recipe variants
# ===========================================================================
def refusal_dir_for(rn, inputs, rho: float) -> tuple[torch.Tensor, torch.Tensor, dict]:
    """Diff-in-means refusal direction at the member's own rho* depth, from the
    FROZEN layer_contrast FIT fold (64 harmful + 64 benign), last prompt token."""
    h = [r["input"] for r in inputs.lc_fit["harmful"]]
    b = [r["input"] for r in inputs.lc_fit["benign"]]
    hs, _ = rn.last_token_states(h + b, batch=8)
    L_sel = max(0, min(rn.L - 1, int(round(rho * rn.L))))
    r, D = refusal_direction(hs, len(h), L_sel)
    return r, D, {"L_sel": L_sel, "rho_star": rho, "n_harmful": len(h), "n_benign": len(b),
                  "hs_shape": list(hs.shape)}


def behaviour_probe(rn, inputs, max_new: int = 32) -> dict:
    """Cheap separability check: does the edit work BEHAVIOURALLY, and is the
    model still fluent?  Kept small on purpose (no judge calls, $0)."""
    fl_texts = [r["input"] for r in inputs.benign40[:3]]
    hm_texts = [r["input"] for r in inputs.core40[:20]]
    gt_f, _n, _f, _c = rn.generate(fl_texts, max_new_tokens=max_new, batch=4)
    gt_h, _n2, _f2, _c2 = rn.generate(hm_texts, max_new_tokens=max_new, batch=8)
    flags = LM.degeneracy_flags(gt_f + gt_h)
    rate = float(np.mean([LD.is_refusal(t) for t in gt_h]))
    return {"harmful_refusal_rate": rate, "n_harmful_probe": len(hm_texts),
            "n_fluency_probe": len(fl_texts), **flags,
            "degenerate": bool(flags["unreliable"]),
            "sample_generation": (gt_f[0] if gt_f else "")[:200]}


def synth_variants(host: str, inputs, *, do_e1: bool = True) -> list[dict]:
    """Every synthetic recipe on one host model."""
    from stages import LocalRunner, attach_lexicon
    arch = P.archive().get(host, {})
    rec = hubio.ensure(host, arch.get("revision"))
    rho = P.rho_star()
    rn = LocalRunner(rec["path"], host, arch.get("renderer", "chatml"), device=DEV)
    attach_lexicon(rn, inputs, arch.get("tokenizer_family", ""))
    r, D, dmeta = refusal_dir_for(rn, inputs, rho)
    n_heads = int(getattr(rn.model.config, "num_attention_heads", 0)) or None

    st = WriteMatrixStore(rn.model)
    parent_sd = {k: v.detach().cpu().clone()
                 for k, v in rn.model.state_dict().items()
                 if k.endswith((".o_proj.weight", ".down_proj.weight"))}

    base_w = measure_edited(st, n_random=N_RANDOM, seed=SEED, device=DEV)
    base_beh = behaviour_probe(rn, inputs)
    rows: list[dict] = []

    def emit(vid, recipe, audit, note="", **kw):
        w = measure_edited(st, n_random=N_RANDOM, seed=SEED, device=DEV)
        beh = behaviour_probe(rn, inputs)
        e1 = {}
        if do_e1:
            cand_sd = {k: v.detach().cpu().clone()
                       for k, v in rn.model.state_dict().items() if k in parent_sd}
            e1 = e1_from_state_dicts(parent_sd, cand_sd, rn.L, device=DEV)
            del cand_sd
        row = {"variant_id": vid, "host": host, "host_revision": rec["revision"],
               "recipe": recipe, "synthetic": True, "uploader": "in-house-synthetic",
               "recipe_class": recipe, "mechanically_different": recipe != "plain",
               "evidence_tier": 0, "evidence_quote": "built in house; recipe known exactly",
               "evidence_url": "", "family": arch.get("family"),
               "lineage_id": arch.get("lineage_id", host), "params": arch.get("param_count"),
               "declared_class": "abliterated_synthetic",
               "W01": w.W01, "W02": w.W02, "W03": w.W03, "W04": w.W04, "W05": w.W05,
               "cos_v1_r": abs(float(np.dot(w.v1, r.numpy()))),
               "delta_W05_vs_host": w.W05 - base_w.W05,
               "behaviour": beh, "behaviour_delta_refusal": beh["harmful_refusal_rate"] -
               base_beh["harmful_refusal_rate"],
               "degenerate": beh["degenerate"], "E1_vs_parent": e1.get("E1"),
               "E1_detail": e1, "audit": audit, "note": note,
               "direction_meta": dmeta, "seconds": w.seconds, **kw}
        rows.append(row)
        logger.info(f"  {vid}: W01={w.W01:.3f} W02={w.W02:.3f} W05={w.W05:.3f} "
                    f"cos={row['cos_v1_r']:.3f} refuse={beh['harmful_refusal_rate']:.2f} "
                    f"degen={beh['degenerate']} E1={e1.get('E1')}")
        return row

    # host itself, unedited, as the in-panel reference
    rows.append({"variant_id": f"{host}::unedited", "host": host, "recipe": "none",
                 "synthetic": False, "uploader": P.uploader(host),
                 "recipe_class": "unedited", "mechanically_different": False,
                 "evidence_tier": 3, "evidence_quote": "", "evidence_url": "",
                 "family": arch.get("family"), "lineage_id": arch.get("lineage_id", host),
                 "params": arch.get("param_count"),
                 "declared_class": arch.get("member_class", "instruct"),
                 "W01": base_w.W01, "W02": base_w.W02, "W03": base_w.W03,
                 "W04": base_w.W04, "W05": base_w.W05,
                 "cos_v1_r": abs(float(np.dot(base_w.v1, r.numpy()))),
                 "delta_W05_vs_host": 0.0, "behaviour": base_beh,
                 "behaviour_delta_refusal": 0.0, "degenerate": base_beh["degenerate"],
                 "E1_vs_parent": None, "E1_detail": {}, "audit": {}, "note": "host reference",
                 "direction_meta": dmeta, "seconds": base_w.seconds})

    # (0) plain global projection -- the reference recipe class
    a = st.apply("plain", r=r, f=1.0, device=DEV)
    emit(f"{host}::plain_f1.00", "plain", a, "the huihui/global reference recipe")
    # (a) norm-preserving projection
    a = st.apply("normpres", r=r, f=1.0, device=DEV)
    emit(f"{host}::normpres", "normpres", a, "projection then Frobenius rescale")
    # (b) rank-k multi-direction
    for k in RANK_KS:
        Rk = rank_k_subspace(D, k)
        a = st.apply("rank_k", Rk=Rk, f=1.0, device=DEV)
        emit(f"{host}::rank_k{k}", "rank_k", a, f"top-{k} right singular subspace", k=k)
    # (c) per-head surgery
    if n_heads:
        a = st.apply("per_head", r=r, f=1.0, n_heads=n_heads, head_frac=0.25, device=DEV)
        emit(f"{host}::per_head25", "per_head", a,
             "top-25% attention heads by write energy along r; down_proj untouched",
             n_heads=n_heads)
    # (d) LAYER-FRACTION SWEEP
    for f in LAYER_FRACTIONS:
        a = st.apply("plain", r=r, f=f, device=DEV)
        emit(f"{host}::band_f{f:.2f}", "band", a, f"contiguous mid-stack band, f={f}",
             layer_fraction=f)

    st.revert()
    del st, parent_sd
    rn.close()
    hubio.gc_cuda()
    hubio.release(host, arch.get("revision"))
    return rows


# ===========================================================================
def run_candidates(tier2: bool = True) -> dict:
    """Arm 1A only: Hub search, card verification, and measurement of the real
    checkpoints.  Separated so it can be re-run without repeating Arm 1B."""
    return run(tier2=tier2, candidates_only=True)


def run(tier2: bool = False, limit: int | None = None,
        candidates_only: bool = False) -> dict:
    t0 = time.time()
    jdump({"prediction": PREREGISTERED_PREDICTION,
           "written_before_arm1_was_run": True,
           "layer_fractions": LAYER_FRACTIONS, "rank_ks": RANK_KS},
          RES / "prereg_arm1.json")
    inputs = LD.load_inputs()

    # ---- A. real new-toolchain checkpoints ----
    search = hub_search()
    # Quantised / converted repos carry no readable fp16 safetensors and cannot be
    # measured; they are excluded HERE (and the exclusion is recorded) rather than
    # silently failing later.
    BAD = ("gguf", "awq", "gptq", "-mlx", "exl2", "bnb-", "-4bit", "-8bit", "onnx")
    def usable(r: str) -> bool:
        low = r.lower()
        return (any(t in low for t in ("abliterated", "orthogonal", "orba", "uncensored",
                                       "decensored", "refusal"))
                and not any(b in low for b in BAD))
    pool = {r: search["repos"][r].get("downloads") or 0
            for r in search["repos"] if usable(r)}
    n_excluded_quantised = sum(1 for r in search["repos"]
                               if any(b in r.lower() for b in BAD))
    # ORDER BY DOWNLOADS, descending -- an alphabetical cut would drop exactly the
    # widely-used toolchain outputs the arm is looking for.
    ordered = [r for r, _ in sorted(pool.items(), key=lambda kv: -kv[1])]
    cands = list(dict.fromkeys(P.NEW_TOOLCHAIN_CANDIDATES + ordered))
    search["n_excluded_quantised"] = n_excluded_quantised
    search["n_usable_pool"] = len(pool)
    verified = verify_candidates(cands[:70], search)
    # STRICT qualification (the plan's target): <=4.2B AND a VERIFIED mechanically
    # different recipe.
    qualified = [v for v in verified if v["size_ok"] and v["mechanically_different"]]
    # Separately: checkpoints that are <=4.2B, exist, and come from an uploader
    # NOT already among the archived eight positives.  These are NOT recipe
    # diversity -- their verified recipe is the same global diff-in-means -- but
    # they ARE uploader diversity, which is what leave-one-uploader-out needs.
    known = {"huihui-ai", "Goekdeniz-Guelmez"}
    new_uploader = [v for v in verified
                    if v["size_ok"] and v["card_chars"] > 0
                    and v["uploader"] not in known and v not in qualified]
    jdump({"search": search, "verified": verified, "n_qualified": len(qualified),
           "qualified": qualified, "n_new_uploader_same_recipe": len(new_uploader),
           "new_uploader_same_recipe": new_uploader,
           "note": "'qualified' means <=4.2B AND a verified MECHANICALLY DIFFERENT recipe. "
                   "'new_uploader_same_recipe' are extra real checkpoints whose verified "
                   "recipe is the SAME global single-direction diff-in-means class as the "
                   "archived eight; they are labelled as such and are never counted as "
                   "recipe diversity."}, RES / "arm1_candidates.json")
    logger.info(f"arm1: {len(verified)} candidates verified, {len(qualified)} qualify "
                f"(<=4.2B AND mechanically different), {len(new_uploader)} new-uploader "
                f"same-recipe")

    # ---- B. synthetic recipe variants ----
    hosts = [] if candidates_only else (P.SYNTH_HOSTS if tier2 else P.SYNTH_HOSTS[:1])
    if limit:
        hosts = hosts[:limit]
    rows: list[dict] = []
    for h in hosts:
        try:
            rows.extend(synth_variants(h, inputs))
            jlines(rows, RES / "arm1_synth.jsonl")
        except Exception as exc:  # noqa: BLE001
            logger.error(f"arm1 host {h} failed: {exc}")
            import traceback
            logger.error(traceback.format_exc()[:2000])

    # ---- real qualified checkpoints, measured ----
    real_rows = []
    to_measure = (qualified + new_uploader) if tier2 else []
    for v in to_measure[:8]:
        try:
            from method import _measure_repo
            m = _measure_repo(v["repo"], None, dtypes=(torch.bfloat16,))
            w = m["by_dtype"]["bfloat16"]
            real_rows.append({"variant_id": v["repo"], "host": v["repo"], "recipe": "real",
                              "synthetic": False, "uploader": v["uploader"],
                              "recipe_class": v["recipe_class"],
                              "mechanically_different": v["mechanically_different"],
                              "is_new_uploader": v["uploader"] not in known,
                              "evidence_tier": v["evidence_tier"],
                              "evidence_quote": v["evidence_quote"],
                              "evidence_url": v["evidence_url"], "params": v["params"],
                              "declared_class": "abliterated",
                              "family": None, "lineage_id": v["repo"],
                              "W01": w["W01"], "W02": w["W02"], "W03": w["W03"],
                              "W04": w["W04"], "W05": w["W05"],
                              "revision": m["revision"], "seconds": w["seconds"]})
            jlines(real_rows, RES / "arm1_real.jsonl")
        except Exception as exc:  # noqa: BLE001
            logger.error(f"arm1 real {v['repo']}: {str(exc)[:300]}")

    out = {"prereg": PREREGISTERED_PREDICTION, "hosts": hosts,
           "n_synth_rows": len(rows), "n_real_rows": len(real_rows),
           "n_candidates_verified": len(verified), "n_qualified": len(qualified),
           "n_new_uploader_same_recipe": len(new_uploader),
           "candidates_only": candidates_only,
           "seconds": round(time.time() - t0, 1)}
    jdump(out, RES / ("arm1_candidates_stage.json" if candidates_only else "arm1.json"))
    return out


if __name__ == "__main__":
    run()
