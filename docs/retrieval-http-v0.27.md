# AkashicNET Retrieval HTTP Adapter v0.27

v0.27 exposes the stable v0.25 retrieval contract over a minimal HTTP/JSON transport. It is an adapter, not a new semantic engine.

## Start locally

```bash
python scripts/retrieval_http_v027.py --host 127.0.0.1 --port 8787
```

The implementation uses only the Python standard library.

## Endpoints

### `GET /health`

Returns service identity, upstream contract identity, and the non-promotion policy.

Expected fields include:

- `service = AKASHICNET_RETRIEVAL_HTTP`
- `service_version = 0.27`
- `upstream_api = AKASHICNET_RETRIEVAL_API`
- `upstream_schema = akashicnet://schemas/retrieval/v0.25`
- truth inference disabled
- rights promotion disabled
- scientific-evidence promotion disabled

### `GET /v1/retrieve`

Query parameters:

- `q` required search string
- `domain` optional: `all`, `reddit`, `library`
- `state` optional: `all`, `accepted`, `hold`
- `limit` optional integer from 1 to 1000

Example:

```text
GET /v1/retrieve?q=Golden%20Book%20of%20Wisdom&state=accepted&limit=5
```

The response envelope adds transport metadata only:

```json
{
  "service": "AKASHICNET_RETRIEVAL_HTTP",
  "service_version": "0.27",
  "transport": "http-json",
  "upstream": {
    "api": "AKASHICNET_RETRIEVAL_API",
    "api_version": "0.25",
    "schema_id": "akashicnet://schemas/retrieval/v0.25"
  }
}
```

All semantic decisions, provenance tiers, policy flags, result guards, and result records remain inside `upstream` unchanged from the stable retrieval API.

## Semantics and safety boundaries

The service must not reinterpret upstream states.

- `DIRECT_METADATA_LOOKUP` is not converted to `ACCEPT`.
- `HOLD` remains `HOLD` unless the reviewed upstream layer changes it.
- provenance tiers such as `P3_SHA256_IDENTITY_PROVENANCE` describe provenance strength, not truth.
- SHA-256 identity proves byte equality for a verified pair only.
- rights status is independent of byte identity and topical retrieval.
- public accessibility, scientific validation, safety, efficacy, and endorsement are not inferred by this transport.

The HTTP layer performs no raw Google Drive access and no hashing. It consumes repository-generated retrieval artifacts only.

## Error behaviour

- missing `q`: HTTP 400, `invalid_request`
- invalid `domain`, `state`, or `limit`: HTTP 400, `invalid_request`
- unknown path: HTTP 404, `not_found`
- upstream retrieval process failure: HTTP 500, `upstream_failure`

## Compatibility

v0.27 intentionally depends on the v0.25 consumer schema rather than inventing a new retrieval schema. A future transport version may change endpoint mechanics, but any semantic/schema change must follow the compatibility policy in `references/community/retrieval-api-compatibility-policy-v0.26.md`.
