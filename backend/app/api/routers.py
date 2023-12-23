from fastapi import APIRouter

from app.api.endpoints import user_endpoints, desk_endpoints, task_type_endpoints, task_endpoints
from app.api.urls import UserURLS, DeskURLS, TaskTypeURLS, TaskURLS

router = APIRouter()

router.include_router(user_endpoints.router, prefix=UserURLS.base_url, tags=["user"])
router.include_router(desk_endpoints.router, prefix=DeskURLS.base_url, tags=["desc"])
router.include_router(task_type_endpoints.router, prefix=TaskTypeURLS.base_url, tags=["task_type"])
router.include_router(task_endpoints.router, prefix=TaskURLS.base_url, tags=["task"])
