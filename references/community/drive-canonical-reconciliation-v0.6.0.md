# Drive canonical reconciliation v0.6.0

Date: 2026-08-29
Status: full live-object baseline established; work-family adjudication continues
Scope: corrected v0.5.0 Drive snapshot only

## Frozen source

The baseline is generated from successful recursive Drive census artifact `9713170876` (run `33247025163`), ZIP SHA256:

`d0a1c3d0a83a6367f086097c5bdab9880c990754a3f1226e6714b141b7f4717b`

The frozen source contains **2,459 unique non-folder Drive objects** under **199 unique folders** from **66 nominated roots**.

## Full object-level baseline

Every live object now has a conservative baseline disposition:

| Baseline disposition | Objects | Meaning |
|---|---:|---|
| `UNIQUE_CANDIDATE` | 2,173 | No exact raw filename + size peer in this snapshot; this is not yet a confirmed canonical work. |
| `REVIEW_REQUIRED` | 258 | Member of an exact raw filename + size candidate family; stronger evidence is required before any duplicate/work promotion. |
| `TECHNICAL_EXCLUSION` | 28 | 16 zero-byte objects, 11 `.DS_Store` artefacts and 1 `.crdownload`. |
| **Total** | **2,459** | **100% of the live physical-object denominator** |

The metadata grouping contains **127 exact filename + size families involving 269 objects**. One family is the 11-object `.DS_Store` technical family. Therefore **126 non-technical families involving 258 objects** remain in the canonical review queue.

No canonical work IDs or edition IDs are automatically promoted by this baseline.

## Relationship to existing Stage-B adjudication

This baseline does **not** erase or downgrade the existing Stage-B evidence in:

- `drive-canonical-resolution-stage-b-batch-0001.csv`
- `drive-canonical-resolution-stage-b-batch-0002.csv`
- `drive-canonical-resolution-stage-b-batch-0003.csv`
- `drive-canonical-resolution-stage-b-batch-0004.csv`
- `drive-canonical-resolution-stage-b-graph-overlay.csv`
- `drive-canonical-resolution-stage-b-progress.md`

Those files contain prior explicit family-level adjudication such as Abramelin work-family grouping and the multi-volume Forbidden History of Europe structure. They remain evidence overlays and must be translated into the merged canonical-resolution v0.1 contract before graph promotion.

The object baseline is deliberately more conservative because its job is denominator completeness, not to infer equivalence from metadata alone.

## Resolution order

1. Map existing Stage-B adjudications into canonical-resolution v0.1 records.
2. Reconcile `hash-verification-results-v0.16.csv` and promote `DUPLICATE_COPY` only where byte/hash evidence supports it.
3. Adjudicate the remaining exact-name+size review families while preserving editions, translations, volumes and aggregate collections.
4. Assign stable `work:*` and `edition:*` IDs only to accepted resolutions.
5. Emit Corpus Graph edges only from accepted decisions with recorded provenance/evidence.

## Non-negotiable guardrails

- title + size similarity is a review signal, not byte identity;
- folder placement is provenance, not semantic truth;
- a unique filename is not proof of a unique work;
- canonicalisation does not establish scientific truth;
- provenance is not evidence;
- public-release eligibility remains independently fail-closed;
- Reddit provenance remains separate until an explicit bridge is adjudicated.

## Milestone interpretation

The live Drive corpus now has **100% physical-object canonical disposition coverage at baseline level**. Issue #21 remains open because canonical-work resolution is an adjudication task: the 126 non-technical candidate families and earlier Stage-B decisions still require evidence-aware reconciliation before work/edition promotion is complete.
