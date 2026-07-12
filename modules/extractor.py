"""
extractor.py

Extract structured information from resumes using
Google Gemini (google-genai SDK) and spaCy.
"""

import json
import re

import spacy
from google import genai

from config import GEMINI_API_KEY

# -------------------------------------------------
# Configure Gemini Client
# -------------------------------------------------
client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.5-flash"

# -------------------------------------------------
# Load spaCy
# -------------------------------------------------

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    raise Exception(
        "spaCy English model not installed.\n"
        "Run:\n"
        "python -m spacy download en_core_web_sm"
    )


# -------------------------------------------------
# Clean Resume Text
# -------------------------------------------------

def clean_text(text):
    """
    Removes unnecessary spaces while preserving words.
    """

    doc = nlp(text)

    cleaned = []

    for token in doc:
        if not token.is_space:
            cleaned.append(token.text)

    return " ".join(cleaned)


# -------------------------------------------------
# Resume Information Extraction
# -------------------------------------------------

def extract_resume_information(resume_text):
    """
    Extracts resume information using Gemini.

    Returns:

    {
        "skills": [],
        "experience": "",
        "education": "",
        "certifications": [],
        "projects": []
    }
    """

    resume_text = clean_text(resume_text)

    prompt = f"""
        You are an expert HR Resume Screening Assistant.

        Extract ONLY the following information.

        Return ONLY valid JSON.

        Format:

        {{
            "skills": [],
            "experience": "",
            "education": "",
            "certifications": [],
            "projects": []
        }}

        Rules:

        - Return only JSON.
        - Do not explain anything.
        - Do not use markdown.
        - Do not wrap JSON inside ```.

        Resume:

        {resume_text}
    """

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown if the model returns it
        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)
        text = text.strip()

        data = json.loads(text)

        return data

    except Exception as e:

        print(f"Gemini Extraction Error:\n{e}")

        return {
            "skills": [],
            "experience": "",
            "education": "",
            "certifications": [],
            "projects": []
        }
