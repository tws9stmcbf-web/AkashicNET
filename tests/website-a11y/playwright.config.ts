import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: '.',
  testMatch: '*.spec.ts',
  workers: 2,
  use: { baseURL: 'http://127.0.0.1:3170' },
  webServer: {
    command: 'npx next start fixture -p 3170 -H 127.0.0.1',
    url: 'http://127.0.0.1:3170',
    reuseExistingServer: false,
  },
});
