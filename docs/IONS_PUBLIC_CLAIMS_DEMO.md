# AkashicOMNI × Public IONS Research: TSC2026 Review Demo

**Independent AkashicNET sample. No IONS endorsement or collaboration agreement. UNRELEASED / REVIEW_REQUIRED.**

This four-claim sample demonstrates traceable extraction and visible evidence gaps using the unchanged engineering contract from [draft PR #367](https://github.com/tws9stmcbf-web/AkashicNET/pull/367), pinned at `7df1de8272b1a03623f8b7d57c258896273f5764`. It does not import the Telepathy Evidence Map, supply a private IONS database, validate a telepathy mechanism or release AkashicOMNI v0.5.0.

## New: a real reproducibility gap

The [telephone data check](IONS_TELEPHONE_DATA_CHECK.md) found that the public workbook's Completer label yields 228/666 pre/post-selected trials rather than the abstract's 210/630. Two parsers agree. The publication-specific subset remains unresolved; no p-values or mechanism are reproduced. This provides a concrete review question for the demo.

## Show this in three minutes

1. Open the [claim packet](../data/akashicomni/ions-public-claims-demo-v0.5.0.json). Choose `OMNI-IONS-M2M-001`: follow its source URL and named passage, then inspect the outcome definition and missing evidence. The missing numerical test details stay missing.
2. Compare `OMNI-IONS-PHONE-001` and `002`. Both are retained, with their distinct conditions. One paper is one source lineage; multiple URLs and multiple endpoints are not independent replications.
3. Open `OMNI-IONS-EHE-001`. Its `TESTIMONY` label describes a questionnaire endpoint. Self-report endorsement is not task performance or demonstrated telepathy.
4. Show the pending assessments, null verification fields and eight false promotion flags. Run the validator/tests below. Passing means the review packet obeys the software contract; it does not authenticate the science.

## Four bounded claims

| Claim | Source type | Reported outcome | Boundary |
|---|---|---|---|
| M2M-001 | TSC2026 abstract | Above-chance receiver-count result in 100 screened dyads | Exact statistic and participant data not obtained |
| PHONE-001 | Published-paper abstract | Pre-selected: 50.0% / 210 trials; p<.001 against 33.3% chance | Repeated trials; full methods and reanalysis pending |
| PHONE-002 | Same paper | Post-selected: 31.9% / 630 trials; p=.61 against 33.3% chance | Nonsignificance does not establish absence; no condition-difference test inferred |
| EHE-001 | Published survey abstract | 93.2% of 175 scientist/engineer respondents endorsed ≥1 exceptional experience | Any of 25 categories, not telepathy-specific prevalence |

These are author-reported outcomes. AkashicNET has not independently reproduced them. The two phone endpoints belong to one study. No pooled effect, credibility score, mechanistic inference or successful-dyad count is generated.

## Source and data access

Full bibliographic metadata, source locations, access date, dependencies, limitations and revision conditions are in the [hash-bound extraction record](../references/akashicomni/IONS-Public-Claims-Extraction-2026-10-12.md).

| Resource | Inspected scope on 12 October 2026 | Status in this sample |
|---|---|---|
| [TSC workshop](https://tsc2026.org/workshops.html) | Brinsmead and Taddeo abstract entries | Claim-description source; not full methods |
| [Telephone paper](https://pubmed.ncbi.nlm.nih.gov/37709571/) | Author abstract and bibliography, checked against IONS | Abstract only; publisher full text returned 403 |
| [Telephone data deposit](https://doi.org/10.6084/m9.figshare.21521235) | Versioned workbook legend and three analytical columns | Local aggregate recount found a subset mismatch; no participant rows committed; license displayed as CC BY 4.0 |
| [Exceptional-experiences paper](https://pubmed.ncbi.nlm.nih.gov/30415782/) | Author abstract and bibliography, checked against IONS | Self-report source; no full-text or item-level analysis |
| [IONS telepathy page](https://noetic.org/telepathy/) | Map status and links | Map still labelled “Coming Soon”; no export identified in this bounded check |
| [Mind2Mind recruitment](https://noetic.org/mind2mind/) | Eligibility, phases, privacy statement | Recruitment target is distinct from observed sample; no trial data obtained |

The previously imported Noetic Signature Inventory is separate questionnaire research and is excluded. No row-level data, slides, full papers, private messages or personal identifiers are copied into this PR. Public accessibility does not automatically satisfy rights or privacy review. All `rights_status` values remain `NOT_ASSESSED`.

## Run locally

From the repository root, using Python 3.11+:

```sh
python -m pip install jsonschema==4.26.0
python scripts/validate_akashicomni_claim_review_v050.py data/akashicomni/ions-public-claims-demo-v0.5.0.json
python -m unittest discover -s tests -p 'test_ions_public_claims_demo.py' -v
python -m unittest discover -s tests -p 'test_akashicomni_*.py' -v
```

The telephone audit and its synthetic tests are described in the linked check. The new path-scoped workflow tests the PR merge result using default checkout behavior and read-only permissions. It validates the packet and tests gate mutations, invented reviews, fabricated attestations, broken lineage and out-of-contract participant data. There is no deploy step. Tests cannot detect every misleading sentence or authenticate source content; semantic review remains essential.

## Schema compatibility and review gates

The existing schema, validators, historical meditation packet, coverage fixture and trusted registry are unchanged. `framework_baseline: 0.4.0` is retained because it is the draft contract's historical constant; it is not a claim that the current public manual remains v0.4.0. `source_kind: PRIMARY` denotes the original author-report source, not access to primary observations. Sources remain `ABSTRACT_ONLY`; only the original AI editorial lineage artifact is `FULL_TEXT_INSPECTED`, with no human attestation.

All claims remain `UNRESOLVED`; assessments are empty and comparisons `PENDING`. Both source and reviewer attestation arrays remain unchanged. `accepted_edges` and `supports_models` are empty; truth, evidence, rights, public_synthesis, website, bq_resolution, privacy and cultural_authority flags remain false. Counter-evidence search is `NOT_COMPLETED` throughout. M01–M12 remain pending. This is a bounded claim-record sample, not the full v0.5.0 methodology or a demonstrated IONS adapter.

## Independent review request

- Check exact wording, source passage, units and denominator: dyads, receivers, trials and survey respondents must remain distinct.
- Inspect original methods and protocol history. Check randomization, blinding, ordinary cue exclusion, clustering, selection/attrition, multiplicity and registration timing.
- For Mind2Mind, obtain a citable report, exact binomial specification and privacy-safe data/access terms before reproducing the result. Do not infer an alpha level or borrow the phone study's chance rate.
- For the telephone study, reconcile the deposited Completer label with the published subset before inferential reanalysis; inspect the full text to reconcile the genetic-relatedness wording noted in the extraction record.
- Review contrary evidence and independent replications. Proposed conventional alternatives are possibilities for testing, not allegations of observed failures.
- Use the existing trusted-registry process for actual human source inspections and independent assessments. AI authoring, passing CI and owner engineering approval do not substitute for independent review.

## Potential interoperability exercise

Propose exchanging **one consented, licensed, public claim record** with IONS. Compare source/work identity, exact passage, claim/outcome units, study dependence, unavailable fields and human-review status. Map their export only once its actual schema and reuse terms are available; do not invent IONS field names or an API. Round-trip without losing provenance or upgrading status, then ask both teams to inspect the result. This is an AI-suggested next step, not an agreed collaboration or a completed adapter.

Staging is on a separate draft branch stacked on PR #367. Do not merge this demo into the parent as a substitute for the parent's outstanding review and release gates. No website publication or release is included.
