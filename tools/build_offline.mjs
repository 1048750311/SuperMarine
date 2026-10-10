// Builds dist/纵线突击_离线版.html: one file, double-click to play, no server, no network.
// Game code + three.js are bundled into a classic script (esbuild via npx), every asset the game
// loads is embedded as a data URI and handed to the game through window.__BUNDLE.
//   node tools/build_offline.mjs
import { readFileSync, writeFileSync, mkdirSync, mkdtempSync, rmSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const html = readFileSync(join(root, 'zongxian_demo.html'), 'utf8');

// 1. game module -> classic script
const open = '<script type="module">', i0 = html.indexOf(open), i1 = html.indexOf('</script>', i0);
let code = html.slice(i0 + open.length, i1);
const lib = join(root, 'lib/three').replace(/\\/g, '/');
code = code.replace(/from 'three\/addons\/([^']+)'/g, (_, p) => `from '${lib}/addons/${p}'`);
const tmp = mkdtempSync(join(tmpdir(), 'zx-'));
writeFileSync(join(tmp, 'entry.js'), code);
execSync(`npx --yes esbuild@0.24.0 "${join(tmp, 'entry.js')}" --bundle --format=iife --minify --target=es2020 ` +
  `--alias:three="${lib}/three.module.min.js" --outfile="${join(tmp, 'bundle.js')}" --log-level=warning`, {stdio: 'inherit'});
const bundle = readFileSync(join(tmp, 'bundle.js'), 'utf8');
rmSync(tmp, {recursive: true, force: true});

// 2. assets, keyed exactly by the URL the game asks for
const B = {}, b64 = (f, mime) => `data:${mime};base64,` + readFileSync(join(root, f)).toString('base64');
const block = (a, b) => html.slice(html.indexOf(a), html.indexOf(b, html.indexOf(a)));
const models = [...block('const MODEL_FILES', '};').matchAll(/'((?:units|bugs|neutral|structures|ships|props)\/\w+)'/g)].map(m => m[1]);
for (const m of models){
  const p = `assets/web/models/${m}.gltf`, dir = dirname(p), j = JSON.parse(readFileSync(join(root, p), 'utf8'));
  for (const im of j.images || []) if (im.uri && !im.uri.startsWith('data:')) im.uri = b64(join(dir, im.uri), im.uri.endsWith('.png') ? 'image/png' : im.uri.endsWith('.jpg') ? 'image/jpeg' : 'image/webp');
  B[p] = 'data:application/json;base64,' + Buffer.from(JSON.stringify(j)).toString('base64');
}
const list = s => [...s.matchAll(/'(\w+)'/g)].map(m => m[1]);
const tex = [...list(block('const TEX_CORE', ';')), ...list(block('TEX_LATE =', ';').replace('TEX_LATE =', ''))];
for (const t of new Set(tex)) for (const k of ['color', 'normal', 'roughness']) B[`assets/web/textures/${t}/${k}.jpg`] = b64(`assets/web/textures/${t}/${k}.jpg`, 'image/jpeg');
for (const f of list(block('const SFX_FILES', ';'))) B[`assets/sfx/${f}.ogg`] = b64(`assets/sfx/${f}.ogg`, 'audio/ogg');
for (const f of ['menu', 'battle', 'boss']) B[`assets/music/${f}.ogg`] = b64(`assets/music/${f}.ogg`, 'audio/ogg');

// 3. page: same markup, no import map / file:// notice, bundle + assets inline
let out = html.slice(0, i0) + '<script>window.__BUNDLE=' + JSON.stringify(B) + ';</script>\n<script>' + bundle.replace(/<\/script/gi, '<\\/script') + '</script>' + html.slice(i1 + 9);
out = out.replace(/<script type="importmap">[\s\S]*?<\/script>\s*/, '');
out = out.replace(/<script>\s*\/\/ Opened by double-click[\s\S]*?<\/script>\s*/, '');
out = out.replace(/<title>([^<]*)<\/title>/, '<title>$1（离线版）</title>');
mkdirSync(join(root, 'dist'), {recursive: true});
const dst = join(root, 'dist', '纵线突击_离线版.html');
writeFileSync(dst, out);
console.log(`dist/纵线突击_离线版.html  ${(out.length / 1e6).toFixed(1)} MB  (${models.length} models, ${Object.keys(B).length} assets)`);
