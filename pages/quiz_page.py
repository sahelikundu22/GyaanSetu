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
from sidebar import render_sidebar
from quiz_utils import generate_ai_quiz

st.set_page_config(page_title="AI Quiz")
render_sidebar()

st.title("🤖 AI Quiz Generator")
up_file = st.file_uploader("Upload Chapter PDF", type="pdf")

if up_file and st.button("Generate Questions"):
    with st.spinner("AI is analyzing..."):
        st.session_state.ai_questions = generate_ai_quiz(up_file)

if "ai_questions" in st.session_state:
    with st.form("quiz"):
        score = 0
        for i, q in enumerate(st.session_state.ai_questions):
            st.write(f"**{i+1}. {q['q']}**")
            ans = st.radio("Select:", q['o'], key=f"q{i}")
            if ans == q['a']: score += 1
        if st.form_submit_button("Submit"):
            st.success(f"Score: {score}/{len(st.session_state.ai_questions)}")