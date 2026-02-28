from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
from dotenv import load_dotenv

from src.ingestion.document_parser import DocumentParser
from src.embeddings.model_loader import EmbeddingModel
from src.vector_store.manager import VectorStoreManager
from src.retrieval.retriever import Retriever
from src.generation.generator import Generator

load_dotenv()

app = FastAPI(title="Multimodal RAG API")

parser = DocumentParser()
embedding_model = EmbeddingModel()
vector_store = VectorStoreManager()
retriever = Retriever(vector_store, embedding_model)
generator = Generator()

class QueryRequest(BaseModel):
    query: str

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb+") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        if file.filename.lower().endswith(".pdf"):
            extracted_items = parser.parse_pdf(file_location)
        else:
            extracted_items = parser.process_image(file_location)

        for item in extracted_items:
            if item["type"] == "text":
                embedding = embedding_model.get_text_embedding(item["content"])
            else:
                embedding = embedding_model.get_image_embedding(item["content"])
            
            vector_store.add_item(embedding, item["content"], item["metadata"], item["type"])

        os.remove(file_location)
        return {"message": "Ingestion successful", "items_processed": len(extracted_items)}

    except Exception as e:
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_system(request: QueryRequest):
    try:
        retrieved_items = retriever.retrieve(request.query)
        answer = generator.generate_response(request.query, retrieved_items)
        
        sources = []
        for item in retrieved_items:
            sources.append({
                "source": item["metadata"]["source"],
                "page": item["metadata"]["page"],
                "type": item["type"]
            })

        return {
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)