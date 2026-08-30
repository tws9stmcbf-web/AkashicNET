# AkashicNET rights review console policy v0.38

## Milestone
Provide one read-only review surface over the production rights ledger and real-candidate triage without granting the review surface authority to promote records.

## Separation of duties
The console can summarize rights state, current evidence, blockers and next review actions. It cannot mutate the production ledger, create `PUBLIC_VERIFIED`, change semantic decisions, or add records to the public manifest.

Every row exposes `can_auto_promote=false`. Promotion remains an explicit R0→R4 adjudication event governed by v0.30, and revocation remains governed by v0.32.

## Current state
The production ledger has no `PUBLIC_VERIFIED` records. v0.37 contributes three real R1 work-level candidates, all blocked on exact manifestation identification and all `UNKNOWN_UNVERIFIED`.

## Review actions
- `GATHER_RIGHTS_EVIDENCE`: provenance exists but work/rights evidence is insufficient.
- `ESTABLISH_EXACT_MANIFESTATION_R2`: work-level evidence exists, but the exact Drive manifestation is not identified.
- `REVERIFY_R4_AND_EXPIRY`: for a future `PUBLIC_VERIFIED` record, re-check authoritative evidence, corroboration, jurisdiction/scope and revocation/expiry state.

## Guardrails
- console is read-only
- automatic rights promotion: OFF
- truth inference: OFF
- scientific-evidence promotion: OFF
- accessibility cannot imply public permission
- provenance strength cannot imply public permission
- review queue priority cannot imply public permission
