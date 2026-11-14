#!/usr/bin/env python3
from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1]
spec={
"Workspace_Study_Pilot_P001.zip":["run_pilot.py","config.json"],
"Workspace_Study_P001_Diagnostics_D002.zip":["pilot_diagnostics_d002/model_from_p001.py","pilot_diagnostics_d002/gpu_check.py"]
}
for archive, paths in spec.items():
 with zipfile.ZipFile(root/"evidence"/archive) as z:
  for path in paths:
   print("\n===== "+archive+" :: "+path+" =====\n")
   print(z.read(path).decode())
