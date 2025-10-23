from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):

    async def get_user_donations(
        self, user_id: int, session: AsyncSession
    ) -> list[Donation]:
        user_donations = await session.execute(
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.create_date)
        )
        return user_donations.scalars().all()

    async def get_open_donations(
        self, session: AsyncSession
    ) -> list[Donation]:
        open_donations = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        return open_donations.scalars().all()


donation_crud = CRUDDonation(Donation)
