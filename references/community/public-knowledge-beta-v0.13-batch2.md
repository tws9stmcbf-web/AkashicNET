# Public Knowledge Beta v0.13 — Batch 2

This batch reduces two v0.13 readiness blockers without adding speculative content.

- Big Questions extensibility: existing `references/big-questions/architecture-v0.1.json` already defines a generic `questions` registry, one canonical tree per question, and fail-closed placement rules. A v0.13 validator now checks that registry structurally. No BQ002 is fabricated.
- Public source/link integrity: a v0.13 validator now scans canonical Big Questions evidence source records, requires preservation of the original URL field, and validates stored link-check metadata when present. Link unavailability is metadata, not evidence that a source is false.

Invariants remain unchanged: truth inference OFF, rights promotion OFF, scientific-evidence promotion OFF, private Drive promotion OFF, and API-unverified Reddit records may not be labelled API-verified.
