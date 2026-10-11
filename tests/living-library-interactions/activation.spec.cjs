const { test, expect } = require('@playwright/test');

const map = '/living-library-map';
const futures = page => page.getByRole('button', { name: /^Possible Futures:/ });
const science = page => page.getByRole('button', { name: /^Science:/ });
const pointer = (node, type, pointerType) => node.dispatchEvent(type, {
  pointerType, pointerId: 1, isPrimary: true, bubbles: true,
});
const preview = async (page, node, label) => {
  await expect(page).toHaveURL(new RegExp(`${map}$`));
  await expect(node).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[aria-live="polite"]')).toContainText(label);
};

// Deliberately dispatch the compatibility sequence separately from native taps:
// old onMouseEnter behavior must not select a node or clear its touch arm.
async function compatibilityMouse(node) {
  await node.dispatchEvent('mouseover', { bubbles: true });
  await node.dispatchEvent('mouseenter');
  await node.dispatchEvent('mousedown', { bubbles: true });
  await node.dispatchEvent('mouseup', { bubbles: true });
}
async function touchStart(node) {
  await pointer(node, 'pointerover', 'touch');
  await pointer(node, 'pointerdown', 'touch');
  await node.focus();
}
async function touchFinish(node) {
  await pointer(node, 'pointerup', 'touch');
  await compatibilityMouse(node);
  await node.dispatchEvent('click', { detail: 1, bubbles: true });
}

test.beforeEach(async ({ page }) => {
  await page.goto(map);
  await expect(futures(page)).toBeVisible();
});

test('pen hover previews note and evidence before single-contact navigation', async ({ page }) => {
  const node = futures(page);
  await pointer(node, 'pointerover', 'pen');
  await preview(page, node, 'Possible Futures');
  await expect(page.locator('[aria-live="polite"]')).toContainText('Visionary futures and openly labelled scenarios.');
  await expect(page.locator('[aria-live="polite"]')).toContainText('Speculation');
  await pointer(node, 'pointerdown', 'pen');
  await node.focus();
  await pointer(node, 'pointerup', 'pen');
  await node.dispatchEvent('click', { detail: 1 });
  await expect(page).toHaveURL(/\/akashicvision$/);
});

for (const prior of ['none', 'mouse hover', 'keyboard focus']) {
  test(`native first tap previews and second tap navigates after ${prior}`, async ({ page }) => {
    const node = futures(page);
    if (prior === 'mouse hover') await node.hover();
    if (prior === 'keyboard focus') await node.focus();
    await node.tap();
    await preview(page, node, 'Possible Futures');
    await node.tap();
    await expect(page).toHaveURL(/\/akashicvision$/);
  });
}

test('compatibility mouse events neither preselect nor disarm a touch preview', async ({ page }) => {
  const node = futures(page);
  await touchStart(node);
  await compatibilityMouse(node);
  await expect(node).toHaveAttribute('aria-pressed', 'false');
  await expect(page.locator('[aria-live="polite"]')).toContainText('Choose a glowing node');
  await pointer(node, 'pointerup', 'touch');
  await node.dispatchEvent('click', { detail: 1 });
  await preview(page, node, 'Possible Futures');
  await compatibilityMouse(node);
  await touchStart(node);
  await touchFinish(node);
  await expect(page).toHaveURL(/\/akashicvision$/);
});

test('a different node requires its own first touch', async ({ page }) => {
  await futures(page).tap();
  await science(page).tap();
  await preview(page, science(page), 'Science');
  await science(page).tap();
  await expect(page).toHaveURL(/\/big-questions$/);
});

test('real mouse hover clears a previous touch arm', async ({ page }) => {
  const node = futures(page);
  await node.tap();
  await node.hover();
  await node.tap();
  await preview(page, node, 'Possible Futures');
  await node.tap();
  await expect(page).toHaveURL(/\/akashicvision$/);
});

test('cancelled touch does not arm a node or consume its next first tap', async ({ page }) => {
  const node = futures(page);
  await touchStart(node);
  await pointer(node, 'pointercancel', 'touch');
  await expect(page).toHaveURL(new RegExp(`${map}$`));
  await expect(node).toHaveAttribute('aria-pressed', 'false');
  await node.tap();
  await preview(page, node, 'Possible Futures');
  await node.tap();
  await expect(page).toHaveURL(/\/akashicvision$/);
});

test('cancellation clears pending touch modality before subsequent focus', async ({ page }) => {
  await touchStart(futures(page));
  await pointer(futures(page), 'pointercancel', 'touch');
  await science(page).focus();
  await preview(page, science(page), 'Science');
});

for (const key of ['Enter', 'Space']) {
  test(`native ${key} activation navigates once after touch preview`, async ({ page }) => {
    const node = futures(page);
    await node.tap();
    await preview(page, node, 'Possible Futures');
    await node.press(key);
    await expect(page).toHaveURL(/\/akashicvision$/);
  });
}

for (const state of ['pending touch', 'touch preview', 'cancelled touch']) {
  test(`detail-zero activation without a key event navigates after ${state}`, async ({ page }) => {
    const node = futures(page);
    await touchStart(node);
    if (state === 'touch preview') await touchFinish(node);
    if (state === 'cancelled touch') await pointer(node, 'pointercancel', 'touch');
    await node.dispatchEvent('click', { detail: 0, bubbles: true });
    await expect(page).toHaveURL(/\/akashicvision$/);
  });
}
