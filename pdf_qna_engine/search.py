from typing import List
import numpy as np
from pdf_qna_engine.embeddings import load_embedding_model

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between vector a and each row of matrix b."""
    a_norm = a / (np.linalg.norm(a) + 1e-10)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-10)
    return b_norm @ a_norm

def search_chunks(
    question: str,
    chunks: List[str],
    embeddings: np.ndarray,
    top_k: int = 5
) -> List[str]:
    """
    Return the top_k most semantically relevant chunks for the given question.
    """
    model = load_embedding_model()
    query_embedding = model.encode([question], convert_to_numpy=True)[0]
    scores = cosine_similarity(query_embedding, embeddings)
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [chunks[i] for i in top_indices]