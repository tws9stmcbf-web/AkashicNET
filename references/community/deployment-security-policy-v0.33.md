# AkashicNET deployment/security policy v0.33

## Purpose

v0.33 hardens the retrieval service without changing semantic, provenance, rights, or scientific-evidence decisions.

## Runtime separation

- `AKASHICNET_DEPLOYMENT_MODE=public` disables internal visibility unconditionally.
- `AKASHICNET_DEPLOYMENT_MODE=internal` may enable internal visibility only when `AKASHICNET_ALLOW_INTERNAL_VISIBILITY=true`.
- Public mode defaults every retrieval request to `visibility=public`.
- Internal mode defaults to `visibility=internal` only when explicitly enabled.

## Public rights boundary

Public retrieval continues to require result-level `PUBLIC_VERIFIED`. Missing rights metadata remains `UNKNOWN_UNVERIFIED`.

## Safe diagnostics

- `/livez` reports process liveness only.
- `/readyz` reports service readiness only.
- `/health` reports deployment mode and guard state, not internal corpus metadata.
- Error responses use fixed public messages; exception text, subprocess stderr, queries, headers, and internal result metadata are not returned.
- HTTP logs contain method and path only, with query strings omitted.

## Resource controls

- query length limit defaults to 512 characters;
- request-target length limit defaults to 2048 characters;
- retrieval result limit is capped at 100;
- per-client in-memory rate limit defaults to 60 requests per 60 seconds.

These defaults may be changed through documented environment variables, but public-mode visibility separation cannot be disabled by configuration.

## Epistemic invariants

Deployment hardening does not imply or modify truth, scientific validation, safety, efficacy, semantic acceptance, provenance confidence, SHA-256 identity, or redistribution rights.
