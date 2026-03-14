import streamlit as st
from sidebar import render_sidebar
from pdf_qna_engine.pdf_reader import extract_text
from pdf_qna_engine.chunking import split_text
from pdf_qna_engine.embeddings import create_embeddings
from pdf_qna_engine.search import search_chunks
from pdf_qna_engine.llm import ask_model
from pdf_qna_engine.translator import translate_to_english_if_needed, detect_language
from pdf_qna_engine.highlighter import find_highlight_coords
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
5. LLaMA 3.3 70B via Groq generates a complete, accurate answer.
6. The answer is highlighted in the PDF.
""")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "highlights" not in st.session_state:
    st.session_state.highlights = None

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    pdf_bytes = uploaded_file.getvalue()

    # ── 1. Process PDF ────────────────────────────────────────────────────
    file_id = uploaded_file.name + str(len(pdf_bytes))
    if st.session_state.get("file_id") != file_id:
        st.session_state.chat_history = []
        st.session_state.highlights = None

        with st.spinner("Extracting text..."):
            raw_text = extract_text(pdf_bytes)

        detected_lang = detect_language(raw_text)

        if detected_lang != "en":
            st.info(f"🌐 Detected language: **{detected_lang.upper()}** — translating using AI4Bharat IndicBART...")
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

    # ── 2. Layout ─────────────────────────────────────────────────────────
    col_pdf, col_chat = st.columns([1.2, 1])

    with col_pdf:
        st.subheader("PDF Preview")
        highlights = st.session_state.get("highlights")
        if highlights:
            annotations = [
                {
                    "page": h["page"],
                    "x": h["x0"],
                    "y": h["y0"],
                    "width": h["x1"] - h["x0"],
                    "height": h["y1"] - h["y0"],
                    "color": "yellow",
                }
                for h in highlights
            ]
            pdf_viewer(input=pdf_bytes, width=500, height=700, annotations=annotations)
        else:
            pdf_viewer(input=pdf_bytes, width=500, height=700)

    with col_chat:
        st.subheader("Chat")

        chat_container = st.container(height=500)
        with chat_container:
            if not st.session_state.chat_history:
                st.caption("Ask a question about the PDF to get started.")
            else:
                for entry in st.session_state.chat_history:
                    with st.chat_message("user"):
                        st.write(entry["question"])
                    with st.chat_message("assistant"):
                        st.write(entry["answer"])
                        st.caption(f"Confidence: {entry['confidence']}%")
                        if entry.get("highlight_page"):
                            st.caption(f"📌 Highlighted on page {entry['highlight_page']}")

        question = st.chat_input("Ask a question about the PDF...")

        if question:
            if "chunks" not in st.session_state:
                st.warning("PDF is still processing. Please wait.")
            else:
                with st.spinner("Thinking..."):
                    results = search_chunks(
                        question,
                        st.session_state.chunks,
                        st.session_state.embeddings,
                    )
                    answer, confidence = ask_model(question, results)  # no api_key needed
                    highlights = find_highlight_coords(pdf_bytes, answer)

                st.session_state.highlights = highlights
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": answer,
                    "confidence": confidence,
                    "highlight_page": highlights[0]["page"] if highlights else None,
                })
                st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat History"):
                st.session_state.chat_history = []
                st.session_state.highlights = None
                st.rerun()

else:
    st.info("👆 Upload a PDF to get started.")