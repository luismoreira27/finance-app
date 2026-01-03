import streamlit as st
import pandas as pd
from utils import load_data
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


if df.empty:
    st.info("No data available.")
else:
    savings= df[df["category"] == "Savings"]
    saved = savings["amount"].sum()
    spent = df[(df["category"] != "Savings") & (df["category"] != "Salary")]
    spent["month"] = spent["date"].dt.month
    spent_month = spent.groupby("month")["amount"].sum()
    month_mean = spent_month.mean()
    salary = df[df["category"] == "Salary"]
    print(salary)
    salary_mean = salary["amount"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Savings", f"€{saved:,.2f}")
    col2.metric("Average Spending per Month", f"€{month_mean:,.2f}")
    col3.metric("Average Salary", f"€{salary_mean:,.2f}")

    st.subheader("Spending Over Time")

    fig1 = px.line(spent, x = "date", y = "amount",
                        title = "Daily Spending Trend")
    st.plotly_chart(fig1, use_container_width = True)

    st.subheader("Spending by Category")

    fig2 = px.bar(spent.groupby("category",  as_index = False)["amount"].sum(),
                    x = "category", y = "amount",
                    title = "Total Amount per Category")
    st.plotly_chart(fig2, use_container_width = True)

    st.subheader("Category Breakdown")

    fig3 = px.pie(spent, names = "category", values = "amount",
                    title = "Spending Distribution")
    st.plotly_chart(fig3, use_container_width = True)