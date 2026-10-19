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
before execution. Read-only generation run 39256106888 produced artifact
12188022370 with SHA-256
`fb345d13426ec9346f206e09a35dddfef05f41257f537d3425c5c161a19a7d42`.

The generator rewrote readable symbolic references while preserving the exact
commits already reviewed on PR #400:

- `actions/checkout@v4.4.0` → `11d5960a326750d5838078e36cf38b85af677262`.
- `actions/setup-python@v5.6.0` → `a26af69be951a213d495a4c3e4e4022e16d87065`.

Run 39256419255 also removed the setup-python workflow entry in a temporary
copy and required `gh actions-lock --verify-local` to fail. The valid lockfile
was restored and verified online before the artifact was staged. The temporary
generator workflow is deliberately absent from the final proposed tree.

Python package specifiers are recorded separately in
`.github/dependency-records/retrieval-validation-python-v078.yml` because
`actions.lock` does not cover shell-installed packages. This record is not a
resolved Python lock: `pytest` and transitive packages remain unpinned, so the
trial must not be described as hermetic dependency reproduction.

All AkashicNET governance boundaries remain unchanged: review-only edge
acceptance, fail-closed privacy, evidence/provenance separation, rights gates,
disabled truth inference, and disabled scientific-evidence promotion. Passing
CI is engineering evidence only; it does not authorize merge, release,
deployment, publication, source use, or promotion.
