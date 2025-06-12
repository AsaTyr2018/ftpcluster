import os
import time
import requests
import psutil

MASTER_URL = os.environ.get('MASTER_URL', 'http://localhost:8080')
SERVER_ALIAS = os.environ.get('SERVER_ALIAS', 'unknown')


def send_telemetry():
    mem = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent(interval=0.5)
    users = len(psutil.users())
    storage = psutil.disk_usage("/").percent
    payload = {
        "alias": SERVER_ALIAS,
        "mem_percent": int(mem),
        "cpu_percent": int(cpu),
        "user_count": users,
        "storage_percent": int(storage),
    }
    try:
        requests.post(f"{MASTER_URL}/telemetry", json=payload)
    except Exception:
        pass


def main():
    while True:
        send_telemetry()
        time.sleep(60)


if __name__ == '__main__':
    main()
