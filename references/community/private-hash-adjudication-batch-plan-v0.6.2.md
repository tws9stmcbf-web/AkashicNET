# Private hash adjudication batch plan v0.6.2

Date: 2026-08-30
Status: ACTIVE

This public document contains no private Drive identifiers, filenames, paths, file-linked hashes, or unresolved family evidence.

## Current sanitised aggregate

- families tested: 9
- physical objects hashed: 24
- byte-identical family determinations: 9
- mismatching families: 0
- canonical work IDs promoted from these private batches: 0
- edition IDs promoted: 0
- rights promotions: 0
- scientific-evidence promotions: 0

## Next execution batches

The remaining two-member review families will be processed in private-runtime batches ordered by expected byte cost, with larger or structurally ambiguous multi-volume sets deferred until the inexpensive copy-identity checks are exhausted.

For every private family:

1. Download each authorised raw object independently.
2. Verify downloaded byte count against the private ledger.
3. Compute SHA-256 locally in the private runtime.
4. Compare every member hash within the family.
5. Record `BYTE_IDENTICAL_VERIFIED` only when all compared hashes agree.
6. Record mismatch without inferring different works or editions.
7. Keep canonical work, edition, rights and scientific-evidence adjudication orthogonal.
8. Publish only sanitised aggregate counts unless the public-release gate is independently satisfied.

## Public-release gate

No object-linked result becomes public merely because hashing succeeds. Public release still requires verified public visibility, sensitivity/PII review, rights/reuse review, explicit public-manifest acceptance, and provenance that does not expose a private provider identifier.
