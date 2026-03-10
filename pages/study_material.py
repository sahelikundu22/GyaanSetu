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

# --- FUNCTION: SEARCH FOR PDF ---
def find_pdf_file(subject_name, chapter_name):
    # This looks in your 'study_material' folder
    base_dir = os.path.join("study_material", subject_name)
    if not os.path.exists(base_dir):
        return None
    
    target = chapter_name.lower().strip().replace(" ", "")
    for f in os.listdir(base_dir):
        name_only = os.path.splitext(f)[0].lower().strip().replace(" ", "")
        if name_only == target and f.lower().endswith(".pdf"):
            return os.path.join(base_dir, f)
    return None

# --- FUNCTION: COMPRESS PDF ---
def get_compressed_pdf(file_path):
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        new_page = writer.add_page(page) # Add to writer first
        new_page.compress_content_streams() # Then compress
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()

# --- FUNCTION: VIEW ONLINE ---
def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # Using an <iframe> with base64 data
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="900px" style="border:none;"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- UI LAYOUT ---
pdf_path = find_pdf_file(subject, chapter)
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 🎥 Video Lesson")
    if yt_link:
        st.video(yt_link)
    else:
        st.info("No video available.")
    
    st.divider()
    
    if pdf_path:
        st.markdown("### 📥 Downloads")
        # Normal Download
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Standard PDF", f, file_name=f"{chapter}.pdf", use_container_width=True)
        
        # Compressed Download
        try:
            compressed_data = get_compressed_pdf(pdf_path)
            st.download_button("📶 Lite Version (Data Saver)", compressed_data, file_name=f"{chapter}_Lite.pdf", use_container_width=True)
        except Exception as e:
            st.error(f"Compression error: {e}")
    else:
        st.warning("PDF file not found. Check folder names.")

with col2:
    st.markdown("### 📜 Read Online")
    if pdf_path:
        display_pdf(pdf_path)
    else:
        st.error("Select a valid chapter from the sidebar.")

st.divider()
st.markdown(f"### 📝 Key Points for {chapter}")
st.write("- Watch the video. \n- Read the notes. \n- Complete the quiz.")