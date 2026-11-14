# P002-GRAPH-001 — Exploratory graph-architecture diagnostic

Date: 2026-11-15. **Status: implementation candidate, not confirmatory.**

## Proven P002 negative scope
Four-arm user-provided logs report that no inspected W=0 held-out-template checkpoint of B/A/K/L at seeds 101/202/303 beats zero predictor MAE 0.1933994668. Best reported is L seed 202 step 256: MAE 0.1944600177 (0.55% worse). A and K have 1.6 effective epochs at 384 updates while B has 8.1: failure at fixed updates does not isolate insufficient data from insufficient exposure. L shows a widening generalisation gap on its longer schedule. All results exploratory and selected from previously inspected diagnostic panels.

The **45,864 labelled instances** consist of **37,800 train-angle**, **7,560 fresh within-template angle**, **504 held-out-template**. There are 126 held-out templates with **4 angles each**, *not 64*. Data-scale review text claiming 8,064 held-out instances should not be relied upon.

## Architecture diagnostic
Implementation: `scripts/run_p002_graph_baseline.py`. Each circuit is represented as a directed graph of actual gate nodes. Edges trace the immediately previous operation on an affected qubit's wire, including both wires at a CNOT. Gate type, qubit IDs, angle sin/cos and chronological position embed each node. Twelve directed message-passing rounds with GRU updates aggregate earlier gate information. Observable queries read the final node state on each qubit and output Z and ZZ predictions using a shared head. This is a *gate-dependency DAG graph model*, not a GNN over a graph of 4-10 qubit-only vertices.

The architecture has different parameters, arithmetic, state access and inductive biases from the encoder, so this is **not** a resource-matched, equal-capacity or definitive architecture comparison. Its architectural prior is designed to test whether the negative finding is peculiar to the token encoder under these budgets.

## Primary diagnostic
Start with K arm training split (30 templates × 4 angles per cell; 7,560 training instances), seed 202, batch 32, 384 AdamW updates (LR .001, weight decay .01, gradient clip 1), common fresh-angle and held-out-template panels. Report MAE and zero MAE, their ratio, sign and output/label correlation at step 0 and every 64 updates including 384. Use *final step* for the primary fixed-step contrast, not the minimum checkpoint. If promising, replicate seeds 101 and 303 under same settings; otherwise review optimization adequacy and simple task controls before interpreting failure. Also retain training MSE per step. These are pilot choices, not preregistered claims.

## Safeguards and conclusions
- Confirm original P002 dataset file hashes before training; do not touch P001/P002 results.
- No update to Step 02B/Step 02B-R1 normative reference. The graph baseline cannot substitute for building it.
- A successful GNN result indicates at least one graph-informed learner beats zero on this panel at tested scale; it does not prove the failure is solely caused by the transformer architecture.
- A failed GNN result indicates two tested architectures failed; it does not prove the target task is intrinsically hard or unlearnable.
- Compare sample exposures and actual measured throughput; nominal optimizer steps do not mean matched compute, and extrapolating 15 ms step from the transformer is unjustified.
- A positive exploratory result requires an untouched independent panel before publication claims.
- No workspace contrast is authorised.
