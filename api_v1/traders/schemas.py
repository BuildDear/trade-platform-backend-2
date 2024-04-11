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


class TraderBaseSchem(BaseModel):

    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr


class TraderCreateSchem(TraderBaseSchem):
    pass


class TraderUpdateSchem(TraderCreateSchem):
    pass


class TraderUpdatePartialSchem(TraderCreateSchem):
    username: Annotated[str, MinLen(3), MaxLen(20)] | None = None
    email: EmailStr | None = None


class TraderSchem(TraderCreateSchem):

    model_config = ConfigDict(from_attributes=True)
    id: int
