"""
reasoner.py

Generates an explanation for each ranked candidate.
"""

from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.5-flash"


def generate_reasoning(job_description, extracted_data, similarity_score):
    """
    Generate a short HR explanation for the candidate.
    """

    prompt = f"""
        You are an HR Resume Screening Assistant.

        Job Description:

        {job_description}

        Candidate Information:

        Skills:
        {extracted_data.get("skills", [])}

        Experience:
        {extracted_data.get("experience", "")}

        Education:
        {extracted_data.get("education", "")}

        Semantic Similarity Score:
        {similarity_score:.2f}

        Limit the response to a maximum of 60 words.
        
        Mention:

        - Strengths
        - Missing skills if any
        - Overall suitability

        Return plain text only.
        """

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:

        print("Reasoning Error:", e)

        return "Reasoning could not be generated."