"""
Embedding generation using sentence-transformers.
"""

import logging
from typing import Optional

import numpy as np

logger = logging.getLogger("ai_job_notifier")

# Lazy-loaded model to avoid startup cost
_model = None
_model_name = None


def _get_model(model_name: str = "all-MiniLM-L6-v2"):
    """Lazy-load the sentence-transformer model."""
    global _model, _model_name
    if _model is None or _model_name != model_name:
        from sentence_transformers import SentenceTransformer
        logger.info("Loading embedding model: %s", model_name)
        _model = SentenceTransformer(model_name)
        _model_name = model_name
    return _model


def create_embedding(
    text: str,
    model_name: str = "all-MiniLM-L6-v2",
) -> np.ndarray:
    """
    Generate an embedding vector for the given text.

    Args:
        text: Input text to embed.
        model_name: Sentence-transformers model name.

    Returns:
        numpy array of shape (embedding_dim,).
    """
    if not text or not text.strip():
        raise ValueError("Cannot create embedding for empty text")

    model = _get_model(model_name)
    embedding = model.encode(text, show_progress_bar=False, normalize_embeddings=True)
    return np.array(embedding, dtype=np.float32)


def create_batch_embeddings(
    texts: list[str],
    model_name: str = "all-MiniLM-L6-v2",
    batch_size: int = 32,
) -> np.ndarray:
    """
    Generate embeddings for a batch of texts.

    Returns:
        numpy array of shape (n_texts, embedding_dim).
    """
    if not texts:
        raise ValueError("Cannot create embeddings for empty text list")

    model = _get_model(model_name)
    embeddings = model.encode(
        texts,
        show_progress_bar=False,
        normalize_embeddings=True,
        batch_size=batch_size,
    )
    return np.array(embeddings, dtype=np.float32)
