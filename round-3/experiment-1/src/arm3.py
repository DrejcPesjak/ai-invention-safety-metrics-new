#!/usr/bin/env python3
"""ARM 3 -- depth invariance of the activation (negative) arm.

Iteration 2 pre-declared ONE relative depth, rho* = 0.679, chosen as the argmax
of a saturated held-out AUROC profile.  A plateau that saturated at 1.000 cannot
distinguish depths, so the falsifier verdict ('the black-box baseline beats every
activation metric') might be an artefact of that one choice.  This arm recomputes
the depth-sensitive metrics at THREE relative depths spanning the plateau and
emits a tidy long table so the falsifier can be re-tested at each depth.

Depths: the BARE AUROC argmax (read from CALIB, not hard-coded), 0.50, and the
pre-declared rho*.

Cost control: one forward pass per member captures ALL layers, so every
state-based metric at every depth is free.  Only the two GENERATION-based
readouts (generated-step logit lens, alpha_50 steering sweep) cost per depth.
"""

from __future__ import annotations

import json
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
from method import DEV, jdump, jlines  # noqa: E402

EPS = LM.EPS


def depths() -> list[dict]:
    c = P.calibration()
    bare = P.bare_argmax_depth()
    return [{"name": "bare_argmax", "rel_depth": bare,
             "source": f"CALIB bare_auroc_argmax_index={c['bare_auroc_argmax_index']}/L={c['L']}"},
            {"name": "mid", "rel_depth": 0.50, "source": "fixed mid-stack"},
            {"name": "rho_star", "rel_depth": P.rho_star(),
             "source": "iteration-2 pre-declared primary"}]


def _rows_for_depth(rn, inputs, hs, dinfo, E, gen_core, want_alpha50: bool) -> list[dict]:
    """Every depth-sensitive metric at ONE relative depth."""
    out = []
    L, d = rn.L, rn.d
    rel = dinfo["rel_depth"]
    L_sel = max(0, min(L - 1, int(round(rel * L))))
    li = L_sel + 1                       # hidden_states index for block L_sel output
    t0 = time.time()

    fit_h, fit_b = hs["fit_h"], hs["fit_b"]
    hold_h, hold_b = hs["hold_h"], hs["hold_b"]
    core, benign = hs["core"], hs["benign"]

    mu = fit_h[:, li].mean(0) - fit_b[:, li].mean(0)
    u = mu / (mu.norm() + EPS)
    ph = (hold_h[:, li] @ u).numpy()
    pb = (hold_b[:, li] @ u).numpy()
    med_norm = float(torch.cat([fit_h[:, li], fit_b[:, li]]).norm(dim=1).median())

    def add(mid, val, **kw):
        out.append({"metric_id": mid, "value": (float(val) if val is not None
                                                and np.isfinite(val) else None),
                    "rel_depth": rel, "depth_name": dinfo["name"], "layer_index": L_sel,
                    "n_layers": L, **kw})

    add("A05_auroc_at_selected_depth", LM.auroc(ph, pb), n_items=len(ph) + len(pb))
    add("A06_dprime_at_selected_depth", LM.dprime(ph, pb), n_items=len(ph) + len(pb))
    add("A07_diffmeans_norm_ratio", float(mu.norm() / (med_norm + EPS)),
        n_items=fit_h.shape[0] + fit_b.shape[0])
    add("DEPTH_diffmeans_separation", float((ph.mean() - pb.mean()) / (med_norm + EPS)),
        n_items=len(ph) + len(pb))

    # refusal-axis-to-unembedding cosine (a DECLARED-EXPECTED-TO-FAIL control:
    # the published Sec.8 negative says this sits at chance)
    Rt, Ct = torch.tensor(rn.refusal_ids), torch.tensor(rn.continuation_ids)
    ref_dir = E[Rt].mean(0) - E[Ct].mean(0)
    add("A19_refusal_axis_unembed_cosine",
        float(torch.nn.functional.cosine_similarity(u, ref_dir, dim=0)), n_items=1)

    # prompt-position logit-lens refusal log-odds AT THIS DEPTH
    r_core = LM._r_from_states(rn, core[:, li], E)
    r_ben = LM._r_from_states(rn, benign[:, li], E)
    add("A11_r_prompt_harmful", r_core.mean(), n_items=len(r_core))
    add("A12_r_prompt_benign", r_ben.mean(), n_items=len(r_ben))
    add("A13_r_prompt_asymmetry", r_core.mean() - r_ben.mean(),
        n_items=len(r_core) + len(r_ben))

    # AMS sigma PINNED to this depth (the published AMS takes a band max; pinning
    # it is what makes it comparable across depths)
    sig = []
    for _c, pairs in hs["ams"].items():
        hp, hm = pairs
        mu2 = hp[:, li].mean(0) - hm[:, li].mean(0)
        u2 = mu2 / (mu2.norm() + EPS)
        a, b = (hp[:, li] @ u2).numpy(), (hm[:, li] @ u2).numpy()
        sp = float(np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2.0))
        sig.append(float((a.mean() - b.mean()) / (sp + EPS)))
    add("A01_ams_sigma_at_depth", min(sig) if sig else None, n_items=len(sig))

    # generated-step logit lens AT THIS DEPTH
    caps = gen_core.get(dinfo["name"], {}).get("caps")
    if caps:
        seqs = [LM._r_from_states(rn, c[:min(8, c.shape[0])], E)
                for c in caps if c.shape[0] > 0]
        if seqs:
            m = min(len(s) for s in seqs)
            M = np.stack([s[:m] for s in seqs])
            add("A14_r_gen_mean_first8", M.mean(), n_items=len(seqs))
            add("A15_r_gen_slope_first8", np.mean([LM.ols_slope(s) for s in M]),
                n_items=len(seqs))
            add("A16_r_gen_max_first8", M.max(axis=1).mean(), n_items=len(seqs))

    # alpha_50 -- the CEILING-CENSORED steering metric
    if want_alpha50:
        try:
            a50, meta = LM.compute_alpha50(rn, [r["input"] for r in inputs.benign40],
                                           u, med_norm, L_sel, n_prompts=16, max_new=24)
            out.append({"metric_id": "A22_alpha_50", "value": (a50 if np.isfinite(a50) else None),
                        "rel_depth": rel, "depth_name": dinfo["name"], "layer_index": L_sel,
                        "n_layers": L, "is_censored": bool(meta["ceiling_censored"]),
                        "n_items": 16, "grid_max": max(meta["grid"]) if meta["grid"] else None,
                        "max_rate": max(meta["rates"]) if meta["rates"] else None})
        except Exception as exc:  # noqa: BLE001
            logger.error(f"alpha50 at {dinfo['name']}: {str(exc)[:200]}")
            out.append({"metric_id": "A22_alpha_50", "value": None, "rel_depth": rel,
                        "depth_name": dinfo["name"], "layer_index": L_sel, "n_layers": L,
                        "is_censored": True, "error": str(exc)[:200]})

    for r in out:
        r.setdefault("is_censored", False)
        r["seconds"] = round(time.time() - t0, 2)
    return out


def member_rows(repo: str, inputs, *, want_alpha50: bool = True) -> list[dict]:
    from stages import LocalRunner, attach_lexicon
    a = P.archive()[repo]
    rec = hubio.ensure(repo, a["revision"])
    rn = LocalRunner(rec["path"], repo, a["renderer"], device=DEV)
    lex = attach_lexicon(rn, inputs, a["tokenizer_family"])
    E = rn.folded_unembed().cpu()

    fh = [r["input"] for r in inputs.lc_fit["harmful"]]
    fb = [r["input"] for r in inputs.lc_fit["benign"]]
    hh = [r["input"] for r in inputs.lc_hold["harmful"]]
    hb = [r["input"] for r in inputs.lc_hold["benign"]]
    core = [r["input"] for r in inputs.core40]
    ben = [r["input"] for r in inputs.benign40]

    t0 = time.time()
    hs_fit, _ = rn.last_token_states(fh + fb, batch=8)
    hs_hold, _ = rn.last_token_states(hh + hb, batch=8)
    hs_core, _ = rn.last_token_states(core, batch=8)
    hs_ben, _ = rn.last_token_states(ben, batch=8)
    ams = {}
    for cname, pairs in inputs.ams_pairs.items():
        hp, _ = rn.last_token_states([p for p, _ in pairs], batch=4)
        hm, _ = rn.last_token_states([m for _, m in pairs], batch=4)
        ams[cname] = (hp, hm)
    hs = {"fit_h": hs_fit[:len(fh)], "fit_b": hs_fit[len(fh):],
          "hold_h": hs_hold[:len(hh)], "hold_b": hs_hold[len(hh):],
          "core": hs_core, "benign": hs_ben, "ams": ams}
    t_fwd = time.time() - t0

    # one generation per depth (capture layer differs), harmful core prompts
    gen_core = {}
    for dd in depths():
        L_sel = max(0, min(rn.L - 1, int(round(dd["rel_depth"] * rn.L))))
        _g, _n, _f, caps = rn.generate(core, max_new_tokens=16, batch=8, capture_layer=L_sel)
        gen_core[dd["name"]] = {"caps": caps}

    rows: list[dict] = []
    for dd in depths():
        for r in _rows_for_depth(rn, inputs, hs, dd, E, gen_core, want_alpha50):
            rows.append({"member_repo": repo, "revision": rec["revision"],
                         "lineage_id": a["lineage_id"], "family": a["family"],
                         "declared_class": a["member_class"], "renderer": a["renderer"],
                         "params": a["param_count"], "dtype": "bfloat16",
                         "chat_template_substituted": bool(
                             getattr(rn, "chat_template_substituted", False)),
                         "lexicon": lex, "forward_s": round(t_fwd, 1), **r})
    del hs, ams, gen_core, E
    rn.close()
    hubio.gc_cuda()
    hubio.release(repo, a["revision"])
    return rows


def run(limit: int | None = None, members: list[str] | None = None) -> dict:
    t0 = time.time()
    inputs = LD.load_inputs()
    arch = P.archive()
    beh = P.behaviour()
    # CHAT-RENDERED members only; base models use the plain renderer and are
    # excluded from the correlations (the falsifier is about chat behaviour).
    chat = [r for r, a in arch.items() if a["renderer"] == "chatml"]
    # priority: members carrying the falsifier (a behaviour row), abliterated first
    def prio(r):
        a = arch[r]
        return (0 if r in beh else 1,
                0 if a["member_class"] in ("abliterated", "behavioral_uncensored") else 1,
                a["param_count"] or 0)
    order = sorted(chat, key=prio)
    if members:
        order = [m for m in members if m in arch]
    if limit:
        order = order[:limit]

    # Resume: keep rows already computed for members we are not re-running, so a
    # targeted re-run (e.g. recovering the members whose tokenizer needed a chat
    # template) EXTENDS the long table rather than replacing it.
    rows, dropped = [], []
    lt = RES / "long_table_depth.jsonl"
    if lt.exists():
        prev = [json.loads(l) for l in lt.read_text().splitlines() if l.strip()]
        keep = [r for r in prev if r["member_repo"] not in set(order)]
        rows.extend(keep)
        logger.info(f"resuming: kept {len(keep)} rows for "
                    f"{len({r['member_repo'] for r in keep})} members not being re-run")
    for i, repo in enumerate(order):
        try:
            r = member_rows(repo, inputs)
            rows.extend(r)
            jlines(rows, RES / "long_table_depth.jsonl")
            logger.info(f"ARM3 [{i+1}/{len(order)}] {repo}: {len(r)} rows, "
                        f"elapsed {time.time()-t0:.0f}s")
        except Exception as exc:  # noqa: BLE001
            import traceback
            logger.error(f"arm3 {repo}: {str(exc)[:300]}")
            logger.debug(traceback.format_exc()[:3000])
            dropped.append({"repo": repo, "reason": str(exc)[:300]})

    cens = {}
    for d in depths():
        sel = [r for r in rows if r["metric_id"] == "A22_alpha_50"
               and r["depth_name"] == d["name"]]
        cens[d["name"]] = {"rel_depth": d["rel_depth"],
                           "n_censored": sum(1 for r in sel if r.get("is_censored")),
                           "n_total": len(sel)}
    out = {"depths": depths(), "n_members_requested": len(order),
           "n_members_done": len({r["member_repo"] for r in rows}),
           "members_done": sorted({r["member_repo"] for r in rows}),
           "n_rows": len(rows), "dropped": dropped,
           "alpha50_censoring_by_depth": cens,
           "chat_rendered_available": len(chat),
           "seconds": round(time.time() - t0, 1)}
    jdump(out, RES / "arm3.json")
    logger.info(f"ARM3 done: {out['n_members_done']} members, {len(rows)} rows, "
                f"censoring {cens}")
    return out


if __name__ == "__main__":
    run()
