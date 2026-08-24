"""
game.html 里的拼音字典  →  assets/pinyin.js
game.html's pinyin dictionary  ->  assets/pinyin.js

网页上的指示与导航文字也要能标拼音，用的必须是<b>同一本字典</b> ——
两边各写一份，迟早会有一个词在游戏里注 hào、在网页上注 hǎo。
The website's instructions need pinyin too, and it must come from the SAME
dictionary. Two hand-kept copies would eventually disagree on a heteronym,
which is exactly the failure this whole approach exists to avoid.

用法 ｜ Usage:  python3 tools/build-pinyin.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "game.html"), encoding="utf-8").read()

m = re.search(r"/\* ▼▼▼ PINYIN-START ▼▼▼.*?\*/\n(.*?)/\* ▲▲▲ PINYIN-END ▲▲▲ \*/", src, re.S)
if not m:
    sys.exit("PINYIN markers not found in game.html")
body = m.group(1).rstrip()

out = '''/* ══════════════════════════════════════════════════════════════
   拼音 ｜ Pinyin
   本档由 tools/build-pinyin.py 从 game.html 抽出，请勿手改。
   要加词或改音，改 game.html 里 PINYIN-START 那一段，再重跑脚本。
   Generated from game.html by tools/build-pinyin.py — do not edit by hand.
   ══════════════════════════════════════════════════════════════ */
(function(global){
"use strict";

''' + body + '''

global.RUBY = RUBY;
global.zhRuby = zh;

/* 把页面上标了 .zh 的中文，照字典包成 <ruby>。
   只碰文字节点，不动标签，所以连结、粗体、样式都原封不动。
   Wrap the dictionary's words in <ruby> inside anything tagged .zh. Only text
   nodes are touched, so links, bold and styling survive untouched. */
global.applyRuby = function(root){
  var nodes = (root || document).querySelectorAll('.zh, [data-py]');
  Array.prototype.forEach.call(nodes, function(el){
    if(el.dataset.pyDone) return;
    el.dataset.pyDone = '1';
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    var texts = [], n;
    while((n = walker.nextNode())) texts.push(n);
    texts.forEach(function(t){
      if(t.parentNode && t.parentNode.tagName === 'RT') return;
      var html = zh(t.nodeValue.replace(/[&<>]/g, function(c){
        return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c];
      }));
      if(html.indexOf('<ruby>') < 0) return;
      var span = document.createElement('span');
      span.innerHTML = html;
      t.parentNode.replaceChild(span, t);
    });
  });
};
})(window);
'''
dst = os.path.join(ROOT, "assets", "pinyin.js")
open(dst, "w", encoding="utf-8").write(out)
print(f"assets/pinyin.js written ({len(out)/1024:.1f} KB)")
