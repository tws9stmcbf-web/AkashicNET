# Scoped GitHub Actions lockfile trial

Date: 2026-10-19. Status: **DRAFT / REVIEW REQUIRED**.

This trial is stacked on draft PR #400 at
`28887d591b8c8bee52c4901d16437e5d0c8f2f20`. It onboards only
`.github/workflows/validate-retrieval-evidence-bridge-v078.yml` to GitHub's
public-preview workflow dependency lockfile. No repository-wide Require
lockfile policy is enabled.

The lockfile was generated and verified by the official
`github/gh-actions-lock` v0.2.0 Linux AMD64 release. The downloaded binary's
SHA-256 was checked as
`79ec84c191667fd935a277e6fd3662cf5d3669cccc9e99998731d8f306f373b6`
before execution. Read-only generation run 39257116800 used the supported
`--no-narrow` mode and produced artifact 12187424960 with SHA-256
`7ff87497e412a67156084cfcd3ec72b09f7813e6d40cd364b29237e6c46566c0`.

The generator preserved AkashicNET's immutable inline SHA references while
recording their readable release tags and exact commits in the lockfile:

- `actions/checkout@11d5960a326750d5838078e36cf38b85af677262` (`v4.4.0`).
- `actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065` (`v5.6.0`).

Run 39257116800 also removed the setup-python workflow entry in a temporary
copy and required `gh actions-lock --verify-local` to fail. The valid lockfile
was restored and verified online before the artifact was staged. The temporary
generator workflow is deliberately absent from the final proposed tree.

At the initial checkpoint `02a13dfe923df9dd662e87e38135eacc3398333d`,
Python package specifiers were recorded separately in
`.github/dependency-records/retrieval-validation-python-v078.yml` because
`actions.lock` does not cover shell-installed packages. That initial record was not a
resolved Python lock: `pytest` and transitive packages remained unpinned, so the
trial must not be described as hermetic dependency reproduction.

All AkashicNET governance boundaries remain unchanged: review-only edge
acceptance, fail-closed privacy, evidence/provenance separation, rights gates,
disabled truth inference, and disabled scientific-evidence promotion. Passing
CI is engineering evidence only; it does not authorize merge, release,
deployment, publication, source use, or promotion.

The separate [Python lock follow-up](retrieval-python-lock-trial-v0.1.md) records
the bounded improvement and remaining limitations. It preserves this Actions
lockfile and the original trial evidence.
