import streamlit as st
import requests
import base64

API = "http://localhost:8000/api/signup"

def set_background(image_file):
    with open(image_file, "rb") as img_file:
        img_bytes = img_file.read()
        img_b64 = base64.b64encode(img_bytes).decode()
    page_bg_img = f"""
    <style>
    .stApp {{
      background-image: url("data:image/jpg;base64,{img_b64}");
      background-size: cover;
      background-repeat: no-repeat;
      background-position: center;
    }}
    /* Hide the Streamlit sidebar */
    [data-testid="stSidebar"], .css-1lcbmhc.e1fqkh3o3 {{
        display: none !important;
    }}
    /* Make input boxes grey */
    .stTextInput > div > div > input, .stPasswordInput > div > div > input {{
        background-color: #cfd2da !important;
        color: #222 !important;
    }}
    .stTextInput > div > div, .stPasswordInput > div > div {{
        background-color: #cfd2da !important;
        border-radius: 10px !important;
    }}
    button[kind="primary"] {{
        color: #fff !important;
        background: #6886A0 !important;
        border-radius: 8px !important;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

def signup_page():
    st.set_page_config(page_title="AgriApp Signup", page_icon="🌾", layout="wide")
    set_background("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/signup.jpg")
    
    st.image("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/logo.png", width=85)
    st.markdown("<h3 style='color:#4ea8ff; margin-top:10px; margin-bottom:18px;'>AgriApp</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="
        margin-left:auto;
        margin-right:auto;
        width: 480px;
        padding: 18px 24px 12px 24px;
        background: rgba(255,255,255,0.75);
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 2px 12px rgba(30,90,30,0.07);
        text-align:center;">
        <span style="font-size:31px; font-weight:800; color:#1986cf; letter-spacing:1px;">Create Account 📝</span>
        <br>
        <span style="display:block; margin-top:9px; font-size:17px; font-weight:700; color:#384a5a;">
            Sign up for your Smart Farming Assistant
        </span>
    </div>
    """, unsafe_allow_html=True)

    with st.form("signup_form"):
        username = st.text_input("Choose a Username")
        password = st.text_input("Choose a Password", type="password")
        submit = st.form_submit_button("Sign Up")

    if submit:
        if not username.strip() or not password.strip():
            st.warning("⚠️ Both fields are required.")
        else:
            response = requests.post(API, json={"username": username, "password": password})
            if response.status_code == 200:
                st.success("✅ Account Created Successfully! Please Login.")
                st.session_state.show_signup = False
                st.rerun()
            elif response.status_code == 400:
                st.error("⚠️ Username already exists. Try another one.")
            else:
                st.error("❌ Signup failed. Try again later.")

    st.markdown("---")
    if st.button("← Back to Login"):
        st.session_state.show_signup = False
        st.rerun()
