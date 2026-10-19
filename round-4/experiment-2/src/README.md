# Can a windowed weight scan catch hidden edits?

Three-arm, **tensor-only, prompt-free** experiment. Zero forward passes, zero LLM calls,
`openrouter_cost_usd = 0.00`.

| file | what it is |
|---|---|
| `method.py` | orchestrator (`--stage {gate,arm1,arm2,arm3,numbers,all}`) |
| `wstats.py` | W01–W05 **vendored unchanged** from the iteration-3 archive + the new windowed statistic `W05w` |
| `eligibility.py` | the **pre-registered** eligibility rule; hashed and stamped before any rate is computed |
| `synth.py` | edit generators written verbatim from the dependency dossier's recipe equations |
| `hubio.py` | metadata-only fetches, snapshot download, immediate purge |
| `statsx.py` | AUROC (always with an explicit orientation), Wilson intervals, grouped bootstrap, permutation |
| `verify_numbers.py` | recomputes **every** entry of `numbers.json` from the raw rows; exit code is stored in `method_out.json.metadata.assertion_block` |
| `numbers.json` | every numeral the paper may quote, each with units, n, CI, CI method, source file, and orientation |
| `method_out.json` | schema-validated artifact output (baseline vs our method as `predict_*` per checkpoint) |

## The statistic

The archived certificate pools the Gram over **every** residual-write matrix in the stack:

```
A   = sum_m  W_m W_m^T / ||W_m||_F^2          (over ALL layers)
v1  = eigenvector of the SMALLEST eigenvalue of A
W05 = log10( min_m  ||v1^T W_m||^2 / (||W_m||_F^2 / d) )
```

`v1` is therefore a **global** object, and the archived unit test showed that with 4 of 12
matrices edited it is no longer the injected direction and `W02` collapses to 0. The blind
spot is a *pooling* artefact, so `W05w` stops pooling across the whole stack:

```
window = k consecutive layers, stride max(1, k//2), ragged tail dropped
A_win  = sum over that window's matrices only  ->  v1_win
W05w(k)  = min over windows of log10( min_{m in win} e(v1_win, W_m) )
c(k)     = min over ADJACENT window pairs of |cos(v1_win_i, v1_win_i+1)|
W05wc(k,tau) = W05w(k) if c(k) >= tau else +inf
```

`k = L` collapses to a single window covering the whole stack, so **`W05w(L) == W05`
exactly** — asserted on every model at 1e-9 as a built-in reproduction gate.

## Reading the numbers

* **Every AUROC carries an `orientation` field.** The abliterated class has *lower* `W05`, so
  the raw (higher-is-positive) AUROC is the complement of the oriented one. Both are emitted.
* **Two denominators are reported, never one.** The primary false-positive rate uses the
  eligibility-filtered population; the archived unfiltered `0/160` is kept as secondary and
  labelled as computed on a population containing unit-test fixtures, speculator heads,
  quantized re-uploads, and mis-indexed >4.2B repos.
* **The operating point is panel-fitted.** `-2.7415117804288127` was fitted on 44 checkpoints
  and never validated out of panel; the panel margin is 0.0763 log10 and is carried by two
  individual checkpoints. `numbers.json` says so in `threshold_provenance`.
* **Panel-fitted `W05w` thresholds are circular for the panel positives** that defined them.
  The frontier therefore reports `sensitivity_G2_out_of_fit` separately from
  `sensitivity_G1_IN_FIT_circular`.
* **UNRESOLVED is a result, not an error.** At Hub scale a quantized or unsupported upload is
  a refusal-to-score — an auditable signal — not a silent clean read.

## Reproducing

```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
uv pip install --python=.venv/bin/python numpy==2.5.2 scipy==1.18.0 safetensors==0.8.0 \
    huggingface-hub==1.27.0 pandas==3.0.5 tqdm==4.70.0 loguru==0.7.3 requests==2.34.2 psutil==7.2.0
.venv/bin/python method.py --stage all
```

Every stage is resumable: re-running appends only rows that are missing from the `results/*.jsonl`
files, so an interrupted scan restarts without re-downloading.
