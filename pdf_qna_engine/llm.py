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


def ask_model(
    question: str,
    contexts: List[str],
    chat_history: List[dict] = None,
    full_text: str = None,
) -> Tuple[str, float]:

    api_key = get_api_key()

    # Use full text for small PDFs, chunks for large ones
    MAX_CHARS = 12000
    if full_text and len(full_text) <= MAX_CHARS:
        context = full_text
    else:
        context = "\n\n".join(contexts[:5])

    system_prompt = f"""You are a helpful assistant answering questions based on a PDF document.
Use only the information provided in the context below.
Give a clear, complete, and accurate answer in 2-4 sentences.
Include relevant details from the context.
If the answer is not in the context, say "The document does not contain this information."
Remember the conversation history and use it to understand follow-up questions.

Context from PDF:
{context}"""

    messages = [{"role": "system", "content": system_prompt}]

    if chat_history:
        for entry in chat_history[-6:]:
            messages.append({"role": "user",      "content": entry["question"]})
            messages.append({"role": "assistant",  "content": entry["answer"]})

    messages.append({"role": "user", "content": question})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "max_tokens": 300,
        "temperature": 0.3,
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    response.raise_for_status()

    data       = response.json()
    answer     = data["choices"][0]["message"]["content"].strip()
    confidence = 0.0 if "does not contain" in answer.lower() else 95.0

    return answer, confidence