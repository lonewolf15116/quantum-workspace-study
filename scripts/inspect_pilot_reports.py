#!/usr/bin/env python3
"""Print bounded textual scientific summaries from verified archives, read-only."""
from pathlib import Path
import hashlib, zipfile, json

ROOT = Path(__file__).resolve().parents[1]
wanted = {
 "Workspace_Study_Pilot_P001.zip": ["REPORT.md","pilot_summary.json","config.json","dataset_status.json"],
 "Workspace_Study_P001_Diagnostics_D001.zip": [
    "pilot_diagnostics/REPORT.md","pilot_diagnostics/diagnostics.json",
    "pilot_diagnostics/learning_checks.json","pilot_diagnostics/check_curves.json"],
 "Workspace_Study_P001_Diagnostics_D002.zip": [
    "pilot_diagnostics_d002/REPORT.md","pilot_diagnostics_d002/results.json",
    "pilot_diagnostics_d002/gpu_status.json"]
}
manifest={}
for line in (ROOT/"SHA256SUMS").read_text().splitlines():
    if line.strip():
        h,p=line.split(maxsplit=1);manifest[Path(p).name]=h
for fname, files in wanted.items():
    path=ROOT/"evidence"/fname
    with path.open("rb") as f: observed=hashlib.file_digest(f,"sha256").hexdigest()
    assert observed==manifest[fname], f"SHA256 mismatch: {fname}"
    with zipfile.ZipFile(path) as z:
        for name in files:
            print(f"===== {fname} :: {name} =====")
            data=z.read(name)
            assert len(data)<=30000, "Unexpected oversized report"
            print(data.decode("utf-8"))
