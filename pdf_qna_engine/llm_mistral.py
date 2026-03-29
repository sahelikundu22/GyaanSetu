from typing import List, Tuple
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "cas/nous-hermes-2-mistral-7b-dpo"

def ask_model(
    question: str,
    contexts: List[str],
    chat_history: List[dict] = None,
    full_text: str = None,
) -> Tuple[str, float]:

    # Choose context (LIMITED)
    MAX_CHARS = 12000
    if full_text and len(full_text) <= MAX_CHARS:
        context = full_text
    else:
        context = "\n\n".join(contexts[:2])  # reduced from 5 → 2

    # Build history text
    history_text = ""
    if chat_history:
        for entry in chat_history[-4:]:
            history_text += f"User: {entry['question']}\nAssistant: {entry['answer']}\n"

    # Build prompt (Ollama style)
    prompt = f"""
You are a helpful assistant answering questions based on a PDF document.
Use only the information provided in the context.
Answer in 2-4 sentences.
If not found, say: "The document does not contain this information."

Context:
{context}

Conversation History:
{history_text}

Question:
{question}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.2,
                "num_predict": 150
            },
            timeout=180
        )

        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", "").strip()
            confidence = 0.0 if "does not contain" in answer.lower() else 90.0
            return answer if answer else "No answer generated.", confidence

        return f"API error {response.status_code}: {response.text}", 0.0

    except requests.exceptions.ConnectionError:
        return "Ollama is not running. Run: ollama run phi3", 0.0
    except requests.exceptions.Timeout:
        return "Request timed out. Reduce context size.", 0.0
    except Exception as e:
        return f"Error: {str(e)}", 0.0