"""Repack a .glb as .gltf: textures become separate .webp/.png/.jpg files next to it,
geometry stays inside the .gltf as a base64 buffer. Usage: python glb_to_gltf.py in.glb out.gltf"""
import base64, json, os, struct, sys

src, dst = sys.argv[1], sys.argv[2]
b = open(src, 'rb').read()
assert b[:4] == b'glTF'
off, js, bin_ = 12, None, b''
while off < len(b):
    ln, typ = struct.unpack('<II', b[off:off + 8]); chunk = b[off + 8:off + 8 + ln]
    if typ == 0x4E4F534A: js = json.loads(chunk)
    elif typ == 0x004E4942: bin_ = chunk
    off += 8 + ln
stem = os.path.splitext(os.path.basename(dst))[0]
outdir = os.path.dirname(dst) or '.'
ext = {'image/webp': 'webp', 'image/png': 'png', 'image/jpeg': 'jpg'}
img_views = set()
for i, im in enumerate(js.get('images', [])):
    if 'bufferView' not in im: continue
    bv = js['bufferViews'][im['bufferView']]
    data = bin_[bv.get('byteOffset', 0):bv.get('byteOffset', 0) + bv['byteLength']]
    name = f"{stem}_{i}.{ext.get(im.get('mimeType'), 'bin')}"
    open(os.path.join(outdir, name), 'wb').write(data)
    img_views.add(im.pop('bufferView')); im.pop('mimeType', None); im['uri'] = name
# repack the remaining buffer views
remap, views, buf = {}, [], bytearray()
for i, bv in enumerate(js.get('bufferViews', [])):
    if i in img_views: continue
    o = bv.get('byteOffset', 0); data = bin_[o:o + bv['byteLength']]
    while len(buf) % 4: buf.append(0)
    nb = dict(bv); nb['byteOffset'] = len(buf); nb['buffer'] = 0
    buf += data; remap[i] = len(views); views.append(nb)
js['bufferViews'] = views
for a in js.get('accessors', []):
    if 'bufferView' in a: a['bufferView'] = remap[a['bufferView']]
    sp = a.get('sparse')
    if sp:
        sp['indices']['bufferView'] = remap[sp['indices']['bufferView']]
        sp['values']['bufferView'] = remap[sp['values']['bufferView']]
js['buffers'] = [{'byteLength': len(buf), 'uri': 'data:application/octet-stream;base64,' + base64.b64encode(bytes(buf)).decode()}]
json.dump(js, open(dst, 'w'), separators=(',', ':'))
