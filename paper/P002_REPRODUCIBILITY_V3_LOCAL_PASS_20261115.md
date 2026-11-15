# P002 v3 — private reproducibility archive local integrity PASS

**Date:** 2026-11-15  
**Evidence source:** researcher-supplied PowerShell console output; archive bytes not independently inspected by the assistant.

## Result

- Script: `scripts/package_p002_reproducibility_v3.py`
- `status`: `PASS_LOCAL_V3`
- `file_count`: **110**
- `missing`: **[]**
- `archive`: `p002_reproducibility_v3_private.zip`
- SHA-256: `de0dc6d99c24b25fc710d82ac2eea8ce02a8a715432ea51281015e3d96fe7be4`
- Source v2 ZIP SHA-256: `6bf984d0fef3843bc135f951669a55e314a6a613fd2c6e974f5d9a3e190237f7`
- `private`: `true`
- Process exit code: **0**

The builder rechecked every original v2 manifest member, added archived P001 simulator and transformer source dependencies and related scripts, recorded the current environment snapshot, then verified all new ZIP members against their freshly created hashes. It did not train models or publish the archive.

## Evidence-level qualification

This closes **local private v3 archive construction and internal integrity**. It does **not** close: independent full training reproduction, full source-to-run binding, cross-platform regeneration, complete environment lock, peer scientific review, or public release. The source and 12 sampled labels previously checked locally exactly, but 45,864-instance regeneration was not run. Current environment versions are not automatically historical experiment versions.

## Manuscript-safe proposed wording

> The frozen dataset and selected run evidence have been preserved in a private, SHA-256-inventoried 110-file archive (SHA-256: `de0dc6d99c24b25fc710d82ac2eea8ce02a8a715432ea51281015e3d96fe7be4`). Local automated verification passed the numerical consistency checks and all archived file-integrity checks. The archived NumPy simulator source hash matched the dataset manifest, and twelve sampled label vectors were reproduced exactly in the local environment. Independent training reproduction and public artifact availability have not yet been established.

**Gate:** package integrity PASS; public reproducibility NOT YET ESTABLISHED; submission NOT AUTHORISED.
