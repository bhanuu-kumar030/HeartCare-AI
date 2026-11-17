# Plain-language reasons behind the numbers a person entered (English + Hindi).

def _t(lang, en, hi):
    return en if lang == "en" else hi


def analyze(row, lang):
    out = []

    def add(icon, title, value, status, text):
        out.append({"icon": icon, "title": title, "value": value, "status": status, "text": text})

    age = row.get("age")
    if age:
        if age >= 55:
            add("🎂", _t(lang, "Age", "उम्र"), str(int(age)), "warn", _t(lang,
                "Risk goes up with age. Indians often get heart attacks about 10 years earlier than people in rich countries, so regular check-ups matter.",
                "उम्र के साथ ख़तरा बढ़ता है। भारतीयों को दिल का दौरा अमीर देशों से लगभग 10 साल पहले पड़ता है, इसलिए नियमित जाँच ज़रूरी है।"))
        elif age >= 40:
            add("🎂", _t(lang, "Age", "उम्र"), str(int(age)), "warn", _t(lang,
                "Risk starts rising after 40 in Indians. Yearly BP, sugar and cholesterol checks are a good habit.",
                "भारतीयों में 40 के बाद ख़तरा बढ़ना शुरू होता है। हर साल BP, शुगर और कोलेस्ट्रॉल की जाँच अच्छी आदत है।"))
        else:
            add("🎂", _t(lang, "Age", "उम्र"), str(int(age)), "good", _t(lang,
                "Younger age helps, but food, tobacco and exercise still matter a lot.",
                "कम उम्र फ़ायदेमंद है, पर खान-पान, तंबाकू और कसरत फिर भी बहुत मायने रखते हैं।"))
    bp = row.get("trestbps")
    if bp == bp and bp is not None:
        if bp >= 140:
            st, tx = "bad", _t(lang, "High BP pushes blood hard against artery walls. Slowly this damages them and lets fat stick inside.",
                               "ऊँचा BP नसों की दीवार पर खून का ज़ोर बढ़ाता है। धीरे-धीरे दीवार खराब होती है और चर्बी जमने लगती है।")
        elif bp >= 120:
            st, tx = "warn", _t(lang, "Slightly above ideal (below 120). Less salt and daily walking can bring it down.",
                                "आदर्श (120 से कम) से थोड़ा ऊपर। कम नमक और रोज़ की सैर से घट सकता है।")
        else:
            st, tx = "good", _t(lang, "Your BP number is in a healthy range.", "आपका BP स्वस्थ सीमा में है।")
        add("🩸", _t(lang, "Blood pressure", "ब्लड प्रेशर"), f"{int(bp)} mmHg", st, tx)
    chol = row.get("chol")
    if chol == chol and chol is not None:
        if chol >= 240:
            st, tx = "bad", _t(lang, "High cholesterol is the 'fat' that collects inside heart arteries and narrows them.",
                               "ऊँचा कोलेस्ट्रॉल वही 'चर्बी' है जो दिल की नसों में जमकर उन्हें तंग करती है।")
        elif chol >= 200:
            st, tx = "warn", _t(lang, "Borderline. Cut fried food, ghee and vanaspati; eat more dal, sabzi and oats.",
                                "सीमा के पास। तला खाना, घी और वनस्पति कम करें; दाल, सब्ज़ी और ओट्स बढ़ाएँ।")
        else:
            st, tx = "good", _t(lang, "Cholesterol is in the desirable range.", "कोलेस्ट्रॉल अच्छी सीमा में है।")
        add("🧈", _t(lang, "Cholesterol", "कोलेस्ट्रॉल"), f"{int(chol)} mg/dl", st, tx)
    if row.get("fbs") == "True":
        add("🍬", _t(lang, "Blood sugar", "ब्लड शुगर"), _t(lang, "Above 120", "120 से ऊपर"), "bad", _t(lang,
            "High sugar harms the inner lining of blood vessels and speeds up blockage.",
            "ऊँची शुगर नसों की अंदरूनी परत को नुकसान पहुँचाती है और ब्लॉकेज जल्दी बनाती है।"))
    elif row.get("fbs") == "False":
        add("🍬", _t(lang, "Blood sugar", "ब्लड शुगर"), _t(lang, "Not high", "ऊँची नहीं"), "good",
            _t(lang, "Good. Keep sweets and sugary chai low.", "अच्छा है। मिठाई और मीठी चाय कम रखें।"))
    cp = row.get("cp")
    if cp == "typical angina":
        add("💢", _t(lang, "Chest pain", "सीने का दर्द"), _t(lang, "On effort", "मेहनत पर"), "bad", _t(lang,
            "Pain on effort that eases with rest is a classic sign that the heart is not getting enough blood.",
            "मेहनत पर दर्द और आराम से ठीक होना इस बात का आम संकेत है कि दिल को ज़रूरत भर खून नहीं मिल रहा।"))
    elif cp == "atypical angina":
        add("💢", _t(lang, "Chest pain", "सीने का दर्द"), _t(lang, "Sometimes", "कभी-कभी"), "warn", _t(lang,
            "Pain that is sometimes linked to effort should be checked by a doctor with an ECG.",
            "जो दर्द कभी-कभी मेहनत से जुड़ा हो, उसकी जाँच डॉक्टर से ECG के साथ करवाएँ।"))
    if row.get("exang") == "True":
        add("🏃", _t(lang, "Pain on exertion", "मेहनत पर दर्द"), _t(lang, "Yes", "हाँ"), "bad", _t(lang,
            "When you walk fast the heart needs more blood. Pain then means the narrowed artery cannot supply enough.",
            "तेज़ चलने पर दिल को ज़्यादा खून चाहिए। तब दर्द होने का मतलब है कि तंग नस पूरा खून नहीं पहुँचा पा रही।"))
    th = row.get("thalch")
    if th == th and th is not None:
        add("⚡", _t(lang, "Peak heart rate (TMT)", "TMT में सबसे ज़्यादा धड़कन"), f"{int(th)} bpm",
            "warn" if th < 120 else "good", _t(lang,
            "A low peak rate in a stress test can mean poor heart fitness." if th < 120 else "Good peak rate in the stress test.",
            "स्ट्रेस टेस्ट में कम धड़कन दिल की कमज़ोर फ़िटनेस का संकेत हो सकती है।" if th < 120 else "स्ट्रेस टेस्ट में धड़कन अच्छी रही।"))
    op = row.get("oldpeak")
    if op == op and op is not None:
        st = "bad" if op >= 2 else "warn" if op >= 1 else "good"
        add("📈", "ST depression", f"{op:g}", st, _t(lang,
            "ST depression on a stress ECG shows the heart muscle was strained." if op >= 1 else "Small ST change, which is reassuring.",
            "स्ट्रेस ECG में ST डिप्रेशन बताता है कि दिल की मांसपेशी पर ज़ोर पड़ा।" if op >= 1 else "ST में बदलाव छोटा है, जो तसल्ली की बात है।"))
    ecg = row.get("restecg")
    if ecg in ("st-t abnormality", "lv hypertrophy"):
        add("📟", "ECG", ecg, "warn", _t(lang, "Your resting ECG shows a change that a heart doctor should review.",
                                         "आपके ECG में बदलाव है जिसे हृदय रोग विशेषज्ञ को दिखाना चाहिए।"))
    ca = row.get("ca")
    if ca == ca and ca is not None and ca >= 1:
        add("🧬", _t(lang, "Blocked vessels", "बंद नसें"), str(int(ca)), "bad", _t(lang,
            "Blockage already seen in heart vessels. This needs a cardiologist's plan.",
            "दिल की नसों में ब्लॉकेज पहले से दिख रहा है। इसके लिए हृदय रोग विशेषज्ञ की योजना चाहिए।"))
    if row.get("thal") in ("fixed defect", "reversable defect"):
        add("☢️", "Nuclear scan", row["thal"], "bad", _t(lang,
            "The scan shows an area of heart muscle that is not getting enough blood.",
            "स्कैन में दिल की मांसपेशी का एक हिस्सा दिख रहा है जिसे पूरा खून नहीं मिल रहा।"))
    if row.get("slope") in ("flat", "downsloping"):
        add("📉", "ST slope", row["slope"], "warn", _t(lang,
            "A flat or downward ST slope in a stress test can point to poor blood supply.",
            "स्ट्रेस टेस्ट में सपाट या नीचे की ढलान खून की कमी का संकेत हो सकती है।"))
    return out


def card_html(f, lang):
    label = "Your value" if lang == "en" else "आपका मान"
    return (f'<div class="f-card {f["status"]}"><div class="f-icon">{f["icon"]}</div><div>'
            f'<div class="f-title">{f["title"]}</div><div class="f-val">{label}: {f["value"]}</div>'
            f'<div class="f-text">{f["text"]}</div></div></div>')
