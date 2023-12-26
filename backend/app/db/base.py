from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: int
    created_at: DateTime
    updated_at: DateTime

    @declared_attr
    def created_at(self):
        return Column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def updated_at(self):
        return Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
