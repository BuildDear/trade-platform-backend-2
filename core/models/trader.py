from sqlalchemy.orm import Mapped

from .base import Base


class Trader(Base):
    name: Mapped[str]
