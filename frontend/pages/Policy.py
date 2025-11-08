import streamlit as st
from lib.client import get
import base64

def set_custom_style(bg_path):
    with open(bg_path, "rb") as image_file:
        bg_base64 = base64.b64encode(image_file.read()).decode()
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        background: rgba(190, 245, 230, 0.42) !important; /* Soft teal, semi-transparent */
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
        background-image: url("data:image/jpeg;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .policy-card {{
        background: rgba(255,255,255,0.92);
        border-radius: 21px;
        box-shadow: 0 3px 29px #7bf0f390;
        padding: 38px 38px 25px 38px;
        margin: 42px auto 24px auto;
        max-width: 700px;
    }}
    .policy-title {{
        font-size:2.3em; font-weight:900; color:#24637a; letter-spacing:1px; text-align:center; text-shadow:0 2px 9px #91e8ea99;
        margin-bottom:13px;
    }}
    </style>
    """, unsafe_allow_html=True)

set_custom_style("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/pages/policy.jpg")

# ---- App Logo at top ----
with open("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/pages/logo.png", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()
st.markdown(f"""
<div class="policy-card">
    <div style='display:flex;justify-content:center;align-items:center;margin-bottom:18px;'>
        <img src='data:image/png;base64,{logo_base64}' width='68' style='border-radius:14px;box-shadow:0 2px 16px #ade8aa40;'>
    </div>
    <div class="policy-title">📄 Policy & Schemes</div>
""", unsafe_allow_html=True)

# Inputs
region = st.text_input("Region / State", "West Bengal")
lang = st.selectbox("Language", ["bn", "hi", "en"], index=0)

# Fetch button
if st.button("Fetch Updates"):
    if not region.strip():
        st.warning("⚠️ Please enter a valid region or state.")
    else:
        with st.spinner("Fetching latest policy and scheme updates..."):
            try:
                res = get("/api/policy", params={"region": region.strip(), "lang": lang})

                st.subheader("📜 Policy Summaries")

                if isinstance(res, dict) and "result" in res:
                    result = res["result"]

                    if isinstance(result, list) and result:
                        for idx, p in enumerate(result, start=1):
                            with st.expander(f"📝 Policy #{idx}: {p.get('title', 'Untitled')}"):
                                st.markdown(f"**Summary:**\n{p.get('summary', 'N/A')}")
                                st.markdown(f"**Recommended Actions:**\n{p.get('actions', 'N/A')}")
                    else:
                        st.json(result)

                else:
                    st.error("Unexpected response format from API.")
                    st.write(res)

            except Exception as e:
                st.error(f"Failed to fetch policy updates: {e}")

st.markdown('</div>', unsafe_allow_html=True)
