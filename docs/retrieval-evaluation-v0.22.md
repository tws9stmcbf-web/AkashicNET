# AkashicNET Retrieval Evaluation v0.22

## Status

Development milestone for evaluating the validated retrieval stack now merged into `main`.

Baseline merge commit: `31a37b2575bef9b4b19b1abe9aa1087eb0edc9ea`

Validated components at baseline:

- ontology expansion v0.20
- expanded concept index v0.21
- semantic representation normalisation v0.22
- evidence-aware retrieval ranking v0.23
- unified retrieval contract v0.24
- retrieval API v0.25
- retrieval consumer contract v0.26
- multi-hop retrieval + provenance v0.19
- concept adjudication v0.11

## Objective

Determine whether AkashicNET retrieves useful, reproducible and provenance-preserving relationships across the library, concept and Reddit layers without promoting unsupported claims.

## Evaluation principles

1. Similarity may nominate a connection; it does not establish one.
2. Ranking must not change semantic decisions.
3. HOLD and unresolved states must remain explicit.
4. Retrieval presence must not imply truth, scientific validity, safety, efficacy, endorsement or rights clearance.
5. Provenance must remain inspectable for every promoted result.
6. Direct metadata lookup is not semantic acceptance.

## Benchmark dimensions

- direct metadata retrieval
- concept retrieval
- cross-source retrieval
- multi-hop traversal
- provenance-chain completeness
- deduplication behaviour
- HOLD preservation
- weak-match rejection
- deterministic ordering
- consumer/API contract stability

## Initial pass gate

A benchmark run passes only if:

- every query returns a schema-valid response;
- no result changes semantic state because of rank alone;
- all ACCEPT results expose provenance sufficient to reproduce the path;
- HOLD results remain HOLD unless a reviewed adjudication changes them;
- no rights, truth or scientific-evidence promotion occurs implicitly;
- known weak lexical coincidences are not promoted as semantic relationships;
- repeated runs over the same frozen inputs are deterministic.

## Next implementation step

Create and freeze a reviewed benchmark corpus of 25-50 queries, execute it through the v0.25 API/consumer contract, and record per-query PASS/HOLD/FAIL outcomes with provenance diagnostics.
