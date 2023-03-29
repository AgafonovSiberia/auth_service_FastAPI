from uuid import UUID

from pydantic import BaseModel
import datetime


class CodeBase(BaseModel):
    code: str | None = None
    expire: datetime.datetime | None = None


class ActivateCode(CodeBase):
    id: str | None = None

    class Config:
        orm_mode = True


class ActivateUser(BaseModel):
    id: UUID
    code: str
