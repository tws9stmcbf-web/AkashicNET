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
