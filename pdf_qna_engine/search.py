from typing import List, Tuple
import numpy as np
from pdf_qna_engine.model import load_embedding_model


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_norm = a / (np.linalg.norm(a) + 1e-10)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-10)
    return b_norm @ a_norm


def search_chunks(
    question: str,
    chunks: List[str],
    embeddings: np.ndarray,
    top_k: int = 5
) -> Tuple[List[str], List[float]]:
    model           = load_embedding_model()
    query_embedding = model.encode([question], convert_to_numpy=True)[0]
    scores          = cosine_similarity(query_embedding, embeddings)
    top_indices     = np.argsort(scores)[::-1][:top_k]
    top_chunks      = [chunks[i] for i in top_indices]
    top_scores      = [round(float(scores[i]), 4) for i in top_indices]
    return top_chunks, top_scores