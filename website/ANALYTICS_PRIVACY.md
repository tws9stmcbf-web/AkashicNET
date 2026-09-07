# AkashicNET.org analytics privacy boundary

AkashicNET.org supports optional privacy-preserving aggregate analytics solely as operational telemetry. Analytics are not scientific evidence, truth-inference input, or a measure of the validity of any claim.

## Activation

Repository support is implemented. Live collection remains off unless the deployment environment explicitly supplies `NEXT_PUBLIC_CLOUDFLARE_ANALYTICS_TOKEN`.

The token is not committed to the repository. Its absence renders no analytics component and is not treated as an error.

Live-beacon presence was not independently retrievable from the current verification environment. Retrieval failure is recorded as unverified, not as evidence that analytics are absent, broken, or disabled.

## Duplicate-beacon protection

The component checks the rendered document for an existing Cloudflare Web Analytics beacon before adding one. Hosting-layer injection therefore takes precedence, and the application does not intentionally add a second beacon.

## Permitted use

- Aggregate page views and page popularity
- Approximate aggregate visits reported by the provider
- Aggregate referral, country or region, device, browser, and operating-system summaries
- Explicitly documented aggregate navigation events, following a privacy review

## Prohibited use

- Advertising trackers or cross-site profiling
- Fingerprinting
- Session replay or invasive heat maps
- Visitor-level public logs
- Precise location tracking
- Sensitive-interest profiles
- Private Drive identifiers, paths, timestamps, or file-linked hashes
- Names, email addresses, private communications, or behavioural dossiers

## Governance

Absence of analytics data does not imply absence of interest. Public analytics must be labelled as measured operational telemetry with provider context and an observation window. Estimates and repository-derived or structural counts remain distinct classes.

Truth inference, rights promotion, scientific-evidence promotion, private Drive promotion, API-unverified Reddit promotion, circular confidence amplification, and forced BQ001 resolution remain off.
