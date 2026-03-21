import streamlit as st
import pandas as pd
import time
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

st.set_page_config(page_title="SentinelOps Dashboard", layout="wide")

st.title("🛡️ SentinelOps System Health Monitoring Dashboard")

# ---------- DATABASE CONNECTION ----------
url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Shiv@m2727",   # your password
    host="localhost",
    port=5432,
    database="sentinelops"
)

engine = create_engine(url)

# ---------- SIDEBAR ----------
st.sidebar.header("Controls")
refresh = st.sidebar.slider("Refresh Rate (seconds)", 2, 10, 5)

placeholder = st.empty()

# ---------- LIVE LOOP ----------
while True:

    # Load system metrics
    df = pd.read_sql(
        "SELECT * FROM system_metrics ORDER BY timestamp DESC LIMIT 50",
        engine
    )

    df = df.sort_values("timestamp")

    # Calculate Health Score dynamically
    df["health_score"] = 100 - (
        df["cpu_usage"] * 0.4 +
        df["memory_usage"] * 0.4 +
        df["disk_usage"] * 0.2
    )

    # Load alerts
    alerts = pd.read_sql(
        "SELECT * FROM system_alerts ORDER BY timestamp DESC LIMIT 5",
        engine
    )

    with placeholder.container():

        st.subheader("📊 Current System Status")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("CPU Usage", f"{df['cpu_usage'].iloc[-1]:.2f}%")
        col2.metric("Memory Usage", f"{df['memory_usage'].iloc[-1]:.2f}%")
        col3.metric("Disk Usage", f"{df['disk_usage'].iloc[-1]:.2f}%")
        col4.metric("Health Score", f"{df['health_score'].iloc[-1]:.2f}")

        st.subheader("📈 Live Resource Usage")
        st.line_chart(
            df.set_index("timestamp")[["cpu_usage", "memory_usage", "disk_usage"]]
        )

        st.subheader("❤️ Health Score Trend")
        st.line_chart(
            df.set_index("timestamp")["health_score"]
        )

        st.subheader("⚠️ Recent Alerts")
        st.dataframe(alerts, use_container_width=True)

    time.sleep(refresh)