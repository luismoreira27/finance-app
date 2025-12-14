import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

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

def load_data():
    r = requests.get(f"{API_URL}/transactions/")
    if r.status_code != 200:
        st.error("Backend not running!")
        return pd.DataFrame()
    return pd.DataFrame(r.json())


df = load_data()

if st.button("Refresh"):
    df = load_data()

if not df.empty:
    df["date"] = pd.to_datetime(df["date"])


st.sidebar.header("Filters")

if not df.empty:
    start_date = st.sidebar.date_input("Start Date", df["date"].min())
    end_date = st.sidebar.date_input("End Date", df["date"].max())

    category_filter = st.sidebar.multiselect(
        "category Filter",
        sorted(df["category"].unique()),
        default = sorted(df["category"].unique())
    )

    df = df[
        (df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date)) &
        (df["category"].isin(category_filter))
    ]

tab1, tab2 = st.tabs([
    "📊 Plotly Charts",
    "🧮 Summary",
])

with tab1:
    if df.empty:
        st.info("No data available.")
    else:
        st.subheader("Spending Over Time")

        fig1 = px.scatter(df, x = "date", y = "amount",
                          title = "Daily Spending Trend")
        st.plotly_chart(fig1, use_container_width = True)

        st.subheader("Spending by Category")

        fig2 = px.bar(df.groupby("category",  as_index = False)["amount"].sum(),
                      x = "category", y = "amount",
                      title = "Total Amount per Category")
        st.plotly_chart(fig2, use_container_width = True)

        st.subheader("Category Breakdown")

        fig3 = px.pie(df, names = "category", values = "amount",
                      title = "Spending Distribution")
        st.plotly_chart(fig3, use_container_width = True)

        st.subheader("Category Tree")

        fig4 = px.treemap(df, path = ["category"], values = "amount",
                          title = "Category Tree Map")
        st.plotly_chart(fig4, use_container_width = True)

with tab2:
    if df.empty:
        st.info("No data available.")
    else:
        total = df["amount"].sum()
        avg = df["amount"].mean()
        max_expense = df["amount"].max()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Spent", f"${total:,.2f}")
        col2.metric("Average Transaction", f"${avg:,.2f}")
        col3.metric("Largest Transaction", f"${max_expense:,.2f}")

        st.write("### Transactions per Category")
        category_table = df.groupby("category")["amount"].sum()
        st.table(category_table)