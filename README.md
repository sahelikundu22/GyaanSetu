# GyaanSetu

## Overview
GyaanSetu is a Streamlit-based educational platform for CBSE students to access study materials,
ask questions about PDF documents, and test their knowledge through quizzes.
The platform provides secure authentication, subject-wise learning resources,
an AI-powered PDF Q&A system, and a scoring system to track student performance.

## Features

### Authentication
- User signup with email validation and OTP verification via SMTP
- User login using registered email
- Session management using Streamlit session state
- Toggle between Signup and Login

### Dashboard
- Displays logged-in user name, email, and points earned from quizzes

### Sidebar
- Subject and chapter selection based on CBSE curriculum (2024-26)
- Curriculum data loaded from `cbse_data.json`

### Study Materials
- View study notes online
- Download notes for offline study based on selected subject and chapter

### Quiz System
- Attempt quizzes related to the selected chapter
- Final score displayed after completing the quiz
- Points stored and updated in the SQLite database

### PDF Q&A (AI-Powered)
- Upload any PDF document and ask questions about its content
- Supports all languages — ask in any language, get answers in the same language
- Semantic search using sentence embeddings to retrieve relevant chunks
- LLaMA 3.3 70B via Groq generates accurate, complete answers
- Chat history with memory — follow-up questions are understood in context
- Answer highlighted and scrolled to directly in the PDF preview

## Technology Stack
| Component        | Technology                        |
|-----------------|-----------------------------------|
| UI Framework     | Streamlit                         |
| Backend          | Python                            |
| Database         | SQLite                            |
| Email OTP        | SMTP                              |
| Session Handling | Streamlit Session State           |
| PDF Extraction   | pdfplumber                        |
| PDF Preview      | streamlit-pdf-viewer              |
| Embeddings       | sentence-transformers (MiniLM)    |
| Semantic Search  | Cosine Similarity (numpy)         |
| AI Q&A           | LLaMA 3.3 70B via Groq API        |
| Curriculum Data  | CBSE 2024-26 JSON                 |

## Project Structure
```
GyaanSetu/
├── .streamlit/
│   └── secrets.toml          ← GROQ_API_KEY
│
├── pdf_qna_engine/
│   ├── __init__.py
│   ├── processor.py          ← PDF extraction + chunking + embeddings
│   ├── search.py             ← semantic search
│   ├── llm.py                ← Groq Q&A
│   └── highlighter.py        ← PDF answer highlighting
│
├── pages/
│   └── pdf_qna.py            ← PDF Q&A page
│
├── notes/                    ← study material files
├── quizzes/                  ← quiz data files
│
├── app.py                    ← main entry point
├── auth.py                   ← authentication logic
├── database.py               ← SQLite database operations
├── quiz.py                   ← quiz logic and scoring
├── sidebar.py                ← sidebar component
├── cbse_data.json            ← CBSE curriculum 2024-26
├── requirements.txt
└── README.md
```

## How to Run

1. Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

2. Add your Groq API key to `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_your_key_here"
SENDER_EMAIL = ""
EMAIL_PASS = ""
```

3. Run the application:
```bash
streamlit run app.py
```

## Requirements
```
streamlit
streamlit-pdf-viewer
pdfplumber
sentence-transformers
numpy
requests
```

## How PDF Q&A Works
1. Upload a PDF — preview appears instantly
2. Text is extracted and split into 150-word overlapping chunks
3. Each chunk is converted to a vector embedding using MiniLM
4. On each question, the top 5 most relevant chunks are retrieved via cosine similarity
5. LLaMA 3.3 70B reads the chunks and generates a complete answer
6. The answer is located in the PDF and highlighted in yellow with auto-scroll
7. Full conversation history is passed to Groq so follow-up questions work naturally