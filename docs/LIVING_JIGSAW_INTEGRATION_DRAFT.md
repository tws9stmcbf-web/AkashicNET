# Living Jigsaw integration proposal

Status: DRAFT / HUMAN_REVIEW_REQUIRED
Date: 2026-09-27
Scope: editorial design and integration specification only

## Purpose

Define a separately reviewed Living Jigsaw that connects the Jigsaw of Life, the HUMAN 2.0 7 × 13 Flourishing Matrix and the 19-lens Living Spectrum while preserving each structure's identity, evidence boundaries and publication history.

This document creates no accepted pieces, canonical edges, release or public-site changes. It is not a prerequisite for the bounded AkashicNET v0.17 Evidence Intelligence Beta release.

## Source and verification scope

This proposal derives its counts and starting comparisons from the supplied editorial memo, "Living Jigsaw · Human Review Stage 1", dated 27 September 2026. That memo is AI-assisted triage for human review, not human approval. Its source references are:

- Jigsaw of Life: https://akashicnet.org/jigsaw-of-life
- HUMAN 2.0 matrix: https://akashicnet.org/human-2#matrix
- Working review inventory: https://akashicnet.org/jigsaw-of-life/review

These URLs are source pointers, not immutable snapshots. This PR has not independently re-read or validated the complete live inventories. Before implementing a crosswalk, capture public-safe, attributable versions of all three inventories and record their content hashes and retrieval scope. Do not infer missing labels, entries or source claims.

The 19-lens Living Spectrum integration is requested scope. Its exact labels, order and source version have not been imported or verified in this PR. No mapping to those lenses is asserted here.

## Count contract

| Structure | Working count | Meaning |
|---|---:|---|
| Jigsaw of Life | 47 | 42 questions in seven neighbourhoods, plus five connective questions |
| Flourishing Matrix | 91 | Seven framework lenses × thirteen dimensions; generated coordinate prompts |
| Combined review queue | 138 | Entries in two different structures; not a deduplicated topic count |
| Living Spectrum | 19 proposed source lenses | Separate interpretive layer, pending source verification |
| Accepted new Living Jigsaw pieces | 0 | No human editorial decisions have been recorded |

Do not add 19 to 138 and call the result a unique-topic total. Do not force the new edition to contain 47, 91, 138 or any other predetermined number.

The memo orders matrix lenses as AWAKEN, HOMESENSE, HIERATIC, ADAPT, TRANSCEND, REGENERATE and #METAD. The thirteen dimensions comprise ten core dimensions and Past, Now and Possible Futures. Verify the published dimension labels and order before generating records.

## First human decision: what is a piece?

Choose and document a counting rule before deciding the new edition's size:

- Retain the 47-piece reading map with optional matrix and Spectrum links.
- Adopt a smaller reviewed set that incorporates some matrix questions.
- Define a new set with its own justified count.

No option is selected by this PR. A standalone inquiry, a framework lens, a dimension and a lens–dimension application are distinct record types.

## Proposed review record

Each later machine-readable record should carry:

- a stable review identifier and a record type;
- original source identifier, URL, source version/hash and verification scope;
- original label and any proposed display label;
- a one-sentence question and concrete example;
- an explanation of how it differs from its nearest neighbour;
- proposed relationship: same question, overlap, applies to, contrasts with, or needs review;
- editorial disposition: not reviewed, keep, revise, combine, set aside, or propose addition;
- named target and written rationale for any proposed combination;
- human decision, attribution and date, left empty until actually supplied;
- evidence/interpretation boundary and any privacy, rights or cultural-authority restrictions.

Default disposition is not reviewed. AI suggestions must be stored separately from human decisions. Editorial links are not accepted evidence-graph edges. Combining entries must retain source identifiers and a traceable history.

## Starting comparisons from the Stage 1 memo

These are editorial suggestions, not adopted decisions.

| Source pair | Proposed next review |
|---|---|
| J01 SELF ↔ M01 AWAKEN × Self | Link identity inquiry to lens application; do not automatically merge. |
| J07 RELATE ↔ M02 AWAKEN × Relationships | Review shared wording while preserving distinct roles. |
| J12 Community ↔ M16 HOMESENSE × Community | Check whether the HOMESENSE cell asks a distinct question. |
| J13 REGENERATE ↔ M72 REGENERATE × Regeneration | Replace tautological wording with a concrete inquiry or set the cell aside. |
| J36 TRANSCEND ↔ M62 TRANSCEND × Cosmos | Distinguish practical experience from cosmological interpretation. |
| J37 ADAPT ↔ M45 ADAPT × Resilience | Test overlap against a concrete example. |
| J41 FUTURES ↔ M13/M26/M39/M52/M65/M78/M91 | Link seven future-facing applications without collapsing their contexts. |
| J43 Context ↔ the matrix | Preserve Context as a connector/navigation principle. |

## Acceptance sequence

- [ ] Human editor defines what counts as a Living Jigsaw piece.
- [ ] Verify and pin the 47-piece, 91-cell and 19-lens source inventories independently.
- [ ] Review the 47 questions for distinctness, usefulness and missing inquiries.
- [ ] Review the 91 generated cells by lens; no cell automatically becomes a piece.
- [ ] Map verified Spectrum lenses without claiming one-to-one equivalence.
- [ ] Record additions, revisions, proposed combinations and set-aside entries with provenance.
- [ ] Derive counts by record type; separately report review status and unique-piece counts.
- [ ] Human editor signs off the selected set and changelog.
- [ ] Implement an accessible prototype: semantic links, keyboard navigation, visible focus, touch access, text equivalent, reduced motion and mobile/zoom checks.
- [ ] Review the exact implementation and separately approve publication.

No schema, complete inventory, crosswalk implementation, runtime prototype or human sign-off is claimed in this documentation-only slice.

## Related work and release boundaries

- #379: PRISM inquiry infrastructure and an ecosystem jigsaw illustration. That architecture illustration is not this Living Jigsaw inventory.
- #304: HUMAN 2.0 and METAD-AK page work. Check compatibility rather than overwriting its historical framework.
- #367: proposed OMNI v0.5.0 claim-review capability. It does not determine Living Jigsaw editorial acceptance.
- #295: AkashicNET v0.17 readiness. This expansion remains outside its minimum bounded scope.

BQ001 remains UNRESOLVED. Accepted canonical edges remain 0. Reddit live access remains HOLD. No automatic truth, scientific-evidence, rights, identity, safety/efficacy or publication promotion is permitted. Interpretive usefulness, personal meaning and diagrammatic proximity do not establish empirical support. Preserve sealed baselines and separately governed framework versions.
