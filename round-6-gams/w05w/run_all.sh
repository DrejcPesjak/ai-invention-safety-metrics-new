#!/usr/bin/env bash
# Sequential: baseline grams (shard-by-shard download, delete) -> score -> drop cache; then trial98.
set -uo pipefail
cd "$(dirname "$0")"
PY=.venv/bin/python
run_one () {  # $1 = src (repo id or local dir), $2 = short name
  local src="$1" name="$2"
  echo "=============== $name  ($src)  $(date)"
  $PY w05w_stream.py grams "$src" "cache/$name" || { echo "GRAMS FAILED $name"; return 1; }
  $PY w05w_stream.py score "cache/$name" "results/$name.json" --ks 2,4 || { echo "SCORE FAILED $name"; return 1; }
  rm -rf "cache/$name" "models/${src//\//__}"
  df -h . | tail -1
}
run_one Qwen/Qwen3-14B                           qwen3-14b
run_one microsoft/phi-4                          phi-4
run_one mistralai/Mistral-Nemo-Instruct-2407     mistral-nemo-12b
$PY summarize.py --negatives qwen3-14b phi-4 mistral-nemo-12b --out results/threshold.json
run_one ../trial98                               gams3-12b-trial98
$PY summarize.py --negatives qwen3-14b phi-4 mistral-nemo-12b --positive gams3-12b-trial98 --out results/summary.json
echo "ALL DONE $(date)"
