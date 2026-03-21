import streamlit as st
import base64
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile
import os
import numpy as np

def save_chart_temp(fig):
    """Save matplotlib figure to temporary file"""
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig.savefig(tmp.name, format='png', dpi=100, bbox_inches='tight')
        return tmp.name

def render_pdf_report(username, subject_stats, selected_subject, accuracy, chapter_stats, weak, developing):
    st.subheader("📄 Download Report")
    
    if st.button("Generate PDF Report"):
        pdf = FPDF()
        temp_files = []
        
        # Page 1: Subject Analysis
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f'Report - {username}', 0, 1, 'C')
        pdf.set_font('Arial', '', 8)
        pdf.cell(0, 5, datetime.now().strftime("%Y-%m-%d"), 0, 1, 'C')
        pdf.ln(5)
        
        # Subject table
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(70, 8, 'Subject', 1, 0)
        pdf.cell(30, 8, 'Accuracy', 1, 0)
        pdf.cell(40, 8, 'Score', 1, 0)
        pdf.cell(40, 8, 'Status', 1, 1)
        
        pdf.set_font('Arial', '', 8)
        for s in subject_stats:
            status_text = "Attempted" if s['Status'] == "✅" else "Not Attempted"
            pdf.cell(70, 6, s['Subject'], 1, 0)
            pdf.cell(30, 6, s['Accuracy'], 1, 0, 'C')
            pdf.cell(40, 6, s['Score'], 1, 0, 'C')
            pdf.cell(40, 6, status_text, 1, 1, 'C')
        
        # Subject chart
        fig, ax = plt.subplots(figsize=(8, 3))
        subs = [s["Subject"] for s in subject_stats if s["Status"] == "✅"]
        accs = [float(s["Accuracy"].strip("%")) for s in subject_stats if s["Status"] == "✅"]
        if subs:
            colors = ['#4CAF50' if a>=70 else '#FF9800' if a>=50 else '#F44336' for a in accs]
            ax.bar(subs, accs, color=colors)
            ax.axhline(y=50, color='gray', linestyle='--')
            ax.axhline(y=70, color='green', linestyle='--')
            ax.set_ylim(0, 100)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            temp_file = save_chart_temp(fig)
            temp_files.append(temp_file)
            pdf.image(temp_file, x=10, y=pdf.get_y()+5, w=190)
        plt.close(fig)
        
        # Page 2: Chapter Details
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, f'{selected_subject} - Details', 0, 1)
        pdf.set_font('Arial', '', 8)
        pdf.cell(0, 6, f'Overall Accuracy: {accuracy:.1f}%', 0, 1)
        
        # Chapter table
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(70, 8, 'Chapter', 1, 0)
        pdf.cell(35, 8, 'Avg %', 1, 0)
        pdf.cell(35, 8, 'Latest %', 1, 0)
        pdf.cell(40, 8, 'Attempts', 1, 1)
        
        pdf.set_font('Arial', '', 8)
        for s in chapter_stats:
            pdf.cell(70, 6, s['Chapter'], 1, 0)
            pdf.cell(35, 6, f"{s['Average']:.1f}%", 1, 0, 'C')
            pdf.cell(35, 6, f"{s['Latest']:.1f}%", 1, 0, 'C')
            pdf.cell(40, 6, str(s['Attempts']), 1, 1, 'C')
        
        # Chapter chart
        fig2, ax2 = plt.subplots(figsize=(8, 3))
        chapters = [s["Chapter"][:12] for s in chapter_stats]
        avg = [s["Average"] for s in chapter_stats]
        latest = [s["Latest"] for s in chapter_stats]
        x = np.arange(len(chapters))
        ax2.bar(x-0.2, avg, 0.4, label='Avg', color='#FF9800')
        ax2.bar(x+0.2, latest, 0.4, label='Latest', color='#2196F3')
        ax2.axhline(y=50, color='gray', linestyle='--')
        ax2.set_ylim(0, 100)
        ax2.set_xticks(x)
        ax2.set_xticklabels(chapters, rotation=45, fontsize=7)
        ax2.legend(fontsize=8)
        plt.tight_layout()
        
        temp_file2 = save_chart_temp(fig2)
        temp_files.append(temp_file2)
        pdf.image(temp_file2, x=10, y=pdf.get_y()+5, w=190)
        plt.close(fig2)
        
        # Page 3: Recommendations
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Recommendations', 0, 1)
        
        pdf.set_font('Arial', '', 9)
        if weak:
            pdf.set_text_color(255, 0, 0)
            weak_text = ', '.join(weak[:3])
            pdf.cell(0, 6, f'Need Attention: {weak_text}', 0, 1)
        if developing:
            pdf.set_text_color(255, 165, 0)
            dev_text = ', '.join(developing[:3])
            pdf.cell(0, 6, f'Developing: {dev_text}', 0, 1)
        pdf.set_text_color(0, 0, 0)
        
        not_attempted = [s["Subject"] for s in subject_stats if s["Status"] == "❌"]
        if not_attempted:
            not_text = ', '.join(not_attempted[:3])
            pdf.cell(0, 6, f'Not Attempted: {not_text}', 0, 1)
        
        pdf.ln(5)
        pdf.set_font('Arial', 'I', 9)
        pdf.cell(0, 6, 'Keep practicing! Consistent effort leads to improvement.', 0, 1, 'C')
        
        # Save PDF as bytes
        pdf_output = pdf.output(dest='S')
        
        # Convert to bytes if it's a string
        if isinstance(pdf_output, str):
            pdf_bytes = pdf_output.encode('latin1')
        else:
            pdf_bytes = pdf_output
        
        # Clean up temp files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        
        # Encode to base64
        b64 = base64.b64encode(pdf_bytes).decode()
        
        # Download button
        st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="{username}_report.pdf">📥 Download PDF Report</a>', unsafe_allow_html=True)
        st.success("✅ Report ready!")