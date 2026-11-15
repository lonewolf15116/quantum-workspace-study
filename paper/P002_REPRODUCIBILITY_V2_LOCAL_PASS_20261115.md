# P002 — Expanded reproducibility archive v2: local integrity PASS

**Date:** 2026-11-15  
**Archive:** `p002_reproducibility_v2.zip`  
**Local build:** `scripts/package_p002_reproducibility.py --include-dataset`, using explicit `--extra-file` arguments for transformer and product-state results.

## Researcher-reported ZIP verification

- `zipfile.testzip()`: PASS
- SHA-256 comparison of every ZIP member against embedded `PACKAGE_SHA256_MANIFEST.json`: PASS
- Total manifest files: **97**
- Missing files: **0**
- `p002_arms_results/` files included: **61**
- `p002_product_state_s202/` files included: **4**
- Full P002 dataset: selected by packaging command; v2 verification excerpt does not separately display the value, but the v1 manifest included it and v2 uses `--include-dataset`.

**Evidence provenance:** all figures above transcribed from the researcher's local PowerShell verification. The ZIP bytes and v2 embedded SHA-256 inventory were **not uploaded or independently inspected here**. The v2 archive-level SHA-256 has not yet been recorded.

### Gate disposition

**PASS** for *local v2 archive internal integrity and manifest coverage*.

**Not yet established:** complete rerun dependency closure (including archived P001 simulator source and dependency versions); independent reproduction; source-to-run binding; externally available artifact release; author-approved public accessibility; independent second-reader manuscript review.

**Publication rule:** Do not claim 'fully independently reproducible from a public archive' until dependency-closure inspection and actual public release are completed. The repository is private at the last recorded access check. No publication or repository visibility change has been authorised.

## Next read-only checks

1. Review the v2 archive file list and identify runtime dependencies referenced by the P002 data generator (including `evidence/Workspace_Study_Pilot_P001.zip`).
2. Record the complete v2 ZIP SHA-256, and make sure the local manifest includes `p002_dataset/{manifest,templates,instances}.json`.
3. Compare `p002_arms_results` and `p002_product_state_s202` filenames to the manuscript's experiment inventory and identify any additional scripts or artifacts needed to regenerate them.
4. Obtain independent scientific and reproducibility review before a public release or arXiv submission.

The original workspace hypothesis remains untested.
