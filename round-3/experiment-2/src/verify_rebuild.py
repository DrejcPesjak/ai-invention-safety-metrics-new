#!/usr/bin/env python3
"""Prove the root rebuilt from results/root_recipe.json is exactly the archived one.

Run while results/root_sd.pt still exists (it is deleted afterwards: 3.8 GB is over
the 100 MB repo limit and the blob is redundant given the recipe).
"""
import json, sys
from pathlib import Path
import torch
sys.argv = ["verify_rebuild"]
import lib_ablate as AB          # noqa: E402
import lib_score as S            # noqa: E402
import method as M               # noqa: E402

HERE = Path(__file__).resolve().parent
M._limits()
recipe = json.loads(M.ROOT_RECIPE.read_text())
rn = M.Runner(recipe["parent_repo"], None)
parent_sd, root_sd = M.rebuild_root(rn, recipe)      # raises if fingerprint differs

ref_path = HERE / "results" / "root_sd.pt"
if ref_path.exists():
    ref = torch.load(ref_path, weights_only=False)["sd"]
    diff = [k for k in ref if k in root_sd and not torch.equal(root_sd[k], ref[k])]
    print(f"full state_dict: {len(ref) - len(diff)}/{len(ref)} tensors bit-identical")
    assert not diff, diff[:5]
else:
    print("archived blob absent (expected after cleanup); fingerprint check stands alone")

AB.load_sd(rn, root_sd)
v = S.abl_weights(rn)
rec = json.loads((HERE / "results" / "root.json").read_text())["root"]
for k in ["W01_abl_suppression_depth", "W02_abl_direction_consistency",
          "W03_abl_gap_vs_random", "W04_abl_isolation",
          "W05_abl_min_layer_energy", "W05q10_abl_p10_layer_energy"]:
    d = abs(v[k] - rec[k])
    print(f"  {k:<32} rebuilt {v[k]:+.9f}  recorded {rec[k]:+.9f}  |d| {d:.2e}")
    assert d < 1e-9, k
print("REBUILD VERIFIED")
