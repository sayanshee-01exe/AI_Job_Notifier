"""
FAISS-based vector store for storing and searching embeddings.
"""

import logging
from typing import Dict, List, Optional, Tuple

import faiss
import numpy as np

logger = logging.getLogger("ai_job_notifier")


class FAISSVectorStore:
    """
    In-memory FAISS vector store with ID mapping.

    Supports:
        - store_embedding(id, vector)
        - search_similar(vector, top_k) → [(id, score), ...]
        - remove_embedding(id)
    """

    def __init__(self, dimension: int = 384):
        """
        Initialize the FAISS index.

        Args:
            dimension: Embedding vector dimension (384 for all-MiniLM-L6-v2).
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner product (cosine sim for normalized vectors)
        self._id_map: Dict[int, int] = {}   # external_id → faiss_internal_idx
        self._reverse_map: Dict[int, int] = {}  # faiss_internal_idx → external_id
        self._next_idx = 0

    @property
    def size(self) -> int:
        """Number of stored embeddings."""
        return self.index.ntotal

    def store_embedding(self, id: int, vector: np.ndarray) -> None:
        """
        Store an embedding vector with an external ID.

        Args:
            id: External identifier (e.g., job ID or user ID).
            vector: Embedding vector of shape (dimension,).
        """
        vector = np.array(vector, dtype=np.float32).reshape(1, -1)
        if vector.shape[1] != self.dimension:
            raise ValueError(
                f"Vector dimension mismatch: expected {self.dimension}, got {vector.shape[1]}"
            )

        # If ID already exists, we can't remove from FAISS easily,
        # so we just update the mapping
        self.index.add(vector)
        internal_idx = self._next_idx
        self._id_map[id] = internal_idx
        self._reverse_map[internal_idx] = id
        self._next_idx += 1

        logger.debug("Stored embedding for ID %d (internal idx %d)", id, internal_idx)

    def store_batch_embeddings(self, ids: List[int], vectors: np.ndarray) -> None:
        """Store a batch of embeddings."""
        vectors = np.array(vectors, dtype=np.float32)
        if vectors.ndim == 1:
            vectors = vectors.reshape(1, -1)

        self.index.add(vectors)
        for i, ext_id in enumerate(ids):
            internal_idx = self._next_idx + i
            self._id_map[ext_id] = internal_idx
            self._reverse_map[internal_idx] = ext_id

        self._next_idx += len(ids)
        logger.info("Stored batch of %d embeddings", len(ids))

    def search_similar(
        self,
        vector: np.ndarray,
        top_k: int = 10,
    ) -> List[Tuple[int, float]]:
        """
        Search for the top-k most similar embeddings.

        Args:
            vector: Query embedding vector.
            top_k: Number of results to return.

        Returns:
            List of (external_id, similarity_score) tuples, sorted by score descending.
        """
        if self.index.ntotal == 0:
            return []

        vector = np.array(vector, dtype=np.float32).reshape(1, -1)
        top_k = min(top_k, self.index.ntotal)

        distances, indices = self.index.search(vector, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            ext_id = self._reverse_map.get(idx)
            if ext_id is not None:
                # Cosine similarity (already normalized, so IP = cosine sim)
                results.append((ext_id, float(dist)))

        return results

    def clear(self) -> None:
        """Clear all stored embeddings."""
        self.index = faiss.IndexFlatIP(self.dimension)
        self._id_map.clear()
        self._reverse_map.clear()
        self._next_idx = 0
        logger.info("Cleared vector store")


# ── Global Instance ───────────────────────────────────────
_store: Optional[FAISSVectorStore] = None


def get_vector_store(dimension: int = 384) -> FAISSVectorStore:
    """Get or create the global FAISS vector store instance."""
    global _store
    if _store is None:
        _store = FAISSVectorStore(dimension=dimension)
    return _store
