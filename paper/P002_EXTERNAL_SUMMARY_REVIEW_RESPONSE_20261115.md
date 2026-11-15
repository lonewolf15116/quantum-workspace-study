# P002 — Response to external summary-only review (15 November 2026)

**Reviewer decision:** MAJOR REVISIONS REQUIRED.  
**Crucial scope limitation:** reviewer explicitly stated that v0.3 manuscript and private evidence were not accessible; assessment was of the invitation summary and public literature, **not a first-hand manuscript review**. Do not describe as a complete external scientific audit of the text, methods, source or ZIP.

## Decision matrix

| Review item | v0.3 evidence / status | Editorial response |
|---|---|---|
| 1.1 Constant zero may reflect target distribution | §3.3 includes train/within/heldout zero, train-fitted mean and median pooled-scalar MAE; §5.4 includes per-instance zero and mean MSE; label concentration quantified at 44.89%. | Correct claim that no diagnostics existed. Keep direct baselines, distinguish pooled-scalar and per-instance weighting. Do **not** call zero Bayes-optimal conditional on circuit inputs; only a candidate constant estimator, with no demonstrated irreducible noise. |
| 1.2 Product-state control differs from entangled workload | §5.3 reports RY product MAE .007755 vs zero .514811; §6 expressly says it does not prove causation or entangled representational adequacy. | Agree with the inferential limitation. No new experiment authorised; reduce claim weight, avoid 'isolates cause'. |
| 1.3 Title broad | Title says 'bounded evaluation' but does not name architecture, angles or target specificity. | Narrow title/scope sentence in new revision: 'When Zero Is Competitive: Transformers and Gate Graph Networks on a Random-Angle Quantum-Observable Benchmark' (proposed; author to choose). |
| 2.1 Cantori–Pilati | §2.1 and prior-work matrix describe their structured theta[n,p]=u[n]+u[p], global magnetisation and R² against P002 independent RX/RY/RZ angles, raw all-Z/ZZ MAE. | Do not assign P002 categorically to their hard/easy regime: their controlled angle-variance axis is not directly instantiated by P002. Say it is closer to unrestricted interlayer variation but **not a matched instance**. Retain novelty as diagnostic/benchmark protocol. |
| 2.2 Liu et al. | §2.1 and source-level review distinguish H/T/CNOT parameter-free expectation regression and rescaled targets from continuous rotations and a different GRU GNN. | Explicitly state not reproduced, and not a contradictory result. Check final publisher chronology when bibliography is finalised. |
| 3.1 Split protocol | §3.1–3.2 state 63 cells, 2016 templates, 45864 examples, panels and split counts. | Add a definition: template is gate kind, qubit positions, CNOT endpoints, and their order, with rotation angles excluded. A template can occur with different angles in train/within, but held-out template hashes are disjoint. Balance per cell should be stated. |
| 3.2 Metrics | §3.2 states masked instance MSE train loss and equal-instance primary heldout MAE; scalar pooled stats explicitly separated. | Do not invent pre-specified 'meaningful' margin. Report final model-to-zero descriptive differences (including D12 step7040 near-tie) and explicitly no CI/equivalence conclusion. |
| 3.3 Architecture spec | GNN hyperparameters and dimensions partly in §4; transformer exact tokenization/schedules deferred to scripts/protocol. | Genuine writing gap: add concise table of transformer architecture, hyperparams and arms only once extracted from actual code, not guessed. |
| 4.1 Data simulator | §3.1 specifies random gates, angle law, observables; §8 states custom NumPy archived state-vector simulator with PCG64. | Methods should be self-contained, with explicit source, precision and sampling process. |
| 4.2 Public access | Private archive v3, SHA256 de0dc6d99c24b25fc710d82ac2eea8ce02a8a715432ea51281015e3d96fe7be4. | Public release *not* completed; honest availability statement; make deposit only with author's explicit approval. Publishing GitHub repo alone does not publish local ZIP. |
| 4.3 Verification | §8 24 local consistency checks, source SHA match, 12 sampled exact labels; 110 member SHA inventory. | Add numbered, bounded verification checklist in supplement. These do not independently check physical quantum simulation correctness or repeat GPU training. |
| 5. Statistical uncertainty | Single-seed GNN depths; 3-seed transformer arms; held-out 504 circuits but only 126 held-out templates (2 templates/cell×4 angles). | If raw per-example predictions are absent, confidence intervals of paired prediction loss are **not reconstructible** from aggregate MAE and training logs. A descriptive study must disclose this instead of inventing intervals. A deterministic zero predictor has no *training-seed variability* on a frozen panel. |
| Reviewer claim 'irreducible noise floor' | Deterministic noiseless simulator labels from circuit structure/angles. | Variance of targets is **not** automatically irreducible error. The Bayes predictor conditional on full circuit input is the true deterministic expectation; a zero *constant* can be optimal among constants for certain target distributions, not automatically globally Bayes-optimal. |

## Scientific disposition

The submitted review is useful as a **summary-only adversarial critique**. Its 'major revision' judgment applies to information in the invitation, not to a line-by-line manuscript assessment. The manuscript does require precise title framing, standalone methods, baseline interpretation, and statistical limitation language. A fresh researcher with actual v0.4 access is still required for a genuine full-text second read.

**Non-negotiable claim boundaries**
- No blanket impossibility claim about transformer/GNN classes.
- No assertion that signal concentration was isolated as the cause.
- No equivalence inference without prespecified margin and valid paired uncertainty.
- No statement that 12 sampled labels prove all 45,864 labels reproduce or that full model training was independently repeated.
- No assertion that the private v3 ZIP is downloadable from GitHub.

## Prioritised editorial actions

1. Narrow title and specify instance-template split, deterministic/noiseless labels, and control limitations in a new draft.
2. Spell out Cantori–Pilati regime non-equivalence, Liu architecture/target differences.
3. Extract transformer exact hyperparameter table from existing archived source/results (no new experiments).
4. Add explicit public/private availability statement and reviewer-facing instructions.
5. Seek an independent reader who can actually open the full manuscript; final bibliography and figure/source inspections remain pending.

**No training, ZIP expansion, public release or arXiv submission authorised by this response.**
