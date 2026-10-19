#!/bin/bash
# Chunked S3: restart the process every N kernels so RSS is bounded absolutely.
# results/armb_w05w.jsonl is append-only and resumable, so a restart loses nothing.
cd "$(dirname "$0")"
N_TOTAL=$(.venv/bin/python -c "
import method; H=None
import json
print(len(method.kernel_specs.__doc__ or '') and 0)" 2>/dev/null || echo 0)
for i in $(seq 1 20); do
  BEFORE=$(wc -l < results/armb_w05w.jsonl 2>/dev/null || echo 0)
  .venv/bin/python method.py --stage s3 --s3-limit 6 2>&1 | grep -vE "Fetching|it/s\]"
  AFTER=$(wc -l < results/armb_w05w.jsonl 2>/dev/null || echo 0)
  echo "CHUNK $i: $BEFORE -> $AFTER rows"
  if [ "$AFTER" == "$BEFORE" ]; then echo "S3 COMPLETE at $AFTER rows"; break; fi
done
