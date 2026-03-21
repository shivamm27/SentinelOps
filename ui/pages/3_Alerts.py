import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

st.title("🚨 Alert Monitoring Console")

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Shiv@m2727",
    host="localhost",
    port=5432,
    database="sentinelops"
)

engine = create_engine(url)

alerts = pd.read_sql(
    "SELECT * FROM system_alerts ORDER BY timestamp",
    engine
)

# ---------- KPI CARDS ----------
col1, col2 = st.columns(2)
col1.metric("Total Alerts", len(alerts))
col2.metric("Latest Alert Level", alerts["alert_level"].iloc[-1])

st.divider()

# ---------- ALERT TREND ----------
trend = alerts.groupby("timestamp").size().reset_index(name="count")
fig = px.line(trend, x="timestamp", y="count", title="Alert Frequency Trend")
st.plotly_chart(fig, use_container_width=True)

# ---------- FILTER ----------
level = st.selectbox("Filter by Severity", ["ALL","WARNING","CRITICAL"])

if level != "ALL":
    alerts = alerts[alerts["alert_level"] == level]

# ---------- COLORED TABLE ----------
def highlight(row):
    if row.alert_level == "CRITICAL":
        return ['background-color: red']*len(row)
    elif row.alert_level == "WARNING":
        return ['background-color: orange']*len(row)
    return ['']*len(row)

st.dataframe(alerts.style.apply(highlight, axis=1), use_container_width=True)