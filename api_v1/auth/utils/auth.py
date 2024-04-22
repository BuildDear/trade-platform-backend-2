from typing import Annotated

import bcrypt
from fastapi import Depends, HTTPException, Query
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jwt import InvalidTokenError
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.auth.utils import jwt
from api_v1.auth.utils.jwt import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from api_v1.auth.utils.validation import validate_token_type
from api_v1.traders.schemas import TraderCreateSchema, TraderSchema
from core import TraderModel, db_helper


http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login/",
)


def hash_password(
    password: str,
) -> bytes:
    """Hash Password using bcrypt"""

    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


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


def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> dict:
    """Decrypt user content"""

    # token = credentials.credentials
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


async def query_user_by_email(email: str, session: AsyncSession) -> TraderModel:
    """Query user by email"""

    result = await session.execute(
        select(TraderModel).where(TraderModel.email == email)
    )
    return result.scalars().first()


async def get_user_by_token_sub(
    payload: dict,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> TraderModel:
    """Get auth user"""
    email = payload.get("sub", "Email not found")
    print(email, "email")

    # result = await session.execute(
    #     select(TraderModel).where(TraderModel.email == email)
    # )
    # user = result.scalars().first()

    stat = select(TraderModel).order_by(TraderModel.id)
    result = await session.execute(stat)
    user = result.scalars().all()

    print(user, "userrrrrrr")

    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    ):
        await validate_token_type(payload, self.token_type)

        email = payload.get("sub", "Email not found")
        result = await session.execute(
            select(TraderModel).where(TraderModel.email == email)
        )
        user = result.scalars().first()

        print(user, "userrrrrrr")

        if user:
            return user

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid (user not found)",
        )

        # return await get_user_by_token_sub(payload=payload)


get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


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
