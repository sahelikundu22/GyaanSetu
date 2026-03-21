# 📚 GyaanSetu
### *Connecting Ambition with Education*

GyaanSetu is an AI-powered learning platform for CBSE students (Classes 5–8) with study material, AI quizzes, performance tracking, and a PDF Q&A assistant — built with Streamlit.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🔐 **OTP Authentication** | Email-verified sign-up with Gmail SMTP; passwordless login |
| 📖 **Study Material** | YouTube lessons + inline PDF viewer with download options |
| 🤖 **AI Quiz Generator** | 10 MCQs auto-generated from chapter PDFs using LLaMA 3.1 |
| 📊 **Performance Dashboard** | Score charts, trend lines, chapter comparison, PDF report |
| 🔍 **PDF Q&A** | Upload any PDF, ask questions, answers highlighted in yellow |

---

## 🗂️ Project Structure

```
GyaanSetu/
├── app.py                  # Main entry point
├── auth.py                 # OTP signup & login
├── database.py             # SQLite3 — users & quiz scores
├── quiz_utils.py           # AI quiz generation (Groq + PyPDF2)
├── sidebar.py              # Shared sidebar navigation
├── cbse_data.json          # CBSE curriculum data (Classes 5–8)
├── pages/
│   ├── study_material.py   # Study material viewer
│   ├── quiz.py             # Quiz page
│   ├── performance.py      # Performance dashboard
│   └── pdf_qna.py          # PDF Q&A page
├── pdf_qna_engine/
│   ├── models.py           # Embedding model
│   ├── search.py           # Cosine similarity search
│   ├── llm.py              # Groq API answer generation
│   └── highlighter.py      # PDF annotation
├── study_material/         # Chapter PDFs by subject folder
├── gyaanset.db             # SQLite database (auto-created)
├── requirements.txt
└── .streamlit/
    └── secrets.toml        # API keys & email credentials
```

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| AI / LLM | Groq API — LLaMA 3.1 8B, LLaMA 3.3 70B |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| PDF | pdfplumber, PyPDF2, streamlit-pdf-viewer, fpdf |
| Data & Charts | pandas, matplotlib, numpy |
| Database | SQLite3 |
| Email | smtplib — Gmail SMTP SSL |

---

## 🧩 Modules

**`database.py`** — SQLite3 with two tables: `users` (id, name, email, class, points) and `quiz_scores` (id, username, subject, chapter, score, total). All queries use parameterised statements to prevent SQL injection.

**`auth.py`** — `@st.dialog` with Login/Sign Up toggle. Sign-up validates email with regex, generates a 6-digit OTP via `random.randint`, and sends it via Gmail SMTP SSL. Login is email-only — loads user into session state and calls `st.rerun()`.

**`sidebar.py`** — Imported by every page. Populates cascading subject/chapter dropdowns from `cbse_data.json` based on the student's class. Writes `selected_subject`, `selected_chapter`, and `selected_yt_link` to session state — the single navigation source of truth across all pages.

**`study_material.py`** — Two-column layout: YouTube video + download buttons on the left, inline Base64 PDF viewer on the right. Lite PDF is compressed on-the-fly using `pypdf`.

**`quiz.py` + `quiz_utils.py`** — Extracts text from up to 6 PDF pages, trims to 3,500 chars, prompts `llama-3.1-8b-instant` to return a JSON array of MCQs. Renders quiz via `st.form` with colour-coded results. Score saved to database.

**`performance.py`** — Loads quiz history, computes average/latest/best scores per chapter, renders 4 matplotlib charts including a numpy linear regression trend line. Exports a 3-page PDF report via `fpdf`.

**`pdf_qna.py` + `pdf_qna_engine/`** — RAG pipeline: pdfplumber extraction → 150-word overlapping chunks → MiniLM embeddings → cosine similarity retrieval → `llama-3.3-70b-versatile` answer with 6-turn memory → fuzzy highlight with auto-scroll.

---

## ⚙️ Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure secrets
Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
SENDER_EMAIL = "your_gmail@gmail.com"
EMAIL_PASS   = "your_gmail_app_password"
```
> Use a [Gmail App Password](https://support.google.com/accounts/answer/185833), not your regular password.

### 3. Add study material PDFs
Place PDFs in `study_material/<Subject Name>/`. Filename must start with the chapter name (case-insensitive).

### 4. Run
```bash
streamlit run app.py
```
The database is created automatically on first run.

---

## 🖥️ How to Use

1. **Sign Up** — enter name, email, class → receive OTP → verify to register
2. **Login** — enter registered email → redirected to dashboard
3. **Select content** — use sidebar to pick subject and chapter
4. **Study** — watch video, read PDF inline, or download it
5. **Quiz** — generate quiz → answer MCQs → view colour-coded results
6. **Performance** — view charts, compare chapters, download PDF report
7. **PDF Q&A** — upload any PDF → ask questions → answers highlighted in the document

---

## ⚠️ Notes

- Never commit `.streamlit/secrets.toml` — add to `.gitignore`
- PDF study material must be placed manually in subject subfolders
- Internet connection required for Groq API calls and OTP email delivery

---

## 📄 Internship

Developed as part of the **Spring Internship 2026** at  
**IDEAS — Institute of Data Engineering, Analytics and Science Foundation, ISI Kolkata**  
Period: 21st January 2026 – 31st March 2026