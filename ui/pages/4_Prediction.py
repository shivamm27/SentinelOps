import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA

st.title("🔮 Failure Prediction Engine")

metrics = pd.read_csv("data/metrics.csv")

cpu_series = metrics["cpu_usage"]

model = ARIMA(cpu_series, order=(3,1,2))
model_fit = model.fit()

forecast = model_fit.forecast(steps=10)

forecast_df = pd.DataFrame({
    "step": range(len(cpu_series), len(cpu_series)+10),
    "forecast_cpu": forecast
})

risk = forecast.mean()

st.metric("Predicted CPU Load", f"{risk:.2f}%")

if risk > 80:
    st.error("🔴 High Failure Risk Predicted")
elif risk > 60:
    st.warning("🟡 Moderate Risk")
else:
    st.success("🟢 System Stable")

fig = px.line(y=cpu_series, title="CPU Forecast")

fig.add_scatter(
    x=forecast_df["step"],
    y=forecast_df["forecast_cpu"],
    mode="lines",
    name="Forecast"
)

st.plotly_chart(fig, use_container_width=True)