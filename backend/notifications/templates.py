"""
Email notification HTML templates.
"""

JOB_MATCH_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f9; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 20px auto; background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
        .header {{ background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #fff; padding: 32px 24px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; font-weight: 700; }}
        .header p {{ margin: 8px 0 0; opacity: 0.9; font-size: 14px; }}
        .content {{ padding: 24px; }}
        .job-card {{ background: #f8f9fb; border-radius: 8px; padding: 16px; margin-bottom: 16px; border-left: 4px solid #6366f1; }}
        .job-card h3 {{ margin: 0 0 8px; color: #1e293b; font-size: 16px; }}
        .job-card .company {{ color: #6366f1; font-weight: 600; font-size: 14px; }}
        .job-card .location {{ color: #64748b; font-size: 13px; margin: 4px 0; }}
        .match-score {{ display: inline-block; background: linear-gradient(135deg, #10b981, #059669); color: #fff; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; }}
        .skills {{ margin-top: 8px; }}
        .skill-tag {{ display: inline-block; background: #e0e7ff; color: #4338ca; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin: 2px 4px 2px 0; }}
        .cta {{ text-align: center; padding: 24px; }}
        .cta a {{ display: inline-block; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #fff; text-decoration: none; padding: 12px 32px; border-radius: 8px; font-weight: 600; font-size: 15px; }}
        .footer {{ text-align: center; padding: 16px 24px; color: #94a3b8; font-size: 12px; border-top: 1px solid #e2e8f0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 New Job Matches Found!</h1>
            <p>We found {match_count} new job(s) matching your profile</p>
        </div>
        <div class="content">
            <p>Hi {user_name},</p>
            <p>Great news! Here are your latest job matches:</p>
            {job_cards}
        </div>
        <div class="cta">
            <a href="{dashboard_url}">View All Recommendations →</a>
        </div>
        <div class="footer">
            <p>AI Job Notifier — You're receiving this because you opted in to job match alerts.</p>
        </div>
    </div>
</body>
</html>
"""

JOB_CARD_TEMPLATE = """
<div class="job-card">
    <h3>{title}</h3>
    <div class="company">{company}</div>
    <div class="location">📍 {location}</div>
    <span class="match-score">✨ {score}% match</span>
    <div class="skills">
        {skill_tags}
    </div>
</div>
"""


def render_job_match_email(
    user_name: str,
    jobs: list,
    dashboard_url: str = "http://localhost:3000",
) -> str:
    """Render the job match notification email HTML."""
    job_cards_html = ""
    for job in jobs:
        skill_tags = "".join(
            f'<span class="skill-tag">{skill}</span>'
            for skill in job.get("skills_required", [])[:6]
        )
        job_cards_html += JOB_CARD_TEMPLATE.format(
            title=job.get("title", ""),
            company=job.get("company", ""),
            location=job.get("location", ""),
            score=int(job.get("match_score", 0) * 100),
            skill_tags=skill_tags,
        )

    return JOB_MATCH_TEMPLATE.format(
        user_name=user_name,
        match_count=len(jobs),
        job_cards=job_cards_html,
        dashboard_url=dashboard_url,
    )
