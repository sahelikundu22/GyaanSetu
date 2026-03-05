import streamlit as st

def pdf_qna_page(selected_chapter, selected_module):
    """PDF Q&A Page"""
    st.subheader("📄 PDF Q&A")

    with st.expander("How it Works", expanded=True):
        st.write("""
        - Upload a PDF document to enable document-based question answering.  
        - The PDF text is segmented into chunks and converted into embeddings, which are stored in a vector database.  
        - For each query, semantic similarity search retrieves the most relevant chunks and Gemini generates a context-aware response.
        """)
    
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file is not None:
        st.success("PDF uploaded successfully!")

    ques = st.text_input("Ask any question from the PDF content:")

    if st.button("Get Answer", use_container_width=True):
        if ques:
            with st.spinner("Finding answer..."):
                st.success("Coding of this part is not done yet...")
        else:
            st.warning("Please enter a question.")