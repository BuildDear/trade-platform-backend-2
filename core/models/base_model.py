from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy declarative models.
    """

    __abstract__ = True  # Indicates that this is an abstract base class

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Generates a default table name based on the class name.
        """
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)
