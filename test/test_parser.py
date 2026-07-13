import os
from pathlib import Path

import pytest
from docx import Document
from reportlab.pdfgen import canvas

from modules.parser import (
    read_pdf,
    read_docx,
    read_txt,
    parse_resume,
    load_all_resumes,
)


# ---------- Helper functions ----------

def create_txt(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def create_docx(path, text):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(path)


def create_pdf(path, text):
    c = canvas.Canvas(str(path))
    c.drawString(100, 750, text)
    c.save()


# ---------- Tests ----------

def test_read_txt(tmp_path):
    file = tmp_path / "resume.txt"
    create_txt(file, "Python Developer")

    text = read_txt(file)

    assert "Python Developer" in text


def test_read_docx(tmp_path):
    file = tmp_path / "resume.docx"
    create_docx(file, "Machine Learning Engineer")

    text = read_docx(file)

    assert "Machine Learning Engineer" in text


def test_read_pdf(tmp_path):
    file = tmp_path / "resume.pdf"
    create_pdf(file, "Data Scientist")

    text = read_pdf(file)

    assert "Data Scientist" in text


def test_parse_resume_txt(tmp_path):
    file = tmp_path / "resume.txt"
    create_txt(file, "Java Developer")

    text = parse_resume(file)

    assert "Java Developer" in text


def test_parse_resume_docx(tmp_path):
    file = tmp_path / "resume.docx"
    create_docx(file, "AI Engineer")

    text = parse_resume(file)

    assert "AI Engineer" in text


def test_parse_resume_pdf(tmp_path):
    file = tmp_path / "resume.pdf"
    create_pdf(file, "Cloud Engineer")

    text = parse_resume(file)

    assert "Cloud Engineer" in text


def test_parse_resume_invalid_extension(tmp_path):
    file = tmp_path / "resume.xyz"

    create_txt(file, "Unsupported")

    with pytest.raises(ValueError):
        parse_resume(file)


def test_load_all_resumes(tmp_path):
    create_txt(tmp_path / "resume1.txt", "Python")

    create_docx(tmp_path / "resume2.docx", "Java")

    create_pdf(tmp_path / "resume3.pdf", "SQL")

    resumes = load_all_resumes(tmp_path)

    assert len(resumes) == 3

    filenames = [r["filename"] for r in resumes]

    assert "resume1.txt" in filenames
    assert "resume2.docx" in filenames
    assert "resume3.pdf" in filenames


def test_load_all_resumes_empty_folder(tmp_path):
    resumes = load_all_resumes(tmp_path)

    assert resumes == []


def test_load_all_resumes_invalid_folder():
    with pytest.raises(FileNotFoundError):
        load_all_resumes("folder_that_does_not_exist")