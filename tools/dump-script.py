"""
game.html  →  docs/全文校对稿.md
把游戏里的题库、指示、答案、讲解、拼音，原封不动倒成一份可校对的 Markdown。

Dump the game's questions, instructions, answers, explanations and pinyin into
one Markdown file for proofreading.

关键在于「不是另抄一份」：内容直接从 game.html 的 LEVELS 与 RUBY 读出来，
所以校对稿永远等于学生看到的东西。改了游戏，重跑一次就好。
The point is that this is NOT a second copy: it reads game.html's own LEVELS
and RUBY, so the proofreading document always equals what students see. Edit
the game, re-run this.

用法 ｜ Usage:  python3 tools/dump-script.py
"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = open(os.path.join(ROOT, "game.html"), encoding="utf-8").read()


def grab(name, open_ch, close_ch):
    """抓出 `const NAME = [...]` 的整段字面量 ｜ pull out the whole literal"""
    i = SRC.index("const " + name + " = ")
    i = SRC.index(open_ch, i)
    depth, j, in_str = 0, i, False
    while j < len(SRC):
        c = SRC[j]
        if in_str:
            if c == "\\": j += 2; continue
            if c == "'": in_str = False
        elif c == "'": in_str = True
        elif c == "/" and SRC[j+1:j+2] == "*":
            j = SRC.index("*/", j) + 2; continue
        elif c == open_ch: depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0: return SRC[i:j+1]
        j += 1
    sys.exit("unterminated literal: " + name)


def js_to_json(src):
    """JS 字面量 → JSON：去注释、单引号转双引号、键名补引号、去掉多余逗号
       JS literal -> JSON: strip comments, requote strings and keys, drop trailing commas"""
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c == "'":                                   # 单引号字串 ｜ single-quoted string
            j, buf = i + 1, []
            while j < n and src[j] != "'":
                if src[j] == "\\":
                    buf.append(src[j+1]); j += 2
                else:
                    buf.append(src[j]); j += 1
            out.append(json.dumps("".join(buf), ensure_ascii=False))
            i = j + 1
        elif c == "/" and src[i+1:i+2] == "*":
            i = src.index("*/", i) + 2
        elif c == "/" and src[i+1:i+2] == "/":
            i = src.index("\n", i)
        elif c.isalpha() or c == "_":                  # 可能是键名 ｜ possibly a key
            j = i
            while j < n and (src[j].isalnum() or src[j] in "_$"): j += 1
            word = src[i:j]
            k = j
            while k < n and src[k] in " \t\n": k += 1
            if k < n and src[k] == ":":
                out.append(json.dumps(word)); i = j
            else:
                out.append("null" if word in ("undefined",) else word); i = j
        else:
            out.append(c); i += 1
    txt = "".join(out)
    txt = re.sub(r",(\s*[\]}])", r"\1", txt)           # 尾逗号 ｜ trailing commas
    return txt


people = grab("PEOPLE", "[", "]")
levels = grab("LEVELS", "[", "]").replace("slots:PEOPLE", "slots:" + people)
ruby   = grab("RUBY", "{", "}")
avn    = grab("AV_NAMES", "[", "]")

LEVELS   = json.loads(js_to_json(levels))
RUBY     = json.loads(js_to_json(ruby))
AV_NAMES = json.loads(js_to_json(avn))

def pmax(d):
    return len([c for c in d["cards"] if c["s"] >= 0]) if d.get("k") == "slots" else 1
def lmax(lv):
    return sum(pmax(d) for d in lv["panels"])
TOTAL = sum(lmax(l) for l in LEVELS)

B = lambda t: str(t).replace("<b>", "**").replace("</b>", "**")
L = []
w = L.append

w("# 单元五《学无止境》· 书山登顶 —— 全文校对稿")
w("")
w("> 本文件由 `game.html` 里的 `LEVELS` 与 `RUBY` **自动生成**，不是另抄一份。")
w("> 游戏里学生看到的每一个字都在这里；改了游戏就重跑一次，两边不会走样。")
w("> 生成方式：`python3 tools/dump-script.py`")
w("")
w("**总分**：%d 分（%s）　**版面**：%d 个　**日期**：2026-08-24"
  % (TOTAL, " · ".join("%s %d" % (l["n"], lmax(l)) for l in LEVELS),
     sum(len(l["panels"]) for l in LEVELS)))
w("")
w("> 满分是从题库**算出来**的，不是写死的。上传 SLS 时 **Maximum Marks 请设成 %d**。" % TOTAL)
w("")
w("## 计分规则")
w("")
w("每张卡片**第一次就放对**才得 1 分。放错的卡片轻弹回原位，人物滑一跤再站起来 ——")
w("不扣分、不设生命值，学生可以一直试到对为止，所以人人都走得完；")
w("但分数记的是第一次的判断，教师后台的数字才有诊断价值。")
w("多选题与选择题同理：第一次按「确定」就对才得分。重做整关时，分数**取最好的一次**。")
w("")
w("---")
w("")
w("## 一、画面文字（非题目）")
w("")
w("### 开场（输入姓名与班级）")
w("")
w("- 标题：**⛰️ 书山登顶**；副题：单元五《学无止境》· 三关共 %d 分" % TOTAL)
w("- 输入栏：姓名 Name（上限 12 字）、班级 Class（上限 10 字）")
w("- 规矩①：**请在 SLS 里作答，不要另开分页。**另开分页，你的分数记录不到。")
w("- 规矩②：**三关做完会出现登顶画面**，请自行截图，交到 SLS 作为完成凭证。")
w("- 附注：姓名只存在这台装置上，不会上传，也不随分数传送。")
w("")
w("### 选角色")
w("")
w("- 标题：选一个角色；说明：这个角色会陪你爬完三关。")
w("- 四个发型：" + " / ".join(AV_NAMES))
w("")
w("### 收关（登顶画面）")
w("")
w("> 《学然后知不足》先反后正，《终身学习》先正后反，两篇课文都用了**对比论证法**。")
w("")
w("成绩单显示：姓名、班级、三关分数与用时、总分 /%d、总用时、完成日期与时间、验证码。" % TOTAL)
w("")
w("---")
w("")

CN = ["二", "三", "四"]
for li, lv in enumerate(LEVELS):
    w("## %s、%s · %s（%d 分）" % (CN[li], lv["n"], lv["t"], lmax(lv)))
    w("")
    for pi, d in enumerate(lv["panels"]):
        kind = d.get("k")
        w("### 版面 %d · %s（%d 分）" % (pi + 1, d["hd"], pmax(d)))
        w("")
        w("**指示（华文）**：" + B(d["tip"]["zh"]))
        w("")
        w("**指示（English）**：" + d["tip"]["en"])
        w("")
        if kind == "slots":
            w("**格子**：" + "　".join(
                "「%s%s」" % (x["t"], (" · " + x["sub"]) if x.get("sub") else "")
                for x in d["slots"]))
            w("")
            w("| # | 卡片（学生看到的文字） | 正确归属 |")
            w("|---|---|---|")
            for i, c in enumerate(d["cards"]):
                where = ("**干扰项**（不属于任何格子）" if c["s"] < 0
                         else "「%s」" % d["slots"][c["s"]]["t"])
                w("| %d.%d | %s | %s |" % (pi + 1, i + 1, c["t"], where))
        elif kind == "multi":
            w("**题目**：" + d["q"])
            w("")
            w("| 选项 | 是否选中 |")
            w("|---|---|")
            for o in d["opts"]:
                w("| %s | %s |" % (o["t"], "✅ **要选**" if o["ok"] else "❌ 不选"))
            w("")
            w("（全部选对才得 1 分）")
        else:
            w("**题目**：" + d["q"])
            w("")
            w("| 选项 | 答案 |")
            w("|---|---|")
            for i, o in enumerate(d["opts"]):
                w("| %s | %s |" % (o, "✅ **正确**" if i == d["a"] else "❌"))
        w("")
        w("**答后讲解**：" + B(d["e"]))
        w("")
    w("---")
    w("")

w("## 五、拼音（人工撰写，请重点校对）")
w("")
w("采用**方案甲**：只标课本已注音的词语。不用转换函式库 —— 官方禁用外部函式库，")
w("而且自动转换必错在多音字上。以下每一条都是手写的，请逐条过目。")
w("")
w("| 词语 | 拼音 |")
w("|---|---|")
for k, v in RUBY.items():
    w("| %s | %s |" % (k, v))
w("")
w("特别留意的多音字：**好**学 hào（非 hǎo）、**乐**在其中 lè（非 yuè）、")
w("逆水**行**舟 xíng（非 háng）、虚心请**教** jiào（非 jiāo）。")
w("")
w("---")
w("")
w("## 六、审阅后的决定 ｜ Decisions taken at review")
w("")
w("下列各项已由科任老师定案，游戏已照此建置。此处留档，日后改题时不必重新讨论。")
w("")
w("| 出处 | 决定 |")
w("|---|---|")
w("| 第二关 · 反问句判断 | 「人生就像一场盛大的演出，我们如何在这场演出中找准自己的位置呢？」"
  "**确认不是反问句** —— 此句为真疑问，是本版面唯一的否定项，也是鉴别点。已复核。 |")
w("| 第二关 · 第1段的修辞手法 | **答案只取「排比」**，不含比喻。已由多选改回单选；"
  "「比喻」留作干扰项，因为那是最像的那个错答案。 |")
w("| 第二关 · 引用语句配意思 | **已整个删去**（原 3 分）。三条引语的「意思」是课本留白处的拟答，"
  "不是可以据以评分的定本 —— 开放式的答案不该在这个游戏里自动批改。 |")
w("| 第三关 · 俗语的意思 | **已整个删去**（原 1 分）。另两个选项是建置时拟的，未经审定。 |")
w("| 第三关 · 篇章结构 | 第4段与第5段合并为一张卡，**确认可行**。 |")
w("")
w("两个版面删去后，总分由 40 降为 %d 分。**上传 SLS 时 Maximum Marks 要设成 %d。**" % (TOTAL, TOTAL))
w("")

dst = os.path.join(ROOT, "docs", "全文校对稿.md")
os.makedirs(os.path.dirname(dst), exist_ok=True)
open(dst, "w", encoding="utf-8").write("\n".join(L))
print("docs/全文校对稿.md  %.1f KB  ·  %d 关 %d 版面 %d 条拼音"
      % (len("\n".join(L)) / 1024, len(LEVELS),
         sum(len(l["panels"]) for l in LEVELS), len(RUBY)))
