import google.generativeai as genai
from PyPDF2 import PdfReader
import json
import re
import streamlit as st


def generate_ai_quiz(pdf_file, num_q=5):
    """
    Generate MCQ quiz from uploaded PDF using Gemini AI.
    Optimized for lightweight processing.
    """

    try:
        # -------- Extract text from PDF --------
        reader = PdfReader(pdf_file)

        extracted_text = ""
        max_pages = min(8, len(reader.pages))  # limit pages for speed

        for i in range(max_pages):
            page_text = reader.pages[i].extract_text()
            if page_text:
                extracted_text += page_text + " "

        if not extracted_text.strip():
            return {"error": "Could not extract text from PDF."}

        # Reduce context size for faster AI processing
        context = extracted_text[:5000]

        # -------- Configure Gemini --------
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

        model = genai.GenerativeModel("gemini-1.5-flash")

        # -------- Prompt --------
        prompt = f"""
        You are an educational quiz generator.

        Using the following study material, generate {num_q} multiple-choice questions.

        Context:
        {context}

        Rules:
        - Each question must have exactly 4 options
        - Only one option should be correct
        - Questions should test understanding of the concept
        - Keep language simple for school students

        Return ONLY valid JSON in this format:

        [
            {{
                "q": "Question text",
                "o": ["Option A", "Option B", "Option C", "Option D"],
                "a": "Correct Option Text"
            }}
        ]
        """

        # -------- Generate response --------
        response = model.generate_content(prompt)

        if not response.text:
            return {"error": "AI returned empty response."}

        text = response.text.strip()

        # -------- Clean AI response --------
        text = re.sub(r"```json|```", "", text).strip()

        start = text.find("[")
        end = text.rfind("]") + 1

        if start == -1 or end == -1:
            return {"error": "AI response format incorrect."}

        json_str = text[start:end]

        quiz_data = json.loads(json_str)

        # -------- Validate output --------
        if not isinstance(quiz_data, list):
            return {"error": "Invalid quiz format returned by AI."}

        for q in quiz_data:
            if not all(k in q for k in ("q", "o", "a")):
                return {"error": "Quiz format missing required fields."}

        return quiz_data

    except Exception as e:
        return {"error": str(e)}