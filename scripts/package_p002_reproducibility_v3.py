#!/usr/bin/env python3
"""Create a PRIVATE v3 archive from hash-verified v2 plus exact source dependencies.

Read-only with respect to original evidence; writes a new ZIP, never overwrites.
No network calls, code execution from archives, publication, or training.
"""
import argparse
import hashlib
import json
import platform
import sys
import zipfile
from pathlib import Path

REQUIRED = [
    "scripts/run_p002_arms.py",
    "scripts/run_p002_probes.py",
    "scripts/bench_archived_model_d128.py",
    "scripts/check_p002_product_state.py",
    "scripts/check_p002_dependencies_and_labels.py",
    "scripts/package_p002_reproducibility.py",
    "SHA256SUMS",
    "p002_dependency_label_audit.json",
    "evidence/Workspace_Study_Pilot_P001.zip",
    "evidence/Workspace_Study_P001_Diagnostics_D002.zip",
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--base", default="p002_reproducibility_v2.zip")
    p.add_argument("--out", default="p002_reproducibility_v3_private.zip")
    args = p.parse_args()
    root = Path(args.root).resolve()
    base = (root / args.base).resolve()
    target = (root / args.out).resolve()
    if target.exists():
        p.error("Refusing to overwrite: " + str(target))
    if not base.is_file():
        p.error("Missing v2 archive: " + str(base))
    if base == target:
        p.error("Input and output must differ")
    contents = {}
    with zipfile.ZipFile(base) as zin:
        if zin.testzip() is not None:
            p.error("v2 archive CRC failure")
        original = json.loads(zin.read("PACKAGE_SHA256_MANIFEST.json"))
        if original.get("missing_files") or not original.get("includes_full_dataset"):
            p.error("v2 must contain full dataset and have no missing selected files")
        claimed = original["files"]
        names = [x["path"] for x in claimed]
        if len(names) != len(set(names)):
            p.error("v2 has duplicate manifest paths")
        for item in claimed:
            name = item["path"]
            data = zin.read(name)
            if sha(data) != item["sha256"] or len(data) != item["bytes"]:
                p.error("v2 content/hash mismatch: " + name)
            contents[name] = data
    expected_checksums = {}
    checksums = (root / "SHA256SUMS")
    if not checksums.is_file():
        p.error("SHA256SUMS not present")
    for line in checksums.read_text().splitlines():
        if line.strip():
            digest, rel = line.split(maxsplit=1)
            expected_checksums[rel.strip()] = digest.lower()
    for rel in REQUIRED:
        path = (root / rel).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            p.error("Required dependency absent or outside root: " + rel)
        data = path.read_bytes()
        if rel in expected_checksums and sha(data) != expected_checksums[rel]:
            p.error("Original archive checksum mismatch: " + rel)
        if rel in contents and contents[rel] != data:
            p.error("Existing v2 member differs from local file: " + rel)
        contents[rel] = data
    # Version records are data, not requirements to reproduce a CPU label check.
    try:
        import numpy as np
        numpy_version = np.__version__
    except ImportError:
        numpy_version = None
    try:
        import torch
        torch_version = torch.__version__
        cuda_runtime = torch.version.cuda
        cuda_available = torch.cuda.is_available()
    except ImportError:
        torch_version = cuda_runtime = None
        cuda_available = False
    environment = {
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "numpy": numpy_version,
        "torch": torch_version,
        "torch_compiled_cuda": cuda_runtime,
        "cuda_available_now": cuda_available,
        "warning": "Current environment metadata, not necessarily original experiment runtime; compare with run identity.json files.",
    }
    contents["P002_ENVIRONMENT_SNAPSHOT.json"] = (
        json.dumps(environment, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    inventory = {
        "protocol": "P002-REPRODUCIBILITY-PACKAGE-003-CANDIDATE",
        "release_status": "PRIVATE_REVIEW_ONLY",
        "source_v2_zip_sha256": sha(base.read_bytes()),
        "includes_full_dataset": True,
        "missing_files": [],
        "files": [{"path": k, "sha256": sha(v), "bytes": len(v)}
                  for k, v in sorted(contents.items())],
        "limitations": [
            "No pretrained model weights; original GNN training not independently reproduced.",
            "Sampled label check is 12/12, not full 45864-instance regeneration.",
            "Check completeness of dependency environment for independent running.",
            "No public archive or repository visibility changes have been authorised.",
        ],
    }
    with zipfile.ZipFile(target, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name, data in sorted(contents.items()):
            z.writestr(name, data)
        z.writestr("PACKAGE_SHA256_MANIFEST.json",
                   json.dumps(inventory, indent=2, sort_keys=True) + "\n")
    # Independently verify new archive members immediately after writing.
    with zipfile.ZipFile(target) as z:
        if z.testzip() is not None:
            raise RuntimeError("Created v3 ZIP failed CRC test")
        for item in inventory["files"]:
            b = z.read(item["path"])
            if sha(b) != item["sha256"] or len(b) != item["bytes"]:
                raise RuntimeError("v3 SHA256 verification failed: " + item["path"])
    print(json.dumps({
        "status": "PASS_LOCAL_V3",
        "file_count": len(inventory["files"]),
        "missing": [],
        "archive": str(target),
        "archive_sha256": sha(target.read_bytes()),
        "source_v2_sha256": inventory["source_v2_zip_sha256"],
        "private": True,
    }, indent=2))

if __name__ == "__main__":
    main()
