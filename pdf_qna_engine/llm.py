from typing import List, Tuple
import requests
import streamlit as st

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_api_key() -> str:
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        st.error("❌ GROQ_API_KEY not found in .streamlit/secrets.toml")
        st.stop()

def ask_model(question: str, contexts: List[str]) -> Tuple[str, float]:
    api_key = get_api_key()
    context = "\n\n".join(contexts[:5])

    prompt = f"""You are a helpful assistant answering questions based on a PDF document.
Use only the information provided in the context below.
Give a clear, complete, and accurate answer in 2-4 sentences.
Include relevant details from the context.
If the answer is not in the context, say "The document does not contain this information."

Context:
{context}

Question: {question}"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.3,
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    answer = data["choices"][0]["message"]["content"].strip()
    confidence = 0.0 if "does not contain" in answer.lower() else 95.0

    return answer, confidence