import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def render_visualizations(stats, progress, chapters_data, chapters_list, subject):
    st.subheader("📊 Performance Charts")
    
    col1, col2 = st.columns(2)
    chapters = [s["Chapter"] for s in stats]
    
    with col1:
        fig, ax = plt.subplots()
        averages = [s["Average"] for s in stats]
        colors = ['#4CAF50' if a>=70 else '#FF9800' if a>=50 else '#F44336' for a in averages]
        ax.bar(chapters, averages, color=colors)
        ax.axhline(y=50, color='gray', linestyle='--', label='50% threshold')
        ax.axhline(y=70, color='green', linestyle='--', label='70% threshold')
        ax.set_title("Average Score per Chapter")
        ax.set_xlabel("Chapter")
        ax.set_ylabel("Average Score (%)")
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots()
        latest = [s["Latest"] for s in stats]
        avg = [s["Average"] for s in stats]
        x = np.arange(len(chapters))
        ax.bar(x-0.2, latest, 0.4, label='Latest', color='#2196F3')
        ax.bar(x+0.2, avg, 0.4, label='Average', color='#FF9800')
        ax.set_xticks(x)
        ax.set_xticklabels(chapters, rotation=45)
        ax.set_title("Latest vs Average Score per Chapter")
        ax.set_xlabel("Chapter")
        ax.set_ylabel("Score (%)")
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
    
    col3, col4 = st.columns(2)
    with col3:
        if progress:
            fig, ax = plt.subplots()
            ax.plot(range(1, len(progress)+1), progress, marker='o', color='#2196F3')
            ax.axhline(y=50, color='gray', linestyle='--', label='50% threshold')
            ax.set_title(f"Overall Progress Over Attempts — {subject}")
            ax.set_xlabel("Attempt Number")
            ax.set_ylabel("Score (%)")
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig)
    
    with col4:
        if chapters_list:
            fig, ax = plt.subplots()
            for ch in chapters_list[:5]:
                attempts = chapters_data[ch]
                scores = [(s/t)*100 for s,t in attempts[::-1]]
                ax.plot(range(1, len(scores)+1), scores, marker='o', label=ch[:10])
            ax.axhline(y=50, color='gray', linestyle='--', label='50% threshold')
            ax.set_title("Chapter-wise Progress Over Attempts")
            ax.set_xlabel("Attempt Number")
            ax.set_ylabel("Score (%)")
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig)