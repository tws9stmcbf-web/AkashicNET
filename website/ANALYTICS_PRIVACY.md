# AkashicNET.org analytics privacy boundary

This website integration implements the privacy-first telemetry policy in `references/community/public-observability-contract-v0.15.json`.

## Activation

Cloudflare Web Analytics is **off by default**. The application emits no analytics beacon unless the deployment environment supplies `NEXT_PUBLIC_CLOUDFLARE_ANALYTICS_TOKEN`. No token belongs in source control.

Before activation, verify the deployed page contains exactly one analytics beacon. Do not combine this component with provider-side automatic beacon injection.

## Permitted purpose

Aggregate operational telemetry may be used to understand whether public pages are reached and which public pathways are useful. Examples include aggregate page views, approximate visits, broad acquisition channels, and provider-supplied country, device, browser, or operating-system summaries.

Analytics are operational telemetry only. They are not scientific evidence, truth-inference input, proof of public interest, or a substitute for repository-derived provenance.

## Prohibited collection and use

Do not add or derive:

- names, email addresses, account identities, or private communications;
- cross-site advertising identifiers or behavioural profiles;
- fingerprinting, session replay, invasive heat maps, or precise GPS location;
- visitor-level public logs;
- private Drive identifiers, paths, timestamps, or file-linked hashes;
- medical, psychedelic, spiritual, political, or other sensitive-interest profiles.

Any new provider, custom event tracking, or expansion beyond aggregate telemetry requires a privacy review and an update to the canonical contract.

## Reporting

Public analytics figures must be labelled **measured analytics**, name their provider/context, include an observation window, and be aggregated sufficiently to avoid identifying individual visitors. Absence of telemetry must not be interpreted as absence of interest or evidence.

The sealed v0.14 baseline, v0.15 release history, public-data boundary, evidence classifications, uncertainty policy, and all promotion controls remain unchanged.
