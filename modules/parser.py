"""
Resume Parser Module

Reads PDF, DOCX and TXT resumes
Returns plain text.
"""

import os
from PyPDF2 import PdfReader
from docx import Document

from config import SUPPORTED_FORMATS


def read_pdf(file_path):
    """
    Read PDF file.
    """

    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text.strip()


def read_docx(file_path):
    """
    Read DOCX file.
    """

    doc = Document(file_path)

    paragraphs = [p.text for p in doc.paragraphs]

    return "\n".join(paragraphs)


def read_txt(file_path):
    """
    Read TXT file.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def parse_resume(file_path):
    """
    Detect file type and parse.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return read_pdf(file_path)

    elif extension == ".docx":
        return read_docx(file_path)

    elif extension == ".txt":
        return read_txt(file_path)

    else:
        raise ValueError(f"Unsupported file format: {extension}")


def load_all_resumes(folder_path):
    """
    Reads every resume inside the folder.

    Returns

    [
        {
            "filename":"resume1.pdf",
            "text":"..."
        },
        ...
    ]
    """

    resumes = []

    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    for filename in os.listdir(folder_path):
        if filename.startswith("."):
            continue

        extension = os.path.splitext(filename)[1].lower()

        if extension not in SUPPORTED_FORMATS:
            continue

        file_path = os.path.join(folder_path, filename)

        print(f"Reading {filename}")

        try:
            text = parse_resume(file_path)

            resumes.append({
                "filename": filename,
                "text": text
            })

        except Exception as e:
            print(f"Could not read {filename}: {e}")

    return resumes