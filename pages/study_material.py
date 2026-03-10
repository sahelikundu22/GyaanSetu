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

# --- IMPROVED SEARCH FUNCTION ---
def find_pdf_case_insensitive(directory, filename):
    if not os.path.exists(directory):
        return None, f"Directory '{directory}' does not exist!"
    
    # Normalize the target name: lowercase and strip extra spaces
    target = filename.lower().strip().replace(" ", "")
    files_in_dir = os.listdir(directory)
    
    for f in files_in_dir:
        # Get filename without extension, lowercase it, strip spaces
        name_only = os.path.splitext(f)[0].lower().strip().replace(" ", "")
        if name_only == target and f.lower().endswith(".pdf"):
            return os.path.join(directory, f), "Success"
            
    return None, f"Looked for '{target}', but found: {files_in_dir}"

# --- PDF UTILITIES ---
def get_compressed_pdf(file_path):
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()

def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # Using object tag as an alternative to iframe for better compatibility
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- MAIN LOGIC ---
pdf_path, debug_msg = find_pdf_case_insensitive("study_material", chapter)

# DEBUG SECTION (Remove this once fixed)
with st.expander("🛠️ Debug Information (Click to see why PDF is missing)"):
    st.write(f"**Searching for Chapter:** {chapter}")
    st.write(f"**Folder Status:** {debug_msg}")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 🎥 Video Lesson")
    if yt_link:
        st.video(yt_link)
    else:
        st.info("No video available.")
    
    st.divider()
    
    if pdf_path:
        st.markdown("### 📥 Downloads")
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Standard PDF", f, file_name=f"{chapter}.pdf", use_container_width=True)
        
        compressed_data = get_compressed_pdf(pdf_path)
        st.download_button("📶 Lite Version", compressed_data, file_name=f"{chapter}_Lite.pdf", use_container_width=True)
    else:
        st.warning("Download unavailable: File not found.")

with col2:
    st.markdown("### 📜 Read Online")
    if pdf_path:
        display_pdf(pdf_path)
    else:
        st.error("PDF view not available. Check the Debug Info above.")