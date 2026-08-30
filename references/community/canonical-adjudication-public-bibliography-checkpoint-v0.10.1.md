# Canonical public-bibliography checkpoint v0.10.1

Date: 2026-08-30

Issue: #69 — Resolve one canonical HOLD with reproducible public bibliography.

## Deterministic selection

The selection rule is deliberately simple and reproducible: take the first candidate in `canonical-adjudication-batch2-v0.7.2.json` whose decision is `HOLD`. This selects `CANON-B2-ABRAMELIN`. The other five batch-2 candidates are not re-adjudicated in this checkpoint.

## Exact relationship tested

**Relationship:** `REPRESENTS_WORK`

The S. L. MacGregor Mathers English translation titled *The Book of the Sacred Magic of Abramelin the Mage* and the Georg Dehn / Steven Guth 2006 English translation titled *The Book of Abramelin: A New Translation* represent the same underlying Abramelin work family.

This checkpoint does **not** assert that they are the same edition, same translation, same manifestation, or byte-identical copies.

## Public bibliography

Two independent public library authority/catalogue records are used:

1. **WorldCat — OCLC 1990985**  
   `https://search.worldcat.org/title/1990985`  
   Records *The book of the sacred magic of Abramelin the mage*, with Abraham ben Simeon and S. L. MacGregor Mathers, as an English print book published by Dover Publications in 1975.

2. **CiNii Books — BB06860691**  
   `https://ci.nii.ac.jp/ncid/BB06860691`  
   Records *The book of Abramelin: a new translation*, compiled/edited by Georg Dehn and translated by Steven Guth, Ibis Press, 2006, ISBN 9780892541270. The authority record lists *Book of the sacred magic of Abramelin the mage* as an alternative title and notes the relationship of the 2006 translation to Mathers's earlier translation.

These sources are sufficient to establish only the shared work-family relationship. They also preserve the important distinction that the publications are different translations/editions.

## Decision

`CANON-B2-ABRAMELIN`: **ACCEPT** for `REPRESENTS_WORK` only.

Rationale: reproducible public bibliography independently identifies the Mathers and Dehn/Guth publications within the same Abramelin work lineage while distinguishing their translation and publication histories.

## Unchanged HOLDs

The following remain exactly at the prior decision level:

- `CANON-B2-FORBIDDEN-HISTORY` — HOLD
- `CANON-B2-AGRIPPA` — HOLD
- `CANON-B2-BARDON-VARIANTS` — HOLD
- `CANON-B2-RAMAYANA` — HOLD
- `CANON-B2-VIVEKANANDA` — HOLD

## Explicit non-promotions

This adjudication does not promote or infer:

- edition identity;
- translation identity;
- duplicate-copy or byte identity;
- rights or public-release status;
- scientific-evidence status;
- truth or metaphysical validity;
- safety or efficacy.

No private Drive IDs, filenames, paths, timestamps, sizes, or object-linked hashes were inspected or published for this adjudication.
