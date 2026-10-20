# Reddit adjudication-reference forwarding (GAP-03)

Scope: draft PR #400, continuing from
`1ece3932d997892ad33942034110b328e871a8a2`. This is a retrieval metadata
correction, not a new adjudication, scientific assessment or public approval.

## Trace and correction

| Stage | Review-reference handling |
| --- | --- |
| Upstream / v0.22 normalizer | Existing Reddit edges, including their `review_id`, pass through unchanged. Some legacy v0.21-generated edges have no review ID. |
| Multihop v0.22 | Previously omitted the Reddit review ID when constructing `concept_hop`. Now copies `e.get('review_id')` into `concept_hop.review_id`. |
| Ranked v0.23 | Retains the hop while computing the existing provenance profile and deterministic ordering. |
| Unified v0.24 | Retains the hop through domain, state and evidence filtering, before limits. |
| API v0.25 | Returns unified results unchanged. |
| Public v0.1 | Validates and projects the snapshot before shared retrieval; review IDs must already be permitted identifiers with matching approved provenance. |

The supplied ID is copied verbatim, with no case folding, derived replacement,
lookup, concatenation or source-reference rebinding. Missing and explicit-null
IDs yield JSON `null` on the trusted-local path. Retrieval does not manufacture
an authoritative identity for an unreferenced legacy observation. The public
loader continues excluding missing, malformed, private-marker, unapproved or
unbound review IDs before matching, ranking, counts and limits. No fallback to
the trusted-local data is introduced.

Only the Reddit result constructor changes at runtime. Human decision precedence,
review states, source references, evidence classifications, provenance profiles,
rights, promotion guards and eligibility rules are unchanged. Library review
references remain in `representation_sources`.

## Compatibility and ordering

`concept_hop.review_id` is an additive nested field, permitted by the existing
open v0.25 schema. No new required input or schema/API version is introduced.
The trusted-local interface retains its trust assumption and is not made into
a public endpoint. Public reference safety still depends on an honest,
authorized snapshot publisher; a syntactically valid ID is not proof of permission.

No ranking algorithm or provenance rank changes. When two observations differ
only in review ID, the existing canonical-payload final tie-break now sees
that difference. They remain separate and sort deterministically, including
under truncation. Previously those returned payloads were indistinguishable.
Multihop itself remains candidate construction in input order, not a ranker.
No observation is deduplicated, reconciled or promoted by this correction.

## Regression evidence

The original GAP-03 contract was run with `--runxfail` at the preceding head
and failed specifically because the returned review ID was absent. Its xfail
marker is removed with this correction.

`tests/test_reddit_review_reference_v01.py` uses the existing byte-for-byte CLI
copy harness and synthetic inputs. It checks all five retrieval stages, exact
distinct references with ACCEPT/HOLD/REJECT and different evidence classes,
same-source/same-concept reviews that differ only in ID, reversed insertion
order and limits, missing/null legacy IDs, normalization preservation, public
rejection before counts/limits, and unchanged stored inputs. Deliberately dropped
or fabricated IDs in isolated script copies execute successfully and are caught
by the forwarding oracle. The retrieval workflow includes these regressions.

Exact tested commit/tree, expanded test counts and workflow identities belong
to the accompanying validation receipt and PR checkpoint. These bounded tests
do not establish production corpus completeness, newer adjudication-artifact
integration, publisher authenticity, source permission, deployment authorization,
atomic publication or scientific validity. The independent historical v0.16
base-position workflow failure remains outside GAP-03.

Keep PR #400 draft. No merge, release, deployment or scientific/rights promotion.
