from functools import wraps

from fastapi import HTTPException, status

from app.models.desk_models import check_belong_desk_to_user
from app.models.task_models import check_belong_task_to_user
from app.models.task_type_models import check_belong_task_type_to_user


class Permissions:
    def __new__(cls, func, *args, **kwargs):
        instance = super().__new__(cls)
        instance = instance(func, *args, **kwargs)
        return instance

    def __call__(self, func, *args, **kwargs):
        self.func = func
        self.current_user = kwargs.get("current_user")
        self.db = kwargs.get("db")

        self.desk = kwargs.get("desk")
        self.task = kwargs.get("task")
        self.task_type = kwargs.get("task_type")

        try:
            if desk_id := kwargs.get("desk_id"):
                self.desk_id = desk_id
            elif desk := self.desk:
                self.desk_id = desk.id
            elif task_type := self.task_type:
                self.desk_id = task_type.desk_id
            else:
                self.desk_id = None
        except AttributeError:
            self.desk_id = None

        try:
            if task_id := kwargs.get("task_id"):
                self.task_id = task_id
            elif task := self.task:
                self.task_id = task.id
            else:
                self.task_id = None
        except AttributeError:
            self.task_id = None

        try:
            if task_type_id := kwargs.get("task_type_id"):
                self.task_type_id = task_type_id
            elif task_type := self.task_type:
                self.task_type_id = task_type.id
            else:
                self.task_type_id = None
        except AttributeError:
            self.task_type_id = None

        return self


class DeskPermissions(Permissions):
    desk_not_belong_to_user_text = "Доска принадлежит другому пользователю"

    @staticmethod
    def desk_belong_to_user(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            _class = DeskPermissions(func, *args, **kwargs)

            user_id = _class.current_user.id
            if not await check_belong_desk_to_user(desk_id=_class.desk_id, user_id=user_id, db=_class.db):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=_class.desk_not_belong_to_user_text)
            return await func(*args, **kwargs)

        return wrapper


class TaskPermissions(Permissions):
    task_not_belong_to_user_text = "Задача принадлежит другому пользователю"

    @staticmethod
    def task_belong_to_user(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            _class = TaskPermissions(func, *args, **kwargs)

            user_id = _class.current_user.id
            if not await check_belong_task_to_user(_class.task_id, user_id, _class.db):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=_class.task_not_belong_to_user_text)
            return await func(*args, **kwargs)

        return wrapper


class TaskTypePermissions(Permissions):
    task_type_not_belong_to_user_text = "Тип задачи принадлежит другому пользователю"

    @staticmethod
    def task_type_belong_to_user(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            _class = TaskTypePermissions(func, *args, **kwargs)

            user_id = _class.current_user.id
            if not await check_belong_task_type_to_user(_class.task_type_id, user_id, _class.db):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail=_class.task_type_not_belong_to_user_text
                )
            return await func(*args, **kwargs)

        return wrapper
