import streamlit as st
import sys, os, base64, io
from pypdf import PdfReader, PdfWriter

# PATH FIX: Allow finding sidebar.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sidebar import render_sidebar

st.set_page_config(page_title="Study Material", layout="wide")
render_sidebar()

sub = st.session_state.get('selected_subject', 'General')
ch = st.session_state.get('selected_chapter', 'Introduction')
yt = st.session_state.get('selected_yt_link', '')

st.title(f"📖 {sub}")
st.subheader(f"Lesson: {ch}")

# --- PDF Search Logic ---
pdf_path = None
# Looks in study_material/Science (Curiosity)/ etc.
sub_folder = os.path.join("study_material", sub)
if os.path.exists(sub_folder):
    target = ch.lower().replace(" ", "")
    for f in os.listdir(sub_folder):
        if f.lower().replace(" ", "").startswith(target):
            pdf_path = os.path.join(sub_folder, f)

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("### 🎥 Video")
    if yt: st.video(yt)
    
    if pdf_path:
        st.divider()
        st.markdown("### 📥 Downloads")
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Normal PDF", f, file_name=f"{ch}.pdf", use_container_width=True)
        
        # Lite Compression
        writer = PdfWriter()
        for page in PdfReader(pdf_path).pages:
            p = writer.add_page(page)
            p.compress_content_streams()
        buf = io.BytesIO()
        writer.write(buf)
        st.download_button("📶 Lite PDF", buf.getvalue(), file_name=f"{ch}_lite.pdf", use_container_width=True)

with col2:
    st.markdown("### 📜 Read Online")
    if pdf_path:
        with open(pdf_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
        pdf_html = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="800px"></iframe>'
        st.markdown(pdf_html, unsafe_allow_html=True)
    else:
        st.error("PDF file not found in folder.")

st.divider()
# st.markdown(f"### 📝 Key Points for {chapter}")
st.write("- Watch the video. \n- Read the notes. \n- Complete the quiz.")