import typing
from datetime import datetime

from fastapi import Depends
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy.sql import select, delete

from app.db.base import Base
from app.db.session import get_db
from app.schemas.base import Schema
from app.schemas.task_schemas import CreateTaskSchema, TaskSchema, EditTaskSchema


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(
        Integer, ForeignKey("task_type.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    date_to = Column(DateTime, default=datetime.utcnow)

    type = relationship("TaskType", back_populates="tasks")


async def create_task_model(
    data: CreateTaskSchema, db: AsyncSession = Depends(get_db)
) -> Task:
    db_task = Task(**data.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)

    return db_task


async def get_task_models_list_by_desk_id(
    desk_id: int, db: AsyncSession = Depends(get_db)
) -> typing.List[TaskSchema]:
    from . import TaskType

    db.expire_all()

    query = (
        select(Task)
        .join(TaskType, TaskType.id == Task.type_id)
        .filter(TaskType.desk_id == desk_id)
    )

    result = await db.execute(query)
    db_tasks = result.fetchall()

    result_list = [await get_task_schema(task["Task"]) for task in db_tasks]
    return result_list


async def edit_task_model(
    task_id: int, data: EditTaskSchema, db: AsyncSession = Depends(get_db)
) -> None:
    db.expire_all()
    db_task = await get_task_model_by_id(task_id, db)

    if db_task:
        db_task.title = data.title if data.title else db_task.title
        db_task.type_id = data.type_id if data.type_id else db_task.type_id
        db_task.description = (
            data.description if data.description else db_task.description
        )
        db_task.date_to = data.date_to if data.date_to else db_task.date_to
        await db.commit()
        await db.refresh(db_task)

    return


async def delete_task_model(task_id: int, db: AsyncSession = Depends(get_db)) -> None:
    query = delete(Task).filter(Task.id == task_id)
    await db.execute(query)
    await db.commit()
    return


async def get_task_model_by_id(
    task_id: int, db: AsyncSession = Depends(get_db)
) -> Task:
    from . import TaskType, Desk, User

    query = (
        select(Task)
        .options(
            selectinload(Task.type).selectinload(TaskType.desk).selectinload(Desk.user)
        )
        .join(TaskType, Task.type_id == TaskType.id)
        .join(Desk, TaskType.desk_id == Desk.id)
        .join(User, Desk.user_id == User.id)
        .filter(Task.id == task_id)
    )

    return (await db.execute(query)).scalar()


async def check_belong_task_to_user(
    task_id: int, user_id: int, db: AsyncSession = Depends(get_db)
) -> bool:
    from . import TaskType, Desk

    subquery = select(
        exists().where(
            (Task.id == task_id)
            & (Task.type_id == TaskType.id)
            & (TaskType.desk_id == Desk.id)
            & (Desk.user_id == user_id)
        )
    )

    return (await db.execute(subquery)).scalar()


async def get_task_schema(task: Task) -> TaskSchema:
    return Schema(TaskSchema, task)
