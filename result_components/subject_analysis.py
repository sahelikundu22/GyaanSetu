import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

def load_all_subjects():
    """Load all subjects from CBSE JSON file"""
    json_path = os.path.join(os.path.dirname(__file__), "..", "cbse_data.json")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    all_subjects = []
    for class_name, class_data in data["cbse_curriculum_2024_26"].items():
        for subject in class_data["subjects"].keys():
            if subject not in all_subjects:
                all_subjects.append(subject)
    
    return all_subjects

def render_subject_analysis(subject_wise):
    """Render subject analysis with table and chart side by side"""
    st.subheader("📊 Subject Analysis")
    
    # Load all subjects from JSON
    all_subjects = load_all_subjects()
    
    # Calculate stats for all subjects
    subject_stats = []
    for sub in all_subjects:
        if sub in subject_wise:
            att = subject_wise[sub]
            total_s = sum(s for s, t in att)
            total_q = sum(t for s, t in att)
            acc = total_s/total_q*100 if total_q else 0
            subject_stats.append({"Subject": sub, "Accuracy": f"{acc:.1f}%", "Score": f"{total_s}/{total_q}", "Status": "✅"})
        else:
            subject_stats.append({"Subject": sub, "Accuracy": "-", "Score": "0/0", "Status": "❌"})
    
    # Side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📋 Performance Table**")
        df = pd.DataFrame(subject_stats)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**📈 Performance Chart**")
        fig, ax = plt.subplots(figsize=(8, 4))
        subs = [s["Subject"] for s in subject_stats]
        accs = []
        for s in subject_stats:
            if s["Accuracy"] != "-":
                accs.append(float(s["Accuracy"].strip("%")))
            else:
                accs.append(0)
        
        colors = []
        for i, s in enumerate(subject_stats):
            if s["Status"] == "❌":
                colors.append('#D3D3D3')
            elif accs[i] >= 70:
                colors.append('#4CAF50')
            elif accs[i] >= 50:
                colors.append('#FF9800')
            else:
                colors.append('#F44336')
        
        bars = ax.bar(subs, accs, color=colors)
        ax.axhline(y=50, color='gray', linestyle='--', alpha=0.7, label='Passing')
        ax.axhline(y=70, color='green', linestyle='--', alpha=0.7, label='Mastery')
        ax.set_ylabel("Accuracy (%)")
        ax.set_title("Subject-wise Performance")
        ax.legend(fontsize=8)
        ax.set_ylim(0, 100)
        plt.xticks(rotation=45, ha='right', fontsize=8)
        
        # Add labels
        for bar, s in zip(bars, subject_stats):
            if s["Status"] == "✅":
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height, 
                       s["Accuracy"], ha='center', va='bottom', fontsize=7)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    # Summary
    attempted = [s for s in subject_stats if s["Status"] == "✅"]
    not_attempted = [s for s in subject_stats if s["Status"] == "❌"]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Subjects", len(all_subjects))
    col2.metric("Attempted", len(attempted))
    col3.metric("Remaining", len(not_attempted))
    
    if not_attempted:
        st.info(f"⚠️ Not attempted: {', '.join([s['Subject'] for s in not_attempted[:5]])}")
        if len(not_attempted) > 5:
            st.info(f"... and {len(not_attempted) - 5} more")
    
    return subject_stats