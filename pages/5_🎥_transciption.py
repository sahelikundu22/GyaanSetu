import streamlit as st
import sys, os, re, requests

# Youtube Video Transcription Page
if not st.session_state.get("logged_in", False):
    st.warning("Please login to access this page.")
    st.stop()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sidebar import render_sidebar

st.set_page_config(page_title="Transcription", layout="wide")
render_sidebar()

st.title("🎥 YouTube Transcription Tool")
st.write("Paste a YouTube link to generate transcript and learning content.")



def extract_video_id(url: str):
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_transcript(video_id: str):
    """Fetch transcript using youtube-transcript-api."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        ytt_api = YouTubeTranscriptApi()

        try:
            transcript_list = ytt_api.list(video_id)
        except Exception:
            # Fallback: try direct fetch
            transcript = ytt_api.fetch(video_id)
            entries = [{"start": s.start, "text": s.text} for s in transcript]
            return entries, "Auto-detected"

        transcript = None
        detected_lang = "Unknown"

        # Prefer manual captions
        for t in transcript_list:
            if not t.is_generated:
                transcript = t.fetch()
                detected_lang = t.language
                break

        # Fallback to auto-generated
        if transcript is None:
            for t in transcript_list:
                transcript = t.fetch()
                detected_lang = t.language
                break

        if transcript is None:
            return None, None

        entries = [{"start": s.start, "text": s.text} for s in transcript]
        return entries, detected_lang

    except Exception as e:
        import traceback
        st.error(f"❌ Could not fetch transcript: {e}")
        st.code(traceback.format_exc())
        return None, None


def cleanup_transcript(entries: list) -> list:
    """Run transcript through AI to fix YouTube's misspellings and garbled text."""
    BATCH_SIZE = 30  # lines per batch
    api_key = st.secrets["GROQ_API_KEY"]
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    cleaned = []
    progress = st.progress(0)
    total = len(entries)

    for i in range(0, total, BATCH_SIZE):
        batch = entries[i:i + BATCH_SIZE]
        raw_lines = [e["text"] for e in batch]
        numbered = "\n".join(f"{j+1}. {line}" for j, line in enumerate(raw_lines))

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": """You fix auto-generated YouTube captions. Rules:
- Fix misspellings, garbled words, and broken grammar.
- Keep the EXACT same meaning — do NOT add or remove information.
- Keep the EXACT same number of lines. Each numbered line maps to one subtitle.
- Output ONLY the corrected numbered lines, nothing else.
- If a line is already correct, output it unchanged.
- Preserve the original language (Hindi stays Hindi, English stays English).""" },
                {"role": "user", "content": numbered}
            ],
            "max_tokens": 2048,
            "temperature": 0.1,
        }

        try:
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers, json=payload
            )
            resp.raise_for_status()
            result = resp.json()["choices"][0]["message"]["content"].strip()

            # Parse numbered lines back
            import re
            fixed_lines = re.findall(r"^\d+\.\s*(.+)$", result, re.MULTILINE)

            if len(fixed_lines) == len(batch):
                for j, e in enumerate(batch):
                    cleaned.append({"start": e["start"], "text": fixed_lines[j].strip()})
            else:
                # Line count mismatch — keep originals
                cleaned.extend(batch)
        except Exception:
            cleaned.extend(batch)

        done = min(i + BATCH_SIZE, total)
        progress.progress(done / total, text=f"Cleaning transcript... {done}/{total} segments")

    progress.empty()
    return cleaned


LANG_CODES = {"English": "en", "Hindi": "hi", "Bengali": "bn"}


def translate_entries(entries: list, target_lang: str) -> list:
    """Translate all transcript entries using Google Translate (via deep-translator)."""
    from deep_translator import GoogleTranslator

    target_code = LANG_CODES.get(target_lang, "en")
    translated = []
    progress_bar = st.progress(0)
    total = len(entries)

    # Batch entries to reduce API calls (Google Translate handles up to ~5000 chars)
    BATCH_CHAR_LIMIT = 4500
    i = 0

    while i < total:
        batch = []
        batch_chars = 0

        while i < total and batch_chars + len(entries[i]["text"]) < BATCH_CHAR_LIMIT:
            batch.append(entries[i])
            batch_chars += len(entries[i]["text"]) + 1  # +1 for newline
            i += 1

        if not batch:
            # Single entry too long — translate it alone
            batch = [entries[i]]
            i += 1

        combined = "\n".join([e["text"] for e in batch])

        try:
            result = GoogleTranslator(source="auto", target=target_code).translate(combined)
            translated_lines = result.split("\n")

            if len(translated_lines) == len(batch):
                for j, e in enumerate(batch):
                    translated.append({"start": e["start"], "text": translated_lines[j].strip()})
            else:
                # Line count mismatch — translate one by one
                for e in batch:
                    try:
                        t = GoogleTranslator(source="auto", target=target_code).translate(e["text"])
                        translated.append({"start": e["start"], "text": t.strip()})
                    except Exception:
                        translated.append(e)
        except Exception:
            # On failure, keep originals for this batch
            translated.extend(batch)

        progress_bar.progress(len(translated) / total, text=f"Translating to {target_lang}... {len(translated)}/{total} segments")

    progress_bar.empty()
    return translated



def summarize_with_ai(text: str, output_lang: str = "English"):
    """Generate an AI study guide from transcript text."""
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        tok_limit = 1500 if output_lang.lower() != "english" else 800

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": f"""OUTPUT LANGUAGE RULE (MANDATORY, HIGHEST PRIORITY):
You MUST write the ENTIRE summary in {output_lang} only.
- If output_language is English, write ONLY in English. Do NOT mix Hindi/Bengali words.
- If output_language is Hindi, write ONLY in Hindi (Devanagari script). Do NOT mix English.
- If output_language is Bengali, write ONLY in Bengali script. Do NOT mix English.
The transcript may be in ANY language. You MUST translate and summarize it entirely into {output_lang}.

GROUNDING RULES (MANDATORY):
- Summarize ONLY information found in the video transcript below.
- Do NOT add outside knowledge. Do NOT invent facts.
- Provide a structured study guide with: Main topics, Key concepts, Important facts."""},
                {"role": "user", "content": f"""[Write summary in {output_lang} ONLY]

Transcript:
{text[:6000]}"""}
            ],
            "max_tokens": tok_limit,
            "temperature": 0.1,
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers, json=payload
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error generating summary: {e}"


def format_timestamp(seconds: float) -> str:
    """Convert seconds to MM:SS format."""
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


# ---------- MAIN UI ----------

youtube_url = st.text_input("🔗 Enter YouTube URL")

if st.button("Generate Transcript"):
    if not youtube_url:
        st.warning("Please enter a YouTube URL")
    else:
        video_id = extract_video_id(youtube_url)
        if not video_id:
            st.error("❌ Could not extract video ID from URL")
        else:
            with st.spinner("Fetching transcript..."):
                entries, detected_lang = fetch_transcript(video_id)

            if entries:
                # AI cleanup pass to fix YouTube's errors
                entries = cleanup_transcript(entries)

                st.session_state.transcript_entries = entries
                st.session_state.transcript_detected_lang = detected_lang
                st.session_state.transcript_video_id = video_id
                # Clear cached translations
                for key in list(st.session_state.keys()):
                    if key.startswith("translated_entries_") or key.startswith("transcript_summary_"):
                        del st.session_state[key]
                st.success(f"✅ Transcript fetched & cleaned! ({len(entries)} segments, Language: {detected_lang})")
            else:
                st.error("❌ No transcript available for this video")


# ---------- DISPLAY TRANSCRIPT ----------

if "transcript_entries" in st.session_state:
    entries = st.session_state.transcript_entries
    detected = st.session_state.get("transcript_detected_lang", "Unknown")

    st.info(f"📝 Source language: **{detected}**")

    tab1, tab2 = st.tabs(["📝 Full Transcript", "🤖 AI Summary"])

    with tab1:
        view_lang = st.selectbox(
            "🌐 View transcript in:",
            ["Original", "English", "Hindi", "Bengali"],
            key="transcript_view_lang"
        )

        display_entries = entries

        if view_lang != "Original":
            # Check if same language
            same_lang = view_lang.lower() == detected.lower() if detected else False
            if same_lang:
                st.info(f"Transcript is already in {view_lang} — no translation needed.")
            else:
                cache_key = f"translated_entries_{view_lang}"
                if cache_key in st.session_state:
                    display_entries = st.session_state[cache_key]
                else:
                    with st.spinner(f"Translating to {view_lang}..."):
                        display_entries = translate_entries(entries, view_lang)
                    st.session_state[cache_key] = display_entries

        # Display entries
        transcript_text = ""
        for e in display_entries:
            ts = format_timestamp(e["start"])
            line = f"{ts} — {e['text']}"
            transcript_text += line + "\n"
            st.text(line)

        # Download button
        lang_suffix = f"_{view_lang}" if view_lang != "Original" else ""
        st.download_button(
            "📥 Download Transcript",
            transcript_text,
            file_name=f"transcript{lang_suffix}.txt",
            mime="text/plain"
        )

    with tab2:
        summary_lang = st.selectbox(
            "🌐 Summary Language",
            ["English", "Hindi", "Bengali"],
            key="summary_lang_tab2"
        )

        def on_summary_click():
            st.session_state._do_summary = True
            st.session_state._do_summary_lang = st.session_state.summary_lang_tab2

        st.button("🤖 Generate Summary", on_click=on_summary_click)

        if st.session_state.pop("_do_summary", False):
            lang_for_summary = st.session_state.pop("_do_summary_lang", "English")
            cache_key = f"transcript_summary_{lang_for_summary}"

            if cache_key not in st.session_state:
                full_text = " ".join([e["text"] for e in entries])
                with st.spinner(f"Generating summary in {lang_for_summary}..."):
                    summary = summarize_with_ai(full_text, lang_for_summary)
                st.session_state[cache_key] = summary

        # Display cached summary
        summary_cache_key = f"transcript_summary_{summary_lang}"
        if summary_cache_key in st.session_state:
            st.markdown("### 📋 Study Guide")
            st.markdown(st.session_state[summary_cache_key])