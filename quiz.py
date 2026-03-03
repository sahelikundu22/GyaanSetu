import streamlit as st
from quizdata import QUIZ

def start_quiz():
    st.subheader("📝 Motion – Quiz")

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    for i, q in enumerate(QUIZ):
        st.write(f"Q{i+1}. {q['question']}")

        st.session_state.answers[i] = st.radio(
            label="Choose one:",
            options=q["options"],
            key=f"question_{i}"
        )

    if st.button("Submit Quiz"):
        score = 0
        for i, q in enumerate(QUIZ):
            if st.session_state.answers[i] == q["answer"]:
                score += 1

        st.success(f"Your score: {score} / {len(QUIZ)}")