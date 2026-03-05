import streamlit as st
from pages.study_material import study_material_page
from pages.quiz_page import quiz_page
from pages.pdf_qna import pdf_qna_page

# Dummy chapter data (can be replaced with DB/JSON later)
CHAPTERS = {
    "Maths": ["Linear Equations", "Quadratic Equations"],
    "English": ["Triangles", "Circles"],
    "Science": ["Motion", "Force"]
}

def dashboard():
    # session state initalization
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False

    if "answers" not in st.session_state:
        st.session_state.answers = {}
    
    
    if "page" not in st.session_state:
        st.session_state.page = "Study Material"  # initialization error fixed

    # SIDEBAR
    with st.sidebar:
        st.title("📚 GyaanSetu")

        st.markdown("---")
        st.write("**User Info**")
        st.write("Name:", st.session_state.name)
        st.write("Class:", st.session_state.user_class)
        st.write("Points:", st.session_state.points)

        st.markdown("---")

        st.markdown("### 🔧 Learning Tools")
        
        if st.button("📖 Study Material", use_container_width=True):
            st.session_state.page = "Study Material"
            st.rerun()
        
        if st.button("❓ Quiz", use_container_width=True):
            st.session_state.page = "Quiz"
            st.rerun()
        
        if st.button("📄 PDF Q&A", use_container_width=True):
            st.session_state.page = "PDF Q&A"
            st.rerun()
        
        st.info(f"📍 Current page: **{st.session_state.page}**")

        st.markdown("---")

        selected_chapter = st.selectbox(
            "Select Chapter",
            list(CHAPTERS.keys()),
            key="sidebar_chapter"
        )

        selected_module = st.selectbox(
            "Select Module",
            CHAPTERS[selected_chapter],
            key="sidebar_module"
        )

        st.markdown("---")

        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.quiz_started = False
            st.session_state.answers = {}
            st.rerun()



    # MAIN CONTENT
    st.markdown(
        "<h1 style='text-align:center;'>Dashboard</h1>",
        unsafe_allow_html=True
    )

    st.write(f"### Welcome, {st.session_state.name}")
    st.write("Class:", st.session_state.user_class)
    st.write("Points:", st.session_state.points)

    st.divider()

    st.subheader("Selected Path")
    st.write(f"**Chapter:** {selected_chapter}")
    st.write(f"**Module:** {selected_module}")

    st.divider()



    # page routing
    if st.session_state.page == "Study Material":
        study_material_page(selected_chapter, selected_module)
    
    elif st.session_state.page == "Quiz":
        quiz_page(selected_chapter, selected_module)
    
    elif st.session_state.page == "PDF Q&A":
        pdf_qna_page(selected_chapter, selected_module)
    
    st.divider()
    
    st.caption(f"Current chapter: {selected_chapter} | Current module: {selected_module}")