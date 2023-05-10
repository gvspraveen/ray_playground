import sys

import requests

question = sys.argv[1]
response = requests.post(f"http://localhost:8000/?question={question}")
print(response.content.decode())