import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title = "Data Upload")

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

st.title("Upload Data")

st.subheader("Add a Transaction")
with st.form("transaction_form"):
    date = st.date_input("Date")
    category = st.text_input("Category")
    amount = st.number_input("Amount", step=0.01)
    note = st.text_area("Note")
    submitted = st.form_submit_button("Add")
    if submitted:
        payload = {"date": str(date), "category": category, "amount": amount, "note": note}
        requests.post(f"{API_URL}/transactions/", json=payload)
        st.success("Transaction added!")
        st.rerun()