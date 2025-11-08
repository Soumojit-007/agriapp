import streamlit as st
from lib.client import post
import base64

def set_custom_style(bg_path):
    with open(bg_path, "rb") as image_file:
        bg_base64 = base64.b64encode(image_file.read()).decode()
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        background: rgba(190, 245, 230, 0.42) !important;  /* Soft teal, semi-transparent */
        border-radius: 22px 44px 24px 18px;
        padding-top: 19px !important;
    }}
    [data-testid="stHeader"] {{
        background: transparent !important;
        height: 0 !important;
        min-height: 0 !important;
        visibility: hidden !important;
    }}
    [data-testid="stSidebarNav"] li a {{
        background: #111 !important;
        border-radius: 15px;
        padding: 18px 30px;
        font-size: 1.34em;
        color: #fff !important;
        font-weight: 900 !important;
        text-shadow: none !important;
        letter-spacing: 0.05em;
        border: 2.2px solid #4ae4a6;
        box-shadow: 0 3px 14px #e3e3e3cc;
        opacity: 1 !important;
    }}
    [data-testid="stSidebarNav"] li.selected a,
    [data-testid="stSidebarNav"] li a:hover {{
        background: #232323 !important;
        color: #fff !important;
        border: 2px solid #14dda4;
        box-shadow: 0 6px 22px #f7f7f7bb;
    }}
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .ask-card {{
        background: rgba(255,255,255,0.87);
        border-radius: 18px;
        box-shadow: 0 3px 26px #91f0bd39;
        padding: 35px 32px 30px 32px;
        margin: 42px auto 18px auto;
        max-width: 670px;
    }}
    .ask-title {{
        font-size:2.6em; font-weight:900; color:#1a532c; letter-spacing:1px; text-align:center; text-shadow:0 2px 11px #ccfee8cc;
        margin-bottom:15px;
    }}
    </style>
    """, unsafe_allow_html=True)

set_custom_style("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/pages/ask.png")

# ---- Add logo at top of card ----
with open("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/pages/logo.png", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()

st.markdown(f"""
<div class="ask-card">
    <div style='display:flex;justify-content:center;align-items:center;margin-bottom:15px;'>
        <img src='data:image/png;base64,{logo_base64}' width='72' style='border-radius:18px;box-shadow:0 2px 16px #ade8aa40;'>
    </div>
    <div class="ask-title">🎤 Ask the Assistant</div>
""", unsafe_allow_html=True)

# Input text area
text = st.text_area(
    "Type in any language",
    height=120,
    placeholder="পাতার রং হলুদ হয়ে যাচ্ছে / Yellowing leaves"
)

# Language selector
lang = st.selectbox("Select Language", ["bn", "hi", "en"], index=0)

# Button click
if st.button("Ask"):
    if not text.strip():
        st.warning("⚠️ Please enter some text before asking.")
    else:
        with st.spinner("Thinking..."):
            res = post("/api/ask", json={"text": text, "lang": lang})

            if not isinstance(res, dict):
                st.error("❌ Unexpected response from backend.")
                st.write(res)
            elif "result" not in res:
                st.error("❌ Backend did not return the expected format.")
                st.write(res)
            else:
                result = res["result"]

                # Display structured sections
                st.subheader("✅ Answer")
                st.write(result.get("answer", "No answer provided."))

                st.subheader("🎯 Intent")
                st.write(result.get("intent", "Not detected."))

                entities = result.get("entities", {})
                if entities:
                    st.subheader("🔍 Extracted Entities")
                    st.json(entities)

                st.caption(f"🌐 Detected Language: {result.get('language', lang)}")
st.markdown('</div>', unsafe_allow_html=True)
