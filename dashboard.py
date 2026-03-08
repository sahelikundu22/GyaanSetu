import streamlit as st
from sidebar import render_sidebar

def dashboard():

    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "answers" not in st.session_state:
        st.session_state.answers = {}

  
    render_sidebar()

    st.title("Dashboard")
    st.write(f"Welcome, {st.session_state.name}!")
    
    if st.session_state.get('selected_subject'):
        st.info(f"Current: Class {st.session_state.user_class} | {st.session_state.selected_subject} | {st.session_state.selected_chapter}")
    else:
        st.warning("Select subject and chapter from sidebar")