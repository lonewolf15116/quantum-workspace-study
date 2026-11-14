#!/usr/bin/env python3
"""Exploratory circuit-DAG message-passing baseline on frozen P002 data.

Graph nodes: gates in circuit order. Directed incoming edges from preceding
gates on involved wires (including control and target for CNOT).
Outputs Z_i and Z_i Z_j from final wire-state gate nodes.
No torch-geometric dependency. No workspace tokens. Not resource matched.
"""
import argparse, hashlib, json, math, time
from pathlib import Path
import numpy as np
import torch
from torch import nn

PROTOCOL="P002-GRAPH-001-CANDIDATE"
ARMS={"B":(6,4),"A":(6,20),"K":(30,4),"L":(6,4)}
NODES=120
EDGES=240
BATCH=32

def load_dataset(folder,smoke=False):
    folder=Path(folder)
    manifest=json.loads((folder/"manifest.json").read_text())
    if manifest.get("protocol")!="P002-DATA-001-CANDIDATE" or (manifest.get("smoke") and not smoke):
        raise RuntimeError("Expected complete P002 data and manifest")
    for name in ("templates.json","instances.json"):
        digest=hashlib.sha256((folder/name).read_bytes()).hexdigest()
        if digest!=manifest["file_sha256"][name]:raise RuntimeError("Dataset hash mismatch "+name)
    templates=json.loads((folder/"templates.json").read_text())
    instances=json.loads((folder/"instances.json").read_text())
    if not smoke:assert len(templates)==2016 and len(instances)==45864
    return templates,instances,manifest

def graph_features(template,row):
    n=template["n"]; gates=template["gates"]; angles=iter(row["angles"])
    typ=np.zeros(NODES,np.int64); wires=np.zeros((NODES,2),np.int64)
    angle=np.zeros((NODES,2),np.float32); valid=np.zeros(NODES,np.float32)
    src=np.zeros(EDGES,np.int64);dst=np.zeros(EDGES,np.int64);emask=np.zeros(EDGES,np.float32)
    previous=[-1]*n; edge=0
    for t,(kind,i,j) in enumerate(gates):
        if t>=NODES:raise RuntimeError("Gate count exceeds fixed node budget")
        typ[t]=kind;wires[t]=[i,j if kind==3 else 10];valid[t]=1.
        if kind!=3:
            theta=next(angles);angle[t]=[np.sin(theta),np.cos(theta)]
        touched=(i,j) if kind==3 else (i,)
        for wire in touched:
            if previous[wire]>=0:
                if edge>=EDGES:raise RuntimeError("Edge overflow")
                src[edge]=previous[wire];dst[edge]=t;emask[edge]=1.;edge+=1
        for wire in touched:previous[wire]=t
    q=n*(n+1)//2
    qi=np.zeros(55,np.int64);qj=np.zeros(55,np.int64);qtype=np.zeros(55,np.int64)
    idx=0
    for i in range(n):qi[idx]=i;qj[idx]=i;idx+=1
    for i in range(n):
        for j in range(i+1,n):qi[idx]=i;qj[idx]=j;qtype[idx]=1;idx+=1
    assert idx==q
    return dict(typ=typ,wires=wires,angle=angle,valid=valid,src=src,dst=dst,
        emask=emask,last=np.asarray([max(x,0) for x in previous]+[0]*(10-n),np.int64),
        qi=qi,qj=qj,qtype=qtype,
        y=np.pad(np.asarray(row["labels"],np.float32),(0,55-q)),
        ymask=np.asarray([1.]*q+[0.]*(55-q),np.float32))

class GateDAG(nn.Module):
    def __init__(self,width=96,layers=12):
        super().__init__();d=width
        self.kind=nn.Embedding(4,d);self.wire=nn.Embedding(11,d)
        self.angle=nn.Linear(2,d,bias=False)
        self.position=nn.Embedding(NODES,d)
        self.input=nn.LayerNorm(d)
        self.msg=nn.ModuleList([nn.Linear(d,d,bias=False) for _ in range(layers)])
        self.cells=nn.ModuleList([nn.GRUCell(d,d) for _ in range(layers)])
        self.qtype=nn.Embedding(2,16)
        self.read=nn.Sequential(nn.Linear(3*d+16,d),nn.GELU(),nn.Linear(d,1))
    def forward(self,b):
        B=b["typ"].shape[0];d=self.kind.embedding_dim
        pos=torch.arange(NODES,device=b["typ"].device).unsqueeze(0)
        h=self.input(self.kind(b["typ"])+self.wire(b["wires"][:,:,0])+
                     self.wire(b["wires"][:,:,1])+self.angle(b["angle"])+self.position(pos))
        mask=b["valid"].unsqueeze(-1)
        h=h*mask
        offsets=(torch.arange(B,device=h.device)*NODES)[:,None]
        source=(b["src"]+offsets).reshape(-1)
        target=(b["dst"]+offsets).reshape(-1)
        em=b["emask"].reshape(-1,1)
        for projection,cell in zip(self.msg,self.cells):
            message=projection(h).reshape(B*NODES,d)[source]*em
            pooled=torch.zeros((B*NODES,d),device=h.device,dtype=h.dtype)
            pooled.index_add_(0,target,message)
            h=cell(pooled,h.reshape(-1,d)).reshape(B,NODES,d)*mask
        last=b["last"].unsqueeze(-1).expand(-1,-1,d)
        wire_state=h.gather(1,last)
        qi=b["qi"].unsqueeze(-1).expand(-1,-1,d)
        qj=b["qj"].unsqueeze(-1).expand(-1,-1,d)
        first=wire_state.gather(1,qi);second=wire_state.gather(1,qj)
        z=self.qtype(b["qtype"])
        return self.read(torch.cat((first,second,first*second,z),dim=-1)).squeeze(-1)

def tensors(features, ids, device):
    return {key:torch.as_tensor(np.stack([features[int(i)][key] for i in ids]),device=device)
            for key in features[0]}

def score(model,features,indices,device):
    model.eval();errors=[];zeros=[];sigs=[];pearson_p=[];pearson_y=[]
    with torch.inference_mode():
        for ids in np.array_split(indices,max(1,math.ceil(len(indices)/BATCH))):
            b=tensors(features,ids,device);p=model(b);y=b["y"];m=b["ymask"]
            errors.extend((((p-y).abs()*m).sum(1)/m.sum(1)).cpu().tolist())
            zeros.extend(((y.abs()*m).sum(1)/m.sum(1)).cpu().tolist())
            selected=(y.abs()>0.1)&m.bool()
            if selected.any():
                sigs.extend((torch.sign(p[selected])==torch.sign(y[selected])).cpu().tolist())
            pearson_p.extend(p[m.bool()].cpu().tolist());pearson_y.extend(y[m.bool()].cpu().tolist())
    corr=float(np.corrcoef(pearson_p,pearson_y)[0,1]) if np.std(pearson_p)>1e-12 else None
    return {"instances":len(indices),"mae":float(np.mean(errors)),"zero_mae":float(np.mean(zeros)),
            "ratio_to_zero":float(np.mean(errors)/np.mean(zeros)),
            "sign_accuracy":float(np.mean(sigs)) if sigs else None,
            "prediction_label_pearson":corr}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data",default="p002_dataset")
    p.add_argument("--out",default="p002_graph_results")
    p.add_argument("--arm",choices=list(ARMS),default="K")
    p.add_argument("--seed",type=int,choices=[101,202,303],default=202)
    p.add_argument("--steps",type=int,default=None)
    p.add_argument("--layers",type=int,choices=[12,24,40],default=12)
    p.add_argument("--device",choices=["cuda","cpu"],default="cuda")
    p.add_argument("--smoke",action="store_true")
    args=p.parse_args()
    if args.steps is None:args.steps=1920 if args.arm=="L" else 384
    if args.steps<=0:raise ValueError("steps must be positive")
    if args.device=="cuda" and not torch.cuda.is_available():raise RuntimeError("CUDA unavailable")
    templates,rows,manifest=load_dataset(args.data,smoke=args.smoke)
    templates={x["template"]:x for x in templates}
    features=[graph_features(templates[x["template"]],x) for x in rows]
    K,A=ARMS[args.arm]
    tr=np.array([i for i,r in enumerate(rows) if r["panel"]=="train" and
                 r["ordinal"]<K and r["angle_ordinal"]<A],dtype=np.int64)
    within=np.array([i for i,r in enumerate(rows) if r["panel"]=="within" and r["ordinal"]<K],dtype=np.int64)
    held=np.array([i for i,r in enumerate(rows) if r["panel"]=="holdout"],dtype=np.int64)
    if not args.smoke:assert len(tr)==63*K*A and len(held)==504
    if args.smoke:
        tr=tr[:32];within=within[:32];held=held[:32];args.steps=2
    device=args.device
    torch.manual_seed(args.seed)
    model=GateDAG(layers=args.layers).to(device)
    optimizer=torch.optim.AdamW(model.parameters(),lr=0.001,weight_decay=0.01)
    order=np.random.default_rng(args.seed);perm=np.empty(0,dtype=np.int64);cursor=0
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    identity={"protocol":PROTOCOL,"P002_dataset_manifest":str(Path(args.data)/"manifest.json"),
              "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "arm":args.arm,"seed":args.seed,"steps":args.steps,"layers":args.layers,"torch":torch.__version__,
              "device":device,"parameters":sum(p.numel() for p in model.parameters()),
              "train_n":len(tr),"within_n":len(within),"holdout_n":len(held),
              "NOTES":"Not compute matched to transformer. Exploratory architecture baseline."}
    (out/"identity.json").write_text(json.dumps(identity,indent=2)+"\n")
    start=time.perf_counter()
    with (out/"steps.jsonl").open("w") as sl,(out/"checkpoints.jsonl").open("w") as cl:
        for step in range(args.steps+1):
            if step:
                if cursor>=len(perm):perm=order.permutation(tr);cursor=0
                ids=perm[cursor:cursor+BATCH];cursor+=len(ids)
                batch=tensors(features,ids,device);model.train()
                optimizer.zero_grad(set_to_none=True)
                pred=model(batch);y=batch["y"];mask=batch["ymask"]
                loss=(((pred-y).square()*mask).sum(1)/mask.sum(1)).mean()
                if not bool(torch.isfinite(loss).item()):raise RuntimeError("Nonfinite loss")
                loss.backward();grad=torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
                optimizer.step()
                sl.write(json.dumps({"step":step,"mse":float(loss.item()),
                    "grad_norm":float(grad.item()),"samples":len(ids)})+"\n")
            if step%64==0 or step==args.steps:
                record={"step":step,"train":score(model,features,tr,device),
                    "within":score(model,features,within,device),
                    "heldout":score(model,features,held,device)}
                cl.write(json.dumps(record)+"\n");cl.flush()
                print(json.dumps({"step":step,"train":record["train"]["mae"],
                    "within":record["within"]["mae"],"within_zero":record["within"]["zero_mae"],
                    "heldout":record["heldout"]["mae"],"zero":record["heldout"]["zero_mae"]}),flush=True)
    (out/"summary.json").write_text(json.dumps({"status":"completed","elapsed_s":time.perf_counter()-start},indent=2)+"\n")
if __name__=="__main__":main()
