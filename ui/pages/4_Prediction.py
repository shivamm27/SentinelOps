import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA

st.title("🔮 Failure Prediction")

metrics = pd.read_csv("data/metrics.csv")

cpu = metrics["cpu_usage"]

model = ARIMA(cpu, order=(3,1,2))
fit = model.fit()

forecast = fit.forecast(steps=10)

risk = forecast.mean()

st.metric("Predicted CPU Load", round(risk,2))

if risk > 80:
    st.error("High Failure Risk")
elif risk > 60:
    st.warning("Moderate Risk")
else:
    st.success("System Safe")

fig = px.line(y=cpu, title="CPU Forecast")

fig.add_scatter(
    x=range(len(cpu), len(cpu)+10),
    y=forecast,
    mode="lines",
    name="Forecast"
)

st.plotly_chart(fig, use_container_width=True)