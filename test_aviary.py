import requests
import time
import argparse
import ray

TOTAL_RUN_TIME = 1 * 60. # Number of seconds to run
TARGET_QPS = 1
post_body = {
    "data":[
        "explain gravity to a first grade student",
        "amazon/LightGPT",
        "stabilityai/stablelm-tuned-alpha-7b",
        "mosaicml/mpt-7b-chat",
        None
    ],
    "fn_index":9,
    "session_hash":"2q30p62xajq"
}

@ray.remote
def scrape_task(host, data):
    start = time.time()
    resp = requests.post(host, json=post_body)
    end = time.time()

    if resp.status_code == 200:
        return "Got result in {0} seconds, Result is: {1}".format(end - start,resp.json())
    else:
        return "Error fetching in {0} seconds, Status is {}, Result is: {}".format(end-start, resp.status_code, resp.text)
        # print(f"Error fetching: [{resp.status_code}] {resp.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", nargs="?", default="https://aviary-staging.anyscale.com/run/predict")
    args = parser.parse_args()

    host = args.host
    
    last_fired_at = 0
    start_time = time.time()
    results = []
    while time.time() - start_time < TOTAL_RUN_TIME:
        now = time.monotonic()
        if now - last_fired_at > (1 / TARGET_QPS):
            results.append(scrape_task.remote(host, post_body))
            last_fired_at = now


    print(ray.get(results))

    
