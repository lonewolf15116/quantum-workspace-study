# P002 — Exact dependency chain and bounded label-regeneration gate

**Date:** 2026-11-15  
**Current publication state:** Local v2 archive passed 97-file manifest check; not public. This file documents what remains and introduces a no-training diagnostic. **No label-regeneration result is claimed until the researcher executes the script.**

## Source-level discovery

Review of the committed scripts established these exact chains:

1. **Dataset labels:** `scripts/generate_p002_data.py` reads `evidence/Workspace_Study_Pilot_P001.zip`, extracts the single `simulate(n, gates, angles)` function from `run_pilot.py`, and compiles it with `numpy` as the numerical dependency. This is an archived **custom NumPy state-vector simulator**; it does not call CUDA-Q or Qiskit to generate P002 labels. The generator records `generator_sha256` and `source_sha256` in `p002_dataset/manifest.json` together with exact NumPy and Python versions, the PCG64 seeds and RNG states, and content SHA-256 for `instances.json` and `templates.json`.
2. **Transformer:** `scripts/run_p002_arms.py` imports `scripts/bench_archived_model_d128.py` and `scripts/run_p002_probes.py`. The benchmark dynamically extracts a P001 archived Transformer from `evidence/Workspace_Study_P001_Diagnostics_D002.zip` and substitutes declared dimensions. Include the archive and the entire import chain before claiming transformer training source availability.
3. **GNN:** `scripts/run_p002_graph_baseline.py` imports NumPy/PyTorch and contains its own GateDAG graph encoding and training/evaluation code. The analytic product-state experiment `scripts/check_p002_product_state.py` imports GateDAG and helpers from this module.
4. **Audit:** `scripts/audit_p002_labels.py`, `scripts/audit_p002_mse_readonly.py`, `scripts/check_p002_entangled_overfit.py` and `scripts/verify_p002_paper_evidence.py` are separate audit dependencies. The existing v2 manifest already contains several of them, but **its source/dependency closure is not yet claimed**.

## New read-only check

`scripts/check_p002_dependencies_and_labels.py` verifies:

- SHA-256 of frozen dataset files vs its own manifest;
- current generator source SHA-256 vs the manifest's `generator_sha256`;
- archived P001 `run_pilot.py` SHA-256 vs manifest's `source_sha256`;
- recomputed observable labels for a fixed selection of at least nine stored dataset rows across train, within and held-out panels and n=4,7,10, comparing with tolerance 1e-10;
- environment metadata: Python, OS/architecture, NumPy and installed torch/quantum-related package versions.

A passing sample check supports reuse of exactly the archived simulator function and confirms agreement on sampled labels. It **does not** prove all 45,864 rows regenerate, independently reproduce training or identify the exact Git source revision behind every run.

## Run command (no retraining)

```powershell
git pull --ff-only
$python = "..\.venv\Scripts\python.exe"
& $python -m py_compile scripts\check_p002_dependencies_and_labels.py
& $python scripts\check_p002_dependencies_and_labels.py `
    --root . `
    --samples 12 `
    --atol 1e-10 `
    --out p002_dependency_label_audit.json
Write-Host "Exit code: $LASTEXITCODE"
```

Run from the repository root with the **same Python environment** as data generation where possible. The P001 archive should already be present from source generation, but if it is absent and only split `.partXX` files remain, use the verified reassembly procedure; do not modify or regenerate P002 labels.

## Remaining v3 reproducibility packaging requirements

Before calling an eventual public archive independently regenerable, include, with SHA-256 hashes, the complete code dependency chain:

- `scripts/run_p002_arms.py`, `scripts/run_p002_probes.py`, `scripts/bench_archived_model_d128.py`, `scripts/check_p002_product_state.py`, `scripts/check_p002_dependencies_and_labels.py`;
- `evidence/Workspace_Study_Pilot_P001.zip` and `evidence/Workspace_Study_P001_Diagnostics_D002.zip` (or their explicitly verified reassembled equivalents);
- `SHA256SUMS`, environment metadata and complete training identities;
- the frozen P002 dataset and all model diagnostics already selected in the local v2 archive.

The P001 archives may contain additional material not needed for P002. Inspect licences, author permissions and data contents **before making a public package**; do not automatically upload the entire research repository or private archives.

**Current gate:** v2 internal integrity PASS; generator source-to-manifest and sampled label regeneration **PENDING**; complete training reproduction **NOT CLAIMED**. No public release or arXiv submission authorised.
