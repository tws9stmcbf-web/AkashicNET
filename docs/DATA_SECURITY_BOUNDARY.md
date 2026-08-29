# Data security boundary

AkashicNET separates open-source processing logic from the private corpus audit
layer.

| Public repository | Private data layer |
|---|---|
| Code and schemas | Provider credentials and tokens |
| Synthetic fixtures | Drive IDs and source URLs |
| Aggregate counts | Filenames, paths, timestamps and sizes |
| Sanitised public-source records | Raw census and canonicalisation ledgers |
| Reviewed public graph edges | File-linked hashes and unresolved evidence |

## Publication gate

A record is not public merely because it was discovered, shared with an
operator, or readable through an authenticated account. Publication requires
`PUBLIC_VERIFIED`, a completed sensitivity/PII review, reviewed reuse rights,
and an explicit `ELIGIBLE` decision.

Public graph identifiers must be project-owned pseudonymous identifiers. They
must not embed a Google Drive ID or another private provider identifier.

## Runtime handling

Private runs should execute in a private repository or controlled local
environment. Raw outputs must use ignored private paths and must not be uploaded
from a public GitHub Actions run. Only an aggregate report that passes the public
boundary check may be copied into the public repository.

## Historical exposure

Deleting a file from the current branch does not remove it from Git history,
forks, clones or existing workflow artefacts. Historical remediation requires a
deliberate history rewrite, deletion of retained artefacts and review of source
sharing permissions.
