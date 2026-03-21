import streamlit as st
import base64
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile, os, numpy as np

def save_temp(fig):
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig.savefig(tmp.name, dpi=100, bbox_inches='tight')
        return tmp.name

def render_pdf_report(username, subject_stats, selected_subject, accuracy, chapter_stats, weak, developing):
    st.subheader("📄 Download Report")
    
    if st.button("Generate PDF Report"):
        pdf = FPDF()
        temps = []
        
        # Page 1 - Subject Analysis
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f'Report - {username}', 0, 1, 'C')
        pdf.set_font('Arial', '', 8)
        pdf.cell(0, 5, datetime.now().strftime("%Y-%m-%d"), 0, 1, 'C')
        
        # Subject table with Chapter Avg column
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(70, 8, 'Subject', 1, 0)
        pdf.cell(35, 8, 'Accuracy', 1, 0)
        pdf.cell(35, 8, 'Chapter Avg', 1, 0)
        pdf.cell(40, 8, 'Status', 1, 1)
        pdf.set_font('Arial', '', 8)
        for s in subject_stats:
            pdf.cell(70, 6, s['Subject'], 1, 0)
            pdf.cell(35, 6, s['Accuracy'], 1, 0, 'C')
            pdf.cell(35, 6, s.get('Chapter Avg', '-'), 1, 0, 'C')
            pdf.cell(40, 6, 'Attempted' if s['Status']=='✅' else 'Not', 1, 1, 'C')
        
        # Subject chart
        fig, ax = plt.subplots(figsize=(8, 3))
        subs = [s["Subject"] for s in subject_stats if s["Status"]=="✅"]
        accs = [float(s["Accuracy"].strip("%")) for s in subject_stats if s["Status"]=="✅"]
        if subs:
            ax.bar(subs, accs, color=['#4CAF50' if a>=70 else '#FF9800' if a>=50 else '#F44336' for a in accs])
            ax.axhline(y=50, color='gray', linestyle='--')
            ax.axhline(y=70, color='green', linestyle='--')
            plt.xticks(rotation=45)
            plt.tight_layout()
            pdf.image(save_temp(fig), x=10, y=pdf.get_y()+5, w=190)
        plt.close()
        
        # Page 2 - Chapter Details
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, f'{selected_subject} - Details', 0, 1)
        pdf.set_font('Arial', '', 8)
        pdf.cell(0, 6, f'Accuracy: {accuracy:.1f}%', 0, 1)
        
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
        chaps = [s["Chapter"][:12] for s in chapter_stats]
        x = np.arange(len(chaps))
        ax2.bar(x-0.2, [s["Average"] for s in chapter_stats], 0.4, label='Avg', color='#FF9800')
        ax2.bar(x+0.2, [s["Latest"] for s in chapter_stats], 0.4, label='Latest', color='#2196F3')
        ax2.axhline(y=50, color='gray', linestyle='--')
        ax2.set_xticks(x)
        ax2.set_xticklabels(chaps, rotation=45, fontsize=7)
        ax2.legend(fontsize=8)
        plt.tight_layout()
        pdf.image(save_temp(fig2), x=10, y=pdf.get_y()+5, w=190)
        plt.close()
        
        # Page 3 - Recommendations
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Recommendations', 0, 1)
        pdf.set_font('Arial', '', 9)
        if weak:
            pdf.set_text_color(255,0,0)
            pdf.cell(0, 6, f'Need Attention: {", ".join(weak[:3])}', 0, 1)
        if developing:
            pdf.set_text_color(255,165,0)
            pdf.cell(0, 6, f'Developing: {", ".join(developing[:3])}', 0, 1)
        pdf.set_text_color(0,0,0)
        
        not_att = [s["Subject"] for s in subject_stats if s["Status"]=="❌"]
        if not_att:
            pdf.cell(0, 6, f'Not Attempted: {", ".join(not_att[:3])}', 0, 1)
        
        pdf.ln(5)
        pdf.set_font('Arial', 'I', 9)
        pdf.cell(0, 6, 'Keep practicing! Consistent effort leads to improvement.', 0, 1, 'C')
        
        # Save
        output = pdf.output(dest='S')
        if isinstance(output, str):
            output = output.encode('latin1')
        
        b64 = base64.b64encode(output).decode()
        st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="{username}_report.pdf">📥 Download PDF</a>', unsafe_allow_html=True)
        st.success("✅ Ready!")
        
        for f in temps:
            try: os.unlink(f)
            except: pass