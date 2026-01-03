import streamlit as st
import requests
import pandas as pd
from utils import load_data, has_data

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

st.title("Data")

tab1, tab2, tab3 = st.tabs(["Upload Data", "Update Data", "Delete Data"])

if "data_uploaded" not in st.session_state:
    st.session_state.data_uploaded = has_data()

with tab1:
    subpage = st.radio(
        "Choose Option",
        ["Add Single Transaction", "Add CSV File"],
        horizontal = True
    )
    if subpage == "Add Single Transaction":
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

    elif subpage == "Add CSV File":
        st.subheader("Upload CSV File")

        uploaded_file = st.file_uploader("Choose a CSV file", type = ["csv"])

        if uploaded_file is None:
            pass
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
                st.dataframe(df_upload.head(), use_container_width=True, key = "preview_table")

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

                    st.session_state.data_uploaded = True
                    st.cache_data.clear()
                    st.success("CSV uploaded sucessfully!")
                    st.rerun()


with tab2:
    st.subheader("Update Data")

    if not st.session_state.data_uploaded:
        st.warning("Please upload data first")
    else:
        df = load_data()

        if st.button("Refresh", key = "refresh_update"):
            df = load_data()
        
        event = st.dataframe(
            df,
            width = "stretch",
            hide_index = True,
            on_select = "rerun",
            selection_mode = "single-row",
            key = "update_table"
        )

        row = event.selection.rows
        filtered_df = df.iloc[row]

        if filtered_df.empty:
            pass
        else:
            transaction_id = int(filtered_df["id"].iloc[0])
            with st.form("update_transaction"):
                date = st.date_input("Date", filtered_df["date"].iloc[0])
                category = st.text_input("Category", filtered_df["category"].iloc[0])
                amount = st.number_input("Amount", value = float(filtered_df["amount"].iloc[0]))
                note = st.text_area("Note", filtered_df["note"].iloc[0])
            
                submitted = st.form_submit_button("Update")

                if submitted:
                    payload = {
                        "date": str(date),
                        "category": category,
                        "amount": amount,
                        "note": note
                    }

                    res = requests.put(
                        f"{API_URL}/transactions/{transaction_id}",
                        json = payload
                    )

                    if res.status_code == 200:
                        st.success("Transaction updated sucessfully!")
                        st.json(res.json())
                        st.cache_data.clear()
                    else:
                        st.error(f"Update failed: {res.text}")


with tab3:
    st.subheader("Delete Data")

    if not st.session_state.data_uploaded:
        st.warning("Please upload data first")
    else:
        df = load_data()
        
        if st.button("Refresh"):
            df = load_data()
        
        event = st.dataframe(
            df,
            width = "stretch",
            hide_index = True,
            on_select = "rerun",
            selection_mode = "multi-row",
            key = "delete_table"
        )

        row = event.selection.rows
        filtered_df = df.iloc[row]

        if st.button("Delete Rows"):
            if filtered_df.empty:
                st.info("Select at least a Row")
            else:
                transaction_ids = filtered_df["id"].to_list()
                payload = {
                    "transaction_ids": transaction_ids
                }

                res = requests.delete(
                    f"{API_URL}/transactions/bulk/",
                    json = payload
                )

                if res.status_code == 200:
                    st.success("Rows successfully deleted")
                    st.cache_data.clear()
                else:
                    st.error(f"Delete failed: {res.text}")

        
        if st.button("Delete Table"):
            st.session_state.confirm_delete = True

        if st.session_state.get("confirm_delete"):
            st.warning("Are you sure you want to delete these transactions?")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, delete!"):
                    res = requests.delete(
                        f"{API_URL}/transactions/all"
                    )

                    if res.status_code == 200:
                        st.success("Transactions deleted")
                        st.cache_data.clear()
                        st.session_state.confirm_delete = False
                    else:
                        st.error(f"Delete failed: {res.text}")

            with col2:
                if st.button("Cancel"):
                    st.session_state.confirm_delete = False