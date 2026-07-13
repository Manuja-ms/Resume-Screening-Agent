"""
Unit tests for similarity.py
"""

import numpy as np
from unittest.mock import patch

from modules.similarity import (
    get_embedding,
    calculate_similarity,
    batch_similarity
)


# -----------------------------
# get_embedding()
# -----------------------------

def test_get_embedding_returns_numpy_array():
    embedding = get_embedding("Python developer")

    assert isinstance(embedding, np.ndarray)
    assert embedding.ndim == 1
    assert len(embedding) > 0


def test_get_embedding_empty_string():
    embedding = get_embedding("")

    assert isinstance(embedding, np.ndarray)
    assert embedding.ndim == 1


# -----------------------------
# calculate_similarity()
# -----------------------------

@patch("modules.similarity.get_embedding")
def test_calculate_similarity_identical(mock_embedding):

    vector = np.array([1.0, 2.0, 3.0])

    mock_embedding.return_value = vector

    score = calculate_similarity(
        "Python Developer",
        "Python Developer"
    )

    assert score == 100.0


@patch("modules.similarity.get_embedding")
def test_calculate_similarity_different(mock_embedding):

    mock_embedding.side_effect = [
        np.array([1.0, 0.0]),
        np.array([0.0, 1.0])
    ]

    score = calculate_similarity(
        "Python",
        "Mechanical Engineer"
    )

    assert score == 0.0


# -----------------------------
# batch_similarity()
# -----------------------------

@patch("modules.similarity.get_embedding")
def test_batch_similarity(mock_embedding):

    mock_embedding.side_effect = [
        np.array([1.0, 0.0]),   # JD
        np.array([1.0, 0.0]),   # Resume 1
        np.array([0.0, 1.0])    # Resume 2
    ]

    resumes = [
        {
            "filename": "resume1.pdf",
            "text": "Python Developer"
        },
        {
            "filename": "resume2.pdf",
            "text": "Civil Engineer"
        }
    ]

    results = batch_similarity(
        "Python Developer",
        resumes
    )

    assert len(results) == 2

    assert results[0]["filename"] == "resume1.pdf"
    assert results[0]["similarity"] == 100.0

    assert results[1]["filename"] == "resume2.pdf"
    assert results[1]["similarity"] == 0.0


@patch("modules.similarity.get_embedding")
def test_batch_similarity_empty(mock_embedding):

    mock_embedding.return_value = np.array([1.0, 0.0])

    results = batch_similarity(
        "Python Developer",
        []
    )

    assert results == []