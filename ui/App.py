import streamlit as st
import pandas as pd
from login import login

st.set_page_config(page_title="SentinelOps", layout="wide")

# ---------- LOGIN CONTROL ----------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ---------- PREMIUM UI STYLE ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#020617,#0f172a);
    color:white;
}
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border-radius:15px;
    padding:20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
metrics = pd.read_csv("data/metrics.csv")
alerts = pd.read_csv("data/alerts.csv")

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align:center;font-size:55px;'>🛡️ SentinelOps</h1>
<p style='text-align:center;color:gray;font-size:20px;'>AI-Driven Predictive Monitoring Platform</p>
""", unsafe_allow_html=True)

# ---------- KPI CARDS ----------
col1,col2,col3,col4 = st.columns(4)

col1.metric("Records", len(metrics))
col2.metric("Alerts", len(alerts))
col3.metric("Avg CPU", round(metrics["cpu_usage"].mean(),2))
col4.metric("Avg Memory", round(metrics["memory_usage"].mean(),2))

st.divider()

# ---------- SYSTEM STATUS ----------
cpu = metrics["cpu_usage"].iloc[-1]
mem = metrics["memory_usage"].iloc[-1]
disk = metrics["disk_usage"].iloc[-1]

health = 100 - (cpu*0.4 + mem*0.4 + disk*0.2)

st.subheader("System Health Status")

if health > 70:
    st.success("🟢 System Stable")
elif health > 40:
    st.warning("🟡 Performance Degrading")
else:
    st.error("🔴 Critical State")

st.divider()

st.subheader("Recent Alerts")
st.dataframe(alerts.tail(10), use_container_width=True)