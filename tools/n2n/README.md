# N2N ingestion prototype

This directory contains the first provenance-first ingestion prototype for the r/NeuronsToNirvana archive workflow.

## Purpose

The prototype is intentionally conservative and designed to support a small, reviewed batch of public Reddit posts without turning the Toolkit into a Reddit mirror.

## Safety model

- canonical source remains Reddit
- fields are structured and reviewable
- bulky or copyrighted media are not copied into the archive
- dry-run mode is the default
- data is classified and provenance-tagged before any write path is allowed

## Usage

```bash
python tools/n2n/ingest_n2n.py --csv references/community/n2n-pilot-index.csv --limit 25 --dry-run
```

This reads a curated candidate batch, validates the schema, detects duplicates, and writes an auditable dry-run log to:

- tools/n2n/dryrun/25_post_test.jsonl

## Scope

The prototype is suitable for a small batch only. It is not intended to support 1,000 or 6,000 post ingestion yet.

## Current status

This prototype is designed for controlled deployment behind valid Reddit API access and a human review gate. It is not yet ready to scale in this environment because public Reddit access was blocked with HTTP 403 during validation.

## Notes

- No post writes are performed by default.
- No Phase 3 completion marker is added.
- The workflow is designed to match the existing N2N archive schema and evidence boundaries.
