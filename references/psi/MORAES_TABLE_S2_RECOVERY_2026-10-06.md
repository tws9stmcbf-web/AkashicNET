# Moraes Table S2 recovery: blocked, review only

On 6 October 2026, PR #395 was open and draft at `500dac3dd55a40c0e213bb98f8d7ca58551cb3ad`. The companion [provenance ledger](moraes-table-s2-provenance-2026-10-06.json) records a bounded recovery attempt, not a completed extraction.

**Table S2 was not recovered. Zero included-study rows were extracted or compared.** The article reports 78 included publications and describes S2 as supplying authors, year, country/territory, design, sample and method. Those fields and the actual row count have not been checked against the supplement itself. No placeholder study identities were invented.

## Recovery evidence

- [Publisher article](https://www.sciencedirect.com/science/article/pii/S1550830721000951): web fetch returned 403; direct HTTPS returned a 195-byte “Site Unavailable” HTML body despite HTTP 200. The Crossref-linked article API and documented attachment-metadata API likewise returned that unusable HTML.
- Two conventional CDN DOCX filename candidates returned 403. These were inferred candidates, **not authenticated S2 links**; their failure does not establish that the supplement is missing.
- [Author-deposited Figshare record](https://api.figshare.com/v2/articles/13234907) lists only `Table S1.docx`. Title and author-name searches returned that S1 record, while the bounded S2 and article-DOI searches returned no S2. S1 is not substituted for S2.
- [UVA's publications list](https://med.virginia.edu/perceptual-studies/publications/academic-publications/) links the [eight-page main article](https://med.virginia.edu/perceptual-studies/wp-content/uploads/sites/360/2021/12/Academic-Studies-on-Claimed-Past-life-memories-A-scoping-Review-Jim-2021-1-s2.0-S1550830721000951-main-1.pdf), which identifies S2 separately. The main article's references and Crossref reference metadata are not treated as the included-study table.

These observations describe access in this session, not universal unavailability. No credentials, access-control bypass or author contact was used.

## Comparison preparation

The ledger retains a **non-exhaustive lookup seed of 16 existing source IDs** from five pinned repository files. These are existing records, not S2 entries or new sources. All have `table_s2_membership: UNVERIFIED`. Missing stored DOI/PMID values are explicitly unresolved; an absent stored value is not evidence that no identifier exists.

Three source files are identical at the requested PR head and main snapshot `60683acdc67ea0f37028603972c41975b2ff58e1`. The Psi and bibliographic pilots exist on the PR branch and are absent from that main snapshot. File hashes and JSON pointers preserve the comparison basis. PR #321's separate boundary remains recorded; no new claim is made to have inventoried all identifiers or all branches.

Two pre-existing publication aliases are recorded without applying canonical merges:

| Existing source IDs | Identity basis |
| --- | --- |
| `MORAES-ET-AL-2022-PLM-SCOPING`; `SRC-BQ001-SCOPING-2021` | Same DOI `10.1016/j.explore.2021.05.006` and PMID `34147343`; 2021 online and 2022 issue dates remain distinct |
| `PEHLIVANOVA-COZZOLINO-TUCKER-2024-FOLLOWUP`; `SRC-BQ001-PEHLIVANOVA-2024-FOLLOWUP` | Same DOI `10.3389/fpsyg.2024.1473340`; PMID `39649781` is supplied by the existing bibliographic pilot only |

Included-study match, non-match and unresolved-identifier counts remain **null / not assessed**, rather than misleading zeros. The lookup seed must be expanded to a repository-wide DOI/PMID and source-record comparison once actual S2 rows are available.

## Required next input

An authoritative Table S2 file or working publisher/author/institution download link is required. Verify its attribution and hash, transcribe its rows with locators, reconcile its row count with the reported 78, then resolve publication identifiers and compare them against the pinned repository records and URL inventories. Similar titles are candidate matches until resolved; contradictory identifiers remain unresolved. Preserve aggregate descriptors while omitting individual case identities and sensitive case material.

The review acknowledges overlapping samples whose extent it could not measure. Publication identity, shared datasets/cases and independent replication therefore remain separate questions. No new independent-study or replication count follows from this ledger.

BQ001, evidence records and labels, model support, accepted edges, rights, privacy, export and publication gates remain unchanged. The four-publication pilot is unchanged. No merge or deployment. Provenance: scope and restrictions from the user; retrieval and lookup preparation AI-executed; no inferred user approval or scientific conclusion.
