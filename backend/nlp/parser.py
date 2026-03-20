"""
Resume parser: extracts text from PDF/DOCX and delegates to extractors.
"""

import logging
from pathlib import Path

from backend.nlp.extractors import extract_skills, extract_experience, extract_education, extract_role, extract_preferred_location
from backend.nlp.utils import clean_text
from backend.schemas.resume import ResumeData

logger = logging.getLogger("ai_job_notifier")


def extract_text_from_pdf(file_path: str) -> str:
    """Extract raw text from a PDF file."""
    import pdfplumber

    text_parts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_text_from_docx(file_path: str) -> str:
    """Extract raw text from a DOCX file."""
    from docx import Document

    doc = Document(file_path)
    return "\n".join(para.text for para in doc.paragraphs if para.text.strip())


def parse_resume(file_path: str) -> ResumeData:
    """
    Parse a resume file (PDF or DOCX) and extract structured data.

    Returns:
        ResumeData with skills, experience, education, and raw_text.
    """
    path = Path(file_path)
    ext = path.suffix.lower()

    logger.info("Parsing resume: %s", path.name)

    # Extract raw text
    if ext == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        raw_text = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    if not raw_text.strip():
        logger.warning("No text extracted from %s", path.name)
        return ResumeData(raw_text="")

    # Clean text
    cleaned = clean_text(raw_text)

    # Extract structured data
    role = extract_role(cleaned)
    skills = extract_skills(cleaned)
    experience = extract_experience(cleaned)
    education = extract_education(cleaned)
    preferred_location = extract_preferred_location(cleaned)

    logger.info(
        "Parsed resume: %d skills, %d education entries",
        len(skills),
        len(education),
    )

    return ResumeData(
        role=role,
        skills=skills,
        experience=experience,
        education=education,
        preferred_location=preferred_location,
        raw_text=cleaned,
    )
