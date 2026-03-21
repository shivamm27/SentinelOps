import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

st.title("🏠 System Overview")

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
    "SELECT * FROM system_metrics ORDER BY timestamp DESC LIMIT 1",
    engine
)

cpu = df["cpu_usage"][0]
mem = df["memory_usage"][0]
disk = df["disk_usage"][0]

health = 100 - (cpu*0.4 + mem*0.4 + disk*0.2)

def gauge(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={'axis': {'range': [0,100]}}
    ))
    st.plotly_chart(fig, use_container_width=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    gauge(cpu, "CPU")

with col2:
    gauge(mem, "Memory")

with col3:
    gauge(disk, "Disk")

with col4:
    gauge(health, "Health Score")

# Status Badge
if health > 70:
    st.success("🟢 System Healthy")
elif health > 40:
    st.warning("🟡 System Warning")
else:
    st.error("🔴 System Critical")
