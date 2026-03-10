import streamlit as st
import json

def load_curriculum():
    try:
        with open('cbse_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data["cbse_curriculum_2024_26"]
    except:
        return {}

def render_sidebar():
    curriculum = load_curriculum()
    
    with st.sidebar:
        st.title("📚 GyaanSetu")
        st.write(f"**User:** {st.session_state.get('name', 'Student')}")
        st.write(f"**Class:** {st.session_state.get('user_class', '5')}")
        st.markdown("---")

        user_class_key = f"class_{st.session_state.get('user_class', '5')}"
        
        if user_class_key in curriculum:
            class_data = curriculum[user_class_key]
            subjects = list(class_data["subjects"].keys())
            
            # Subject Selection
            selected_subject = st.selectbox("Select Subject", subjects, key="sb_sub")
            
            # Chapter Selection
            chapters_list = class_data["subjects"][selected_subject]
            chapter_names = [c["chapter"] for c in chapters_list]
            selected_chapter = st.selectbox("Select Chapter", chapter_names, key="sb_ch")
            
            # Find matching YT link
            yt_link = ""
            for c in chapters_list:
                if c["chapter"] == selected_chapter:
                    yt_link = c.get("yt", "")
                    break
            
            # Update Session State
            st.session_state.selected_subject = selected_subject
            st.session_state.selected_chapter = selected_chapter
            st.session_state.selected_yt_link = yt_link
        
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()