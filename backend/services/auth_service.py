"""
Authentication service: user registration and login logic.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exceptions import ConflictException, UnauthorizedException
from backend.core.security import hash_password, verify_password, create_access_token
from backend.models.user import User
from backend.schemas.user import UserCreate, UserLogin, Token, UserResponse


async def register_user(db: AsyncSession, user_data: UserCreate) -> UserResponse:
    """Register a new user. Raises ConflictException if email exists."""
    # Check for existing user
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise ConflictException("User with this email already exists")

    # Create new user
    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    return UserResponse.model_validate(user)


async def authenticate_user(db: AsyncSession, login_data: UserLogin) -> Token:
    """Authenticate user and return JWT token. Raises UnauthorizedException on failure."""
    result = await db.execute(select(User).where(User.email == login_data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise UnauthorizedException("Invalid email or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)
