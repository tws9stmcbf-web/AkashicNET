# Pilot data handling

The app runs on Reddit's Devvit infrastructure. It has no external HTTP permission
or external analytics integration. Reddit's own infrastructure and developer tooling
remain governed by Reddit's terms and privacy notices.

| Data | Purpose | App retention |
| --- | --- | --- |
| Current Reddit user ID and username | Verify moderator identity and `posts`/`all` permission | Used during the request; the username is not persisted by app code |
| Moderator's user ID, source-post ID, destination, draft and preview ID | Bind a reviewed preview to its owner and installation | One replaceable draft per moderator/source post, with a ten-minute Redis expiry |
| Published title, summary, source URLs, claim labels, research status and boundary | Preserve the exact public discussion snapshot | Stored in installation-scoped Redis for the lifetime of the publication/installation |
| Content digest, publication state, Reddit post ID and public URL | Prevent duplicate posts and reconcile uncertain outcomes | Persistent in the installation; contains no moderator identity |
| Launcher post ID and public URL | Reopen one companion per installation | Persistent in the installation |

Reader browsing does not create an app-stored history, profile or draft. Request
responses are marked `Cache-Control: no-store`. The app does not log draft content,
usernames, user IDs, secrets or stack traces. Platform logs may still record request
metadata independently of this code.

Only public, reviewed-for-publication prose belongs in the composer. Do not enter
private correspondence, personal case records, medical details, credentials or
restricted corpus material. Submitted discussion snapshots are public community
content and include a link to their canonical article.

This pilot has no public data-export, deletion or claim-reset endpoint. Normal
Reddit post controls apply to published posts. Operator reconciliation of saved
snapshots/receipts must preserve duplicate protection and the repository's existing
public/private boundary. Uninstalling the app is not claimed here to delete Redis
data; verify Reddit's current platform retention behavior before making that promise.
# Metadata capture addition · 24 October 2026

The optional moderator metadata scanner reads known post IDs only after an
explicit action. It returns dated title, flair, creation date, submitted-link
and engagement snapshots to the open app view. It does not capture post
bodies, comments, author identities or user flair. Removed, deleted, mature,
quarantined, wrong-community and unavailable responses have no content payload.

Captured packets remain in the open view's memory until explicitly copied;
closing or reloading loses unsaved packets. The scanner stores no captured
post content on its server, logs none of the returned content, and uses only
a short-lived installation-wide cooldown marker in Redis. No external service
receives packets automatically. External reuse requires a separate reviewed
deletion, refresh and provenance workflow. See METADATA-SCAN.md.


## Offline retention safeguards · 24 October 2026

The synthetic-only continuation in [RETENTION.md](RETENTION.md) adds a private
local reconciler, 24-hour expiry checks, removal/suppression, dependent-projection
purging, persistent replay blocking and Git publication barriers. It never
authenticates packets or makes them publicly eligible. A private suppression
token only prevents re-import; it is not anonymous data or retained deleted
content. Its necessity and duration require operating-policy review. No TTL
scheduler, removal inbox, encryption service or hosted deletion propagation is
deployed. Real copied metadata remains blocked from external storage and
incorporation until those dependencies and approvals are satisfied. Earlier
public-discussion snapshot/receipt retention needs its own review; this patch
does not certify that separate workflow.
