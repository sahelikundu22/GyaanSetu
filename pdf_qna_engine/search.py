from typing import List, Tuple
import numpy as np
import faiss
from pdf_qna_engine.model import load_embedding_model

# Global FAISS index and chunks
faiss_index = None
faiss_chunks = None
embedding_dim = 384  # all-MiniLM-L6-v2 output size

def build_faiss_index(chunks: List[str], embeddings: np.ndarray):
    """Build FAISS index from embeddings."""
    global faiss_index, faiss_chunks
    faiss_chunks = chunks
    faiss_index = faiss.IndexFlatIP(embedding_dim)  # cosine similarity
    faiss.normalize_L2(embeddings)
    faiss_index.add(embeddings.astype(np.float32))

def search_chunks(question: str, top_k: int = 2) -> Tuple[List[str], List[float]]:
    """Search top_k chunks for the question using FAISS."""
    global faiss_index, faiss_chunks
    if faiss_index is None or faiss_chunks is None:
        raise ValueError("FAISS index not built. Call build_faiss_index() first.")

    model = load_embedding_model()
    query_embedding = model.encode([question], convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)

    distances, indices = faiss_index.search(query_embedding.astype(np.float32), top_k)
    top_chunks = [faiss_chunks[i] for i in indices[0]]
    top_scores = [float(d) for d in distances[0]]
    return top_chunks, top_scores