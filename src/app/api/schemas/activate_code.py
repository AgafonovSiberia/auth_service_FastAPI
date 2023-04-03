import datetime
from uuid import UUID

from pydantic import BaseModel


class CodeBase(BaseModel):
    code: str | None = None
    expire: datetime.datetime | None = None


class ActivateCode(CodeBase):
    user_id: UUID | None = None

    class Config:
        orm_mode = True


class ActivateUser(BaseModel):
    user_id: UUID
    code: str
