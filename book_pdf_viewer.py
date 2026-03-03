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