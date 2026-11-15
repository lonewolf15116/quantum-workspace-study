# P002 — Final read-only MSE audit results and experimental stop

**Recorded:** 2026-11-15  
**Protocol:** P002-MSE-READONLY-001  
**Status:** Completed locally; results transcribed from researcher-provided console output. The full local output JSON has **not** been independently fetched or rerun in this commit.  
**Scope:** Arm K, seed 202, 7,560 training instances, 7,560 within-template instances, 504 held-out-template instances. Existing GNN runs at 12/24/40 message-passing rounds, 7,680 steps. No additional training or workspace comparison.

## Constant-predictor MSE under actual per-instance masked MSE definition

| Panel | Literal zero MSE | Training-derived per-n/per-query mean MSE | Mean/zero |
|---|---:|---:|---:|
| Training | 0.095368639301 | 0.095235721498 | 0.9986062735 |
| Within-template | 0.094945839311 | 0.094957721950 | 1.0001251518 |
| Held-out-template | 0.097297121055 | 0.097275549251 | 0.9997782894 |

Mean-constant training improvement vs literal zero: 0.0001329178 (0.1394%). Other panel differences are smaller. Per-n/per-observable means are fit exclusively using the K training panel.

## Existing stochastic training-loss logs, last 512 updates

| Depth | Mean minibatch MSE | SD across minibatches | Final logged minibatch MSE | Mean unclipped pre-clip gradient norm |
|---|---:|---:|---:|---:|
| 12 | 0.094991724123 | 0.019412683030 | 0.106974475086 | 0.025127474457 |
| 24 | 0.095266484605 | 0.019450384202 | 0.107036933303 | 0.022150919180 |
| 40 | 0.095261335831 | 0.019455098393 | 0.106899559498 | 0.022354082999 |

Step window is 7,169–7,680 inclusive for each run; `steps.jsonl` contains 7,680 rows per run. The instantaneous final logged minibatch MSE is **not** the final model's whole-training-set loss. The 512-step averages are online predictions over changing models and stochastic mini-batches, not matched full-dataset evaluations. The per-minibatch SD is not a confidence interval on any GNN-vs-constant difference.

## Findings

1. Zero and train-fitted constant means are extremely competitive **among constant, input-independent predictors** on the frozen Arm K dataset under MSE, as earlier shown under MAE.
2. The online 512-step training losses for D12, D24 and D40 are numerically near the corresponding training-set constant baselines, without a meaningful depth-dependent improvement trend. D12's mean stochastic training loss is about 0.000377 below the training zero-MSE reference, but the unmatched evaluation protocols prohibit a definitive final-model performance claim.
3. The label distribution and weak learning evidence do not establish a causal 'signal starvation' mechanism, flat gradient, architecture-intrinsic impossibility, or global benchmark unlearnability.
4. Existing positive control (analytic product state) and restricted entangled-set partial fit remain as recorded in `P002_AUDIT_001_RESULTS_20261115.md`.

## Stopping decision

**Stop architecture, scaling and depth experiments on this frozen workload.** Preserve evidence and begin drafting a bounded descriptive negative-result preprint, contingent on checking source artifacts, literature novelty, and coauthor review. A defensible title candidate is *When Zero Is Competitive: A Bounded Evaluation of Neural Quantum-Circuit Observable Surrogates*. Do not claim that either MAE or MSE is statistically indistinguishable from zero without matched full-panel predictions and uncertainty analysis.

The original dedicated-workspace contrast remains **UNTESTED and ON HOLD**. No workspace effect can be inferred.

### Local evidence references

- `p002_mse_final_readonly_audit.json` (machine-generated local full audit)
- `p002_graph_K7680_s202/steps.jsonl`
- `p002_graph_K7680_D24_s202/steps.jsonl`
- `p002_graph_K7680_D40_s202/steps.jsonl`
- `p002_dataset/{manifest.json,templates.json,instances.json}`

These local files are referenced, not asserted to be committed into the GitHub repository.
