# AkashicNET Research Companion for Reddit

A bounded Devvit pilot for browsing public AkashicNET article descriptions and
preparing moderator-reviewed research discussions inside Reddit.

**Status: development pilot.** Local build and automated verification are recorded
in [VALIDATION.md](VALIDATION.md). A Reddit developer account has not been connected
in the build environment. The app name is provisional and has not been reserved;
no Reddit playtest, installation, review submission or public launch is claimed.

## What the pilot does

- Readers browse and filter a bundled public catalog, inspect the uncertainty
  boundary, and open the canonical article using Reddit's navigation API.
- A moderator with `posts` or `all` permission chooses an article, edits the title
  and plain-text summary, and selects an actual flair from the installation's
  subreddit. A date suffix can be added to the editable title when appropriate.
- **Preview exact post** stores an immutable draft for ten minutes. Claim types,
  research status, source URLs, destination and app-account attribution are visible.
- **Publish this post** checks moderator permissions again and submits the saved
  preview as an interactive custom post. Its complete Markdown text is provided
  as the old-Reddit text fallback. The app account is the author.
- Readers see the saved publication snapshot even if a later app version changes
  the catalog. Source links lead to the articles' current wording and references.

The initial catalog contains BQ001 and Intention Awareness. It preserves BQ001's
open conclusion and the intention proposal's untested status. These are editorial
public-page descriptions, not completed source appraisals or independent findings.
The pilot does not import PRISM, promote evidence, or change the v0.18 release gate.

## Run the checks

From the repository root, using Node.js 24.18.0 or later:

```sh
cd apps/reddit-research-companion
npm ci --ignore-scripts --no-audit --no-fund
npm run check
```

The checks validate the actual configuration against the installed Reddit schema,
run the service and HTTP authorization tests, typecheck strictly, and build the
client and CommonJS server. The Node test loader avoids a local test-runner socket.
The GitHub workflow runs the same checks and audits production dependencies.

## Connect and playtest

Follow [HOSTED-PLAYTEST.md](HOSTED-PLAYTEST.md) for the private-community
preflight, approval stop points, reproducible commands and hosted test record.
Devvit can automatically create a development community and test content; the
absence of an app installation trigger does not disable CLI/platform behavior.

1. Sign into the intended Reddit account at
   [Reddit for Developers](https://developers.reddit.com/new).
2. In this app directory, run `npm run login`. For a remote terminal that cannot
   receive a localhost callback, use `npm run login -- --copy-paste` and complete
   the official CLI flow in your own terminal. Keep all codes and tokens private.
3. Run `npm run register` once to connect this source to a newly registered app.
   This invokes `devvit init --force`: in an existing Devvit directory the CLI
   updates the registered app name while retaining the custom source. If the
   proposed name is unavailable, choose another name in the official wizard.
   Review the resulting metadata/lockfile changes and rerun `npm run check`.
4. Verify a dedicated private community and the intended moderator account first.
   Use the explicit-target upload and playtest sequence in HOSTED-PLAYTEST.md;
   do not run bare `npm run dev` on a newly registered app. Obtain approval for
   platform-created test content before starting the playtest. Do not start the
   pilot in r/NeuronsToNirvana or r/microdosing.
5. Use the subreddit menu **Open AkashicNET Research Companion** to create its
   launcher post. Installation itself has no posting trigger. Reopening the menu
   returns the existing launcher instead of creating a second one.
6. Prepare and preview a test discussion, publish it once, then verify the actual
   post, flair, app-account attribution, canonical links and old-Reddit fallback.
   Test a reader/non-moderator account, mobile layout and reduced-motion settings.

Reddit-hosted API calls cannot be proven by a local browser preview. Record the
actual app slug, development community, version and test-post URL only after this
hosted playtest succeeds. No authentication secrets belong in that record.

## Review and community rollout

`npm run deploy` validates the app and uploads a development version. `npm run launch`
validates, uploads and requests Reddit review. These are explicit operator actions;
neither CI nor app installation runs them. Reddit's quickstart says apps require
review before installation in communities with more than 200 members.
An unconfigured upload can also bootstrap a default development community. Use
the bounded sequence in HOSTED-PLAYTEST.md for this private pilot. Do not run
`npm run launch` or `devvit publish` as part of the playtest.

Complete the hosted tests and review the open dependency-tooling note in
[VALIDATION.md](VALIDATION.md) before deciding on broader rollout. A working local
build does not mean the app is registered, approved or installed on N2N.

## Publication integrity and recovery

- Every mutation checks the authenticated server context, not client-supplied
  identities or moderator flags. Drafts are bound to user, source post and subreddit.
- The final request names only a preview ID. Its replacement title, sources,
  destination or evidence labels cannot override the stored preview.
- A permanent atomic Redis claim is keyed by installation and exact content.
  Repeated or concurrent submissions return the existing receipt or a pending
  response. This also covers identical previews prepared by different moderators.
- If submission times out, its claim stays pending: a retry must not silently
  create another post. Inspect the subreddit and Devvit logs before reconciling.
  An operator may write a verified existing post ID/URL into that receipt, or
  clear a pending claim only after confirming that Reddit created no post. This
  pilot deliberately has no public unlock endpoint. Do not change the title to
  evade an unresolved claim.
- Public snapshots are stored before submission. Reddit post data contains only
  their short identifier, within the SDK's two-kilobyte post-data limit.

## Data and permissions

See [PRIVACY.md](PRIVACY.md). The app requests Reddit API and installation-scoped
Redis access. HTTP fetch, external endpoints, schedulers, install triggers, media,
payments and posting as a user's account are absent or disabled. The pilot does
not need website-to-Reddit webhooks, domain approval or AI-provider credentials.

To update the catalog, edit `src/shared/catalog.ts`, inspect the current public
sources, retain uncertainty boundaries, increment `CATALOG_VERSION`, and rerun
checks. A snapshot check date is an editorial check, not a scientific-review date.

## Source and license

Scaffold adapted from the official
[reddit/devvit-template-react](https://github.com/reddit/devvit-template-react)
at `d1b4e25666e23109428476f5d69f62252f85c40d`, using Devvit 0.15.0.
The starter's BSD-3-Clause notice is retained in [LICENSE](LICENSE).

Primary documentation consulted:

- [App quickstart](https://developers.reddit.com/docs/quickstart)
- [Devvit Web](https://developers.reddit.com/docs/capabilities/devvit-web/devvit_web_overview)
- [Reddit API](https://developers.reddit.com/docs/capabilities/server/reddit-api)
- [App configuration](https://developers.reddit.com/docs/capabilities/devvit-web/devvit_web_configuration)

Where prose examples differ, the installed SDK's schema and types are used.
