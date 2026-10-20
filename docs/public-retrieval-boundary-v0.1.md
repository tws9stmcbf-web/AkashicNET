# Draft public retrieval boundary v0.1

Status: review required. No merge, deployment, independent security certification,
or scientific effectiveness validation. Implements the public route of GAP-01
from PR #400; the trusted private-local API remains explicitly separate.

## Interface decision

```bash
python scripts/query_public_v01.py "synthetic rare concept" \
  --snapshot /operator-selected/public-snapshot.json --domain all --state all --limit 20
```

`--snapshot` is required. This new contract is
`AKASHICNET_PUBLIC_RETRIEVAL`, version `0.1`; it is **not API v0.25** and must not
be substituted for it under the same schema identifier. Domain, state and limit
have the existing semantics. `accepted` includes direct metadata lookup, which
does not create semantic acceptance. Evidence filtering remains unsupported.

The existing `query_api_v025.py` CLI, v0.26 client and private file defaults are
unchanged. The v0.22/v0.23/v0.24 algorithms were extracted into in-memory
`retrieve` functions; their original CLIs still load/call the original chain.
The public CLI invokes those same functions only after projection. It never
calls the private CLI, follows a snapshot-provided path, or falls back to the
legacy corpus. These Python functions are trusted internal APIs, not public
entry points or authorization boundaries.

Both routes read one JSON document once, giving them the same parsed generation.
This avoids separate graph/concept/dedup reads on the public path. It is not a
transactional publishing system: a future publisher must validate and atomically
replace snapshots and control their location and permissions.

## Snapshot contract and approval

Root shape:

```json
{
  "schema_version": "public-retrieval-snapshot/0.1",
  "graph": {"nodes": []},
  "concept": {"concept_nodes": [], "reddit_edges": [], "library_edges": []},
  "dedup": {"retrieval_units": []}
}
```

Each family node, concept, edge, representation and unit needs both
`public_safe: true` and `metadata_eligible: true`, as JSON booleans. False,
missing, null, numeric, string, array and object values fail closed. There is
no truthiness conversion or inheritance of approval from a parent.

Every such record also needs this exact provenance shape:

```json
{
  "artifact_id": "artifact:public-example",
  "record_id": "public:unit:example",
  "independence_key": "source:public-example",
  "public_safe": true
}
```

The nonempty strings must be bounded stable identifiers without whitespace,
paths or provider links. `artifact_id` must begin `artifact:` and
`independence_key` must begin `source:`. `record_id` must equal the row's
`node_id`, `review_id` or `retrieval_unit_id`, respectively. Public unit IDs
begin `public:unit:` (`synthetic:unit:` supports fixtures); raw digest/provider
unit IDs are prohibited. This requires publisher preparation; **do not mass-set
approval flags on a legacy corpus**. Reddit source refs are public stable IDs,
not arbitrary URLs; resolving those IDs to links requires a future contract.

Approval is a trusted publisher assertion. The loader checks its shape and
binding; it does not authenticate the publisher, verify source contents or
perform rights adjudication. No approved production snapshot or deployment
wiring is created by this change. Snapshot selection is an operator capability,
not an end-user-selectable filesystem path in a future network service.

## Public field allowlist

The loader constructs new dictionaries before search, joins, ranking or
summaries. It never passes through original row dictionaries. Unknown fields
are discarded; malformed/ineligible rows are discarded without logging their
identifiers, contents or counts. Provenance is validated rather than copied
wholesale into output.

| Record | Allowed retrieval fields |
| --- | --- |
| Family | node ID, public family ID, canonical/candidate type, curated label |
| Concept | node ID, label, definition |
| Reddit edge | target concept, public stable source ref, relationship, review state/decision, basis; review ID and provenance retained internally |
| Library edge | family ID, target concept, relationship, review state/decision, basis set, matched terms, checked representation count and projected representations |
| Representation | public original-source ref, review ID, validated provenance, review state/decision and accepted flag |
| Unit | public unit/family IDs, labels, collapse basis, deduplicated flag, approved aggregate physical count, rights states, fixed non-promotion guards |

Allowed scalar and nested fields are typed/validated. Known private Drive,
local path and provider markers in allowed text are rejected. The existing
`check_public_data_boundary.validate_entry` runs as a second check on projected
data; its detailed findings never reach the caller. Arbitrary confidential
prose mislabeled as approved public text by a trusted publisher cannot be
detected by an allowlist or marker scanner.

Private filenames, paths, timestamps, object IDs, object links, digests,
unapproved nested dictionaries, graph proposal objects and raw input summaries
never pass through. Unit `manifestations` is always empty and `sha256` always
null. Public aggregate counts/collapse assertions remain publisher-approved
metadata, not object identities or independent verification of byte identity.

Library edges need approved families and concepts. Every representation must
be independently eligible, and parent acceptance must agree with whether any
representation is accepted. A unit with any unapproved family is excluded
entirely because its labels may describe all associated families. An approved
family/concept edge can survive without an ineligible unit as metadata-only;
its private unit cannot supply content or rank. Independently approved concepts
may appear in `matched_concepts` without any surviving edge. Rejected concepts
never contribute to that summary.

## Rights, evidence and adjudication

Rights states are retained verbatim; metadata eligibility does not clear content
redistribution. No content, object links or digests are exposed even if a row
asserts `PUBLIC_VERIFIED`. Truth, rights and scientific promotion remain disabled.
Ranking remains provenance ranking; SHA-based rank cannot promote HOLD to ACCEPT
or represent scientific evidence.

Review-state/accepted-flag/explicit-decision contradictions fail closed on the
public path. Retrieval creates no reviews or accepted edges and does not alter
stored proposal parents/children. Stable public review references are required
at ingestion. [GAP-03 review-reference forwarding](reddit-review-reference-v0.1.md)
now preserves the approved Reddit review ID through the shared retrieval path.
This does not establish complete upstream adjudication lineage. GAP-03 failure
counts and status entries below describe the earlier boundary checkpoint.

## Errors and diagnostics

Success emits one public JSON response and no stderr. Ineligible rows have no
diagnostics. Missing/invalid snapshot files, duplicate JSON keys, nonfinite JSON
constants, ambiguous projected identifiers, malformed root structures and runtime
errors produce exit 1, no stdout, and exactly:

```text
Public retrieval unavailable: invalid snapshot
```

Invalid requests produce exit 2, no stdout, and exactly:

```text
Invalid public retrieval request
```

No traceback, parser snippet, filesystem path or argument value is printed.
Detailed public diagnostics are deliberately suppressed. Resource exhaustion,
malicious publishers, network authorization and deployment logging require
separate review.

## Exact local validation

Environment: Python 3.12.14, pytest 9.1.1, Linux. Pytest installed into an isolated
task dependency directory. Tests use only synthetic inputs. Full repository
checkout; no `AGENTS.md` found in the repository tree.

Baseline at `ee8bc018b09e9733e1682087f0f04d7eb3a6ce38`:
**145 passed, 5 xfailed in 10.94s**. Refactor-only non-gap legacy checks:
**35 passed, 5 deselected in 9.51s**. Initial public/regression run:
**406 passed, 3 xfailed in 35.17s**.

Final selected regression and privacy suite:

```bash
python -m pytest -q -rx \
  tests/test_public_retrieval_boundary_v01.py \
  tests/test_actual_retrieval_continuity_v01.py \
  tests/test_filtered_retrieval_continuity_v01.py \
  tests/test_retrieval_evidence_bridge_v078.py \
  tests/test_retrieval_api_compat_v026.py \
  tests/test_public_data_boundary.py \
  tests/test_public_safe_endpoint_registry_v014.py \
  tests/test_public_safe_semantic_endpoint_registry_v019.py \
  tests/test_evidence_provenance_contract_v05.py \
  tests/test_semantic_link_adjudication_v021.py
```

**445 passed, 3 xfailed in 28.78s**. These expected failures remain unmet
requirements. This is a selected suite, not every repository test.

Diagnostic run (intentionally nonzero):

```bash
python -m pytest -q --runxfail tests/test_actual_retrieval_continuity_v01.py \
  -k 'test_contract and not private_canary' --tb=short
```

**3 failed, 37 deselected in 0.76s**: unsupported evidence argument, absent
Reddit review ID, and reordered equal-key results under a limit of one.

New boundary tests cover strict boolean approval across six record types and
the direct route, unsafe/malformed/unbound provenance, dropped nested object
metadata, hidden concept summaries, fixed errors (including an injected secret
exception), no fallback to private files, unchanged private-local behavior,
preserved rights/decisions, and partially private multi-family units. Three
successful deliberately regressed script variants (truthy approval, raw nested
manifestations and leaked summary) are caught by canary assertions. These
controls are in isolated temporary copies, never tracked production edits.

Retrieval evidence bridge, API compatibility, evidence/provenance and public
endpoint validators passed. The full materialized tracked-file public boundary
scan passed. Explicit changed-file scan and `git diff --check` also passed before
publishing the commit. CI is configured to include public boundary tests;
remote workflow status must be checked separately.

## Corrected versus remaining requirements

| Requirement | Draft result |
| --- | --- |
| GAP-01 concept privacy | Corrected for explicit public snapshot interface; original canary assertion is now a normal passing test of that interface |
| GAP-01 direct privacy | Shared gate/projection before matching and ranking; normal passing test |
| Private-local compatibility | Original CLI still exposes local input to its trusted caller; a regression test makes this boundary explicit |
| GAP-02 evidence filter | Still strict expected failure; no filter/taxonomy change |
| GAP-03 Reddit review-reference forwarding | Still strict expected failure; no claim of complete lineage |
| GAP-04 equal-key ordering | Still strict expected failure; public result metadata states this limitation |
| Deployment/security effectiveness | Not evaluated/certified; no service, corpus or deployment change |
| Publisher authentication/lifecycle | Not implemented; no atomic publication or durability claim |

The fixture producer is test-only, not an approval engine, production snapshot
builder or alternative retrieval algorithm. The two GAP-01 xfail markers are
removed because the new **public** entry point is tested, not because the
trusted private CLI has been silently restricted. Existing endpoint/public-data
validators were reused as policy references; their artifact-wide six-type
registry requirements cannot be applied wholesale to a retrieval snapshot.
