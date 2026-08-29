# AKASHICNET-006 — Public Manifest Rights Gate

Date: 2026-08-29
Status: SPECIFICATION + LEDGER INITIALISED

## Purpose

Prevent the AkashicNET public manifest from treating Drive accessibility, catalogue membership, filename similarity, or source discovery as evidence of publication rights.

## Allowed public-status states

- `PUBLIC_VERIFIED` — explicit public-domain, open-licence, or other documented permission basis recorded.
- `PRIVATE` — not eligible for public publication.
- `SHARED_RESTRICTED` — accessible to a limited audience but not cleared for public redistribution.
- `UNKNOWN_UNVERIFIED` — rights status not established.

## Gate rule

Only `PUBLIC_VERIFIED` records may enter a public-content manifest.

`PRIVATE`, `SHARED_RESTRICTED`, and `UNKNOWN_UNVERIFIED` records may remain in the private provenance/index layer where permitted, but must not be exposed as publicly redistributable content.

## Evidence hierarchy

1. Explicit licence or public-domain statement attached to the work/source.
2. Reliable rights metadata from the authoritative source.
3. Documented ownership/permission supplied by the rights holder.
4. Work-specific legal/public-domain determination with jurisdiction and date recorded.

Search-engine discovery, Drive accessibility, identical filenames, identical file sizes, or archive membership are **not** rights evidence.

## Current status

The connected Google Drive capability available to this workflow does not expose a sufficiently authoritative permission/licence field for the imported corpus. Therefore the imported corpus remains `UNKNOWN_UNVERIFIED` until rights evidence is independently recorded.

This is intentional. The project must not manufacture a 100% rights score.

## Completion condition for the final 10-point gate

A rights audit is complete only when every object intended for the public manifest has an auditable rights basis and every excluded object has an explicit exclusion state. A final reconciliation must demonstrate that no `UNKNOWN_UNVERIFIED` or restricted object is present in the public manifest.

## Epistemic boundary

Rights clearance is separate from scientific evidence status. A public-domain text may still contain unsupported claims; public accessibility does not make those claims scientifically valid. AkashicNET therefore maintains separate provenance, rights, and evidence fields.
