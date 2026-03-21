import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def render_visualizations(chapter_stats, progress_data, chapters_data, chapters_list, selected_subject):
    """Render all performance visualizations"""
    st.subheader("📊 Performance Visualizations")
    
    # Row 1: Chapter Performance and Latest vs Average
    col1, col2 = st.columns(2)
    
    with col1:
        if chapter_stats:
            fig, ax = plt.subplots(figsize=(10, 6))
            chapters = [stat["Chapter"] for stat in chapter_stats]
            averages = [stat["Average"] for stat in chapter_stats]
            
            colors = ['#4CAF50' if avg >= 70 else '#FF9800' if avg >= 50 else '#F44336' for avg in averages]
            bars = ax.bar(chapters, averages, color=colors)
            ax.axhline(y=50, color='orange', linestyle='--', label='Passing (50%)')
            ax.axhline(y=70, color='green', linestyle='--', label='Mastery (70%)')
            ax.set_ylabel("Average Score (%)")
            ax.set_title(f"{selected_subject} - Chapter Performance")
            ax.legend()
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
    
    with col2:
        if chapter_stats:
            fig, ax = plt.subplots(figsize=(10, 6))
            chapters = [stat["Chapter"] for stat in chapter_stats]
            latest_scores = [stat["Latest"] for stat in chapter_stats]
            avg_scores = [stat["Average"] for stat in chapter_stats]
            
            x = np.arange(len(chapters))
            width = 0.35
            
            bars1 = ax.bar(x - width/2, latest_scores, width, label='Latest Score', color='#2196F3')
            bars2 = ax.bar(x + width/2, avg_scores, width, label='Average Score', color='#FF9800')
            
            ax.set_xlabel('Chapters')
            ax.set_ylabel('Score (%)')
            ax.set_title('Latest vs Average Performance')
            ax.set_xticks(x)
            ax.set_xticklabels(chapters, rotation=45, ha='right')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_ylim(0, 100)
            
            for bar in bars1:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%', ha='center', va='bottom', fontsize=8)
            for bar in bars2:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%', ha='center', va='bottom', fontsize=8)
            
            plt.tight_layout()
            st.pyplot(fig)
    
    # Row 2: Progress Trend and Chapter-wise Progress
    col3, col4 = st.columns(2)
    
    with col3:
        if progress_data:
            fig, ax = plt.subplots(figsize=(10, 6))
            df_progress = pd.DataFrame(progress_data)
            ax.plot(df_progress["Attempt"], df_progress["Percentage"], 
                    marker='o', linewidth=2, markersize=8, color='#2196F3')
            
            if len(df_progress) > 1:
                z = np.polyfit(df_progress["Attempt"], df_progress["Percentage"], 1)
                p = np.poly1d(z)
                ax.plot(df_progress["Attempt"], p(df_progress["Attempt"]), 
                        "--", color='red', alpha=0.7, label='Trend Line')
            
            ax.set_xlabel("Attempt Number")
            ax.set_ylabel("Score (%)")
            ax.set_title("Overall Progress Trend")
            ax.set_ylim(0, 100)
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)
        else:
            st.info("Not enough data to show progress trend")
    
    with col4:
        if chapters_list:
            fig, ax = plt.subplots(figsize=(10, 6))
            display_chapters = chapters_list[:5] if len(chapters_list) > 5 else chapters_list
            
            for chapter in display_chapters:
                attempts = chapters_data[chapter]
                attempts_scores = [(s/t)*100 for s, t in attempts[::-1]]
                ax.plot(range(1, len(attempts_scores) + 1), attempts_scores, 
                        marker='o', label=chapter[:15], linewidth=2)
            
            ax.set_xlabel("Attempt Number")
            ax.set_ylabel("Score (%)")
            ax.set_title("Chapter-wise Progress Over Time")
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(True, alpha=0.3)
            ax.set_ylim(0, 100)
            plt.tight_layout()
            st.pyplot(fig)