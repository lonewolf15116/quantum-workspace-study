# P002 closest-prior-work review — source-level adjudication

**Date:** 2026-11-15  
**Review mode:** Independent descriptive comparison of directly accessible source text, rather than a proof of novelty.  
**Target manuscript:** `paper/P002_BOUNDED_NEGATIVE_RESULT_DRAFT_v01.md`.

## Primary source A: Cantori & Pilati

**Published:** Simone Cantori and Sebastiano Pilati, *Challenges and opportunities in the supervised learning of quantum circuit expectation values*, Physical Review E **112**, 015304, 21 July 2025. DOI https://doi.org/10.1103/9bq5-sqhd. Accessible early arXiv full text: https://arxiv.org/pdf/2402.04992, v1 2024, title *Challenges and opportunities in the supervised learning of quantum circuit outputs*. **Version distinction:** findings below were read in full early preprint; publication title/abstract verified from the publisher, final published full text not line-by-line compared.

**Question:** Can classical supervised neural networks accurately predict output magnetisation of circuits with single-qubit rotations interleaved with CNOTs, and how does learning cost vary with random-angle structure?

**Specific circuit/data construction:** N qubits, P layers, each containing a y-axis rotation on each qubit and adjacent-qubit CNOT gates with open boundaries. Their angles are structured as θ[n,p]=u[n]+u[p], with separate between-qubit and between-layer variation. Three regimes: (i) between-layer only, (ii) between-qubit only, and (iii) both. The target is **one global magnetisation**, m_z=(1/N)Σ_i ⟨Z_i⟩, not a vector of every Z_i and Z_i Z_j. Inputs are angle descriptor vectors or matrices rather than a gate-DAG representation. They compare MLP/CNN/LSTM and use supervised MSE with held-out **R²**, rather than a primary MAE-vs-zero evaluation. Exact state-vector simulators (Qiskit/qsimcirq) generate labels.

**Key empirical findings:** For between-layer angle fluctuations, test R² degrades rapidly with their variance; required training examples to achieve R²≥0.99 grow exponentially in that tested variance range, and MLP/CNN/LSTM behave similarly on fixed N and P. Conversely, when there are only between-qubit fluctuations, scalable CNN models can interpolate/extrapolate successfully to larger/deeper circuits. Their interpretation is learnability depends heavily on the angle-distribution structure.

**Direct overlap with P002:** Both study noiseless rotation/CNOT quantum circuits, classical supervised observable regression, and a contrast between training feasibility and challenging random-angle regimes. **This is highly relevant and arguably pre-empts a generic novelty claim about angle-induced learning failure.**

**Critical differences:** P002 uses independent Uniform[-π,π) angles on a randomly selected RX/RY/RZ axis for each gate, samples ordered CNOT edges with random direction across path/ring/all-to-all connectivity, stratifies 4–10 qubits and round budgets, predicts **all** one- and two-qubit Z/ZZ observables jointly, and evaluates a preselected held-out-template MAE against literal zero with independent within-template angles. Unlike Cantori–Pilati's structured θ[n,p] and single averaged magnetisation, P002's target-vector weighting changes the baseline and task sharply. The results cannot establish their proposed exponential sample-complexity scaling (P002 does not vary the comparable angle-variance parameter).

**Novelty implication:** Do **not** claim discovery that layered random-angle CNOT circuits are hard for neural surrogates. At most, P002 independently documents a distinct high-dimensional observable workload, its target-magnitude concentration and an explicit negative baseline comparison. A causal claim of “signal starvation” remains unverified.

Sources: https://arxiv.org/pdf/2402.04992 (Sections 2.1–3.2, Figures 1–5); https://journals.aps.org/pre/abstract/10.1103/9bq5-sqhd.

## Primary source B: Liu et al.

**Source:** Yuxiang Liu, Fanxu Meng, Lu Wang, Yi Hu, Zaichen Zhang, and Xutao Yu, *Output Prediction of Quantum Circuits based on Graph Neural Networks*, arXiv:2504.00464 (April 2025), https://arxiv.org/abs/2504.00464. Full text accessed as a ResearchGate-hosted searchable text transcription: https://www.researchgate.net/publication/390405663_Output_Prediction_of_Quantum_Circuits_based_on_Graph_Neural_Networks. **Limit:** Original arXiv PDF could not be fetched via the available web tool in this audit; numerical figure panels were not visually revalidated from the native PDF.

**Question:** Can GNNs learn selected quantum-circuit output expectation values in noisy/noiseless regimes and compare candidate parameterised circuits?

**Key distinction:** Their primary expectation-prediction task uses a **parameter-free** random gate set {T,H,CNOT} (after a gate-cancellation/simplification preprocessing step), whereas P002 uses real-valued RX/RY/RZ parameters and retained gate sequences. For the initial expectation-prediction task, Liu et al. map circuits to a DAG of input, gate and measurement nodes; encode gate type, indices, qubits and optional hardware noise metadata. They use a four-layer, two-head attention GNN with pooling of gate features and global gate/count/depth information. P002 instead uses a 12/24/40-round GRU message-passing GateDAG with final-wire-state query pairs. These are not equivalent GNNs.

**Targets and metrics:** Liu et al. use a *rescaled* Z/ZZ target, conventionally (1-⟨Z⟩)/2 for one- and two-qubit expectation values; they often predict a selected first qubit or selected first pair after relabelling. Their test criterion is **R²**, trained with MSE. P002 uses raw signed ⟨Z⟩, ⟨ZZ⟩ across all valid queries, and tests equal-instance MAE against literal zero. A zero predictor of raw Z corresponds to a different constant on Liu's rescaled scale and is not an apples-to-apples baseline.

**Scale and split:** Liu et al. report 20,000 generated circuits per configured case with 70/20/10 train/validation/test splitting, and separate 40,000-circuit extrapolation datasets. Their expectation-prediction split evaluates different circuits under this parameter-free distribution, not fresh continuous angles on the **same template** followed by disjoint continuous-angle templates as P002. Their subsequent parameterised Rx/Ry CNOT setup optimises VQE ground-state energies and the direct/indirect comparison problem; **do not conflate this VQE task with their initial expectation-value regression task.** They report successful performance in their tested settings, with a direct-vs-indirect comparison gain in their separate VQE evaluation.

**Direct overlap with P002:** Both build gate graphs and regress one- or two-qubit observables in a noiseless simulation regime. This overlaps the architecture family and output quantity but not the continuous-angle learning problem, target transformation, graph neural network, or primary metric.

**Novelty implication:** P002 cannot claim the first circuit GNN observable predictor, and Liu et al.'s successes are a counterexample to statements that *all* graph-based surrogates fail. P002 could contribute a contrasting **continuous-angle, query-rich, hard-baseline benchmark case**, provided implementation fidelity and reproducibility are verified. Do not frame it as a direct replication or contradiction.

Sources: https://arxiv.org/abs/2504.00464; ResearchGate full-text extract, Sections 3.1–4.3, especially 3.1.1, 3.1.3–3.1.5, 4.1 and 4.2.

## Head-to-head summary

| Dimension | Cantori–Pilati 2025 | Liu et al. 2025 | P002 |
|---|---|---|---|
| Core task | Magnetisation regression | Selected Z/ZZ prediction; separate PQC comparison | All raw Z/ZZ queries jointly |
| Main gates | Ry and adjacent CNOT | H/T/CNOT, nonparametric for initial regression | RX/RY/RZ and CNOT, continuous angles |
| Angle distribution | Structured θ[n,p]=u[n]+u[p] | No trainable angle in core prediction set | Independent Uniform[-π,π) |
| Target representation | Mean magnetisation | Rescaled Z/ZZ, generally selected qubit/pair | Raw signed individual/pair observables |
| Model | MLP, CNN, LSTM | Attention GNN with pooling and global features | Transformer, GRU GateDAG |
| Training/eval | MSE/R² | MSE/R² | MSE/primary held-out MAE vs zero |
| Main result | Difficult between-layer variation; easy within-layer regimes | Positive GNN predictions on its data | No useful tested held-out MAE improvement |
| P002's distinct opportunity | Quantify full query distribution and easy baseline | Test different continuous-angle query learning regime | Descriptive case study and diagnostic controls |

## Novelty verdict

**Novelty status: LIMITED / UNDER REVIEW.** A narrowly scoped methodological case study remains plausible, but the two closest sources substantially diminish the claim of a new theoretical mechanism. P002 has no evidence isolating target concentration as the *cause* of its model failure and cannot show that the underlying input-output task is inherently unlearnable. Better positioning: transparency about target distribution, equal-instance-vs-scalar weighting, matched constant baselines, same-template fresh-angle failure, and a positive product-state control.

**Important open requirement:** Check full final-publisher Cantori–Pilati methods against this preprint and visually verify Liu et al. original figure captions/tables when original PDF is available. These limits do not negate the text-level comparisons above.
