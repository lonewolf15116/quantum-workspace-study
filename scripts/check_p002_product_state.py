#!/usr/bin/env python3
"""Analytic four-qubit product-state learnability test for the unchanged GateDAG.

One RY rotation on each qubit. Input: four rotation angles.
Targets: <Z_i>=cos(theta_i), <Z_i Z_j>=cos(theta_i)cos(theta_j).
Independent train/test angles, shared circuit structure. Diagnostic only.
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

from run_p002_graph_baseline import GateDAG, graph_features, tensors, score

PROTOCOL="P002-GRAPH-PRODUCT-001"
GATES=[(1,i,10) for i in range(4)]
TEMPLATE={"n":4,"r":1,"family":"product_ry","gates":GATES}
BATCH=32

def make_examples(count,seed):
    rng=np.random.Generator(np.random.PCG64(seed))
    rows=[]
    for index in range(count):
        angle=rng.uniform(-np.pi,np.pi,4)
        cos=np.cos(angle)
        labels=list(cos)+[cos[i]*cos[j] for i in range(4) for j in range(i+1,4)]
        assert len(labels)==10 and np.isfinite(labels).all()
        rows.append({"n":4,"angles":angle.tolist(),"labels":labels,
                     "template":"analytic_fixed_RY_product","angle_ordinal":index})
    return rows

def per_observable_types(model,features,ids,device):
    model.eval()
    z_err=[];zz_err=[];z_zero=[];zz_zero=[]
    with torch.inference_mode():
        for subset in np.array_split(ids,max(1,math.ceil(len(ids)/BATCH))):
            batch=tensors(features,subset,device)
            predictions=model(batch).cpu().numpy()
            target=batch["y"].cpu().numpy()
            for p,y in zip(predictions,target):
                z_err.append(float(np.abs(p[:4]-y[:4]).mean()))
                zz_err.append(float(np.abs(p[4:10]-y[4:10]).mean()))
                z_zero.append(float(np.abs(y[:4]).mean()))
                zz_zero.append(float(np.abs(y[4:10]).mean()))
    return {"Z_mae":float(np.mean(z_err)),"Z_zero_mae":float(np.mean(z_zero)),
            "ZZ_mae":float(np.mean(zz_err)),"ZZ_zero_mae":float(np.mean(zz_zero))}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--device",choices=["cpu","cuda"],default="cuda")
    p.add_argument("--out",default="p002_product_state_results")
    p.add_argument("--seed",type=int,default=202)
    p.add_argument("--train",type=int,default=2048)
    p.add_argument("--validation",type=int,default=512)
    p.add_argument("--steps",type=int,default=1000)
    p.add_argument("--smoke",action="store_true")
    args=p.parse_args()
    if args.smoke:args.train,args.validation,args.steps=64,32,2
    if args.device=="cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA unavailable")
    assert args.train>0 and args.validation>0 and args.steps>0
    rows=make_examples(args.train,2026111507)+make_examples(args.validation,2026111508)
    assert len({tuple(row["angles"]) for row in rows})==len(rows)
    features=[graph_features(TEMPLATE,row) for row in rows]
    train=np.arange(args.train,dtype=np.int64)
    validation=np.arange(args.train,len(rows),dtype=np.int64)
    torch.manual_seed(args.seed)
    model=GateDAG().to(args.device)
    optimizer=torch.optim.AdamW(model.parameters(),lr=.001,weight_decay=.01)
    order=np.random.default_rng(args.seed)
    perm=np.empty(0,dtype=np.int64);cursor=0
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    identity={
        "protocol":PROTOCOL,"model_source_sha256":hashlib.sha256(
            (Path(__file__).parent/"run_p002_graph_baseline.py").read_bytes()).hexdigest(),
        "test_source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "device":args.device,"torch":torch.__version__,"seed":args.seed,
        "train_samples":args.train,"validation_samples":args.validation,
        "steps":args.steps,"batch":BATCH,
        "training_angles_rng_seed":2026111507,"validation_angles_rng_seed":2026111508,
        "circuit":"four independent RY(theta_i) gates on |0000>, no entangling gates",
        "targets":"Z_i=cos(theta_i), ZZ_ij=cos(theta_i)*cos(theta_j)",
        "scope":"fixed-template angle generalization sanity test; does not test cross-template behavior"
    }
    (out/"identity.json").write_text(json.dumps(identity,indent=2)+"\n")
    start=time.perf_counter()
    with (out/"steps.jsonl").open("w") as sf,(out/"checkpoints.jsonl").open("w") as cf:
        for step in range(args.steps+1):
            if step:
                if cursor>=len(perm):
                    perm=order.permutation(train);cursor=0
                chosen=perm[cursor:cursor+BATCH];cursor+=len(chosen)
                b=tensors(features,chosen,args.device)
                optimizer.zero_grad(set_to_none=True);model.train()
                pred=model(b);y=b["y"];mask=b["ymask"]
                loss=(((pred-y).square()*mask).sum(1)/mask.sum(1)).mean()
                if not bool(torch.isfinite(loss).item()):
                    raise RuntimeError("Nonfinite loss at step "+str(step))
                loss.backward()
                norm=nn.utils.clip_grad_norm_(model.parameters(),1.)
                optimizer.step()
                sf.write(json.dumps({"step":step,"train_mse":float(loss.item()),
                    "grad_norm":float(norm.item()),"sample_count":len(chosen)})+"\n")
            if step % 100 == 0 or step==args.steps:
                test=score(model,features,validation,args.device)
                training=score(model,features,train,args.device)
                diagnostic=per_observable_types(model,features,validation,args.device)
                row={"step":step,"training":training,"validation":test,"observable_types":diagnostic}
                cf.write(json.dumps(row)+"\n");cf.flush()
                print(json.dumps({"step":step,
                    "train_mae":training["mae"],
                    "val_mae":test["mae"],"zero_val_mae":test["zero_mae"],
                    "ratio":test["ratio_to_zero"],
                    "Z_mae":diagnostic["Z_mae"],"Z_zero":diagnostic["Z_zero_mae"],
                    "ZZ_mae":diagnostic["ZZ_mae"],"ZZ_zero":diagnostic["ZZ_zero_mae"]}),flush=True)
    (out/"summary.json").write_text(json.dumps({"status":"completed",
        "elapsed_seconds":time.perf_counter()-start,"primary_step":args.steps},indent=2)+"\n")

if __name__=="__main__":main()
