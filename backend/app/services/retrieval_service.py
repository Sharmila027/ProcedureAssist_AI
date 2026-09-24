import chromadb
from sentence_transformers import SentenceTransformer


class RetrievalService:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="government_procedures"
        )

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def search(self, query: str, limit: int = 3):

        query_embedding = self.embedding_model.encode(
            query
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit
        )

        services = []

        if not results["documents"]:
            return services

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):
            services.append({
                "document": document,
                "metadata": metadata,
                "distance": distance
            })

        return services