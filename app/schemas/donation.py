from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt, Field

from app.core.config import settings


class DonationBase(BaseModel):
    full_amount: PositiveInt = Field(
        ...,
        example=settings.donation_full_amount_example
    )
    comment: Optional[str] = Field(
        None,
        example=settings.donation_comment_example
    )

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationFullDB(DonationDB):
    user_id: int
    invested_amount: int = Field(settings.default_invested_amount)
    fully_invested: bool = Field(False)
    close_date: Optional[datetime]


class DonationShortDB(DonationDB):
    pass
