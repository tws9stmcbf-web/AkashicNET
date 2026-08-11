# Privacy, Ethics & Data Protection Guidance

This document summarises practical privacy and ethics guidance for Phase 3 experiments and citizen-science projects. It is not a substitute for legal advice or institutional review.

Key obligations and recommendations

- Data minimisation: collect the minimum data necessary for the research question.
- Pseudonymisation: store personal identifiers separately from observation data and use stable pseudonyms for participants.
- Anonymisation: when publishing datasets, prefer anonymised or aggregated data; follow de-identification best practices.
- Consent: use the `experiments/consent-template.md` and record consent artifacts.
- Retention & deletion: specify retention periods in the protocol; implement a deletion workflow for withdrawal requests.
- Access control: restrict raw data access to authorised personnel; use encrypted storage for sensitive data.

Legal compliance checklist (non-exhaustive)

- Identify applicable laws (e.g., GDPR, CCPA) and whether the project triggers special protections for health data.
- If operating with EU data subjects or EU-based servers, perform a Data Protection Impact Assessment (DPIA) for higher-risk projects.
- Document lawful basis for processing (consent, legitimate interests, etc.) and maintain records of processing activities.

Technical measures

- Encryption-at-rest and in-transit for sensitive files.
- Use access logs and audit trails for data access.
- Keep a `data/experiments/<id>/README.md` describing storage location and access controls.

Ethical review and safety

- For interventions with health or psychological risks, obtain appropriate ethics review or professional oversight.
- Provide participant resources and emergency contacts when interventions could cause harm.

Special considerations for community-derived material

- Do not scrape or republish identifiable community posts without permission.
- When summarising community signals, report aggregated patterns and avoid verbatim reproduction of potentially identifying content.

Record-keeping

- Keep consent records, provenance of third-party materials, permission evidence, and a decision log for any reuse of external visuals or posts.
