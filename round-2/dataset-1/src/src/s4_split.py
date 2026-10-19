#!/usr/bin/env python3
"""Stage 4: the frozen dev / held-out split over weight lineages.

Run SEPARATELY and AFTER stages 1-3; the wall-clock time of this run is recorded in
the pre-registration statement, together with the sha256 of the emitted split file
so any later edit is detectable.

The rule is deterministic and is written verbatim into the artifact: re-running this
script reproduces the split exactly, with no dependence on wall-clock time, process
order, or an unseeded RNG. Randomness comes only from sha256(lineage_id + '|' + SEED).
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from loguru import logger

HERE = Path(__file__).resolve().parent.parent
RESULTS, LOGS = HERE / "results", HERE / "logs"
LOGS.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOGS / "s4_split.log"), rotation="30 MB", level="DEBUG")

SEED = "20260813-iter2-split"
HELDOUT_FLOOR = 1 / 3
# The Qwen3-4B lineage is the iteration-1/2 EXPLORATION lineage: metrics in the
# 50-metric battery will be designed while looking at it. Putting it in HELDOUT
# would be self-deception, so it is forced to DEV by name, deliberately and on the
# record, before any hash is computed.
FORCED_DEV_LINEAGES = ["Qwen/Qwen3-4B-Base"]

RULE_TEXT = """\
DETERMINISTIC SPLIT RULE (reproducible from this text alone)
SEED = '20260813-iter2-split' (fixed literal; no clock, no unseeded RNG)
1. Take every weight lineage in the iteration-1 frozen panel manifest -- ALL of
   them, not only the <=4.2B ones -- and sort the lineage ids lexicographically.
2. Force the exploration lineages (FORCED_DEV = ['Qwen/Qwen3-4B-Base']) to DEV and
   remove them from further consideration. Rationale: metric definitions will be
   designed while looking at this lineage, so holding it out would be self-deception.
3. Form strata as the triple (architecture_family, has_hard_case, size_bucket) where
     architecture_family = config model_type, back-filled from a same-lineage sibling
                           when a member repo exposes no config, else 'unknown:<owner>'
     has_hard_case       = any member has member_class in
                           {abliterated, behavioral_uncensored}
     size_bucket         = bucket of the lineage's MAX resolved parameter count,
                           one of '<1B', '1-2B', '2-4.2B', '>4.2B'
4. Within each stratum, order lineages by the hex digest of
   sha256(lineage_id + '|' + SEED), ascending.
5. Concatenate the strata in sorted-key order, each stratum internally in the hash
   order of step 4, and walk the concatenation with a running counter i starting at
   0, assigning HELDOUT when i % 3 == 0 and DEV otherwise (systematic stratified
   sampling at a 1-in-3 rate). A per-stratum 'first ceil(n/3)' rule was tried first
   and REJECTED: with 105 lineages over 24 families x 2 hard-case flags x 4 size
   buckets most strata are singletons, and ceil(1/3) of 1 is 1, which sent 54/105
   lineages to HELDOUT and left DEV with only 12 of the 34 <=4.2B lineages. The
   running counter keeps the global rate at ~1/3 while preserving the stratification.
6. FAMILY CONSTRAINT: order architecture families by (member lineage count ascending,
   family name ascending) and force ALL lineages of the first two families that are
   not already fully assigned and whose removal leaves DEV non-empty, to HELDOUT, so
   at least two families are absent from DEV entirely and leave-one-family-out is
   possible.
7. FLOOR CHECK: if fewer than ceil(1/3) of all lineages are in HELDOUT, promote
   further DEV lineages to HELDOUT in global sha256(lineage_id + '|' + SEED) order,
   skipping FORCED_DEV, until the floor holds.
8. LEAK CHECK: assert no lineage has members on both sides. The split is over
   LINEAGES precisely so an abliterated member can never land opposite its parent.
"""


def h(lineage_id: str) -> str:
    return hashlib.sha256(f"{lineage_id}|{SEED}".encode()).hexdigest()


def size_bucket(params: int | None) -> str:
    if not params:
        return "unknown"
    if params < 1_000_000_000:
        return "<1B"
    if params < 2_000_000_000:
        return "1-2B"
    if params <= 4_200_000_000:
        return "2-4.2B"
    return ">4.2B"


def main() -> None:
    frozen_utc = datetime.now(timezone.utc).isoformat()
    panel = json.loads((RESULTS / "panel_resolved.json").read_text())

    lin: dict[str, dict] = defaultdict(lambda: {
        "members": [], "max_params": 0, "model_types": set(), "classes": set(),
        "n_in_panel": 0,
    })
    for x in panel:
        L = lin[x["lineage_id"]]
        L["members"].append({
            "checkpoint_id": x["hf_repo_id"],
            "member_class": x["member_class"],
            "param_count": x["param_count_resolved"],
            "in_panel_le_4p2b": x["in_panel_le_4p2b"],
            "revision": x.get("revision", ""),
        })
        L["max_params"] = max(L["max_params"] or 0, x["param_count_resolved"] or 0)
        if x.get("model_type"):
            L["model_types"].add(x["model_type"])
        L["classes"].add(x["member_class"])
        L["n_in_panel"] += int(x["in_panel_le_4p2b"])

    lineages = []
    for lid in sorted(lin):
        L = lin[lid]
        fam = sorted(L["model_types"])[0] if L["model_types"] else "unknown:" + lid.split("/")[0].lower()
        lineages.append({
            "lineage_id": lid,
            "architecture_family": fam,
            "has_hard_case": bool(L["classes"] & {"abliterated", "behavioral_uncensored"}),
            "size_bucket": size_bucket(L["max_params"]),
            "max_param_count": L["max_params"],
            "n_members": len(L["members"]),
            "n_members_in_panel_le_4p2b": L["n_in_panel"],
            "member_classes": sorted(L["classes"]),
            "members": sorted(L["members"], key=lambda m: m["checkpoint_id"]),
            "hash": h(lid),
        })
    logger.info(f"{len(lineages)} lineages over "
                f"{len({l['architecture_family'] for l in lineages})} architecture families")

    assign: dict[str, str] = {}
    reason: dict[str, str] = {}
    for lid in FORCED_DEV_LINEAGES:
        if lid in lin:
            assign[lid] = "dev"
            reason[lid] = "FORCED_DEV_EXPLORATION_LINEAGE"
        else:
            logger.warning(f"FORCED_DEV lineage {lid} is not in the manifest")

    strata: dict[tuple, list] = defaultdict(list)
    for l in lineages:
        if l["lineage_id"] in assign:
            continue
        strata[(l["architecture_family"], l["has_hard_case"], l["size_bucket"])].append(l)
    i = 0
    for key in sorted(strata):
        members = sorted(strata[key], key=lambda z: z["hash"])
        for rank, m in enumerate(members):
            assign[m["lineage_id"]] = "heldout" if i % 3 == 0 else "dev"
            reason[m["lineage_id"]] = (
                f"STRATUM{key}_RANK{rank}_OF_{len(members)}_GLOBALIDX{i}_MOD3"
            )
            i += 1

    fam_counts = defaultdict(int)
    for l in lineages:
        fam_counts[l["architecture_family"]] += 1
    forced_families: list[str] = []
    for fam in sorted(fam_counts, key=lambda f: (fam_counts[f], f)):
        if len(forced_families) >= 2:
            break
        fam_lids = [l["lineage_id"] for l in lineages if l["architecture_family"] == fam]
        if any(lid in FORCED_DEV_LINEAGES for lid in fam_lids):
            continue
        remaining_dev = [
            l for l in lineages
            if assign[l["lineage_id"]] == "dev" and l["architecture_family"] != fam
            and l["architecture_family"] not in forced_families
        ]
        if not remaining_dev:
            continue
        for lid in fam_lids:
            assign[lid] = "heldout"
            reason[lid] = f"FORCED_HELDOUT_FAMILY_{fam}_FOR_LEAVE_ONE_FAMILY_OUT"
        forced_families.append(fam)
    logger.info(f"Families forced entirely into HELDOUT: {forced_families}")

    floor = math.ceil(len(lineages) * HELDOUT_FLOOR)
    promoted: list[str] = []
    if sum(1 for v in assign.values() if v == "heldout") < floor:
        for l in sorted(lineages, key=lambda z: z["hash"]):
            if sum(1 for v in assign.values() if v == "heldout") >= floor:
                break
            lid = l["lineage_id"]
            if assign[lid] == "dev" and lid not in FORCED_DEV_LINEAGES:
                assign[lid] = "heldout"
                reason[lid] = "PROMOTED_TO_MEET_ONE_THIRD_HELDOUT_FLOOR"
                promoted.append(lid)
    logger.info(f"Promoted to meet the >=1/3 floor: {len(promoted)} -> {promoted}")

    dev_fams = {l["architecture_family"] for l in lineages if assign[l["lineage_id"]] == "dev"}
    all_fams = set(fam_counts)
    absent = sorted(all_fams - dev_fams)
    n_held = sum(1 for v in assign.values() if v == "heldout")
    assert n_held >= floor, f"held-out floor violated: {n_held} < {floor}"
    assert len(absent) >= 2, f"only {len(absent)} families absent from DEV"
    for l in lineages:
        sides = {assign[l["lineage_id"]]}
        assert len(sides) == 1, "a lineage cannot straddle the split"

    for l in lineages:
        l["split"] = assign[l["lineage_id"]]
        l["split_reason"] = reason[l["lineage_id"]]

    n_panel_held = sum(1 for l in lineages
                       if l["split"] == "heldout" and l["n_members_in_panel_le_4p2b"])
    n_panel_dev = sum(1 for l in lineages
                      if l["split"] == "dev" and l["n_members_in_panel_le_4p2b"])
    logger.info(f"SPLIT: {n_held} heldout / {len(lineages) - n_held} dev "
                f"(floor was {floor}); families absent from DEV: {absent}")
    logger.info(f"Among <=4.2B lineages only: {n_panel_held} heldout / {n_panel_dev} dev")

    split_payload = {
        "seed": SEED,
        "rule_text": RULE_TEXT,
        "forced_dev_lineages": FORCED_DEV_LINEAGES,
        "forced_heldout_families": forced_families,
        "promoted_for_floor": promoted,
        "families_absent_from_dev": absent,
        "n_lineages_total": len(lineages),
        "n_heldout": n_held,
        "n_dev": len(lineages) - n_held,
        "heldout_floor_required": floor,
        "lineages": lineages,
    }
    blob = json.dumps(split_payload, indent=1, sort_keys=True)
    (RESULTS / "split_assignments.json").write_text(blob)
    digest = hashlib.sha256(blob.encode()).hexdigest()

    prereg = {
        "statement_type": "PRE_REGISTRATION_OF_FROZEN_SPLIT",
        "frozen_at_utc": frozen_utc,
        "seed": SEED,
        "rule_text": RULE_TEXT,
        "n_lineages_total": len(lineages),
        "n_dev": len(lineages) - n_held,
        "n_heldout": n_held,
        "heldout_fraction": round(n_held / len(lineages), 4),
        "families_absent_from_dev": absent,
        "forced_heldout_families": forced_families,
        "forced_dev_lineages_and_why": {
            lid: "iteration-1/2 exploration lineage: metrics WILL be designed while "
                 "looking at it, so holding it out would be self-deception. Declared "
                 "deliberately, before any metric definition exists."
            for lid in FORCED_DEV_LINEAGES
        },
        "assertion": (
            "No metric definition from the 50-metric battery had been chosen when this "
            "split was written. The split depends only on the frozen iteration-1 panel "
            "manifest, the lineage metadata resolved from the HF Hub, and the fixed "
            "literal SEED above -- it cannot depend on any metric's value because no "
            "metric value is an input to the rule."
        ),
        "split_file_sha256": digest,
        "split_file": "results/split_assignments.json",
        "reproduce_with": "python src/s4_split.py (deterministic; overwrites the same file)",
    }
    (RESULTS / "split_prereg.json").write_text(json.dumps(prereg, indent=1))
    logger.info(f"Pre-registration frozen at {frozen_utc}; split sha256={digest}")


if __name__ == "__main__":
    main()
