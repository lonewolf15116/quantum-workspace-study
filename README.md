# Quantum Circuit Observable Prediction — Transformer and Gate-Graph Surrogates

**Research repository · Mahesh Reddy Pagadala · Aston University, Birmingham, UK**

This repository studies whether classical neural networks can predict quantum-circuit expectation values better than inexpensive baseline estimators. It also contains an earlier investigation of **dedicated workspace tokens in transformer encoders**. The negative-result pilot and the workspace-token hypothesis are **distinct stages**: no confirmatory workspace-benefit claim has been established.

## Current paper: P002

**[When Zero Is Competitive: A Descriptive Pilot of Transformer and Gate-Graph Surrogates on Random-Angle Quantum Circuits](paper/P002_BOUNDED_NEGATIVE_RESULT_DRAFT_v012.md)**

**arXiv status:** Submitted 15 November 2026; **awaiting public arXiv identifier and announcement**. Primary category selected: `cs.LG`; requested cross-list: `cs.NE`. This repository links to the submitted-manuscript text, **not** yet to a public arXiv record. [Submission confirmation](paper/P002_ARXIV_SUBMISSION_CONFIRMED_20261115.md).

### Research question

For noiseless, layered circuits with independently sampled `RX/RY/RZ` angles and `CNOT` connectivity, can a transformer or gate-dependency graph network predict **single-qubit Z** and **pairwise ZZ** expectation values more accurately on **unseen circuit templates** than a simple zero predictor?

The question concerns classical supervised prediction of observables, **not** a quantum neural network, a quantum advantage claim, or a proof that these functions are unlearnable.

### Main findings (descriptive, not confirmatory)

| Measurement | P002 observation |
|---|---:|
| Circuit templates | 2,016 across 63 stratified workload cells |
| Angle instances | 45,864 |
| Arm K training targets with `|y| < 0.05` | 44.89% |
| Held-out-template, equal-instance literal-zero MAE | **0.193399** |
| Best evaluated transformer held-out MAE (approximately) | **0.194460** |
| GateDAG, 12 rounds / 1,920 updates, held-out MAE | 0.193497 |
| GateDAG, 12 rounds / 7,680 updates, held-out MAE | 0.193707 |
| GateDAG, 24 rounds / 7,680 updates, held-out MAE | 0.194118 |
| GateDAG, 40 rounds / 7,680 updates, held-out MAE | 0.194155 |
| Separate product-state positive control, model vs zero MAE | **0.007755 vs 0.514811** |

Under the stated evaluation and checkpoint selections, **none of the evaluated transformer checkpoints or final GateDAG endpoints outperformed the literal-zero baseline on the held-out-template panel**. A **transient** GateDAG checkpoint did slightly outperform zero, so this statement must not be expanded into “no checkpoint ever outperformed zero.” The restricted product-state control shows the pipeline can learn a simpler analytic task; it does not explain the failure on the entangled workload.

The measured 0.193399 is **equal-instance held-out MAE** and must not be substituted for pooled scalar MAE (0.17076277). The comparisons are point estimates, not a formal equivalence test or causal attribution. In particular, no per-model conditional error analysis of high-magnitude observable tails has been established.

Read the [full manuscript](paper/P002_BOUNDED_NEGATIVE_RESULT_DRAFT_v012.md) for methods, limitations, related work, source checks, and reference details.

## Earlier stage: P001 / workspace-token investigation

The original study asks whether converting four reserved masked-padding positions into learned **workspace tokens** improves observable prediction at fixed dense sequence capacity (179 positions) and under compute/parameter-matching constraints.

- [Transformer/workspace architecture protocol](protocol/Workspace_Study_Step_01.md)
- [Workload and resource-tolerance protocol](protocol/Workspace_Study_Step_02A.md)
- [P002 findings and workspace hold](roadmap/P002_FINDINGS_STATUS_20261115.md)

**Current status:** P001 diagnostics are exploratory. P002 then tested the predictive signal and baseline competitiveness of the circuit-observable task. The **workspace W=0 versus W=4 confirmatory contrast remains on hold**; do not interpret the P002 findings as a measured workspace-token effect.

## Repository guide

| Location | What it contains |
|---|---|
| [`paper/`](paper/) | Manuscript drafts, literature positioning, verification notes, independent review responses, and submission record |
| [`roadmap/`](roadmap/) | Experimental gates, diagnostic plans and findings; **some earlier status notes predate later experiments** |
| [`protocol/`](protocol/) | Original workspace experiment definitions |
| [`scripts/`](scripts/) | Data-generation, evaluation, diagnostic, integrity and evidence-packaging scripts |
| [`evidence/`](evidence/) | Legacy **P001** ZIP evidence and split ZIP parts, not the full frozen P002 dataset |

Useful entry points: [P002 evidence verification](paper/P002_MANUSCRIPT_EVIDENCE_VERIFICATION_20261115.md) · [P002 scientific findings](roadmap/P002_FINDINGS_STATUS_20261115.md) · [final pre-submission checks](paper/P002_FINAL_PRESUBMISSION_AUDIT_20261115.md).

## Evidence, reproducibility and access limits

**Public source code is not the same as a fully reproducible published experiment.** This repository contains scripts and protocol descriptions that can inform a comparable implementation of the circuit workload. It **does not** contain the exact frozen P002 training/evaluation dataset, the complete original model-run evidence or the 110-file P002 reproducibility archive.

The P002 archive is recorded as **private**, with local SHA-256 inventory and integrity checks. Local verification reported **24 numerical consistency checks** and **12 exact sampled-label regenerations**. These are **not** 24 independent training replications, a complete 45,864-instance regeneration, or an independent end-to-end training reproduction. See [private archive status](paper/P002_REPRODUCIBILITY_V3_LOCAL_PASS_20261115.md) and [submission record](paper/P002_ARXIV_SUBMISSION_CONFIRMED_20261115.md).

Five older **P001** evidence ZIPs (some stored as numbered parts) are present in the public repository. They can be reassembled and checked against [`SHA256SUMS`](SHA256SUMS):

```bash
python scripts/reassemble_evidence.py
```

That script verifies the **archived P001 ZIP bytes**; it does not reproduce the P002 experiments or establish that every embedded archived artifact has been independently reviewed. **Public visibility of those legacy archives should not be taken as an authorisation to publish the separate private P002 archive.**

> **Public-archive audit limitation:** The repository file inventory, archive names, sizes and checksums were checked during this README refresh, but the internal contents of all legacy binary ZIP archives have **not** been independently inspected for privacy, credentials or redistribution rights. Repository owners should complete that review before broadly promoting these archives.

## Scope and next steps

1. Complete an independent, distribution-aware reproduction with explicit dependency versions and full source-to-run verification.
2. Measure per-observable conditional errors, including `|y| > 0.3` and `|y| > 0.5`, on a newly instrumented comparable workload.
3. Test signal-rich or structured-angle workloads with baseline-aware, compute-matched comparisons.
4. Revisit the dedicated workspace-token contrast **only after** a predictive signal suitable for the comparison has been established.

These are research directions, not completed experiments or promised results.

## Citation

The P002 paper was **submitted to arXiv on 15 November 2026**, but a public identifier has **not yet been assigned**. Please do not cite a placeholder arXiv number. Once announced, the canonical `arxiv.org/abs/...` link and BibTeX citation will be added here.

For now, the work can be identified by its full title and author as a submitted preprint, with the understanding that its arXiv record is pending.

## Contact and attribution

**Mahesh Reddy Pagadala** · Aston University, Birmingham, UK  
[GitHub profile](https://github.com/lonewolf15116)

This repository does not specify a blanket open-source licence for its code and legacy archives. The paper's **CC BY 4.0** arXiv submission licence should not be assumed to apply automatically to all repository code, datasets or third-party materials.
