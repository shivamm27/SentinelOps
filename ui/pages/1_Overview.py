import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 System Overview")

metrics = pd.read_csv("data/metrics.csv")

fig = px.line(
    metrics,
    x="timestamp",
    y=["cpu_usage","memory_usage","disk_usage"],
    title="Resource Usage Trend"
)

st.plotly_chart(fig, use_container_width=True)