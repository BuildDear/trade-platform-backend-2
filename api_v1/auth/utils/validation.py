import bcrypt
from fastapi import HTTPException, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.auth.utils.jwt import TOKEN_TYPE_FIELD
from api_v1.auth.utils.queries import query_user_by_email
from core import db_helper, TraderModel


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    """Validate Password against hashed version"""

    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


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


async def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    print(current_token_type)
    print(token_type)

    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )
