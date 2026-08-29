# AkashicNET Drive pagination and terminality audit

Status: executable validation procedure — no gate credit until a complete output ledger passes
Scope: nominated Akashic Library Google Drive tree only
Date: 2026-08-29

## Validation gate

This procedure implements `PAGINATION_AND_TERMINALITY_AUDIT`, worth 2 points in the five-gate validation model.

## Denominator

The audit denominator is the complete known folder-node census:

- 66 top-level roots
- 129 descendant folder nodes
- 195 folder nodes total

The denominator is fixed before execution.

## Procedure

Run `scripts/drive_pagination_audit.py` with a read-only Google Drive OAuth access token in `GOOGLE_DRIVE_ACCESS_TOKEN`.

For every one of the 195 known folder nodes the script:

1. queries direct children with `trashed = false`;
2. requests up to 1000 items per provider page;
3. follows every returned `nextPageToken` until exhausted;
4. records the provider page count;
5. separately counts direct documents and direct child folders;
6. compares descendant-node counts with the frozen metadata census;
7. verifies that nodes labelled `TERMINAL_LEAF` or `EMPTY_CONFIRMED` contain zero child folders;
8. persists provider/API errors as `ERROR` rather than silently treating the node as terminal.

## Output

The audit writes:

`references/community/drive-pagination-terminality-audit.csv`

Required columns include node path and Drive ID, expected state/counts, observed document/folder counts, number of pages consumed, terminality result, PASS/FAIL/ERROR status and any exception.

## Pass criteria

The gate passes only when all of the following are true:

- exactly 195 unique known folder nodes are represented;
- every query has exhausted pagination (`nextPageToken` no longer returned);
- no row has `ERROR`;
- no row has `FAIL`;
- every descendant node with frozen direct counts matches those counts;
- every `TERMINAL_LEAF` and `EMPTY_CONFIRMED` node has zero direct child folders;
- any newly discovered child folder is reconciled into the census before the gate can pass.

A spot check, connector folder listing capped at 100 children, or inferred terminality from historical traversal notes is insufficient for credit.

## Current score

0 / 2 points for `PAGINATION_AND_TERMINALITY_AUDIT` until the complete generated ledger exists and passes the criteria above.
