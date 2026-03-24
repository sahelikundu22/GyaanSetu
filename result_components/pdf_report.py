import streamlit as st
import base64
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile, os, numpy as np


def clean(text: str) -> str:
    """Remove or replace characters that cannot be encoded in latin-1."""
    return str(text).encode('latin-1', errors='replace').decode('latin-1')


def save_temp(fig):
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig.savefig(tmp.name, dpi=100, bbox_inches='tight')
        return tmp.name


def render_pdf_report(username, subject_stats, selected_subject, accuracy, chapter_stats, chapter_wise):
    st.subheader("📄 Download Report")

    if st.button("Generate PDF Report"):
        pdf = FPDF()
        temps = []

        # ── Page 1: Subject Overview ──────────────────────────────────────
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, clean(f'Report - {username}'), 0, 1, 'C')
        pdf.set_font('Arial', '', 8)
        pdf.cell(0, 5, datetime.now().strftime("%Y-%m-%d"), 0, 1, 'C')
        pdf.ln(3)

        # Subject table
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(70, 8, 'Subject', 1, 0)
        pdf.cell(35, 8, 'Accuracy', 1, 0)
        pdf.cell(35, 8, 'Chapter Avg', 1, 0)
        pdf.cell(40, 8, 'Status', 1, 1)
        pdf.set_font('Arial', '', 8)
        for s in subject_stats:
            pdf.cell(70, 6, clean(s['Subject']), 1, 0)
            pdf.cell(35, 6, clean(s['Accuracy']), 1, 0, 'C')
            pdf.cell(35, 6, clean(s.get('Chapter Avg', '-')), 1, 0, 'C')
            pdf.cell(40, 6, 'Attempted' if s['Status'] == '✅' else 'Not Attempted', 1, 1, 'C')

        # Subject chart
        fig, ax = plt.subplots(figsize=(8, 3))
        subs = [s["Subject"] for s in subject_stats if s["Status"] == "✅"]
        accs = [float(s["Accuracy"].strip("%")) for s in subject_stats if s["Status"] == "✅"]
        if subs:
            ax.bar(subs, accs, color=['#4CAF50' if a >= 70 else '#FF9800' if a >= 50 else '#F44336' for a in accs])
            ax.axhline(y=50, color='gray', linestyle='--')
            ax.axhline(y=70, color='green', linestyle='--')
            ax.set_title("Subject-wise Accuracy")
            ax.set_ylabel("Accuracy (%)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            tmp = save_temp(fig)
            temps.append(tmp)
            pdf.image(tmp, x=10, y=pdf.get_y() + 5, w=190)
        plt.close()

        # ── One Page per Attempted Subject ───────────────────────────────
        attempted_subjects = [s for s in subject_stats if s["Status"] == "✅"]

        for subj in attempted_subjects:
            sub_name = subj["Subject"]
            chapters = chapter_wise.get(sub_name, {})
            if not chapters:
                continue

            sub_chapter_stats = []
            total_s = 0
            total_q = 0

            for ch, att in chapters.items():
                avg    = sum(s / t for s, t in att) / len(att) * 100
                best   = max(s / t for s, t in att) * 100
                latest = att[0][0] / att[0][1] * 100
                total_s += sum(s for s, t in att)
                total_q += sum(t for s, t in att)
                sub_chapter_stats.append({
                    "Chapter":  ch,
                    "Average":  avg,
                    "Latest":   latest,
                    "Best":     best,
                    "Attempts": len(att),
                })

            sub_accuracy = total_s / total_q * 100 if total_q else 0

            pdf.add_page()
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, clean(f'{sub_name} - Detailed Report'), 0, 1)
            pdf.set_font('Arial', '', 8)
            pdf.cell(0, 6, clean(f'Overall Accuracy: {sub_accuracy:.1f}%   |   Chapters Attempted: {len(sub_chapter_stats)}'), 0, 1)
            pdf.ln(2)

            # Chapter table
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(70, 8, 'Chapter', 1, 0)
            pdf.cell(30, 8, 'Avg %', 1, 0)
            pdf.cell(30, 8, 'Latest %', 1, 0)
            pdf.cell(30, 8, 'Best %', 1, 0)
            pdf.cell(20, 8, 'Attempts', 1, 1)
            pdf.set_font('Arial', '', 8)
            for s in sub_chapter_stats:
                pdf.cell(70, 6, clean(s['Chapter'][:35]), 1, 0)
                pdf.cell(30, 6, f"{s['Average']:.1f}%", 1, 0, 'C')
                pdf.cell(30, 6, f"{s['Latest']:.1f}%", 1, 0, 'C')
                pdf.cell(30, 6, f"{s['Best']:.1f}%", 1, 0, 'C')
                pdf.cell(20, 6, str(s['Attempts']), 1, 1, 'C')

            # Chapter chart
            fig2, ax2 = plt.subplots(figsize=(8, 3))
            chaps = [s["Chapter"][:12] for s in sub_chapter_stats]
            x = np.arange(len(chaps))
            ax2.bar(x - 0.2, [s["Average"] for s in sub_chapter_stats], 0.4, label='Avg',    color='#FF9800')
            ax2.bar(x + 0.2, [s["Latest"]  for s in sub_chapter_stats], 0.4, label='Latest', color='#2196F3')
            ax2.axhline(y=50, color='gray',  linestyle='--')
            ax2.axhline(y=70, color='green', linestyle='--')
            ax2.set_xticks(x)
            ax2.set_xticklabels(chaps, rotation=45, fontsize=7)
            ax2.set_title(clean(f"{sub_name} - Average vs Latest Score per Chapter"))
            ax2.set_ylabel("Score (%)")
            ax2.legend(fontsize=8)
            plt.tight_layout()
            tmp = save_temp(fig2)
            temps.append(tmp)
            pdf.image(tmp, x=10, y=pdf.get_y() + 5, w=190)
            plt.close()

        # ── Save & Download ───────────────────────────────────────────────
        output = pdf.output(dest='S')
        if isinstance(output, str):
            output = output.encode('latin-1')

        b64 = base64.b64encode(output).decode()
        st.markdown(
            f'<a href="data:application/octet-stream;base64,{b64}" download="{clean(username)}_report.pdf">📥 Download PDF</a>',
            unsafe_allow_html=True
        )
        st.success("✅ Ready!")

        for f in temps:
            try:
                os.unlink(f)
            except:
                pass