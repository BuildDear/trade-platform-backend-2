from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.auth.schemas import TokenInfo
from api_v1.auth.utils import jwt, auth
from api_v1.auth.utils.auth import (
    get_current_token_payload,
    get_current_active_auth_user,
    get_current_auth_user_for_refresh,
)
from api_v1.auth.utils.jwt import create_access_token, create_refresh_token
from api_v1.auth.utils.validation import validate_auth_user
from api_v1.traders.schemas import TraderSchema, TraderCreateSchema
from core import db_helper

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(http_bearer)],
)


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
    refresh_token = create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
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


# Endpoint to update access toekn by refresh token
@router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
async def auth_refresh_jwt(
    # todo: validate user is active!!
    user: TraderSchema = Depends(get_current_auth_user_for_refresh),
    # user: UserSchema = Depends(get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)),
    # user: UserSchema = Depends(UserGetterFromToken(REFRESH_TOKEN_TYPE)),
):
    print(user, "userrr")
    access_token = create_access_token(user)

    return TokenInfo(
        access_token=access_token,
    )
