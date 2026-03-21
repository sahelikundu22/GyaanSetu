# 📚 GyaanSetu  
### Connecting Ambition with Education

GyaanSetu is an AI-powered learning platform for CBSE students (Classes 5–8). It combines study material, AI-generated quizzes, performance analytics, and a PDF question-answering assistant into a single Streamlit web application.

---

## 🚀 Features

- 🔐 OTP-based authentication (Gmail SMTP, passwordless login)  
- 📖 Study material with YouTube lessons and inline PDF viewer  
- 🤖 AI quiz generator (10 MCQs from PDFs using LLaMA via Groq)  
- 📊 Performance dashboard with charts, trends, and PDF reports  
- 🔍 PDF Q&A with semantic search and highlighted answers  

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
│   └── pdf_qna.py
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

### 4. Add study material

Place PDFs inside:
```
study_material/<Subject Name>/
```

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
4. Study using videos and PDFs  
5. Generate and attempt quizzes  
6. Track performance in dashboard  
7. Upload PDFs and ask questions  

---

## ⚠️ Important Notes

- Do not commit `.streamlit/secrets.toml`  
- Database is auto-created on first run  
- Internet required for AI features and email OTP  
- Study material PDFs must be added manually  

---

## 📄 Internship

Developed during **Spring Internship 2026**  
**IDEAS — Institute of Data Engineering, Analytics and Science Foundation, ISI Kolkata**  
(21 Jan 2026 – 31 Mar 2026)

---

## 📌 Summary

GyaanSetu integrates AI, data processing, and interactive dashboards to create an intelligent and accessible learning platform for school students.