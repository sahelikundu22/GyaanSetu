import streamlit as st
import yt_dlp
import whisper
import os
import uuid

st.set_page_config(
    page_title="SmartLearn AI",
    page_icon="🎥",
    layout="wide"
)

# UI HEADER
st.markdown(
    "<h1 style='text-align:center;'>🎥 SmartLearn AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center; color:gray;'>Convert YouTube Videos into Transcripts</h4>",
    unsafe_allow_html=True
)

st.divider()

# INPUT
youtube_url = st.text_input(
    "🔗 Enter YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

generate = st.button("🚀 Generate Transcript")

# FUNCTIONS
def download_audio(url, filename):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,
        "quiet": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_audio(file_path):
    model = whisper.load_model("tiny")  # tiny = faster on CPU
    result = model.transcribe(file_path)
    return result["text"]

# TRANSCRIPT LOGIC
if generate:

    if not youtube_url.strip():
        st.warning("Please enter a valid YouTube URL.")
        st.stop()

    video_id = str(uuid.uuid4())
    audio_file = f"{video_id}.mp3"

    with st.spinner("📥 Downloading audio..."):
        download_audio(youtube_url, audio_file)

    if not os.path.exists(audio_file):
        st.error("Audio download failed.")
        st.stop()

    with st.spinner("🧠 Transcribing... please wait"):
        transcript = transcribe_audio(audio_file)

    st.success("✅ Transcription Completed!")

    st.subheader("📄 Transcript")

    st.text_area("", transcript, height=400)

    # cleanup
    os.remove(audio_file)