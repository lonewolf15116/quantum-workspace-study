# P002 — arXiv source preparation record (15 November 2026)

> **Superseded after a one-word title clarification.** The current paper title adds **Quantum** before **Circuits**. Use [`P002_ARXIV_QUANTUM_TITLE_LOCAL_PASS_20261115.md`](P002_ARXIV_QUANTUM_TITLE_LOCAL_PASS_20261115.md) for the rebuilt source ZIP, PDF and metadata checksums. Hashes below are an accurate record of the **earlier, superseded** package and should not be used for the current upload.

**Status:** Source package built and independently clean-folder compiled **locally**. **NOT SUBMITTED OR PUBLICLY RELEASED.** The generated binary files live in the conversation artifacts, not in this GitHub repository. This document is a reproducibility/change-control record; it is not evidence that arXiv accepted a submission.

## Manuscript

- Title: *When Zero Is Competitive: A Descriptive Pilot of Transformer and Gate-Graph Surrogates on Random-Angle Circuits*
- Author: **Mahesh Reddy Pagadala**
- Affiliation: Aston University, Birmingham, UK
- Correspondence: mahesh15116@gmail.com
- Primary subject suggestion: `cs.LG` (not yet selected on arXiv)
- **9 pages, 1 figure**
- LaTeX is a source-preserving **editorial adaptation**, not a verbatim conversion, of `paper/P002_BOUNDED_NEGATIVE_RESULT_DRAFT_v011.md`. The author must proofread the final source and PDF.
- Scientific scope: **descriptive pilot**; no causal mechanism, statistical equivalence, architectural impossibility, workspace-token comparison, public benchmark or independently repeated training run claimed.

## Private, generated deliverables (not yet GitHub files)

1. `P002_Arxiv_Source_Upload.zip` — arXiv upload payload; 3 members only: `main.tex`, `main.bbl`, `figures/heldout_mae.pdf`.
2. `P002_Arxiv_Preview.pdf` — compiled 9-page preview; **do not upload as a PDF-only submission of TeX-authored work**.
3. `P002_Arxiv_Metadata.txt` — final title/byline, proposed category, short ASCII abstract (1357 characters, below arXiv's 1920-character limit), comments.
4. `P002_Arxiv_Validation_Report.txt` — compilation and ZIP validation evidence.
5. `P002_Arxiv_Complete_Kit.zip` — combined author review bundle, including editable source, metadata, PDF, validation record and generating figure script.

## Checksums (SHA-256)

```
P002_Arxiv_Source_Upload.zip 4a1c44cbda41fffdd30421eb1a7006934d520b9457553bf5ff310e613aea3d89
P002_Arxiv_Preview.pdf cd1c54b86e81060e4e464dcc2c3f760f09ceacc352e5ba980f7782c5fdcb3f8c
P002_Arxiv_Metadata.txt 40ff8a30c76f3f201a18f28863930747f8842219be8184c4d71609c6246eddd9
main.tex 2c3869ff7ce7ba8bdb7feb753eb13947326ab889f866487e8868fba666c2a548
main.bbl d76fe71f89d5a531a71a214a86cfb382e8b6668d0f034c5d77de3541d0687ea9
figures/heldout_mae.pdf 9b9c47922c5f3d78de6283dd379c9e0f7e6623f4b7ba49b074a6e9e8fc33f2a5
P002_Arxiv_Complete_Kit.zip 05c48e14e23f21132ce242b00f9e4ec0c02dd135c37279f8d3b89a142792d60b
```

## Local technical validation

- ZIP CRC and member list **PASS** (only the required .tex, .bbl and PDF figure).
- Fresh-directory PDFLaTeX twice from extracted ZIP **PASS** (both exit 0).
- Output **9 pages**, **one figure**, font types Type 1/CID TrueType all embedded, no Type 3.
- Final LaTeX warnings, missing citations/references, overfull boxes **none**.
- Fresh-directory PDF extracted text **matches preview**.
- Metadata abstract **1357 ASCII characters**.
- **No private dataset or 110-file v3 evidence archive** in ZIP.
- Bibliography correction: Huang, Chen and Preskill's 2022 arXiv preprint has published **PRX Quantum 4, 040337 (2023)**; Petersen is **Anne Helby Petersen, PMLR 286, pp. 3465–3479 (2025)**.

## Author-controlled submission gates

- Author reads and signs off on the **editorially adapted** final paper, title and figures.
- arXiv account eligibility/category/endorsement status must be checked in the actual submission UI.
- Author personally selects license and agrees to the arXiv submittal agreement.
- Upload source ZIP to arXiv, verify the automatically generated PDF there, confirm metadata and complete submission.
- Any future public release of the separate private v3 research archive requires explicit owner authorisation. Making the GitHub repository public alone would not make the local ZIP public.

## arXiv official guidance used

- https://info.arxiv.org/help/submit_tex.html
- https://info.arxiv.org/help/submit/index.html
- https://info.arxiv.org/help/prep.html

**Nothing has been submitted, uploaded to arXiv, made public, or released by this record.**
