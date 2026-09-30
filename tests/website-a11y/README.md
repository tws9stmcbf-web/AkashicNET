# Multilingual homepage regressions

Run `npm ci`, `npx playwright install --with-deps chromium`, `npm run build`,
then `npm test` in this directory. CI runs the same checks on the exact PR head.

The repository preserves a website snapshot without its hosting build manifest
or vendor CSS. `prepare.mjs` copies the real root layout, middleware, authored
CSS and five homepages into an isolated Next.js 15 fixture. Only unavailable
framework/vendor CSS imports are omitted. This is a focused production-build
and browser regression, not a full hosted-site build or deployment check.

Checks cover initial server HTML with JavaScript disabled, caller language
header override, canonical/alternate metadata, locale navigation and return
to English, and viewport/keyboard reachability at 320–1440px (including both
sides of 820px). The wrapped header must not overlap the hero.

The document-language fix requires the middleware and a request-rendered Next
root layout (`headers()`); it is not compatible with static HTML export. Any
future static-export host must use locale-specific root layouts instead.
English remains the technical reference; localized canonical URLs and reciprocal
hreflang metadata are unchanged. No automatic language redirects are introduced.
