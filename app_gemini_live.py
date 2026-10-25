import os, re, requests
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
KEY = os.getenv("GEMINI_API_KEY") or os.getenv("LLM_API_KEY", "")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

st.set_page_config(page_title="Customer Support AI", page_icon="💬", layout="wide")
st.markdown("""
<style>
.stApp {background:linear-gradient(135deg,#101827,#17263a);color:#f5f7fb}
h1,h2,h3,p,label {color:#f5f7fb}
[data-testid="stMetric"] {background:#22344b;padding:18px;border-radius:14px;border:1px solid #344a64}
.stButton>button {background:#ff8a3d;color:white;border:0;border-radius:10px;padding:10px 20px}
</style>
""", unsafe_allow_html=True)

st.title("💬 Customer Support AI Agent")
st.caption("Gemini-powered reply drafting • Human review required • Replies are not sent automatically")

a,b,c = st.columns(3)
a.metric("AI provider", "Gemini")
b.metric("Model", MODEL)
c.metric("Mode", "Live API" if KEY else "No API key")

with st.expander("📊 Example support dashboard", expanded=True):
    left,right = st.columns(2)
    with left:
        st.subheader("Illustrative ticket distribution")
        fig = px.pie(pd.DataFrame({"Status":["Resolved","Waiting","Escalated"],"Count":[68,22,10]}),
                     names="Status", values="Count", hole=.58)
        fig.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig,use_container_width=True)
    with right:
        st.subheader("Illustrative weekly activity")
        fig2 = px.area(pd.DataFrame({"Day":["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
                                    "Tickets":[18,25,21,31,27,35,29]}),x="Day",y="Tickets")
        fig2.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2,use_container_width=True)
    st.caption("Charts use demonstration values, not real customer data.")

st.divider()
st.subheader("Draft a customer response")
message = st.text_area("Customer message", placeholder="Example: I received a damaged product and want a refund.", height=140)
tone = st.selectbox("Reply tone", ["Warm and professional","Brief and direct","Empathetic"])
if st.button("✨ Generate reply with Gemini", type="primary"):
    if not message.strip():
        st.warning("Enter a customer message first.")
    elif not KEY:
        st.error("No Gemini key found in the portfolio .env file.")
    else:
        prompt = f"""You are a careful customer-support assistant.
Classify the issue and draft a helpful reply in this tone: {tone}.
Do not claim a refund, replacement, shipment, or account action has occurred.
Do not invent company policies. Ask only for information needed through approved support channels.
Flag when a human agent must review the case.
Return sections: CATEGORY, DRAFT REPLY, HUMAN REVIEW.
Customer message:
{message[:6000]}"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
        try:
            with st.spinner("Gemini is drafting a response..."):
                response = requests.post(
                    url, params={"key": KEY},
                    json={"contents":[{"parts":[{"text":prompt}]}],
                          "generationConfig":{"temperature":0.3,"maxOutputTokens":700}},
                    timeout=45
                )
            if response.status_code != 200:
                st.error(f"Gemini request failed (HTTP {response.status_code}). Check the model name, key permissions, and API limits. The response body is hidden to protect secrets.")
            else:
                data = response.json()
                candidates = data.get("candidates", [])
                parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
                answer = "\n\n".join(p.get("text","") for p in parts if p.get("text"))
                if answer:
                    st.success("Gemini generated a draft.")
                    st.markdown(answer)
                    st.info("Human review required before using this reply. Nothing has been sent.")
                else:
                    st.error("Gemini returned no text. Try again or check API usage limits.")
        except requests.RequestException:
            st.error("Could not reach Gemini. Check your internet connection and try again.")
