import json

# ---------- conversation tree (English + Hindi). "o" = options [label, next]. ----------
TREE = {
"en": {
 "ui": {"title": "HeartCare Assistant", "sub": "Demo helper. Not a doctor.", "ph": "Type your problem here...", "send": "Send",
        "menu": "Main menu", "again": "Start over", "amb": "🚑 Request ambulance (demo)", "c112": "📞 Call 112", "c108": "📞 Call 108",
        "you_ok": "I did not fully understand. Please choose one option below or type: chest pain, breathless, dizzy, ambulance.",
        "demo": ["📡 Sending your request... (DEMO)", "✅ Request received at control room (demo)",
                 "🚑 Ambulance assigned. ETA 8 minutes (demo)",
                 "⚠️ This is only a DEMO. No real ambulance has been called. In a real emergency, dial 112 or 108 yourself."]},
 "n": {
  "start": {"q": "Namaste 🙏 I am the HeartCare assistant. What problem are you facing?",
            "o": [["Chest pain or heaviness", "cp1"], ["Breathlessness", "br1"], ["Dizziness or fainting", "dz1"],
                  ["Fast or irregular heartbeat", "hr1"], ["Someone has collapsed", "col1"], ["I need an ambulance", "amb"], ["I have a question", "faq"]]},
  "cp1": {"q": "How long has the chest pain lasted?", "o": [["More than 5 minutes", "cp2L"], ["Less than 5 minutes", "cp2S"], ["It comes and goes", "cp2S"]]},
  "cp2L": {"q": "Do you also have sweating, breathlessness, nausea, or pain in the arm, jaw or back?", "o": [["Yes", "E_EMG"], ["No", "E_URG"]]},
  "cp2S": {"q": "Do you also have sweating, breathlessness, nausea, or pain in the arm, jaw or back?", "o": [["Yes", "E_URG"], ["No", "E_SOON"]]},
  "br1": {"q": "How is the breathlessness?", "o": [["Sudden, or even at rest", "E_EMG"], ["With chest pain", "E_EMG"], ["Only on stairs or fast walking", "E_SOON"]]},
  "dz1": {"q": "Did you faint or lose consciousness?", "o": [["Yes", "E_URG"], ["No, only dizzy", "dz2"]]},
  "dz2": {"q": "Any chest pain or breathlessness with it?", "o": [["Yes", "E_EMG"], ["No", "E_SOON"]]},
  "hr1": {"q": "Do you also have chest pain, dizziness or breathlessness?", "o": [["Yes", "E_EMG"], ["No", "E_CALM"]]},
  "col1": {"q": "Is the person breathing normally?", "o": [["No, not breathing normally", "E_CPR"], ["Yes, breathing", "E_SIDE"]]},
  "amb": {"end": "emg", "msg": "🚨 Let us get help now. Please call 112 or 108. You can also try the demo request below."},
  "faq": {"q": "What would you like to know?", "o": [["Warning signs", "i_signs"], ["Healthy food", "i_diet"], ["Exercise", "i_ex"], ["Aspirin", "i_asp"], ["Back", "start"]]},
  "i_signs": {"info": "Warning signs: chest pressure or heaviness, pain spreading to left arm, jaw or back, cold sweat, breathlessness, nausea. Women, elders and diabetics may feel only tiredness or a 'gas' feeling."},
  "i_diet": {"info": "Salt under 1 teaspoon a day. Less fried food, vanaspati and sweets. More dal, sabzi, fruits, oats and nuts."},
  "i_ex": {"info": "Walk fast for 30 minutes, 5 days a week. Yoga and pranayama help with stress. Stop if you get chest pain."},
  "i_asp": {"info": "In a suspected heart attack, after calling 112/108, chew one 300 mg aspirin only if you are not allergic and no doctor has told you to avoid it. If unsure, skip it."},
  "E_EMG": {"end": "emg", "msg": "🚨 This may be an EMERGENCY. Call 112 or 108 NOW. Sit down, loosen tight clothes, do not drive yourself, and do not walk around. Chew one 300 mg aspirin only if you are not allergic. Ask someone to stay with you."},
  "E_URG": {"end": "urg", "msg": "⚠️ Please get medical help right away, within the hour. Go to the nearest hospital with someone. Do not drive yourself. If the pain grows or you feel faint, call 108 at once."},
  "E_SOON": {"end": "soon", "msg": "This does not sound like an emergency right now. Please see a doctor in 1 to 2 days for BP, ECG, sugar and cholesterol. If it gets worse, call 112."},
  "E_CALM": {"end": "soon", "msg": "Sit down, breathe slowly, avoid tea and coffee. Please see a doctor for an ECG soon. If chest pain, dizziness or breathlessness starts, call 112."},
  "E_CPR": {"end": "emg", "msg": "🚨 Call 112 NOW. Start hands-only CPR: push hard and fast in the centre of the chest, 100 to 120 times a minute, until help arrives. Use an AED if one is nearby."},
  "E_SIDE": {"end": "urg", "msg": "Lay the person on their side, keep them warm, give no food or water, and call 108. Stay with them and watch their breathing."},
 }},
"hi": {
 "ui": {"title": "हार्टकेयर सहायक", "sub": "डेमो सहायक। डॉक्टर नहीं।", "ph": "अपनी तकलीफ़ यहाँ लिखें...", "send": "भेजें",
        "menu": "मुख्य मेनू", "again": "फिर से शुरू करें", "amb": "🚑 एम्बुलेंस बुलाएँ (डेमो)", "c112": "📞 112 पर कॉल", "c108": "📞 108 पर कॉल",
        "you_ok": "मैं पूरी तरह समझ नहीं पाया। नीचे से एक विकल्प चुनें या लिखें: सीने में दर्द, साँस फूलना, चक्कर, एम्बुलेंस।",
        "demo": ["📡 आपकी रिक्वेस्ट भेजी जा रही है... (डेमो)", "✅ कंट्रोल रूम में रिक्वेस्ट मिल गई (डेमो)",
                 "🚑 एम्बुलेंस तय हो गई। पहुँचने का समय 8 मिनट (डेमो)",
                 "⚠️ यह सिर्फ़ डेमो है। कोई असली एम्बुलेंस नहीं बुलाई गई। असली इमरजेंसी में खुद 112 या 108 डायल करें।"]},
 "n": {
  "start": {"q": "नमस्ते 🙏 मैं हार्टकेयर सहायक हूँ। आपको क्या तकलीफ़ है?",
            "o": [["सीने में दर्द या भारीपन", "cp1"], ["साँस फूलना", "br1"], ["चक्कर या बेहोशी", "dz1"],
                  ["तेज़ या अनियमित धड़कन", "hr1"], ["कोई बेहोश होकर गिर गया", "col1"], ["मुझे एम्बुलेंस चाहिए", "amb"], ["मेरा एक सवाल है", "faq"]]},
  "cp1": {"q": "सीने का दर्द कितनी देर से है?", "o": [["5 मिनट से ज़्यादा", "cp2L"], ["5 मिनट से कम", "cp2S"], ["आता-जाता रहता है", "cp2S"]]},
  "cp2L": {"q": "क्या साथ में पसीना, साँस फूलना, मिचली, या हाथ, जबड़े या पीठ में दर्द भी है?", "o": [["हाँ", "E_EMG"], ["नहीं", "E_URG"]]},
  "cp2S": {"q": "क्या साथ में पसीना, साँस फूलना, मिचली, या हाथ, जबड़े या पीठ में दर्द भी है?", "o": [["हाँ", "E_URG"], ["नहीं", "E_SOON"]]},
  "br1": {"q": "साँस फूलना कैसा है?", "o": [["अचानक, या आराम में भी", "E_EMG"], ["सीने के दर्द के साथ", "E_EMG"], ["सिर्फ़ सीढ़ी या तेज़ चलने पर", "E_SOON"]]},
  "dz1": {"q": "क्या आप बेहोश हुए या होश खोया?", "o": [["हाँ", "E_URG"], ["नहीं, सिर्फ़ चक्कर", "dz2"]]},
  "dz2": {"q": "साथ में सीने का दर्द या साँस फूलना है?", "o": [["हाँ", "E_EMG"], ["नहीं", "E_SOON"]]},
  "hr1": {"q": "क्या साथ में सीने का दर्द, चक्कर या साँस फूलना भी है?", "o": [["हाँ", "E_EMG"], ["नहीं", "E_CALM"]]},
  "col1": {"q": "क्या व्यक्ति सामान्य साँस ले रहा है?", "o": [["नहीं, सामान्य साँस नहीं", "E_CPR"], ["हाँ, साँस चल रही है", "E_SIDE"]]},
  "amb": {"end": "emg", "msg": "🚨 अभी मदद लेते हैं। कृपया 112 या 108 पर कॉल करें। नीचे डेमो रिक्वेस्ट भी आज़मा सकते हैं।"},
  "faq": {"q": "आप क्या जानना चाहते हैं?", "o": [["चेतावनी के लक्षण", "i_signs"], ["सेहतमंद खाना", "i_diet"], ["कसरत", "i_ex"], ["एस्पिरिन", "i_asp"], ["वापस", "start"]]},
  "i_signs": {"info": "चेतावनी के लक्षण: सीने पर दबाव या भारीपन, दर्द का बाएँ हाथ, जबड़े या पीठ तक फैलना, ठंडा पसीना, साँस फूलना, मिचली। महिलाओं, बुज़ुर्गों और डायबिटीज़ वालों को सिर्फ़ थकान या 'गैस' जैसा लग सकता है।"},
  "i_diet": {"info": "नमक दिन में 1 छोटे चम्मच से कम। तला खाना, वनस्पति और मिठाई कम। दाल, सब्ज़ी, फल, ओट्स और मेवे ज़्यादा।"},
  "i_ex": {"info": "हफ़्ते में 5 दिन 30 मिनट तेज़ चलें। तनाव के लिए योग और प्राणायाम मदद करते हैं। सीने में दर्द हो तो रुक जाएँ।"},
  "i_asp": {"info": "हार्ट अटैक का शक हो तो 112/108 पर कॉल करने के बाद, अगर एलर्जी नहीं है और डॉक्टर ने मना नहीं किया है, तो 300 mg की एक एस्पिरिन चबाएँ। पक्का न हो तो छोड़ दें।"},
  "E_EMG": {"end": "emg", "msg": "🚨 यह इमरजेंसी हो सकती है। अभी 112 या 108 पर कॉल करें। बैठ जाएँ, तंग कपड़े ढीले करें, खुद गाड़ी न चलाएँ और चलें-फिरें नहीं। एलर्जी न हो तो 300 mg की एक एस्पिरिन चबाएँ। किसी को अपने पास रहने को कहें।"},
  "E_URG": {"end": "urg", "msg": "⚠️ कृपया तुरंत, एक घंटे के भीतर, चिकित्सा मदद लें। किसी के साथ सबसे नज़दीकी अस्पताल जाएँ। खुद गाड़ी न चलाएँ। दर्द बढ़े या चक्कर आए तो तुरंत 108 पर कॉल करें।"},
  "E_SOON": {"end": "soon", "msg": "अभी यह इमरजेंसी नहीं लगती। कृपया 1 से 2 दिन में डॉक्टर से BP, ECG, शुगर और कोलेस्ट्रॉल की जाँच करवाएँ। हालत बिगड़े तो 112 पर कॉल करें।"},
  "E_CALM": {"end": "soon", "msg": "बैठ जाएँ, धीरे-धीरे साँस लें, चाय-कॉफ़ी से बचें। जल्दी ECG के लिए डॉक्टर से मिलें। सीने में दर्द, चक्कर या साँस फूलना शुरू हो तो 112 पर कॉल करें।"},
  "E_CPR": {"end": "emg", "msg": "🚨 अभी 112 पर कॉल करें। हैंड्स-ओनली CPR शुरू करें: छाती के बीच में ज़ोर से और तेज़ी से दबाएँ, एक मिनट में 100 से 120 बार, जब तक मदद न आए। पास में AED हो तो इस्तेमाल करें।"},
  "E_SIDE": {"end": "urg", "msg": "व्यक्ति को करवट से लिटाएँ, गर्म रखें, खाना-पानी न दें और 108 पर कॉल करें। उसके पास रहें और साँस पर नज़र रखें।"},
 }},
}
KEYWORDS = [
 [r"ambulance|एम्बुलेंस|एंबुलेंस|108", "amb"],
 [r"collaps|unconscious|behosh|बेहोश|gir gaya|गिर गया|fainted", "col1"],
 [r"chest|seene|seena|सीने|सीना|छाती|chhati|dard|दर्द|pain|heavy|bhaar|भारी", "cp1"],
 [r"breath|saans|सांस|साँस|dam phool|दम", "br1"],
 [r"dizz|chakkar|चक्कर|faint", "dz1"],
 [r"palpit|dhadkan|धड़कन|racing|irregular", "hr1"],
 [r"aspirin|एस्पिरिन|disprin", "i_asp"],
 [r"diet|food|khana|खाना|namak|नमक|salt", "i_diet"],
 [r"exercise|walk|yoga|vyayam|व्यायाम|कसरत|sair|सैर", "i_ex"],
 [r"sign|symptom|lakshan|लक्षण", "i_signs"],
]


def validate():
    for lang, d in TREE.items():
        for nid, n in d["n"].items():
            for _, nxt in n.get("o", []):
                assert nxt in d["n"], (lang, nid, nxt)
    return True


WIDGET = r"""
<script>
(function(){
 const T = __TREE__, KW = __KW__;
 let P, D;
 try { P = window.parent; D = P.document; D.body; } catch(e) { return; }
 ['hc-root','hc-style'].forEach(id => { const o = D.getElementById(id); if (o) o.remove(); });
 const U = T.ui, N = T.n;
 const st = D.createElement('style'); st.id = 'hc-style';
 st.textContent = `
 #hc-root{position:fixed;right:22px;bottom:22px;z-index:2147483000;font-family:'Segoe UI',system-ui,sans-serif;touch-action:none}
 #hc-bubble{width:66px;height:66px;border-radius:50%;background:linear-gradient(135deg,#0a8f8f,#08707a);color:#fff;font-size:30px;
   display:flex;align-items:center;justify-content:center;cursor:grab;box-shadow:0 6px 20px rgba(0,0,0,.35);user-select:none;position:relative}
 #hc-bubble:after{content:"";position:absolute;inset:-6px;border-radius:50%;border:3px solid rgba(10,143,143,.5);animation:hcp 1.8s infinite}
 @keyframes hcp{0%{transform:scale(.9);opacity:1}100%{transform:scale(1.35);opacity:0}}
 #hc-panel{display:none;position:absolute;width:350px;max-width:92vw;height:480px;max-height:78vh;background:#fff;border-radius:18px;
   box-shadow:0 12px 40px rgba(0,0,0,.35);overflow:hidden;flex-direction:column;bottom:78px;right:0}
 #hc-root.open #hc-panel{display:flex} #hc-root.open #hc-bubble:after{display:none}
 #hc-head{background:linear-gradient(100deg,#08707a,#0a8f8f);color:#fff;padding:10px 14px;cursor:grab;display:flex;align-items:center;gap:10px;user-select:none}
 #hc-head b{font-size:17px;display:block} #hc-head small{opacity:.85;font-size:12px}
 #hc-x{margin-left:auto;background:rgba(255,255,255,.2);border:0;color:#fff;width:30px;height:30px;border-radius:50%;font-size:18px;cursor:pointer}
 #hc-msgs{flex:1;overflow-y:auto;padding:12px;background:#f3f9fb;display:flex;flex-direction:column;gap:8px}
 .hc-m{max-width:88%;padding:9px 13px;border-radius:14px;font-size:15.5px;line-height:1.4;white-space:pre-wrap}
 .hc-b{background:#fff;border:1px solid #cfe5ea;align-self:flex-start;color:#10303a}
 .hc-u{background:#0a8f8f;color:#fff;align-self:flex-end}
 #hc-opts{padding:8px 10px;display:flex;flex-wrap:wrap;gap:6px;background:#eaf4f7;max-height:150px;overflow-y:auto}
 .hc-c{border:1.5px solid #0a8f8f;background:#fff;color:#08707a;border-radius:999px;padding:7px 13px;font-size:14.5px;font-weight:700;cursor:pointer;text-decoration:none}
 .hc-c.red{background:#d62839;border-color:#d62839;color:#fff}
 .hc-c.teal{background:#0a8f8f;color:#fff}
 #hc-in{display:flex;gap:6px;padding:8px;border-top:1px solid #d7e7ec;background:#fff}
 #hc-in input{flex:1;border:1.5px solid #cfe5ea;border-radius:999px;padding:9px 14px;font-size:15px;outline:none}
 #hc-in button{border:0;background:#0a8f8f;color:#fff;border-radius:999px;padding:0 16px;font-weight:700;cursor:pointer}`;
 D.head.appendChild(st);
 const root = D.createElement('div'); root.id = 'hc-root';
 root.innerHTML = `<div id="hc-panel"><div id="hc-head"><span style="font-size:26px">🫀</span><div><b></b><small></small></div>
   <button id="hc-x">–</button></div><div id="hc-msgs"></div><div id="hc-opts"></div>
   <div id="hc-in"><input id="hc-t"/><button id="hc-s"></button></div></div><div id="hc-bubble">💬</div>`;
 D.body.appendChild(root);
 const $ = s => root.querySelector(s);
 $('#hc-head b').textContent = U.title; $('#hc-head small').textContent = U.sub;
 $('#hc-t').placeholder = U.ph; $('#hc-s').textContent = U.send;
 const msgs = $('#hc-msgs'), opts = $('#hc-opts');
 function say(text, who) { const m = D.createElement('div'); m.className = 'hc-m ' + (who === 'u' ? 'hc-u' : 'hc-b');
   m.textContent = text; msgs.appendChild(m); msgs.scrollTop = msgs.scrollHeight; }
 function chip(label, fn, cls, href) { const c = D.createElement(href ? 'a' : 'button'); c.className = 'hc-c ' + (cls || '');
   c.textContent = label; if (href) c.href = href; else c.onclick = fn; opts.appendChild(c); }
 function go(id) {
   const n = N[id]; opts.innerHTML = '';
   if (n.q) { say(n.q); n.o.forEach(o => chip(o[0], () => { say(o[0], 'u'); go(o[1]); })); }
   else if (n.info) { say(n.info); chip(U.menu, () => go('start')); }
   else {
     say(n.msg);
     if (n.end === 'emg' || n.end === 'urg') chip(U.amb, demo, 'red');
     if (n.end === 'emg') { chip(U.c112, null, 'red', 'tel:112'); }
     chip(U.c108, null, 'teal', 'tel:108'); chip(U.again, () => go('start'));
   }
 }
 function demo() { opts.innerHTML = ''; say(U.amb, 'u');
   U.demo.forEach((t, k) => setTimeout(() => { say(t); if (k === U.demo.length - 1) {
     chip(U.c112, null, 'red', 'tel:112'); chip(U.c108, null, 'teal', 'tel:108'); chip(U.again, () => go('start')); } }, 900 * (k + 1))); }
 function handle(txt) {
   txt = txt.trim(); if (!txt) return; say(txt, 'u');
   for (const [re, id] of KW) { if (new RegExp(re, 'i').test(txt)) { if (id === 'amb') { go('amb'); } else go(id); return; } }
   opts.innerHTML = ''; say(U.you_ok); N.start.o.forEach(o => chip(o[0], () => { say(o[0], 'u'); go(o[1]); }));
 }
 $('#hc-s').onclick = () => { const t = $('#hc-t'); handle(t.value); t.value = ''; };
 $('#hc-t').onkeydown = e => { if (e.key === 'Enter') { handle(e.target.value); e.target.value = ''; } };
 function place() { const r = root.getBoundingClientRect(), p = $('#hc-panel');
   p.style.top = r.top < 520 ? '78px' : 'auto'; p.style.bottom = r.top < 520 ? 'auto' : '78px';
   p.style.left = r.left < 360 ? '0' : 'auto'; p.style.right = r.left < 360 ? 'auto' : '0'; }
 function drag(handle) {
   let sx, sy, ox, oy, moved = false, down = false;
   handle.addEventListener('pointerdown', e => { if (e.target.id === 'hc-x') return; down = true; moved = false; sx = e.clientX; sy = e.clientY;
     const r = root.getBoundingClientRect(); ox = r.left; oy = r.top; handle.setPointerCapture(e.pointerId); });
   handle.addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - sx, dy = e.clientY - sy;
     if (Math.abs(dx) + Math.abs(dy) > 5) moved = true; if (!moved) return;
     const w = root.offsetWidth, h = root.offsetHeight;
     const x = Math.max(0, Math.min(P.innerWidth - w, ox + dx)), y = Math.max(0, Math.min(P.innerHeight - h, oy + dy));
     root.style.left = x + 'px'; root.style.top = y + 'px'; root.style.right = 'auto'; root.style.bottom = 'auto'; place(); });
   handle.addEventListener('pointerup', e => { if (!down) return; down = false;
     if (moved) { try { P.localStorage.setItem('hc_pos', JSON.stringify({l: root.style.left, t: root.style.top})); } catch (_) {} }
     else if (handle.id === 'hc-bubble') toggle(); });
 }
 function toggle() { root.classList.toggle('open'); place(); if (root.classList.contains('open') && !msgs.children.length) go('start'); }
 drag($('#hc-bubble')); drag($('#hc-head'));
 $('#hc-x').onclick = () => root.classList.remove('open');
 try { const p = JSON.parse(P.localStorage.getItem('hc_pos') || 'null');
   if (p) { root.style.left = p.l; root.style.top = p.t; root.style.right = 'auto'; root.style.bottom = 'auto'; } } catch (_) {}
 place();
})();
</script>
"""


def build_chat(lang):
    return WIDGET.replace("__TREE__", json.dumps(TREE[lang], ensure_ascii=False)).replace(
        "__KW__", json.dumps(KEYWORDS, ensure_ascii=False))
