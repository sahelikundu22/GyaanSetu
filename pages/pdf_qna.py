"""
import streamlit as st
from sidebar import render_sidebar

st.set_page_config(page_title="PDF Q&A", page_icon="📄")

render_sidebar()

st.title("📄 PDF Q&A")

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
"""
import streamlit as st
from sidebar import render_sidebar
import google.generativeai as genai
from PyPDF2 import PdfReader

# Configure Gemini (Ensure this is in your secrets.toml)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="PDF Q&A", page_icon="📄")
render_sidebar()

st.title("📄 PDF Q&A")

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    # Cache the text extraction so it doesn't re-run every time
    if "pdf_text" not in st.session_state:
        with st.spinner("Reading PDF..."):
            st.session_state.pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("PDF analyzed!")

ques = st.text_input("Ask any question from the PDF content:")

if st.button("Get Answer", use_container_width=True):
    if uploaded_file and ques:
        with st.spinner("Thinking..."):
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Sending the context + question to Gemini
            prompt = f"Context: {st.session_state.pdf_text[:10000]}\n\nQuestion: {ques}\n\nAnswer based ONLY on the context provided."
            response = model.generate_content(prompt)
            st.markdown(f"### Answer:\n{response.text}")
    elif not uploaded_file:
        st.warning("Please upload a PDF first.")