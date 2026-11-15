#!/usr/bin/env python3
"""Tiny entangled-circuit memorisation test; separate from P002 study runs.

Selects 64 frozen training examples (16 different n4-r2-path templates * 4
angles); holds corresponding fresh-angle examples diagnostic-only. GateDAG
uses the unchanged model, AdamW/MSE and batch32, avoiding heldout-template
model selection. Endpoints fixed; checkpoint bests explicitly exploratory.
"""
import argparse
import hashlib
import json
import math
import time
from pathlib import Path
import numpy as np
import torch
from torch import nn
from run_p002_graph_baseline import GateDAG, graph_features, load_dataset, score, tensors

def select(rows):
    def base(row):
        return row["n"]==4 and row["r"]==2 and row["family"]=="path" and row["ordinal"]<16
    train=[r for r in rows if base(r) and r["panel"]=="train" and r["angle_ordinal"]<4]
    within=[r for r in rows if base(r) and r["panel"]=="within"]
    assert len(train)==64 and len(within)==64
    assert len(set(r["template"] for r in train))==16
    return train,within

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data",default="p002_dataset")
    p.add_argument("--out",default="p002_entangled_overfit_s202")
    p.add_argument("--seed",type=int,default=202)
    p.add_argument("--steps",type=int,default=1500)
    p.add_argument("--layers",type=int,choices=[12,24,40],default=12)
    p.add_argument("--device",choices=["cuda","cpu"],default="cuda")
    p.add_argument("--smoke",action="store_true")
    args=p.parse_args()
    if args.smoke:args.steps=2
    if args.steps<=0:raise ValueError("steps must be positive")
    if args.device=="cuda" and not torch.cuda.is_available():raise RuntimeError("CUDA not available")
    templates,rows,manifest=load_dataset(args.data,smoke=args.smoke)
    if args.smoke:
        selected=[r for r in rows if r["panel"]=="train"]
        if len(selected)<2:raise RuntimeError("small dataset has no training instances")
        train=selected[:min(2,len(selected))]
        within=selected[:min(2,len(selected))]  # only tests code path; not scientific data
    else:
        train,within=select(rows)
    by_id={r["template"]:r for r in templates}
    combined=train+within
    features=[graph_features(by_id[r["template"]],r) for r in combined]
    train_i=np.arange(len(train),dtype=np.int64)
    within_i=np.arange(len(train),len(combined),dtype=np.int64)
    torch.manual_seed(args.seed)
    model=GateDAG(layers=args.layers).to(args.device)
    optimizer=torch.optim.AdamW(model.parameters(),lr=.001,weight_decay=.01)
    order=np.random.default_rng(args.seed)
    permutation=np.empty(0,dtype=np.int64);cursor=0
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    identity={"protocol":"P002-ENTANGLED-OVERFIT-001","not_confirmatory":True,
              "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "graph_source_sha256":hashlib.sha256((Path(__file__).parent/"run_p002_graph_baseline.py").read_bytes()).hexdigest(),
              "dataset_sha256":manifest["file_sha256"],"steps":args.steps,"layers":args.layers,"seed":args.seed,
              "train_n":len(train),"within_n":len(within),"batch":32,
              "selection":"16 n4-r2-path templates, each 4 train angles and 4 independent within angles",
              "primary":"final training MAE on exactly selected 64 examples, not heldout prediction"}
    (out/"identity.json").write_text(json.dumps(identity,indent=2)+"\n")
    start=time.perf_counter()
    with (out/"steps.jsonl").open("w") as sf,(out/"checkpoints.jsonl").open("w") as cf:
        for step in range(args.steps+1):
            if step:
                if cursor>=len(permutation):
                    permutation=order.permutation(train_i);cursor=0
                ids=permutation[cursor:cursor+32];cursor+=len(ids)
                batch=tensors(features,ids,args.device)
                model.train();optimizer.zero_grad(set_to_none=True)
                pred=model(batch);y=batch["y"];mask=batch["ymask"]
                loss=(((pred-y).square()*mask).sum(1)/mask.sum(1)).mean()
                if not bool(torch.isfinite(loss).item()):raise RuntimeError("Nonfinite training loss")
                loss.backward();grad=nn.utils.clip_grad_norm_(model.parameters(),1.)
                optimizer.step()
                sf.write(json.dumps({"step":step,"mse":float(loss.item()),"grad_norm":float(grad.item())})+"\n")
            if step%100==0 or step==args.steps:
                tr=score(model,features,train_i,args.device)
                val=score(model,features,within_i,args.device)
                record={"step":step,"train":tr,"within":val}
                cf.write(json.dumps(record)+"\n");cf.flush()
                print(json.dumps({"step":step,"train_mae":tr["mae"],"train_zero":tr["zero_mae"],
                    "within_mae":val["mae"],"within_zero":val["zero_mae"]}),flush=True)
    (out/"summary.json").write_text(json.dumps({"status":"completed",
        "elapsed_seconds":time.perf_counter()-start,"primary_step":args.steps},indent=2)+"\n")

if __name__=="__main__":main()
