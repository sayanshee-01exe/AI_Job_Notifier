"""
SQLAlchemy Job model.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY

from backend.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    skills_required = Column(ARRAY(String), default=list)
    experience_level = Column(String(50), nullable=True)  # e.g., "Junior", "Mid", "Senior"
    salary_range = Column(String(100), nullable=True)
    job_type = Column(String(50), default="Full-time")  # Full-time, Part-time, Contract
    source_url = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    )

    def __repr__(self) -> str:
        return f"<Job id={self.id} title={self.title} company={self.company}>"
