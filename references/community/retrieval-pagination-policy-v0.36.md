# AkashicNET retrieval pagination policy v0.36

## Milestone
Stable logical result identifiers and deterministic cursor pagination without changing semantic decisions, provenance ranking meaning, rights state, or evidence status.

## Stable result IDs
`result_id` is derived from logical identity fields, not the row's current rank or list position. It is not a document-content hash, rights assertion, truth claim, scientific-evidence claim, or physical manifestation identifier.

## Ordering
Rows are sorted deterministically by provenance support rank, semantic-decision class, domain, and stable result ID. Ranking remains retrieval/provenance support only and cannot change semantic decisions.

## Cursor
The cursor is opaque to consumers and bound to query + domain + semantic-state filter. Reusing a cursor with a different request is rejected. Pagination is deterministic for a fixed corpus snapshot; corpus changes may change membership and offsets.

## Limits
Page size is 1–100. The current pre-alpha adapter scans at most 1000 upstream results. This is a bounded compatibility layer, not a claim of complete corpus pagination beyond that scan window.

## Guardrails
- truth inference: OFF
- rights promotion: OFF
- scientific-evidence promotion: OFF
- stable ID does not imply canonical identity beyond the logical retrieval row
- stable ID does not imply byte identity
- pagination does not alter ACCEPT/HOLD/REJECT/DIRECT_METADATA_LOOKUP
