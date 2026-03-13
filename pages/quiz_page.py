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

# PATH FIX: Allow finding sidebar and quiz_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sidebar import render_sidebar

# Import utility safely
try:
    from quiz_utils import generate_ai_quiz
except ImportError:
    st.error("Error: quiz_utils.py not found in main directory.")

st.set_page_config(page_title="AI Quiz")
render_sidebar()

st.title("🤖 AI Quiz Generator")
st.write("Upload a PDF to generate a practice quiz instantly.")

up_file = st.file_uploader("Upload PDF", type="pdf")

if up_file and st.button("Generate AI Quiz", use_container_width=True):
    with st.spinner("AI is analyzing content..."):
        questions = generate_ai_quiz(up_file)
        if "error" not in questions:
            st.session_state.ai_quiz_data = questions
            st.success("Quiz Generated!")
        else:
            st.error(f"Error: {questions['error']}")

if "ai_quiz_data" in st.session_state:
    score = 0
    with st.form("ai_form"):
        for i, q in enumerate(st.session_state.ai_quiz_data):
            st.write(f"**{i+1}. {q['q']}**")
            user_ans = st.radio("Choose:", q['o'], key=f"ai_q_{i}")
            if user_ans == q['a']:
                score += 1
        
        if st.form_submit_button("Submit Quiz"):
            st.success(f"Final Score: {score} / {len(st.session_state.ai_quiz_data)}")
            if score == len(st.session_state.ai_quiz_data):
                st.balloons()