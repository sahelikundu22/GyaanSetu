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