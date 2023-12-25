from pydantic import BaseModel

from app.schemas.base import _BaseModel


class UserSchema(_BaseModel):
    id: int
    username: str
    password: str


class UserCreateSchema(BaseModel):
    username: str
    password: str


class UserLoginSchema(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    token: str
    type: str
