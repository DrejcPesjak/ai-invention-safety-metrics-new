#!/usr/bin/env python3
"""Diagnostic: is the sub-1.0 cache-hit rate caused by batch composition or by GPU?

The archived run ran on an RTX 2000 Ada; this box is an RTX 4090.  Greedy decoding is
deterministic GIVEN a kernel schedule, but bf16 matmul kernel selection is
device-dependent, so a near-tie at any of 64 argmax steps can flip.  This probe varies
the ONLY knob under our control -- batch size, which changes padding and reduction
order -- and reports the cache-hit rate for each, so the residual can be attributed.
"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "vendor"))
import torch
from loguru import logger
import lib_behave as B, lib_edit as E
from lib_model import Runner
from lib_prompts import Prompts
from regen import load_archive_cache, cache_key, ARCH3

P = Prompts()
cache = load_archive_cache()
rn = Runner("Qwen/Qwen3-1.7B", None)
recipe = json.loads((ARCH3 / "archive" / "root_recipe.json").read_text())
parent_sd = E.snapshot_sd(rn)
keys = [k["key"] for k in E.write_matrix_keys(rn)]
r = torch.tensor(recipe["r"], dtype=torch.float32); r = r / r.norm()
root_sd = E.ablate_sd(parent_sd, keys, r, emb_key=None)
out = []
for tag, sd in (("A_parent", parent_sd), ("A_root", root_sd)):
    E.load_sd(rn, sd)
    for bs in (8, 16, 32, 40):
        txt, _n, _f, _c = rn.generate(P.harmful40, max_new_tokens=64, batch=bs)
        hit = sum(1 for p, t in zip(P.harmful40, txt) if cache.get(cache_key(p, t)) in B.VALID_LABELS)
        out.append({"stage": tag, "batch": bs, "n": len(txt), "hit": hit,
                    "hit_rate": hit / len(txt)})
        logger.info(f"{tag} batch={bs}: hit_rate={hit/len(txt):.3f}")
Path("results/probe_batch.json").write_text(json.dumps(out, indent=2))
