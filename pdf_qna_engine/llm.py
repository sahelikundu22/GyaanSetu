from typing import List, Tuple
import torch
import math
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

@st.cache_resource
def load_qa_model():
    model_name = "google/flan-t5-large"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.eval()
    return tokenizer, model

def ask_model(question: str, contexts: List[str]) -> Tuple[str, float]:
    tokenizer, model = load_qa_model()

    best_answer = ""
    best_score = -float("inf")

    for chunk in contexts:
        if not chunk.strip():
            continue

        # Simple, clean prompt — flan-t5 works best with minimal instructions
        prompt = f"""Context: {chunk}

Question: {question}

Based on the context, provide a detailed answer in multiple sentences:"""

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024,
            padding=True,
        )

        with torch.no_grad():
            outputs = model.generate(
                input_ids=inputs.input_ids,
                attention_mask=inputs.attention_mask,
                max_new_tokens=150,
                min_new_tokens=30,
                num_beams=3,           # reduced from 5 — faster
                early_stopping=True,
                no_repeat_ngram_size=2,
                repetition_penalty=1.2,
                length_penalty=1.5,
                output_scores=True,
                return_dict_in_generate=True,
            )

        answer = tokenizer.decode(
            outputs.sequences[0], skip_special_tokens=True
        ).strip()

        # Clean up any prompt leakage
        for phrase in [
            "Based on the context,",
            "provide a detailed answer in multiple sentences:",
            "Context:",
            "Question:",
        ]:
            answer = answer.replace(phrase, "").strip()

        score = outputs.sequences_scores[0].item() if outputs.sequences_scores is not None else 0.0

        if (
            answer
            and len(answer.split()) > 5
            and "does not contain" not in answer.lower()
            and score > best_score
        ):
            best_score = score
            best_answer = answer

    if not best_answer:
        return "❌ The document does not contain information about this. Try rephrasing.", 0.0

    confidence = round(min(max(math.exp(best_score) * 100, 1.0), 99.0), 1)

    return best_answer, confidence