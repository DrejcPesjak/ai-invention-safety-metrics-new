#!/usr/bin/env python3
"""Stages control / arm1 / arm2 / arm3 / assemble."""

from __future__ import annotations

import json
import os
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
import wstats  # noqa: E402
from e1 import e1_from_state_dicts, e1_pair  # noqa: E402
from edits import (WriteMatrixStore, measure_edited, rank_k_subspace,  # noqa: E402
                   refusal_direction)
from method import (ARCHIVE_DTYPE, DEV, N_RANDOM, SEED, _measure_repo,  # noqa: E402
                    jdump, jlines, load_model)

import vendored_lib_data as LD  # noqa: E402
import vendored_lib_metrics as LM  # noqa: E402

# vendored_lib_metrics imports `lib_model` by name inside one function; alias it
sys.modules.setdefault("lib_model", __import__("vendored_lib_model"))
import vendored_lib_model as VM  # noqa: E402


# Standard ChatML, byte-identical to what the Qwen parents of the affected
# abliterated repos ship.  Used ONLY as a recorded fallback (see LocalRunner).
CHATML_TEMPLATE = (
    "{% for message in messages %}"
    "{{'<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>' + '\n'}}"
    "{% endfor %}"
    "{% if add_generation_prompt %}{{ '<|im_start|>assistant\n' }}{% endif %}"
)


# ===========================================================================
# A Runner over an ALREADY-DOWNLOADED snapshot (vendored Runner re-downloads)
# ===========================================================================
class LocalRunner(VM.Runner):
    """vendored_lib_model.Runner, but pointed at a local snapshot path and with
    the renderer FORCED explicitly (iteration-4 note: an 'auto' renderer broke a
    base-model cosine to 0.13, so the renderer is never inferred here)."""

    def __init__(self, path: str, repo: str, renderer: str, device: str = DEV):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.repo = repo
        self.device = device
        self.tok = AutoTokenizer.from_pretrained(path, trust_remote_code=False)
        if self.tok.pad_token is None:
            self.tok.pad_token = self.tok.eos_token or self.tok.unk_token
        self.tok.padding_side = "left"
        self.model = AutoModelForCausalLM.from_pretrained(
            path, torch_dtype=VM.DTYPE, attn_implementation="eager",
            trust_remote_code=False).to(device).eval().requires_grad_(False)
        cfg = self.model.config
        self.L = int(cfg.num_hidden_layers)
        self.d = int(cfg.hidden_size)
        self.blocks = VM.find_block_list(self.model)
        assert renderer in ("chatml", "plain"), renderer
        self.renderer = renderer
        self.has_chat = renderer == "chatml"
        # Some abliterated repos ship a tokenizer_config WITHOUT a chat_template
        # even though the archive rendered them as chatml (older transformers
        # supplied a default; 5.x does not).  Dropping them would remove three of
        # the abliterated positives, so we substitute the standard ChatML template
        # -- which is what their Qwen parents use -- and RECORD the substitution.
        self.chat_template_substituted = False
        if self.has_chat and not getattr(self.tok, "chat_template", None):
            self.tok.chat_template = CHATML_TEMPLATE
            self.chat_template_substituted = True
            logger.warning(f"{repo}: no chat_template on the tokenizer; substituted the "
                           f"standard ChatML template (recorded as a deviation)")
        self.final_norm = VM.find_final_norm(self.model, self.d)
        self.state = VM.SteerState()
        self._handle = None
        self._write_cache = {}
        logger.info(f"loaded {repo}: L={self.L} d={self.d} renderer={self.renderer}")


def attach_lexicon(rn, inputs, declared_family: str) -> dict:
    """Re-resolve the refusal/continuation token lexicon against THIS tokenizer."""
    fam = declared_family if declared_family in inputs.lexicon else None
    fallback = fam is None
    if fallback:  # pick the family whose vocab size matches, else the first
        cands = [k for k, v in inputs.lexicon.items() if v["vocab_size"] == len(rn.tok)]
        fam = cands[0] if cands else sorted(inputs.lexicon)[0]
    ent = inputs.lexicon[fam]
    rn.refusal_ids, rmeta = LM.resolve_token_ids(rn.tok, ent["refusal"], len(rn.tok))
    rn.continuation_ids, cmeta = LM.resolve_token_ids(rn.tok, ent["continuation"], len(rn.tok))
    rn.continuation_ids = [i for i in rn.continuation_ids if i not in set(rn.refusal_ids)]
    return {"family_declared": declared_family, "family_used": fam, "fallback": fallback,
            "n_refusal": len(rn.refusal_ids), "n_continuation": len(rn.continuation_ids)}


# ===========================================================================
# STAGE control -- the two archived positive controls, fresh code
# ===========================================================================
def stage_control() -> dict:
    """Injected global rank-one edit and the band-limited middle-third edit on
    Qwen/Qwen3-0.6B (the INSTRUCT member -- its Base sibling is the wrong model,
    W01=0.628 in the archive)."""
    repo = P.CONTROL_MODEL
    arch = P.archive()[repo]
    rec = hubio.ensure(repo, arch["revision"])
    m = load_model(rec["path"])
    st = WriteMatrixStore(m)
    d = st.d
    g = torch.Generator().manual_seed(1234)
    r = torch.randn(d, generator=g)
    r = r / r.norm()

    unedited = measure_edited(st, n_random=N_RANDOM, seed=SEED, device=DEV)
    audit_full = st.apply("plain", r=r, f=1.0)
    full = measure_edited(st, n_random=N_RANDOM, seed=SEED, device=DEV)
    cos_full = abs(float(np.dot(full.v1, r.numpy())))
    # band-limited: the archived control edited the MIDDLE THIRD
    audit_band = st.apply("plain", r=r, f=1 / 3)
    band = measure_edited(st, n_random=N_RANDOM, seed=SEED, device=DEV)
    cos_band = abs(float(np.dot(band.v1, r.numpy())))
    st.revert()
    reverted = measure_edited(st, n_random=N_RANDOM, seed=SEED, device=DEV)

    ref = P.diagnostics()["abliteration_positive_control"]
    def g5(dd):
        return {k: dd[f"{k}_{n}"] for k, n in (
            ("W01", "abl_suppression_depth"), ("W02", "abl_direction_consistency"),
            ("W03", "abl_gap_vs_random"), ("W04", "abl_isolation"),
            ("W05", "abl_min_layer_energy"))}

    out = {
        "model": repo, "revision": rec["revision"], "d": d, "L": st.L,
        "n_write_matrices": len(st.entries),
        "unedited": {k: getattr(unedited, k) for k in P.WKEYS},
        "full_rank_one_edit": {**{k: getattr(full, k) for k in P.WKEYS},
                               "cos_v1_r": cos_full, **audit_full},
        "band_limited_middle_third": {**{k: getattr(band, k) for k in P.WKEYS},
                                      "cos_v1_r": cos_band, **audit_band},
        "reverted": {k: getattr(reverted, k) for k in P.WKEYS},
        "archived_reference": {"unedited": g5(ref["unedited"]),
                               "full_edit": g5(ref["full_edit"]),
                               "band_limited": g5(ref["band_limited_edit"]),
                               "archived_cos_v1_r_full": ref["full_edit"]["cos_v1_r"],
                               "archived_band_layers": ref["band_limited_edit"]["layers_edited"]},
    }
    out["deltas_vs_archive"] = {
        "unedited": {k: out["unedited"][k] - out["archived_reference"]["unedited"][k]
                     for k in P.WKEYS},
        "full_edit_W01": out["full_rank_one_edit"]["W01"] - out["archived_reference"]["full_edit"]["W01"],
        "full_edit_W02": out["full_rank_one_edit"]["W02"] - out["archived_reference"]["full_edit"]["W02"],
    }
    checks = {
        "cos_v1_r_is_one": cos_full > 0.999,
        "full_W02_is_one": full.W02 == 1.0,
        "full_W01_above_4": full.W01 > 4.0,
        "unedited_W01_near_archive": abs(out["deltas_vs_archive"]["unedited"]["W01"]) < 0.05,
        "band_limited_W02_is_zero": band.W02 == 0.0,
        "revert_exact": abs(reverted.W05 - unedited.W05) < 1e-9,
    }
    out["checks"] = checks
    out["pass"] = all(checks.values())
    del st, m
    hubio.gc_cuda()
    hubio.release(repo, arch["revision"])
    jdump(out, RES / "controls.json")
    logger.info(f"CONTROL pass={out['pass']} cos={cos_full:.6f} "
                f"W01 {unedited.W01:.3f}->{full.W01:.3f} bandW02={band.W02}")
    return out


def dispatch(args) -> None:
    if args.stage == "control":
        stage_control()
    elif args.stage == "arm1":
        import arm1
        arm1.run(tier2=args.tier2, limit=args.limit)
    elif args.stage == "arm1c":
        import arm1
        arm1.run_candidates(tier2=True)
    elif args.stage == "arm2":
        import arm2
        arm2.run(limit=args.limit)
    elif args.stage == "arm3":
        import arm3
        arm3.run(limit=args.limit, members=(args.members.split(",") if args.members else None))
    elif args.stage == "assemble":
        import assemble
        assemble.run()
