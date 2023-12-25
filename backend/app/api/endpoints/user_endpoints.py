from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.urls import UserURLS
from app.core.security import get_current_user, pwd_context, create_access_token
from app.db.session import get_db
from app.models.user_models import User, create_user_model, get_user_model_by_username, get_user_schema
from app.schemas.user_schemas import UserCreateSchema, UserLoginSchema, UserSchema, TokenSchema
from app.utils.user_utils import create_preload_data


router = APIRouter()


@router.post(UserURLS.register, status_code=status.HTTP_201_CREATED)
async def user_register(user: UserCreateSchema, db: AsyncSession = Depends(get_db)) -> TokenSchema:
    """
    Эндпоинт регистрации юзера
    """
    username = user.username
    password = user.password

    db_user = await get_user_model_by_username(username, db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Пользователь {username} уже существует")

    hashed_password = pwd_context.hash(password)
    user = await create_user_model(username=username, password=hashed_password, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Произошла неизвестная ошибка")
    access_token = await create_access_token(data={"sub": username})

    # Создаем начальные данные для использования
    await create_preload_data(user.id, db)

    return_data = TokenSchema(
        token=access_token,
        type="bearer",
    )

    return return_data


@router.post(UserURLS.login, status_code=status.HTTP_200_OK)
async def user_login(user: UserLoginSchema, db: Session = Depends(get_db)) -> TokenSchema:
    """
    Логин
    """
    db_user = await get_user_model_by_username(user.username, db)
    if db_user and pwd_context.verify(user.password, db_user.password):
        access_token = await create_access_token(data={"sub": db_user.username})

        return_data = TokenSchema(
            token=access_token,
            type="bearer",
        )

        return return_data

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


@router.get(UserURLS.user_data, status_code=status.HTTP_200_OK)
async def get_private_data(current_user: User = Depends(get_current_user)) -> UserSchema:
    return get_user_schema(current_user)
