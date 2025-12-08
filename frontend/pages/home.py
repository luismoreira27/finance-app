import streamlit as st


st.set_page_config(page_title = "Home", layout = "centered")

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Home Page")

if st.button("Upload Data"):
    st.switch_page("pages/insert_data.py")

if st.button("Dashboard"):
    st.switch_page("pages/dashboard.py")

if st.button("Predictions"):
    st.switch_page("pages/predictions.py")