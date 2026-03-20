"""
Request/response logging middleware.
"""

import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("ai_job_notifier")


class LoggingMiddleware(BaseHTTPMiddleware):
    """Logs every request with method, path, status code, and duration."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = str(uuid.uuid4())[:8]
        start_time = time.perf_counter()

        # Log incoming request
        logger.info(
            "[%s] ➜  %s %s",
            request_id,
            request.method,
            request.url.path,
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            duration = (time.perf_counter() - start_time) * 1000
            logger.error(
                "[%s] ✖  %s %s — ERROR in %.1fms: %s",
                request_id,
                request.method,
                request.url.path,
                duration,
                str(exc),
            )
            raise

        duration = (time.perf_counter() - start_time) * 1000
        logger.info(
            "[%s] ✔  %s %s — %s in %.1fms",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        response.headers["X-Request-ID"] = request_id
        return response
