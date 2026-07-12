"""
extractor.py

Extract structured information from resumes using
Google Gemini (google-genai SDK) and spaCy.
"""

import json
import re

import spacy
from google import genai

from config import GEMINI_API_KEY, MODEL_NAME

# -------------------------------------------------
# Configure Gemini Client
# -------------------------------------------------
client = genai.Client(api_key=GEMINI_API_KEY)

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

def extract_resume_information(resume_text, job_description, similarity_score):
    """
    Extracts structured resume information and generates
    a short HR reasoning in ONE Gemini API call.
    """

    resume_text = clean_text(resume_text)

    prompt = f"""
    You are an expert HR Resume Screening Assistant.

    Job Description:
    {job_description}

    Semantic Similarity Score:
    {similarity_score:.2f}

    Resume:
    {resume_text}

    Analyze the resume.

    Return ONLY valid JSON.

    {{
        "skills": [],
        "experience": "",
        "education": "",
        "certifications": [],
        "projects": [],
        "reason": ""
    }}

    Rules:
    - Return valid JSON only.
    - Do not use markdown.
    - Do not wrap JSON inside ```.

    The "reason" should:
    - Be under 60 words.
    - Mention strengths.
    - Mention missing skills (if any).
    - Mention overall suitability.
    """

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        text = response.text.strip()

        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)
        text = text.strip()

        data = json.loads(text)

        return data

    except Exception as e:

        print(f"Gemini Error:\n{e}")

        return {
            "skills": [],
            "experience": "",
            "education": "",
            "certifications": [],
            "projects": [],
            "reason": "Reasoning could not be generated."
        }
