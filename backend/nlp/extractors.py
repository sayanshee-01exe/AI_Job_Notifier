"""
NLP extractors for skills, experience, and education from resume text.
Uses pattern matching and keyword-based extraction.
"""

import re
from typing import List

from backend.nlp.utils import SKILL_KEYWORDS, EDUCATION_KEYWORDS, DEGREE_PATTERNS


def extract_skills(text: str) -> List[str]:
    """
    Extract skills from resume text using keyword matching.
    Matches against a comprehensive list of tech/professional skills.
    """
    text_lower = text.lower()
    found_skills = []

    for skill in SKILL_KEYWORDS:
        # Use word boundary matching to avoid partial matches
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    # Deduplicate while preserving order
    seen = set()
    unique_skills = []
    for s in found_skills:
        s_lower = s.lower()
        if s_lower not in seen:
            seen.add(s_lower)
            unique_skills.append(s)

    return unique_skills


def extract_experience(text: str) -> str:
    """
    Extract experience section from resume text.
    Looks for common section headers and captures content until the next section.
    """
    # Common experience section headers
    headers = [
        r"(?:work\s+)?experience",
        r"professional\s+experience",
        r"employment\s+history",
        r"work\s+history",
        r"career\s+history",
    ]

    # Try to find experience section
    for header in headers:
        pattern = rf"(?i)(?:^|\n)\s*(?:#+\s*)?{header}\s*:?\s*\n([\s\S]*?)(?=\n\s*(?:#+\s*)?(?:education|skills|projects|certifications|awards|references|interests|summary|objective)\b|\Z)"
        match = re.search(pattern, text)
        if match:
            experience_text = match.group(1).strip()
            if experience_text:
                # Clean up and limit length
                lines = [line.strip() for line in experience_text.split('\n') if line.strip()]
                return '\n'.join(lines[:30])  # Cap at 30 lines

    # Fallback: extract years of experience mentions
    year_patterns = [
        r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
        r'experience\s*:?\s*(\d+)\+?\s*years?',
    ]
    for pattern in year_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return f"{match.group(1)} years of experience"

    return ""


def extract_education(text: str) -> List[str]:
    """
    Extract education entries from resume text.
    Looks for degree names, institutions, and graduation years.
    """
    education_entries = []

    # Look for degree patterns
    for pattern in DEGREE_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                entry = " ".join(m.strip() for m in match if m.strip())
            else:
                entry = match.strip()
            if entry and len(entry) > 3:
                education_entries.append(entry)

    # Look for education section
    edu_section_pattern = r'(?i)(?:^|\n)\s*(?:#+\s*)?education\s*:?\s*\n([\s\S]*?)(?=\n\s*(?:#+\s*)?(?:experience|skills|projects|certifications|awards|references|interests|work)\b|\Z)'
    match = re.search(edu_section_pattern, text)
    if match:
        section_text = match.group(1)
        lines = [line.strip() for line in section_text.split('\n') if line.strip()]
        for line in lines[:10]:
            # Check if line contains education keywords
            if any(kw.lower() in line.lower() for kw in EDUCATION_KEYWORDS):
                if line not in education_entries:
                    education_entries.append(line)

    # Deduplicate
    seen = set()
    unique = []
    for entry in education_entries:
        entry_lower = entry.lower()
        if entry_lower not in seen:
            seen.add(entry_lower)
            unique.append(entry)

    return unique
