import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🚨 Alert Monitoring Console")

alerts = pd.read_csv("data/alerts.csv")

col1, col2 = st.columns(2)

col1.metric("Total Alerts", len(alerts))
col2.metric("Latest Alert Level", alerts["alert_level"].iloc[-1])

trend = alerts.groupby("timestamp").size().reset_index(name="count")

fig = px.line(trend, x="timestamp", y="count", title="Alert Frequency Trend")

st.plotly_chart(fig, use_container_width=True)

level = st.selectbox("Filter by Severity", ["ALL","WARNING","CRITICAL"])

if level != "ALL":
    alerts = alerts[alerts["alert_level"] == level]

st.dataframe(alerts, use_container_width=True)