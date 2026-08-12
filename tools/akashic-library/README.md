# Akashic Library importer

## Purpose

This directory contains a proposed importer for public Google Drive content associated with the Akashic Library / Codex Nexus archive.

The design is intentionally conservative:

- dry-run mode is the default
- no full archive download is performed automatically
- all items are classified before any import decision
- resumable batch processing is supported
- provenance and rights status are recorded before reuse is approved

## Safety guardrails

- Do not import or replicate the archive wholesale.
- Keep canonical source URLs and provenance records intact.
- Treat public accessibility as a discovery signal, not as licence clearance.
- Default to `INDEX_ONLY` or `LINK_PLUS_METADATA` when rights are unclear.
- Only allow `IMPORT` after an explicit rights decision.
- No Phase 3 completion marker is added by this design.

## Proposed structure

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

This structure is a design scaffold only. The runtime code would be activated in a later, permission-reviewed implementation step.

## CLI proposal

```bash
python tools/akashic-library/drive_importer.py \
  --source-url "https://drive.google.com/drive/folders/1TPFgWXNA1FfL0SzJh9Y0bBoLd0eb1ffQ" \
  --batch-size 50 \
  --dry-run \
  --checkpoint tools/akashic-library/state/checkpoint.json
```

### Optional future commands

```bash
python tools/akashic-library/drive_importer.py \
  --source-url "https://drive.google.com/drive/folders/1TPFgWXNA1FfL0SzJh9Y0bBoLd0eb1ffQ" \
  --batch-size 100 \
  --resume \
  --allow-import \
  --checkpoint tools/akashic-library/state/checkpoint.json
```

## Batch behavior

The importer uses a checkpointed workflow so it can resume after interruption or after a human review gate.

Each batch should:

- traverse a folder slice or page
- collect item metadata
- classify it
- write the audit log
- persist checkpoint state
- continue to the next slice

## Decision matrix

| Decision | Meaning | Local copy? | Human review required |
| --- | --- | --- | --- |
| INDEX_ONLY | Publicly visible, licence unclear | No | Yes |
| LINK_PLUS_METADATA | Citeable but not reproduceable without clarity | No | Yes |
| IMPORT | Explicit open licence or structured permission | Yes | Yes |

## Dry-run output

Dry-run mode should produce a summary including:

- discovered items
- processed items
- duplicates skipped
- index-only count
- link-plus-metadata count
- import-approved count
- error count
- checkpoint location

## Notes

This importer is designed for progressive mapping of a large public archive, not for immediate bulk reproduction. The Toolkit keeps rights clarity and provenance ahead of any local archive expansion.
