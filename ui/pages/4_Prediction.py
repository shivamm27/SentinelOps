import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from statsmodels.tsa.arima.model import ARIMA

st.title("🤖 AI Failure Forecast Engine")

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
    "SELECT * FROM system_metrics ORDER BY timestamp",
    engine
)

cpu_series = df["cpu_usage"]

# -------- Train Forecast Model ----------
model = ARIMA(cpu_series, order=(3,1,2))
model_fit = model.fit()

# -------- Predict Next 10 Steps ----------
forecast = model_fit.forecast(steps=10)

forecast_df = pd.DataFrame({
    "timestamp": range(len(cpu_series), len(cpu_series)+10),
    "forecast_cpu": forecast
})

# -------- Risk Score ----------
risk = forecast.mean()

st.metric("Predicted CPU Load", f"{risk:.2f}%")

if risk > 80:
    st.error("🔴 High Failure Risk Predicted")
elif risk > 60:
    st.warning("🟡 Moderate Risk")
else:
    st.success("🟢 System Stable")

# -------- Plot ----------
fig = px.line(y=cpu_series, title="CPU Forecast")

fig.add_scatter(
    x=forecast_df["timestamp"],
    y=forecast_df["forecast_cpu"],
    mode="lines",
    name="Forecast"
)

st.plotly_chart(fig, use_container_width=True)

# -------- Recommendation Engine --------

st.subheader("🧠 AI Recommendations")

recent_anomalies = df.tail(20)["cpu_usage"].mean()

if risk > 80:
    st.error("Recommendation: Immediate resource scaling required.")
    st.write("• Possible CPU overload predicted")
    st.write("• Consider load balancing or instance upgrade")

elif risk > 60:
    st.warning("Recommendation: Monitor system closely.")
    st.write("• Rising CPU trend detected")
    st.write("• Check background services")

elif recent_anomalies > 70:
    st.warning("Recommendation: Memory / CPU spikes observed.")
    st.write("• Possible inefficient process running")

else:
    st.success("System operating within safe limits.")
    st.write("• No preventive action required")