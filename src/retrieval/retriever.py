class Retriever:
    def __init__(self, vector_store, embedding_model):
        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def retrieve(self, query_text, top_k=5):
        query_embedding = self.embedding_model.get_text_embedding(query_text)
        results = self.vector_store.query(query_embedding, n_results=top_k)
        
        parsed_results = []
        if results['ids']:
            for i in range(len(results['ids'][0])):
                parsed_results.append({
                    "id": results['ids'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "type": results['metadatas'][0][i]["type"],
                    "content": results['metadatas'][0][i]["content_reference"]
                })
        
        return parsed_results