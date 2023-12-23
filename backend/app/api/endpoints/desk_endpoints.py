import typing

from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

from app.api.urls import DeskURLS, TaskTypeURLS, TaskURLS
from app.api.permissions import DeskPermissions
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user_models import User
from app.models.desk_models import (
    Desk,
    create_desk_model,
    get_desk_models_list_by_user_id,
    get_desk_schema,
    edit_desk_model,
    delete_desk_model_by_id,
    check_belong_desk_to_user,
)
from app.schemas.desk_schemas import CreateDeskSchema, DeskSchema


router = APIRouter()


@router.post(DeskURLS.create, status_code=status.HTTP_201_CREATED)
def desk_create_endpoint(
        desk: CreateDeskSchema,
        current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> DeskSchema:
    """
    Эндпоинт на создание доски
    """
    db_desk: Desk = create_desk_model(user_id=current_user.id, title=desk.title, db=db)
    return get_desk_schema(db_desk)


@router.get(DeskURLS.list, status_code=status.HTTP_200_OK)
def desk_list_endpoint(
        current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> typing.List[DeskSchema]:
    """
    Эндпоинт на получение списка досок по user_id
    """
    desk_models_list = get_desk_models_list_by_user_id(user_id=current_user.id, db=db)
    return desk_models_list


@router.patch(DeskURLS.edit, status_code=status.HTTP_200_OK)
@DeskPermissions.desk_belong_to_user
def desk_edit_endpoint(
        desk_id: int, desk: CreateDeskSchema,
        current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
) -> dict:
    """
    Эндпоинт для редактирования доски
    """
    edit_desk_model(desk_id, desk, db)
    return {}


@router.delete(DeskURLS.delete, status_code=status.HTTP_200_OK)
@DeskPermissions.desk_belong_to_user
def desk_delete_endpoint(
        desk_id: int,
        current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    """
    Эндпоинт для удаления доски
    """
    delete_desk_model_by_id(desk_id, db)
    return {}
