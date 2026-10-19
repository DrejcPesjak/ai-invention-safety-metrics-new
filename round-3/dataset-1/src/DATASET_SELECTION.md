# Dataset selection — keep / discard, with reasons

Scope guard: this artifact ships **data only**. No model weights were downloaded, no
forward pass was run, nothing was fine-tuned, no W01–W05 statistic was computed and no
AUROC is reported. Parameter counts come from the Hub's safetensors index; file sizes
from the Hub file index. Total LLM API spend: **$0.00** (no OpenRouter call was made).

## Search coverage

- **40 HuggingFace *dataset* searches** (three parallel batches) over broad terms:
  instruction following / instruction tuning / open assistant / dolly / wikitext /
  benign instructions / creative writing / tulu / lima / no-robots / guanaco / self-instruct /
  flan / evol-instruct / everyday conversations / brainstorming / summarization instructions /
  alpaca / sft chat data / …
- **61 HuggingFace *model* sweeps** for the manifest and scan pool: 20 search terms
  (abliterated, gabliterated, obliterated, uncensored, decensored, orthogonalized,
  norm-preserved, biprojected, refusal, Josiefied, lorablated, heretic, unaligned,
  refusal-removed, projected abliteration, amoral, toxic-dpo, unfiltered, no-refusal,
  safetensors abliterated), 20 uploaders, 20 per-architecture passes, plus one global
  top-downloads pass. **20,197 distinct repos** enumerated; 6,361 sub-4.2B.

## Block 2 corpora — KEPT

| Dataset | Role | Downloads | Likes | License | Provenance |
|---|---|---|---|---|---|
| `OpenAssistant/oasst1` | 2a benign SFT | 20,967 | 1,559 | Apache-2.0 | NeurIPS 2023 D&B, arXiv:2304.07327; 161,443 messages, 13,500+ volunteers |
| `Salesforce/wikitext` (`wikitext-2-raw-v1`, test) | 2b fluency/perplexity | 1,493,298 | 758 | CC BY-SA 3.0 / GFDL | Merity et al., *Pointer Sentinel Mixture Models*, ICLR 2017 (arXiv:1609.07843); the standard lm-evaluation-harness perplexity corpus |
| `databricks/databricks-dolly-15k` | 2c held-out benign prompts | 42,510 | 1,074 | CC BY-SA 3.0 | 5,000+ Databricks employees, Mar–Apr 2023; InstructGPT behavioural categories |

All three clear the bars: ≫100 downloads, a dataset card, and a citable paper or an
identified corporate author. 2a and 2c come from **different source repos by
construction**, then disjointness is enforced mechanically (exact normalised-text dedupe
plus a 5-gram Jaccard ≥ 0.5 filter).

## Block 2 corpora — DISCARDED, and why

| Dataset | Verdict | Reason |
|---|---|---|
| `tatsu-lab/alpaca`, `yahma/alpaca-cleaned` | discard | OpenAI-output derived, non-commercial terms — the direction explicitly excludes NC sources |
| `HuggingFaceH4/no_robots` | discard | CC-BY-**NC**-4.0; two existing blocks are already NC-limited |
| `GAIR/lima` | discard | **gated** on the Hub (`DatasetNotFoundError: … is a gated dataset`) — unusable without a manual access grant, so not reproducible for a downstream artifact |
| `allenai/tulu-3-sft-mixture` | not primary | ODC-BY overall but its own card says "some portions of the dataset are non-commercial" — mixed provenance defeats the point of a clean permissive laundering set |
| `WizardLM_evol_instruct_*`, `Magicoder-Evol-Instruct` | discard | GPT-output derived and code-heavy; a code-skewed laundering fine-tune is not a neutral benign edit |
| `Trendyol-Cybersecurity-Instruction-Tuning` | discard | security/harm-adjacent content — the whole design requires the laundering data be *unrelated* to safety |
| `shiv96/harmful_benign_instructions` | discard | 70 downloads, no card, no paper — fails the popularity **and** documentation bars |

## Ten candidates in, five datasets out

Ten HuggingFace dataset candidates were downloaded to `temp/datasets/` and inspected.
Three are shipped (Blocks 2a/2b/2c); the other two delivered datasets (`edit_manifest`,
`hub_scan_pool`) come from the **model** Hub metadata harvest, not a dataset repo — which
is why the five shipped datasets are not simply five of the ten. Every verdict, kept and
dropped, is recorded in `metadata.dataset_selection.candidates`:

| Candidate | Verdict |
|---|---|
| `OpenAssistant/oasst1` | **SHIPPED** → `sft_benign` — Apache-2.0, the only permissive human-written option; per-message `rank` picks the best sibling reply with no model in the loop |
| `Salesforce/wikitext` | **SHIPPED** → `fluency_wikitext` — the reference perplexity corpus, so the screen is comparable to published numbers |
| `databricks/databricks-dolly-15k` | **SHIPPED** → `heldout_benign_prompts` — a *different* source repo from 2a, which is what makes the held-out set disjoint by construction |
| `allenai/tulu-3-sft-personas-instruction-following` | dropped — synthetic persona prompts with IFEval-style format constraints; laundering wants ordinary text, not constraint drills |
| `allenai/tulu-3-sft-mixture` | dropped — its own card says some portions are non-commercial |
| `OpenAssistant/oasst2` | dropped — superset of oasst1, same structure; more rows without independence |
| `OpenAssistant/oasst_top1_2023-08-25` | dropped — pre-flattened oasst export; not independent of 2a |
| `timdettmers/openassistant-guanaco` | dropped — oasst subset **and multilingual** (sampled rows are Spanish); 2a is English-only |
| `argilla/databricks-dolly-15k-curated-en` | dropped — curation pass over the same dolly rows; not independent of 2c |
| `HuggingFaceTB/everyday-conversations-llama3.1-2k` | dropped — 2,260 rows, below the ≥3000 floor, and LLM-generated |

## Also downloaded for inspection (`temp/datasets/`)

`allenai/tulu-3-sft-personas-instruction-following` (ODC-BY),
`HuggingFaceTB/everyday-conversations-llama3.1-2k`,
`timdettmers/openassistant-guanaco` (Apache-2.0),
`OpenAssistant/oasst_top1_2023-08-25` (Apache-2.0),
`argilla/databricks-dolly-15k-curated-en`, `OpenAssistant/oasst2` (Apache-2.0),
`allenai/tulu-3-sft-mixture`. These were evaluated as fallbacks for 2a/2c; oasst1 won on
size, license and the availability of per-message quality ranks.

## Blocks 1 and 3 — not "datasets" but Hub metadata

Blocks 1 and 3 are built from the HuggingFace **model** Hub, not the dataset hub, so the
popularity/documentation bars are applied per-repo instead: every manifest row carries its
30-day download count, its likes, its resolved revision sha, and — where a method is
declared — a verbatim quoted span from the card it came from. Rows whose card declares
nothing are labelled `UNKNOWN`; that count is a headline output, not a gap to paper over.

Recipe-class evidence was fetched from six primary documents (saved with sha256 under
`evidence/`): grimjim's *Projected Abliteration* and *Norm-Preserving Biprojected
Abliteration* posts, mlabonne's *Uncensor any LLM with abliteration*, the Heretic README,
the jim-plus `llm-abliteration` README, and the OBLITERATUS README.

## What landed

| Block | Rows | Notes |
|---|---|---|
| 1 `edit_manifest` | **672** (513 edited + 159 parents) | **189 uploaders** (iter-2 had 2), **6 of 7** recipe classes populated, **388** complete parent↔child pairs, all **8** iter-2 members present, every row `status=ok` |
| 2a `sft_benign` | 3,370 | Apache-2.0; 627 safety-topic pairs and 6,695 duplicate instructions dropped |
| 2b `fluency_wikitext` | 1,000 | median 148 GPT-2 tokens, 163,496 total |
| 2c `heldout_benign_prompts` | 200 | 1 dropped by exact match, 0 by 5-gram Jaccard vs 2a |
| 3 `hub_scan_pool` | 2,139 | strata 407 declared / 1,105 non-declaring chat / 627 non-declaring base — all floors met; 7.3 TB costed, per-decile cumulative GB emitted |

Three numbers the downstream experiments should read first:

- **`UNKNOWN` = 120 of 513 edited rows (23.4%).** Nearly a quarter of self-declared edited
  checkpoints name no mechanism at all. That is the ceiling on how much recipe provenance
  the Hub carries.
- **`repo_id_contains_abliteration_string` = 259 of 513 (50.5%).** A plain string match on
  the repo id already solves *half* the detection task for free. Any detector must be
  scored against that baseline, not against chance.
- **`R5_SPECTRAL_CASCADE_DCT` = 0.** The plan expected this class from OBLITERATUS's
  "spectral_cascade" mode, but the README we actually fetched contains **zero** occurrences
  of "spectral", "frequency", "Fourier" or "DCT" — its documented profiles are
  basic/advanced/aggressive/surgical/optimized/inverted over diff-in-means, SVD and
  whitened SVD. No sub-4.2B checkpoint declaring a frequency-domain recipe exists in this
  harvest, so any H1 arm requiring one is unrunnable at this scale.

## Self-audit

Three independent 10-row samples (seeds 20260813 / 7 / 42) were read by hand against the
raw cards: **27 of 30 survived**. All three failures share one shape — an inherited or
implied recipe, or evidence quoted from a config dump / marketing line rather than a method
claim. None was the labeller inventing a mechanism the card does not mention. Auditing
found and fixed four real bugs (recorded in `dataset_meta.coverage.block_1.hand_check`),
including `trained` matching inside `from_pretrained(...)` and corpus-sense "unfiltered".

A fifth bug was found outside the audit and is worth flagging: **the Hub's safetensors
index is not always right.** `samuelcardillo/Qwen3-Coder-Next-Opus-4.6-Reasoning-Distilled`
reports `safetensors.total = 6,208,256` while shipping 159 GB of shards, and two 35B
checkpoints report 664,944. Taking the index at face value silently admitted 32–35B models
into a sub-4B pool. The ceiling is now enforced twice — once from the index and once from
on-disk safetensors bytes divided by the repo's widest declared dtype — which rejected 25
rows (5 manifest, 20 pool).

## Not published

`cache/` (4.3 GB of raw Hub responses), `results/enumerated.json` and
`results/details.json` (regenerable intermediates; `details.json` also holds 2,650 full
model-card texts, and the design is deliberately to ship card *hashes* rather than
redistribute card prose), and the `temp/datasets/full_*.json` dumps (374 MB of copies of
public HF datasets). `results/download_report.json` and the `mini_`/`preview_` dumps stay,
so what was fetched is still auditable.
