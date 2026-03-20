"""
Scraper configuration: target URLs, CSS selectors, and retry settings.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ScraperTarget:
    """Configuration for a single scraping target."""
    name: str
    url: str
    selectors: Dict[str, str]
    pagination_selector: str = ""
    max_pages: int = 5


@dataclass
class ScraperConfig:
    """Global scraper configuration."""
    targets: List[ScraperTarget] = field(default_factory=list)
    max_retries: int = 3
    retry_delay: float = 2.0
    request_timeout: int = 30
    user_agent: str = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    rate_limit_seconds: float = 1.0


# ── Default Configuration ────────────────────────────────
# Mock targets for demonstration. Replace with real URLs.
DEFAULT_CONFIG = ScraperConfig(
    targets=[
        ScraperTarget(
            name="MockJobs",
            url="https://realpython.github.io/fake-jobs/",
            selectors={
                "job_card": "div.card-content",
                "title": "h2.title",
                "company": "h3.company",
                "location": "p.location",
                "description": "div.card-content",
                "link": "a[href]",
            },
            max_pages=1,
        ),
    ],
    max_retries=3,
    retry_delay=2.0,
)
