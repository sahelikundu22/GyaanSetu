import streamlit as st
from quizdata import QUIZ_DATA

def start_quiz(subject, chapter):
    st.subheader(f"📝 {subject} – {chapter} Quiz")

    questions = QUIZ_DATA.get(subject, {}).get(chapter, [])

    if not questions:
        st.warning("No quiz available for this chapter.")
        return

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q['question']}**")

        options = ["-- Select an answer --"] + q["options"]

        selected = st.selectbox(
            "Choose your answer",
            options,
            key=f"{subject}_{chapter}_q{i}"
        )

        if selected != "-- Select an answer --":
            st.session_state.answers[i] = selected

    st.divider()

    if st.button("Submit Quiz"):
        score = 0

        for i, q in enumerate(questions):
            if st.session_state.answers.get(i) == q["answer"]:
                score += 1

        st.success(f"✅ Your Score: {score} / {len(questions)}")