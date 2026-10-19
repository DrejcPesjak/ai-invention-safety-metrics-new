#!/bin/bash
# Arm B sweep to completion, then the tiered Arm A scan. Detached and resumable:
# both stages append to their jsonl and skip what is already there.
cd "$(dirname "$0")"
{
  ./run_s3.sh
  echo "=== ARM B DONE: $(wc -l < results/armb_w05w.jsonl) rows at $(date +%H:%M) ==="
  ./run_s4.sh 105
  echo "=== ARM A DONE: $(wc -l < results/arma_w05w.jsonl) rows at $(date +%H:%M) ==="
} >> logs/sweep.log 2>&1
