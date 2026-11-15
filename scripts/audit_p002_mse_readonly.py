#!/usr/bin/env python3
"""Read-only P002 MSE audit. No model training or checkpoint selection.

Compute exact full-panel MSE constant baselines under the runner's
per-instance mask normalisation, and summarize pre-update stochastic
training minibatch MSE from the existing steps.jsonl. Logged minibatch
MSE is NOT full-panel final-model MSE: no final weights were archived.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data",default="p002_dataset")
    p.add_argument("--runs",nargs="+",default=["p002_graph_K7680_s202",
        "p002_graph_K7680_D24_s202","p002_graph_K7680_D40_s202"])
    p.add_argument("--window",type=int,default=512)
    p.add_argument("--out",default="p002_mse_final_readonly_audit.json")
    args=p.parse_args()
    if args.window<2:raise SystemExit("window must be >= 2")
    folder=Path(args.data)
    manifest=json.loads((folder/"manifest.json").read_text())
    if manifest.get("protocol")!="P002-DATA-001-CANDIDATE" or manifest.get("smoke"):
        raise SystemExit("Require full frozen P002 dataset")
    for name in ("instances.json","templates.json"):
        sha=hashlib.sha256((folder/name).read_bytes()).hexdigest()
        if sha!=manifest["file_sha256"][name]:raise SystemExit("Dataset hash mismatch: "+name)
    rows=json.loads((folder/"instances.json").read_text())
    panels={
        "training":[r for r in rows if r["panel"]=="train" and r["ordinal"]<30 and r["angle_ordinal"]<4],
        "within":[r for r in rows if r["panel"]=="within" and r["ordinal"]<30],
        "heldout":[r for r in rows if r["panel"]=="holdout"],
    }
    if [len(panels[k]) for k in ("training","within","heldout")]!=[7560,7560,504]:
        raise SystemExit("Panel sizes unexpected")
    means={}
    for n in range(4,11):
        ys=np.asarray([r["labels"] for r in panels["training"] if r["n"]==n],dtype=np.float64)
        means[n]=ys.mean(axis=0)
    result={"protocol":"P002-MSE-READONLY-001","data_sha256":manifest["file_sha256"],
            "loss":"mean over examples of mean squared error across valid observables",
            "panels":{},"run_training_logs":[],"caveat":"Logged mse is on moving pre-update model and stochastic training minibatches; it is NOT full-panel final model MSE. No saved model checkpoints were available."}
    for panel,records in panels.items():
        errors_zero=[]
        errors_mean=[]
        for row in records:
            y=np.asarray(row["labels"],dtype=np.float64)
            errors_zero.append(float(np.mean(y*y)))
            errors_mean.append(float(np.mean((y-means[row["n"]])**2)))
        mse_zero=float(np.mean(errors_zero))
        mse_mean=float(np.mean(errors_mean))
        result["panels"][panel]={
            "instances":len(records),"zero_mse":mse_zero,
            "training_fitted_mean_constant_mse":mse_mean,
            "mean_advantage_over_zero":mse_zero-mse_mean,
            "mean_ratio_to_zero":mse_mean/mse_zero,
        }
    for name in args.runs:
        directory=Path(name)
        ident=directory/"identity.json"
        steps=directory/"steps.jsonl"
        if not steps.exists() or not ident.exists():
            raise SystemExit(f"Missing original run evidence in {directory}")
        identity=json.loads(ident.read_text())
        if identity.get("arm")!="K" or identity.get("steps")!=7680 or identity.get("train_n")!=7560:
            raise SystemExit(f"Unexpected run identity in {directory}")
        rec=[json.loads(line) for line in steps.read_text().splitlines() if line.strip()]
        if len(rec)!=7680 or rec[-1]["step"]!=7680:
            raise SystemExit(f"Incomplete 7680-step log {directory}")
        tail=rec[-args.window:]
        vals=np.asarray([float(x["mse"]) for x in tail],dtype=np.float64)
        grads=np.asarray([float(x["grad_norm"]) for x in tail],dtype=np.float64)
        result["run_training_logs"].append({
            "directory":str(directory),"layers":identity.get("layers",12),
            "n_logged_steps":len(rec),"last_step_minibatch_mse":float(rec[-1]["mse"]),
            "last_window_steps":[tail[0]["step"],tail[-1]["step"]],
            "window_mean_minibatch_mse":float(vals.mean()),
            "window_std_minibatch_mse":float(vals.std()),
            "window_mean_grad_norm":float(grads.mean()),
            "window_min_grad_norm":float(grads.min()),
            "window_max_grad_norm":float(grads.max()),
            "train_zero_mse":result["panels"]["training"]["zero_mse"],
            "train_mean_constant_mse":result["panels"]["training"]["training_fitted_mean_constant_mse"],
        })
    target=Path(args.out)
    if target.exists():raise SystemExit("Refusing to overwrite: "+str(target))
    target.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"panels":result["panels"],"run_training_logs":result["run_training_logs"]},indent=2))
    print("Saved:",target)
    print("LIMITATION: logged online minibatch MSE is not exact full-panel final model MSE.")

if __name__=="__main__":main()
