# P002 — Preliminary literature and novelty matrix (15 November 2026)

**Review scope:** Sources located via web search, mainly verified publisher abstracts/records and arXiv abstract pages. This is a **preliminary matrix**, not a systematic review or full-text independent audit. Direct similarity to P002 is ranked by target, circuit distribution, learnable architecture and learning regime. Do not assert that P002 introduces the first observation that random-angle quantum-circuit outputs can be hard to learn.

| Work | Verified link | Relation to P002 | Directness | Distinction / manuscript use |
|---|---|---|---|---|
| Cantori & Pilati (2025), *Challenges and opportunities in the supervised learning of quantum circuit expectation values*, Phys. Rev. E 112, 015304 | https://doi.org/10.1103/9bq5-sqhd ; preprint https://arxiv.org/abs/2402.04992 | Alternating random rotations and CNOT circuits; reports learning cost depending on angle variance and success in more restricted regimes | **CRITICAL / closest** | Explicitly acknowledge related learnability failure; compare distributions/targets/architecture/metrics before claiming novelty. |
| Liu et al. (2025), *Output Prediction of Quantum Circuits based on Graph Neural Networks* | https://arxiv.org/abs/2504.00464 | GNN prediction of circuit expectation values under noisy/noiseless conditions | **CRITICAL / closest** | Their positive GNN results are compatible with P002 failures because circuit families/data/tasks differ; compare graph encoding and splits. |
| *Demonstration of efficient predictive surrogates for large-scale quantum processors* (2026), Nat. Commun. | https://www.nature.com/articles/s41467-026-72506-5 | Predictive surrogates for mean observables with tailored assumptions and hardware validation up to 42 qubits | High | Contextual counterexample to general failure of surrogates; workload-specific successes. |
| Schreiber, Eisert & Meyer (2023), *Classical Surrogates for Quantum Learning Models*, Phys. Rev. Lett. 131, 100803 | https://doi.org/10.1103/PhysRevLett.131.100803 | Classical surrogates for learned quantum models; importance of classical comparison | Medium | Different target: emulate learned quantum model, not P002 graph-to-observable data. |
| Carleo & Troyer (2017), *Solving the quantum many-body problem with artificial neural networks*, Science 355 | https://doi.org/10.1126/science.aag2302 | Neural quantum states, ground states/dynamics | Background | Different setting, avoid equating NQS with supervised gate-circuit expectation surrogates. |
| Carleo, Nomura & Imada (2018), *Constructing exact representations of quantum many-body systems with deep neural networks*, Nat. Commun. 9, 5322 | https://www.nature.com/articles/s41467-018-07520-3 | Expressivity of neural representations for quantum states | Background | Mathematical representation context, not evidence for this GateDAG. |
| Huang, Kueng & Preskill (2020), *Predicting many properties of a quantum system from very few measurements*, Nat. Phys. 16 | https://doi.org/10.1038/s41567-020-0932-7 | Classical shadows for many local observables | High contextual | Uses quantum measurement sketches, not model trained from full gate list/angles. |
| Huang et al. (2022), *Provably efficient machine learning for quantum many-body problems*, Science 377 | https://doi.org/10.1126/science.abk3333 | Positive ML theory for predicting ground-state properties from data | Medium | Distinct physical input family and assumptions. |
| Huang, Chen & Preskill (2022), *Learning to predict arbitrary quantum processes* | https://arxiv.org/abs/2210.14894 | Classical learning of local output properties of processes under distributional assumptions | High | Distinguish rigorous regime from P002 empirical circuit family. |
| McClean et al. (2018), *Barren plateaus in quantum neural network training landscapes*, Nat. Commun. 9, 4812 | https://doi.org/10.1038/s41467-018-07090-4 | Concentration of measure, vanishing gradients for optimisation of parameterised quantum circuits | Contextual caution | **Do not identify P002 classical-surrogate SGD with a quantum-circuit barren plateau.** Different gradients and objectives. |
| Molteni, Gyurik & Dunjko (2026), *Exponential quantum advantages in learning quantum observables from classical data*, npj Quantum Inf. 12, 19 | https://www.nature.com/articles/s41534-025-01162-2 | Theoretical boundaries of learnability for quantum observable tasks | Medium | Theorems address other observation/access models, not a no-learnability result for P002. |
| Fanizza et al. (2024), *Learning Quantum Processes Without Input Control*, PRX Quantum 5, 020367 | https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.5.020367 | Classical-parameter-dependent quantum process statistical learning | Medium | Distinct input-control and process-learning formalisation. |
| Petersen (2025), *Are You Doing Better Than Random Guessing? A Call for Using Negative Controls When Evaluating Causal Discovery Algorithms*, UAI / PMLR 286 | https://proceedings.mlr.press/v286/petersen25a.html | Methodology of including trivial control benchmarks | Methodological analogy | Different area; useful to justify benchmark hygiene without claiming domain equivalence. |

## Priority full-text reading

1. **Cantori–Pilati 2025:** Determine whether their alternating random-rotation/CNOT setting, target distribution, variance control, and interpolation splits render P002's main observation an extension/replication rather than a new mechanism.
2. **Liu et al. 2025:** Compare their GNN graph features, encoding of two-qubit gates, noise assumptions, loss, label scaling, and evaluation split.
3. **2026 predictive-surrogate demonstration:** Contrast physically motivated restricted surrogate assumptions with P002's uniform-angle/highly mixed distribution.

## Current novelty assessment

- Established descriptive P002 finding: 44.9% of valid training labels have |y|<0.05; scalar zero MAE ~0.169, Arm K equal-instance zero held-out MAE ~0.1934; no tested transformer or GateDAG variant beats zero at held-out MAE primary endpoint.
- Possible incremental contribution: unusually transparent fixed-data split audits with literal-zero and train-fit mean/median constants, independent product-state learning check, and failure-mode stratification by data exposure and graph depth.
- **Novel discovery that uniform-random rotation-CNOT circuits are hard to learn: NOT ESTABLISHED.** Cantori & Pilati already connect circuit learning difficulty to random-angle variation.
- **Claim that signal concentration caused surrogate failure: NOT ESTABLISHED.** Model optimisation, representation and correlations have not been causally isolated.
- Negative result could be useful as a benchmark case study, but publication eligibility and scientific novelty require source-level comparisons and independent scientific review.

## Writing constraints

Use 'competitive zero predictor' rather than 'dominates all predictors'; 'under tested conditions' rather than 'intrinsically unlearnable'; 'consistent with a limited effective learning signal' rather than 'identified signal-starvation mechanism'; and distinguish stochastic online train MSE from exact held-out model MSE. Workspace intervention was not executed.

## Supplementary literature sweep — 15 November 2026 (source-qualified)

The following additional sources were verified against publisher or PMLR records. They **do not** replace the two closest comparisons above. Add only those that address a distinct concept in the paper; avoid padding the bibliography with loosely related quantum ML.

| Additional study | Publisher/source | Scope relative to P002 | Evidentiary use |
|---|---|---|---|
| Karl, Kemeter, Dax & Sierak (2024), *Position: Embracing Negative Results in Machine Learning*, ICML/PMLR 235 | https://proceedings.mlr.press/v235/karl24a.html | General value and reporting incentives for negative ML studies | Supports motivation for publishing bounded negative results; **not** proof of empirical novelty |
| Liao et al. (2026), *Demonstration of efficient predictive surrogates for large-scale quantum processors*, Nature Communications 17, 4731 | https://www.nature.com/articles/s41467-026-72506-5 | Surrogates for fixed layouts and noisy devices, practical quantum observables | Successful positive contrast; highlights importance of specified circuit distribution and data access |
| Liao et al. (2026), *Sample-efficient quantum error mitigation via classical learning surrogates*, Communications Physics | https://www.nature.com/articles/s42005-026-02827-w | Surrogate-enabled zero-noise extrapolation | Related application, but **not** equivalent to the noiseless P002 target |
| Nemkov (2025), *Statistical Models of Barren Plateaus and Anti-Concentration of Pauli Observables*, JETP Letters 122, 190–196 | https://link.springer.com/article/10.1134/S0021364025607511 | Pauli-observable concentration and quantum circuit barren-plateau statistics | Contextual physics mechanism; **do not conflate quantum-parameter gradient concentration with classical-network training dynamics** |
| Petersen (2025), *Are You Doing Better Than Random Guessing?*, UAI/PMLR 286 | https://proceedings.mlr.press/v286/petersen25a.html | Negative controls in causal discovery benchmark metrics | Methodological analogy for trivial baselines, not a direct quantum-learning baseline |
| Molteni, Gyurik & Dunjko (2026), *Exponential quantum advantages in learning quantum observables from classical data*, npj Quantum Information 12, 19 | https://www.nature.com/articles/s41534-025-01162-2 | Conditions for quantum/classical learning separations with measured-out classical data | Different access and target setting, **not** an impossibility result for P002 |

### Thematic synthesis

- **Direct novelty pressure:** Cantori–Pilati and Liu et al. remain the controlling prior art. P002 should not claim that random-angle difficulty or GNN circuit-observable prediction is new.
- **Positive counterexamples:** Liao et al. illustrate that tailored surrogate tasks can succeed; broad surrogate-failure claims are inappropriate.
- **Methodology:** Karl et al. and Petersen support framing as a reproducible benchmarking and negative-control case study, not a new loss-landscape theorem.
- **Quantum-concentration context:** Nemkov and McClean et al. address quantum parameter/observable concentration, which cannot directly establish flat *classical surrogate* optimisation gradients.
- **Reference quality:** These six entries have verified publisher/program records. Earlier entries in this matrix with arXiv-only metadata should remain tagged accordingly; total raw entries do not imply exhaustive coverage.

### Bibliography triage

**Core citations for revised manuscript:** Cantori–Pilati (2025), Liu et al. (2025), Liao et al. (2026, Nature Communications), Karl et al. (2024), McClean et al. (2018), Carleo & Troyer (2017), Huang–Kueng–Preskill (2020), Molteni et al. (2026). Add others sparingly when making the specific claim they support.
