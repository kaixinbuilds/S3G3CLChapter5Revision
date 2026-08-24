"""
读 game.html 的题库 ｜ Read the question bank out of game.html

题库只有一本，就在 game.html 的 LEVELS 里。任何脚本要知道「满分是多少」，
都得从这里算，不准自己写一个数字 —— 上一版就是因为 build-sls.py 里
硬写了 40，删了两个版面之后它还在叫人把 Maximum Marks 设成 40。

There is exactly one question bank, in game.html's LEVELS. Any script that
needs the maximum computes it from here rather than hard-coding a number: the
previous version had 40 written into build-sls.py, and after two panels were
removed it went on telling people to set Maximum Marks to 40.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _grab(src, name, open_ch, close_ch):
    i = src.index("const " + name + " = ")
    i = src.index(open_ch, i)
    depth, j, in_str = 0, i, False
    while j < len(src):
        c = src[j]
        if in_str:
            if c == "\\": j += 2; continue
            if c == "'": in_str = False
        elif c == "'": in_str = True
        elif c == "/" and src[j+1:j+2] == "*":
            j = src.index("*/", j) + 2; continue
        elif c == open_ch: depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0: return src[i:j+1]
        j += 1
    sys.exit("unterminated literal: " + name)


def _to_json(src):
    """JS 字面量 → JSON ｜ JS literal -> JSON"""
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c == "'":
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
        elif c.isalpha() or c == "_":
            j = i
            while j < n and (src[j].isalnum() or src[j] in "_$"): j += 1
            word, k = src[i:j], j
            while k < n and src[k] in " \t\n": k += 1
            out.append(json.dumps(word) if (k < n and src[k] == ":") else word)
            i = j
        else:
            out.append(c); i += 1
    return re.sub(r",(\s*[\]}])", r"\1", "".join(out))


def load(path=None):
    """回传 (LEVELS, RUBY, AV_NAMES) ｜ returns (LEVELS, RUBY, AV_NAMES)"""
    src = open(path or os.path.join(ROOT, "game.html"), encoding="utf-8").read()
    people = _grab(src, "PEOPLE", "[", "]")
    levels = _grab(src, "LEVELS", "[", "]").replace("slots:PEOPLE", "slots:" + people)
    return (json.loads(_to_json(levels)),
            json.loads(_to_json(_grab(src, "RUBY", "{", "}"))),
            json.loads(_to_json(_grab(src, "AV_NAMES", "[", "]"))))


def panel_max(d):
    """每张可放的卡片 1 分；选择题与多选题各 1 分
       One mark per placeable card; one for a choice or multi question"""
    return len([c for c in d["cards"] if c["s"] >= 0]) if d.get("k") == "slots" else 1

def level_max(lv):
    return sum(panel_max(d) for d in lv["panels"])

def total_max(levels):
    return sum(level_max(l) for l in levels)


def pass_mark(levels, frac=0.65):
    """登顶门槛：满分的 65%，往上取整。与 game.html 里的 PASS 同一条算式。
       The summit threshold: 65% of the maximum, rounded up — the same
       expression as PASS in game.html."""
    import math
    return math.ceil(total_max(levels) * frac)
