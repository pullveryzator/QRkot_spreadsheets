from fastapi import APIRouter

from app.api.endpoints import user_router
from app.api.endpoints.charity_project import charity_project_router
from app.api.endpoints.donation import donation_router

main_router = APIRouter()
main_router.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['charity projects']
)
main_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['donations']
)
main_router.include_router(user_router)
