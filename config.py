import os

# ==============================
# API Configuration
# ==============================

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

# ==============================
# Folder Paths
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

RESUME_FOLDER = os.path.join(DATA_DIR, "resumes")

JOB_DESCRIPTION_FILE = os.path.join(DATA_DIR, "job_description", "jd.txt")

OUTPUT_FOLDER = os.path.join(DATA_DIR, "output")

# ==============================
# NLP Model
# ==============================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ==============================
# Output Files
# ==============================

CSV_OUTPUT = os.path.join(
    OUTPUT_FOLDER,
    "ranked_candidates.csv"
)

JSON_OUTPUT = os.path.join(
    OUTPUT_FOLDER,
    "ranked_candidates.json"
)

# ==============================
# Supported Resume Formats
# ==============================

SUPPORTED_FORMATS = [".pdf", ".docx", ".txt"]