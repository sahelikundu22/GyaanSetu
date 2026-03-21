import streamlit as st
import sys, os
from datetime import datetime
import pandas as pd

# Path fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sidebar import render_sidebar
from database import get_scores_by_user
from result_components.data_utils import *
from result_components.subject_analysis import render_subject_analysis
from result_components.chapter_analysis import render_chapter_analysis
from result_components.chapter_comparison import render_chapter_comparison
from result_components.visualizations import render_visualizations
from result_components.weak_areas import render_weak_areas
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
subject_wise_data, chapter_wise_data = organize_data(subject_data_raw)

# Subject-wise analysis if no subject selected
if not selected_subject:
    subject_summary = calculate_subject_stats(subject_wise_data)
    render_subject_analysis(subject_summary)
    st.stop()

# Process selected subject data
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
progress_data = create_progress_data(subject_data_raw, selected_subject)

# Calculate chapter stats
chapter_stats, chapters_list = calculate_chapter_stats(chapters_data)

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

# Render all components
chapter_stats = render_chapter_analysis(chapters_data, chapters_list)
st.divider()

render_chapter_comparison(chapters_data, chapters_list)
st.divider()

render_visualizations(chapter_stats, progress_data, chapters_data, chapters_list, selected_subject)
st.divider()

# Weak areas and PDF report
df_chapters = pd.DataFrame(chapter_stats) if chapter_stats else pd.DataFrame()
weak_chapters = df_chapters[df_chapters["Average"] < 50]["Chapter"].tolist() if not df_chapters.empty else []
developing_chapters = df_chapters[(df_chapters["Average"] >= 50) & (df_chapters["Average"] < 70)]["Chapter"].tolist() if not df_chapters.empty else []

render_weak_areas(chapter_stats)
st.divider()

render_pdf_report(username, selected_subject, total_attempts, total_questions, total_score, accuracy, 
                  chapter_stats, weak_chapters, developing_chapters)

st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")