from datetime import datetime
from typing import Annotated, List
from pydantic import BaseModel, EmailStr, ConfigDict
from annotated_types import MinLen, MaxLen

from api_v1.applications.schemas import ApplicationCreateSchema


class TraderBaseSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    email: EmailStr
    password: bytes
    name: Annotated[str, MinLen(1), MaxLen(64)]
    surname: Annotated[str, MinLen(1), MaxLen(64)]
    active: bool = True


class TraderCreateSchema(TraderBaseSchema):
    pass


class TraderUpdateSchema(TraderBaseSchema):
    pass


class TraderUpdatePartialSchema(TraderCreateSchema):
    email: EmailStr | None = None
    name: Annotated[str, MinLen(1), MaxLen(64)] | None = None
    surname: Annotated[str, MinLen(1), MaxLen(64)] | None = None
    application_ids: List[ApplicationCreateSchema] | None = None


class TraderSchema(TraderBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
