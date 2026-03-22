import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

st.title("🤖 AI Analytics")

metrics = pd.read_csv("data/metrics.csv")

features = metrics[["cpu_usage","memory_usage","disk_usage"]]

model = IsolationForest(contamination=0.05, random_state=42)
metrics["anomaly"] = model.fit_predict(features)
metrics["anomaly"] = metrics["anomaly"].map({1:0,-1:1})

st.metric("Anomalies Detected", int(metrics["anomaly"].sum()))

fig = px.line(metrics, x="timestamp", y="cpu_usage", title="CPU Usage with Anomalies")

anom = metrics[metrics["anomaly"]==1]

fig.add_scatter(
    x=anom["timestamp"],
    y=anom["cpu_usage"],
    mode="markers",
    marker=dict(color="red", size=10),
    name="Anomaly"
)

st.plotly_chart(fig, use_container_width=True)