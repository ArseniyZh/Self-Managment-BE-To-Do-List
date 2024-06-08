import typing

from fastapi import Depends
from sqlalchemy import Column, Integer, String, ForeignKey, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.session import get_db
from app.schemas.base import Schema
from app.schemas.desk_schemas import DeskSchema, CreateDeskSchema


class Desk(Base):
    __tablename__ = "desk"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, index=True, nullable=False)

    user = relationship("User", back_populates="desks")
    tasks_types = relationship("TaskType", back_populates="desk")


async def create_desk_model(
    user_id: int, title: str, db: AsyncSession = Depends(get_db)
) -> Desk:
    db_desk = Desk(title=title, user_id=user_id)
    db.add(db_desk)
    await db.commit()
    await db.refresh(db_desk)

    return db_desk


async def get_desk_models_list_by_user_id(
    user_id: int, db: AsyncSession = Depends(get_db)
) -> typing.List[DeskSchema]:
    query = select(Desk).filter(Desk.user_id == user_id).order_by(Desk.created_at)
    result = await db.execute(query)
    db_desk_list = result.fetchall()

    result_list = [await get_desk_schema(desk["Desk"]) for desk in db_desk_list]

    return result_list


async def get_desk_model_by_id(
    desk_id: int, db: AsyncSession = Depends(get_db)
) -> Desk:
    query = select(Desk).filter(Desk.id == desk_id)
    result = await db.execute(query)
    db_desk = result.scalar()
    return db_desk


async def edit_desk_model(
    desk_id: int, data: CreateDeskSchema, db: AsyncSession = Depends(get_db)
) -> None:
    query = select(Desk).filter(Desk.id == desk_id)
    result = await db.execute(query)
    db_desk = result.scalar()
    if db_desk:
        db_desk.title = data.title
        await db.commit()
        await db.refresh(db_desk)
    return


async def delete_desk_model_by_id(
    desk_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    query = delete(Desk).filter(Desk.id == desk_id)
    await db.execute(query)
    await db.commit()
    return


async def check_belong_desk_to_user(
    desk_id: int, user_id: int, db: AsyncSession = Depends(get_db)
) -> bool:
    db_desk = await get_desk_model_by_id(desk_id, db)
    return db_desk and db_desk.user.id == user_id


async def get_desk_schema(desk: Desk) -> DeskSchema:
    return Schema(DeskSchema, desk)
