# Google Drive API setup for the Akashic Library importer

## Purpose

This document records the exact authenticated access required to enumerate the Akashic Library Drive tree beyond the public HTML landing page. It does not authorize any file download or redistribution. The current work remains metadata-only and dry-run until an explicit authenticated listing is available.

## Required capability

The importer must be able to do all of the following with a valid Google account or service identity:

- list files and folders recursively under the shared archive root
- paginate through Drive results
- inspect item metadata fields
- capture MIME type, size, and modified timestamps
- read owner/display metadata where available
- check whether a licence or reuse statement exists in metadata or a sidecar note
- resume interrupted batch runs with checkpoint state
- avoid importing or redistributing collection files before rights review

## Authentication modes supported

### 1. Service account mode

Use this when the Google Drive folder is shared with a service account or the project has domain-level access.

Required:

- a Google Cloud project
- a Google Drive API enabled project
- a service account JSON key
- the Drive folder shared with the service account email
- `drive.readonly` and `drive.metadata.readonly` scopes

Example environment variables:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
export AKASHIC_AUTH_MODE="service-account"
export AKASHIC_DRIVE_FOLDER_ID="<folder-id>"
```

Example CLI call:

```bash
python tools/akashic-library/drive_importer.py \
  --auth-mode service-account \
  --root-folder-id "<folder-id>" \
  --credentials-file "$GOOGLE_APPLICATION_CREDENTIALS" \
  --dry-run \
  --batch-size 50
```

### 2. OAuth mode

Use this when a human user must authorize access to a shared Google Drive folder.

Required:

- Google Cloud project
- Google Drive API enabled
- OAuth client ID JSON file from Google Cloud Console
- user consent to authorize Drive access
- a local token file to persist the granted session

Example environment variables:

```bash
export AKASHIC_AUTH_MODE="oauth"
export AKASHIC_DRIVE_FOLDER_ID="<folder-id>"
export AKASHIC_DRIVE_TOKEN_FILE="/path/to/drive-token.json"
```

Example CLI call:

```bash
python tools/akashic-library/drive_importer.py \
  --auth-mode oauth \
  --root-folder-id "<folder-id>" \
  --credentials-file "/path/to/client-secrets.json" \
  --token-file "/path/to/drive-token.json" \
  --dry-run \
  --batch-size 50
```

## Required Google Cloud setup

1. Create a Google Cloud project.
2. Enable the Google Drive API.
3. Create OAuth client credentials or a service account as needed.
4. If using OAuth, add the `https://www.googleapis.com/auth/drive.readonly` and `https://www.googleapis.com/auth/drive.metadata.readonly` scopes.
5. Share the target folder with the service account email or user account that will grant consent.
6. Confirm the account can view the archive tree before running the importer.

## Required scopes

The importer is designed for readonly access only:

- `https://www.googleapis.com/auth/drive.readonly`
- `https://www.googleapis.com/auth/drive.metadata.readonly`

These are sufficient for metadata listing and recursive traversal without granting write access.

## Do not include

- private credentials in source code
- hard-coded API keys or OAuth tokens
- workspace-local secret files in Git history
- real archive downloads or copies before licence review

Use environment variables or a local secret store outside the repository.

## Validation checklist before live import

The importer should not proceed to a real collection import until all of the following are true:

- the shared folder is reachable from the authenticated account
- recursive traversal returns folder and file IDs
- pagination works without truncation
- file metadata includes MIME type, size, and modified times
- authorship/owner fields are captured when the data is present
- licence/reuse information is explicitly documented or classified as unknown
- the checkpoint state can resume a prior run
- duplicate detection is verified
- rate-limit handling and retry logic are exercised
- dry-run output verifies expected metadata before any copy

## Current safety status

This repository does not permit or perform a live collection import from the public folder. The authenticated importer scaffold is ready for an authorized Drive listing, but the actual archive remains out of scope until the above access and rights checks are complete.
