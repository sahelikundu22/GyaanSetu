import streamlit as st
import sys, os
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

# Path fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sidebar import render_sidebar
from database import get_scores_by_user


st.set_page_config(page_title="Quiz Report", layout="wide")

render_sidebar()

st.title("📊 Subject Performance Report")

username = st.session_state.get("name", "student")
selected_subject = st.session_state.get("selected_subject")

data = get_scores_by_user(username)

if not data:
    st.info("No quiz attempts yet.")
    st.stop()

if not selected_subject:
    st.warning("Please select a subject from sidebar.")
    st.stop()


# ---------- FILTER DATA FOR SELECTED SUBJECT ----------

subject_data = []

for subject, chapter, score, total in data:
    if subject == selected_subject:
        subject_data.append((chapter, score, total))


if not subject_data:
    st.info(f"No attempts yet for {selected_subject}")
    st.stop()


# ---------- ORGANIZE DATA ----------

chapters = defaultdict(list)

total_score = 0
total_questions = 0

for chapter, score, total in subject_data:
    chapters[chapter].append((score, total))
    total_score += score
    total_questions += total


st.header(f"📘 {selected_subject}")

# ---------- METRICS AND OVERALL QUIZ HISTORY IN SAME DIVIDER ----------
st.subheader("📊 Performance Overview & Quiz History")

# Metrics in 4 columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Attempts", len(subject_data))

with col2:
    st.metric("Total Questions", total_questions)

with col3:
    accuracy = (total_score / total_questions * 100) if total_questions > 0 else 0
    st.metric("Overall Accuracy", f"{accuracy:.1f}%", f"{accuracy - 50:.1f}%")

with col4:
    st.metric("Questions Correct", f"{total_score}/{total_questions}")

# Overall quiz history table
st.write("")  # Add some spacing
overall_history = []
for i, (chapter, score, total) in enumerate(subject_data):
    percentage = (score / total) * 100
    status = "✅ Pass" if percentage >= 50 else "❌ Needs Improvement"
    overall_history.append({
        "S.No": i + 1,
        "Chapter": chapter,
        "Score": f"{score}/{total}",
        "Percentage": f"{percentage:.1f}%",
        "Status": status
    })

overall_df = pd.DataFrame(overall_history)
st.dataframe(overall_df, use_container_width=True)

st.divider()

# ---------- DETAILED CHAPTER ANALYSIS (TAB VERSION WITH TABLES) ----------
st.subheader("📚 Detailed Chapter Analysis")

# Create tabs for each chapter
tabs = st.tabs([f"📖 {chapter}" for chapter in chapters.keys()])

chapter_names = []
avg_scores = []
weak_topics = []

for tab, chapter in zip(tabs, chapters.keys()):
    with tab:
        attempts = chapters[chapter]
        
        # Calculate average score
        avg = sum(s/t for s, t in attempts) / len(attempts)
        percentage = int(avg * 100)
        
        chapter_names.append(chapter)
        avg_scores.append(percentage)
        
        if percentage < 50:
            weak_topics.append(chapter)
        
        # Display chapter statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            latest_score, latest_total = attempts[0]
            latest_pct = int((latest_score / latest_total) * 100)
            st.metric("Latest Score", f"{latest_score}/{latest_total}", f"{latest_pct}%")
        
        with col2:
            st.metric("Average Score", f"{percentage}%")
        
        with col3:
            best_score = max([(s/t) for s, t in attempts]) * 100
            st.metric("Best Score", f"{best_score:.0f}%")
        
        # Progress bar for latest score
        st.progress(latest_pct)
        
        # Quiz history table
        with st.expander("📜 View Complete Quiz History"):
            # Create dataframe for quiz history
            history_data = []
            for i, (s, t) in enumerate(attempts):
                pct = (s/t) * 100
                status = "✅ Pass" if pct >= 50 else "❌ Needs Improvement"
                history_data.append({
                    "Attempt": i + 1,
                    "Score": f"{s}/{t}",
                    "Percentage": f"{pct:.1f}%",
                    "Status": status
                })
            
            history_df = pd.DataFrame(history_data)
            st.dataframe(history_df, use_container_width=True)
        
        st.divider()

st.divider()

# ---------- 4 FIGURES IN 2 COLUMNS ----------
st.subheader("📊 Performance Visualizations")

# Row 1: Pie Chart and Bar Chart
col1, col2 = st.columns(2)

with col1:
    st.subheader("Overall Performance")
    correct = total_score
    incorrect = total_questions - total_score
    
    fig1 = plt.figure()
    plt.pie([correct, incorrect], labels=["Correct", "Incorrect"], autopct="%1.1f%%")
    plt.title(f"{selected_subject} Accuracy")
    st.pyplot(fig1)

with col2:
    st.subheader("Chapter-wise Performance")
    fig2 = plt.figure()
    plt.bar(chapter_names, avg_scores)
    plt.xlabel("Chapters")
    plt.ylabel("Score (%)")
    plt.title(f"{selected_subject} Performance")
    plt.ylim(0, 100)
    st.pyplot(fig2)

# Row 2: Performance Over Time and Chapter-wise Progress
col3, col4 = st.columns(2)

with col3:
    st.subheader("Performance Over Time")
    
    attempt_numbers = []
    scores_percent = []
    
    for i, (chapter, score, total) in enumerate(subject_data[::-1]):
        attempt_numbers.append(i + 1)
        percentage = int((score / total) * 100)
        scores_percent.append(percentage)
    
    fig3 = plt.figure()
    plt.plot(attempt_numbers, scores_percent, marker='o')
    plt.xlabel("Attempt Number")
    plt.ylabel("Score (%)")
    plt.title(f"{selected_subject} Progress Over Time")
    plt.xticks(attempt_numbers)
    plt.ylim(0, 100)
    st.pyplot(fig3)

with col4:
    st.subheader("Chapter-wise Progress Over Time")
    
    chapter_attempts = defaultdict(list)
    
    for chapter, score, total in subject_data[::-1]:
        percentage = int((score / total) * 100)
        chapter_attempts[chapter].append(percentage)
    
    fig4 = plt.figure()
    
    for chapter in chapter_attempts:
        scores = chapter_attempts[chapter]
        attempts = list(range(1, len(scores) + 1))
        plt.plot(attempts, scores, marker='o', label=chapter)
    
    plt.xlabel("Attempt Number")
    plt.ylabel("Score (%)")
    plt.title(f"{selected_subject} Chapter-wise Progress")
    plt.legend()
    plt.grid(True)
    plt.ylim(0, 100)
    
    st.pyplot(fig4)

# ---------- WEAK TOPICS ----------
st.subheader("⚠️ Weak Topics")

if weak_topics:
    for topic in weak_topics:
        st.error(f"{topic}")
else:
    st.success("No weak topics 🎉")