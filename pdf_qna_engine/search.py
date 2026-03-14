import numpy as np
from pdf_qna_engine.embeddings import embed_query

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_chunks(question, chunks, embeddings, top_k=3):

    query_vector = embed_query(question)

    scores = []

    for i, vec in enumerate(embeddings):
        score = cosine_similarity(query_vector, vec)
        scores.append((score, chunks[i]))

    scores.sort(reverse=True)

    results = [chunk for _, chunk in scores[:top_k]]

    return results