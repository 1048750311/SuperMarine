# 素材来源与授权

预览图：`previews/models.jpg`（全部模型）、`previews/textures.jpg`（地面贴图）。

## 本项目自制（可随意使用、修改）

以下素材由 `tools/assetgen/` 里的脚本生成：模型用 Blender（bpy）程序化建模、绑定节点并制作动画，音效和音乐用 Python 合成。模型表面使用 ambientCG 的 CC0 贴图（见下）。改脚本后重新运行即可重新生成。

| 类别 | 文件 | 动画 |
| --- | --- | --- |
| 人类单位 | `models/units/` marine、player、flamer、rocketeer、medic、mech | idle、run、shoot、die |
| 虫族 | `models/bugs/` beetle（甲虫）、brute（重甲虫）、spitter（喷吐虫）、bomber（自爆虫）、flyer（飞虫）、mortar（迫击虫）、lancer（刺镰虫）、queen（虫后） | idle、run、attack、die（虫后另有 summon） |
| 中立野怪 | `models/neutral/` burrower（掘地虫）、behemoth（沙原巨兽） | idle、run、attack、die |
| 建筑 | `models/structures/` base、barracks、armory、outpost、tower（人类炮塔，炮台节点名 `turret_head`）、nest、hatchery、bug_tower | 部分有 idle（雷达旋转、核心起伏） |
| 岩石 | `models/props/rock_1` – `rock_6` | — |
| 音效 | `sfx/` 共 30 个 | — |
| 音乐 | `music/` menu（55 秒）、battle（69 秒）、boss（58 秒），均可循环 | — |

模型约定：1 单位 = 游戏里 1 像素，Y 轴朝上，正面朝 +X，原点在脚底中心。

## 第三方素材

| 文件 | 原始素材包 | 作者 | 授权 | 主页 |
| --- | --- | --- | --- | --- |
| `models/props/prop_*.glb`、`column_pipes.glb` | Modular SciFi MegaKit（免费版） | Quaternius | CC0 1.0 | https://quaternius.com |
| `models/ships/` imperial、insurgent、spitfire（运输机候选） | Ultimate Spaceships Pack | Quaternius | CC0 1.0 | https://quaternius.com |
| `textures/*`、自制模型的表面贴图 | ambientCG 材质（编号见下） | ambientCG | CC0 1.0 | https://ambientcg.com |

地面贴图编号：sand = Ground005，sand_warm = Ground025，scorched = Ground023，gravel = Gravel006，creep = Rock007，metal_floor = MetalPlates001，metal_dark = MetalPlates006。

自制模型用到的贴图：Metal010、Metal015、Metal017、Metal019、Leather008、Leather009、Rock012、Rock013、Rock016、Concrete002、Concrete007、MetalPlates001、MetalPlates004（已去色并缩小到 512 像素，放在 `tools/assetgen/textures/`）。

## 获取途径说明

- Quaternius Modular SciFi MegaKit、ambientCG 材质：从 jgengine 项目在 GitHub Releases 的镜像下载（https://github.com/Noisemaker111/jgengine/releases/tag/packs）。
- Quaternius Ultimate Spaceships Pack：来自 https://github.com/Malcolmnixon/Quaternius-Ultimate-Spaceships-Pack 的 .blend 文件，用 Blender 转成 .glb。

原始授权均为 CC0，与官网版本相同。
