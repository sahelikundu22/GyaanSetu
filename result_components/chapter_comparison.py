import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def render_chapter_comparison(chapters_data, chapters_list):
    """Render chapter comparison section"""
    st.subheader("🔍 Compare Chapters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        chapter1 = st.selectbox("Select First Chapter", chapters_list, key="chapter1")
    with col2:
        chapter2 = st.selectbox("Select Second Chapter", chapters_list, key="chapter2")
    
    if chapter1 and chapter2 and chapter1 != chapter2:
        # Get data
        attempts1 = chapters_data[chapter1]
        attempts2 = chapters_data[chapter2]
        
        # Calculate metrics
        avg1 = sum(s/t for s, t in attempts1) / len(attempts1) * 100
        avg2 = sum(s/t for s, t in attempts2) / len(attempts2) * 100
        latest1 = (attempts1[0][0] / attempts1[0][1]) * 100
        latest2 = (attempts2[0][0] / attempts2[0][1]) * 100
        
        improvement1 = 0
        improvement2 = 0
        if len(attempts1) > 1:
            first1 = (attempts1[-1][0] / attempts1[-1][1]) * 100
            improvement1 = latest1 - first1
        if len(attempts2) > 1:
            first2 = (attempts2[-1][0] / attempts2[-1][1]) * 100
            improvement2 = latest2 - first2
        
        # Display metrics
        st.markdown("### 📊 Performance Comparison")
        comp_col1, comp_col2, comp_col3, comp_col4 = st.columns(4)
        
        with comp_col1:
            st.metric(f"📖 {chapter1}", f"{avg1:.1f}%", "Average Score")
            st.metric(f"📖 {chapter2}", f"{avg2:.1f}%", "Average Score")
        
        with comp_col2:
            st.metric(f"📖 {chapter1}", f"{latest1:.1f}%", "Latest Score")
            st.metric(f"📖 {chapter2}", f"{latest2:.1f}%", "Latest Score")
        
        with comp_col3:
            st.metric(f"📖 {chapter1}", f"{improvement1:+.1f}%", "Improvement")
            st.metric(f"📖 {chapter2}", f"{improvement2:+.1f}%", "Improvement")
        
        with comp_col4:
            better_chapter = chapter1 if avg1 > avg2 else chapter2
            diff = abs(avg1 - avg2)
            st.info(f"🏆 **Better Performer:** {better_chapter}\n\n{diff:.1f}% higher average score")
        
        # Comparison chart
        fig, ax = plt.subplots(figsize=(10, 6))
        metrics = ['Average Score', 'Latest Score', 'Best Score', 'Improvement']
        val1 = [avg1, latest1, max(s/t for s, t in attempts1) * 100, improvement1]
        val2 = [avg2, latest2, max(s/t for s, t in attempts2) * 100, improvement2]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, val1, width, label=chapter1, color='#2196F3')
        bars2 = ax.bar(x + width/2, val2, width, label=chapter2, color='#FF9800')
        
        ax.set_xlabel('Metrics')
        ax.set_ylabel('Percentage (%)')
        ax.set_title(f'Chapter Comparison: {chapter1} vs {chapter2}')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')
        for bar in bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        st.pyplot(fig)
        
        # Trend comparison
        if len(attempts1) > 1 and len(attempts2) > 1:
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            attempts1_scores = [(s/t)*100 for s, t in attempts1[::-1]]
            attempts2_scores = [(s/t)*100 for s, t in attempts2[::-1]]
            
            ax2.plot(range(1, len(attempts1_scores) + 1), attempts1_scores, 
                    marker='o', label=chapter1, color='#2196F3', linewidth=2)
            ax2.plot(range(1, len(attempts2_scores) + 1), attempts2_scores, 
                    marker='s', label=chapter2, color='#FF9800', linewidth=2)
            
            ax2.set_xlabel('Attempt Number')
            ax2.set_ylabel('Score (%)')
            ax2.set_title('Learning Progress Comparison')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.set_ylim(0, 100)
            st.pyplot(fig2)