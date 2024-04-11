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


class TraderBase(BaseModel):

    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr


class TraderCreate(TraderBase):
    pass


class TraderUpdate(TraderCreate):
    pass


class TraderUpdatePartial(TraderCreate):
    username: Annotated[str, MinLen(3), MaxLen(20)] | None = None
    email: EmailStr | None = None


class Trader(TraderCreate):

    model_config = ConfigDict(from_attributes=True)
    id: int
