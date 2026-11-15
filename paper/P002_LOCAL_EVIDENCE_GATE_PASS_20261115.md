# P002 local evidence-consistency verification — PASS

**Date:** 2026-11-15  
**Verifier:** `scripts/verify_p002_paper_evidence.py` at commit `234cbb3485addd0c444ba34426897933034c1b70`  
**Command:** `python scripts/verify_p002_paper_evidence.py --root . --out p002_paper_evidence_verification_v2.json`

## Researcher-reported verification outcome

- Status: `PASS_COMPLETE`
- Process exit: `0`
- Checks reported: **24**
- Missing files: **0**
- Errors: **0**

The original local report resides at `p002_paper_evidence_verification_v2.json` and **has not been uploaded or independently read in this GitHub commit**. The check names and result above are transcribed from researcher-supplied PowerShell output.

### Checks reported as passed

- Dataset cardinalities and template split consistency.
- Original D12 legacy identity accepted with missing `layers` field; expected 823809 parameters and other identity attributes.
- D12, D24, D40 training and held-out MAE endpoints at step 7680.
- Each depth run's 7680-step log.
- D24 and D40 explicit identity metadata.
- Training scalar mean absolute label, near-zero label fraction, and held-out fitted-constant MAE.
- Zero MSE for training and held-out panels; D12/D24/D40 online stochastic MSE summaries.
- Restricted entangled-set training and fresh-angle MAE.

### Gate disposition

**CLOSE: local P002 evidence-consistency verification** for the checks enumerated in this script.

**Not closed:** independent re-execution or external reproduction, complete source-revision binding (particularly legacy D12), public release of raw P002 evidence, full-template/per-seed statistical uncertainty, full-text prior-art novelty assessment and independent second-reader review.

**Scientific boundary:** no held-out final-model GNN MSE was measured; online training-minibatch MSE is not a held-out result. Workspace intervention was never tested. Novelty and causality remain carefully bounded.

### Manuscript next stage

The result tables in manuscript v0.1 now have local checked numerical support for the specific checked endpoints. Proceed to manuscript revision, final raw-evidence export / reproducibility packaging and second-reader scientific review. Do not yet label the paper ready for arXiv submission.
