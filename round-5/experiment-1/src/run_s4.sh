#!/bin/bash
# Chunked Arm A: restart every few rows so RSS stays bounded (same reason as run_s3.sh).
# $1 = total wall-clock budget in minutes for the whole tiered scan.
cd "$(dirname "$0")"
BUDGET_MIN=${1:-120}
END=$(( $(date +%s) + BUDGET_MIN*60 ))
for i in $(seq 1 60); do
  NOW=$(date +%s); LEFT=$(( (END - NOW) / 60 ))
  if [ "$LEFT" -le 1 ]; then echo "S4 BUDGET EXHAUSTED"; break; fi
  BEFORE=$(wc -l < results/arma_w05w.jsonl 2>/dev/null || echo 0)
  .venv/bin/python method.py --stage s4 --arm-a-budget-min "$LEFT" --arm-a-max-rows 200 \
     2>&1 | grep -vE "Fetching|it/s\]|B/s\]" | tail -20
  AFTER=$(wc -l < results/arma_w05w.jsonl 2>/dev/null || echo 0)
  echo "S4 CHUNK $i: $BEFORE -> $AFTER rows, ${LEFT} min were left"
  if [ "$AFTER" == "$BEFORE" ]; then echo "S4 COMPLETE or STALLED at $AFTER rows"; break; fi
done
