const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: '.',
  testMatch: '*.spec.cjs',
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: 1,
  use: { baseURL: 'http://127.0.0.1:4173', hasTouch: true },
  webServer: {
    command: 'node server.mjs',
    url: 'http://127.0.0.1:4173/living-library-map',
    reuseExistingServer: false,
  },
});
