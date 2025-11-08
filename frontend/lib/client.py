import os
import requests
import streamlit as st

# Fetch API base URL from Streamlit secrets or environment variable
def api_base() -> str:
    return (
        st.secrets.get("API_BASE_URL")
        or os.getenv("API_BASE_URL")
        or "http://localhost:8000"
    )

# Generic POST request helper
def post(path: str, json: dict = None, files: dict = None, data: dict = None) -> dict:
    url = f"{api_base().rstrip('/')}/{path.lstrip('/')}"
    try:
        response = requests.post(url, json=json, files=files, data=data, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"POST request failed: {e}")
        return {"error": str(e)}

# Generic GET request helper
def get(path: str, params: dict = None) -> dict:
    url = f"{api_base().rstrip('/')}/{path.lstrip('/')}"
    try:
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"GET request failed: {e}")
        return {"error": str(e)}
