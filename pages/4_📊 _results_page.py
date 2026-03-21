import streamlit as st
import sys, os
from collections import defaultdict
from datetime import datetime
import pandas as pd

# Path fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sidebar import render_sidebar
from database import get_scores_by_user
from result_components.visualizations import render_visualizations
from result_components.comparison import render_chapter_comparison
from result_components.pdf_report import render_pdf_report

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

render_sidebar()
st.title("📊 Student Performance Dashboard")

username = st.session_state.get("name", "student")
selected_subject = st.session_state.get("selected_subject")

# Get data
subject_data_raw = get_scores_by_user(username)

if not subject_data_raw:
    st.info("📭 No quiz attempts yet. Start taking quizzes to see your performance!")
    st.stop()

# Organize data
subject_wise_data = defaultdict(list)
chapter_wise_data = defaultdict(lambda: defaultdict(list))

for subject, chapter, score, total in subject_data_raw:
    subject_wise_data[subject].append((score, total))
    chapter_wise_data[subject][chapter].append((score, total))

# Subject-wise analysis if no subject selected
if not selected_subject:
    st.subheader("📚 Subject-wise Performance Overview")
    
    subject_summary = []
    for subject, attempts in subject_wise_data.items():
        total_score = sum(s for s, t in attempts)
        total_questions = sum(t for s, t in attempts)
        accuracy = (total_score / total_questions * 100) if total_questions > 0 else 0
        
        subject_summary.append({
            "Subject": subject,
            "Attempts": len(attempts),
            "Accuracy": f"{accuracy:.1f}%",
            "Questions": f"{total_score}/{total_questions}",
            "Status": "✅ On Track" if accuracy >= 60 else "⚠️ Needs Focus"
        })
    
    st.dataframe(pd.DataFrame(subject_summary), use_container_width=True)
    st.info("💡 **Tip:** Select a subject from the sidebar to dive deeper into chapter-wise analysis.")
    st.stop()

# Process selected subject
if selected_subject not in chapter_wise_data:
    st.info(f"No attempts yet for {selected_subject}")
    st.stop()

chapters_data = chapter_wise_data[selected_subject]

# Calculate totals
total_score = 0
total_questions = 0
for chapter_attempts in chapters_data.values():
    for score, total in chapter_attempts:
        total_score += score
        total_questions += total

accuracy = (total_score / total_questions * 100) if total_questions > 0 else 0
subject_attempts = [attempt for attempt in subject_data_raw if attempt[0] == selected_subject]
total_attempts = len(subject_attempts)

# Create progress data
progress_data = []
for subject, chapter, score, total in subject_data_raw:
    if subject == selected_subject:
        progress_data.append({
            "Attempt": len(progress_data) + 1,
            "Chapter": chapter,
            "Percentage": (score/total)*100
        })

# Calculate chapter stats
chapters_list = list(chapters_data.keys())
chapter_stats = []

for chapter in chapters_list:
    attempts = chapters_data[chapter]
    avg_score = sum(s/t for s, t in attempts) / len(attempts) * 100
    latest_score, latest_total = attempts[0]
    latest_pct = (latest_score / latest_total) * 100
    best_score = max(s/t for s, t in attempts) * 100
    
    chapter_stats.append({
        "Chapter": chapter,
        "Average": avg_score,
        "Latest": latest_pct,
        "Best": best_score,
        "Attempts": len(attempts),
        "Status": "Strong" if avg_score >= 70 else "Needs Work" if avg_score < 50 else "Developing"
    })

# Header with metrics
st.header(f"📘 {selected_subject}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Attempts", total_attempts)
with col2:
    st.metric("Questions Answered", total_questions)
with col3:
    st.metric("Overall Accuracy", f"{accuracy:.1f}%", f"{accuracy - 60:.1f}%" if accuracy != 60 else None)
with col4:
    st.metric("Correct Answers", f"{total_score}/{total_questions}")

st.divider()

# Detailed Chapter Analysis
st.subheader("📚 Detailed Chapter Analysis")

tabs = st.tabs([f"📖 {chapter}" for chapter in chapters_list])

for tab, chapter in zip(tabs, chapters_list):
    with tab:
        attempts = chapters_data[chapter]
        avg_score = sum(s/t for s, t in attempts) / len(attempts) * 100
        latest_score, latest_total = attempts[0]
        latest_pct = (latest_score / latest_total) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Latest Score", f"{latest_score}/{latest_total}", f"{latest_pct:.1f}%")
        with col2:
            st.metric("Average Score", f"{avg_score:.1f}%")
        with col3:
            best = max(s/t for s, t in attempts) * 100
            st.metric("Best Score", f"{best:.1f}%")
        
        st.progress(latest_pct / 100)
        
        with st.expander("📜 View Complete Quiz History"):
            history_data = []
            for i, (s, t) in enumerate(attempts):
                pct = (s/t) * 100
                history_data.append({
                    "Attempt": i + 1,
                    "Score": f"{s}/{t}",
                    "Percentage": f"{pct:.1f}%",
                    "Status": "✅ Pass" if pct >= 50 else "❌ Needs Improvement"
                })
            st.dataframe(pd.DataFrame(history_data), use_container_width=True)

st.divider()

# Comparison component
render_chapter_comparison(chapters_data, chapters_list)
st.divider()

# Visualizations component
render_visualizations(chapter_stats, progress_data, chapters_data, chapters_list, selected_subject)
st.divider()

# Weak areas
st.subheader("⚠️ Areas for Improvement")

weak_chapters = [stat["Chapter"] for stat in chapter_stats if stat["Average"] < 50]
developing_chapters = [stat["Chapter"] for stat in chapter_stats if 50 <= stat["Average"] < 70]

if weak_chapters:
    st.error(f"🔴 **Critical Focus Areas ({len(weak_chapters)} chapters)**")
    for ch in weak_chapters:
        st.write(f"- **{ch}**")
    st.markdown("**Recommended Actions:** Review fundamentals, seek help, and retake quizzes.")
    
if developing_chapters:
    st.warning(f"🟡 **Developing Areas ({len(developing_chapters)} chapters)**")
    for ch in developing_chapters:
        st.write(f"- **{ch}**")
    st.markdown("**Recommended Actions:** Regular practice and focused revision.")
    
if not weak_chapters and not developing_chapters:
    st.success("🎉 **Excellent!** You're performing well in all chapters. Keep up the great work!")

st.divider()

# PDF Report component
render_pdf_report(username, selected_subject, total_attempts, total_questions, total_score, accuracy, chapter_stats)

st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")