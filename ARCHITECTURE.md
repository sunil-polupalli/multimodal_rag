# System Architecture

## Overview
This Multimodal RAG system allows users to query a knowledge base consisting of PDFs and images. It uses a decoupled pipeline approach involving Ingestion, Embedding, Indexing, Retrieval, and Generation.

## Components

### 1. Ingestion Layer
- **Tools**: PyMuPDF (Fitz), Pytesseract
- **Function**: Extracts text chunks and embedded images from PDFs. Performs OCR on extracted images to capture text embedded within visuals.

### 2. Embedding Layer
- **Model**: CLIP (via `sentence-transformers`)
- **Function**: Generates vector embeddings for both text and images in a shared semantic space, enabling cross-modal retrieval.

### 3. Vector Store
- **Database**: Local JSON/NumPy Store (Custom Implementation)
- **Choice Rationale**: A lightweight, file-based vector store was implemented to ensure strict compatibility with the Python 3.14 runtime environment, removing complex C++ dependencies while maintaining fast cosine similarity search via NumPy.
- **Function**: Persists embeddings and rich metadata (source document, page number, content type).

### 4. Retrieval Layer
- **Strategy**: Cosine Similarity Search.
- **Function**: Retrieves the top-k most relevant items (text or image) based on the user's query embedding.

### 5. Generation Layer
- **Model**: GPT-4o (Vision) / Mock Diagnostic (Demo Mode)
- **Function**: Synthesizes the final answer using retrieved text and images. In Demo Mode, it provides a retrieval validation report.