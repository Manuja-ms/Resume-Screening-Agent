"""
Unit tests for ranker.py
"""

import pytest
from modules.ranker import rank_candidates


def test_rank_candidates_sorting():
    """Candidates should be sorted by Final Score in descending order."""

    candidates = [
        {"Filename": "A.pdf", "Final Score": 75},
        {"Filename": "B.pdf", "Final Score": 92},
        {"Filename": "C.pdf", "Final Score": 81},
    ]

    ranked = rank_candidates(candidates)

    assert ranked[0]["Filename"] == "B.pdf"
    assert ranked[1]["Filename"] == "C.pdf"
    assert ranked[2]["Filename"] == "A.pdf"


def test_rank_assignment():
    """Ranks should be assigned correctly."""

    candidates = [
        {"Filename": "A.pdf", "Final Score": 60},
        {"Filename": "B.pdf", "Final Score": 90},
        {"Filename": "C.pdf", "Final Score": 80},
    ]

    ranked = rank_candidates(candidates)

    assert ranked[0]["Rank"] == 1
    assert ranked[1]["Rank"] == 2
    assert ranked[2]["Rank"] == 3


def test_empty_candidate_list():
    """An empty input should return an empty list."""

    ranked = rank_candidates([])

    assert ranked == []


def test_missing_final_score():
    """Candidates without Final Score should be treated as 0."""

    candidates = [
        {"Filename": "A.pdf"},
        {"Filename": "B.pdf", "Final Score": 50},
    ]

    ranked = rank_candidates(candidates)

    assert ranked[0]["Filename"] == "B.pdf"
    assert ranked[0]["Rank"] == 1

    assert ranked[1]["Filename"] == "A.pdf"
    assert ranked[1]["Rank"] == 2


def test_string_final_score():
    """String scores should be converted to float correctly."""

    candidates = [
        {"Filename": "A.pdf", "Final Score": "88.5"},
        {"Filename": "B.pdf", "Final Score": "92"},
    ]

    ranked = rank_candidates(candidates)

    assert ranked[0]["Filename"] == "B.pdf"
    assert ranked[1]["Filename"] == "A.pdf"


def test_same_scores():
    """Candidates with equal scores should both receive valid ranks."""

    candidates = [
        {"Filename": "A.pdf", "Final Score": 80},
        {"Filename": "B.pdf", "Final Score": 80},
    ]

    ranked = rank_candidates(candidates)

    assert len(ranked) == 2
    assert ranked[0]["Rank"] == 1
    assert ranked[1]["Rank"] == 2