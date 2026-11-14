# P002-DATA-001 — Four-arm template/angle generalisation experiment (candidate execution contract)

Date: 2026-11-15. Status: **candidate; validation required before training**. This is exploratory, post-P001, not preregistered confirmation and not a workspace efficacy test.

## Prior evidence and correction
P002-L (1920 updates): training MAE 0.082593, held-out-template MAE 0.249351 vs zero 0.186746. P002-V selected n=6, rounds=2, path from training-label variance; 384 updates: training MAE 0.0000610, held-out MAE 0.506893 vs zero 0.293365. Both are one-seed exploratory diagnostics on previously inspected P001 data. Direct local result logs have not yet been deposited in the repository. The next experiment changes data availability, not the task distribution, and uses W=0 only.

## Fixed candidate arms
| Arm | Training templates per workload cell K | Training angles per template A | Optimiser updates | Interpretation |
|---|---:|---:|---:|---|
| B | 6 | 4 | 384 | fresh-data baseline |
| A | 6 | 20 | 384 | increased within-template angles |
| K | 30 | 4 | 384 | increased template diversity |
| L | 6 | 4 | 1920 | longer training at baseline data size |

There are 63 cells: n=4,...,10, rounds=2/4/6, families path/ring/all_to_all. Each cell also has 2 held-out templates, four held-out angles per template; all arms see an **identical** held-out-template panel. For each of the 30 training templates in every cell, generate 20 training angles and 4 additional, never-trained evaluation angles; all arms use the same within-template panel for the six shared training templates. Use nested template/angle prefixes, never generate separate datasets per arm. Total unique full-design topology templates = 63*(30+2)=2016. No template from evaluation may appear in training.

## Source and labeling
Reuse the exact P001 n/r/family gate-generation conventions and the archived P001 exact state-vector simulator with its complex128 labels; preserve qubit/gate budget and label query ordering. Dataset generation is new and fully separate from P001's seed streams. Record source digest, Python/NumPy/PyTorch versions, RNG states, collision counts, cardinalities and manifest hash. The dataset generator must demonstrate deterministic replay, split uniqueness and strict nesting in a small CI smoke test before any full dataset generation.

## Frozen candidate training conventions
Archived P001 Model/pack, with four checked dimension substitutions d=128, L=4, FFN=512 and gather-width=128 (W=0 only). This remains a **dimension-substituted archived pilot**, not normative AC-002 source equivalence. AdamW lr=0.001, weight_decay=0.01, clip norm 1, float32, batch 32, no early stopping. Training seeds 101, 202, 303; common fixed optimiser-update budgets, recorded individual steps. Per arm, record samples processed, per-step MSE and gradient norm. Use a deterministic repeated shuffled-instance stream, not equal epoch count. No tuning on the shared hold-out panel.

## Evaluation contract
At step 0 and every 64 updates, including terminal step, report training MAE, fresh angles on seen training templates, and unseen-template MAE; each against its appropriate zero baseline. Additionally: output/label Pearson (with undefined null explicitly), output standard deviation and range, |label|>0.1 sign accuracy, max_j|label_j|>0.3 high-signal subset MAE with zero reference, per-n and per-cell MAE, separate Z and ZZ MAE, all with exact denominators. Within-template panel is limited to templates **actually used by the arm**; held-out-template panel identical across all arms. Numerical failures or missing results remain visible.

## Decision boundaries
No change to WORKLOAD-002 or the primary comparison. No workspace-effect claim. Improvement on seen templates alone means only interpolation/memorisation; held-out improvement over zero on identical template panels is exploratory evidence of template generalisation. Failure motivates a scientific review; do not assert unlearnability or automatic publication. No significance from choosing minimum across arms/seeds. A later independent test and reviewed analysis design are required.

## Gates
G0: verify original five archive hashes; source-identity checks and successful G2c laptop CUDA check already reported by user, but local run artifacts should be preserved.
G1: code preflight and deterministic dataset/split audit.
G2: independent protocol/code review and full manifest generation with zero split leakage.
G3: run four arms and three predeclared seeds on RTX 5050; archive all outcomes including failures. Stop any failing arm rather than retuning it silently.
No confirmatory workspace experiment is authorised by this document.
