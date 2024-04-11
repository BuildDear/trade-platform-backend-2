from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.traders.schemas import TraderCreate, Trader
from core import TraderModel


async def get_traders(session: AsyncSession) -> list[TraderModel]:
    """
    Retrieves all traders from the database asynchronously.
    """
    stat = select(TraderModel).order_by(TraderModel.id)
    result: Result = await session.execute(stat)
    traders = result.scalars().all()
    return list(traders)


async def get_trader(session: AsyncSession, trader_id: int) -> Trader | None:
    """
    Retrieves a trader by ID from the database asynchronously.
    """
    return await session.get(Trader, trader_id)


async def create_trader(session: AsyncSession, trader_in: TraderCreate) -> TraderModel:
    """
    Creates a new trader in the database asynchronously.
    """
    trader = TraderModel(**trader_in.dict())
    session.add(trader)
    await session.commit()
    await session.refresh(trader)
    return trader
