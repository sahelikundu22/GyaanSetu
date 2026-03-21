import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json, os
from collections import defaultdict

def load_subjects_for_class(user_class):
    """Load subjects for specific class from CBSE JSON file"""
    try:
        with open(os.path.join(os.path.dirname(__file__), "..", "cbse_data.json")) as f:
            data = json.load(f)
        
        class_key = f"class_{user_class}"
        if class_key in data["cbse_curriculum_2024_26"]:
            subjects = list(data["cbse_curriculum_2024_26"][class_key]["subjects"].keys())
            return subjects
        return []
    except:
        return []

def render_subject_analysis(subject_wise, chapter_wise, user_class):
    st.subheader("📊 Subject Analysis")
    
    # Load subjects for user's class
    all_subs = load_subjects_for_class(user_class)
    
    if not all_subs:
        st.warning(f"No subjects found for Class {user_class}")
        return []
    
    stats = []
    for sub in all_subs:
        if sub in subject_wise:
            att = subject_wise[sub]
            total_s = sum(s for s,t in att)
            total_q = sum(t for s,t in att)
            acc = total_s/total_q*100 if total_q else 0
            
            # Calculate chapter-wise average for this subject
            chapters = chapter_wise.get(sub, {})
            chapter_avgs = []
            for ch, ch_att in chapters.items():
                ch_avg = sum(s/t for s,t in ch_att) / len(ch_att) * 100
                chapter_avgs.append(ch_avg)
            overall_chapter_avg = sum(chapter_avgs) / len(chapter_avgs) if chapter_avgs else 0
            
            stats.append({
                "Subject": sub, 
                "Accuracy": f"{acc:.1f}%", 
                "Chapter Avg": f"{overall_chapter_avg:.1f}%",
                "Status": "✅"
            })
        else:
            stats.append({
                "Subject": sub, 
                "Accuracy": "-", 
                "Chapter Avg": "-",
                "Status": "❌"
            })
    
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(pd.DataFrame(stats), use_container_width=True, hide_index=True)
    
    with col2:
        fig, ax = plt.subplots(figsize=(8, 4))
        subs = [s["Subject"] for s in stats]
        accs = [float(s["Accuracy"].strip("%")) if s["Accuracy"] != "-" else 0 for s in stats]
        colors = ['#D3D3D3' if s["Status"]=="❌" else '#4CAF50' if a>=70 else '#FF9800' if a>=50 else '#F44336' for s,a in zip(stats, accs)]
        ax.bar(subs, accs, color=colors)
        ax.axhline(y=50, color='gray', linestyle='--')
        ax.axhline(y=70, color='green', linestyle='--')
        ax.set_ylim(0, 100)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
    
    attempted = [s for s in stats if s["Status"]=="✅"]
    not_att = [s["Subject"] for s in stats if s["Status"]=="❌"]
    c1,c2,c3 = st.columns(3)
    c1.metric("Total", len(all_subs))
    c2.metric("Attempted", len(attempted))
    c3.metric("Remaining", len(not_att))
    
    if not_att:
        subjects = ', '.join(not_att[:5]) + (f" and {len(not_att)-5} more" if len(not_att)>5 else "")
        st.info(f"⚠️ Not attempted: {subjects}")
    
    return stats