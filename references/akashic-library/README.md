# Akashic Library private-source boundary

This directory documents the interface to the private Google Drive corpus. It
must not contain live provider identifiers or object-level metadata.

The public repository may contain:

- reusable metadata-processing code;
- schemas and synthetic examples;
- aggregate counts and validation results;
- records independently verified as public and cleared for publication.

The private data layer must contain:

- Drive IDs and URLs;
- filenames and folder paths;
- timestamps and file sizes;
- file-linked hashes;
- raw census, canonicalisation and rights-review ledgers;
- credentials, tokens and checkpoints.

Discovery or shared access is not publication permission. An object may enter a
public manifest only after its visibility is independently verified, its PII
scan passes, its rights state is reviewed and its public-manifest decision is
explicitly accepted.
