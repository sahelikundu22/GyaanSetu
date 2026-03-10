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

# 1. Page Config
st.set_page_config(page_title="Study Material", page_icon="📖", layout="wide")
render_sidebar()

# 2. Get session data
subject = st.session_state.get('selected_subject', 'Subject')
chapter = st.session_state.get('selected_chapter', 'Chapter')
yt_link = st.session_state.get('selected_yt_link', '')

st.title(f"📖 {subject}")
st.subheader(f"Lesson: {chapter}")

# --- HELPER FUNCTIONS ---
def get_compressed_pdf(file_path):
    """Compresses PDF content streams to save bandwidth."""
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        page.compress_content_streams() 
        writer.add_page(page)
    remote_buffer = io.BytesIO()
    writer.write(remote_buffer)
    return remote_buffer.getvalue()

def display_pdf(file_path):
    """Embeds PDF in an iframe for online reading."""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🎥 Video Lesson")
    if yt_link:
        st.video(yt_link)
    else:
        st.info("No video available.")

    st.divider()

    st.markdown("### 📥 Downloads")
    pdf_path = f"study_material/{chapter}.pdf"
    
    if os.path.exists(pdf_path):
        # Normal Download
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download Standard PDF", f, file_name=f"{chapter}.pdf", use_container_width=True)
        
        # Compressed Download
        with st.spinner("Preparing Lite version..."):
            compressed_data = get_compressed_pdf(pdf_path)
            st.download_button(
                label=f"📶 Download Lite PDF (Saves Data)",
                data=compressed_data,
                file_name=f"{chapter}_compressed.pdf",
                use_container_width=True
            )
    else:
        st.error(f"File not found: {pdf_path}")

with col2:
    st.markdown("### 📜 Read Online")
    if os.path.exists(pdf_path):
        display_pdf(pdf_path)
    else:
        st.warning("PDF is currently unavailable for online viewing.")

st.divider()

# Fixed Markdown Section
st.markdown(f"### 📝 Key Points for {chapter}:")
st.write("Review these points before taking the quiz!")