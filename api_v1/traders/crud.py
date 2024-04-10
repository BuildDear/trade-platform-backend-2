from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.traders.schemas import TraderCreate, Trader


async def get_traders(session: AsyncSession) -> list[Trader]:
    """
    Retrieves all traders from the database asynchronously.

    :param session: Asynchronous session object.
    :return: List of traders retrieved from the database.
    """
    stat = select(Trader, Trader.id).order_by(Trader.id)  # Constructing a SELECT query
    result: Result = await session.execute(stat)  # Executing the query
    traders = result.scalars().all()  # Extracting and converting traders into a list
    return list(traders)


async def get_trader(session: AsyncSession, trader_id: int) -> Trader | None:
    """
    Retrieves a trader by ID from the database asynchronously.

    :param session: Asynchronous session object.
    :param trader_id: ID of the trader to retrieve.
    :return: Retrieved trader object or None if not found.
    """
    return await session.get(Trader, trader_id)  # Retrieving a trader by ID


async def create_trader(session: AsyncSession, trader_in: TraderCreate) -> Trader:
    """
    Creates a new trader in the database asynchronously.

    :param session: Asynchronous session object.
    :param trader_in: Data of the trader to be created.
    :return: Newly created trader object.
    """
    trader = Trader(**trader_in.model_dump())  # Creating a new Trader object
    session.add(trader)  # Adding the new trader to the session
    await session.commit()  # Committing the transaction
    return trader  # Returning the newly created trader object
