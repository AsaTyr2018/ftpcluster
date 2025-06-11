import os
import time
import requests
import psutil

MASTER_URL = os.environ.get('MASTER_URL', 'http://localhost:8080')
SERVER_ALIAS = os.environ.get('SERVER_ALIAS', 'unknown')


def send_memory_usage():
    usage = psutil.virtual_memory().percent
    try:
        requests.post(f"{MASTER_URL}/telemetry", json={"alias": SERVER_ALIAS, "mem_percent": usage})
    except Exception:
        pass


def main():
    while True:
        send_memory_usage()
        time.sleep(60)


if __name__ == '__main__':
    main()
