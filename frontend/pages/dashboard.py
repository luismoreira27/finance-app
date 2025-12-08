import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Finance Dashboard")

if st.button("Home"):
    st.switch_page("pages/home.py")

@st.cache_data
def load_data(start_date=None, end_date=None, category=None):
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if category:
        params["category"] = category
    r = requests.get(f"{API_URL}/transactions/", params=params)
    return pd.DataFrame(r.json())

st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start date")
end_date = st.sidebar.date_input("End date")
category_filter = st.sidebar.text_input("Category")

df = load_data(start_date=str(start_date), end_date=str(end_date), category=category_filter)

if not df.empty:
    df["date"] = pd.to_datetime(df["date"])
    st.subheader("Spending Over Time")
    st.line_chart(df.set_index("date")["amount"].cumsum())

    st.subheader("Expenses by Category")
    cat_sum = df.groupby("category")["amount"].sum()
    st.bar_chart(cat_sum)

    st.subheader("Category Distribution")
    st.pyplot(cat_sum.plot.pie(autopct='%1.1f%%').figure)
else:
    st.error("No Data has been found!")