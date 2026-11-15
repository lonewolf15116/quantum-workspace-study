#!/usr/bin/env python3
"""Read-only P002 label audit. No model or GPU required.

Reports true per-observable (not per-example) zero MAE, train-derived mean/
median constant baselines, signal prevalence, and Z/ZZ breakdown by panel.
Selections match the frozen Arm K training and evaluation splits.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from run_p002_graph_baseline import load_dataset

def select(rows, panel, k=30, a=4):
    return [r for r in rows if r["panel"]==panel and (
        (panel=="holdout") or (r["ordinal"]<k and (panel!="train" or r["angle_ordinal"]<a)))]

def flatten(rows, type_):
    out=[]
    for r in rows:
        n=r["n"]
        z=np.asarray(r["labels"][:n],dtype=np.float64)
        zz=np.asarray(r["labels"][n:],dtype=np.float64)
        out.extend(z.tolist() if type_=="Z" else zz.tolist() if type_=="ZZ" else np.concatenate((z,zz)).tolist())
    return np.asarray(out,dtype=np.float64)

def baseline_by_observable(train, test, method="mean"):
    by_n={}
    for n in sorted({r["n"] for r in train}):
        y=np.stack([r["labels"] for r in train if r["n"]==n])
        by_n[n] = np.mean(y,axis=0) if method=="mean" else np.median(y,axis=0)
    diffs=[]
    for row in test:
        target=np.asarray(row["labels"],np.float64)
        diffs.extend(np.abs(target-by_n[row["n"]]).tolist())
    return float(np.mean(diffs))

def panel_summary(rows, train):
    results={"instances":len(rows),"observable_labels":sum(len(r["labels"]) for r in rows)}
    for kind in ("all","Z","ZZ"):
        arr=flatten(rows,kind)
        absvals=np.abs(arr)
        results[kind]={
            "labels":len(arr),
            "mean":float(arr.mean()),
            "mean_abs":float(absvals.mean()),
            "median_abs":float(np.median(absvals)),
            "std":float(arr.std()),
            "fraction_abs_gt_0_3":float(np.mean(absvals>.3)),
            "fraction_abs_gt_0_5":float(np.mean(absvals>.5)),
            "fraction_abs_gt_0_7":float(np.mean(absvals>.7)),
            "fraction_near_zero_lt_0_05":float(np.mean(absvals<.05)),
            "p90_abs":float(np.quantile(absvals,.9)),
        }
    results["training_mean_constant_mae_per_n_observable"]=baseline_by_observable(train,rows,"mean")
    results["training_median_constant_mae_per_n_observable"]=baseline_by_observable(train,rows,"median")
    return results

def run(folder):
    templates,rows,manifest=load_dataset(folder)
    armKtrain=select(rows,"train")
    within=select(rows,"within")
    holdout=select(rows,"holdout")
    assert len(armKtrain)==7560 and len(within)==7560 and len(holdout)==504
    summary={
        "protocol":"P002-LABEL-AUDIT-001",
        "source":"actual frozen P002 dataset, not simulated replacement",
        "dataset_sha256":manifest["file_sha256"],
        "arm":"K: 30 templates * 4 training angles per cell",
        "scoring_caveat":"mean_abs is literal-zero predictor MAE across all labels; original GNN score is mean of per-instance MAEs with equal instance weights, not necessarily equal observable weighting",
        "training":panel_summary(armKtrain,armKtrain),
        "within":panel_summary(within,armKtrain),
        "heldout":panel_summary(holdout,armKtrain),
    }
    return summary

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--data",default="p002_dataset")
    p.add_argument("--out",default="p002_label_audit.json")
    args=p.parse_args()
    results=run(args.data)
    Path(args.out).write_text(json.dumps(results,indent=2,sort_keys=True)+"\n")
    print(json.dumps({panel:results[panel]["all"] for panel in ("training","within","heldout")},indent=2))
    print("Full Z/ZZ and constant-baseline audit:",args.out)
