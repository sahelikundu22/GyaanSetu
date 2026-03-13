import google.generativeai as genai
from google.generativeai.types import RequestOptions
from PyPDF2 import PdfReader
import json, re, streamlit as st

def generate_ai_quiz(pdf_file, num_q=5):
    """AI logic optimized for low-bandwidth rural use."""
    try:
        reader = PdfReader(pdf_file)
        # Extract only first 3 pages to save data/processing
        text = " ".join([page.extract_text() for page in reader.pages[:10]])
        context = text[:5000] 
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

        # Force the model to use the standard API version
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            # This bypasses the v1beta issue if it's persisting
        )
        # Configure Gemini
        # Try this version:
        # model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        prompt = f"""
        Context: {context}
        Task: Generate {num_q} multiple choice questions.
        Format: Return ONLY a JSON list of objects with keys "q", "o" (list of 4), and "a" (correct string).
        """
        
        response = model.generate_content(prompt)
        # Clean JSON response
        json_str = re.sub(r"```json|```", "", response.text).strip()
        return json.loads(json_str)
    except Exception as e:
        return {"error": str(e)}
    

