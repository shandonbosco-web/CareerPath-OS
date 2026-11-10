"""Run after starting app.py. Sends parallel requests to the local API."""
from concurrent.futures import ThreadPoolExecutor
import requests

URL = "http://127.0.0.1:5000/api/recommend"
payloads = [
    {"name": f"Test Student {i}", "education": "Undergraduate",
     "interests": "technology coding data",
     "skills": ["python", "java", "sql"]}
    for i in range(1, 6)
]

def send(payload):
    response = requests.post(URL, json=payload, timeout=15)
    return response.status_code, response.json()

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=5) as pool:
        for result in pool.map(send, payloads):
            print(result)
