import io
import numpy as np
import pdfplumber
import streamlit as st
from typing import List, Tuple
from sentence_transformers import SentenceTransformer


# ── Embedding Model ───────────────────────────────────────────────────────

@st.cache_resource
def load_embedding_model() -> SentenceTransformer:
    return SentenceTransformer("all-MiniLM-L6-v2")


# ── PDF Reader ────────────────────────────────────────────────────────────

def extract_text(pdf_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text.strip())
    return "\n\n".join(text_parts)


# ── Chunking ──────────────────────────────────────────────────────────────

def split_text(text: str, chunk_size: int = 150, overlap: int = 30) -> List[str]:
    if not text.strip():
        return []
    words  = text.split()
    chunks = []
    start  = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks


# ── Embeddings ────────────────────────────────────────────────────────────

def create_embeddings(chunks: List[str]) -> np.ndarray:
    model = load_embedding_model()
    return model.encode(chunks, show_progress_bar=False, convert_to_numpy=True)


# ── Full Pipeline (from bytes) ────────────────────────────────────────────

def process_pdf(pdf_bytes: bytes) -> Tuple[str, List[str], np.ndarray]:
    raw_text   = extract_text(pdf_bytes)
    chunks     = split_text(raw_text)
    embeddings = create_embeddings(chunks)
    return raw_text, chunks, embeddings


# ── Partial Pipeline (from text) ─────────────────────────────────────────

def process_text(text: str) -> Tuple[List[str], np.ndarray]:
    chunks     = split_text(text)
    embeddings = create_embeddings(chunks)
    return chunks, embeddings