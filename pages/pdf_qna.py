import streamlit as st
import tempfile
import os

from sidebar import render_sidebar
from pdf_qna_engine.pdf_reader import extract_text
from pdf_qna_engine.chunking import split_text
from pdf_qna_engine.embeddings import create_embeddings
from pdf_qna_engine.search import search_chunks
from pdf_qna_engine.llm import ask_model
from pdf_qna_engine.translator import translate_to_english_if_needed, detect_language
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(page_title="PDF Q&A", page_icon="📄")

render_sidebar()

st.title("📄 PDF Q&A")

with st.expander("How it Works", expanded=False):
    st.write("""
Upload a PDF document and ask questions about its content.

Steps:
1. PDF text is extracted and language is auto-detected.
2. If non-English, AI4Bharat IndicBART translates it to English.
3. Text is split into chunks and converted to embeddings.
4. Relevant chunks are retrieved using semantic search.
5. Google Flan-T5 generates a complete answer.
""")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    pdf_bytes = uploaded_file.getvalue()

    st.subheader("PDF Preview")
    pdf_viewer(input=pdf_bytes, width=700, height=600)

    file_id = uploaded_file.name + str(len(pdf_bytes))
    if st.session_state.get("file_id") != file_id:

        # Clear previous answers when new PDF is uploaded
        for key in ["last_question", "last_answer", "last_confidence"]:
            st.session_state.pop(key, None)

        with st.spinner("Extracting text..."):
            raw_text = extract_text(pdf_bytes)

        detected_lang = detect_language(raw_text)

        if detected_lang != "en":
            st.info(f"🌐 Detected language: **{detected_lang.upper()}** — translating to English using AI4Bharat IndicBART...")
            with st.spinner("Translating PDF content..."):
                translated_text, _ = translate_to_english_if_needed(raw_text)
            st.success("✅ Translation complete!")
        else:
            st.info("🌐 Detected language: **English** — no translation needed.")
            translated_text = raw_text

        with st.spinner("Building search index..."):
            chunks = split_text(translated_text)
            embeddings = create_embeddings(chunks)
            st.session_state.chunks = chunks
            st.session_state.embeddings = embeddings
            st.session_state.detected_lang = detected_lang
            st.session_state.file_id = file_id

        st.success("✅ PDF processed and ready!")

    elif "detected_lang" in st.session_state:
        lang = st.session_state.detected_lang
        if lang != "en":
            st.info(f"🌐 PDF language: **{lang.upper()}** (translated to English)")
        else:
            st.info("🌐 PDF language: **English**")

    st.markdown("---")
    st.subheader("Ask a Question")

    question = st.text_input("Type your question about the PDF")

    if st.button("Get Answer"):
        if not question.strip():
            st.warning("Please enter a question.")
        elif "chunks" not in st.session_state:
            st.warning("PDF is still processing. Please wait.")
        else:
            with st.spinner("Finding answer..."):
                results = search_chunks(
                    question,
                    st.session_state.chunks,
                    st.session_state.embeddings,
                )
                answer, confidence = ask_model(question, results)

            st.session_state.last_question = question
            st.session_state.last_answer = answer
            st.session_state.last_confidence = confidence

    # Only show answer if it matches the current question
    if (
        "last_answer" in st.session_state
        and "last_question" in st.session_state
        and st.session_state.get("last_question") == question
    ):
        st.subheader("Answer")
        st.write(st.session_state.last_answer)
        st.caption(f"Confidence: {st.session_state.last_confidence}%")

else:
    st.info("👆 Upload a PDF to get started.")