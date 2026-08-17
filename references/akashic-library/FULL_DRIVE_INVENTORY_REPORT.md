# Akashic Library — full authenticated drive inventory audit

## Executive summary

The live OAuth retry for the configured root did not produce a valid authenticated Drive session in this environment. The importer reached the Google consent URL again, but no persisted OAuth token was created and no successful `files().list()` traversal completed. Because there was no successful token exchange and no live Drive listing, there is no evidence-backed authenticated total for the archive.

The only defensible inventory remains the current repository snapshot of the reachable subset:

- 4 authenticated records
- 1 folder: Philosophy
- 3 PDFs
- 0 imported files
- all records remain `INDEX_ONLY`

This is not proof that the Google Drive library contains only 4 items. It is proof that the current recorded access path reached only a subset of the archive under the current permissions context.

## Authenticated root identity

The configured root identity currently documented in the repository is:

- Root folder ID: `1TPFgWXNA1FfL0SzJh9Y0bBoLd0eb1ffQ`
- Root/source URL: `https://drive.google.com/drive/folders/1TPFgWXNA1FfL0SzJh9Y0bBoLd0eb1ffQ`
- Public folder title observed in repository doc: `Books`

Repository evidence:

- `tools/akashic-library/drive_importer.py` sets the canonical source URL and root-folder input.
- `references/akashic-library/README.md` and `DRIVE_API_SETUP.md` document the same Drive folder as the configured archive root.

## Enumeration method

The repository importer implements a recursive Drive scan using Google Drive API metadata listing with:

- `supportsAllDrives=True`
- `includeItemsFromAllDrives=True`
- recursive `_walk_folder()` traversal
- `files().list()` pagination via `nextPageToken`
- `batch_size` defaulting to 50
- duplicate detection by normalized signature
- dry-run, metadata-only architecture

The code does not allow an import or any file-body extraction. It only collects metadata such as:

- Drive file ID
- parent ID
- name
- MIME type
- folder/file classification
- path
- size
- modified timestamp
- owner / author metadata when exposed
- Drive URL
- accessibility status

## Actual authentication status at execution time

The authenticated enumeration was retried with:

- `--auth-mode oauth`
- `--root-folder-id 1TPFgWXNA1FfL0SzJh9Y0bBoLd0eb1ffQ`
- client secret file present under `tools/akashic-library/`
- a fresh token target at `/tmp/akashic-drive-token.json`

The command output showed:

> Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?... 

The Google consent flow was initiated, but no valid OAuth token file was created in the environment and no successful callback/authorization completed. There was no successful token exchange and no Drive API listing beyond the consent redirect.

Therefore, there is no evidence-backed authenticated full-drive count from this session.

## Pagination and recursive traversal status

The code supports full pagination in principle, but the real run did not progress past OAuth consent, so the actual pagination state is unknown beyond the implementation.

The following technical facts are known from the code:

- pagination continues while `nextPageToken` is present
- recursive folder traversal occurs for every child folder encountered
- item batches are capped only by the configured `batch_size`
- there is no hard-coded `--limit` in the default configuration

However, because the live authentication was not completed, no actual page-by-page recursive enumeration was produced.

## Permission and access findings

The repository documentation and code make clear that complete archive enumeration requires:

- valid Drive access to the archive root
- explicit folder-sharing or service-account permissions
- a valid OAuth access token or service-account credentials
- permission to list the folder tree and metadata

The available evidence shows that the repository does not have a verified live, full, authenticated library inventory. The current 4-record inventory is therefore best described as:

- verified = current reachable subset recorded in repo metadata
- not verified = full archive total

## Previous 4-record inventory vs. true collection size

The previous 4-record inventory is historically significant as a repository snapshot, but it is not a proof that the complete archive contains only 4 records.

It represents the subset that was visible and recorded under the current access context and current data capture path.

The code and metadata strongly suggest that the current inventory can be incomplete because:

- the root folder may not be the full archive root
- branch-level access may be restricted
- shared-drive or shortcut structures may hide additional content
- a consented full enumeration was never successfully completed in this environment
- the checkpoint state records run status, not the full archive size

## Historical ~12,438 estimate

The historical estimate of approximately 12,438 files remains unverified.

The repository currently contains no traceable API-backed result, no exported Drive manifest, and no evidence of a reproduced count matching 12,438. It is therefore not a verified total. It should remain classified as:

- historical estimate
- unverified
- not reproduced by current repository metadata

## Verified counts

The following counts are the only verified counts currently supported by repository evidence, because the live Drive traversal did not complete:

- folders discovered: 1 (Philosophy)
- files discovered: 3 (PDFs)
- shortcuts: 0 verified in the current recorded snapshot
- duplicates: 0 verified in the current recorded snapshot
- inaccessible items: 0 explicitly verified in the recorded snapshot
- permission errors: 0 observed in the recorded snapshot
- traversal errors: 0 observed because no successful authenticated listing completed
- total records: 4 in the current documented subset
- traversal completed: no

This is a verified subset count, not a verified library total.

## Unresolved gaps

The following remain unresolved:

1. whether the configured root is the actual full archive root
2. whether more folders or files exist outside the recorded subset
3. whether hidden/shared/permission-restricted branches exist
4. whether the historical ~12,438 estimate reflects an actual Drive result or a UI-derived assumption
5. whether the current OAuth session can be authorized to enumerate the full archive

## Exact next technical step

The next technical step is not a content import or a rights approval. It is a restored, successfully completed OAuth session that persists a valid token and then a recursive Drive API enumeration from the correct archive root.

Required next step:

- complete the Google OAuth consent flow for the repository’s configured Drive account in a session that persists the token
- confirm the authenticated account can list the actual archive root
- run the recursive metadata enumeration without `--limit`
- page to completion via `nextPageToken`
- log inaccessible branches, permission errors, and duplicate IDs
- record the final authenticated total as a separate verified count rather than treating the current 4-record snapshot as the full library

The observed state here is still blocked at the consent/token stage: the URL was shown, but the authorization callback did not complete in a way that produced a valid token in this environment.

## Content and rights safety

This audit does not retrieve, extract, copy, OCR, or redistribute PDF content.

The following remain true:

- PDF contents were not retrieved
- no document bodies were imported
- `TOTAL FILES IMPORTED` remains 0
- all existing records remain `INDEX_ONLY`
- no existing metadata-only records were removed

## Conclusion

The present evidence supports a narrow but honest conclusion:

- the current 4-record inventory is verified only as a reachable subset under the presently recorded access path
- the true archive size remains unresolved
- the historical ~12,438 figure remains unverified and cannot be accepted as a proven total
- a full authenticated Drive enumeration remains blocked until the OAuth consent step completes successfully in a session that writes a valid token and the true archive root is confirmed accessible
- no live recursive Drive traversal was observed in this environment, so the report reflects the verified subset count only

## Verified live-enumeration result summary

- folder count: 1
- file count: 3
- shortcut count: 0
- duplicate count: 0
- inaccessible/error count: 0 in the current verified subset snapshot
- total records: 4
- traversal completed: no
- historical ~12,438 verified: no
- PR number: 5
- current commit SHA: not yet updated by a new live-enumeration commit; the report remains the verified subset snapshot until a successful authenticated session produces a real Drive listing
