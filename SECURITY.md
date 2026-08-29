# Security policy

## Reporting a vulnerability

Do not publish credentials, private Drive identifiers, personal data or exploit
details in a public issue. Use GitHub's private vulnerability-reporting flow
when available. If it is unavailable, contact the repository owner through the
GitHub profile before sharing sensitive details.

## Public/private data boundary

AkashicNET's public repository is for code, schemas, synthetic fixtures,
sanitised aggregates and independently verified public-source records.

The following are private by default:

- OAuth credentials, API secrets and runtime tokens;
- Google Drive IDs, URLs, filenames, paths, timestamps and sizes;
- raw provider census and canonicalisation ledgers;
- file-linked hashes and unresolved candidate-family evidence;
- personal, medical, administrative, diary-like or correspondence data;
- workflow artefacts containing any of the above.

Public release requires all of the following:

1. independently verified public visibility;
2. a completed PII/sensitivity review;
3. a reviewed rights and reuse disposition;
4. an explicit public-manifest acceptance decision;
5. provenance that does not disclose a private provider identifier.

## Credential handling

Use least-privilege scopes and GitHub Secrets or a private runtime secret store.
Never commit credential files or pass secrets through command-line arguments,
generated reports or workflow artefacts. Rotate a credential immediately if
exposure is suspected.

## Supported versions

Security fixes apply to the default branch. Earlier commits may contain data
that has since been removed; historical-data remediation is tracked separately
from normal source changes.
