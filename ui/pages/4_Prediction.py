import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from pathlib import Path

st.title("🔮 Failure Prediction")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

metrics = pd.read_csv(DATA_DIR / "metrics.csv")

cpu_series = metrics["cpu_usage"]

model = ARIMA(cpu_series, order=(3,1,2))
model_fit = model.fit()

forecast_steps = 10
forecast = model_fit.forecast(steps=forecast_steps)

risk = forecast.mean()

st.metric("Predicted CPU", round(risk,2))

fig = go.Figure()

fig.add_trace(go.Scatter(y=cpu_series.tolist(), mode="lines", name="History"))

fig.add_trace(go.Scatter(
    x=list(range(len(cpu_series), len(cpu_series)+forecast_steps)),
    y=forecast.tolist(),
    mode="lines",
    name="Forecast"
))

st.plotly_chart(fig, use_container_width=True)