from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.traders.schemas import (
    TraderCreateSchem,
    TraderSchem,
    TraderUpdateSchem,
    TraderUpdatePartialSchem,
)
from core import TraderModel


async def get_traders(session: AsyncSession) -> list[TraderModel]:
    """
    Retrieves all traders from the database asynchronously.
    """
    stat = select(TraderModel).order_by(TraderModel.id)
    result: Result = await session.execute(stat)
    traders = result.scalars().all()
    return list(traders)


async def get_trader(session: AsyncSession, trader_id: int) -> TraderModel | None:
    """
    Retrieves a trader by ID from the database asynchronously.
    """
    return await session.get(TraderModel, trader_id)


async def create_trader(
    session: AsyncSession, trader_in: TraderCreateSchem
) -> TraderModel:
    """
    Creates a new trader in the database asynchronously.
    """
    trader = TraderModel(**trader_in.dict())
    session.add(trader)
    await session.commit()
    await session.refresh(trader)
    return trader


async def update_trader(
    session: AsyncSession,
    trader: TraderSchem,
    trader_update: TraderUpdateSchem | TraderUpdatePartialSchem,
    partial: bool = False,
) -> TraderSchem:
    """
    PUT and PATCH trader
    """
    for name, value in trader_update.model_dump(exclude_unset=partial).items():
        setattr(trader, name, value)
    await session.commit()
    return trader


async def delete_trader(
    session: AsyncSession,
    trader: TraderSchem,
) -> None:
    """
    Delete trader
    """
    await session.delete(trader)
    await session.commit()
