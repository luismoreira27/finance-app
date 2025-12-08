import streamlit as st
import pathlib as Path
import requests

st.set_page_config(page_title = "Create Profile")

API_URL = "http://127.0.0.1:8000"

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if st.button("Home"):
    st.switch_page("pages/home.py")

st.title("Create Your Profile")
st.write("Fill out the information below to create your user profile.")

with st.form("profile_form"):
    name = st.text_input("Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type = "password")
    password_check = st.text_input("Confirm Password", type = "password")

    submitted = st.form_submit_button("Create Profile")

if submitted:
    if password != password_check:
        st.error("Passwords do not match!")
    elif len(password) < 6:
        st.error("Password needs to be at least 6 characters long!")
    else:
        st.success("Password OK! Creating profile...")

        res = requests.post(
            f"{API_URL}/auth/register",
            json = {"name": name, "username": username, "password": password}
        )

        if res.status_code == 200:
            st.success("Profile created sucessfully!")
        else:
            st.error(res.json()["detail"])