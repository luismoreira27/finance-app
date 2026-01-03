import requests
import streamlit as st
import pandas as pd

API_URL = "http://127.0.0.1:8000"

@st.cache_data
def load_data():
    r = requests.get(f"{API_URL}/transactions/")
    if r.status_code != 200:
        st.error("Backend not running!")
        return pd.DataFrame()
    return pd.DataFrame(r.json())

@st.cache_data
def has_data():
    df = load_data()
    return not df.empty