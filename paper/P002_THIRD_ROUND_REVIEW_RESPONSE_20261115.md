# P002 — Third-round full-text review response and disposition

**Date:** 15 November 2026  
**Reviewed version:** v0.5  
**Reviewer verdict:** MAJOR REVISIONS REQUIRED / HOLD arXiv  
**Reviewer access:** full v0.5 manuscript and response, **not** the private evidence archive or repository.

## Changes in v0.6

- **P1 — Access / framing: OPEN.** Selected a consistently **descriptive pilot case study** framing rather than claiming a fully public benchmark. v0.6 title/abstract/intro/related-work language reflects this. There is still no public archive. Making the GitHub repository public would not publish the 110-file local ZIP. Only the author can authorise release, after reviewing contents and digest.
- **P2 — Transformer specification: PARTIAL / SOURCE AUDIT PREPARED.** Source already confirms d128, L4, 4 heads, FFN512; W=0; fixed AdamW .001/.01, batch32, clip1, eval every 64 updates, B/A/K/L configurations and 3 seeds. Added `scripts/audit_p002_transformer_source.py` to check original/substituted source SHA against `p002_arms_results/identity.json`, instantiate W=0 on **CPU** to count parameters and record parameter shapes, inspect first frozen instance's packed fields, and write verbatim `pack()` and `Model` source excerpts to a separate local text file. **No output exists yet; exact tokenisation, positional encoding and parameter count must not be invented.** Do not claim P2 closed before running/reviewing this audit.
- **P3 — Framing: EDITED.** Explicitly treats result as exploratory descriptive pilot; no causal mechanism, formal equivalence, universal transformer/GNN limitation or public benchmark claim.
- **P4 — Constants: EDITED.** Says compare against sensible train-fitted mean/median and literal zero; rejects broad assertion that *every* constant is equally competitive. The 0.14% training MSE difference is descriptive, with no uncertainty claim.
- **P5 — Verifier checklist: RESOLVED IN TEXT.** v0.6 Appendix A enumerates exactly 24 check descriptions corresponding to the programmed `checked` list in `scripts/verify_p002_paper_evidence.py`, including D12 legacy identity caveat and online training MSE. The 24 are not independent replications, and recording a SHA-256 is not equivalent to independently reproducing scientific findings.
- **P6 — Liu bibliography: VERIFIED.** Publisher's 2026 *Frontiers of Physics* **21**(6), 063201, DOI `10.15302/frontphys.2026.063201` (earlier arXiv:2504.00464, April 2025). See https://journal.hep.com.cn/fop/EN/2026/21/6 and https://arxiv.org/abs/2504.00464. Cantori and Pilati 2025 PRE 112 015304 source verified.

## Read-only transformer check — next local command

```powershell
git pull --ff-only
$python = "..\.venv\Scripts\python.exe"
& $python -m py_compile scripts\audit_p002_transformer_source.py
if ($LASTEXITCODE -ne 0) { throw "Syntax failed" }
& $python scripts\audit_p002_transformer_source.py --root . --out p002_transformer_source_audit.json --source-excerpts p002_transformer_model_and_pack_source.txt
Write-Host "Exit code: $LASTEXITCODE"
```

`p002_transformer_model_and_pack_source.txt` contains verbatim original/substituted model excerpts, **private code**; do not publish without author review. For a closed review, report the source audit metadata and inspect source excerpts; never equate successful CPU model instantiation with independent GPU training reproduction.

## Still unresolved

- **Access:** public deposit or a permitted, explicitly declared restricted-access pilot submission. Current archive SHA-256 `de0dc6d99c24b25fc710d82ac2eea8ce02a8a715432ea51281015e3d96fe7be4` is for a private, locally verified file. No deposit URI exists.
- **Transformer encoding/parameter count:** pending local source audit.
- **Conditional |y|>.3/.5 model error:** no raw predictions/weights established, so cannot fabricate or recover from scalar aggregate logs.
- **Review:** v0.6 not yet externally reviewed; no signed-off independent replication.

**Decision:** HOLD arXiv, no public release and no new model training.


## Post-review source audit update — 2026-11-15

**Local run reported by researcher:** `scripts/audit_p002_transformer_source.py` → `PASS_SOURCE_IDENTITY`, exit code 0. Exact W=0 parameter count: **815,233**. Both SHA-256 identity checks passed:

- Original archive model: `c591d3d59d421b118a4900379682f637fecf47ee2159ff815b40147c40b793d8`.
- Dimension-substituted effective model: `2e1e2c6388548e2e5b022570d448fb46b327db42d17c8dad32c0831b59763721`.
- CPU `pack()` result for first frozen instance: integer arrays indices 0–4 of shape [179], angle feature index 5 [179,2] float32, scalar integer fields indices 6–8 (observed values 16, 10, 4). Protocol `protocol/Workspace_Study_Step_01.md` describes the intended gate, observable, position/role and sine/cosine encoding, but **the semantic mapping of archived source must be verified against the generated `p002_transformer_model_and_pack_source.txt` before claiming it is confirmed**.

**P2 updated:** Parameter-count and archived source-identity subgates **PASSED LOCALLY**; exact implementation-level tokenization and position encoding **OPEN pending source-excerpt inspection**. This was an architecture-introspection run, not model retraining or independent reproduction. Manuscript v0.7 reflects this distinction. The repository and ZIP remain private, with no public-release authorization.
