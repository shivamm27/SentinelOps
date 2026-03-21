import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from config.db_config import DB_CONFIG


def fetch_metrics(limit=30):
    """
    Fetch last N system metric records from PostgreSQL
    using SQLAlchemy engine (safe for special characters)
    """

    # Build DB URL safely (handles special characters in password)
    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
    )

    engine = create_engine(db_url)

    query = """
        SELECT timestamp, cpu_usage, memory_usage, disk_usage
        FROM system_metrics
        ORDER BY timestamp DESC
        LIMIT %(limit)s
    """

    df = pd.read_sql(query, engine, params={"limit": limit})

    # Ensure correct time order
    return df.sort_values("timestamp")


def engineer_features(df):
    """
    Create engineered features from raw metrics
    """

    # Not enough data for rolling window
    if len(df) < 5:
        return pd.DataFrame()

    # Moving averages
    df["cpu_ma"] = df["cpu_usage"].rolling(window=5).mean()
    df["memory_ma"] = df["memory_usage"].rolling(window=5).mean()
    df["disk_ma"] = df["disk_usage"].rolling(window=5).mean()

    # Trend (rate of change)
    df["cpu_trend"] = df["cpu_usage"].diff()
    df["memory_trend"] = df["memory_usage"].diff()
    df["disk_trend"] = df["disk_usage"].diff()

    # Remove rows with NaN values
    df = df.dropna()

    return df


if __name__ == "__main__":
    df = fetch_metrics()
    df_features = engineer_features(df)

    print("Engineered Features:")
    print(df_features)
