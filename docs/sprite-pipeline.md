# 角色贴图怎么做 ｜ Sprite pipeline: from AI image to game-ready spritesheet

> **不想碰程序码？** 走[路径 2](../tasks/2-change-art.html)：那一页有现成的提示语，让 AI 帮你把图去背、拼好、换进游戏。这份文件是给想自己动手、或想知道原理的人看的。
>
> **Don't want to touch code?** [Path 2](../tasks/2-change-art.html) has ready-made prompts that get an AI to key, stitch and swap the sheet for you. This document is for doing it yourself, or understanding what's happening.

## 流程一览 ｜ Pipeline overview

```
AI 生图（洋红 #FF00FF 背景）｜ AI image generation on a magenta #FF00FF background
   → Python：色键去背 ｜ chroma-key the magenta out
   → 五格共用同一缩放比例，各自放进 128×160 的格子 ｜ scale every pose by ONE shared factor into a 128×160 cell
   → 拼成一张 640×160 的贴图 ｜ stitch into a 640×160 sheet
   → 转成 base64 ｜ base64-encode
   → 直接内嵌进 HTML，当作 canvas drawImage() 的来源 ｜ embed inline as the drawImage() source
```

贴图里的五个姿势，顺序固定：
The sheet holds five poses in this order:

| # | 姿势 ｜ Pose | 什么时候用 ｜ Used when |
|---|---|---|
| 0 | 站立 ｜ stand | 站在地面、没有移动 ｜ on the ground, not moving |
| 1 | 走路 A ｜ walk-A | 在地面移动（与 2 交替）｜ on the ground, moving (alternates with 2) |
| 2 | 走路 B ｜ walk-B | 在地面移动 ｜ on the ground, moving |
| 3 | 跳跃 ｜ jump | 离地 ｜ airborne |
| 4 | 摔倒 ｜ stumble | 答错时滑一跤，随即自己站起来 ｜ a slip on a wrong answer, then straight back up |

> 本单元的贴图是 **4 行（四个发型）× 5 帧**，一张 560×560，学生开场时自己挑一个。
> 摔倒**不是失败画面** —— 这个游戏不设生命值，滑一跤只是让那一下踩空看得见。
> This unit's sheet is **4 rows (hairstyles) x 5 poses**, 560x560, and the student
> picks a row at the start. The stumble is **not** a fail state: there are no
> lives, it just makes the misstep visible.

格数与姿势顺序只写在 `game.html` 里的 `AV_COLS`、`AV_ROWS` 与 `POSE` 三个常量，改了这几行其余程式会跟着走。

本单元不必手动跑上面那些步骤 —— 整条流程已经写成脚本：

`AV_COLS`, `AV_ROWS` and `POSE` in `game.html` are the only places the frame
count and pose order are written down. For this unit you don't need to run any
of the steps below by hand — the whole pipeline is scripted:

```bash
python3 tools/build-avatars.py    # art/ 四张原图 → assets/avatars.png
python3 tools/embed-avatars.py    # 贴回 game.html 的 AV_SRC ｜ paste back into game.html
python3 tools/build-sls.py        # 重建 SLS 版 ｜ rebuild the SLS build
```

换角色只要把 `art/` 里那四张图换掉（洋红背景、五个姿势一排），再跑这三行。
四张图**共用同一个缩放比例**，所以换了发型，角色不会忽大忽小。

To swap characters, replace the four sheets in `art/` (magenta background, five
poses in a row) and run those three lines. All four are scaled by one shared
factor, so switching hairstyle never changes how big the character is.

下面是这条流程背后的原理，想自己动手或换成别的工具时可以参考。

What follows is how that pipeline works, for anyone doing it by hand.

## 第一步：生成角色图 ｜ Step 1 — Generate the art

用 ChatGPT Image 或类似工具，**一次只画一个姿势**，比例才不会跑掉。制服换成你们学校的 —— 这是最容易个人化的部分。

Use ChatGPT Image or similar, **one pose per generation** so the scale doesn't drift. Swap in your own school's uniform — this is the easiest part to personalise.

提示语里有两句话最关键：
Two things in the prompt do most of the work:

- **要求纯洋红 `#FF00FF` 背景。** 角色身上不会出现的颜色，才好干净地键掉；这远比从白色背景里分出白色球鞋和高光容易。
  **Ask for a solid magenta `#FF00FF` background.** A colour that appears nowhere on the character keys out cleanly — far easier than separating a white background from white shoes and highlights.
- **要求角色是一个完整相连的整体** ——「头发与头相连、身体各部位之间不要有背景色的细线、缝隙或轮廓，不要有悬空的部件」。AI 生的图常在脖子、腰部、膝盖画出背景色的细缝；去背之后角色就断成好几块，事后再补会把像素弄糊。
  **Ask for one connected silhouette** — "hair merged into the head, no background-coloured line, gap or outline between body parts, no floating pieces". Generated art often draws thin background-coloured seams at the neck, waist and knees; keying those out leaves the character in visibly separate pieces, and patching it afterwards smears the pixels.

完整提示语见[路径 2](../tasks/2-change-art.html)，可以一键复制。
The full prompt is on [Path 2](../tasks/2-change-art.html), ready to copy.

## 第二步：去背 ｜ Step 2 — Remove the background

背景是洋红的话，用单纯的颜色判断就好，不必做边界填充 —— 而且这样连被轮廓围住的洋红色小块（两脚之间、膝盖下方）也会一并清掉，那是边界填充永远到不了的地方。

With a magenta background this is a plain colour test — no flood-fill needed — and it also clears magenta trapped *inside* the outline (between the ankles, under a bent knee) that a border flood-fill can never reach.

```python
from PIL import Image
import numpy as np

img = Image.open('pose.png').convert('RGB')
p = np.array(img).astype(int)
r, g, b = p[..., 0], p[..., 1], p[..., 2]

# 洋红＝红与蓝都远高于绿；角色身上没有这种颜色
# magenta = red and blue both far above green; nothing on the character is
bg = (r - g > 45) & (b - g > 45) & (g < 140)

rgba = np.dstack([p, np.where(bg, 0, 255)]).astype(np.uint8)
Image.fromarray(rgba).save('pose_transparent.png')
```

缩图之前，先把角色的颜色往透明区域扩散几个像素。少了这一步，缩图会把背景平均进边缘，留下一圈粉红色光晕。

Before downscaling, bleed the character's colours a few pixels outward into the transparent area. Without it the resize averages background into the edge and leaves a magenta halo.

```python
filled, known = rgb.copy(), ~bg
for _ in range(10):
    for dy, dx in ((1,0), (-1,0), (0,1), (0,-1)):
        take = np.roll(known, (dy,dx), (0,1)) & ~known
        filled[take] = np.roll(filled, (dy,dx), (0,1))[take]
        known |= take
```

然后把颜色与 alpha 两个通道**分开**用 LANCZOS 缩放，再合并。
Then resize the colour and alpha channels **separately** with LANCZOS and merge them.

**背景不是洋红的话**，改用从图片边缘开始的填充：它只移除与边缘相连的背景，所以角色内部的深色像素（轮廓、头发、鞋子）即使颜色接近背景也会留下来。

**If your background isn't magenta**, flood-fill from the image borders instead: it only removes background *connected* to the edges, so dark pixels inside the character (outlines, hair, shoes) survive even when they're close to the background shade.

```python
from PIL import Image
import numpy as np
from scipy import ndimage

img = Image.open('sprite_raw.png').convert('RGBA')
arr = np.array(img)

# 先标出「深色」像素 ｜ build a mask of "dark" pixels (tune the threshold to your art)
dark_mask = arr[:, :, :3].sum(axis=2) < 200

labels, n = ndimage.label(dark_mask)

# 碰到图片边缘的区块＝背景 ｜ regions touching the border are background, not character
border_labels = set(labels[0, :]) | set(labels[-1, :]) | set(labels[:, 0]) | set(labels[:, -1])
border_labels.discard(0)

for lbl in border_labels:
    arr[labels == lbl, 3] = 0

Image.fromarray(arr).save('sprite_transparent.png')
```

## 第三步：缩放并拼成贴图 ｜ Step 3 — Resize and stitch into a spritesheet

**五格必须共用同一个缩放比例**，不要各自缩放到填满格子。姿势的比例本来就不同（跳跃时腿收起来，摔落时又宽又矮），各自填满格子的话，角色跑起来就会忽大忽小。请以最高的那个姿势决定比例，再套用到全部五格：

**Scale every pose by the same factor** — don't resize each one to fill its cell. Poses have different proportions (the jump tucks the legs up, the fall is wide and short), so stretching each to its cell makes the character grow and shrink as it animates. Pick the factor from the tallest pose and apply it to all of them:

```python
frames = ['stand.png', 'walk_a.png', 'walk_b.png', 'jump.png', 'fall.png']
cell_w, cell_h, base = 128, 160, 158     # base = 格子里的脚底基线 ｜ the feet line inside the cell

crops = [trim_to_content(Image.open(f).convert('RGBA')) for f in frames]
scale = 150 / max(c.height for c in crops)   # 最高的姿势占 160 里的 150 ｜ tallest pose fills 150 of 160px

sheet = Image.new('RGBA', (cell_w * len(crops), cell_h), (0, 0, 0, 0))
for i, c in enumerate(crops):
    nw, nh = round(c.width * scale), round(c.height * scale)
    r = c.resize((nw, nh), Image.LANCZOS)
    sheet.alpha_composite(r, (i * cell_w + (cell_w - nw) // 2, base - nh))

sheet.save('spritesheet.png')  # 五帧＝640×160 ｜ 640×160 for 5 frames
```

姿势在格子里的位置其实不影响游戏 —— `measureSprite()` 会在载入时重新量出每一格真正的范围，并以头部为水平锚点 —— 但让五格的脚底对齐同一条基线，肉眼检查会容易得多。

Where a pose sits inside its cell doesn't actually matter — `measureSprite()` re-measures each frame's real bounding box on load and anchors on the head — but keeping the feet on a common baseline makes the sheet much easier to eyeball.

## 第四步：转 base64 并内嵌 ｜ Step 4 — Base64-encode and embed

```python
import base64
with open('spritesheet.png', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('ascii')
print(f'data:image/png;base64,{b64}')
```

把这串字直接贴给 JavaScript 里 `Image()` 的 `src`：
Paste the resulting string directly as the `src` of an `Image()` object in your JavaScript:

```javascript
const sprite = new Image();
sprite.onload = () => { spriteLoaded = true; };
sprite.src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...'; // 你的字串 ｜ your string here
```

之后用 canvas 的 `drawImage()` 从 640×160 的贴图里切出对应的 128×160 区块，画哪一格由角色状态决定（见上面的对照表）。

Then draw individual frames with canvas `drawImage()`, slicing the relevant 128×160 region out of the 640×160 sheet according to the player's state (see the table at the top).

## 为什么用 base64，而不是另外一个图档 ｜ Why base64 instead of a separate image file

因为 SLS 的 sandbox 挡掉所有外部网址（见 [sls-deployment.md](sls-deployment.md)）—— 所有东西都必须待在同一个 `index.html` 里。把贴图 base64 编码后以 data URI 内嵌，是让图片在 SLS 里还能显示的唯一办法。

Because the SLS sandbox blocks all external URLs (see [sls-deployment.md](sls-deployment.md)) — everything has to live inside the single `index.html`. Base64-encoding the sheet and embedding it as a data URI is the only way to keep a visual asset working once the game is inside SLS.

## 档案大小 ｜ File size note

640×160、五格的贴图，base64 之后大约在 HTML 里占 120KB 文字。素材尽量简单（平涂、少量颜色）—— 细节太多或写实的图会让 base64 暴涨，学生 iPad 载入会变慢。

A 640×160 five-frame sheet base64-encodes to roughly 120KB of text inside the HTML. Keep the source art simple — flat colours, a limited palette. Highly detailed or photographic sprites bloat the string and slow loading on student iPads.
