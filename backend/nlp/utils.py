"""
NLP utilities: text cleaning, normalization, and keyword lists.
"""

import re


def clean_text(text: str) -> str:
    """Clean and normalize extracted text."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,;:!?@#\-+/()&\'\"•●○■□▪▫–—]', '', text)
    # Normalize bullet points
    text = re.sub(r'[•●○■□▪▫]', '-', text)
    # Restore line breaks around section headers
    text = re.sub(r'\s*((?:EDUCATION|EXPERIENCE|SKILLS|PROJECTS|WORK|PROFESSIONAL|SUMMARY|OBJECTIVE|CERTIFICATIONS|AWARDS)\b)', r'\n\n\1', text, flags=re.IGNORECASE)
    return text.strip()


# ── Skill Keywords ────────────────────────────────────────
SKILL_KEYWORDS = [
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust",
    "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB", "Perl",
    "Dart", "Lua", "Shell", "Bash", "PowerShell", "SQL", "HTML", "CSS",

    # Frameworks & Libraries
    "React", "Angular", "Vue.js", "Next.js", "Node.js", "Express.js",
    "Django", "Flask", "FastAPI", "Spring Boot", "Rails", "Laravel",
    "ASP.NET", "Svelte", "Nuxt.js", "Gatsby", "Tailwind CSS", "Bootstrap",
    "jQuery", "Redux", "GraphQL",

    # Data Science & ML
    "TensorFlow", "PyTorch", "Keras", "scikit-learn", "Pandas", "NumPy",
    "spaCy", "NLTK", "OpenCV", "Hugging Face", "LangChain",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "Data Science", "Data Analysis", "Statistics",

    # Cloud & DevOps
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform",
    "CI/CD", "Jenkins", "GitHub Actions", "GitLab CI",
    "Ansible", "Linux", "Nginx", "Apache",

    # Databases
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
    "DynamoDB", "Cassandra", "SQLite", "Oracle", "SQL Server",
    "Neo4j", "Firebase",

    # Tools & Practices
    "Git", "GitHub", "Jira", "Agile", "Scrum",
    "REST API", "Microservices", "System Design",
    "Unit Testing", "Integration Testing", "TDD",
    "Figma", "Sketch", "Adobe XD",

    # AI / LLM
    "LLM", "GPT", "ChatGPT", "OpenAI", "Prompt Engineering",
    "RAG", "Vector Databases", "FAISS", "Embeddings",
    "Transformers", "BERT", "Generative AI",
]

# ── Education Keywords ────────────────────────────────────
EDUCATION_KEYWORDS = [
    "Bachelor", "Master", "PhD", "Doctorate", "Associate",
    "B.S.", "B.A.", "M.S.", "M.A.", "M.B.A.", "B.Tech", "M.Tech",
    "B.E.", "M.E.", "B.Sc.", "M.Sc.", "B.Com.", "M.Com.",
    "University", "College", "Institute", "School",
    "Computer Science", "Engineering", "Information Technology",
    "Data Science", "Mathematics", "Business Administration",
    "Diploma", "Certification", "Degree",
]

# ── Degree Patterns ───────────────────────────────────────
DEGREE_PATTERNS = [
    r'((?:Bachelor|Master|PhD|Doctorate|Associate)(?:\'?s)?\s+(?:of\s+)?(?:Science|Arts|Engineering|Technology|Business Administration|Computer Science|Information Technology)\s*(?:in\s+[\w\s]+)?)',
    r'((?:B\.?S\.?|B\.?A\.?|M\.?S\.?|M\.?A\.?|M\.?B\.?A\.?|B\.?Tech|M\.?Tech|B\.?E\.?|M\.?E\.?|Ph\.?D\.?)\s*(?:in\s+)?[\w\s]{3,40})',
    r'((?:B\.?Sc\.?|M\.?Sc\.?|B\.?Com\.?|M\.?Com\.?)\s*(?:in\s+)?[\w\s]{3,40})',
]
