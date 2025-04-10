from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings as ChromaSettings
from litellm import embedding
from config import settings

class ChromaManager:
    def __init__(self):
        # Initialize Chroma client
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_DIR,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Create collections for different content types
        self.topics = self.client.get_or_create_collection("topics")
        self.vocab = self.client.get_or_create_collection("vocabulary")
        self.monologues = self.client.get_or_create_collection("monologues")
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding using LiteLLM"""
        response = embedding(
            model=settings.EMBEDDING_MODEL,
            input=[text],
            api_key=settings.EMBEDDING_MODEL_API_KEY
        )
        return response.data[0].embedding
    
    def add_example(self, collection_name: str, text: str, metadata: Dict[str, Any]) -> str:
        """Add an example to specified collection"""
        collection = self.client.get_collection(collection_name)
        embeddings = [self._get_embedding(text)]
        
        collection.add(
            embeddings=embeddings,
            documents=[text],
            metadatas=[metadata],
            ids=[metadata.get("id", str(len(collection.get()["ids"]) + 1))]
        )
        return metadata["id"]
    
    def find_similar(self, collection_name: str, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Find similar examples in specified collection"""
        collection = self.client.get_collection(collection_name)
        query_embedding = [self._get_embedding(query)]
        
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        return [
            {"text": doc, "metadata": meta}
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]

    def get_recent_topics(self, n: int = 10) -> List[str]:
        """Get the n most recently added topics"""
        collection = self.client.get_collection("topics")
        try:
            results = collection.get()
            # Get unique topics from metadata, most recent first
            topics = []
            seen = set()
            for meta in reversed(results["metadatas"]):
                topic = meta.get("topic")
                if topic and topic not in seen:
                    topics.append(topic)
                    seen.add(topic)
                if len(topics) >= n:
                    break
            return topics
        except Exception as e:
            print(f"Failed to get recent topics: {e}")
            return []
