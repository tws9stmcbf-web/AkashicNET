# AkashicNET Drive checkpoint — PRE-ALPHA v0.4.8-dev

Scope: nominated Akashic Library Google Drive tree only.

## Denominator correction

A fresh metadata-only recheck found that `PDF/Montalk` contains 5 direct documents and one child folder (`Not Important`) containing 8 documents. The earlier descendant census recorded 13 at the Montalk parent and then separately counted the 8 child documents, double-counting 8 objects. The corrected corpus denominator is therefore:

- top-level direct documents: 1,287
- corrected descendant documents: 857
- corrected observed document denominator: 2,144

This is a document-object denominator, not a canonical-work count.

## Stage-A canonicalisation screening

Stage-A means metadata-only title/size/provenance screening. It does not mean final canonical IDs have been resolved or hashes verified.

Screened in the cumulative Stage-A workflow:

- all 66 top-level roots: 1,287 documents
- freshly screened descendant documents in this pass: 376
  - Ancient Religions descendants: 131
  - PDF descendants: 135 (corrected)
  - Literature descendants: 98
  - Biographies / David Hume: 4
  - Biographies / Hermann Hesse: 8

Total Stage-A screened document objects: 1,663 / 2,144 = 77.565299%.

Under the scoring convention already used for v0.4.7, the 15-point canonicalisation component credits Stage-A screening coverage linearly while retaining unresolved dispositions such as `REVIEW_REQUIRED`:

- canonicalisation points = 77.565299% × 15 = 11.634795 / 15

## Validation

The 66 top-level root direct-document inventories were independently re-run during Stage-A screening against the earlier root census. For a conservative validation denominator of all 195 known folder nodes, only these 66 independently rechecked root nodes are credited:

- validation coverage = 66 / 195 = 33.846154%
- validation points = 3.384615 / 10

No descendant validation points are awarded yet.

## Verified completion

- traversal: 40.000000 / 40
- metadata inventory: 25.000000 / 25
- canonicalisation Stage-A: 11.634795 / 15
- privacy/public-status: 0.000000 / 10
- validation: 3.384615 / 10

Verified AKASHICNET-004 completion = **80.019410%**.

Therefore the 80% gate is earned and the project advances to:

**AkashicNET PRE-ALPHA v0.4.8-dev — 80%+ verified Library Mapping milestone**

## Caveats

- Stage-A screening completion is not final canonicalisation.
- Identical title and size are strong duplicate-copy evidence but do not prove byte identity without hashes.
- Translations, editions, multi-volume works and aggregate collections remain separate manifestation structures until resolved.
- Folder membership is provenance, not truth or epistemic authority.
- `source_visibility_status=access_not_verified` remains in force; shared Drive access does not establish public permission.
- No privacy/public-status points are awarded in this checkpoint.
