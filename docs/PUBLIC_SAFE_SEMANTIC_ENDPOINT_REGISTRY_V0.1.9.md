# Public-safe semantic endpoint registry v0.1.9

This stage turns existing reviewed repository metadata into real typed graph endpoints before broader cross-source matching is enabled.

The deterministic registry includes:

- the 68 audited public-metadata topic labels;
- framework labels explicitly present in the validated Reddit metadata batch;
- the 13 Stage-B Drive publication families;
- canonical Big Questions and their unresolved status-preserving labels;
- deduplicated source records from canonical Big Question evidence batches.

Endpoint registration is not an edge, truth claim, evidence upgrade, rights grant, or global identity resolution. The registry contains zero edges. Evidence endpoints use `SOURCE_CLASSIFICATION_ONLY`; their inclusion never upgrades a claim to Established Evidence.

After installation, input changes create a draft registry pull request automatically. Only the repository owner may apply `human-reviewed`; exact-head validation and the packet-only diff restriction then control mechanical squash merge.
