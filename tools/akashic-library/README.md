# Akashic Library importer

## Purpose

This directory contains the resumable Akashic Library importer design and a dry-run batch processor for the public Google Drive folder.

The current environment does not expose a complete item listing or reliable licence metadata for the archive from the unauthenticated public page alone. The importer therefore follows the repository's strict provenance model:

- preserve canonical source links
- classify items conservatively
- keep public access separate from import permission
- write checkpoints and audit state before any further expansion

## Safety guardrails

- no bulk document copy without explicit rights
- no invention of licence information
- no claim that the entire archive has been fully enumerated from the public page alone
- no Phase 3 completion claim while archive validation is incomplete
- default to metadata-first, link-only, or review-required handling

## Batch design

The importer processes item lists in batches and persists state:

- checkpoint JSON for resume state
- audit JSONL for decisions and events
- error JSONL for failed or unavailable items
- CSV output for the current batch index

## Current status

This is not a complete archive import. It is a resumable ingestion scaffold for a public archive whose full item list is not yet verified from the current environment.

## CLI usage

```bash
python tools/akashic-library/drive_importer.py \
  --source-url "https://drive.google.com/drive/folders/1TPFgWXNA1FfL0SzJh9Y0bBoLd0eb1ffQ" \
  --batch-size 50 \
  --dry-run \
  --checkpoint tools/akashic-library/state/checkpoint.json \
  --out-csv references/akashic-library/AKASHIC_LIBRARY_INDEX.csv
```

## Decision matrix

| Decision | Meaning | Local copy | Review |
| --- | --- | --- | --- |
| INDEX_ONLY | Publicly accessible but licence unclear | No | Yes |
| LINK_PLUS_METADATA | Source may be cited, but reproduction is not clear | No | Yes |
| IMPORT | Explicit open licence or permission | Yes | Yes |

## Notes

This is a reproducible, resumable pathway for the archive, but the actual collection size and file-level licence state must be validated with a Drive API or a verified public listing before a large-scale import is considered safe.
