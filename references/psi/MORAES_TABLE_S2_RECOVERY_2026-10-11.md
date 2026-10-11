# Moraes Table S2 recovery continuation — 11 October 2026

Status: **REVIEW_REQUIRED / S2 NOT_RECOVERED**. This is a bounded access investigation and an unsent request, not a completed bibliography or evidence appraisal.

## Scope and preserved boundary

PR #395 was open, unmerged and draft at `3dda93a3dc1c235431bd3c522e101d815510dcdd` when checked. Read alongside the unchanged [6 October note](MORAES_TABLE_S2_RECOVERY_2026-10-06.md) and [historical ledger](moraes-table-s2-provenance-2026-10-06.json). The [new retrieval manifest](moraes-table-s2-access-2026-10-11.json) records this session's results separately; it does not authenticate historical HTTP responses.

Parent publication: DOI [10.1016/j.explore.2021.05.006](https://doi.org/10.1016/j.explore.2021.05.006), PMID [34147343](https://pubmed.ncbi.nlm.nih.gov/34147343/). PubMed distinguishes online publication on 5 June 2021 from the May–June 2022 issue, 18(3):371–378.

**Zero S2 rows extracted or compared.** Observed S2 row count, matched publications, unmatched publications and unresolved included-study identifiers remain null / not assessed. The preliminary 16-source lookup seed remains non-exhaustive and its S2 membership unverified. No source identities or aliases were added to or merged in the existing registries.

## Access routes and fresh findings

| Route | Result on 11 October |
| --- | --- |
| [Publisher article](https://www.sciencedirect.com/science/article/pii/S1550830721000951) | Web retrieval returned 403. Direct HTTPS returned HTTP 200 with a 195-byte “Site Unavailable” HTML body, not article or supplement content. |
| [Crossref parent metadata](https://api.crossref.org/works/10.1016%2Fj.explore.2021.05.006) | Parent DOI verified. Its links identify Elsevier article XML/plain-text APIs; the returned relation object is empty. No S2 attachment authenticated. |
| [Elsevier article XML](https://api.elsevier.com/content/article/PII:S1550830721000951?httpAccept=text/xml) and [object metadata](https://api.elsevier.com/content/object/pii/S1550830721000951?view=META) | Both returned the same unusable 195-byte HTML body, despite HTTP 200. These are environment-specific access observations, not evidence that Elsevier has lost S2. |
| [Author-deposited Figshare item 13234907](https://api.figshare.com/v2/articles/13234907) and [versions](https://api.figshare.com/v2/articles/13234907/versions) | Lists Lucam Justo de Moraes, version 1 only, DOI `10.6084/m9.figshare.13234907.v1`, and one file, `Table S1.docx`, file ID 25491170. No related material listed. |
| [Deposit-linked file](https://ndownloader.figshare.com/files/25491170) | Downloaded and inspected as DOCX XML. Contains the search strategy, not the included-publication table: one table, eight XML rows. 15,998 bytes; MD5 matches Figshare's supplied/computed value. SHA-256: `9ba970a20ea4d9d1b96ae03ee684578e299f8075a50c8b312aa7c34d9f503387`. This authenticates the deposited S1 bytes only. |
| Figshare public API searches | With limit 100: author-name query returned S1 only; article-title query returned S1 plus item 33330264; quoted past-life/S2 query returned no items. Item 33330264 was checked and rejected: different author and migration/kinship subject, not the review supplement. Negative searches are bounded, not proof of absence. |
| [UVA academic-publications page](https://med.virginia.edu/perceptual-studies/publications/academic-publications/) and [linked main PDF](https://med.virginia.edu/perceptual-studies/wp-content/uploads/sites/360/2021/12/Academic-Studies-on-Claimed-Past-life-memories-A-scoping-Review-Jim-2021-1-s2.0-S1550830721000951-main-1.pdf) | Eight-page main article, zero embedded files. Pages 2–3 identify S2 separately; page 6 acknowledges unquantified sample overlap. SHA-256: `317271510edd5f7b1fda353a5ebf4331b98f10aa2aabcf40b1a68c89d09e1aaa`. |
| [UFJF exact-author browse](https://repositorio.ufjf.br/jspui/browse?type=author&value=Moraes%2C+Lucam+Justo+de) | One result, a 2017 dissertation on a different topic. Indexed searches found a 2024 doctoral-research announcement but no authenticated S2 link. This is not an exhaustive institutional holdings search. |
| Author-uploaded ResearchGate result | Indexed page attributes the full-text upload to coauthor Alexander Moreira-Almeida and exposes the main article. No authenticated S2 file was established. |

No inferred CDN filename was promoted to an authoritative link. No access-control bypass, credential use, author contact or publisher ticket submission occurred. Raw articles, S1, third-party datasets and case material are not included in this change.

## Verified contact routes

1. **Lucam J. Moraes: `lucam.justo@estudante.ufjf.br`.** The review's first page and PubMed publish this correspondence address. It also appears on page 2 of the [UVA-hosted 2024 author pre-proof](https://med.virginia.edu/perceptual-studies/wp-content/uploads/sites/360/2024/09/Moraes2024_Children-who-claim-previous-life-memories_A-case-report-and-literature-review.pdf). Identity and published contact provenance are verified; current mailbox delivery has not been tested.
2. **[ScienceDirect Support](https://www.elsevier.support/sciencedirect/contact).** The official legacy [contact route](https://service.elsevier.com/app/contact/supporthub/sciencedirect/) redirects here. Use it to ask support to locate/restore the article-linked attachment, quoting the DOI and PII `S1550830721000951`. No individual publisher email is guessed.

### Author request — draft, not sent

To: lucam.justo@estudante.ufjf.br  
Subject: Request for Table S2 and included-study references — DOI 10.1016/j.explore.2021.05.006

Dear Dr Moraes,

I am compiling a provenance-tracked bibliography for AkashicNET and would appreciate your help with your review, *Academic studies on claimed past-life memories: A scoping review* (online 2021; Explore 18(3), 2022, 371–378).

The article describes Table S2 as summarising the 78 included studies. I could access the main article and your Figshare Table S1, but could not retrieve an authenticated S2.

Could you please provide the final published Table S2, or a stable publisher or institutional link, and confirm its version and whether any corrections apply? If available, an RIS, BibTeX or EndNote export limited to the included publications would also help resolve their identifiers.

Any existing notes identifying publications that reuse cases or samples would be helpful. We are distinguishing publications from datasets and independent replications; we are not requesting personal case records.

Please also indicate the appropriate citation and reuse terms for the supplement and any derived bibliographic metadata.

Thank you for your help,  
AkashicNET — independent research project

### Publisher fallback request — draft, not submitted

Please locate or restore the authoritative Table S2 attachment for DOI 10.1016/j.explore.2021.05.006, PII S1550830721000951, Explore 18(3), 2022, 371–378. The article explicitly refers to an included-study summary in Table S2. The author-deposited Figshare item 13234907 contains S1 only. In our 11 October retrieval environment, the publisher article and attachment-metadata route returned unusable HTML; this does not establish that the attachment is absent for all users. Please provide the correct article-linked S2 download, its filename/version and applicable reuse terms, or route this enquiry to journal production.

## Conditions for continuing the bibliography

- Authenticate the received file through the article's actual attachment link, an identifiable author deposit or a documented author/institution reply. Record receipt date, origin, final URL, version, filename, byte size, SHA-256 and any reuse terms. A matching filename or a count near 78 is insufficient.
- Preserve original rows with stable table/page/row locators and transcribed fields. Reconcile the observed rows and distinct publications with the review's reported 78; record discrepancies without forcing the count or inventing missing entries.
- Resolve each publication's identifiers against publisher, Crossref and PubMed metadata. Retain title variants, online/issue dates, query endpoints and unresolved conflicts. Similar titles alone establish candidates, not identity.
- Expand comparison beyond the 16-source seed to the pinned repository-wide source registry and URL inventories. Keep existing source IDs and proposed alias links separately; require review before canonical merges.
- Track publication identity and sample dependence separately. Multiple papers may describe the same cases, a follow-up, a subset or pooled datasets. Use privacy-safe dataset/group references with supporting publication locators; leave overlap and independence unknown when unassessed. Do not derive an independent-case total by summing samples.
- Keep rights, privacy FAIL_CLOSED, export, publication and promotion gates in place. Do not put identifying case details in the public bibliography.

**78 is the review's reported included-publication count, not 78 independent replications or confirmations of reincarnation.** BQ001 remains **UNRESOLVED**. Existing evidence labels, `supports_models`, accepted edges, source records, pilots, historical ledgers and review requirements are unchanged. This continuation requires review at its own commit; earlier approvals/checks do not cover it. PR stays draft; no merge or deployment.

Provenance: scope/restrictions user-provided; retrieval and preparation AI-executed; requests AI-drafted and unsent. No user scientific conclusion or approval is inferred.
