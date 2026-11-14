# P002 — Corrective learning diagnostic (PROPOSAL; not a scientific freeze)

Date: 2026-11-14
Status: proposed, not executed; no new training evidence
Predecessors: immutable P001, D001, D002 in `evidence/`.
Primary intent: determine whether P001's main-task failure responds to more angle instances per training template, more distinct training templates, or merely more optimisation steps. Suspend any workspace-effect claim and use W=0 only.

## Observed basis (read directly from verified evidence archives)
- P001 validation zero MAE 0.18674571; W=0 average 0.19177204; W=4 average 0.19079900. Three seeds, six CPU runs. All models also failed zero on final training MAE.
- D001 W=0 small-sample overfit MAE 0.000707098. Simple H-RZ(theta)-H angle interpolation task: final all-query MAE 0.004992987, Z0 MAE 0.008901803. These are narrow learning checks, not validation of unseen circuit templates.
- D001 main-task output/label Pearson 0.0051–0.0214; P001 training produces near-zero outputs.
- D002 re-evaluated saved checkpoints, reproducing validation predictions within <2e-7. Final W=0 training MAE 0.192701–0.194094 (zero 0.189457), validation MAE 0.190837–0.192332 (zero 0.186746). No saved per-step learning curves are available, only epoch-level online MSE.
- D002 hardware gate: CUDA unavailable in its execution environment, GPU-fit not measured. Do not infer laptop GPU capacity from these results.
- Original P001 has 63 workload cells, 6 templates per cell (4 training, 2 validation), 4 angle instances per template, 378 templates, 1,512 instances. W=0 pilot uses width 64 / 3 layers / 4 heads / FFN 128 / P=179, AdamW LR .001, batch 32, 12 epochs.

## Gate G0 — Hardware and source identity
Before larger experiments, use the archived `pilot_diagnostics_d002/gpu_check.py` on the intended CUDA-equipped machine with a CUDA-enabled PyTorch installation. Record device name, software versions, actual free/total VRAM, allocated/reserved peak memory and five complete synthetic training step times for W=0 and W=4 at batch 32/P=179. If CUDA is unavailable, explicitly log a CPU fallback decision; do not claim GPU fit. Keep the P001/diagnostics original ZIPs unchanged and record their SHA256SUMS entries, source hashes, new code digest and environment.

## Gate G1 — Pre-run matrix freeze (must precede training)
Use a single W=0 architecture first. The working candidate factors are:
- A: angle instances **per training template**; nested levels 4 and 20.
- K: **training templates per cell**; nested levels 4 and 8.
- This 2x2 diagnostic design is a proposal, not a frozen experimental plan. Specify the exact new random streams, complete train/within-template/held-out-template allocations, deduplication, resource budgets, and fixed optimiser-step count *before* running any arm.
- Each arm must use the *same independently generated held-out-template panel*. In addition, reserve fresh angles on the training templates as a within-template evaluation panel, strictly disjoint from training angles. No template leakage into held-out-template evaluation.
- Keep a common nested training-template pool, nested per-template training-angle pool and common training permutations/seeds where feasible. Disclose the differences from P001; never relabel this a P001 replication.
- Compare at a fixed optimiser-update budget, not equal epochs, because increasing A or K changes instances/batches/updates per epoch. Record each optimisation-step loss and checkpoint metrics; consider an explicitly logged secondary compute/effective-data comparison.
- Do not filter examples by target magnitude or alter the declared WORKLOAD-002 task distribution to force a positive workspace result.

## Measurements and decision logic
Report, separately per arm and seed: train MAE, fresh-angle-on-seen-template MAE, unseen-template MAE, corresponding zero and training-only constant baselines, output/label Pearson correlation, prediction variance and range, single-Z and ZZ MAE, per-n and per-cell summaries, checkpoint trajectory, update count, total samples seen, CPU/GPU runtime and peak memory. Training-only constant predictors must not use evaluation labels.

Interpretation:
- Seen-template performance improves but unseen-template does not: evidence for limited template generalisation, not yet workspace value.
- More angles help at fixed template count: training-angle coverage may be limiting.
- More distinct templates help at fixed angles: template diversity may be limiting.
- Neither helps: further task-specific architecture/optimisation or representation audit is indicated; does not prove the task unlearnable.
- Any W=0 gain relative to zero is **exploratory** and requires independent repetition before a workspace experiment. Do not use a post-hoc favourable arm to claim confirmatory success.

## No-go and evidence control
No P002 training, no confirmatory run, no new workspace-effect comparison and no GPU-fit claim are authorised by this document alone. The hardware result and exact run matrix must be frozen and reviewed first. Preserve original evidence and failure logs, report all planned runs and failures, and record amendments. Any final scientific comparison must still satisfy Steps 03–05, independent novelty review and coverage validation. 
