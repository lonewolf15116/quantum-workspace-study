# Step 02A — workload and resource-tolerance specification

Version: WORKLOAD-002 / Step02A-r3
Date: 2026-11-14
Status: fixed-padding amendment prepared for review; not registered. WORKLOAD-001 enumeration has been observed; WORKLOAD-002 has not yet been enumerated. No model training outcomes observed.
Basis: Step 01 r2. New workload choices below are explicit design decisions, not measured findings.

## 1. Task rationale and scope

Predict all Z_i and Z_i Z_j expectations for noiseless parameterised circuits on 4–10 qubits. Use balanced qubit counts, three gate budgets and three connectivity families to avoid allowing the largest systems or one topology to dominate. This seeks an intermediate learning regime through bounded, structured circuits, not through an established guarantee of difficulty. Large random circuits can also yield near-zero observables and become deceptively easy for a constant predictor. Pilot diagnostics must therefore include label distributions and zero/summary-predictor errors as well as training/validation residuals.

A pilot finding of trivial or unlearnable targets triggers a documented task amendment and a new workload version before confirmation; it does not justify adjusting the workload to admit a comparator. Any such amendment discloses old/new resource matches. Delta remains justified by downstream relevance, never by the observed winning effect or pilot variance.

## 2. Finite analytical workload

Choose n uniformly from {4,5,6,7,8,9,10}. Conditional on n, choose r uniformly from {2,4,6}; gate count g=2nr, hence g belongs to {4n,8n,12n}, each with probability 1/3. Maximum g=120, below the architectural cap of 128. These are gate counts, not circuit depths.

Choose family independently conditional on n, uniformly from {path,ring,all_to_all}. All 63 cells (n,r,family) have probability 1/63. This is a fully enumerated discrete distribution, not an empirical estimate. Within each cell, angle draws and topology choices follow the rules below. Template quota K per cell is identical, with K set after pilot precision analysis; angle-instance count A per template is also common and set before confirmation. Thus the main score and accounting use the same cell weights. Pilot and confirmatory templates are disjoint.

| n | g values (equal conditional probabilities) | Query count |
|---|---|---|
| 4 | 16,32,48 | 10 |
| 5 | 20,40,60 | 15 |
| 6 | 24,48,72 | 21 |
| 7 | 28,56,84 | 28 |
| 8 | 32,64,96 | 36 |
| 9 | 36,72,108 | 45 |
| 10 | 40,80,120 | 55 |

## 3. Family and angle rules

Start each circuit in |0>^n. Each of r rounds contains n single-qubit rotation gates, one per qubit in ascending index order, followed by n CNOT gates. Each rotation axis is independently uniform over RX, RY, RZ and belongs to the template. Each angle is independently uniform on [-pi,pi), for every family and axis. There are no angle correlations or family-dependent angle distributions in this version.

For each CNOT, sample an undirected allowed edge uniformly with replacement and choose its direction with probability 1/2. Path edges are (i,i+1); ring adds (n-1,0); all_to_all permits all unordered pairs. Self edges are forbidden. Gate order is sampled order. Do not simplify or cancel gates, as this would change gate count. Duplicate circuits/templates are grouped before splitting; duplicate-draw handling and family-overlap grouping must be fully specified in Step 03. In particular, a ring/all_to_all draw may also fit a more restricted family: retain the generation-family metadata but never let identical normalised templates cross splits. Primary families are generation distributions, not claims that each realised circuit has a unique topology class.

Main circuits are not guaranteed phase-sensitive at every RZ gate. Step 03 must tag guaranteed irrelevant cases separately from numerical sensitivity checks. H-RZ-H analytical checks below verify phase handling without claiming all main rotations influence labels.

## 4. Batching and executed padding — r3 replacement

Both PRIMARY conditions use P_max=179 encoder positions per instance. This is max(g+Q)+4=120+55+4, the smallest common capacity accommodating every declared cell and the four-token reference. It is chosen from workload capacity, not enlarged to 250 or to dilute a percentage mismatch. Data distributions and valid query count are unchanged; the execution-policy amendment warrants WORKLOAD-002.

For an instance with g gate and Q query tokens, put gates at indices 0..g-1, queries at g..g+Q-1, and reserve slots g+Q..g+Q+3. In W=4 these are learned workspace tokens and valid attention keys. In W=0 they are zero-initialised padding rows masked as keys at every layer, as are all remaining trailing padding rows in both conditions. Do not zero or discard intermediate padded query-row states to save arithmetic: all 179 rows execute the same dense blocks. Key masking prevents their information from reaching valid tokens. Read out only valid query positions for scoring. This defines 'four positions converted from masked padding to learned workspace', not 'four newly allocated positions'. Effective valid attention connectivity changes as part of the intervention.

Both conditions allocate a 55-row readout buffer, populate valid query representations, zero-fill unused rows and execute the same shared scalar head on all 55 rows. Only valid observables enter loss and metrics. All padded encoder arithmetic is charged. Padding-skipping kernels are excluded from primary AC accounting, and actual hardware costs/latency still require measurement.

The W=0 model does not allocate the four workspace vectors. It retains the shared three-role table as in AC-001. Consequently the models differ by 512 allocated parameters at d=128; do not call parameter counts identical. Under the existing token-construction algorithm, W=4 also executes W*d additional embedding additions. Exact equality of the complete arithmetic scalar is therefore not asserted; Step 02B must rerun it before eligibility is claimed.

This policy leaves the reference encoder length unchanged at 179 and raises the original W=0 encoder length from 175 to 179. It does not increase reference computation by 1.5 times. Report the new charged/useful ratios per cell and in aggregate. Useful counts continue to use g+Q+W valid positions and Q readouts; useful compute remains unequal.

Secondary W=2 can use the same capacity; W=8 cannot fit the maximum cell within 179. W=8 is deferred from this primary contract and requires its own declared capacity/control design before execution. Do not silently expand primary padding to accommodate a secondary condition.

## 5. Expected-resource formula

For model configuration a, E[F(a)] = (1/63) sum over n in 4..10, r in {2,4,6}, f in {path,ring,all_to_all} of F(a;n,2nr,f,179).

F is the exact declared analytical operation convention from Step 02B, not big-O or a sampled profiler estimate. If a component depends on random gate axes, use its analytic expectation or explicitly execute/count that component for all gate positions; record the chosen implementation. The rotation projection should be executed for every valid gate using zero features on nonrotations. Step 02B must count embedding summations, projections, bias, layer norms, attention, FFN, residual additions and the 55-slot readout. MAC=2 arithmetic operations; report special-function calls and comparisons separately. Do not equate these logical counts with GPU instructions or elapsed time. The final matching scalar and treatment of special functions must be fixed in Step 02B before eligibility enumeration.

## 6. Hard tolerances and selection

Proposed hard bands: |E[F(candidate)]/E[F(reference)]-1| <= 0.01 and |parameters(candidate)/parameters(reference)-1| <= 0.01. Denominators always use the four-workspace reference. Both must hold. Filter first, then minimise absolute expected-operation difference, then fewer parameters, then lower depth, then lexicographic configuration ID.

Justification principle: limit residual resource differences to at most one part in 100 of each reference budget so the claim is explicitly a comparison within a narrow resource envelope. This is a conservative design constraint, not an empirically established threshold of negligible performance impact, and not derived from grid spacing. Neither a 1% nor any nonzero tolerance proves extra compute cannot explain an improvement. Report achieved differences and limit causal wording accordingly. Stronger attribution requires additional controls, not an assertion that the tolerance is causally inert.

Prior maximum-length estimates around 2.6% were already disclosed before this proposal. The 1% band intentionally allows an empty eligible set; it is not enlarged to obtain a result. No comparator is asserted eligible or ineligible here. The previously seen approximation uses a different maximum length and cannot be presented as the exact result for WORKLOAD-001. After review fixes this workload and these bands, Step 02B will publish the same-backbone arithmetic and all-grid results. If no comparator qualifies, report primary comparison unavailable as specified; an amended denser grid would be a separate, disclosed pre-outcome design decision, not a silent tolerance change.

## 7. Sanity checks outside the primary workload

Exclude all sanity cases from primary training/validation/test score, expected-resource averaging and comparator selection. For each n=4..10 generate 16 product-state circuits (one RY per qubit), one GHZ circuit (H on qubit 0 followed by chain CNOTs), and three phase-sensitive H-RZ(theta)-H circuits on qubit 0 with theta in {0,pi/2,pi}, other qubits idle. Total 140 cases: 112 product, 7 GHZ, 21 phase checks. Report separately and use for simulator/encoding correctness. Product angles follow independent U[-pi,pi). No model-selection tuning against these checks.

## 8. Reproducible draws and quotas

Use NumPy Generator(PCG64), pinning the NumPy version before generation and saving its initial/final bit-generator states. Separate integer seeds: pilot topology 2026111401; pilot angles 2026111402; confirmatory topology 2026111403; confirmatory angles 2026111404; sanity angles 2026111405; split assignment 2026111406. These are dataset streams, not model-training seeds. Enumerate cells in ascending n, then r, then family order path/ring/all_to_all; loop templates before angle instances. Do not generate confirmatory data until Step 03 fixes deduplication and split semantics. RNG seeds alone are not sufficient for reproducibility: archive code revision, draw ordering, dependency versions and realised manifests.

Use equal fixed cell quotas, not random sampling of cell identities. Conditional random draws generate templates/angles within each cell. Publish realised joint distributions and expected operations on the realised manifest. Cell-count mismatch blocks sealing rather than silently reweighting results; duplicate resolution must preserve quotas or report generation failure.

## 9. Completion boundary

Step 02A supplies concrete choices for review before enumeration. Step 02B must fix the exact accounting scalar, instantiate parameter tables, and only then evaluate eligibility. Step 03 must operationalise circuit grouping, template novelty checks, canonical hashes, split assignment and quota completion. Step 05 retains coverage validation, failed-run rules and estimand scope from Step 01 r2. No pilot, training, exact enumeration, eligibility decision or performance claim was produced here.


## 10. Review resolution r1 — scope and anticipated feasibility

The supplied structural review predicts an empty eligible set for the existing 15-model grid under the unchanged +/-1% bands. Record this expectation before exact enumeration. It remains a prediction until Step 02B applies its complete accounting convention. No matched candidate is selected in this revision.

Do not widen tolerances to 3% or lengthen circuits/padding to manufacture eligibility. Both would alter the already-stated resource constraint or task. If exact enumeration is empty, the primary comparison is unavailable as specified. A separately reviewed pre-outcome architecture-grid amendment is the preferred next design investigation, but is not a promised remedy. A finer width/depth grid can compensate part of the position-related compute difference while changing parameter count; whether it satisfies BOTH bands must be checked. The four-position gap is not an impossibility theorem for every possible no-workspace architecture. Any amendment must explicitly disclose that old-grid enumeration was observed; predicting that enumeration in advance does not make the subsequent design choice blind.

### Charged versus useful operations

This study matches fixed padded operations, not equal useful-token computation. Step 02B must show charged and unpadded logical operation counts for every condition, per cell and averaged over all 63 cells. For useful counts, use valid sequence length g+Q+W and Q valid readouts; retain the same arithmetic convention. Report charged/useful ratios separately from padded/valid position ratios.

At n=4,r=2,W=0 the position ratio is 175/26, about 6.73. This is a position ratio, not a FLOP ratio: attention includes a quadratic term. The average padding overhead must be calculated, not inferred from this smallest cell. Charged encoder work is constant across cells for a given architecture under this implementation, even though valid-token work varies. Do not claim useful-compute matching from a charged-compute match.

### Query-budget scope

All 55 query tokens at n=10 participate throughout the encoder; their cost is not limited to the final scalar head. A result applies to the incremental value of four workspace positions on top of this fixed query-rich architecture. A statistically inconclusive result establishes neither no effect here nor uselessness elsewhere. Even a precise negligible-effect finding remains scoped to the workload, query design, training procedure and resource policy.

### Circuit-distribution scope

The main task is a specific layered rotation-then-CNOT ansatz distribution: exactly one rotation per qubit and n CNOTs per round. It is not generic random-circuit sampling and does not represent all hardware-efficient ansatz designs. Results do not automatically transfer to randomly placed gates, sparse qubit activation, other gate sets or other observable readouts. Use reporting labels such as path-drawn at n=4,r=2. Expected undirected path-edge uses are n/(n-1) per round, or rn/(n-1) per circuit; these are expectations per allowed edge, not proof each edge is visited. Realised multiplicities and active-edge counts belong in the manifest diagnostics.

### Sanity terminology

The H-RZ(theta)-H family has <Z_0>=cos(theta) on the specified initial state. Its theta=0 member is the identity/no-op check, theta=pi/2 checks zero expectation and theta=pi checks inversion. Do not label individual points generically insensitive: local derivative and finite parameter dependence are different notions. Product-state, GHZ and all phase checks remain outside expected-resource matching, primary scores and comparator selection.

### Digest and version pinning

At freeze, compute and record SHA-256 of the exact UTF-8 workload-specification file bytes, which include distributions, cell weights, angle rules, padding, tolerances and dataset RNG seeds. Store the digest outside the hashed file in the freeze manifest alongside generator/configuration digests, dependency versions and RNG states. Pin that manifest in each accounting and dataset result. Later text or configuration changes require new digests and amendment reasons. This revision is not itself represented as an approved freeze.

Amendment boundary: no distribution, tolerance, grid or RNG seed was changed. Required useful-operation reporting was strengthened and the predicted empty-grid outcome recorded. No exact enumeration, training or scientific outcomes were produced in this revision.


## 11. Review resolution r2 — joint-search scope and cell interpretation

Any architecture amendment considered after empty eligibility will investigate width and depth jointly, subject to the existing four-head constraint d divisible by 4 and FFN width 4d. A width-only adjustment at reference depth is not assumed sufficient. The review's fixed-depth impossibility statement is a leading-order prediction, not a substitute for exact accounting; do not turn it into a proved theorem before checking the full parameter and operation formulas. The illustrative d=115,L=5 point is inadmissible with four equal-sized attention heads. No joint candidate is promised eligible and no expanded grid is defined or evaluated here.

If original-grid enumeration finds any eligible candidates, apply its existing selection rule and proceed with that grid: the prediction of emptiness does not authorise densification. If it finds none, report that result before proposing a separately reviewed, joint width/depth amendment. Training outcomes remain unavailable, but original resource enumeration will have been observed and must be disclosed.

Valid-token perturbations depend on both n and r. Correct example counts (g=2nr, Q=n(n+1)/2) are:

| n,r | g | Q | W=0 valid S | W=4 valid S | Position increase |
|---|---|---|---|---|---|
| 4,2 | 16 | 10 | 26 | 30 | 15.3846% |
| 7,4 | 56 | 28 | 84 | 88 | 4.7619% |
| 10,6 | 120 | 55 | 175 | 179 | 2.2857% |

These are position increases, not useful-operation ratios. Step 02B computes the latter using the full arithmetic convention. Per-cell charged and useful counts remain mandatory. An aggregate negligible or inconclusive error difference can coexist with heterogeneous cell-level differences. Positive error differences in some cells would not by themselves establish a useful-compute-matched advantage: those conditions may use different amounts of useful computation. Per-cell performance analyses are secondary, carry uncertainty and multiplicity qualifications, and cannot replace the primary result.

Sanity suite: 140 cases (112 product + 7 GHZ + 21 phase).

Digest target clarified: the exact complete UTF-8 bytes of this Step 02A Markdown document at its approved freeze revision, not an extracted specification. Archive those bytes alongside the external manifest; record filename, byte length, revision and SHA-256. The manifest references the archived document rather than embedding its own digest in that document. Every textual amendment changes the document digest. No freeze digest is claimed until the revision is actually fixed for accounting.

This revision changes explanatory scope only. Workload, tolerances, architecture grid and seeds remain unchanged. No resource enumeration or model training occurred.


## 12. Dated policy amendment r3 — 2026-11-14

### Observed evidence and precedence

WORKLOAD-001 / AC-001 found 0/15 original-grid and 0/588 diagnostic-grid eligible candidates under +/-1% arithmetic and parameter bands. The observed diagnostic range was widths 64..256 in steps of four and depths 1..12. No training, accuracy or GPU benchmark outcomes were observed. Resource enumeration is observed evidence, not an unobserved prior. Preserve the original Step02B ZIP unchanged as historical evidence.

This section and replacement section 4 supersede prior historical statements refusing shared-padding changes or using P(W)=175+W. Earlier review-resolution sections document the history rather than govern execution where inconsistent. WORKLOAD-002 changes execution policy and the operational primary contrast; it does not change qubit, gate, family, angle distributions, RNG seeds, original grid or +/-1% bands.

### Scientific rationale and claim

Primary amended question: does converting four reserved, key-masked positions into learned non-input workspace improve prediction under fixed dense encoder capacity, fixed query architecture and the stated arithmetic/parameter tolerances?

This controls allocated sequence length and dominant dense operations. It does not isolate role separation from changes in active attention connectivity and does not demonstrate optimal use of deployable hardware. The padded baseline deliberately performs masked computation; inference without such padding is a separate comparison. A gain could establish benefit from using otherwise masked slots, not general efficiency superiority over optimised no-workspace inference.

### Limits of the structural interpretation

The old empty result documents a resource-compatibility restriction for the stated architecture family and finite ranges. AC-001 leading layer parameters are 12d^2, not 20d^2. Leading linear arithmetic per layer is 24Sd^2, whose ratio to leading parameters is 2S, while the 4S^2d attention term varies with width at fixed approximate parameter budget. Embeddings, biases and scalar operations also matter. Thus a simple constant-ratio theorem is not established. Joint feasibility cannot be ruled out universally by the supplied approximation. Head count leaves dominant projection/matrix terms unchanged at fixed d but changes softmax/scaling/comparison terms in AC-001.

### Required revised accounting and version control

Create a separate Step02B-R1 package with a new convention/version and immutable input hashes. Preserve the original package. Rerun the original 15 candidates and the previously defined 588-point diagnostic range, using the same scalar rules except shared P=179 for charged encoder operations. Retain per-cell useful counts and all function-call ledgers. Apply the same original-grid eligibility and selection ordering. Do not declare a primary candidate eligible until these results exist.

The first Git checkpoint should include the reviewed source annexes, both accounting revisions, executable enumeration, manifests and a concise amendment history, preserving the old empty result. No remote repository or commit has yet been created for this study; repository destination remains unspecified. User has authorised committing when needed, so no additional permission is required merely to commit these files once the destination is established. Do not upload unrelated project files or replace another study's repository.

Status boundary: Step02A-r3 amendment prepared; revised enumeration pending; no training permitted by an assertion that the comparison is already validated.
