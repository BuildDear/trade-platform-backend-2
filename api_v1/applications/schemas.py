from datetime import datetime
from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel


class ApplicationBaseSchema(BaseModel):
    name: str
    status: str


class ApplicationCreateSchema(ApplicationBaseSchema):
    pass


class ApplicationUpdateSchema(ApplicationBaseSchema):
    pass


class ApplicationUpdatePartialSchema(BaseModel):
    name: str | None = None
    status: Annotated[str, MaxLen(64)] | None = None


class ApplicationSchema(ApplicationBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
