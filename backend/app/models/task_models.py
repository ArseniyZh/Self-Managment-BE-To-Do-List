import typing
from datetime import datetime

from fastapi import Depends
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Session, relationship, joinedload

from app.db.base import Base
from app.db.session import get_db
from app.schemas.base import Schema
from app.schemas.task_schemas import (
    CreateTaskSchema,
    TaskSchema,
    EditTaskSchema
)


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("task_type.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    date_to = Column(DateTime, default=datetime.utcnow)

    type = relationship("TaskType", back_populates="tasks")


def create_task_model(
        data: CreateTaskSchema,
        db: Session = Depends(get_db)
) -> Task:
    db_task = Task(**data.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def get_task_models_list_by_desk_id(desk_id: int, db: Session) -> typing.List[TaskSchema]:
    from app.models.task_type_models import TaskType
    db_tasks = db.query(Task).join(Task.type).filter(TaskType.desk_id == desk_id)
    result_list = [get_task_schema(task) for task in db_tasks]
    return result_list


def edit_task_model(task_id: int, data: EditTaskSchema, db: Session = Depends(get_db)) -> None:
    db_task = get_task_model_by_id(task_id, db)
    if db_task:
        db_task.title = data.title if data.title else db_task.title
        db_task.type_id = data.type_id if data.type_id else db_task.type_id
        db_task.description = data.description if data.description else db_task.description
        db_task.date_to = data.date_to if data.date_to else db_task.date_to
        db.commit()
    return


def delete_task_model(task_id: int, db: Session = Depends(get_db)) -> None:
    db.query(Task).filter(Task.id == task_id).delete()
    db.commit()
    return


def get_task_model_by_id(task_id: int, db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.id == task_id).first()


def check_belong_task_to_user(task_id: int, user_id: int, db: Session = Depends(get_db)):
    db_task = get_task_model_by_id(task_id, db)
    if db_task and db_task.type.desk.user.id == user_id:
        return True
    return False


def get_task_schema(task: Task) -> TaskSchema:
    return Schema(TaskSchema, task)
