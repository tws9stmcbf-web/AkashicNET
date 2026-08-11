# Citizen-Science Operational Guidance (lightweight)

This document provides practical, operational guidance for running citizen-science pilots aligned with Phase 3 integration frameworks.

Onboarding & training

- Provide a short onboarding script explaining goals, data collected, consent, and privacy protections.
- Offer simple training examples for any self-report measures or tasks to reduce variability.

Minimal submission metadata (required for every record)

- `timestamp` (ISO 8601)
- `participant_id` (pseudonym)
- `platform` (e.g., web, app, community-forum)
- `context_tag` (short label describing context)
- `protocol_id` (experiment-YYYY-NNN)

Data validation & quality control

- Apply basic automatic checks: timestamp validity, value ranges, required fields present.
- Implement duplicate detection heuristics (same pseudonym + identical timestamps, text similarity thresholds).
- Flag low-quality submissions for manual review (e.g., impossible values, incoherent text).

Provenance & provenance fields

- Require `provenance` fields for externally-sourced inputs (see `experiments/visual-provenance-template.md`).
- For community signals, record `source_platform`, `post_id` (if permitted to record), and `access_date`.

Data pipelines & storage

- Store raw inputs under `data/experiments/<protocol_id>/raw/` and processed outputs under `data/experiments/<protocol_id>/processed/`.
- Maintain a `data-dictionary.yaml` at the protocol root describing fields and units.

Analysis & transparency

- Publish analysis scripts and environment specifications alongside reports. Use commit hashes or release tags for reproducibility.
- Document any deviations from the preregistered plan and justify them in the protocol record.

Community engagement & feedback

- Share plain-language summaries and anonymised aggregated results with participants and community channels when appropriate.
- Provide an opt-out mechanism and an easy data-deletion request procedure.

Governance

- Maintain a small steering group or maintainers responsible for triage, ethical review referrals, and final decisions on reuse of community material.
