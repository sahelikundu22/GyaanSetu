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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sidebar import render_sidebar
from quiz_utils import generate_ai_quiz


st.set_page_config(page_title="AI Quiz", layout="wide")

render_sidebar()

st.title("🤖 AI Quiz Generator")

st.write("Upload a chapter PDF and generate practice questions instantly.")

# Upload PDF
uploaded_pdf = st.file_uploader("Upload Chapter PDF", type="pdf")


# Generate Quiz
if uploaded_pdf and st.button("Generate Quiz", use_container_width=True):

    with st.spinner("Generating quiz from PDF..."):

        quiz = generate_ai_quiz(uploaded_pdf)

        if isinstance(quiz, dict) and "error" in quiz:
            st.error(quiz["error"])
        else:
            st.session_state.ai_quiz = quiz
            st.success("Quiz generated successfully!")


# Show quiz
if "ai_quiz" in st.session_state:

    questions = st.session_state.ai_quiz

    st.subheader("Practice Quiz")

    with st.form("quiz_form"):

        answers = []

        for i, q in enumerate(questions):

            st.write(f"**{i+1}. {q['q']}**")

            ans = st.radio(
                "Select answer",
                q["o"],
                key=f"q{i}"
            )

            answers.append(ans)

        submitted = st.form_submit_button("Submit Quiz")

    if submitted:

        score = 0

        for i, q in enumerate(questions):
            if answers[i] == q["a"]:
                score += 1

        st.success(f"Score: {score} / {len(questions)}")

        if score == len(questions):
            st.balloons()