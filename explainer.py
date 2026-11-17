import json

STR = {
"en": {
  "risk": {"Low": "LOW RISK", "Moderate": "MODERATE RISK", "High": "HIGH RISK"},
  "chance": "Estimated chance", "model": "Estimate from a computer model, not a diagnosis.",
  "head": "What may be happening inside your heart",
  "live": "Illustration (not your real scan). Tap a step to see it.",
  "beat": {"Low": "Heart beats calmly.", "Moderate": "Heart works harder and beats faster.", "High": "Heart struggles and beats much faster."},
  "label_art": {"Low": "Healthy artery", "Moderate": "Narrowing artery", "High": "Badly narrowed artery"},
  "label_mus": "Heart muscle short of blood",
  "steps": {
    "Low": [["1. Artery stays clear", "Blood flows freely through the heart arteries."],
            ["2. Heart gets enough blood", "The heart muscle gets all the oxygen it needs."],
            ["3. Heart beats calmly", "It does not need to work extra hard."],
            ["4. Usually no symptoms", "Keep walking daily, eat less salt, avoid tobacco."]],
    "Moderate": [["1. Fat collects in the artery", "Cholesterol and fat slowly stick to the wall and form a patch (plaque)."],
                 ["2. The artery gets narrower", "Less blood passes, mainly when you climb stairs or walk fast."],
                 ["3. The heart works harder", "It pumps faster to make up for the missing blood."],
                 ["4. You may feel", "Tiredness, breathlessness on effort, mild chest heaviness."]],
    "High": [["1. A big patch of fat blocks the artery", "The plaque has grown and the artery is badly narrowed."],
             ["2. Heart muscle is starved of blood", "The area beyond the block gets very little oxygen."],
             ["3. The heart struggles and beats faster", "It races to push blood through, which is tiring and risky."],
             ["4. You may feel", "Chest pressure, sweating, breathlessness, pain in left arm or jaw. If a clot forms, it becomes a heart attack."]]},
  "symptoms": {"Low": ["Usually none", "Keep a yearly check-up"],
               "Moderate": ["Tiredness", "Breathless on stairs", "Mild chest heaviness", "Palpitations"],
               "High": ["Chest pressure", "Breathlessness", "Cold sweat", "Pain in left arm / jaw", "Dizziness", "Ankle swelling"]},
  "symhead": "Problems you may notice (possible, not certain)",
  "next": {"Low": ["Walk 30 minutes, 5 days a week", "Less salt, sugar and fried food", "Check BP, sugar and cholesterol every year"],
           "Moderate": ["Meet a doctor in the next few days", "Ask for ECG, lipid profile, sugar and TMT", "Stop tobacco, cut salt and fried food, walk daily"],
           "High": ["Meet a heart doctor (cardiologist) soon, do not delay", "Ask for ECG, echo, TMT or angiography as advised", "If chest pain starts, call 112 or 108 at once"]},
  "nexthead": "What to do next", "stepshead": "Step by step",
},
"hi": {
  "risk": {"Low": "कम ख़तरा", "Moderate": "मध्यम ख़तरा", "High": "ज़्यादा ख़तरा"},
  "chance": "अनुमानित संभावना", "model": "यह कंप्यूटर मॉडल का अनुमान है, बीमारी की पहचान नहीं।",
  "head": "आपके दिल के अंदर क्या हो रहा हो सकता है",
  "live": "यह चित्र समझाने के लिए है (आपका असली स्कैन नहीं)। किसी स्टेप पर टैप करें।",
  "beat": {"Low": "दिल शांत ढंग से धड़कता है।", "Moderate": "दिल ज़्यादा मेहनत करता है और तेज़ धड़कता है।", "High": "दिल संघर्ष करता है और बहुत तेज़ धड़कता है।"},
  "label_art": {"Low": "स्वस्थ नस", "Moderate": "तंग होती नस", "High": "बुरी तरह तंग नस"},
  "label_mus": "दिल की मांसपेशी को खून कम",
  "steps": {
    "Low": [["1. नस साफ़ रहती है", "दिल की नसों में खून आराम से बहता है।"],
            ["2. दिल को पूरा खून मिलता है", "दिल की मांसपेशी को पूरी ऑक्सीजन मिलती है।"],
            ["3. दिल शांत धड़कता है", "उसे ज़्यादा मेहनत नहीं करनी पड़ती।"],
            ["4. आम तौर पर कोई तकलीफ़ नहीं", "रोज़ टहलें, नमक कम खाएँ, तंबाकू से दूर रहें।"]],
    "Moderate": [["1. नस में चर्बी जमती है", "कोलेस्ट्रॉल और चर्बी दीवार पर धीरे-धीरे जमकर परत (प्लाक) बनाती है।"],
                 ["2. नस तंग हो जाती है", "कम खून निकलता है, ख़ासकर सीढ़ी चढ़ते या तेज़ चलते समय।"],
                 ["3. दिल ज़्यादा मेहनत करता है", "खून की कमी पूरी करने के लिए वह तेज़ पंप करता है।"],
                 ["4. आपको महसूस हो सकता है", "थकान, मेहनत पर साँस फूलना, सीने में हल्का भारीपन।"]],
    "High": [["1. चर्बी की बड़ी परत नस रोक देती है", "प्लाक बढ़ गया है और नस बुरी तरह तंग है।"],
             ["2. दिल की मांसपेशी को खून नहीं मिलता", "रुकावट के आगे के हिस्से को बहुत कम ऑक्सीजन मिलती है।"],
             ["3. दिल संघर्ष करता है और तेज़ धड़कता है", "खून धकेलने के लिए वह दौड़ता है, जो थकाने वाला और जोखिम भरा है।"],
             ["4. आपको महसूस हो सकता है", "सीने पर दबाव, पसीना, साँस फूलना, बाएँ हाथ या जबड़े में दर्द। थक्का बन जाए तो हार्ट अटैक होता है।"]]},
  "symptoms": {"Low": ["आम तौर पर कुछ नहीं", "हर साल जाँच कराएँ"],
               "Moderate": ["थकान", "सीढ़ी पर साँस फूलना", "सीने में हल्का भारीपन", "धड़कन तेज़ लगना"],
               "High": ["सीने पर दबाव", "साँस फूलना", "ठंडा पसीना", "बाएँ हाथ / जबड़े में दर्द", "चक्कर", "टखनों में सूजन"]},
  "symhead": "जो तकलीफ़ें महसूस हो सकती हैं (संभव हैं, पक्की नहीं)",
  "next": {"Low": ["हफ़्ते में 5 दिन 30 मिनट चलें", "नमक, चीनी और तला खाना कम करें", "हर साल BP, शुगर और कोलेस्ट्रॉल जँचवाएँ"],
           "Moderate": ["अगले कुछ दिनों में डॉक्टर से मिलें", "ECG, लिपिड प्रोफ़ाइल, शुगर और TMT के लिए पूछें", "तंबाकू छोड़ें, नमक और तला खाना कम करें, रोज़ चलें"],
           "High": ["जल्दी हृदय रोग विशेषज्ञ (कार्डियोलॉजिस्ट) से मिलें, देर न करें", "सलाह पर ECG, इको, TMT या एंजियोग्राफी करवाएँ", "सीने में दर्द शुरू हो तो तुरंत 112 या 108 पर कॉल करें"]},
  "nexthead": "आगे क्या करें", "stepshead": "एक-एक करके",
},
}

TEMPLATE = r"""
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:'Segoe UI',system-ui,sans-serif}
body{background:transparent;color:#10303a;font-size:18px}
.wrap{display:flex;flex-direction:column;gap:14px}
.meter{background:#fff;border:1px solid #cfe5ea;border-radius:18px;padding:16px 20px;box-shadow:0 3px 12px rgba(10,80,100,.1)}
.rt{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.pill{font-size:1.9rem;font-weight:900;padding:8px 22px;border-radius:999px;color:#fff}
.pct{font-size:2.6rem;font-weight:900}.pctl{font-size:1rem;color:#3d6470}
.bar{position:relative;height:26px;border-radius:14px;margin:14px 0 4px;
 background:linear-gradient(90deg,#2e9e5b 0%,#2e9e5b 30%,#f1c40f 45%,#f1c40f 62%,#d62839 78%,#d62839 100%)}
.pin{position:absolute;top:-8px;width:6px;height:42px;background:#10303a;border-radius:4px;transition:left 1.4s}
.pin:after{content:"";position:absolute;top:-8px;left:-6px;border:9px solid transparent;border-top-color:#10303a}
.ticks{display:flex;justify-content:space-between;font-size:.85rem;color:#3d6470}
.small{font-size:.9rem;color:#4a6b75;margin-top:6px}
.main{display:grid;grid-template-columns:minmax(260px,1fr) minmax(260px,1fr);gap:14px}
@media(max-width:760px){.main{grid-template-columns:1fr}}
.card{background:#fff;border:1px solid #cfe5ea;border-radius:18px;padding:14px 16px;box-shadow:0 3px 12px rgba(10,80,100,.08)}
h3{font-size:1.25rem;color:#0b4f60;margin-bottom:6px}
svg{width:100%;height:auto;display:block}
.beat{transform-box:view-box;transform-origin:200px 190px;animation:beat var(--dur,1s) ease-in-out infinite}
@keyframes beat{0%,100%{transform:scale(1)}12%{transform:scale(1.045)}24%{transform:scale(1)}36%{transform:scale(1.03)}48%{transform:scale(1)}}
.plaque{transform-box:fill-box;transform-origin:center;transform:scale(var(--pl,0));transition:transform 1.4s}
.starve{opacity:0;transition:opacity 1s;animation:starve 1.6s ease-in-out infinite}
@keyframes starve{0%,100%{fill-opacity:.25}50%{fill-opacity:.55}}
svg[data-step="1"] .plaque{filter:drop-shadow(0 0 7px #ffd23f)}
svg[data-step="2"] .starve{opacity:1}
svg[data-step="3"] .beat{animation-duration:var(--fast,.7s)}
svg[data-step="4"] .sym{opacity:1}
.sym{opacity:0;transition:opacity .8s}
.lbl{font-size:13px;font-weight:700;fill:#10303a}
.steps{display:flex;flex-direction:column;gap:8px}
.step{border-left:7px solid #cfe5ea;background:#f6fbfc;border-radius:10px;padding:8px 12px;cursor:pointer;opacity:.55;transition:all .4s}
.step b{display:block;font-size:1.08rem}.step span{font-size:.98rem;color:#27505c}
.step.on{opacity:1;background:#fff;border-left-color:var(--c);box-shadow:0 3px 10px rgba(0,0,0,.1)}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{background:#fdecee;color:#9b1c2b;border:1px solid #f4b8c0;border-radius:999px;padding:5px 14px;font-weight:700;font-size:.98rem}
ul{padding-left:22px}li{margin:5px 0;font-size:1.05rem}
.beatcap{font-weight:700;margin-top:6px}
</style>
<div class="wrap" id="root">
 <div class="meter">
  <div class="rt"><div class="pill" id="pill"></div><div><div class="pct" id="pct"></div><div class="pctl" id="pctl"></div></div></div>
  <div class="bar"><div class="pin" id="pin" style="left:0"></div></div>
  <div class="ticks"><span>0%</span><span>35%</span><span>65%</span><span>100%</span></div>
  <div class="small" id="model"></div>
 </div>
 <div class="main">
  <div class="card">
   <h3 id="head"></h3>
   <svg id="svg" viewBox="0 0 400 350" data-step="1">
    <defs>
     <linearGradient id="hg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff9aa8"/><stop offset="1" stop-color="#d62839"/></linearGradient>
    </defs>
    <g class="beat" id="beatg">
     <path d="M200 330 C90 250 40 170 40 110 C40 60 85 30 125 30 C160 30 185 50 200 80 C215 50 240 30 275 30 C315 30 360 60 360 110 C360 170 310 250 200 330 Z" fill="url(#hg)" stroke="#9b1c2b" stroke-width="4"/>
     <ellipse class="starve" cx="198" cy="238" rx="58" ry="52" fill="#3a0010" fill-opacity=".4"/>
     <path d="M200 70 C190 130 180 200 200 290" stroke="#8c1c2b" stroke-width="10" fill="none" stroke-linecap="round"/>
     <path d="M198 80 C140 80 90 110 75 170" stroke="#8c1c2b" stroke-width="8" fill="none" stroke-linecap="round"/>
     <path d="M205 80 C270 75 320 100 335 160" stroke="#8c1c2b" stroke-width="8" fill="none" stroke-linecap="round"/>
     <g id="cells" fill="#ffd6dd"></g>
     <ellipse class="plaque" id="plq1" cx="189" cy="158" rx="17" ry="30" fill="#f6c945" stroke="#b8860b" stroke-width="2"/>
    </g>
    <line id="ln1" x1="214" y1="150" x2="262" y2="205" stroke="#10303a" stroke-width="2"/>
    <text class="lbl" id="t1" x="228" y="222"></text>
    <line id="ln2" x1="170" y1="245" x2="120" y2="300" stroke="#10303a" stroke-width="2"/>
    <text class="lbl" id="t2" x="20" y="318"></text>
    <g class="sym" fill="#d62839" font-size="26"><text x="318" y="62">💦</text><text x="22" y="62">😮‍💨</text><text x="330" y="220">⚡</text></g>
   </svg>
   <div class="beatcap" id="beatcap"></div>
   <div class="small" id="live"></div>
  </div>
  <div class="card">
   <h3 id="stepshead"></h3><div class="steps" id="steps"></div>
  </div>
 </div>
 <div class="main">
  <div class="card"><h3 id="symhead"></h3><div class="chips" id="chips"></div></div>
  <div class="card"><h3 id="nexthead"></h3><ul id="next"></ul></div>
 </div>
</div>
<script>
const D = __DATA__;
const C = {Low:'#2e9e5b', Moderate:'#d99a00', High:'#d62839'};
const col = C[D.level], $ = id => document.getElementById(id);
$('pill').textContent = D.s.risk[D.level]; $('pill').style.background = col;
$('pct').textContent = D.pct.toFixed(1) + '%'; $('pctl').textContent = D.s.chance;
$('model').textContent = D.s.model;
setTimeout(() => { $('pin').style.left = 'calc(' + Math.min(99, D.pct) + '% - 3px)'; }, 200);
$('head').textContent = D.s.head; $('stepshead').textContent = D.s.stepshead;
$('live').textContent = D.s.live; $('beatcap').textContent = D.s.beat[D.level];
$('beatcap').style.color = col;
$('symhead').textContent = D.s.symhead; $('nexthead').textContent = D.s.nexthead;
const svg = $('svg');
const dur = {Low:1.25, Moderate:0.95, High:0.72}[D.level];
const fast = {Low:1.0, Moderate:0.75, High:0.5}[D.level];
svg.style.setProperty('--dur', dur + 's'); svg.style.setProperty('--fast', fast + 's');
svg.style.setProperty('--pl', {Low:0, Moderate:0.55, High:1.05}[D.level]);
if (D.level === 'Low') { $('ln1').style.display = 'none'; $('ln2').style.display = 'none'; $('t2').style.display='none'; $('t1').textContent = D.s.label_art.Low; $('t1').setAttribute('x','225'); $('t1').setAttribute('y','150'); }
else { $('t1').textContent = D.s.label_art[D.level]; $('t2').textContent = D.s.label_mus; }
const ns = 'http://www.w3.org/2000/svg';
const slow = {Low:2.4, Moderate:3.6, High:5.4}[D.level];
for (let k = 0; k < 4; k++) {
  const c = document.createElementNS(ns, 'circle'); c.setAttribute('r', 4.5);
  const a = document.createElementNS(ns, 'animateMotion');
  a.setAttribute('dur', slow + 's'); a.setAttribute('repeatCount', 'indefinite');
  a.setAttribute('begin', (-k * slow / 4) + 's');
  a.setAttribute('path', 'M200 70 C190 130 180 200 200 290');
  c.appendChild(a); $('cells').appendChild(c);
}
const S = D.s.steps[D.level]; let cur = 0;
S.forEach((s, k) => { const d = document.createElement('div'); d.className = 'step';
  d.style.setProperty('--c', col); d.innerHTML = '<b></b><span></span>';
  d.querySelector('b').textContent = s[0]; d.querySelector('span').textContent = s[1];
  d.onclick = () => { cur = k; setStep(); }; $('steps').appendChild(d); });
function setStep() {
  svg.setAttribute('data-step', cur + 1);
  [...$('steps').children].forEach((e, k) => e.classList.toggle('on', k === cur));
}
setStep(); setInterval(() => { cur = (cur + 1) % S.length; setStep(); }, 6000);
D.s.symptoms[D.level].forEach(t => { const e = document.createElement('span'); e.className = 'chip'; e.textContent = t; $('chips').appendChild(e); });
D.s.next[D.level].forEach(t => { const e = document.createElement('li'); e.textContent = t; $('next').appendChild(e); });
</script>
"""


def build_explainer(level, pct, lang):
    data = {"level": level, "pct": pct, "s": STR[lang]}
    return TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False))
