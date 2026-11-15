#!/usr/bin/env python3
"""Read-only validation of local P002 evidence. No retraining or file mutation."""
import argparse
import hashlib
import json
import math
from pathlib import Path

EXPECTED = {
    12: ("p002_graph_K7680_s202", .19047649691741245, .19370665999927691),
    24: ("p002_graph_K7680_D24_s202", .19128138681839185, .19411771398200284),
    40: ("p002_graph_K7680_D40_s202", .19126903796014155, .1941549369200532),
}

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def digest(path, report):
    if not path.is_file():
        report["missing"].append(str(path))
        return False
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    report["files"][str(path)]={"sha256":h.hexdigest(),"size":path.stat().st_size}
    return True

def close(actual, expected, label, report, tol=1e-6):
    if not math.isfinite(float(actual)) or abs(float(actual)-expected)>tol:
        report["errors"].append(f"{label}: got {actual}, expected {expected}")
    else:
        report["checked"].append(label)

def run(root):
    rep={"protocol":"P002-PAPER-EVIDENCE-VERIFY-002","files":{},
         "checked":[],"missing":[],"errors":[],
         "limitations":["Checks retained file hashes and recorded endpoints, not simulator correctness or independent reproduction.",
                        "Moving-minibatch training MSE is not full-panel final-model MSE."]}
    data=root/"p002_dataset"
    mp=data/"manifest.json"
    if digest(mp,rep):
        try:
            m=read(mp)
            for name in ("templates.json","instances.json"):
                p=data/name
                if digest(p,rep) and rep["files"][str(p)]["sha256"]!=m["file_sha256"][name]:
                    rep["errors"].append(f"dataset SHA256 mismatch: {p}")
            tp=data/"templates.json";ip=data/"instances.json"
            if tp.is_file() and ip.is_file():
                templates=read(tp);rows=read(ip)
                panel={v:sum(r["panel"]==v for r in rows) for v in ("train","within","holdout")}
                rep["dataset"]={"templates":len(templates),"instances":len(rows),"panels":panel}
                if len(templates)!=2016 or len(rows)!=45864 or panel!={"train":37800,"within":7560,"holdout":504}:
                    rep["errors"].append("dataset cardinalities differ")
                else:rep["checked"].append("dataset cardinalities")
                by_id={t["template"]:t["split"] for t in templates}
                wrong=[r["template"] for r in rows if r["template"] not in by_id or
                    ((r["panel"]=="holdout")!=(by_id.get(r["template"])=="holdout"))]
                if wrong:rep["errors"].append(f"split inconsistency ({len(wrong)} rows)")
                else:rep["checked"].append("template split consistency")
        except (KeyError,ValueError,TypeError) as e:
            rep["errors"].append("dataset parsing: "+str(e))
    for layers,(dirname,train,held) in EXPECTED.items():
        folder=root/dirname
        paths=[folder/x for x in ("identity.json","checkpoints.jsonl","steps.jsonl","summary.json")]
        ready=[digest(p,rep) for p in paths]
        if not all(ready):continue
        try:
            identity=read(paths[0])
            if identity.get("layers")!=layers or identity.get("steps")!=7680 or identity.get("train_n")!=7560:
                rep["errors"].append(dirname+": identity mismatch")
            logs=[json.loads(x) for x in paths[1].read_text().splitlines() if x.strip()]
            final=[x for x in logs if x["step"]==7680]
            if len(final)!=1:rep["errors"].append(dirname+": no unique final checkpoint")
            else:
                close(final[0]["train"]["mae"],train,dirname+" train MAE",rep)
                close(final[0]["heldout"]["mae"],held,dirname+" held-out MAE",rep)
            steps=[json.loads(x) for x in paths[2].read_text().splitlines() if x.strip()]
            if len(steps)!=7680 or steps[-1]["step"]!=7680:
                rep["errors"].append(dirname+": incomplete step log")
            else:rep["checked"].append(dirname+" 7680-step log")
        except (KeyError,ValueError,TypeError,IndexError) as e:
            rep["errors"].append(dirname+": "+str(e))
    label=root/"p002_bounded_audit_s202_labels.json"
    if digest(label,rep):
        try:
            d=read(label)
            close(d["training"]["all"]["mean_abs"],.16884919185063033,"training scalar mean |y|",rep)
            close(d["training"]["all"]["fraction_near_zero_lt_0_05"],.44886243386243385,"training fraction near zero",rep)
            close(d["heldout"]["training_mean_constant_mae_per_n_observable"],.17178618129705842,"heldout mean constant MAE",rep)
        except (KeyError,ValueError,TypeError) as e:rep["errors"].append("label audit: "+str(e))
    mse=root/"p002_mse_final_readonly_audit.json"
    if digest(mse,rep):
        try:
            d=read(mse)
            close(d["panels"]["training"]["zero_mse"],.09536863930118622,"training zero MSE",rep)
            close(d["panels"]["heldout"]["zero_mse"],.09729712105490554,"heldout zero MSE",rep)
            bydepth={x["layers"]:x for x in d["run_training_logs"]}
            for depth,value in ((12,.09499172412324697),(24,.09526648460450815),(40,.09526133583131013)):
                close(bydepth[depth]["window_mean_minibatch_mse"],value,f"D{depth} online MSE",rep)
        except (KeyError,ValueError,TypeError) as e:rep["errors"].append("MSE audit: "+str(e))
    ent=root/"p002_bounded_audit_s202_entangled"
    for name in ("identity.json","checkpoints.jsonl","steps.jsonl","summary.json"):
        digest(ent/name,rep)
    cp=ent/"checkpoints.jsonl"
    if cp.is_file():
        try:
            rows=[json.loads(x) for x in cp.read_text().splitlines() if x.strip()]
            last=[x for x in rows if x["step"]==1500]
            if len(last)!=1:rep["errors"].append("entangled final checkpoint missing/duplicated")
            else:
                close(last[0]["train"]["mae"],.17188171588350087,"entangled train MAE",rep)
                close(last[0]["within"]["mae"],.42540828650817275,"entangled fresh-angle MAE",rep)
        except (KeyError,ValueError,TypeError) as e:rep["errors"].append("entangled audit: "+str(e))
    rep["status"]="PASS_COMPLETE" if not rep["missing"] and not rep["errors"] else "PARTIAL_OR_FAIL"
    return rep

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root",default=".")
    p.add_argument("--out",default="p002_paper_evidence_verification.json")
    args=p.parse_args()
    output=Path(args.out)
    if output.exists():p.error("Refusing to overwrite existing report: "+str(output))
    result=run(Path(args.root))
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("status","checked","missing","errors")},indent=2))
    print("Saved:",output)
    raise SystemExit(2 if result["errors"] else 3 if result["missing"] else 0)
