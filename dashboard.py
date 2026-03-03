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

CHAPTERS = {
    "Algebra": ["Linear Equations", "Quadratic Equations"],
    "Geometry": ["Triangles", "Circles"],
    "Science": ["Motion", "Force"]
}

def dashboard():

    # ---------------- SESSION INIT ----------------
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False

    # ---------------- SIDEBAR ----------------
    with st.sidebar:
        st.title("📚 GyaanSetu")

        st.write("Name:", st.session_state.name)
        st.write("Class:", st.session_state.user_class)
        st.write("Points:", st.session_state.points)

        st.divider()

        selected_chapter = st.radio(
            "Select Chapter",
            list(CHAPTERS.keys()),
            key="chapter_radio"
        )

        selected_module = st.radio(
            "Select Module",
            CHAPTERS[selected_chapter],
            key="module_radio"
        )

        st.divider()

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.quiz_started = False
            st.rerun()

    # ---------------- MAIN PAGE ----------------
    st.title("Dashboard")
    st.write(f"Welcome, **{st.session_state.name}**")
    st.write("Selected Module:", selected_module)

    st.divider()

    # ---------------- START QUIZ ----------------
    if not st.session_state.quiz_started:
        if st.button("Start Quiz"):
            st.session_state.quiz_started = True
            st.rerun()

    # ---------------- QUIZ (FORM – IMPORTANT) ----------------
    if st.session_state.quiz_started:
        st.subheader("📝 Quiz")

        with st.form("quiz_form"):
            start_quiz()
            submitted = st.form_submit_button("Submit Quiz")

        if submitted:
            st.success("Quiz submitted successfully 🎉")

            if st.button("End Quiz"):
                st.session_state.quiz_started = False
                st.session_state.answers = {}
                st.rerun()