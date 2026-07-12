# AI Resume Screening Agent

## Overview

The **AI Resume Screening Agent** is an AI-powered application that automates resume screening by comparing candidate resumes against a given job description. It uses Google Gemini for resume information extraction and candidate reasoning, Sentence Transformers for semantic similarity, and a weighted scoring algorithm to rank candidates.

## Features

* Parse resumes in **PDF**, **DOCX**, and **TXT** formats
* Extract candidate information using Google Gemini

  * Skills
  * Experience
  * Education
  * Certifications
  * Projects
* Compute semantic similarity between resumes and the job description
* Calculate weighted candidate scores
* Generate AI-based explanations for each candidate
* Rank candidates automatically
* Export results to **CSV** and **JSON**
* Simple Streamlit web interface

# Project Structure

```text
Resume-Screening-Agent/
│
├── app.py # Command-line application 
├── streamlit_app.py # Streamlit frontend
├── config.py
├── requirements.txt
├── README.md
│
├── modules/
│   ├── parser.py
│   ├── extractor.py
│   ├── similarity.py
│   ├── scorer.py
│   ├── ranker.py
│   ├── reasoner.py
│   └── exporter.py
│
├── data/
│   ├── resumes/
│   ├── job_description/
│   │   └── jd.txt
│   └── output/
│
└── .gitignore
```

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd Resume-Screening-Agent
```

## 2. Create a Conda environment

```bash
conda create -n resume_agent python=3.11
```

Activate it:

```bash
conda activate resume_agent
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you do not have a requirements file, install manually:

```bash
pip install streamlit pandas numpy scikit-learn sentence-transformers spacy google-genai PyPDF2 python-docx openpyxl
```

Download the spaCy English model:

```bash
python -m spacy download en_core_web_sm
```

# Configure the Gemini API Key

Open **config.py** and set your Gemini API key.

```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Alternatively, you can store the key in an environment variable and read it inside `config.py`.

# Input Files

Place resumes inside:

```
data/resumes/
```

Supported formats:

* PDF
* DOCX
* TXT

Place the job description in:

```
data/job_description/jd.txt
```

# Running the Application

## Option 1 – Command Line

```bash
python app.py
```

The application will:

1. Load the job description
2. Parse all resumes
3. Extract candidate information
4. Calculate semantic similarity
5. Compute weighted scores
6. Generate AI reasoning
7. Rank candidates
8. Export results

Results are saved in:

```
data/output/
```

## Option 2 – Streamlit Web Application

Run:

```bash
streamlit run streamlit_app.py
```

Open:

```
http://localhost:8501
```

Upload:

* Job Description
* Multiple resumes

The application displays ranked candidates and allows downloading the results as CSV.

## Model and NLP Approach

### Google Gemini

Google Gemini was selected because it can accurately extract structured information such as skills, education, certifications, projects, and experience from resumes with different formats and writing styles. This reduces the need for complex rule-based extraction.

### Sentence Transformers

The `all-MiniLM-L6-v2` Sentence Transformer model is used to generate semantic embeddings for both the job description and resumes. Unlike keyword matching, semantic embeddings capture contextual meaning, allowing resumes with similar skills expressed using different words to be matched effectively.

### Cosine Similarity

Cosine similarity measures how closely the semantic embeddings of a resume and job description align. The similarity score is converted to a percentage and used as the primary ranking metric.

## Scoring Method

The final candidate score is computed using a weighted combination of multiple evaluation factors.

| Component | Weight | Reason |
|-----------|--------|--------|
| Semantic Similarity | 60% | Measures overall alignment between the resume and the job description. |
| Skills | 20% | Rewards candidates with more relevant technical skills. |
| Experience | 15% | Gives preference to experienced candidates. |
| Education | 5% | Considers educational qualifications while keeping practical skills more important. |

These weights were chosen to prioritize semantic relevance while still considering candidate qualifications.

# AI Reasoning

Google Gemini generates a short explanation for every candidate describing:

* Candidate strengths
* Missing skills (if any)
* Overall suitability for the job

This reasoning is included in the exported CSV and JSON files.


# Output

The project generates:

```
data/output/ranked_candidates.csv
```

and

```
data/output/ranked_candidates.json
```

Each candidate record contains:

* Rank
* Resume filename
* Similarity score
* Final score
* Skills
* Experience
* Education
* AI-generated reasoning

# Testing

The application was tested using multiple real resume examples.

### Test Summary

| Test                   | Description                   | Result |
| ---------------------- | ----------------------------- | ------ |
| Resume Parsing         | PDF, DOCX, TXT                | Passed |
| Gemini Extraction      | Skills, Education, Experience | Passed |
| Similarity Calculation | Resume vs Job Description     | Passed |
| Candidate Ranking      | Multiple resumes              | Passed |
| CSV Export             | Ranked candidates             | Passed |
| JSON Export            | Ranked candidates             | Passed |
| AI Reasoning           | Explanation generation        | Passed |
| Streamlit Interface    | Resume upload and ranking     | Passed |

The system was evaluated using 5–10 resumes with different skill sets and experience levels to verify ranking accuracy and export functionality.

# Design Choices

### Modular Architecture

Each responsibility is separated into an independent module:

* parser.py → Resume parsing
* extractor.py → AI information extraction
* similarity.py → Semantic similarity
* scorer.py → Candidate scoring
* ranker.py → Ranking
* reasoner.py → AI explanations
* exporter.py → CSV/JSON export

This design improves readability, maintainability, and testing.

### Semantic Matching

Instead of keyword matching, the project uses Sentence Transformer embeddings to compare resumes with the job description based on semantic meaning.

### AI-based Resume Extraction

Google Gemini extracts structured candidate information, reducing the need for manually written parsing rules.

### Weighted Scoring

Candidate ranking combines semantic similarity with extracted information such as skills, education, and experience to provide a more balanced evaluation.


# Tradeoffs and Limitations

* Resume extraction quality depends on the response generated by Gemini.
* Experience extraction is based on numeric values in the extracted text and may not capture complex career histories.
* Education scoring is rule-based and may not recognize all degree formats.
* Semantic similarity depends on the selected embedding model.
* API usage requires a valid Google Gemini API key and internet connectivity.
* OCR is not implemented for scanned PDF resumes.


# Future Improvements

* OCR support for scanned resumes
* Skill matching against predefined job requirements
* Customizable scoring weights
* Support for additional resume formats
* Database integration
* Candidate dashboard with analytics
* Email notifications
* Recruiter authentication
* Interview recommendation module


# Technologies Used

* Python
* Streamlit
* Google Gemini API
* Sentence Transformers
* spaCy
* scikit-learn
* pandas
* NumPy
* PyPDF2
* python-docx

# Author

Developed as an AI-powered Resume Screening Agent for automated candidate evaluation and ranking.
