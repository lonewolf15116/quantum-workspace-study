# Workspace study — Step 01: architecture specification

Date: 2026-11-14
Revision: Step 01 r3, WORKLOAD-002 contrast annotation.
Status: revised implementation specification; not preregistered, no experiments run.
Basis: conversation protocol v0.3, with subsequent technical corrections retained.

## Agreed scientific boundary

The primary question is whether four dedicated non-input positions improve template-averaged observable MAE relative to one compute-matched no-workspace model, subject to a hard parameter-tolerance gate. This does not isolate role separation. The parameter-matched model is secondary and cannot rescue the primary result. Gate and query positions already provide computational capacity.

## Step 01 decisions

The following are concrete engineering choices proposed for the specification, not empirical findings or previously approved numerical freezes.

| Component | Specification |
|---|---|
| Model | Bidirectional transformer encoder; pre-layer-normalisation; residual attention and FFN blocks |
| Reference backbone | 4 layers, width 128, 4 attention heads, FFN hidden width 512 |
| Activation | Erf-based GELU: x/2 * (1 + erf(x/sqrt(2))); transcendental calls reported separately from elementary arithmetic |
| Normalisation | LayerNorm epsilon 1e-5, affine parameters; final LayerNorm |
| Dropout | Zero for the initial design, identical across conditions |
| Linear layers | Bias enabled, including Q/K/V/output and FFN projections |
| Input | One token per gate; qubit indices zero-based |
| Gate vocabulary | H, X, RX, RY, RZ, CNOT; rotations in radians |
| Scope | 4–10 qubits; at most 128 gate tokens per instance |
| Query set | All Z_i and all Z_i Z_j for i<j; Q=n(n+1)/2 |
| Workspace | 4 learned vectors for reference, 0 for baseline; 2 and 8 secondary |
| Attention | Full bidirectional attention among all non-padding positions in every layer |
| Readout | Shared affine scalar head on each final query representation; no workspace/gate head; no output clipping |
| Loss | Mean squared error, average over queries within instance, then instances; evaluation remains MAE |

### Token construction

Each gate token sums learned gate-type, ordered first-qubit, ordered second-qubit, role, qubit-count and gate-position embeddings plus one bias-free 2-to-d linear projection of (sin(theta), cos(theta)), shared across RX, RY and RZ; the gate-type embedding distinguishes axes. Nonrotation gates use (0,0). A dedicated NONE index identifies the absent second qubit. Gate positions are indexed within the gate sequence, independent of query/workspace count.

Query tokens sum observable-type (Z or ZZ), ordered qubit-index, query-role and qubit-count embeddings. For ZZ, i<j. For Z, the second index is NONE. Queries have no gate-position embedding. They are ordered first by single-qubit index, then lexicographically by pair. This fixes query identity without shifting gate positions when workspace is added.

The role embeddings come from one shared three-row table (gate, query, workspace). Ordered first/second-qubit tables and the qubit-count table are shared between gate and query tokens. Workspace tokens are four distinct learned vectors plus the workspace-role row. They receive no circuit-specific initial features or positional embedding and evolve through all blocks. Workspace identity resides in learned vectors rather than slot position; permuting workspace vectors permutes their states without changing query outputs in exact arithmetic. Sequence layout is gates, queries, workspace. Padding is a batch implementation detail: padded keys are masked, padded outputs ignored, and executed padded operations must still be counted unless actually skipped.

This provides up to 55 queries at 10 qubits. A maximum-length reference sequence therefore has 128+55+4=187 non-padding positions. The query count is part of the resource budget and may reduce the incremental value of workspace; it is not changed to obtain an effect.

### Primary metric weighting

Each observable has equal weight within an instance, each angle instance equal weight within its template, and each test template equal weight in the final score. Because all pairs are included, ZZ terms receive more aggregate weight at larger n. Report single-Z and ZZ errors separately as secondary diagnostics. This choice is explicit rather than an accidental consequence of query sampling.

## Candidate comparator grid

Enumerate widths {96,112,128,144,160}, depths {3,4,5}, four heads, and FFN width 4d. All 15 no-workspace candidates share tokenisation, attention, readout and bias conventions. The reference is fixed at d=128, L=4, W=4; the engineering pilot also includes its same-backbone W=0 counterpart. The same-backbone pair is eligible but not automatically selected. If the deterministic rule selects it, it serves as the primary compute-matched comparator and this identity is disclosed. The secondary parameter-matched comparator cannot rescue a failed or unavailable primary comparison.

Do not train every candidate to select the primary comparator. Compute parameters and operations analytically, filter by the hard compute and parameter tolerances, then select the smallest absolute FLOP distance, then fewer parameters, then lower depth, then lexicographic configuration ID. Empty eligibility means the primary comparison is unavailable as specified. Tolerances and workload remain unresolved; no selected matched model is claimed here.

## Remaining sequence of work

1. Architecture specification — this document; cross-check implementation details before freeze.
2. Exact operation accounting and parameter enumeration — distinguish MAC=2 FLOPs, non-matmul costs, padding and wall-clock measurements; specify the workload distribution and tolerances.
3. Dataset generator, template normalisation/hashing, leakage rules and label verification specification.
4. Literature matrix and bounded independent review before registration; novelty remains unverified.
5. Meaningful-margin rule and statistical analysis specification. No margin based on pilot variance or discretionary fallback baseline. Seed/template interaction and cell residual must not be claimed separately identifiable from one observation per cell.
6. Freeze pre-pilot methods, run zero/four engineering pilot, estimate feasibility and precision, then freeze confirmatory counts and sealed test manifest.

Training schedule, optimiser, batch construction, workload probabilities, tolerances, margin and sample sizes remain pending. No confirmatory run is authorised by an assertion that these are already frozen. No novelty, GPU-fit, runtime or performance claim has been established.

## Change control

This is the first saved architecture annex, not a replacement for a completed preregistration. Future changes must state date, reason and whether any pilot/test outcomes were available. A cryptographic freeze digest will be produced for the complete protocol/configuration package once the pending specifications are resolved.


## Review resolution r1 — 2026-11-14

### Gate-cap enforcement

Generate templates within a gate budget of at most 128 from the outset, counting the actual encoded elementary gates after any macro expansion. Do not truncate input or circuits. Any generator violation is an error that blocks dataset sealing; it is not silently filtered or replaced. Store intended gate budget, realised gate count, qubit count, family and separately defined circuit depth per template. Publish realised template and instance gate-count/depth distributions and any failed generation counts. Angle draws cannot change topology or gate count. Labels are computed on exactly the circuit encoded in the input.

### Workload and comparator eligibility

Step 02 must explicitly specify probabilities over qubit counts and gate counts, query count Q=n(n+1)/2, and batching/padding. Selection uses expected operations over that declared workload, not the n=10 maximum-length example. Report aggregate and per-workload-cell differences, as well as parameters. Filter by both hard tolerances before tie-breaking. Do not widen tolerances after discovering an empty eligible set without a dated pre-outcome amendment. The review's approximate counts are illustrative, not validated full counts: no claim about grid eligibility is accepted before exact enumeration.

### Selected uncertainty remedy: crossed resampling, no interaction decomposition

Choose the analysis fix. Define D[s,t] as the paired difference in template-averaged absolute error for training-run pair s and template group t. Observables and angle instances are averaged before constructing D. The estimand averages over training randomness and independent template groups, each containing its fixed generated angle set; inference does not separately estimate uncertainty conditional on a template from infinitely many new angle draws.

Use a two-way product (pigeonhole) bootstrap: independently sample S run-pair indices and T template-group indices with replacement, form their Cartesian submatrix of D, and average it. Use 10,000 bootstrap replicates with a recorded independent RNG stream and a two-sided 95% percentile interval. Both architectures remain paired in every resampled cell. Do not fit or report separately identified interaction and cell-residual variances. Retain original cell data and report variability without claiming that decomposition. Reference: Art B. Owen, The pigeonhole bootstrap (2007), https://arxiv.org/abs/0712.1111.

This procedure addresses both crossed sources but has no blanket finite-sample coverage guarantee. Validate coverage through prespecified synthetic scenarios with seed, template and cell effects before confirmation; publish that validation even if unfavourable. Three pilot seeds are diagnostic, not adequate evidence of reliable confirmatory interval coverage. If validation is inadequate, amend and review the analysis before accessing confirmatory outcomes. Do not choose among estimators by interval width or observed significance.

Taking the maximum of seed-only and template-only clustered variances is not accepted as automatically conservative: each can miss the other's positive variance contribution. Multiple angle instances alone do not justify a simple independent residual model either, since the same instances are evaluated by every trained model.

### RZ relevance and generator checks

RZ commutes with immediate Z measurement, but later H, RX, RY or downstream interactions can change whether its phase affects a target. Merely appearing before H is not sufficient to establish relevance, and appearing after the last H does not prove irrelevance. Step 03 must include analytically verified phase-sensitive cases (for example H, RZ(theta), H on |0>) and explicitly tagged phase-insensitive cases. Record structural relevance guarantees separately from numerical sensitivity diagnostics; do not call a gate a mathematical no-op because selected probes show negligible change. Main-family mixture and sensitivity-check thresholds remain to be specified before the pilot.

### Loss and prediction diagnostics

MSE training with MAE evaluation is deliberate: squared loss supplies smooth residual-dependent gradients, while MAE measures absolute observable error. This mismatch is held constant across conditions. Although targets are bounded, raw-output MAE is not bounded. Report out-of-range prediction fraction and maximum absolute prediction in every pilot and confirmatory result. Always report secondary MAE after deterministic projection to [-1,1], rather than activating this diagnostic after a subjective threshold. Clipping cannot increase absolute error for labels in that interval; it is a specified postprocessing comparison, not an intrinsically less honest output. Raw MAE remains primary. Out-of-range predictions can affect both average error and variability.

### Mandatory pre-pilot training freeze checklist

Before training any pilot model, record and version: weight/bias initialisation for every module; LayerNorm initialisation; independent/shared RNG streams; optimiser and hyperparameters; learning rate, warmup and schedule; batch size and sampling order; gradient accumulation; gradient clipping; numerical precision; number of optimisation steps or validation stopping rule; checkpoint-selection rule; loss weighting; and any hyperparameter-search allowance. The initial pilot uses identical training rules across conditions, with shape-aware initialisation following the same stated scheme, not identical tensors across incompatible shapes. Any changes motivated by pilot outcomes require a dated amendment before confirmatory runs. These values remain pending; the annex is not yet a complete freeze package.

### Amendment record

Reason: close gate-budget ambiguity, specify an estimable uncertainty approach, disclose possible same-backbone comparator selection, clarify token parameters, and make training freeze requirements explicit. No pilot or confirmatory outcomes were available. Preserved: independent gate-position indexing, fixed observable identities and query count, bias-enabled linear layers, affine LayerNorm, zero dropout, and honest executed padding accounting.


## Review resolution r2 — 2026-11-14

### Mandatory order before comparator enumeration

First specify and version the joint workload from task considerations: qubit-count and realised gate-count probabilities, circuit-family mixture, conditional angle distributions, and batching/padding policy. Fix the resource-accounting convention and hard parameter/compute tolerances with written scientific justification. Only then calculate candidate resource totals, enumerate eligibility, and apply the existing selection order. Neither workload nor tolerances may be chosen or adjusted to obtain a preferred comparator. The grid's configurations are already listed; the prohibited step is evaluating their eligibility or selections under alternative candidate workloads before these decisions are fixed. Prior approximate maximum-length comparisons in the conversation are disclosed as already seen; this procedure is prospective, not a claim that no resource information has been observed. A genuine task correction after enumeration requires a documented amendment disclosing the previous selection and rationale, not an undisclosed re-selection.

### Step 05 requirements: finite-sample validation

Include S=3,5,8 and every proposed confirmatory seed count in synthetic coverage validation, with template counts and seed/template/cell-effect regimes specified before inspecting coverage results. Define the coverage acceptance criterion, Monte Carlo precision and simulation replication count in Step 05. Choose confirmatory S partly from this validation, not solely from precision calculations. If coverage at the proposed S is inadequate, amend the design and repeat validation before confirmation. No satisfactory coverage is presumed from the method's asymptotic justification. For S=3 there are 27 ordered row draws but only 10 distinct seed-count vectors; more bootstrap replicates cannot manufacture independent training runs.

### Failed-run policy

Keep a run ledger containing all planned IDs, execution attempts, failures, reasons and recovery actions. No silent exclusions, seed substitutions, finite-error imputation or resampling an incomplete D matrix. An external interruption may resume from an intact checkpoint with restored optimiser/RNG state; absent a valid checkpoint, allow one logged rerun of the exact configuration and random streams for a documented infrastructure failure. Numerical divergence, persistent OOM, implementation errors or non-finite predictions are not infrastructure failures to be retried until success. If a planned pair cannot supply finite results on every template under the frozen procedure, the primary analysis is unavailable as specified. Report the failure and any descriptive completed-run results separately. Any corrected experiment requires a dated amendment and a clearly distinct run set; it cannot replace the failure invisibly. Step 05 must implement these rules and the failure classification checklist before confirmation.

### Realised workload check

Before model evaluation, publish the sealed manifest's realised joint distribution of qubit counts, gate counts and family, including both template-weighted and instance-weighted summaries. Compare it with the declared workload. Report expected resource differences under both the declared distribution and realised test composition, including per-n results. Set generation quotas or distribution acceptance thresholds in Step 03 before drawing the sealed set. No post-hoc comparator re-selection or outcome-based template removal is permitted. Any mismatch outside the predefined acceptance rule blocks confirmation until a documented correction; incidental differences within the rule remain disclosed.

### Interval interpretation

The interval targets the population mean paired difference over training randomness and generated template groups with their fixed angle sets, as defined above. It is not a prediction interval for a new individual run or template, and not an uncertainty interval conditional on only the particular realised runs and templates. The empirical mean on those realised results is separately reported as the point estimate.

### Embedding ownership

The six-row gate-type embedding table is dedicated to gate tokens. The two-row observable-type table is separate and dedicated to query tokens. Neither is shared with the other or with workspace vectors. The previously specified shared role, ordered-qubit and qubit-count tables are unchanged.

### Amendment record

r2 incorporates the Step 01 r1 review. It adds prospective protection against workload-driven comparator shopping, failure handling and small-S validation requirements, realised-workload checks, interval scoping and embedding ownership. No models were trained, no comparator eligibility was calculated, and no coverage experiments were run in this amendment. Numerical workload probabilities, tolerances and Step 05 validation settings remain unresolved. Step 02 begins by specifying them in the required order, not by selecting a comparator.


## WORKLOAD-002 contrast amendment — Step 01 r3, 2026-11-14

The governing primary contrast is now conversion of four reserved key-masked positions into learned non-input workspace at shared dense capacity P=179. Use the external label masked-padding baseline for W=0. Gate and observable-query positions already support computation. This replaces the earlier shorthand of adding positions to a no-workspace model; Step02A-r3 section 4 and section 12 govern layout and masks.

Step02B-R1 / AC-002 selects d128_L04_W0 from the original grid, with one eligible candidate in both the 15-point original and 588-point diagnostic grids. Arithmetic difference is -512 operations per instance, parameters -512, relative to the four-token reference. Original WORKLOAD-001 empty eligibility remains preserved and applies to its original padding policy. No scientific outcome has been observed.

Secondary W=2 trains a separate model from scratch with the first two reserved slots active and the other two masked under the same P=179. It tests converting 0,2,4 masked slots into active workspace; monotonic improvement is not assumed. W=8 is deferred: a future separately specified comparison could use shared P=183, with fresh controls and accounting, disclosing all previous results. It cannot reuse the P=179 primary matching claim.

Step 05 must interpret gains as benefit from using otherwise masked slots, not general efficiency superiority over optimised unpadded inference. The downstream-relevance principle for delta persists; its numerical value still requires justification for the intended use case before confirmation. Dataset specification, literature review, training choices, analysis specification, coverage validation and pilot remain outstanding; resource eligibility is not readiness to train. No Git commit is made before the complete agreed checkpoint.