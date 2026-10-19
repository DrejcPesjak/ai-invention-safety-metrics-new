# Labelled Edit-Recipe Model Manifest + laundering corpora + Hub scan pool

Five delivered datasets in one schema-validated `data_out.json`, in three blocks.

| Block | `metadata_fold` | Rows | What it is | `input` | `output` |
|---|---|---|---|---|---|
| 1 | `edit_manifest` | 672 | recipe-labelled sub-4.2B edited checkpoints **and their declared parents** | `repo_id` | `recipe_class` (`PARENT` for parent rows) |
| 2a | `sft_benign` | 3,370 | benign, non-safety single-turn instruction pairs (oasst1, Apache-2.0) | instruction | response |
| 2b | `fluency_wikitext` | 1,000 | WikiText-2-raw test paragraphs for a perplexity screen | paragraph | `""` |
| 2c | `heldout_benign_prompts` | 200 | short benign prompts, mechanically disjoint from 2a (dolly-15k) | prompt | `""` |
| 3 | `hub_scan_pool` | 2,139 | ranked, byte-costed metadata-only scan pool | `repo_id` | `declared` / `not_declared` |

7,381 examples, 16.8 MB. Block 1 spans **189 uploaders** (iteration 2 had 2) and 6 of the
7 recipe classes, with **388** complete parent↔child pairs and all 8 iteration-2 members
flagged via `is_iter2_class_member`. Block 3's strata are 407 declared / 1,105
non-declaring chat / 627 non-declaring base, costed at 7.3 TB with per-decile cumulative
gigabytes so a partial scan has a stateable coverage.

Everything else per row lives under `metadata_features`. Per-block provenance
(source repos, pinned revision shas, licenses) and the full coverage report live under
`metadata.dataset_meta`.

## Scope guard

**Data only.** No model weights were downloaded, no forward pass was run, nothing was
fine-tuned, no W01–W05 statistic was computed and no AUROC is reported. Parameter counts
come from the Hub's safetensors index (`param_count_source`), never from summing on-disk
file bytes — repos shipping both `.safetensors` and `.bin` double-count, which is the
error this field exists to prevent. LLM API spend: **$0.00**.

## Recipe-class vocabulary

`R1_GLOBAL_RANK1_DIM`, `R2_NORM_PRESERVING_PROJECTED`, `R3_MULTIDIRECTION_SVD`,
`R4_PARTIAL_LAYER_OR_PER_HEAD`, `R5_SPECTRAL_CASCADE_DCT`,
`R6_BEHAVIOURAL_SFT_UNCENSORED`, `R7_MERGE_OF_ABLITERATED`, `UNKNOWN`.

`UNKNOWN` is a legitimate, expected and frequently-correct value. A card that only says
"this is an abliterated version" names no mechanism and is labelled `UNKNOWN` with
`label_rule="ambiguous"` and the bare phrase quoted — deliberately **not** folded into
R1, which would inflate R1 until it meant nothing. The `UNKNOWN` count and fraction are
headline outputs: they measure how much recipe provenance the Hub actually carries.

`recipe_evidence` is always a verbatim substring of a card that was actually fetched. If
nothing was fetched, it is `null`.

**`R5_SPECTRAL_CASCADE_DCT` is empty**, and that is a result rather than a gap: the
OBLITERATUS README we fetched contains zero occurrences of "spectral", "frequency",
"Fourier" or "DCT". Any experiment arm needing a frequency-domain recipe is unrunnable at
this scale.

## Three numbers to read first

- `UNKNOWN` = **120 / 513 edited rows (23.4%)** — the ceiling on Hub recipe provenance.
- `repo_id_contains_abliteration_string` = **259 / 513 (50.5%)** — a plain string match on
  the repo id already solves half the detection task, so that is the baseline to beat.
- Hand-check: **27 / 30** rows survived a manual read against their raw cards across three
  seeds (`dataset_meta.coverage.block_1.hand_check`, failures and fixes recorded).

The ceiling is enforced **twice**: once from the Hub safetensors index and once from
on-disk safetensors bytes ÷ the repo's widest declared dtype. The index is not always
right — one repo reports 6.2 M parameters while shipping 159 GB of shards — and the
second check rejected 25 rows that would otherwise have put 32–35B models in a sub-4B pool.

## Pipeline

**Build it:** `uv run data.py` — reads only local files (`temp/datasets/` + `results/`),
makes no network calls, and writes `full_data_out.json`. Verified to reproduce the
network build row-for-row (3,370 / 1,000 / 200 in Block 2, identical Block 1 and 3).

| Script | Does |
|---|---|
| **`data.py`** | **entry point — builds all five datasets from local files** |
| `hub_common.py` | cached, retrying, unauthenticated-safe Hub helpers |
| `harvest_enumerate.py` | 61 `list_models` sweeps (20 search terms, 20 uploaders, 20 architectures, 1 global) |
| `resolve_parents.py` | resolves declared parents the sweeps missed, by name |
| `fetch_repo_details.py` | per-repo file list + `README.md` + `config.json` (kilobytes; never weights) |
| `details_from_cache.py` | rebuilds `results/details.json` from the cache after an interruption |
| `recipes.py` | the controlled vocabulary and the card → class rules |
| `build_corpora.py` | Block 2 (oasst1 / wikitext / dolly), with the safety-topic and disjointness filters |
| `build_dataset.py` | assembles `data_out.json` and computes the coverage report |
| `audit_sample.py` | prints 10 random labelled rows against their raw cards for the hand-check |
| `download_candidates.py` | the evaluated dataset candidates → `temp/datasets/` |

Harvest order (network, run once): `harvest_enumerate` → `resolve_parents` →
`fetch_repo_details` → `download_candidates`. After that, `uv run data.py` rebuilds the
deliverable offline. `build_corpora.py` / `build_dataset.py` are the original
network-sourced path; `data.py` imports `build_manifest`/`build_pool` from the latter so
there is one implementation of the labelling and stratification, not two.

## Integrity checks (all pass on the shipped file)

| Check | Result |
|---|---|
| rows with a missing or `main` revision sha | **0** of 2,811 |
| manifest rows missing `param_count_hub` | **0** |
| rows above their block's parameter ceiling | **0** (both blocks) |
| `recipe_evidence` verbatim-in-card | **482 / 482** verified, 0 fabricated |
| evidence rows carrying an `evidence_url` | 482 / 482 |
| parent rows wrongly carrying a `recipe_class` | 0 |
| 2a pairs leaking a safety topic / duplicated / over the 2000-char cap | 0 / 0 / 0 |
| 2b heading lines or paragraphs under 200 chars | 0 / 0 |
| 2c exact overlap with 2a; max 5-gram Jaccard | 0; **0.273** (threshold 0.5) |

See `DATASET_SELECTION.md` for keep/discard decisions and `evidence/` for the six primary
recipe-documentation sources (each recorded with its sha256 in `dataset_meta`).

`cache/` holds raw Hub API responses and is excluded from publication; deleting it only
costs time on a rerun.
