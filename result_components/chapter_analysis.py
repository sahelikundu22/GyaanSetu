import streamlit as st
import pandas as pd

def render_chapter_analysis(chapters_data, chapters_list):
    """Render detailed chapter analysis with tabs"""
    st.subheader("📚 Detailed Chapter Analysis")
    
    tabs = st.tabs([f"📖 {chapter}" for chapter in chapters_list])
    chapter_stats = []
    
    for tab, chapter in zip(tabs, chapters_list):
        with tab:
            attempts = chapters_data[chapter]
            
            # Calculate statistics
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
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Latest Score", f"{latest_score}/{latest_total}", f"{latest_pct:.1f}%")
            with col2:
                st.metric("Average Score", f"{avg_score:.1f}%")
            with col3:
                st.metric("Best Score", f"{best_score:.1f}%")
            
            st.progress(latest_pct / 100)
            
            # Quiz history
            with st.expander("📜 View Complete Quiz History"):
                history_data = []
                for i, (s, t) in enumerate(attempts):
                    pct = (s/t) * 100
                    status = "✅ Pass" if pct >= 50 else "❌ Needs Improvement"
                    history_data.append({
                        "Attempt": i + 1,
                        "Score": f"{s}/{t}",
                        "Percentage": f"{pct:.1f}%",
                        "Status": status
                    })
                
                history_df = pd.DataFrame(history_data)
                st.dataframe(history_df, use_container_width=True)
    
    return chapter_stats