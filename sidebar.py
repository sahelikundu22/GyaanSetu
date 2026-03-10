"""
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
"""

import streamlit as st
import json

# We remove @st.cache_data so it updates instantly when you edit the JSON
def load_curriculum():
    try:
        with open('cbse_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data["cbse_curriculum_2024_26"]
    except Exception as e:
        st.error(f"Error loading JSON: {e}")
        return {}

def render_sidebar():
    curriculum = load_curriculum()
    
    with st.sidebar:
        st.title("📚 GyaanSetu")
        st.markdown("---")
        
        # User details from session state
        name = st.session_state.get('name', 'Student')
        u_class = st.session_state.get('user_class', '5')
        points = st.session_state.get('points', 0)
        
        st.write(f"**User:** {name}")
        st.write(f"**Class:** {u_class}")
        st.write(f"**Points:** {points}")
        st.markdown("---")

        # Class selection logic
        user_class_key = f"class_{u_class}"
        
        if user_class_key in curriculum:
            class_data = curriculum[user_class_key]
            subjects = list(class_data["subjects"].keys())
            
            # Subject Dropdown
            selected_subject = st.selectbox("Select Subject", subjects, key="sidebar_subject")
            
            # Get all chapters for that subject
            chapters_data = class_data["subjects"][selected_subject]
            chapter_names = [item["chapter"] for item in chapters_data]
            
            # Chapter Dropdown - Now showing all chapters in the list
            selected_chapter = st.selectbox("Select Chapter", chapter_names, key="sidebar_chapter")
            
            # Safely get YouTube link (prevents StopIteration error if link is missing)
            selected_yt_link = ""
            for item in chapters_data:
                if item["chapter"] == selected_chapter:
                    selected_yt_link = item.get("yt", "")
                    break
            
            # Store in session state for other pages to use
            st.session_state.selected_subject = selected_subject
            st.session_state.selected_chapter = selected_chapter
            st.session_state.selected_yt_link = selected_yt_link
        else:
            st.warning(f"No data found for Class {u_class}")

        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()