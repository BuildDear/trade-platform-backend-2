from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.auth.schemas import TokenInfo
from api_v1.auth.utils import jwt, auth
from api_v1.auth.utils.auth import (
    validate_auth_user,
    get_current_token_payload,
    get_current_active_auth_user,
)
from api_v1.auth.utils.jwt import create_access_token
from api_v1.traders.schemas import TraderSchema, TraderCreateSchema
from core import db_helper

router = APIRouter(prefix="/auth", tags=["Auth"])


# Endpoint to register new trader
@router.post(
    "/registration/",
    response_model=TraderSchema,
    status_code=status.HTTP_201_CREATED,
)
async def user_registration(
    trader_in: TraderCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await auth.registration(session=session, trader_in=trader_in)


# Endpoint to login new trader
@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: TraderSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user)

    return TokenInfo(
        access_token=access_token,
    )


# Endpoint to get current user
@router.get("/users/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: TraderSchema = Depends(get_current_active_auth_user),
):

    return {
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
    }
