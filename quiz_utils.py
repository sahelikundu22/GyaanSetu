from groq import Groq
from PyPDF2 import PdfReader
import streamlit as st
import json
import re


def generate_ai_quiz(pdf_path, num_q=10):

    try:
        reader = PdfReader(pdf_path)

        text = ""
        pages_to_read = min(6, len(reader.pages))

        for i in range(pages_to_read):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text += page_text + " "

        if not text.strip():
            return {"error": "Could not read PDF content"}

        context = text[:3500]

        client = Groq(api_key=st.secrets["GROQ_API_KEY"])

        prompt = f"""
        You are an educational quiz generator.

        Using the following study material, create {num_q} multiple choice questions.

        Context:
        {context}

        Rules:
        - Each question must have exactly 4 options
        - Only one correct answer
        - Language should be simple for school students

        Return ONLY JSON in this format:

        [
        {{
        "q": "Question text",
        "o": ["Option A","Option B","Option C","Option D"],
        "a": "Correct option text"
        }}
        ]
        """
      

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You create educational quizzes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        result = response.choices[0].message.content

        # Clean JSON
        result = re.sub(r"```json|```", "", result).strip()

        start = result.find("[")
        end = result.rfind("]") + 1

        quiz_data = json.loads(result[start:end])

        return quiz_data

    except Exception as e:
        return {"error": str(e)}