/* ════════════════════════════════════════════════
   老师页面共用脚本 ｜ Shared script for the teacher-facing pages
   ① 语言切换：华文 / 双语 / English —— 记住选择，换页也保持
   ① Language switch: Chinese / bilingual / English — remembered across pages
   ② 拼音开关 ｜ ② the pinyin toggle
   ③ 提示语「复制」按钮 ｜ ③ copy buttons for the ready-made AI prompts

   两个开关用的 localStorage 键，跟 game.html 里的是同一组 ——
   学生在落地页开了拼音，进游戏还是开着；在游戏里关掉，退回来也还是关着。
   （SLS 里的游戏跑在 sandbox iframe，同源不成立，那一份只能各记各的。）
   Both switches use the SAME localStorage keys as game.html, so a student who
   turns pinyin on here still has it on inside the game, and vice versa. (The
   SLS build runs in a sandboxed iframe, a different origin, so that copy
   necessarily keeps its own setting.)
   ════════════════════════════════════════════════ */
(function(){
  var KEY='u5_lang', DEFAULT='both';
  var PY_KEY='u5_pinyin';

  var saved=DEFAULT;
  try{saved=localStorage.getItem(KEY)||DEFAULT}catch(e){}
  document.documentElement.dataset.lang=saved;      // 先设好，避免闪一下 ｜ set early to avoid a flash

  function setLang(l){
    document.documentElement.dataset.lang=l;
    document.documentElement.lang=(l==='en')?'en':'zh-Hans';
    try{localStorage.setItem(KEY,l)}catch(e){}
    document.querySelectorAll('.seg button[data-lang]').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.lang===l));
    });
  }

  var pyOn=false;
  try{pyOn=localStorage.getItem(PY_KEY)==='1'}catch(e){}
  document.documentElement.classList.toggle('py',pyOn);

  function setPy(on){
    pyOn=on;
    document.documentElement.classList.toggle('py',on);
    try{localStorage.setItem(PY_KEY,on?'1':'0')}catch(e){}
    var b=document.getElementById('pyToggle');
    if(b)b.setAttribute('aria-pressed',String(on));
    /* 第一次开才做标注，之后只切换显示 —— 标注一次就够，重复走 DOM 没意义
       Annotate once on first use, then only toggle visibility */
    if(on&&window.applyRuby)window.applyRuby(document);
  }

  // 语言切换列：写进页面里 id="langbar" 的位置
  // The switch renders into whatever element has id="langbar"
  function mountLangBar(){
    var host=document.getElementById('langbar');
    if(!host)return;
    host.className='langbar';
    host.innerHTML='<div class="seg" role="group" aria-label="Language">'+
      '<button type="button" data-lang="zh">华文</button>'+
      '<button type="button" data-lang="both">双语 Bilingual</button>'+
      '<button type="button" data-lang="en">English</button></div>'+
      '<button type="button" class="pytog" id="pyToggle" aria-pressed="false" '+
        'title="拼音 Pinyin">拼音 Pinyin</button>';
    host.querySelectorAll('.seg button').forEach(function(b){
      b.addEventListener('click',function(){setLang(b.dataset.lang)});
    });
    host.querySelector('#pyToggle').addEventListener('click',function(){setPy(!pyOn)});
    setLang(document.documentElement.dataset.lang||DEFAULT);
    setPy(pyOn);
  }

  // 「复制提示语」：按钮的 data-copy 指向要复制的 <pre> 的 id
  // Copy buttons: data-copy holds the id of the <pre> whose text should be copied
  function wireCopy(){
    document.querySelectorAll('[data-copy]').forEach(function(btn){
      btn.addEventListener('click',function(){
        var el=document.getElementById(btn.dataset.copy);
        if(!el)return;
        var text=el.innerText;
        var done=function(){
          var old=btn.dataset.label||btn.textContent;
          btn.dataset.label=old;
          btn.textContent='✓ 已复制 Copied';
          setTimeout(function(){btn.textContent=old},1800);
        };
        if(navigator.clipboard&&navigator.clipboard.writeText){
          navigator.clipboard.writeText(text).then(done,fallback);
        }else fallback();
        function fallback(){
          var ta=document.createElement('textarea');
          ta.value=text;ta.style.position='fixed';ta.style.opacity='0';
          document.body.appendChild(ta);ta.select();
          try{document.execCommand('copy');done()}catch(e){}
          document.body.removeChild(ta);
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded',function(){mountLangBar();wireCopy()});
  window.setLang=setLang;
  window.setPy=setPy;
})();
