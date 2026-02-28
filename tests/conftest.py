import os
import sys

# Set a dummy API key so the OpenAI client doesn't crash during initialization
os.environ["OPENAI_API_KEY"] = "test-key-for-unit-testing"
os.environ["CHROMA_DB_PATH"] = "test_db"