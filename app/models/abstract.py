from datetime import datetime as dt

from sqlalchemy import Column, Integer, DateTime, Boolean

from app.core.constants import DEFAULT_AMOUNT
from app.core.db import Base


class CharityDonationAbstractModel(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=DEFAULT_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=dt.now)
    close_date = Column(DateTime)
