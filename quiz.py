import streamlit as st
from quizdata import QUIZ

def start_quiz():
    st.subheader("📝 Motion – Quiz")

    # Initialize answers dict once
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    # Render questions
    for i, q in enumerate(QUIZ):
        st.markdown(f"**Q{i+1}. {q['question']}**")

        options = ["-- Select an answer --"] + q["options"]

        selected = st.selectbox(
            "Choose your answer",
            options,
            key=f"quiz_q_{i}"
        )

        # Save only valid answers
        if selected != "-- Select an answer --":
            st.session_state.answers[i] = selected

    st.divider()

    # Submit button
    if st.button("Submit Quiz", key="submit_quiz"):
        score = 0
        unanswered = 0

        for i, q in enumerate(QUIZ):
            if i not in st.session_state.answers:
                unanswered += 1
            elif st.session_state.answers[i] == q["answer"]:
                score += 1

        if unanswered > 0:
            st.warning(f"Please answer all questions ({unanswered} left).")
        else:
            st.success(f"✅ Your Score: {score} / {len(QUIZ)}")