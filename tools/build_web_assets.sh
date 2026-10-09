#!/bin/sh
# Builds the in-game asset pack (assets/web/) from the source assets (assets/models, assets/textures).
# Needs: Node.js (npx @gltf-transform/cli) and Python 3 with Pillow.
#   sh tools/build_web_assets.sh
set -e
cd "$(dirname "$0")/.."
GT="npx --yes @gltf-transform/cli@4.5.1"
OUT=assets/web
mkdir -p $OUT/models $OUT/textures
for f in assets/models/*/*.glb; do
  cat=$(basename "$(dirname "$f")"); name=$(basename "$f")
  case $cat in structures|ships) size=512 ;; *) size=256 ;; esac
  mkdir -p $OUT/models/$cat
  tmp=$OUT/models/$cat/.tmp_$name
  $GT resize "$f" "$tmp" --width $size --height $size >/dev/null
  $GT dedup "$tmp" "$tmp.glb" >/dev/null
  # .gltf + separate textures: plain web file types, so any static host (or a claude.ai artifact) can serve them
  python3 tools/glb_to_gltf.py "$tmp.glb" "$OUT/models/$cat/${name%.glb}.gltf"
  rm -f "$tmp" "$tmp.glb"
  echo "$cat/$name -> ${size}px"
done
python3 - <<'PY'
import os
from PIL import Image
src, out = 'assets/textures', 'assets/web/textures'
for d in sorted(os.listdir(src)):
    p = os.path.join(src, d)
    if not os.path.isdir(p): continue
    os.makedirs(os.path.join(out, d), exist_ok=True)
    for m, q in (('color', 84), ('normal', 90), ('roughness', 80)):
        im = Image.open(os.path.join(p, m + '.jpg'))
        im = im.convert('L') if m == 'roughness' else im.convert('RGB')
        im = im.resize((1024, 1024), Image.LANCZOS)
        im.save(os.path.join(out, d, m + '.jpg'), quality=q, optimize=True, progressive=False)
    print('textures/' + d)
PY
du -sh $OUT
