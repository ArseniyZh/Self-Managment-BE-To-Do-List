import typing

from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.permissions import DeskPermissions, TaskTypePermissions
from app.api.urls import TaskTypeURLS
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.task_type_models import (
    TaskType,
    create_task_type_model,
    get_task_types_by_desk_id,
    edit_task_type_model,
    delete_task_type_model,
    get_task_type_schema,
)
from app.models.user_models import User
from app.schemas.task_type_schemas import (
    CreateTaskTypeSchema,
    EditTaskTypeSchema,
    TaskTypeSchema,
)

router = APIRouter()


@router.post(TaskTypeURLS.create, status_code=status.HTTP_201_CREATED)
@DeskPermissions.desk_belong_to_user
async def task_type_create_endpoint(
    task_type: CreateTaskTypeSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskTypeSchema:
    """
    Эндпоинт для создания типа задачи
    """
    db_task_type: TaskType = await create_task_type_model(data=task_type, db=db)
    return await get_task_type_schema(db_task_type)


@router.get(TaskTypeURLS.list, status_code=status.HTTP_200_OK)
@DeskPermissions.desk_belong_to_user
async def get_task_type_list(
    desk_id: int,
    is_show: typing.Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> typing.List[TaskTypeSchema]:
    task_type_models_list = await get_task_types_by_desk_id(
        desk_id=desk_id, is_show=is_show, db=db
    )
    return task_type_models_list


@router.patch(TaskTypeURLS.edit, status_code=status.HTTP_200_OK)
@TaskTypePermissions.task_type_belong_to_user
async def edit_task_type(
    task_type_id: int,
    data: EditTaskTypeSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    await edit_task_type_model(task_type_id, data, db)
    return {}


@router.delete(TaskTypeURLS.delete, status_code=status.HTTP_200_OK)
@TaskTypePermissions.task_type_belong_to_user
async def delete_task_type(
    task_type_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    await delete_task_type_model(task_type_id, db)
    return {}
