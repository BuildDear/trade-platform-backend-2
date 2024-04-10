from typing import Annotated
from annotated_types import (
    MinLen,
    MaxLen,
)
from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict,
)


class TraderCreate(BaseModel):
    """
    Pydantic model for creating a trader.

    This model defines the structure and constraints for creating a trader.
    """

    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr


class Trader(TraderCreate):
    """
    Pydantic model representing a trader.

    This model inherits from TraderCreate and adds an 'id' field.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
