# Pilot validation record

Prepared 22 October 2026. This records local engineering checks, not Reddit app
approval, hosted behavior, scientific review or AkashicNET release readiness.

| Check | Recorded result |
| --- | --- |
| Clean install from package-lock | PASS: `npm ci --ignore-scripts --no-audit --no-fund` |
| Strict TypeScript project build | PASS: `npm run type-check` |
| Service, HTTP and schema tests | PASS: 20 tests, zero failures |
| Production client and CommonJS server build | PASS: `npm run build` |
| Installed official Devvit config schema | PASS, included in the test suite |
| Runtime dependency audit | Zero reported vulnerabilities: `npm audit --omit=dev --json` |
| Full tooling dependency audit | 12 high-severity package entries remain, derived from the upstream `braces` advisory below |
| Reddit CLI identity | Not authenticated: `devvit whoami` reported “Not currently logged in” |
| Reddit developer browser | Timed out while opening the developer app-creation page |
| Reddit-hosted playtest and mobile visual inspection | NOT RUN |
| App registration/name reservation, review submission, installation and launch | NOT COMPLETED |

The final app check ran under Node.js 24.19.0 and npm 11.9.0. The pinned Devvit
SDK/CLI is 0.15.0. Tests use injected storage and publishing dependencies; the
suite does not call Reddit or claim to reproduce its hosted runtime.

## What the tests cover

- Configuration validity; public catalog URLs and preserved research status.
- Anonymous browsing; forged moderator flags; direct internal-menu calls;
  moderator permission loss between preview and publication.
- Invalid input, oversized bodies, malformed JSON, arbitrary article IDs,
  forged/outdated flair templates and Markdown-like moderator prose.
- Preview expiry, replacement, identity/source-post/installation binding and
  rejection of final-request fields that try to change the frozen preview.
- Concurrent submissions, retries, and identical content from another moderator.
- Ambiguous Reddit failures and receipt-write failures without automatic resubmission.
- Saved public snapshots, visible failure for missing snapshots, and one launcher
  per installation.

## Upstream CLI advisory

The official starter's Devvit CLI brings in `braces@3.0.3`, through both file-watching
and CLI globbing dependencies. npm reports
[GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm): stack-exhaustion
denial of service from deeply nested patterns. At inspection, `npm view braces version`
returned 3.0.3, so no patched release was available from the configured npm registry.
The 12 audit entries represent affected packages in that dependency chain, not
12 independently established vulnerabilities in this app.

The CLI and Vite tooling are development dependencies. They are not imported by
the app's client or server entry points. This reduces hosted exposure but does
not establish that the developer tooling is safe against hostile local inputs.
Two available compatible patches are pinned through npm overrides: `image-size`
2.0.4 and `tmp` 0.2.7. A clean install and the app checks pass with those patches.
No forced downgrade of Devvit or cross-major CLI dependency replacement was made.

Review the upstream advisory before broader rollout. Re-run both audit commands
when dependencies change; the production-only audit does not clear the full toolchain.

## Still required on Reddit

Authenticate the intended developer account, register the app, verify the test
community's visibility and moderator permissions, and exercise a real publication
and its fallback. Check mobile layout, links, flair behavior and Redis responses.
Keep the pilot in a development community until those results are recorded and
Reddit's review requirements for the intended community have been satisfied.

No message or post was sent to r/NeuronsToNirvana or r/microdosing during this build.

## Private-playtest preflight follow-up

Checked 22 October 2026 America/Los_Angeles (23 October UTC), against implementation
commit `ca6ef2135dfeef3b930e066c7a3ed99863731c74`. PR #414 remained open and draft;
all 14 returned PR-triggered workflow runs for that commit had succeeded,
including Reddit Research Companion run `39890457937`. No PR comments recorded
a subsequent hosted installation when checked.

A fresh checkout and locked install under Node 24.19.0/npm 11.9.0 passed all
20 tests, strict typecheck and production build. Installed CLI: 0.15.0.
`devvit whoami` reported that it was not logged in. No CLI token file or
DEVVIT environment variables were present before setup; no credentials were read.
The production audit again reported zero vulnerabilities; the full audit still
reported 12 high-severity affected-package entries. `npm view braces version`
returned 3.0.3; the upstream advisory still listed no patched version.

The developer-browser request first timed out. Recovery exposed Reddit's login
page with a site-served network-security block and no usable sign-in form.
Developer identity, app registration/name availability, private community,
moderator roles and current flair options could not be verified.

No registration, upload, installation, Reddit post, review submission or launch
was performed. All hosted behavior, old-Reddit fallback and mobile acceptance
checks remain NOT RUN. See [HOSTED-PLAYTEST.md](HOSTED-PLAYTEST.md) for a bounded
continuation, including the CLI's automatic-community/content side effects and
approval stop points. The follow-up changes documentation only.

## Known-ID metadata scanner · 24 October 2026

Added a server-only manifest for 7,463 saved N2N IDs, an offline structural
preflight/citation generator, moderator-only metadata plan and batch endpoints,
and a cursor-continuation UI. Private playtests can read only their current
companion post; the N2N manifest is refused in other installations.

Node 24.19.0/npm 11.9.0: strict TypeScript checks, **32 automated tests** and
the production client/CommonJS-server build pass. The 12 added tests cover
manifest integrity, bounded capture, permission checks, private isolation,
invalid cursors/fingerprints, shared cooldown, transient/unavailable outcomes,
content suppression, wrong-community responses, final batches and actual HTTP
authorization/request-size/cache headers. No dependency versions changed.

The saved export was fully processed offline: 7,463 unique matching IDs,
3 curated titles, 22 prior observed titles, 7,438 uncaptured titles, 237
site-cited records and 7,226 remaining discovery citations. Fingerprints and
zero-live-retrieval status are in the preflight JSON. These are structural
checks, not confirmation that the posts exist or are currently available.

The metadata scanner stores no captured post content on the server and makes
no automatic website/export calls. Captures remain in the open view's memory
until the operator copies them. Saving packets and a resume cursor is manual;
unattended operation and durable result storage are not implemented.

The installed CLI still reports **Not currently logged in**. No registration,
upload, installation, live lookup or Reddit publication was performed. The
expanded native mobile UI and real Reddit-hosted capture remain unverified.
External retention/deletion handling must precede any live-content integration.

## Offline metadata staging continuation · 24 October 2026

Added `tools/stage-n2n-capture.mjs` and 14 adversarial/staging/CLI tests.
Strict application TypeScript checks, **46 total tests**, and the production
build pass. The importer validates manifests, community/URL identity, bounded
packet sequences, gaps, retries, timestamps, content suppression, same-time
conflicts, unknown fields and review gates. It preserves input files, refuses
output overwrite and writes the new review file with mode 0600.

All capture examples used in these tests are explicitly synthetic. No live
Reddit metadata was acquired or imported. Staging marks a supplied packet as
UNVERIFIED_OPERATOR_EXPORT: structural validity is not authentication. Public
eligibility remains HOLD; rights/evidence promotion and canonical writes are OFF.

A fresh access check still found an unauthenticated CLI. The developer app
page showed a signed-out permission screen; its normal Log in link led to a
Reddit-served network-security block without usable credential fields. No
attempt was made to evade the block, and app ownership/installation remains
unverified. No upload, hosted scan or live Reddit change occurred.
