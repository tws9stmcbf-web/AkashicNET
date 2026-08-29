# Hash adjudication queue v0.6.2

Date: 2026-08-29

Purpose: convert the 126 non-technical exact filename+size review families in the v0.6.0 canonical baseline into a deterministic SHA-256 work queue.

Frozen denominator:
- exact filename+size families: 127
- technical `.DS_Store` family: 1 / 11 objects
- review families queued: 126
- objects queued: 258

Priority order:
1. `P0_MULTIPLICITY` — families with 3+ objects, because one hash pass can resolve more duplicate-copy candidates.
2. `P1_LOW_COST` — two-object families requiring <=10 MiB total reads.
3. `P2_MEDIUM_COST` — two-object families requiring <=100 MiB total reads.
4. `P3_HIGH_COST` — larger families.

Within a tier, families sort by total bytes to hash and then stable candidate-family ID.

For each family the generated CSV records all Drive IDs and parent paths and requests SHA-256 over every member.

Interpretation rule:
- all hashes equal => `BYTE_IDENTICAL_VERIFIED` for those physical files
- hashes differ => `NOT_BYTE_IDENTICAL`
- neither outcome automatically establishes canonical-work or edition identity

The queue therefore resolves physical-copy identity first while leaving semantic/work adjudication as a separate evidence gate.

The builder hard-fails unless it sees exactly 127 baseline families, exactly 126 `REVIEW_REQUIRED` families, exactly 258 queued objects, and exact agreement between family counts and object-ledger membership.
