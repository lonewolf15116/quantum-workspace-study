# P002 — Fifth-round review disposition (v0.8 → v0.9)

**Date:** 15 November 2026  
**Reviewer decision:** **ACCEPTABLE WITH MINOR REVISIONS** for arXiv as a *descriptive pilot* (not an acceptance by arXiv or a journal).  
**Review basis:** full v0.8 text and prior response, **without access to the private repository or 110-file archive**.

## Resolution of requested minor changes

| ID | Review issue | v0.9 action | Disposition |
|---|---|---|---|
| M1 | Author names and affiliations unknown | Retained an explicitly unconfirmed author block; author must approve the precise byline/affiliation and any coauthors before final submission. No names, endorsements or institutional affiliations have been invented. | OPEN — author decision required |
| M2 | Bibliographic metadata incomplete | Verified and completed Carleo–Nomura–Imada *Nature Communications* **9**, 5322 (2018); Huang–Kueng–Torlai–Albert–Preskill *Science* **377**(6613), eabk3333 (2022). Liu et al. 2026 final publication already documented. Remaining entries still require a final bibliography pass; **do not claim the entire bibliography checked**. | PARTIALLY RESOLVED |
| M3 | Transformer input encoding caveat | Abstract explicitly says packed field semantics were not independently verified; §4 distinguishes observed tensor shapes/dtypes from unverified semantic meanings. Exact archived source and 815,233 W=0 parameter count remain source-identity verified locally. | DISCLOSURE REVISED — semantic source check not completed |
| M4 | Diagnostic benchmark vs pilot language | Replaced 'bounded diagnostic benchmark' in introduction with 'bounded diagnostic pilot study'. | RESOLVED |
| M5 | Interpretation of 0.14% mean-constant training-MSE difference | §5.4 explicitly says no interval is available and no statistically resolved effect is implied. | RESOLVED |

## Review constraints and honest remaining scope

- This is a **descriptive pilot**, not a generalizable negative result about transformer/GNN architecture classes or a theoretical demonstration of a hard circuit ensemble.
- GNN D12 step7040 transient advantage of ~0.0000096 is included; all listed final GNN endpoints fail the equal-instance held-out zero MAE benchmark, without a formal equivalence claim.
- 110-file private ZIP digest `de0dc6d99c24b25fc710d82ac2eea8ce02a8a715432ea51281015e3d96fe7be4` passed its local archive checks; exact training/evaluation artifact replication is *not publicly available*. Comparable independently written generators are possible from methods; exact replay of frozen data requires author-approved access.
- The transformer source hashes and W=0 815,233-parameter CPU count matched user-supplied local audit; the mapping of each packed tensor field to its implementation-level meaning was **not directly inspected**.
- Conditional trained-model errors for high-magnitude labels were not archived; no post hoc results are imputed.
- Reviewer 'acceptable with minor revisions' is a conditional scientific opinion, not arXiv editorial acceptance and not a verification of private source/experiments.

## Bibliography records verified in this pass

1. Carleo, G., Nomura, Y., and Imada, M. (2018). *Nature Communications* **9**, 5322. https://doi.org/10.1038/s41467-018-07520-3 (publisher).
2. Huang, H.-Y., Kueng, R., Torlai, G., Albert, V. V., and Preskill, J. (2022). *Science* **377**(6613), eabk3333. https://doi.org/10.1126/science.abk3333 (PubMed).
3. Liu et al. (2026). *Frontiers of Physics* **21**(6), 063201. https://doi.org/10.15302/frontphys.2026.063201 (publisher; earlier arXiv 2025).

## Final owner-controlled gates

1. Confirm author/byline/affiliation and any coauthor permissions.
2. Complete remaining bibliography metadata verification and final manuscript proof.
3. If possible, inspect locally generated `p002_transformer_model_and_pack_source.txt` to authenticate token/position semantics; otherwise retain caveat and reader-facing limitation.
4. Approve final data/code availability language and select whether any artifact will be released; **no repository visibility change or archive upload** has occurred.
5. Convert to arXiv-compatible format and obtain final author sign-off **before submission**.

**Disposition: EDITORIAL MINOR REVISIONS — in progress.** No new training, no additional archive expansion, no public release, and no arXiv submission.


## Final post-review title clarification — 15 November 2026

**Adopted title (v0.12 and arXiv source):** *When Zero Is Competitive: A Descriptive Pilot of Transformer and Gate-Graph Surrogates on Random-Angle Quantum Circuits*.

This adds **only the word “Quantum”** before “Circuits” relative to the fifth-round-reviewed title. The modification clarifies the domain of the underlying circuits; it does not change the task, models, experimental results, statistics, conclusions, or scope. The transformer and gate-graph surrogates remain **classical neural models** used to predict quantum-circuit observables; the title does **not** call them quantum neural networks. This is a post-review editorial clarification, not a new independent review.

The change is reflected in the source manuscript `paper/P002_BOUNDED_NEGATIVE_RESULT_DRAFT_v012.md`, the LaTeX title and PDF metadata, the regenerated author preview, the arXiv form metadata, the local submission README/checklist, and the source-only ZIP. A separate GitHub preparation record logs the new file hashes; prior ZIP hashes describe superseded, earlier files and must not be used for the revised package. The private P002 evidence archive remains unchanged and unsubmitted.
