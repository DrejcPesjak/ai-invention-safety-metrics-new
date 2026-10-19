#!/usr/bin/env bash
# Reproduce this evaluation end to end.
#
#   ./run_all.sh
#
# Requires OPENROUTER_API_KEY for the reliability arm. With cache/judge_cache.jsonl
# present the run makes ZERO API calls and costs $0; without it, it makes 2,866
# calls to google/gemini-3.1-flash-lite and hard-stops at $0.90.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  uv venv .venv --python=3.12
  # pyproject.toml pins every version the reported numbers were produced with
  uv pip install --python=.venv/bin/python .
fi

.venv/bin/python eval.py
.venv/bin/python verify_reproducible.py
