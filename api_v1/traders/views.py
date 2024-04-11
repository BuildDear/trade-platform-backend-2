from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.traders import crud
from api_v1.traders.schemas import Trader, TraderCreate
from core import db_helper

router = APIRouter(prefix="/traders", tags=["Traders"])


# Endpoint to get all traders
@router.get("/", response_model=list[Trader])
async def get_traders(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_traders(session=session)


# Endpoint to create a new trader
@router.post(
    "/",
    response_model=Trader,
    status_code=status.HTTP_201_CREATED,
)
async def create_trader(
    trader_in: TraderCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_trader(session=session, trader_in=trader_in)


#
# @router.get("/{trader_id}/", response_model=Trader)
# async def get_product(
#     trader: Trader = Depends(trader_by_id),
# ):
#     return trader
