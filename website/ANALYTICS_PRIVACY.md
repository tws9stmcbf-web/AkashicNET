# AkashicNET.org analytics privacy boundary

AkashicNET.org may use privacy-preserving aggregate website analytics solely to understand whether public knowledge pages are being reached and which public pathways are useful.

## Provider

The repository integration supports Cloudflare Web Analytics. The beacon is disabled unless the deployment environment provides `NEXT_PUBLIC_CLOUDFLARE_ANALYTICS_TOKEN`. No analytics token is committed to source control.

## Intended aggregate metrics

- Page views and page popularity
- Approximate unique visits as reported by the analytics provider
- Referring sites / acquisition channels at aggregate level
- Country or region aggregates where provided by the analytics service
- Device, browser and operating-system aggregates
- Aggregate navigation/outbound-link patterns only when explicitly configured and documented

## Not collected by AkashicNET application code

- Names, email addresses or account identities
- Form profiles or behavioural dossiers
- Cross-site advertising identifiers
- Fingerprinting identifiers
- Precise GPS location
- Private Drive identifiers, paths, timestamps or file-linked hashes
- Psychedelic, medical, spiritual, political or other sensitive-interest profiles
- Content of private communications

## Rules

1. Analytics must remain aggregate and privacy-preserving.
2. Do not add advertising trackers, cross-site profiling, fingerprinting, session replay or invasive heat-map tooling.
3. Do not expose visitor-level logs publicly.
4. Any future analytics provider or event-tracking expansion requires a privacy review and an update to this document.
5. Website analytics are operational telemetry, not scientific evidence and not input to AkashicNET truth inference.
6. Absence of analytics data must not be interpreted as absence of public interest or evidence.
7. Public statistics should be reported only at sufficiently aggregated levels to avoid identifying individual visitors.

## Activation state

Repository support: IMPLEMENTED.

Live collection: OFF by default and activates only after the deployment environment is configured with the analytics token and the deployed site is verified to load the privacy-safe beacon.
