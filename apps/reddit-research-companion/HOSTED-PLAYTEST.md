# Private Reddit-hosted playtest continuation

Prepared 22 October 2026 America/Los_Angeles (23 October UTC).
Implementation checked: `ca6ef2135dfeef3b930e066c7a3ed99863731c74`, PR #414.

**Hosted status: BLOCKED / NOT RUN.** A fresh locked installation, 20 local
tests, strict typecheck and production build pass. Devvit 0.15.0 reports that
the CLI is not logged in. The developer-browser navigation redirected to
Reddit login, where Reddit displayed a network-security block before usable
sign-in controls appeared. No developer identity, registered app, community,
installation, post or mobile result has been verified in this session.

This is an operator continuation, not a completed hosted test report. Keep
the original implementation; do not generate a replacement starter app.

## 1. Reproduce the verified local baseline

Use a supported computer/terminal with Node.js >=24.18.0, npm and Git, plus
ordinary access to Reddit. A separate browser sign-in does not authenticate
the blocked cloud browser or this CLI. Never put tokens or initialization
codes in chat, Git, screenshots or PR comments.

For a fresh checkout in an unused directory:

```sh
git clone --branch codex/devvit-research-companion --single-branch https://github.com/tws9stmcbf-web/AkashicNET.git AkashicNET-devvit-playtest
cd AkashicNET-devvit-playtest
git switch --detach ca6ef2135dfeef3b930e066c7a3ed99863731c74
cd apps/reddit-research-companion
npm ci --ignore-scripts --no-audit --no-fund
npm run check
./node_modules/.bin/devvit --version
```

The detached checkout reproduces the checked implementation. Use a separate
working branch if registration metadata will be committed. Alternatively,
review the current PR head and record its SHA before testing that version.

## 2. Authenticate and register, without starting the playtest

```sh
npm run login
./node_modules/.bin/devvit whoami
```

If the browser and terminal are on different hosts, the official alternative
is `npm run login -- --copy-paste`. Complete the code exchange privately in
your own terminal. Use the intended account in both the developer browser and
CLI. Inspect any developer terms and permission requests before accepting.

First check the developer dashboard for an app already owned by this account.
The configured `akashicnet-research` name is provisional; availability remains
unknown. If it has not already been registered for this project:

```sh
npm run register
git diff -- devvit.json package.json package-lock.json src
npm run check
```

This invokes the pinned `devvit init --force` and official creation wizard.
In an existing app directory this CLI retains custom source, updates app
metadata and installs dependencies. Review those changes; stop if source was
replaced or ownership is unexpected. Do not repeatedly register new apps on
retry. Record the actual registered slug and confirm the CLI account owns it.

## 3. Verify the private destination before any upload or post

Use a dedicated existing private test community, or create one through Reddit
with the user's agreement. Do not treat an automatically generated `_dev`
community, a private app version or an unlisted URL as proof of private
community visibility.

Record these observations before proceeding:

- Community name and ID; Reddit settings explicitly show **Private**.
- Fewer than 200 members; the intended operator has the permissions needed
  to install/manage apps, plus `posts` or `all` for companion publication.
- An approved non-moderator tester can access the private community; an
  unapproved/logged-out visitor cannot read its content. Do not open community
  visibility to test anonymous app access.
- Current post-flair template names and IDs, or an explicitly observed empty
  list. Note any flair requirement. Do not reuse N2N/microdosing flair guesses.
- The exact test community is neither r/NeuronsToNirvana nor r/microdosing.

**Approval stop point:** show the actual destination, registered app identity,
requested app permissions and planned test content before allowing any
CLI/platform-created test post or the companion launcher. For article posts,
obtain approval of the exact saved preview, selected flair and app-account
attribution before pressing Publish. No such approval has been recorded here.

## 4. Upload to the explicit private target, then playtest

Do not start with bare `npm run dev`. Reddit's quickstart says the default
development flow creates a community and test post. The pinned 0.15.0 CLI's
`playtest` first-version path requests automatic community creation even when
a target argument is present. The pinned upload path suppresses that request
when the app is already registered/owned and an explicit development target
is supplied. This is code inspection, not hosted confirmation.

After registration, privacy verification and the approval above, run the
following in **Bash**, replacing the placeholder with the verified name,
without `r/`. The environment value is intentional: in this CLI it takes
precedence over a positional subreddit argument.

```bash
AKN_TEST_SUBREDDIT='REPLACE_WITH_VERIFIED_PRIVATE_COMMUNITY'
case "$(printf '%s' "$AKN_TEST_SUBREDDIT" | tr '[:upper:]' '[:lower:]')" in
  ''|replace_with_verified_private_community|neuronstonirvana|microdosing)
    printf '%s\n' 'STOP: select the verified private test community.'
    exit 1 ;;
esac
[[ "$AKN_TEST_SUBREDDIT" =~ ^[A-Za-z0-9_]+$ ]] || exit 1

# Registered/owned app only; seeds the first private app version.
DEVVIT_SUBREDDIT="$AKN_TEST_SUBREDDIT" npm run deploy
```

Stop if upload offers to initialize another app, announces a different/default
community or reports unexpected ownership. Verify the uploaded app version and
any installation/content side effects before continuing. Private **app-version**
visibility does not establish private **community** visibility.

```bash
DEVVIT_SUBREDDIT="$AKN_TEST_SUBREDDIT" npm run dev -- "$AKN_TEST_SUBREDDIT"
```

This installs/updates the app and watches files. Record the actual playtest URL
and version; verify that they refer to the approved private community. Review
any platform-created post. Then, with approval, open the subreddit menu
**Open AkashicNET Research Companion**. It creates an app launcher if none is
recorded. Opening it again should navigate to the same launcher.

Do not run `npm run launch`, `devvit publish`, or a production-community install.
Ctrl+C ends watching, but the installed version can remain. Inspect the final
state; uninstall only from the verified test community if cleanup is requested.

## 5. Hosted acceptance record

All rows below are **NOT RUN**. Fill each with PASS, FAIL or BLOCKED, timestamp,
app version, observed result and a sanitized evidence reference. Local tests
are supporting implementation evidence, not a replacement for these checks.

| Check | Hosted procedure and expected observation | Result |
| --- | --- | --- |
| Private isolation | Confirm Private in settings; approved reader admitted; unapproved visitor denied | NOT RUN |
| Installation | Developer account, registered slug, exact version and installed private community agree | NOT RUN |
| Moderator permissions | Account with `posts`/`all` sees composer; reader and moderator lacking post permission cannot preview/publish or create launcher | NOT RUN |
| Permission loss | With a disposable tester and owner agreement, remove post permission after preview; publish must fail; restore only authorized permissions | NOT RUN |
| Reader access | Approved non-moderator browses both catalog articles, filters, uncertainty labels, source links and saved discussion; sees no composer/drafts | NOT RUN |
| Current flair | Compare selector names/IDs with live templates; publish chosen flair; changed/deleted template requires a new preview | NOT RUN |
| Exact preview | Preview creates no post; capture title, summary, destination, flair, complete Markdown, source trail and status; edits invalidate it; expiry blocks publication | NOT RUN |
| Publication and attribution | Approve one exact preview, publish once, compare actual post/title/flair/fallback with saved preview; author is the registered app account, not moderator | NOT RUN |
| Duplicate protection | Retry identical content while preview is valid, then prepare identical content again; same receipt/post; second launcher open returns same post | NOT RUN |
| Cross-moderator duplicate | If a second authorized moderator is available, identical snapshot resolves to the existing post; otherwise BLOCKED | NOT RUN |
| Concurrent/uncertain outcomes | Only with a controlled approved harness: concurrent requests create one post; uncertain submission remains locked and is reconciled against actual posts/logs before retry | NOT RUN |
| Snapshot persistence | Reopen the published post/restart session; saved text and source trail remain unchanged | NOT RUN |
| Markdown fallback | Open actual post in old Reddit using an approved reader account; compare full body, escaping, canonical/source links and uncertainty labels | NOT RUN |
| Mobile behavior | On actual Reddit iOS and/or Android clients, record device/app version; test launch, scroll, filters, forms/keyboard, preview, links and return navigation; no clipped controls | NOT RUN |
| Narrow screen/accessibility | Check narrow portrait/landscape, text zoom, keyboard focus and reduced motion; browser emulation alone does not establish native mobile behavior | NOT RUN |

Suggested first article test: BQ001 with a title prefixed `[PRIVATE PLAYTEST]`;
retain its open-question status and source trail. Preview Intention Awareness
separately and retain its untested/no-results status. Publish either only after
review of the actual preview. Do not use personal research accounts or private
observations as test data. Do not change the title merely to bypass a pending
publication claim.

For an ambiguous failure, inspect real posts and Devvit logs before deciding
whether any retry is safe. The existing README describes receipt reconciliation;
do not clear Redis claims automatically or claim failure injection was tested
without an actual hosted harness.

## 6. Record verified results in PR #414

Record: source commit (and any registration diff), Node/npm/CLI versions,
registered slug, test-community visibility, installed version, test case IDs,
sanitized observations and outstanding failures. Keep private-community links,
screenshots and tester identities out of a public PR unless separately approved;
use a restricted evidence record and a sanitized reference when needed. Record
test-post URLs only after they exist and only in the authorized evidence location.

Current blocking dependencies are a functioning authenticated Reddit developer
session/CLI, confirmed app ownership/registration, and a verified private test
community with authorized operator and reader accounts. These cannot be inferred
from a successful build or a green GitHub workflow.

Primary references: [Reddit quickstart](https://developers.reddit.com/docs/quickstart),
[official CLI reference](https://developers.reddit.com/docs/guides/tools/devvit_cli),
and the locked `@devvit/cli@0.15.0` files `dist/commands/init.js`,
`dist/commands/playtest.js`, `dist/commands/upload.js` and `dist/util/project.js`.
