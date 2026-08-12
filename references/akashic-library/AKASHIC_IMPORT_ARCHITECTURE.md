# Akashic Library importer architecture

## Purpose

This document defines a resumable, rights-safe pipeline for progressively mapping the public Akashic Library Google Drive into the Noetic Sciences Toolkit without copying the archive wholesale.

This is a design-only workflow. It does not perform a large import, does not download the archive automatically, and does not mark Phase 3 complete.

## Safety model

The importer must follow the Toolkit's proven archive rules:

- canonical source remains the original Google Drive public archive
- the Toolkit stores metadata, links, and provenance records, not a mirror of the archive
- public access does not imply unrestricted reuse
- the importer must default to dry-run mode
- no item is imported locally until a valid licence/reuse status is classified and reviewed

## Processing modes

### INDEX ONLY

Use when the item is publicly accessible but no clear licence or reuse statement is available.

- retain the source URL and folder path
- record the item title and metadata
- classify as `INDEX_ONLY`
- do not create a local copy
- flag for manual permission review

### LINK + METADATA

Use when the source may be referenced but reproduction is not clearly permitted or is uncertain.

- retain canonical link
- record metadata, date, source, author, and provenance
- mark as `LINK_PLUS_METADATA`
- do not copy, transform, or redistribute the file
- keep the import state separate from any 'reuse-approved' set

### IMPORT

Use only when explicit usage rights are present or the source is clearly under an open licence that allows local reproduction and archiving.

Examples may include:

- explicit CC-BY / CC0 / public-domain statements
- documented rights notice from the archive owner
- a clearly permitted redistribution agreement

When `IMPORT` is selected:

- the file may be downloaded or retained locally under the review decision
- provenance and licence status must be recorded before any copy is made
- the importer must log the exact decision and source statement

## Core workflow

1. Discover root folder and child folders/items.
2. Preserve the full folder hierarchy as a logical path.
3. Extract file metadata such as title, ID, MIME type, size, URL, and parent folder.
4. Infer author/source identity using public metadata, parent folder names, and explicit author fields when available.
5. Extract dates from the file name, Drive metadata, folder naming, or the parent archive context.
6. Classify subject using a controlled taxonomy.
7. Classify source type such as book, article, note, image, transcript, video, or archive bundle.
8. Detect licence or reuse permission from folder metadata, file metadata, or a sidecar permissions notice.
9. Record provenance and a stable canonical URL.
10. Detect duplicates using a normalized fingerprint such as Drive ID, URL, title + date, or file hash where available.
11. Log errors, retries, and skipped items.
12. Save a checkpoint after each batch.
13. Resume from the last committed batch rather than restarting the whole archive.

## Folder hierarchy preservation

The archive should be preserved as a `folder_path` field rather than flattening everything into a generic listing.

Example:

- `Library / Books / Philosophy / ...`
- `Library / Transcripts / Sessions / ...`

This path should be stored alongside each item so the archive remains traceable to the public structure without copying the original tree.

## Metadata extraction rules

For each discovered item, capture:

- drive_id
- title
- parent_folder_id
- parent_folder_path
- file_type
- mime_type
- size_bytes
- drive_url
- canonical_source_url
- author_name
- source_name
- date_raw
- year
- subject_category
- source_type
- licence_status
- reuse_decision
- provenance_status
- last_seen_at

The importer should never guess a licence when the public record is unclear. It should default to `unknown` and route the item to `INDEX_ONLY` or `LINK_PLUS_METADATA` unless a permission statement is explicit.

## Author and source identification

Author/source detection should be conservative and evidence-based.

### Preferred order

1. explicit author field in Drive metadata
2. folder owner / archive owner metadata
3. visible source note in folder description
4. file name or parent folder naming only as weak evidence
5. unknown when no reliable attribution exists

### Rule

If the author cannot be verified from public metadata, the importer should record `author: unknown` and keep the provenance note explicit rather than guessing.

## Date extraction

Dates must be extracted from high-confidence metadata first.

### Preferred order

1. Drive-created or modified timestamp
2. embedded metadata in the file
3. filename pattern such as `YYYY-MM-DD`, `YYYY`, `MM/YYYY`
4. folder naming or archive naming conventions
5. `unknown`

Any extracted date should be normalized to ISO 8601 when possible, while retaining the original raw value for provenance.

## Subject classification

Use a controlled taxonomy aligned with the Toolkit, for example:

- consciousness
- philosophy
- neuroscience
- contemplative practices
- wisdom traditions
- human development
- cultural memory
- symbolic systems
- literature
- art / visual culture
- ecology / nature
- community discourse
- speculative frameworks
- unknown

The importer should assign one primary category plus optional secondary tags.

## Source-type classification

Possible types include:

- book
- article
- essay
- transcript
- lecture
- image
- diagram
- audio
- video
- notebook
- archive bundle
- unknown

This field is used to separate `source type` from `subject category`, which are intentionally distinct.

## Licence and reuse detection

This is a critical gate.

### Signals to check

- Drive permissions or visibility notice
- folder-level disclaimers
- file-level licence text
- open-source statements
- copyright line or reuse terms
- sidecar README / metadata notes

### Decision model

- `INDEX_ONLY`: public access without a clear licence or reuse statement
- `LINK_PLUS_METADATA`: source can be cited but reproduction is unclear or restricted
- `IMPORT`: explicit open licence or permission for local reproduction

The importer must never silently upgrade an item from `INDEX_ONLY` to `IMPORT` without a clear evidence trail.

## Provenance recording

Each processed item should record all of the following:

- original Drive URL
- canonical Toolkit reference URL
- parent folder path
- source statement or rights note
- retrieval timestamp
- processing batch ID
- classification state
- import status
- review status

The `provenance_status` field should be explicit and reviewable.

## Duplicate detection

Duplicates must be detected before a record is considered new.

### Canonical duplicate keys

- Drive file ID
- normalized canonical URL
- file hash, when available
- normalized title + date + author

If a near-duplicate is found, it should be quarantined for review instead of silently merged.

## Error handling and retry

The pipeline must handle transient and structural failures gracefully.

### Error categories

- rate limiting / API throttling
- permission denied
- missing metadata
- parent folder not found
- invalid item type
- malformed date data
- temporary network error
- large item set timeout

### Retry policy

- backoff with jitter
- maximum retry count per batch item
- record all failures in the audit log
- quarantine permanently failing items
- continue processing the rest of the batch

## Checkpoint and resume capability

A checkpoint file should be stored after each batch, including:

- run_id
- last_processed_cursor or page token
- last_folder_id
- processed_count
- skipped_count
- duplicate_count
- error_count
- batch_index
- timestamp
- source_url

The importer should resume from the latest valid checkpoint and avoid reprocessing items already marked as complete.

### Example checkpoint state

```json
{
  "run_id": "2026-08-12-akashic-batch-004",
  "source_url": "https://drive.google.com/drive/folders/1TPFgWXNA1FfL0SzJh9Y0bBoLd0eb1ffQ",
  "last_folder_id": "abc123",
  "last_cursor": "page_token_17",
  "processed_count": 320,
  "skipped_count": 12,
  "duplicate_count": 8,
  "error_count": 2,
  "batch_index": 4,
  "last_updated_utc": "2026-08-12T14:42:10Z"
}
```

## Incremental processing and batch mode

The importer should process in bounded batches so it can be resumed over multiple runs.

Recommended policy:

- default batch size: 50–200 items
- allow explicit `--limit` override for dry-run or testing
- after each batch, write checkpoint and audit log
- continue on partial failures without losing progress

## Accurate item counter

The counter must be based on a single source of truth from the processing state, not on transient page counts.

### Count categories

- discovered_total
- processed_total
- indexed_total
- link_plus_metadata_total
- import_total
- duplicate_total
- skipped_total
- failed_total

Counter values should be updated only after a successful state commit.

## Audit log

The importer writes a JSONL audit log for all batches.

Each line may contain:

- timestamp
- run_id
- item_id
- title
- parent_path
- decision
- reason
- licence_status
- provenance_status
- error or warning text

This log is the authoritative review trail and should be preserved with the batch output.

## Dry-run mode

Dry-run mode is the default and is required for the design stage.

In dry-run mode the importer should:

- enumerate candidate items
- classify them
- detect duplicates
- create checkpoint state
- write audit log entries
- print a report
- not copy, download, or import files

Dry-run should still produce a summary such as:

- discovered
- processed
- duplicates
- index-only
- link-plus-metadata
- import-approved
- errors

## Proposed implementation structure

```text
tools/akashic-library/
├── README.md
├── __init__.py
├── drive_importer.py
├── checkpoint.py
├── audit.py
├── classifiers.py
├── models.py
├── dryrun/
│   └── README.md
└── state/
    └── .gitkeep
```

## Proposed module responsibilities

### `drive_importer.py`

Main orchestration layer.

Responsibilities:

- parse CLI arguments
- call traversal logic
- manage batch execution
- resume from checkpoint
- write batch summary

### `checkpoint.py`

Responsible for checkpoint creation, loading, and validation.

Responsibilities:

- read/write JSON state
- update counters
- handle resume logic
- detect corrupt or partial checkpoints

### `audit.py`

Responsible for audit logging, dry-run logs, and error records.

Responsibilities:

- JSONL append events
- aggregate summary counters
- maintain batch history

### `classifiers.py`

Responsible for subject, source-type, and licence classification logic.

Responsibilities:

- category mapping
- type inference
- reuse decision rules
- unknown detection

### `models.py`

Contains the clear data models for records and state objects.

Responsibilities:

- define ItemRecord
- define CheckpointState
- define BatchSummary
- define reuse decision enum

## Execution policy

This importer must be designed to be safe by default and incremental by design.

It should not be used to pull the entire archive in a single pass without review.

Recommended initial deployment:

- start with a single folder or shallow batch
- process in dry-run mode
- write a checkpoint
- manually review the first batch summary
- only then consider a permission-reviewed import phase

## Compliance note

This approach intentionally distinguishes between:

- public discovery and indexing
- link-based citation and metadata preservation
- permitted local reproduction under explicit rights

This preserves the Toolkit's evidential boundaries and avoids converting a public archive into an unreviewed local copy.
