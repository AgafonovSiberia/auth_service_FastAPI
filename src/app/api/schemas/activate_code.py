from pydantic import BaseModel
import datetime


class CodeBase(BaseModel):
    code: int | None = None
    expire: datetime.datetime | None = None


class ActivateCode(CodeBase):
    id: int | None = None

    class Config:
        orm_mode = True


class ActivateUser(BaseModel):
    id: int
    code: int
