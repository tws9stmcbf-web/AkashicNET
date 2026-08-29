# Canonical promotion checkpoint v0.6.1

Date: 2026-08-29

Status: evidence-gated promotion layer over the v0.6.0 live-corpus canonical baseline.

## Scope

This checkpoint does not reclassify the 2,459-object baseline. It promotes only relationships for which Stage-B adjudication and persisted SHA-256 evidence jointly support a stronger canonical statement.

## Accepted promotions

Three logical works are promoted:

1. `work:alice-a-bailey-discipleship-new-age-vol-1`
   - two manifestations
   - SHA-256 match: `HASH-0001`
   - relation: verified duplicate-copy pair
2. `work:alice-a-bailey-discipleship-new-age-vol-2`
   - two manifestations
   - SHA-256 match: `HASH-0002`
   - relation: verified duplicate-copy pair
3. `work:franz-bardon-golden-book-of-wisdom`
   - two manifestations
   - SHA-256 match: `HASH-0003`
   - relation: verified duplicate-copy pair

Graph output: 6 `REPRESENTS` edges + 3 `DUPLICATE_OF` edges = 9 accepted edges.

## Holds

Twelve Stage-B subjects remain `HOLD`. Metadata-only family alignment, collection overlap, edition labels, differing file sizes or author overlap are preserved as adjudication evidence but are not promoted into stronger canonical identity claims.

Notably:
- Abramelin remains a same-logical-work family without manifestation-level byte identity.
- Forbidden History preserves multi-volume / edition-or-copy distinctions.
- Agrippa preserves numbered-work versus aggregate distinctions.
- Bardon edition/copy variant sets remain unresolved except for the independently hash-verified Golden Book pair.
- Ramayana remains unresolved cross-collection provenance debt.
- Vivekananda remains a related-author classification rather than a duplicate collapse.

## Deliberate non-promotions

- edition IDs promoted: **0**
- translation relationships promoted: **0**
- public/right-cleared states promoted: **0**
- scientific-evidence states promoted: **0**

Matching hashes prove byte identity for the specific compared files only. They do not establish copyright status, truth, scientific support or public-release eligibility.

## CI contract

`scripts/validate_canonical_promotions_v061.py` requires:
- exactly 15 decision rows: 3 ACCEPT and 12 HOLD
- exactly 3 promoted work IDs
- exactly 9 graph edges
- every ACCEPT to cite a persisted matching SHA-256 record
- every graph edge to derive from an ACCEPT decision
- all referenced manifestations and work IDs to exist
- no edition promotion
- rights state to remain `UNKNOWN_UNVERIFIED`
- scientific evidence state to remain `NOT_EVALUATED`

This advances Issue #21 from complete object-level disposition coverage into reproducible evidence-backed canonical promotion while preserving fail-closed uncertainty.
