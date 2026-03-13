import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import json
import re


def generate_ai_quiz(pdf_file, num_q=5):
    """
    Generate MCQ quiz from uploaded PDF using OpenAI.
    Optimized for lightweight processing.
    """

    try:
        # ---------- Extract text from PDF ----------
        reader = PdfReader(pdf_file)

        extracted_text = ""
        max_pages = min(8, len(reader.pages))

        for i in range(max_pages):
            text = reader.pages[i].extract_text()
            if text:
                extracted_text += text + " "

        if not extracted_text.strip():
            return {"error": "Could not extract text from the PDF."}

        context = extracted_text[:5000]

        # ---------- OpenAI Client ----------
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        # ---------- Prompt ----------
        prompt = f"""
        You are an educational quiz generator.

        Based on the following study material, generate {num_q} multiple choice questions.

        Context:
        {context}

        Rules:
        - Each question must have exactly 4 options
        - Only one correct answer
        - Questions should be suitable for school students
        - Keep language simple

        Return ONLY valid JSON in this format:

        [
          {{
            "q": "Question text",
            "o": ["Option A","Option B","Option C","Option D"],
            "a": "Correct Option Text"
          }}
        ]
        """

        # ---------- AI Request ----------
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You generate educational quizzes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        text = response.choices[0].message.content.strip()

        # ---------- Clean JSON ----------
        text = re.sub(r"```json|```", "", text).strip()

        start = text.find("[")
        end = text.rfind("]") + 1

        if start == -1 or end == -1:
            return {"error": "AI response format incorrect."}

        json_str = text[start:end]

        quiz_data = json.loads(json_str)

        # ---------- Validate ----------
        if not isinstance(quiz_data, list):
            return {"error": "Invalid quiz format."}

        for q in quiz_data:
            if not all(k in q for k in ("q", "o", "a")):
                return {"error": "Missing fields in quiz data."}

        return quiz_data

    except Exception as e:
        return {"error": str(e)}