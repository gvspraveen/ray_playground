import sys
import requests

prompt = sys.argv[1]

response = requests.post(
    "http://127.0.0.1:8000/query", params={"prompt": prompt}
)

# response = requests.post(f"http://localhost:8000/query?prompt={prompt}")
print(response.content.decode())