"""
Async notification system for sending job match email alerts.
"""

import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, List

import aiosmtplib

from backend.core.config import get_settings
from backend.notifications.templates import render_job_match_email

logger = logging.getLogger("ai_job_notifier")
settings = get_settings()


async def send_email(
    to_email: str,
    subject: str,
    html_body: str,
) -> bool:
    """
    Send an email asynchronously using SMTP.

    Returns:
        True if email sent successfully, False otherwise.
    """
    if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
        logger.warning("SMTP credentials not configured. Skipping email to %s", to_email)
        return False

    message = MIMEMultipart("alternative")
    message["From"] = settings.NOTIFICATION_FROM_EMAIL or settings.SMTP_USERNAME
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(html_body, "html"))

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
        logger.info("Email sent to %s: %s", to_email, subject)
        return True
    except Exception as e:
        logger.error("Failed to send email to %s: %s", to_email, str(e))
        return False


async def notify_job_matches(
    user_email: str,
    user_name: str,
    matched_jobs: List[Dict[str, Any]],
    score_threshold: float = 0.7,
) -> bool:
    """
    Send a notification email for new job matches above the score threshold.

    Args:
        user_email: Recipient email.
        user_name: User's display name.
        matched_jobs: List of job match dicts with 'match_score' key.
        score_threshold: Minimum score to trigger notification.
    """
    # Filter jobs above threshold
    high_matches = [
        job for job in matched_jobs
        if job.get("match_score", 0) >= score_threshold
    ]

    if not high_matches:
        logger.debug("No jobs above threshold %.2f for %s", score_threshold, user_email)
        return False

    # Render email
    html = render_job_match_email(
        user_name=user_name,
        jobs=high_matches,
        dashboard_url=settings.FRONTEND_URL,
    )

    subject = f"🎯 {len(high_matches)} New Job Match{'es' if len(high_matches) > 1 else ''} for You!"
    return await send_email(user_email, subject, html)


async def send_batch_notifications(
    notifications: List[Dict[str, Any]],
) -> Dict[str, int]:
    """
    Send batch notifications to multiple users.

    Args:
        notifications: List of dicts with 'email', 'name', 'jobs' keys.

    Returns:
        Dict with 'sent' and 'failed' counts.
    """
    sent = 0
    failed = 0

    for notif in notifications:
        success = await notify_job_matches(
            user_email=notif["email"],
            user_name=notif["name"],
            matched_jobs=notif["jobs"],
            score_threshold=settings.MATCH_SCORE_THRESHOLD,
        )
        if success:
            sent += 1
        else:
            failed += 1

    logger.info("Batch notifications: %d sent, %d failed", sent, failed)
    return {"sent": sent, "failed": failed}
