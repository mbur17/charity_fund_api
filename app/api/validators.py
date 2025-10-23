from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DEFAULT_AMOUNT
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_unique_name(project_name: str, session: AsyncSession) -> None:
    """Проверка названия проекта на уникальность."""
    charity_project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """Проверка существования проекта по id."""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


def check_project_not_closed(fully_invested: bool) -> None:
    """Проверка, что проект ещё не закрыт (не fully_invested)."""
    if fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


def check_new_amount_not_less_than_invested(
    new_amount: int, invested_amount: int
) -> None:
    """Проверка, что требуемая сумма не меньше уже вложенной."""
    if new_amount < invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                'Нелья установить значение full_amount '
                'меньше уже вложенной суммы.'
            )
        )


def check_invested_amount_is_null(invested_amount: int) -> None:
    """Проверка, что в проект еще не проинвестированы стредства."""
    if invested_amount > DEFAULT_AMOUNT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                'В проект были внесены средства, не подлежит удалению!'
            )
        )
