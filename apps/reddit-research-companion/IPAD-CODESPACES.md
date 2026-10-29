# iPad and Codespaces continuation

Checked 28 October 2026 (America/Los_Angeles). Reproduce implementation commit
`9014cb37b67d4e84c7f5a49886106aec78f7daa8` from PR #414. This guide changes no
application code, dependency pins, evidence status or release gates.

**Outcome:** a documented, technically supported route exists without a MacBook.
An iPad can operate the Codespaces terminal; Node runs on GitHub's Linux VM.
The pinned Devvit 0.15.0 CLI implements `login --copy-paste`, so the authorisation
page can run in another Safari tab without a localhost callback or forwarded port.
Actual Codespaces availability, Reddit authentication and hosted behaviour remain
unverified. Do not describe this as a deployed or working hosted app.

## Verified here and still pending

| Item | Result |
| --- | --- |
| Fresh PR inspection | Open, draft, unmerged; head still `9014cb3`; all 14 returned PR-triggered workflows successful |
| Locked checkout in the task's Linux runtime | PASS, Node 24.22.1 and npm 11.9.0 |
| Locked dependency installation | PASS, `npm ci --ignore-scripts --no-audit --no-fund` |
| `npm run check` | PASS, strict TypeScript, 68/68 synthetic tests and production client/server build |
| Metadata index publication guard | PASS, 45 blobs inspected |
| Production dependency audit | Zero reported vulnerabilities; this does not clear the existing tooling advisory |
| Pinned CLI | 0.15.0; help and source confirm `--copy-paste`; no upgrade performed |
| CLI identity | Not currently logged in |
| GitHub cloud-browser access | Ordinary GitHub sign-in page; no authenticated Codespace established |
| iPad/Codespace terminal, quota and outbound Reddit access | NOT RUN / account-dependent |
| Reddit code exchange, app ownership, private community and hosted tests | NOT RUN |

The successful task-runtime checks are **not** Codespaces checks or real Reddit
service tests. The older 20-test baseline in HOSTED-PLAYTEST.md is historical;
the pinned implementation above includes the later metadata and retention work.

## 1. Open the existing PR on your iPad

1. In current Safari, sign into the intended GitHub account and open
   [PR #414](https://github.com/tws9stmcbf-web/AkashicNET/pull/414).
2. Use **Code → Codespaces → +** to open its existing branch
   `codex/devvit-research-companion`. If necessary, use Safari's desktop website
   view to expose those controls. Reuse an existing Codespace only if it is yours
   and its uncommitted work can be preserved.
3. Check the displayed billing owner, remaining quota and any spending controls
   before creating compute. Use a small machine to start. Do not add payment
   details or increase a budget merely to follow this guide.
4. In the VS Code web editor, choose **Terminal → New Terminal** and use Bash.
   A hardware keyboard helps but is not a requirement of the documented route.

Use a real **Codespace**, rather than the `github.dev` editor: the latter has no
compute or integrated terminal. No custom dev container is required for this
first attempt. The pinned repository has no devcontainer configuration; GitHub's
default environment supplies Git, Node, npm and nvm. Its default Node version
must still be checked and selected explicitly.

If the Codespaces control is missing, or GitHub reports exhausted quota, repository
policy or account restrictions, stop there. The remaining dependency is GitHub
Codespaces access, not a missing MacBook. Do not create a template repository.

## 2. Pin and check the existing implementation

Run in the Codespace's repository terminal. Run each block only after the preceding
one succeeds. A failed guarded command closes that terminal; open a new Bash terminal
and fix the stated dependency before continuing. If the working tree is not clean, preserve the work and stop; do not
use reset, clean or force checkout.

```bash
cd "$(git rev-parse --show-toplevel)"
test -z "$(git status --porcelain)" || exit 1
git fetch origin codex/devvit-research-companion || exit 1
git switch --detach 9014cb37b67d4e84c7f5a49886106aec78f7daa8 || exit 1
test "$(git rev-parse HEAD)" = 9014cb37b67d4e84c7f5a49886106aec78f7daa8 || exit 1
```

In the default Codespace Bash terminal, nvm should already be loaded. If `command
-v nvm` fails, open a fresh Bash terminal and, if the environment supplies
`NVM_DIR`, load it with `. "$NVM_DIR/nvm.sh"`. Stop if nvm is still unavailable;
do not substitute an arbitrary download-and-execute installer.

```bash
command -v nvm || exit 1
nvm install 24.22.1 || exit 1
nvm use 24.22.1 || exit 1
npm install --global npm@11.9.0 --ignore-scripts --no-audit --no-fund || exit 1
node --version
npm --version
cd apps/reddit-research-companion || exit 1
npm ci --ignore-scripts --no-audit --no-fund || exit 1
npm run check || exit 1
npm run metadata:git-check || exit 1
./node_modules/.bin/devvit --version
./node_modules/.bin/devvit login --help
git diff --exit-code
```

Expected: Node `v24.22.1`, npm `11.9.0`, CLI `0.15.0`, 68 passing tests and a
successful production build. Node 24.22.1 exceeds the project's and current Reddit
quickstart's minimum of 24.18.0. The nvm install also requires Codespaces network
access to the Node distribution; npm ci requires registry access. Failure there
does not prove an iPad limitation. Save only sanitised error text.

Use the repository's installed CLI. Do not run `npm create devvit`, a new template,
`devvit update app`, `npm install devvit@latest` or `npm audit fix --force`.
The CLI currently advertises 0.15.1; that notification does not authorise changing
the pilot's locked toolchain. In each new terminal, select Node 24.22.1 again.

Optional local publication barrier, before making approved changes:

```bash
git config core.hooksPath .githooks
```

This enables the existing hook in this checkout only. It is not a substitute for
keeping live metadata and secrets out of Git, terminal exports and public logs.

## 3. Authenticate through two Safari tabs

From `apps/reddit-research-companion`, with the selected Node version:

```bash
./node_modules/.bin/devvit whoami
```

If it already identifies the intended developer, do not log out merely to repeat
the test. If unauthenticated:

```bash
umask 077
npm run login -- --copy-paste
```

1. Leave the terminal running. Open the **exact URL printed by the CLI** in a
   second Safari tab. Do not forward localhost port 65010 or expose a Codespace
   port publicly for login.
2. Sign into the intended Reddit account. Inspect the permission request and any
   developer-account setup or terms yourself. The pinned CLI requests broad OAuth
   scope `*`; this is distinct from the app's configured capabilities. Only grant
   access if you intend to authorise the official Devvit CLI.
3. Copy the code Reddit displays and paste it **only into the waiting Codespaces
   terminal**, then press Enter. Never send the code, URL state, token file or
   developer initialisation code to chat, Git, screenshots or PR comments.
4. Verify the account and inspect app inventory without creating anything:

```bash
./node_modules/.bin/devvit whoami
./node_modules/.bin/devvit list apps
```

Success means the intended username is returned. Browser sign-in alone does not
prove the CLI is authenticated, and GitHub sign-in does not authenticate Reddit.
If Reddit requires developer-account enrolment or verified email, complete that
on Reddit before app operations; login success does not prove those gates cleared.

On ordinary Linux Codespaces the CLI stores its credential under `~/.devvit/token`.
Keep the Codespace account-private, do not share terminal access and do not copy
that file into the repository, a Codespaces secret or an environment file as a
workaround. `umask 077` limits newly created file permissions; it does not narrow
Reddit's OAuth grant. No credential values were exposed or recorded in this investigation.

### Pinned CLI refresh caveat

Source inspection found that 0.15.0's `loginViaCopyPaste()` calls
`writeFSToken(token)` without its copy-paste marker. The store serialises the
missing marker as false; later refresh chooses OAuth client headers using that
marker. This suggests that a successful initial login may fail after token expiry.
It is a source-based inference, **not an observed Reddit refresh failure**.

If later commands become unauthenticated, stop any hosted operation, reconcile its
actual result and repeat `npm run login -- --copy-paste` privately, then `whoami`.
Do not edit credential contents or silently upgrade the CLI. A reliable long-lived
session remains an acceptance item. If the code is expired or denied, start a fresh
login, rather than reusing or sharing it. If Reddit blocks the client or network,
stop and report the actual error; do not try to bypass its controls.

## 4. Stop before registration or installation

`akashicnet-research` in devvit.json is provisional. Listing apps does not establish
that this slug exists, is owned by the intended account or belongs to this pilot.
Confirm those facts in the developer dashboard.

If no suitable owned registration exists, the next dependency is explicit approval
for the actual app identity and registration. The existing `npm run register`
executes **`devvit init --force`**, not a harmless status check. It can alter metadata
and install dependencies. Do not run it as part of this baseline or generate a second
starter. After an approved registration, preserve the custom src tree, inspect
`git diff -- devvit.json package.json package-lock.json src`, record the slug and
rerun `npm run check`. Stop on unexpected source or dependency changes.

Before a hosted test, verify and record privately:

- An existing, explicitly **Private** community with fewer than 200 members.
- The actual community name and ID, intended operator's full/Everything app-management
  permissions and `posts`/`all` for the companion composer. The installed app account
  may itself receive broad moderator powers; review the real installation request.
- Approved-reader access and denied access for an unapproved/logged-out reader.
- Live flair template names/IDs or a genuinely empty list.
- The destination is neither r/NeuronsToNirvana nor r/microdosing.
- Approval for the exact app, destination, permissions and any platform-created test
  content or companion launcher. Article publication additionally needs approval of
  the actual frozen preview, flair and app-account attribution.

No private test community or post has been approved or verified here. Creating a
community is a separate action. Private app visibility does not establish private
community visibility. Do not enable public access for testing.

## 5. Conditional hosted commands — NOT RUN

Use only after section 4 is satisfied. Keep the commands separate so the uploaded
version can be inspected before installation. The lower-case allow/deny checks
below reject both protected communities and the placeholder; they cannot establish
privacy, permission or approval.

In the same Bash terminal, from the app directory:

```bash
AKN_TEST_SUBREDDIT='REPLACE_WITH_VERIFIED_PRIVATE_COMMUNITY'
case "${AKN_TEST_SUBREDDIT,,}" in
  ''|replace_with_verified_private_community|neuronstonirvana|microdosing)
    printf '%s\n' 'STOP: select the verified private test community.'
    exit 1 ;;
esac
[[ "$AKN_TEST_SUBREDDIT" =~ ^[A-Za-z0-9_]+$ ]] || exit 1
./node_modules/.bin/devvit whoami || exit 1
DEVVIT_SUBREDDIT="$AKN_TEST_SUBREDDIT" npm run deploy
```

For an already registered/owned app and explicit target, source inspection shows
0.15.0's upload path requests a private version with automatic community creation
disabled. **If ownership is absent, upload can enter app creation and request a new
community anyway.** This is not an account-verified or hosted guarantee. Stop if
initialisation, a different target or automatic community creation is offered.
Inspect actual version, ownership and side effects before proceeding.

```bash
DEVVIT_SUBREDDIT="$AKN_TEST_SUBREDDIT" npm run dev -- "$AKN_TEST_SUBREDDIT"
```

The environment value intentionally overrides other defaults. Do not use bare
`npm run dev`: the pinned first-version playtest path requests community creation
even when a target was supplied. Seeding and verifying the private version first
avoids that code path, according to source inspection. The hosted result is untested.

Open only the URL returned by the CLI and verify the actual private destination.
The moderator menu **Open AkashicNET Research Companion** can create a launcher;
it is a write action, not merely navigation. Do not select it without the approval
above. Do not run `npm run launch`, `devvit publish` or a production-community install.

## 6. Acceptance, metadata and shutdown

Use every row of the [existing hosted acceptance matrix](HOSTED-PLAYTEST.md#5-hosted-acceptance-record).
Record PASS, FAIL or BLOCKED with source SHA, actual app/version, time, device/client
version and sanitised evidence. All hosted rows currently remain **NOT RUN**.

First confirm private isolation, account/role boundaries, current flair and reader
access. Then, only with a reviewed preview and authorisation, test one
`[PRIVATE PLAYTEST]` article, exact frozen output, app-account attribution, duplicate
and uncertain-response handling, persistence and old-Reddit fallback. Keep BQ001
unresolved and Intention Awareness untested. Check portrait/landscape and iPad text
size, keyboard, copy, pause/resume and links in the actual Reddit iOS client;
Safari success is not native-app verification. Mark Android and second-moderator
checks BLOCKED if those clients/accounts are unavailable.

The private metadata control **Check this test post** is bounded to the current
companion post. The N2N queue must remain refused. Use only approved, non-sensitive
test content. Do not copy, download or retain live private packets outside the
open view in this first test; do not put them in the curation queue or claim iPad
packet export was tested. Separate export testing requires an approved lifecycle.

RETENTION.md still applies: all supplied captures are UNVERIFIED_OPERATOR_EXPORT,
public eligibility HOLD and evidence/rights promotion OFF. The offline 24-hour
sweeper runs only when invoked. Codespaces auto-stop does not provide continuous
TTL/deletion monitoring, authenticated capture integrity, encrypted/RBAC external
storage, request intake or downstream/backup purging. No live-data integration gate
is cleared by login, build or private playtest.

To finish, press **Ctrl+C** in the terminal (with an on-screen-only keyboard, use
the terminal's context menu/Command Palette to send the interrupt or kill that
terminal). Watching stops, but Reddit's installed version and posts can remain.
Inspect their actual state; cleanup must target only the verified private community.
Run `./node_modules/.bin/devvit logout` when finished with the credential, then stop
the Codespace using its management menu. Closing Safari alone need not stop compute;
stopped Codespaces still consume storage. Preserve only approved source changes and
sanitised results before any later deletion.

## Primary references

- [GitHub explicitly supports iPad Codespaces](https://github.com/features/codespaces)
- [Opening a PR in Codespaces](https://docs.github.com/en/codespaces/developing-in-a-codespace/using-github-codespaces-for-pull-requests)
- [Default Node environment and nvm](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-nodejs-project-for-codespaces)
- [Codespaces billing and included usage](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces)
- [github.dev and Codespaces differences](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor)
- [nvm usage](https://github.com/nvm-sh/nvm#usage)
- [Reddit quickstart and Node minimum](https://developers.reddit.com/docs/quickstart)
- [CLI login, upload, playtest and identity commands](https://developers.reddit.com/docs/guides/tools/devvit_cli)
- [Reddit playtest side effects and persistence](https://developers.reddit.com/docs/guides/tools/playtest)
- [FAQ: backend testing and credential storage](https://developers.reddit.com/docs/guides/faq)
- [Moderator app permissions](https://developers.reddit.com/docs/guides/best-practices/mod_resources)
- Local pinned source: `node_modules/@devvit/cli/dist/commands/{login,upload,playtest}.js`,
  `dist/util/{auth,project}.js`, `dist/lib/auth/{NodeFSAuthenticationPlugin,AuthTokenStore}.js`
  and `dist/lib/http/oauth.js`.
