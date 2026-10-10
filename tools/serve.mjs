// Tiny static server for local play: node tools/serve.mjs  (no npm install needed)
// Serves the repository folder and opens the game in the default browser.
import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { extname, join, normalize, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { exec } from 'node:child_process';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const TYPES = {'.html':'text/html; charset=utf-8', '.js':'text/javascript', '.mjs':'text/javascript', '.json':'application/json', '.gltf':'model/gltf+json',
  '.glb':'model/gltf-binary', '.webp':'image/webp', '.jpg':'image/jpeg', '.png':'image/png', '.ogg':'audio/ogg', '.css':'text/css', '.md':'text/plain; charset=utf-8'};
const server = http.createServer(async (req, res) => {
  try {
    let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    if (p === '/') p = '/zongxian_demo.html';
    const f = normalize(join(root, p));
    if (!f.startsWith(root)) { res.writeHead(403); return res.end(); }
    if (!(await stat(f)).isFile()) throw 0;
    res.writeHead(200, {'Content-Type': TYPES[extname(f).toLowerCase()] || 'application/octet-stream', 'Cache-Control': 'no-cache'});
    res.end(await readFile(f));
  } catch { res.writeHead(404); res.end('not found'); }
});
function listen(port){
  server.once('error', e => { if (e.code === 'EADDRINUSE' && port < 8100) listen(port + 1); else throw e; });
  server.listen(port, '127.0.0.1', () => {
    const url = `http://localhost:${port}/zongxian_demo.html`;
    console.log(`\n  纵线突击已启动： ${url}\n  关掉这个窗口就会停止游戏服务器。\n`);
    const open = process.platform === 'win32' ? `start "" "${url}"` : process.platform === 'darwin' ? `open "${url}"` : `xdg-open "${url}"`;
    exec(open, () => {});
  });
}
listen(8080);
