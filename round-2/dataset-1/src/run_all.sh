#!/usr/bin/env bash
# Reproduce the whole artifact from scratch.
#
# Stages 0-3 harvest and measure. Stage 4 (the frozen split) is run SEPARATELY and
# AFTER them on purpose: its wall-clock time is recorded in the pre-registration
# statement, so it must not appear to precede the harvest.
#
# Deterministic given the same upstream sources: the split depends only on the
# frozen manifest, Hub-resolved lineage metadata, and the fixed literal SEED.
# Network-dependent stages cache to cache/, so a re-run is offline and byte-stable
# unless the caches are cleared.
set -euo pipefail
cd "$(dirname "$0")"

PY=.venv/bin/python
[ -x "$PY" ] || { uv venv .venv --python=3.12; uv pip install --python=.venv/bin/python \
  datasets huggingface-hub pandas pyarrow requests loguru jsonschema; }

echo "== stage 0: resolve the frozen panel manifest against the HF Hub"
$PY src/s0_panel.py
echo "== stage 1: capability harvest (Open LLM Leaderboard v1 + v2)"
$PY src/s1_capability.py
echo "== stage 2a: fetch and scan every panel model card"
$PY src/s2a_cards.py
echo "== stage 2b: HELM Safety v1.0.0 + AIR-Bench 2024 v1.1.0"
$PY src/s2b_helm.py
echo "== stage 2c: panel-overlap census over 10 published safety benchmarks"
$PY src/s2c_census.py
echo "== stage 2d: curated external_score rows from official model cards"
$PY src/s2d_curated.py
echo "== stage 3: coverage report"
$PY src/s3_coverage.py
echo "== stage 4: FROZEN SPLIT (separate run, timestamped)"
$PY src/s4_split.py
echo "== stage 5: machine-readable rules"
$PY src/s5_rules.py
echo "== assemble full_data_out.json (artifact rows + 10 measurement corpora)"
uv run data.py
echo "== validate"
$PY src/validate_rows.py

SKILL_DIR="/ai-inventor/.claude/skills/aii-json"
"$SKILL_DIR/../.ability_client_venv/bin/python" \
  "$SKILL_DIR/scripts/aii_json_validate_schema.py" \
  --format exp_sel_data_out --file "$PWD/full_data_out.json"
"$SKILL_DIR/../.ability_client_venv/bin/python" \
  "$SKILL_DIR/scripts/aii_json_format_mini_preview.py" --input "$PWD/full_data_out.json"
rm -f full_full_data_out.json
mv -f mini_full_data_out.json mini_data_out.json
mv -f preview_full_data_out.json preview_data_out.json
# The format script truncates the top-level array to 3 blocks, which would hide all
# 10 measurement corpora from the preview. Rebuild it over every block.
$PY src/make_preview.py
ls -lh full_data_out.json mini_data_out.json preview_data_out.json
