# BQ001 Question Graph v0.1

This forward-only v0.16 slice adds deterministic retrieval to the existing
six-node, four-edge Knowledge Graph Beta fixture. BQ001 stays `UNRESOLVED` and
`NEVER_FINAL`. This is a bounded review artifact, not a v0.16 release declaration.

## Use

Install `jsonschema==4.25.1`, then run:

```sh
python scripts/bq001_question_graph_v01.py validate
python scripts/bq001_question_graph_v01.py query
python scripts/bq001_question_graph_v01.py query --view curated
python scripts/bq001_question_graph_v01.py query --node node:model:MODEL-BQ001-BIOLOGICAL-DEPENDENCE --view inferred
```

The question query returns the entire bounded fixture. Other exact node IDs
return only incident edges and their endpoint nodes, ordered by stable ID.
There is no recursive traversal, scoring, ranking, voting or confidence update.
Unknown IDs fail closed. Every returned edge retains its original artifact,
record locator, digest, derivation, independence keys and review state.

`curated_edges` contains selected `DIRECT_SOURCE_METADATA` relationships;
curated does not mean human-adjudicated acceptance, truth or scientific evidence.
`inferred_candidates` contains only `INFERRED_CANDIDATE` relationships with
`REVIEW_REQUIRED` and `accepted_edge: false`. Even curated edges remain unaccepted.
The two views partition the original edges without changing their assertions.

## Coverage and limits

Both competing model nodes are addressable. Existing support and competition
candidates remain review-only. Counter-evidence coverage is limited to the
existing competing-model candidate; no new empirical counter-evidence is claimed.
The author correction remains `CORRECTED_NOT_RETRACTED`. There are zero observed
retractions and zero accepted edges. This is not an exhaustive literature graph.

The projection pins the upstream repository artifact by SHA-256 and validates
its transitive source pins and locators through the existing graph validator.
Digests describe governed repository artifacts, never private Drive objects.
JSON Schema is actually evaluated, including closed property sets; runtime
validation also requires exact deterministic projection. Duplicate JSON keys,
non-finite values, private keys/links/paths, unscoped digests, unknown metadata,
missing provenance, forged endpoints, graph reclassification and promotions fail.
CLI failure diagnostics do not echo rejected input.

`build` can generate a privacy-screened changed input for review without claiming
readiness. `validate` and `query` reject unreviewed source drift. A source change
never silently advances the audited input pin. Existing sealed v0.14/v0.15
artifacts and the upstream graph fixture are unchanged.

## Resume

Run `.github/workflows/validate-bq001-question-graph-v01.yml` at the PR head.
Require all applicable CI and a clean review before merging. Keep #277 open
until the complete candidate gate is reassessed. Any existing composite release
candidate must explicitly include this slice before claiming its coverage.
Persistent operational state belongs in issue #98.
