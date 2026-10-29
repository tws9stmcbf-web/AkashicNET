import { Hono } from 'hono';
import { bodyLimit } from 'hono/body-limit';
import { AppError } from './policy.js';
import { createService, type Dependencies } from './service.js';
import { createMetadataScanner, type MetadataDependencies } from './metadata.js';

export const createApp = (deps: Dependencies, metadataDeps?: MetadataDependencies) => {
  const app = new Hono();
  const service = createService(deps);
  app.use('*', async (c, next) => { c.header('Cache-Control', 'no-store'); await next(); });
  app.use('/api/*', bodyLimit({ maxSize: 8192, onError: (c) => c.json({ error: 'Request is too large.' }, 413) }));
  app.onError((error, c) => {
    if (error instanceof AppError) return c.json({ error: error.message }, error.status);
    if (error instanceof SyntaxError) return c.json({ error: 'Invalid JSON request.' }, 400);
    console.error('Research Companion request failed.');
    return c.json({ error: 'The request could not be completed. Please try again later.' }, 503);
  });
  app.get('/api/session', async (c) => c.json(await service.session()));
  app.post('/api/preview', async (c) => c.json(await service.preview(await c.req.json<unknown>())));
  app.post('/api/publish', async (c) => c.json(await service.publish(await c.req.json<unknown>())));
  if (metadataDeps) {
    const scanner = createMetadataScanner(metadataDeps);
    app.get('/api/metadata/plan', async (c) => c.json(await scanner.plan()));
    app.post('/api/metadata/batch', async (c) => c.json(await scanner.batch(await c.req.json<unknown>())));
  }
  app.post('/internal/menu/companion', async (c) => {
    try {
      const post = await service.launcher();
      return c.json({ navigateTo: post.url });
    } catch (error) {
      return c.json({ showToast: error instanceof AppError ? error.message : 'Unable to open the companion.' });
    }
  });
  return app;
};
