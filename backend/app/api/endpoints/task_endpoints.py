import typing

from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.permissions import DeskPermissions, TaskPermissions
from app.api.urls import TaskURLS
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.task_models import (
    Task,
    create_task_model,
    delete_task_model,
    edit_task_model,
    get_task_models_list_by_desk_id,
    get_task_schema,
)
from app.models.user_models import User
from app.schemas.task_schemas import CreateTaskSchema, EditTaskSchema, TaskSchema

router = APIRouter()


@router.post(TaskURLS.create, status_code=status.HTTP_201_CREATED)
@DeskPermissions.desk_belong_to_user
async def task_create_endpoint(
    desk_id: int,
    task: CreateTaskSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskSchema:
    """
    Эндпоинт для создания задачи
    """
    db_task: Task = await create_task_model(data=task, db=db)
    return await get_task_schema(db_task)


@router.get(TaskURLS.list, status_code=status.HTTP_200_OK)
@DeskPermissions.desk_belong_to_user
async def task_list_endpoint(
    desk_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> typing.List[TaskSchema]:
    """
    Эндпоинт для списка задач
    """
    task_models_list = await get_task_models_list_by_desk_id(desk_id=desk_id, db=db)
    return task_models_list


@router.patch(TaskURLS.edit, status_code=status.HTTP_200_OK)
@TaskPermissions.task_belong_to_user
async def task_edit_endpoint(
    task_id: int,
    data: EditTaskSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Эндпоинт для редактирования задачи
    """
    await edit_task_model(task_id, data, db)
    return {}


@router.delete(TaskURLS.delete, status_code=status.HTTP_200_OK)
@TaskPermissions.task_belong_to_user
async def task_delete_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Эндпоинт для удаления задачи
    """
    await delete_task_model(task_id, db)
    return {}
