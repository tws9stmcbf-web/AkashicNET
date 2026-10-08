/** Previous released reference, preserved at its original version and date. */
export const akashicOmniPreviousRelease = {
  version: "0.4.5",
  anchor: "v0-4-5",
  date: "27 September 2026",
  dateTime: "2026-09-27",
  status: "PRE-ALPHA",
  changeNote: "Clarifies EXPAND² as two review passes, DISCERN and DEEPEN, followed by a synthesis output; aligns the ACTC lens with its existing repository description of agency, context, temporal order and candidate causes; and distinguishes interpretive outcome labels from evidence ratings. Prompted by the 27 September cross-surface consistency audit, not an external framework or post series. This documentation patch adds no lens or capability and changes no evidence status or prior assessment. Earlier assessments retain their original version and date and are not recalculated. At this release, the proposed v0.5.0 claim-review capability was unreleased; the later Public Review Specification is recorded separately.",
} as const;

/** Public manual specification, not a software release. Verified 7 October 2026.
 * Sources and engineering boundaries: docs/AKASHICOMNI_V050_PUBLIC_STATUS.md.
 */
export const akashicOmniRelease = {
  version: "0.5.0",
  anchor: "v0-5-0",
  date: "1 October 2026",
  dateTime: "2026-10-01",
  status: "PUBLIC REVIEW SPECIFICATION",
  specificationHref: "https://akashicnet.org/akashicomni/v0-5-0",
  clarificationNote: "Method clarified 2 October; availability and researcher starter kit updated 7 October 2026.",
  availability: "Available for manual, human-reviewed analysis. Full software integration and independent effectiveness validation remain incomplete.",
  softwarePilotHref: "https://github.com/tws9stmcbf-web/AkashicNET/pull/367",
  softwarePilotStatus: "UNRELEASED / REVIEW_REQUIRED",
  reflection: "Embodied intelligence informs wisdom; love and discernment guide it into service.",
  interpretation: "Within this framework, bodily awareness can contribute to wise judgement when considered alongside reflection, evidence, ethics and consequences. Bodily intuition can be mistaken. This is an interpretive principle, not a validated formula, a clinical assessment or a claim that illness produces wisdom.",
  guidance: [
    ["Identify the claim", "State the precise question and distinguish observation, testimony, interpretation, hypothesis and speculation."],
    ["Name the source and access", "Give the source and location, say what was actually inspected, and distinguish first-person testimony, secondary biography and independent corroboration. A link alone does not establish verification or reuse rights."],
    ["Examine the inference", "Separate biographical context, interpretive descriptions of work and contribution. Compare alternative explanations; do not infer diagnosis or causation from resemblance or achievement."],
    ["Preserve uncertainty", "Record missing information and relevant contrary evidence. An outcome signal expresses an assessment, not a truth score or permission to promote evidence."],
    ["Connect insight with action", "Explain what a proportionate, compassionate action could be and what observations would change the assessment. Keep the framework version and assessment date with the result."],
  ],
  changeNote: "Records the published manual methodology: twelve analytical perspectives plus synthesis, structured claims, perspective coverage, source-access limits and conditions for revision. The researcher starter kit supports manual use. This status reconciliation does not release the separate engineering pilot or establish independent validation. Earlier assessments keep their original method and date; evidence, rights and review gates are unchanged.",
} as const;
