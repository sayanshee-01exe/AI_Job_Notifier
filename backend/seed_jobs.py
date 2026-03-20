import asyncio
from backend.core.database import async_session_factory
from backend.models.job import Job

async def seed_jobs():
    async with async_session_factory() as db:
        # Check if jobs already exist
        from sqlalchemy import select
        result = await db.execute(select(Job))
        existing_jobs = result.scalars().all()
        if existing_jobs:
            print(f"Database already has {len(existing_jobs)} jobs.")
            return

        dummy_jobs = [
            Job(
                title="Frontend Developer",
                company="TechCorp",
                location="Remote",
                description="Looking for a skilled frontend developer with React experience.",
                skills_required=["React", "JavaScript", "HTML", "CSS"],
                experience_level="Mid",
                salary_range="$100k - $130k",
                job_type="Full-time"
            ),
            Job(
                title="Machine Learning Engineer",
                company="AI Solutions",
                location="San Francisco, CA",
                description="Train and deploy NLP and CV models. Working with PyTorch and Transformers.",
                skills_required=["Python", "PyTorch", "Machine Learning", "NLP", "Transformers", "SQL"],
                experience_level="Mid",
                salary_range="$150k - $180k",
                job_type="Full-time"
            ),
            Job(
                title="Backend Software Engineer",
                company="DataSystems",
                location="New York, NY",
                description="Develop scalable backend APIs using Node.js and Python.",
                skills_required=["Python", "Node.js", "Express.js", "MongoDB", "Redis", "SQL"],
                experience_level="Senior",
                salary_range="$140k - $170k",
                job_type="Full-time"
            ),
            Job(
                title="Full Stack Developer",
                company="Startup Inc",
                location="Remote",
                description="We are seeking a versatile developer who knows React, Node.js, and MongoDB.",
                skills_required=["React", "Node.js", "MongoDB", "JavaScript", "CSS"],
                experience_level="Junior",
                salary_range="$90k - $110k",
                job_type="Full-time"
            ),
            Job(
                title="Data Scientist",
                company="Big Data Co",
                location="Seattle, WA",
                description="Analyze large datasets to extract insights. Requires ML and Python.",
                skills_required=["Python", "Machine Learning", "scikit-learn", "SQL", "NLTK"],
                experience_level="Mid",
                salary_range="$120k - $150k",
                job_type="Full-time"
            )
        ]
        
        db.add_all(dummy_jobs)
        await db.commit()
        print(f"Successfully seeded {len(dummy_jobs)} jobs!")

if __name__ == "__main__":
    asyncio.run(seed_jobs())
