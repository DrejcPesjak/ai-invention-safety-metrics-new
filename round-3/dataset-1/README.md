# Who Edited This Model, and How

`demo/` — Self-contained demo (Colab-ready notebook or markdown). Run without setup.  
`src/` — Full source code, data, and outputs from the experiment execution.

**Type:** dataset  
**ID:** `art_8OlSrcw-hzgO`

## Layman Summary

A pinned, evidence-carrying catalogue of 672 small language models that were modified to remove their safety refusals, plus the benign text corpora and the ranked scan list a follow-up study needs.

## Full Summary

Ships ONE schema-validated full_data_out.json with five datasets (7,381 examples, 16.5 MiB) in three blocks. DATA ONLY: no weights downloaded, no forward passes, no training, no W01-W05, no AUROC, $0.00 OpenRouter spend. Built offline by `uv run data.py` from temp/datasets/ + results/ (48 deps pinned exactly in pyproject.toml).

BLOCK 1 `edit_manifest` (672 rows = 513 edited + 159 parents). Harvested from 61 Hub sweeps (20 search terms, 20 uploaders, 20 architectures, 1 global top-downloads) over 20,313 enumerated repos. Spans **189 distinct uploaders** against the plan's floor of 5 -- iteration 2's 8 positives came from only TWO uploaders, so this directly removes that confound. **6 of 7** recipe classes populated: R1_GLOBAL_RANK1_DIM 78, R2_NORM_PRESERVING_PROJECTED 20, R3_MULTIDIRECTION_SVD 26, R4_PARTIAL_LAYER_OR_PER_HEAD 235, R6_BEHAVIOURAL_SFT_UNCENSORED 19, R7_MERGE_OF_ABLITERATED 15, UNKNOWN 120. **388 complete parent-child pairs** for the H3 head-to-head; all 8 iteration-2 members present and flagged `is_iter2_class_member`; 1,536 over-ceiling near-misses recorded separately; every row `status=ok`.

THREE NUMBERS THAT SHOULD DRIVE THE PAPER. (i) **UNKNOWN = 23.4%** of edited rows: nearly a quarter of self-declared edited checkpoints name no mechanism, which is the ceiling on Hub recipe provenance. (ii) **repo_id_contains_abliteration_string = 50.5%** (259/513): a plain regex on the repo id alone already solves HALF the detection task, so that -- not chance -- is the baseline any detector must beat. This is the reviewer's previously unmeasured point, now quantified. (iii) **R5_SPECTRAL_CASCADE_DCT is EMPTY**, and that is a finding, not a gap: the OBLITERATUS README we fetched contains ZERO occurrences of 'spectral', 'frequency', 'Fourier' or 'DCT' (its profiles are basic/advanced/aggressive/surgical/optimized/inverted over diff-in-means, SVD, whitened SVD). Any H1 arm needing a frequency-domain recipe is UNRUNNABLE at this scale.

BLOCK 2, three laundering corpora. 2a `sft_benign` 3,370 English single-turn pairs from OpenAssistant/oasst1 (Apache-2.0, sha fdf72ae0), 627 safety-topic pairs and 6,695 duplicate instructions dropped. 2b `fluency_wikitext` 1,000 paragraphs from Salesforce/wikitext wikitext-2-raw-v1 test (sha b08601e0), median 148 GPT-2 tokens, 163,496 total; the @-@ artifact is documented, not silently carried. 2c `heldout_benign_prompts` 200 prompts from databricks-dolly-15k (sha bdd27f4d) -- a DIFFERENT repo from 2a, then exact dedupe (1 dropped) and 5-gram Jaccard >= 0.5 (0 dropped); measured max Jaccard vs any 2a instruction is **0.273**. NC sources excluded throughout (alpaca, no_robots rejected).

BLOCK 3 `hub_scan_pool` 2,139 metadata-only rows, all strata floors beaten: 407 declared / 1,105 non-declaring chat / 627 non-declaring base. Ranked by `scan_rank` (undeclared chat by descending downloads first) with `cumulative_bytes`, so a scan stopping at rank k has a stateable coverage and a cost in GB; 7.3 TB total with per-decile cumulative gigabytes.

INTEGRITY, ALL VERIFIED ON THE SHIPPED FILE: 0 rows with a missing or 'main' sha; 0 rows missing a param count; 0 rows above either ceiling; **482/482 recipe_evidence spans verified as verbatim substrings of the cards they cite (0 fabricated)**; 482/482 carry an evidence_url; 0 parent rows wrongly carrying a recipe_class; 2a leaks no safety terms and has no duplicates.

TWO BUG CLASSES FOUND AND FIXED, both consequential downstream. (1) A three-seed 10-row hand-check (27/30 survived, failures and objections recorded in coverage.block_1.hand_check) exposed four labeller defects, including 'trained' matching inside `from_pretrained(...)` in a usage snippet and corpus-sense 'unfiltered' labelling a pedagogy study as an uncensoring fine-tune. (2) **The Hub's safetensors index is not always right**: samuelcardillo/Qwen3-Coder-Next-Opus-4.6-Reasoning-Distilled reports 6,208,256 parameters while shipping 159 GB of shards, and two 35B checkpoints report 664,944. Taking it at face value silently admits 32-35B models into a sub-4B pool. The ceiling is now enforced TWICE -- once from the index, once from on-disk safetensors bytes divided by the repo's widest declared dtype -- which rejected 25 such rows. Any downstream artifact resolving parameter counts from the Hub should apply the same cross-check.

A bare 'this is an abliterated version' is deliberately labelled UNKNOWN/ambiguous rather than folded into R1, which would have inflated R1 until the class meant nothing. Ten HF dataset candidates were downloaded and evaluated; three are shipped and each of the seven other verdicts is recorded in metadata.dataset_selection (GAIR/lima is gated; tulu-3-sft-mixture is partly non-commercial; oasst2/oasst_top1/guanaco are not independent of 2a and guanaco is multilingual).

## Dependencies

- `art_lMTPOpnFwKnw` — guidance

## Output Files

- `data.py`
- `full_data_out.json`
- `preview_data_out.json`
- `mini_data_out.json`

## Demo Files

- **data.py** — Dataset fetching/generation script

---
*Generated by AI Inventor Pipeline*
