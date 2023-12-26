from fastapi import Depends
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.session import get_db
from app.schemas.base import Schema
from app.schemas.user_schemas import UserSchema


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    desks = relationship("Desk", back_populates="user")


async def create_user_model(username: str, password: str, db: AsyncSession = Depends(get_db)) -> User:
    db_user = User(username=username, password=password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def get_user_model_by_username(username: str, db: AsyncSession = Depends(get_db)) -> User:
    query = select(User).filter(User.username == username)
    return (await db.execute(query)).scalar()


async def get_user_schema(user: User) -> UserSchema:
    return Schema(UserSchema, user)
