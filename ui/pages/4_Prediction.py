import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA

st.title("🔮 Failure Prediction")

metrics = pd.read_csv("../data/metrics.csv")

cpu_series = metrics["cpu_usage"]

# ---------- TRAIN MODEL ----------
model = ARIMA(cpu_series, order=(3,1,2))
model_fit = model.fit()

# ---------- FORECAST ----------
forecast_steps = 10
forecast = model_fit.forecast(steps=forecast_steps)

# Convert forecast to proper list
forecast_values = forecast.tolist()

# Create future index
future_index = list(range(len(cpu_series), len(cpu_series) + forecast_steps))

# ---------- RISK ----------
risk = sum(forecast_values) / len(forecast_values)

st.metric("Predicted CPU Load", round(risk,2))

if risk > 80:
    st.error("🔴 High Failure Risk")
elif risk > 60:
    st.warning("🟡 Moderate Risk")
else:
    st.success("🟢 System Safe")

# ---------- PLOT ----------
fig = go.Figure()

fig.add_trace(go.Scatter(
    y=cpu_series.tolist(),
    mode="lines",
    name="Historical CPU"
))

fig.add_trace(go.Scatter(
    x=future_index,
    y=forecast_values,
    mode="lines",
    name="Forecast CPU"
))

st.plotly_chart(fig, use_container_width=True)