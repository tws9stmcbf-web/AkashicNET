# AKASHICNET-004 — v0.4.6-dev metadata checkpoint

Status: PRE-ALPHA

This checkpoint records a conservative, denominator-based estimate for the Google Drive library-mapping phase.

## Verified scoring

- Known folder-node denominator: 195
  - 66 top-level roots
  - 115 immediate child folders
  - 14 known deeper child folders
- Structurally closed roots: 65 / 66 = 98.4848%
- Traversal contribution: 39.3939 / 40
- Metadata nodes with exact direct-document / direct-folder counts: 185 / 195 = 94.8718%
  - 66 root nodes from `drive-metadata-root-census.csv`
  - 119 exact descendant nodes from `drive-metadata-descendant-census.csv`
- Metadata contribution: 23.7179 / 25
- Conservative verified total: 63.1119%

No points are awarded yet in this checkpoint for canonicalisation/deduplication, privacy/public-status classification, or validation. This makes the score intentionally conservative.

## Release gate

- v0.4.1-dev >=10%: earned
- v0.4.2-dev >=20%: earned
- v0.4.3-dev >=30%: earned
- v0.4.4-dev >=40%: earned
- v0.4.5-dev >=50%: earned
- v0.4.6-dev >=60%: earned
- v0.4.7-dev >=70%: not yet earned

Current milestone: **AkashicNET v0.4.6-dev — Library Mapping: 60%+ verified milestone**.

## Remaining metadata uncertainty

The descendant census currently contains 121 rows: 119 EXACT and 2 PARTIAL. The two explicit partial rows are:

1. Ancient Religions / Gnosis — document count observed, but child-folder closure remains ACCESS_UNRESOLVED after a connector-level access failure.
2. Apocrypha / Gospels — subtree size is known from earlier traversal, but the direct-versus-descendant object split still requires reconciliation.

Together with known folder nodes not yet represented by exact descendant-census rows, 10 of the 195 known folder nodes remain outside the exact-metadata numerator.

## Important interpretation

Drive file objects are not equivalent to canonical works, independent sources, or evidence. The intended model remains:

`Drive object -> usable document -> edition/copy -> logical volume -> canonical work -> author -> tradition -> concepts -> claims -> supporting/conflicting sources -> evidence state`

Folder membership is provenance/context, not a truth or evidence rating. Duplicate and cross-listed collections should become `appears_in` relationships around canonical works rather than inflating the corpus.

## Privacy boundary

This checkpoint is metadata-only. No document bodies were fetched for the census. No Drive object has been promoted to the public manifest by this work. Shared access is not treated as proof of public availability; public inclusion still requires explicit verification.
