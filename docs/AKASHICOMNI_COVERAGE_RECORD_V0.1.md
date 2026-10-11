# AkashicOMNI perspective coverage record v0.1 (draft)

Status: **UNRELEASED / REVIEW_REQUIRED**. This is a bounded engineering companion
in PR #367, not adoption or implementation of the complete manual methodology.
The [public v0.5.0 Public Review Specification](https://akashicnet.org/akashicomni/v0-5-0)
is separately available for manual, human-reviewed analysis. Its availability
neither releases this software nor establishes independent effectiveness.

## Contract and boundaries

The closed schema `schemas/akashicomni-perspective-coverage-v0.1.schema.json`
records a reading's declared scope, source context, twelve baseline perspectives,
and separate synthesis. It binds to a claim packet by ID and SHA-256 of its exact
file bytes. Reformatting the packet changes that binding. The caller supplies both
local file paths; the record cannot choose a path or trigger source retrieval.
The existing claim-packet validator and fixed trust registry must also pass.

`FULL` covers all twelve perspectives for the selected claim IDs, which need not
include every claim in the packet. `NARROW` explicitly excludes at least one
perspective, with a reason for each exclusion. Included and excluded perspectives
must be unique, disjoint, and together account for all twelve. Exclusion is a scope
decision, distinct from an included perspective marked `NOT_RELEVANT`.

Included perspectives have a reason and one of `APPLIED`, `NOT_RELEVANT`, or
`INSUFFICIENT_INFORMATION`. `APPLIED` additionally requires a contribution and
at least one referenced source whose packet access status indicates inspection.
This first slice represents source-informed readings; it does not represent a
source-free application. Referenced uninspected material cannot justify
`NOT_RELEVANT`. These structural rules do not establish that reasons are sound,
that source material supports a contribution, or that a reading is adequate.

Source context must cover exactly the sources linked to the selected claims and
copy their access statuses without upgrades. Inspected-scope descriptions are
self-reports, not attestations. An inspected editorial artifact remains editorial
context, not primary-source verification. This record never adds trust entries.

`RECORDED` requires a separate synthesis summary and uncertainty statement.
It is an author-declared recording state, not acceptance or methodological
completion. `IN_PROGRESS` permits a missing or provisional synthesis. All M01–M12
manual gates remain `PENDING` in either state. Source-access accuracy, relevance,
reason quality, synthesis adequacy, independent human verification, and the
original acceptance requirements still require human review.

The twelve identifier spellings match the compatibility vocabulary in PR #379 at
`570aee1632fc036d8f114c0fa584ad6c198575a2`:
`AWAKEN`, `HIERATIC`, `HOMESENSE`, `ADAPT`, `REGENERATE`, `TRANSCEND`, `#METAD`,
`ACTC`, `MultidimensionalCUT_PAST`, `MultidimensionalCUT_PRESENT`,
`MultidimensionalCUT_FUTURE`, and `UMASC`. Reusing identifiers is not PRISM
interchange, execution, optional-module support, or equivalence to evidence lanes.

## Provenance and validation

`REAL_RECORD` and `SYNTHETIC_FIXTURE`, like `HUMAN` and `AI` author types, are
unverified declarations. Relabeling a fixture cannot authenticate a person or
establish a real reading. Attribution is always `UNVERIFIED_SELF_REPORT`.
The only committed example is explicitly synthetic test data under
`tests/fixtures/akashicomni/`; it contains no actual perspective analysis.

The validator performs read-only structural checks, rejects duplicate JSON keys
and non-finite constants, and uses the unchanged claim-packet validator. It does
not write assessments, change decisions, inspect sources, or grant manual gates.
Accepted edges and supported models stay empty; all eight promotion flags stay
false. Release, review, and independent-review statuses stay `UNRELEASED`,
`REVIEW_REQUIRED`, and `PENDING`. A structural PASS is not an acceptance result.

From the repository root, with Python and `jsonschema==4.26.0` installed:

```sh
python scripts/validate_akashicomni_coverage_v01.py tests/fixtures/akashicomni/coverage-synthetic-v0.1.json data/akashicomni/meditation-crime-pilot-v0.5.0.json
python -m unittest discover -s tests -p 'test_akashicomni*py'
```

Regression checks cover packet binding, unchanged claim validation, perspective
accounting, source scope, non-promoting access statuses, mandatory synthesis,
closed fields, immutable gates, ambiguous JSON, and read-only CLI behavior.
No real reading, source reinspection, independent assessment, full-spec adoption,
merge, deployment, publication, or release follows from passing these checks.
