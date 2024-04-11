from sqlalchemy.orm import Mapped, mapped_column

from core import Base


class TraderModel(Base):
    username: Mapped[str]
    email: Mapped[str]
