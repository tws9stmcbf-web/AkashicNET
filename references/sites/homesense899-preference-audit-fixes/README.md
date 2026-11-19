# HOMESENSE899 Preference Audit Fixes

This is a review reference for the authoritative Sites checkout, not a public-repository deployment.

Base Sites source: `5816499f243bff493632d5966efe3e8c8e4991e3` (version 1923).
Implementation commit in the isolated checkout: `73291bdc`.
The older PR #420 reference is historical; do not apply it over these changes.

## Changes

- Explicit optional sharing and a skip action that clears unsent fields and returns focus.
- Retry-After cooldowns and editable choices after a definitive first rejection.
- Frozen original payload/key after uncertain outcomes, including later rejections, with a safe 23-hour retry deadline.
- Preference reporting requires both a Sites user ID and the existing configured owner email. Access is not expanded.
- Content-free scheduled cleanup success/failure events and an hourly Worker trigger request.
- Updated privacy disclosures covering retired comments, consent, operational safeguards and idle-time retention.
- Operations runbook inside the patch covering deployment, scheduling, edge abuse controls and staging verification.

## Validation

13 local API/client tests passed. TypeScript checks and the full build passed.
Build checks include public routes/assets, page history/search, capacity, security headers and a sitemap of 444 public URLs.
The built Worker configuration retains the requested hourly cron, `17 * * * *`.

The local preview timed out during startup, so interactive browser verification of the revised UI remains incomplete.
Production writes, identity-header stripping, migrations, physical cleanup, trigger installation and edge enforcement were not tested.
No production records, owner access rules or live pages were modified.

## Apply Later

Use `git apply --check source.patch` against the named Sites base, or reconcile the patch into newer authoritative source.
The patch adds no database migration. Existing totals and unexpired legacy comments are preserved.
Review `docs/homesense899-preference-operations.md` after applying.
Do not claim automatic retention is operational until the deployed scheduler and independent run are confirmed.
The shared application quota remains; edge controls and alerts require deployment-time configuration.
Deployment is held under the original request's explicit restriction.
