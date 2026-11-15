# P002 v0.3 — internal, non-independent manuscript assessment

**Date:** 2026-11-15  
**Scope:** review of exact committed v0.2 manuscript text against P002 evidence milestones. This is an **assistant/editorial review, not an external independent ML-reader review**.

## Disposition: REVISE (v0.3 created); do not submit yet

### Major scientific-claims checks

1. **Causal mechanism — corrected.** The near-zero target distribution and unsuccessful held-out MAE are *associated observations*. A positive product-state control rules out gross pipeline dysfunction for that distinct analytic subproblem only. It **does not** isolate the entangled-workload failure to label concentration. Classical optimization, information loss, model expressivity and finite data remain alternatives. v0.3 makes this explicit.
2. **Depth/exposure/compute — bounded.** D12/D24/D40 at one GNN seed, a 7680-update budget and a successful CUDA memory sanity check exclude only the narrow claims that those exact configurations failed to execute or achieve a meaningful final MAE gain. They cannot rule out depth, compute or optimisation generally. v0.3 restricts that inference.
3. **MAE/MSE discipline — retained.** Primary held-out zero MAE is **0.1933994673** under equal-instance weighting. Held-out zero MSE is **0.0972971211**, not ~0.095 (the latter is training zero MSE). The GNN logged online MSE is minibatch/training loss, not fixed-model held-out model MSE. The pooled-scalar MAE 0.170763 is not the primary metric. v0.3 preserves these distinctions.
4. **Best checkpoint caveat — retained.** D12 checkpoint update 7040 beat literal zero by approximately 0.0000096, hence an unconditional claim that not a single checkpoint beat zero is false. v0.3 uses 'no meaningful' endpoint improvement.
5. **Workspace — confined.** v0.3 removes an extra workspace mention from methods, retaining a single short limitations sentence; no W=0 vs W=4 experiment is claimed.
6. **Source evidence — updated.** Manifest/source checks and 12 exactly matching sampled label vectors and v3 archive hash are in v0.3 with explicitly local/private status. The 110-file archive **is not committed to the private GitHub repository**. Making the repo public by itself would *not* make that archive public.

### Reader-facing issues that still deserve a fresh reader

- The opening now explains the zero-baseline hazard before giving experiment history.
- Methods still relies on external protocol documents for exact transformer input encoding, schedules and other configuration details. A reviewer should evaluate sufficiency for standalone comprehension.
- No figures are embedded in the Markdown draft. A later version needs legible workload schematic and endpoint comparison/target-magnitude plot **generated from original evidence**, if figures are used; do not invent values.
- Bibliography metadata and nearest-prior-work claims should be rechecked against full texts/publisher records, separately from the present editorial read.
- The conclusion should remain a bounded benchmarking result. No peer review, full cross-system rerun, formal uncertainty quantification or external reproducibility has occurred.

### Suggested external review assignment

Ask a reviewer with ML experience and no prior P002 exposure, explicitly independently from this assistant, to return (a) major issues; (b) claim-to-evidence mismatch table with manuscript quote and section; (c) five-minute comprehension assessment; (d) closest-prior-work novelty objection; (e) recommended precise edits, and (f) ACCEPT / MINOR REVISE / MAJOR REVISE disposition. Supply manuscript v0.3 and at least the archive manifest; grant private evidence access only with owner permission. Do not ask the reviewer to certify quantum circuit simulator correctness solely from the product-state control.

## Remaining decision gates

1. External independent manuscript and methodology review.
2. Author-authorised release, with checked ZIP bytes and an accessible stable URI, or truthful disclosure of private/request-only evidence.
3. Final bibliography, figure/table, author/permission and submission format checks.

No new model training is necessary for the **current descriptive paper plan**; this statement is an editing priority, not a claim that a stronger future science review could never request additional data.
