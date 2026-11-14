#!/usr/bin/env python3
"""P002 graph-DAG dependency-path audit (no training).

Computes the number of gate vertices in the longest directed predecessor
chain, following exactly the wire-predecessor edge policy used by GateDAG.
Reports paths by (n, rounds, family), gate count, and coverage at 12 rounds.
"""
import argparse
import collections
import hashlib
import json
import statistics
from pathlib import Path

def longest_path(gates, n):
    previous = [-1] * n
    longest = []
    edges = 0
    for kind, first, second in gates:
        affected = (first, second) if kind == 3 else (first,)
        parents = [previous[w] for w in affected if previous[w] >= 0]
        depth = 1 + max((longest[p] for p in parents), default=0)
        longest.append(depth)
        edges += len(parents)
        for w in affected:
            previous[w] = len(longest) - 1
    return max(longest, default=0), edges

def audit(folder):
    folder = Path(folder)
    manifest = json.loads((folder / "manifest.json").read_text())
    if manifest.get("protocol") != "P002-DATA-001-CANDIDATE":
        raise ValueError("Not the expected P002 dataset")
    for filename in ("templates.json", "instances.json"):
        observed = hashlib.sha256((folder / filename).read_bytes()).hexdigest()
        if observed != manifest["file_sha256"][filename]:
            raise ValueError("SHA-256 mismatch: " + filename)
    templates = json.loads((folder / "templates.json").read_text())
    by_cell = collections.defaultdict(list)
    global_depths = []
    max_gate = 0
    edge_max = 0
    for row in templates:
        length, edge_count = longest_path(row["gates"], row["n"])
        assert length <= len(row["gates"]) <= 120
        assert edge_count <= 240
        by_cell[(row["n"], row["r"], row["family"])].append(length)
        global_depths.append(length)
        max_gate = max(max_gate, len(row["gates"]))
        edge_max = max(edge_max, edge_count)
    if not manifest["smoke"]:
        assert len(templates) == 2016
        assert len(by_cell) == 63
        assert all(len(v) == 32 for v in by_cell.values())
    def summary(values):
        values = sorted(values)
        return {
            "count": len(values),
            "minimum": values[0],
            "median": statistics.median(values),
            "p90_nearest_rank": values[(9 * len(values) - 1) // 10],
            "maximum": values[-1],
            "greater_than_12": sum(x > 12 for x in values),
            "fraction_greater_than_12": sum(x > 12 for x in values) / len(values),
            "greater_than_24": sum(x > 24 for x in values),
        }
    return {
        "protocol": "P002-GRAPH-CHAIN-001",
        "definition": "gate vertices in longest path in the exact directed immediate-qubit-predecessor graph",
        "source": str(folder / "templates.json"),
        "template_sha256": manifest["file_sha256"]["templates.json"],
        "all_templates": summary(global_depths),
        "max_gates": max_gate,
        "max_edges": edge_max,
        "per_cell": {
            f"n{n}_r{r}_{fam}": summary(v)
            for (n, r, fam), v in sorted(by_cell.items())
        },
    }

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--data", default="p002_dataset")
    p.add_argument("--out", default="p002_graph_chain_audit.json")
    args = p.parse_args()
    results = audit(args.data)
    Path(args.out).write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    print(json.dumps(results["all_templates"], indent=2))
    print("max_gates", results["max_gates"], "max_edges", results["max_edges"])
    print("per-cell detail:", args.out)
