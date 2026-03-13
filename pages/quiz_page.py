"""
import streamlit as st
from sidebar import render_sidebar
from quiz import start_quiz

st.set_page_config(page_title="Quiz", page_icon="❓")

render_sidebar()

st.title("❓ Quiz")

subject = st.session_state.get('selected_subject', 'Not selected')
chapter = st.session_state.get('selected_chapter', 'Not selected')

st.subheader(f"{subject} - {chapter}")


if not st.session_state.quiz_started:
    if st.button("Start Quiz", use_container_width=True):
        st.session_state.quiz_started = True
        st.session_state.answers = {}
        st.rerun()

if st.session_state.quiz_started:
    start_quiz(subject, chapter)

st.divider()

if st.button("End Quiz", use_container_width=True):
    st.session_state.quiz_started = False
    st.session_state.answers = {}
    st.rerun()
"""

import streamlit as st
import sys, os

# Fix path so we can import files from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sidebar import render_sidebar

try:
    from quiz_utils import generate_ai_quiz
except ImportError:
    st.error("quiz_utils.py not found in project root.")

st.set_page_config(page_title="AI Quiz", layout="wide")

render_sidebar()

st.title("🤖 AI Quiz Generator")
st.write("Upload a chapter PDF to generate a practice quiz instantly.")

# ---------------- FILE UPLOAD ----------------

uploaded_pdf = st.file_uploader("📄 Upload Chapter PDF", type="pdf")

if uploaded_pdf and st.button("Generate AI Quiz", use_container_width=True):

    with st.spinner("AI is reading the chapter and creating questions..."):

        result = generate_ai_quiz(uploaded_pdf)

        if isinstance(result, dict) and "error" in result:
            st.error(f"AI Error: {result['error']}")
        else:
            st.session_state.ai_quiz_data = result
            st.session_state.ai_quiz_submitted = False
            st.success("✅ Quiz generated successfully!")

# ---------------- DISPLAY QUIZ ----------------

if "ai_quiz_data" in st.session_state:

    questions = st.session_state.ai_quiz_data

    st.divider()
    st.subheader("📝 AI Generated Quiz")

    with st.form("ai_quiz_form"):

        user_answers = []

        for i, q in enumerate(questions):

            st.markdown(f"**{i+1}. {q['q']}**")

            ans = st.radio(
                "Choose your answer:",
                q["o"],
                key=f"ai_question_{i}"
            )

            user_answers.append(ans)

        submitted = st.form_submit_button("Submit Quiz")

    # ----------- SCORE CALCULATION AFTER SUBMIT -----------

    if submitted:

        score = 0

        for i, q in enumerate(questions):
            if user_answers[i] == q["a"]:
                score += 1

        total = len(questions)

        st.session_state.ai_quiz_submitted = True

        st.success(f"🎯 Final Score: {score} / {total}")

        if score == total:
            st.balloons()

        # Show correct answers
        st.divider()
        st.subheader("✅ Correct Answers")

        for i, q in enumerate(questions):
            st.write(f"**Q{i+1}: {q['a']}**")