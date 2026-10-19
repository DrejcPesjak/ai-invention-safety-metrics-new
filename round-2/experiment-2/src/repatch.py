#!/usr/bin/env python3
"""Recompute two per-member diagnostics offline (tokenizer + recorded rates only), so
every member carries the same, corrected definition regardless of which code version ran
its GPU pass.

1. sign_flip_flag. The original check compared the refusal rate at alpha=4 against
   alpha=0. Because the dose-response is non-monotone - it peaks in alpha ~[0.3, 1] and
   then collapses as the model degenerates - every member trivially failed that check.
   The corrected check compares the PEAK over alpha in (0, 2] against alpha=0.

2. AXIS-B disjointness. The strict criterion (no token shared with ANY word of the 12
   Arditi refusal substrings) is unsatisfiable: those phrases contain "I", "am", "not",
   "to", "a", "as", "but" - function words no English sentence can avoid. Both criteria
   are now recorded:
     strict  - disjoint from every token of every word of every refusal substring;
     relaxed - disjoint from the empirical refusal_onset id set AND from the FIRST token
               of every refusal substring (the fallback criterion), with the exact
               residual overlapping ids reported either way.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from loguru import logger
from transformers import AutoTokenizer

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib_common as C


def disjointness(tok, onset_ids: set[int]) -> dict:
    strict, first_tok = set(onset_ids), set(onset_ids)
    for phrase in C.ARDITI_REFUSAL_SUBSTRINGS:
        for variant in (phrase, " " + phrase):
            ids = tok(variant, add_special_tokens=False)["input_ids"]
            if ids:
                first_tok.add(ids[0])
        for w in phrase.split():
            for variant in (w, " " + w, w.lower(), " " + w.lower()):
                strict.update(tok(variant, add_special_tokens=False)["input_ids"])

    def check(score_ids: set[int]) -> dict:
        ov = {}
        for r in C.AXIS_B_REFUSALS:
            ids = set(tok(" " + r, add_special_tokens=False)["input_ids"])
            hit = ids & score_ids
            if hit:
                ov[r] = [[i, tok.decode([i])] for i in sorted(hit)]
        return dict(verified=len(ov) == 0, n_overlapping_responses=len(ov),
                    n_scoring_ids=len(score_ids), overlaps=ov)

    # The criterion that actually carries the circularity argument: no AXIS-B response is
    # scored as a refusal by the regex screen, so an AXIS-B refusal is INVISIBLE to the
    # lexical scorer by construction.
    scorer_blind = dict(
        verified=not any(C.regex_refusal(r) or C.regex_refusal(r, C.REGEX_WINDOW_AMS)
                         for r in C.AXIS_B_REFUSALS),
        n_matching_scoring_regex=sum(1 for r in C.AXIS_B_REFUSALS if C.regex_refusal(
            r, C.REGEX_WINDOW_AMS)),
        n_responses=len(C.AXIS_B_REFUSALS))
    return dict(strict=check(strict), relaxed=check(first_tok),
                disjoint_from_scoring_regex=scorer_blind,
                criterion_strict="disjoint from refusal_onset ids AND from every token of "
                                 "every WORD of the 12 Arditi refusal substrings",
                criterion_relaxed="disjoint from refusal_onset ids AND from the FIRST "
                                  "token of each of the 12 Arditi refusal substrings",
                criterion_scorer_blind="no AXIS-B response matches the Arditi scoring "
                                       "regex anywhere in its first 250 characters")


def main():
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    folds = C.load_folds()
    lex = C.lexicons(folds)
    cache: dict[str, dict] = {}

    for p in sorted(C.RESULTS.glob("member_*.json")):
        rec = json.loads(p.read_text())
        # 1. sign convention
        rA = {x["alpha"]: x["rate"] for x in rec["dose_response"] if x["axis"] == "A"}
        low = [r for a, r in rA.items() if 0.0 < a <= 2.0]
        rec["sign_flip_flag"] = bool(low and max(low) <= rA.get(0.0, 0.0))
        rec["sign_check"] = dict(rate_at_0=rA.get(0.0),
                                 max_rate_alpha_in_0_2=max(low) if low else None)
        # 2. disjointness
        key = rec["repo"]
        if key not in cache:
            tok = AutoTokenizer.from_pretrained(rec["repo"], revision=rec["revision"])
            onset = {t["token_id"] for t in lex[rec["tokenizer_family"]]["refusal_onset"]}
            cache[key] = disjointness(tok, onset)
        rec["axes"]["axis_B_disjointness"] = cache[key]
        rec["diagnostics_recomputed"] = True
        p.write_text(json.dumps(rec, indent=1))
        d = cache[key]
        logger.info(f"{rec['slug']:26s} sign_flip={rec['sign_flip_flag']} "
                    f"(0:{rA.get(0.0)} peak:{max(low) if low else None}) | "
                    f"disjoint strict={d['strict']['verified']} "
                    f"({d['strict']['n_overlapping_responses']} overlap) "
                    f"relaxed={d['relaxed']['verified']} "
                    f"({d['relaxed']['n_overlapping_responses']} overlap)")


if __name__ == "__main__":
    main()
