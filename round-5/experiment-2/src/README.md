# Is the name-guess baseline really that good?

Three arms over one shared **download → eligibility → W05 → delete** pipeline. Every
statistic that this artifact compares against was produced by archived
iteration-3/4 code, vendored here byte-identically and hashed into
`results/provenance.json`.

```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python -r <(python3 -c "import tomllib;print('\n'.join(tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']))")

.venv/bin/python method.py --stage gates       # stage 0: provenance, stamp, G1-G4
.venv/bin/python method.py --stage arm1        # de-biased regex baseline
.venv/bin/python method.py --stage arm3        # chat-stratum specificity
.venv/bin/python method.py --stage arm2        # behavioural verification (paid)
.venv/bin/python method.py --stage determinism
.venv/bin/python method.py --stage assemble    # writes method_out.json
.venv/bin/python verify.py                     # re-derives every headline number
```

`--stage all` runs the whole thing in the plan's order. Every stage appends to its
own `results/*.jsonl` after each checkpoint, so a kill at any moment leaves a valid
partial table and a rerun resumes.

## What each arm measures

**ARM 1 — the de-biased regex baseline.** The archived 0.727 regex sensitivity was
measured on a pool discovered by 61 Hub sweeps, 20 of whose search terms *are*
abliteration vocabulary. The plan assumed the per-repo discovery channel was
unrecoverable and specified a reconstruction. It is recoverable:
`iter_3/gen_art_dataset_1/results/enumerated.json` stores `found_by` per repo and
the full per-query hit lists. So the de-biasing here is a **measurement** on the
name-free discovery channel (`arch:*` architecture sweeps and `top:all`), not a
reconstruction. The arm then newly scores W05 on the undeclared stratum and reports
the `{W05, regex} × {declared-by-name, undeclared}` 2×2 with Wilson intervals.

**ARM 2 — behavioural verification of the positive class.** 14 card-labelled
positives spanning 9 re-derived recipe classes, plus their declared parents where
resolvable; greedy generation on the frozen 40-item harmful core with each model's
own chat template; rubric-B judge (`meta-llama/llama-3.3-70b-instruct`,
temperature 0) behind a content-addressed cache. Sensitivity is then reported three
ways — on all 44 archived positives, on verified-un-censored rows only, and as an
interval over the positive-class denominator itself.

**ARM 3 — specificity where it matters.** 60 repos from `hub_scan_pool`'s 1,105-row
non-declaring **chat** stratum, in ascending `scan_rank`, under the *unmodified*
pre-stamped eligibility rule (`vendored_eligibility.py`, sha256 stamped into
`results/eligibility_stamp.json` before any rate existed). False-positive rates are
reported at **both** taus and split chat-vs-base.

## Design notes worth knowing before reading the numbers

- **The two "name regex" estimators are not the same thing.** The 11-term
  `REGEX_11` copied verbatim from the archive fires on **459/513** self-declared
  edited manifest rows, while the dependency's own
  `repo_id_contains_abliteration_string` flag fires on **259/513**. The planned
  smoke assertion (259) therefore fails, and not because the term list was
  mistyped — `heretic` alone contributes 220 hits and is absent from the
  dependency's flag. Both are reported.
- **Identities are labelled as identities.** `sens(regex | declared-by-name) = 1.0`
  and `sens(regex | undeclared) = 0.0` are consequences of how the two strata are
  defined, not measurements, and the output says so in the cell.
- **A coherence guard on Arm 2.** Rubric B scores a degenerate loop as REFUSAL,
  because it redirects rather than complying. On a 30M checkpoint that turns
  incapacity into apparent safety. Rows whose distinct-3 falls below 0.25 are
  reported as `INCOHERENT_NOT_ASSESSABLE` rather than counted either way.
- **The Arditi substring screen is a labelled cross-check only.** It reads 0.000 on
  every stage here where the judge reads 0.9-1.0.
- **W05w (windowed) is not computed here** — it belongs to a separate artifact, and
  a rushed re-implementation would ship a number that disagrees with the one that
  artifact owns (plan fallback F5).
- **The archived 0/122 cannot be rebuilt row by row.** The archive reports it as
  82 archived-eligible + 40 new-eligible-completed but ships no per-row list for
  the 40. `results/arm3_rates.json` carries the reconciliation and uses every
  shipped hub-scan row that has a W05 and is eligible under the unmodified rule.

## Files

| path | what |
|---|---|
| `method.py` | all three arms + assembly |
| `common.py` | frozen constants, dependency loading, selection predicates |
| `scoring.py` | download → eligibility → W05 → purge, one repo at a time |
| `verify.py` | standalone re-derivation of every headline number |
| `vendored_*.py`, `lib_data.py` | archived iteration-3/4 code, byte-identical |
| `results/gates.json` | G1-G4 + the regex and eligibility unit tests |
| `results/arm1_rows.jsonl` | per-checkpoint W05 for the name-free strata |
| `results/arm2_behaviour.jsonl`, `results/generations/` | refusal rates and raw completions |
| `results/arm3_rows.jsonl` | per-repo eligibility, chat label, W05 |
| `results/verify.json` | the check ledger |
| `method_out.json` | the shipped artifact |

`hf_cache/` is transient (every snapshot is deleted immediately after scoring) and
is excluded from the published repo, as are `logs/` and `.venv/`.
