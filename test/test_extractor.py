import pytest
from unittest.mock import patch, MagicMock

from modules.extractor import (
    clean_text,
    extract_resume_information
)


# ---------------------------------------
# Test clean_text()
# ---------------------------------------

def test_clean_text_removes_extra_spaces():
    text = "Python     Developer\n\nwith    AI skills"

    cleaned = clean_text(text)

    assert isinstance(cleaned, str)
    assert "Python" in cleaned
    assert "Developer" in cleaned
    assert "AI" in cleaned


def test_clean_text_empty():
    assert clean_text("") == ""


# ---------------------------------------
# Test extract_resume_information()
# ---------------------------------------

@patch("modules.extractor.client.models.generate_content")
def test_extract_resume_information_success(mock_generate):
    mock_response = MagicMock()

    mock_response.text = """
    {
        "skills": ["Python", "Machine Learning"],
        "experience": "3 years",
        "education": "B.E Computer Science",
        "certifications": ["AWS"],
        "projects": ["Resume Screening"],
        "reason": "Good candidate with relevant skills."
    }
    """

    mock_generate.return_value = mock_response

    result = extract_resume_information(
        "Python developer with ML experience",
        "Need Python and ML engineer",
        0.92
    )

    assert result["skills"] == ["Python", "Machine Learning"]
    assert result["experience"] == "3 years"
    assert result["education"] == "B.E Computer Science"
    assert result["certifications"] == ["AWS"]
    assert result["projects"] == ["Resume Screening"]
    assert "Good candidate" in result["reason"]


@patch("modules.extractor.client.models.generate_content")
def test_extract_resume_information_markdown_json(mock_generate):
    mock_response = MagicMock()

    mock_response.text = """
    ```json
    {
        "skills": ["Python"],
        "experience": "2 years",
        "education": "B.Tech",
        "certifications": [],
        "projects": [],
        "reason": "Suitable candidate."
    }
    ```
    """

    mock_generate.return_value = mock_response

    result = extract_resume_information(
        "Python Developer",
        "Python Developer",
        0.90
    )

    assert result["skills"] == ["Python"]
    assert result["experience"] == "2 years"
    assert result["reason"] == "Suitable candidate."


@patch("modules.extractor.client.models.generate_content")
def test_extract_resume_information_api_failure(mock_generate):
    mock_generate.side_effect = Exception("Gemini API Error")

    result = extract_resume_information(
        "Resume text",
        "Job description",
        0.75
    )

    assert result["skills"] == []
    assert result["experience"] == ""
    assert result["education"] == ""
    assert result["certifications"] == []
    assert result["projects"] == []
    assert result["reason"] == "Reasoning could not be generated."


@patch("modules.extractor.client.models.generate_content")
def test_extract_resume_information_invalid_json(mock_generate):
    mock_response = MagicMock()
    mock_response.text = "Invalid JSON Response"

    mock_generate.return_value = mock_response

    result = extract_resume_information(
        "Resume",
        "Job",
        0.50
    )

    assert result["skills"] == []
    assert result["reason"] == "Reasoning could not be generated."