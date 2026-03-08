import streamlit as st
from sidebar import render_sidebar

st.set_page_config(page_title="Study Material", page_icon="📖")

render_sidebar()

st.title("📖 Study Material")


subject = st.session_state.get('selected_subject', 'Not selected')
chapter = st.session_state.get('selected_chapter', 'Not selected')
yt_link = st.session_state.get('selected_yt_link', '')

st.subheader(f"{subject} - {chapter}")


if yt_link:
    st.video(yt_link)
else:
    st.info("No video available for this chapter")


st.markdown("### 📝 Study Notes")
st.markdown(f"""
**Key Points for {chapter}:**
- Point 1: Understanding the basic concepts
- Point 2: Important formulas and definitions
- Point 3: Real-life applications
- Point 4: Practice examples
""")


st.markdown("### 📚 Additional Resources")
st.markdown("- [NCERT Textbook](https://ncert.nic.in/)")
st.markdown("- [Practice Worksheets](#)")
st.markdown("- [Reference Videos](#)")


if st.button("✅ Mark as Completed"):
    st.success(f"Completed {chapter}!")
    st.balloons()