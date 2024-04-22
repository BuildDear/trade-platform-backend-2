from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import TraderModel


async def query_user_by_email(email: str, db) -> TraderModel:
    """Query user by email"""

    result = await db.execute(select(TraderModel).where(TraderModel.email == email))
    return result.scalars().first()
