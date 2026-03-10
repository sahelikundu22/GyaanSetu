import streamlit as st
from sidebar import render_sidebar
import base64
import os
import io
from pypdf import PdfReader, PdfWriter

st.set_page_config(page_title="Study Material", page_icon="📖", layout="wide")
render_sidebar()

# 1. Fetch data from session state
subject = st.session_state.get('selected_subject', 'General')
chapter = st.session_state.get('selected_chapter', 'Introduction')
yt_link = st.session_state.get('selected_yt_link', '')

st.title(f"📖 {subject}")
st.subheader(f"Chapter: {chapter}")

# --- HELPER FUNCTIONS ---

def find_pdf_case_insensitive(directory, filename):
    """Finds a file in a directory regardless of case (e.g., matching 'super senses' to 'SUPER SENSES.pdf')."""
    if not os.path.exists(directory):
        return None
    
    # Normalize the target name
    target = filename.lower().replace(" ", "")
    
    for f in os.listdir(directory):
        # Normalize the actual file name found in folder
        actual_name = os.path.splitext(f)[0].lower().replace(" ", "")
        if actual_name == target and f.lower().endswith(".pdf"):
            return os.path.join(directory, f)
    return None

def get_compressed_pdf(file_path):
    """Compresses the PDF and returns a bytes object."""
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)
    
    remote_buffer = io.BytesIO()
    writer.write(remote_buffer)
    return remote_buffer.getvalue()

def display_pdf(file_path):
    """Encodes PDF to base64 for inline browser viewing."""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" style="border:none;"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- MAIN LOGIC ---

# Search for the file in the study_material folder
pdf_path = find_pdf_case_insensitive("study_material", chapter)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 🎥 Video Lesson")
    if yt_link:
        st.video(yt_link)
    else:
        st.info("No video available for this chapter.")
    
    st.divider()
    
    st.markdown("### 📥 Download Options")
    
    if pdf_path:
        # Normal Download
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download Standard PDF",
                data=f,
                file_name=f"{chapter}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        # Compressed Download
        with st.spinner("Compressing for low bandwidth..."):
            compressed_data = get_compressed_pdf(pdf_path)
            st.download_button(
                label="📶 Download Lite Version (Saves Data)",
                data=compressed_data,
                file_name=f"{chapter}_Lite.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.warning(f"Could not find PDF for: {chapter}")
        st.info("Check if the file exists in the 'study_material' folder.")

with col2:
    st.markdown("### 📜 Read Online")
    if pdf_path:
        display_pdf(pdf_path)
    else:
        st.info("PDF view not available.")

st.divider()

# Fixed Markdown Section (Correct Syntax)
st.markdown(f"### 📝 Key Points for {chapter}")
st.markdown("- Critical concepts covered in this chapter.")
st.markdown("- Key definitions and terminology.")