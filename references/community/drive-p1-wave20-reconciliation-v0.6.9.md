# P1 wave20 reconciliation v0.6.9

## Scope

This note reconciles two merged v0.6.8 aggregates that both covered the same deterministic queue window: rows 31–50 (20 P1 families / 40 Drive objects).

- PR #40 is the authoritative first adjudication of this window: 20/20 families `BYTE_IDENTICAL_VERIFIED`, 33,041,612 queue bytes.
- PR #44 duplicated the same window and reported 15 byte-identical / 5 mismatches from a delayed local-path hashing workflow.

## Root cause

The delayed workflow relied on local downloaded PDF paths after subsequent connector activity. Some local artefacts were later overwritten or replaced, so delayed hashes were not guaranteed to correspond to the originally fetched Drive object.

## Re-verification

The five families reported as mismatches by PR #44 were re-fetched from Google Drive and hashed immediately after each fetch, before any subsequent same-name download.

For all five disputed families:

- local byte count exactly matched the deterministic queue member size;
- both members of each family produced the same SHA-256 digest;
- therefore the five PR #44 mismatch claims are invalidated.

No object-level Drive IDs or SHA-256 values are published in this reconciliation note.

## Canonical result

- 20 families adjudicated in this queue window
- 40 objects
- 20 `BYTE_IDENTICAL_VERIFIED`
- 0 `BYTE_MISMATCH`
- 0 hash failures
- incremental families contributed by PR #44: **0**
- unresolved byte-identity review surface after this window remains **75 families**

## Required execution rule

Every future Drive hash adjudication must use:

`fetch object -> verify expected size -> hash immediately -> persist digest privately -> only then fetch another same-name object`

A delayed batch must never derive SHA-256 from mutable local download paths.

## Guardrails

Byte identity does not establish canonical work identity, edition identity, rights status, public-release status, or scientific evidence. Those remain separately adjudicated and fail-closed.
