# Actual retrieval continuity investigation

Date: 2026-10-12. Status: **DRAFT / REVIEW REQUIRED; continuity contract not satisfied**.

Investigated PR #400 at `bfa5b94bf483cb2c2c8b641700b7b8e2731943ee`, based on
`9cf967a7a9ed7921e6220189e46f4dc51c845a88`. This follow-up changes tests,
the existing CI hook, and this report only. Production scripts, API/schema,
corpora, rights rules and adjudication artifacts are unchanged.

## What was actually executed

`tests/test_actual_retrieval_continuity_v01.py` copies the repository scripts
byte-for-byte into a fresh pytest temporary directory, checks byte equality,
creates synthetic JSON inputs, and invokes the real subprocess chain:

1. `scripts/query_api_v025.py`: CLI request validation and versioned response wrapper.
2. `scripts/query_unified_v024.py`: domain/state filters, limit, counts and policy guards.
3. `scripts/query_ranked_v023.py`: provenance profiles, direct-family fallback and ordering.
4. `scripts/query_multihop_v022.py`: concept match and file-backed source joins.

Every invocation starts a new process. A temporary `python` symlink points to
the test interpreter because the legacy chain invokes literal `python`.
There is no mocked subprocess, substitute ranking implementation, live service
call, credential use, or private corpus import. The three deliberately mutated
negative controls operate only on temporary script copies.

Inputs are synthetic substitutes at the filenames the actual implementation
opens relative to its working directory:

| File | Actual role |
| --- | --- |
| `data/knowledge-graph-v0.16.json` | Canonical-family labels; contains synthetic protected graph edges in the test |
| `data/concept-layer-v0.22.json` | Concept labels/definitions and Reddit/library adjudicated relations |
| `data/dedup-retrieval-view-v0.17.json` | Logical units, manifestation provenance, rights states and direct title fallback |

The real `normalise_semantic_representations_v022.py` also runs on a synthetic
v0.21 input to check repeatable normalization and preservation of representation
review decisions. This does not test the complete graph/hash/dedup build pipeline.

## Retrieval semantics and access boundaries

Concept matching is case-insensitive substring matching over labels/definitions,
or an exact concept ID match. It is not vector similarity. All matching edges
are read before unified domain/state filtering and the final limit. The test
with 150 higher-ranked, ineligible distractors establishes that the eligible
held library target survives a limit of one in this implementation.

Ranking is descending provenance tier: P3 SHA-256 identity, P2 manifestation,
P1 reviewed topical relation, P0 other topical/direct metadata candidate.
`profile()` reads `review_state`, whereas the unified decision prefers an
explicit decision when present. Inconsistent input adjudication fields are not
validated by this suite. SHA identity does not establish scientific validity or
rights clearance. HOLD can outrank ACCEPT without changing either decision.

`--domain` is the available source-domain equivalent of the reference adapter's
`source` filter. It is not a source-artifact/record provenance filter. `--state`
has `all`, `accepted`, `hold`; `accepted` deliberately also includes
`DIRECT_METADATA_LOOKUP`, which remains explicitly distinct from acceptance.
`--evidence` and `--source` are rejected as unsupported CLI arguments.

`check_public_data_boundary.py` blocks tracked private graph/dedup paths and
private object metadata. That repository publication boundary is separate
from runtime authorization. The legacy CLI assumes its local inputs are
appropriate for its caller. It does not enforce `public_safe`,
`metadata_eligible`, provenance-public eligibility or a public field allowlist.
The conceptual route copies manifestation dictionaries; the direct route
returns the original retrieval unit. The dedup builder can carry object IDs,
filenames and digests. No deployed data exposure was tested or established.

Newer public-safe endpoint/graph validators and
`validate_semantic_link_adjudication_v021.py` enforce separate public artifact
and human-review contracts. The latter preserves proposal parents and explicit
accepted children with adjudication references. None is called by this legacy
four-script query chain. The new tests preserve synthetic proposal/child bytes,
but do not establish that those newer adjudicated artifacts feed API v0.25.

## Contract mapping

| Synthetic reference guarantee | Meaningful actual-path equivalent | Result / remaining gap |
| --- | --- | --- |
| Public/private separation | Repository boundary plus runtime projection | Scanner regression tests pass; runtime canary exclusion fails on both routes (GAP-01) |
| Source filter | `--domain reddit/library/all` | Exact expected source sets pass; not arbitrary source provenance filtering |
| Evidence-class filter | No current CLI or schema field | Unsupported; GAP-02 |
| Rare-concept filtered recall | Exhaustive concept matching, filter before limit | Bounded distractor test passes; no ANN recall claim |
| Frozen provenance and rights | Source refs, manifestation lineage, rights states, policy flags | Covered on synthetic inputs; no rights promotion; Reddit review ID missing (GAP-03) |
| Human decisions stay human | Forward ACCEPT/HOLD/REJECT and keep stored inputs unchanged | States/bytes preserved; review lineage incomplete for Reddit; modern adjudication integration untested |
| Multivectors / second-vector match | No vector backend in this chain | Not applicable; representation multiplicity is different and is tested separately |
| Representation multiplicity is not evidence strength | Normalized family-concept edges and provenance rank | Multiplicity does not raise rank or accept a held relation in the bounded tests |
| Deterministic insertion order | Sorting of results from permuted input arrays | Distinct rank keys pass; equal keys change top-one concept selection (GAP-04) |
| Restart / persistence | Fresh processes re-read synthetic JSON files | Identical response and unchanged bytes pass; no database durability certification |
| Index rebuild | Real semantic normalizer only | Duplicate representation and repeat-build checks pass; not a vector/index rebuild |
| Missing required indexes | Missing/malformed file inputs | Six cases return nonzero and no success payload, without writes; structured safe errors unimplemented |
| Transactional insertion / rollback | No insert/batch/transaction API in query chain | No equivalent coverage; multi-file snapshots and atomic publication untested |

Other available interfaces: `examples/retrieval_client_v026.py::retrieve`
wraps the same CLI. Older `query_knowledge_graph_v06.py::query(graph, text,
limit, node_type)` and `query_cross_source_graph_v07.py::query(graph, text,
limit)` accept in-memory graphs / `--graph` paths, but have different output,
ranking and filtering contracts and are not used by API v0.25. No interchangeable
backend lifecycle interface was found in the traced implementation. The new
`ActualCLI` is a test harness, not an implementation of SQLite's full lifecycle
surface, and does not translate an evidence request into a provenance rank.

## Exact validation record

Environment: Python 3.12.14, pytest 9.1.1, Linux; pytest installed only into a
task-local dependency directory. Sparse checkout of selected source, tests and
public contract documents; no private data files checked out. Complete tree
path inspection found no `AGENTS.md`.

From the repository root (with pytest available):

```bash
python -m pytest -q -rx tests/test_actual_retrieval_continuity_v01.py tests/test_filtered_retrieval_continuity_v01.py tests/test_retrieval_evidence_bridge_v078.py tests/test_retrieval_api_compat_v026.py tests/test_public_data_boundary.py
```

**145 passed, 5 xfailed in 12.05 seconds.** Breakdown: 66 existing synthetic
SQLite contract tests, 44 pre-existing bridge/API/privacy regressions, and
35 new actual-script checks. The five strict expected failures are not passes.
They comprise two privacy routes and one each for evidence filtering, Reddit
review reference and tied ranking. `strict=True` makes an unexpected pass fail
CI until the requirement and marker are reviewed. CI uses `-rx` to display gaps.

The 35 passing cases are: wrapper fidelity (1); domain/state matrix (9);
distractor/limit (1); ranking/provenance/rights/decisions (1); direct lookup (1);
fresh process/read-only (1); unreferenced synthetic private store exclusion (1);
distinct-key order permutations (3); multiplicity (1); semantic rebuild (1);
missing/malformed inputs (6); rejected requests (6); controlled regressions (3).
The three controlled regressions remove domain filtering, promote returned
decisions, or invert ranking in temporary scripts. All execute successfully
and are caught by the expected-result assertions.

Diagnostic run (intentionally nonzero):

```bash
python -m pytest -q --runxfail tests/test_actual_retrieval_continuity_v01.py -k test_contract --tb=short
```

**5 failed, 32 deselected in 1.30 seconds**, before adding the three negative
controls. Failures were inspected: the literal synthetic private canary was
returned on both paths; evidence CLI exit was 2; Reddit review ID was absent;
reversing equal-key input changed the returned concept under limit 1.

Additional executed checks: `validate_retrieval_evidence_bridge_v078.py`,
`validate_retrieval_api_compat_v026.py`, `check_public_data_boundary.py`, and
`git diff --check` passed. The repository scanner pass is scoped to materialized
tracked files in this sparse checkout; changed files also receive explicit
path/content checks before commit. It is not a new full-repository privacy audit.

Before this follow-up, GitHub reported PR-head retrieval bridge CI success
(run 38224024939) and combined-candidate CI failure (run 38224024884). The latter
was not diagnosed or fixed here. Fresh CI on the follow-up commit must be
reviewed separately. No merge, release, deployment or draft-to-ready transition
is part of this work.

## Specific changes needed before claiming continuity

1. **GAP-01, public boundary:** introduce an explicit validated public retrieval
   snapshot/loader and a field allowlist shared by concept and direct fallback
   paths. Keep any private operator interface separate. Require affirmative
   boolean eligibility and public provenance, preserve independent rights
   constraints, reject missing/ambiguous eligibility, and suppress rejected
   payloads in diagnostics. Add canary cases for false/missing/null/non-boolean
   eligibility, unsafe provenance, hidden labels, direct fallback, summaries
   and errors. Do not silently repurpose the existing private-local CLI as a
   public endpoint.
2. **GAP-02, evidence:** define the authoritative evidence-class taxonomy and
   public field independently of provenance tier; thread an explicit filter
   through API, unified layer, retrieval and documented schema. Fail closed on
   unknown values and filter before limit. Test independent and intersecting
   domain/evidence/state combinations. Use compatibility/version review for
   any required-field or existing-semantics changes.
3. **GAP-03, adjudication provenance:** forward stable review/adjudication
   references in Reddit results and explicitly map newer public adjudication
   artifacts if those are to become inputs. Preserve proposal parents and
   accepted children separately; validate contradictory decision fields before
   publication. Retrieval must never create acceptance or promote evidence.
4. **GAP-04, total ordering:** replace the `str(source)` tie key with an explicit
   canonical tuple including source identity, concept ID and relevant unit/edge
   ID. Define duplicate identity first; test equal-rank ties, reversed JSON key
   order, duplicate relations and truncation without deleting valid lineage.
5. **Lifecycle:** expose a snapshot-qualified read interface (query, domain,
   state, evidence, limit) and separately define any backend create/open,
   insert-batch, rebuild and inspection operations. Atomic publication must
   prevent mixed graph/concept/dedup generations. Add fault-injection rollback,
   interrupted publication and concurrent snapshot tests only once that actual
   interface exists. The current dedup builder's hard-coded historical counts
   and direct JSON writes are not a general transactional index adapter.

## Limits and review decision

This is executable local integration evidence for the named repository scripts
on synthetic inputs. It is not independent effectiveness validation of the
deployed site, a production corpus, ANN backend, or AkashicOMNI v0.5.0. No live
deployment identity, representative public gold set, retrieval quality,
latency, concurrent durability or scientific claim validity was established.
Keep PR #400 draft. Review the gap assertions and the intended public/private
interface before implementing or releasing a new retrieval contract.
