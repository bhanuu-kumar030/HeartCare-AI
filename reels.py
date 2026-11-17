import json

TEMPLATE = r"""
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:'Segoe UI',system-ui,-apple-system,sans-serif}
html,body{background:transparent;color:#fff}
#reel{position:relative;width:100%;max-width:760px;margin:0 auto;height:__H__px;border-radius:24px;
  overflow:hidden;box-shadow:0 10px 40px rgba(0,0,0,.5);transition:background .6s}
#bars{position:absolute;top:12px;left:14px;right:14px;display:flex;gap:5px;z-index:5}
.bar{flex:1;height:4px;border-radius:4px;background:rgba(255,255,255,.28);overflow:hidden}
.bar i{display:block;height:100%;width:0;background:#fff}
#slide{position:absolute;inset:0;padding:34px 26px 70px 26px;overflow-y:auto}
.emoji{font-size:54px;display:inline-block;animation:pop 1.6s ease-in-out infinite}
@keyframes pop{0%,100%{transform:scale(1)}50%{transform:scale(1.18)}}
h2{font-size:28px;margin:6px 0 14px 0;line-height:1.2;animation:rise .6s both}
ul{list-style:none}
li{font-size:19px;line-height:1.4;margin:0 0 11px 0;padding-left:26px;position:relative;
  opacity:0;animation:rise .6s forwards}
#slide.small li{font-size:16px;margin-bottom:8px;line-height:1.35}
#slide.small h2{font-size:24px}
li:before{content:"➤";position:absolute;left:0;color:#ffd166}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.note{font-size:12px;opacity:.7;margin-top:8px}
.viz{margin:6px 0 12px 0}
.lbl{font-size:14px;margin:6px 0 3px 0;opacity:.95}
.track{height:22px;border-radius:12px;background:rgba(255,255,255,.14);overflow:hidden}
.fill{height:100%;border-radius:12px;width:0;animation:grow 1.6s .4s forwards}
@keyframes grow{to{width:var(--w)}}
.donut{display:flex;align-items:center;gap:14px;margin-top:10px}
.donut circle.bg{stroke:rgba(255,255,255,.16)}
.donut circle.fg{stroke:#ff6b81;stroke-dasharray:0 251.2;animation:ring 1.8s .6s forwards}
@keyframes ring{to{stroke-dasharray:66.8 251.2}}
.plaque{transform-box:fill-box;transform-origin:center;transform:scaleY(0);animation:plq 4s .5s forwards}
@keyframes plq{to{transform:scaleY(1)}}
.cell{animation:flow 2.4s linear infinite}
@keyframes flow{from{transform:translateX(0)}to{transform:translateX(250px)}}
#ctrl{position:absolute;bottom:12px;left:0;right:0;display:flex;justify-content:center;gap:14px;z-index:6}
button{border:0;border-radius:999px;padding:8px 20px;font-size:18px;color:#fff;cursor:pointer;
  background:rgba(255,255,255,.18);backdrop-filter:blur(6px)}
button:active{transform:scale(.94)}
.zone{position:absolute;top:30px;bottom:60px;width:30%;z-index:4;cursor:pointer}
#zl{left:0}#zr{right:0}
.count{position:absolute;top:22px;right:18px;font-size:12px;opacity:.7;z-index:5}
</style>
<div id="reel">
  <div id="bars"></div>
  <div class="count" id="count"></div>
  <div id="slide"></div>
  <div class="zone" id="zl"></div><div class="zone" id="zr"></div>
  <div id="ctrl"><button id="prev">‹</button><button id="pp">⏸</button><button id="next">›</button></div>
</div>
<script>
const R = __DATA__;
const TICK = 50;
let DUR = 9000, i = 0, t = 0, paused = false;
const reel = document.getElementById('reel'), slide = document.getElementById('slide');
const bars = document.getElementById('bars'), count = document.getElementById('count');
R.forEach(() => { const b = document.createElement('div'); b.className = 'bar';
  b.innerHTML = '<i></i>'; bars.appendChild(b); });

function vizHTML(r) {
  if (r.viz === 'artery') {
    return `<div class="viz"><svg viewBox="0 0 300 110" width="100%">
      <rect x="6" y="14" width="288" height="82" rx="41" fill="#8a2a3a"/>
      <rect x="14" y="22" width="272" height="66" rx="33" fill="#c0152f"/>
      <ellipse class="plaque" cx="150" cy="26" rx="62" ry="17" fill="#f5d76e"/>
      <ellipse class="plaque" cx="150" cy="84" rx="62" ry="17" fill="#f5d76e"/>
      <g fill="#ffb3c1"><circle class="cell" cx="20" cy="55" r="6"/>
      <circle class="cell" style="animation-delay:-.8s" cx="20" cy="55" r="6"/>
      <circle class="cell" style="animation-delay:-1.6s" cx="20" cy="55" r="6"/></g></svg></div>`;
  }
  if (r.viz === 'india') {
    return `<div class="viz">
      <div class="lbl">${r.bar_a}</div><div class="track"><div class="fill" style="--w:84%;background:#ff6b81"></div></div>
      <div class="lbl">${r.bar_b}</div><div class="track"><div class="fill" style="--w:100%;background:#4cc9f0"></div></div>
      <div class="donut"><svg width="92" height="92" viewBox="0 0 100 100">
        <circle class="bg" cx="50" cy="50" r="40" fill="none" stroke-width="14"/>
        <circle class="fg" cx="50" cy="50" r="40" fill="none" stroke-width="14" stroke-linecap="round"
          transform="rotate(-90 50 50)"/></svg>
        <div style="font-size:15px;line-height:1.35">${r.donut}</div></div></div>`;
  }
  return '';
}

function show(n) {
  i = (n + R.length) % R.length; t = 0;
  const r = R[i];
  reel.style.background = `linear-gradient(160deg, ${r.c1}, ${r.c2})`;
  const chars = r.bullets.join('').length;
  DUR = Math.max(8000, 4000 + chars * 45);
  slide.className = chars > 330 ? 'small' : '';
  const lis = r.bullets.map((b, k) => `<li style="animation-delay:${0.5 + k * 0.7}s">${b}</li>`).join('');
  slide.innerHTML = `<span class="emoji">${r.emoji}</span><h2>${r.title}</h2>${vizHTML(r)}<ul>${lis}</ul>` +
    (r.note ? `<div class="note">${r.note}</div>` : '');
  slide.scrollTop = 0;
  count.textContent = (i + 1) + ' / ' + R.length;
  [...bars.children].forEach((b, k) => { b.firstChild.style.width = k < i ? '100%' : '0'; });
}
function next() { show(i + 1); }
function prev() { show(i - 1); }
setInterval(() => {
  if (paused) return;
  t += TICK;
  bars.children[i].firstChild.style.width = Math.min(100, t / DUR * 100) + '%';
  if (t >= DUR) next();
}, TICK);
document.getElementById('zr').onclick = next; document.getElementById('zl').onclick = prev;
document.getElementById('next').onclick = next; document.getElementById('prev').onclick = prev;
document.getElementById('pp').onclick = e => { paused = !paused; e.target.textContent = paused ? '▶' : '⏸'; };
show(0);
</script>
"""


def build_html(reels, height=560):
    return TEMPLATE.replace("__DATA__", json.dumps(reels, ensure_ascii=False)).replace("__H__", str(height - 20))
