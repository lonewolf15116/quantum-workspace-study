#!/usr/bin/env python3
"""Create an owner-reviewed, local-only, hash-inventoried P002 evidence ZIP.

No publication, GitHub push, permission change, training, regeneration or
network calls. Review packaged contents before deciding to share.
"""
import argparse
import hashlib
import json
import os
import zipfile
from pathlib import Path

SOURCES=[
    "scripts/generate_p002_data.py",
    "scripts/run_p002_graph_baseline.py",
    "scripts/audit_p002_labels.py",
    "scripts/check_p002_entangled_overfit.py",
    "scripts/audit_p002_mse_readonly.py",
    "scripts/verify_p002_paper_evidence.py",
    "roadmap/P002_AUDIT_001_RESULTS_20261115.md",
    "roadmap/P002_FINAL_MSE_RESULTS_20261115.md",
    "paper/P002_LOCAL_EVIDENCE_GATE_PASS_20261115.md",
]
FILES=[
    "p002_paper_evidence_verification_v2.json",
    "p002_bounded_audit_s202_labels.json",
    "p002_mse_final_readonly_audit.json",
    "p002_bounded_audit_s202_summary.json",
]
DIRS=[
    "p002_graph_K7680_s202",
    "p002_graph_K7680_D24_s202",
    "p002_graph_K7680_D40_s202",
    "p002_bounded_audit_s202_entangled",
]
# Only bounded audit/run artifacts; reject any unexpected files in evidence dirs.
ALLOWED_RUN={"identity.json","checkpoints.jsonl","steps.jsonl","summary.json"}
ALLOWED_ENTANGLED={"identity.json","checkpoints.jsonl","steps.jsonl","summary.json"}
DATASET=["p002_dataset/manifest.json","p002_dataset/templates.json","p002_dataset/instances.json"]

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",default=".")
    parser.add_argument("--out",default="p002_reproducibility_candidate.zip")
    parser.add_argument("--include-dataset",action="store_true")
    parser.add_argument("--extra-file",action="append",default=[],
        help="Explicit relative file to include (repeat for transformer/product-state provenance)")
    parser.add_argument("--allow-partial",action="store_true",
        help="Allow missing optional artifacts but record omissions clearly")
    args=parser.parse_args()
    root=Path(args.root).resolve()
    output=Path(args.out).resolve()
    if output.exists():parser.error("Refusing to overwrite "+str(output))
    if root in output.parents and output.parent != root:
        parser.error("Output should be placed at repo root or outside it")
    selected=SOURCES+FILES+args.extra_file+(DATASET if args.include_dataset else ["p002_dataset/manifest.json"])
    for dirname in DIRS:
        candidate=root/dirname
        if not candidate.is_dir():
            selected.append(dirname+"/MISSING_DIRECTORY")
            continue
        names=sorted(p.name for p in candidate.iterdir() if p.is_file())
        unknown=set(names)-(ALLOWED_ENTANGLED if "entangled" in dirname else ALLOWED_RUN)
        if unknown:parser.error("Unexpected files in "+dirname+": "+repr(sorted(unknown)))
        selected.extend(dirname+"/"+name for name in names)
    contents=[]
    absent=[]
    for rel in selected:
        path=root/rel
        if not path.is_file():
            absent.append(rel)
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            parser.error("Refusing symlink/out-of-root path "+rel)
        contents.append((rel,path.read_bytes()))
    if absent and not args.allow_partial:
        parser.error("Missing evidence; no archive created: "+", ".join(absent))
    metadata={
        "title":"P002 research reproducibility archive, private local review copy",
        "protocol":"P002-REPRODUCIBILITY-PACKAGE-001",
        "includes_full_dataset":bool(args.include_dataset),
        "contains_sensitive_data_review_required":True,
        "missing_files":absent,
        "files":[{"path":rel,"sha256":sha256(payload),"bytes":len(payload)}
                 for rel,payload in contents],
        "notes":[
            "No archived GNN model weights were produced by the original runner.",
            "A PASS_COMPLETE verification confirms specific local checks, not a full scientific reproduction.",
            "P002 training MSE summaries are stochastic online minibatch statistics.",
            "Default inventory does not include all transformer or product-state logs; include explicitly with --extra-file before calling an archive complete.",
            "Keep repository PRIVATE unless the owner explicitly authorizes release.",
            "Before distribution confirm licences, privacy, dataset size, and authorship.",
        ],
    }
    with zipfile.ZipFile(output,"x",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for rel,payload in contents:archive.writestr(rel,payload)
        archive.writestr("PACKAGE_SHA256_MANIFEST.json",
            json.dumps(metadata,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"archive":str(output),"sha256":sha256(output.read_bytes()),
         "files":len(contents),"missing":absent,
         "includes_dataset":args.include_dataset},indent=2))
    print("Archive created locally only. REVIEW BEFORE SHARING.")

if __name__=="__main__":main()
