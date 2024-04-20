from datetime import timedelta, datetime

import bcrypt
import jwt
from fastapi import Form, HTTPException, Depends
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.traders.schemas import TraderCreateSchema, TraderSchema
from core import TraderModel, db_helper
from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    """Encode JWT with payload"""

    to_encode = payload.copy()
    now = datetime.utcnow()

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    """Decode JWT token"""

    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def create_access_token(user: TraderSchema):
    jwt_payload = {
        "sub": user.email,
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
    }
    return encode_jwt(jwt_payload)


def create_refresh_token(user: TraderSchema):
    jwt_payload = {
        "sub": user.email,
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
    }
    return encode_jwt(jwt_payload)
