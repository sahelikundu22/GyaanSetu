import streamlit as st
import sys, os

# fixing default page
if not st.session_state.get("logged_in", False):
    st.warning("Please login to access this page.")
    st.stop()
# Allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sidebar import render_sidebar
from quiz_utils import generate_ai_quiz
from database import save_quiz_score


st.set_page_config(page_title="AI Quiz", layout="wide")

render_sidebar()

st.title("🤖 AI Quiz Generator")
st.write("Select the subject and chapter from sidebar to generate quiz.")

# ---------- CSS FOR QUIZ UI ----------
st.markdown("""
<style>

.correct-answer {
    background-color:#c8f7c5;
    color:black !important;
    padding:10px;
    border-radius:6px;
    margin:4px 0;
    font-weight:600;
}

.wrong-answer {
    background-color:#ffcdd2;
    color:black !important;
    padding:10px;
    border-radius:6px;
    margin:4px 0;
    font-weight:600;
}

.neutral-answer {
    padding:8px;
}

</style>
""", unsafe_allow_html=True)


# ---------- Generate Quiz from Study Material ----------

subject = st.session_state.get("selected_subject", "")
chapter = st.session_state.get("selected_chapter", "")

pdf_path = None

# Find PDF same way as study_material page
sub_folder = os.path.join("study_material", subject)

if os.path.exists(sub_folder):
    target = chapter.lower().replace(" ", "")
    for f in os.listdir(sub_folder):
        if f.lower().replace(" ", "").startswith(target):
            pdf_path = os.path.join(sub_folder, f)
            break


if st.button("🧠 Generate Quiz", use_container_width=True):

    if not pdf_path:
        st.error("❌ PDF not found for this chapter")
    else:
        with st.spinner("Generating quiz from chapter..."):

            quiz = generate_ai_quiz(open(pdf_path, "rb"), num_q=10)

            if isinstance(quiz, dict) and "error" in quiz:
                st.error(quiz["error"])
            else:
                st.session_state.ai_quiz = quiz
                st.session_state.quiz_submitted = False
                st.success("✅ Quiz generated successfully!")

# ---------- SHOW QUIZ ----------

if "ai_quiz" in st.session_state and not st.session_state.get("quiz_submitted", False):

    questions = st.session_state.ai_quiz

    st.subheader("📝 Practice Quiz")

    with st.form("quiz_form"):

        user_answers = []

        for i, q in enumerate(questions):

            st.markdown(f"### Q{i+1}. {q['q']}")

            ans = st.radio(
                "Select your answer:",
                q["o"],
                key=f"q{i}"
            )

            user_answers.append(ans)

        submitted = st.form_submit_button("Submit Quiz")

    if submitted:
        st.session_state.quiz_submitted = True
        st.session_state.user_answers = user_answers


# ---------- SHOW RESULTS ----------

if "ai_quiz" in st.session_state and st.session_state.get("quiz_submitted"):

    questions = st.session_state.ai_quiz
    user_answers = st.session_state.user_answers

    score = 0

    st.subheader("📊 Quiz Results")
    st.divider()

    for i, q in enumerate(questions):

        correct = q["a"]
        user = user_answers[i]

        st.markdown(f"### Q{i+1}. {q['q']}")

        for option in q["o"]:

            if option == correct:

                st.markdown(
                    f"<div class='correct-answer'>✅ {option}</div>",
                    unsafe_allow_html=True
                )

            elif option == user and user != correct:

                st.markdown(
                    f"<div class='wrong-answer'>❌ {option}</div>",
                    unsafe_allow_html=True
                )

            else:
                st.markdown(
                    f"<div class='neutral-answer'>{option}</div>",
                    unsafe_allow_html=True
                )

        if user == correct:
            score += 1

        st.divider()

    total = len(questions)

    st.success(f"🎯 Final Score: {score} / {total}")

    if score == total:
        st.balloons()


    # ---------- SAVE SCORE TO DATABASE ----------

    save_quiz_score(
        st.session_state.get("name", "student"),
        st.session_state.get("selected_subject", "General"),
        st.session_state.get("selected_chapter", "Chapter"),
        score,
        total
    )