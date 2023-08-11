import sys
import requests

# first run the service locally: serve run qa_serve:deployment
question = sys.argv[1]
response = requests.post(
    "http://127.0.0.1:8000/question", params={"question": question}
)
print(response.content.decode())