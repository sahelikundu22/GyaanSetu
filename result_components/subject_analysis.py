import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def render_subject_analysis(subject_summary):
    """Render subject-wise analysis when no subject is selected"""
    st.subheader("📚 Subject-wise Performance Overview")
    
    df = pd.DataFrame(subject_summary)
    st.dataframe(df, use_container_width=True)
    
    # Subject-wise comparison chart
    if subject_summary:
        fig, ax = plt.subplots(figsize=(10, 6))
        subjects = [s["Subject"] for s in subject_summary]
        accuracies = [float(s["Accuracy"].strip("%")) for s in subject_summary]
        colors = ['#4CAF50' if acc >= 60 else '#FF9800' for acc in accuracies]
        bars = ax.bar(subjects, accuracies, color=colors)
        ax.axhline(y=60, color='red', linestyle='--', label='Target (60%)')
        ax.set_ylabel("Accuracy (%)")
        ax.set_title("Subject-wise Performance Comparison")
        ax.legend()
        
        for bar, acc in zip(bars, accuracies):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                    f'{acc:.1f}%', ha='center', va='bottom')
        
        st.pyplot(fig)
    
    st.info("💡 **Tip:** Select a subject from the sidebar to dive deeper into chapter-wise analysis.")