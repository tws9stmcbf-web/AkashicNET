import { serve } from '@hono/node-server';
import { context, createServer, getServerPort, reddit, redis } from '@devvit/web/server';
import { createApp } from './app.js';
import type { Dependencies } from './service.js';

const deps: Dependencies = {
  async actor() {
    const { userId, postId, subredditName } = context;
    let canPublish = false;
    if (userId && subredditName) {
      const username = await reddit.getCurrentUsername();
      if (username) {
        const moderators = await reddit.getModerators({ subredditName, username }).all();
        canPublish = moderators.some((mod) => mod.username.toLowerCase() === username.toLowerCase() &&
          (mod.moderatorInfo.modPermissions.includes('all') || mod.moderatorInfo.modPermissions.includes('posts')));
      }
    }
    return { userId, postId, subredditName, canPublish };
  },
  async flairs(subredditName) {
    return (await reddit.getPostFlairTemplates(subredditName)).map((flair) => ({ id: flair.id, text: flair.text }));
  },
  store: {
    get: (key) => redis.get(key),
    async set(key, value, options) {
      const result = await redis.set(key, value, {
        ...(options?.onlyIfAbsent ? { nx: true } : {}),
        ...(options?.ttlSeconds ? { expiration: new Date(Date.now() + options.ttlSeconds * 1000) } : {}),
      });
      return result === 'OK';
    },
  },
  async publish(snapshot, snapshotId, subredditName) {
    const post = await reddit.submitCustomPost({
      subredditName, title: snapshot.title,
      ...(snapshot.flair ? { flairId: snapshot.flair.id } : {}),
      entry: 'default',
      postData: { kind: 'article', snapshotId },
      textFallback: { text: snapshot.body },
    });
    return { postId: post.id, url: `https://www.reddit.com/r/${subredditName}/comments/${post.id.substring(3)}/` };
  },
  async createLauncher(subredditName) {
    const post = await reddit.submitCustomPost({
      subredditName, title: 'AkashicNET Research Companion',
      postData: { kind: 'launcher' },
      textFallback: { text: 'Explore public AkashicNET articles and their evidence boundaries at https://akashicnet.org. Moderators can open this app to preview and publish a research discussion. The app does not independently appraise scientific evidence.' },
    });
    return { postId: post.id, url: `https://www.reddit.com/r/${subredditName}/comments/${post.id.substring(3)}/` };
  },
  snapshotId: () => typeof context.postData?.snapshotId === 'string' ? context.postData.snapshotId : undefined,
};

const app = createApp(deps);
serve({ fetch: app.fetch, createServer, port: getServerPort() });
