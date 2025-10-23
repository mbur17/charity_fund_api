from typing import Optional, Union

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self, project_name: str, session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id)
            .where(CharityProject.name == project_name)
        )
        return db_project_id.scalars().first()

    async def get_open_projects(
        self, session: AsyncSession
    ) -> list[CharityProject]:
        open_projects = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        return open_projects.scalars().all()

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> list[dict[str, Union[str, float]]]:
        fundraise_time = (
            func.julianday(self.model.close_date) -
            func.julianday(self.model.create_date)
        )
        closed_projects_sorted = await session.execute(
            select(
                self.model.name,
                self.model.description,
                fundraise_time
            )
            .where(self.model.fully_invested.is_(True))
            .order_by(fundraise_time)
        )
        closed_projects_sorted = closed_projects_sorted.all()
        return [
            {
                'name': name,
                'duration': duration,
                'description': description
            }
            for name, description, duration in closed_projects_sorted
        ]


charity_project_crud = CRUDCharityProject(CharityProject)
