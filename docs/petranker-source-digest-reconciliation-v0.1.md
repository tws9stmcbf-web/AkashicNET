# Petranker source-digest reconciliation v0.1

Status: isolated review-only correction extracted from draft PR #400; no merge, release or deployment.

Extracted on 18 October 2026 from `28887d591b8c8bee52c4901d16437e5d0c8f2f20` onto current main `e920533004eb8b7a10031c0b38ec20576250a665`. The source split, research index, regression tests and two-line combined-workflow addition are preserved verbatim. This note alone is updated for the isolated scope. No retrieval implementation or historical v0.16 CLI change is included. The historical investigation below retains its original commit identities.

## Verified cause

Investigated PR head: `88e620320c31c9a3a84e9b07c5d454f5ec54ada4`.
The failed combined-candidate run [38323187853](https://github.com/tws9stmcbf-web/AkashicNET/actions/runs/38323187853)
checked out that exact head. Job `115055740021` failed in
"Validate inherited candidate and sealed public status" with
`source-status-v0.16: FAIL: input digest drift: SRC-MICRODOSING-PETRANKER-2026`.
The failure was also reproduced locally before correction.

- `f3d3c99e6eb4f60544914971a7f543263a703367` (2 September): the research
  document became blob `05b14477d17edafdfcb80481f134848066cd3a2a`.
- `1f679ddec72a6c47413ccb20c1eb17415fb72aeb` (8 September): the observed
  source-status fixture bound the Petranker node and its 2 September retrieval
  event to that blob.
- `9cf967a7a9ed7921e6220189e46f4dc51c845a88` (11 October): appended 37 lines
  about a different rat study, changing the document to blob
  `14abd8c56074af6d361818c82bd13ccf736cf7be`. All earlier bytes were unchanged.
  This commit is in PR #400's base; the retrieval-boundary correction did not
  introduce the mismatch.

## Identity and provenance decision

The Petranker source is DOI `10.1016/j.drugpo.2026.105459`, with preserved
ScienceDirect PII `S0955395926003129` and PMID `42566966`. The repository's
2 September review records DOI/publisher timeouts and identifier matching via
Crossref/PubMed. The fixture reflects that dated observation as
`UNAVAILABLE_INDETERMINATE`, not a live availability check or a scientific verdict.
This investigation verifies repository provenance; it does not repeat or certify
the historical external HTTP probes.

[Issue #282](https://github.com/tws9stmcbf-web/AkashicNET/issues/282) requires
original URLs, historical outputs, retrieval timestamps, prior classifications
and immutable digests to be preserved, with no silent advancement of governed
digests. The inherited manifest additionally pins the fixture, schema, validator
and existing mutation suite. Replacing the node/event hashes with the October
digest would falsely bind a September event to a later multi-study document.

The correction restores the historical document's exact bytes and relocates the
entire October appendix, verbatim, to
[`research/rat-psilocybin-5ht2a-2026.md`](../research/rat-psilocybin-5ht2a-2026.md).
The research index links both records. The appendix's SHA-256 is
`658d1ee20a6500b988a2780d8e373d2cde041bf831b5ba2f666ae99685b7dc16`.
Concatenating the restored document and new file reconstructs the exact October
blob. No scientific wording, evidence classification or qualification was lost.
The old appendix anchor moves to the new file; the original document URL remains.

No fixture, schema, validator, inherited test, manifest or sealed baseline is
changed. Human-review state, original identifiers, event evidence, all promotion
guards, rights restrictions and privacy controls are preserved. Future updates
belong in separate research records or an explicitly versioned provenance change;
the historical input must not become a rolling multi-study document again.

## Verification

`tests/test_petranker_source_binding.py` checks historical bytes, lossless appendix
relocation/reconstruction, and unchanged fixture/event identity and guards.
The combined workflow runs this suite before inherited validation, using its
existing exact-head checkout. Existing mutation tests and all dependency gates
remain enabled.

Run locally on the committed candidate:

```sh
python -m pytest -q tests/test_petranker_source_binding.py
python scripts/validate_source_status_v016.py
python -m pytest -q tests/test_source_status_v016.py
```

Then run every `run` step of `.github/workflows/validate-v017-combined-candidate.yml`
with `EXPECTED_HEAD` and `CANDIDATE_HEAD_SHA` equal to `git rev-parse HEAD`.
The forward combined workflow deliberately uses the historical manifest's
`validate_manifest` and `run_dependencies` functions; the old standalone v0.16
CLI requires a historical `origin/main` and is not the forward-candidate gate.
See [the existing contract](v017-combined-validation.md).

Exact tested commit, local outcomes and live Actions results are recorded in
the PR validation update after the correction commit exists. A successful run
does not authorize release or scientific promotion. Retrieval-contract changes in PR #400 are outside this isolated correction. Historical test counts from that PR do not describe this new candidate.


## PR #400 integration checkpoint, 20 October 2026 UTC

The text above records the earlier investigation and isolated extraction. PR #407
was subsequently merged as `85af5b6eb7a086a0a330575552b7eb1b82b92abf`;
PR #406 then brought the STARGATE metadata index into main at
`e342c8fea7ef6da7ffe2a5efa8fca17de72df6a4`. Earlier draft/pending wording is
historical and is not a statement of those merged PRs' current status.

This reconciliation brings that main into draft PR #400 without rewriting its
history. The existing source split, historical validator, preservation entry
point, associated tests, workflows and governed pins are unchanged. This note
retains main's extraction record; the original PR #400 version remains available
at [`28887d591b8c8bee52c4901d16437e5d0c8f2f20`](https://github.com/tws9stmcbf-web/AkashicNET/blob/28887d591b8c8bee52c4901d16437e5d0c8f2f20/docs/petranker-source-digest-reconciliation-v0.1.md).

The retrieval improvements are retained from PR #400 and require fresh validation
against the integrated head. Earlier test counts are historical evidence only.
PR #409's dependency-locking experiment remains separate. See the
[reconciliation scope and stack plan](pr400-main-reconciliation-20261020.md).
No merge to main, release, deployment, scientific or rights promotion is approved
by this reconciliation; PR #400 remains draft pending independent review.
