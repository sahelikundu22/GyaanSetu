import requests
import streamlit as st

HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL      = "meta-llama/Llama-3.1-8B-Instruct"


def ask_model(question, chunks, chat_history=None, full_text=""):
    """
    Generate an answer using HuggingFace Router API.

    Args:
        question     : the student's question string
        chunks       : list of chunk text strings from search.py
        chat_history : list of {"question": ..., "answer": ...} dicts
        full_text    : full document text (used if under 12,000 chars)

    Returns:
        (answer string, confidence int)
    """
    if chat_history is None:
        chat_history = []

    try:
        hf_token = st.secrets["HF_TOKEN"]

        # Choose context
        if full_text and len(full_text) < 12000:
            context = full_text
        else:
            context = "\n\n".join(chunks) if chunks else ""

        # Build messages
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful educational assistant. "
                    "Answer only from the provided context in 2 to 4 complete sentences. "
                    "If the answer is not in the context, say so clearly.\n\n"
                    f"Context:\n{context}"
                )
            }
        ]

        # Append last 6 conversation turns for memory
        for turn in chat_history[-6:]:
            messages.append({"role": "user",      "content": turn["question"]})
            messages.append({"role": "assistant", "content": turn["answer"]})

        # Add current question
        messages.append({"role": "user", "content": question})

        headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type":  "application/json"
        }

        payload = {
            "model":       MODEL,
            "messages":    messages,
            "max_tokens":  300,
            "temperature": 0.3,
        }

        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)

        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"].strip()
            return (answer, 85) if answer else ("No answer generated.", 0)

        elif response.status_code == 503:
            return "Model is loading, please try again in a moment.", 0

        elif response.status_code == 429:
            return "Rate limit reached. Please wait a minute and try again.", 0

        return f"API error {response.status_code}: {response.text}", 0

    except KeyError:
        return "HF_TOKEN not found. Add HF_TOKEN = 'hf_...' to .streamlit/secrets.toml", 0
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again.", 0
    except Exception as e:
        return f"Error: {str(e)}", 0