"""
核对三份档案是不是同一个东西 ｜ Check the three artefacts really are the same game

  game.html        网页版 / GitHub Pages ｜ the web build
  sls/index.html   SLS 版（由 build-sls.py 生成）｜ the SLS build
  unit5sls.zip     上传 SLS 的压缩档 ｜ the archive you upload

改了游戏却忘了重跑 build-sls.py，是这个专案最容易犯、也最难发现的错：
网页上看起来好好的，学生在 SLS 里做的却是旧版，而且画面上没有任何迹象。
这个脚本把它变成一句话就能查的事。

Editing the game and forgetting to re-run build-sls.py is the easiest mistake
to make here and the hardest to notice: the website looks right while students
in SLS get the old version, with nothing on screen to say so. This turns that
into a one-command check.

用法 ｜ Usage:  python3 tools/check-builds.py
"""
import os, re, sys, zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
web  = open(os.path.join(ROOT, "game.html"), encoding="utf-8").read()
slsp = os.path.join(ROOT, "sls", "index.html")
sls  = open(slsp, encoding="utf-8").read()

fails = []
def check(label, ok, hint=""):
    print(("  ✅ " if ok else "  ❌ ") + label + ("" if ok else "  → " + hint))
    if not ok: fails.append(label)


def strip(t):
    """去掉两版<b>应该</b>不同的部分，剩下的必须一字不差
       Remove the parts that are SUPPOSED to differ; the rest must match exactly"""
    t = re.sub(r"/\* ═+\n   三、记分接口.*?SLS-HOOK-END ▲▲▲ \*/", "<HOOK>", t, flags=re.S)
    t = re.sub(r"<script>\n/\*! xAPIWrapper.*?</script>\n", "", t, flags=re.S)
    for a, b in [
        ("这是「SLS 版」：内嵌 xAPIWrapper，做完自动把分数送进教师后台。",
         "这是「网页版」：没有 xAPI，分数只显示在画面上，不会送进 SLS。"),
        ("  网页版在 game.html，内容一字不差，只少了记分程式码。",
         "  SLS 版在 sls/index.html，内容一字不差，只多了记分程式码。"),
        ("  This is the SLS build: xAPIWrapper embedded, scores land in the gradebook.\n"
         "  The web build is game.html — identical content, minus the scoring code.",
         "  This is the WEB build: no xAPI, the score only ever shows on screen.\n"
         "  The SLS build is sls/index.html — identical content, plus the scoring code."),
    ]:
        t = t.replace(a, b)
    return t


print("三份档案核对 ｜ Build consistency check\n")

check("两版除了记分程式码一字不差 ｜ builds identical apart from the scoring code",
      strip(web) == strip(sls),
      "跑 python3 tools/build-sls.py 重建 ｜ re-run build-sls.py")

zp = os.path.join(ROOT, "unit5sls.zip")
if not os.path.exists(zp):
    check("unit5sls.zip 存在 ｜ archive exists", False, "跑 build-sls.py ｜ run build-sls.py")
else:
    z = zipfile.ZipFile(zp)
    names = z.namelist()
    check("zip 内只有一个 index.html，无资料夹 ｜ single index.html, no folders",
          names == ["index.html"], f"实际内容 ｜ found {names}")
    check("zip 与 sls/index.html 逐字节相同 ｜ archive matches the built file",
          z.read("index.html").decode("utf-8") == sls,
          "跑 build-sls.py 重新打包 ｜ re-run build-sls.py")

check("SLS 版内嵌 xAPIWrapper ｜ library inlined in the SLS build",
      "xAPIWrapper v 1.11.0" in sls)
check("SLS 版送的是累计总分 ｜ SLS build sends the running total",
      "XAPI.sendScore(total(), MAX)" in sls)
check("网页版不含 xAPI ｜ web build carries no xAPI",
      "ADL.XAPIWrapper" not in web)
check("没有对外引用 ｜ no external references in the SLS build",
      'src="http' not in sls and "src='http" not in sls,
      "SLS 的 sandbox 会挡掉 ｜ the SLS sandbox blocks these")

levels, ruby, _ = bank.load()
mx = bank.total_max(levels)
panels = sum(len(l["panels"]) for l in levels)
missing_src = [d["hd"] for l in levels for d in l["panels"] if not d.get("src")]
check("每个版面都标了课本出处 ｜ every panel names its place in the textbook",
      not missing_src, f"缺 ｜ missing: {missing_src}")

print(f"\n题库 ｜ bank: {len(levels)} 关 {panels} 版面 {mx} 分 · {len(ruby)} 条拼音")
print(f"上传 SLS 时 Maximum Marks 设 {mx} ｜ set Maximum Marks to {mx}")

if fails:
    print(f"\n❌ {len(fails)} 项不通过 ｜ {len(fails)} check(s) failed")
    sys.exit(1)
print("\n✅ 全部通过 ｜ all checks passed")
