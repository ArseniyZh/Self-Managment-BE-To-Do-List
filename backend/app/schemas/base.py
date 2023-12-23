import typing
from datetime import datetime
from pydantic import BaseModel


class _BaseModel(BaseModel):
    created_at: datetime
    updated_at: datetime


class BaseReturnSchema(BaseModel):
    message: str
    data: typing.Any


class Schema:
    def __new__(cls, *args, **kwargs):
        schema = None
        obj = None

        if len(args) >= 1:
            schema = args[0]
        if len(args) >= 2:
            obj = args[1]

        schema = schema if schema else kwargs.get("schema")
        obj = obj if obj else kwargs.get("obj")

        if not schema and not obj:
            raise AttributeError("Необходимо передать схему и объект")

        properties_keys = schema.schema().get("properties").keys()

        fields = {}
        for field in dir(obj):
            if field in properties_keys:
                fields[field] = eval(f"obj.{field}")

        if not fields:
            return {}
        return schema(**fields)
