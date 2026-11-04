# BQ001 Pilot: Stevenson Source-Recovery Handoff

30 October 2026 · **PENDING_HUMAN_REVIEW · Public HOLD · BQ001 UNRESOLVED**

This dated addendum updates the existing v0.18 human-review packet and the
source-access account in [the integration record](../../../docs/research-integration-v018.md).
It is an AI-authored review aid, not a new source, native assessment, executable
contract, completed OMNI review or permission decision. It preserves the r190
input lock, prior observations and assessment history.

## Exact Inputs and Publication Identity

- Pilot baseline: draft [PR #413](https://github.com/tws9stmcbf-web/AkashicNET/pull/413),
  historical commit `b45b990032c05e4223b1a613acdd37e1792f90d6`.
  Prewrite head `d3b08470c39ac8120d35316544a73fbb1b13f2d0` adds a separate
  OMNI-provenance documentation follow-up, inspected and preserved by this change.
- Recovery/appraisal: draft [PR #416](https://github.com/tws9stmcbf-web/AkashicNET/pull/416),
  commit `7625004ccbf4efc4e0b7ef0f457b5007fb3ac8a8`.
- [Pinned provenance manifest](https://github.com/tws9stmcbf-web/AkashicNET/blob/7625004ccbf4efc4e0b7ef0f457b5007fb3ac8a8/references/big-questions/BQ001/stevenson-1988-seven-cases-appraisal-2026-10-28.json),
  Git blob `66371003f1dd72b80d7622631bb85e077a408670`.
- [Pinned full appraisal](https://github.com/tws9stmcbf-web/AkashicNET/blob/7625004ccbf4efc4e0b7ef0f457b5007fb3ac8a8/references/big-questions/BQ001/STEVENSON_1988_SEVEN_CASES_APPRAISAL_2026-10-28.md),
  Git blob `7c66a8375eed404b803793b30f91dfb8c4c9dcd2`.

The pilot's title, three authors, year and original UVA locator match PR #416:
Ian Stevenson, Satwant Pasricha and Godwin Samararatne (1988), *Deception and
Self-Deception in Cases of the Reincarnation Type: Seven Illustrative Cases in
Asia*, *Journal of the American Society for Psychical Research* 82(1), pp.1–31.
The original URL is also exactly the manifest's `access.original_url` and the
embedded target of its archive URL. This reconciles two representations of the
selected publication; it adds no independent study or canonical work-family
decision. The manifest's descriptive work key is not a replacement source ID.

**Stable primary source ID (unchanged):**
`https://med.virginia.edu/perceptual-studies/wp-content/uploads/sites/360/2016/12/STE23.pdf`.

**Community ID (unchanged):** `PRISM-REDDIT-1tlcanb`; retain native assessment 43
and any existing ordered history. The supplied-post review is contextual.
Neither this recovery nor the post establishes that the post cites the selected
paper or concerns these seven cases. Do not add a citation, same-case or
independence relationship.

## Dated Access Reconciliation

The 22 October direct 403/404 observations remain valid historical route outcomes,
not evidence that the publication was deleted. The packet's 27 October failed
search and partial-reading statements also remain dated history.

PR #416 records retrieval on **28 October 2026** of
[the archived representation](https://web.archive.org/web/20250708055558if_/https://med.virginia.edu/perceptual-studies/wp-content/uploads/sites/360/2016/12/STE23.pdf):
HTTP 200, `application/pdf`, **3,174,141 bytes**, **31 pages**, SHA-256
`aa2666f8ac7efed684e3f217f5451398085c182d78867348f34ace7632de514c`.

The URL encodes **8 July 2025, 05:55:58 UTC**; the manifest explicitly says that
capture timestamp was not independently verified. Do not relabel it a verified
capture time or a retrieval date. The original publisher master was not
byte-compared and live UVA availability is not newly verified here.

The prior appraisal reports OCR reading of all 31 pages and visual inspection of
pages **1, 6, 7, 9, 10, 14, 16, 17, 18, 20, 21, 22, 25, 28, 29, 30 and 31**.
Printed page n corresponds to PDF page n. This is full published-scan reading
reported in a dated AI-executed appraisal, not authenticated human reading or
inspection of original field records. This reconciliation reads the pinned
manifest and appraisal; it does not claim a new scan download, rehash or OCR pass.

**Access-gap disposition:** documented access to the complete published scan and
a bounded AI methodological draft are now available. The old blanket
“full primary text unavailable” limitation is superseded for that representation.
Rights, original-case documentation and human/independent appraisal remain open.

## Existing Contract Fields: Precise Revision Instructions

Use `schemas/research-integration-v0.18.schema.json` and the existing
`OMNI-0.5.0-manual-reference` review method. No schema extension or fresh source ID
is needed. The r190 import itself remains a historical metadata import.

| Existing field / location | Revision supported by this recovery | Boundary retained |
| --- | --- | --- |
| Primary `source_id`, `kind`, `work_family`, `relationships` | Retain original UVA ID and `primary_research`; attach this handoff to that source in the worksheet. | Keep `work_family=null` and existing relationships; no identity promotion. |
| Primary `observations` | Preserve every old value. A later authorised observation must append with a new unique `observation_id`, `supersedes` pointing to the actual latest ID and an explicit `correction_reason`. | No invented prior IDs, overwritten access failure or replaced native assessment. |
| New observation `url`, `retrieved_at`, `observed_at` | Proposed archive URL above; `retrieved_at=2026-10-28` attributed to PR #416. Use the actual observation/recording date, not the encoded 2025 capture date, for `observed_at`. | Earlier retrieval dates remain null where unknown. No present-day live-URL verification inferred. |
| `reading_depth`, `access_scope`, `provenance` | A later observation may record `full_text_read` only with explicit attribution to PR #416's AI OCR reading, selected visual pages, scan scope and exact commit/blob provenance. | Existing r190 primary observation remains `metadata_only`, with its recorded prior partial-read scope. This turn is record-level reading. |
| Observation `input_sha256`, `input_path` | Bind the actual input representation used by a governed append/reconciliation. Keep the scan checksum separately identified in provenance text. | Do not replace the r190 packet digest with a PDF digest or pretend the external appraisal was in `collections.source_metadata`. |
| `upstream_assessment_id`, community observations | Primary upstream assessment remains null unless genuinely assigned upstream; preserve community assessment 43 and its history. | No new PRISM assessment number or community full-source reading inferred. |
| `evidence_status`, `upstream_integration_status`, `visibility`, all five `restrictions` | Keep `unassessed`, actual upstream status/visibility and exact access, cultural_authority, privacy, provenance and rights values. | Documented access is not clearance for scope. This sidecar overrides no held/unknown category. |
| Review `direct_evidence` | Draft: “PR #416 records complete archived-scan access and the published authors' retrospective investigations; original case artifacts remain uninspected.” | These are reported observations and testimony, not independently verified anomalous acquisition. |
| `interpretation`, `counter_evidence`, `synthesis`, `hypothesis` | Use the bounded page-specific prompts below; provisional synthesis is that these cases illustrate failure mechanisms without a population rate or survival conclusion. Leave hypothesis empty unless explicitly proposed. | No seven-frauds shorthand, general refutation, survival endorsement or inference from residual uncertainty. |
| `missing_information`, `uncertainty` | Replace the blanket access gap in the new worksheet revision with rights, original-record, OCR/completeness and reviewer limitations listed below. Retain the historical list in earlier reviews. | Access to the scan does not settle source authenticity, case facts or permission. |
| Review ID/history, `source_bindings`, `state`, `reviewer`, `perspectives`, `disclosures` | Any later executable revision needs a fresh unique review ID, actual `supersedes`, recording date and recomputed full-source-history bindings. Keep `PENDING_HUMAN_REVIEW`, `reviewer=null`, no disclosures and twelve `INSUFFICIENT_INFORMATION` dispositions pending governed review. | Preserve earlier reviews. No approval transfer, completed human attestation or automatic perspective completion. |

The default adapter still hard-pins r190, constructs a primary `metadata_only`
observation and leaves retrieval null. Its optional reconciliation requires a
later complete input snapshot with a new dataset revision/digest and a fresh
unreviewed worksheet. It does not ingest PR #416 by URL. Admitting a later real
PRISM packet requires a reviewed input-lock change and validation. Do not invent
r191, alter r190's table hashes or manually relabel the baseline import.

A separately governed manual `--contract` append can use the existing schema
only after resolving actual prior observation/review IDs, input provenance and
full history hashes. It must be labelled as that manual route, never as a
replayed later PRISM import. No executable append is performed by this addendum.

## Methodological Prompts for the Existing Worksheet

These are compressed paraphrases of the pinned appraisal, not a duplicate
seven-case review or new inspection of the scan. Locators are printed/PDF pages.

| Worksheet use | Pages | Finding and question for the reviewer |
| --- | --- | --- |
| Design, dependence and inference limits | 2–3 | Selected retrospective cases, not a representative or prospectively controlled sample. No complete intake denominator or detection-sensitivity estimate. Do not calculate a deception prevalence or count seven independent replications. |
| Prompting and reconstructed testimony | 5–7 | Nimal's watch test was described differently by later witnesses, including prompting and prior disclosure of the search purpose. Distinguish inaccurate recollection from proven dishonesty. |
| Contrary evidence and uncertainty | 9–10; 14–15 | Wijesuriya remained untraced and hoax unproven. Shishupal's reconstruction is hypothetical; congenital-mark status and the complete wrong-answer inventory are missing. Do not equate all defects with intentional fabrication. |
| Exposure chronology | 15–18 | Mahender selected from supplied names; indirect family contact preceded the proposed identification. Letters before a family meeting do not prove statements before exposure. Ask for dates, prompts, all misses and original letters. |
| Conflicting testimony | 20–22 | Mahesh's alleged coaching confession was not corroborated by its alleged recipient; debt evidence was disputed. Authors withheld a definite interpretation while favouring possible genuine memories. Preserve both their uncertainty and that interpretation. |
| Early records and reported exposure | 23–26; 28–29 | Kenedi's earlier record constrains the later story but does not reveal the exact learning mechanism. Morris is the strongest reported journalistic-hoax exposure; the original investigation/retraction was not freshly authenticated. |

**Draft synthesis:** the recovered publication enables a substantive, checkable
review of prompting, prior information routes, testimony reconstruction and
disputed reporting. Its conclusions vary by case. Neither seven equally proven
frauds nor a deception rate, universal ordinary explanation or evidence of
personal survival follows. BQ001 remains UNRESOLVED.

**Remaining review questions:** independently check the scan/appraisal and OCR
against the cited pages; obtain original field notes, interviews, letters, mark/
autopsy records and the original Morris retraction where available; examine
supportive sources at their own full-text depth; resolve child/family privacy,
cultural context, reuse rights and scope-specific disclosure upstream. Archive
access establishes no reuse licence. Do not seek identities behind pseudonyms.

## Packet Locations and Separate Gates

In `AkashicNET-v018-Pilot-Review-Packet-2026-10-27.html`, append a dated **Section
16: Stevenson Source Recovery and BQ001 Reassessment — 30 October 2026**, with a
current-status notice at the beginning pointing to it. It supersedes primary-
access limitations in Sections 1–3, 5, 7, 11–15 for this archived representation,
without rewriting those dated decisions. Reuse the claim/source register,
DISCERN/DEEPEN, synthesis, uncertainty and review-sharing fields already present.
Keep the supplied-community and Atlas reviews at their original scope.

The following are separate and unchanged: authenticated human appraisal;
independent scientific review and objections; all five scope-specific source
restrictions; **14 OMNI bindings across 13 distinct historical dependencies**;
complete component/method-pin gates; release review and release approval.

Keep `real-public-status.json` byte-identical: **HOLD**, `sources=[]`,
`review=null`, **UNRESOLVED** and all promotion guards false. No model support,
accepted edge, evidence/rights/identity promotion, merge, release, deployment or
website/social publication follows from this recovery.
