#!/usr/bin/env python3
"""P001 source-fidelity resource benchmark, dimension-substituted to d128/L4/FFN512.

Uses the archived P001 Model and pack implementation with only four audited
dimension literals changed. It is NOT a frozen confirmatory implementation.
Read-only: outputs a result JSON in the current working directory.
"""
import argparse
import hashlib
import json
import time
import types
import zipfile
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "evidence" / "Workspace_Study_P001_Diagnostics_D002.zip"
REPLACEMENTS = [
    ("self.W=W;d=64", "self.W=W;d=128"),
    ("nn.TransformerEncoderLayer(d,4,128,", "nn.TransformerEncoderLayer(d,4,512,"),
    ("),3,enable_nested_tensor=False", "),4,enable_nested_tensor=False"),
    ("expand(-1,-1,64)", "expand(-1,-1,128)"),
]


def load_original_model():
    with zipfile.ZipFile(ARCHIVE) as z:
        source = z.read("pilot_diagnostics_d002/model_from_p001.py").decode()
    original_sha = hashlib.sha256(source.encode()).hexdigest()
    modified = source
    for before, after in REPLACEMENTS:
        count = modified.count(before)
        if count != 1:
            raise RuntimeError(f"Source drift: {before!r} occurs {count} times, expected once")
        modified = modified.replace(before, after)
    mod = types.ModuleType("p001_dimension_substituted")
    exec(compile(modified, "archived_model_dimension_substituted.py", "exec"), mod.__dict__)
    return mod, original_sha, hashlib.sha256(modified.encode()).hexdigest()


def get_batch(mod, W, device):
    with zipfile.ZipFile(ROOT / "evidence" / "Workspace_Study_Pilot_P001.zip") as z:
        ledger = json.loads(z.read("templates.json"))
        rows = json.loads(z.read("instances.json"))
    mod.templates = {x["template"]: x for x in ledger}
    chosen = [x for x in rows if x["n"] == 10 and x["r"] == 6][:32]
    assert len(chosen) == 32
    packs = [mod.pack(x, W) for x in chosen]
    arrays = [torch.as_tensor(np.stack(field), device=device) for field in zip(*packs)]
    labels = torch.zeros((32, 55), dtype=torch.float32, device=device)
    for k, row in enumerate(chosen):
        labels[k, :len(row["labels"])] = torch.tensor(row["labels"], device=device)
    mask = torch.arange(55, device=device)[None, :] < arrays[7][:, None]
    return arrays, labels, mask


def measure(mod, W, device, steps):
    torch.manual_seed(404)
    mod.device = device
    model = mod.Model(W).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
    batch, labels, mask = get_batch(mod, W, device)
    stage_peaks = {"forward": 0, "backward": 0, "optimizer": 0}
    timings = []
    completed = 0
    if device == "cuda":
        torch.cuda.reset_peak_memory_stats()
    for step in range(steps):
        optimizer.zero_grad(set_to_none=True)
        if device == "cuda":
            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()
        start = time.perf_counter()
        pred = model(batch)
        loss = ((((pred-labels)**2)*mask).sum(1) / mask.sum(1)).mean()
        assert torch.isfinite(loss).item()
        if device == "cuda":
            torch.cuda.synchronize()
            stage_peaks["forward"] = max(stage_peaks["forward"],torch.cuda.max_memory_allocated())
            torch.cuda.reset_peak_memory_stats()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        if device == "cuda":
            torch.cuda.synchronize()
            stage_peaks["backward"] = max(stage_peaks["backward"],torch.cuda.max_memory_allocated())
            torch.cuda.reset_peak_memory_stats()
        optimizer.step()
        if device == "cuda":
            torch.cuda.synchronize()
            stage_peaks["optimizer"] = max(stage_peaks["optimizer"],torch.cuda.max_memory_allocated())
        timings.append(time.perf_counter()-start)
        completed += 1
    return dict(W=W, steps_completed=completed, parameter_count=sum(p.numel() for p in model.parameters()),
                final_loss=float(loss.detach().cpu()),stage_peak_allocated_MiB={k:round(v/1048576,3) for k,v in stage_peaks.items()},
                peak_reserved_MiB=round(torch.cuda.max_memory_reserved()/1048576,3) if device=="cuda" else None,
                avg_step_seconds_excluding_first=float(np.mean(timings[1:])) if len(timings)>1 else None)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--device",choices=["cpu","cuda"],default="cuda")
    p.add_argument("--steps",type=int,default=10)
    args=p.parse_args()
    if args.device=="cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA not available")
    mod, orig, changed = load_original_model()
    out = dict(status="DIMENSION_SUBSTITUTED_P001_NOT_NORMATIVE_REFERENCE",
               archived_source_sha256=orig, substituted_source_sha256=changed,
               replacements=[{"from":a,"to":b} for a,b in REPLACEMENTS],
               batch="32 actual P001 n10/r6 labelled circuit instances; not synthetic inputs",
               torch=torch.__version__,device=args.device,results=[])
    for W in (0,4):
        out["results"].append(measure(mod,W,args.device,args.steps))
    assert out["results"][1]["parameter_count"]-out["results"][0]["parameter_count"]==512
    print(json.dumps(out,indent=2))
    Path("exact_model_resource_result.json").write_text(json.dumps(out,indent=2)+"\n")


if __name__ == "__main__":
    main()
