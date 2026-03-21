import streamlit as st
import base64
from datetime import datetime
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Student Performance Report', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def render_pdf_report(username, selected_subject, total_attempts, total_questions, total_score, accuracy, chapter_stats, weak_chapters, developing_chapters):
    """Render PDF report generation section"""
    st.subheader("📄 Generate PDF Report")
    
    if st.button("📄 Generate PDF Report"):
        pdf = PDF()
        pdf.add_page()
        
        # Student info
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f'Student: {username}', 0, 1)
        pdf.cell(0, 10, f'Subject: {selected_subject}', 0, 1)
        pdf.ln(5)
        
        # Overall performance
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Overall Performance', 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 8, f'Total Attempts: {total_attempts}', 0, 1)
        pdf.cell(0, 8, f'Questions Answered: {total_questions}', 0, 1)
        pdf.cell(0, 8, f'Correct Answers: {total_score}/{total_questions}', 0, 1)
        pdf.cell(0, 8, f'Overall Accuracy: {accuracy:.1f}%', 0, 1)
        pdf.ln(5)
        
        # Chapter-wise performance
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Chapter-wise Performance', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        for stat in chapter_stats:
            pdf.cell(0, 8, f"{stat['Chapter']}:", 0, 1)
            pdf.cell(0, 6, f"  Average: {stat['Average']:.1f}% | Latest: {stat['Latest']:.1f}% | Best: {stat['Best']:.1f}%", 0, 1)
            pdf.cell(0, 6, f"  Status: {stat['Status']}", 0, 1)
            pdf.ln(2)
        
        # Weak areas
        if weak_chapters or developing_chapters:
            pdf.ln(5)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Areas for Improvement', 0, 1)
            pdf.set_font('Arial', '', 10)
            
            if weak_chapters:
                pdf.set_text_color(255, 0, 0)
                pdf.cell(0, 8, 'Critical Focus Areas:', 0, 1)
                for ch in weak_chapters:
                    pdf.cell(0, 6, f'  - {ch}', 0, 1)
            
            if developing_chapters:
                pdf.set_text_color(255, 165, 0)
                pdf.cell(0, 8, 'Developing Areas:', 0, 1)
                for ch in developing_chapters:
                    pdf.cell(0, 6, f'  - {ch}', 0, 1)
            
            pdf.set_text_color(0, 0, 0)
        
        # Recommendations
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Recommendations', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        if weak_chapters:
            pdf.multi_cell(0, 6, '- Focus on weak chapters: Review fundamentals and retake quizzes')
        if developing_chapters:
            pdf.multi_cell(0, 6, '- Regular practice for developing chapters to achieve mastery')
        if not weak_chapters and not developing_chapters:
            pdf.multi_cell(0, 6, '- Excellent performance! Consider helping peers or exploring advanced topics')
        
        # Save PDF
        pdf_output = pdf.output(dest='S').encode('latin1')
        b64 = base64.b64encode(pdf_output).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{username}_{selected_subject}_report.pdf">Download PDF Report</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("✅ PDF Report generated successfully!")