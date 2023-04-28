import requests
import time
import argparse

TARGET_QPS = {
    "PEAR": 1,
    "MANGO": 1.5,
    "ORANGE": 4,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", nargs="?", default="http://localhost:8000")
    parser.add_argument("token", nargs="?")
    args = parser.parse_args()

    host = args.host
    token = args.token

    headers = {"Authorization": f"Bearer {token}"} if token else None

    last_fetched_at = {}
    while True:
        now = time.monotonic()
        for fruit, target in TARGET_QPS.items():
            last_fetched = last_fetched_at.get(fruit, 0)
            if now - last_fetched > (1 / target):
                resp = requests.post(host, data=f'["{fruit}", 5]', headers=headers)
                last_fetched_at[fruit] = now
                if resp.status_code < 400:
                    print("fetching for fruit: " + fruit)
                else:
                    print(f"Error fetching: [{resp.status_code}] {resp.text}")
        after = time.monotonic()
        time.sleep(max(0, 0.05 - (after - now)))
