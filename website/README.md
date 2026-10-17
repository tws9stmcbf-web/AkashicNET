# AKASHICNET.ORG website snapshot

This directory preserves the public-facing AkashicNET website as a historical record alongside the evolving research toolkit.

- Canonical public domain: https://akashicnet.org
- Snapshot date: 30 August 2026
- Public pages represented: home and community
- Hosting source of truth: ChatGPT Sites
- Repository role: historical provenance, review and change tracking

The public website describes an evolving citizen data-science project. Statements may be revised, corrected or rejected as evidence and interpretation develop. Git history is part of the epistemic record: it should show how both useful and mistaken theories change over time.

Private Google Drive corpus material, credentials, private research notes and personal data are intentionally excluded.

Binary artwork is deployed with the Site. Its integrity hashes and provenance are recorded in `assets/MANIFEST.md`.

## Latest-news maintenance

The 16 October 2026 TSC2026 alignment is documented in
[`docs/tsc2026-news-publication-audit-2026-10-16.md`](../docs/tsc2026-news-publication-audit-2026-10-16.md).
The curated records in `lib/tsc-research-highlights.ts` feed this snapshot's ticker
and homepage template. TSC2026 links open the canonical public Site because those
routes are not present in this snapshot.

Edit `status-templates/home.tsx.in`, then regenerate with
`python scripts/validate_public_status_consistency_v016.py --write` from the
repository root. Update and deploy the separate Sites source for live changes;
a GitHub merge alone does not publish them.
