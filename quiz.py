import streamlit as st
from quiz_data import QUIZ

def start_quiz():
    st.subheader("📝 Motion – Quiz")

    score = 0
    answers = {}

    for i, q in enumerate(QUIZ):
        st.write(f"Q{i+1}. {q['question']}")

        answers[i] = st.radio(
            label="Choose one:",
            options=q["options"],
            key=f"question_{i}"
        )

    if st.button("Submit Quiz"):
        for i, q in enumerate(QUIZ):
            if answers[i] == q["answer"]:
                score += 1

        st.success(f"Your score: {score} / {len(QUIZ)}")