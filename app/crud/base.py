from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models import User
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.services.investition import (
    add_donation_to_project, add_project_from_donations
)
from app.core.config import settings


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        obj_in_data['invested_amount'] = settings.default_invested_amount
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        if isinstance(db_obj, Donation):
            session = await add_donation_to_project(db_obj, session)
        elif isinstance(db_obj, CharityProject):
            session = await add_project_from_donations(db_obj, session)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
