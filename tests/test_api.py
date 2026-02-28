from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.api.main import app, generator

client = TestClient(app)

def test_read_main():
    # Mock the generator's response to avoid hitting the real OpenAI API
    # This replaces the real function with a fake one that returns a specific string
    generator.generate_response = MagicMock(return_value="This is a mocked response for testing.")
    
    response = client.post("/query", json={"query": "test query"})
    
    assert response.status_code == 200
    json_response = response.json()
    assert "answer" in json_response
    assert json_response["answer"] == "This is a mocked response for testing."

def test_ingest_endpoint_no_file():
    # This checks if the API correctly rejects a request without a file
    response = client.post("/ingest")
    assert response.status_code == 422