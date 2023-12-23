import typing

from datetime import datetime
from pydantic import BaseModel

from app.schemas.base import _BaseModel


class TaskSchema(_BaseModel):
    id: int
    type_id: int
    title: str
    description: typing.Optional[str]
    date_to: typing.Optional[datetime]


class CreateTaskSchema(BaseModel):
    type_id: int
    title: str
    date_to: typing.Optional[datetime]
    description: typing.Optional[str]


class EditTaskSchema(BaseModel):
    title: typing.Optional[str]
    type_id: typing.Optional[int]
    description: typing.Optional[str]
    date_to: typing.Optional[datetime]
