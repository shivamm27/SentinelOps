import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sklearn.ensemble import IsolationForest

st.title("📊 AI System Analytics")

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Shiv@m2727",
    host="localhost",
    port=5432,
    database="sentinelops"
)

engine = create_engine(url)

df = pd.read_sql(
    "SELECT * FROM system_metrics ORDER BY timestamp",
    engine
)

features = df[["cpu_usage","memory_usage","disk_usage"]]

model = IsolationForest(contamination=0.05, random_state=42)
df["anomaly"] = model.fit_predict(features)
df["anomaly"] = df["anomaly"].map({1:0,-1:1})

# ----------- KPI CARD -------------
st.metric("Total Anomalies Detected", int(df["anomaly"].sum()))

# ----------- AI CHART -------------
fig = px.line(df, x="timestamp", y="cpu_usage", title="CPU Usage with Anomalies")

anomalies = df[df["anomaly"] == 1]

fig.add_scatter(
    x=anomalies["timestamp"],
    y=anomalies["cpu_usage"],
    mode="markers",
    marker=dict(color="red", size=10),
    name="Anomaly"
)

st.plotly_chart(fig, use_container_width=True)