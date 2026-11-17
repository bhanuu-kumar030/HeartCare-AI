# Run with:  streamlit run app.py
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from chatbot import build_chat
from content import get as get_text
from explainer import build_explainer
from factors import analyze, card_html
from reels import build_html
from styles import CSS, hero_html
from ui import UI
from utils import age_group, risk_level, top_importances

st.set_page_config(page_title="HeartCare AI", page_icon="❤️", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)


@st.cache_resource
def load():
    saved = joblib.load("model.joblib")
    return saved["pipeline"], saved["info"]


pipe, info = load()
age_lo, age_hi = int(info["num_ranges"]["age"][0]), int(info["num_ranges"]["age"][1])

# ---------- language ----------
lang_pick = st.radio("Language / भाषा", ["English", "हिंदी"], horizontal=True, label_visibility="collapsed")
lang = "en" if lang_pick == "English" else "hi"
L = UI[lang]
T = get_text(lang)

st.markdown(hero_html(L["title"], L["subtitle"], L["badges"]), unsafe_allow_html=True)

main, side = st.columns([2.4, 1], gap="large")

# ---------- right side: always-visible emergency guide ----------
with side:
    do_html = "".join(f"<li>{x}</li>" for x in T["do"])
    dont_html = "".join(f"<li>{x}</li>" for x in T["dont"])
    st.markdown(
        f'<div class="side-marker"></div><div class="side-box"><h3>{L["side_title"]}</h3>'
        f'<a class="call c112" href="tel:112">📞 112</a><a class="call c108" href="tel:108">🚑 108</a>'
        f'<div class="sub do">{L["side_do"]}</div><ul>{do_html}</ul>'
        f'<div class="sub dont">{L["side_dont"]}</div><ul>{dont_html}</ul>'
        f'<div class="hc-foot">{T["disclaimer"]}</div></div>',
        unsafe_allow_html=True)


def pick(label, options, key):
    """Selectbox with a 'Don't know' first option. options = [[label, value], ...]. Returns value or None."""
    labels = [L["unknown"]] + [o[0] for o in options]
    choice = st.selectbox(label, labels, key=key)
    return None if choice == L["unknown"] else dict(options)[choice]


def yes_no(label, key):
    choice = st.selectbox(label, [L["unknown"], L["no"], L["yes"]], key=key)
    return {L["unknown"]: None, L["no"]: "False", L["yes"]: "True"}[choice]


with main:
    tab_check, tab_vid, tab_about = st.tabs([L["tab_check"], L["tab_videos"], L["tab_about"]])

    # ======================= Heart check =======================
    with tab_check:
        with st.form("check"):
            st.markdown(f'<div class="hc-step">{L["step1"]}</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            age = c1.number_input(L["age"], min_value=1, max_value=110, value=50, step=1)
            sex_label = c2.radio(L["sex"], [L["male"], L["female"]], horizontal=True)
            sex = "Male" if sex_label == L["male"] else "Female"

            st.markdown(f'<div class="hc-step">{L["step2"]}</div>', unsafe_allow_html=True)
            st.caption(L["step2_hint"])
            c1, c2 = st.columns(2)
            bp = c1.number_input(L["bp"], min_value=70, max_value=260, value=None, step=1,
                                 placeholder="120", help=L["bp_help"])
            chol = c2.number_input(L["chol"], min_value=100, max_value=600, value=None, step=1,
                                   placeholder="190", help=L["chol_help"])
            c1, c2 = st.columns(2)
            with c1:
                fbs = yes_no(L["sugar"], "fbs")
            with c2:
                exang = yes_no(L["exang"], "exang")
            cp = pick(L["chest"], L["cp_opts"], "cp")

            with st.expander(L["step3"]):
                c1, c2 = st.columns(2)
                thalch = c1.number_input(L["thalch"], min_value=60, max_value=230, value=None, step=1,
                                         placeholder="150", help=L["thalch_help"])
                oldpeak = c2.number_input(L["oldpeak"], min_value=-3.0, max_value=7.0, value=None, step=0.1,
                                          placeholder="0.5", help=L["oldpeak_help"])
                c1, c2 = st.columns(2)
                with c1:
                    restecg = pick(L["restecg"], L["restecg_opts"], "restecg")
                with c2:
                    slope = pick(L["slope"], L["slope_opts"], "slope")
                c1, c2 = st.columns(2)
                with c1:
                    ca_choice = st.selectbox(L["ca"], [L["unknown"], "0", "1", "2", "3"], key="ca")
                with c2:
                    thal = pick(L["thal"], L["thal_opts"], "thal")
            go = st.form_submit_button(L["submit"], type="primary", use_container_width=True)

        nan = np.nan
        row = {
            "age": float(age), "sex": sex,
            "trestbps": float(bp) if bp is not None else nan,
            "chol": float(chol) if chol is not None else nan,
            "fbs": fbs, "cp": cp, "exang": exang,
            "thalch": float(thalch) if thalch is not None else nan,
            "oldpeak": float(oldpeak) if oldpeak is not None else nan,
            "restecg": restecg, "slope": slope,
            "ca": float(ca_choice) if ca_choice != L["unknown"] else nan,
            "thal": thal,
        }
        if go:
            st.session_state["result"] = {"row": row}

        res = st.session_state.get("result")
        if res:
            r = res["row"]
            group, emoji = age_group(int(r["age"]))
            filled = sum(1 for k, v in r.items() if v is not None and v == v)
            st.progress(min(1.0, filled / 13), text=L["filled"].format(n=filled))
            st.markdown(f'<div class="hc-step">{L["result_title"]}</div>', unsafe_allow_html=True)

            if r["age"] < 18:
                st.warning(L["kid"].format(emoji=emoji, group=group, age=int(r["age"]), lo=age_lo, hi=age_hi))
            else:
                cols = ["age", "trestbps", "chol", "thalch", "oldpeak", "ca", "sex", "cp", "fbs", "restecg",
                        "exang", "slope", "thal"]
                df = pd.DataFrame([r])[cols]
                for c in ["age", "trestbps", "chol", "thalch", "oldpeak", "ca"]:
                    df[c] = df[c].astype(float)
                prob = float(pipe.predict_proba(df)[0, 1])
                level, _ = risk_level(prob)
                components.html(build_explainer(level, prob * 100, lang), height=1010, scrolling=True)
                if r["age"] < age_lo or r["age"] > age_hi:
                    st.info(L["range_note"].format(lo=age_lo, hi=age_hi, age=int(r["age"])))
                st.markdown(f'<div class="hc-step">{L["reasons"]}</div>', unsafe_allow_html=True)
                cards = analyze(r, lang)
                if cards:
                    st.markdown("".join(card_html(f, lang) for f in cards), unsafe_allow_html=True)
                else:
                    st.info(L["reasons_none"])
            st.caption(L["disc"])

    # ======================= Short videos =======================
    with tab_vid:
        st.caption(T["videos_intro"])
        components.html(build_html(T["reels"], height=620), height=620)
        st.caption(T["disclaimer"])

    # ======================= About =======================
    with tab_about:
        st.subheader(L["about_head"])
        for line in L["about"]:
            st.markdown(f"- {line}")
        st.subheader(L["feat"])
        imp = top_importances(pipe)
        if imp is not None:
            st.bar_chart(imp)

# ---------- floating, draggable chat assistant (injected into the page) ----------
components.html(build_chat(lang), height=0)
