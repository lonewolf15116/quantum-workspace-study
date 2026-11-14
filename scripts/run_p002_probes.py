#!/usr/bin/env python3
"""P002 exploratory probes, W=0 only, source-fidelity d128/L4/FFN512.

Requires a successful on-device benchmark artifact in repository root.
Reads only P001 archived examples; does not generate or access a sealed test set.
Produces per-step JSONL and per-checkpoint JSONL; NEVER overwrites original P001.
"""
import argparse, collections, hashlib, json, math, sys, time, zipfile
from pathlib import Path
import numpy as np
import torch
sys.path.insert(0,str(Path(__file__).resolve().parent))
from bench_archived_model_d128 import ROOT, load_original_model

PROTOCOL="P002-PROBES-FREEZE-001"
SEED=101
LONG_UPDATES=1920
CELL_UPDATES=384
BATCH=32
EVAL_EVERY=64

def get_data():
    with zipfile.ZipFile(ROOT/"evidence"/"Workspace_Study_Pilot_P001.zip") as z:
        templates=json.loads(z.read("templates.json"))
        rows=json.loads(z.read("instances.json"))
    return templates, rows

def choose_cell(rows):
    # Entirely training-only selection, pooled per-observable variance of labels.
    pools=collections.defaultdict(list)
    for r in rows:
        if r["split"]=="train":
            pools[(r["n"],r["r"],r["family"])].append(r["labels"])
    ranking=[]
    for cell, labels in pools.items():
        y=np.array(labels,dtype=float)
        score=float(np.var(y,axis=0,ddof=0).mean())
        ranking.append((score,cell))
    ranking.sort(key=lambda x:(-x[0],x[1]))
    return ranking[0],ranking

def metrics(model, arrays, target, mask, ids):
    model.eval()
    obs=[]; gold=[]; masks=[]
    with torch.inference_mode():
        for piece in np.array_split(ids, math.ceil(len(ids)/32)):
            ix=torch.as_tensor(piece,device=target.device)
            obs.append(model([a[ix] for a in arrays]).float().cpu().numpy())
            gold.append(target[ix].float().cpu().numpy())
            masks.append(mask[ix].cpu().numpy())
    p=np.concatenate(obs);y=np.concatenate(gold);m=np.concatenate(masks)
    instance_err=(np.abs(p-y)*m).sum(1)/m.sum(1)
    zero=(np.abs(y)*m).sum(1)/m.sum(1)
    sign=(np.abs(y)>0.1)&m
    high=(np.max(np.where(m,np.abs(y),0),axis=1)>0.3)
    validp=p[m];validy=y[m]
    corr=float(np.corrcoef(validp,validy)[0,1]) if np.std(validp)>1e-12 and np.std(validy)>1e-12 else None
    return dict(n_instances=len(ids),mae=float(instance_err.mean()),zero_mae=float(zero.mean()),
      advantage_over_zero=float(zero.mean()-instance_err.mean()),
      high_signal_instances=int(high.sum()),
      high_signal_mae=float(instance_err[high].mean()) if high.any() else None,
      high_signal_zero_mae=float(zero[high].mean()) if high.any() else None,
      sign_labels=int(sign.sum()),
      sign_accuracy=float(np.mean(np.sign(p[sign])==np.sign(y[sign]))) if sign.any() else None,
      prediction_label_pearson=corr,prediction_std=float(validp.std()),
      prediction_min=float(validp.min()),prediction_max=float(validp.max()))

def build_tensors(mod,rows,device):
    packs=[mod.pack(r,0) for r in rows]
    arrays=[torch.as_tensor(np.stack(values),device=device) for values in zip(*packs)]
    y=torch.zeros((len(rows),55),dtype=torch.float32,device=device)
    for k,r in enumerate(rows):
        y[k,:len(r["labels"])]=torch.as_tensor(r["labels"],dtype=torch.float32,device=device)
    mask=torch.arange(55,device=device)[None,:]<arrays[7][:,None]
    return arrays,y,mask

def run(which,mod,rows,cell,outdir,device):
    if which=="long":
        train=np.array([k for k,r in enumerate(rows) if r["split"]=="train"])
        val=np.array([k for k,r in enumerate(rows) if r["split"]=="validation"])
        steps=LONG_UPDATES
    else:
        train=np.array([k for k,r in enumerate(rows) if r["split"]=="train" and (r["n"],r["r"],r["family"])==cell])
        val=np.array([k for k,r in enumerate(rows) if r["split"]=="validation" and (r["n"],r["r"],r["family"])==cell])
        steps=CELL_UPDATES
    assert len(train)>0 and len(val)>0
    torch.manual_seed(SEED)
    mod.device=device
    model=mod.Model(0).to(device)
    optimizer=torch.optim.AdamW(model.parameters(),lr=0.001,weight_decay=0.01)
    arrays,y,mask=build_tensors(mod,rows,device)
    order=np.random.default_rng(SEED)
    permutation=np.empty(0,dtype=int)
    cursor=0
    stem=outdir/which
    stepfile=stem.with_suffix(".steps.jsonl")
    checkfile=stem.with_suffix(".checkpoints.jsonl")
    def check(step):
        return {"protocol":PROTOCOL,"probe":which,"step":step,
                "train":metrics(model,arrays,y,mask,train),
                "validation":metrics(model,arrays,y,mask,val)}
    start=time.perf_counter()
    with stepfile.open("w") as sf, checkfile.open("w") as cf:
        cf.write(json.dumps(check(0))+"\n")
        for step in range(1,steps+1):
            if cursor>=len(permutation):
                permutation=order.permutation(train)
                cursor=0
            batch_ids=permutation[cursor:cursor+BATCH];cursor+=len(batch_ids)
            ix=torch.as_tensor(batch_ids,device=device)
            model.train()
            optimizer.zero_grad(set_to_none=True)
            pred=model([a[ix] for a in arrays])
            loss=((((pred-y[ix])**2)*mask[ix]).sum(1)/mask[ix].sum(1)).mean()
            if not bool(torch.isfinite(loss).item()):
                raise RuntimeError(f"Non-finite training loss at update {step}")
            loss.backward()
            norm=torch.nn.utils.clip_grad_norm_(model.parameters(),1.0)
            optimizer.step()
            sf.write(json.dumps({"step":step,"mse":float(loss.detach().cpu()),"grad_norm":float(norm.detach().cpu()),
                                  "samples":int(len(ix))})+"\n")
            if step%EVAL_EVERY==0 or step==steps:
                rec=check(step)
                cf.write(json.dumps(rec)+"\n");cf.flush()
                print(json.dumps({"probe":which,"step":step,"train_mae":rec["train"]["mae"],
                    "validation_mae":rec["validation"]["mae"],
                    "zero_mae":rec["validation"]["zero_mae"]}),flush=True)
    return dict(probe=which,steps=steps,train_instances=len(train),validation_instances=len(val),
                seconds=time.perf_counter()-start,step_log=str(stepfile),checkpoints=str(checkfile))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--device",choices=["cuda","cpu"],default="cuda")
    parser.add_argument("--out",default="p002_local_results")
    parser.add_argument("--run",choices=["long","cell","both"],default="both")
    parser.add_argument("--require-gpu-benchmark",action="store_true",default=False)
    args=parser.parse_args()
    if args.device=="cuda" and not torch.cuda.is_available():
        raise SystemExit("CUDA unavailable")
    if args.require_gpu_benchmark:
        p=ROOT/"exact_model_resource_result.json"
        if not p.exists():raise SystemExit("Run exact d128 GPU benchmark first from repository root.")
        b=json.loads(p.read_text())
        if b["device"]!="cuda" or any(x["steps_completed"]!=10 for x in b["results"]):
            raise SystemExit("No passing ten-step actual-model GPU benchmark.")
        if any(max(x["stage_peak_allocated_MiB"].values())>=6656 or x["peak_reserved_MiB"]>=7372.8 for x in b["results"]):
            raise SystemExit("GPU planning thresholds not met; do not run probes.")
    mod,original,substituted=load_original_model()
    template,rows=get_data()
    mod.templates={x["template"]:x for x in template}
    best,ranking=choose_cell(rows)
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    manifest=dict(protocol=PROTOCOL,device=args.device,torch=torch.__version__,numpy=np.__version__,
          seed=SEED,original_source_sha256=original,substituted_source_sha256=substituted,
          selected_cell=dict(n=best[1][0],rounds=best[1][1],family=best[1][2],train_label_variance=best[0]),
          ranking=[{"cell":c,"variance":v} for v,c in ranking],results=[])
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    for which in (["long","cell"] if args.run=="both" else [args.run]):
        manifest["results"].append(run(which,mod,rows,best[1],out,args.device))
        (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print("PROBES_COMPLETED",json.dumps({k:v for k,v in manifest.items() if k!="ranking"},indent=2))

if __name__=="__main__":
    main()
