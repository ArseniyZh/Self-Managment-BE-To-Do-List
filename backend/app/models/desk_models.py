import typing

from fastapi import Depends
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Session, relationship, joinedload

from app.db.base import Base
from app.db.session import get_db
from app.schemas.base import Schema
from app.schemas.desk_schemas import (
    DeskSchema,
    CreateDeskSchema,
)


class Desk(Base):
    __tablename__ = "desk"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, index=True, nullable=False)

    user = relationship("User", back_populates="desks")
    tasks_types = relationship("TaskType", back_populates="desk")


def create_desk_model(user_id: int, title: str, db: Session = Depends(get_db)) -> Desk:
    db_desk = Desk(title=title, user_id=user_id)
    db.add(db_desk)
    db.commit()
    db.refresh(db_desk)

    return db_desk


def get_desk_models_list_by_user_id(user_id: int, db: Session = Depends(get_db)) -> typing.List[DeskSchema]:
    db_desk_list = db.query(Desk).filter(Desk.user_id == user_id).order_by(Desk.created_at)
    result_list = [
        get_desk_schema(desk) for desk in db_desk_list
    ]
    return result_list


def get_desk_model_by_id(desk_id: int, db: Session = Depends(get_db)) -> Desk:
    db_desk = db.query(Desk).filter(Desk.id == desk_id).first()
    return db_desk


def edit_desk_model(desk_id: int, data: CreateDeskSchema, db: Session = Depends(get_db)) -> None:
    db_desk = db.query(Desk).filter(Desk.id == desk_id).first()
    if db_desk:
        db_desk.title = data.title
        db.commit()
    return


def delete_desk_model_by_id(desk_id: int, db: Session = Depends(get_db)) -> None:
    from app.models.task_models import Task
    db.query(Task).filter(desk_id == desk_id).delete()
    db.query(Desk).filter(Desk.id == desk_id).delete()
    db.commit()
    return


def check_belong_desk_to_user(desk_id: int, user_id: int, db: Session = Depends(get_db)) -> bool:
    db_desk = get_desk_model_by_id(desk_id, db)

    if db_desk and db_desk.user.id == user_id:
        return True
    return False


def get_desk_schema(desk: Desk) -> DeskSchema:
    return Schema(DeskSchema, desk)
