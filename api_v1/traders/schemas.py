from typing import Annotated
from pydantic import BaseModel, EmailStr
from annotated_types import MinLen, MaxLen


class TraderBaseSchema(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(64)]
    name: Annotated[str, MinLen(1), MaxLen(64)]
    surname: Annotated[str, MinLen(1), MaxLen(64)]


class TraderCreateSchema(TraderBaseSchema):
    pass


class TraderUpdateSchema(TraderBaseSchema):
    pass


class TraderUpdatePartialSchema(BaseModel):
    email: EmailStr | None = None
    password: Annotated[str, MinLen(8), MaxLen(64)] | None = None
    name: Annotated[str, MinLen(1), MaxLen(64)] | None = None
    surname: Annotated[str, MinLen(1), MaxLen(64)] | None = None


class TraderSchema(TraderBaseSchema):
    id: int
