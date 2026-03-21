import streamlit as st
import pandas as pd

def render_weak_areas(chapter_stats):
    """Render weak areas and recommendations"""
    st.subheader("⚠️ Areas for Improvement")
    
    df_chapters = pd.DataFrame(chapter_stats) if chapter_stats else pd.DataFrame()
    weak_chapters = df_chapters[df_chapters["Average"] < 50]["Chapter"].tolist() if not df_chapters.empty else []
    developing_chapters = df_chapters[(df_chapters["Average"] >= 50) & (df_chapters["Average"] < 70)]["Chapter"].tolist() if not df_chapters.empty else []
    
    if weak_chapters:
        st.error(f"🔴 **Critical Focus Areas ({len(weak_chapters)} chapters)**")
        for ch in weak_chapters:
            st.write(f"- **{ch}**")
        st.markdown("**Recommended Actions:** Review fundamentals, seek help, and retake quizzes.")
        
    if developing_chapters:
        st.warning(f"🟡 **Developing Areas ({len(developing_chapters)} chapters)**")
        for ch in developing_chapters:
            st.write(f"- **{ch}**")
        st.markdown("**Recommended Actions:** Regular practice and focused revision.")
        
    if not weak_chapters and not developing_chapters and not df_chapters.empty:
        st.success("🎉 **Excellent!** You're performing well in all chapters. Keep up the great work!")