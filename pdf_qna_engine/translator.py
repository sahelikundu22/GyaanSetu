import streamlit as st
import torch
from transformers import MBartTokenizer, AutoModelForSeq2SeqLM
from langdetect import detect

LANG_MAP = {
    "hi": "<2hi>",
    "bn": "<2bn>",
    "gu": "<2gu>",
    "ta": "<2ta>",
    "te": "<2te>",
    "mr": "<2mr>",
    "kn": "<2kn>",
    "ml": "<2ml>",
    "pa": "<2pa>",
    "or": "<2or>",
    "as": "<2as>",
    "en": "<2en>",
}

@st.cache_resource
def load_translation_model():
    tokenizer = MBartTokenizer.from_pretrained(
        "ai4bharat/IndicBART",
        do_lower_case=False,
        use_fast=False,
        keep_accents=True,
    )
    model = AutoModelForSeq2SeqLM.from_pretrained("ai4bharat/IndicBART")
    model.eval()
    return tokenizer, model

def detect_language(text: str) -> str:
    """Detect language of text, return langdetect code."""
    try:
        return detect(text[:500])
    except Exception:
        return "en"

def translate(text: str, src_lang: str, tgt_lang: str = "en") -> str:
    """Translate text from src_lang to tgt_lang using IndicBART."""
    tokenizer, model = load_translation_model()

    src_tag = LANG_MAP.get(src_lang)
    tgt_tag = LANG_MAP.get(tgt_lang, "<2en>")
    tgt_token_id = tokenizer.convert_tokens_to_ids(tgt_tag)

    if not src_tag:
        return text

    words = text.split()
    chunk_size = 200
    translated_parts = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        formatted = f"{src_tag} {chunk} </s> {tgt_tag}"

        inputs = tokenizer(
            formatted,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True,
        )

        with torch.no_grad():
            output = model.generate(
                input_ids=inputs.input_ids,
                attention_mask=inputs.attention_mask,
                num_beams=5,
                max_new_tokens=256,
                repetition_penalty=1.3,
                no_repeat_ngram_size=3,
                early_stopping=True,
                decoder_start_token_id=tgt_token_id,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
                bos_token_id=tokenizer.bos_token_id,
            )

        decoded = tokenizer.decode(output[0], skip_special_tokens=True)
        for tag in LANG_MAP.values():
            decoded = decoded.replace(tag, "")
        translated_parts.append(decoded.strip())

    return " ".join(translated_parts)

def translate_to_english_if_needed(text: str) -> tuple:
    """Detect language and translate to English if not already English."""
    lang = detect_language(text)
    if lang == "en":
        return text, "en"
    translated = translate(text, src_lang=lang, tgt_lang="en")
    return translated, lang
