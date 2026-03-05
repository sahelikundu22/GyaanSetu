import streamlit as st
from quiz import start_quiz

def quiz_page(selected_chapter, selected_module):
    """Quiz Page"""
    st.subheader("❓ Quiz")

    if not st.session_state.quiz_started:
        if st.button("Start Quiz", use_container_width=True):
            st.session_state.quiz_started = True
            st.session_state.answers = {}
            st.rerun()

    if st.session_state.quiz_started:
        start_quiz(selected_chapter, selected_module)

    st.divider()

    if st.button("End Quiz", use_container_width=True):
        st.session_state.quiz_started = False
        st.session_state.answers = {}
        st.rerun()