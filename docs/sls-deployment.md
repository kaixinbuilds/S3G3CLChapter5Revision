# 上传到 SLS ｜ Deploying to SLS

> 目标：学生在 SLS 里做完，分数自己出现在教师后台，不必截图核对、不必手动改分。
> Goal: the student finishes inside SLS and the score appears in the gradebook by itself.

## 一、先把档案准备好 ｜ Get the file ready

要上传的是 **`sls/index.html`**，不是 `game.html`。

Upload **`sls/index.html`**, not `game.html`.

改过题目的话，先重跑一次，否则上传的还是旧版：
If you have edited the questions, rebuild first or you will upload the old version:

```bash
python3 tools/build-sls.py
```

压缩：**只压 `index.html` 这一个档案**，压缩档里不要有资料夹层级。

Zip it: **the single `index.html`**, with no folder nesting inside the archive.

```bash
cd sls && zip unit5.zip index.html
```

> 档案大约 250KB，其中约 180KB 是四个角色的贴图、41KB 是 xAPIWrapper。全部内嵌是必须的 —— 见下面「为什么不能有外部档案」。
> The file is ~250KB: ~180KB of character sprites and 41KB of xAPIWrapper, all inlined by necessity — see below.

## 二、在 SLS 里建组件 ｜ Create the component

1. 课业里 **Add Section → Interactive Response**
   —— **一定要选 Interactive Response**。选 Text/Media 的话，游戏照样能玩，但**分数永远是空的**，这是最常见的失败原因。
2. 上传 `unit5.zip`
3. **Maximum Marks 设成 40**
   —— 留在预设的 0，分数送出了老师也看不到。
4. 存档，用学生视角试做一遍

<br>

1. In your lesson: **Add Section → Interactive Response**. It **must** be Interactive Response — with Text/Media the game still plays but the score is always blank, which is the single most common failure.
2. Upload `unit5.zip`
3. Set **Maximum Marks to 40** — left at the default 0, the score is sent but never shown.
4. Save, then try it as a student.

## 三、确认分数真的进去了 ｜ Confirm the score actually lands

用学生账号做完一关，然后看 **Learning Progress**。

分数是**累计总分**：做完第一关送 10，第一二关都做完送 25，全部做完送 40。中间隔几天再回来补做，分数会继续往上叠，不会把之前的洗掉 —— 这一点是刻意处理过的，见 [xapi-scoring-wrapper.md](xapi-scoring-wrapper.md)。

The score is the **running total**: 10 after level 1, 25 after two, 40 after all three. Coming back days later to finish adds to it rather than replacing it — see [xapi-scoring-wrapper.md](xapi-scoring-wrapper.md) for why that took deliberate handling.

## 四、常见状况 ｜ When something is off

| 状况 ｜ Symptom | 多半是 ｜ Usually |
|---|---|
| 后台分数一片空白<br>Gradebook column is blank | 组件不是 Interactive Response，或 Maximum Marks 还是 0<br>Wrong component type, or Maximum Marks still 0 |
| 学生说「我做完了但没分」<br>"I finished but got nothing" | 学生另开了分页。游戏会先弹双语警告拦一次，但学生可以按「仍要继续」——请他在 SLS 里重做一遍<br>They opened it in a new tab. The game warns first, but they can continue anyway; have them redo it inside SLS |
| 画面一片空白<br>Blank screen | 压缩档里多了一层资料夹，SLS 找不到 index.html<br>The zip has a nested folder, so SLS can't find index.html |
| 分数卡在 99<br>Score caps at 99 | SLS 的硬性上限。本游戏满分 40，不会碰到<br>An SLS hard limit; at 40 marks this game never hits it |
| 图片不显示 / 没有声音<br>No sprites, no sound | 档案被改动过，或不是用 build-sls.py 生成的<br>The file was hand-edited, or not produced by build-sls.py |

## 五、为什么不能有外部档案 ｜ Why nothing external is allowed

SLS 把上传的内容放进 **sandbox iframe** 执行，挡掉所有对外的网络请求：不能载 CDN、不能用外部 `<script src>`、不能引用外部字体或图档。

所以这个游戏里：

- 角色贴图 **base64 内嵌**（`assets/avatars.png` → 一长串文字）
- 山景是**程式画出来的 SVG**，不是图档
- 音效与音乐用 **Web Audio 即时合成**，没有任何音档 —— 顺带也不牵涉音乐版权
- xAPIWrapper 整个程式库贴成纯文字
- 没有下载按钮：sandbox 里下载不可靠，html2canvas 之类的函式库也用不了，所以**登顶画面以装置原生截图为准**

SLS runs uploaded content in a sandboxed iframe that blocks every outbound request — no CDN, no external `<script src>`, no external fonts or images. Hence: sprites base64-inlined, scenery drawn as generated SVG, sound synthesised live in Web Audio (which also sidesteps music licensing), the whole xAPI library pasted in as text, and no download button — the summit screen relies on the device's own screenshot.

## 六、iframe 只有 450px 高 ｜ The frame is only 450px tall

官方建议尺寸是宽 100%、高 450px。整个版面是照这个数字设计的：矮而宽，山景在上、题目在下，**任何一个版面都不需要卷动**。

在投影机上这是一条 1600×188 的细长带，在学生手机上却接近正方形 —— 所以山景是**按框的形状现画的**，不是一张固定比例的图，两种极端都不会被裁掉。

The recommended frame is 100% wide and 450px tall, and the whole layout is built to that number: no panel ever needs scrolling. Because that frame is a 1600x188 ribbon on a projector and nearly square on a phone, the scenery is generated to fit its measured box rather than drawn at a fixed aspect.
