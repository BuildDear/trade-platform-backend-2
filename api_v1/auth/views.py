from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.auth import jwt_utils
from api_v1.traders.schemas import TraderSchema, TraderCreateSchema
from core import db_helper

router = APIRouter(prefix="/auth", tags=["Auth"])


# Endpoint to create a new trader
@router.post(
    "/",
    response_model=TraderSchema,
    status_code=status.HTTP_201_CREATED,
)
async def user_registration(
    trader_in: TraderCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await jwt_utils.registration(session=session, trader_in=trader_in)
