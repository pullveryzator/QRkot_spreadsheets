from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import User, current_superuser, current_user
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate, DonationFullDB, DonationShortDB
)

donation_router = APIRouter()


@donation_router.get(
    '/',
    response_model=list[DonationFullDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров.

    Возвращает список всех пожертвований."""
    return await donation_crud.get_multi(session)


@donation_router.post(
    '/',
    response_model=DonationShortDB,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """ Сделать пожертвование."""
    return await donation_crud.create(donation, session, user)


@donation_router.get(
    '/my',
    response_model=list[DonationShortDB],
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    return await donation_crud.get_donations_by_user(session, user)
