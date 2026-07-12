"""
Ranker Module

Sorts candidates based on their final score.
"""

from typing import List, Dict


def rank_candidates(candidates: List[Dict]) -> List[Dict]:
    """
    Sort candidates by Final Score in descending order
    and assign ranks.

    Parameters:
        candidates (list): List of candidate dictionaries

    Returns:
        list: Ranked candidate list
    """

    if not candidates:
        return []

    # Sort candidates by Final Score (highest first)
    ranked = sorted(
        candidates,
        key=lambda x: float(x.get("Final Score", 0)),
        reverse=True
    )

    # Assign rank
    for index, candidate in enumerate(ranked, start=1):
        candidate["Rank"] = index

    return ranked


def display_top_candidates(ranked_candidates: List[Dict], top_n: int = 5):
    """
    Display the top N ranked candidates.

    Parameters:
        ranked_candidates (list): Ranked candidate list
        top_n (int): Number of top candidates to display
    """

    print("\n" + "=" * 70)
    print("TOP CANDIDATES")
    print("=" * 70)

    for candidate in ranked_candidates[:top_n]:
        print(
            f"Rank: {candidate['Rank']}\n"
            f"Resume: {candidate['Filename']}\n"
            f"Final Score: {candidate['Final Score']:.2f}\n"
            f"Reason: {candidate['Reason']}\n"
        )
        print("-" * 70)