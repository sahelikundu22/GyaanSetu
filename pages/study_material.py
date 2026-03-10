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

# --- FUNCTION: FIND PDF IN STATIC FOLDER ---
def find_static_pdf(subject_name, chapter_name):
    # OS Path for the server to find the file
    base_dir = os.path.join("static", "study_material", subject_name)
    
    if not os.path.exists(base_dir):
        return None, None
    
    # Normalize for case-insensitive search
    target = chapter_name.lower().strip().replace(" ", "")
    for f in os.listdir(base_dir):
        name_only = os.path.splitext(f)[0].lower().strip().replace(" ", "")
        if name_only == target and f.lower().endswith(".pdf"):
            full_os_path = os.path.join(base_dir, f)
            # URL path for the browser (Streamlit maps /static/ to /app/static/ or /static/)
            web_url = f"static/study_material/{subject_name}/{f}"
            return full_os_path, web_url
            
    return None, None

# --- FUNCTION: PDF COMPRESSION ---
@st.cache_data
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

col1, col2 = st.columns([1, 2])

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
            compressed_data = get_compressed_pdf(full_os_path)
            st.download_button("📶 Lite (Data Saver)", compressed_data, file_name=f"{chapter}_Lite.pdf", use_container_width=True)
        except Exception as e:
            st.error(f"Compression error: {e}")

        st.divider()
        # ULTIMATE FALLBACK: If the viewer on the right is blank, this button WILL work.
        st.markdown(f'''
            <a href="{pdf_web_url}" target="_blank">
                <button style="width:100%; padding:12px; background-color:#007BFF; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold;">
                    📖 Open in Full Screen / New Tab
                </button>
            </a>
            <p style="font-size:12px; color:gray; text-align:center; margin-top:5px;">
                (Use this if the viewer on the right is blank)
            </p>
        ''', unsafe_allow_html=True)
    else:
        st.warning("PDF file not found in 'static/study_material' folder.")

with col2:
    st.markdown("### 📜 Read Online")
    if pdf_web_url:
        # We use an iframe. If it's blank, the user now has the Blue Button on the left.
        pdf_display = f'<iframe src="{pdf_web_url}" width="100%" height="900px" style="border:2px solid #eee; border-radius:10px;"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.error("Online viewer unavailable.")

st.divider()
st.markdown(f"### 📝 Key Points for {chapter}")
st.write("1. Finish the video. 2. Read the chapter. 3. Earn points by completing the quiz!")