# Akashic Library importer

## Purpose

This directory contains the resumable Akashic Library importer design and the authenticated Google Drive intake scaffold. It is intentionally conservative: it supports authenticated enumeration without downloading the archive yet, and defaults to a metadata-only dry run unless explicit rights are documented.

The current environment does not expose a complete item listing or reliable licence metadata from the unauthenticated public page alone. The importer therefore follows the repository's strict provenance model:

- preserve canonical source links
- classify items conservatively
- keep public access separate from import permission
- write checkpoints and audit state before any further expansion
- never fabricate collection totals or licence status

## Safety guardrails

- no bulk document copy without explicit rights
- no invention of licence information
- no claim that the entire archive has been fully enumerated without authenticated Drive access
- no Phase 3 completion claim while archive validation remains incomplete
- default to metadata-first, link-only, or review-required handling
- do not attempt further public-folder scraping for item enumeration

## Supported workflow

The importer now supports:

- Google Drive API authentication via service account or OAuth
- recursive folder traversal
- pagination
- file metadata extraction
- MIME type and file size capture
- modified times
- author/source metadata when present
- licence/reuse metadata classification
- checkpoint/resume state storage
- duplicate detection
- rate-limit handling and retry backoff
- error logging
- dry-run mode
- CSV and Markdown index generation

## Default runtime mode

The default mode remains `dry_run` and metadata-only to keep the archive safe while access is being validated.

## CLI usage

```bash
python tools/akashic-library/drive_importer.py \
  --auth-mode service-account \
  --root-folder-id "<folder-id>" \
  --credentials-file "$GOOGLE_APPLICATION_CREDENTIALS" \
  --batch-size 50 \
  --dry-run \
  --checkpoint tools/akashic-library/state/checkpoint.json \
  --audit-log tools/akashic-library/state/audit.jsonl \
  --error-log tools/akashic-library/state/errors.jsonl \
  --out-csv references/akashic-library/AKASHIC_LIBRARY_INDEX.csv \
  --out-md references/akashic-library/AKASHIC_LIBRARY_INDEX.md
```

Mock/local testing without live Drive access:

```bash
python tools/akashic-library/drive_importer.py \
  --auth-mode mock \
  --root-folder-id root \
  --mock-data-path tests/mock_akashic_drive.json \
  --dry-run \
  --out-csv references/akashic-library/AKASHIC_LIBRARY_INDEX.csv \
  --out-md references/akashic-library/AKASHIC_LIBRARY_INDEX.md
```

## Decision matrix

| Decision | Meaning | Local copy | Review |
| --- | --- | --- | --- |
| INDEX_ONLY | Publicly accessible but licence unclear | No | Yes |
| LINK_PLUS_METADATA | Source may be cited, but reproduction is not clear | No | Yes |
| IMPORT | Explicit open licence or permission | Yes | Yes |

## Notes

This is a reproducible, resumable pathway for the archive, but the actual collection size and file-level licence state must be validated with Drive API access or another authenticated listing mechanism before a large-scale import is considered safe.
