import streamlit as st
import sys, os
from collections import defaultdict
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sidebar import render_sidebar
from database import get_scores_by_user
from result_components.visualizations import render_visualizations
from result_components.comparison import render_comparison
from result_components.pdf_report import render_pdf_report
from result_components.subject_analysis import render_subject_analysis

st.set_page_config(page_title="Student Dashboard", layout="wide")
render_sidebar()
st.title("📊 Student Performance Dashboard")

username = st.session_state.get("name", "student")
selected_subject = st.session_state.get("selected_subject")
data = get_scores_by_user(username)

if not data:
    st.info("📭 No quiz attempts yet. Start taking quizzes to see your performance!")
    st.stop()

# Organize data
subject_wise = defaultdict(list)
chapter_wise = defaultdict(lambda: defaultdict(list))

for subject, chapter, score, total in data:
    subject_wise[subject].append((score, total))
    chapter_wise[subject][chapter].append((score, total))

# If no subject selected, show subject analysis
if not selected_subject:
    subject_stats = render_subject_analysis(subject_wise)
    st.info("💡 Select a subject from the sidebar to view detailed chapter analysis")
    st.stop()

# Check if selected subject has data
if selected_subject not in chapter_wise:
    st.info(f"No attempts yet for {selected_subject}")
    st.stop()

chapters = chapter_wise[selected_subject]

# Calculate totals
total_score = sum(s for a in chapters.values() for s, t in a)
total_q = sum(t for a in chapters.values() for s, t in a)
accuracy = total_score/total_q*100 if total_q else 0
attempts = len([x for x in data if x[0] == selected_subject])

# Calculate chapter stats
stats = []
for ch, att in chapters.items():
    avg = sum(s/t for s, t in att) / len(att) * 100
    latest = att[0][0]/att[0][1] * 100
    stats.append({
        "Chapter": ch, 
        "Average": avg, 
        "Latest": latest, 
        "Attempts": len(att)  # Make sure this is included
    })
# Header with metrics
st.header(f"📘 {selected_subject}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Attempts", attempts)
c2.metric("Questions", total_q)
c3.metric("Accuracy", f"{accuracy:.1f}%")
c4.metric("Correct", f"{total_score}/{total_q}")

st.divider()

# Chapter tabs with tables
st.subheader("📚 Chapter Analysis")

if stats:
    tabs = st.tabs([f"📖 {s['Chapter']}" for s in stats])
    
    for tab, stat in zip(tabs, stats):
        with tab:
            att = chapters[stat['Chapter']]
            latest = att[0][0]/att[0][1] * 100
            
            # Metrics row
            col1, col2, col3 = st.columns(3)
            col1.metric("Latest", f"{att[0][0]}/{att[0][1]}", f"{latest:.1f}%")
            col2.metric("Average", f"{stat['Average']:.1f}%")
            col3.metric("Best", f"{max(s/t for s, t in att) * 100:.1f}%")
            
            # Progress bar
            st.progress(latest/100)
            
            # Quiz history table
            with st.expander("📜 Quiz History", expanded=True):
                history = []
                for i, (s, t) in enumerate(att):
                    pct = (s/t) * 100
                    history.append({
                        "Attempt": i+1,
                        "Score": f"{s}/{t}",
                        "Percentage": f"{pct:.1f}%",
                        "Status": "✅ Pass" if pct >= 50 else "❌ Needs Work"
                    })
                st.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True)

st.divider()

# Progress data for visualizations
progress = []
for subject, ch, score, total in data:
    if subject == selected_subject:
        progress.append(score/total*100)

# Visualizations
render_visualizations(stats, progress, chapters, list(chapters.keys()), selected_subject)

st.divider()

# Chapter Comparison
render_comparison(chapters, list(chapters.keys()))

st.divider()

# Areas for Improvement
weak = [s["Chapter"] for s in stats if s["Average"] < 50]
developing = [s["Chapter"] for s in stats if 50 <= s["Average"] < 70]
strong = [s["Chapter"] for s in stats if s["Average"] >= 70]

st.subheader("⚠️ Areas for Improvement")

col1, col2, col3 = st.columns(3)
with col1:
    if weak:
        st.error(f"🔴 Need Attention\n{len(weak)} chapters")
        for ch in weak[:3]:
            st.write(f"- {ch}")
        if len(weak) > 3:
            st.write(f"- ... and {len(weak)-3} more")
    else:
        st.success("✅ No weak chapters")
        
with col2:
    if developing:
        st.warning(f"🟡 Developing\n{len(developing)} chapters")
        for ch in developing[:3]:
            st.write(f"- {ch}")
    else:
        st.info("📚 All chapters above 70%")
        
with col3:
    if strong:
        st.success(f"✅ Strong\n{len(strong)} chapters")
        for ch in strong[:3]:
            st.write(f"- {ch}")

st.divider()

# Subject Analysis (for all subjects)
subject_stats = render_subject_analysis(subject_wise)

st.divider()

# PDF Report
render_pdf_report(username, subject_stats, selected_subject, accuracy, stats, weak, developing)

st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")