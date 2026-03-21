# SentinelOps

SentinelOps is a predictive system health monitoring tool that collects
system-level metrics, analyzes historical trends, computes a health score,
generates early warnings, and visualizes system behavior over time.

## Features
- Real-time CPU, memory, and disk monitoring
- PostgreSQL-based persistent storage
- Time-series feature engineering
- Health score calculation
- Predictive alert generation
- Historical visualization of metrics and health

## Technology Stack
- Python
- PostgreSQL
- psutil(used to get information about system resources and running processes)
- SQLAlchemy(work with databases in Python)
- Pandas
- Matplotlib

## How to Run

1. Install dependencies

   pip install -r requirements.txt

2. Run the monitoring pipeline:

python main.py


3. Visualize metrics and health:

python -m dashboard.visualize


## 🔹 STEP 3 — Final Project Structure (MEMORIZE THIS)

You should now have:

SentinelOps/
│
├── collector/
│ └── metrics_collector.py
│
├── analysis/
│ └── feature_engineering.py
│
├── prediction/
│ └── health_predictor.py
│
├── alerts/
│ └── alert_engine.py
│
├── dashboard/
│ └── visualize.py
│
├── config/
│ └── db_config.py
│
├── database/
│ └── init_db.sql
│
├── main.py
├── requirements.txt
└── README.md

## 🔹 STEP 4 — FINAL RUN CHECKLIST (VERY IMPORTANT)

Before submission or demo, always do this:

python main.py
python main.py
python main.py
python -m dashboard.visualize
