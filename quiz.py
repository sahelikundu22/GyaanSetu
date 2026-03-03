import streamlit as st
from quizdata import QUIZ

def start_quiz():
    st.subheader("📝 Motion – Quiz")

    score = 0

    for i, q in enumerate(QUIZ):
        st.write(f"Q{i+1}. {q['question']}")
        ans = st.radio(
            "Select answer",
            q["options"],
            key=i
        )

        if ans == q["answer"]:
            score += 1

    if st.button("Submit Quiz"):
        st.success(f"Your score: {score} / {len(QUIZ)}")