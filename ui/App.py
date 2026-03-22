import streamlit as st
import pandas as pd

st.set_page_config(page_title="SentinelOps", layout="wide")

# ---------- LOAD DATA ----------
metrics = pd.read_csv("data/metrics.csv")
alerts = pd.read_csv("data/alerts.csv")

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align:center;'>🛡️ SentinelOps AI Monitoring Platform</h1>
<p style='text-align:center; color:gray;'>Predict • Detect • Prevent Failures</p>
""", unsafe_allow_html=True)

# ---------- KPI CARDS ----------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(metrics))
col2.metric("Total Alerts", len(alerts))
col3.metric("Avg CPU", round(metrics["cpu_usage"].mean(),2))
col4.metric("Avg Memory", round(metrics["memory_usage"].mean(),2))

st.divider()

# ---------- HEALTH STATUS ----------
latest_cpu = metrics["cpu_usage"].iloc[-1]
latest_mem = metrics["memory_usage"].iloc[-1]
latest_disk = metrics["disk_usage"].iloc[-1]

health = 100 - (latest_cpu*0.4 + latest_mem*0.4 + latest_disk*0.2)

if health > 70:
    st.success("🟢 System Running Normally")
elif health > 40:
    st.warning("🟡 Performance Degradation Detected")
else:
    st.error("🔴 Critical System State")

st.divider()

st.subheader("Recent Alerts")
st.dataframe(alerts.tail(10), use_container_width=True)