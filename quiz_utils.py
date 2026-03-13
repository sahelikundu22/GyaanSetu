import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import json
import re


def generate_ai_quiz(pdf_file, num_q=5):

    try:
        # Extract text from PDF
        reader = PdfReader(pdf_file)

        text = ""
        pages_to_read = min(5, len(reader.pages))

        for i in range(pages_to_read):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text += page_text + " "

        if not text.strip():
            return {"error": "Could not read text from PDF"}

        context = text[:4000]

        # OpenAI client
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        prompt = f"""
        Create {num_q} multiple choice questions from the following study material.

        Context:
        {context}

        Return ONLY JSON in this format:

        [
        {{
        "q": "Question text",
        "o": ["A","B","C","D"],
        "a": "Correct option text"
        }}
        ]
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You generate educational quizzes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        result = response.choices[0].message.content

        # Clean JSON
        result = re.sub(r"```json|```", "", result).strip()

        start = result.find("[")
        end = result.rfind("]") + 1

        json_str = result[start:end]

        quiz = json.loads(json_str)

        return quiz

    except Exception as e:
        return {"error": str(e)}