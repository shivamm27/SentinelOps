import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-GUI backend (no Tkinter)
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from config.db_config import DB_CONFIG


def get_engine():
    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
    )
    return create_engine(db_url)


def fetch_metrics():
    engine = get_engine()
    query = """
        SELECT timestamp, cpu_usage, memory_usage
        FROM system_metrics
        ORDER BY timestamp
    """
    return pd.read_sql(query, engine)


def fetch_health_scores():
    engine = get_engine()
    query = """
        SELECT timestamp, health_score
        FROM system_health
        ORDER BY timestamp
    """
    return pd.read_sql(query, engine)


def visualize():
    metrics_df = fetch_metrics()
    health_df = fetch_health_scores()

    if metrics_df.empty or health_df.empty:
        print("Not enough data to visualize.")
        return

    fig, axes = plt.subplots(2, 1, figsize=(10, 8))

    # CPU & Memory
    axes[0].plot(metrics_df["timestamp"], metrics_df["cpu_usage"], label="CPU Usage (%)")
    axes[0].plot(metrics_df["timestamp"], metrics_df["memory_usage"], label="Memory Usage (%)")
    axes[0].set_title("CPU and Memory Usage Over Time")
    axes[0].set_ylabel("Usage (%)")
    axes[0].legend()
    axes[0].tick_params(axis="x", rotation=45)

    # Health Score
    axes[1].plot(health_df["timestamp"], health_df["health_score"], label="Health Score", color="green")
    axes[1].set_title("System Health Score Over Time")
    axes[1].set_ylabel("Health Score")
    axes[1].set_xlabel("Time")
    axes[1].legend()
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig("system_health_dashboard.png")
    print("Dashboard saved as system_health_dashboard.png")


if __name__ == "__main__":
    visualize()
