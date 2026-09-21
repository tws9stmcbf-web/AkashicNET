# Sandbox integration intake proposal

Status: DRAFT / HOLD. Documentation only; no source records imported.

## Purpose

Bring eligible owner-authored sandbox work into AkashicNET through a private inventory, provenance review, topic mapping and separately reviewed publication. Scope includes Perspectives and HOMESENSE as well as other flairs. Inventory scope is not publication permission.

## Current evidence and limits

An authenticated, user-requested browser inspection displayed 50 entries in one Perspectives flair view. This is a lower-bound discovery observation, not an exhaustive archive count, verified authorship census, or ingestion result. Search results and loaded-page counts must not be presented as complete totals. No raw content, titles, source identifiers, URLs, timestamps or per-record hashes are included in this proposal.

Existing repository archive denominators remain unchanged. No new sandbox entries are represented as part of the canonical index.

## Intake route

1. Obtain an owner-provided account export or other specifically authorised export, or use an approved authenticated API route whose scope includes the source. Do not activate a crawler or bulk HTML scrape.
2. Keep source files, private identifiers, raw text, media and inventory outside this repository in the controlled private data layer. Exclude other users' contributions without appropriate permission; separately handle deleted or withdrawn material.
3. Deduplicate by source identity within that boundary. Record exact flair text, missing flair, available dates, authorship, content type and completeness privately. Count unique posts by flair, including an explicit no-flair category. Record the coverage boundary and source snapshot; do not equate search matches with archive totals.
4. Review sensitivity, third-party rights and source visibility. Personal, medical, diary-like, administrative and moderation material remain private by default under SECURITY.md.
5. Map topics and proposed destinations without asserting evidential support or canonical identity. Distinguish established evidence, interpretation, lived experience/testimony, hypothesis and speculation. Historical AI-generated claims require source reinspection, not automatic adoption.
6. Prepare sanitised candidate adaptations and a private source-to-adaptation record. Remove private provider identifiers from public outputs. Reuse existing public articles where appropriate rather than silently overwriting or duplicating them.
7. Submit eligible adaptations for explicit public-manifest review. Only PUBLIC_VERIFIED records with completed sensitivity and rights reviews and an explicit ELIGIBLE decision may enter a public build.

## Destination responsibilities

| Destination | Permitted stage |
|---|---|
| Controlled private data layer | Authorised source export, raw inventory, provenance and review decisions |
| GitHub | Code, schemas, synthetic fixtures, boundary-checked aggregates and independently verified public-source records |
| akashicnet.org | Separately reviewed public adaptations, evidence labels and public-safe sources |
| Magazine and social channels | Approved publication derivatives; never automatic mirrors of the sandbox |

## Completion checklist

- [ ] Authorised full-source export or approved API scope available
- [ ] Private inventory complete, with coverage and deduplication documented
- [ ] Unique-post counts by exact flair, including missing flair, reconciled
- [ ] Owner authorship and third-party rights reviewed
- [ ] Sensitivity and visibility reviewed per candidate
- [ ] Existing public duplicates and destination mapping reviewed
- [ ] Claims reinspected against accessible sources; unresolved claims retained
- [ ] Public candidates pass existing manifest and privacy gates
- [ ] Separate publication changes reviewed and authorised

## Invariants

Live automated Reddit intake remains HOLD. Accepted canonical edges remain 0; supports_models remains empty. BQ001/BQ002/BQ003 remain UNRESOLVED. Truth, evidence, rights, canonical-identity, website, public-synthesis and other promotion gates remain closed. This document grants no runtime capability, changes no release status, enables no CI job, publishes no website content and authorises no merge.

The proposed workflow follows [Data security boundary](DATA_SECURITY_BOUNDARY.md) and [Security policy](../SECURITY.md). Checkbox completion must be backed by evidence; none is asserted here.
