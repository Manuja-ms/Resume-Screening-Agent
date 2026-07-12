import os
import tempfile
import pandas as pd
import streamlit as st

from modules.parser import parse_resume
from modules.extractor import extract_resume_information
from modules.similarity import calculate_similarity
from modules.scorer import calculate_final_score
from modules.ranker import rank_candidates
from modules.reasoner import generate_reasoning

st.set_page_config(
    page_title="Resume Screening Agent",
    page_icon="📄",
    layout="wide"
)

st.title("AI Resume Screening Agent")

st.write("Upload a Job Description and multiple resumes to rank candidates.")

# Job Description
job_description = st.text_area(
    "Job Description",
    height=220
)

# Resume Upload
uploaded_files = st.file_uploader(
    "Upload Resumes",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if st.button("Screen Resumes"):

    if not job_description:
        st.warning("Please enter a Job Description.")
        st.stop()

    if not uploaded_files:
        st.warning("Please upload resumes.")
        st.stop()

    candidates = []

    progress = st.progress(0)

    for index, uploaded_file in enumerate(uploaded_files):

        with tempfile.NamedTemporaryFile(delete=False,
            suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:

            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        resume_text = parse_resume(temp_path)

        extracted = extract_resume_information(resume_text)

        similarity = calculate_similarity(
            job_description,
            resume_text
        )

        score = calculate_final_score(
            extracted,
            similarity
        )

        reason = generate_reasoning(
            job_description,
            extracted,
            similarity
        )

        candidates.append({

            "Filename": uploaded_file.name,

            "Similarity (%)": similarity,

            "Final Score": score,

            "Skills": ", ".join(extracted.get("skills", [])),

            "Experience": extracted.get("experience", ""),

            "Education": extracted.get("education", ""),

            "Reason": reason

        })

        progress.progress((index + 1) / len(uploaded_files))

    ranked = rank_candidates(candidates)

    st.success("Screening Completed!")

    st.subheader("Ranked Candidates")

    df = pd.DataFrame(ranked)

    st.dataframe(
        df,
        use_container_width=True
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        csv,
        "ranked_candidates.csv",
        "text/csv"
    )

    st.subheader("Top Candidate")

    top = ranked[0]

    st.metric(
        "Best Match",
        top["Filename"],
        f"{top['Final Score']:.2f}"
    )

    st.write("### Reason")

    st.info(top["Reason"])