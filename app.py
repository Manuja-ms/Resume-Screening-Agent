"""
Resume Screening Agent

Main Application
"""

import os

from config import (
    JOB_DESCRIPTION_FILE,
    RESUME_FOLDER,
    OUTPUT_FOLDER
)

from modules.parser import load_all_resumes

# These modules will be created next
from modules.extractor import extract_resume_information
from modules.similarity import calculate_similarity
from modules.scorer import calculate_final_score
from modules.ranker import (
    rank_candidates,
    display_top_candidates
)
from modules.exporter import export_results

def load_job_description():

    with open(JOB_DESCRIPTION_FILE, "r", encoding="utf-8") as f:
        return f.read()


def main():

    print("=" * 50)
    print("Resume Screening Agent")
    print("=" * 50)

    print("\nLoading Job Description...")

    jd = load_job_description()

    print("Done.")

    print("\nLoading Resumes...")

    resumes = load_all_resumes(RESUME_FOLDER)

    print(f"{len(resumes)} resumes found.\n")

    candidates = []

    for resume in resumes:

        print("-" * 40)

        print(f"Processing {resume['filename']}")

        similarity = calculate_similarity(
            jd,
            resume["text"]
        )

        extracted = extract_resume_information(
            resume["text"],
            jd,
            similarity
        )

        score = calculate_final_score(
            extracted,
            similarity
        )

        reason = extracted.get(
            "reason",
            "Reasoning could not be generated."
        )
        
        candidate = {
            "Filename": resume["filename"],
            "Similarity": float(similarity),
            "Final Score": float(score),
            "Skills": extracted.get("skills", []),
            "Experience": extracted.get("experience", ""),
            "Education": extracted.get("education", ""),
            "Reason": extracted.get("reason", "Reasoning could not be generated.")
        }

        candidates.append(candidate)

    ranked_candidates = rank_candidates(candidates)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    export_results(
        ranked_candidates,
        OUTPUT_FOLDER
    )

    print("\nRanking Completed.")

    print("\nTop Candidates\n")

    display_top_candidates(ranked_candidates)

    print("\nResults saved inside data/output/")


if __name__ == "__main__":
    main()
