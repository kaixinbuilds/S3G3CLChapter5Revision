"""
art/ 里四张原图（发型不同）→ assets/avatars.png，一张 4 行 × 5 帧的贴图
Four source sheets in art/ (hairstyle variants) -> assets/avatars.png,
one 4-row x 5-frame spritesheet.

用法 ｜ Usage:  python3 tools/build-avatars.py
改了 art/ 里的图之后重跑，再把 assets/avatars.b64.txt 的内容贴回
game.html 与 sls/index.html 里 AV.src 的那一行。
Re-run after editing anything in art/, then paste assets/avatars.b64.txt
back into the AV.src line in game.html and sls/index.html.

行 = 头像 ｜ row = avatar          列 = 姿势 ｜ col = pose
0 站立 stand ｜ 1 走路A walk-A ｜ 2 走路B walk-B ｜ 3 欢呼 cheer ｜ 4 摔倒 stumble

「摔倒」不是失败画面 —— 本游戏不设生命值。答错时人物滑一跤、退半步，
随即自己站起来接着爬：错了不必重来，但看得见自己刚才踩空了。
The stumble is not a fail state — there are no lives. On a wrong answer the
character slips back half a step and immediately gets up again: nothing is
lost, but the misstep is visible.
"""
from PIL import Image
import numpy as np, base64, io, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sorted(glob.glob(os.path.join(ROOT, "art", "avatar-*.png")))   # 1 短发 2 马尾 3 短鲍伯 4 平头
assert len(SRC) == 4, SRC
KEEP = [0, 1, 2, 3, 4]       # 五格全留 ｜ keep all five poses
CELL_W, CELL_H = 112, 140
BASE = 137                   # 格子里的脚底基线 ｜ feet baseline inside the cell


def panels(path):
    """按整幅高的黑色分隔线切出五格 ｜ split on the full-height black divider lines"""
    p = np.array(Image.open(path).convert("RGB")).astype(int)
    dark = (p.sum(2) < 180).mean(0)
    cols = np.where(dark > 0.85)[0]
    groups = []
    for c in cols:
        if groups and c - groups[-1][-1] <= 3:
            groups[-1].append(c)
        else:
            groups.append([c])
    edges = [(g[0], g[-1]) for g in groups]
    assert len(edges) == 6, (path, edges)
    # 整幅图外围还有一圈黑框，横线不去掉的话会跟着角色一起被裁进格子里
    # the sheet also has a black outer frame; left in, those rules get cropped
    # into the cell along with the character
    darkrow = (p.sum(2) < 180).mean(1)
    rows = np.where(darkrow > 0.85)[0]
    y0 = rows[rows < p.shape[0] // 2].max() + 1 if (rows < p.shape[0] // 2).any() else 0
    y1 = rows[rows > p.shape[0] // 2].min() if (rows > p.shape[0] // 2).any() else p.shape[0]
    return [(edges[i][1] + 1, edges[i + 1][0]) for i in range(5)], p, (y0, y1)


def keyed(p, x0, x1, y0, y1):
    """色键去洋红，并把角色颜色往外扩散，缩图时才不会留粉红光晕
       chroma-key the magenta and bleed the character colours outward so the
       downscale doesn't average background into the edge (a magenta halo)"""
    sub = p[y0:y1, x0:x1]
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    bg = (r - g > 45) & (b - g > 45) & (g < 140)
    rgb, known = sub.copy(), ~bg
    for _ in range(12):
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            take = np.roll(known, (dy, dx), (0, 1)) & ~known
            rgb[take] = np.roll(rgb, (dy, dx), (0, 1))[take]
            known |= take
    a = np.where(bg, 0, 255)
    im = Image.fromarray(np.dstack([rgb, a]).astype(np.uint8))
    bb = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    return im.crop(bb)


crops = []
for path in SRC:
    edges, p, (y0, y1) = panels(path)
    crops.append([keyed(p, edges[i][0], edges[i][1], y0, y1) for i in KEEP])

# 四个头像共用同一个缩放比例，换头像时角色不会忽大忽小
# ONE shared scale factor across all four avatars, so switching avatar never
# changes how big the character is on screen
tallest = max(c.height for row in crops for c in row)
scale = 132 / tallest

sheet = Image.new("RGBA", (CELL_W * len(KEEP), CELL_H * len(SRC)), (0, 0, 0, 0))
for ri, row in enumerate(crops):
    for ci, c in enumerate(row):
        nw, nh = max(1, round(c.width * scale)), max(1, round(c.height * scale))
        rgb = c.convert("RGB").resize((nw, nh), Image.LANCZOS)
        alp = c.getchannel("A").resize((nw, nh), Image.LANCZOS)
        rgb.putalpha(alp)
        sheet.alpha_composite(rgb, (ci * CELL_W + (CELL_W - nw) // 2,
                                    ri * CELL_H + BASE - nh))

sheet = sheet.quantize(colors=128, method=Image.FASTOCTREE).convert("RGBA")
buf = io.BytesIO()
sheet.save(buf, "PNG", optimize=True)
raw = buf.getvalue()

out = os.path.join(ROOT, "assets", "avatars.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "wb").write(raw)
b64 = base64.b64encode(raw).decode()
open(os.path.join(ROOT, "assets", "avatars.b64.txt"), "w").write(b64)

print(f"sheet      {sheet.size[0]}x{sheet.size[1]}  cell {CELL_W}x{CELL_H}  scale {scale:.4f}")
print(f"png        {len(raw)/1024:.1f} KB")
print(f"base64     {len(b64)/1024:.1f} KB  (embedded as text in the HTML)")
