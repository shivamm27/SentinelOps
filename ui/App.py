import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

st.set_page_config(page_title="SentinelOps", layout="wide")

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align:center; font-size:60px;'>🛡️ SentinelOps AI Monitoring Platform</h1>
<p style='text-align:center; font-size:20px; color:gray;'>
Predict • Detect • Prevent System Failures
</p>
""", unsafe_allow_html=True)

# ---------- DB ----------
url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Shiv@m2727",
    host="localhost",
    port=5432,
    database="sentinelops"
)

engine = create_engine(url)

metrics = pd.read_sql("SELECT * FROM system_metrics", engine)
alerts = pd.read_sql("SELECT * FROM system_alerts", engine)

# ---------- KPIs ----------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(metrics))
col2.metric("Total Alerts", len(alerts))
col3.metric("Avg CPU", round(metrics["cpu_usage"].mean(),2))
col4.metric("Avg Memory", round(metrics["memory_usage"].mean(),2))

st.divider()

# ---------- STATUS PANEL ----------
health = 100 - (
    metrics["cpu_usage"].iloc[-1]*0.4 +
    metrics["memory_usage"].iloc[-1]*0.4 +
    metrics["disk_usage"].iloc[-1]*0.2
)

if health > 70:
    st.success("🟢 System Running Normally")
elif health > 40:
    st.warning("🟡 Performance Degradation Detected")
else:
    st.error("🔴 Critical System State")

st.divider()

# ---------- FEATURE GRID ----------
c1, c2, c3 = st.columns(3)

with c1:
    st.info("📊 Real-Time Monitoring")

with c2:
    st.info("🤖 AI Failure Prediction")

with c3:
    st.info("🚨 Smart Alert Engine")

st.markdown("---")
st.caption("SentinelOps © AI System Monitoring Platform")