from typing import Annotated

from fastapi import Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from . import crud
from core import db_helper, TraderModel


async def trader_by_id(
    trader_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> TraderModel:
    trader = await crud.get_trader(session=session, trader_id=trader_id)

    if trader is not None:
        return trader

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {trader_id} not found!",
    )
