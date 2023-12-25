import typing

from fastapi import Depends
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, exists
from sqlalchemy.orm import Session, relationship, joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, delete

from app.db.base import Base
from app.db.session import get_db
from app.schemas.base import Schema
from app.schemas.task_type_schemas import CreateTaskTypeSchema, EditTaskTypeSchema, TaskTypeSchema


class TaskType(Base):
    __tablename__ = "task_type"

    id = Column(Integer, primary_key=True, index=True)
    desk_id = Column(Integer, ForeignKey("desk.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, index=True, nullable=False)
    sequence = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    is_show = Column(Boolean, default=True)

    desk = relationship("Desk", back_populates="tasks_types")
    tasks = relationship("Task", back_populates="type")


async def create_task_type_model(
        data: CreateTaskTypeSchema, db: AsyncSession = Depends(get_db)
) -> TaskType:
    query = select(TaskType).filter(TaskType.desk_id == data.desk_id).order_by(-TaskType.sequence)
    result = await db.execute(query)

    sequence = 0
    if result := result.scalar():
        sequence = result.sequence + 1
    data.sequence = sequence

    db_task_type = TaskType(**data.dict())
    db.add(db_task_type)
    await db.commit()
    await db.refresh(db_task_type)

    return db_task_type


async def get_task_types_by_desk_id(
        desk_id: int, is_show: typing.Optional[bool] = None, db: AsyncSession = Depends(get_db)
) -> typing.List[TaskTypeSchema]:
    query = select(TaskType).filter(TaskType.desk_id == desk_id)

    if is_show is not None:
        query = query.filter(TaskType.is_show == is_show)

    result = await db.execute(query.order_by(TaskType.sequence))
    db_task_types = result.fetchall()
    result_list = [await get_task_type_schema(task_type["TaskType"]) for task_type in db_task_types]

    return result_list


async def edit_task_type_model(
        task_type_id: int, data: EditTaskTypeSchema, db: AsyncSession = Depends(get_db)
) -> None:
    db_task_type = await get_task_type_model_by_id(task_type_id, db)

    if db_task_type:
        db_task_type.title = data.title
        db_task_type.color = data.color
        if data.sequence is not None:
            db_task_type.sequence = data.sequence
        await db.commit()
        await db.refresh(db_task_type)

    return


async def delete_task_type_model(task_type_id: int, db: AsyncSession = Depends(get_db)) -> None:
    query = delete(TaskType).filter(TaskType.id == task_type_id)
    await db.execute(query)
    await db.commit()
    return


async def get_task_type_model_by_id(task_type_id: int, db: AsyncSession = Depends(get_db)) -> TaskType:
    from . import Desk, User

    query = (
        select(TaskType)
        .options(
            selectinload(TaskType.desk)
            .selectinload(Desk.user)
        )
        .join(Desk, TaskType.desk_id == Desk.id)
        .join(User, Desk.user_id == User.id)
        .filter(TaskType.id == task_type_id)
    )

    return (await db.execute(query)).scalar()


async def check_belong_task_type_to_user(task_type_id: int, user_id: int, db: AsyncSession = Depends(get_db)) -> bool:
    from . import Desk
    subquery = (
        select(exists()
               .where((TaskType.id == task_type_id) &
                      (TaskType.desk_id == Desk.id) &
                      (Desk.user_id == user_id)))
    )

    return (await db.execute(subquery)).scalar()


async def get_task_type_schema(task_type: TaskType) -> TaskTypeSchema:
    return Schema(TaskTypeSchema, task_type)
