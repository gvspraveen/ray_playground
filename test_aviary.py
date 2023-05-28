import requests
import time
import argparse

TOTAL_RUN_TIME = 1 * 60
TARGET_QPS = 1
post_body = {
    "data":[
        "explain gravity to a first grade student",
        "CarperAI/stable-vicuna-13b-delta",
        "OpenAssistant/oasst-sft-7-llama-30b-xor",
        "mosaicml/mpt-7b-chat",null
    ],
    "fn_index":9,
    "session_hash":"2q30p62xajq"
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", nargs="?", default="https://aviary-staging.anyscale.com/run/predict")
    args = parser.parse_args()

    host = args.host
    
    last_fetched_at = 0
    start_time = time.time()
    while time.time() - start_time < TOTAL_RUN_TIME:
        now = time.monotonic()
        if now - last_fetched_at > (1 / TARGET_QPS):
            resp = requests.post(host, json=post_body)
            last_fetched_at = now
            if resp.status_code == 200:
                print("Got 200 response: ", resp.json())
            else:
                print(f"Error fetching: [{resp.status_code}] {resp.text}")
        # after = time.monotonic()
        # time.sleep(max(0, 0.05 - (after - now)))
