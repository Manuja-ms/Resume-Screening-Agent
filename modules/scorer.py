"""
Scorer Module

Calculates the final weighted score for each candidate.
"""

import re


# -----------------------------
# Helper Functions
# -----------------------------

def calculate_skill_score(skills):
    """
    Calculates skill score based on the number of extracted skills.

    Maximum score = 100
    """

    if not skills:
        return 0

    skill_count = len(skills)

    # Assume 10 or more skills = full score
    score = min(skill_count, 10) * 10

    return score


def calculate_experience_score(experience):
    """
    Converts years of experience into a score.

    Example:
        0 years -> 0
        2 years -> 40
        5 years -> 100
    """

    if not experience:
        return 0

    match = re.search(r"(\d+)", str(experience))

    if match:

        years = int(match.group(1))

        score = min(years, 5) * 20

        return score

    return 0


def calculate_education_score(education):
    """
    Gives score based on education level.
    """

    if not education:
        return 0

    education = education.lower()

    if "phd" in education:
        return 100

    elif "master" in education or "m.tech" in education or "m.e" in education:
        return 90

    elif "bachelor" in education or "b.tech" in education or "b.e" in education:
        return 80

    elif "diploma" in education:
        return 60

    return 40


# -----------------------------
# Final Score
# -----------------------------

def calculate_final_score(extracted_data, similarity_score):
    """
    Calculates weighted score.

    Parameters
    ----------
    extracted_data : dict

        {
            "skills": [...],
            "experience": "...",
            "education": "..."
        }

    similarity_score : float

        Semantic similarity (0-100)

    Returns
    -------
    float
        Final weighted score
    """

    skill_score = calculate_skill_score(
        extracted_data.get("skills", [])
    )

    experience_score = calculate_experience_score(
        extracted_data.get("experience", "")
    )

    education_score = calculate_education_score(
        extracted_data.get("education", "")
    )

    final_score = (

        similarity_score * 0.60 +

        skill_score * 0.20 +

        experience_score * 0.15 +

        education_score * 0.05

    )

    return float(round(final_score, 2))