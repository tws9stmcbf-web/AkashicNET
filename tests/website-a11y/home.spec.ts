import { test, expect } from '@playwright/test';

const locales = [['/', 'en'], ['/de', 'de'], ['/es', 'es'], ['/pt', 'pt-BR'], ['/fr', 'fr']];

for (const [route, language] of locales) {
  test(`server declares ${language} on ${route}`, async ({ request }) => {
    const response = await request.get(route, {
      headers: { 'x-akashicnet-document-language': 'fr', 'Accept-Language': 'fr' },
    });
    expect(response.status()).toBe(200);
    expect(await response.text()).toMatch(new RegExp(`<html[^>]* lang="${language}"`));
  });
  test(`document language and metadata on ${route} without JavaScript`, async ({ browser }) => {
    const context = await browser.newContext({ javaScriptEnabled: false });
    const page = await context.newPage();
    await page.goto(route);
    await expect(page.locator('html')).toHaveAttribute('lang', language);
    await expect(page.locator('link[rel="alternate"][hreflang="x-default"]')).toHaveAttribute('href', 'https://akashicnet.org/');
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', `https://akashicnet.org${route === '/' ? '/' : route}`);
    await context.close();
  });
}

test('locale links change the document language and restore English', async ({ page }) => {
  await page.goto('/');
  for (const [route, language] of [...locales.slice(1), locales[0]]) {
    await page.locator(`header nav a[href="${route}"]`).click();
    await expect(page.locator('html')).toHaveAttribute('lang', language);
  }
});

for (const width of [320, 375, 820, 821, 900, 1024, 1280, 1440]) {
  test(`all homepage locale controls are visible and keyboard reachable at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 1000 });
    await page.goto('/');
    const header = page.locator('.home-nav');
    if (width > 820) await expect(header.locator("nav a:visible")).toHaveCount(17);
    expect(await header.evaluate(el => el.scrollWidth <= el.clientWidth)).toBe(true);
    for (const [route] of locales) {
      const link = header.locator(`nav a[href="${route}"]`);
      await expect(link).toBeVisible();
      const box = await link.boundingBox();
      expect(box!.x).toBeGreaterThanOrEqual(0);
      expect(box!.x + box!.width).toBeLessThanOrEqual(width);
    }
    const reached = new Set<string>();
    for (let i = 0; i < 19; i++) {
      await page.keyboard.press('Tab');
      const href = await page.evaluate(() => document.activeElement?.closest('header nav a')?.getAttribute('href'));
      if (href) reached.add(href);
    }
    for (const [route] of locales) expect(reached.has(route)).toBe(true);
    const bounds = await header.boundingBox();
    const hero = await page.locator('.hero').boundingBox();
    expect(hero!.y).toBeGreaterThanOrEqual(bounds!.y + bounds!.height);
  });
}
