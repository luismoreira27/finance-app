import streamlit as st
import requests
import pandas as pd

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

tab1, tab2 = st.tabs(["Add Single Transaction", "Add CSV File"])

with tab1:
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

with tab2:
    st.subheader("Upload CSV File")

    uploaded_file = st.file_uploader("Choose a CSV file", type = ["csv"])

    if uploaded_file is None:
        st.info("Please upload CSV file")
    else:
        try:
            df_upload = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            st.stop()

        required_cols = {"date", "category", "amount"}
        if not required_cols.issubset(df_upload.columns):
            st.error("CSV must contain columns: date, category, amount")
        else:
            st.write("Preview of uploaded CSV:")
            st.dataframe(df_upload.head(), use_container_width=True)

            if st.button("Upload CSV"):
                upload_records = df_upload.to_dict(orient = "records")

                for row in upload_records:
                    if "note" not in row or pd.isna(row["note"]):
                        row["note"] = None

                    row.pop("id", None)
                    
                    payload = {
                        "date" : str(row["date"]),
                        "category" : str(row["category"]),
                        "amount" : float(row["amount"]),
                        "note" : row.get("note", None),
                    }

                    requests.post(f"{API_URL}/transactions/", json = payload)

                st.success("CSV uploaded sucessfully!")
                st.rerun()