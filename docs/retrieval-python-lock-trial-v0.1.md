# Scoped Python dependency lock follow-up

Status: **DRAFT / INDEPENDENT REVIEW REQUIRED**. No merge, release, deployment,
repository-wide enforcement or retrieval-implementation change is authorised by
this experiment. It extends PR #409 at
`02a13dfe923df9dd662e87e38135eacc3398333d`, stacked on PR #400 at
`28887d591b8c8bee52c4901d16437e5d0c8f2f20`. Reconciliation of PR #400 with main,
including historical repair #407, remains separate work.

## Decision and guarantees

Use a workflow-specific `.in` file and generated, fully pinned, hash-checked
requirements `.txt`. Keep pip in CI and pip-tools only in the maintainer's
generation environment. Keep `actions.lock` and both immutable `uses:` SHAs
byte-for-byte unchanged. Neither lock substitutes for the other.

| Approach | Versions and transitive closure | Distribution identity | Cost and boundary |
| --- | --- | --- | --- |
| Pin only pytest and jsonschema | Direct versions fixed; transitive selection can change | No hashes | Smallest edit, but does not resolve the stated gap |
| Exact constraints with direct requirements | Fixes constrained packages; constraints do not install packages or reject newly unconstrained dependencies | No byte verification unless separately enforced with a complete hashed requirements set | Useful for shared version policy; an unnecessary second version-policy file for one job |
| Full pinned requirements without hashes, including a clean `pip freeze` | Fixes the captured target closure; freeze does not itself prove satisfiability or portability | Trusts the index's bytes for each version | Simple intermediate step, still weaker than hash enforcement |
| **Generated full requirements with hashes** | Exact roots and transitives for the generation target; pip validates dependency compatibility | Requires a permitted SHA-256 for every downloaded distribution | **Selected:** standard pip consumption; generator needed only for deliberate updates |
| `uv pip compile` with hashes | Can produce the same class of pinned requirements | Hash enforcement still required during installation | Viable alternative generator; no reason to introduce two generators |
| Scoped uv project and `uv.lock` | Structured resolution with environment markers; `uv sync --locked` checks freshness and syncs the selected environment | Lock records distribution identities | Good for a broader project migration; adds uv bootstrap and project metadata for this two-root experiment |
| `pylock.toml` / `pip lock` | Structured lock for the current Python/platform target | Records distributions and hashes | pip's documented lock and pylock requirements support remain experimental; avoid stacking another preview integration here |

The committed lock determines version selection during installation. Re-running
resolution from direct requirements against a changing index is **not** a
time-independent operation. Reusing the existing generated output preserves
compatible pins; explicit updates are reviewed changes. A successful unchanged
regeneration is a bounded check, not proof about every future resolver or index.

Hash verification constrains downloads to the allowed artifact set. Several
hashes may be allowed for a package, especially platform-specific rpds-py wheels;
this does not promise one identical wheel across every platform. The generator
is restricted to binary distributions, and CI also specifies `--only-binary=:all:`
so it cannot silently build an sdist with unlocked build dependencies. Dependency
resolution stays enabled: do not add `--no-deps` to conceal an incomplete closure.

The fresh venv excludes hosted-runner site packages. Hash checking applies to
downloads, not arbitrary already-installed packages; this is why using a clean
environment matters. `pip check` verifies installed requirements, and test
invocation uses `python -m pytest` from that same environment.

## Provenance and compatibility

The baseline package versions come from successful retrieval
[run 39257543519](https://github.com/tws9stmcbf-web/AkashicNET/actions/runs/39257543519),
job `118077763101`. The job was associated with PR head `02a13dfe...`, but its
actual checkout was GitHub's synthetic merge
`24ed1d3b08da71a5a1d7def7ceba0905ede31aea`, on Ubuntu 24.04.5, CPython 3.12.15.
Those identities are deliberately distinct. That historical job passed 687
tests; it is not validation of this new candidate.

All eleven versions are retained, with no package upgrade:

| Direct | Transitive |
| --- | --- |
| pytest 9.1.1 | iniconfig 2.3.1; packaging 26.3; pluggy 1.7.0; pygments 2.21.0 |
| jsonschema 4.25.1 | attrs 26.1.0; jsonschema-specifications 2025.9.1; referencing 0.37.0; rpds-py 2026.9.1; typing-extensions 4.16.0 |

Generation target: CPython 3.12.14, Linux x86_64, Ubuntu 24.04.3;
pip-tools 7.6.2 and pip 25.0.1. The first compile was seeded with the eleven
exact versions recovered from the baseline job, then regenerated normally.
Compatibility is checked for Python 3.12 on the actual tested Linux environment;
the existence of other hashes is not evidence of Windows, macOS, ARM or other
Python compatibility. CI logs the checkout SHA/tree, interpreter, pip, OS,
architecture and installed package versions for each new run.

## Deliberate update procedure

Run from the repository root on the target Python/platform. Use an isolated
maintainer environment outside the checkout. Tool bootstrap itself is not a
hash-locked toolchain; record its installed versions with the candidate evidence.

```bash
python3.12 -m venv /tmp/akashicnet-lock-tools
/tmp/akashicnet-lock-tools/bin/python -m pip --isolated install \
  --index-url https://pypi.org/simple pip==25.0.1 pip-tools==7.6.2
/tmp/akashicnet-lock-tools/bin/python -m piptools compile \
  --generate-hashes --resolver=backtracking \
  --index-url=https://pypi.org/simple --no-emit-index-url --no-emit-trusted-host \
  --pip-args='--only-binary=:all:' \
  --output-file=.github/dependency-records/retrieval-validation-python-v078.txt \
  .github/dependency-records/retrieval-validation-python-v078.in
```

For a direct dependency update, change its exact version in `.in` first. For a
targeted transitive update, add `--upgrade-package PACKAGE==VERSION` to the
compile command. Inspect resolver warnings: even a targeted update can require
other version changes. Avoid `--upgrade` unless a whole-closure refresh is
intentional. Commit the input and generated output together; normal CI consumes
the output rather than re-resolving or automatically rewriting it. Dependency
file path filters ensure these changes trigger the scoped workflow.

Review the version and hash diff, package provenance and Python compatibility.
Repeat generation without an update and compare bytes. Then use two fresh
virtual environments, install with the workflow's exact hash/binary flags, run
`pip check`, and compare installed versions and download SHA-256s. Review any
compiler or installer change separately. A lock does not make old packages safe
indefinitely; updates remain explicit maintenance decisions.

## Validation and negative-control procedure

Run both existing retrieval validators and the workflow's unchanged nine-file
regression suite in the fresh environment. Run the existing immutable-Actions
audit and public-data boundary scanner. Confirm the only changed repository
paths belong to this dependency experiment, and confirm no diff in `actions.lock`
or in PR #400's retrieval code, tests or governed artifacts.

For negative controls, first download an intact wheelhouse with:

```bash
python -m pip --isolated download --index-url https://pypi.org/simple \
  --require-hashes --only-binary=:all: --no-cache-dir \
  -r .github/dependency-records/retrieval-validation-python-v078.txt \
  --dest /tmp/akashicnet-lock-wheels
```

In temporary copies of the requirements, test each mutation independently:

1. Replace the attrs SHA-256 with 64 zeroes: hash mismatch must fail.
2. Delete the attrs hash while retaining its exact version: missing hash must fail.
3. Remove the entire attrs entry: the indirect dependency must fail as unpinned.
4. Change `attrs==26.1.0` to `attrs>=26.1.0`: non-exact pin must fail.
5. With the intact requirements, append bytes to a temporary copy of the attrs
   wheel: hash mismatch must fail before installation. Restore the original.

Use `python -m pip --isolated install --dry-run --ignore-installed
--require-hashes --only-binary=:all: --no-cache-dir --no-index
--find-links /tmp/akashicnet-lock-wheels -r TEMPORARY_REQUIREMENTS` for these
offline probes. Require a successful intact control before and after mutations,
and verify the expected diagnostic, not merely a nonzero return code. Never
mutate the tracked lock or leave a corrupted wheel in a reusable directory.

Record the exact tested commit/tree, commands, environment, selected download
hashes and results in the PR validation checkpoint. A later documentation commit
or synthetic merge must not silently inherit another commit's test identity.

## Remaining boundaries and sources

This is package-level reproducibility, not a hermetic build. `ubuntu-latest`,
Python's 3.12 patch selection, pip supplied by venv bootstrap, system libraries,
the GitHub runner and the maintainer's generator toolchain remain outside this
lock. Index availability is still required unless a separately maintained
wheelhouse is retained. Hashes do not establish publisher authenticity,
malware absence, rights clearance or scientific validity. No repository-wide
freshness/enforcement policy or automatic dependency update is introduced.

Review-only acceptance, fail-closed privacy, evidence/provenance separation,
rights gates, disabled truth inference and disabled scientific-evidence
promotion remain unchanged. Green CI is engineering evidence only.

Primary references consulted for this comparison:

- [pip repeatable installs](https://pip.pypa.io/en/stable/topics/repeatable-installs/)
- [pip secure installs and hash-checking mode](https://pip.pypa.io/en/stable/topics/secure-installs/)
- [pip constraints semantics](https://pip.pypa.io/en/stable/user_guide/#constraints-files)
- [pip-tools generation and updates](https://pip-tools.pypa.io/en/stable/)
- [uv requirements compilation](https://docs.astral.sh/uv/pip/compile/)
- [uv locking and sync](https://docs.astral.sh/uv/concepts/projects/sync/)
- [pip lock target and experimental status](https://pip.pypa.io/en/stable/cli/pip_lock/)
