"""
game.html 里的山景程式码  →  assets/scene.js
game.html's scenery code  ->  assets/scene.js

网站的页面（落地页、三条老师路径）要用同一片山景，但游戏本身必须是单一自足档案 ——
SLS 的 sandbox 不准引用外部档案。两边都要，又不能各写一份，所以从游戏里抽出来。
The website pages reuse the same scenery, but the game itself has to stay a
single self-contained file (the SLS sandbox blocks external files). Both need
it and neither may drift, so the website's copy is extracted from the game.

用法 ｜ Usage:  python3 tools/build-scene.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "game.html"), encoding="utf-8").read()

m = re.search(r"/\* ▼▼▼ SCENE-START ▼▼▼.*?\*/\n(.*?)/\* ▲▲▲ SCENE-END ▲▲▲ \*/", src, re.S)
if not m:
    sys.exit("SCENE markers not found in game.html")
body = m.group(1).rstrip()

out = '''/* ══════════════════════════════════════════════════════════════
   山景 ｜ The scenery
   本档由 tools/build-scene.py 从 game.html 抽出，请勿手改 ——
   要改山形、配色、云或太阳，改 game.html 里 SCENE-START 那一段，再重跑脚本。
   Generated from game.html by tools/build-scene.py — do not edit by hand.
   To change the hills, palette, clouds or sun, edit the SCENE-START block in
   game.html and re-run the script.
   ══════════════════════════════════════════════════════════════ */
(function(global){
"use strict";

/* 网页版不画人物，这几个常量只是让抽出来的程式码跑得起来
   The website never draws the character; these constants just satisfy the
   extracted code, whose avatar branches are never taken. */
var AV_SRC = "", AV_COLS = 5, AV_ROWS = 4, CELL_W = 112, CELL_H = 140;
var S = {av:0};

''' + body + '''

global.sceneSVG = sceneSVG;

/* 量好容器的形状，再把山景画进去 ｜ measure the box, then paint the scene into it */
global.fitScene = function(node, opt){
  if(!node) return;
  var w = node.clientWidth || 800, h = node.clientHeight || 260;
  opt = opt || {};
  opt.aspect = w / Math.max(1, h);
  node.innerHTML = sceneSVG(opt);
};
})(window);
'''
dst = os.path.join(ROOT, "assets", "scene.js")
open(dst, "w", encoding="utf-8").write(out)
print(f"assets/scene.js written ({len(out)/1024:.1f} KB)")
