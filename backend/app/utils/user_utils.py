from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.desk_models import Desk, create_desk_model
from app.models.task_models import create_task_model
from app.models.task_type_models import TaskType, create_task_type_model
from app.schemas.task_schemas import CreateTaskSchema
from app.schemas.task_type_schemas import CreateTaskTypeSchema


async def create_preload_data(user_id: int, db: AsyncSession = Depends(get_db)) -> None:
    title = "title"
    color = "color"

    work = "Работа"
    home = "Дом"

    done = "Завершено"
    in_progress = "В работе"
    to_do = "К выполнению"

    done_color = "#7BF96B"
    in_progress_color = "#A7A2FC"
    to_do_color = "#969696"

    desk_data = {
        home: {title: home},
        work: {title: work},
    }
    task_type_data = [
        {title: to_do, color: to_do_color},
        {title: in_progress, color: in_progress_color},
        {title: done, color: done_color},
    ]
    task_data = {
        home: {
            to_do: [{title: "Посидеть с детьми"}],
            in_progress: [{title: "Помыть посуду"}],
            done: [{title: "Прибраться"}],
        },
        work: {
            to_do: [{title: "Завершить сделку"}],
            in_progress: [{title: "Подписать документы"}],
            done: [{title: "Встретиться с начальником"}],
        },
    }

    async def create(_type: str) -> None:
        _desk = desk_data.get(_type)
        db_desk: Desk = await create_desk_model(user_id, _desk.get(title), db)
        desk_id = db_desk.id

        for task_type in task_type_data:
            _desk["desk_id"] = desk_id
            db_task_type: TaskType = await create_task_type_model(
                CreateTaskTypeSchema(desk_id=desk_id, **task_type), db
            )
            for task in task_data.get(_type).get(task_type.get(title)):
                task["type_id"] = db_task_type.id
                await create_task_model(CreateTaskSchema(**task), db)

    await create(home)
    return
