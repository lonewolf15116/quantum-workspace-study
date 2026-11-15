# P002-AUDIT-001 — Bounded failure-mode audit

Date: 2026-11-15. Exploratory / not confirmatory. No new workspace contrast.

## Motivation and verified scope

GNN K at 7,680 updates plateaus near MAE 0.19 on the training panel for 12, 24 and 40 message-passing rounds, while the analytic fixed-template product-state positive control succeeded. This does NOT establish a mathematical representation bound. Optimisation, weak gradients, data distribution, information loss, and query readout are unresolved.

The objective here is to **test elementary fitting and signal content without another full workload training or depth sweep**.

## Audit 1 — Frozen label distribution

Run `scripts/audit_p002_labels.py` on the exact existing P002 dataset. It selects the K training pool: 30 templates × 4 train angles × 63 cells = 7,560 examples, 7,560 separate within-template examples, and 504 held-out-template examples. Verify source hashes. Report the number of label scalars, mean absolute target (literal-zero predictor), tail proportions |y| > .3, .5, .7, the Z/ZZ breakdown, and constant mean/median baselines fitted **only to training labels**, independently for each n and observable index.

Important: the current training objective is masked **MSE**, reported generalisation metric **MAE**. A small mean |label| alone does not prove a stationary/trivial MSE optimum. Distinguish training-derived mean and median from literal-zero baselines. Keep panel-specific baselines distinct.

## Audit 2 — Small entangled overfit

Run `scripts/check_p002_entangled_overfit.py`: frozen 64 examples from n=4, r=2, path; 16 independently sampled templates × 4 training angles, with their separate 64 within-template fresh-angle examples for context. Train the **unchanged GateDAG** with 12 rounds, seed 202, AdamW LR .001, weight decay .01, batch 32, squared-error loss and gradient clip 1, fixed 1,500 updates. Log at steps 0,100,...,1500; final TRAIN MAE is primary. Log train/within Z and ZZ diagnostics and panel-specific zero baselines. Source and dataset hashes in identity. Run with separate output directory. The small test is NOT used to select a paper checkpoint or to claim cross-template generalisation.

Decision interpretation (diagnostic, not scientific significance):
- Train MAE near zero (e.g. below 0.01) => basic ability to memorise a restricted entangled subset under this regime; says nothing by itself about cross-template generalisation.
- Train MAE remains near zero predictor => failure to fit **this particular** entangled subset with this architecture/optimizer/seed. Not enough to prove representational incapacity; check label amplitude, per-observable errors and gradients before a fix.
- Strong fitting but poor fresh-angle performance => memorisation vs interpolation distinction on the fixed template sample.

## Follow-up gate

Do not modify model, add sample weighting or curriculum, or infer optimality until both audits return. A single deterministic run is not replication. Evaluate observable-specific high-|label| errors; use the recorded per-step gradient norms as a first screening diagnostic. Only run targeted mechanistic follow-ups after findings are inspected. No paper or workspace contrast is authorised on these diagnostics alone.
