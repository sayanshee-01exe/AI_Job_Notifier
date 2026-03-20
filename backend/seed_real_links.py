import asyncio
import random
from backend.core.database import async_session_factory
from backend.models.job import Job

# ── Realistic Job Data with Real Platform Links ─────────────────────────────
# We generate realistic job listings that link directly to active search pages
# on major platforms (LinkedIn, Indeed, Naukri, Glassdoor, etc.)

PLATFORMS = [
    {
        "name": "LinkedIn",
        "url_template": "https://www.linkedin.com/jobs/search/?keywords={title}&location={location}"
    },
    {
        "name": "Indeed",
        "url_template": "https://www.indeed.com/jobs?q={title}&l={location}"
    },
    {
        "name": "Naukri",
        "url_template": "https://www.naukri.com/{title}-jobs-in-{location}"
    },
    {
        "name": "Glassdoor",
        "url_template": "https://www.glassdoor.com/Job/jobs.htm?sc.keyword={title}&locT=C&locName={location}"
    }
]

JOB_TEMPLATES = [
    {
        "title": "Frontend React Developer",
        "company": "TechVision AI",
        "location": "Remote",
        "description": "We are looking for an experienced Frontend Developer passionate about building sleek, modern UIs for our AI SAAS platform. Strong React and Tailwind CSS required.",
        "skills": ["React", "Next.js", "TypeScript", "Tailwind CSS", "JavaScript", "HTML", "CSS"],
        "experience": "Mid",
        "salary": "$110k - $140k"
    },
    {
        "title": "Senior Machine Learning Engineer",
        "company": "Quantum Innovations",
        "location": "San Francisco",
        "description": "Join our core AI research team. You will be training and fine-tuning Large Language Models (LLMs) and deploying scalable inference endpoints.",
        "skills": ["Python", "PyTorch", "Machine Learning", "NLP", "Transformers", "AWS", "CUDA"],
        "experience": "Senior",
        "salary": "$170k - $220k"
    },
    {
        "title": "Backend Python Developer",
        "company": "DataFlow Networks",
        "location": "New York",
        "description": "Build high-throughput APIs using FastAPI and PostgreSQL. You will be responsible for orchestrating background scraping tasks and database architecture.",
        "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis", "SQL", "Git"],
        "experience": "Mid",
        "salary": "$130k - $160k"
    },
    {
        "title": "Full Stack Software Engineer",
        "company": "StartupX",
        "location": "Remote",
        "description": "We need a versatile full-stack engineer who can handle everything from database schema design to frontend components using the MERN stack.",
        "skills": ["React", "Node.js", "Express.js", "MongoDB", "JavaScript", "Git", "REST APIs"],
        "experience": "Junior",
        "salary": "$80k - $100k"
    },
    {
        "title": "Data Scientist (NLP)",
        "company": "Insight Analytics",
        "location": "London",
        "description": "Extract actionable insights from millions of customer feedback documents. Experience with HuggingFace, SpaCy, and Scikit-learn is essential.",
        "skills": ["Python", "Machine Learning", "scikit-learn", "NLTK", "SpaCy", "SQL", "Pandas"],
        "experience": "Mid",
        "salary": "$120k - $150k"
    },
    {
        "title": "DevOps Engineer",
        "company": "CloudScale Solutions",
        "location": "Austin",
        "description": "Manage our Kubernetes clusters across AWS and GCP. Automate CI/CD pipelines using GitHub Actions.",
        "skills": ["AWS", "Kubernetes", "Docker", "CI/CD", "Linux", "Terraform", "Python"],
        "experience": "Mid",
        "salary": "$140k - $160k"
    },
    {
        "title": "Mobile App Developer (React Native)",
        "company": "Fintech Mobile",
        "location": "Toronto",
        "description": "Build highly responsive cross-platform mobile applications for our new digital wallet product.",
        "skills": ["React Native", "JavaScript", "TypeScript", "Mobile Development", "Redux", "API Integration"],
        "experience": "Junior",
        "salary": "$90k - $115k"
    },
    {
        "title": "Database Administrator",
        "company": "SecureTrust Bank",
        "location": "Chicago",
        "description": "Ensure the performance, security, and availability of our databases. Strong SQL and performance tuning skills required.",
        "skills": ["SQL", "PostgreSQL", "MySQL", "Database Administration", "Performance Tuning"],
        "experience": "Senior",
        "salary": "$130k - $155k"
    },
    {
        "title": "UI/UX Designer",
        "company": "Creative Agency",
        "location": "Remote",
        "description": "Design user-centric interfaces for web and mobile. Must have a strong portfolio demonstrating clean aesthetics.",
        "skills": ["Figma", "UI/UX", "Adobe Creative Suite", "Prototyping", "Wireframing"],
        "experience": "Mid",
        "salary": "$100k - $125k"
    },
]

async def seed_real_links():
    async with async_session_factory() as db:
        # Check if jobs already exist and clear them to insert the new rich dataset
        from sqlalchemy import select, delete
        await db.execute(delete(Job))
        
        jobs_to_insert = []
        
        # We'll generate 3 variants for each job template across different platforms
        # to simulate a populated job board.
        for template in JOB_TEMPLATES:
            for _ in range(3):
                platform = random.choice(PLATFORMS)
                
                # Format URL for the platform
                formatted_title = template["title"].replace(" ", "%20")
                formatted_location = template["location"].replace(" ", "%20")
                if platform["name"] == "Naukri":
                    formatted_title = template["title"].replace(" ", "-").lower()
                    formatted_location = template["location"].replace(" ", "-").lower()

                source_url = platform["url_template"].format(
                    title=formatted_title, 
                    location=formatted_location
                )
                
                jobs_to_insert.append(
                    Job(
                        title=template["title"],
                        company=f"{template['company']} (via {platform['name']})",
                        location=template["location"],
                        description=template["description"],
                        skills_required=template["skills"],
                        experience_level=template["experience"],
                        salary_range=template["salary"],
                        job_type="Full-time",
                        source_url=source_url
                    )
                )
        
        db.add_all(jobs_to_insert)
        await db.commit()
        print(f"Successfully seeded {len(jobs_to_insert)} hyper-realistic platform jobs!")

if __name__ == "__main__":
    asyncio.run(seed_real_links())
