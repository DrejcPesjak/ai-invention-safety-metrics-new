# Is the name-guess baseline really that good?

`demo/` — Self-contained demo (Colab-ready notebook or markdown). Run without setup.  
`src/` — Full source code, data, and outputs from the experiment execution.

**Type:** experiment  
**ID:** `art_BlPNy1aBYVSE`

## Layman Summary

Checks whether a weights-only detector for uncensored AI models actually beats simply reading the model's name, by measuring both on models that were found without searching for those names.

## Full Summary

Three arms over one shared download -> eligibility -> W05 -> delete pipeline, reusing archived iteration-3/4 code byte-identically (sha256 of every vendored file in results/provenance.json). Tier completed = ALL. Gates G1-G4 PASS (G1 archived-W05 reproduction delta 6.6e-08, tolerance 1e-3), determinism byte-identical on 3 checkpoints, verify.py 193/193 checks, judge spend $0.048 of the $1.50 cap.

ARM 1 (the deliverable of record). The plan assumed the Hub-sweep discovery channel was unrecoverable; it is NOT. iter_3/gen_art_dataset_1/results/enumerated.json stores `found_by` per repo plus all 61 per-query hit lists, so the de-biasing is a MEASUREMENT, not a reconstruction. Repo-name-regex sensitivity by discovery channel: name-free (arch/top sweeps) 0.642 [0.507, 0.757] n=53; term-sweep-discovered 0.953 [0.925, 0.970] n=358; uploader-only 0.888 n=80; whole manifest 0.895 (459/513). The archived 0.727 (32/44) lies INSIDE the de-biased interval, so it survives as an estimate -- of a much weaker baseline than the term-swept pool suggests. IMPORTANT CORRECTION for any downstream text: the 11-term REGEX_11 and the dependency's own repo_id_contains_abliteration_string flag are DIFFERENT estimators -- 459/513 vs 259/513; 'heretic' alone contributes 220 hits and is absent from the dependency flag. The '50.5% name baseline' sentence quotes the narrower flag, not the regex scored against W05.

ARM 1 KEY NEGATIVE RESULT. The 2x2 on 84 measured edited checkpoints (44 archived Arm-A rows reused at their archived W05 + 40 newly measured): W05 at TAU_PANEL fires 10/50 on rows the regex already names and 0/34 on rows it does not (Wilson upper bound 0.102); at TAU_REFIT, 16/50 and 1/34 (KnutJaegersberg/Walter-Falcon-1B, W05 -2.470). caught_by_W05_missed_by_name is EMPTY at the calibrated panel threshold. sens(regex | declared) = 1.0 and sens(regex | undeclared) = 0.0 are labelled in-cell as identities, not measurements. Tier-C card mining over all 1,650 name-clean non-declaring pool cards found only 6 hits (0.36%), so the census's 23.4% UNKNOWN does not imply a large hidden name-clean edited population at the top of the scan pool. w05w_status = NOT_AVAILABLE (plan F5).

ARM 2. 14 card-labelled positives over 9 re-derived recipe classes plus 12 resolvable parents (23 models generated), greedy on the frozen 40-item core with each model's own chat template, rubric-B judge (meta-llama/llama-3.3-70b-instruct, T=0) behind a content-addressed cache. Verdicts: 4 VERIFIED_UNCENSORED, 3 NOT_UNCENSORED, 5 AMBIGUOUS, 1 INCOHERENT_NOT_ASSESSABLE, 1 generation failure. Card-label error rate 0.250 [0.089, 0.532] among assessable rows -- a quarter of the positive class does not behave as un-censored, so the 44-row denominator is itself uncertain and sensitivity ships as an interval over denominators. sens_verified is NOT estimable at n=4 (< the pre-set floor of 6). Paired regex - W05 = +0.615 [0.308, 0.846] over 13 rows, excluding zero. NEW METHODOLOGICAL GUARD: rubric B scores a degenerate loop as REFUSAL, so a 30M checkpoint reads 1.00 refusal from incapacity; rows with distinct-3 < 0.25 are reported as unknown rather than counted either way.

ARM 3. 180 repos scanned from the non-declaring chat stratum in ascending scan_rank, 128 eligible under the UNMODIFIED pre-stamped rule (stamp written before any rate file). Denominator 251 (159 chat / 78 base / 14 unlabelled). FPR at TAU_PANEL: 0/251 pooled, 0/159 chat (Wilson hi 0.024), 0/78 base. FPR at TAU_REFIT: 0.080 pooled, 0.044 chat, 0.154 base -- the refit threshold costs real specificity and costs it disproportionately on BASE models. Closest negative W05 = -2.6139, margin 0.128 log10 to TAU_PANEL. Two bookkeeping findings: the archived 0/122 cannot be rebuilt row by row (no per-row list for its 40 new-eligible rows; shipped rows support 138), and theyur/dhamma-parrot-v01 was a card-declaring edit sitting inside the negative denominator and is removed as a contaminant.

OUTPUT. method_out.json carries metadata.verdicts (six plain-English conclusions written from the computed numbers), headline_numbers, gates, eligibility_stamp, provenance, arm1/arm2/arm3 blocks, determinism, spend and 12 direct-claim limitations; datasets holds 84 arm1 positives, 180 arm3 negatives and 14 arm2 behavioural rows, each with predict_baseline_repo_name_regex beside predict_our_method_W05_tau_panel/tau_refit so the baseline and the method are scored on identical rows. Gotchas for reuse: vendored_lib_behave._is_refusal needs lib_data.py alongside it, and two concurrent `--stage arm2` processes will double-append (kill by PID, delete results/generations and arm2_behaviour.jsonl, restart).

## Dependencies

- `art_8OlSrcw-hzgO` — scan pool
- `art_CKWQh2cOQLLQ` — prompts
- `art_BCxIq6GX4WIw` — rules
- `art_gqCRODISeyg2` — recipe spec

## Output Files

- `method.py`
- `full_method_out.json`
- `mini_method_out.json`
- `preview_method_out.json`

## Demo Files

- **method.py** — Research methodology implementation

---
*Generated by AI Inventor Pipeline*
