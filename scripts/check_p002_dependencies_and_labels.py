#!/usr/bin/env python3
"""Read-only check: P002 generator/simulator source identity and sampled frozen labels."""
import argparse
import ast
import hashlib
import importlib.metadata
import json
import platform
import zipfile
from pathlib import Path
import numpy as np

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

def version(name):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--samples", type=int, default=12)
    p.add_argument("--atol", type=float, default=1e-10)
    p.add_argument("--out", default="p002_dependency_label_audit.json")
    a = p.parse_args()
    if not 9 <= a.samples <= 100 or a.atol <= 0:
        p.error("require samples 9..100 and positive atol")
    root = Path(a.root).resolve()
    target = Path(a.out).resolve()
    if target.exists():
        p.error("refusing to overwrite report: " + str(target))
    data = root / "p002_dataset"
    manifest = json.loads((data / "manifest.json").read_text(encoding="utf-8"))
    errors = []
    for name in ("instances.json", "templates.json"):
        if sha(data / name) != manifest["file_sha256"][name]:
            errors.append(name + " hash differs from manifest")
    generator_sha = sha(root / "scripts/generate_p002_data.py")
    if generator_sha != manifest.get("generator_sha256"):
        errors.append("generator source hash mismatch")
    archive = root / "evidence/Workspace_Study_Pilot_P001.zip"
    with zipfile.ZipFile(archive) as z:
        source = z.read("run_pilot.py")
    sim_sha = hashlib.sha256(source).hexdigest()
    if sim_sha != manifest.get("source_sha256"):
        errors.append("archived simulator source hash mismatch")
    funcs = [x for x in ast.parse(source.decode()).body
             if isinstance(x, ast.FunctionDef) and x.name == "simulate"]
    if len(funcs) != 1:
        raise RuntimeError("Expected one archived simulate function")
    namespace = {"np": np}
    exec(compile(ast.Module(body=funcs, type_ignores=[]),
                 "<archived-P001-simulate>", "exec"), namespace)
    simulate = namespace["simulate"]
    templates = json.loads((data / "templates.json").read_text())
    rows = json.loads((data / "instances.json").read_text())
    lookup = {x["template"]: x for x in templates}
    selected = []
    for panel in ("train", "within", "holdout"):
        for n in (4, 7, 10):
            idx = next((i for i, row in enumerate(rows)
                        if row["panel"] == panel and row["n"] == n), None)
            if idx is not None and idx not in selected:
                selected.append(idx)
    for idx in np.linspace(0, len(rows)-1, num=a.samples, dtype=np.int64):
        if int(idx) not in selected:
            selected.append(int(idx))
    selected = selected[:max(a.samples, 9)]
    checks = []
    for idx in selected:
        row = rows[idx]
        tmpl = lookup[row["template"]]
        predicted, _, _ = simulate(row["n"], tmpl["gates"],
                                   np.asarray(row["angles"], dtype=np.float64))
        actual = np.asarray(predicted, dtype=np.float64)
        expected = np.asarray(row["labels"], dtype=np.float64)
        if actual.shape != expected.shape:
            errors.append("shape mismatch row " + str(idx))
            continue
        diffs = np.abs(actual - expected)
        max_error = float(np.max(diffs))
        if not np.isfinite(diffs).all() or max_error > a.atol:
            errors.append("label mismatch row " + str(idx) + ": " + str(max_error))
        checks.append({"index": idx, "panel": row["panel"], "n": row["n"],
                       "r": row["r"], "family": row["family"],
                       "max_abs_error": max_error,
                       "float64_exact_equal": bool(np.array_equal(actual, expected))})
    report = {
        "protocol": "P002-DEPENDENCY-LABEL-CHECK-001",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors, "tolerance": a.atol,
        "source": {
            "generator_sha256_current": generator_sha,
            "generator_sha256_manifest": manifest.get("generator_sha256"),
            "simulator_source": "evidence/Workspace_Study_Pilot_P001.zip:run_pilot.py",
            "simulator_sha256_archived": sim_sha,
            "simulator_sha256_manifest": manifest.get("source_sha256"),
            "implementation": "custom NumPy state-vector simulator; not CUDA-Q/Qiskit"},
        "environment": {
            "python": platform.python_version(), "platform": platform.platform(),
            "machine": platform.machine(), "numpy": np.__version__,
            "torch": version("torch"), "qiskit": version("qiskit"),
            "cuda_quantum": version("cuda-quantum"),
            "torch_geometric": version("torch-geometric"),
            "rng": "NumPy Generator(PCG64)"},
        "dataset": {"templates": len(templates), "instances": len(rows)},
        "samples": checks,
        "limitations": [
            "This spot-check is not full-dataset regeneration.",
            "No GPU training or independent training-run reproduction.",
            "Bitwise equality can vary across operating systems/dependency versions."]}
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": report["status"], "checks": len(checks),
        "exact_float64_matches": sum(c["float64_exact_equal"] for c in checks),
        "max_abs_error": max((c["max_abs_error"] for c in checks), default=None),
        "errors": errors, "report": str(target)}, indent=2))
    raise SystemExit(0 if not errors else 2)

if __name__ == "__main__":
    main()
