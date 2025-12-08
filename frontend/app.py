import streamlit as st
import requests

st.set_page_config(page_title = "Login")

API_URL = "http://127.0.0.1:8000"

st.markdown("""
    <style>-
    [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type = "password")

if st.button("Login"):
    res = requests.post(
        f"{API_URL}/auth/login",
        json = {"username": username, "password": password}
    )
    if res.status_code == 200:
        st.success("Login Successful!")
        st.switch_page("pages/home.py")
    else:
        st.error(res.json()["detail"])

if st.button("Create Profile"):
    st.switch_page("pages/create_profile.py")