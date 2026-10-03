# Bounded AWARE publication identity crosswalk

Status: **REVIEW_REQUIRED · LINK_AND_METADATA_ONLY**. Provenance: **ai-executed**.

This batch stages two proposed discovery links to existing publications. It adds **zero new publication records, zero independent studies and zero accepted edges**. It does not change BQ001, the catalogue, the seven-entry pilot or any existing record. All batch evidence, canonical, rights, publication, promotion and privacy gates remain closed; model support is empty. No merge or deployment is authorised by this packet.

## Pinned inputs and deduplication

The source boundary is [PR #392 at c54a946](https://github.com/tws9stmcbf-web/AkashicNET/tree/c54a946f7f4abef3ad2a7f2a70102c801b697d09), `references/psi/psi-encyclopedia-metadata-pilot-v0.1.json`, record `SRC-SPR-PE-0001`. Its empty identifiers and `NOT_EXTRACTED_IN_THIS_PILOT` status are preserved as a historical statement. This separate follow-up supplies the proposed underlying-publication crosswalk.

Before staging, both publications were checked against all 70 catalogue records at [PR #394, c2262f8](https://github.com/tws9stmcbf-web/AkashicNET/blob/c2262f8df8e800478e3f7abfd5407cbc9069173a/website/public/research/source-catalogue/records.json). The JSON packet records the complete catalogue file's SHA-256. Both normalized DOIs already occur exactly once. The catalogue already links the encyclopedia entry to these leads; this packet does not claim those discovery links are new.

| Publication | DOI / PMID | Existing catalogue ID | Existing BQ001 source ID |
| --- | --- | --- | --- |
| Parnia et al., AWARE, 2014 | `10.1016/j.resuscitation.2014.09.004` / `25301715` | `CM-LEAD-001` | `SRC-BQ001-AWARE-2014` |
| Parnia et al., AWARE II, 2023 | `10.1016/j.resuscitation.2023.109903` / `37423492` | `CM-LEAD-002` | `SRC-BQ001-AWARE2-2023` |

Related records checked at the source head include `references/community/bq001-scientific-baseline-batch1.json`, BQ001 `evidence-batch1-v0.1.json`, `source-integrity-batch6-review-v0.1.json`, and `issue-343-source-dedup-ledger-v0.1.json`. The latter already maps `WORK-343-AWARE2-2023` to the governed AWARE II source and explicitly prohibits a duplicate source record. The prior AWARE work/version/correspondence discussion in `docs/audits/manual-corpus-reading-2026-09-22.md` was inspected for identity context only. A bounded identifier scan of main at `befb52736d642ff9f114bcded2dac61401fe25bc` also returned these existing identities and source-integrity receipts.

The 2014 catalogue lead has no PMID: absence is not a conflict. Its DOI matches the existing BQ001 DOI/PMID pair and the fresh Europe PMC bibliographic record. The 2023 catalogue lead carries the matching PMID. Title punctuation differences do not mint another identity. No participant-level independence, replication or scientific adjudication is inferred.

## External verification, 3 October 2026

Only the two named publications and the selected [AWARE NDE Studies](https://psi-encyclopedia.spr.ac.uk/articles/aware-nde-study/) entry were inspected. Locators: Works Cited, Parnia et al. (2014)/(2023), and the AWARE programme sections. No bibliography export, site-wide crawl, article-body retention or extended quotation was performed.

Stable identifiers: [AWARE DOI](https://doi.org/10.1016/j.resuscitation.2014.09.004), [PMID 25301715](https://pubmed.ncbi.nlm.nih.gov/25301715/), [AWARE II DOI](https://doi.org/10.1016/j.resuscitation.2023.109903), [PMID 37423492](https://pubmed.ncbi.nlm.nih.gov/37423492/).

Both DOI/PMID/title/year pairs were freshly verified through Europe PMC's public bibliographic API; exact query URLs are in each JSON record. These are indexing records for the primary publications, not a full-text appraisal. Direct PubMed retrieval supplied usable metadata for AWARE II. For AWARE 2014 it did not, and the DOI publisher route failed; Europe PMC supplied the bibliographic check. No access bypass, missing-full-text inference or current retraction-status claim is made. The 2014 API request used `resultType=core` and the 2023 request used the default result shape; the stored links use the reproducible default bibliographic query. Only selected bibliographic fields were retained, not API response bodies.

## Validation

Run from the repository root:

```sh
python scripts/validate_aware_identity_batch.py
python -m unittest discover -s tests -p test_aware_identity_batch.py
python scripts/validate_bq001_scientific_baseline_batch1.py
```

The first command requires the pinned catalogue commit in the local Git object store. Alternatively pass `--catalogue-file /path/to/exact/records.json`; its bytes must match the recorded SHA-256. Missing inputs fail closed. No live fetch is required by the validator itself.

Validation performed: pinned catalogue hash and normalized DOI uniqueness; exact DOI/PMID/source pairing; existing source and catalogue pointers; community aliases; closed gates; six regression tests including duplicate normalization, swapped PMID, unrelated endpoint, each gate opening, promotion and article-body retention; existing BQ001 scientific-baseline validator; public-data boundary check; unchanged pre-existing files and whitespace check. No broader appraisal, supplement retrieval or participant overlap assessment was attempted.
