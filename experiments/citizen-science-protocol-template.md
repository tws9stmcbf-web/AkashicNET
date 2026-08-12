---
id: experiment-YYYY-NNN
title: "Short descriptive title"
authors:
  - Contributor Name (role)
year: 2026
status: exploratory # use Phase 2 categories: established|emerging|working hypothesis|speculative
preregistered: false
preregistration_uri: ""
data_path: data/experiments/experiment-YYYY-NNN/
evidence_rationale: "Short rationale for evidence status"
---

# Citizen Science Protocol Template

## Purpose

This template is a reusable framework for designing citizen-science research protocols in the Noetic Sciences Toolkit.
It is intended to support transparent documentation of research planning without prescribing a specific study.

This template is aligned with Phase 2 evidence and documentation principles, including:
- research database structure
- evidence-rating methodology
- structured references
- research landscape categories

**Required metadata:** contributors must complete the YAML frontmatter above with a unique `id`, `title`, `authors`, `year`, `status`, `preregistered` (boolean), `data_path`, and `evidence_rationale` before publishing the protocol. When `preregistered: true` provide `preregistration_uri` and a timestamped record of the preregistration.

## 1. Research Question

- What specific question will the protocol investigate?
- The question should be clear, focused, and answerable through observation, measurement, or structured inquiry.
- It should be aligned with the Toolkit's domains, such as consciousness, neuroscience, contemplative science, wellbeing, or systems research.

## 2. Hypothesis

- Describe the expected relationship or outcome.
- Distinguish between:
  - exploratory hypotheses: tentative ideas intended to guide investigation
  - confirmatory hypotheses: pre-specified predictions based on prior evidence or theory
- Include a brief rationale that is consistent with available evidence and does not overstate what is known.

## 3. Exploratory vs Confirmatory Status

- Explicitly classify the protocol as one of the following:
  - N-of-1 exploratory work: single-participant observation that generates hypotheses and documents individual experience.
  - Naturalistic observation: open-ended observation of real-world behaviour or experience without a controlled intervention.
  - Citizen science: collaborative data collection with participants contributing as co-researchers or volunteers.
  - Confirmatory research: hypothesis testing with pre-defined criteria, controls, and an analysis plan intended to support inferential conclusions.

- Note that these modes can overlap, but their research claims and interpretation differ.
- Emphasise that N-of-1 exploratory work and naturalistic observation are valuable for generating questions, not for generalisable proof.

## 4. Preregistration

- State whether the protocol will be preregistered.
- If yes, specify the preregistration platform or storage method and the planned timestamp.
- Include the key elements to preregister:
  - research question
  - hypothesis
  - primary outcomes
  - analysis plan
  - criteria for interpretation

**Preregistration: required fields (recommended when confirmatory)**

- `primary_outcome`: exact variable name and units
- `primary_timepoint`: when primary outcome is measured
- `analysis_plan`: short description plus link to analysis code/notebook
- `alpha`: statistical threshold or statement if not applicable
- `sample_size_calc`: either the calculation or reason sample-size calculation is not applicable
- `stopping_rules`: any stopping or interim analysis plans
- `preregistration_timestamp`: ISO 8601 timestamp or link to timestamped preregistration

## 5. Study Design

- Describe the overall design, for example:
  - observational
  - within-subject or repeated measures
  - comparative or cross-sectional
  - longitudinal
  - mixed methods
- Indicate the intended level of control and the degree of standardisation.
- For exploratory work, describe how the design supports pattern discovery or hypothesis generation.
- For confirmatory research, describe how the design supports hypothesis testing.

## 6. Participants / Sampling

- Define who will participate and how they will be selected.
- For citizen science, note whether participants are self-selected, community-recruited, or invited through a call.
- Describe inclusion and exclusion criteria.
- Note any relevant demographic, experiential, or contextual characteristics.

## 7. Variables

- List independent variables or factors.
- List dependent variables or outcomes.
- Identify covariates, moderators, or potential confounders.
- Clarify which variables are manipulated, observed, or measured.

## 8. Outcomes

- Define primary outcomes clearly.
- Define any secondary or exploratory outcomes.
- Specify the type of outcomes, such as:
  - subjective experience
  - behaviour
  - physiological measures
  - task performance
  - qualitative descriptions

## 9. Measurements and Instruments

- Describe the instruments, tools, or measures used.
- Note whether measures are validated, self-report, sensor-based, qualitative, or quantitative.
- Specify the timing, frequency, and context of measurements.
- Describe any training or standardised instructions for participants.

## 10. Controls and Confounders

- Identify potential confounders.
- Describe control or comparison strategies, such as:
  - baseline measures
  - repeated measures
  - within-subject comparisons
  - standardised procedures
  - counterbalancing
- Explain any limitations when control conditions are not feasible.

## 11. Data Collection

- Describe how data will be collected and recorded.
- Include methods for logging, storing, and preserving data.
- Note whether data collection is prospective or retrospective.
- Specify any tools, platforms, or formats used for data entry.

## 12. Analysis Plan

- Describe the planned analytic approach.
- For exploratory work, specify how patterns, themes, or observations will be identified and described.
- For confirmatory research, specify statistical or analytic criteria for hypothesis evaluation.
- Describe how data quality will be assessed.

## 13. Missing Data

- Describe how missing or incomplete data will be handled.
- Specify whether missing data will be:
  - excluded
  - interpolated
  - documented as part of the protocol
- Explain how missing data will be reported.

## 14. Reproducibility

- Document the protocol in enough detail for another researcher to understand and follow it.
- Include materials, procedures, timings, measurement tools, and analytic steps.
- Note where raw or anonymised summary data may be shared, subject to privacy and ethics constraints.

## 15. Ethics and Informed Consent

- Describe ethical considerations and potential risks.
- Specify how informed consent will be obtained and documented.
- Note when professional oversight, qualified advice, or ethics review is required.
- Emphasise that this framework does not replace clinical or ethical review.

## 16. Privacy and Data Minimisation

- Describe how personal data will be protected.
- Use the minimum data necessary for the research question.
- Describe anonymisation, de-identification, or pseudonymisation procedures.
- Explain how data retention and deletion will be managed.

## 17. Safety Considerations

- Identify any safety risks and how they will be minimised.
- Describe any contraindications or warning criteria.
- For research involving wellbeing, cognitive practices, or substances, note when qualified supervision is needed.
- Emphasise participant wellbeing throughout the protocol.

## 18. Limitations

- Describe known limitations of the protocol.
- Distinguish between limitations of the study design and limitations of inference.
- Be explicit about what the protocol cannot establish.
- Note any sources of uncertainty.

## 19. Interpretation

- Describe how the results will be interpreted in light of the evidence hierarchy:
  - Evidence → Observation → Interpretation → Hypothesis → Speculation
- Emphasise that exploratory N-of-1 observations and naturalistic observations are not equivalent to population-level confirmation.
- For confirmatory research, specify the conditions under which a hypothesis would be supported, not supported, or remain inconclusive.

## 20. Replication / Follow-up

- Describe whether and how the protocol can be replicated.
- Note follow-up studies, extensions, or confirmatory research that could build on the protocol.
- For exploratory work, describe how the findings could inform future questions or more controlled designs.
- For confirmatory work, describe replication criteria and potential next steps.
