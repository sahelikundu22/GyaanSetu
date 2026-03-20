import streamlit as st
import json

def render_sidebar():
    with st.sidebar:
        st.title("📚 GyaanSetu")
        st.write(f"👤 **{st.session_state.get('name', 'Student')}**")
        st.write(f"🎓 **Class {st.session_state.get('user_class', '5')}**")
        st.divider()

        try:
            with open('cbse_data.json', 'r', encoding='utf-8') as f:
                curriculum = json.load(f)["cbse_curriculum_2024_26"]
            
            class_key = f"class_{st.session_state.get('user_class', '5')}"
            subjects = list(curriculum[class_key]["subjects"].keys())
            
            sel_sub = st.selectbox("Select Subject", subjects, key="sb_sub")
            chapters = curriculum[class_key]["subjects"][sel_sub]
            chapter_names = [c["chapter"] for c in chapters]
            sel_ch = st.selectbox("Select Chapter", chapter_names, key="sb_ch")
            
            # Global session updates
            st.session_state.selected_subject = sel_sub
            st.session_state.selected_chapter = sel_ch
            st.session_state.selected_yt_link = next(c["yt"] for c in chapters if c["chapter"] == sel_ch)
            
        except Exception:
            st.info("Select subject details above.")

        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()