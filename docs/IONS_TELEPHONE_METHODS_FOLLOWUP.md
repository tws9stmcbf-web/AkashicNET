# Telephone Study: Methods and Version Follow-up

12 October 2026. AI-executed source investigation. **PARTIAL_NUMERICAL_RECONCILIATION / FINAL_SUBSET_UNRESOLVED. Independent human review pending.**

This follows [the original recount](IONS_TELEPHONE_DATA_CHECK.md). The unchanged, hash-pinned Figshare workbook was identified again; only its headers and legend were additionally inspected. The existing two-parser aggregate receipt is reused. No participant records, identifiers, per-triad results, or workbook bytes are included here.

## What was recovered

The article-in-press PDF [S1] describes retaining the first six pre-selected trials and removing 30 excess trials (p.4). Its randomization methods use 228 completer observations and hit proportion 0.5044 (p.5), matching the earlier deposited-data recount numerically. Table 3 (p.6) differs from the abstract. These are different passages of one study, not independent replications.

| Endpoint / source passage | Pre-selected | Post-selected |
|---|---:|---:|
| Abstract, as originally recorded | 210 responses; 50.0% | 630 responses; 31.9% |
| Table 3, completers [S1] | 101/210; 48.1% | 205/630; 32.5% |
| Figshare v1, Status=Completer [S2] | 115/228; 50.4% | 216/666; 32.4% |
| Table 3 including dropouts [S1], also matching all deposited rows [S2] | 147/289; 50.9% | 243/762; 31.9% |

The author preprint [S3] contains supplementary analysis output on pp.35–44. Page 36 gives binomial command inputs of 210/101 and 630/205; page 37 gives 289/147 and 762/243. These support the Table 3 integers, without supplying the upstream workbook transformation. Summary commands taking counts as input are not a reproducible row-selection pipeline. The current publisher-formatted full text and publisher-hosted supplement were not retrieved; S1 is explicitly article-in-press and S3 an author preprint.

## What the documented rules establish

The official KPU register [S4] lists the original registration (28 July 2021) and revisions of 23 February, 14 March and 20 July 2022. All four PDFs were read.

| Record | Relevant documented rule/change | What it does not establish |
|---|---|---|
| KPU1062, original | Six completed calls per path; incomplete triads excluded from main analysis but included in a separate analysis; 50-attempt limit | Which Figshare rows belong to each final analysis |
| Revision 2 | Changes to registration/consent and compensation; same six-per-path design | A final row-selection script |
| Revision 3 | Adaptive path assignment after six completed and five active groups; attempt limit increased to 100 | Chronological ordering of the deposited observations |
| Revision 4 | Target reduced to 30 triads; unrelated friends admitted; compensation increased | A retrospective mapping from the deposit's Status label to the final completer population |

Eligibility screening and recruitment changes do not themselves specify a filter on the deposited response rows. Nor should the stated removal of 30 earlier observations automatically be applied again: whether the deposit already reflects that operation is not established.

## Reconciliation assessment

**Verified numerical agreement:** the all-status deposited totals match Table 3's including-dropout totals. The pre-selected completer recount also matches the randomization-method sample size and rounded proportion. This substantially narrows the question.

**Still unresolved:** which final records/labels generated the completer endpoint, why the abstract percentages differ from Table 3, and how the excess-trial removal relates to the deposited file.

Our arithmetic comparison, not an exclusion rule: moving from the deposited completers to Table 3 would reduce pre-selected counts by 18 responses and 14 hits, and post-selected counts by 36 responses and 11 hits. Because the combined totals agree, deleting observations alone would not preserve those totals; any proposed reconstruction must explain the analysis-population labels too. No records were moved, discarded, ranked or selected to make these numbers fit.

The workbook header and legend contain no documented timestamp, call-event identifier or trial-sequence field. Worksheet order cannot be assumed to mean chronological order. The three-column audit deliberately cannot implement a per-triad chronological rule. Obtaining an authoritative mapping is preferable to silently expanding it.

The intended design's denominator arithmetic is compatible with 35 triads: 35 × 6 × 1 = 210 pre-selected responses and 35 × 6 × 3 = 630 post-selected responses. This explains the units, not which deposited observations should count. Post-selected response rows are not independent calls or participants.

## Versions and access limits

- Figshare's article/version APIs returned only v1, dated 9 November 2022, with one XLSX file. Metadata size and MD5 plus the prior SHA-256 pin matched. No additional analysis script was listed [S2].
- The OSF API returned preprint version 1 as latest, a single primary-file version, and one root file; pagination was closed. Its file hash matched the downloaded PDF [S3]. A metadata modification date is not evidence of changed PDF contents.
- The registry links the preprint and journal article. Crossref metadata exposed no correction relationship; bounded title/DOI searches did not identify a correction or standalone analysis script. This is not proof that none exists.
- The author's BIAL project summary and the IONS publication page were checked; neither supplies the missing transformation. Direct publisher access returned an unavailable page. No claim is made that the preprint supplement is byte-identical to the publisher-hosted supplement.

## Clarification needed

The verified corresponding author is **Dr Helané Wahbeh, hwahbeh@noetic.org**, identified in the article, PubMed record and KPU registration. Her current IONS profile corroborates the institutional role [S5].

Request: (1) the authoritative final analysis file/version and selection/recoding script or privacy-safe exclusion summary; (2) how the first-six rule and excess-trial removal map to Figshare v1; (3) which abstract/Table 3/randomization endpoints should be treated as definitive; and (4) a link to the final supplement or correction, if applicable. Do not request identities or unredacted participant records. No author contact has been sent at this checkpoint.

## Contact-status verification — 15 October 2026 UTC

The original statement above, “No author contact has been sent at this checkpoint,” is preserved as the historical 12 October source-investigation checkpoint at `b1e3646fdb15b995c32f26963e39aa1e36074435`; it is not a current delivery-status assertion.

**Contact status: DRAFT_PRESENT / SEND_STATUS_UNVERIFIED.** A clarification message addressed to Dr Helané Wahbeh (the verified institutional recipient above) has a Date header of 12 October 2026, 15:47:46 UTC, after the PR update at 15:42:35 UTC. Authenticated Gmail reads currently return it with a DRAFT label. The Date/Received headers alone do not establish dispatch. The inspected thread contains only that draft; bounded sent-mail searches returned no matching sent copy. On 14 October 2026 (America/Los_Angeles; 15 October UTC), the user clarified that they are unsure whether it sent. Sending and delivery are therefore unverified; this is not recorded as confirmed author contact.

The verified draft content prepares these methodological questions; their submission is unverified:
1. The authoritative final analysis script or a privacy-safe selection/recoding summary connecting Figshare v1 to the published completer population.
2. How the first-six-trials rule and removal of excess trials map to the deposited observations.
3. Which published endpoints are definitive where the abstract, Table 3 and randomization-method passage differ.
4. A link to the final supplement or any applicable correction.

**Outstanding:** confirmed send provenance, the final dataset/version-to-analysis-population mapping, operational row-selection and recoding rules, and authoritative endpoint/supplement clarification. No substantive author response was found in the inspected thread or the bounded mailbox searches. This does not establish that no response exists under another address or through another channel.

Communication provenance is summarized in [the contact-status receipt](../references/akashicomni/ions-telephone-contact-status-2026-10-15.json). Private Gmail links, message identifiers, sender details and correspondence text are omitted from the public record. No verified methodological clarification has been incorporated. Preparing or sending an author inquiry does not constitute scientific endorsement or experimental confirmation. PARTIAL_NUMERICAL_RECONCILIATION / FINAL_SUBSET_UNRESOLVED, scientific classifications, independent review PENDING, engineering UNRELEASED / REVIEW_REQUIRED and false promotion flags remain unchanged.

## Provenance and boundaries

Exact source URLs, versions, hashes and inspection locations are in [the source receipt](../references/akashicomni/ions-telephone-methods-followup-2026-10-12.json). PDF tables and supplementary commands were visually checked against their text extraction. All literature copies and workbook bytes remain outside the repository and research-note archive. No inferential test, confidence interval, regression or mechanism was independently reproduced. Scientific claims, independent review and release remain unresolved/pending; all promotion flags stay false.

- S1: [Article-in-press copy](https://www.sheldrake.org/files/pdfs/papers/Whos-calling-evaluating-the-accuracy-of-guessing-who-is-on-the-phone.pdf), DOI [10.1016/j.explore.2023.08.008](https://doi.org/10.1016/j.explore.2023.08.008).
- S2: [Figshare v1](https://doi.org/10.6084/m9.figshare.21521235.v1); [article API](https://api.figshare.com/v2/articles/21521235); [versions API](https://api.figshare.com/v2/articles/21521235/versions); prior [aggregate receipt](../references/akashicomni/ions-telephone-data-check-2026-10-12.json).
- S3: [Author preprint](https://osf.io/preprints/psyarxiv/hxj5n_v1), DOI [10.31234/osf.io/hxj5n](https://doi.org/10.31234/osf.io/hxj5n); [primary PDF](https://osf.io/download/kdc8u/); [file metadata](https://api.osf.io/v2/files/64fa5853989de6390ddd154b/).
- S4: [Official registered-study index](https://koestlerunit.wordpress.com/study-registry/registered-studies/), entry 1062, with [original](https://www.koestler-parapsychology.psy.ed.ac.uk/Documents/KPU_Registry_1062.pdf), [revision 2](https://www.koestler-parapsychology.psy.ed.ac.uk/Documents/KPU_Registry_1062_2.pdf), [revision 3](https://www.koestler-parapsychology.psy.ed.ac.uk/Documents/KPU_Registry_1062_3.pdf), [revision 4](https://www.koestler-parapsychology.psy.ed.ac.uk/Documents/KPU_Registry_1062_4.pdf).
- S5: [PubMed](https://pubmed.ncbi.nlm.nih.gov/37709571/); [current IONS profile](https://noetic.org/profile/helane-wahbeh/); [BIAL author summary](https://assets.ctfassets.net/osaht2ckekgb/3lYdh88xc54P1NjcJEJHzs/b79c86e2178241cff6b25a1b236ac6ca/APOIOS-2020-a-telephone-telepathy-study.pdf).

