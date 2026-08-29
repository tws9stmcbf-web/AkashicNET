# AkashicNET Retrieval HTTP v0.28

## Milestone

**Machine-readable retrieval contract plus deployable packaging without semantic drift.**

v0.28 turns the v0.27 HTTP adapter into a formally described and reproducibly testable service layer while retaining the stable upstream retrieval contract `AKASHICNET_RETRIEVAL_API` v0.25.

## Interfaces

- `GET /health`
- `GET /openapi.json`
- `GET /v1/retrieve?q=<query>&domain=<all|reddit|library>&state=<all|accepted|hold>&limit=<1..1000>`

The OpenAPI 3.1 document is committed at `api/openapi-retrieval-v0.28.json` and is also served at runtime from `/openapi.json`.

## Contract fixtures

Deterministic integration expectations are stored at `tests/fixtures/retrieval-http-v0.28.json`. They cover:

- health and OpenAPI discovery;
- verified SHA-256 provenance retrieval for `Golden Book of Wisdom`;
- preservation of explicit `HOLD` results;
- accepted Reddit topical retrieval;
- invalid-request behaviour;
- truth, rights-clearance, and scientific-evidence non-claim guards.

Fixtures verify interface behaviour; they do not promote semantic decisions, scientific evidence, rights status, or truth.

## Deployment

`deploy/retrieval-v0.28/Containerfile` produces a self-contained Python 3.11 service image. The build reconstructs the prerequisite metadata/provenance layers from repository inputs and then starts:

```text
python scripts/retrieval_http_v028.py --host 0.0.0.0 --port 8787
```

No additional raw Google Drive access or hashing is performed by v0.28. The previously authorised v0.16 digests are consumed as persisted provenance evidence only.

## Epistemic and rights boundaries

The service continues to enforce the existing separations:

- ranking does not change semantic decisions;
- topical `ACCEPT` does not mean truth;
- direct metadata lookup does not mean semantic acceptance;
- SHA-256 identity proves byte identity for the verified pair only;
- byte identity does not establish edition equivalence, scientific validity, safety, efficacy, rights, or public-domain status;
- rights remain governed independently by the R0-R4 rights ladder;
- public redistribution/retrieval eligibility must not be inferred from accessibility or catalogue membership;
- `PUBLIC_VERIFIED` remains the independent public-manifest requirement.

## Version boundary

The transport/service layer is v0.28. The upstream consumer contract deliberately remains v0.25 (`akashicnet://schemas/retrieval/v0.25`) because v0.28 does not alter the retrieval result semantics.
