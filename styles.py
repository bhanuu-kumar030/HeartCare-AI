CSS = """
<style>
html, body, .stApp {font-size: 18px;}
.stApp {background: linear-gradient(180deg,#eaf6f8 0%,#f7fbfc 40%,#ffffff 100%);}
.block-container {padding-top: 1.2rem; max-width: 1400px;}
label p, [data-testid="stWidgetLabel"] p {font-size: 1.08rem !important; font-weight: 600; color:#0c3b47;}
.stButton>button, .stFormSubmitButton>button {font-size: 1.2rem; padding: .7rem 1.4rem; border-radius: 12px; font-weight: 700;}
[data-testid="stTabs"] button p {font-size: 1.15rem; font-weight: 700;}
h2, h3 {color:#0b4f60;}
.hc-hero {background: linear-gradient(100deg,#08707a 0%,#0a8f8f 55%,#37b5b0 100%); border-radius: 20px;
  padding: 18px 26px 6px 26px; color:#fff; box-shadow: 0 8px 24px rgba(8,112,122,.25); margin-bottom: 14px;}
.hc-top {display:flex; align-items:center; gap:20px; flex-wrap:wrap;}
.hc-cross {width:64px; height:64px; background:#fff; border-radius:16px; position:relative; flex:none;}
.hc-cross:before, .hc-cross:after {content:""; position:absolute; background:#e63946; border-radius:4px;}
.hc-cross:before {left:26px; top:12px; width:12px; height:40px;}
.hc-cross:after {left:12px; top:26px; width:40px; height:12px;}
.hc-hero h1 {margin:0; font-size: 2.5rem; color:#fff; line-height:1.1;}
.hc-hero p {margin:4px 0 0 0; font-size:1.25rem; opacity:.95;}
.hc-heart {margin-left:auto; width:120px; height:110px; animation: hbeat 1.1s infinite; transform-origin:center;
  filter: drop-shadow(0 4px 10px rgba(0,0,0,.35));}
@keyframes hbeat {0%,100%{transform:scale(1)} 14%{transform:scale(1.16)} 28%{transform:scale(1)}
  42%{transform:scale(1.1)} 56%{transform:scale(1)}}
.hc-ecg {width:100%; height:78px; margin-top:4px; display:block;}
.hc-ecg .trace {fill:none; stroke:#ffffff; stroke-width:3; stroke-linejoin:round; stroke-linecap:round;
  filter: drop-shadow(0 0 5px rgba(255,255,255,.9));}
.hc-ecg .scroll {animation: ecgscroll 1.6s linear infinite;}
@keyframes ecgscroll {from{transform:translateX(0)} to{transform:translateX(-200px)}}
.hc-badge {display:inline-block; background:rgba(255,255,255,.2); border-radius:999px; padding:3px 14px; font-size:.95rem; margin:2px 6px 8px 0;}
.hc-card {background:#fff; border:1px solid #cfe5ea; border-radius:16px; padding:16px 20px; box-shadow:0 3px 12px rgba(10,80,100,.08); margin-bottom:12px;}
.hc-step {font-size:1.35rem; font-weight:800; color:#0b4f60; margin:8px 0 6px 0;}
.f-card {display:flex; gap:14px; background:#fff; border-radius:14px; padding:12px 16px; margin-bottom:10px;
  border:1px solid #d7e7ec; border-left:8px solid #999; box-shadow:0 2px 8px rgba(0,0,0,.05);}
.f-card.good {border-left-color:#2e9e5b} .f-card.warn {border-left-color:#e0a100} .f-card.bad {border-left-color:#d62839}
.f-icon {font-size:2rem;} .f-title {font-weight:800; font-size:1.15rem;} .f-val {font-weight:700;}
.f-text {font-size:1.02rem; color:#27505c;}
.side-box {background:#fff; border:2px solid #d62839; border-radius:18px; padding:14px 16px;
  box-shadow:0 6px 20px rgba(214,40,57,.15);}
.side-box h3 {margin:0 0 6px 0; color:#d62839; font-size:1.45rem;}
.side-box .call {display:block; text-align:center; text-decoration:none; font-size:1.5rem; font-weight:800;
  padding:10px; border-radius:12px; margin:6px 0; color:#fff !important;}
.call.c112 {background:#d62839} .call.c108 {background:#0a8f8f}
.side-box .sub {font-weight:800; font-size:1.2rem; margin:12px 0 4px 0;}
.side-box .do {color:#1c7a45} .side-box .dont {color:#b3202f}
.side-box ul {padding-left:20px; margin:0;} .side-box li {font-size:1.05rem; line-height:1.4; margin-bottom:7px;}
div[data-testid="stColumn"]:has(.side-marker), div[data-testid="column"]:has(.side-marker) {
  position: sticky; top: 3.2rem; align-self: flex-start; max-height: calc(100vh - 4rem); overflow-y: auto;}
.hc-foot {font-size:.9rem; color:#4a6b75; margin-top:10px;}
</style>
"""

def _ecg_path(n=6):
    """One heartbeat (P wave, QRS spike, T wave) repeated n times, 200 units wide each."""
    parts = ["M0 40"]
    for k in range(n):
        o = 200 * k
        parts.append(
            f"L{o+30} 40 Q{o+40} 40 {o+45} 33 Q{o+50} 26 {o+55} 40 L{o+70} 40 "
            f"L{o+75} 45 L{o+82} 6 L{o+90} 62 L{o+96} 40 L{o+116} 40 "
            f"Q{o+131} 40 {o+139} 27 Q{o+147} 14 {o+155} 40 L{o+200} 40")
    return " ".join(parts)


def hero_html(title, subtitle, badges):
    path = _ecg_path(6)
    badge_html = "".join(f'<span class="hc-badge">{b}</span>' for b in badges)
    return f"""
<div class="hc-hero">
  <div class="hc-top">
    <div class="hc-cross"></div>
    <div><h1>{title}</h1><p>{subtitle}</p>{badge_html}</div>
    <svg class="hc-heart" viewBox="0 0 100 92">
      <defs><linearGradient id="hg" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#ff8a9b"/><stop offset="1" stop-color="#e0293f"/></linearGradient></defs>
      <path d="M50 88 C18 62 3 44 3 26 C3 11 14 3 27 3 C37 3 45 9 50 18 C55 9 63 3 73 3 C86 3 97 11 97 26 C97 44 82 62 50 88 Z"
        fill="url(#hg)" stroke="#fff" stroke-width="3"/>
      <path d="M18 30 C20 18 30 14 38 16" stroke="#fff" stroke-width="4" fill="none" opacity=".6" stroke-linecap="round"/>
    </svg>
  </div>
  <svg class="hc-ecg" viewBox="0 0 800 78" preserveAspectRatio="none">
    <g class="scroll"><path class="trace" d="{path}"/></g>
  </svg>
</div>
"""
