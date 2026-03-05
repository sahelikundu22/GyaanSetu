import streamlit as st
import os
import base64

BASE_DIR = "studymaterial"

def show_book_pdf(subject, chapter):
    st.subheader(f"📘 {subject} – {chapter}")

    pdf_path = os.path.join(BASE_DIR, subject, f"{chapter}.pdf")

    if not os.path.exists(pdf_path):
        st.warning("📕 Book PDF not available for this chapter.")
        return

    # Read PDF
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    # Download button
    st.download_button(
        label="⬇️ Download Book PDF",
        data=pdf_bytes,
        file_name=f"{chapter}.pdf",
        mime="application/pdf"
    )

    # Display PDF in browser
    base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
    pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="600"
            style="border:none;">
        </iframe>
    """

    st.markdown(pdf_display, unsafe_allow_html=True)

def study_material_page(selected_chapter, selected_module):
    """Study Material Page"""
    st.subheader("📖 Study Material")

    with st.expander("Chapter Notes", expanded=True):
        st.write(f"Here are the study notes for **{selected_module}** from **{selected_chapter}**:")
        st.markdown("""
        - The study material is taken from the **NCERT textbook PDF**.
        - It follows the **official NCERT syllabus and chapter structure**.
        - The content is provided for **concept understanding and exam preparation**.
        """)

    if st.button("📘 View Book (PDF)", use_container_width=True):
        show_book_pdf(selected_chapter, selected_module)

    # Additional study material content
    st.markdown("---")
    st.subheader("Additional Resources")
    
    col1, col2 = st.columns(2)
    with col1:
        st.video("https://youtu.be/NE0P02M_gMQ?si=mfj4rh22DQVtlSjQ")  
    with col2:
        st.video("https://youtu.be/tHm3X_Ta_iE?si=Z6lPYlu_qUizBEUd")  