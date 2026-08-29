# AkashicNET Drive checkpoint — PRE-ALPHA v0.4.8-dev

Scope: nominated Akashic Library Google Drive tree only.

## Corrected denominator

A fresh metadata-only recheck found that `PDF/Montalk` contains 5 direct documents and one child folder (`Not Important`) containing 8 documents. The earlier descendant census recorded 13 at the Montalk parent and then separately counted the 8 child documents, double-counting 8 objects. The corrected corpus denominator is therefore:

- top-level direct documents: 1,287
- corrected descendant documents: 857
- corrected observed document denominator: 2,144

This is a physical/document-object denominator, not a canonical-work count.

## Stage-A canonicalisation screening

Stage-A means metadata-only title/size/provenance screening and explicit admission into the canonicalisation workflow. It does not mean final canonical IDs have been resolved or hashes verified.

The cumulative screening ledgers now account for the entire corrected denominator:

- initial Stage-A root batches: 750 documents
- remaining 51 root batches: 537 documents
- non-PDF descendant expansion: 722 documents
- corrected PDF descendant batch: 135 documents

750 + 537 + 722 + 135 = 2,144 screened document objects.

Canonicalisation Stage-A coverage = 2,144 / 2,144 = 100%.

Under the scoring convention already used for v0.4.7, the 15-point canonicalisation component credits Stage-A screening coverage linearly while retaining unresolved dispositions such as `REVIEW_REQUIRED`:

- canonicalisation points = 15.000000 / 15

This does not imply that every duplicate, edition, translation, aggregate or multi-volume relationship has been finally resolved. It means no observed document object remains outside the Stage-A screening queue.

## Validation

The 66 top-level root direct-document inventories were independently re-run during Stage-A screening against the earlier root census. For the conservative validation denominator of all 195 known folder nodes, only these 66 independently rechecked root nodes are credited:

- validation coverage = 66 / 195 = 33.846154%
- validation points = 3.384615 / 10

No descendant validation points are awarded yet.

## Privacy/public-status

No global privacy/public-status points are awarded. Shared Drive access remains `access_not_verified` and is not treated as public permission. Public-manifest inclusion still requires separate public verification.

## Verified completion

- traversal: 40.000000 / 40
- metadata inventory: 25.000000 / 25
- canonicalisation Stage-A: 15.000000 / 15
- privacy/public-status: 0.000000 / 10
- validation: 3.384615 / 10

Verified AKASHICNET-004 completion = **83.384615%**.

Therefore the project remains:

**AkashicNET PRE-ALPHA v0.4.8-dev — 80%+ verified Library Mapping milestone**

The v0.4.9 / 90% gate is not yet earned. With Stage-A screening now closed, the next measurable gains must come from deeper canonical resolution, descendant validation, and privacy/public-status classification rather than merely adding more objects to the screening queue.

## Canonicalisation hierarchy

`Drive object -> usable document -> copy/edition/translation -> logical volume -> canonical work -> appears_in collection`

Downstream dispositions include `UNIQUE_CANDIDATE`, `DUPLICATE_COPY`, `SAME_DRIVE_OBJECT_MULTICOLLECTION`, `DUPLICATE_WORK`, `EDITION_VARIANT`, `TRANSLATION_VARIANT`, `MULTI_VOLUME_MEMBER`, `AGGREGATE_COLLECTION`, `TECHNICAL_EXCLUSION`, and `REVIEW_REQUIRED`.

## Caveats

- Stage-A screening completion is not final canonicalisation.
- Identical title and size are strong duplicate-copy evidence but do not prove byte identity without hashes.
- Translations, editions, multi-volume works and aggregate collections remain separate manifestation structures until resolved.
- Folder membership is provenance, not truth or epistemic authority.
- No privacy/public-status points are awarded in this checkpoint.
