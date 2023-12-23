import typing

from pydantic import BaseModel

from app.schemas.base import _BaseModel


class TaskTypeSchema(_BaseModel):
    id: int
    desk_id: int
    title: str
    sequence: int
    color: str
    is_show: bool


class CreateTaskTypeSchema(BaseModel):
    desk_id: int
    title: str
    color: str
    sequence: typing.Optional[int]


class EditTaskTypeSchema(BaseModel):
    title: str
    color: str
    sequence: typing.Optional[int]
