# When Zero Is Competitive: Transformer and Gate-Graph Surrogates on Random-Angle Quantum Circuits

**Manuscript version:** v0.5, second-round response draft, 15 November 2026  
**Authors:** [Author names and affiliations to confirm]  
**Suggested subject area:** cs.LG, with quantum-information readership; category decision pending review.  
**Evidence status:** exploratory P002 pilot, not confirmatory. Local numerical consistency PASS_COMPLETE (24 checks); a private 110-file package passed local archive checks and archived generator/simulator hashes plus 12 sampled labels matched exactly; no independent full training reproduction. **DO NOT SUBMIT UNREVIEWED.**

## Abstract

We examine supervised classical prediction of all single-qubit Z and pairwise ZZ expectation values for 4–10-qubit, noiseless layered RX/RY/RZ–CNOT circuits, using a transformer encoder and a gate-graph network. The workload stratifies qubit count, circuit depth, and path, ring or all-to-all edge-sampling families with independently uniform rotation angles. We compare a transformer-encoder baseline and gate-dependency graph neural networks under disjoint circuit-template evaluation, alongside literal-zero and training-fitted constant predictions. The observable distribution is concentrated near zero: 44.9% of 226,800 scalar training labels have absolute magnitude below 0.05. On the held-out-template panel, the literal-zero baseline achieves mean absolute error (MAE) 0.193399 under equal-instance weighting; none of the evaluated transformer endpoints or final graph-network configurations meaningfully improves this primary metric. Extending the graph-network training budget and increasing message-passing depth from 12 to 40 rounds does not resolve this failure. A separate product-state positive control nevertheless achieves MAE 0.007755 against zero-baseline MAE 0.514811. Under the training loss, mean squared error (MSE), train-fitted mean constants improve over zero by only 0.14% on the Arm K training panel; archived online graph-network minibatch MSE also remains numerically close, although exact final-model full-panel MSE is not available. These findings provide a descriptive case study demonstrating the importance of reporting constant predictors under a specified circuit/observable distribution. They neither establish that the workload is unlearnable nor identify signal concentration as the unique cause of model failure.

## 1. Introduction

Supervised surrogates seek to approximate functions of quantum-circuit structure and parameters without executing a full quantum simulation at every new query. Their appeal depends not only on accurate prediction but on demonstrating value over inexpensive reference estimators. For local Pauli observables, especially in ensembles of strongly mixing parameterised circuits, the answer zero can be an unusually strong baseline. This creates a potential evaluation pitfall: aggregate error may be low even when a model ignores its input.

For a quantum-observable surrogate, small absolute error alone can be misleading: many true expectation values may be close to zero, allowing an input-independent model to look accurate. The pilot therefore asks whether tested transformer and graph architectures extract predictive structure from a frozen circuit workload beyond inexpensive constant predictions. It is deliberately a bounded diagnostic benchmark, not an impossibility study.

We report: (i) a fixed and stratified random-rotation/CNOT workload and disjoint-template split, (ii) direct measurement of target concentration and constant-estimator performance, (iii) negative held-out-template performance for the tested transformer and graph architectures across specified training interventions, and (iv) a positive analytic product-state control alongside a restricted entangled-circuit memorisation check. Our contribution is deliberately empirical and bounded. We make no claim about quantum advantage, arbitrary circuits, or the intrinsic expressive power of all possible neural surrogates.

## 2. Related work and positioning

### 2.1 Classical prediction of circuit observables

The closest earlier study is **Cantori and Pilati (2025)**, who analyse supervised prediction of output magnetisation for circuits with random rotations interleaved with CNOTs. They show that learning cost changes markedly with *interlayer* angle variation and demonstrate successful scalable predictions under other angle-variation structures. Their experiments precede ours and already establish that rotation-angle structure can change the difficulty of quantum-circuit output learning. Our experiment is **not** the first observation of this phenomenon. Because Cantori and Pilati explicitly control structured interqubit versus interlayer angle variation, whereas P002 samples independent gate angles and mixes three rotation axes and CNOT topologies, P002 cannot be assigned unambiguously to their operational 'easy' or 'hard' regimes. It is qualitatively closer to unrestricted variation across layers, but not a matched test of their sample-complexity boundary. The present workload differs in using independently uniform RX/RY/RZ angles, multiple random CNOT connectivity families, joint prediction of all raw single- and two-qubit Z/ZZ observables, and explicit scalar versus per-instance constant baselines. This is a **protocol-level benchmarking contribution**: a workload not deliberately tuned along their interlayer-variance axis nevertheless produces competitive constant baselines in the tested models. P002 neither reproduces their stated hardness transition nor proves a new one.

**Liu et al. (2025)** show that a GNN can predict circuit outputs in distinct regimes. Their primary expectation-prediction experiment uses H/T/CNOT circuits, an attention-based graph architecture, selected/rescaled observable targets and MSE/R² evaluation. We did not reproduce or approximate their specific network as a controlled replication. Our continuous-angle GateDAG is not the same model, task or target transformation; the present negative result neither replicates nor contradicts their positive findings. Their successful study and our failed evaluated configurations differ jointly in the *gate set* (discrete H/T/CNOT versus continuous rotations), *targets* (selected/rescaled versus full raw signed Z/ZZ), *graph architecture and split* (attention-based graph and different circuit data partitioning versus a gate-wire GRU with disjoint template tests), and *evaluated settings* (their noisy and noiseless cases versus P002's noiseless-only experiments). These simultaneous differences cannot be causally disentangled by P002; they make a direct performance comparison inappropriate.

**Liao et al. (2026)** demonstrate efficient predictive surrogates under specific circuit and data-access assumptions, including experimental applications involving superconducting quantum processors. Their positive results reinforce that the learnability of observable targets is distribution and task dependent; they do not establish that generic surrogates solve the uniform-angle workload here. A separate 2026 paper on surrogate-enabled quantum error mitigation addresses a different objective and is not an equivalent noiseless regression result.

### 2.2 Quantum learning and concentration

Neural quantum states (Carleo and Troyer, 2017; Carleo, Nomura and Imada, 2018) represent wavefunctions and ground-state physics, rather than the supervised circuit-description-to-observable mapping tested here. Classical shadows (Huang, Kueng and Preskill, 2020), classical quantum-property learning (Huang et al., 2022) and theoretical observable learning separations (Molteni, Gyurik and Dunjko, 2026) each assume other data and problem settings. They provide context but do not prove that this particular task is hard.

Quantum-parameter barren plateaus (McClean et al., 2018) and Pauli-observable concentration models (Nemkov, 2025) should not be conflated with gradients of the **classical neural-network** training objective. No barren-plateau theorem or causal 'signal-starvation' mechanism follows from P002's target distribution alone.

### 2.3 Negative-result and baseline methodology

Karl et al. (2024) argue for publishing informative negative ML results; Petersen (2025) advocates explicit negative-control baselines in another benchmark field. Their methodological lesson is relevant here: when a trivial estimator is competitive, model error should be interpreted against that reference, with careful metric definitions. We do not claim these papers establish the novelty of P002.

**Novelty scope:** a narrowly specified benchmark case study with explicit near-zero target concentration, multiple architectures and exposures, same-template angle diagnostics, data-derived constant predictors and a restricted analytic positive control. The design does **not** establish that target concentration uniquely caused the failures.

## 3. Workload and data

### 3.1 Circuit family

Each circuit begins in the computational-basis product state |0>^n with n in {4,...,10}. For each n, choose r in {2,4,6} and family in {path, ring, all-to-all}, obtaining 63 balanced cells. Every round contains n independently axis-selected RX/RY/RZ gates, one per qubit, followed by n CNOT gates. Angles are drawn independently from Uniform[-pi,pi). CNOT endpoints are drawn from the permitted undirected family edges with random control–target direction. The resulting number of gates is 2nr, spanning 4n, 8n and 12n.

For every example we simulate the noiseless expectations E[Z_i] and E[Z_i Z_j] for all i and i<j. The number of valid observables is n(n+1)/2, from 10 at n=4 to 55 at n=10. Labels are deterministic, noiseless, double-precision state-vector expectations from an archived custom NumPy simulator (not measurement-shot outcomes), with separated PCG64 streams for topology and the three angle panels. The generator records RNG seeds, state snapshots, source hashes and file checksums in the dataset manifest. The exact generator is `scripts/generate_p002_data.py`. This pilot is not a claim about generic quantum circuits.

### 3.2 Split design

A circuit **template** fixes the ordered gate types, target/control qubits and CNOT connectivity, but excludes the numerical rotation angles. Per 63 (qubits, rounds, connectivity-family) cells, 30 templates were designated for train/within-template angle evaluation and 2 disjoint templates for hold-out. Each train template has 20 training-angle instances and 4 separately sampled within-template angles; each held-out template has 4 angles. All 63 cells have equal template counts, so held-out results evaluate 126 distinct templates rather than 504 independently sampled template identities. The frozen dataset contains 2,016 unique circuit templates and 45,864 angle instances: 37,800 training examples, 7,560 distinct within-template validation-angle examples, and 504 examples from held-out templates. The `K` data regime selects 30 training templates and four independent training angles per template per 63 cells (7,560 training instances). Within-template validation uses four fresh, independently drawn Uniform[-π,π) angles per rotation gate for each training template, from a separate fixed PCG64 stream; these draws use the **same angle distribution** as training but do not reuse its sampled angle instances. This panel therefore measures new-angle prediction on seen gate sequences. The held-out panel instead uses distinct gate sequences with four angles each, drawn from a third independent stream.

P002 training uses a masked per-example mean squared loss; the primary reported prediction metric is the average across examples of each example's mean absolute error over its valid observables. The equal-instance metric differs from pooling all observable scalars: n-dependent output counts cause different effective weighting. We report those statistics distinctly.

### 3.3 Trivial baselines and distribution diagnostics

A literal-zero predictor sets all predicted Z/ZZ expectations to zero. We also fit per-n/per-observable mean and median constants exclusively on Arm K training labels. No test-label fitting occurs.

Across the Arm K training scalar labels, mean absolute magnitude is 0.168849 and median absolute magnitude is 0.064561. Of 226,800 training scalar labels, 44.89% have |y|<0.05, 19.22% have |y|>0.3, and 10.48% have |y|>0.5. Similar fractions occur on the within-template and held-out panels. This is target concentration, not proof that the input-output function lacks exploitable structure.

| Per-scalar MAE | Train | Within | Held-out |
|---|---:|---:|---:|
| Literal zero | 0.168849 | 0.169009 | 0.170763 |
| Train-fitted mean constant | 0.169606 | 0.169906 | 0.171786 |
| Train-fitted median constant | 0.168833 | 0.169028 | 0.170789 |

Under the original equal-instance weighting, the Arm K held-out literal-zero MAE is 0.193399. The per-scalar value 0.170763 and equal-instance value 0.193399 are **not interchangeable**.

## 4. Model families and training

We evaluated a transformer encoder under four exploratory exposure/data arms (B, A, K and L), each with three seeds; the archived protocol documents fix its input tokenisation and selected hyperparameters. Each reported transformer configuration uses the baseline without added workspace tokens. The transformer source is derived from a pinned P001 archive using four literal substitutions (embedding dimension 64→128, feedforward dimension 128→512, encoder layers 3→4, and a corresponding 64→128 expansion). The explicit PyTorch encoder-layer call fixes four attention heads. The input packaging and positional/structural encodings inherit the archived model's `pack()` and `Model` implementation; their precise feature encoding and total parameter count still require a source-derived table before publication. The training runner fixes AdamW learning rate 0.001, weight decay 0.01, batch size 32, norm-1 gradient clipping, and evaluations every 64 updates. No LR scheduler or early-stopping rule is implemented in this runner; arms use fixed update counts.\n\n| Transformer arm | Training templates/cell | Training angles/template | Training examples across 63 cells | Updates | Seeds |\n|---|---:|---:|---:|---:|---|\n| B | 6 | 4 | 1,512 | 384 | 101, 202, 303 |\n| A | 6 | 20 | 7,560 | 384 | 101, 202, 303 |\n| K | 30 | 4 | 7,560 | 384 | 101, 202, 303 |\n| L | 6 | 4 | 1,512 | 1,920 | 101, 202, 303 |\n\nAll transformer arms use the same d=128, 4-layer, 4-head, feedforward-512 W=0 encoder with fixed hyperparameters in this candidate experiment. Transformer conclusions remain restricted to this one instantiation and these four data/exposure arms.

The independent gate-dependency graph model (GateDAG) uses gate-kind, qubit-identity, sine/cosine rotation-angle and positional embeddings, followed by gate-wire predecessor message-passing rounds with GRU cells and a shared query head. The evaluated depths were 12, 24 and 40 (with 823,809; 1,604,865; and 2,646,273 parameters respectively). Training uses AdamW (learning rate 0.001, weight decay 0.01), batch size 32, mean squared error over valid outputs, and gradient clipping at norm 1. A separate four-qubit, one-layer RY product-state control uses 2,048 training and 512 validation angle instances, seed 202 and 1,000 training updates. Its analytic targets are ⟨Zᵢ⟩=cos θᵢ and ⟨ZᵢZⱼ⟩=cos θᵢ cos θⱼ. This is deliberately easier than the entangled main task and is not a workload-matched causal intervention.

## 5. Results

### 5.1 Transformer arms

All four exploratory transformer arms and their three model seeds failed to surpass the shared literal-zero held-out-template MAE baseline 0.193399 at the evaluated checkpoints recorded in the retained console evidence. The best observed held-out MAE across those runs was approximately 0.19446. This is a descriptive **tested-configuration** result, not a proof of transformer-family incapacity or a statistically tested equivalence outcome. No formal minimum-effect or equivalence margin was preregistered.

### 5.2 GateDAG training exposure and depth

| GateDAG regime | Params | Updates | Train MAE | Held-out MAE |
|---|---:|---:|---:|---:|
| K, 12 rounds | 823,809 | 1,920 | 0.190717 | 0.193497 |
| K, 12 rounds | 823,809 | 7,680 | 0.190476 | 0.193707 |
| K, 24 rounds | 1,604,865 | 7,680 | 0.191281 | 0.194118 |
| K, 40 rounds | 2,646,273 | 7,680 | 0.191269 | 0.194155 |

The held-out literal-zero MAE is 0.193399 throughout. Training MAE also remains near 0.19 across depth and exposure interventions. A structural graph audit found a median longest gate-predecessor path of 19, a 90th percentile of 30 and a maximum of 40 nodes. The 12-round run showed a transient checkpoint at update 7,040 that beat the zero baseline by approximately 0.0000096, far smaller than the final-endpoint differences; its final endpoint failed. This near-tie is not evidence of a reliable improvement: a single GNN seed and the absence of paired uncertainty estimates prevent an inferential conclusion. The failure of deeper models weakens a simple depth-shortfall explanation within this model/optimizer; it does not rule out different message passing, skip connections or representations.

In an Arm L experiment with 1,512 training examples, final training MAE decreased to approximately 0.122, but within-template and held-out scores worsened to approximately 0.226 and 0.234, respectively. A small-data fit is therefore not sufficient for interpolation or template generalisation.

### 5.3 Positive control and restricted entangled fitting

For a product-state RY benchmark, the GateDAG achieved mean MAE 0.007755 on held-out angles, compared with literal-zero MAE 0.514811. Z and ZZ MAEs were 0.006748 and 0.008426, respectively. This demonstrates functional learning for the restricted analytic mapping, not a guarantee of correctness on the full entangled workload.

A diagnostic selected 64 actual entangled training examples from 16 n=4, r=2 path-drawn templates, with a corresponding 64 examples at independent within-template angles. After 1,500 updates, training MAE fell to 0.171882 from a literal-zero baseline of 0.402068, but fresh-angle MAE was 0.425408 against zero 0.414512. Both Z and ZZ training errors improved, yet full memorisation and reliable fresh-angle prediction were not demonstrated.

### 5.4 Training-objective MSE audit

Using equal-instance weighting, the P002 Arm K frozen-label MSE baselines are:

| MSE baseline | Train | Within | Held-out |
|---|---:|---:|---:|
| Zero | 0.095369 | 0.094946 | 0.097297 |
| Train-derived mean constant | 0.095236 | 0.094958 | 0.097276 |

The last 512 training minibatches in the D12, D24 and D40 archived logs have mean online MSE 0.094992, 0.095266 and 0.095261. These values are numerically near the train fitted-constant and literal-zero MSE baselines. **They are not matched evaluations of a fixed final model**: the model changes after every logged minibatch, and the model weights were not archived. Thus no formal equivalence test, full-panel held-out model MSE result, or claim that the fitted models are exactly constant is available.

The 10-step CUDA resource test passed even at 40 rounds, with approximately 954 MiB peak reserved memory on the 8 GB laptop GPU. Insufficient device memory did not prevent these configurations from running.

## 6. Discussion

The case study illustrates that low aggregate error on quantum-observable tasks need not indicate input-dependent predictive skill. Under this particular uniform-angle layered rotation/CNOT distribution, literal zero is close to data-derived mean and median constants on both MAE and MSE. For the chosen transformer and GateDAG training configurations, we find no held-out-template MAE advantage over literal zero.

Several distinct explanations remain compatible with the observations. Circuit-output information may be poorly preserved in the graph representation or query head; the trainability of deep graph message passing may deteriorate; the loss may favour input-independent approximations under target concentration; and the tested data/optimisation choices may be inadequate. The restricted entangled-set fitting test provides a useful train-versus-fresh-angle comparison. The analytic product-state control only checks basic pipeline functionality on an easier, unentangled target and does not test the entangled workload's representational adequacy or explain its failures. A target-concentration diagnosis should not be confused with proof of intrinsic unlearnability or causation.

The observed 44.89% near-zero scalar targets and competitiveness of the zero predictor are consistent with target concentration contributing to this failure, but do not establish it as a cause. The product-state control confirms that the GateDAG can learn an easier analytic map and does not establish any irreducible error floor for the noiseless main task; the full circuit inputs determine their simulated observable labels. Target variance is not equivalent to irreducible measurement noise. The control does not rule out deficiencies in circuit representation, entangled-case expressivity or classical optimisation. Similarly, tested GNN depth, update counts and GPU feasibility do not rule out other architectures, scaling regimes or optimization schedules. The project contains no experiment that selectively varies target concentration while otherwise holding difficulty fixed.

For benchmark design, we recommend reporting target-magnitude distributions, literal-zero predictors, train-derived constant predictors, and panel-specific MAE and MSE with identical weighting. A family of simple constant predictors—not zero alone—is the appropriate basic comparator; the observed closeness of zero and training-fitted mean/median is the substantive point. Easy-to-achieve aggregate error should be supplemented with conditional errors on high-magnitude observables and matched fixed-model evaluation when such claims are central. These are recommendations, not interventions validated in this pilot.

## 7. Limitations and threats to validity

This study is limited to 4–10 qubits, finite-depth noiseless simulated circuits, specified connectivity sampling and independently uniform rotation angles. The architecture experiments are exploratory, with no preregistered equivalence margin or paired uncertainty interval for neural-minus-zero MAE. The transformer arm metrics come from three seeds, but the detailed GateDAG depth sweep is a single seed. We did not evaluate stronger graph-network architectural variations or prove an impossibility for any network family.

The dataset has multiple observables per circuit; pooled-scalar and equal-instance metrics must not be combined without disclosure. Model-specific conditional MAE/MSE for scalar targets with |y|>0.3 and |y|>0.5 were not archived, and cannot be reconstructed from aggregate endpoint logs. Therefore these experiments cannot rule out selective model improvements on high-magnitude targets. No such conditional model outcome is claimed. The MSE audit does not include full-panel final trained-model predictions. No significance claim of indistinguishability can be supported from its minibatch standard deviations. We did not evaluate hardware data or compare total wall-clock advantages to a simulator. The numerical evidence is sufficient for a bounded descriptive case study, not a causal finding identifying signal concentration as the operative mechanism.

The motivating workspace hypothesis was not tested here because the evaluated backbones did not attain useful held-out prediction; it remains open for a future signal-rich workload.

## 8. Reproducibility and artifact status

**Code and package status.** Study code is maintained at `https://github.com/lonewolf15116/quantum-workspace-study`, a **private** GitHub repository as of this draft. A local, private, SHA-256-inventoried archive, `p002_reproducibility_v3_private.zip`, contains 110 selected files, including frozen P002 dataset records, manifests, transformer and GateDAG result logs, product-state-control evidence, experimental scripts, and archived P001 simulator/model sources. The researcher reported successful local ZIP integrity and per-member SHA-256 validation. The archive digest is `de0dc6d99c24b25fc710d82ac2eea8ce02a8a715432ea51281015e3d96fe7be4`. The archive is **not** currently available through the repository: publication of the repository alone would not publish this local ZIP.

**Numerical and source checks.** The local verifier `scripts/verify_p002_paper_evidence.py` returned `PASS_COMPLETE` with 24 enumerated checks, no missing items and no errors. `scripts/check_p002_dependencies_and_labels.py` checked the frozen dataset hashes and the generator/simulator SHA-256 hashes against the P002 manifest and recomputed 12 sampled label vectors from the archived custom NumPy `simulate()` function; all 12 matched exactly in the researcher's environment (maximum absolute error 0.0). The simulation source was extracted from `evidence/Workspace_Study_Pilot_P001.zip:run_pilot.py`. It is not a CUDA-Q or Qiskit data-generation pipeline. The NumPy `PCG64` RNG streams, seeds, initial/final states, and local Python/NumPy versions are recorded in the dataset manifest. Archived transformer code is derived from a separate P001 model archive by documented dimension substitutions.

**Boundaries.** These checks establish local integrity and *sampled* numerical regeneration, not a complete independent re-execution of the 45,864-item dataset or any GPU training run. The reported 110-file archive contains a current-environment snapshot, not a complete historical lockfile. The D12 GNN run has legacy identity metadata lacking an explicit depth field; the verifier accepts its parameter count and other metadata but cannot independently prove that run's exact original source revision. The online minibatch training-MSE logs should not be confused with fixed-model held-out MSE measurements.

Before external release, the author must inspect the archive for unintended materials and permissions, select an accessible deposit with a persistent link, and verify the deposited bytes match the recorded SHA-256. Accordingly, this draft **does not** claim that all experiments can currently be independently reproduced from a public archive.

## References (selected source entrypoints; bibliographic metadata to finalise)

1. Carleo, G., and Troyer, M. (2017). Solving the quantum many-body problem with artificial neural networks. *Science*. https://doi.org/10.1126/science.aag2302
2. Carleo, G., Nomura, Y., and Imada, M. (2018). Constructing exact representations of quantum many-body systems with deep neural networks. *Nature Communications*. https://www.nature.com/articles/s41467-018-07520-3
3. Huang, H.-Y., Kueng, R., and Preskill, J. (2020). Predicting many properties of a quantum system from very few measurements. *Nature Physics*. https://doi.org/10.1038/s41567-020-0932-7
4. McClean, J. R., et al. (2018). Barren plateaus in quantum neural network training landscapes. *Nature Communications*. https://doi.org/10.1038/s41467-018-07090-4
5. Huang, H.-Y., et al. (2022). Provably efficient machine learning for quantum many-body problems. *Science*. https://doi.org/10.1126/science.abk3333
6. Huang, H.-Y., Chen, S., and Preskill, J. (2022). Learning to predict arbitrary quantum processes. https://arxiv.org/abs/2210.14894
7. Schreiber, F. J., Eisert, J., and Meyer, J. J. (2023). Classical Surrogates for Quantum Learning Models. *Physical Review Letters*. https://doi.org/10.1103/PhysRevLett.131.100803
8. Cantori, S., and Pilati, S. (2025). Challenges and opportunities in the supervised learning of quantum circuit expectation values. *Physical Review E*. https://doi.org/10.1103/9bq5-sqhd
9. Liu, Y., et al. (2025). Output Prediction of Quantum Circuits based on Graph Neural Networks. https://arxiv.org/abs/2504.00464
10. *Demonstration of efficient predictive surrogates for large-scale quantum processors* (2026). *Nature Communications*. https://www.nature.com/articles/s41467-026-72506-5
11. Molteni, R., Gyurik, C., and Dunjko, V. (2026). Exponential quantum advantages in learning quantum observables from classical data. *npj Quantum Information*. https://www.nature.com/articles/s41534-025-01162-2
12. Karl, F., Kemeter, M., Dax, G., and Sierak, P. (2024). Position: Embracing Negative Results in Machine Learning. *ICML, PMLR 235*. https://proceedings.mlr.press/v235/karl24a.html
13. Petersen, A. H. (2025). Are You Doing Better Than Random Guessing? A Call for Using Negative Controls When Evaluating Causal Discovery Algorithms. *UAI, PMLR 286*. https://proceedings.mlr.press/v286/petersen25a.html
14. Nemkov, N. A. (2025). Statistical Models of Barren Plateaus and Anti-Concentration of Pauli Observables. *JETP Letters 122*, 190–196. https://link.springer.com/article/10.1134/S0021364025607511
15. Liao, W.-Y., Yan, G., Song, Y., et al. (2026). Sample-efficient quantum error mitigation via classical learning surrogates. *Communications Physics*. https://www.nature.com/articles/s42005-026-02827-w

---

**DRAFT CHECKLIST (NOT COMPLETE):** Confirm authorship/permissions; independently check nearest-prior-work source claims; verify exact transformer run-source identity and manuscript tables; arrange independent scientific review; inspect and publish a permitted archive if authorised; convert to arXiv-compilable LaTeX and confirm submission requirements. No arXiv submission has occurred.
