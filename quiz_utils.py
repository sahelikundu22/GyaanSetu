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

        # 🌐 Language selection
        lang = st.session_state.get("language", "English")

        if lang == "Hindi":
            lang_prompt = "Generate questions in Hindi."
        elif lang == "Bengali":
            lang_prompt = "Generate questions in Bengali."
        else:
            lang_prompt = "Generate questions in English."


        prompt = f"""{lang_prompt}
        You are an educational quiz generator.

        Using the following study material, create {num_q} multiple choice questions.

        Context:
        {context}
        STRICT INSTRUCTIONS:
        - Generate EXACTLY {num_q} questions
        - No explanation, no markdown
        - Use double quotes ONLY
        - Each question must have exactly 4 options
        - Only one correct answer
        - Language should be simple for school students
        - Return ONLY valid JSON
        - Each question MUST be separate and complete.
        - Do NOT merge questions.

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

        raw = response.choices[0].message.content


        # Remove markdown
        clean = re.sub(r"```json|```", "", raw).strip()

        # 🔥 Extract each question object safely
        objects = re.findall(r"\{.*?\}", clean, re.DOTALL)

        quiz = []

        for obj in objects:
            try:
                q = json.loads(obj)
                if "q" in q and "o" in q and "a" in q:
                    if len(q["o"]) == 4:
                        quiz.append(q)
            except:
                continue

        # 🔥 Ensure exact number of questions
        if len(quiz) > num_q:
            quiz = quiz[:num_q]

        if len(quiz) == 0:
            return {"error": "AI returned invalid quiz format"}

        MAX_RETRIES = 3

        all_questions = []

        for attempt in range(MAX_RETRIES):

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You create educational quizzes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )

            raw = response.choices[0].message.content

            clean = re.sub(r"```json|```", "", raw).strip()

            objects = re.findall(r"\{.*?\}", clean, re.DOTALL)

            for obj in objects:
                try:
                    q = json.loads(obj)
                    if "q" in q and "o" in q and "a" in q:
                        if len(q["o"]) == 4:
                            all_questions.append(q)
                except:
                    continue

            # ✅ STOP when enough questions collected
            if len(all_questions) >= num_q:
                break

        # ✅ FINAL CUT
        final_quiz = all_questions[:num_q]

        if len(final_quiz) < num_q:
            return {"error": "Could not generate enough valid questions"}

        return final_quiz


    except Exception as e:
        return {"error": str(e)}