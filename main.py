from collector.metrics_collector import collect_metrics, store_metrics
from alerts.alert_engine import generate_alert


def main():
    cpu, memory, disk = collect_metrics()
    store_metrics(cpu, memory, disk)

    alert = generate_alert()
    print(f"[{alert['level']}] {alert['message']}")


if __name__ == "__main__":
    main()
