from datetime import datetime
import psycopg2

from analysis.feature_engineering import fetch_metrics, engineer_features
from config.db_config import DB_CONFIG


def calculate_health_score(row):
    """
    Calculate overall system health score (0–100)
    based on weighted resource usage.
    """
    score = 100

    score -= row["cpu_usage"] * 0.4
    score -= row["memory_usage"] * 0.3
    score -= row["disk_usage"] * 0.3

    return max(0, round(float(score), 2))


def store_health_score(health_score):
    """
    Store calculated health score into PostgreSQL
    (ensure native Python type)
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO system_health (timestamp, health_score)
        VALUES (%s, %s)
        """,
        (datetime.now(), float(health_score)),
    )

    conn.commit()
    cursor.close()
    conn.close()


def predict_health():
    """
    Predict current system health using engineered features
    and store the result in the database.
    """
    df = fetch_metrics(limit=30)
    df_features = engineer_features(df)

    # Not enough data yet
    if df_features.empty:
        return None

    latest = df_features.iloc[-1]
    health_score = calculate_health_score(latest)

    # Persist health score safely
    store_health_score(health_score)

    return health_score


if __name__ == "__main__":
    health = predict_health()

    if health is None:
        print("Not enough data yet to calculate health score.")
    else:
        print(f"System Health Score stored successfully: {health}")
 