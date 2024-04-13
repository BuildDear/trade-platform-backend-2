from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


if TYPE_CHECKING:
    from .trader import TraderModel


class ApplicationModel(Base):
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    trader_id: Mapped[int] = mapped_column(ForeignKey("traders.id"))
    trader: Mapped["TraderModel"] = relationship(back_populates="applications")
