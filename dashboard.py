"""
import streamlit as st
from quiz import start_quiz

    
# Dummy Data --- Replace it by DB/ JSON
CHAPTERS = {
    "Algebra": ["Linear Equations", "Quadratic Equations"],
    "Geometry": ["Triangles", "Circles"],
    "Science": ["Motion", "Force"]
}
def dashboard():

    with st.sidebar:

        st.title("📚 GyaanSetu 📚")

        st.markdown("---")
        st.write("**User Info**")
        st.write("Name:", st.session_state.name)
        st.write("Class:", st.session_state.user_class)
        st.write("Points:", st.session_state.points)

        st.markdown("---")

        st.subheader("Select Chapter")
        selected_chapter = st.radio(
            "Chapters",
            list(CHAPTERS.keys())
        )

        st.subheader("Select Module")
        selected_module = st.radio(
            "Modules",
            CHAPTERS[selected_chapter]
        )

        st.markdown("---")

        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()


    # main page area
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

    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False

    if st.button("Start Quiz", use_container_width=True):
        st.success(f"Starting Quiz for {selected_module}")
        st.session_state.quiz_started = True

    quiz_container = st.container()

    if st.session_state.quiz_started:
        with quiz_container:
            start_quiz()"""


import streamlit as st
from quiz import start_quiz

# Dummy chapter data (can be replaced with DB later)
CHAPTERS = {
    "Algebra": ["Linear Equations", "Quadratic Equations"],
    "Geometry": ["Triangles", "Circles"],
    "Science": ["Motion", "Force"]
}

def dashboard():

    # ---------------- SESSION STATE INIT ----------------
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    # ---------------- SIDEBAR ----------------
    with st.sidebar:
        st.title("📚 GyaanSetu")

        st.markdown("---")
        st.write("**User Info**")
        st.write("Name:", st.session_state.name)
        st.write("Class:", st.session_state.user_class)
        st.write("Points:", st.session_state.points)

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

    # ---------------- MAIN CONTENT ----------------
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

    # ---------------- QUIZ CONTROLS ----------------
    if not st.session_state.quiz_started:
        if st.button("Start Quiz", use_container_width=True):
            st.session_state.quiz_started = True
            st.session_state.answers = {}
            st.rerun()

    # ---------------- QUIZ AREA ----------------
    if st.session_state.quiz_started:
        start_quiz()

        st.divider()

        if st.button("End Quiz", use_container_width=True):
            st.session_state.quiz_started = False
            st.session_state.answers = {}
            st.rerun()