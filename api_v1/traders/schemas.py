from typing import Annotated
from pydantic import BaseModel, EmailStr
from annotated_types import MinLen, MaxLen


class TraderBaseSchem(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(64)]
    name: Annotated[str, MinLen(1), MaxLen(64)]
    surname: Annotated[str, MinLen(1), MaxLen(64)]


class TraderCreateSchem(TraderBaseSchem):
    pass


class TraderUpdateSchem(TraderBaseSchem):
    pass


class TraderUpdatePartialSchem(BaseModel):
    email: EmailStr | None = None
    password: Annotated[str, MinLen(8), MaxLen(64)] | None = None
    name: Annotated[str, MinLen(1), MaxLen(64)] | None = None
    surname: Annotated[str, MinLen(1), MaxLen(64)] | None = None


class TraderSchem(TraderBaseSchem):
    id: int
