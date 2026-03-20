import streamlit as st
from sidebar import render_sidebar
from pdf_qna_engine.search import search_chunks
from pdf_qna_engine.llm import ask_model
from pdf_qna_engine.highlighter import find_highlight_coords
from streamlit_pdf_viewer import pdf_viewer
from pdf_qna_engine.processor import extract_text, process_text

st.set_page_config(page_title="PDF Q&A", page_icon="📄", layout="wide")

render_sidebar()

st.title("📄 PDF Q&A")

with st.expander("How it Works", expanded=False):
    st.write("""
Upload a PDF document and ask questions about its content.
Supports all languages — ask in any language, get answers in the same language.

Steps:
1. PDF text is extracted.
2. Text is split into chunks and converted to embeddings.
3. Relevant chunks are retrieved using semantic search.
4. LLaMA 3.3 70B via Groq generates a complete, accurate answer.
5. The answer is highlighted and scrolled to in the PDF.
""")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "highlights" not in st.session_state:
    st.session_state.highlights = None

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    pdf_bytes = uploaded_file.getvalue()

    col_pdf, col_chat = st.columns([1.2, 1])

    with col_pdf:
        st.subheader("PDF Preview")

        highlights = st.session_state.get("highlights")
        if highlights:
            h = highlights[0]
            annotations = [{
                "page":   h["page"],
                "x":      h["x0"],
                "y":      h["y0"],
                "width":  h["x1"] - h["x0"],
                "height": h["y1"] - h["y0"],
                "color":  "yellow",
            }]
            pdf_viewer(
                input=pdf_bytes,
                width=500,
                height=700,
                annotations=annotations,
                scroll_to_page=h["page"],
            )
            st.caption(f"📌 Answer highlighted on **page {h['page']}**")
        else:
            pdf_viewer(input=pdf_bytes, width=500, height=700)

    with col_chat:
        st.subheader("Chat")

        # Process PDF once per upload 
        file_id = uploaded_file.name + str(len(pdf_bytes))
        if st.session_state.get("file_id") != file_id:
            st.session_state.chat_history = []
            st.session_state.highlights   = None

            with st.spinner("Processing PDF..."):
                raw_text           = extract_text(uploaded_file)
                chunks, embeddings = process_text(raw_text)

            st.session_state.raw_text     = raw_text
            st.session_state.chunks       = chunks
            st.session_state.embeddings   = embeddings
            st.session_state.file_id      = file_id
            st.session_state.total_chunks = len(chunks)

            st.success(f"✅ PDF processed — {len(chunks)} chunks created.")

        else:
            st.info(f"✅ Ready — {st.session_state.get('total_chunks', 0)} chunks indexed.")

        # Chat display
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

        # Chat input 
        question = st.chat_input("Ask a question about the PDF...")

        if question:
            if "chunks" not in st.session_state:
                st.warning("PDF is still processing. Please wait.")
            else:
                with st.spinner("Thinking..."):
                    results, scores = search_chunks(
                        question,
                        st.session_state.chunks,
                        st.session_state.embeddings,
                    )
                    answer, confidence = ask_model(
                        question,
                        results,
                        chat_history=st.session_state.chat_history,
                        full_text=st.session_state.get("raw_text"),
                    )
                    highlights = find_highlight_coords(pdf_bytes, answer)

                st.session_state.highlights = highlights
                st.session_state.chat_history.append({
                    "question":       question,
                    "answer":         answer,
                    "confidence":     confidence,
                    "highlight_page": highlights[0]["page"] if highlights else None,
                })
                st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat History"):
                st.session_state.chat_history = []
                st.session_state.highlights   = None
                st.rerun()

else:
    st.info("👆 Upload a PDF to get started.")