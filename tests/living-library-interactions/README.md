# Living Library interaction regression

Run from this directory:

```sh
npm ci
npx playwright install --with-deps chromium
npm test
```

The harness bundles and renders the actual `website/app/living-library-map/page.tsx`
and its CSS with React. No handlers are copied or mocked. Assertions observe the
rendered preview, `aria-pressed`, and actual destination navigation. The test server
serves placeholder destination documents; it does not build the full website.

Chromium supplies native touchscreen tap sequences and native Enter/Space button
activation. Explicit DOM events cover pen hover, compatibility mouse ordering,
pointer cancellation, and an assistive-technology-style `detail === 0` click without
a key event. These synthetic sequences do not constitute physical stylus/hybrid
hardware or VoiceOver/TalkBack acceptance testing, which remains separate.

The dedicated touch arm must stay independent of the hover/focus preview. The
suite checks first-touch preview even on a previously hovered/focused node,
second-touch navigation, per-node arming, and clearing an arm on real mouse hover.
A cancelled initial contact must neither navigate nor arm the next first touch,
and must clear stale touch modality before subsequent focus.

CI installs locked dependencies and verifies the checkout against the exact PR
head before executing the suite. The former Python source-string assertions have
been removed; this browser suite is their replacement.
