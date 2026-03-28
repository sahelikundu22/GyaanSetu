import faiss
import numpy as np
from typing import List, Tuple
from pdf_qna_engine.model import load_embedding_model

_faiss_index = None
_faiss_chunks = []

def build_faiss_index(chunks: List[str], embeddings: np.ndarray):
    """Builds a FAISS index from embeddings and stores chunks."""
    global _faiss_index, _faiss_chunks
    dim = embeddings.shape[1]
    _faiss_index = faiss.IndexFlatL2(dim)
    _faiss_index.add(embeddings)
    _faiss_chunks = chunks.copy()

def search_chunks(
    question: str,
    top_k: int = 5
) -> Tuple[List[str], List[float]]:
    """Search FAISS index for most similar chunks to the question."""
    global _faiss_index, _faiss_chunks
    if _faiss_index is None:
        raise ValueError("FAISS index not built. Call build_faiss_index() first.")

    model = load_embedding_model()
    query_embedding = model.encode([question], convert_to_numpy=True)
    D, I = _faiss_index.search(query_embedding, top_k)
    top_chunks = [_faiss_chunks[i] for i in I[0]]
    top_scores = [float(d) for d in D[0]]
    return top_chunks, top_scores