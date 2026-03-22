import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 System Overview")

metrics = pd.read_csv("data/metrics.csv")

col1, col2, col3 = st.columns(3)

col1.metric("Latest CPU", f"{metrics['cpu_usage'].iloc[-1]:.2f}%")
col2.metric("Latest Memory", f"{metrics['memory_usage'].iloc[-1]:.2f}%")
col3.metric("Latest Disk", f"{metrics['disk_usage'].iloc[-1]:.2f}%")

fig = px.line(
    metrics,
    x="timestamp",
    y=["cpu_usage","memory_usage","disk_usage"],
    title="System Resource Usage"
)

st.plotly_chart(fig, use_container_width=True)