#!/usr/bin/env python3
"""P002 candidate dataset: 63 cells; nested train template/angle pools; disjoint evaluations.

Run from repository root. Never overwrites P001 evidence.
This is a candidate experiment pending independent review, not confirmatory data.
"""
import argparse, ast, hashlib, json, platform, zipfile
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "evidence" / "Workspace_Study_Pilot_P001.zip"
PROTOCOL = "P002-DATA-001-CANDIDATE"
KMAX, AMAX, AWITHIN, KHOLD, AHOLD = 30, 20, 4, 2, 4
SEEDS = dict(topology=2026111501, train_angles=2026111502,
             within_angles=2026111503, holdout_angles=2026111504)
FAMILIES = ("path", "ring", "all_to_all")


def archived_simulator():
    with zipfile.ZipFile(ARCHIVE) as z:
        source = z.read("run_pilot.py")
    tree = ast.parse(source.decode("utf-8"))
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name=="simulate"]
    assert len(functions)==1
    namespace = {"np":np}
    exec(compile(ast.Module(body=functions, type_ignores=[]), "<archived-P001-simulate>", "exec"), namespace)
    return namespace["simulate"], hashlib.sha256(source).hexdigest()


def run(smoke=False, out=None):
    simulate, source_sha = archived_simulator()
    rng = {key: np.random.Generator(np.random.PCG64(seed)) for key,seed in SEEDS.items()}
    # Fresh topology/angle streams disjoint from P001; ledger ordered canonically.
    initial_rng_states={k:v.bit_generator.state for k,v in rng.items()}
    seen=set(); ledger=[]; instances=[]; collisions=0
    cells = [(n,r,f) for n in range(4,11) for r in (2,4,6) for f in FAMILIES]
    if smoke:cells=cells[:1]
    kmax=3 if smoke else KMAX
    amax=3 if smoke else AMAX
    awithin=2 if smoke else AWITHIN
    for n,r,family in cells:
        edges=[(i,i+1) for i in range(n-1)]
        if family=="ring":edges += [(n-1,0)]
        elif family=="all_to_all":edges=[(i,j) for i in range(n) for j in range(i+1,n)]
        for ordinal in range(kmax+KHOLD):
            while True:
                gates=[]
                for _ in range(r):
                    gates += [(int(rng["topology"].integers(3)),i,10) for i in range(n)]
                    for _ in range(n):
                        i,j=edges[int(rng["topology"].integers(len(edges)))]
                        if rng["topology"].integers(2):i,j=j,i
                        gates.append((3,int(i),int(j)))
                canonical=json.dumps({"n":n,"gates":gates},sort_keys=True,separators=(",",":"))
                tid=hashlib.sha256(canonical.encode()).hexdigest()
                if tid not in seen:break
                collisions+=1
                if collisions>10000:raise RuntimeError("Excessive duplicate topology draws")
            seen.add(tid)
            split="train" if ordinal<kmax else "holdout"
            ledger.append(dict(template=tid,n=n,r=r,family=family,ordinal=ordinal,split=split,gates=gates))
            panels=[("train",amax,"train_angles"),("within",awithin,"within_angles")] if split=="train" else [("holdout",AHOLD,"holdout_angles")]
            for panel,count,stream in panels:
                for idx in range(count):
                    angles=rng[stream].uniform(-np.pi,np.pi,n*r)
                    labels,_,_=simulate(n,gates,angles)
                    if len(labels)!=n*(n+1)//2 or not np.all(np.isfinite(labels)):
                        raise RuntimeError("Bad simulator labels")
                    instances.append(dict(template=tid,n=n,r=r,family=family,ordinal=ordinal,
                        panel=panel,angle_ordinal=idx,angles=angles.tolist(),labels=labels.tolist()))
    assert len(seen)==len(ledger)
    expected=len(cells)*((kmax*(amax+awithin))+(KHOLD*AHOLD))
    assert len(instances)==expected,(len(instances),expected)
    manifest=dict(protocol=PROTOCOL,smoke=smoke,cells=len(cells),kmax=kmax,amax=amax,
        a_within=awithin,k_holdout=KHOLD,a_holdout=AHOLD,
        source_sha256=source_sha,generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        seeds=SEEDS,initial_rng_states=initial_rng_states,
        final_rng_states={k:v.bit_generator.state for k,v in rng.items()},
        python=platform.python_version(),numpy=np.__version__,
        template_count=len(ledger),instance_count=len(instances),duplicate_draws=collisions,
        train_instances=sum(r["panel"]=="train" for r in instances),
        within_instances=sum(r["panel"]=="within" for r in instances),
        holdout_instances=sum(r["panel"]=="holdout" for r in instances),
        arm_config={"B":{"K":6,"A":4,"steps":384},
                    "A":{"K":6,"A":20,"steps":384},
                    "K":{"K":30,"A":4,"steps":384},
                    "L":{"K":6,"A":4,"steps":1920}})
    if not smoke:
        # Strictly verify expected cardinalities for the 63-cell contract.
        assert len(cells)==63 and manifest["template_count"]==2016
        assert manifest["train_instances"]==37800
        assert manifest["within_instances"]==7560
        assert manifest["holdout_instances"]==504
    if out:
        target=Path(out)
        target.mkdir(parents=True,exist_ok=False)
        for name, data in (("templates.json",ledger),("instances.json",instances),("manifest.json",manifest)):
            (target/name).write_text(json.dumps(data,separators=(",",":"),sort_keys=True)+"\n",encoding="utf-8")
        manifest["file_sha256"]={x:hashlib.sha256((target/x).read_bytes()).hexdigest() for x in ("templates.json","instances.json")}
        (target/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,sort_keys=True))
    return manifest


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--smoke",action="store_true")
    p.add_argument("--out",default=None)
    args=p.parse_args()
    run(smoke=args.smoke,out=args.out)
