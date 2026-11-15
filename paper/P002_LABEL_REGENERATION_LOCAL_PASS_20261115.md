# P002 — archived simulator/source and sampled-label check PASSED

**Date:** 2026-11-15  
**Script:** `scripts/check_p002_dependencies_and_labels.py`  
**Local report:** `p002_dependency_label_audit.json` (not yet deposited in GitHub)

## User-reported execution

- Status: **PASS**
- Sampled instance checks: **12**
- Bitwise-equal float64 label vectors: **12**
- Maximum absolute label difference: **0.0**
- Error count: **0**
- Exit code: **0**

The script checks frozen dataset file SHA-256 hashes, P002 generator SHA-256 against the frozen manifest, and the source SHA-256 of the NumPy `simulate` function extracted from `evidence/Workspace_Study_Pilot_P001.zip:run_pilot.py` against that same manifest. PASS indicates those checks did not raise errors. The script recomputes labels from archived gate templates/angles for its selected train, within, and holdout instances, spanning n=4,7,10 when present.

**Evidence level:** researcher-provided PowerShell stdout; the full JSON report has not been inspected via this GitHub record. Twelve spot checks do **not** demonstrate full 45,864-instance regeneration, reproducible GPU training, or complete run-source identity. Dataset generation uses an archived custom NumPy simulator, not CUDA-Q or Qiskit.

## Related gates

- Local manuscript verifier `PASS_COMPLETE`, 24 checked items, 0 missing, 0 errors; D12 legacy identity caveat preserved.
- v2 local ZIP manifest: 97 member files; all matched stored SHA-256; transformer 61 files, product-state 4 files, missing 0. v2 itself not yet public.
- Source dependency inventory: `paper/P002_DEPENDENCY_REPRODUCIBILITY_GATE_20261115.md`.

**Decision:** Close the bounded simulator source/12-label regeneration gate. Keep public reproducibility and independent scientific review OPEN. No public release or arXiv submission has occurred.
