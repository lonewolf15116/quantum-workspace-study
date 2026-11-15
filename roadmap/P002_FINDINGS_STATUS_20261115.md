# P002 research status — 2026-11-15

**Study:** Dedicated Workspace in Transformers for Quantum-Circuit Observable Prediction

**Status:** Pre-confirmatory. **Workspace contrast ON HOLD**. No confirmatory workspace-effect experiment has occurred.

## Original question

Does replacing four reserved masked-padding positions with learned non-input workspace tokens improve template-averaged Z/ZZ observable MAE, at shared encoder length 179, with compute/parameter matching? WORKLOAD-002 admits same-backbone d=128 L=4 W=0/W=4 comparison under 1% resource tolerance. This establishes resource feasibility, **not** predictive validity or workspace benefit.

## Positive control

An unchanged 12-round GateDAG learned analytic product-state predictions on independent test angles, final MAE **0.007755** vs literal-zero predictor **0.514811** (98.5% lower). Z MAE 0.006748 vs zero 0.650305; ZZ MAE 0.008426 vs zero 0.424482. This supports functionality on that restricted task, **not** full entangled-workload correctness.

## Full-workload negatives

The P002 transformer B/A/K/L 3-seed diagnostic did not beat literal zero on held-out templates at evaluated checkpoints. Best observed held-out MAE 0.19446 vs zero 0.193399. These comparisons are exploratory and not a confirmatory workspace result.

GNN Arm L (1,512 examples, 1,920 steps) ended at training MAE 0.12198, within MAE 0.22631 vs zero 0.19291, held-out MAE 0.23359 vs zero 0.19340: severe train/eval divergence.

GNN Arm K (7,560 examples) endpoints:

| Depth | Updates | Parameters | Train MAE | Held-out MAE |
|---|---:|---:|---:|---:|
| 12 | 1,920 | 823,809 | 0.190717 | 0.193497 |
| 12 | 7,680 | 823,809 | 0.190476 | 0.193707 |
| 24 | 7,680 | 1,604,865 | 0.191281 | 0.194118 |
| 40 | 7,680 | 2,646,273 | 0.191269 | 0.194155 |

Held-out literal-zero MAE 0.193399; Arm K within-template literal-zero MAE 0.189912. No meaningful held-out gain at endpoint.

Dependency-path audit: 2,016 templates; median longest directed gate path 19 vertices, p90 30, maximum 40; 1,389 (68.9%) exceed 12. A larger message-passing receptive field was justified to test but **depth 24/40 did not improve training fit under tested optimisation**. This is evidence against a simple depth-only rescue, not a mathematical impossibility theorem or proof that receptive field cannot matter under a different implementation.

CUDA depth 40 smoke: 10 training steps passed at batch 32, peak reserved ~954 MiB on RTX 5050 8GB. Hardware memory was not the obstacle for these configurations.

## Pending mechanism audit — do not pre-judge

- `scripts/check_p002_entangled_overfit.py`: 64 real entangled examples, fixed 12-round GateDAG, final train MAE primary, Z/ZZ and within-template diagnostics.
- `scripts/audit_p002_labels.py`: panel-specific signal distribution, `E|y|`, fractions `|y|>0.3/0.5/0.7`, Z/ZZ distributions, plus training-derived mean/median constant predictor.
- See `roadmap/P002_AUDIT_001_BOUNDED.md`. Both scripts smoke-tested on GitHub Actions, **not yet executed on full P002 data** as of this note.

### Scientific interpretation constraints

- A training-MAE plateau near 0.19 does **not** by itself prove an architectural representational limit; optimiser, MSE loss dynamics, graph information use, and readout remain open.
- The learning objective is MSE while reported endpoint is MAE; literal-zero MAE is not the same as a training-derived mean/median constant baseline. A small `E|y|` does not demonstrate that zero is a local MSE optimum.
- Training-set overfit on 64 entangled samples would show restricted memorisation, **not** full-workload generalisation. Failure on 64 samples also does not mathematically prove non-representability.
- Data/exposure/depth interventions were insufficient *at the tested configurations*, not universally ruled out.
- No paper drafted and no workspace contrast authorised. Audit findings should drive at most one bounded targeted corrective hypothesis before reassessment.

**Source record:** user-provided “P002 Findings Note — Consolidated Research Record” (2026-11-15); this project note retains numeric findings and qualifies stronger causal claims pending the audit.
