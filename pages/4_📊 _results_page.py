import streamlit as st
import sys, os
from collections import defaultdict
from datetime import datetime
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sidebar import render_sidebar
from database import get_scores_by_user
from result_components.visualizations import render_visualizations
from result_components.comparison import render_comparison
from result_components.pdf_report import render_pdf_report
from result_components.subject_analysis import render_subject_analysis

st.set_page_config(page_title="Dashboard", layout="wide")
render_sidebar()
st.title("📊 Student Report")

username = st.session_state.get("name", "student")
selected_subject = st.session_state.get("selected_subject")
user_class = st.session_state.get("class", 6)  # Get user's class from session
data = get_scores_by_user(username)

if not data:
    st.info("No attempts yet")
    st.stop()

subject_wise = defaultdict(list)
chapter_wise = defaultdict(lambda: defaultdict(list))
for subject, chapter, score, total in data:
    subject_wise[subject].append((score, total))
    chapter_wise[subject][chapter].append((score, total))

if not selected_subject:
    render_subject_analysis(subject_wise, chapter_wise, user_class)
    st.info("Select a subject from sidebar")
    st.stop()

if selected_subject not in chapter_wise:
    st.info(f"No data for {selected_subject}")
    st.stop()

chapters = chapter_wise[selected_subject]

total_score = sum(s for a in chapters.values() for s,t in a)
total_q = sum(t for a in chapters.values() for s,t in a)
accuracy = total_score/total_q*100 if total_q else 0
attempts = len([x for x in data if x[0]==selected_subject])

stats = []
for ch, att in chapters.items():
    stats.append({
        "Chapter": ch,
        "Average": sum(s/t for s,t in att)/len(att)*100,
        "Latest": att[0][0]/att[0][1]*100,
        "Best": max(s/t for s,t in att)*100,
        "Attempts": len(att)
    })

st.header(f"📘 {selected_subject}")
c1,c2,c3,c4 = st.columns(4)
c1.metric("Attempts", attempts)
c2.metric("Questions", total_q)
c3.metric("Accuracy", f"{accuracy:.1f}%")
c4.metric("Correct", f"{total_score}/{total_q}")

st.divider()
st.subheader("📚 Chapter Analysis")
tabs = st.tabs([f"📖 {s['Chapter']}" for s in stats])

for tab, s in zip(tabs, stats):
    with tab:
        att = chapters[s['Chapter']]
        c1,c2,c3 = st.columns(3)
        c1.metric("Latest", f"{att[0][0]}/{att[0][1]}", f"{s['Latest']:.1f}%")
        c2.metric("Average", f"{s['Average']:.1f}%")
        c3.metric("Best", f"{s['Best']:.1f}%")
        st.progress(s['Latest']/100)
        with st.expander("History"):
            df = pd.DataFrame([{"Attempt":i+1, "Score":f"{sc}/{tot}", "%":f"{(sc/tot)*100:.1f}%"} 
                              for i,(sc,tot) in enumerate(att)])
            st.dataframe(df, use_container_width=True)

st.divider()
progress = [score/total*100 for subject,ch,score,total in data if subject==selected_subject]
render_visualizations(stats, progress, chapters, list(chapters.keys()), selected_subject)

st.divider()
render_comparison(chapters, list(chapters.keys()))

st.divider()
weak = [s["Chapter"] for s in stats if s["Average"]<50]
developing = [s["Chapter"] for s in stats if 50<=s["Average"]<70]
st.subheader("Areas for Improvement")
if weak: st.warning(f"Need Attention: {', '.join(weak[:3])}")
if developing: st.info(f"Developing: {', '.join(developing[:3])}")
if not weak and not developing: st.success("All chapters above 70%!")

st.divider()
subject_stats = render_subject_analysis(subject_wise, chapter_wise, user_class)

st.divider()
render_pdf_report(username, subject_stats, selected_subject, accuracy, stats, weak, developing)

st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")