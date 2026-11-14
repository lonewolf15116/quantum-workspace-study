#!/usr/bin/env python3
"""P002 candidate four-arm W=0 study. Exploratory only, no confirmations or Git writes."""
import argparse, hashlib, json, math, os, sys, time
from pathlib import Path
import numpy as np
import torch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from bench_archived_model_d128 import load_original_model
from run_p002_probes import build_tensors, metrics

ARMS={"B":(6,4,384),"A":(6,20,384),"K":(30,4,384),"L":(6,4,1920)}
SEEDS=(101,202,303)
EVAL_EVERY=64
BATCH=32
PROTOCOL="P002-DATA-001-CANDIDATE"


def load_data(folder):
    folder=Path(folder)
    ledger=json.loads((folder/"templates.json").read_text())
    rows=json.loads((folder/"instances.json").read_text())
    manifest=json.loads((folder/"manifest.json").read_text())
    if manifest["protocol"]!=PROTOCOL or manifest["smoke"]:
        raise RuntimeError("Require complete non-smoke P002 dataset")
    for name in ("templates.json","instances.json"):
        observed=hashlib.sha256((folder/name).read_bytes()).hexdigest()
        if observed!=manifest["file_sha256"][name]:
            raise RuntimeError(f"Dataset integrity failure: {name}")
    tids={x["template"]:x for x in ledger}
    assert len(tids)==2016 and len(rows)==45864
    for x in ledger:
        assert x["n"] in range(4,11) and x["r"] in (2,4,6)
        assert (x["split"]=="train")==(x["ordinal"]<30)
    for r in rows:
        assert r["template"] in tids
        assert r["n"]==tids[r["template"]]["n"]
        assert r["r"]==tids[r["template"]]["r"]
        assert r["family"]==tids[r["template"]]["family"]
        assert ((r["panel"]=="holdout") == (tids[r["template"]]["split"]=="holdout"))
    assert len({(r["template"],r["panel"],r["angle_ordinal"]) for r in rows})==len(rows)
    return ledger,rows,manifest


def panel_indices(rows, arm):
    K,A,_=ARMS[arm]
    tr=np.array([i for i,r in enumerate(rows) if r["panel"]=="train" and r["ordinal"]<K and r["angle_ordinal"]<A],dtype=int)
    within=np.array([i for i,r in enumerate(rows) if r["panel"]=="within" and r["ordinal"]<K],dtype=int)
    hold=np.array([i for i,r in enumerate(rows) if r["panel"]=="holdout"],dtype=int)
    assert len(tr)==63*K*A and len(within)==63*K*4 and len(hold)==504
    assert not (set(tr)&set(within) or set(tr)&set(hold) or set(within)&set(hold))
    return {"train":tr,"within":within,"holdout":hold}


def eval_panels(model,arrays,y,mask,panels):
    return {k:metrics(model,arrays,y,mask,idx) for k,idx in panels.items()}


def subgroup_scores(model,arrays,y,mask,ids,rows):
    # Endpoint diagnostics only; each cell is evaluated with its own denominator.
    out={"by_n":{},"by_cell":{}}
    for n in range(4,11):
        ix=np.array([i for i in ids if rows[i]["n"]==n],dtype=int)
        out["by_n"][str(n)]=metrics(model,arrays,y,mask,ix)
    for n in range(4,11):
        for rounds in (2,4,6):
            for fam in ("path","ring","all_to_all"):
                ix=np.array([i for i in ids if (rows[i]["n"],rows[i]["r"],rows[i]["family"])==(n,rounds,fam)],dtype=int)
                out["by_cell"][f"n{n}_r{rounds}_{fam}"]=metrics(model,arrays,y,mask,ix)
    return out


def run(arm,seed,rows,mod,device,outdir,smoke=False):
    K,A,steps=ARMS[arm]
    if smoke:K,A,steps=2,2,2
    panels=panel_indices(rows,arm) if not smoke else {
        "train":np.array([i for i,r in enumerate(rows) if r["panel"]=="train" and r["ordinal"]<K and r["angle_ordinal"]<A]),
        "within":np.array([i for i,r in enumerate(rows) if r["panel"]=="within" and r["ordinal"]<K]),
        "holdout":np.array([i for i,r in enumerate(rows) if r["panel"]=="holdout"])}
    torch.manual_seed(seed)
    mod.device=device
    model=mod.Model(0).to(device)
    opt=torch.optim.AdamW(model.parameters(),lr=0.001,weight_decay=0.01)
    arrays,y,mask=build_tensors(mod,rows,device)
    train=panels["train"]
    shuffle=np.random.default_rng(seed)
    permutation=np.empty(0,dtype=int);cursor=0
    outdir.mkdir(parents=True,exist_ok=False)
    (outdir/"settings.json").write_text(json.dumps({"protocol":PROTOCOL,"arm":arm,"seed":seed,
        "K":K,"A":A,"updates":steps,"batch":BATCH,"device":device,"torch":torch.__version__,
        "training_n":len(train),"within_n":len(panels["within"]),"holdout_n":len(panels["holdout"])},indent=2)+"\n")
    start=time.perf_counter()
    with (outdir/"steps.jsonl").open("w") as sl, (outdir/"checkpoints.jsonl").open("w") as cl:
        for step in range(steps+1):
            if step>0:
                if cursor>=len(permutation):
                    permutation=shuffle.permutation(train);cursor=0
                take=permutation[cursor:cursor+BATCH];cursor+=len(take)
                ix=torch.as_tensor(take,device=device)
                model.train()
                opt.zero_grad(set_to_none=True)
                pred=model([a[ix] for a in arrays])
                loss=((((pred-y[ix])**2)*mask[ix]).sum(1)/mask[ix].sum(1)).mean()
                if not bool(torch.isfinite(loss).item()):
                    raise RuntimeError(f"Nonfinite loss arm={arm} seed={seed} step={step}")
                loss.backward()
                norm=torch.nn.utils.clip_grad_norm_(model.parameters(),1.0)
                opt.step()
                sl.write(json.dumps({"step":step,"mse":float(loss.detach().cpu()),
                    "grad_norm":float(norm.detach().cpu()),"samples":len(take)})+"\n")
            if step%EVAL_EVERY==0 or step==steps:
                rec={"step":step,"panels":eval_panels(model,arrays,y,mask,panels)}
                if step==steps and not smoke:
                    rec["holdout_diagnostics"]=subgroup_scores(model,arrays,y,mask,panels["holdout"],rows)
                cl.write(json.dumps(rec)+"\n");cl.flush()
                print(json.dumps({"arm":arm,"seed":seed,"step":step,
                    "train":rec["panels"]["train"]["mae"],"within":rec["panels"]["within"]["mae"],
                    "heldout":rec["panels"]["holdout"]["mae"],
                    "zero":rec["panels"]["holdout"]["zero_mae"]}),flush=True)
    (outdir/"summary.json").write_text(json.dumps({"arm":arm,"seed":seed,"completed_updates":steps,
        "seconds":time.perf_counter()-start,"status":"completed"},indent=2)+"\n")


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data",default="p002_dataset")
    p.add_argument("--out",default="p002_arms_results")
    p.add_argument("--arm",choices=[*ARMS,"all"],default="all")
    p.add_argument("--device",choices=["cuda","cpu"],default="cuda")
    p.add_argument("--smoke",action="store_true",help="two-step execution check only")
    args=p.parse_args()
    if args.device=="cuda" and not torch.cuda.is_available():raise RuntimeError("CUDA unavailable")
    if not args.smoke:
        ledger,rows,manifest=load_data(args.data)
    else:
        base=Path(args.data)
        ledger=json.loads((base/"templates.json").read_text())
        rows=json.loads((base/"instances.json").read_text())
    mod,original,changed=load_original_model()
    mod.templates={r["template"]:r for r in ledger}
    out=Path(args.out)
    out.mkdir(parents=True,exist_ok=False)
    (out/"identity.json").write_text(json.dumps({"protocol":PROTOCOL,"source_original":original,
        "source_substituted":changed,"smoke":args.smoke},indent=2)+"\n")
    for arm in (ARMS if args.arm=="all" else [args.arm]):
        for seed in ((101,) if args.smoke else SEEDS):
            run(arm,seed,rows,mod,args.device,out/f"{arm}_s{seed}",smoke=args.smoke)
    print("P002_ARMS_FINISHED (exploratory only)")


if __name__=="__main__":
    main()
