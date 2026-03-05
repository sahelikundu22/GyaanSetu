# GyaanSetu

## Overview
- GyaanSetu is a Streamlit-based educational platform for students to access study materials and test their knowledge through quizzes.
- The platform provides secure authentication, subject-wise learning resources, and a scoring system to track student performance.

## Work Done

- Built a **Streamlit application** with a modular project structure.
- Organized the project into separate files:
  - `app.py` – Main application
  - `auth.py` – Authentication logic
  - `database.py` – Database operations
  - `quiz.py` – Quiz logic and scoring

- Created an **SQLite database** to store user information such as:
  - Name  
  - Email  
  - Points

- Implemented **user signup** with:
  - Email validation
  - OTP verification using SMTP.

- Implemented **user login** using the registered email stored in the database.

- Used **Streamlit session state** to manage authentication and maintain user login sessions.

- Added a **toggle option for Signup and Login** within the application.

- Created a **user dashboard** that displays:
  - Logged-in user name
  - Email
  - Points earned from quizzes.

- Added a **sidebar section** where students can choose:
  - Subject
  - Chapter.

- Based on the selected **subject and chapter**, students can:
  - View study notes online
  - Download notes for offline study.

- Implemented a **quiz system** where:
  - Students can attempt quizzes related to the selected chapter.
  - The final score is displayed after completing the quiz.
  - Points are stored and updated in the database.

## Technology Stack
- Streamlit – Application framework and UI
- Python – Backend logic
- SQLite – Database
- SMTP – Email OTP verification
- Streamlit Session State – User authentication and session handling

## Project Structure
GyaanSetu  
├── app.py  
├── auth.py  
├── database.py  
├── quiz.py  
├── notes/  
├── quizzes/  
└── README.md  

## How to Run
- Install dependency:
  - `pip install streamlit`
- Run the application:
  - `streamlit run app.py`
