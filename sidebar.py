import streamlit as st
import json

@st.cache_data
def load_curriculum():
    with open('cbse_data.json', 'r') as file:
        data = json.load(file)
    return data["cbse_curriculum_2024_26"]

def render_sidebar():
    curriculum = load_curriculum()
    
    with st.sidebar:
        st.title("📚 GyaanSetu")
        st.markdown("---")
        st.write("**User Info**")
        st.write("Name:", st.session_state.name)
        st.write("Class:", st.session_state.user_class)
        st.write("Points:", st.session_state.points)
        st.markdown("---")

        # Class selection
        user_class_key = f"class_{st.session_state.user_class}"
        
        if user_class_key in curriculum:
            class_data = curriculum[user_class_key]
            subjects = list(class_data["subjects"].keys())
            
            selected_subject = st.selectbox("Subject", subjects, key="sidebar_subject")
            chapters_data = class_data["subjects"][selected_subject]
            chapter_names = [item["chapter"] for item in chapters_data]
            selected_chapter = st.selectbox("Chapter", chapter_names, key="sidebar_chapter")
            
            # Get YouTube link
            selected_yt_link = next(item["yt"] for item in chapters_data if item["chapter"] == selected_chapter)
            
            # Store in session state
            st.session_state.selected_subject = selected_subject
            st.session_state.selected_chapter = selected_chapter
            st.session_state.selected_yt_link = selected_yt_link
            st.session_state.user_class_key = user_class_key

        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()