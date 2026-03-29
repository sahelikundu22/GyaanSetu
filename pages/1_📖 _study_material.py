import streamlit as st
import sys, os, io
from pypdf import PdfReader, PdfWriter
from streamlit_pdf_viewer import pdf_viewer

# fixing default page
if not st.session_state.get("logged_in", False):
    st.warning("Please login to access this page.")
    st.stop()

# PATH FIX: Allow finding sidebar.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sidebar import render_sidebar

st.set_page_config(page_title="Study Material", layout="wide")
render_sidebar()

sub = st.session_state.get('selected_subject', 'General')
ch = st.session_state.get('selected_chapter', 'Introduction')
yt = st.session_state.get('selected_yt_link', '')
lang = st.session_state.get("language", "English")

# ---------- UI TEXT ----------
TEXT = {
    "English": {
        "title": "📖",
        "lesson": "Lesson",
        "video": "### 🎥 Video",
        "downloads": "### 📥 Downloads",
        "normal_pdf": "📄 Standard PDF",
        "lite_pdf": "📶 Lite PDF",
        "read_online": "### 📜 Read Online",
        "pdf_not_found": "PDF file not found in folder.",
        "key_points": "### 📝 Key Points for",
        "points": "- Watch the video. \n- Read the notes. \n- Complete the quiz."
    },
    "Hindi": {
        "title": "📖",
        "lesson": "पाठ",
        "video": "### 🎥 वीडियो",
        "downloads": "### 📥 डाउनलोड",
        "normal_pdf": "📄 सामान्य PDF",
        "lite_pdf": "📶 संपीड़ित PDF",
        "read_online": "### 📜 ऑनलाइन पढ़ें",
        "pdf_not_found": "इस अध्याय के लिए PDF नहीं मिला।",
        "key_points": "### 📝 मुख्य बिंदु:",
        "points": "- वीडियो देखें। \n- नोट्स पढ़ें। \n- क्विज़ पूरा करें।"
    },
    "Bengali": {
        "title": "📖",
        "lesson": "পাঠ",
        "video": "### 🎥 ভিডিও",
        "downloads": "### 📥 ডাউনলোড",
        "normal_pdf": "📄 সাধারণ PDF",
        "lite_pdf": "📶 কমপ্রেসড PDF",
        "read_online": "### 📜 অনলাইনে পড়ুন",
        "pdf_not_found": "এই অধ্যায়ের PDF ফোল্ডারে পাওয়া যায়নি।",
        "key_points": "### 📝 মূল পয়েন্ট:",
        "points": "- ভিডিও দেখো। \n- নোট পড়ো। \n- কুইজ সম্পূর্ণ করো।"
    }
}

t = TEXT.get(lang, TEXT["English"])

st.title(f"{t['title']} {sub}")
st.subheader(f"{t['lesson']}: {ch}")

# --- PDF Search Logic ---
pdf_path = None

# 1. Try language-specific folder first
# Example: study_material/Hindi/Science/
sub_folder_lang = os.path.join("study_material", lang, sub)

if os.path.exists(sub_folder_lang):
    target = ch.lower().replace(" ", "")
    for f in os.listdir(sub_folder_lang):
        if f.lower().replace(" ", "").startswith(target) and f.lower().endswith(".pdf"):
            pdf_path = os.path.join(sub_folder_lang, f)
            break

# 2. Fallback to English folder
if not pdf_path:
    sub_folder_english = os.path.join("study_material", "English", sub)
    if os.path.exists(sub_folder_english):
        target = ch.lower().replace(" ", "")
        for f in os.listdir(sub_folder_english):
            if f.lower().replace(" ", "").startswith(target) and f.lower().endswith(".pdf"):
                pdf_path = os.path.join(sub_folder_english, f)
                break

# 3. Fallback to your old existing structure
if not pdf_path:
    sub_folder = os.path.join("study_material", sub)
    if os.path.exists(sub_folder):
        target = ch.lower().replace(" ", "")
        for f in os.listdir(sub_folder):
            if f.lower().replace(" ", "").startswith(target) and f.lower().endswith(".pdf"):
                pdf_path = os.path.join(sub_folder, f)
                break

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(t["video"])
    if yt:
        st.video(yt)

    if pdf_path:
        st.divider()
        st.markdown(t["downloads"])

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        st.download_button(
            t["normal_pdf"],
            pdf_bytes,
            file_name=f"{ch}.pdf",
            use_container_width=True
        )

        # Lite Compression
        writer = PdfWriter()
        for page in PdfReader(pdf_path).pages:
            p = writer.add_page(page)
            try:
                p.compress_content_streams()
            except Exception:
                pass

        buf = io.BytesIO()
        writer.write(buf)

        st.download_button(
            t["lite_pdf"],
            buf.getvalue(),
            file_name=f"{ch}_lite.pdf",
            use_container_width=True
        )

with col2:
    st.markdown(t["read_online"])
    if pdf_path:
        pdf_viewer(pdf_path)
    else:
        st.error(t["pdf_not_found"])

st.divider()
st.markdown(f"{t['key_points']} {ch}")
st.write(t["points"])