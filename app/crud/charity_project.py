from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.services.investition import close_object
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        project = await session.execute(
            select(CharityProject).where(
                CharityProject.id == obj_id
            )
        )
        return project.scalars().first()

    async def update(
            self,
            project: CharityProject,
            obj_in: CharityProjectUpdate,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(project)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(project, field, update_data[field])
        if project.invested_amount == project.full_amount:
            project = close_object(object=project)
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project

    async def remove(
            self,
            db_obj: CharityProject,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ):
        query_time_delta = (
            func.julianday(CharityProject.close_date)
            - func.julianday(CharityProject.create_date))
        result = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested.is_(True)
            ).order_by(query_time_delta)
        )
        projects = result.scalars().all()
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
