/* ══════════════════════════════════════════════════════════════
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

/* 山丘的高点（比例）—— 只给这几个点，中间的起伏由 smoothD() 补成圆缓的曲线
   The hilltops as fractions; smoothD() rounds the gaps into rolling curves */
/* 三条山脊都从左边低处一路升到右边的山顶 ——
   横平的山形配一条上扬的小路，看起来只是路在爬，山没有在爬。
   All three ridges climb from a low left to the summit on the right. Level
   ridges under a rising path read as "the path climbs", not "we are climbing". */
const FARn  = [[0,.63],[.20,.51],[.40,.47],[.57,.34],[.735,.19],[.88,.28],[1,.25]];
const MIDn  = [[0,.79],[.20,.69],[.40,.63],[.58,.52],[.75,.41],[.90,.48],[1,.46]];
const NEARn = [[0,.94],[.22,.86],[.44,.79],[.64,.70],[.82,.72],[1,.70]];
const SUMMIT = [.735,.19];     /* 插旗的地方 ｜ where the flag goes */
const SUN    = [.915,.165];    /* 太阳，离旗子远远的 ｜ the sun, well clear of the flag */
const TRAILn = [[.04,.965],
  [.20,.92,.13,.835,.30,.808], [.46,.782,.34,.675,.50,.648],
  [.62,.625,.55,.505,.655,.435], [.71,.392,.69,.262,SUMMIT[0],SUMMIT[1]]];

const px = (n,W,H) => n.map(([x,y])=>[+(x*W).toFixed(1), +(y*H).toFixed(1)]);

/* 折线 → 圆缓的曲线（Catmull-Rom 转贝塞尔）。
   山要「连绵」不要「锯齿」，靠的就是这一步：只给高点，让曲线自己圆过去。
   Polyline -> rolling curve (Catmull-Rom converted to beziers). This is what
   makes the hills roll instead of zigzag: give only the hilltops and let the
   curve round its own way between them. */
function smoothD(pts){
  let d = 'M' + pts[0][0] + ',' + pts[0][1];
  for(let i=0;i<pts.length-1;i++){
    const p0 = pts[i-1] || pts[i], p1 = pts[i], p2 = pts[i+1], p3 = pts[i+2] || pts[i+1];
    d += ' C' + (p1[0]+(p2[0]-p0[0])/6).toFixed(1) + ',' + (p1[1]+(p2[1]-p0[1])/6).toFixed(1) +
         ' '  + (p2[0]-(p3[0]-p1[0])/6).toFixed(1) + ',' + (p2[1]-(p3[1]-p1[1])/6).toFixed(1) +
         ' '  + p2[0] + ',' + p2[1];
  }
  return d;
}
const hill = (pts,W,H) => smoothD(pts) + ' L'+W+','+H + ' L0,'+H + ' Z';

/* 曲线上某一点的高度 —— 树要长在山坡上，不能浮在半空
   Height of the curve at x, so trees sit on the slope instead of hovering */
function curveY(pts,x){
  for(let i=1;i<pts.length;i++){
    if(x <= pts[i][0]){
      const [x0,y0]=pts[i-1], [x1,y1]=pts[i];
      const t = (x-x0)/(x1-x0 || 1);
      return y0 + (y1-y0) * (t*t*(3-2*t));      /* 平滑内插，配合圆缓的山形 ｜ smoothstep, to match */
    }
  }
  return pts[pts.length-1][1];
}
/* 圆头的树，配得上圆缓的山 ｜ round-topped trees, to match round-topped hills */
function trees(pts,n,h,W,fill){
  let o = '';
  for(let i=0;i<n;i++){
    const x = W*(.03 + i*(.94/(n-1))), y = curveY(pts,x)+1;
    const r = h*.44;
    o += '<g transform="translate('+x.toFixed(1)+','+y.toFixed(1)+')" fill="'+fill+'">' +
         '<rect x="'+(-h*.07).toFixed(1)+'" y="'+(-h*.34).toFixed(1)+'" width="'+(h*.14).toFixed(1)+
           '" height="'+(h*.36).toFixed(1)+'"/>' +
         '<circle cx="0" cy="'+(-h*.55).toFixed(1)+'" r="'+r.toFixed(1)+'"/>' +
         '<circle cx="'+(-r*.7).toFixed(1)+'" cy="'+(-h*.34).toFixed(1)+'" r="'+(r*.72).toFixed(1)+'"/>' +
         '<circle cx="'+(r*.7).toFixed(1)+'" cy="'+(-h*.34).toFixed(1)+'" r="'+(r*.72).toFixed(1)+'"/></g>';
  }
  return o;
}
/* 云会慢慢飘 —— 动画写在 CSS 里，外层管飘、内层管摆位，两个 transform 才不打架
   Drifting clouds: the animation is CSS. An outer <g> drifts and an inner <g>
   positions, so the two transforms don't fight over the same attribute */
function clouds(list,W,H){
  return list.map(([fx,fy,sc,o],i)=>
    '<g class="cloud c'+(i%4)+'">' +
      '<g transform="translate('+(fx*W).toFixed(1)+','+(fy*H).toFixed(1)+') scale('+(sc*H/135).toFixed(3)+')" opacity="'+o+'">' +
        '<ellipse cx="0" cy="0" rx="17" ry="8"/><ellipse cx="13" cy="3" rx="12" ry="6.5"/>' +
        '<ellipse cx="-13" cy="3" rx="11" ry="6"/><ellipse cx="4" cy="-6" rx="10.5" ry="7"/>' +
        '<ellipse cx="-6" cy="-4" rx="9" ry="6"/></g></g>').join('');
}
function trailD(W,H){
  let d = 'M' + (TRAILn[0][0]*W).toFixed(1) + ',' + (TRAILn[0][1]*H).toFixed(1);
  for(let i=1;i<TRAILn.length;i++){
    const c = TRAILn[i];
    d += ' C' + (c[0]*W).toFixed(1)+','+(c[1]*H).toFixed(1) + ' ' +
                (c[2]*W).toFixed(1)+','+(c[3]*H).toFixed(1) + ' ' +
                (c[4]*W).toFixed(1)+','+(c[5]*H).toFixed(1);
  }
  return d;
}

let sceneN = 0;   /* 同一页上好几幅山景，渐层 id 不能撞 ｜ ids must not collide between scenes */

function sceneSVG(o){
  o = o || {};
  const H = 220, W = Math.round(H * Math.max(.75, Math.min(6, o.aspect || 1.8)));
  const u = '_' + (++sceneN);
  const far = px(FARn,W,H), mid = px(MIDn,W,H), near = px(NEARn,W,H);
  const sx = SUMMIT[0]*W, sy = SUMMIT[1]*H;
  const sunX = SUN[0]*W, sunY = SUN[1]*H;
  const av = H*.15, flag = H*.125;

  const cell = (id,x,y,w,row,col) =>
    '<svg' + (id?' id="'+id+'"':'') + ' x="'+x.toFixed(1)+'" y="'+y.toFixed(1)+
    '" width="'+w.toFixed(1)+'" height="'+(w*CELL_H/CELL_W).toFixed(1)+
    '" viewBox="'+(col*CELL_W)+' '+(row*CELL_H)+' '+CELL_W+' '+CELL_H+'">' +
    '<image href="'+AV_SRC+'" x="0" y="0" width="'+(AV_COLS*CELL_W)+'" height="'+(AV_ROWS*CELL_H)+
    '" style="image-rendering:pixelated"/></svg>';

  /* 推近山顶时，取景框要<b>夹在画面之内</b>。
     不夹的话，框会越过右边界 —— 那一块没有东西可画，露出的是页面底色，
     看起来就像风景旁边多了一条黑带。
     When pushing in on the summit, the window must be clamped inside the
     artwork. Unclamped it runs past the right edge, where there is nothing to
     paint, and the page background shows through as a dark band beside the
     scenery. */
  let vb = '0 0 '+W+' '+H;
  if(o.zoom){
    const vw = W*o.zoom, vh = H*o.zoom;
    const vx = Math.max(0, Math.min(W - vw, sx - vw*.42));
    const vy = Math.max(0, Math.min(H - vh, sy - vh*.30));
    vb = [vx.toFixed(1), vy.toFixed(1), vw.toFixed(1), vh.toFixed(1)].join(' ');
  }

  return '<svg viewBox="'+vb+'" preserveAspectRatio="'+(o.fit||'xMidYMid slice')+'">' +
    '<defs>' +
      /* 蓝天：上头深一点，接近地平线转淡 ｜ blue sky, paler toward the horizon */
      '<linearGradient id="sky'+u+'" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0" stop-color="#2b8fd6"/><stop offset=".55" stop-color="#79c4ee"/>' +
        '<stop offset="1" stop-color="#cfeafb"/></linearGradient>' +
      '<radialGradient id="glow'+u+'"><stop offset="0" stop-color="#FFE479" stop-opacity=".95"/>' +
        '<stop offset=".45" stop-color="#FFC72C" stop-opacity=".45"/>' +
        '<stop offset="1" stop-color="#FFC72C" stop-opacity="0"/></radialGradient>' +
      /* 三层绿：远淡近深，做出纵深 ｜ three greens, hazier far away */
      '<linearGradient id="far'+u+'" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0" stop-color="#9fd3ae"/><stop offset="1" stop-color="#77b98f"/></linearGradient>' +
      '<linearGradient id="mid'+u+'" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0" stop-color="#5cae76"/><stop offset="1" stop-color="#3c8a57"/></linearGradient>' +
      '<linearGradient id="near'+u+'" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0" stop-color="#358f57"/><stop offset="1" stop-color="#1c6238"/></linearGradient>' +
    '</defs>' +
    '<rect width="'+W+'" height="'+H+'" fill="url(#sky'+u+')"/>' +
    /* 太阳：黄，外面一圈会呼吸的光晕 ｜ a yellow sun inside a breathing halo */
    '<g class="sun"><circle cx="'+sunX.toFixed(1)+'" cy="'+sunY.toFixed(1)+'" r="'+(H*.27).toFixed(1)+
      '" fill="url(#glow'+u+')"/></g>' +
    '<circle cx="'+sunX.toFixed(1)+'" cy="'+sunY.toFixed(1)+'" r="'+(H*.075).toFixed(1)+'" fill="#FFDC4A"/>' +
    '<circle cx="'+sunX.toFixed(1)+'" cy="'+sunY.toFixed(1)+'" r="'+(H*.054).toFixed(1)+'" fill="#FFF3B0"/>' +
    '<g fill="#ffffff">' + clouds([[.18,.22,1,.9],[.60,.14,.82,.78],[.40,.33,.6,.62],[.88,.38,.7,.5]],W,H) + '</g>' +
    '<path d="'+hill(far,W,H)+'"  fill="url(#far'+u+')"/>' +
    '<path d="'+hill(mid,W,H)+'"  fill="url(#mid'+u+')"/>' +
    trees(mid, Math.max(5, Math.round(W/95)), H*.045, W, '#2f7a4c') +
    '<path d="'+hill(near,W,H)+'" fill="url(#near'+u+')"/>' +
    trees(near, Math.max(6, Math.round(W/62)), H*.07, W, '#14512d') +
    '<path'+(o.trail?' id="'+o.trail+'"':'')+' d="'+trailD(W,H)+'" fill="none" stroke="#FFC72C" ' +
      'stroke-width="'+(H*.009).toFixed(2)+'" stroke-dasharray="'+(H*.023).toFixed(1)+' '+(H*.027).toFixed(1)+
      '" stroke-linecap="round" opacity=".8"/>' +
    '<g transform="translate('+sx.toFixed(1)+','+sy.toFixed(1)+')">' +
      '<line x1="0" y1="0" x2="0" y2="'+(-flag).toFixed(1)+'" stroke="#8a5a2b" stroke-width="'+(H*.011).toFixed(2)+'"/>' +
      '<path d="M0,'+(-flag).toFixed(1)+' L'+(flag*.72).toFixed(1)+','+(-flag*.75).toFixed(1)+
        ' L0,'+(-flag*.5).toFixed(1)+' Z" fill="#FFC72C"/></g>' +
    /* 站在旗子旁边的山坡上 —— 脚底的高度要从山形曲线上量，
       照搬山顶的高度就会浮在半空（旗子左边的地面本来就比较低）。
       Standing on the slope beside the flag: the feet height is measured off
       the hill curve. Reusing the summit's height would leave the character
       hovering, because the ground left of the flag is lower. */
    (o.avatar == null ? '' : (function(){
      const ax = sx - av*1.15;
      return cell(null, ax - av/2, curveY(far, ax) - av*CELL_H/CELL_W, av, avRow(o.avatar), 3);
    })()) +
    (o.hiker ? cell('hiker', 0, 0, H*.17, avRow(S.av), 0) : '') +
  '</svg>';
}

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
