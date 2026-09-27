# BQ001 comparison schema contract

JSON Schema accepts arbitrary annotation keywords. That permissiveness is not the
metadata policy for this governed comparison packet.

The comparison validator now requires the exact reviewed schema structure,
compared through a canonical structural SHA-256 in validator code. This covers
property names, keywords, constraints, constants and reference targets. A change
to that structure requires an explicit reviewed validator update. Packet fields
remain closed by the existing semantic validator and schema.

Only `title` and `description` may vary as annotations. Each must be a plain string
of 1 to 512 characters, and all such strings undergo privacy screening both
individually and as one ordered sequence. Custom annotation keys, maps and arrays
are rejected, even when their contents appear harmless. This prevents private
locators or metadata labels from being hidden in arbitrary annotation key trees.

Existing privacy scanners remain defense in depth for permitted packet/schema
content. They are not claimed to reconstruct every possible steganographic JSON
encoding. The sibling-key example from review is rejected by the closed schema
contract; this change does not claim to fix the general-purpose scalar scanner
for all arbitrary objects. Reopening schema extensions requires a new design and
review, not an exception to this gate.

Earlier regression tests are preserved in
`docs/review-evidence/comparison-privacy-tests-before-contract.py.txt`. Active
regressions continue to require rejection; schema payloads may now be rejected
by the structural gate before a particular privacy pattern is evaluated.

BQ001 stays UNRESOLVED, accepted edges stay zero and Reddit access stays HOLD.
No packet, schema, governed input pin, evidence record, release, publication or
promotion decision changes with this validator redesign.
