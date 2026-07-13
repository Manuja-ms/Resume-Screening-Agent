import os

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
MODEL_NAME = "gemini-3.5-flash"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

RESUME_FOLDER = os.path.join(DATA_DIR, "resumes")

JOB_DESCRIPTION_FILE = os.path.join(DATA_DIR, "job_description", "jd.txt")

OUTPUT_FOLDER = os.path.join(DATA_DIR, "output")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CSV_OUTPUT = os.path.join(
    OUTPUT_FOLDER,
    "ranked_candidates.csv"
)

JSON_OUTPUT = os.path.join(
    OUTPUT_FOLDER,
    "ranked_candidates.json"
)

SUPPORTED_FORMATS = [".pdf", ".docx", ".txt"]
