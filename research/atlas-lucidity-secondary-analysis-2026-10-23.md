# Dementia lucidity: focused secondary-analysis appraisal

Reviewed 23 October 2026. AI-assisted editorial appraisal, pending independent review. This resolves the unassessed lead in draft PR #412 without promoting evidence.

## Publication and cohort accounting

| Item | Original prospective report | Related secondary analysis |
| --- | --- | --- |
| Stable source ID | `SRC-ATLAS-LUCIDITY-GNAF178-2025` | `SRC-ATLAS-LUCIDITY-LCA-2026` |
| DOI | [10.1093/geront/gnaf178](https://doi.org/10.1093/geront/gnaf178) | [10.1177/13872877261445464](https://doi.org/10.1177/13872877261445464) |
| PMID / PMCID | [40748700](https://pubmed.ncbi.nlm.nih.gov/40748700/) / PMC12871080 | [42081117](https://pubmed.ncbi.nlm.nih.gov/42081117/) / PMC13225770 |
| First online / issue | 1 August 2025 / 8 September 2025 | 4 May 2026 / June 2026 |
| Question | Detect and characterise prospectively observed episodes | Can statistical classes help detect communication changes, and do definitions need to vary by person? |
| People | 20 enrolled; 19 recorded; validated episodes in three | The same three previously validated cases; zero newly recruited people |
| Measurement units | 539 observations; nine validated episodes | 1,283 coded audiovisual segments from the selected cases |
| Approach | Multi-informant validation; GEE comparisons with sampled baseline; Poisson observation-planning model | Latent class analysis; person-specific versus shared response probabilities; internal LOOCV |
| Contribution | Direct documentation of behavioural changes | Exploratory measurement development using existing observations |

Primary provenance: original [PMC report](https://pmc.ncbi.nlm.nih.gov/articles/PMC12871080/), Methods and Results; follow-up [PMC report](https://pmc.ncbi.nlm.nih.gov/articles/PMC13225770/), Participants, Segmentation, Variables, Validation and Tables 2–5. Bibliographic identifiers and dates were cross-checked against PubMed and the [follow-up publisher page](https://journals.sagepub.com/doi/10.1177/13872877261445464).

The two papers describe **one cohort**, not two independent studies of different people. The secondary paper explicitly selects the three people with previously validated episodes. Observations, episodes and coded segments cannot be added together. Nine episodes can span multiple segments; 1,283 is neither the number of people nor the number of newly observed lucid episodes. The structured receipt records 20 unique enrolled people, 19 recorded people, one independent cohort and zero new people contributed by the secondary paper. Do not calculate population prevalence from this selected subset.

## Focused appraisal

The original report compares validated episodes with a random 20% selection of codable baseline material. The follow-up uses episode-containing segments and a random 20% of communicative segments. These sampling rules enrich the material for communication and known episodes; the analysed material is not an unselected continuous surveillance sample.

The follow-up reduces 68 variables to 14 binary indicators through pooled filtering and correlation screening. Its three-class unconstrained solution minimises BIC among the compared grouped solutions; constraining response probabilities across people worsens BIC. This supports exploring personal baselines. It does not establish a universal three-state taxonomy: one separately fitted case favoured four classes, and model criteria need not agree.

The candidate high-engagement class captures most previously labelled lucid segments. Main-analysis sensitivity ranges from 53% to 100% and specificity from 56% to 97% across the three cases. These are published comparisons against existing segment labels, not externally validated clinical performance or estimates of consciousness. Only suspected episodes received informant review, and the comparison negative category includes unreviewed material. Consequently, apparent false positives could contain missed episodes or ordinary engagement, and specificity lacks a fully verified reference standard.

The paper reports leave-one-out cross-validation for individual models. This is an internal robustness exercise; it does not recruit an independent cohort. The exact hold-out unit, temporal isolation, preprocessing within folds, numerical supplement results and uncertainty estimates remain unverified here. Repeated measurements within people and episodes require attention before interpreting model precision or transportability. No absence of cross-validation is claimed.

Binary encoding loses information about intensity and duration. The reported continuous, duration-normalised follow-up comparisons help examine class differences but do not settle external detection accuracy. High engagement and informant-validated lucidity are overlapping operational categories, rather than interchangeable labels.

## Interpretation and review boundary

**Editorial assessment:** this is a useful candidate method for directing human attention to changes in communication relative to a person's baseline. The shared cases and label-selection process limit its evidential independence. Behavioural clustering alone cannot decide whether the underlying change reflects attention, cognition, conscious experience or another mechanism. Neither paper tests survival after death. The record adds no support edge to a consciousness model and leaves BQ001 UNRESOLVED.

The initial appraisal used publisher bibliographic material, abstract and data statement, plus search-indexed primary methods/results passages. A subsequent audit below obtained both complete main author manuscripts through NCBI EFetch. The supplement, code, publisher-version comparison and independent scientific review remain incomplete. No participant-level records, audiovisual material or clinical narratives were copied into the repository. Data access requires IRB-approved procedures and sharing agreements; both main manuscripts explicitly state that the research was not preregistered.

Targeted DOI/title searches did not verify a correction or retraction. This is not a complete Crossmark or linked-notice audit. The previous correction-check scope and 22 October lead entry remain unchanged as history; the 23 October receipt resolves the lead by reference rather than rewriting it.

## Reproducible amendment

[Metadata and history](../references/research-atlas/review-candidates-2026-10-22-grief-lucidity.json), version 0.1.3, records reciprocal publication links, a shared cohort identifier and an appended main-manuscript audit. Existing grief records and the AWARE II duplicate receipt remain intact. The initial amendment baseline is commit `fe130ec0df56f72decaf8c7aa026cb9bee7c0af3`; the subsequent audit preserves the history at `5879b6daedf1096beabf2a168f474f5fb504bfe6`.

Run from the repository root:

```sh
python scripts/validate_atlas_lucidity_amendment.py
python scripts/validate_metadata.py
python scripts/check_public_data_boundary.py
python scripts/validate_bq001_public_status_boundary.py
```

The focused validator checks identifiers, normalised DOI ownership in repository reference/research JSON, reciprocal cohort links, denominators, retained history and governance, and limits changed paths relative to the amendment baseline. It validates the metadata amendment; it does not reproduce LCA or certify scientific validity.

Independent review must inspect the complete papers and supplement, verify validation labels and LOOCV isolation, evaluate uncertainty and temporal dependence, and audit code if obtainable. External evaluation needs new people and appropriately verified reference labels. Publication, PRISM import, canonical evidence promotion and accepted model edges remain disabled. Draft PR #412 stays draft.

## Subsequent main-manuscript and notice audit

NCBI EFetch returned the complete main author manuscripts, identified as `PMC12871080.1` and `PMC13225770.1`. Their identifiers match the article-level PubMed and Crossref records. Five response URL, SHA-256 and byte-count receipts are recorded under `methods_audit.source_snapshots`; source text and sensitive research data are not redistributed.

The original GEE analyses account for day-level clusters and use jackknife standard errors. However, the authors explicitly retain unadjusted nominal p values across many exploratory comparisons. The new LCA analysis is a different analytical question, so its class separation cannot be counted as a second independent confirmation of those tests.

The follow-up main text confirms that selected representative segments sometimes led to entire days being labelled lucid. The resulting reference labels include quieter periods as well as highly communicative periods. This makes an apparent missed segment partly a question of temporal episode boundaries, rather than necessarily a failed observation of communicative change. The authors also caution that a larger cohort could favour shared-class subgroups. Better fit for individual models here does not establish a universal modelling rule.

The original Results reports **539 audiovisual observations**, while its power/sample-size subsection uses **556 observation days**. Their mapping is not established here. The metadata records both with different labels and an open reconciliation question; it neither substitutes one for the other nor asserts an author error. The original cohort and the secondary-analysis segment denominators remain unchanged.

| Check | Verified scope | Remaining boundary |
| --- | --- | --- |
| Main manuscripts | Both complete main XML texts and main tables read | Publisher-version equivalence not compared |
| Identification | PMID, PMCID and DOI agree across article-level records | These checks do not validate scientific conclusions |
| Notice links | No CommentsCorrections entries in inspected PubMed articles; empty Crossref relation objects and no update-to/updated-by entries | Reverse notice search and complete Crossmark audit remain open; no proof of absence |
| LOOCV | Main text reports robustness results and automated class selection | Exact fold unit, temporal isolation and nested preprocessing still require supplement/code |
| Supplement access | Publisher request returned 403; PMC asset returned a browser challenge | Supplement not read; no complete supplement-review claim |
| Independent review | Still required | AI-assisted main-text review does not fulfil it |

The source-cache option checks saved public responses against the recorded fingerprints and extracts article-level identifiers and notice fields independently of bibliography reference lists:

```sh
python scripts/validate_atlas_lucidity_amendment.py --source-cache /path/to/source-cache
```

Use the five recorded URLs to retrieve `pubmed-records.xml`, `pmc-original.xml`, `pmc-secondary.xml`, `crossref-original.json` and `crossref-secondary.json` respectively. The validator reports a mismatch if a response changes; that calls for a new dated audit receipt, not silent replacement of the historical fingerprint. This does not reproduce the statistical analyses.
