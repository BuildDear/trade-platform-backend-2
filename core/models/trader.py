from sqlalchemy import String, Column, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core import Base

class TraderModel(Base):
    __tablename__ = 'traders'

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    surname: Mapped[str] = mapped_column(String(255), nullable=False)

    __table_args__ = (UniqueConstraint('email', name='_email_uc'),)
