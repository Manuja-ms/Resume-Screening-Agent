"""
similarity.py

Computes semantic similarity between
Job Description and Resume using
SentenceTransformer embeddings.
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config import EMBEDDING_MODEL

# Load the embedding model once
print("Loading Sentence Transformer model...")
model = SentenceTransformer(EMBEDDING_MODEL)
print("Model loaded successfully.")


def get_embedding(text):
    """
    Convert text into an embedding vector.

    Parameters
    ----------
    text : str
        Input text

    Returns
    -------
    numpy.ndarray
        Embedding vector
    """

    if not text:
        text = ""

    embedding = model.encode(
        text,
        convert_to_numpy=True
    )

    return embedding


def calculate_similarity(job_description, resume_text):
    """
    Calculate semantic similarity between
    Job Description and Resume.

    Parameters
    ----------
    job_description : str

    resume_text : str

    Returns
    -------
    float
        Similarity score (0-100)
    """

    jd_embedding = get_embedding(job_description)
    resume_embedding = get_embedding(resume_text)

    similarity = cosine_similarity(
        [jd_embedding],
        [resume_embedding]
    )[0][0]

    similarity_percentage = float(round(float(similarity) * 100, 2))

    return similarity_percentage


def batch_similarity(job_description, resumes):
    """
    Calculate similarity for multiple resumes.

    Parameters
    ----------
    job_description : str

    resumes : list
        [
            {
                "filename": "...",
                "text": "..."
            }
        ]

    Returns
    -------
    list
    """

    results = []

    jd_embedding = get_embedding(job_description)

    for resume in resumes:

        resume_embedding = get_embedding(resume["text"])

        score = cosine_similarity(
            [jd_embedding],
            [resume_embedding]
        )[0][0]

        results.append(
            {
                "filename": resume["filename"],
                "similarity": float(round(float(score) * 100, 2))
            }
        )

    return results
