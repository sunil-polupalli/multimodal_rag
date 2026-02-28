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
        print(f"Created {SAMPLE_DIR}. Please add 10 PDF/Image files there.")
        return

    files = [f for f in os.listdir(SAMPLE_DIR) if f.lower().endswith(('.pdf', '.png', '.jpg'))]
    
    if not files:
        print("No files found. Please add test documents.")
        return
        
    print(f"Found {len(files)} documents.")
    
    # 1. Bulk Ingestion
    for filename in files:
        print(f"Ingesting {filename}...")
        try:
            with open(os.path.join(SAMPLE_DIR, filename), "rb") as f:
                requests.post(f"{BASE_URL}/ingest", files={"file": f})
        except Exception as e:
            print(f"Error: {e}")

    # 2. Query Test
    queries = ["Summarize the documents", "What data is in the charts?"]
    for q in queries:
        print(f"\nQuery: '{q}'")
        res = requests.post(f"{BASE_URL}/query", json={"query": q})
        if res.status_code == 200:
            print(f"Success. Sources found: {len(res.json().get('sources', []))}")
        else:
            print("Query Failed")

if __name__ == "__main__":
    evaluate_system()