"""
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
    subject_path = os.path.join(root_dir, subject_name)
    if not os.path.exists(subject_path):
        return None, f"Subject folder '{subject_name}' not found."
    
    target_name = chapter_name.lower().strip().replace(" ", "")
    for f in os.listdir(subject_path):
        name_only = os.path.splitext(f)[0].lower().strip().replace(" ", "")
        if name_only == target_name and f.lower().endswith(".pdf"):
            return os.path.join(subject_path, f), "Success"
    return None, f"Could not find '{chapter_name}' in {subject_name}."

# --- PDF UTILITIES ---
@st.cache_data
def get_compressed_pdf(file_path):
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        # Fix: Add to writer first, then compress
        new_page = writer.add_page(page)
        new_page.compress_content_streams() 
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()

def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- EXECUTION ---
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
        
        try:
            compressed_data = get_compressed_pdf(pdf_path)
            st.download_button("📶 Lite Version (Saves Data)", compressed_data, file_name=f"{chapter}_Lite.pdf", use_container_width=True)
        except Exception as e:
            st.error(f"Compression error: {e}")
    else:
        st.warning(f"File Missing: {error_msg}")

with col2:
    st.markdown("### 📜 Read Online")
    if pdf_path:
        display_pdf(pdf_path)
    else:
        st.error("PDF viewer unavailable.")

st.divider()
st.markdown(f"### 📝 Quick Notes for {chapter}")
st.write("Keep these points in mind for your upcoming quiz!")
"""

import streamlit as st
from sidebar import render_sidebar
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

# --- UPDATED SEARCH FUNCTION (Point to Static) ---
def find_static_pdf(subject_name, chapter_name):
    # This path is for the OS to check if the file exists
    base_dir = os.path.join("static", "study_material", subject_name)
    
    if not os.path.exists(base_dir):
        return None, None
    
    target = chapter_name.lower().strip().replace(" ", "")
    for f in os.listdir(base_dir):
        name_only = os.path.splitext(f)[0].lower().strip().replace(" ", "")
        if name_only == target and f.lower().endswith(".pdf"):
            # Internal OS path for compression/download
            full_path = os.path.join(base_dir, f)
            # Web URL path for the iframe (Streamlit serves /static/ as /app/static/)
            web_url = f"static/study_material/{subject_name}/{f}"
            return full_path, web_url
            
    return None, None

# --- COMPRESSION LOGIC (REFIXED) ---
def get_compressed_pdf(file_path):
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        new_page = writer.add_page(page)
        new_page.compress_content_streams() 
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()

# --- EXECUTION ---
full_os_path, pdf_web_url = find_static_pdf(subject, chapter)

col1, col2 = st.columns([1, 2]) # Give more space to the PDF (Right side)

with col1:
    st.markdown("### 🎥 Video Lesson")
    if yt_link:
        st.video(yt_link)
    else:
        st.info("No video available.")
    
    st.divider()
    
    if full_os_path:
        st.markdown("### 📥 Downloads")
        # Standard Download
        with open(full_os_path, "rb") as f:
            st.download_button("📄 Standard PDF", f, file_name=f"{chapter}.pdf", use_container_width=True)
        
        # Compressed Download
        try:
            with st.spinner("Preparing Lite version..."):
                compressed_data = get_compressed_pdf(full_os_path)
                st.download_button("📶 Lite (Data Saver)", compressed_data, file_name=f"{chapter}_Lite.pdf", use_container_width=True)
        except Exception as e:
            st.error(f"Compression error: {e}")
    else:
        st.warning("File not found in static folder.")

with col2:
    st.markdown("### 📜 Read Online")
    if pdf_web_url:
        # Direct URL serving - Fixes the Blank Page issue
        # Note: We use /st/ or direct path depending on version, but usually just the relative path works
        pdf_display = f'<iframe src="{pdf_web_url}" width="100%" height="900px" style="border:1px solid #ddd;"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.error("Online viewer unavailable. Ensure file is in static/study_material/Subject/Chapter.pdf")

st.divider()
st.markdown(f"### 📝 Key Points for {chapter}")
st.write("1. Review the video lessons. \n2. Read the digital textbook. \n3. Take the quiz to earn points!")