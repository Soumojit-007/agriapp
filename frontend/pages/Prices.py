import streamlit as st
import plotly.express as px
from lib.client import get
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
    .price-card {{
        background: rgba(255,255,255,0.91);
        border-radius: 21px;
        box-shadow: 0 3px 26px #efd79091;
        padding: 36px 36px 27px 36px;
        margin: 42px auto 24px auto;
        max-width: 720px;
    }}
    .price-title {{
        font-size:2.3em; font-weight:900; color:#a07511; letter-spacing:1px; text-align:center; text-shadow:0 2px 11px #ffeabb99;
        margin-bottom:15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---> UPDATE THIS LINE TO USE PRICES.JPG
set_custom_style("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/pages/prices.jpg")

with open("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/pages/logo.png", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()
st.markdown(f"""
<div class="price-card">
    <div style='display:flex;justify-content:center;align-items:center;margin-bottom:12px;'>
        <img src='data:image/png;base64,{logo_base64}' width='64' style='border-radius:13px;box-shadow:0 2px 16px #ffeabb40;'>
    </div>
    <div class="price-title">📈 Market Prices</div>
""", unsafe_allow_html=True)

crop = st.text_input("Crop", "Tomato")
region = st.text_input("Region", "Kolkata")

if st.button("Get Prices"):
    if not crop.strip() or not region.strip():
        st.warning("⚠️ Please enter both crop and region.")
    else:
        with st.spinner("Fetching market data..."):
            try:
                data = get("/api/prices", params={"crop": crop.strip(), "region": region.strip()})

                if not isinstance(data, dict):
                    st.error("Unexpected response format from API.")
                    st.write(data)
                    st.stop()

                hist = data.get("history", [])
                fc = data.get("forecast", [])
                best = data.get("best_mandi", {})

                if not hist and not fc:
                    st.info("No price data available for this crop and region.")
                else:
                    combined = hist + fc

                    fig = px.line(
                        combined,
                        x="date",
                        y="price",
                        title=f"{crop} Price Trend in {region}",
                        markers=True
                    )
                    fig.update_traces(mode="lines+markers")
                    st.plotly_chart(fig, use_container_width=True)

                if best and "name" in best:
                    st.subheader("🏪 Best Mandi Suggestion")
                    st.metric("Market", best["name"], f"{best.get('expected_price', 0)} ₹")
                else:
                    st.info("No best mandi data available.")

            except Exception as e:
                st.error(f"Failed to fetch market prices: {e}")

st.markdown('</div>', unsafe_allow_html=True)
