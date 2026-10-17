# TSC2026 latest-news alignment

Checked 16 October 2026. GitHub baseline: `9cf967a7a9ed7921e6220189e46f4dc51c845a88`.

## Publishing authority

`website/README.md` identifies this directory as a historical website snapshot and ChatGPT Sites as the hosting source of truth. The connected AkashicNET Public Portal owns `https://akashicnet.org`; its inspected production version was 993, from source commit `2fd1c24d0f23de8a885eb3e92a25cf82544d85d1`.

The live source contains the TSC2026 routes. This GitHub snapshot does not. Consequently, GitHub news entries use absolute canonical URLs; merging this change does not deploy the public portal.

The live homepage already exposed conference companions through its scrolling highlights. Its separate static highlight cards were older. Live ticker inputs are `lib/recent-page-highlights.ts` → `lib/page-highlights.ts` → `app/NewsTicker.tsx` and `app/InsightsTicker.tsx`. The conference tickers also consume `recentPageHighlights`. The homepage card collection is in `app/page.tsx`.

The curated records now live in `lib/tsc-research-highlights.ts` on Sites, mirrored in `website/lib/tsc-research-highlights.ts` here. Each publishing source must be updated and validated separately; there is no automatic GitHub-to-Sites deployment claim.

## Selected public companions

Dates below describe the AkashicNET publication day in **America/Los_Angeles**, the conference timezone. First-addition source history and a successful same-day deployment support each date. They are not highlight dates, conference-wide dates or dates of scientific discovery.

| Publication | Public URL | Publication day | Successful deployed source |
| --- | --- | --- | --- |
| Conscious Beings, Living Worlds | https://akashicnet.org/tsc2026/conscious-beings-living-worlds | 16 Oct 2026 | Version 990, `1cb48def053cda7ab9fab52ef3a7bbebfd25fa03`; succeeded 16 Oct 08:03 UTC |
| Giulio Tononi: Being, Doing and Consciousness | https://akashicnet.org/tsc2026/giulio-tononi | 15 Oct 2026 | Version 984, `16db966ffc7ceb5ef487a85050eb877bb3063220`; succeeded 15 Oct 23:35 UTC |
| Donald Hoffman: From Observer Windows to Testable Predictions | https://akashicnet.org/tsc2026/donald-hoffman | 15 Oct 2026 | Version 980, `bf44bcfa4f1f3787262e33891a23f6e1c37f16e4`; succeeded 15 Oct 19:49 UTC |
| The Kite of Consciousness: Jonathan Schooler at TSC2026 | https://akashicnet.org/tsc2026/jonathan-schooler | 15 Oct 2026 | Version 978, `43e26a1b69125df03d3abd4f1b6cf5e2d74ec1f6`; succeeded 15 Oct 19:24 UTC |
| When Thoughts Become Thinkers: Michael Levin Follow-Up | https://akashicnet.org/tsc2026/michael-levin | 15 Oct 2026 | Version 977, `ec08402dadb8ee3e2d6dddf5ca5d678dfa06f9be`; succeeded 15 Oct 18:03 UTC |

Selection favours substantial source-linked explanations, research questions and explicit limits, with one synthesis linking the conference themes. Summaries distinguish theory-dependent conclusions, mathematical results, interpretation and proposed experiments. Publication does not imply speaker endorsement or scientific validation.

## Availability and loading checks

Anonymous HTTP GETs returned 200 for all five companions and for `/tsc2026/hide-saegusa`. The six HTML responses were approximately 42–86 KB and took 3.8–4.5 seconds from this environment in one batch. This is not a browser performance benchmark.

All seven distinct image `src` URLs used on these pages returned 200. The previously reported `conscious-beings-living-worlds` page already uses responsive WebP images with JPEG fallbacks, explicit dimensions, an eager prioritised hero and a lazy secondary image. Both JPEGs and all four WebP variants returned 200. The hero variants are approximately 99 KB (768 px WebP), 206 KB (1280 px WebP) and 238 KB (JPEG). The earlier image fix was retained.

Web-search fetching failed for the public pages; direct anonymous HTTP fetching succeeded. Browser rendering, interaction and device-specific loading remain unverified in this environment. No claim of a complete performance fix is made.

## Durable GitHub change and validation

- Add the shared curated records to the latest ticker and homepage highlights.
- Edit `website/status-templates/home.tsx.in` and regenerate `website/app/page.tsx` with `python scripts/validate_public_status_consistency_v016.py --write`.
- Preserve the existing seven latest ticker links, six archive links, older highlight cards, navigation, status values, focus pause, manual controls and CSS.
- Keep external TSC2026 links and artwork canonical rather than inventing local routes or copying the live articles into this snapshot.

Required source checks passed: v0.16 generated-status consistency, v0.15 status contract, evidence taxonomy, public route QA, and all 12 current-status regression tests. Route QA explicitly leaves manual visual checks outstanding.

Live publication and this GitHub review are separate operations. The change description should record the new Sites version when deployment completes; this audit's version 993 is the inspected baseline.
