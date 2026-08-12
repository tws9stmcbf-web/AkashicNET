# N2N Ingestion Architecture

## Purpose

This document defines a lawful, provenance-first ingestion pipeline for publicly available material from r/NeuronsToNirvana that may be relevant to the Noetic Sciences Toolkit.

The design follows four constraints:

- The canonical source remains Reddit.
- The Toolkit stores structured metadata and permitted excerpts, not a blind copy of Reddit pages.
- Community content remains a community archive, not scientific evidence.
- All ingestion is subject to Reddit's current API and developer platform requirements, rate limits, and legal terms.

## Scope and non-goals

### In scope

- Public posts from r/NeuronsToNirvana
- Public metadata: Reddit post ID, title, URL, author handle, creation date, subreddit, permalink, and related flags
- Permitted content fields only: title, short summary, extracted selftext, links, media metadata, and tags that are explicitly public and intended for archival use
- Classification into categories such as research, consciousness, philosophy, psychedelics, wisdom, lived experience, frameworks, art, music, humour, stories, nature, community, and speculation
- Provenance and rights status for each record
- GitHub-backed archival storage using structured records and stable identifiers

### Out of scope

- Indiscriminate scraping of Reddit pages or comment trees
- Bulk harvesting without review or rate-limit controls
- Copying copyrighted text, images, videos, or memes at scale
- Treating community discourse as scientific evidence
- Any phase that begins a large-scale extraction before the legal and provenance design is approved

## Architecture principles

1. Canonical source first
   - Every imported record must retain the original Reddit URL and post ID as the authoritative source reference.
   - The archive should link out; it should not attempt to replace the original publication.

2. Minimal extraction
   - Prefer metadata and short summaries over full-page or full-body copying.
   - Extract only what is necessary for classification, provenance, and future discovery.

3. Evidence separation
   - Community records are labelled by evidence status and provenance status, never promoted to scientific evidence status by default.

4. Traceable provenance
   - Every record must capture when it was ingested, what fields were captured, and whether the original source later changed, was removed, or was deleted.

5. Reversible governance
   - If a post is deleted, edited, removed, or later restricted, the archive must preserve the historical state while flagging the current status.

## Current permitted Reddit access model

The toolkit should rely on Reddit's official developer platform and API access only. It must not use unofficial scraping or headless browser techniques to circumvent rate limits or TOS restrictions.

### API / developer platform requirements

At the time of design, Reddit access is governed by Reddit's Developer Platform and API rules. A compliant implementation should:

- Create or use a Reddit API app registration with an app name, redirect URI, and platform type appropriate to the operating model
- Use a respectful User-Agent header that identifies the project and the purpose of the request
- Use OAuth when required by the endpoint or by Reddit policy for higher-privilege access
- Prefer documented public endpoints and avoid any endpoint or method that is not explicitly permitted for public content access
- Maintain separate credentials for ingestion jobs, with no shared secrets embedded in repository files

Operationally, this means the ingestion workflow should be implemented as a controlled script or service run with a dedicated Reddit app identity and a project-specific user agent, rather than as anonymous bulk scraping from arbitrary websites.

### Rate limits and throttling

Reddit enforces rate limiting on API calls and may reject or throttle requests that exceed documented quotas. The ingestion system should assume all limits are strict and must be treated as hard ceilings, not soft guidelines.

Required controls:

- Respect `X-Ratelimit-*` headers when present
- Use exponential backoff on 429 and transient server errors
- Prefer scheduled, low-volume ingestion rather than bursts
- Queue requests by post or subreddit, not by page scraping loops
- Separate one-off reviews from bulk ingestion jobs
- Record failed requests and retry state in the archive metadata

A conservative implementation should use a queue-based job system with a fixed request budget per hour and a default backoff of 1x to 5x on rate-limit responses. The system should never assume it can fetch vast portions of a subreddit without throttling.

### Permitted data usage

Permitted use is limited to public Reddit metadata and content that is lawful to ingest under Reddit's terms and the Toolkit's own provenance rules.

This design permits:

- Public post metadata (ID, title, URL, author, subreddit, created time, score, flair if public, and associated permalink)
- Public body text only when it is necessary to classify or summarise the record and when its use is consistent with platform rules
- Public external links and embedded media metadata if they are included in the public post and lawful to archive
- Historical snapshots of public content when intentionally retained as a provenance-preserving record

This design does not permit:

- Copying full Reddit pages, comment threads, or media files wholesale
- Storing private or restricted content
- Reproducing copyrighted images, memes, videos, or large textual passages without a clear rights basis and a human review decision
- Using a Reddit dataset as an unreviewed scientific corpus

### Attribution requirements

Every imported record must carry attribution to the original Reddit post and author where appropriate. A compliant archive entry should preserve at least:

- Reddit post ID
- canonical Reddit URL
- subreddit name
- title
- original author handle when publicly shown and not removed by the author
- creation date
- retrieval date
- provenance status

The archive should clearly state that the source is Reddit and that the Toolkit is preserving a link-based record rather than reproducing the original content at scale.

### Deletion and update handling

Reddit content is dynamic: posts can be edited, deleted, removed by moderators, or made inaccessible after initial retrieval.

The ingestion pipeline must therefore keep a structured lifecycle. Each record should include a state machine such as:

- `active`
- `edited`
- `deleted`
- `removed`
- `rate_limited`
- `invalid_url`
- `rejected_by_policy`

Behavior rules:

- Preserve the original canonical Reddit URL even if the post is later deleted.
- Keep a historical snapshot of the retrieved metadata and any allowed extracted fields.
- Do not silently overwrite the canonical record when the source changes.
- Create a new event or update record rather than deleting the historical provenance trail.
- Mark the post as `deleted` or `removed` and preserve the old record for auditability.

This is essential because the archive is meant to maintain provenance across time, not just a current state snapshot.

### Copyright and rights considerations

The Toolkit must not treat Reddit as a free-for-reuse public domain source for text, images, or media. The safest default is a link-first archival model.

Required rights controls:

- Store canonical URLs rather than copying full pages
- Prefer metadata fields and short summaries over long text copies
- Do not archive images, videos, or user-generated media unless the workflow has a documented rights basis and review decision
- Do not use Reddit text as if it were a scientific publication or primary evidence source
- Add a `provenance_status` field that records whether the imported content is link-only, metadata-only, or contains a permitted excerpt
- If a short excerpt is stored, keep it minimal and clearly labelled as an excerpt from a public Reddit post, not as an original or derived work

In practice, the project should assume that the safest lawful default is: link to Reddit + store metadata + store a short summary, all while avoiding reproduction of copyrighted media and large bodies of text.

## Required record model

Each ingested record must include the following core fields:

- reddit_post_id
- title
- reddit_url
- subreddit
- author
- author_attribution_status
- date_created_utc
- date_ingested_utc
- source_type
- category
- evidence_status
- lived_experience_flag
- external_links
- toolkit_frameworks
- short_summary
- provenance_status
- licensing_status
- source_state

The repository's existing schema already reflects a comparable pattern, including fields such as title, reddit_url, author, source_type, category, evidence_status, toolkit_framework, and provenance_status.

### Classification support

The classification taxonomy must support the project's community archive categories:

- research
- consciousness
- philosophy
- psychedelics
- wisdom
- lived experience
- frameworks
- art
- music
- humour
- stories
- nature
- community
- speculation

A record may also carry more than one signal, but it should have a primary category for archive navigation and a separate set of supporting tags.

## Data flow design

The canonical ingestion flow is:

Reddit post
→ source URL
→ metadata
→ permitted content extraction
→ classification
→ provenance
→ GitHub archive

### Step 1: Candidate discovery

The system should not blindly crawl the entire subreddit. It should work from a controlled intake list such as:

- manually selected Reddit URLs
- approved subreddit search workflows
- known thematic seed posts identified by project maintainers
- curated lists of high-value posts for specific topics

This ensures the project remains provenance-first, reviewable, and narrow in scope.

### Step 2: Reddit API retrieval

Each candidate URL is resolved to a canonical Reddit post ID. The system then requests only the required public data from the official API and preserves the original permalink.

Fetches should include:

- post metadata
- title
- author
- created_utc
- subreddit
- permalink
- url
- selftext
- media metadata if present
- flair or tags if public

The system should reject or quarantine requests that would require private data, account-mediated access, or scraping outside the permitted API surface.

### Step 3: Permitted content extraction

Only approved fields are extracted and stored. A safe default is:

- title
- post URL
- public author name if available
- date
- short summary created by a human reviewer
- external links present in the post body or comments when relevant and safe to archive
- permitted textual snippet only when necessary and reviewed

Large blocks of final body text should be excluded unless there is a specific, review-approved reason to store them. This is deliberately conservative.

### Step 4: Classification and tagging

The ingest pipeline assigns:

- primary category
- source type
- evidence status
- lived experience flag
- Toolkit framework relevance
- tags for search and retrieval

This stage should be deterministic when possible and require human review for ambiguity. The project must not infer scientific support from a community post merely because it is archived.

### Step 5: Provenance and licensing state

For every record, the system records:

- source type: discussion, personal_experience, framework_discussion, art_discussion, music_thread, etc.
- provenance status: link-only, metadata-only, excerpted, external link preserved, removed, deleted, or edited
- licensing status: rights unknown, link-only archive, public metadata, short excerpt under review, or no reproduction

This is essential for later legal review and for preventing accidental rights violations.

### Step 6: GitHub archive publication

A normal archive record should be stored in a GitHub-friendly structured form such as:

- a machine-readable CSV or JSONL dataset
- a corresponding markdown index for human navigation
- a provenance record containing the ingest time, retrieval state, and source metadata

The GitHub repository remains the archival layer; the canonical source is still Reddit. The repository should not be overloaded with large copied media files or full page dumps.

## Storage model

The project should maintain a separate community archive structure such as:

- `references/community/` for curated record store and design documents
- `references/community/archive/` for JSON or CSV datasets
- `references/community/provenance/` for ingest event and rights records
- `references/community/indexes/` for human-readable index files

This preserves a clean separation between raw ingest state and curated repository output.

## Enforcement and review controls

### Legal and policy checks

Every ingestion job should perform these checks before persisting a record:

- Is the source public and accessible without private or restricted credentials?
- Is the request using Reddit's documented API surface?
- Did the request respect rate limits and user-agent requirements?
- Is the extracted content minimal, necessary, and lawful to retain?
- Is the source URL retained in full?
- Is the author attribution and provenance state recorded?
- Is the record labelled as community material, not scientific evidence?

### Human review gate

Any record involving:

- a potentially sensitive topic
- a contentious claim
- a copyrighted image or video
- ambiguous provenance
- potentially identifying personal information

must be reviewed by a maintainer before archival publication. The archive should never quietly ingest high-risk content without a human decision.

## Operational safeguards

The pipeline must include:

- idempotent intake to avoid duplicate records by Reddit post ID
- canonical primary key based on `reddit_post_id`
- rate-limit backoff and job retries
- explicit `source_state` tracking
- a record quarantine bucket for removed or risky posts
- separate curatorial review before publication to GitHub

## Phase gating

This architecture is intentionally the design phase only. It does not begin a 1,000-post extraction run, does not assume bulk harvesting, and does not mark Phase 3 complete.

The next permitted phase after design review would be a constrained pilot intake of a small, curated set of public Reddit posts, with explicit approval, provenance review, and legal audit.

## Summary

The lawful and sustainable design is straightforward:

- use Reddit's official developer API and app model
- respect rate limits and TOS boundaries
- archive only minimal public metadata and permitted content
- preserve canonical Reddit URLs and post IDs at all times
- classify material without elevating it to scientific evidence
- track edits, deletions, and rights status as part of provenance
- store the output as a structured GitHub archive, not a blind copy of Reddit pages

This gives the Noetic Sciences Toolkit a repository-safe, provenance-first N2N ingestion method that remains consistent with the project's evidence boundaries and rights concerns.
