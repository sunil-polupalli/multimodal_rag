# 🧠 Multimodal Retrieval-Augmented Generation (RAG) System

## 📋 Overview

This project implements an advanced **Multimodal RAG System** capable of ingesting, understanding, and synthesizing information from complex documents containing both text and images. Unlike traditional text-only RAG systems, this solution utilizes **CLIP (Contrastive Language-Image Pre-Training)** to project text and visual data into a shared semantic vector space, allowing for cross-modal retrieval.

The system is exposed via a RESTful API built with **FastAPI**, enabling users to upload PDF documents or images and query them using natural language.

## ✨ Key Features

* **Multimodal Ingestion**: Supports parsing of PDF documents (extracting text and embedded images) and standalone image files.
* **Intelligent Chunking**: Preserves document structure by associating images with their source pages.
* **Shared Vector Space**: Uses `sentence-transformers/clip-ViT-B-32` to generate embeddings for both text and images, enabling semantic search across modalities.
* **Local Vector Store**: Implements a lightweight, persistent JSON/NumPy-based vector store for efficient similarity search (optimized for local testing and Python 3.14 compatibility).
* **Visual Grounding**: Retrieves exact source references (page numbers, image paths) to ground generated answers in specific document evidence.
* **Modular Architecture**: Decoupled pipelines for Ingestion, Embedding, Retrieval, and Generation.

---

## 🏗️ Architecture

The system follows a standard RAG pipeline adapted for multimodal data:

1. **Ingestion**: `PyMuPDF` extracts text blocks and renders images from PDFs.
2. **Embedding**: Text and Images are passed through the CLIP model to generate 512-dimensional vectors.
3. **Indexing**: Vectors and metadata (source, page, type) are stored in the local vector store.
4. **Retrieval**: User queries are embedded; Cosine Similarity is used to find the top-k most relevant text chunks or images.
5. **Generation**:
* **Production Mode**: Retrieved context is formatted and sent to GPT-4o (Vision) for answer synthesis.
* **Demo Mode (Current)**: Returns a structured diagnostic report validating the retrieval pipeline without incurring API costs.



---

## 📂 Project Structure

```text
multimodal_rag/
├── src/
│   ├── api/                 # FastAPI application entry point
│   ├── ingestion/           # PDF parsing and image extraction logic
│   ├── embeddings/          # CLIP model loader
│   ├── retrieval/           # Semantic search and ranking logic
│   ├── vector_store/        # Local vector database implementation
│   └── generation/          # LLM integration (OpenAI/Mock)
├── tests/                   # Automated integration and unit tests
├── sample_documents/        # Test files for ingestion
├── extracted_images/        # Storage for images extracted during ingestion
├── vector_store.json        # Persistent vector database file
├── requirements.txt         # Python dependencies
├── pytest.ini               # Test configuration
└── submission.yml           # Automated build/test instruction

```

---

## 🚀 Setup & Installation

### Prerequisites

* Python 3.10 or higher
* pip

### 1. Clone and Install Dependencies

Navigate to the project root and install the required packages:

```bash
pip install -r requirements.txt

```

### 2. Environment Configuration

Create a `.env` file in the root directory.

```bash
cp .env.example .env

```

**Note on API Keys:**

* **For Demo/Free Mode:** You do *not* need an OpenAI API key. The system will mock the generation step.
* **For Production Mode:** Add your key to `.env`: `OPENAI_API_KEY=sk-...`

### 3. Start the Server

Launch the FastAPI server using Uvicorn:

```bash
python -m src.api.main

```

*The API will be available at `http://localhost:8000`.*

---

## 🧪 Usage Guide

### 1. Ingest a Document

Upload a PDF to build the knowledge base.

**cURL:**

```bash
curl -X POST -F "file=@sample_documents/report.pdf" http://localhost:8000/ingest

```

**Response:**

```json
{
  "message": "Ingestion successful",
  "items_processed": 16
}

```

### 2. Query the Knowledge Base

Ask a question about the uploaded document.

**cURL:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"query": "What are the key trends in the chart?"}' http://localhost:8000/query

```

**Response (Demo Mode):**
The system will return the retrieved context references to prove the pipeline is working.

```json
{
  "answer": "**[FREE MODE] System Operational.**\nFound content in report.pdf (Page 3)...",
  "sources": [
    {
      "source": "report.pdf",
      "page": 3,
      "type": "image"
    },
    {
      "source": "report.pdf",
      "page": 3,
      "type": "text"
    }
  ]
}

```

---

## ⚙️ Configuration: Demo vs. Production

This project is currently submitted in **Demo Mode**.

| Feature | Demo Mode (Default) | Production Mode |
| --- | --- | --- |
| **Ingestion** | ✅ Real (PyMuPDF) | ✅ Real (PyMuPDF) |
| **Embeddings** | ✅ Real (CLIP) | ✅ Real (CLIP) |
| **Retrieval** | ✅ Real (Vector Search) | ✅ Real (Vector Search) |
| **Generation** | 🔹 **Mocked** (Diagnostic) | 🔹 **Real** (GPT-4o) |
| **Cost** | $0.00 | Requires OpenAI Credits |

**To enable Production Mode:**

1. Ensure you have a funded OpenAI API Key in `.env`.
2. Uncomment the OpenAI client code in `src/generation/generator.py`.

---

## ✅ Automated Testing

The project includes a comprehensive test suite using `pytest` to validate the ingestion, API endpoints, and internal logic.

**Run all tests:**

```bash
pytest tests/

```

