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

# --- TARGETED SEARCH FUNCTION ---
def find_pdf_in_subject_folder(root_dir, subject_name, chapter_name):
    # 1. Build the path to the subject folder
    subject_path = os.path.join(root_dir, subject_name)
    
    if not os.path.exists(subject_path):
        return None, f"Subject folder '{subject_name}' not found in {root_dir}"
    
    # 2. Normalize chapter name for matching (lowercase, no spaces)
    target_name = chapter_name.lower().strip().replace(" ", "")
    
    # 3. Look inside that specific subject folder
    for f in os.listdir(subject_path):
        name_only = os.path.splitext(f)[0].lower().strip().replace(" ", "")
        if name_only == target_name and f.lower().endswith(".pdf"):
            return os.path.join(subject_path, f), "Success"
            
    return None, f"Could not find '{chapter_name}' inside '{subject_name}' folder."

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
    # Embed tag works well for most modern browsers
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- EXECUTION ---
# This looks in: study_material / Science (Curiosity) / THE WONDERFUL WORLD OF PLANTS.pdf
pdf_path, error_msg = find_pdf_in_subject_folder("study_material", subject, chapter)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 🎥 Video Lesson")
    if yt_link:
        st.video(yt_link)
    else:
        st.info("Video link not found.")
    
    st.divider()
    
    if pdf_path:
        st.markdown("### 📥 Downloads")
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Standard PDF", f, file_name=f"{chapter}.pdf", use_container_width=True)
        
        with st.spinner("Compressing for rural access..."):
            compressed_data = get_compressed_pdf(pdf_path)
            st.download_button("📶 Lite Version (Saves Data)", compressed_data, file_name=f"{chapter}_Lite.pdf", use_container_width=True)
    else:
        st.warning(f"File Missing: {error_msg}")

with col2:
    st.markdown("### 📜 Read Online")
    if pdf_path:
        display_pdf(pdf_path)
    else:
        st.error("PDF viewer unavailable. Please check the filename in the subject folder.")

st.divider()
st.markdown(f"### 📝 Quick Notes for {chapter}")
st.write("Keep these points in mind for your upcoming quiz!")