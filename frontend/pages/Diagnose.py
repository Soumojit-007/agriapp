import streamlit as st
from lib.client import post
import base64

def set_custom_style(bg_path):
    with open(bg_path, "rb") as image_file:
        bg_base64 = base64.b64encode(image_file.read()).decode()
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        background: rgba(190, 245, 230, 0.42) !important;
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
    .diag-card {{
        background: rgba(255,255,255,0.95);
        border-radius: 21px;
        box-shadow: 0 3px 26px #6be9c340;
        padding: 38px 38px 33px 38px;
        margin: 44px auto 28px auto;
        max-width: 670px;
    }}
    .diag-title {{
        font-size:2.3em; font-weight:900; color:#28455a; letter-spacing:1px; text-align:center; text-shadow:0 2px 9px #cafff1cc;
        margin-bottom:13px;
    }}
    </style>
    """, unsafe_allow_html=True)

set_custom_style("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/pages/diagonise.jpg")

# ---- App Logo at top ----
with open("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/pages/logo.png", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()
st.markdown(f"""
<div class="diag-card">
    <div style='display:flex;justify-content:center;align-items:center;margin-bottom:18px;'>
        <img src='data:image/png;base64,{logo_base64}' width='68' style='border-radius:14px;box-shadow:0 2px 16px #ade8aa40;'>
    </div>
    <div class="diag-title">🦠 Crop Disease Diagnosis</div>
""", unsafe_allow_html=True)

# File uploader
file = st.file_uploader(
    "Upload a leaf image (optional)",
    type=["jpg", "jpeg", "png"]
)

# Symptom input
symptom = st.text_input(
    "Describe the symptoms",
    placeholder="e.g., Yellow spots appearing"
)

# Diagnose button
if st.button("Diagnose"):
    if not symptom.strip() and not file:
        st.warning("⚠️ Please provide either a symptom description or upload an image.")
    else:
        with st.spinner("Analyzing..."):
            try:
                files = {"image": (file.name, file, file.type)} if file else None
                data = {"symptom": symptom.strip()}
                res = post("/api/diagnose", files=files, data=data)

                st.subheader("🧾 Diagnosis Result")
                if isinstance(res, dict) and "result" in res:
                    result = res["result"]
                    st.write(f"**Disease:** {result.get('disease', 'Not detected')}")
                    st.write(f"**Confidence:** {result.get('confidence', 0)}")

                    if result.get("treatment_steps"):
                        st.subheader("🩺 Treatment Steps")
                        for step in result["treatment_steps"]:
                            st.write(f"- {step}")

                    if result.get("pesticide_options"):
                        st.subheader("🧪 Pesticide Options")
                        for item in result["pesticide_options"]:
                            st.write(f"- {item}")

                else:
                    st.error("Unexpected response format from API.")
                    st.write(res)

            except Exception as e:
                st.error(f"Diagnosis failed: {e}")

st.markdown('</div>', unsafe_allow_html=True)
