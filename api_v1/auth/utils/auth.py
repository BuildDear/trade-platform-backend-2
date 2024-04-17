import bcrypt
from fastapi import Form, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.auth.utils import jwt
from api_v1.traders.schemas import TraderCreateSchema, TraderSchema
from core import TraderModel, db_helper


http_bearer = HTTPBearer()


def hash_password(
    password: str,
) -> bytes:
    """Hash Password using bcrypt"""

    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    """Validate Password against hashed version"""

    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


async def registration(
    session: AsyncSession, trader_in: TraderCreateSchema
) -> TraderModel:
    """
    Creates a new trader in the database asynchronously.
    """

    try:
        password = trader_in.password
        trader_data = trader_in.dict(exclude={"password"})

        trader = TraderModel(**trader_data, password=hash_password(password))

        session.add(trader)
        await session.commit()
        await session.refresh(trader)
        return trader

    except Exception as e:
        await session.rollback()
        raise e


async def query_user_by_email(email: str, db: AsyncSession) -> TraderModel:
    """Query user by email"""

    result = await db.execute(select(TraderModel).where(TraderModel.email == email))
    return result.scalars().first()


async def validate_auth_user(
    email: str = Form(),
    password: str = Form(),
    db: AsyncSession = Depends(db_helper.get_scoped_session),
) -> TraderModel:
    """Validate authentication for user"""

    user = await query_user_by_email(email, db)

    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )

    if not user:
        raise unauthed_exc

    if not validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User inactive",
        )

    return user


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    # token: str = Depends(oauth2_scheme),
) -> dict:
    """Decrypt user content"""

    token = credentials.credentials
    try:
        payload = jwt.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
            # detail=f"invalid token error",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: AsyncSession = Depends(db_helper.get_scoped_session),
) -> TraderModel:
    """Get auth user"""

    email: str | None = payload.get("sub")

    user = await query_user_by_email(email, db)

    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_current_active_auth_user(
    user: TraderSchema = Depends(get_current_auth_user),
):
    """Get auth and active user"""
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )
