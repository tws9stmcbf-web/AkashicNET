# Retrieval source-classification filter v0.1

Date: 2026-10-13. Status: **DRAFT / HUMAN REVIEW REQUIRED**.
Implements GAP-02 on PR #400, based on
`4ad95255e95b9ae0965e37daae87e2a9fb25b201`. No merge, release or deployment.

## Vocabulary and representation

`--evidence` takes exactly one case-sensitive source status:
`NOT_APPLICABLE`, `UNASSESSED`, or `SOURCE_CLASSIFICATION_ONLY`.
This vocabulary comes from the allowed `evidence_status` values in
`scripts/validate_public_safe_endpoint_registry_v014.py`, its governed fixture,
and `docs/PUBLIC_SAFE_SEMANTIC_ENDPOINT_REGISTRY_V0.1.9.md`.
The regression suite checks vocabulary agreement with the endpoint validator.

This is **source classification**, not a scientific-evidence tier or claim
assessment. `data/evidence_claim_v01.schema.json` separately defines
`EMPIRICAL_REFERENCE`, `HISTORICAL`, `CONTEMPLATIVE_PHILOSOPHICAL`, and
`EXPERIENTIAL_ESOTERIC`, along with claim statuses and assessment states.
Those fields, public evidence legends and canonical identity evidence classes
are not aliases for this filter and are not rewritten or promoted.

| Route | Classification source |
| --- | --- |
| Reddit concept result | The matching reviewed edge's `evidence_status` or fixture alias `evidence` |
| Library concept result | The matching logical edge's explicit status, checked against supplied representation statuses; otherwise unanimous complete representation statuses |
| Direct library lookup | The matching logical retrieval unit's status |
| Library unit nested under a concept result | Its own status is forwarded separately; it does not override the edge status |

The normalized result field is `evidence_classification`, with a supported
string or JSON null. Known unit statuses use `evidence_status`. These optional
fields describe supplied metadata, not a new scientific assessment.

## Matching and missing values

- Exact equality only. No case folding, whitespace trimming, substring match,
  list membership, status precedence, provenance inference or majority vote.
- `evidence_status` and `evidence` may both occur only when their exact values
  agree. An unsupported, malformed, null or conflicting supplied value produces
  an unknown classification; it matches no explicit status, including UNASSESSED.
- Missing classification is unknown. It is never defaulted to UNASSESSED or
  SOURCE_CLASSIFICATION_ONLY based on domain, rights, review state or rank.
- An explicit library edge status can coexist with legacy representations that
  carry no classification. Any explicitly supplied conflicting/invalid
  representation prevents a match. Without an explicit edge status, every
  representation must carry the same supported status.
- The semantic normalizer preserves supplied representation status aliases and
  aggregates only complete unanimous classifications; ambiguous groups stay null.
- Omitting `--evidence` retains all otherwise eligible results, including unknown
  classifications. The original required response fields and API versions remain
  unchanged; the request adds `evidence` only when supplied.

## Interface and controls

The API v0.25 forwards the option to unified retrieval v0.24. Both use the same
shared filter as `query_public_v01.py`. The example v0.26 consumer accepts an
optional final `evidence` argument. Existing positional calls remain valid.
The lower-level multihop/ranked stages forward classifications and continue
ranking only on the existing provenance profile.

All domain, state and evidence predicates run before slicing to `--limit`.
Counts describe the filtered result set; the existing matched-concept summary
continues to describe query matching, not a claim that each concept has a
returned result. The filter neither changes nor reorders surviving rows.

The public route still reads one explicit snapshot, gates every participating
record/representation on affirmative eligibility and bound public provenance,
and constructs an allowlist before joining, matching, ranking or filtering.
Only supported status strings or null enter the public projection; arbitrary
classification text is never echoed. Invalid public filter requests retain the
constant parser error, and rejected private records never enter counts/results.
There is no fallback to the trusted private-local inputs.

Rights states, source references, adjudication decisions, review requirements,
scientific classifications and all false promotion/truth guards are preserved.
An accepted topical relation is not scientific evidence; a SHA identity is not
a rights grant. No production corpus or approved snapshot was modified.

## Validation scope and remaining requirements

The original strict GAP-02 requirement is now an ordinary regression test.
New synthetic subprocess coverage exercises all supported statuses and aliases
on all three routes, unknown/ambiguous values, domain/state combinations,
filter-before-limit with 150 higher-ranked distractors, conservative normalized
representation aggregation, the public/private boundary, constant public
errors and a deliberate filter-removal negative control.

GAP-03 (Reddit adjudication-reference forwarding) and GAP-04 (equal-key ordering)
remain separate strict expected failures. The obsolete historical v0.16
base-commit gate remains separate from the repaired Petranker digest and GAP-02.
Synthetic integration checks do not certify a deployment, publisher authenticity,
source permission, clinical efficacy or independent research validity.

The exact tested commit, local results and remote Actions checks are recorded in
PR #400 after validation. Historical checkpoint reports retain their original
results; this document supersedes only their claim that evidence filtering is
unsupported in the current interface.
