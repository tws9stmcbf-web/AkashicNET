# PR #400 focused code and security review, 20 October 2026

**AI-executed review and corrections; independent human review is still required. Keep draft. No merge, release, deployment or approval is granted by this report.**

Reviewed head: `98f37442b9c293c43120b23bdc6b2b67f3448d97`.
Main/base: `e342c8fea7ef6da7ffe2a5efa8fca17de72df6a4`.
The live GitHub inspection found the PR open, draft and mergeable, with no submitted reviews. The complete main-relative diff comprises 28 files, 3,401 additions and 45 deletions. All changed source, tests, fixture, schema, client, workflow and documentation were examined, together with the imported retrieval algorithms and public-data scanner. No reconciliation was repeated.

Three medium-priority defects were reproduced on synthetic inputs and corrected. No production data exposure was observed or tested. The two privacy defects require problematic text in publisher-approved metadata, or an incompatible output encoding; these are boundary-validation defects, not evidence of an unauthenticated network exploit.

## Confirmed findings and corrections

### R400-01 / P2: output encoding bypasses the fixed public error boundary

Original references: [query_public_v01.py, lines 44–50](https://github.com/tws9stmcbf-web/AkashicNET/blob/98f37442b9c293c43120b23bdc6b2b67f3448d97/scripts/query_public_v01.py#L44-L50) and [public_retrieval_snapshot_v01.py, lines 26–35](https://github.com/tws9stmcbf-web/AkashicNET/blob/98f37442b9c293c43120b23bdc6b2b67f3448d97/scripts/public_retrieval_snapshot_v01.py#L26-L35).

An approved concept label containing an escaped lone surrogate (`\ud800`) passes the text validator and `json.dumps(..., ensure_ascii=False)`. The subsequent `print(rendered)` was outside `try`. Under UTF-8 output, the process exits with a `UnicodeEncodeError` traceback disclosing the local script path instead of the constant diagnostic. An ordinary multilingual label with `PYTHONIOENCODING=ascii:strict` reproduces the same error-boundary failure without malformed input.

Correction: reject surrogate code points during public text projection, preflight the complete serialized response against the output encoding, and perform the write and immediate flush inside the protected block. No replacement or lossy decoding is used. Valid Unicode, including Punjabi and supplementary-plane emoji, remains supported. Invalid rows are excluded using the existing row-level policy; output encoding failure returns the existing constant error and no success payload.

Regressions in `tests/test_public_retrieval_boundary_v01.py`:

- `test_lone_surrogates_are_excluded_before_output_encoding` (both routes; high and low lone surrogates).
- `test_output_encoding_error_has_constant_public_diagnostic`.
- `test_valid_multilingual_and_non_bmp_text_survives_public_projection` (positive control).

### R400-02 / P2: recognizable local paths survive approved text fields

Original reference: [public_retrieval_snapshot_v01.py, lines 26–35](https://github.com/tws9stmcbf-web/AkashicNET/blob/98f37442b9c293c43120b23bdc6b2b67f3448d97/scripts/public_retrieval_snapshot_v01.py#L26-L35).

The existing marker list recognizes `/home/` and `/users/`, but not Windows separators, drive-rooted paths, UNC paths, `/root/`, `/tmp/`, `/workspace/` or home-relative paths. Placing `C:\Users\private-canary\notes.txt` or `/root/private-canary/notes.txt` after the matching text in an approved concept label yields exit 0 and returns the full path in every matching concept result. Direct-unit labels exhibit the same problem. The repository scanner adds no protection for these strings under ordinary label keys.

Correction: normalize separators for known-marker detection, reject drive-rooted Windows/UNC/home-relative paths, and recognize selected standard POSIX local roots. The new POSIX check uses a boundary so an ordinary public URL such as `https://example.org/media/topic` remains allowed. Twenty subprocess regressions cover ten path forms across both public routes.

Regression: `test_recognizable_local_paths_are_excluded_from_allowed_text`.

Limit: this is recognizable-marker screening, not a proof that approved prose is non-confidential. Arbitrary relative filenames, opaque provider identifiers, deliberately encoded strings and confidential prose still require trustworthy publisher review. The fix does not grant permission or claim complete data-loss prevention.

### R400-03 / P2: repeated family membership double-counts a public unit

Original references: [public_retrieval_snapshot_v01.py, lines 142–159](https://github.com/tws9stmcbf-web/AkashicNET/blob/98f37442b9c293c43120b23bdc6b2b67f3448d97/scripts/public_retrieval_snapshot_v01.py#L142-L159), [query_multihop_v022.py, lines 34–36](https://github.com/tws9stmcbf-web/AkashicNET/blob/98f37442b9c293c43120b23bdc6b2b67f3448d97/scripts/query_multihop_v022.py#L34-L36), and `query_ranked_v023.py::profile`.

A single approved retrieval unit with `family_ids = ["synthetic:hash", "synthetic:hash"]` passes the loader. The family join then attaches the same unit twice. A one-manifestation hashed unit is reported as two logical units, two physical manifestations and two SHA-verified units. The direct route reports it once, creating inconsistent provenance across routes. The P3 tier and HOLD decision remain unchanged; this is count inflation, not scientific or rights promotion.

Correction: require distinct family IDs in each public unit and exclude the malformed unit before any join, matching, ranking or count. Do not silently repair asserted lineage or change the trusted-local algorithms. An independently eligible concept edge can still appear without that unit as metadata-only, matching existing policy.

Regressions:

- `test_duplicate_family_membership_cannot_inflate_provenance` (concept and direct routes).
- `test_distinct_approved_families_keep_one_unit_per_concept_join` (positive control).

## Controls examined without a new confirmed defect

| Area | Observed behavior and boundary |
| --- | --- |
| Public eligibility | Literal `true` required for both approvals and provenance-public status; approval is checked per row and per representation before joins. Unknown fields are projected away. All unit families must be independently eligible. |
| Provenance and decisions | Record ID binds to the row ID; explicit decisions must agree with review state/accepted flag; library parent acceptance must agree with accepted representations. These structural checks do not authenticate a reviewer or publisher. |
| Evidence statuses | Exact vocabulary and alias equality; unknown/conflicting statuses remain null and match no explicit filter. Sixteen additional explicit-edge/representation status combinations produced the expected result. An explicit edge status with a legacy representation lacking status is intentionally allowed; conflicting supplied statuses are not. |
| Propagation | Reddit uses edge status; library concepts use logical edge/representation status; nested units retain their own status; direct lookup uses unit status. Rank and acceptance do not substitute for source classification. |
| Filtering | Domain, state and evidence filters run before limits. Direct metadata lookup remains distinct from semantic ACCEPT, including under `--state accepted`. |
| Ordering | Canonical source metadata, exact concept/unit identity and returned payload break ties. Ranked retrieval orders joined units; unified/API/public paths preserve this order. Existing reversal and top-one tests pass. |
| Private identifiers | Unknown object fields, manifestations and digest fields are removed; ineligible rows never enter summaries. The corrected marker and error cases close the demonstrated omissions, subject to publisher trust. |
| Fail closed | Invalid roots, duplicate JSON keys, nonfinite constants, ambiguous projected node/unit identities and loader/retrieval exceptions produce the fixed error without fallback. Invalid rows are silently excluded by policy. |
| Tests and CI | The SQLite adapter is explicitly test infrastructure, not the production backend. The workflow executes real subprocess-chain tests separately. Its unchanged dependency-install strategy remains separate from #409. |

Already-covered or intentional cases were not reported as new defects: exact duplicate concept observations remain separate; invalid classifications do not remove otherwise eligible unfiltered metadata; approved concepts can appear in `matched_concepts` without a surviving edge; nested representation/manifestation array order is preserved rather than canonicalized. Trusted-local retrieval still assumes trusted inputs and is not a public authorization boundary.

## Validation and reproducibility

Environment: Linux x86_64, CPython 3.12.14, isolated venv; pytest 9.1.1 and jsonschema 4.25.1. `pip check` passed. This local installation is not claimed to be a hash-locked reproduction of #409.

| Run | Result |
| --- | --- |
| Original nine-file retrieval/privacy suite on reviewed head | **687 passed in 78.57s**, no xfails |
| New cases before runtime corrections | **27 failed, 2 passed**, failures at the intended assertions |
| New cases after runtime corrections | **29 passed** |
| Expanded nine-file suite after corrections | **716 passed in 82.76s**, no failures or xfails |
| Source-binding and historical-preservation regressions | **17 passed, 3 subtests passed** |
| Retrieval bridge and API-compatibility validators | PASS |
| Complete materialized tracked-file public-data scan | PASS |
| Immutable Actions-reference audit and whitespace check | PASS |

The expanded suite uses the same nine test files listed in `.github/workflows/validate-retrieval-evidence-bridge-v078.yml`; all new regressions are in its existing boundary-test file, so no workflow or dependency-lock change is needed. Reproduce the new cases with:

```bash
python -m pytest -q tests/test_public_retrieval_boundary_v01.py \
  -k 'lone_surrogates or output_encoding_error or valid_multilingual or recognizable_local_paths or duplicate_family_membership or distinct_approved_families'
```

Independent follow-up probes preserved a public URL containing `/media/` and supplementary Unicode (six results). Directing the full response to `/dev/full` returned exit 1 and only the constant diagnostic in the tested environment. This is bounded I/O evidence, not a guarantee under unavailable stderr, process termination or every host-stream failure.

The local runs validate the corrected source/test bytes in this commit. Hosted CI results for the eventual published SHA must be inspected separately and are not invented here. The original PR description's 16 successful workflows describe the earlier reconciled head.

## Review scope and remaining work

The correction changes only `scripts/public_retrieval_snapshot_v01.py`, `scripts/query_public_v01.py`, `tests/test_public_retrieval_boundary_v01.py` and this report. No normalization, evidence vocabulary, ranking, stored adjudication, source identity, governed artifact, dependency lock, reconciliation record or existing privacy/rights promotion guard is rewritten.

PR #409 was inspected at `ff4b15c39ed22547615bc109eb9939bbb4126675` and remains a distinct draft experiment. Its branch, seven-file experiment, locks and base targeting must not be modified by this correction. Its future forward integration and renewed hosted validation remain separate work.

Unresolved deployment requirements remain: authenticated and authorized snapshot publication, actual source permissions, approved snapshot production, atomic/durable publication and rollback, deployed authorization and logging, resource bounds, and full integration with newer adjudication artifacts if adopted. These are documented scope gaps, not newly reproduced exploits. No production corpus, live deployment, throughput, concurrency, memory exhaustion, or unseen alternative public interface was tested. Trust in publisher-supplied provenance/rank assertions is not replaced by this loader.

An independent human reviewer should review the three corrections and the complete candidate, inspect final-head validation, and explicitly approve any integration. This AI review is preparatory evidence and must not be recorded as that approval.
