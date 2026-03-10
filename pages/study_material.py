"""
import streamlit as st
from sidebar import render_sidebar

st.set_page_config(page_title="Study Material", page_icon="📖")

render_sidebar()

st.title("📖 Study Material")


subject = st.session_state.get('selected_subject', 'Not selected')
chapter = st.session_state.get('selected_chapter', 'Not selected')
yt_link = st.session_state.get('selected_yt_link', '')

st.subheader(f"{subject} - {chapter}")


if yt_link:
    st.video(yt_link)
else:
    st.info("No video available for this chapter")


st.markdown("### 📝 Study Notes")
st.markdown(f"""
**Key Points for {chapter}:**
- Point 1: Understanding the basic concepts
- Point 2: Important formulas and definitions
- Point 3: Real-life applications
- Point 4: Practice examples
""")


st.markdown("### 📚 Additional Resources")
st.markdown("- [NCERT Textbook](https://ncert.nic.in/)")
st.markdown("- [Practice Worksheets](#)")
st.markdown("- [Reference Videos](#)")


if st.button("✅ Mark as Completed"):
    st.success(f"Completed {chapter}!")
    st.balloons()
"""

import streamlit as st
from sidebar import render_sidebar
import base64
import os
import io
from pypdf import PdfReader, PdfWriter

st.set_page_config(page_title="Study Material", page_icon="📖", layout="wide")
render_sidebar()

# Fetch data from session state
subject = st.session_state.get('selected_subject', 'General')
chapter = st.session_state.get('selected_chapter', 'Introduction')
yt_link = st.session_state.get('selected_yt_link', '')

st.title(f"📖 {subject}")
st.subheader(f"Chapter: {chapter}")

# --- HELPER FUNCTIONS ---

def get_compressed_pdf(file_path):
    """Compresses the PDF and returns a bytes object."""
    reader = PdfReader(file_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()  # This reduces the size of text/graphics
        writer.add_page(page)
    
    # Save to a byte buffer instead of a file
    remote_buffer = io.BytesIO()
    writer.write(remote_buffer)
    return remote_buffer.getvalue()

def display_pdf(file_path):
    """Encodes PDF to base64 for inline browser viewing."""
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" style="border:none;"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error displaying PDF: {e}")

# --- MAIN UI LAYOUT ---

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 🎥 Video Lesson")
    if yt_link:
        st.video(yt_link)
    else:
        st.info("Video coming soon for this chapter.")
    
    st.divider()
    
    # DOWNLOAD SECTION
    st.markdown("### 📥 Download Options")
    pdf_path = f"study_material/{chapter}.pdf"
    
    if os.path.exists(pdf_path):
        # Normal Download
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download High Quality (Standard)",
                data=f,
                file_name=f"{chapter}_HQ.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        # Compressed Download for Rural Students
        with st.spinner("Compressing for low bandwidth..."):
            compressed_data = get_compressed_pdf(pdf_path)
            orig_size = os.path.getsize(pdf_path) / 1024
            comp_size = len(compressed_data) / 1024
            
            st.download_button(
                label=f"📶 Download Lite Version ({comp_size:.1f} KB)",
                data=compressed_data,
                file_name=f"{chapter}_Lite.pdf",
                mime="application/pdf",
                use_container_width=True,
                help=f"Reduced from {orig_size:.1f} KB. Best for slow internet."
            )
    else:
        st.warning("Physical PDF file not found in 'study_material' folder.")

with col2:
    st.markdown("### 📜 Read Online")
    if os.path.exists(pdf_path):
        display_pdf(pdf_path)
    else:
        st.info("Please upload the PDF to the server to enable online reading.")

st.divider()

if st.button("✅ Mark Chapter as Completed"):
    st.success(f"Progress Saved for {chapter}!")
    st.balloons()