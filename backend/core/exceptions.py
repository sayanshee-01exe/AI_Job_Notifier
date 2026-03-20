"""
Custom exception classes and global exception handlers.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


# ── Custom Exceptions ─────────────────────────────────────
class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(AppException):
    """Resource not found."""

    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} not found", status_code=404)


class UnauthorizedException(AppException):
    """Authentication failed."""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, status_code=401)


class ForbiddenException(AppException):
    """Insufficient permissions."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status_code=403)


class ConflictException(AppException):
    """Resource conflict (e.g., duplicate)."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=409)


class ValidationException(AppException):
    """Custom validation error."""

    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=422)


# ── Exception Handlers ────────────────────────────────────
def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers on the FastAPI app."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred. Please try again later."},
        )
