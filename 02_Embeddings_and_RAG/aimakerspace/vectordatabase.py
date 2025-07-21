import numpy as np
from collections import defaultdict
from typing import List, Tuple, Callable, Dict, Any, Optional
from aimakerspace.openai_utils.embedding import EmbeddingModel
import asyncio


def cosine_similarity(vector_a: np.array, vector_b: np.array) -> float:
    """Computes the cosine similarity between two vectors."""
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    return dot_product / (norm_a * norm_b)


def euclidean_distance(vector_a: np.array, vector_b: np.array) -> float:
    """Computes the Euclidean distance between two vectors (lower is more similar)."""
    return -np.linalg.norm(vector_a - vector_b)  # Negative for consistent sorting


def manhattan_distance(vector_a: np.array, vector_b: np.array) -> float:
    """Computes the Manhattan distance between two vectors (lower is more similar)."""
    return -np.sum(np.abs(vector_a - vector_b))  # Negative for consistent sorting


def dot_product_similarity(vector_a: np.array, vector_b: np.array) -> float:
    """Computes the dot product similarity between two vectors."""
    return np.dot(vector_a, vector_b)


def chebyshev_distance(vector_a: np.array, vector_b: np.array) -> float:
    """Computes the Chebyshev distance between two vectors (lower is more similar)."""
    return -np.max(np.abs(vector_a - vector_b))  # Negative for consistent sorting


# Distance metrics registry
DISTANCE_METRICS = {
    "cosine": cosine_similarity,
    "euclidean": euclidean_distance,
    "manhattan": manhattan_distance,
    "dot_product": dot_product_similarity,
    "chebyshev": chebyshev_distance,
}


class VectorDatabase:
    def __init__(self, embedding_model: EmbeddingModel = None):
        self.vectors = defaultdict(np.array)
        self.metadata = defaultdict(dict)  # Store metadata for each key
        self.embedding_model = embedding_model or EmbeddingModel()

    def insert(self, key: str, vector: np.array, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Insert a vector with optional metadata."""
        self.vectors[key] = vector
        if metadata:
            self.metadata[key] = metadata

    def search(
        self,
        query_vector: np.array,
        k: int,
        distance_measure: Callable = cosine_similarity,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Search for similar vectors with optional metadata filtering."""
        scores = []
        for key, vector in self.vectors.items():
            # Apply metadata filter if provided
            if metadata_filter and not self._matches_filter(self.metadata.get(key, {}), metadata_filter):
                continue
            
            score = distance_measure(query_vector, vector)
            metadata = self.metadata.get(key, {})
            scores.append((key, score, metadata))
        
        return sorted(scores, key=lambda x: x[1], reverse=True)[:k]

    def _matches_filter(self, item_metadata: Dict[str, Any], filter_criteria: Dict[str, Any]) -> bool:
        """Check if item metadata matches filter criteria."""
        for key, value in filter_criteria.items():
            if key not in item_metadata:
                return False
            if isinstance(value, list):
                # If filter value is a list, check if item value is in the list
                if item_metadata[key] not in value:
                    return False
            elif item_metadata[key] != value:
                return False
        return True

    def search_by_text(
        self,
        query_text: str,
        k: int,
        distance_measure: Callable = cosine_similarity,
        return_as_text: bool = False,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Search by text with optional metadata filtering."""
        query_vector = self.embedding_model.get_embedding(query_text)
        results = self.search(query_vector, k, distance_measure, metadata_filter)
        
        if return_as_text:
            return [result[0] for result in results]
        return results

    def search_by_distance_metric(
        self,
        query_text: str,
        k: int,
        metric_name: str = "cosine",
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Search using a named distance metric."""
        if metric_name not in DISTANCE_METRICS:
            raise ValueError(f"Unknown distance metric: {metric_name}. Available: {list(DISTANCE_METRICS.keys())}")
        
        distance_func = DISTANCE_METRICS[metric_name]
        return self.search_by_text(query_text, k, distance_func, metadata_filter=metadata_filter)

    def retrieve_from_key(self, key: str) -> Tuple[np.array, Dict[str, Any]]:
        """Retrieve vector and metadata for a given key."""
        vector = self.vectors.get(key, None)
        metadata = self.metadata.get(key, {})
        return vector, metadata

    def get_all_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Get all metadata in the database."""
        return dict(self.metadata)

    def filter_by_metadata(self, filter_criteria: Dict[str, Any]) -> List[str]:
        """Get all keys that match the metadata filter."""
        matching_keys = []
        for key, metadata in self.metadata.items():
            if self._matches_filter(metadata, filter_criteria):
                matching_keys.append(key)
        return matching_keys

    async def abuild_from_list(self, list_of_text: List[str]) -> "VectorDatabase":
        """Build database from list of texts (legacy method)."""
        embeddings = await self.embedding_model.async_get_embeddings(list_of_text)
        for text, embedding in zip(list_of_text, embeddings):
            self.insert(text, np.array(embedding))
        return self

    async def abuild_from_list_with_metadata(
        self, 
        texts_with_metadata: List[Tuple[str, Dict[str, Any]]]
    ) -> "VectorDatabase":
        """Build database from list of texts with metadata."""
        texts = [text for text, _ in texts_with_metadata]
        embeddings = await self.embedding_model.async_get_embeddings(texts)
        
        for (text, metadata), embedding in zip(texts_with_metadata, embeddings):
            self.insert(text, np.array(embedding), metadata)
        return self


if __name__ == "__main__":
    # Test the enhanced vector database
    list_of_text = [
        "I like to eat broccoli and bananas.",
        "I ate a banana and spinach smoothie for breakfast.", 
        "Chinchillas and kittens are cute.",
        "My sister adopted a kitten yesterday.",
        "Look at this cute hamster munching on a piece of broccoli.",
    ]

    # Test with metadata
    texts_with_metadata = [
        (text, {"category": "food" if any(word in text.lower() for word in ["eat", "banana", "broccoli", "smoothie"]) else "animals"})
        for text in list_of_text
    ]

    vector_db = VectorDatabase()
    vector_db = asyncio.run(vector_db.abuild_from_list_with_metadata(texts_with_metadata))
    
    # Test different distance metrics
    query = "I think fruit is awesome!"
    print("=== Testing Different Distance Metrics ===")
    for metric in DISTANCE_METRICS.keys():
        print(f"\n{metric.upper()} Results:")
        results = vector_db.search_by_distance_metric(query, k=2, metric_name=metric)
        for text, score, metadata in results:
            print(f"  Score: {score:.4f}, Category: {metadata.get('category', 'N/A')}")
            print(f"  Text: {text[:50]}...")
    
    # Test metadata filtering
    print("\n=== Testing Metadata Filtering ===")
    food_results = vector_db.search_by_text(query, k=5, metadata_filter={"category": "food"})
    print("Food-related results:")
    for text, score, metadata in food_results:
        print(f"  Score: {score:.4f}, Text: {text[:50]}...")

    # Test retrieving by key
    print("\n=== Testing Key Retrieval ===")
    first_text = list_of_text[0]
    vector, metadata = vector_db.retrieve_from_key(first_text)
    print(f"Retrieved vector shape: {vector.shape if vector is not None else 'None'}")
    print(f"Retrieved metadata: {metadata}")
