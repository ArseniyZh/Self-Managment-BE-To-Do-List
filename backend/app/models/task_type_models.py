import typing

from fastapi import Depends
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Session, relationship, joinedload

from app.db.base import Base
from app.db.session import get_db
from app.schemas.base import Schema
from app.schemas.task_type_schemas import (
    CreateTaskTypeSchema,
    EditTaskTypeSchema,
    TaskTypeSchema,
)


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


def create_task_type_model(
        data: CreateTaskTypeSchema, db: Session = Depends(get_db)
) -> TaskType:
    db_last_task_type = db.query(TaskType).filter(TaskType.desk_id == data.desk_id).order_by(-TaskType.sequence).first()
    sequence = db_last_task_type.sequence + 1 if db_last_task_type else 0
    data.sequence = sequence
    db_task_type = TaskType(**data.dict())
    db.add(db_task_type)
    db.commit()
    db.refresh(db_task_type)

    return db_task_type


def get_task_type_models_list_by_user_id(
        user_id: int, is_show: typing.Optional[bool] = None, db: Session = Depends(get_db)
) -> typing.List[TaskTypeSchema]:
    db_task_type_list = db.query(TaskType).filter(TaskType.user_id == user_id)

    if is_show is not None:
        db_task_type_list = db_task_type_list.filter(TaskType.is_show == is_show)

    result_list = [get_task_type_schema(task_type) for task_type in db_task_type_list]

    return result_list


def get_task_types_by_desk_id(
        desk_id: int, is_show: typing.Optional[bool] = None, db: Session = Depends(get_db)
) -> typing.List[TaskTypeSchema]:
    db_task_types = db.query(TaskType).filter(TaskType.desk_id == desk_id)

    if is_show is not None:
        db_task_types = db_task_types.filter(TaskType.is_show == is_show)

    result_list = [get_task_type_schema(task_type) for task_type in db_task_types.order_by(TaskType.sequence).all()]

    return result_list


def edit_task_type_model(
        task_type_id: int, data: EditTaskTypeSchema, db: Session = Depends(get_db)
):
    db_task_type = get_task_type_model_by_id(task_type_id, db)
    if db_task_type:
        db_task_type.title = data.title
        db_task_type.color = data.color
        if data.sequence is not None:
            db_task_type.sequence = data.sequence
        db.commit()
    return


def delete_task_type_model(task_type_id: int, db: Session = Depends(get_db)) -> None:
    from . import Task
    db.query(Task).filter(Task.type_id == task_type_id).delete()
    db.query(TaskType).filter(TaskType.id == task_type_id).delete()
    db.commit()
    return


def get_task_type_model_by_id(task_type_id: int, db: Session = Depends(get_db)) -> TaskType:
    return db.query(TaskType).filter(TaskType.id == task_type_id).first()


def check_belong_task_type_to_user(task_type_id: int, user_id: int, db: Session = Depends(get_db)):
    db_task_type = get_task_type_model_by_id(task_type_id, db)
    if db_task_type and db_task_type.desk.user.id == user_id:
        return True
    return False


def get_task_type_schema(task_type: TaskType) -> TaskTypeSchema:
    return Schema(TaskTypeSchema, task_type)
