# N2N access recovery — 2 October 2026

## Diagnosis

The 100-record tranche and four individually requested unread URLs returned `DisabledError`. The welcome-post control and community landing page remained readable from returned copies. Four additional IDs from the archive's final unobserved rows (`1vnz6a2`, `1vnvx24`, `1vntbfx`, `1vn54g4`) also returned `DisabledError` (`turn44view0`–`turn44view3`).

Following link 5 on the readable welcome post returned an explicit HTTP 429 for `yn6jmx` (`turn47view0`). This is evidence of rate limiting at that request, not proof that every prior failure had the same cause. No Retry-After value was supplied by the reader. No retry was attempted.

The regularly patterned `10001c` archive entry already exists in the August 12 import commit `af0555d26abcd90d1dac685f67290cfdd772d1f9`; regularity alone is insufficient evidence of fabrication. Preserve the exact PR #376 archive boundary. Do not silently remove records or mark reader failures as deletion.

## Recovery behavior

Run `python tools/n2n_access_gate.py references/community/n2n-access-diagnostic-2026-10-02.json` before considering another reader batch. Any explicit 429/401/403 stops requests. A successful cached control does not override wholly disabled new records. Do not generate another blind batch when this gate says STOP_WEB_READER.

Only source-discovered URLs whose post IDs match the pinned archive qualify for a bounded diagnostic; its maximum is five requests. No URL slug supplies a title. The gate itself performs no network calls and schedules no retry.

For continuing enrichment, use an authorized, metadata-only offline export with `tools/import_n2n_metadata_snapshot.py`. This validates the pinned archive hashes, source URLs and post IDs, capture timestamp, snapshot SHA-256, duplicate IDs and exact allowed columns. Batches are bounded to 1–1,000 rows. Extra body/comment/media columns are rejected. Missing values stay missing; flair is labelled at capture, not current. Output is an unreviewed source assertion; no canonical CSV, rights, evidence or website promotion occurs.

CSV header:

```csv
post_id,source_url,title,created_at,author,flair_at_capture,outbound_url
```

Receipt JSON requires exactly `schema`, `source_head`, `snapshot_sha256`, `captured_at`, `source_description`, `acquisition_method`. Use schema `akashicnet.n2n.snapshot-receipt.v1`, source head `808564658800a1ab230bbb837aa3b228911d671f`, an actual SHA-256 of the CSV bytes, a timezone-aware capture timestamp, attribution to the actual source, and acquisition method `existing_export` or `saved_metadata_snapshot`. Never label an unapproved source as approved.

```sh
python tools/import_n2n_metadata_snapshot.py authorized-metadata.csv receipt.json --limit 1000 > candidates.json
python tests/test_n2n_metadata_import.py
```

Seven focused tests pass, including exact acceptance of 1,000 fixture rows, rejection of 1,001 rows, tampered snapshots, body columns, duplicate IDs, mismatched URLs, future creation timestamps, missing values and cached-control/rate-limit stop behavior. Fixture titles are test data only, never corpus enrichment.

Actual source metadata added during this repair: zero. Approved Reddit API credentials or an authorized export are still needed to restore scalable acquisition. The reader's block cannot be fixed in repository code.
