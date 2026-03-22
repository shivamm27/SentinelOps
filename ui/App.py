import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from login import login

st.set_page_config(page_title="SentinelOps", layout="wide")

# ---------- LOGIN ----------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ---------- LOGOUT ----------
st.sidebar.title("SentinelOps")
if st.sidebar.button("🚪 Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

# ---------- DYNAMIC PATH ----------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

metrics = pd.read_csv(DATA_DIR / "metrics.csv")
alerts = pd.read_csv(DATA_DIR / "alerts.csv")

# ---------- HERO ----------
st.markdown("<h1 style='text-align:center;'>🛡️ SentinelOps</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>AI Predictive Monitoring Platform</p>", unsafe_allow_html=True)

col1,col2,col3,col4 = st.columns(4)
col1.metric("Records", len(metrics))
col2.metric("Alerts", len(alerts))
col3.metric("Avg CPU", round(metrics["cpu_usage"].mean(),2))
col4.metric("Avg Memory", round(metrics["memory_usage"].mean(),2))

st.divider()

cpu = metrics["cpu_usage"].iloc[-1]
mem = metrics["memory_usage"].iloc[-1]
disk = metrics["disk_usage"].iloc[-1]

health = 100 - (cpu*0.4 + mem*0.4 + disk*0.2)

fig = px.pie(names=["Healthy","Used"], values=[health,100-health], hole=0.6)
st.plotly_chart(fig, use_container_width=True)