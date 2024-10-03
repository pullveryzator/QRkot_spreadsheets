from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.config import settings


class CharityProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=settings.min_project_name_length,
        max_length=settings.max_project_name_length,
        example=settings.project_name_example
    )
    description: str = Field(
        ...,
        min_length=settings.min_project_description_length,
        example=settings.project_description_example
    )
    full_amount: PositiveInt = Field(
        ...,
        example=settings.project_full_amount_example
    )

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=settings.min_project_name_length,
        max_length=settings.max_project_name_length
    )
    description: Optional[str] = Field(
        None,
        min_length=settings.min_project_description_length
    )
    full_amount: Optional[PositiveInt] = settings.default_invested_amount

    class Config:
        orm_mode = True
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
