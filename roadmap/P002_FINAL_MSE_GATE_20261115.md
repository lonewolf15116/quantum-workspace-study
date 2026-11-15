# P002 final read-only MSE gate — stopping protocol

**Date:** 2026-11-15

Full-workload D12/D24/D40, data-scale, exposure and product-state tests completed. Bounded entangled audit was partially successful on training (MAE 0.17188 vs zero 0.40207) and unsuccessful at fresh-angle interpolation (0.42541 vs zero 0.41451). Frozen Arm K scalar labels: E|y|=0.168849, std(y)=0.287566, approximately 44.9% |y|<0.05; fitted constant mean/median under MAE are no better than zero on evaluation panels. These are **descriptive observations**, not identification of an MSE learning trap.

**One remaining task** is `scripts/audit_p002_mse_readonly.py`. It calculates exact data-only zero and train-fitted per-n/query mean-constant MSE across all Arm K train/within/held-out instances, with equal instance weighting exactly matching `run_p002_graph_baseline.py`'s objective. It reports the last 512 archived training-step minibatch MSE values for each K7680 depth run. It **does not** reconstruct exact final-model full-panel MSE, because `run_p002_graph_baseline.py` saved training logs but no trained model checkpoint. The model loss in `steps.jsonl` was recorded BEFORE each update.

### Decision constraints

- MSE mean-constant baseline is the optimum within the per-n-and-observable, input-independent prediction class on the training data; it is **not** the optimal prediction function of circuit inputs.
- A model minibatch MSE near the full-panel constant MSE is supporting descriptive evidence for poor effective input-dependent fit, not proof of a stationary point or gradient starvation.
- A model minibatch MSE materially below the constant MSE while MAE remains near or above zero can indicate useful squared-error signal even when MAE does not improve. This would **not** justify switching the primary metric post hoc to MSE or calling the original MAE question positive.
- A model minibatch MSE above the constant requires an implementation/optimisation caveat; not a proven bug.
- No retraining, no additional architecture sweep, no workspace contrast, no confirmatory paper claims.

**Stop rule:** after read-only MSE accounting and discrepancy review, freeze the bounded negative-result evidence. A manuscript may describe task-signal concentration, constant-predictor competitiveness and evaluated architecture failures, but not 'unlearnable', 'no architecture can overcome', 'signal concentration caused failure', or 'receptive field ruled out universally'. Verify literature novelty and venue fit separately before asserting publishability. The workspace question remains UNTESTED / HOLD.
