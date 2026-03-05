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
from book_pdf_viewer import show_book_pdf

# Dummy chapter data (can be replaced with DB later)
CHAPTERS = {
    "Maths": ["Linear Equations", "Quadratic Equations"],
    "English": ["Triangles", "Circles"],
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

        # THREE MAIN OPTIONS - LAYOUT
        st.markdown("### 🔧 Learning Tools")

        if st.button("📖 Study Material", use_container_width=True):
            st.session_state.selected_option = "Study Material"
              
        if st.button("❓ Quiz", use_container_width=True):
            st.session_state.selected_option = "Quiz"
            
        if st.button("📄 PDF Q&A", use_container_width=True):
            st.session_state.selected_option = "PDF Q&A"

        # currently selected option
        if st.session_state.selected_option == "Study Material":
            st.info("✅ Viewing: Study Material")
        elif st.session_state.selected_option == "Quiz":
            st.info("✅ Viewing: Quiz")
        elif st.session_state.selected_option == "PDF Q&A":
            st.info("✅ Viewing: PDF Q&A")

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


    # needs to modify the page based on which option is selected ...

    if st.session_state.selected_option == "Study Material":
        st.subheader("Study Material")

        with st.expander("Chapeter Notes", expanded=True):
            st.write(f"Here are the study notes for **{selected_module}** from **{selected_chapter}**:")
            st.markdown("""
            - The study material is taken from the **NCERT textbook PDF**.
            - It follows the **official NCERT syllabus and chapter structure**.
            - The content is provided for **concept understanding and exam preparation**.
            """)

        if st.button("📘 View Book (PDF)", use_container_width=True):
            show_book_pdf(selected_chapter, selected_module)

    elif st.session_state.selected_option == "Quiz":
        st.subheader("Quiz")

        # ---------------- QUIZ CONTROLS ----------------
        if not st.session_state.quiz_started:
            if st.button("Start Quiz", use_container_width=True):
                st.session_state.quiz_started = True
                st.session_state.answers = {}
                st.rerun()

        # ---------------- QUIZ AREA ----------------
        if st.session_state.quiz_started:
            start_quiz(selected_chapter, selected_module)

        st.divider()

        if st.button("End Quiz", use_container_width=True):
            st.session_state.quiz_started = False
            st.session_state.answers = {}
            st.rerun()

    
    elif st.session_state.selected_option == "PDF Q&A": # pdf qna
        st.subheader("PDF Q&A")

        with st.expander("How it Works", expanded=True):
            st.write("""
            - Upload a PDF document to enable document-based question answering.  
            - The PDF text is segmented into chunks and converted into embeddings, which are stored in a vector database.  
            - For each query, semantic similarity search retrieves the most relevant chunks and Gemini generates a context-aware response.
            """)