"""
Job scraper using BeautifulSoup with retry mechanism, logging, and config-driven URLs.
"""

import logging
import time
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup

from backend.scraper.config import DEFAULT_CONFIG, ScraperConfig, ScraperTarget

logger = logging.getLogger("ai_job_notifier")


class JobScraper:
    """
    Configurable job scraper with:
    - BeautifulSoup HTML parsing
    - Retry mechanism with exponential backoff
    - Config-driven target URLs & selectors
    - Structured JSON output
    """

    def __init__(self, config: Optional[ScraperConfig] = None):
        self.config = config or DEFAULT_CONFIG
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.config.user_agent})

    def scrape_all(self) -> List[Dict[str, Any]]:
        """Scrape all configured targets and return combined results."""
        all_jobs = []
        for target in self.config.targets:
            logger.info("Scraping target: %s (%s)", target.name, target.url)
            try:
                jobs = self._scrape_target(target)
                all_jobs.extend(jobs)
                logger.info("Scraped %d jobs from %s", len(jobs), target.name)
            except Exception as e:
                logger.error("Failed to scrape %s: %s", target.name, str(e))
        return all_jobs

    def _scrape_target(self, target: ScraperTarget) -> List[Dict[str, Any]]:
        """Scrape a single target with pagination."""
        jobs = []
        url = target.url

        for page in range(target.max_pages):
            html = self._fetch_with_retry(url)
            if not html:
                break

            soup = BeautifulSoup(html, "lxml")
            page_jobs = self._extract_jobs(soup, target)
            jobs.extend(page_jobs)

            if not page_jobs:
                break

            # Check for next page
            if target.pagination_selector:
                next_link = soup.select_one(target.pagination_selector)
                if next_link and next_link.get("href"):
                    url = next_link["href"]
                    time.sleep(self.config.rate_limit_seconds)
                else:
                    break
            else:
                break

        return jobs

    def _fetch_with_retry(self, url: str) -> Optional[str]:
        """Fetch a URL with retry mechanism."""
        for attempt in range(1, self.config.max_retries + 1):
            try:
                response = self.session.get(url, timeout=self.config.request_timeout)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.warning(
                    "Fetch attempt %d/%d failed for %s: %s",
                    attempt, self.config.max_retries, url, str(e),
                )
                if attempt < self.config.max_retries:
                    delay = self.config.retry_delay * (2 ** (attempt - 1))
                    time.sleep(delay)

        logger.error("All retry attempts exhausted for %s", url)
        return None

    def _extract_jobs(
        self, soup: BeautifulSoup, target: ScraperTarget
    ) -> List[Dict[str, Any]]:
        """Extract job listings from parsed HTML."""
        selectors = target.selectors
        job_cards = soup.select(selectors.get("job_card", ""))

        if not job_cards:
            logger.warning("No job cards found with selector: %s", selectors.get("job_card"))
            return []

        jobs = []
        for card in job_cards:
            job = {
                "title": self._extract_text(card, selectors.get("title", "")),
                "company": self._extract_text(card, selectors.get("company", "")),
                "location": self._extract_text(card, selectors.get("location", "")),
                "description": self._extract_text(card, selectors.get("description", "")),
                "source": target.name,
                "source_url": target.url,
            }

            # Extract link if available
            link_selector = selectors.get("link", "")
            if link_selector:
                link_elem = card.select_one(link_selector)
                if link_elem and link_elem.get("href"):
                    job["source_url"] = link_elem["href"]

            # Only add if we have at least a title
            if job["title"]:
                jobs.append(job)

        return jobs

    @staticmethod
    def _extract_text(element: BeautifulSoup, selector: str) -> str:
        """Safely extract text from a CSS selector."""
        if not selector:
            return ""
        found = element.select_one(selector)
        return found.get_text(strip=True) if found else ""

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()


def run_scraper(config: Optional[ScraperConfig] = None) -> List[Dict[str, Any]]:
    """Convenience function to run the scraper and return results."""
    scraper = JobScraper(config)
    try:
        return scraper.scrape_all()
    finally:
        scraper.close()
