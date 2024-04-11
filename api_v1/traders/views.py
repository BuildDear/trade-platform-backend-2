from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.traders import crud
from api_v1.traders.dependencies import trader_by_id
from api_v1.traders.schemas import (
    TraderSchem,
    TraderCreateSchem,
    TraderUpdateSchem,
    TraderUpdatePartialSchem,
)
from core import db_helper

router = APIRouter(prefix="/traders", tags=["Traders"])


# Endpoint to get all traders
@router.get("/", response_model=list[TraderSchem])
async def get_traders(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_traders(session=session)


# Endpoint to get trader by id
@router.get("/{trader_id}/", response_model=TraderSchem)
async def get_product(
    trader: TraderSchem = Depends(trader_by_id),
):
    return trader


# Endpoint to create a new trader
@router.post(
    "/",
    response_model=TraderSchem,
    status_code=status.HTTP_201_CREATED,
)
async def create_trader(
    trader_in: TraderCreateSchem,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_trader(session=session, trader_in=trader_in)


# Endpoint to put trader by id
@router.put("/{trader_id}/")
async def update_product(
    trader_update: TraderUpdateSchem,
    trader: TraderSchem = Depends(trader_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_trader(
        session=session,
        trader=trader,
        trader_update=trader_update,
    )


# Endpoint to patch trader by id
@router.patch("/{trader_id}/")
async def update_product(
    trader_update: TraderUpdatePartialSchem,
    trader: TraderSchem = Depends(trader_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_trader(
        session=session,
        trader=trader,
        trader_update=trader_update,
        partial=True,
    )


# Endpoint to delete trader by id
@router.delete("/{trader_id}/")
async def delete_product(
    trader: TraderSchem = Depends(trader_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_trader(session=session, trader=trader)
