# 单元五《学无止境》· 学海登顶
### Secondary 3 (G3) Chinese Language · Unit 5 — Learning Never Ends

> 这份 README 的每一段都有中英文两种版本。网页版还可以一键切换「华文／双语／English」，并开关拼音。
> Every section appears in both languages. The web version also has a 华文 / Bilingual / English switch and a pinyin toggle.

**▶ 打开这里 ｜ Start here:** https://kaixinbuilds.github.io/S3G3CLChapter5ArgumentativeComparison/

---

## 这是什么 ｜ What this is

一款拖曳式的华文游戏，帮中三 G3（普通程度）学生看懂两篇课文都在用**对比论证法**。三关十二个版面，共 40 分，做完自动把分数送进 SLS 教师后台。由一位华文老师主要透过与 Claude（Anthropic）对话完成，**不需要任何编程基础**。

A drag-and-drop Chinese Language game that gets Secondary 3 (G3 / lower-readiness) students to see that both texts in this unit run on **对比论证法** (argument by contrast). Three levels, twelve panels, 40 marks, and the score posts itself into the SLS gradebook. Built by a Chinese Language teacher, mostly in conversation with Claude (Anthropic), with **no prior coding background**.

| | |
|---|---|
| **课文 ｜ Texts** | 生活空间《你在学什么》· 核心《学然后知不足》· 巩固《终身学习》 |
| **总分 ｜ Marks** | 40（第一关 10 · 第二关 15 · 第三关 15）|
| **版面 ｜ Panels** | 12 |
| **用在哪里 ｜ Where** | SLS Interactive Response（单一组件，跨三节课）｜ one SLS component across three lessons |

---

## 三关在教什么 ｜ What the three levels do

| 关 ｜ Level | 课文 ｜ Text | 学习点 ｜ The learning point |
|---|---|---|
| 第一关（10 分）| 生活空间《你在学什么》 | 五位受访者，从 6 岁到 76 岁 —— 学的内容各不相同，**看法**却要读得更细 |
| 第二关（15 分）| 核心《学然后知不足》 | **先反后正**：楚国人（反）→ 芝诺（正）→ 引用论证；另有反问句判断与篇章结构 |
| 第三关（15 分）| 巩固《终身学习》 | **先正后反**：李光耀（正）→ 方仲永（反）—— 正反位置对调，这个对调本身就是学习点 |

收关时才点破：两篇课文一个先反后正、一个先正后反，做的是同一件事 —— **对比**。

The closing screen is where it lands: one text goes negative-then-positive, the other positive-then-negative, and both are doing the same thing — **contrast**.

---

## 几个刻意的决定 ｜ Decisions worth knowing about

### 分数记的是第一次的判断 ｜ The mark is for the first judgement

每张卡片**第一次就放对**才得 1 分。放错的卡片轻弹回原位，人物滑一跤再自己站起来 —— **不扣分、不设生命值**，学生可以一直试到对为止，所以人人都走得完全程。但分数记的是第一次的判断，教师后台那个数字才有诊断价值。

A card scores only if it is placed correctly on the **first** try. A wrong drop springs back and the character stumbles and gets up — **no penalty, no lives** — so every student finishes. But the mark reflects the first judgement, which is what makes the gradebook number worth reading. Without this, everyone eventually scores 40/40 and the number means nothing.

### 干扰项是诊断，不是填充 ｜ Distractors that diagnose

第三关「李光耀的好学表现」，三个干扰项全部取自方仲永。会中招的，正是把一正一反两个例子混为一谈的学生 —— 这比随意编造的干扰项有用得多。

In Level 3's evidence panel, all three distractors belong to 方仲永, not 李光耀. The only student who falls for them is one who has merged the unit's positive and negative examples — far more informative than filler options.

### 拼音一律人工撰写 ｜ Every pinyin syllable is hand-written

**不使用拼音转换函式库**：官方禁用外部函式库，而且自动转换必错在多音字上 —— **好**学 hào 不是 hǎo，**乐**在其中 lè 不是 yuè，逆水**行**舟 xíng 不是 háng。在华文课上把拼音标错，比不标更糟。70 条注音存在 `game.html` 的 `RUBY` 字典里，网页那一份由脚本从同一本字典抽出，两边不可能不一致。

**No pinyin conversion library**: external libraries are barred, and automatic conversion always trips on heteronyms. A wrong pinyin in a Chinese lesson is worse than none. All 70 entries live in the `RUBY` dictionary in `game.html`; the website's copy is extracted from that same dictionary by a script, so the two cannot disagree.

采用**方案甲** —— 只标课本已注音的词语，与课本保持一致。

Plan A: annotate only what the textbook itself annotates.

### 双语只到导航为止 ｜ Bilingual chrome, Chinese content

英文只用于**系统与导航文字**：按钮、操作说明、警告、登顶画面。**所有学习内容一律只用华文** —— 卡片、引语、段落大意、答案、干扰项。

题目内容若附英译，等于直接给出答案，阅读理解就变成英文配对练习。要扶的是「怎么操作」，不是「怎么理解」。

English is used for **chrome and navigation only**: buttons, instructions, warnings, the summit screen. **All learning content stays Chinese-only** — cards, quotations, paragraph summaries, answers, distractors. An English gloss on the content would hand over the answer and turn reading comprehension into an English matching exercise. The scaffold is for *how to operate it*, not *how to understand it*.

「拼音」与「EN」两个开关**跨页记忆**：在落地页开了，进游戏还是开着。

Both switches persist **across pages**: set on the landing page, still set inside the game.

### 登顶画面就是完成凭证 ｜ The summit screen is the proof

**没有下载按钮** —— SLS 的 iframe sandbox 里下载不可靠，而且官方禁用外部函式库（html2canvas 用不了）。以装置原生截图为准；截图会把 SLS 页面一并拍进去，反而可以佐证学生确实是在登入状态下作答的。

画面上有：姓名、班级、三关分数、**三关各自的用时与总用时**、完成日期与时间、验证码。

**No download button**: downloads are unreliable inside the SLS sandbox and external libraries are barred, so html2canvas is out. The device's own screenshot is the mechanism — and it catches the surrounding SLS page too, which is itself evidence the student was logged in. The screen carries the name, class, per-level marks, **per-level and total climb times**, the finish date and time, and a short verification code.

姓名只存在学生自己的装置里，**不随分数传送，不上传任何服务器**。

The name never leaves the student's own device: it is not sent with the score and not uploaded anywhere.

---

## 两个版本 ｜ Two builds

| | `game.html` | `sls/index.html` |
|---|---|---|
| **用在哪里**<br>**Where it runs** | 任何网站 / GitHub Pages<br>Any website / GitHub Pages | SLS Interactive Response |
| **分数进不进教师后台**<br>**Scores in the gradebook** | ❌ 只在画面上<br>❌ On screen only | ✅ 自动送进 Learning Progress<br>✅ Posted automatically |
| **内含 xAPI wrapper** | 否 ｜ No | 是，内嵌 xAPIWrapper v1.11.0 ｜ Yes, embedded inline |
| **怎么部署 ｜ Deploy** | Settings → Pages | 压缩成 .zip 上传 ｜ Zip and upload |

**内容一字不差**，差别只在于分数会不会送回 SLS。`sls/index.html` 由 `tools/build-sls.py` 从 `game.html` 生成 —— **不要手改**，改了 `game.html` 重跑脚本就好。

The content is identical; only the score reporting differs. `sls/index.html` is generated from `game.html` by `tools/build-sls.py` — **never edit it by hand**; edit the game and re-run the script.

> 上传 SLS 时，**Maximum Marks 要设成 40**。SLS 对 Interactive Response 的上限是 99，40 分安全。
> Set **Maximum Marks to 40** when uploading. SLS caps Interactive Response at 99, so 40 is safe.

---

## 改成自己的课文 ｜ Adapt it to your own text

先看这一份：📄 **[全文校对稿](docs/全文校对稿.md)** —— 12 个版面的指示、卡片、答案、干扰项、答后讲解，加上 70 条拼音，全在一页里。这份文件由 `tools/dump-script.py` 从 `game.html` **自动生成**，不是另抄一份，所以永远等于学生看到的东西。

Start here: 📄 **[the full text dump](docs/全文校对稿.md)** — every instruction, card, answer, distractor and explanation across the 12 panels, plus all 70 pinyin entries. It is **generated** from `game.html` by `tools/dump-script.py` rather than maintained separately, so it always equals what students actually see.

三条路径 ｜ Three paths: [原样拿去用](tasks/1-use-as-is.html) · [换角色美术](tasks/2-change-art.html) · [换成自己的课文](tasks/3-change-questions.html)

### 题目都在哪里 ｜ Where the questions live

全部在 `game.html` 的 **`LEVELS` 数组**里（注释写着 `二、题库 ｜ THE QUESTION BANK`）。四种版面型别：

All in the **`LEVELS` array** in `game.html`, under the comment `二、题库 ｜ THE QUESTION BANK`. Four kinds of panel:

```javascript
// 拖进格子 ｜ drag into slots
{ k:'slots', cols:3, hd:'版面标题',
  tip:{zh:'指示', en:'instruction'},
  slots:[{t:'格子名', sub:'小字'}],       // 格子 ｜ the slots
  cap:1,                                  // 每格最多几张 ｜ cards per slot
  flow:'row',                             // 格子里横排（可省）｜ lay cards in a row (optional)
  cards:[{t:'卡片文字', s:0}],            // s = 正确格子编号，-1 = 干扰项 ｜ -1 = distractor
  e:'答后讲解' }

// 多选，全对才得 1 分 ｜ multi-select, all-or-nothing
{ k:'multi', hd:'…', tip:{…}, q:'题目', opts:[{t:'选项', ok:true}], e:'…' }

// 三选一 ｜ single choice
{ k:'choice', hd:'…', tip:{…}, q:'题目', opts:['甲','乙','丙'], a:0, e:'…' }
```

每张可放的卡片值 1 分，多选与选择题各 1 分 —— 所以**改了题数就要重算总分**：`sendScore(total(), 40)` 与 SLS 的 Maximum Marks 都要跟着改。

Each placeable card is worth 1 mark; multi and choice are worth 1 each. **Change the number of items and you must recalculate the total** in `sendScore(total(), 40)` and in the SLS component's Maximum Marks.

### 改完记得重跑 ｜ Re-run after editing

```bash
python3 tools/build-sls.py      # 重建 SLS 版 ｜ rebuild the SLS build
python3 tools/dump-script.py    # 重建校对稿 ｜ rebuild the proofreading dump
python3 tools/build-pinyin.py   # 网页那份拼音字典 ｜ the website's pinyin copy
python3 tools/build-scene.py    # 网页那份山景 ｜ the website's copy of the scenery
```

---

## 档案结构 ｜ Repo structure

```
├── index.html                  ← 落地页：两道门 ｜ Landing page: the two doors
├── game.html                   ← 游戏（网页版）｜ The game (web build)  ← 唯一的真本 ｜ the source of truth
├── sls/index.html              ← 游戏（SLS 版，自动记分，由脚本生成）｜ generated SLS build
├── tasks/                      ← 老师的三条分层路径 ｜ the three teacher paths
├── assets/
│   ├── avatars.png             ← 四个角色 × 五个姿势 ｜ 4 characters x 5 poses
│   ├── scene.js                ← 山景（从 game.html 抽出）｜ scenery, extracted
│   ├── pinyin.js               ← 拼音字典（从 game.html 抽出）｜ pinyin, extracted
│   ├── site.css / site.js      ← 网页样式与语言／拼音开关 ｜ site styling and switches
├── art/                        ← 四张角色原图（洋红背景）｜ the four source sheets
├── docs/
│   ├── 全文校对稿.md            ← 全部题目与答案（自动生成）｜ full text dump (generated)
│   ├── 创作思路.md              ← 教学设计的思路 ｜ the pedagogical thinking
│   ├── xapi-scoring-wrapper.md ← 自动记分的原理 ｜ how the auto-scoring works
│   ├── sls-deployment.md       ← 压缩、上传、确认分数 ｜ zip, upload, verify
│   └── sprite-pipeline.md      ← 角色贴图怎么做 ｜ how the sprite was made
├── tools/                      ← 建置脚本（都是 python3，无需安装任何东西）
└── LICENSE                     ← MIT
```

---

## 仍待复核 ｜ Still to be checked

以下几题在题库审阅时标了［存疑］，已照决定建置，但建议第二位华文老师复核。详见[全文校对稿](docs/全文校对稿.md)最后一节。

These were flagged during review, built as decided, but a second Chinese Language teacher should look at them. See the last section of the [full text dump](docs/全文校对稿.md).

1. 第二关反问句判断中「人生就像一场盛大的演出……呢？」判为**不是**反问句 —— 这是该版面唯一的否定项，也是鉴别点
2. 第二关第1段修辞手法已改为**多选**（排比＋比喻），避开二选一的争议
3. 第二关三条引语的「意思」为拟答（课本留白）
4. 第三关俗语题的另两个选项由建置时拟定

---

## 制作与致谢 ｜ Credits

游戏设计与内容：**郑凯欣老师** · 百德中学母语部主任
Game design and content: **Mdm Chun Kai Xin** · HOD/MTL · Bukit View Secondary School

姊妹作 ｜ Companion project：[中三G3华文论证冒险](https://github.com/kaixinbuilds/S3G3CLArgumentativeAdventure)（单元三、四，马里奥式平台游戏）

使用的工具 ｜ Built with:

- **Claude** (Anthropic) — 游戏设计、程序码、全部文件 ｜ game design, code, all documentation
- **ChatGPT Image** — 四个角色的像素贴图 ｜ the four pixel-art characters
- **[xAPIWrapper v1.11.0](https://github.com/adlnet/xAPIWrapper)** (ADL) — 内嵌于 SLS 版 ｜ embedded in the SLS build

坦白说：这是一位不会编程的老师，在 AI 协助下做出来的。如果你是老师，正在想「我肯定做不出这种东西」—— 你想错了，这个 repo 就是证明。

Full transparency: this is an AI-assisted build from a non-programmer teacher. If you're a teacher thinking "I could never build this" — you're wrong, and this repo is the proof.

## 授权 ｜ License

MIT —— 见 [LICENSE](LICENSE)。欢迎使用、改编，拿去教学。
MIT — see [LICENSE](LICENSE). Use it, adapt it, teach with it.
