import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# ---------- DATABASE CONNECTION ----------
url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Shiv@m2727",
    host="localhost",
    port=5432,
    database="sentinelops"
)

engine = create_engine(url)

# ---------- LOAD DATA ----------
df = pd.read_sql(
    "SELECT * FROM system_metrics ORDER BY timestamp",
    engine
)

# ---------- FEATURE SELECTION ----------
features = df[["cpu_usage", "memory_usage", "disk_usage"]]

# ---------- TRAIN MODEL ----------
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

model.fit(features)

# ---------- DETECT ANOMALIES ----------
df["anomaly"] = model.predict(features)

# convert: -1 = anomaly , 1 = normal
df["anomaly"] = df["anomaly"].map({1:0, -1:1})

# ---------- SAVE RESULT ----------
df.to_csv("anomaly_output.csv", index=False)

print("✅ Anomaly Detection Completed")
print(df.tail())