## Current correction status: 22 October 2026

**AUTHOR_CLARIFIED / DESCRIPTIVE_RECONCILIATION_COMPLETE / INFERENTIAL_REVIEW_PENDING.** See [the dated correction](../references/akashicomni/IONS-Telephone-Correction-2026-10-22.md). Author-confirmed Table 3 gives pre-selected 101/210 (48.1%) and post-selected 205/630 (32.5%). Three completion-status labels caused the v1 completer mismatch; all-status totals are unchanged. The first-six restriction was already applied correctly. Corrected completer randomization, the post-selected abstract explanation, formal corrigendum, public v2/scripts and independent scientific review remain pending. No mechanism inference or evidence promotion. PR #399 remains draft; no merge or release.

The following text is preserved verbatim as historical checkpoints and superseded only on the matters clarified above.

---

# Telephone Study: Public-Data Reconciliation Check

**12 October 2026. AI-executed descriptive check. MISMATCH_REQUIRES_RECONCILIATION. Independent human review pending.**

The public workbook's own `Completer` label does **not** reproduce the two completer endpoints in the published abstract using the documented mapping alone. This identifies an unresolved data-to-publication mapping, not proof that the published result is wrong.

| Condition | Abstract trials | Abstract accuracy | Deposited Completer trials | Deposited hits | Recount accuracy |
|---|---:|---:|---:|---:|---:|
| Pre-selected | 210 | 50.0% | 228 | 115 | 50.4% |
| Post-selected | 630 | 31.9% | 666 | 216 | 32.4% |

The source contains 1,051 trial rows. Its remaining Dropout rows total 61 pre-selected trials with 32 hits and 96 post-selected trials with 27 hits. These are trial counts, not independent participant counts. No p-values, confidence intervals, regression models or between-condition tests are reproduced.

**Later methods follow-up:** [Full text, registration history and supplementary analysis output recovered](IONS_TELEPHONE_METHODS_FOLLOWUP.md). There is partial numerical agreement with other passages of the paper, but the final subset remains unresolved. The original recount below remains unchanged.

## Sources and exact input

- Wahbeh, Cannard, Radin and Delorme, *Who's calling? Evaluating the accuracy of guessing who is on the phone*, Explore 20(2), 239–247 (2024), online 25 August 2023. [DOI](https://doi.org/10.1016/j.explore.2023.08.008), [PubMed author abstract](https://pubmed.ncbi.nlm.nih.gov/37709571/), [IONS abstract](https://noetic.org/publication/telephone/).
- Wahbeh, Delorme, Cannard and Radin, *Dataset to accompany telephone telepathy manuscript*, [Figshare version 1](https://doi.org/10.6084/m9.figshare.21521235.v1), posted 9 November 2022. License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Analysis is a new derivative aggregate, not a republished workbook.
- [Figshare metadata API](https://api.figshare.com/v2/articles/21521235) and [version history](https://api.figshare.com/v2/articles/21521235/versions), checked 12 October 2026. Only v1 was returned. File ID `38149656`, `Whos calling anonymized data 11_8_22.xlsx`, 87,755 bytes, MD5 `07158e08d430cd17345428cf76728382`, SHA-256 `83231d102887e6faae295afca161419cefce606c8463ed07e3246c6feeb03097`.

The download matched both the API's file size and MD5. The audit CLI pins SHA-256 and size before parsing. The workbook remains outside the repository; reviewers can retrieve the source from Figshare under its stated terms.

## Method

Resolve the worksheet named `Data` through the workbook's relationship metadata. Read only `Status`, `Trialtype`, and `Hit` for aggregation. The `Legend` defines trial type 0 as post-selected and 1 as pre-selected, and hit 0 as incorrect and 1 as correct. Filter `Status` exactly equal to `Completer`, group by trial type, sum hits and count rows. Calculate percentages from integer counts, rounded to one decimal. No additional exclusions or outcome-dependent selection are applied.

The named-sheet XML reader and a separate read-only `openpyxl` recount returned identical counts for all four status/condition groups. This cross-check reduces parser-error concerns but is not an independent researcher replication. It does not establish that the source Status label implements the publication's final analysis population.

## What remains unresolved

The deposit predates the final paper. Differences could reflect a later analysis subset, eligibility/exclusion rules, cleaning, an earlier data snapshot, or an issue in the data or publication. This bounded check cannot choose among these explanations.

The IONS abstract discloses protocol amendments. Its [official blog](https://noetic.org/blog/telephone-telepathys-accuracy/) describes the design but does not supply the missing exclusion/analysis mapping. Full publisher methods remained inaccessible in the earlier check; a BIAL summary link returned a 404 during this follow-up. No alternative exclusion rule has been inferred or fitted to reproduce the headline values.

**Concrete review question:** Which version and prespecified or documented filter produce the published 210 pre-selected and 630 post-selected completer trials from Figshare v1? A citable analysis script or exclusion log would let us test the mapping. No author contact has been sent.

## Run and interpret

```sh
python scripts/audit_ions_telephone_dataset.py /path/to/telephone-v1.xlsx
python -m unittest discover -s tests -p 'test_ions_telephone_data_audit.py' -v
```

The CLI reads a user-supplied local workbook; it never downloads or executes workbook code. Exit 2 is expected for this deposit and means the descriptive endpoints differ. Exit 1 indicates an invalid or changed input. Exit 0 would mean descriptive endpoints matched, still without verifying p-values, methods or mechanism.

The [saved aggregate receipt](../references/akashicomni/ions-telephone-data-check-2026-10-12.json) records the source hash, legend mapping, filter and computed counts. CI runs synthetic parser/aggregation/gate tests and checks the saved receipt's arithmetic. It does not download the source data or rerun the row-level recount. Tests explicitly guard against treating a mismatch or empty input as success, accepting another source version, accepting cached formulas as observations, and exporting extra participant fields.

## Privacy, rights and evidence boundaries

The deposit is described as anonymized and contains participant/triad identifiers, demographic fields and relational variables. No re-identification is attempted. Only the three analytical columns are used for the scripted aggregate. IDs, demographic values, relational measures, row-level records, workbook metadata and the workbook itself are excluded from the PR. No per-person or per-triad breakdown is published.

Attribution and the displayed CC BY license are recorded. This scoped public-data check does not clear broader rights/privacy gates or authorize redistributing participant-level data. Claim records retain the author's reported outcomes with an explicit reconciliation gap. All existing evidence, privacy, publication, independent-review and release gates remain closed. Mind2Mind data, the Evidence Map and the separate NSI import are not used.
