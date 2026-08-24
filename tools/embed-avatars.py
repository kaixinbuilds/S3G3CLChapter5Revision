"""
把 assets/avatars.b64.txt 贴进 game.html 里 AV_SRC 的那一行。
Paste assets/avatars.b64.txt into the AV_SRC line of game.html.

用法 ｜ Usage:  python3 tools/build-avatars.py && python3 tools/embed-avatars.py
（之后再跑 tools/build-sls.py 重建 SLS 版 ｜ then re-run tools/build-sls.py)
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b64 = open(os.path.join(ROOT, "assets", "avatars.b64.txt")).read().strip()
path = os.path.join(ROOT, "game.html")
src = open(path, encoding="utf-8").read()

new, n = re.subn(r"(const AV_SRC = 'data:image/png;base64,)[^']*(';)",
                 lambda m: m.group(1) + b64 + m.group(2), src, count=1)
if n != 1:
    sys.exit("AV_SRC line not found in game.html")

open(path, "w", encoding="utf-8").write(new)
print(f"embedded {len(b64)/1024:.1f} KB of base64 into game.html")
print(f"game.html is now {len(new)/1024:.1f} KB")
