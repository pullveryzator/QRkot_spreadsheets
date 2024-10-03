from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.models.base import AbstractModel
from app.core.config import settings


class CharityProject(Base, AbstractModel):
    name = Column(String(
        settings.max_project_name_length),
        unique=True,
        nullable=False
    )
    description = Column(Text, nullable=False)
