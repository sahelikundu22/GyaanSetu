# 📚 GyaanSetu  
### Connecting Ambition with Education  

Live App: https://gyaansetu.streamlit.app  

GyaanSetu is an AI-powered learning platform designed for school students. It combines study material, AI-generated quizzes, performance analytics, a PDF question-answering assistant, and a YouTube transcription tool into a single Streamlit web application.

The platform is data-driven — curriculum, subjects, and chapters are controlled via structured JSON input and study material folders. While it currently uses CBSE-based content, the system is flexible and can be adapted to any educational board by modifying the input data.

---

## 🚀 Features

- 🔐 OTP-based authentication (Gmail SMTP, passwordless login)  
- 📖 Study material with YouTube lessons, inline PDF viewer, and transcript support  
- 🤖 AI quiz generator (10 MCQs from PDFs using LLaMA via Groq)  
- 📊 Performance dashboard with charts, trends, and PDF reports  
- 🔍 PDF Q&A with semantic search and highlighted answers  
- 🎥 YouTube Transcription Tool (transcript extraction, cleanup, translation, and study-guide generation)  
- 🔄 Easily adaptable to any board by changing curriculum JSON and PDFs  

---

## 🗂️ Project Structure

```
GyaanSetu/
├── app.py
├── auth.py
├── database.py
├── quiz_utils.py
├── sidebar.py
├── cbse_data.json
├── pages/
│   ├── study_material.py
│   ├── quiz.py
│   ├── performance.py
│   ├── pdf_qna.py
│   └── youtube_tool.py
├── pdf_qna_engine/
│   ├── models.py
│   ├── search.py
│   ├── llm.py
│   └── highlighter.py
├── study_material/
├── gyaanset.db
├── requirements.txt
└── .streamlit/secrets.toml
```

---

## 📦 Tech Stack

- **Frontend:** Streamlit  
- **AI Models:** Groq API (LLaMA 3.1, LLaMA 3.3)  
- **Embeddings:** sentence-transformers (MiniLM)  
- **PDF Processing:** pdfplumber, PyPDF2  
- **Data & Charts:** pandas, matplotlib, numpy  
- **Database:** SQLite3  
- **Email:** smtplib (Gmail SMTP)  
- **YouTube Processing:** transcript APIs + LLM-based processing  

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/gyaansetu.git
cd gyaansetu
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure secrets

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_groq_api_key"
SENDER_EMAIL = "your_email@gmail.com"
EMAIL_PASS = "your_app_password"
```

Use a Gmail App Password instead of your normal password.

---

### 4. Add / Customize Study Material

Place PDFs inside:
```
study_material/<Subject Name>/
```

To adapt for a different board:
- Modify `cbse_data.json` with your own curriculum structure  
- Replace PDFs inside `study_material/` with relevant content  

---

### 5. Run the app
```bash
streamlit run app.py
```

---

## 🖥️ Usage

1. Sign up using email OTP  
2. Login with your email  
3. Select subject and chapter from sidebar  
4. Study using videos, PDFs, and transcripts  
5. Generate and attempt quizzes  
6. Track performance in dashboard  
7. Upload PDFs and ask questions  
8. Use YouTube transcription tool for summaries, translation, and study guides  

---

## ⚠️ Important Notes

- Do not commit `.streamlit/secrets.toml`  
- Database is auto-created on first run  
- Internet required for AI features, email OTP, and YouTube transcription  
- Study material PDFs must be added manually  

---

## 📄 Internship

Developed during **Spring Internship 2026**  
**IDEAS — Institute of Data Engineering, Analytics and Science Foundation, ISI Kolkata**  
(21 Jan 2026 – 31 Mar 2026)

---

## 📌 Summary

GyaanSetu is a flexible, AI-driven learning platform where the curriculum is fully configurable through input data. With the addition of a PDF Q&A chatbot and YouTube transcription tool, it enables interactive, query-driven learning and content understanding across multiple formats.