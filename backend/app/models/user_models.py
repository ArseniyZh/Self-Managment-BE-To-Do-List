from fastapi import Depends
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship

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


def create_user_model(username: str, password: str, db: Session = Depends(get_db)) -> User:
    db_user = User(username=username, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_model_by_username(username: str, db: Session = Depends(get_db)) -> User:
    db_user = db.query(User).filter(User.username == username).first()
    return db_user


def get_user_schema(user: User) -> UserSchema:
    return Schema(UserSchema, user)
