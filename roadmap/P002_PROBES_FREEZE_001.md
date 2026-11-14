# P002-PROBES-FREEZE-001 — two exploratory corrective probes

Date: 2026-11-15. Status: **implementation and diagnostic decision rules frozen for local execution; not confirmatory registration**.
Source: unchanged original P001, D001, D002 ZIPs recorded in `SHA256SUMS`.
Training source: `scripts/run_p002_probes.py` imports `scripts/bench_archived_model_d128.py`, which reads the exact archived P001 `model_from_p001.py`, changing exactly four checked dimensional literals. Source and post-substitution SHA-256 are recorded at runtime. It is *not* the frozen normative confirmatory implementation, and this is a new architecture-sized engineering diagnostic, not a P001 replication.

## Eligibility before running on RTX 5050
- Run `python scripts/reassemble_evidence.py`; all five archive digests must pass.
- Run `python scripts/bench_archived_model_d128.py --device cuda --steps 10` from repository root. It uses actual archived n=10/r=6 circuit tensors, labels, embedding/position/role construction, workspace insertion, query gathering and instance-averaged observable MSE, with W=0 and W=4 in turn. This is the archived implementation with changed width/depth/FFN/gather dimensions. It logs stage-wise absolute allocated peaks, reserved peak, parameters, and steady step time; it is not a validation of AC-002 FLOPs or a normative model implementation.
- G2c planning gate PASS if W=0/W=4 both finish ten steps with finite loss, allocated peak < 6656 MiB, reserved peak < 7372.8 MiB, no OOM, parameter difference +512. Otherwise HOLD for documented scope decision.
- No direct ChatGPT control of the laptop is available; only a user-run local CUDA benchmark can clear the laptop hardware gate. CI CPU smoke proves code executes, not GPU fitness.

## Fixed probes
**Long-training dynamics (P002-L):**
- Model W=0, d128/L4/FFN512, same archived token construction and P=179; archived 1008 training examples and 504 distinct-template validation examples.
- Seed 101, AdamW lr .001 weight decay .01, effective batch at most 32, clip norm 1, float32, 1920 optimiser updates (5 times P001's 384), no early stopping.
- Shuffle with NumPy default_rng(101) per permutation cycle. Record every optimisation step's MSE, global gradient norm and sample count; evaluate after step 0 and every 64 updates, including final step.
- Fixed P001 validation panels are previously inspected/used; therefore results are exploratory, not new sealed test outcomes. Evaluation is MAE against zero on full train and validation, plus prediction/label Pearson, sign accuracy for |y|>0.1, high-signal instance MAE for max_j |y_j|>0.3, output range/variance. Separate single-Z/ZZ diagnostics may be added with a dated amendment; they are not currently reported by this executable.

**Highest-training-variance cell (P002-V):**
- Select exactly one of 63 (n,rounds,family) cells by the highest *training-only* mean across observables of population variance of labels, with lexicographic cell tie-break; preserve full ranking. This uses 16 training-angle instances from 4 templates, not validation outcomes.
- Train independent W=0 d128/L4/FFN512 model, seed 101, same optimisation conventions, 384 updates with batch up to 32, gradient norm clipping, no early stopping. Evaluate at steps 0, 64, ..., 384 on both the training examples and the original separate two-template/eight-instance validation panel for that cell.
- The cell is chosen for difficulty/signal before any new training; no representative generalisation claim can be made from its outcomes.

## Decision and reporting
- These probes diagnose optimisation time and cell-specific learnability. A model beating zero on training but not held-out templates motivates template-generalisation analysis. Beating zero on held-out templates is encouraging but not a confirmation of any workspace benefit. Failure on both motivates a scientific review, not an impossibility claim or automatic publication pivot.
- Keep P001 archives intact. Results stay in untracked `p002_local_results/` until checked for source identity, nonfinite values, counts, and failure completeness. No automatic Git push, outcome suppression, cherry-picking or confirmatory claim.
- Four-arm dataset-scale P002 is not yet execution-ready. Its older document `roadmap/P002_corrective_learning_diagnostic.md` remains a roadmap, not an approved freeze.
- The exact on-device G2c result must exist before a gated run of probes. A synthetic encoder-only prior GPU test does not satisfy G2c.
