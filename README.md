# 纵线突击（SuperMarine）

纵向单线对推的俯视角射击网页游戏，用 three.js 渲染。玩法参考 2008 年 Flash 游戏《Super Marine》（作者 aaldrin），代码、美术、音效全部原创，不使用原作任何素材。

## 当前状态

| 版本 | 状态 | 内容 |
| --- | --- | --- |
| v0.4 | 已完成 | 3 关、1440 宽战场、战术终端风格界面、星级与本地存档、教学提示 |
| v0.5 | 制作中 | 军械库、兵营与孵化池、新兵种、中线据点与野怪营地、新酸液弹、加血框、金手指 |
| v0.7 | 素材已就绪 | 写实风格模型、贴图、音效、音乐已在 `assets/`，待接入游戏 |

## 运行

用 Chrome 或 Edge 直接打开 `zongxian_demo.html`。需要联网（three.js 和字体从 CDN 加载）。

本地起一个静态服务器也可以：

```bash
npx serve .
```

## 操作

| 动作 | 键鼠 | 手机 |
| --- | --- | --- |
| 移动 | WASD / 方向键 | 左半屏拖动 |
| 射击 | 鼠标瞄准，按住左键（F 切换自动射击） | 自动瞄准射击 |
| 翻滚 | 空格 | 右下角按钮 |
| 手雷 | Q / 右键 | 右下角按钮 |
| 维修 | 靠近己方建筑按住 E | 维修按钮 |
| 暂停 | P / Esc | 切出页面自动暂停 |

## 目录

```
zongxian_demo.html     当前 Demo（单文件）
docs/设计文档.md        完整设计文档，所有需求和数值以它为准
docs/zongxian_map.png  战场布局缩略图
docs/素材清单.md        正式版需要的模型、贴图、音效、音乐清单与规格
assets/                正式素材：模型、贴图、音效、音乐（来源见 assets/CREDITS.md）
tools/assetgen/        生成自制模型、音效、音乐的脚本（Blender bpy + Python）
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
