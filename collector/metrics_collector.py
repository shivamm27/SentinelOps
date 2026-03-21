import psutil
import psycopg2
from datetime import datetime
from config.db_config import DB_CONFIG

def collect_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    return cpu_usage, memory_usage, disk_usage

def store_metrics(cpu, memory, disk):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO system_metrics (timestamp, cpu_usage, memory_usage, disk_usage)
        VALUES (%s, %s, %s, %s)
    """, (datetime.now(), cpu, memory, disk))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    cpu, memory, disk = collect_metrics()
    store_metrics(cpu, memory, disk)
    print("System metrics collected and stored successfully.")
