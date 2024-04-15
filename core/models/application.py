from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


if TYPE_CHECKING:
    from .trader import TraderModel


class StatusEnum(Enum):
    PENDING = "Pending"
    SUCCESS = "Success"


class ApplicationModel(Base):
    __tablename__ = "applications"

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(
        String(64), nullable=False, default=StatusEnum.PENDING
    )
    trader_id: Mapped[int] = mapped_column(ForeignKey("traders.id"), nullable=True)
    trader: Mapped["TraderModel"] = relationship(back_populates="applications")
