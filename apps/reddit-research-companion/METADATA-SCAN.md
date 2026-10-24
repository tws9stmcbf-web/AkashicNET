# N2N metadata capture and source citations

Prepared 24 October 2026, America/Los_Angeles. **Live lookup: NOT RUN.**
The existing authentication and private-playtest requirements still apply.

## Saved archive preparation completed

The offline preflight validated all **7,463** known IDs, with no duplicates,
wrong-community URLs or ID/permalink mismatches. These are the complete saved
IDs, not proof of every post ever published on N2N. The original export has
3 curated titles, 22 previously observed titles and 7,438 uncaptured titles.
237 records have website citations; the remaining 7,226 are discovery links.

Inputs and fingerprints are in `docs/n2n-metadata-preflight-2026-10-24.json`.
The input export SHA-256 is
`0104e285d8bacfa5dc898932beef892b6b4326d8dc40172576ecdd7741d6f121`.
The sorted-ID fingerprint is
`b2967e5e262c5eaf81564f7514fcc90a4f5b71e234b9c77651d471bf9fae6a1e`.

Reproduce from an authorised local copy of the existing public export:

```sh
node tools/prepare-n2n-scan.mjs /absolute/path/to/n2n-metadata-curation-2026-10-22.json
```

This command makes no network requests. It generates the server-only ID
manifest, preflight report and source-citation register. The register is
published through the website source repository, rather than duplicating the
large generated file in this app's GitHub patch. Each row preserves a source
URL, canonical permalink, archive fingerprint, citation role and explicit
`live_checked_this_run: false` / `appraisal_added_this_run: false` flags.

## Capture after authenticated private testing

Open the companion as a moderator with post permissions. The metadata panel
does nothing until the operator inspects the queue and explicitly starts it.

- In a private test installation, **Check this test post** reads only the
  current companion post. The N2N queue is denied before any read.
- In an approved N2N installation, **Capture next 5** performs one batch.
  **Start / resume known-ID scan** continues while the view remains open,
  waiting at least 31 seconds between completed batches.
- **Pause after current request** stops continuation. No scheduler, install
  trigger, external fetch, new Reddit post or automatic website write occurs.
- Save the JSON packets and their `next_cursor` before closing or reloading.
  Packets are held only in the open view's memory. On another session, enter
  the saved cursor and retain earlier packets separately. This is a cursor
  continuation, not durable server-side result storage or unattended scanning.

The server binds the queue to the installation and checks actual moderator
permissions on every batch. The caller cannot supply post IDs, alternate
communities, lookup URLs or a replacement manifest. An installation-wide
30-second cooldown limits competing moderators as well as one browser tab.
This conservative batch rate is a pilot setting, not a measured Reddit quota.
Hosted throughput, timeouts and native mobile copy behaviour are unverified.

## Metadata and unresolved outcomes

Each record carries a post ID, observation timestamp and lookup status.
Eligible responses include a title, flair, creation time, canonical permalink,
submitted URL, SDK-returned score snapshot and comment-count snapshot. Missing
fields stay null. SDK zero defaults may mean unavailable values; neither
score nor comment counts are exact or permanent measurements.

No post bodies, comments, images, account identities or user flair are read
into the capture. Removed, spam, deleted, mature or quarantined responses
have no metadata payload. Wrong-ID and wrong-community responses are also
contentless. HTTP 403/404/410 mean unavailable, not proof of deletion.
Unrecognised errors and throttling stop at the same cursor for a later retry.

Only a short-lived cooldown marker is stored in app Redis. Captured metadata
is returned to the moderator's open view and is not logged or retained by
this scanner on the server. No HTTP-fetch domains are requested.

## Integration boundary

Every packet is `public_merge_status: REVIEW_REQUIRED`. Capturing a title
does not appraise the linked paper, confirm a claim or establish reuse rights.
Historical annotations and existing website labels must remain separate
from new Reddit-observed fields. Never reconstruct a title from a URL slug.

Before storing copied packets externally, implement deletion propagation,
refresh/expiry, access controls and provenance checks. A permanent public Git
archive of captured post content cannot honour deletion by merely removing
the latest version. Do not add these packets directly to public Git history.
The source-citation register contains contextual IDs and archive citations;
it is not a live-content export or a scientific bibliography.

Primary references: [Reddit client](https://developers.reddit.com/docs/api/redditapi/RedditClient/classes/RedditClient),
[API overview](https://developers.reddit.com/docs/capabilities/server/reddit-api),
[Devvit privacy and deletion rules](https://developers.reddit.com/docs/devvit_rules).

## Hosted acceptance additions — all NOT RUN

1. A non-moderator and a moderator lacking post permissions cannot inspect
   or call either metadata endpoint.
2. The private installation cannot start the N2N queue; its one-post capture
   matches the actual private source post and copies correctly on iPad.
3. After separate approval and installation, N2N batches match live titles,
   flair, creation dates and submitted links. No body or author is exported.
4. Competing requests obey cooldown; transient failure preserves the cursor;
   pause, refresh and manual cursor continuation do not claim missing packets.
5. Capture and inspect unavailable, removed, deleted and wrong-community
   outcomes without exporting their content. Verify external deletion and
   refresh handling before any content integration is enabled.
