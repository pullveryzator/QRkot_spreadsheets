from datetime import datetime

from sqlalchemy import asc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


def close_object(object):
    object.fully_invested = True
    object.close_date = datetime.now()
    return object


def invest(donation: Donation, project: CharityProject):
    saldo_project = project.full_amount - project.invested_amount
    saldo_donation = donation.full_amount - donation.invested_amount
    amount_to_invest = min(saldo_project, saldo_donation)
    project.invested_amount += amount_to_invest
    donation.invested_amount += amount_to_invest

    if saldo_project > saldo_donation:
        donation = close_object(object=donation)
    elif saldo_project < saldo_donation:
        project = close_object(object=project)
    else:  # saldo_project == saldo_donation
        project = close_object(object=project)
        donation = close_object(object=donation)
    return project, donation


async def add_donation_to_project(
        donation: Donation,
        session: AsyncSession,
):
    result = await session.execute(select(CharityProject).where(
        CharityProject.fully_invested.is_(False),
        CharityProject.close_date.is_(None)
    ).order_by(asc(CharityProject.create_date)))
    project = result.scalars().first()
    if not project:
        session.add(donation)
        return session
    session.add_all(invest(donation, project))
    return session


async def add_project_from_donations(
        project: CharityProject,
        session: AsyncSession,
):
    result = await session.execute(select(Donation).where(
        Donation.fully_invested.is_(False),
        Donation.close_date.is_(None)
    ))
    donations = result.scalars().all()
    if not donations:
        session.add(project)
        return session
    if not project.fully_invested:
        for donation in donations:
            invest(donation, project)
    session.add_all(donations)
    session.add(project)
    return session
