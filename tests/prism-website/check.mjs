// Review-only harness: build a temporary snapshot and serve it on loopback.
// Nothing is deployed or uploaded. Build/type errors and browser failures fail CI.
import assert from 'node:assert/strict';
import {cp, mkdtemp, rm, writeFile, symlink, access, readdir, readFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawn} from 'node:child_process';
import net from 'node:net';
import {chromium} from 'playwright';
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const temp = await mkdtemp(path.join(tmpdir(), 'prism-review-'));
const next = path.join(here, 'node_modules/next/dist/bin/next');
let server, browser;
const routes = ['/faq', '/insights/akashicprism-big-questions', '/insights/akashicprism-plug-and-play-consciousness'];
const releaseSource = await readFile(path.join(root, 'website/lib/akashicomni-release.ts'), 'utf8');
const currentOmniVersion = releaseSource.match(/version:\s*"([^"]+)"/)[1];
const builtRoutes = new Set(['/', '/about', '/akashicomni', ...routes]);
// Existing logo is hash-only in website/assets/MANIFEST.md, not in the snapshot.
// Do not recover/publish an external binary merely to satisfy this review harness.
const snapshotOnlyMissingAssets = new Set(['/images/akashicnet-toroidal-love-logo.png']);
async function run(args) {
  await new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [next, ...args], {cwd: temp,
      env: {...process.env, NEXT_TELEMETRY_DISABLED: '1'}, stdio: 'inherit'});
    child.on('error', reject);
    child.on('exit', code => code === 0 ? resolve() : reject(new Error(`next ${args[0]} exited ${code}`)));
  });
}
try {
  await cp(path.join(root, 'website'), temp, {recursive: true});
  // The historical snapshot imports a Sites-vendored dependency it does not
  // contain. Restore that pinned, licensed dependency only inside this harness.
  await cp(path.join(here, 'vendor'), path.join(temp, 'vendor'), {recursive:true});
  await writeFile(path.join(temp,'postcss.config.mjs'),
    'export default {plugins:{"@tailwindcss/postcss":{}}};\n');
  // Build the six PR surfaces, plus their real imported components and libraries.
  // Other snapshot routes have unrelated build errors; no synthetic routes are used.
  for (const entry of await readdir(path.join(temp, 'app'), {withFileTypes:true}))
    if(entry.isDirectory() && !['about','akashicomni','faq','insights'].includes(entry.name))
      await rm(path.join(temp,'app',entry.name),{recursive:true});
  for (const entry of await readdir(path.join(temp,'app/insights'),{withFileTypes:true}))
    if(entry.isDirectory() && !['akashicprism-big-questions','akashicprism-plug-and-play-consciousness'].includes(entry.name))
      await rm(path.join(temp,'app/insights',entry.name),{recursive:true});
  await cp(path.join(here, 'package.json'), path.join(temp, 'package.json'));
  await symlink(path.join(here, 'node_modules'), path.join(temp, 'node_modules'), 'dir');
  await writeFile(path.join(temp, 'next.config.mjs'), 'export default {experimental:{cpus:2}};\n');
  await writeFile(path.join(temp, 'tsconfig.json'), JSON.stringify({compilerOptions:{
    target:'ES2020',lib:['dom','dom.iterable','esnext'],strict:true,noEmit:true,
    esModuleInterop:true,module:'esnext',moduleResolution:'bundler',resolveJsonModule:true,
    isolatedModules:true,jsx:'preserve',skipLibCheck:true,plugins:[{name:'next'}]},
    include:['next-env.d.ts','**/*.ts','**/*.tsx','.next/types/**/*.ts'],exclude:['node_modules']}));
  await run(['build']);
  const probe = net.createServer();
  await new Promise(resolve => probe.listen(0, '127.0.0.1', resolve));
  const port = probe.address().port;
  await new Promise(resolve => probe.close(resolve));
  const base = `http://127.0.0.1:${port}`;
  server = spawn(process.execPath, [next, 'start', '--hostname', '127.0.0.1', '--port', String(port)],
    {cwd:temp,env:{...process.env,NEXT_TELEMETRY_DISABLED:'1'},stdio:'inherit'});
  let ready = false;
  for (let attempt=0;attempt<100;attempt++) {
    try { if ((await fetch(base+'/faq')).ok) {ready=true;break;} } catch {}
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  assert(ready, 'loopback server did not start');
  browser = await chromium.launch({headless:true});
  for (const width of [1440, 821, 768, 390]) {
    const context = await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});
    // No third-party fetches, telemetry, embeds or source reads during review.
    await context.route('**/*', route => route.request().url().startsWith(base)
      ? route.continue() : route.abort());
    const page = await context.newPage();
    const failures=[];page.on('pageerror',error=>failures.push(error.message));
    for (const route of routes) {
      assert.equal((await page.goto(base+route)).status(),200,route);
      await page.waitForLoadState('networkidle');
      assert.equal(await page.locator('main').count(),1);
      assert.equal(await page.locator('h1').count(),1);
      assert.equal(await page.locator('html').getAttribute('lang'),'en');
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`${width}: page overflow ${route}`);
      const problems=await page.evaluate(()=>{
        const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);
        const errors=ids.filter((id,i)=>ids.indexOf(id)!==i).map(id=>'duplicate id '+id);
        for(const e of document.querySelectorAll('[aria-labelledby],[aria-describedby]'))
          for(const id of (e.getAttribute('aria-labelledby')||e.getAttribute('aria-describedby')).split(/\s+/))
            if(!document.getElementById(id))errors.push('unresolved accessible reference '+id);
        for(const e of document.querySelectorAll('img'))if(!e.hasAttribute('alt'))errors.push('image missing alt');
        return errors;
      });
      assert.deepEqual(problems,[],`${width}: ${route}`);
      const links=await page.locator('a[href]').evaluateAll(els=>els.map(e=>e.getAttribute('href')));
      for(const href of new Set(links)) {
        if(href.startsWith('#'))assert(await page.locator(`[id="${href.slice(1)}"]`).count(),href);
        if(href.startsWith('/')&&!href.startsWith('//')) {
          const url=new URL(href,base);
          const pathname=decodeURIComponent(url.pathname).replace(/\/$/,'')||'/';
          if(builtRoutes.has(pathname)) {
            assert((await context.request.get(url.href)).ok(),`broken internal link ${href}`);
          } else {
            // Unchanged destinations are checked against repository route sources.
            const destination=path.join(root,'website/app',pathname,'page.tsx');
            await access(destination);
            if(url.hash)assert((await readFile(destination,'utf8')).includes(decodeURIComponent(url.hash.slice(1))),`missing destination anchor ${href}`);
          }
          if(url.hash && builtRoutes.has(pathname)) {
            const check=await context.newPage();await check.goto(url.href);
            assert(await check.locator(`[id="${decodeURIComponent(url.hash.slice(1))}"]`).count(),`broken anchor ${href}`);
            await check.close();
          }
        }
      }
      for (const source of await page.locator('img[src]').evaluateAll(els=>els.map(e=>e.getAttribute('src'))))
        if(source.startsWith('/') && !snapshotOnlyMissingAssets.has(source))
          assert((await context.request.get(base+source)).ok(),`missing image ${source}`);
      if(route==='/faq') {
        const item=page.locator('#prism-architecture');
        await item.locator('summary').focus();await page.keyboard.press('Enter');
        assert(await item.evaluate(e=>e.open),'FAQ keyboard activation');
        assert.match(await item.innerText(),/proposed AkashicOMNI v0\.5\.0/);
        assert((await item.innerText()).includes(`v${currentOmniVersion} remains current`));
        await page.keyboard.press('Enter');assert.equal(await item.evaluate(e=>e.open),false);
      }
      if(route.includes('plug-and-play')) {
        const region=page.getByRole('region',{name:'Structure diagram; scroll horizontally on small screens'});
        await region.focus();const before=await region.evaluate(e=>e.scrollLeft);
        await page.keyboard.press('ArrowRight');await page.waitForTimeout(150);
        if(width<1000)assert(await region.evaluate(e=>e.scrollLeft)>before,'diagram keyboard scrolling');
        const text=page.getByText('Read the structure as text',{exact:true});
        await text.focus();await page.keyboard.press('Enter');
        assert.equal(await text.evaluate(e=>e.parentElement.open),true);
        assert.match(await text.locator('..').innerText(),/publication separately reviewed/);
      }
    }
    assert.deepEqual(failures,[],`browser errors at ${width}`);await context.close();
  }
  console.log('PASS: six PR surfaces build/types; PRISM/FAQ rendered anchors/assets/keyboard at 4 viewports; unchanged link destinations exist in repository; no publication approval');
} finally {
  await browser?.close();server?.kill('SIGTERM');await rm(temp,{recursive:true,force:true});
}
