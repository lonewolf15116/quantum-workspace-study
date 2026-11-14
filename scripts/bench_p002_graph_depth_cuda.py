#!/usr/bin/env python3
"""Non-study CUDA resource preflight for P002 GateDAG depths.

Runs real archived P002 training examples through forward/backward/AdamW for
ten (or chosen number of) iterations. Does not overwrite or select study
checkpoints. Each depth has fresh model and optimiser. Resource metrics are
engineering diagnostics, not learning-effect comparisons.
"""
import argparse, hashlib, json, time
from pathlib import Path
import numpy as np
import torch
from run_p002_graph_baseline import GateDAG, graph_features, tensors, load_dataset

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--data",default="p002_dataset")
    parser.add_argument("--depths",type=int,nargs="+",choices=[12,24,40],default=[12,24,40])
    parser.add_argument("--steps",type=int,default=10)
    parser.add_argument("--batch",type=int,default=32)
    parser.add_argument("--out",default="p002_graph_depth_cuda_preflight.json")
    args=parser.parse_args()
    if not torch.cuda.is_available():raise SystemExit("CUDA unavailable; no GPU-fit claim")
    if args.steps<2 or args.batch!=32:raise SystemExit("Preflight contract requires >=2 steps, batch 32")
    ledger, rows, manifest=load_dataset(args.data)
    by_id={x["template"]:x for x in ledger}
    idx=[i for i,r in enumerate(rows) if r["panel"]=="train" and
         r["ordinal"]<30 and r["angle_ordinal"]<4][:args.batch]
    if len(idx)!=args.batch:raise RuntimeError("Insufficient arm K training rows")
    features=[graph_features(by_id[rows[i]["template"]],rows[i]) for i in idx]
    batch=tensors(features,np.arange(args.batch),device="cuda")
    result=dict(protocol="P002-GRAPH-DEPTH-CUDA-PREFLIGHT-001",
                training_source="P002 Arm K first 32 real instances; labels included",
                data_sha256=manifest["file_sha256"],batch=args.batch,steps=args.steps,
                torch=torch.__version__,gpu=torch.cuda.get_device_name(),
                gpu_memory_MiB=round(torch.cuda.get_device_properties(0).total_memory/1048576,3),
                results=[])
    for depth in args.depths:
        torch.cuda.empty_cache()
        torch.manual_seed(202)
        model=GateDAG(layers=depth).cuda()
        optimizer=torch.optim.AdamW(model.parameters(),lr=.001,weight_decay=.01)
        per_step=[]
        peak_alloc=0
        peak_reserved=0
        finite=True
        try:
            for step in range(args.steps):
                optimizer.zero_grad(set_to_none=True)
                torch.cuda.synchronize()
                torch.cuda.reset_peak_memory_stats()
                started=time.perf_counter()
                pred=model(batch)
                loss=(((pred-batch["y"]).square()*batch["ymask"]).sum(1)/batch["ymask"].sum(1)).mean()
                if not bool(torch.isfinite(loss).item()):
                    finite=False
                    raise RuntimeError("Nonfinite loss")
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
                optimizer.step()
                torch.cuda.synchronize()
                per_step.append(time.perf_counter()-started)
                peak_alloc=max(peak_alloc,torch.cuda.max_memory_allocated())
                peak_reserved=max(peak_reserved,torch.cuda.max_memory_reserved())
            status="PASS"
            error=None
        except torch.cuda.OutOfMemoryError as e:
            status="OOM"
            error=str(e)
        except Exception as e:
            status="ERROR"
            error=str(e)
        result["results"].append(dict(depth=depth,status=status,error=error,
            completed=len(per_step),parameters=sum(p.numel() for p in model.parameters()),
            peak_allocated_MiB=round(peak_alloc/1048576,3),
            peak_reserved_MiB=round(peak_reserved/1048576,3),
            mean_step_seconds_excluding_first=round(float(np.mean(per_step[1:])),6) if len(per_step)>1 else None,
            last_loss=float(loss.detach().cpu()) if len(per_step)>0 else None))
        del model,optimizer
        torch.cuda.empty_cache()
        if status!="PASS":break
    Path(args.out).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    if len(result["results"])!=len(args.depths) or any(x["status"]!="PASS" for x in result["results"]):
        raise SystemExit("Depth preflight failed; do not run full depth training")
if __name__=="__main__":main()
