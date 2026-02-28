import json
import os
import numpy as np
import uuid

class ChromaManager:
    def __init__(self, persist_path="./vector_store.json"):
        self.persist_path = persist_path
        self.data = []
        if os.path.exists(self.persist_path):
            with open(self.persist_path, 'r') as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = []

    def add_item(self, embedding, content, metadata, item_type):
        doc_id = str(uuid.uuid4())
        metadata["type"] = item_type
        metadata["content_reference"] = content 
        
        record = {
            "id": doc_id,
            "embedding": embedding,
            "metadata": metadata,
            "content": content
        }
        self.data.append(record)
        self._save()

    def _save(self):
        with open(self.persist_path, 'w') as f:
            json.dump(self.data, f)

    def query(self, query_embedding, n_results=5):
        if not self.data:
            return {'ids': [[]], 'metadatas': [[]], 'documents': [[]]}
            
        # Convert to numpy for calculation
        # Ensure embeddings are lists of floats
        embeddings = np.array([d['embedding'] for d in self.data], dtype=np.float32)
        query = np.array(query_embedding, dtype=np.float32)
        
        # Cosine Similarity: (A . B) / (||A|| * ||B||)
        norm_embeddings = np.linalg.norm(embeddings, axis=1)
        norm_query = np.linalg.norm(query)
        
        # Handle zero division if norms are 0
        if norm_query == 0:
            return {'ids': [[]], 'metadatas': [[]], 'documents': [[]]}
            
        # Avoid division by zero in embeddings
        norm_embeddings[norm_embeddings == 0] = 1e-10
            
        similarities = np.dot(embeddings, query) / (norm_embeddings * norm_query)
        
        # Get top k indices
        # If we have fewer items than n_results, take all of them
        k = min(n_results, len(self.data))
        top_k_indices = np.argsort(similarities)[::-1][:k]
        
        # Format response to match what the Retriever expects (ChromaDB format)
        ids = [self.data[i]['id'] for i in top_k_indices]
        metadatas = [self.data[i]['metadata'] for i in top_k_indices]
        documents = [self.data[i]['content'] for i in top_k_indices]
        
        return {
            'ids': [ids],
            'metadatas': [metadatas],
            'documents': [documents]
        }