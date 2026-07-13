"""
Unit tests for scorer.py
"""

import pytest

from modules.scorer import (
    calculate_skill_score,
    calculate_experience_score,
    calculate_education_score,
    calculate_final_score
)


# -----------------------------
# Skill Score Tests
# -----------------------------

def test_skill_score_empty():
    assert calculate_skill_score([]) == 0


def test_skill_score_five_skills():
    skills = ["Python", "SQL", "Java", "Git", "Docker"]
    assert calculate_skill_score(skills) == 50


def test_skill_score_max():
    skills = [
        "Python", "Java", "C++", "SQL", "Git",
        "Docker", "AWS", "Linux", "HTML", "CSS",
        "JavaScript", "React"
    ]
    assert calculate_skill_score(skills) == 100


# -----------------------------
# Experience Score Tests
# -----------------------------

def test_experience_none():
    assert calculate_experience_score("") == 0


def test_experience_two_years():
    assert calculate_experience_score("2 years") == 40


def test_experience_five_years():
    assert calculate_experience_score("5 years") == 100


def test_experience_more_than_five():
    assert calculate_experience_score("10 years") == 100


def test_experience_invalid():
    assert calculate_experience_score("No experience") == 0


# -----------------------------
# Education Score Tests
# -----------------------------

def test_education_phd():
    assert calculate_education_score("PhD in Computer Science") == 100


def test_education_mtech():
    assert calculate_education_score("M.Tech") == 90


def test_education_be():
    assert calculate_education_score("B.E") == 80


def test_education_btech():
    assert calculate_education_score("B.Tech") == 80


def test_education_diploma():
    assert calculate_education_score("Diploma in CSE") == 60


def test_education_other():
    assert calculate_education_score("PUC") == 40


def test_education_empty():
    assert calculate_education_score("") == 0


# -----------------------------
# Final Score Tests
# -----------------------------

def test_final_score():

    extracted_data = {
        "skills": ["Python", "SQL", "Java", "Git", "Docker"],
        "experience": "3 years",
        "education": "B.Tech"
    }

    similarity = 80

    score = calculate_final_score(extracted_data, similarity)

    expected = (
        80 * 0.60 +     # similarity
        50 * 0.20 +     # skills
        60 * 0.15 +     # experience
        80 * 0.05       # education
    )

    assert score == round(expected, 2)


def test_final_score_empty_data():

    extracted_data = {
        "skills": [],
        "experience": "",
        "education": ""
    }

    score = calculate_final_score(extracted_data, 0)

    assert score == 0.0