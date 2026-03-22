import streamlit as st
import pandas as pd
from pathlib import Path

st.title("🚨 Alert Center")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

alerts = pd.read_csv(DATA_DIR / "alerts.csv")

level = st.selectbox("Filter", ["ALL","WARNING","CRITICAL"])

if level != "ALL":
    alerts = alerts[alerts["alert_level"] == level]

st.dataframe(alerts, use_container_width=True)