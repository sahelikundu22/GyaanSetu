from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
import streamlit as st

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(chunks: List[str]) -> np.ndarray:
    """
    Convert a list of text chunks into a 2D numpy array of embeddings.
    Shape: (num_chunks, embedding_dim)
    """
    model = load_embedding_model()
    embeddings = model.encode(chunks, show_progress_bar=False, convert_to_numpy=True)
    return embeddings