#!/bin/bash
# End-to-end reproduction of the alpha_50 steering experiment.
# One model is resident at a time; each member's result is written to results/ as soon as
# it finishes, so a crash never loses earlier work and any prefix of the panel is a
# complete, reportable artifact.
set -euo pipefail
cd "$(dirname "$0")"

# Triton JIT-compiles a CUDA utility module at first GPU use and fails hard without a
# C compiler.
command -v gcc >/dev/null || apt-get install -y gcc

uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python torch --torch-backend=auto
uv pip install --python=.venv/bin/python "transformers>=4.51" accelerate huggingface_hub \
    numpy scipy pandas loguru httpx

# GPU pass, tier by tier (T1 reproduces + powers iteration 1; T4 carries the SafeRL arm).
for T in T1 T2 T3 T4; do
  .venv/bin/python runner.py --members "$T" --seeds 5 --seeds-d 2
done

# Offline recomputes: corrected fluency screen and per-member diagnostics, applied
# uniformly from the recorded generations (no GPU work repeated).
.venv/bin/python refluency.py
.venv/bin/python repatch.py

# Circularity control (ii): semantic re-scoring of the recorded generations.
.venv/bin/python judge.py

# Analysis + method_out.json
.venv/bin/python method.py
