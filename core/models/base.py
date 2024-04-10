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

        :return: Table name as a string.
        """
        return f"{cls.__name__.lower()}s"  # Generates a table name by converting the class name to lowercase and
        # appending 's'

    id: Mapped[int] = mapped_column(
        primary_key=True
    )  # Defines an 'id' column as a primary key
