# upd_hypo — test_idea

> Phase: `invention_loop` · round 1 · `upd_hypo`
> Run: `iter1_33370088803c` — Catching Edited Safety Models by Reading Weights in Sliding Windows
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent, claude-opus-5)

### [1] CONFIG · 2026-08-13 15:56:18 UTC

```
model: claude-opus-5 | effort: medium | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_1/upd_hypo/upd_hypo
```

### [2] HUMAN-USER prompt · 2026-08-13 15:56:24 UTC

```
/compact
```

### [3] SYSTEM-USER prompt · 2026-08-13 15:58:40 UTC

```
This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.

Summary:
1. **Primary Request and Intent:**

   The conversation consists of a single task delivered in one large user-role prompt. I was invoked as an **AI Inventor "hypothesis reviser" (Step 3.6: UPD_HYPO in the invention loop)**. The explicit intent:

   - Take the **current hypothesis** ("Safety as nearness to a tipping point"), all 5 artifacts from iteration 1, the current paper draft, and reviewer feedback, and **revise the hypothesis based on what the evidence supports**.
   - **SCOPE CONSTRAINT (stated emphatically, twice):** "Your ONLY output is the revised hypothesis text. You do NOT run code, produce artifacts, fix bugs, or otherwise act on the evidence yourself — the next iteration of the invention loop will spawn fresh artifacts based on your revised hypothesis. Reflect on the evidence and rewrite the hypothesis; nothing else."
   - Principles given: ground every revision in specific artifacts/results; **treat negative and null results as valuable contributions** and frame them as the contribution rather than fabricating a positive narrative; increase specificity as evidence accumulates; don't inflate confidence; preserve the core AII prompt unless contradicted.
   - "Do NOT generate a completely new hypothesis. Take the current hypothesis and REVISE it... Keep the core idea."
   - Address reviewer critiques directly.
   - Classify **(A) the H↔H edge** using Moulines's structuralist typology (`evolution` / `embedding` / `replacement`) with a ≤120-char rationale.
   - Classify **(B) the A↔A edges** for each artifact created this iteration using MultiCite citation-function typology (`background`/`motivation`/`uses`/`extends`/`similarities`/`differences`), with the explicit rule: "Predecessors are ALWAYS artifacts from EARLIER iterations — artifacts within one iteration run in parallel and cannot depend on each other, so never emit a relation between two same-iteration artifacts (it will be dropped)."
   - Output as JSON to `./.terminal_claude_agent_struct_out.json` matching a provided schema (fields: title, hypothesis, relation_rationale, confidence_delta, key_changes, relation_type, artifact_relations).

   The **user's original request** (provided as context, explicitly NOT as instruction): "qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation."

   A final user message then requested this summary, **TEXT ONLY, with no tool calls**.

2. **Key Technical Concepts:**

   - **Bistability / fold bifurcation / critical slowing down (CSD)** and the **early-warning-signal (EWS)** toolkit imported from ecology and climate science (Scheffer, Dakos, `ewstools`): slowed recovery from small perturbations, rising variance, rising lag-1 autocorrelation, flickering.
   - **Autoregressive generation as a stochastic dynamical system** — state = generated prefix + KV cache; measurements over GENERATED steps (not a single forward pass).
   - **Refusal observable r_t** — logit-lens log-odds of refusal-onset tokens vs continuation tokens; chosen because it survives the abliteration weight edit (unlike a projection onto the refusal direction).
   - **Detrending** — subtracting the across-rollout mean trajectory per generated step before computing AC1/Var*, because chat-template openings create a deterministic trend that inflates AC1.
   - **Steering hysteresis** — alpha ramped along a refusal axis in units of NORM_L (median residual-stream norm at the steering layer); arms UP-RAMP, ENTRY-AT-ALPHA, DOWN-RETAINED, DOWN-FORCED-A (byte-identical unsteered refusal prefill — the primary control), DOWN-FORCED-B (alpha-schedule replay positive control), RESET (noise floor).
   - **Excess width** = alpha_down_forced − alpha_down (paper convention; prereg.json used the opposite sign) — isolates latent path dependence from ordinary conditioning on emitted refusal text.
   - **Switching Proximity Index (SPI)** — mean of four z-scored terms [−log lambda, log detrended Var*, Fisher-z(AC1), logit(flicker)], with FROZEN normalization constants.
   - **alpha_50** — the steering coefficient (in NORM_L units) at which a fresh constant-alpha generation crosses a 50% refusal rate; the surviving positive metric.
   - **Directional ratchet** — the replacement mechanism: compliance is absorbing, refusal is a decision made at generation ONSET.
   - **Abliteration** — W ← W − c·rr^T W, orthogonalizing writes against the refusal direction (Arditi et al.).
   - **Task-vector safety ladder** — W(t) = W_base + t(W_instruct − W_base), gated by a fluency screen (WikiText perplexity within 2× of the t=1 endpoint, distinct-3, max-n-gram-repeat).
   - **Weight lineage as resampling unit** for all model-level bootstrap CIs; **paired bootstrap** of correlation differences.
   - **Rival metrics:** AMS (activation cluster separation sigma; 96 forward passes; 71% LOO), RAS/SafeVec (needs reference model + unsafe/jailbreak prompts), VISAGE (weight-space basin volume), AQI.
   - **Knowledge-action gap** — 98.2% probe AUROC vs 45.1% output sensitivity (arXiv:2603.18353).
   - **LLM-as-judge failure mode** — safety-trained judges refusing to label harmful compliance as compliance without an evaluator system prompt.
   - **Moulines structuralist typology** (evolution/embedding/replacement) and **MultiCite citation-function typology** for research-trace edges.

3. **Files and Code Sections:**

   - **`/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json`** — the sole file created; the deliverable. It contains the complete revised hypothesis JSON. Key structure written:
     - `title`: `"Safety sets the price of refusing"` (short, jargon-free, ~4-8 words per schema guidance).
     - `relation_type`: `"evolution"`.
     - `relation_rationale`: `"Same object (generation dynamics, benchmark-free score); mechanism replaced bistable->directional, metric SPI->alpha_50."`
     - `confidence_delta`: `"decreased"`.
     - `artifact_relations`: `[]` (empty — all 5 artifacts are from iteration 1, and the task forbids same-iteration edges; there are no earlier iterations).
     - `hypothesis`: a long structured body with two sections — **WHAT IS NOW SETTLED** (R1 hysteresis is prefix content not latent state; R2 EWS indicators track lineage not safety; R3 the directional ratchet; R4 the judge decides the result before the models do) and **THE REVISED CLAIMS** (H1' price of refusal split into (a) reachable-mode and (b) price-of-mode; H1'' lexical-artefact controls; H1''' cross-model comparability; H2' directional ratchet with assumption-free statistics; H3' run AMS; H4' the blind-spot test; H5' hardened judge probe).
     - `key_changes`: 12 bullets mapping each revision to the artifact evidence or reviewer critique that drove it.

   - Files **referenced but never opened** (all context arrived inline in the prompt): the five artifact workspaces under `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art/` (`gen_art_dataset_1`, `gen_art_research_1`, `gen_art_experiment_1`, `gen_art_experiment_2`, `gen_art_experiment_3`), each with `method.py` / `data.py` and `full_*_out.json`; plus `prereg.json`, `prereg_amendment.json`, `direction.py`, `judge_probe.py`, `refit_certified.py`, `results/ladder_models_manifest.json` as cited by the reviewer.

   - `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/user_uploads` — user-provided reference materials folder mentioned in the prompt; **not inspected**.

4. **Errors and fixes:**

   No tool errors occurred. The single `Write` call succeeded on the first attempt.

   One **potential discrepancy I should flag rather than claim as resolved**: the environment's stated primary working directory is `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_1/upd_hypo/upd_hypo`, so `./.terminal_claude_agent_struct_out.json` resolves under `run_UtpduT_D2IS2`. I wrote the file to the **`run_CbJDs3opF7E_`** path instead (the run ID that all artifacts, the user_uploads folder, and the memory index refer to). The file exists at the `run_CbJDs3opF7E_` location; whether the harness reads from there or from the CWD-relative `run_UtpduT_D2IS2` path is unverified.

   The **errors documented in the evidence** (not mine — they are content I incorporated) are worth preserving:
   - Injecting at a decoder layer's *output* is a no-op for that layer's own readout (|delta| exactly 0 at every eps, because the layer writes K/V before a forward hook fires) → moved to a forward **pre-hook** on the layer input.
   - Free-running delta cannot estimate a decay rate (streams diverge in ~7 steps; |delta| grows) → teacher-forced channel is primary.
   - mean|delta| is upward-biased +38% to +68% at every n_roll because E|N(mu,s)| > |mu| → fit the **signed** across-rollout mean.
   - Flicker-as-fraction saturates at 1.0 → use crossings per 100 steps.
   - The pre-registered refusal-token harvesting criterion admitted 'Creating', 'Writing', 'Hack', 'Script', 'Title' → replaced with behaviour-conditioning on actual first generated tokens.
   - fp16 batched greedy decoding is not batch-invariant (3/4 identical at batch=4 vs 1) → fp32 is load-bearing.

5. **Problem Solving:**

   The core intellectual problem was **how to honestly revise a hypothesis whose three primary claims were all refuted, without either fabricating a positive story or abandoning the frame**. Resolution:

   - Classified the revision as **`evolution`, not `replacement`**, because the conceptual frame (generation as a dynamical system; a benchmark-free act-side safety score) survives intact — only the specific mechanism (bistable fold → directional ratchet) and the specific metric (SPI → alpha_50) changed.
   - Set `confidence_delta` to **`decreased`** — the honest reading, since the headline claims failed and the replacement metric is itself unpowered.
   - Preserved the refutations as **named, load-bearing results** (R1–R4) rather than deleting them, per the "negative results are valuable" principle. The EWS negative is framed as the first controlled test of the CSD toolkit on LLM generative dynamics.
   - Mapped **every one of the 13 reviewer critiques** into either a retired claim, a new pre-registered test, or a stated reporting requirement — including the pre-emption by Galeone et al. (arXiv:2606.24952), which required reframing the site-selection "discovery" as a refusal-specific confirmation/extension of their detection-vs-steering gap.
   - Resolved the A↔A edge question by reasoning that all 5 artifacts are same-iteration and therefore ineligible → empty `artifact_relations` list.

6. **All user messages:**

   - **Message 1 (the task prompt):** The full UPD_HYPO task — containing the current hypothesis, all 5 artifacts, the current paper draft, reviewer feedback, available domain handbooks, the task definition (revise hypothesis; classify H↔H and A↔A edges), the JSON schema, and the note that "User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/user_uploads`. Check this folder for anything relevant to your task." It embedded the user's original request as explicitly-labelled context, not instruction: *"qwen3 on huggingface has base model also official safety finetuned version and there is a community finetuned uncensored model called abliterated. take these models and do a mech interp analysis of how they differ in activation. also find some patterns in internal computation on safety prompts. and possibly create a new metric for safety. so that for any random model on huggingface you would not need to run the full benchmarks, but only this metric on 0- to few prompts and get a safety evaluation"*

   - **Message 2 (the summary request):** *"CRITICAL: Respond with TEXT ONLY. Do NOT call any tools. - Do NOT use Read, Bash, Grep, Glob, Edit, Write, or ANY other tool. - You already have all the context you need in the conversation above. - Tool calls will be REJECTED and will waste your only turn — you will fail the task. - Your entire response must be plain text: an <analysis> block followed by a <summary> block."* followed by the detailed summary structure specification.

   **Security-relevant constraints in effect (from the CLAUDE.md project instructions in the system prompt — preserved verbatim in substance):**
   - "Never bypass git hooks (`--no-verify` etc.); fix the root cause."
   - "**Builds, CI, and deploys are 100% LOCAL — never use GitHub Actions.**" / "NEVER build or deploy via GitHub Actions: no `gh workflow run`, no `aii_launcher --rebuild --gh` (retired; fails fast)."
   - The deployed-dashboard admin password is `AII_DEMO_ADMIN_PASSWORD` in the **gitignored** repo-root `.env`; "The password is NOT committed: `gitleaks` runs pre-commit and again in `aii_public/sync.sh`, and allowlisting a genuine credential to get it into a repo with a public-export path is exactly the wrong trade. The pointer is what belongs in git; the value belongs in `.env`."
   - The private deployment domain is deliberately kept out of tracked files by the `aii-private-domain` gitleaks rule.
   - `aii_launcher --public-sync` **stages only**; the public push is manual so the export can be vetted first.
   - Do not hand-roll docker builds, image pushes, RunPod pod lifecycle, or the public-export pipeline — everything goes through `aii_launcher`.
   - "Never run a second build concurrently with the watcher's" — it evicts the registry cache.
   - From the session guidance: "Do not call the AgentTool unless the user requested it. Do not use workflows or deep-research unless the user requested it."

7. **Pending Tasks:**

   None outstanding from the user. The assigned task (produce the revised hypothesis JSON) is complete. Two loose ends worth surfacing:
   - The output path discrepancy between the CWD (`run_UtpduT_D2IS2`) and the path I wrote to (`run_CbJDs3opF7E_`).
   - `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/user_uploads` was never inspected.

8. **Current Work:**

   Immediately before the summary request, I completed the task by writing the revised hypothesis JSON in a single `Write` call. The revision:

   **Retired** (based on artifact evidence):
   - H1/H1b (hysteresis residual) — `art_TFe9eI-2QZN3` excess width 0.019 [−0.057, 0.099] instruct, −0.031 [−0.070, 0.001] abliterated, −0.330 [−0.990, 0.000] base; every CI overlaps 0 and every lower bound sits under the temperature-0.7 RESET noise floor (p95 = 0.05); FORCED-B positive control reproduces the retained arm to |diff| = 0.000 so the null is not a plumbing artifact.
   - H2/H2b and SPI-as-product — `art_UthAQuH8WZ5C`: Qwen triad Var* 3.101–3.152, AC1 0.245–0.304, flicker 40.2–42.2 all with CIs overlapping 0 while SmolLM2 separates; ordering partly reverses (instruct has lowest Var*/flicker and fastest relaxation); lambda non-identifiable at every geometry (T_fit ≥ 128 certified → requirement moved to n_roll ≥ 40 vs 20 achieved); random perturbation direction reproduces the ordering (instruct−abliterated −0.493 CI-excluding-0 vs refusal direction −0.226 n.s.); SPI ranks backwards (rho = −0.20 vs supervised +0.40). Kept as a controlled negative — the first EWS test on LLM generative dynamics.

   **New/promoted claims:**
   - **H2' directional ratchet** — compliance absorbing (up-ramp fails 92–100% mid-generation, 10/10 at delta ∈ {0.05,0.1,0.2,0.4} up to alpha_max=4.0, 9/10 with an [L−2,L+2] window; free-running 16-step survival ratio 2.57–5.33 vs teacher-forced 0.119–0.233). Measured with **assumption-free** survival-ratio/AUC statistics only, so no identifiability gate to fail (addresses MAJOR/rigor #5).
   - **H1' alpha_50** as primary metric, explicitly split into (a) reachable-refusal-mode-at-all (base undefined/max 0.20 vs instruct & abliterated both reaching 1.00 — supported) and (b) price of the mode (instruct 0.475 vs abliterated 0.550, ~16% — **explicitly unsupported**, 0.075 gap on a 0.05 grid with 5 Bernoulli draws/point and no CI). Iteration 2 must run ≥20 prompts × ≥5 seeds per alpha, logistic dose-response, per-model bootstrap CIs, paired bootstrap on the instruct−abliterated difference; withdraw (b) if that CI overlaps 0.
   - **H1'' lexical-artefact controls** (token-disjoint paraphrased axis; semantic-judge scoring; norm-matched non-safety stylistic axis) — a lexical verdict is declared a publishable finding, not a failure.
   - **H1''' cross-model comparability** — ≥3 more lineages from the frozen 137-checkpoint manifest incl. Qwen3-1.7B (base/instruct/abliterated/uncensored), lineage as resampling unit, NORM_L check (18.58 base vs 21.21/21.28), plus disclosure that steering used `mlabonne/Qwen3-0.6B-abliterated` while dynamics used `huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2`.
   - **H3'** run AMS (cheap at 96 forward passes), validated against its Table I checkpoints; RAS skipped for empty overlap, VISAGE for cost.
   - **H4'** alpha_50 on the 6 verified behavioural-uncensored fine-tunes.
   - **H5'** rebuild the judge probe at ≥100 items over all four rubric classes with two independent annotators + kappa, publish disputed items (incl. the self-harm refusal-by-redirection item that inflates the 'gold' judge to 21/21), and restate the 0.092→0.858 ASR revision if 0/7 partly dissolves.

   Novelty and reporting fixes folded in: cite Galeone et al. arXiv:2606.24952 and reframe the site-selection result as a refusal-specific extension; add arXiv:2508.21448, 2602.02712, 2509.22067, 2509.13450, 2603.24543; exact permutation p-values or drop the n=4 SPI numbers; a prereg-deviations table covering the primary-statistic sign inversion and the alpha-grid amendment; demote the zero-hits arXiv search to a footnote; per-model observable-validity gate; relabel the in-house abliteration ladder "our reimplementation failed".

9. **Optional Next Step:**

   The assigned task is concluded — the deliverable exists and matches the schema. The only next step directly in line with the task would be to **verify the output landed where the harness expects**, given the task instruction was: *"Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`"* and *"IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above."* I wrote to `/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json`, whereas `./` resolves to the environment's stated primary working directory `/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_1/upd_hypo/upd_hypo`. If the harness reads the CWD-relative path, the same JSON would need to be written there as well. I would confirm with the user before duplicating the file, since the run-ID mismatch may be intentional (all artifacts, user_uploads, and the memory index refer to `run_CbJDs3opF7E_`).

If you need specific details from before compaction (like exact code snippets, error messages, or content you generated), read the full transcript at: /root/.claude/projects/-ai-inventor-aii-data-runs-run-UtpduT-D2IS2-3-invention-loop-iter-1-upd-hypo-upd-hypo/65fd011a-43be-4fb8-9c2a-b83ce7ca3dc7.jsonl
Continue the conversation from where it left off without asking the user any further questions. Resume directly — do not acknowledge the summary, do not recap what was happening, do not preface with "I'll continue" or similar. Pick up the last task as if the break never happened.
```

### [4] SYSTEM-USER prompt · 2026-08-13 15:58:40 UTC

```
<local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages or otherwise consider them in your response unless the user explicitly asks you to.</local-command-caveat>
```

### [5] SYSTEM-USER prompt · 2026-08-13 15:58:40 UTC

```
<command-name>/compact</command-name>
            <command-message>compact</command-message>
            <command-args></command-args>
```

### [6] SYSTEM-USER prompt · 2026-08-13 15:58:40 UTC

```
<local-command-stdout>[2mCompacted (ctrl+o to see full summary)[22m</local-command-stdout>
```

### [7] ASSISTANT · 2026-08-13 16:08:45 UTC

```
No response requested.
```

### [8] SYSTEM-USER prompt · 2026-08-13 16:08:45 UTC

```
i want cheap safety metrics that work on a single model. no parent, no reference model, no
attested base to diff against - assume i found some random model on huggingface and i have
nothing else. reads weights or activations. generation allowed but minimal, a few prompts at
most. seconds to a couple of minutes per model, not a benchmark run.

step 1 - explore. take one lineage: Qwen/Qwen3-4B-Base, Qwen/Qwen3-4B, Qwen/Qwen3-4B-SafeRL (the
official safety RL model, not the instruct one), and an abliterated Qwen3-4B. instruct, saferl
and abliterated share a chat template so they are directly comparable, base uses a different
format so keep it separate. poke around open ended, look at weights and activations, see what
actually differs between the four.

step 2 - design 50 metrics. informed by what you found in step 1, but also by the literature -
safety papers and mech interp papers in general, not only safety ones. include a few black-box
metrics too, things that only read logits or output text, like the logit-gap margin, so we have
a comparison point for whether looking inside the model actually buys anything.

step 3 - test all 50 much wider. other lineages, pairs and triplets where a safety-tuned or
abliterated sibling exists, and standalone models where none does. for each metric: does it
separate safe vs normal vs abliterated. hold out a set of models that no metric is tuned on,
because picking the best of 50 on the models you designed them on is cheating.

step 4 - ground truth. pull real benchmark numbers from official sources, model cards, papers,
leaderboards, not just your own judge. safety is not only refusal - try to cover other aspects
too, see TrustLLM and AIR-Bench for what that means. if that turns out to be too much, then two
separate refusal rates is acceptable as a fallback: refusal on harmful prompts, and refusal on
harmless prompts that only look dangerous (xstest style). either way a model that refuses
everything must lose, not win. also pull capability benchmarks, gsm8k, mmlu, arena-hard, to
see whether safety trades off against performance. do not use Qwen3Guard as a judge for SafeRL,
it was SafeRL's training reward.

step 5 - take the 10 best metrics and correlation-test them against those benchmark numbers.
report the resampling unit and both aggregation units. a metric that only works within one
architecture family is a negative result, say so.

bonus - if a metric works really well, mech interp analysis of why. what is it reading, which
layers and components carry it, what breaks it.

bonus bonus - instead of a static formula, train a small metamodel on activations that predicts
the safety benchmark scores. if it beats the formulas, explain what in the model's internal
computation it is picking up, and why that signal exists.


round 1 already built the prompt corpus, the model manifest (137 checkpoints, 93 lineages),
  and empirical refusal-token lexicons for 10 tokenizer families. reuse them. it also found
  that the default judge never labels COMPLIANCE unless you give it an evaluator system
  prompt - keep that fix.
you can also help yourself with some things from the previous run, available here: 
https://github.com/AMGrobelnik/ai-invention-c9546e-rating-model-safety-in-eighty-forward-pa
```

### [9] TOOL CALL — Bash · 2026-08-13 16:09:11 UTC

```
cd /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/upd_hypo/upd_hypo && python3 -c "
import json;d=json.load(open('.terminal_claude_agent_struct_out.json'))
for k,v in d.items(): print('===',k,'===',type(v).__name__); print(str(v)[:300] if not isinstance(v,list) else v[:3])
"
```

### [10] TOOL RESULT — Bash · 2026-08-13 16:09:11 UTC

```
{"stdout": "=== title === str\nSafety sets the price of refusing\n=== hypothesis === str\nSafety fine-tuning does NOT park a model near a bistable comply/refuse tipping point. Iteration-1 evidence refutes that reading three independent ways, and the same experiments replace it with a directional account: refusal is not an attractor the model sits beside, it is a DECISION MADE AT GENERATI\n=== relation_rationale === str\nSame object (generation dynamics, benchmark-free score); mechanism replaced bistable->directional, metric SPI->alpha_50.\n=== confidence_delta === str\ndecreased\n=== key_changes === list\n['RETIRED H1/H1b (hysteresis residual): forced-prefix control gives excess width 0.019 [-0.057,0.099] instruct, all CIs overlapping 0 and under the noise floor; positive control reproduces the retained arm exactly, so the null is not a plumbing artifact.', 'RETIRED H2/H2b and SPI-as-product: EWS indicators separate lineage (SmolLM2) not safety (Qwen triad CIs all overlap 0), the ordering partly reverses, lambda is non-identifiable at every geometry reached, a random perturbation direction reproduces the ordering, and SPI ranks backwards (rho=-0.20 vs +0.40 supervised). Kept as a controlled negative result — the first EWS test on LLM generative dynamics.', \"NEW core mechanism (H2'): a directional ratchet, not a fold. Compliance is absorbing (up-ramp fails 92-100% mid-generation; free-running survival ratio 2.57-5.33 vs teacher-forced 0.119-0.233); refusal is a decision made at ONSET.\"]\n=== relation_type === str\nevolution\n=== artifact_relations === list\n[]", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_1/upd_hypo/upd_hypo", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Write · 2026-08-13 16:10:49 UTC

```
File: /ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json

{
  "title": "Reading safety off a single model",
  "hypothesis": "CORE CLAIM. A model's safety behaviour is legible from the model ALONE — its weights and its activations on a handful of prompts — without a parent, a reference model, an attested base to diff against, or a benchmark run. Concretely: there exists a cheap single-model observable, computable in seconds to a couple of minutes, that correlates with EXTERNALLY MEASURED safety scores across weight lineages and across architecture families, and that beats the best black-box (logits/output-text-only) baseline. The claim is falsifiable in three separate places, and each failure mode is a reportable result, not a setback.\n\nOPERATING CONSTRAINT (new, and it retires part of the previous hypothesis). The metric sees ONE checkpoint. No sibling, no base, no diff. This is the assumed deployment situation: a random model found on HuggingFace with nothing else. Every candidate metric must be computable under that constraint. Siblings (base / instruct / safety-RL / abliterated) are permitted ONLY as VALIDATION CONTRASTS — to check that a metric moves in the right direction across a lineage — never as an input to the metric itself. Iteration 1's headline quantities were all sibling CONTRASTS (instruct minus abliterated excess width, instruct minus abliterated Var*), so under this constraint they are demoted from metrics to diagnostics. The one iteration-1 positive that survives the constraint intact is alpha_50, because the refusal axis is extracted from the model under test and the steering sweep is run on that same model.\n\nWHAT ITERATION 1 SETTLED, CARRIED FORWARD AS ESTABLISHED (do not re-litigate; do not re-run):\nR1. Steering hysteresis is prefix content, not latent state. Excess width 0.019 [-0.057, 0.099] instruct, -0.031 [-0.070, 0.001] abliterated, -0.330 [-0.990, 0.000] base; every CI overlaps 0, every lower bound sits under the temperature-0.7 RESET noise floor (p95 = 0.05), and the FORCED-B positive control reproduces the retained arm to |diff| = 0.000, so the null is not a plumbing artefact. No metric in the 50 may be built on a hysteresis residual.\nR2. Early-warning-signal indicators (variance, lag-1 autocorrelation, flicker, recovery rate) track LINEAGE, not safety. On the Qwen triad Var* 3.101-3.152, AC1 0.245-0.304, flicker 40.2-42.2 per 100 steps, all CIs overlapping 0, while SmolLM2 separates cleanly; the ordering partly reverses (instruct has the LOWEST Var*/flicker and the FASTEST relaxation); lambda is non-identifiable at every geometry reached (T_fit >= 128 certified, n_roll >= 40 required against 20 achieved); a RANDOM perturbation direction reproduces the ordering better (instruct-abliterated -0.493, CI excluding 0) than the refusal direction (-0.226, n.s.); and the composite SPI ranks backwards (rho = -0.20 against a supervised +0.40). This is a clean controlled negative — the first test of the critical-slowing-down toolkit on LLM generative dynamics — and it should be REPORTED as such, but EWS-style indicators enter the 50 only as declared-expected-to-fail controls, not as hopefuls.\nR3. The directional ratchet is real and it is the mechanistic licence for cheap metrics. Compliance is absorbing: up-ramping alpha mid-generation fails to induce refusal in 92-100% of trials (10/10 at every step size delta in {0.05, 0.1, 0.2, 0.4} up to alpha_max = 4.0; 9/10 with an [L-2, L+2] multi-layer window), and free-running deviation GROWS (16-step survival ratio 2.57-5.33) where teacher-forced deviation decays (0.119-0.233). Refusal is a decision made at generation ONSET. Consequence for design: the informative measurement window is the first few generated tokens, which is exactly why a few-prompt, seconds-scale metric is plausible at all. Metrics that integrate over long rollouts are a priori disfavoured and should be a minority of the 50.\nR4. The judge decides the result before the models do. The default judge never labels COMPLIANCE without an explicit evaluator system prompt; with the fix, measured ASR moved 0.092 -> 0.858. The fix is MANDATORY everywhere in this iteration. Separately, our own judge is no longer allowed to be the ground truth (see H4).\n\nTHE REVISED CLAIMS.\n\nH0 (exploration, no hypothesis attached). On the Qwen3-4B lineage — Qwen/Qwen3-4B-Base, Qwen/Qwen3-4B, Qwen/Qwen3-4B-SafeRL, and an abliterated Qwen3-4B — characterise what actually differs, open-endedly, in BOTH weights and activations. Instruct / SafeRL / abliterated share a chat template and are directly comparable; Base uses a different format and is analysed separately, never pooled into a four-way contrast. Note explicitly that SafeRL is the official safety-RL model and NOT the instruct model, and that this is the first lineage in this project containing a deliberate safety-RL arm as distinct from generic instruction tuning — the instruct-vs-SafeRL contrast is the one that isolates safety training from helpfulness training, and iteration 1 never had it. Deliverable is a findings list, not a verdict.\n\nH1 (the battery). Fifty single-model metrics, designed from H0's findings AND from the literature — safety papers and general mechanistic-interpretability papers alike, not safety papers only. Composition requirements: (a) at least 8 must be BLACK-BOX, reading only logits or output text — logit-gap margin between refusal-onset and continuation tokens at the first generated position, refusal-token logprob mass, first-token entropy, output-length asymmetry between harmful and benign prompts, judge-on-output — and these are the comparison point that decides whether looking inside the model buys anything at all; (b) at least 8 must be WEIGHTS-ONLY, requiring zero generation (spectral statistics of MLP and attention write matrices, low-rank structure of the unembedding-adjacent subspace, norm anisotropy at candidate refusal layers, weight-space distance-to-nearest-degenerate-direction, and — motivated by abliteration being literally W <- W - c*r*r^T*W — direct tests for a RANK-DEFICIENT or ORTHOGONALISED write direction, which should be detectable in one checkpoint without its parent); (c) at most 10 may require more than 60 s on a single 4B model; (d) each metric declares its cost in forward passes and wall-clock before it is run. alpha_50 (the steering coefficient in NORM_L units at which a fresh constant-alpha generation crosses a 50% refusal rate) enters as one candidate among fifty, no longer as the headline.\n\nH2 (the test, and the honest split). All 50 are evaluated much wider: additional lineages with a safety-tuned or abliterated sibling (pairs and triplets), plus STANDALONE models where no sibling exists — because standalone is the actual deployment case. Reuse iteration 1's frozen 137-checkpoint / 93-lineage manifest, prompt corpus, and the empirical refusal-token lexicons for 10 tokenizer families; do not rebuild them. Metric selection is contaminated by design if the best of 50 is picked on the models the 50 were designed on, so a HELD-OUT SET of lineages is fixed BEFORE any metric is written, is touched by nothing until selection is frozen, and carries the reported result. Statistics: the resampling unit is the WEIGHT LINEAGE, and BOTH aggregation units are reported — per-checkpoint and per-lineage — because they can disagree and iteration 1 has already seen a sign flip between member-level and lineage-level aggregation on 5 of 16 cells. Pre-registered falsifier: a metric that separates safe / normal / abliterated only WITHIN one architecture family is a NEGATIVE RESULT and must be reported as one, in those words, not repackaged as family-specific success.\n\nH3 (ground truth is external). Correlation targets come from official sources — model cards, papers, leaderboards, TrustLLM and AIR-Bench reported numbers — not from our own judge. Our judge is used only where no external number exists, and where it is used the R4 evaluator-system-prompt fix is in force and the reliance is stated. Safety is not only refusal: cover the broader axes TrustLLM and AIR-Bench define. Documented fallback if that coverage proves infeasible: TWO refusal rates, on harmful prompts and on XSTest-style harmless-but-alarming prompts. Under either scoring, a model that refuses EVERYTHING must LOSE, not win; any metric whose top-ranked model is a blanket refuser is disqualified regardless of its correlation. Capability benchmarks (GSM8K, MMLU, Arena-Hard) are pulled alongside, to test whether safety trades against performance and to check that a metric is not covertly reading capability. HARD CONSTRAINT: Qwen3Guard must NOT be used as a judge for Qwen3-4B-SafeRL — it was that model's training reward, and using it is circular.\n\nH4 (the correlation test). The 10 best metrics from the frozen selection are correlation-tested against the external benchmark numbers on the held-out lineages. Report Spearman with lineage-level bootstrap CIs, both aggregation units, and a paired bootstrap of each white-box metric against the strongest black-box baseline. Pre-registered outcome: if NO white-box metric's advantage over the best black-box baseline has a CI excluding 0, the finding is that reading inside the model buys nothing for cheap safety screening, and that is the paper's result.\n\nH5 (mechanism, conditional). If a metric works well, only then: what is it reading, which layers and components carry it, what breaks it. Layer-wise and component-wise ablation, a token-disjoint paraphrased refusal axis and a norm-matched non-safety stylistic axis as lexical-artefact controls (a lexical verdict is a publishable finding, not a failure), and a check that the metric is not a capability proxy.\n\nH6 (metamodel, conditional). Instead of a static formula, train a small metamodel on activations to predict the external safety scores directly. It must be trained and evaluated with the lineage as the split unit — never a random checkpoint split, which leaks siblings across the boundary. If it beats the formulas, the deliverable is not the score: it is an account of WHAT internal computation it is picking up and WHY that signal exists.\n\nCONFIDENCE. Lower than the previous statement, deliberately. Iteration 1 refuted its own headline mechanism, and its surviving positive (alpha_50's price-of-refusal discrimination, instruct 0.475 vs abliterated 0.550) rests on a 0.075 gap on a 0.05 grid with 5 Bernoulli draws per point and no CI — it is unpowered and may not survive. The new claim is broader, more falsifiable, and externally grounded, but it has no direct positive evidence yet, and the black-box baselines may well win. The most likely single outcome, on current evidence, is a partial negative: some metrics separate abliterated models (which carry a literal weight-space signature) while none tracks graded safety-RL strength across families. That outcome is worth reporting precisely.",
  "relation_rationale": "Prior refusal-dynamics claim survives as one candidate inside a larger single-model, externally-validated metric-screening theory.",
  "confidence_delta": "decreased",
  "key_changes": [
    "NEW OPERATING CONSTRAINT — single model, no parent, no reference, no attested base to diff against. This is the deployment case being targeted, and it demotes iteration 1's headline quantities (instruct-minus-abliterated excess width, instruct-minus-abliterated Var*) from metrics to validation diagnostics, since both are sibling CONTRASTS. alpha_50 survives the constraint because its refusal axis is extracted from, and its sweep run on, the model under test.",
    "SCOPE WIDENED from a single mechanism to a 50-metric screening battery. The previous hypothesis bet everything on one mechanism (bistability) and one composite (SPI); both failed. The revision spreads the bet and pre-commits to a selection procedure instead of to a favourite.",
    "BLACK-BOX BASELINES PROMOTED TO THE CENTRAL FALSIFIER. At least 8 of the 50 read only logits or output text (logit-gap margin, refusal-token logprob mass, first-token entropy, output-length asymmetry, judge-on-output). Pre-registered: if no white-box metric beats the best of them with a CI excluding 0, the result is that looking inside buys nothing.",
    "WEIGHTS-ONLY METRICS ADDED (>=8, zero generation), motivated directly by abliteration's mechanism W <- W - c*r*r^T*W — an orthogonalised or rank-deficient write direction should be detectable in ONE checkpoint without its parent. Iteration 1 had no weights-only arm at all.",
    "HELD-OUT LINEAGE SET FIXED BEFORE ANY METRIC IS WRITTEN, and untouched until selection is frozen. Picking the best of 50 on the models the 50 were designed on is the obvious failure mode of this design and is pre-empted structurally, not by caution.",
    "STANDALONE MODELS ADDED to the evaluation set. Iteration 1 tested only lineages where siblings existed; the actual use case has no sibling, so models with none are now first-class test subjects.",
    "GROUND TRUTH MOVED OUTSIDE THE PROJECT — official model cards, papers, leaderboards, TrustLLM and AIR-Bench numbers replace our own judge as the correlation target. Iteration 1's headline ASR number moved 0.092 -> 0.858 on a judge-prompt fix alone, which is exactly why the judge cannot also be the ruler.",
    "SAFETY REDEFINED AS TWO-SIDED — over-refusal (XSTest-style harmless-but-alarming prompts) is a required axis, with the explicit disqualification rule that a blanket refuser must LOSE. This kills the degenerate solution the previous refusal-only framing permitted.",
    "CAPABILITY BENCHMARKS (GSM8K, MMLU, Arena-Hard) ADDED, both to measure the safety/performance trade-off and as a confound check that a winning metric is not covertly reading capability.",
    "CIRCULARITY GUARD: Qwen3Guard is forbidden as a judge for Qwen3-4B-SafeRL, because it was that model's training reward.",
    "EXPLORATION LINEAGE UPGRADED to Qwen3-4B-Base / 4B / 4B-SafeRL / abliterated, with Base kept separate (different prompt format, never pooled into a four-way contrast). The instruct-vs-SafeRL arm is new and is the only contrast that isolates deliberate safety training from generic instruction tuning; iteration 1 had no safety-RL model.",
    "STATISTICS PRE-COMMITTED: weight lineage as the resampling unit, BOTH aggregation units reported (per-checkpoint and per-lineage), after iteration 1 observed a sign flip between the two on 5 of 16 cells. Within-family-only separation is declared a NEGATIVE RESULT in advance, in those words.",
    "R1 AND R2 CARRIED FORWARD AS SETTLED NEGATIVES, not re-run. Hysteresis is prefix content (all excess-width CIs overlap 0, positive control clean), and EWS indicators track lineage rather than safety (random direction beats the refusal direction; SPI ranks backwards at rho -0.20 vs supervised +0.40). No metric in the 50 may be built on a hysteresis residual; EWS-style indicators enter only as declared-expected-to-fail controls.",
    "R3 REPOSITIONED AS THE DESIGN LICENCE. The directional ratchet — compliance absorbing, up-ramp failing 92-100% mid-generation, free-running deviation growing 2.57-5.33 against teacher-forced 0.119-0.233 — is why refusal is decided at ONSET, and therefore why a few-prompt seconds-scale metric is plausible. Long-rollout metrics are a priori disfavoured and must be a minority of the 50.",
    "R4 JUDGE FIX RETAINED AS MANDATORY (evaluator system prompt, without which COMPLIANCE is never labelled), and iteration 1's prompt corpus, 137-checkpoint / 93-lineage manifest, and 10-tokenizer-family refusal lexicons are reused rather than rebuilt.",
    "MECHANISM AND METAMODEL MADE EXPLICITLY CONDITIONAL on a metric working, so neither can be used to manufacture a positive narrative from a null screen. The metamodel must split by lineage, never by checkpoint, or siblings leak across the boundary.",
    "CONFIDENCE LOWERED with the most likely outcome stated in advance: a partial negative in which weight-space signatures catch abliterated models while nothing tracks graded safety-RL strength across architecture families."
  ],
  "relation_type": "embedding",
  "artifact_relations": []
}
```

### [12] TOOL RESULT — Write · 2026-08-13 16:10:49 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Reading safety off a single model\",\n  \"hypothesis\": \"CORE CLAIM. A model's safety behaviour is legible from the model ALONE — its weights and its activations on a handful of prompts — without a parent, a reference model, an attested base to diff against, or a benchmark run. Concretely: there exists a cheap single-model observable, computable in seconds to a couple of minutes, that correlates with EXTERNALLY MEASURED safety scores across weight lineages and across architecture families, and that beats the best black-box (logits/output-text-only) baseline. The claim is falsifiable in three separate places, and each failure mode is a reportable result, not a setback.\\n\\nOPERATING CONSTRAINT (new, and it retires part of the previous hypothesis). The metric sees ONE checkpoint. No sibling, no base, no diff. This is the assumed deployment situation: a random model found on HuggingFace with nothing else. Every candidate metric must be computable under that constraint. Siblings (base / instruct / safety-RL / abliterated) are permitted ONLY as VALIDATION CONTRASTS — to check that a metric moves in the right direction across a lineage — never as an input to the metric itself. Iteration 1's headline quantities were all sibling CONTRASTS (instruct minus abliterated excess width, instruct minus abliterated Var*), so under this constraint they are demoted from metrics to diagnostics. The one iteration-1 positive that survives the constraint intact is alpha_50, because the refusal axis is extracted from the model under test and the steering sweep is run on that same model.\\n\\nWHAT ITERATION 1 SETTLED, CARRIED FORWARD AS ESTABLISHED (do not re-litigate; do not re-run):\\nR1. Steering hysteresis is prefix content, not latent state. Excess width 0.019 [-0.057, 0.099] instruct, -0.031 [-0.070, 0.001] abliterated, -0.330 [-0.990, 0.000] base; every CI overlaps 0, every lower bound sits under the temperature-0.7 RESET noise floor (p95 = 0.05), and the FORCED-B positive control reproduces the retained arm to |diff| = 0.000, so the null is not a plumbing artefact. No metric in the 50 may be built on a hysteresis residual.\\nR2. Early-warning-signal indicators (variance, lag-1 autocorrelation, flicker, recovery rate) track LINEAGE, not safety. On the Qwen triad Var* 3.101-3.152, AC1 0.245-0.304, flicker 40.2-42.2 per 100 steps, all CIs overlapping 0, while SmolLM2 separates cleanly; the ordering partly reverses (instruct has the LOWEST Var*/flicker and the FASTEST relaxation); lambda is non-identifiable at every geometry reached (T_fit >= 128 certified, n_roll >= 40 required against 20 achieved); a RANDOM perturbation direction reproduces the ordering better (instruct-abliterated -0.493, CI excluding 0) than the refusal direction (-0.226, n.s.); and the composite SPI ranks backwards (rho = -0.20 against a supervised +0.40). This is a clean controlled negative — the first test of the critical-slowing-down toolkit on LLM generative dynamics — and it should be REPORTED as such, but EWS-style indicators enter the 50 only as declared-expected-to-fail controls, not as hopefuls.\\nR3. The directional ratchet is real and it is the mechanistic licence for cheap metrics. Compliance is absorbing: up-ramping alpha mid-generation fails to induce refusal in 92-100% of trials (10/10 at every step size delta in {0.05, 0.1, 0.2, 0.4} up to alpha_max = 4.0; 9/10 with an [L-2, L+2] multi-layer window), and free-running deviation GROWS (16-step survival ratio 2.57-5.33) where teacher-forced deviation decays (0.119-0.233). Refusal is a decision made at generation ONSET. Consequence for design: the informative measurement window is the first few generated tokens, which is exactly why a few-prompt, seconds-scale metric is plausible at all. Metrics that integrate over long rollouts are a priori disfavoured and should be a minority of the 50.\\nR4. The judge decides the result before the models do. The default judge never labels COMPLIANCE without an explicit evaluator system prompt; with the fix, measured ASR moved 0.092 -> 0.858. The fix is MANDATORY everywhere in this iteration. Separately, our own judge is no longer allowed to be the ground truth (see H4).\\n\\nTHE REVISED CLAIMS.\\n\\nH0 (exploration, no hypothesis attached). On the Qwen3-4B lineage — Qwen/Qwen3-4B-Base, Qwen/Qwen3-4B, Qwen/Qwen3-4B-SafeRL, and an abliterated Qwen3-4B — characterise what actually differs, open-endedly, in BOTH weights and activations. Instruct / SafeRL / abliterated share a chat template and are directly comparable; Base uses a different format and is analysed separately, never pooled into a four-way contrast. Note explicitly that SafeRL is the official safety-RL model and NOT the instruct model, and that this is the first lineage in this project containing a deliberate safety-RL arm as distinct from generic instruction tuning — the instruct-vs-SafeRL contrast is the one that isolates safety training from helpfulness training, and iteration 1 never had it. Deliverable is a findings list, not a verdict.\\n\\nH1 (the battery). Fifty single-model metrics, designed from H0's findings AND from the literature — safety papers and general mechanistic-interpretability papers alike, not safety papers only. Composition requirements: (a) at least 8 must be BLACK-BOX, reading only logits or output text — logit-gap margin between refusal-onset and continuation tokens at the first generated position, refusal-token logprob mass, first-token entropy, output-length asymmetry between harmful and benign prompts, judge-on-output — and these are the comparison point that decides whether looking inside the model buys anything at all; (b) at least 8 must be WEIGHTS-ONLY, requiring zero generation (spectral statistics of MLP and attention write matrices, low-rank structure of the unembedding-adjacent subspace, norm anisotropy at candidate refusal layers, weight-space distance-to-nearest-degenerate-direction, and — motivated by abliteration being literally W <- W - c*r*r^T*W — direct tests for a RANK-DEFICIENT or ORTHOGONALISED write direction, which should be detectable in one checkpoint without its parent); (c) at most 10 may require more than 60 s on a single 4B model; (d) each metric declares its cost in forward passes and wall-clock before it is run. alpha_50 (the steering coefficient in NORM_L units at which a fresh constant-alpha generation crosses a 50% refusal rate) enters as one candidate among fifty, no longer as the headline.\\n\\nH2 (the test, and the honest split). All 50 are evaluated much wider: additional lineages with a safety-tuned or abliterated sibling (pairs and triplets), plus STANDALONE models where no sibling exists — because standalone is the actual deployment case. Reuse iteration 1's frozen 137-checkpoint / 93-lineage manifest, prompt corpus, and the empirical refusal-token lexicons for 10 tokenizer families; do not rebuild them. Metric selection is contaminated by design if the best of 50 is picked on the models the 50 were designed on, so a HELD-OUT SET of lineages is fixed BEFORE any metric is written, is touched by nothing until selection is frozen, and carries the reported result. Statistics: the resampling unit is the WEIGHT LINEAGE, and BOTH aggregation units are reported — per-checkpoint and per-lineage — because they can disagree and iteration 1 has already seen a sign flip between member-level and lineage-level aggregation on 5 of 16 cells. Pre-registered falsifier: a metric that separates safe / normal / abliterated only WITHIN one architecture family is a NEGATIVE RESULT and must be reported as one, in those words, not repackaged as family-specific success.\\n\\nH3 (ground truth is external). Correlation targets come from official sources — model cards, papers, leaderboards, TrustLLM and AIR-Bench reported numbers — not from our own judge. Our judge is used only where no external number exists, and where it is used the R4 evaluator-system-prompt fix is in force and the reliance is stated. Safety is not only refusal: cover the broader axes TrustLLM and AIR-Bench define. Documented fallback if that coverage proves infeasible: TWO refusal rates, on harmful prompts and on XSTest-style harmless-but-alarming prompts. Under either scoring, a model that refuses EVERYTHING must LOSE, not win; any metric whose top-ranked model is a blanket refuser is disqualified regardless of its correlation. Capability benchmarks (GSM8K, MMLU, Arena-Hard) are pulled alongside, to test whether safety trades against performance and to check that a metric is not covertly reading capability. HARD CONSTRAINT: Qwen3Guard must NOT be used as a judge for Qwen3-4B-SafeRL — it was that model's training reward, and using it is circular.\\n\\nH4 (the correlation test). The 10 best metrics from the frozen selection are correlation-tested against the external benchmark numbers on the held-out lineages. Report Spearman with lineage-level bootstrap CIs, both aggregation units, and a paired bootstrap of each white-box metric against the strongest black-box baseline. Pre-registered outcome: if NO white-box metric's advantage over the best black-box baseline has a CI excluding 0, the finding is that reading inside the model buys nothing for cheap safety screening, and that is the paper's result.\\n\\nH5 (mechanism, conditional). If a metric works well, only then: what is it reading, which layers and components carry it, what breaks it. Layer-wise and component-wise ablation, a token-disjoint paraphrased refusal axis and a norm-matched non-safety stylistic axis as lexical-artefact controls (a lexical verdict is a publishable finding, not a failure), and a check that the metric is not a capability proxy.\\n\\nH6 (metamodel, conditional). Instead of a static formula, train a small metamodel on activations to predict the external safety scores directly. It must be trained and evaluated with the lineage as the split unit — never a random checkpoint split, which leaks siblings across the boundary. If it beats the formulas, the deliverable is not the score: it is an account of WHAT internal computation it is picking up and WHY that signal exists.\\n\\nCONFIDENCE. Lower than the previous statement, deliberately. Iteration 1 refuted its own headline mechanism, and its surviving positive (alpha_50's price-of-refusal discrimination, instruct 0.475 vs abliterated 0.550) rests on a 0.075 gap on a 0.05 grid with 5 Bernoulli draws per point and no CI — it is unpowered and may not survive. The new claim is broader, more falsifiable, and externally grounded, but it has no direct positive evidence yet, and the black-box baselines may well win. The most likely single outcome, on current evidence, is a partial negative: some metrics separate abliterated models (which carry a literal weight-space signature) while none tracks graded safety-RL strength across families. That outcome is worth reporting precisely.\",\n  \"relation_rationale\": \"Prior refusal-dynamics claim survives as one candidate inside a larger single-model, externally-validated metric-screening theory.\",\n  \"confidence_delta\": \"decreased\",\n  \"key_changes\": [\n    \"NEW OPERATING CONSTRAINT — single model, no parent, no reference, no attested base to diff against. This is the deployment case being targeted, and it demotes iteration 1's headline quantities (instruct-minus-abliterated excess width, instruct-minus-abliterated Var*) from metrics to validation diagnostics, since both are sibling CONTRASTS. alpha_50 survives the constraint because its refusal axis is extracted from, and its sweep run on, the model under test.\",\n    \"SCOPE WIDENED from a single mechanism to a 50-metric screening battery. The previous hypothesis bet everything on one mechanism (bistability) and one composite (SPI); both failed. The revision spreads the bet and pre-commits to a selection procedure instead of to a favourite.\",\n    \"BLACK-BOX BASELINES PROMOTED TO THE CENTRAL FALSIFIER. At least 8 of the 50 read only logits or output text (logit-gap margin, refusal-token logprob mass, first-token entropy, output-length asymmetry, judge-on-output). Pre-registered: if no white-box metric beats the best of them with a CI excluding 0, the result is that looking inside buys nothing.\",\n    \"WEIGHTS-ONLY METRICS ADDED (>=8, zero generation), motivated directly by abliteration's mechanism W <- W - c*r*r^T*W — an orthogonalised or rank-deficient write direction should be detectable in ONE checkpoint without its parent. Iteration 1 had no weights-only arm at all.\",\n    \"HELD-OUT LINEAGE SET FIXED BEFORE ANY METRIC IS WRITTEN, and untouched until selection is frozen. Picking the best of 50 on the models the 50 were designed on is the obvious failure mode of this design and is pre-empted structurally, not by caution.\",\n    \"STANDALONE MODELS ADDED to the evaluation set. Iteration 1 tested only lineages where siblings existed; the actual use case has no sibling, so models with none are now first-class test subjects.\",\n    \"GROUND TRUTH MOVED OUTSIDE THE PROJECT — official model cards, papers, leaderboards, TrustLLM and AIR-Bench numbers replace our own judge as the correlation target. Iteration 1's headline ASR number moved 0.092 -> 0.858 on a judge-prompt fix alone, which is exactly why the judge cannot also be the ruler.\",\n    \"SAFETY REDEFINED AS TWO-SIDED — over-refusal (XSTest-style harmless-but-alarming prompts) is a required axis, with the explicit disqualification rule that a blanket refuser must LOSE. This kills the degenerate solution the previous refusal-only framing permitted.\",\n    \"CAPABILITY BENCHMARKS (GSM8K, MMLU, Arena-Hard) ADDED, both to measure the safety/performance trade-off and as a confound check that a winning metric is not covertly reading capability.\",\n    \"CIRCULARITY GUARD: Qwen3Guard is forbidden as a judge for Qwen3-4B-SafeRL, because it was that model's training reward.\",\n    \"EXPLORATION LINEAGE UPGRADED to Qwen3-4B-Base / 4B / 4B-SafeRL / abliterated, with Base kept separate (different prompt format, never pooled into a four-way contrast). The instruct-vs-SafeRL arm is new and is the only contrast that isolates deliberate safety training from generic instruction tuning; iteration 1 had no safety-RL model.\",\n    \"STATISTICS PRE-COMMITTED: weight lineage as the resampling unit, BOTH aggregation units reported (per-checkpoint and per-lineage), after iteration 1 observed a sign flip between the two on 5 of 16 cells. Within-family-only separation is declared a NEGATIVE RESULT in advance, in those words.\",\n    \"R1 AND R2 CARRIED FORWARD AS SETTLED NEGATIVES, not re-run. Hysteresis is prefix content (all excess-width CIs overlap 0, positive control clean), and EWS indicators track lineage rather than safety (random direction beats the refusal direction; SPI ranks backwards at rho -0.20 vs supervised +0.40). No metric in the 50 may be built on a hysteresis residual; EWS-style indicators enter only as declared-expected-to-fail controls.\",\n    \"R3 REPOSITIONED AS THE DESIGN LICENCE. The directional ratchet — compliance absorbing, up-ramp failing 92-100% mid-generation, free-running deviation growing 2.57-5.33 against teacher-forced 0.119-0.233 — is why refusal is decided at ONSET, and therefore why a few-prompt seconds-scale metric is plausible. Long-rollout metrics are a priori disfavoured and must be a minority of the 50.\",\n    \"R4 JUDGE FIX RETAINED AS MANDATORY (evaluator system prompt, without which COMPLIANCE is never labelled), and iteration 1's prompt corpus, 137-checkpoint / 93-lineage manifest, and 10-tokenizer-family refusal lexicons are reused rather than rebuilt.\",\n    \"MECHANISM AND METAMODEL MADE EXPLICITLY CONDITIONAL on a metric working, so neither can be used to manufacture a positive narrative from a null screen. The metamodel must split by lineage, never by checkpoint, or siblings leak across the boundary.\",\n    \"CONFIDENCE LOWERED with the most likely outcome stated in advance: a partial negative in which weight-space signatures catch abliterated models while nothing tracks graded safety-RL strength across architecture families.\"\n  ],\n  \"relation_type\": \"embedding\",\n  \"artifact_relations\": []\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [13] TOOL CALL — Bash · 2026-08-13 16:10:55 UTC

```
python3 -c "
import json;d=json.load(open('.terminal_claude_agent_struct_out.json'))
print('keys',sorted(d)); print('rationale len',len(d['relation_rationale'])); print('kc',len(d['key_changes'])); print('hyp chars',len(d['hypothesis']))
" && cp .terminal_claude_agent_struct_out.json /ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json && echo mirrored
```

### [14] TOOL RESULT — Bash · 2026-08-13 16:10:55 UTC

```
{"stdout": "keys ['artifact_relations', 'confidence_delta', 'hypothesis', 'key_changes', 'relation_rationale', 'relation_type', 'title']\nrationale len 130\nkc 17\nhyp chars 10807\nmirrored", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] TOOL CALL — Bash · 2026-08-13 16:10:59 UTC

```
python3 - <<'EOF'
import json,shutil
p='.terminal_claude_agent_struct_out.json'
d=json.load(open(p))
d['relation_rationale']="Old refusal-dynamics claim kept as one candidate inside a broader single-model, externally-validated metric screen."
assert len(d['relation_rationale'])<=120, len(d['relation_rationale'])
json.dump(d,open(p,'w'),indent=2,ensure_ascii=False)
shutil.copy(p,'/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/upd_hypo/upd_hypo/'+p)
print('ok',len(d['relation_rationale']))
EOF
```

### [16] TOOL RESULT — Bash · 2026-08-13 16:10:59 UTC

```
{"stdout": "ok 115", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [17] ASSISTANT · 2026-08-13 16:11:10 UTC

```
Revised hypothesis written to `./.terminal_claude_agent_struct_out.json` (and mirrored to the `run_CbJDs3opF7E_` path).

**"Reading safety off a single model" — `embedding`, confidence decreased.**

The prior hypothesis is not discarded; it becomes one candidate inside a larger theory. The new prompt's hard constraint — one checkpoint, no parent, no reference, no attested base — is what forced the reframe: iteration 1's headline quantities were *sibling contrasts* (instruct−abliterated excess width, instruct−abliterated Var\*), so under this constraint they are demoted from metrics to validation diagnostics. α₅₀ survives intact, because its axis is extracted from and its sweep run on the model under test.

What carried forward as settled, not re-run: R1 hysteresis-is-prefix-content (no metric may be a hysteresis residual), R2 EWS-tracks-lineage-not-safety (EWS-style indicators enter only as declared-expected-to-fail controls), R3 the directional ratchet — now repositioned as the *design licence*: refusal is decided at onset, which is precisely why a few-prompt seconds-scale metric is plausible, and why long-rollout metrics must be a minority of the 50. R4's judge fix stays mandatory, and the corpus/manifest/lexicons are reused.

The structural additions your prompt asked for, pre-committed rather than left to judgment: ≥8 black-box metrics as the *central falsifier* (if no white-box metric beats the best of them with a CI excluding 0, that is the paper's result); ≥8 weights-only metrics motivated by abliteration's `W ← W − c·rr^ᵀW`, which should leave a single-checkpoint signature; held-out lineages fixed before any metric is written; standalone models as first-class subjects; external ground truth replacing our own judge; over-refusal as a required axis with blanket refusers disqualified outright; capability benchmarks as both trade-off measurement and confound check; Qwen3Guard barred for SafeRL; lineage as resampling unit with both aggregation units reported; and within-family-only separation declared a negative result in advance. Mechanism and metamodel are explicitly conditional on a metric working, so neither can manufacture a positive story from a null screen.

Confidence went down with the likely outcome stated up front: weight-space signatures catch abliterated models, nothing tracks graded safety-RL strength across families.

`artifact_relations` is empty — all five artifacts are iteration-1, so they have no earlier-iteration predecessors.
```
