# AkashicNET Hash Evidence Schema v0.15

## Scope

This schema prepares controlled byte-identity verification for manifestation nodes already identified by immutable Google Drive document IDs.

It does **not** hash files automatically and does **not** change the current metadata-only ingestion boundary.

## Hash evidence record

Required fields:

- `hash_record_id`
- `family_id`
- `manifestation_node_ids`
- `algorithm` = `SHA-256`
- `hash_execution_state`
- `comparison_state`
- `evidence_scope`
- `observed_at`
- `review_state`

Allowed `hash_execution_state` values:

- `NOT_AUTHORISED`
- `AUTHORISED_NOT_RUN`
- `COMPLETED`
- `FAILED`

Allowed `comparison_state` values:

- `NOT_COMPARED`
- `MATCH`
- `MISMATCH`
- `PARTIAL`

## Identity rules

- Equal title and equal file size are **candidate evidence only**.
- Byte identity may be asserted only when SHA-256 values for all compared manifestations are available and equal.
- A `MATCH` is evidence of byte identity for the compared raw objects only; it is not a truth claim, rights clearance, scientific validation, or endorsement.
- A `MISMATCH` preserves both manifestations as distinct physical objects.
- Hashing must never change rights state.

## Privacy and provenance boundary

The queue may contain immutable Drive IDs, filenames, sizes, collection paths, and canonical-family identifiers.
Raw file bytes are not stored in the graph or repository.

Current execution policy for v0.15:

`hash_execution_state = NOT_AUTHORISED`

Therefore:

- hashes computed = 0
- byte-identity assertions = 0
- rights promotion = disabled
- scientific-evidence promotion = disabled
- truth inference = disabled
