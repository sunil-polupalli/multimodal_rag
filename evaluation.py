import requests
import json
import os
import time

BASE_URL = "http://localhost:8000"
SAMPLE_DIR = "sample_documents"

def evaluate_system():
    print(f"--- Starting System Evaluation on {SAMPLE_DIR} ---")
    
    if not os.path.exists(SAMPLE_DIR):
        os.makedirs(SAMPLE_DIR)
        print(f"Created {SAMPLE_DIR}. Please add PDF files there.")
        return

    files = [f for f in os.listdir(SAMPLE_DIR) if f.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg'))]
    
    if not files:
        print("No files found to ingest. Skipping ingestion test.")
    else:
        print(f"Found {len(files)} documents.")
        
        # 1. Bulk Ingestion Test
        for filename in files:
            file_path = os.path.join(SAMPLE_DIR, filename)
            print(f"Ingesting {filename}...")
            start = time.time()
            try:
                with open(file_path, "rb") as f:
                    response = requests.post(f"{BASE_URL}/ingest", files={"file": f})
                    if response.status_code == 200:
                        print(f" - Success ({time.time() - start:.2f}s): {response.json()}")
                    else:
                        print(f" - Failed: {response.text}")
            except Exception as e:
                print(f" - Error: {e}")

    # 2. Query Test
    queries = [
        "Summarize the key points.",
        "What data is shown in the charts?",
        "Explain the main concept."
    ]
    
    print("\n--- Running Query Evaluation ---")
    for q in queries:
        print(f"Query: '{q}'")
        start = time.time()
        try:
            response = requests.post(f"{BASE_URL}/query", json={"query": q})
            if response.status_code == 200:
                data = response.json()
                print(f" - Latency: {time.time() - start:.2f}s")
                print(f" - Sources Retrieved: {len(data.get('sources', []))}")
                print(f" - Answer Preview: {data.get('answer', '')[:100]}...")
            else:
                print(f" - Failed: {response.text}")
        except Exception as e:
            print(f" - Error: {e}")

if __name__ == "__main__":
    evaluate_system()