import streamlit as st
import requests
import base64

API = "http://localhost:8000/api/login"

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
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

def login_page():
    st.set_page_config(page_title="AgriApp Login", page_icon="🌾", layout="wide")
    set_background("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/first.jpg")

    st.image("C:/Users/uddip/Downloads/agriapp/agriapp/frontend/logo.png", width=85)
    st.markdown("<h3 style='color:#4ea8ff; margin-top:10px; margin-bottom:18px;'>AgriApp</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:28px;color:#4ea8ff;font-weight:600;margin-bottom:10px;'>Welcome Back 👋</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:15px;color:#d0f5ff;margin-bottom:28px;'>Login to continue to your Smart Farming Assistant</div>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
    
    if submit:
        response = requests.post(API, json={"username": username, "password": password})
        if response.status_code == 200 and "result" in response.json():
            data = response.json()["result"]
            st.session_state.logged_in = True
            st.session_state.token = data.get("token", "")
            st.success("✅ Login Successful")
            st.rerun()
        else:
            st.error("❌ Invalid Credentials")

    if st.button("Create a new account →"):
        st.session_state.show_signup = True
        st.rerun()
