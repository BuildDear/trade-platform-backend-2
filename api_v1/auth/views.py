from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.auth import jwt_utils
from api_v1.auth.jwt_utils import validate_auth_user
from api_v1.auth.schemas import TokenInfo
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
    return await jwt_utils.registration(session=session, trader_in=trader_in)


# Endpoint to login new trader
@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: TraderSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.email,
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
    }
    token = jwt_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
