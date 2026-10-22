# AKN24 homepage: authoritative Sites source review

The editable and deployed homepage belongs to ChatGPT Sites. GitHub's `website/` is a historical review snapshot, generated from `website/status-templates/home.tsx.in`; merging this PR does not deploy the site.

This PR records the exact patch implemented in the authoritative repository. It does not overwrite the older homepage or supersede open PR #403.

## Review this change

- Baseline Sites commit: `b37723f30fb68e102f4e104911e9145d9b5d9867` (version 1072).
- Implementation commit: `4cd6fa6b9f468e490e36b9f8eb54b0b8fa53caac`.
- Source patch: [source.patch](source.patch). Paths are relative to the Sites checkout.
- Source project: `appgprj_6a93c8c170388191b89b2d90a544c0b1`.
- Public site: https://akashicnet.org.

Apply only to the matching Sites baseline. In an isolated checkout, first run `git apply --check source.patch`. Do not apply this patch directly to GitHub's `website/` tree.

## Changes

The homepage already had branding, functional public page search, tickers and opt-in radio near the top. This work reuses those components, promotes the existing cinematic Pachamama newsroom artwork, adds a finite three-report evidence desk and extends search into the report bodies. Report dates, source links, evidence/status wording, uncertainty and private/unlisted discovery exclusions are retained.

The explicit featured-report adapter reuses the already-published 21 October source records. It does not infer evidence classifications or scrape protected material. Search scope, clear-search focus and result count announcements support accessible discovery. Existing radio consent and ticker motion controls are retained.

## Validation

TypeScript checking passed. The initial production build, public route/media/sitemap gates, four focused search tests and two rendered page tests passed. Final reconciliation/build and deployment status are recorded separately in `deployment.json` when complete.

The managed browser preview timed out twice during Vite startup. Phone/tablet visual appearance, keyboard interaction and reduced-motion behaviour were not verified in a browser. Responsive CSS and retained controls are source-level safeguards, not proof of browser QA.

Historical source dates are preserved using full Git history. The newer QCI source update is included as the baseline. The patch does not change research findings or publication claims.

## Maintenance

Update `lib/newsroom-stories.mjs` when changing the featured editorial edition; retain original source/correction/bulletin labels and verify the target anchors. The normal Sites build regenerates the public search index and page-history ledger. Use complete Git history for that generator.
