import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.title("📊 System Overview")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

metrics = pd.read_csv(DATA_DIR / "metrics.csv")

fig = px.line(metrics, x="timestamp", y=["cpu_usage","memory_usage","disk_usage"])
st.plotly_chart(fig, use_container_width=True)