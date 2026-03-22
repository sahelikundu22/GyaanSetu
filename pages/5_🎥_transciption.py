import streamlit as st
import sys, os

# fixing default page
if not st.session_state.get("logged_in", False):
    st.warning("Please login to access this page.")
    st.stop()

# Path fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sidebar import render_sidebar

st.set_page_config(page_title="Transcription", layout="wide")

render_sidebar()

st.title("🎥 YouTube Transcription Tool")

st.write("Paste a YouTube link to generate transcript and learning content.")

st.divider()

youtube_url = st.text_input(
    "🔗 Enter YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

col1, col2, col3 = st.columns([3,1,3])

with col2:
    if st.button("Generate Transcript", use_container_width=True):
        if youtube_url:
            st.success(f"Processing: {youtube_url}")
            # 👉 Call your transcript function here
        else:
            st.warning("Please enter a YouTube URL")