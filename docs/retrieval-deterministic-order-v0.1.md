# Deterministic retrieval ordering (GAP-04)

Follow-up: [GAP-03 review-reference forwarding](reddit-review-reference-v0.1.md)
restores Reddit review IDs. Its distinct review-only observations now use the
existing final payload tie-break. GAP-03 statements below describe this earlier
GAP-04 checkpoint.

Scope: draft PR #400, continuing from `4f8bf09146dcdc26011a402854f11897e32d2b95`.
No merge, release, deployment or change to human adjudication is authorized by
this engineering checkpoint.

## Construction and ordering

| Stage | Behavior |
| --- | --- |
| Multihop v0.22 | Matches concept IDs and builds Reddit observations and family/unit joins; candidate construction order follows source arrays. It does not promise ranked output. |
| Ranked v0.23 | Computes the existing provenance profile, constructs direct-family fallback, then orders all candidates deterministically. |
| Unified v0.24 | Preserves that order while filtering by domain, semantic state and source classification, before applying the limit. |
| API v0.25 | Preserves unified request, policy, summary and results. |
| Public v0.1 | Projects an explicitly eligible metadata snapshot before joins, matching and ranking, then uses the same ranker and filters. No private-local fallback. |

The old key was descending provenance rank, domain and `str(source)`. Distinct
observations of the same source across different concepts could have identical
keys; stable Python sorting retained insertion order and changed top-one results.
Dictionary representation also depended on dictionary insertion order.

The new ascending tuple is:

1. Negative provenance rank (unchanged P3, P2, P1, P0 precedence).
2. Domain.
3. Canonical JSON of source metadata, with sorted dictionary keys.
4. Canonical JSON of exact source type/family/ref, query path, target concept ID,
   relationship, sorted logical unit IDs and concept label.
5. Canonical JSON of the returned candidate payload, as a final discriminator
   when duplicate identities have different returned metadata.

Canonical JSON uses sorted object keys, compact separators and ASCII escaping.
There is no randomized hash, input offset, new score, external lookup or exposed
ordering field. The final discriminator compares payloads rather than a digest,
so there is no hash collision that can silently equate different returned rows.

Logical units attached to a concept are ordered by exact unit ID and canonical
unit payload, without rewriting their metadata, rights or manifestation lineage.
The private direct route retains its existing suppression of repeated
family/unit identities but visits units in that same deterministic order first.
If trusted local data repeats a direct identity with conflicting metadata,
the canonical first payload is repeatably selected; this is not reconciliation
or clearance. Public duplicate unit IDs still reject the snapshot. Conflicting
identity data should be corrected upstream rather than treated as authoritative.

Distinct target concept IDs and distinct unit IDs remain distinct results even
when labels or sources coincide. Concept observations are never deduplicated by
this change. Exact duplicate returned observations remain separate and compare
equal because their output is indistinguishable. Different review records whose
only difference is a Reddit review ID remain subject to the independent GAP-03:
v0.22 still drops that review ID. GAP-04 does not repair or mask that missing field.

## Compatibility and guards

Source metadata now has a canonical key instead of Python dictionary repr.
Ordering within a provenance/domain tier can therefore change, which is the
intended correction. Provenance ranks, acceptance/hold/rejection, evidence
classification, rights states, API/schema versions, filters and eligibility rules
are unchanged. No representation vote or scientific/rights promotion is added.
Nested representation and manifestation metadata is preserved as supplied;
this is candidate/unit ordering, not a normalization of every metadata sequence.

Public ordering uses only fields admitted by the existing public projection.
Private filenames, object IDs, hashes and rejected candidates do not become
ordering inputs or response fields. The obsolete public GAP-04 override is
removed, allowing the unified deterministic-order declaration to apply.

## Validation

`tests/test_retrieval_tie_break_v01.py` adds 43 cases using real CLI copies and
independent expected identities. Coverage includes accepted and held Reddit and
library observations with identical source keys and identical concept labels;
reversed edge/concept order; limits 1, 2 and 100; direct-unit identities; exact and
conflicting duplicate observations; legacy direct duplicate suppression; public
duplicate-unit rejection; multiple-unit join order; stage construction/ordering;
dictionary insertion order; and rejected public canaries before ranking/counts.
A deliberate removal of the tie-break in an isolated script copy must execute
successfully and be detected by the top-one reversal oracle.

The original `test_contract_equal_rank_keys_require_stable_tie_break` is an
ordinary regression now. GAP-03 retains its strict expected-failure marker.
The retrieval workflow runs the new suite. Validation receipts record exact
commit/tree IDs, local suite counts and Actions run identities separately.
Successful synthetic tests do not certify production authorization, publisher
authenticity, source permission, atomic publication or full backend continuity.
