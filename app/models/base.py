from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.config import settings


class AbstractModel():
    """Абстрактная модель для CharityProject и Donation."""
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=settings.default_invested_amount)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
