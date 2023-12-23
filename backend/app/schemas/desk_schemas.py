from pydantic import BaseModel

from app.schemas.base import _BaseModel


class DeskSchema(_BaseModel):
    id: int
    title: str
    user_id: int


class CreateDeskSchema(BaseModel):
    title: str
