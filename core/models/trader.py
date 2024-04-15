from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base

if TYPE_CHECKING:
    from .application import ApplicationModel


class TraderModel(Base):
    __tablename__ = "traders"

    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    surname: Mapped[str] = mapped_column(String(64), nullable=False)
    applications: Mapped[list["ApplicationModel"] | None] = relationship(
        back_populates="trader",
    )
