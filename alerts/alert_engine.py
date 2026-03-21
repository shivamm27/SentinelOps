from datetime import datetime
import psycopg2

from prediction.health_predictor import predict_health
from config.db_config import DB_CONFIG


def store_alert(alert_level, message):
    """
    Store alert information into PostgreSQL
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO system_alerts (timestamp, alert_level, message)
        VALUES (%s, %s, %s)
        """,
        (datetime.now(), alert_level, message),
    )

    conn.commit()
    cursor.close()
    conn.close()


def generate_alert():
    """
    Generate alert based on current system health
    and store it in the database.
    """
    health = predict_health()

    # Not enough data yet
    if health is None:
        alert_level = "INFO"
        message = "Not enough data available to generate alerts."
        store_alert(alert_level, message)
        return {"level": alert_level, "message": message}

    # Determine alert level
    if health < 50:
        alert_level = "CRITICAL"
        message = (
            f"CRITICAL ALERT: System health is {health}. "
            f"Immediate action required."
        )
    elif health < 70:
        alert_level = "WARNING"
        message = (
            f"WARNING: System health is {health}. "
            f"Performance degradation detected."
        )
    else:
        alert_level = "NORMAL"
        message = (
            f"System health is {health}. "
            f"System operating normally."
        )

    # Store alert in database
    store_alert(alert_level, message)

    return {"level": alert_level, "message": message}


if __name__ == "__main__":
    alert = generate_alert()
    print(f"[{alert['level']}] {alert['message']}")
