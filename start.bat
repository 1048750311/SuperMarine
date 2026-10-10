@echo off
chcp 65001 >nul
cd /d "%~dp0"
where node >nul 2>nul
if not errorlevel 1 goto node
where python >nul 2>nul
if not errorlevel 1 goto python
echo 没有找到 Node.js 或 Python。
echo 请安装 Node.js（https://nodejs.org），或者直接双击 dist\纵线突击_离线版.html 玩离线版。
pause
goto :eof
:node
node tools\serve.mjs
pause
goto :eof
:python
start "" "http://localhost:8080/zongxian_demo.html"
python -m http.server 8080
