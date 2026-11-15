# P002 — Fourth-round independent full-text review response (v0.7 → v0.8)

**Date:** 15 November 2026  
**Reviewer basis:** full manuscript v0.7 and third-round response; **private source repo and 110-file archive inaccessible to reviewer**.  
**Reviewer verdict:** MAJOR REVISIONS; remaining decisions principally artifact accessibility and verified transformer token semantics.

## Issue dispositions

| Reviewer request | v0.8 action | Status |
|---|---|---|
| P1 — Public artifact or honest comparable-regeneration statement | Abstract explicitly limits regenerated work to a comparable circuit workload, not frozen identical records. Section 8 now distinguishes independent implementation of the specified sampling procedure from exact reproduction of 2,016 template identities / 45,864 labels, individual run artifacts and checkpoints. Private archive has not been released; access may be requested only with author approval, **not promised**. | **DISCLOSED, no public release** |
| P2 — Transformer intended vs verified semantics | §4 distinguishes protocol's *intended* token conventions from executable implementation, whose recovered source excerpts still require independent inspection. Reports audit-established 815,233 W=0 parameters and matching original/substituted source hashes; leaves field semantics explicitly unconfirmed, including three metadata scalars. | **PARTIAL; source excerpt review open** |
| P3 — 'Meaningfully' undefined | Removed the ambiguous adverb from abstract. §5.1 defines non-improvement solely as descriptive recorded held-out MAE comparison to zero; no effect-size margin, seed uncertainty, or inferential equivalence claim. The separate D12 transient near-tie remains disclosed. | **RESOLVED** |
| P4 — 0.14% lack of uncertainty | Abstract marks 0.14% Arm K training MSE difference as a descriptive point estimate with no uncertainty interval. | **RESOLVED** |
| P5 — Authorship/bibliography | Retained unconfirmed author/affiliation placeholders and marked outstanding bibliographic finalisation in checklist; did not invent authorship, endorsements or unverified citations. | **OPEN for author/editor** |

## Evidence discipline and release controls

- Existing numerical verifier: locally reported 24 checks, no errors; **not independent replication**.
- Archived P001 custom NumPy simulator: local generator/simulator hash match and 12 exactly regenerated label vectors; **not full dataset regeneration**.
- Private local v3 ZIP: 110 files, SHA-256 `de0dc6d99c24b25fc710d82ac2eea8ce02a8a715432ea51281015e3d96fe7be4`; **not public**.
- Transformer CPU source audit: `PASS_SOURCE_IDENTITY`, W=0 parameters **815,233**, exact matching source hashes; **implementation-level meaning of fields not certified**.
- Conditional tail errors for neural models: **not archived/verified**; no claim on `|y|>0.3` or `|y|>0.5` possible from aggregate logs.

## Editorial decision

**v0.8 is a revised descriptive pilot, not a publicly reproducible benchmark.** Fourth-round reviewer said this scope could be acceptable for an arXiv descriptive pilot if clearly disclosed, but that conditional opinion **is not a submission acceptance or permission**. Exact artifact access, reviewer source checking, final author/bibliography approval, and LaTeX/compliance checks remain open.

No training, simulator generation, public-repository permission change, ZIP upload, DOI creation, or arXiv submission has been undertaken.
