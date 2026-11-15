# P002 manuscript v0.1 — Claim-level evidence verification

**Audit date:** 2026-11-15  
**Basis:** The existing GitHub source repository, plus user-supplied PowerShell text logs in this ChatGPT conversation. These text logs were read and numerical JSONL records parsed independently in the analysis runtime. **This is a transcript-value verification, not a fresh execution or binary integrity audit.**

## 1. What was verified against a different accessible source

### Dataset and workload design (source-level)

GitHub `scripts/generate_p002_data.py` defines 63 cells (n=4..10, r=2/4/6, path/ring/all_to_all), training template quota 30 and angles 20, within angles 4, held-out templates 2 and angles 4. Its full-data assertions demand 2,016 templates, 37,800 train, 7,560 within, 504 held-out, summing **45,864** instances. It uses a separate topology stream, training-angle stream, within-angle stream, held-out-angle stream with pinned PCG64 seeds. These are **code assertions**, not a re-hash of the full realised dataset.

`scripts/run_p002_graph_baseline.py` confirms K=30 templates × A=4 training angles, batch32, MSE training loss with per-example mean over valid observables, AdamW LR0.001 weight decay0.01, clip norm1; score averages each valid-observable MAE within example then averages examples. The `--layers` flag creates separately parameterised linear+GRU cells for 12/24/40 rounds. The raw output vector has up to 55 observables.

### Verified numerical logs (from supplied local PowerShell text)

| Draft claim | Exact support from readable stdout | Result | Evidence origin |
|---|---|---|---|
| Best transformer B MAE ≈ 0.19464 | 0.1946444189556991, seed202, step256 | MATCH | `Pasted text (2)(2).txt` |
| Best transformer A MAE ≈ 0.19520 | 0.19520198524417387, seed202, step320 | MATCH | same |
| Best transformer K MAE ≈ 0.19461 | 0.19461455881240994, seed101, step128 | MATCH | same |
| Best transformer L MAE ≈ 0.19446 | 0.19446001766495405, seed202, step256 | MATCH | same |
| GNN L@1920 training MAE ≈ 0.122 | 0.1219801879524889 | MATCH | `Pasted text(20261114-233333).txt` |
| GNN L@1920 within MAE ≈ 0.226 | 0.22630842580711322 | MATCH | same |
| GNN L@1920 held-out MAE ≈ 0.234 | 0.23359466968695558 | MATCH | same |
| GNN K@1920 D12 train/held-out | 0.19071748898088656 / 0.19349666018896397 | MATCH | same |
| GNN K@7680 D12 train/held-out | 0.19047649691741245 / 0.19370665999927691 | MATCH | `Pasted text(20261114-234736).txt` |
| GNN K@7680 D24 train/held-out | 0.19128138681839185 / 0.19411771398200284 | MATCH | `Pasted text(20261115-000309).txt` |
| GNN K@7680 D40 train/held-out | 0.19126903796014155 / 0.1941549369200532 | MATCH | `Pasted text(20261115-002104).txt` |
| Held-out literal-zero for GNN | 0.19339946731888052 | MATCH | same K logs |
| Product control at update1000 | MAE 0.007754660440241423, Z 0.006748016513938637, ZZ 0.008425756383417138, zero 0.5148107764980523 | MATCH | `Pasted text(20261114-233333).txt` |

For the transformer, parsed 156 reported checkpoint records across the 4 arms × 3 seeds; all held-out MAEs in that console transcript exceed zero=0.19339946679504386. However these **are sampled checkpoints**, not predictions at every optimiser step; state ‘all evaluated checkpoints’ rather than ‘all checkpoints’. For D12@7680, an intermediate reported checkpoint at step7040 achieved held-out MAE 0.1933898901149246, *marginally* below zero by 0.0000095772; the predetermined final endpoint **failed**. Avoid ‘no checkpoint ever beat zero’ across all GNN runs.

## 2. Results only supported by user-supplied summaries / unavailable native files

| Claim | Current disposition | Reason |
|---|---|---|
| Total 2,016 distinct generated templates, 45,864 actual rows, no overlap or leaks | Source assertions, NOT independently reproduced | Full realised `p002_dataset` not available in current repository attachments or analysis runtime |
| Arm K label scalar distribution (44.886% <0.05, scalar MAE 0.168849) | TRANSCRIPT ONLY | Console stdout supplied, but original `p002_bounded_audit_s202_labels.json` not fetched |
| Per-scalar mean/median MAE constants | TRANSCRIPT ONLY | User separately pasted six computed values; full original JSON not inspected |
| Small-set entangled fit MAE 0.171882, fresh-angle MAE 0.425408 | TRANSCRIPT ONLY | User pasted auditor console run; `checkpoints.jsonl` and `identity.json` not fetched |
| Final MSE training zero 0.095369, mean constant 0.095236, D12/D24/D40 online 512-step means 0.094992/0.095266/0.095261 | TRANSCRIPT ONLY | User pasted computed report, but local audit JSON and full original `steps.jsonl` files not accessible |
| GNN parameter counts 823809/1604865/2646273 | COMPUTATION/SOURCE + TRANSCRIPT | Counts reported in user's 10-step CUDA preflight; model source has separately parameterised layers; did not execute PyTorch model locally |
| Gate dependency-chain percentiles 19/30/40, 68.9% >12 | RESEARCH NOTE ONLY | Code exists but no `p002_graph_chain_audit.json` currently fetched and verified |
| Step02B R1 eligibility ±1%, 512 parameter gap | SOURCE / ARCHIVE ONLY | ZIP and protocol archived with SHA256SUMS; no independent local archive extraction/accounting in this audit |
| Raw P002 independent reproducibility | BLOCKED | The GitHub repository is **private**, and its `evidence/` directory presently has P001 and Step02B archives rather than full P002 datasets/results |

## 3. Corrections / caveats required in manuscript

1. **Reproducibility blocker:** Repository status queried from GitHub API is `private=true`. Do not promise public dataset/code access or universal independent reproduction. No instruction here to make private research public without the owner's explicit authorisation.
2. **Weighting:** Per-scalar heldout MAE of zero is 0.1707627674; equal-instance heldout MAE of zero is 0.1933994673. The current draft correctly distinguishes them. Never put one in a comparison against model MAE scored under the other convention.
3. **MSE status:** Archived last-512-step results are moving online training-minibatch means. They are not a matched full-panel final model MSE and have no equivalence confidence interval. Do **not** write ‘models fail held-out MSE’ or ‘statistically indistinguishable’ without new data.
4. **Do not claim joint architecture tested as workspace effect:** No W=0-vs-W=4 workspace intervention was evaluated. It remains untested.
5. **Source-version specificity:** The Cantori–Pilati comparison was based on arXiv v1 and the journal abstract, not a line-by-line inspection of journal-final PDF. Liu et al. based on searchable article-text copy and arXiv abstract because native PDF could not be loaded by web tool.
6. **Model precision:** One seed underlies the 7,680-step GateDAG depth sweep. No failure claim extends to all seeds, all architectures, or all depths.
7. **Novelty:** The 2025 Cantori–Pilati paper already investigates learnability failures from random-angle variance in layered rotation/CNOT circuits. Reposition ‘signal concentration’ as a measured **characteristic** and ‘baseline-aware evaluation’ as methodological value, not a newly proven causal mechanism.
8. **No hidden archive relabelling:** SHA256SUMS lists P001 and Step02B archives (not P002 full logs), e.g. 6c0ae206300932d1d8ffa5ae643299a4dc8e598d1ef535e42ab8e133cc953922 for Step02B_R1. Those archive checksums do not validate P002 outcomes.

## 4. Readiness decision

**Numerical consistency within accessible console transcripts:** PASS for the listed Transformer/GNN/product control endpoints.  
**Full binary source-identity and dataset reproducibility:** **NOT VERIFIED / BLOCKED** (absent local `p002_dataset` and JSONL/run artifacts).  
**Scientific novelty vs direct prior work:** LOW-TO-MODERATE as a descriptive benchmark case study; mechanism originality NOT ESTABLISHED.  
**Submission-readiness:** **HOLD** until authentic full P002 outputs/dataset or reproducible derivation are available, manuscript claims match audited tables, and independent reader reviews novelty. Working manuscript can continue, but **not** labelled submission-ready.

This status does not itself authorise any new experiment, public GitHub visibility change or arXiv submission.
