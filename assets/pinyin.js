/* ══════════════════════════════════════════════════════════════
   拼音 ｜ Pinyin
   本档由 tools/build-pinyin.py 从 game.html 抽出，请勿手改。
   要加词或改音，改 game.html 里 PINYIN-START 那一段，再重跑脚本。
   Generated from game.html by tools/build-pinyin.py — do not edit by hand.
   ══════════════════════════════════════════════════════════════ */
(function(global){
"use strict";

const RUBY = {
  /* —— 课本注音词语 ｜ words annotated in the textbook —— */
  '雄鹰':'xióng yīng','渺小':'miǎo xiǎo','寓言':'yù yán','奥妙':'ào miào',
  '浅尝辄止':'qiǎn cháng zhé zhǐ','哲学':'zhé xué','比喻':'bǐ yù','热忱':'rè chén',
  '持之以恒':'chí zhī yǐ héng','清澈':'qīng chè','干涸':'gān hé','浇灌':'jiāo guàn',
  '楷模':'kǎi mó','孜孜不倦':'zī zī bù juàn','敷衍':'fū yǎn','淘汰':'táo tài',
  '佐证':'zuǒ zhèng','平庸':'píng yōng','阶段':'jiē duàn','同侪':'tóng chái',
  '撰写':'zhuàn xiě','筹备':'chóu bèi','募捐':'mù juān','实践':'shí jiàn',
  '震撼':'zhèn hàn','循规蹈矩':'xún guī dǎo jǔ','融会贯通':'róng huì guàn tōng',
  '腼腆':'miǎn tiǎn','咨询':'zī xún','分析':'fēn xī','桨':'jiǎng','岂':'qǐ',

  /* —— 多音字：自动转换一定错在这几个上 ｜ heteronyms: where auto-conversion always fails —— */
  '好学':'hào xué',                 /* 不是 hǎo ｜ not hǎo */
  '乐在其中':'lè zài qí zhōng',      /* 不是 yuè ｜ not yuè */
  '逆水行舟':'nì shuǐ xíng zhōu',    /* 不是 háng ｜ not háng */
  '虚心请教':'xū xīn qǐng jiào',     /* 不是 jiāo ｜ not jiāo */
  '应用':'yìng yòng',                /* 不是 yīng ｜ not yīng */
  '差不多':'chà bu duō',             /* 不是 chā ｜ not chā */
  '兴趣':'xìng qù',                  /* 不是 xīng ｜ not xīng */

  /* —— 人名与专名 ｜ names —— */
  '芝诺':'zhī nuò','朱熹':'zhū xī','鲁迅':'lǔ xùn','笛卡尔':'dí kǎ ěr',
  '方仲永':'fāng zhòng yǒng','李光耀':'lǐ guāng yào','楚国':'chǔ guó',

  /* —— 本单元反复出现的语文术语与成语 ｜ recurring terms and idioms —— */
  '反问句':'fǎn wèn jù','排比':'pái bǐ','论证':'lùn zhèng','引论':'yǐn lùn',
  '本论':'běn lùn','结论':'jié lùn','论点':'lùn diǎn','手足无措':'shǒu zú wú cuò',
  '骄傲自满':'jiāo ào zì mǎn','死记硬背':'sǐ jì yìng bèi','纸上谈兵':'zhǐ shàng tán bīng',
  '天资聪颖':'tiān zī cōng yǐng','赞叹':'zàn tàn','夸耀':'kuā yào','软技能':'ruǎn jì néng',
  '实习':'shí xí','义工':'yì gōng','策划':'cè huà','讲座':'jiǎng zuò','精明':'jīng míng',
  '增广见闻':'zēng guǎng jiàn wén','律师':'lǜ shī','总理':'zǒng lǐ','刻苦攻读':'kè kǔ gōng dú'
};
/* 长词优先，免得「好学」被「学」之类的短词抢先切开
   Longest-first, so 好学 isn't broken apart by a shorter key */
const RUBY_RE = new RegExp(Object.keys(RUBY).sort((a,b)=>b.length-a.length).join('|'),'g');

/* 把词语包成 <ruby>，一个汉字配一个音节 ｜ wrap a word as <ruby>, one syllable per character */
function zh(s){
  return String(s).replace(RUBY_RE, function(w){
    const py = RUBY[w].split(' ');
    if(py.length !== w.length) return w;        // 音节数对不上就不标 ｜ mismatch: leave it alone
    let out = '<ruby>';
    for(let i=0;i<w.length;i++) out += w[i] + '<rt>' + py[i] + '</rt>';
    return out + '</ruby>';
  });
}

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
