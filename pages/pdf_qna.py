import streamlit as st
from sidebar import render_sidebar

from pdf_qna_engine.pdf_reader import extract_text
from pdf_qna_engine.chunking import split_text
from pdf_qna_engine.embeddings import create_embeddings
from pdf_qna_engine.search import search_chunks
from pdf_qna_engine.llm import ask_model

st.set_page_config(page_title="PDF Q&A", page_icon="📄")

render_sidebar()

st.title("PDF Q&A")

with st.expander("How it Works", expanded=True):
    st.write("""
Upload a PDF document and ask questions about its content.

Steps:
1. The PDF text is extracted.
2. The text is split into chunks.
3. Each chunk is converted into embeddings.
4. Similar chunks are retrieved using semantic search.
5. The AI4Bharat model generates the final answer.
""")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:

    if "chunks" not in st.session_state:

        text = extract_text(uploaded_file)

        chunks = split_text(text)

        embeddings = create_embeddings(chunks)

        st.session_state.chunks = chunks
        st.session_state.embeddings = embeddings

        st.success("PDF processed successfully")

question = st.text_input("Ask a question from the PDF")

if st.button("Get Answer"):

    if question and "chunks" in st.session_state:

        with st.spinner("Searching document..."):

            chunks = st.session_state.chunks
            embeddings = st.session_state.embeddings

            results = search_chunks(question, chunks, embeddings)

            context = "\n".join(results)

            answer = ask_model(question, context)

            st.subheader("Answer")
            st.write(answer)

    else:
        st.warning("Please upload a PDF and enter a question.")