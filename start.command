#!/bin/sh
# macOS: double-click to play. Linux: sh start.command
cd "$(dirname "$0")"
if command -v node >/dev/null 2>&1; then exec node tools/serve.mjs; fi
if command -v python3 >/dev/null 2>&1; then
  (sleep 1; open "http://localhost:8080/zongxian_demo.html" 2>/dev/null || xdg-open "http://localhost:8080/zongxian_demo.html") &
  exec python3 -m http.server 8080
fi
echo "没有找到 Node.js 或 Python。请安装 Node.js（https://nodejs.org），或者直接打开 dist/纵线突击_离线版.html。"
