# 纵线突击（SuperMarine）

纵向单线对推的俯视角射击网页游戏，用 three.js 渲染。玩法参考 2008 年 Flash 游戏《Super Marine》（作者 aaldrin），代码、美术、音效全部原创，不使用原作任何素材。

## 当前状态

| 版本 | 状态 | 内容 |
| --- | --- | --- |
| v0.4 | 已完成 | 3 关、1440 宽战场、战术终端风格界面、星级与本地存档、教学提示 |
| v0.5 | 进行中 | 已完成：高清模型、PBR 地面、采样音效和音乐，单位 AI 重写，帧率优化；兵营与兵营面板、孵化池；人类新兵种（火焰兵、火箭兵、医疗兵、步行机甲）、虫族新兵种（自爆虫、飞虫、迫击虫、刺镰虫）、中立野怪（掘地虫群、沙原巨兽）；金手指面板。待做：军械库、中线据点与野怪营地、新酸液弹、加血框 |

## 运行

三种方式，画面和功能完全一样，都不需要联网（只有标题字体走 Google Fonts，连不上会自动换成系统字体）：

| 方式 | 怎么做 | 适合 |
| --- | --- | --- |
| 离线单文件版 | 双击 `dist/纵线突击_离线版.html` | 直接玩、发给别人玩 |
| 启动脚本 | Windows 双击 `start.bat`；macOS 双击 `start.command`；Linux 运行 `sh start.command` | 改代码后马上看效果 |
| 自己起服务器 | 在仓库目录运行 `node tools/serve.mjs`、`npx serve .` 或 `python -m http.server`，再打开 `zongxian_demo.html` | 同上 |

启动脚本需要电脑上装了 Node.js 或 Python（装过 Claude Code 就有 Node.js）。直接双击 `zongxian_demo.html` 不行：浏览器不允许本地网页读取旁边的代码和素材文件，页面会提示你改用上面的方式。

**拿到最新版**：在已经克隆的仓库目录里运行 `git pull`。

**改了游戏之后**重新生成离线版：`node tools/build_offline.mjs`（需要联网下载一次打包工具 esbuild）。

画质在「设置」里调：高、中、低。帧率不够时游戏会自动降低渲染分辨率；打开「显示帧率」可以看到当前帧率和分辨率。

## 操作

| 动作 | 键鼠 | 手机 |
| --- | --- | --- |
| 移动 | WASD / 方向键 | 左半屏拖动 |
| 射击 | 鼠标瞄准，按住左键（F 切换自动射击） | 自动瞄准射击 |
| 翻滚 | 空格 | 右下角按钮 |
| 手雷 | Q / 右键 | 右下角按钮 |
| 维修 | 靠近己方建筑按住 E | 维修按钮 |
| 兵营 | 站进兵营前的黄框：1–5 选兵种，U 升级，T 部队训练，R 重建 | 站进黄框后点面板 |
| 金手指 | 设置里打开「允许金手指」，再按 ` 键 | 暂停菜单里的「金手指」按钮 |
| 暂停 | P / Esc | 切出页面自动暂停 |

## 目录

```
zongxian_demo.html     当前 Demo（游戏代码都在这一个文件里）
dist/纵线突击_离线版.html  离线单文件版：代码、three.js 和全部素材打包在一起，双击就能玩
lib/three/             three.js r160（本地副本，不依赖 CDN）
start.bat / start.command  一键启动本地服务器并打开游戏
docs/设计文档.md        完整设计文档，所有需求和数值以它为准
docs/设计文档.docx      同一份设计文档的 Word 版（由 .md 导出）
docs/zongxian_map.png  战场布局缩略图
docs/素材清单.md        正式版需要的模型、贴图、音效、音乐清单与规格
assets/                正式素材：模型、贴图、音效、音乐（来源见 assets/CREDITS.md）
assets/web/            游戏实际加载的素材包：模型贴图缩到 256/512 像素、地面贴图 1024 像素
tools/assetgen/        生成自制模型、音效、音乐的脚本（Blender bpy + Python）
tools/build_web_assets.sh  从 assets/ 重新生成 assets/web/
tools/build_offline.mjs    生成离线单文件版
tools/serve.mjs            本地静态服务器（启动脚本调用它）
```

## 用 Claude Code 继续开发

设计文档第 10 部分有完整的开发提示词，在 VS Code 里打开本仓库后粘贴给 Claude Code 即可。

## 重新生成自制素材

```bash
pip install bpy numpy scipy          # bpy 是 Blender 的 Python 模块，需要 Python 3.13
python tools/assetgen/marine.py -- out/      # 人类单位
python tools/assetgen/bugs.py -- out/        # 甲虫、重甲虫、喷吐虫、机甲、炮塔
python tools/assetgen/bugs2.py -- out/       # 其余虫族和中立野怪
python tools/assetgen/structures.py -- out/  # 建筑和岩石
python tools/assetgen/sfx.py out/sfx         # 音效（需要 ffmpeg）
python tools/assetgen/music.py out/music     # 音乐（需要 ffmpeg）
```

改了 `assets/models` 或 `assets/textures` 之后，重新生成游戏用的素材包：

```bash
sh tools/build_web_assets.sh   # 需要 Node.js 和 Python（Pillow）
```
