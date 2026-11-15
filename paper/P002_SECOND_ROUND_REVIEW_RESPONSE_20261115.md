# P002 — Second-round full-manuscript review disposition

**Date:** 2026-11-15  
**External verdict:** MAJOR REVISIONS REQUIRED.  
**Review scope:** reviewer reports reading the full v0.4 manuscript and response document, with independent public literature checking, but **not** the private v3 archive or source evidence.

## Revision status (v0.5)

| External priority | Status | Response |
|---|---|---|
| P1 — Public reproducibility or pilot framing | **OPEN — owner release decision required** | Archive `p002_reproducibility_v3_private.zip` is local, 110 files, digest `de0dc6d99c24b25fc710d82ac2eea8ce02a8a715432ea51281015e3d96fe7be4`. It is **not** automatically available on GitHub. Nothing has been published. v0.5 continues explicitly as an exploratory bounded pilot pending accessibility. |
| P2 — Transformer specification | **PARTIALLY RESOLVED** | From `scripts/run_p002_arms.py` and `scripts/bench_archived_model_d128.py`: d128, 4 encoder layers, 4 heads, FFN512, W=0; AdamW lr .001/decay .01, batch32, grad clip1, eval each 64 updates; arms B/A/K/L, 384/1920 steps and seeds 101/202/303. v0.5 adds arm table. **Open:** exact archived token/positional encoding and parameter count need inspection of archived `model_from_p001.py` or run inventory; do not infer them. |
| P3 — Conditional |y|>.3/.5 neural endpoint errors | **OPEN / EVIDENCE NOT FOUND** | Aggregate MAE and MSE checkpoints cannot reconstruct per-target conditional model errors. No weights or heldout per-observable outputs have been established. v0.5 acknowledges missing evidence and that high-magnitude-tail learning cannot be excluded. Do not invent values or interpret a zero-only conditional metric as a neural result. If future inspection finds persisted per-observable predictions, this can be assessed read-only. |
| P4 — Liu non-tension | **RESOLVED IN TEXT** | v0.5 organises non-equivalence across gate set, label scale, graph model, split and noise settings. |
| P5 — Within-angle law | **RESOLVED IN TEXT** | Generator uses separate PCG64 random streams and identical Uniform[-π,π) per rotation, with new angles for seen templates and distinct held-out template identities. |
| P6 — Step7040 near-tie | **RESOLVED IN TEXT** | v0.5 states that 0.0000096 advantage is a single-checkpoint near-tie without paired uncertainty/seed evidence, not reliable improvement. |

## Additional corrections

- Product-state positive control is **only** a pipeline check on a separate analytic task.
- Target variation in a deterministic noiseless supervised map does not constitute irreducible uncertainty.
- Distinguish the zero predictor from the broader set of training-derived constant estimators.
- Manuscript title and interpretation specify tested architecture instances; no impossibility or causal claim.
- Missing numerical uncertainty is acknowledged rather than converted to an unsupported equivalence conclusion.

## Publication readiness decision

**REVISE / HOLD for arXiv** pending P1 accessible evidence or appropriately restricted pilot framing, final source-specific transformer architecture detail (P2) and an editorial decision on P3 (whether existing raw outputs allow conditional metrics, else disclose explicit limitation and narrow 'diagnostic' claims). Seek independent v0.5 read after the changes. The published ZIP must be byte-identical to the claimed SHA-256 and reviewed for release permissions.

No new training, private archive upload, repository visibility change or submission has been performed or approved.
