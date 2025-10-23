from sqlalchemy import Column, ForeignKey, Integer, Text

from .abstract import CharityDonationAbstractModel


class Donation(CharityDonationAbstractModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
