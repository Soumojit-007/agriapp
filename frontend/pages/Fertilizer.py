import streamlit as st
import json
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
    .fert-card {{
        background: rgba(255,255,255,0.92);
        border-radius: 21px;
        box-shadow: 0 3px 26px #53f09340;
        padding: 38px 38px 33px 38px;
        margin: 44px auto 28px auto;
        max-width: 670px;
    }}
    .fert-title {{
        font-size:2.3em; font-weight:900; color:#226a38; letter-spacing:1px; text-align:center; text-shadow:0 2px 9px #b0ffd2cc;
        margin-bottom:13px;
    }}
    </style>
    """, unsafe_allow_html=True)

set_custom_style("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/pages/fertiliser.jpg")

# ---- App Logo at top ----
with open("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/pages/logo.png", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()
st.markdown(f"""
<div class="fert-card">
    <div style='display:flex;justify-content:center;align-items:center;margin-bottom:18px;'>
        <img src='data:image/png;base64,{logo_base64}' width='68' style='border-radius:14px;box-shadow:0 2px 16px #ade8aa40;'>
    </div>
    <div class="fert-title">🧪 Fertilizer Advisor</div>
""", unsafe_allow_html=True)

# User inputs
crop = st.text_input("Crop", "Tomato")
symptoms = st.text_input("Symptoms (optional)", "")
npk = st.text_input("Soil NPK (e.g., N=120,P=40,K=80)", "")
ph = st.number_input("Soil pH", min_value=3.5, max_value=9.5, value=6.5, step=0.1)
organic = st.checkbox("Prefer organic options", value=False)

# Recommend button
if st.button("Recommend"):
    if not crop.strip():
        st.warning("⚠️ Please enter crop name.")
        st.stop()
    # Convert NPK input safely to dict
    soil_dict = {"pH": ph}
    if npk.strip():
        try:
            soil_parts = [x.strip() for x in npk.split(",")]
            for part in soil_parts:
                k, v = part.split("=")
                soil_dict[k.upper()] = float(v)
        except:
            st.warning("⚠️ Invalid NPK format. Use N=120,P=40,K=80")
            st.stop()

    # Convert dict → JSON text for query param
    soil_param = json.dumps(soil_dict)
    params = {
        "crop": crop.strip(),
        "soil": soil_param,
        "symptoms": symptoms.strip(),
        "organicPreferred": organic
    }
    with st.spinner("Generating fertilizer recommendation..."):
        try:
            res = get("/api/fertilizer", params=params)
            st.subheader("🌱 Recommended Fertilizer Plan")
            if isinstance(res, dict) and "result" in res:
                result = res["result"]
                st.write(f"**NPK Ratio:** {result.get('npk', 'N/A')}")
                st.write("**Recommended Products:**")
                for product in result.get("product_options", []):
                    st.write(f"- {product}")
                st.write(f"**Dosage per Hectare:** {result.get('dosage_per_ha', 'N/A')}")
                st.write(f"**Notes:** {result.get('notes', 'N/A')}")
            else:
                st.error("Unexpected response format from API.")
                st.write(res)
        except Exception as e:
            st.error(f"Failed to get fertilizer recommendation: {e}")

st.markdown('</div>', unsafe_allow_html=True)
