# N2N Ingestion Architecture

## Purpose

This document defines a lawful, provenance-first ingestion pipeline for publicly available material from r/NeuronsToNirvana that may be included in the Noetic Sciences Toolkit.

The design follows the project's existing archive standards:

- The canonical source remains Reddit.
- The archive stores structured metadata and links, not a Reddit mirror.
- Community records are not scientific evidence by default.
- The workflow is intentionally limited to documented, permitted public-access patterns.
- No large-scale extraction begins before the design and review process is approved.

## Scope and non-goals

### In scope

- Public posts from r/NeuronsToNirvana
- Public metadata such as Reddit post ID, title, URL, author, subreddit, creation date, and permalink
- Permitted short-form content extraction such as summaries or minimal excerpts reviewed by maintainers
- Classification into archive categories and evidence categories
- Provenance, attribution, and rights tracking
- GitHub-backed structured storage for future archival use

### Out of scope

- Indiscriminate scraping of Reddit pages or comment trees
- Bulk harvesting without review and rate-limit controls
- Copying copyrighted text, images, audio, video, or memes at scale
- Treating community discourse as scientific evidence
- A public mirror of Reddit content
- Any extraction phase beyond a curated, reviewed pilot

## Canonical-source model

The archive is not a mirror of Reddit. It is a provenance-first catalogue that stores:

- the canonical Reddit URL
- the Reddit post ID
- public metadata
- a short summary or human-written description
- classification labels
- provenance/licensing status
- related external links

The canonical source remains the original Reddit post at all times. Reddit is the source of record; GitHub is the archive layer.

## Consistency check against the existing N2N archive schema

The repository already defines a practical schema for the community archive, including the following fields:

- title
- reddit_url
- author
- attribution_note
- date
- source_type
- category
- short_summary
- external_source_url
- toolkit_framework
- research_question_potential
- visual_audio_art_flag
- evidence_status
- provenance_status

This ingestion design is consistent with that schema and adds pipeline-specific fields that are not intended to replace it. The workflow should produce records that can be ingested directly into the existing archive structure without schema drift.

Recommended ingestion-to-archive mapping:

- reddit_post_id -> stored as part of the canonical URL or derived archival ID
- title -> title
- reddit_url -> reddit_url
- author -> author
- author attribution / public credit -> attribution_note
- created_utc -> date
- source_type -> source_type
- category -> category
- short summary -> short_summary
- external links -> external_source_url and related links
- toolkit relevance -> toolkit_framework
- research question -> research_question_potential
- visual/audio/art -> visual_audio_art_flag
- evidence class -> evidence_status
- provenance/licensing -> provenance_status

## Reddit access model

The pipeline must use Reddit's official Developer Platform and documented API access only. It must not rely on unofficial scraping, browser automation, or hidden endpoints meant to circumvent the platform's rules.

### API and developer platform requirements

A compliant implementation should:

- register a Reddit app or use a documented public API workflow appropriate to the deployment model
- use a clear, project-specific User-Agent string that identifies the Toolkit and its purpose
- use OAuth when required by the access pattern or platform policy
- prefer official endpoints and documented public data access methods
- keep credentials out of the repository and out of shared logs
- separate staging and production access keys

### Operational constraints

The workflow should assume that Reddit API usage is rate-limited and subject to policy changes. The implementation must be designed conservatively:

- use low-volume, scheduled jobs instead of bursts
- respect rate-limit headers when present
- use backoff and retry logic for 429 and transient failures
- avoid any large-scale subreddit crawl without explicit review
- maintain a queue of pending URLs and a record of prior attempts

## Rate limits and enforcement

Reddit rate limits may change over time and often vary by endpoint and access context. The ingestion system should treat any rate-limit value as a hard ceiling, not a target to hit.

Operational safeguards:

- fixed request budget per hour per job
- exponential backoff on rate-limit responses
- deduplication before each fetch
- per-source provenance tracking for retries
- quarantine for rejected or restricted posts

## Permitted data usage

The pipeline may ingest only data that is public and permitted under Reddit's terms and the Toolkit's archival rules.

Allowed:

- public post metadata
- public author handles when visible and appropriate
- public post URLs and permalinks
- public links in the post body
- public media metadata when relevant and lawful to preserve
- brief summaries written by a human reviewer
- minimal excerpts only when explicitly approved and necessary for provenance or research context

Disallowed:

- wholesale copying of Reddit pages
- scraping comment trees indiscriminately
- storing private or restricted content
- copying images, video, or audio without review and rights clearance
- copying large text blocks without a specific legal and editorial review decision
- using a Reddit archive as a substitute for scientific evidence

## Attribution and author handling

Every record must preserve attribution in a way that is accurate, respectful, and easy to audit.

Required provenance fields:

- Reddit post ID
- canonical Reddit URL
- subreddit name
- title
- original author handle when publicly visible
- creation date
- retrieval date
- attribution_note
- provenance_status

Rules:

- Prefer public author attribution over inferred authorship.
- Never invent an author.
- Do not extract or store private or identifying information beyond what is publicly necessary and approved.
- If author identity is unavailable or restricted, record that fact explicitly rather than guessing.

## Copyright and content ownership

The repository should operate under a link-first model and a minimal-extraction model. The archive should not treat Reddit content as a public-domain or unrestricted content source.

Copyright-safe design rules:

- store the canonical URL and not a full page copy
- prefer metadata and summaries over full-body copies
- do not archive images, video, or audio without a documented review decision
- never reproduce a Reddit meme, screenshot, or large post body without explicit clearance
- include a `provenance_status` label that captures whether the record is link-only, metadata-only, or excerpted
- keep source text and media separated from research and archive logic

## Deleted, edited, and removed posts

Reddit posts are not stable over time. A proper archive must treat changes as first-class provenance events.

Required lifecycle states:

- active
- edited
- deleted
- removed_by_moderator
- rate_limited
- invalid_url
- rejected_by_policy
- inaccessible

Behavior:

- preserve the original URL and post ID even if the post is later removed
- record the retrieval timestamp and any later status changes
- keep the original record as a historical artifact instead of overwriting it silently
- create change events rather than deleting provenance history
- flag the current status separately from the original source record

## Duplicate detection

The archive must avoid duplicate ingestion by repeated post IDs and near-duplicate titles.

Canonical deduplication keys:

- Reddit post ID
- canonical Reddit URL
- normalized title + creation timestamp

Operational rules:

- do not ingest the same post ID more than once
- quarantine near-duplicate posts for review instead of auto-merging them
- preserve a unique record ID for each accepted item
- detect duplicates before classification and before publication to GitHub

## Evidence classification

Community material should be classified by evidence status and not by scientific value.

Existing repository categories are consistent with the archive's evidence boundary:

- community_observation
- lived_experience
- creative_cultural_material
- speculation
- scientific_evidence (explicitly avoided for this archive)

Rules:

- community discussions and reflective commentary are usually `community_observation`
- first-person testimony is `lived_experience`
- music, art, humour, storytelling, and cultural material are usually `creative_cultural_material`
- frameworks, speculative systems, and future-facing models are often `speculation`
- scientific evidence is not used as a default label for Reddit posts

## Lived-experience classification

The pipeline should support an explicit lived-experience flag to separate personal accounts from general discussion.

Recommended model:

- lived_experience_flag: yes/no/unknown
- evidence_status: lived_experience when the record contains first-person report or experiential testimony

This is especially important for posts describing altered states, sensory changes, shifts in selfhood, or personal integration narratives.

The archive must avoid turning such material into clinical or causal evidence. It is evidence-relevant only as lived testimony, not as scientific proof.

## Source provenance and audit trail

Every ingestion task should leave an auditable record.

Minimum audit fields:

- source_url
- reddit_post_id
- source_status
- ingestion_timestamp
- retrieval_method
- api_endpoint_or_documented_source
- rate_limit_state
- duplicate_check_result
- classification_result
- human_review_required
- final_record_status

This ensures each imported record has a traceable path from Reddit to GitHub without relying on memory or undocumented assumptions.

## External source links and related references

The pipeline should preserve external URLs when they are embedded in the source post and are relevant to the archive.

Rules:

- keep the canonical Reddit source link as primary
- record any relevant external links separately from the canonical source
- do not broaden the archive into a general web crawl
- do not treat external links as evidence unless separately reviewed

The existing schema already supports `external_source_url` and `toolkit_framework`, which should be used for relevant external links and framework associations without overclaiming.

## Images, audio, and video handling

The archive should treat media as secondary evidence and should not mirror Reddit media files by default.

Policy:

- preserve only the URL to the media or a documented reference if it is public and relevant
- record a flag such as `visual_audio_art_flag` when the content is media-related
- avoid copying or storing images, audio, or video files unless explicitly approved
- if a post contains art, music, or visual symbolism, classify it as `creative_cultural_material` rather than treating it as scientific material

This matches the existing archive model, where `visual_audio_art_flag` is already used as a structured indicator.

## Error handling

The pipeline should explicitly handle failure cases rather than silently skipping them.

Common errors:

- 429 rate limit
- 401 or 403 access error
- deleted or inaccessible post
- bad URL or malformed permalink
- payload changes or missing fields
- API schema mismatch
- rejected content due to legal or policy concerns

Handling model:

- log each failure with the source URL and error code
- quarantine the record rather than discarding it silently
- retry with backoff only when the failure is transient
- mark policy rejects and inaccessible posts with explicit status codes

## Validation

Before a record is accepted into the GitHub archive, it should be validated against the schema and project rules.

Validation checks:

- title present
- reddit_url present and valid
- author present or explicitly marked as unavailable
- category valid and from the approved taxonomy
- source_type valid
- evidence_status valid
- provenance_status present
- short_summary present or flagged as missing
- toolkit_framework used only when relevant
- duplicate detection passes
- no private or identifying data is stored without approval

The system should reject or quarantine records that fail required validations rather than publishing incomplete or ambiguous entries.

## Incremental update strategy

The design should support the eventual 6,000-record target without forcing a one-time bulk extraction.

Recommended process:

- maintain a curated intake queue
- ingest in reviewed batches
- update a status log after each accepted batch
- revalidate counts and schema after each batch
- preserve change history for deleted or edited posts
- keep a clear distinction between pending, approved, and archived records

This ensures the archive can scale from a pilot to a broad community catalogue without drifting into a live mirror or a low-quality bulk scrape.

## GitHub archive model

The repository should store the archive in structured form rather than as scraped web pages.

Expected outputs:

- a CSV or JSONL archive for machine-readable records
- a markdown index for maintainers and readers
- a provenance/status file documenting scope and record counts
- a change log or audit log for updates and lifecycle transitions

The archive should remain lightweight and human-readable while staying consistent with the repository's current N2N archive schema.

## Governance and review

For each batch or intake cycle, maintainers should review:

- record quality
- provenance status
- rights risk
- duplicate risk
- classification fit
- evidence boundary compliance

No queue entry should be auto-published to the archive without review. This keeps the system aligned to the project's evidence standards and avoids accidental over-interpretation.

## Phase gating

This document is the architecture design step only. It does not begin a large-scale ingestion run, does not add large curated batches, and does not mark Phase 3 complete.

The next allowed phase after design approval would be a small pilot of a curated set of public Reddit posts, with explicit review and provenance checks.

## Summary

This design keeps the project lawful, provenance-first, and consistent with the existing archive schema. The canonical source remains Reddit, while GitHub holds the reviewed, structured archive. The system favors metadata, summaries, attribution, and classification over wholesale copying and does not convert community content into scientific evidence.

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
