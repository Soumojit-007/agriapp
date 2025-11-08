import streamlit as st
from Login import login_page
from Signup import signup_page
import base64

st.set_page_config(page_title="AI Agri Assistant", page_icon="🌾", layout="wide")

# ----- SIDEBAR & HEADER -----
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: rgba(190, 245, 230, 0.42) !important; /* Soft teal, semi-transparent */
    border-radius: 22px 44px 24px 18px;
    padding-top: 19px !important;
}
[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
    min-height: 0 !important;
    visibility: hidden !important;
}
/* Sidebar nav boxes: black background, white bold text */
[data-testid="stSidebarNav"] li a {
    background: #111 !important;         /* dark/black box for each menu item */
    border-radius: 15px;
    padding: 18px 30px;
    font-size: 1.34em;
    color: #fff !important;              /* white text */
    font-weight: 900 !important;
    text-shadow: none !important;
    letter-spacing: 0.05em;
    border: 2.2px solid #4ae4a6;
    box-shadow: 0 3px 14px #e3e3e3cc;
    opacity: 1 !important;
    transition: background 0.14s, color 0.11s, border 0.13s;
}
[data-testid="stSidebarNav"] li.selected a,
[data-testid="stSidebarNav"] li a:hover {
    background: #232323 !important;
    color: #fff !important;
    border: 2px solid #14dda4;
    box-shadow: 0 6px 22px #f7f7f7bb;
}
/* Team Section (unchanged) */
.team-row-new {
  display: flex; gap: 33px; justify-content: center; flex-wrap: wrap;
}
.team-tile-new {
  background: linear-gradient(108deg,rgba(210,232,255,0.63) 0%, rgba(241,255,215,0.63) 100%);
  border-radius: 25px;
  box-shadow: 0 4px 32px #bdfafd1f;
  min-width: 218px; max-width:270px;
  padding: 23px 18px 15px 18px;
  margin-bottom: 24px;
  text-align:center; transition: box-shadow 0.19s;
}
.team-tile-new:hover { box-shadow: 0 8px 38px #ace8ff44;}
.team-avatar-new {
  margin-top: 5px;
  margin-bottom: 13px;
  width: 70px; height: 70px; border-radius: 50%;
  display:inline-block; font-size:2.7em;box-shadow:0 2px 13px #e3efecbb; background:#fff5e0;
}
.team-name { margin-top: 7px; font-weight:900; font-size:1.13em; color:#2d231a;}
.team-role { font-size: 1.02em; color: #1e8354; font-weight:700;}
.team-resp {font-size:1.01em;color:#17539a;margin-top:8px;}
</style>
""", unsafe_allow_html=True)

# ----- VIDEO BACKGROUND -----
def add_video_background(video_file):
    video_bytes = open(video_file, "rb").read()
    video_b64 = base64.b64encode(video_bytes).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{ background: transparent !important; }}
        #video-background {{
            position: fixed; right:0; bottom:0; min-width:100vw; min-height:100vh;
            z-index:-1; opacity:0.62; object-fit:cover;
        }}
        .overlay {{
            position:fixed; left:0; top:0; width:100vw; height:100vh;
            background:rgba(8,33,28,0.48); z-index:0;
        }}
        </style>
        <video autoplay loop muted id="video-background">
            <source src="data:video/mp4;base64,{video_b64}" type="video/mp4" />
        </video>
        <div class="overlay"></div>
        """,
        unsafe_allow_html=True,
    )

# ---- AUTH ----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if not st.session_state.logged_in:
    if st.session_state.show_signup:
        signup_page()
    else:
        login_page()
    st.stop()

add_video_background("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/aboutus.mp4")

logo_path = "C:/Users/uddip/Downloads/agriapp/agriapp/frontend/logo.png"
st.markdown(
    """
    <div style='display:flex;align-items:center;gap:20px;margin-bottom:10px;margin-top:15px;'>
      <img src='data:image/png;base64,{}' width='74'/>
      <span style='font-size:40px;color:#203c0b;font-weight:900;letter-spacing:2px;text-shadow:1px 2px 10px #d2ffb3, 0 0 12px #93f58b;'>
        AI-Powered Agri Assistant
      </span>
    </div>
    """.format(base64.b64encode(open(logo_path, "rb").read()).decode()),
    unsafe_allow_html=True,
)

st.markdown("""
<div style='max-width:1050px; margin:42px auto 8px auto; background:rgba(255,255,255,0.51); border-radius:22px; box-shadow:0 6px 42px #81f3df36; padding:36px 20px 28px 20px;'>
<div style="font-size:2.2em; font-weight:900; color:#36210c; margin-bottom:18px;">
    About the Unified Agricultural Assistance System
</div>
<div style="font-size:1.24em; font-weight:900; color:#226a38;margin-bottom:19px;">
    Our system offers an all-in-one platform for intelligent farming:<br/>
    Detecting crop disease, recommending fertilizer upgrades, performing market analysis, providing policy updates, and featuring an Ask Assistant.
</div>
<div class="team-row-new">
  <div class="team-tile-new">
    <div class="team-avatar-new">👨‍💻</div>
    <div class="team-name">Soumojit </div>
    <div class="team-role">Backend Lead</div>
    <div class="team-resp">Built the robust backend powering all core app features.</div>
  </div>
  <div class="team-tile-new">
    <div class="team-avatar-new">🧑‍🎨</div>
    <div class="team-name">Arghya</div>
    <div class="team-role">Frontend Developer</div>
    <div class="team-resp">Designed the modern, user-friendly dashboard and UI.</div>
  </div>
  <div class="team-tile-new">
    <div class="team-avatar-new">🧑‍💻</div>
    <div class="team-name">Uddipan</div>
    <div class="team-role">Frontend Developer, UI/UX Designer</div>
    <div class="team-resp">Created seamless flows, built intuitive user experience, and led UI/UX design.</div>
  </div>
  <div class="team-tile-new">
    <div class="team-avatar-new">🔗</div>
    <div class="team-name">Ankit</div>
    <div class="team-role">Integration Specialist</div>
    <div class="team-resp">Unified all features into a single, smart dashboard.</div>
  </div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
if st.button("Logout 🚪"):
    st.session_state.logged_in = False
    st.rerun()
