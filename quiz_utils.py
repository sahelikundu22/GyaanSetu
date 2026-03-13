import google.generativeai as genai
from PyPDF2 import PdfReader
import json
import re
import streamlit as st

def generate_quiz_low_bandwidth(pdf_file, num_questions=3):
    """
    Optimized for rural use: 
    - Extracts only the first few pages to save processing time.
    - Limits character count strictly to reduce data packets.
    """
    try:
        reader = PdfReader(pdf_file)
        text = ""
        # Only read the first 3 pages to minimize data processing
        pages_to_read = min(len(reader.pages), 3)
        for i in range(pages_to_read):
            text += reader.pages[i].extract_text()
        
        # Strip extra whitespace to shrink the string size
        context = " ".join(text.split())[:5000] 

        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Short, precise prompt to get a compact JSON response
        prompt = f"""
        Text: {context}
        Task: Create {num_questions} MCQ. 
        Format: JSON list [ {{"q": "...", "o": ["a", "b", "c", "d"], "a": "correct_option"}} ]
        """

        response = model.generate_content(prompt)
        json_str = re.sub(r"```json|```", "", response.text).strip()
        return json.loads(json_str)
    except Exception as e:
        return {"error": str(e)}