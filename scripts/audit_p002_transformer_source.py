#!/usr/bin/env python3
"""Read-only P002 transformer model provenance and architecture extraction.

Uses P001 archived original model; invokes the same four literal substitutions
as the P002 transformer runner. CPU instantiation only. NO training, evaluation,
archive modification, Git operations, or publication.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path

import numpy as np
import torch

from bench_archived_model_d128 import ARCHIVE, REPLACEMENTS, load_original_model


def digest(data):
    return hashlib.sha256(data).hexdigest()


def definition(source, name):
    tree = ast.parse(source)
    matches = [node for node in tree.body
               if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError("Expected exactly one top-level definition: " + name)
    return ast.get_source_segment(source, matches[0])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--out", default="p002_transformer_source_audit.json")
    parser.add_argument("--source-excerpts",
                        default="p002_transformer_model_and_pack_source.txt")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    report_path = (root / args.out).resolve()
    excerpts_path = (root / args.source_excerpts).resolve()
    if report_path.exists() or excerpts_path.exists():
        parser.error("Refusing to overwrite output: choose new filenames")
    with __import__("zipfile").ZipFile(ARCHIVE) as archive:
        original_bytes = archive.read("pilot_diagnostics_d002/model_from_p001.py")
    original_source = original_bytes.decode("utf-8")
    effective_source = original_source
    for before, after in REPLACEMENTS:
        count = effective_source.count(before)
        if count != 1:
            raise RuntimeError("Replacement occurrence count != 1: " + repr(before))
        effective_source = effective_source.replace(before, after)

    module, original_sha, effective_sha = load_original_model()
    if original_sha != digest(original_bytes):
        raise RuntimeError("Original source hash differs from the loaded archive")
    if effective_sha != digest(effective_source.encode("utf-8")):
        raise RuntimeError("Effective source hash differs from the loader")

    original_identity = json.loads(
        (root / "p002_arms_results/identity.json").read_text(encoding="utf-8"))
    checks = {
        "original_matches_run_identity":
            original_identity.get("source_original") == original_sha,
        "effective_matches_run_identity":
            original_identity.get("source_substituted") == effective_sha,
    }

    module.device = "cpu"
    torch.manual_seed(202)
    model = module.Model(0).cpu()
    parameters = sum(p.numel() for p in model.parameters())
    named = [{"name": name, "shape": list(p.shape), "numel": p.numel()}
             for name, p in model.named_parameters()]

    templates = json.loads(
        (root / "p002_dataset/templates.json").read_text(encoding="utf-8"))
    instances = json.loads(
        (root / "p002_dataset/instances.json").read_text(encoding="utf-8"))
    module.templates = {entry["template"]: entry for entry in templates}
    packed = module.pack(instances[0], 0)
    fields = []
    for index, value in enumerate(packed):
        arr = np.asarray(value)
        fields.append({
            "index": index,
            "shape": list(arr.shape),
            "dtype": str(arr.dtype),
            "first_eight_values": arr.reshape(-1)[:8].tolist(),
        })

    excerpts = (
        "P002 transformer archived ORIGINAL + dimension-substituted definitions\n"
        "PRIVATE SOURCE AUDIT: review before distributing\n"
        "Original source SHA-256: " + original_sha + "\n"
        "Effective source SHA-256: " + effective_sha + "\n\n"
        "=== ORIGINAL pack ===\n" + definition(original_source, "pack") +
        "\n\n=== ORIGINAL Model ===\n" + definition(original_source, "Model") +
        "\n\n=== EFFECTIVE pack ===\n" + definition(effective_source, "pack") +
        "\n\n=== EFFECTIVE Model ===\n" + definition(effective_source, "Model") +
        "\n"
    )
    excerpts_path.write_text(excerpts, encoding="utf-8")
    report = {
        "protocol": "P002-TRANSFORMER-SOURCE-AUDIT-001",
        "status": "PASS_SOURCE_IDENTITY" if all(checks.values()) else "SOURCE_MISMATCH",
        "checks": checks,
        "archive_member": "pilot_diagnostics_d002/model_from_p001.py",
        "original_source_sha256": original_sha,
        "substituted_source_sha256": effective_sha,
        "transformer_parameters_W0": parameters,
        "parameter_details": named,
        "pack_W0_first_frozen_instance": fields,
        "torch_runtime": torch.__version__,
        "numpy_runtime": np.__version__,
        "source_excerpts": str(excerpts_path),
        "limitations": [
            "CPU model instantiation only; no training or inference executed.",
            "This records and confirms source identity and parameter count for the archived transformer.",
            "The original GPU training is not independently reproduced.",
            "Source excerpts remain private and may contain unrelated P001 implementation.",
        ],
    }
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "checks": checks,
        "transformer_parameters_W0": parameters,
        "original_source_sha256": original_sha,
        "substituted_source_sha256": effective_sha,
        "pack_fields": fields,
        "source_excerpts": str(excerpts_path),
        "report": str(report_path),
    }, indent=2))
    raise SystemExit(0 if all(checks.values()) else 2)


if __name__ == "__main__":
    main()
