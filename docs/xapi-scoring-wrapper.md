# 自动记分的原理（xAPI wrapper）｜ How the auto-scoring works

> **不必看懂这一页也能用。** 这是给想知道「分数为什么会自己跑进教师后台」的人看的。只想部署的话，看 [sls-deployment.md](sls-deployment.md) 就够了。
>
> **You don't need this page to use the game.** It's here for anyone curious about *why* the score lands in the gradebook by itself. If you just want to deploy, [sls-deployment.md](sls-deployment.md) is enough.

大多数老师卡住的就是这一关。SLS 会不会自动把分数记进 gradebook，**取决于**你的 HTML5 课业有没有用一个叫 **xAPI**（Experience API，又称 Tin Can）的标准跟 SLS 讲话。这份文件说明这个游戏是怎么接上去的，你可以照抄到自己的课业里。

This is the part most teachers get stuck on. SLS can auto-record a score in the gradebook **only if** your HTML5 activity talks to SLS using a standard called **xAPI** (Experience API / "Tin Can"). This doc explains exactly how that's wired up in this game, so you can copy the pattern into your own activity.

## 它解决了什么问题 ｜ The problem this solves

没有它的话，SLS 上的 HTML5 游戏要「算分」，只能叫学生截图上传当凭证 —— 多数老师自制的游戏就是这样做的，两边都麻烦。内嵌了 xAPI wrapper 之后，**学生一做完，分数就自动送出**，直接出现在教师的 **Learning Progress** 里。不必截图，不必人工核对。

Without this, the only way to "grade" an SLS HTML5 game is to make students screenshot their result and upload it as proof — which is what most teacher-made games do, and it's a pain for everyone. With the xAPI wrapper embedded, **the score is sent automatically the moment the student finishes**, and it shows up in the teacher's **Learning Progress** view. No screenshots, no manual checking.

## 为什么整个程式库都得内嵌 ｜ Why it has to be embedded inline

SLS 把上传的 HTML5 内容放进一个 sandbox iframe 里执行，那里**挡掉所有对外的网络请求** —— 不能载 CDN 脚本，不能用外部 `<script src="...">`，压缩档以外的东西一律拿不到。所以整个 xAPI 程式库必须直接贴进 HTML 的 `<script>` 里。这就是 `sls/index.html` 看起来那么大的原因 —— 其中大约 130KB 是 [xAPIWrapper v1.11.0](https://www.npmjs.com/package/xapiwrapper)，以纯文字嵌在 `<head>` 里。

SLS runs uploaded HTML5 content inside a sandboxed iframe that **blocks all external network requests** — no CDN scripts, no external `<script src="...">`, nothing fetched from outside the zip. So the entire xAPI library has to be pasted directly into a `<script>` tag in the HTML file. That's why `sls/index.html` looks huge — roughly 130KB of it is the [xAPIWrapper v1.11.0](https://www.npmjs.com/package/xapiwrapper) library, embedded as plain text inside `<head>`.

取得程式库的方法 ｜ To get that library:
```bash
curl -sL "https://registry.npmjs.org/xapiwrapper/-/xapiwrapper-1.11.0.tgz" -o xapiwrapper.tgz
tar -xzf xapiwrapper.tgz
cat package/dist/xapiwrapper.min.js
# paste the contents into a <script> tag in your HTML <head>
```

## 中间那层程式码 ｜ The wrapper code

贴在 xAPIWrapper 程式库之后，一样放在 `<head>` 里。这就是本游戏实际使用的那一层，只做两件事：读取 SLS 启动课业时透过网址传进来的连线资讯，以及在学生做完时把分数送回去。

Paste this after the xAPIWrapper library, still inside `<head>`. It's the actual utility layer used in this game, and it does two things: read the connection details SLS passes in via the URL when it launches your activity, and send the score back when the student finishes.

```html
<script>
const XAPIUtils = {
  parameters: null,

  // Called once on page load. Reads SLS's launch parameters from the URL.
  // If they're missing (e.g. you're testing the file locally in a browser),
  // this quietly does nothing instead of crashing.
  init: function () {
    try {
      const p = new URLSearchParams(window.location.search);
      const ep       = p.get('endpoint');
      const auth     = p.get('auth');
      const agent    = JSON.parse(p.get('agent') || 'null');
      const stateId  = p.get('stateId');
      const activityId = p.get('activityId');

      if (!ep) return; // not launched from inside SLS — skip xAPI entirely

      ADL.XAPIWrapper.changeConfig({
        endpoint: ep + '/',
        auth: 'Basic ' + auth
      });
      this.parameters = { agent, stateId, activityId };
    } catch (e) {
      console.warn('xAPI init failed (not in SLS?)');
    }
  },

  // Call this whenever you want to report a score, e.g. at level checkpoints
  // and again at the very end of the game.
  sendScore: function (rawScore, maxScore) {
    try {
      if (!this.parameters) return; // init() never got valid SLS parameters
      const { agent, stateId, activityId } = this.parameters;
      ADL.XAPIWrapper.sendState(activityId, agent, stateId, null, {
        score: rawScore,
        maxScore: maxScore,
        completed: true
      });
      console.log('Score sent to SLS:', rawScore, '/' + maxScore);
    } catch (e) {
      console.warn('xAPI sendScore failed:', e);
    }
  }
};

document.addEventListener('DOMContentLoaded', () => XAPIUtils.init());
</script>
```

## 游戏里怎么呼叫它 ｜ How to call it from your game logic

通常两个地方 ｜ Two places, typically:

```javascript
// 1. Optional checkpoint — e.g. after level 1 finishes
XAPI.sendScore(total(), 40);   // (累计总分, 满分) ｜ (running total, max)

// 2. Required — when the whole game/activity is completed
XAPI.sendScore(total(), 40);
```

`total()` 是本游戏算三关累计总分的函式，换成你自己程式里的名称即可。

`total()` is this game's running-total function — rename it to match your own code.

## 一定会踩到的坑 ｜ Gotchas that will bite you

| 状况 ｜ Issue | 怎么办 ｜ Fix |
|---|---|
| 后台分数是空的<br>Score shows blank in the gradebook | 元件**必须**用 **Interactive Response** 上传，不能用 Text/Media（见 [sls-deployment.md](sls-deployment.md)）<br>The component **must** be uploaded as **Interactive Response**, not Text/Media |
| 分数卡在 99 上不去<br>Score caps at 99 | SLS 对 Interactive Response 的 **Maximum Marks** 硬性上限就是 99 —— 请重新设计配分（本游戏是每张卡片 1 分 × 40 = 40 分），而不是每题 10 分<br>That's SLS's hard limit — recalibrate your scoring (this game: 1 mark per card x 40 = 40) rather than 10 marks per question |
| 什么都没发生，也没有错误讯息<br>Nothing happens, no console errors | 确认你是在 SLS *里面*测试。在本机浏览器打开时，网址里没有 `endpoint` 参数，`init()` 会安静跳过 —— 这是正常行为，不是坏了<br>Check you're testing *inside* SLS; opened locally there's no `endpoint` parameter, so `init()` silently skips — expected, not a bug |
| 分数送出了，老师却看不到<br>Score submitted but the teacher can't see it | 确认 SLS 元件里的 **Maximum Marks** 真的设了（不是留在预设的 0）<br>Confirm **Maximum Marks** was actually set on the component, not left at 0 |

## 搬到自己的游戏里 ｜ Adapting this for your own game

不必看懂 xAPI 的内部机制也能重用。整个模式就三步：

1. 把上面两段 `<script>`（程式库 + XAPIUtils）复制到你自己 HTML 的 `<head>` 里
2. 在游戏结束的地方呼叫 `XAPIUtils.sendScore(你的分数变量, 你的满分)`
3. 满分不要超过 99，上传 SLS 时把 **Maximum Marks** 设成同一个数字

You don't need to understand the internals of xAPI to reuse this. The whole pattern is:

1. Copy the two `<script>` blocks above (library + XAPIUtils) into your own HTML file's `<head>`
2. Call `XAPIUtils.sendScore(yourScoreVariable, yourMaxScore)` at your game's end condition
3. Keep your max score at 99 or below, and set **Maximum Marks** to match when you upload to SLS

接上去就只有这些。这个 repo 里其余的东西（平台游戏机制、题目资料、角色贴图）都跟它无关，可以自由替换。

That's the entire integration. Everything else in this repo — the platformer mechanics, the question data, the sprite — is independent of this and can be swapped out freely.


---

## 一个真的会咬人的坑：state 文件会覆盖 ｜ The one that actually bites: state documents overwrite

`sendState` 存的是一份 **state 文件**，后写的会**整个覆盖**前写的 —— 不是累加。

这在单一组件跨三节课使用时特别要命：学生第一节做完第一关，送出 10 分；隔了两天回来做第三关，如果程式送的是「这一关得了 15 分」，那 15 就会**把 10 整个盖掉**，学生凭空少了 10 分，而且没有任何错误讯息。

所以本游戏**每次都送三关的累计总分**：

`sendState` stores a **state document**, and a later write **replaces** the earlier one wholesale — it does not accumulate. That matters enormously for one component spanning three lessons: a student who scores 10 in lesson 1 and comes back two days later would have that 10 silently overwritten if the game sent "15 for this level". So this game always sends the running total across all three levels:

```javascript
// 对：每次都送累计总分 ｜ right: always the running total
XAPI.sendScore(total(), 40);

// 错：送单关分数，日后补做会把之前的洗掉
// wrong: sending one level's score wipes the earlier ones
XAPI.sendScore(thisLevelScore, 15);
```

## 静默失败是怎么发生的 ｜ How the silent failure happens

官方范例的 `sendScore()` 只在 `catch` 里 `console.error`。学生若另开分页，网址里的 `endpoint`、`auth`、`agent` 全部丢失，`JSON.parse(agent)` 抛出错误 —— 游戏照常运作，学生做完，分数从未送出，**没有任何人会发现**。

本游戏的 `init()` 因此**回传成功与否**：读不到启动参数就先显示双语警告，并给一个「仍要继续」的出口。

The official sample's `sendScore()` only `console.error`s in its catch. Open the activity in a new tab and the launch parameters are gone, `JSON.parse(agent)` throws, and the game plays on perfectly while nothing is ever sent — and nobody finds out. So this game's `init()` **returns whether it succeeded**, and shows a bilingual warning with a "continue anyway" escape hatch when it did not.
