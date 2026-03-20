"""
Prompt templates for the RAG pipeline.
"""

JOB_FIT_PROMPT = """You are a job recommendation engine.

User Profile:
- Role: {role}
- Skills: {skills}
- Experience: {experience}
- Education: {education}
- Preferred Location: {preferred_location}

Jobs:
{job_context}

Tasks:
1. Rank top 5 jobs for this user
2. Explain match score
3. Suggest skill gaps
4. Be concise and actionable

User Question:
{question}
"""

RESUME_IMPROVEMENT_PROMPT = """You are an expert resume coach. Based on the user's current profile and the types of jobs they might be interested in, provide resume improvement suggestions.

## Current Profile
- **Skills**: {skills}
- **Experience**: {experience}
- **Education**: {education}

## Relevant Job Market Trends
{job_context}

## User Question
{question}

Provide specific, actionable suggestions to improve their resume and increase their chances of landing interviews.
"""

GENERAL_CAREER_PROMPT = """You are a job recommendation engine.

User Profile:
- Role: {role}
- Skills: {skills}
- Experience: {experience}
- Education: {education}
- Preferred Location: {preferred_location}

Jobs Context:
{job_context}

Tasks:
1. Answer the user's question directly
2. Suggest skill gaps to improve
3. Be concise and actionable

User Question:
{question}
"""


def select_prompt(question: str) -> str:
    """Select the most appropriate prompt template based on the question."""
    question_lower = question.lower()

    if any(kw in question_lower for kw in ["fit", "match", "good for", "suitable", "qualify"]):
        return JOB_FIT_PROMPT
    elif any(kw in question_lower for kw in ["resume", "cv", "improve", "better", "enhance"]):
        return RESUME_IMPROVEMENT_PROMPT
    else:
        return GENERAL_CAREER_PROMPT
