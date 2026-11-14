# Transformer workspace tokens for quantum circuit observables

This exploratory study tests whether converting four masked padding slots into learned workspace improves observable prediction at fixed dense sequence capacity (179 positions).

## Contents

- `protocol/Workspace_Study_Step_01.md`: architecture specification.
- `protocol/Workspace_Study_Step_02A.md`: workload and resource-tolerance specification.
- `evidence/Workspace_Study_Step_02B.zip` and `evidence/Workspace_Study_Step_02B_R1.zip`: resource/evidence packages.
- `evidence/Workspace_Study_P001_Diagnostics_D001.zip`: first diagnostics package.
- `evidence/Workspace_Study_Pilot_P001.zip.part01` through `.part03`: original Pilot 01 archive, split into exact binary parts.
- `evidence/Workspace_Study_P001_Diagnostics_D002.zip.part01` through `.part04`: second diagnostics package, split into exact binary parts.
- `SHA256SUMS`: SHA-256 of the five *complete original ZIP archives*.
- `scripts/reassemble_evidence.py`: reconstruct the two split archives and verify all five ZIP hashes.

The two larger archives are split only to accommodate an upload-connection size limit. Their content is otherwise unchanged. From a fresh repository checkout, run:

```bash
python scripts/reassemble_evidence.py
```

The script recreates the two ZIP files in `evidence/` and prints PASS/FAIL for every checksum. Keep the original numbered parts intact.

## Current scientific status

Pilot 01 is exploratory. All six final checkpoints had higher training MAE than the zero predictor. GPU fit and confirmatory performance remain unmeasured. The diagnostics and source archives are provided for investigation and reproduction; they do not establish a positive performance finding.
