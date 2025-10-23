from sqlalchemy import Column, String, Text

from app.core.constants import NAME_MAX_LENGTH
from .abstract import CharityDonationAbstractModel


class CharityProject(CharityDonationAbstractModel):
    name = Column(String(NAME_MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)