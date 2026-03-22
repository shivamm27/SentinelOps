import streamlit as st
import pandas as pd

st.title("🚨 Alert Center")

alerts = pd.read_csv("data/alerts.csv")

level = st.selectbox("Filter Severity", ["ALL","WARNING","CRITICAL"])

if level != "ALL":
    alerts = alerts[alerts["alert_level"] == level]

st.dataframe(alerts, use_container_width=True)