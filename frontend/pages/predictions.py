import streamlit as st

st.set_page_config(page_title = "Predictions")

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

st.title("Finance Predictions")
st.write("Page Under Development!!")