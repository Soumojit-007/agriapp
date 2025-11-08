import streamlit as st
import plotly.express as px
from lib.client import get
import base64

# ---- STYLE & BACKGROUND ----
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
    .dash-card {{
        background: rgba(255,255,255,0.89);
        border-radius: 18px;
        box-shadow: 0 3px 26px #3eeec839;
        padding: 38px 38px 33px 38px;
        margin: 44px auto 28px auto;
        max-width: 780px;
    }}
    .dash-title {{
        font-size:2.3em; font-weight:900; color:#265a4c; letter-spacing:1px; text-align:center; text-shadow:0 2px 9px #65ffcabb;
        margin-bottom:13px;
    }}
    </style>
    """, unsafe_allow_html=True)

set_custom_style("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/pages/dashboard.jpg")

# ---- Add App Logo at Top ----
with open("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/pages/logo.png", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()
st.markdown(f"""
<div class="dash-card">
    <div style='display:flex;justify-content:center;align-items:center;margin-bottom:14px;'>
        <img src='data:image/png;base64,{logo_base64}' width='68' style='border-radius:14px;box-shadow:0 2px 16px #ade8aa40;'>
    </div>
    <div class="dash-title">📊 Dashboard</div>
""", unsafe_allow_html=True)

# Fetch dashboard data
with st.spinner("Loading dashboard data..."):
    try:
        data = get("/api/dashboard")
    except Exception as e:
        st.error(f"Failed to load dashboard data: {e}")
        st.stop()

# 🔥 Ensure we extract `result` field properly
if not isinstance(data, dict) or "result" not in data:
    st.error("Unexpected response format from API.")
    st.write(data)
    st.stop()

result = data["result"]
metrics = result.get("metrics", {})
trends = result.get("trends", [])

# Metrics Section
c1, c2, c3 = st.columns(3)
c1.metric("Queries Today", metrics.get("queries_today", 0))
c2.metric("Diagnoses", metrics.get("diagnoses", 0))
c3.metric("Avg Latency (ms)", metrics.get("avg_latency_ms", 0))

# Chart Section
if isinstance(trends, list) and trends:
    try:
        fig = px.bar(
            trends,
            x="day",
            y="queries",
            title="Weekly Queries",
            color="day",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error generating chart: {e}")
else:
    st.info("No trend data available to display.")

st.markdown('</div>', unsafe_allow_html=True)
